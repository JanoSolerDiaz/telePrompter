"""Motor de tiempos (tarea T-12): ppm deducido del guion, duracion por bloque de
respiracion, agregados por escena y total, y contraste con la duracion objetivo.

`calcular_tiempos` es la UNICA funcion que calcula tiempos (requisito 4 de T-12):
el informe, la cabecera de `guion-escenas.md` (T-16), el `.srt` (T-27) y el
reproductor (T-18+) consumen su resultado, ninguno recalcula por su cuenta.

Ritmo (requisitos 1, 7 y 8): el ppm de referencia se deduce como valor UNICO para
todo el guion (nunca por escena, para no anular el aviso del requisito 6) a partir
de las palabras de locucion totales frente a la suma de las duraciones objetivo
por escena que ya trae cada encabezado (`## BLOQUE N — <titulo> (m:ss - m:ss)`,
T-08). Cae al respaldo configurado (120 ppm) si falta la duracion objetivo de
alguna escena o si el valor deducido cae fuera de la banda de plausibilidad, y
avisa siempre del motivo. Una calibracion manual (`Configuracion.ppm_manual`,
requisito 8) tiene prioridad sobre ambos.

Duracion por bloque (requisito 2): palabras del bloque al ritmo aplicado, mas una
pausa segun la puntuacion final -- coma < punto < fin de parrafo < fin de escena
(en ese orden creciente). "Fin de parrafo" y "fin de escena" se deciden por
posicion (ultimo bloque de respiracion de una `BloqueClasificado` de T-09, o de
toda la escena), no por puntuacion: sustituyen a la puntuacion final cuando
aplican, no se suman a ella.

Contraste (requisito 6): por escena, contra la duracion objetivo de esa escena
-- la diferencia entre los dos extremos del rango horario de su encabezado
(`(m:ss - m:ss)`, que son marcas de tiempo del video, no una horquilla de
duraciones posibles: la escena 4 de `guion-08` empieza en el minuto 1:55 y acaba
en el 3:10, dura 75s, no "162s de media" entre esos dos instantes). En total,
contra el metadato **Duración objetivo:** de cabecera (2), que si es una
horquilla real de duracion total ("3:40 - 3:55"): se usa tal cual si esta
presente; si no, se cae a la suma de las duraciones por escena como objetivo
total de respaldo. Avisa cuando la desviacion relativa supera
`Configuracion.umbral_desviacion_tiempos`, indicando cuantas palabras sobran o
faltan para encajar al ritmo aplicado.
"""

from __future__ import annotations

from dataclasses import dataclass

from clasificador import TIPO_LOCUCION, BloqueClasificado, clasificar_escena
from config import Configuracion
from parser import Escena, ResultadoParseo, rango_segundos_titulo
from troceo import BloqueRespiracion, categoria_puntuacion_final, trocear_bloque_locucion

_PAUSA_NINGUNA = "ninguna"
_PAUSA_COMA = "coma"
_PAUSA_PUNTO = "punto"
_PAUSA_FIN_PARRAFO = "fin_parrafo"
_PAUSA_FIN_ESCENA = "fin_escena"

ORIGEN_DEDUCIDO = "deducido"
ORIGEN_RESPALDO = "respaldo"
ORIGEN_MANUAL = "manual"


@dataclass
class RitmoAplicado:
    """Que ritmo se ha usado y por que (requisito 7: transparencia del ritmo)."""

    ppm_aplicado: int
    origen: str  # ORIGEN_DEDUCIDO | ORIGEN_RESPALDO | ORIGEN_MANUAL
    ppm_deducido: float | None
    ppm_alternativo: float
    motivo: str


@dataclass
class BloqueConTiempo:
    """Un bloque de respiracion (T-11) con su tiempo estimado.

    `inicio_segundos` es acumulado desde el arranque del guion; `fin_segundos`
    (propiedad) incluye la pausa posterior, asi que el bloque siguiente empieza
    exactamente donde este termina: no hay huecos ni solapes sin contabilizar.
    """

    bloque: BloqueRespiracion
    inicio_segundos: float
    duracion_palabras_segundos: float
    tipo_pausa: str
    pausa_segundos: float

    @property
    def fin_segundos(self) -> float:
        return self.inicio_segundos + self.duracion_palabras_segundos + self.pausa_segundos


