"""Encadenar los comandos `ffmpeg` reales de montaje para un guion concreto (tarea R-30).

`references/contrato-montaje.md` (T-33) documenta con precision que archivos deja
preparados esta skill (`guion.srt`/`guion-alineado.srt`, `tarjetas.json`,
`concat-ffmpeg.txt`, `capitulos-ffmpeg.txt`) y da, como ilustracion, fragmentos de
comando `ffmpeg` sueltos con nombres de archivo de ejemplo (`video.mp4`,
`video-final.mp4`): uno para concatenar (R-19) y otro para incrustar capitulos
(R-22), cada uno aislado, sin encadenar, y sin ningun paso de subtitulos. El dueno,
formador en solitario sin equipo de produccion, tenia que traducir el a mano esa
documentacion de referencia a comandos ejecutables cada vez que terminaba de grabar.
Este modulo cierra ese ultimo tramo: construye la secuencia real de 1 a 3 comandos
`ffmpeg` -- concatenar las tomas buenas, anadir subtitulos, incrustar capitulos --
con los nombres de archivo REALES de la carpeta de salida de este guion, la salida
de cada paso literalmente la entrada del siguiente.

Decisiones de diseno (detalle completo en `DECISIONES_TECNICAS.md`):

- **Documento, no script ejecutado por la skill** (mismo patron que
  `convencion.generar_convencion_guiones`, R-25): texto para que el dueno copie y
  pegue, nunca una invocacion real de `ffmpeg`/subproceso. Este modulo no gana
  ninguna dependencia nueva ni ejecuta nada (§0.2: cero red, runtime solo biblioteca
  estandar).
- **Pura funcion de lo que las piezas ya calculadas producirian**, nunca relee del
  disco lo que otras salidas ya escribieron: reutiliza tal cual
  `concat_ffmpeg.calcular_lista_concat_ffmpeg` (R-19), `srt_alineado.generar_srt_alineado`
  (R-05) y `capitulos_youtube.generar_capitulos_youtube`/`formatear_capitulos_ffmpeg`
  (R-07/R-22) -- las mismas tres condiciones que ya deciden si `concat-ffmpeg.txt`,
  `guion-alineado.srt` y `capitulos-ffmpeg.txt` existirian en esta misma pasada de
  `scripts/salidas.py` (generacion independiente, T-30 requisito 3), sin
  reimplementar ninguna de las tres.
- **El paso 1 (concatenacion) decide si hay algo real que montar todavia**: sin el
  (ningun parte de rodaje registrado, mismo caso que deja `concat-ffmpeg.txt` sin
  generar), no hay nada mas que encadenar -- `motivo_sin_generar` explicito, nunca
  un documento con pasos inventados.
- **Subtitulos como pista blanda (`mov_text`) por defecto**, con la alternativa
  incrustada ("quemada") como comentario explicito, nunca como comando activo:
  quemar subtitulos exige recodificar video, una pista blanda es reversible y de
  copia directa (`-c copy`), coherente con que ningun otro paso de la cadena
  recodifica tampoco.
- **`guion-alineado.srt` si al menos una escena esta alineada con su toma buena, si
  no `guion.srt`** (mismo criterio que `references/contrato-montaje.md` y
  `salidas._generar_srt`).
- **Los capitulos son el unico paso realmente opcional**: sin seccion `Capitulos` en
  el guion, la cadena se detiene en el paso de subtitulos y lo dice explicitamente
  en el documento generado -- nunca inventa un paso con un archivo que no existe.

Requisito 5 (regenerable sin intervencion manual, fuera de alcance explicito): este
modulo no ejecuta `ffmpeg` ni comprueba que este instalado, no anade recodificacion,
normalizacion de audio, cortes ni transiciones, y no cambia ninguna regla de
`concat_ffmpeg.py`, `srt.py`/`srt_alineado.py` ni `capitulos_youtube.py` en si.

R-31 cierra la grieta que abre la propia independencia de generacion de este modulo:
como `calcular_comandos_montaje` es una funcion pura de `tomas_por_escena` (nunca relee
del disco), el documento se genera igual si el dueno selecciona SOLO `COMANDOS_MONTAJE`
sin tambien `CONCAT_FFMPEG`/`SRT`/`CAPITULOS_YOUTUBE`, citando esos tres archivos por su
nombre fijo aunque no existan todavia en la carpeta de salida. Con `carpeta_salida`
(parametro opcional, comprobacion de EXISTENCIA en disco, nunca de contenido -- eso ya
lo hacen los validadores propios de cada salida en su propia ruta de generacion, R-21/
R-28), cada archivo ausente gana una nota visible al principio del documento citando la
opcion exacta del selector que hay que marcar -- nunca bloquea ni degrada la generacion.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from capitulos_youtube import formatear_capitulos_ffmpeg, generar_capitulos_youtube
from concat_ffmpeg import EscenaPendiente, calcular_lista_concat_ffmpeg
from config import (
    DESCRIPCION_OPCION_CAPITULOS_YOUTUBE,
    DESCRIPCION_OPCION_CONCAT_FFMPEG,
    DESCRIPCION_OPCION_SRT,
    NOMBRE_ARCHIVO_CAPITULOS_FFMPEG,
    NOMBRE_ARCHIVO_COMANDOS_MONTAJE,
    NOMBRE_ARCHIVO_CONCAT_FFMPEG,
    NOMBRE_ARCHIVO_SRT,
    NOMBRE_ARCHIVO_SRT_ALINEADO,
    Configuracion,
)
from parser import ResultadoParseo
from srt_alineado import generar_srt_alineado
from tiempos import ResultadoTiempos

_MOTIVO_SIN_RODAJE = "aún no hay ningún parte de rodaje con una toma buena."


@dataclass(frozen=True)
class PasoComandoMontaje:
    """Un paso de la cadena: su explicacion de una frase (requisito 2) y el
    comando `ffmpeg` listo para copiar. `comentario_alternativo`, si no es
    `None`, es una alternativa documentada pero nunca el comando activo
    (p. ej. subtitulos incrustados en vez de pista blanda)."""

    descripcion: str
    comando: str
    comentario_alternativo: str | None = None


@dataclass(frozen=True)
class ArchivoReferenciadoFaltante:
    """Un archivo que los comandos citan por su nombre pero que todavia no
    existe en la carpeta de salida (R-31): el dueno no selecciono tambien esa
    opcion del selector en esta misma pasada, ni en ninguna anterior."""

    nombre_archivo: str
    descripcion_opcion: str


@dataclass(frozen=True)
class ResultadoComandosMontaje:
    """Salida de `calcular_comandos_montaje`.

    `pasos` vacio junto con `motivo_sin_generar` (no `None`) es la senal de "no
    generar el documento" (mismo patron que `ResultadoConcatFfmpeg`/
    `ResultadoCapitulos`): sin ningun parte de rodaje con una toma buena, no hay
    nada real que montar todavia. `escenas_pendientes` son las escenas de
    `concat-ffmpeg.txt` que todavia no tienen un archivo de video real (sin toma
    buena, o con ella pero sin anotar) -- vacio significa que todas las escenas
    con toma buena ya tienen su archivo real. `incluye_capitulos` dice si el
    tercer paso (capitulos) se incluyo. `archivos_referenciados_faltantes`
    (R-31) son los archivos que los pasos citan por su nombre pero que todavia
    no existen en `carpeta_salida` -- vacio si no se paso `carpeta_salida` a
    `calcular_comandos_montaje` (comportamiento identico al de antes de R-31)
    o si los tres ya estan en disco.
    """

    pasos: tuple[PasoComandoMontaje, ...]
    escenas_pendientes: tuple[EscenaPendiente, ...]
    incluye_capitulos: bool
    motivo_sin_generar: str | None
    archivos_referenciados_faltantes: tuple[ArchivoReferenciadoFaltante, ...] = ()


def calcular_comandos_montaje(
    resultado: ResultadoParseo,
    resultado_tiempos: ResultadoTiempos,
    nombre_guion: str,
    tomas_por_escena: dict[str, Any] | None = None,
    configuracion: Configuracion | None = None,
    carpeta_salida: Path | None = None,
) -> ResultadoComandosMontaje:
    """Construye la secuencia de 1 a 3 comandos encadenados (requisito 1).

    Reutiliza tal cual las mismas tres funciones de calculo que ya deciden si
    `concat-ffmpeg.txt`, `guion-alineado.srt` y `capitulos-ffmpeg.txt` existirian
    en esta misma pasada de `scripts/salidas.py` -- nunca relee del disco lo que
    esas salidas ya hayan escrito, para no depender de que el dueno las haya
    seleccionado tambien en esta pasada (generacion independiente, T-30
    requisito 3).

    `carpeta_salida` (R-31, opcional) solo se usa para comprobar si los
    archivos referenciados por los pasos YA ESTAN en disco -- nunca para
    releer ni revalidar su contenido (eso ya lo hacen sus propios validadores
    en su propia ruta de generacion, R-21/R-28). Sin ella (`None`, valor por
    defecto), el comportamiento es identico al de antes de R-31: ningun
    archivo se marca como faltante."""
    configuracion = configuracion or Configuracion()
    tomas_por_escena = tomas_por_escena or {}

    resultado_concat = calcular_lista_concat_ffmpeg(resultado_tiempos, tomas_por_escena)
    if resultado_concat.motivo_sin_generar is not None:
        return ResultadoComandosMontaje(
            pasos=(),
            escenas_pendientes=(),
            incluye_capitulos=False,
            motivo_sin_generar=_MOTIVO_SIN_RODAJE,
        )

    archivo_concatenado = f"{nombre_guion}{configuracion.comandos_montaje_sufijo_concatenado}"
    pasos: list[PasoComandoMontaje] = [
        PasoComandoMontaje(
            descripcion="Concatenar las tomas buenas en un único vídeo, sin recodificar.",
            comando=(
                f"ffmpeg -f concat -safe 0 -i {NOMBRE_ARCHIVO_CONCAT_FFMPEG} "
                f"-c copy {archivo_concatenado}"
            ),
        )
    ]
    entrada_video = archivo_concatenado

    _contenido_alineado, alineacion = generar_srt_alineado(
        resultado_tiempos, tomas_por_escena, configuracion
    )
    nombre_srt = (
        NOMBRE_ARCHIVO_SRT_ALINEADO if alineacion.escenas_alineadas else NOMBRE_ARCHIVO_SRT
    )
    archivo_con_subtitulos = (
        f"{nombre_guion}{configuracion.comandos_montaje_sufijo_con_subtitulos}"
    )
    pasos.append(
        PasoComandoMontaje(
            descripcion=(
                "Añadir los subtítulos como pista blanda (reversible, sin recodificar vídeo)."
            ),
            comando=(
                f"ffmpeg -i {entrada_video} -i {nombre_srt} -c copy -c:s mov_text "
                f"{archivo_con_subtitulos}"
            ),
            comentario_alternativo=(
                "Alternativa: subtítulos incrustados (\"quemados\") — exige recodificar el "
                "vídeo y no es reversible: "
                f"ffmpeg -i {entrada_video} -vf \"subtitles={nombre_srt}\" "
                f"{archivo_con_subtitulos}"
            ),
        )
    )
    entrada_video = archivo_con_subtitulos

    _contenido_youtube, calculo_capitulos = generar_capitulos_youtube(
        resultado, resultado_tiempos, tomas_por_escena, configuracion
    )
    incluye_capitulos = formatear_capitulos_ffmpeg(calculo_capitulos, configuracion) is not None
    if incluye_capitulos:
        archivo_final = f"{nombre_guion}{configuracion.comandos_montaje_sufijo_final}"
        pasos.append(
            PasoComandoMontaje(
                descripcion="Incrustar los capítulos reales en el vídeo final.",
                comando=(
                    f"ffmpeg -i {entrada_video} -i {NOMBRE_ARCHIVO_CAPITULOS_FFMPEG} "
                    f"-map_metadata 1 -codec copy {archivo_final}"
                ),
            )
        )

    archivos_referenciados_faltantes: list[ArchivoReferenciadoFaltante] = []
    if carpeta_salida is not None:
        candidatos = [
            (NOMBRE_ARCHIVO_CONCAT_FFMPEG, DESCRIPCION_OPCION_CONCAT_FFMPEG),
            (nombre_srt, DESCRIPCION_OPCION_SRT),
        ]
        if incluye_capitulos:
            candidatos.append(
                (NOMBRE_ARCHIVO_CAPITULOS_FFMPEG, DESCRIPCION_OPCION_CAPITULOS_YOUTUBE)
            )
        archivos_referenciados_faltantes = [
            ArchivoReferenciadoFaltante(nombre_archivo, descripcion_opcion)
            for nombre_archivo, descripcion_opcion in candidatos
            if not (carpeta_salida / nombre_archivo).exists()
        ]

    return ResultadoComandosMontaje(
        pasos=tuple(pasos),
        escenas_pendientes=resultado_concat.escenas_pendientes,
        incluye_capitulos=incluye_capitulos,
        motivo_sin_generar=None,
        archivos_referenciados_faltantes=tuple(archivos_referenciados_faltantes),
    )


def formatear_comandos_montaje(
    resultado: ResultadoComandosMontaje, nombre_guion: str
) -> str | None:
    """Texto final de `comandos-montaje.md` (requisito 2). `None` si `resultado`
    no trae ningun paso (nada real que montar todavia).

    Cada paso trae su explicacion de una frase y el comando en un bloque de
    codigo listo para copiar tal cual -- nunca una ruta de ejemplo, solo
    nombres de archivo reales de esta carpeta de salida. Si la cadena se
    detiene antes de los capitulos (sin seccion `Capitulos` en el guion), lo
    dice explicitamente. Si quedan escenas de `concat-ffmpeg.txt` sin toma
    buena o sin archivo anotado, una nota al final avisa de que el resultado
    no estara completo hasta grabar o anotar esas escenas. Si algun archivo
    referenciado todavia no existe en la carpeta de salida (R-31), una nota
    al principio avisa de que opcion del selector hay que marcar para
    generarlo antes de ejecutar los comandos."""
    if not resultado.pasos:
        return None

    lineas = [f"# Comandos de montaje — {nombre_guion}", ""]
    lineas.append(
        "Comandos `ffmpeg` listos para copiar y pegar, en el orden real de montaje "
        "de este guion. No se ejecutan desde la skill — cópialos en tu terminal, "
        "dentro de esta misma carpeta de salida."
    )
    lineas.append("")

    if resultado.archivos_referenciados_faltantes:
        lineas.append(
            "**Archivos referenciados que todavía no existen en esta carpeta de "
            "salida** — selecciona la opción correspondiente del selector de "
            "salidas y vuelve a generar antes de ejecutar estos comandos:"
        )
        lineas.append("")
        for faltante in resultado.archivos_referenciados_faltantes:
            lineas.append(
                f"- `{faltante.nombre_archivo}`: selecciona «{faltante.descripcion_opcion}»"
            )
        lineas.append("")

    for indice, paso in enumerate(resultado.pasos, start=1):
        lineas.append(f"## {indice}. {paso.descripcion}")
        lineas.append("")
        lineas.append("```")
        lineas.append(paso.comando)
        lineas.append("```")
        if paso.comentario_alternativo is not None:
            lineas.append("")
            lineas.append(f"<!-- {paso.comentario_alternativo} -->")
        lineas.append("")

    if not resultado.incluye_capitulos:
        lineas.append(
            "Este guion no trae sección «Capítulos»: la cadena de comandos termina en "
            "el paso de subtítulos. En cuanto el guion la tenga, vuelve a generar esta "
            "salida para incorporar el paso de capítulos."
        )
        lineas.append("")

    if resultado.escenas_pendientes:
        lineas.append(
            "**Escenas todavía sin toma buena o sin archivo de vídeo anotado** — el "
            "resultado de estos comandos no estará completo hasta grabar o anotar "
            "estas escenas:"
        )
        lineas.append("")
        for pendiente in resultado.escenas_pendientes:
            lineas.append(f"- Escena {pendiente.numero_escena}: {pendiente.motivo}")
        lineas.append("")

    return "\n".join(lineas).rstrip("\n") + "\n"


def generar_comandos_montaje(
    resultado: ResultadoParseo,
    resultado_tiempos: ResultadoTiempos,
    nombre_guion: str,
    tomas_por_escena: dict[str, Any] | None = None,
    configuracion: Configuracion | None = None,
    carpeta_salida: Path | None = None,
) -> tuple[str | None, ResultadoComandosMontaje]:
    """Punto de entrada de R-30: calcula y formatea en un solo paso, mismo
    patron que `concat_ffmpeg.generar_lista_concat_ffmpeg`/
    `capitulos_youtube.generar_capitulos_youtube`. `contenido` es `None`
    cuando no hay nada que generar: no llamar a `guardar_comandos_montaje` en
    ese caso. `carpeta_salida` (R-31, opcional) se pasa tal cual a
    `calcular_comandos_montaje`."""
    resultado_comandos = calcular_comandos_montaje(
        resultado, resultado_tiempos, nombre_guion, tomas_por_escena, configuracion, carpeta_salida
    )
    contenido = formatear_comandos_montaje(resultado_comandos, nombre_guion)
    return contenido, resultado_comandos


def guardar_comandos_montaje(contenido: str, carpeta_salida: Path) -> Path:
    """Escribe `comandos-montaje.md` en la carpeta de salida del guion. Nunca
    fuera de `carpeta_salida` (regla de aislamiento, §0.2). No llamar con
    `contenido=None`: quien orquesta decide no escribir nada."""
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    destino = carpeta_salida / NOMBRE_ARCHIVO_COMANDOS_MONTAJE
    destino.write_text(contenido, encoding="utf-8", newline="\n")
    return destino
