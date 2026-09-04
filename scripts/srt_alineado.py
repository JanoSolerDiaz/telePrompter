"""`.srt` alineado con la toma buena (tarea R-05).

Cierra la promesa que `references/contrato-montaje.md` (T-33) ya dejaba anotada
como trabajo futuro: el `guion.srt` de `srt.py` (T-27) es un borrador con
tiempos ESTIMADOS a partir del ritmo deducido del guion (T-12), no del tiempo
real de la toma que se grabo de verdad. Con el registro de tomas de R-02 ya
disponible en `estado.tomas`, este modulo reescala los bloques de cada escena a
la duracion real de su toma marcada `buena`, para que el montaje empiece con
subtitulos casi finales en vez de con una aproximacion que hay que rehacer
entera.

Este modulo no calcula tiempos por su cuenta (misma disciplina que `srt.py`
respecto a T-12, requisito 4 de T-12): parte del `ResultadoTiempos` ya
calculado -- idealmente el de una revalidacion (`revalidacion.revalidar_guion`),
para que el texto sea el locutado final con las reescrituras aceptadas ya
materializadas, mismo criterio que T-27 -- y solo REESCALA los tiempos que ya
trae, nunca inventa uno nuevo. La duracion real de cada escena sale de
`tomas.duracion_toma_buena` (R-02, promovida a publica en esta tarea para que
R-04 y R-05 compartan el mismo criterio): la de la toma marcada `buena`, `None`
si la escena todavia no tiene ninguna marcada asi.

Requisito 1 (reescalar a la duracion real): `reescalar_a_toma_buena` recorre
las escenas del guion en orden y, para cada una con toma buena registrada,
multiplica la duracion de palabras y la pausa de cada uno de sus bloques por
`duracion_real / duracion_estimada` -- el mismo factor para todo el bloque, asi
que el reparto relativo entre bloques (mas pausa tras una coma que tras una
palabra suelta) se conserva, solo cambia la escala. Una escena sin toma buena
todavia conserva su duracion ESTIMADA sin tocar (factor 1.0): mezclar un tiempo
inventado con el resto de tiempos reales habria sido peor que dejarlo estimado
y decirlo (honestidad, mismo criterio que R-04). El cursor de tiempo se
acumula de forma continua escena a escena, igual que hace `tiempos.py`, asi
que el resultado sigue siendo una unica linea de tiempo sin huecos ni solapes
aunque unas escenas esten alineadas y otras todavia no.

Requisito 2 (el .srt estimado sigue siendo una salida independiente): este
modulo nunca sobrescribe `NOMBRE_ARCHIVO_SRT` (T-27) -- `guardar_srt_alineado`
escribe en `NOMBRE_ARCHIVO_SRT_ALINEADO`, un archivo distinto en la misma
carpeta de salida. Generar el alineado no requiere volver a generar el
estimado ni viceversa.

Requisito 3 (mismas reglas estrictas de validacion que T-27): la generacion de
entradas y el formato reutilizan `srt.generar_entradas_srt`/`srt.formatear_srt`
tal cual -- ninguna logica de agrupacion o particion limpia se duplica aqui --,
y la validacion reutiliza `srt.validar_srt` sin cambios. El `ResultadoTiempos`
reescalado que produce este modulo es, para esas dos funciones, indistinguible
de cualquier otro `ResultadoTiempos`: no necesitan saber que sus tiempos vienen
de una toma real en vez de una estimacion.

Criterio de aceptacion (tolerancia documentada): con una toma real
cronometrada, la duracion total de la escena alineada coincide con
`duracion_segundos` de esa toma dentro de
`Configuracion.srt_alineado_tolerancia_segundos` -- el reescalado en si es
exacto en coma flotante, la tolerancia cubre solo el redondeo a milisegundos
que introduce `srt.formatear_marca_tiempo` al serializar.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from config import NOMBRE_ARCHIVO_SRT_ALINEADO, Configuracion
from srt import formatear_srt, generar_entradas_srt, validar_srt
from tiempos import BloqueConTiempo, ResultadoTiempos, TiempoEscena
from tomas import duracion_toma_buena

# Se reexporta para que quien valide un .srt alineado no tenga que importar de
# `srt.py` aparte (mismo modulo, mismas reglas, requisito 3).
validar_srt_alineado = validar_srt


@dataclass(frozen=True)
class ResultadoAlineacion:
    """Salida de `reescalar_a_toma_buena`: el `ResultadoTiempos` ya reescalado
    mas que escenas tienen evidencia real y cuales siguen en estimada, para que
    quien informe al dueno pueda decirlo con honestidad (nunca en silencio)."""

    resultado_tiempos: ResultadoTiempos
    escenas_alineadas: tuple[int, ...]
    escenas_sin_toma_buena: tuple[int, ...]


def _bloques_por_escena(bloques: list[BloqueConTiempo]) -> dict[int, list[BloqueConTiempo]]:
    agrupado: dict[int, list[BloqueConTiempo]] = {}
    for bloque_con_tiempo in bloques:
        agrupado.setdefault(bloque_con_tiempo.bloque.numero_escena, []).append(bloque_con_tiempo)
    return agrupado


def reescalar_a_toma_buena(
    resultado_tiempos: ResultadoTiempos, tomas_por_escena: dict[str, Any]
) -> ResultadoAlineacion:
    """Reescala cada escena a la duracion real de su toma buena (requisito 1).

    `tomas_por_escena` es `EstadoProyecto.tomas` tal cual (claves de escena en
    texto, ver `references/contrato-tomas.md`) -- el mismo contenedor que
    consume `calibracion.py` (R-04). Una escena sin toma buena conserva su
    duracion estimada intacta (factor 1.0) y se reporta en
    `escenas_sin_toma_buena`, nunca se estima ni se inventa un tiempo real que
    no existe todavia.
    """
    bloques_por_escena = _bloques_por_escena(resultado_tiempos.bloques)
    bloques_alineados: list[BloqueConTiempo] = []
    escenas_alineadas: list[int] = []
    escenas_sin_toma_buena: list[int] = []
    escenas_tiempo: list[TiempoEscena] = []
    cursor_segundos = 0.0

    for tiempo_escena in resultado_tiempos.escenas:
        bloques_escena = bloques_por_escena.get(tiempo_escena.numero, [])
        duracion_real = duracion_toma_buena(
            tomas_por_escena.get(str(tiempo_escena.numero)), tiempo_escena.numero
        )
        estimada = tiempo_escena.duracion_estimada_segundos
        if duracion_real is not None and duracion_real > 0:
            escenas_alineadas.append(tiempo_escena.numero)
            factor = duracion_real / estimada if estimada > 0 else 1.0
        else:
            escenas_sin_toma_buena.append(tiempo_escena.numero)
            factor = 1.0

        inicio_escena = cursor_segundos
        for bloque_con_tiempo in bloques_escena:
            duracion_palabras_segundos = bloque_con_tiempo.duracion_palabras_segundos * factor
            pausa_segundos = bloque_con_tiempo.pausa_segundos * factor
            bloques_alineados.append(
                BloqueConTiempo(
                    bloque=bloque_con_tiempo.bloque,
                    inicio_segundos=cursor_segundos,
                    duracion_palabras_segundos=duracion_palabras_segundos,
                    tipo_pausa=bloque_con_tiempo.tipo_pausa,
                    pausa_segundos=pausa_segundos,
                )
            )
            cursor_segundos += duracion_palabras_segundos + pausa_segundos

        escenas_tiempo.append(
            TiempoEscena(
                numero=tiempo_escena.numero,
                duracion_estimada_segundos=cursor_segundos - inicio_escena,
                duracion_objetivo_segundos=tiempo_escena.duracion_objetivo_segundos,
                aviso=tiempo_escena.aviso,
            )
        )

    resultado_alineado = ResultadoTiempos(
        ritmo=resultado_tiempos.ritmo,
        bloques=bloques_alineados,
        escenas=escenas_tiempo,
        duracion_total_segundos=cursor_segundos,
        duracion_objetivo_total_segundos=resultado_tiempos.duracion_objetivo_total_segundos,
        aviso_total=resultado_tiempos.aviso_total,
    )
    return ResultadoAlineacion(
        resultado_tiempos=resultado_alineado,
        escenas_alineadas=tuple(escenas_alineadas),
        escenas_sin_toma_buena=tuple(escenas_sin_toma_buena),
    )


def exportar_srt_alineado(
    resultado_alineacion: ResultadoAlineacion, configuracion: Configuracion | None = None
) -> str:
    """Genera el contenido completo del `.srt` alineado: reutiliza tal cual la
    agrupacion, particion limpia y formato de `srt.py` (requisito 3) sobre el
    `ResultadoTiempos` ya reescalado."""
    configuracion = configuracion or Configuracion()
    entradas = generar_entradas_srt(resultado_alineacion.resultado_tiempos, configuracion)
    return formatear_srt(entradas)


def guardar_srt_alineado(
    contenido: str, carpeta_salida: Path, configuracion: Configuracion | None = None
) -> Path:
    """Escribe el `.srt` alineado en la carpeta de salida del guion, en un
    archivo distinto del `.srt` estimado (requisito 2, `NOMBRE_ARCHIVO_SRT_ALINEADO`
    != `NOMBRE_ARCHIVO_SRT`): nunca fuera de `carpeta_salida` (regla de
    aislamiento, §0.2)."""
    configuracion = configuracion or Configuracion()
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    destino = carpeta_salida / NOMBRE_ARCHIVO_SRT_ALINEADO
    codificacion = "utf-8-sig" if configuracion.srt_con_bom else "utf-8"
    destino.write_text(contenido, encoding=codificacion, newline="\n")
    return destino


def generar_srt_alineado(
    resultado_tiempos: ResultadoTiempos,
    tomas_por_escena: dict[str, Any],
    configuracion: Configuracion | None = None,
) -> tuple[str, ResultadoAlineacion]:
    """Punto de entrada de R-05: reescala (requisito 1) y exporta (requisito 3)
    en un solo paso. La skill no la invoca sola: es Claude quien reune el
    `ResultadoTiempos` (idealmente de una revalidacion) y `EstadoProyecto.tomas`
    ya fusionado por R-02, y llama a esta funcion dentro de la sesion cuando el
    dueno entrega un parte de rodaje con al menos una toma buena -- mismo
    patron que `calibracion.calcular_calibracion` (R-04) y
    `salidas.generar_salidas_seleccionadas` (T-30)."""
    configuracion = configuracion or Configuracion()
    resultado_alineacion = reescalar_a_toma_buena(resultado_tiempos, tomas_por_escena)
    contenido = exportar_srt_alineado(resultado_alineacion, configuracion)
    return contenido, resultado_alineacion