@dataclass
class TiempoEscena:
    """Agregado de tiempos de una escena, con el contraste frente al objetivo.

    `duracion_objetivo_segundos` es un unico numero (fin - inicio del rango
    horario del encabezado), no el rango en si: ese rango son marcas de tiempo
    del video, no una horquilla de duraciones posibles para la escena.
    """

    numero: int
    duracion_estimada_segundos: float
    duracion_objetivo_segundos: float | None
    aviso: str | None


@dataclass
class ResultadoTiempos:
    """Salida completa de `calcular_tiempos`: la unica fuente de tiempos (requisito 4).

    `duracion_objetivo_total_segundos` es la horquilla del metadato de cabecera
    **Duración objetivo:** cuando el guion lo trae; si no, un par degenerado
    (mismo valor dos veces) con la suma de las duraciones por escena, para que
    el tipo sea siempre el mismo independientemente del origen.
    """

    ritmo: RitmoAplicado
    bloques: list[BloqueConTiempo]
    escenas: list[TiempoEscena]
    duracion_total_segundos: float
    duracion_objetivo_total_segundos: tuple[int, int] | None
    aviso_total: str | None


def _duracion_objetivo_escena(escena: Escena) -> float | None:
    """Duracion objetivo de una escena: la diferencia entre los dos extremos del
    rango horario de su encabezado (marcas de tiempo del video), no el rango en
    si. `None` si el encabezado no trae rango horario."""
    rango = rango_segundos_titulo(escena.titulo)
    return float(rango[1] - rango[0]) if rango is not None else None


_CLAVE_METADATO_DURACION_OBJETIVO = "Duración objetivo"


def _duracion_objetivo_metadato(resultado: ResultadoParseo) -> tuple[int, int] | None:
    """Horquilla de duracion total del guion completo, del metadato de cabecera
    `**Duración objetivo:**` (T-08). A diferencia del rango de un encabezado de
    escena, esta si es una horquilla real de duraciones ("3:40 - 3:55"), no un
    par de marcas de tiempo."""
    valor = resultado.metadatos.get(_CLAVE_METADATO_DURACION_OBJETIVO)
    return rango_segundos_titulo(valor) if valor is not None else None


def _bloques_respiracion_marcados(
    escena: Escena, configuracion: Configuracion
) -> list[tuple[BloqueRespiracion, bool, bool]]:
    """`(bloque, es_fin_de_parrafo, es_fin_de_escena)` de cada bloque de respiracion.

    Reclasifica la escena en vez de recibir los bloques ya troceados, mismo patron
    que ya uso T-11 (`trocear_guion`) para no ampliar `BloqueClasificado` (T-09)
    solo por conveniencia. "Fin de parrafo" es el ultimo bloque de respiracion
    producido por un mismo `BloqueClasificado` de tipo locucion (T-11 trocea cada
    uno por separado); "fin de escena" es ademas el ultimo parrafo de la escena.
    """
    bloques_clasificados: list[BloqueClasificado] = [
        bloque
        for bloque in clasificar_escena(escena, configuracion)
        if bloque.tipo == TIPO_LOCUCION
    ]
    marcados: list[tuple[BloqueRespiracion, bool, bool]] = []
    for indice_parrafo, bloque_clasificado in enumerate(bloques_clasificados):
        es_ultimo_parrafo = indice_parrafo == len(bloques_clasificados) - 1
        fragmentos = trocear_bloque_locucion(bloque_clasificado, escena.numero, configuracion)
        for indice_fragmento, fragmento in enumerate(fragmentos):
            es_fin_de_parrafo = indice_fragmento == len(fragmentos) - 1
            es_fin_de_escena = es_fin_de_parrafo and es_ultimo_parrafo
            marcados.append((fragmento, es_fin_de_parrafo, es_fin_de_escena))
    return marcados


def _tipo_pausa(texto: str, es_fin_de_parrafo: bool, es_fin_de_escena: bool) -> str:
    if es_fin_de_escena:
        return _PAUSA_FIN_ESCENA
    if es_fin_de_parrafo:
        return _PAUSA_FIN_PARRAFO
    categoria = categoria_puntuacion_final(texto)
    if categoria == "fuerte":
        return _PAUSA_PUNTO
    if categoria == "debil":
        return _PAUSA_COMA
    return _PAUSA_NINGUNA


def _pausa_segundos(tipo_pausa: str, configuracion: Configuracion) -> float:
    return {
        _PAUSA_NINGUNA: 0.0,
        _PAUSA_COMA: configuracion.pausa_coma_segundos,
        _PAUSA_PUNTO: configuracion.pausa_punto_segundos,
        _PAUSA_FIN_PARRAFO: configuracion.pausa_fin_parrafo_segundos,
        _PAUSA_FIN_ESCENA: configuracion.pausa_fin_escena_segundos,
    }[tipo_pausa]


def _deducir_ritmo(
    palabras_totales: int,
    duraciones_objetivo_por_escena: list[float | None],
    configuracion: Configuracion,
) -> RitmoAplicado:
    if configuracion.ppm_manual is not None:
        return RitmoAplicado(
            ppm_aplicado=configuracion.ppm_manual,
            origen=ORIGEN_MANUAL,
            ppm_deducido=None,
            ppm_alternativo=float(configuracion.ppm_respaldo),
            motivo=(
                "ppm fijado a mano por el dueno tras calibrar con una toma real "
                "(requisito 8), con prioridad sobre el deducido y el respaldo"
            ),
        )

    if not duraciones_objetivo_por_escena or any(
        duracion is None for duracion in duraciones_objetivo_por_escena
    ):
        return RitmoAplicado(
            ppm_aplicado=configuracion.ppm_respaldo,
            origen=ORIGEN_RESPALDO,
            ppm_deducido=None,
            ppm_alternativo=float(configuracion.ppm_respaldo),
            motivo=(
                "el guion no trae duracion objetivo `(m:ss - m:ss)` en todas las escenas: "
                "no se puede deducir un ppm, se aplica el respaldo"
            ),
        )

    total_objetivo_segundos = sum(
        duracion for duracion in duraciones_objetivo_por_escena if duracion is not None
    )
    if palabras_totales == 0 or total_objetivo_segundos <= 0:
        return RitmoAplicado(
            ppm_aplicado=configuracion.ppm_respaldo,
            origen=ORIGEN_RESPALDO,
            ppm_deducido=None,
            ppm_alternativo=float(configuracion.ppm_respaldo),
            motivo=(
                "no hay palabras de locucion o duracion objetivo con las que deducir un ppm: "
                "se aplica el respaldo"
            ),
        )

    ppm_deducido = palabras_totales / (total_objetivo_segundos / 60)
    minimo_banda, maximo_banda = configuracion.ppm_banda_plausible
    if not (minimo_banda <= ppm_deducido <= maximo_banda):
        return RitmoAplicado(
            ppm_aplicado=configuracion.ppm_respaldo,
            origen=ORIGEN_RESPALDO,
            ppm_deducido=ppm_deducido,
            ppm_alternativo=ppm_deducido,
            motivo=(
                f"el ppm deducido ({ppm_deducido:.0f}) cae fuera de la banda plausible "
                f"[{minimo_banda}, {maximo_banda}]: se aplica el respaldo"
            ),
        )

    return RitmoAplicado(
        ppm_aplicado=round(ppm_deducido),
        origen=ORIGEN_DEDUCIDO,
        ppm_deducido=ppm_deducido,
        ppm_alternativo=float(configuracion.ppm_respaldo),
        motivo=(
            f"deducido de {palabras_totales} palabras de locucion frente a "
            f"{total_objetivo_segundos:.0f}s de duracion objetivo del guion"
        ),
    )


def _aviso_desviacion(
    estimada_segundos: float,
    objetivo_segundos: float | None,
    ppm_aplicado: int,
    configuracion: Configuracion,
    *,
    contexto: str,
) -> str | None:
    """Aviso de desviacion frente a una duracion objetivo ya reducida a un unico
    numero (el punto medio de una horquilla, o la duracion exacta de una escena;
    esa reduccion la hace quien llama, esta funcion ya no distingue el origen)."""
    if objetivo_segundos is None or objetivo_segundos <= 0:
        return None
    desviacion_relativa = abs(estimada_segundos - objetivo_segundos) / objetivo_segundos
    if desviacion_relativa <= configuracion.umbral_desviacion_tiempos:
        return None
    diferencia_segundos = estimada_segundos - objetivo_segundos
    palabras = abs(diferencia_segundos) * ppm_aplicado / 60
    verbo = "sobran" if diferencia_segundos > 0 else "faltan"
    return (
        f"En {contexto} la estimacion ({estimada_segundos:.0f}s) se desvia del objetivo "
        f"({objetivo_segundos:.0f}s) mas de {configuracion.umbral_desviacion_tiempos:.0%}: "
        f"{verbo} unas {palabras:.0f} palabras para encajar en el objetivo."
    )


def calcular_tiempos(
    resultado: ResultadoParseo, configuracion: Configuracion | None = None
) -> ResultadoTiempos:
    """Calcula todos los tiempos de un guion ya parseado (T-08). Unica fuente
    de tiempos del proyecto (requisito 4): ninguna otra parte del codigo debe
    recalcular una duracion por su cuenta, siempre a partir de este resultado."""
    configuracion = configuracion or Configuracion()

    marcados_por_escena = {
        escena.numero: _bloques_respiracion_marcados(escena, configuracion)
        for escena in resultado.escenas
    }
    palabras_totales = sum(
        bloque.num_palabras
        for marcados in marcados_por_escena.values()
        for bloque, _es_fin_parrafo, _es_fin_escena in marcados
    )
    duraciones_objetivo_por_escena = [
        _duracion_objetivo_escena(escena) for escena in resultado.escenas
    ]

    ritmo = _deducir_ritmo(palabras_totales, duraciones_objetivo_por_escena, configuracion)
    palabras_por_segundo = ritmo.ppm_aplicado / 60

    bloques_con_tiempo: list[BloqueConTiempo] = []
    tiempos_escenas: list[TiempoEscena] = []
    cursor_segundos = 0.0
    for escena in resultado.escenas:
        inicio_escena = cursor_segundos
        for bloque, es_fin_de_parrafo, es_fin_de_escena in marcados_por_escena[escena.numero]:
            tipo_pausa = _tipo_pausa(bloque.texto, es_fin_de_parrafo, es_fin_de_escena)
            pausa_segundos = _pausa_segundos(tipo_pausa, configuracion)
            duracion_palabras_segundos = bloque.num_palabras / palabras_por_segundo
            bloques_con_tiempo.append(
                BloqueConTiempo(
                    bloque=bloque,
                    inicio_segundos=cursor_segundos,
                    duracion_palabras_segundos=duracion_palabras_segundos,
                    tipo_pausa=tipo_pausa,
                    pausa_segundos=pausa_segundos,
                )
            )
            cursor_segundos += duracion_palabras_segundos + pausa_segundos

        objetivo_escena = _duracion_objetivo_escena(escena)
        duracion_escena_segundos = cursor_segundos - inicio_escena
        tiempos_escenas.append(
            TiempoEscena(
                numero=escena.numero,
                duracion_estimada_segundos=duracion_escena_segundos,
                duracion_objetivo_segundos=objetivo_escena,
                aviso=_aviso_desviacion(
                    duracion_escena_segundos,
                    objetivo_escena,
                    ritmo.ppm_aplicado,
                    configuracion,
                    contexto=f"la escena {escena.numero}",
                ),
            )
        )

    duracion_total_segundos = cursor_segundos

    objetivo_total_segundos = _duracion_objetivo_metadato(resultado)
    if objetivo_total_segundos is None and duraciones_objetivo_por_escena and all(
        duracion is not None for duracion in duraciones_objetivo_por_escena
    ):
        suma_escenas = sum(
            duracion for duracion in duraciones_objetivo_por_escena if duracion is not None
        )
        objetivo_total_segundos = (round(suma_escenas), round(suma_escenas))
    objetivo_total_medio = (
        (objetivo_total_segundos[0] + objetivo_total_segundos[1]) / 2
        if objetivo_total_segundos is not None
        else None
    )

    return ResultadoTiempos(
        ritmo=ritmo,
        bloques=bloques_con_tiempo,
        escenas=tiempos_escenas,
        duracion_total_segundos=duracion_total_segundos,
        duracion_objetivo_total_segundos=objetivo_total_segundos,
        aviso_total=_aviso_desviacion(
            duracion_total_segundos,
            objetivo_total_medio,
            ritmo.ppm_aplicado,
            configuracion,
            contexto="el guion completo",
        ),
    )
