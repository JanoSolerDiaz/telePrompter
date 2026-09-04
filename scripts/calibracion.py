"""Recalibrar el ritmo con tiempos reales (tarea R-04).

Cierra el bucle que T-12 y R-02 dejaron abierto cada uno por su lado: T-12
deduce el ppm de las duraciones OBJETIVO de cabecera del guion (una intencion
del guionista, `(m:ss - m:ss)` del encabezado de cada escena) y calcula con
ese ppm la duracion ESTIMADA de cada bloque; R-02 aporta la duracion REAL de
cada toma marcada como buena (`estado.tomas`, fusionado por `scripts/tomas.py`).
Este modulo no calcula tiempos por su cuenta -- lee el `ResultadoTiempos` que
ya produjo `tiempos.calcular_tiempos`/`calcular_tiempos_desde_marcados` (unica
fuente de tiempos, T-12 requisito 4) y el registro de tomas ya fusionado.

Requisito 1 (comparar por escena y en total): `calcular_calibracion` construye
un `ContrasteGuion` por guion de entrada, con un `ContrasteEscena` por escena
que trae las tres duraciones -- estimada, objetivo, real -- una al lado de
otra. La real es la de la toma marcada `buena` (R-02, `tomas.duracion_toma_buena`
-- publica desde R-05, que la reutiliza tal cual en vez de reimplementar el
mismo criterio): una escena con tomas pero ninguna marcada `buena` no aporta
evidencia real todavia, a proposito -- mezclar una toma fallida o repetida sin
marcar habria contaminado la calibracion con tiempos que el propio dueno no
valido como representativos.

Requisito 2 (ppm calibrado propuesto, nunca aplicado solo): `_propuesta_ppm`
agrega palabras y duracion real de TODAS las escenas con toma buena de TODOS
los guiones de entrada (`evidencia acumulada de varios guiones`, literal del
requisito) y deduce un ppm con la misma formula que `tiempos._deducir_ritmo`
(palabras entre minutos), sujeto a los mismos guardarraíles: banda de
plausibilidad (`Configuracion.ppm_banda_plausible`, reutilizada tal cual) y un
minimo de evidencia (`calibracion_guiones_minimos`/`calibracion_palabras_minimas`,
nuevos en `config.py`) para no sobreajustar a un unico guion o a un puñado de
palabras. Sin evidencia suficiente, `ppm_calibrado` es `None` con un motivo
explicito -- nunca un numero especulativo. Este modulo NUNCA escribe
`Configuracion.ppm_manual`: la propuesta es datos para que Claude se la
formule al dueno dentro de la sesion (mismo patron que
`salidas.construir_pregunta_salidas`, T-30), y es el dueno quien decide si se
aplica en una proxima pasada -- no hay mecanismo de persistencia nuevo porque
`ppm_manual` ya viaja dentro de `configuracion_efectiva` (decision de T-12).

Requisito 3 (informe corto, que tipo de escena acelera y cual frena):
`_tipo_escena` clasifica cada escena por POSICION dentro de su propio guion
-- apertura (primera), cierre (ultima), desarrollo (el resto) -- en vez de
por titulo: mismo criterio ya usado en T-10 para el subtitulo entrecomillado,
porque el titulo de la ultima escena no siempre dice literalmente "Cierre"
(`guion-09-proyectos.md` cierra con "Qué NO va en un proyecto") y la posicion
es la unica señal que funciona igual en cualquier guion. `_resumen_por_tipo`
agrega estimada/real por tipo entre todos los guiones para que el informe
diga, por ejemplo, que las escenas de cierre se alargan un 12% mientras las
de desarrollo van casi exactas.

No hay migracion de `estado.json` (ficha R-04, "Migración: No"): este modulo
solo LEE `ResultadoTiempos` y `EstadoProyecto.tomas`, ya persistidos por T-12
y R-02 respectivamente.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from config import Configuracion
from presentacion import Nivel, mostrar, titulo
from tiempos import ResultadoTiempos
from tomas import duracion_toma_buena

TIPO_APERTURA = "apertura"
TIPO_DESARROLLO = "desarrollo"
TIPO_CIERRE = "cierre"

_ETIQUETA_TIPO = {
    TIPO_APERTURA: "apertura",
    TIPO_DESARROLLO: "desarrollo",
    TIPO_CIERRE: "cierre",
}


@dataclass(frozen=True)
class EvidenciaGuion:
    """Lo que aporta un guion grabado a la calibracion.

    `resultado_tiempos` deberia venir, cuando exista una revalidacion previa,
    de `revalidacion.revalidar_guion(...).resultado_tiempos` -- mismo criterio
    que T-27 (`srt.py`) para que la estimacion refleje las reescrituras ya
    aceptadas, no el guion sin revisar. `tomas_por_escena` es
    `EstadoProyecto.tomas` tal cual (T-07/R-02): claves de escena en texto,
    cada una con `titulo` y una lista `tomas`.
    """

    nombre_guion: str
    resultado_tiempos: ResultadoTiempos
    tomas_por_escena: dict[str, Any]


@dataclass(frozen=True)
class ContrasteEscena:
    """Las tres duraciones de una escena, una al lado de otra (requisito 1)."""

    numero: int
    titulo: str
    tipo: str
    palabras: int
    duracion_estimada_segundos: float
    duracion_objetivo_segundos: float | None
    duracion_real_segundos: float | None


@dataclass(frozen=True)
class ContrasteGuion:
    """El contraste de un guion completo: sus escenas mas los totales."""

    nombre_guion: str
    escenas: tuple[ContrasteEscena, ...]
    duracion_estimada_total_segundos: float
    duracion_objetivo_total_segundos: float | None
    duracion_real_total_segundos: float | None


@dataclass(frozen=True)
class PropuestaPpm:
    """El ppm calibrado propuesto (requisito 2), o por que no se propone
    ninguno todavia. Nunca se aplica por su cuenta -- ver docstring del modulo."""

    ppm_calibrado: int | None
    ppm_deducido: float | None
    palabras_totales: int
    duracion_real_total_segundos: float
    num_guiones_con_evidencia: int
    num_escenas_con_evidencia: int
    motivo: str


@dataclass(frozen=True)
class ResumenTipoEscena:
    """Agregado de un tipo de escena (apertura/desarrollo/cierre) entre todos
    los guiones de entrada, con evidencia real (requisito 3)."""

    tipo: str
    num_escenas: int
    palabras_totales: int
    duracion_estimada_total_segundos: float
    duracion_real_total_segundos: float

    @property
    def desviacion_relativa(self) -> float:
        """(real - estimada) / estimada. Negativo = el locutor va mas rapido
        que lo estimado (acelera); positivo = va mas lento (frena)."""
        if self.duracion_estimada_total_segundos <= 0:
            return 0.0
        return (
            self.duracion_real_total_segundos - self.duracion_estimada_total_segundos
        ) / self.duracion_estimada_total_segundos


@dataclass(frozen=True)
class InformeCalibracion:
    """Salida completa de `calcular_calibracion`."""

    guiones: tuple[ContrasteGuion, ...]
    propuesta_ppm: PropuestaPpm
    resumen_por_tipo: tuple[ResumenTipoEscena, ...]

    def mostrar_informe(self) -> None:
        """Muestra el informe por `presentacion.py` (requisito 3: informe
        corto y legible). Solo muestra: nunca decide ni aplica nada -- el
        ppm propuesto es una pregunta para el dueno, no una accion."""
        titulo("Contraste de tiempos por guion y escena")
        for guion in self.guiones:
            mostrar(f"{guion.nombre_guion}:", Nivel.INFO)
            for escena in guion.escenas:
                objetivo = (
                    f"{escena.duracion_objetivo_segundos:.0f}s"
                    if escena.duracion_objetivo_segundos is not None
                    else "sin dato"
                )
                real = (
                    f"{escena.duracion_real_segundos:.0f}s"
                    if escena.duracion_real_segundos is not None
                    else "sin toma buena"
                )
                mostrar(
                    f"  Escena {escena.numero} ({_ETIQUETA_TIPO[escena.tipo]}) — "
                    f"{escena.titulo}: estimada {escena.duracion_estimada_segundos:.0f}s · "
                    f"objetivo {objetivo} · real {real}",
                    Nivel.INFO,
                )

        if self.resumen_por_tipo:
            titulo("Ritmo por tipo de escena")
            for resumen in self.resumen_por_tipo:
                desviacion = resumen.desviacion_relativa
                if desviacion < 0:
                    tendencia = "más rápido"
                elif desviacion > 0:
                    tendencia = "más lento"
                else:
                    tendencia = "igual"
                mostrar(
                    f"{_ETIQUETA_TIPO[resumen.tipo]}: el locutor va un "
                    f"{abs(desviacion):.0%} {tendencia} que lo estimado "
                    f"({resumen.num_escenas} escenas con toma buena)",
                    Nivel.INFO,
                )

        titulo("Ppm calibrado propuesto")
        propuesta = self.propuesta_ppm
        if propuesta.ppm_calibrado is not None:
            mostrar(f"{propuesta.ppm_calibrado} ppm — {propuesta.motivo}", Nivel.OK)
            mostrar(
                "Es una propuesta: hace falta que el dueño la acepte para aplicarla "
                "(Configuracion.ppm_manual) en una próxima pasada.",
                Nivel.INFO,
            )
        else:
            mostrar(f"Sin propuesta todavía — {propuesta.motivo}", Nivel.AVISO)


def _tipo_escena(indice: int, total_escenas: int) -> str:
    """Clasificacion posicional (ver docstring del modulo): la primera escena
    de cada guion es apertura, la ultima es cierre, el resto es desarrollo.
    Un guion de una sola escena es apertura (precedencia del primer `if`)."""
    if indice == 0:
        return TIPO_APERTURA
    if indice == total_escenas - 1:
        return TIPO_CIERRE
    return TIPO_DESARROLLO


def _contraste_guion(evidencia: EvidenciaGuion) -> ContrasteGuion:
    palabras_por_escena: dict[int, int] = defaultdict(int)
    for bloque_con_tiempo in evidencia.resultado_tiempos.bloques:
        palabras_por_escena[bloque_con_tiempo.bloque.numero_escena] += (
            bloque_con_tiempo.bloque.num_palabras
        )

    total_escenas = len(evidencia.resultado_tiempos.escenas)
    escenas: list[ContrasteEscena] = []
    for indice, tiempo_escena in enumerate(evidencia.resultado_tiempos.escenas):
        tomas_escena = evidencia.tomas_por_escena.get(str(tiempo_escena.numero))
        titulo_escena = (
            tomas_escena.get("titulo") if tomas_escena else None
        ) or f"Escena {tiempo_escena.numero}"
        escenas.append(
            ContrasteEscena(
                numero=tiempo_escena.numero,
                titulo=titulo_escena,
                tipo=_tipo_escena(indice, total_escenas),
                palabras=palabras_por_escena[tiempo_escena.numero],
                duracion_estimada_segundos=tiempo_escena.duracion_estimada_segundos,
                duracion_objetivo_segundos=tiempo_escena.duracion_objetivo_segundos,
                duracion_real_segundos=duracion_toma_buena(tomas_escena, tiempo_escena.numero),
            )
        )

    duraciones_reales = [
        escena.duracion_real_segundos
        for escena in escenas
        if escena.duracion_real_segundos is not None
    ]
    objetivo_total = evidencia.resultado_tiempos.duracion_objetivo_total_segundos
    return ContrasteGuion(
        nombre_guion=evidencia.nombre_guion,
        escenas=tuple(escenas),
        duracion_estimada_total_segundos=evidencia.resultado_tiempos.duracion_total_segundos,
        duracion_objetivo_total_segundos=(
            (objetivo_total[0] + objetivo_total[1]) / 2 if objetivo_total is not None else None
        ),
        duracion_real_total_segundos=sum(duraciones_reales) if duraciones_reales else None,
    )


def _propuesta_ppm(
    guiones: tuple[ContrasteGuion, ...], configuracion: Configuracion
) -> PropuestaPpm:
    escenas_con_evidencia = [
        (guion.nombre_guion, escena)
        for guion in guiones
        for escena in guion.escenas
        if escena.duracion_real_segundos is not None and escena.duracion_real_segundos > 0
    ]
    guiones_con_evidencia = {nombre for nombre, _escena in escenas_con_evidencia}
    palabras_totales = sum(escena.palabras for _nombre, escena in escenas_con_evidencia)
    duracion_real_total = sum(
        escena.duracion_real_segundos or 0.0 for _nombre, escena in escenas_con_evidencia
    )
    num_guiones_con_evidencia = len(guiones_con_evidencia)
    num_escenas_con_evidencia = len(escenas_con_evidencia)

    def _sin_propuesta(ppm_deducido: float | None, motivo: str) -> PropuestaPpm:
        return PropuestaPpm(
            ppm_calibrado=None,
            ppm_deducido=ppm_deducido,
            palabras_totales=palabras_totales,
            duracion_real_total_segundos=duracion_real_total,
            num_guiones_con_evidencia=num_guiones_con_evidencia,
            num_escenas_con_evidencia=num_escenas_con_evidencia,
            motivo=motivo,
        )

    if not escenas_con_evidencia:
        return _sin_propuesta(
            None,
            "ningún guion tiene todavía una toma marcada como buena: no hay tiempo real "
            "con el que calibrar.",
        )

    if num_guiones_con_evidencia < configuracion.calibracion_guiones_minimos:
        return _sin_propuesta(
            None,
            f"solo hay evidencia real de {num_guiones_con_evidencia} guion(es); hacen "
            f"falta al menos {configuracion.calibracion_guiones_minimos} para no "
            "sobreajustar a las particularidades de uno solo.",
        )

    if palabras_totales < configuracion.calibracion_palabras_minimas:
        return _sin_propuesta(
            None,
            f"solo {palabras_totales} palabras de evidencia real; hacen falta al menos "
            f"{configuracion.calibracion_palabras_minimas} para que el ppm calibrado sea "
            "fiable.",
        )

    ppm_deducido = palabras_totales / (duracion_real_total / 60)
    minimo_banda, maximo_banda = configuracion.ppm_banda_plausible
    if not (minimo_banda <= ppm_deducido <= maximo_banda):
        return _sin_propuesta(
            ppm_deducido,
            f"el ppm deducido de la evidencia real ({ppm_deducido:.0f}) cae fuera de la "
            f"banda plausible [{minimo_banda}, {maximo_banda}]: probablemente una toma mal "
            "cronometrada o marcada como buena por error. No se propone hasta revisarlo.",
        )

    return PropuestaPpm(
        ppm_calibrado=round(ppm_deducido),
        ppm_deducido=ppm_deducido,
        palabras_totales=palabras_totales,
        duracion_real_total_segundos=duracion_real_total,
        num_guiones_con_evidencia=num_guiones_con_evidencia,
        num_escenas_con_evidencia=num_escenas_con_evidencia,
        motivo=(
            f"deducido de {palabras_totales} palabras reales frente a "
            f"{duracion_real_total:.0f}s de tomas buenas, en {num_escenas_con_evidencia} "
            f"escenas de {num_guiones_con_evidencia} guiones."
        ),
    )


def _resumen_por_tipo(guiones: tuple[ContrasteGuion, ...]) -> tuple[ResumenTipoEscena, ...]:
    escenas_por_tipo: dict[str, list[ContrasteEscena]] = defaultdict(list)
    for guion in guiones:
        for escena in guion.escenas:
            if escena.duracion_real_segundos is not None:
                escenas_por_tipo[escena.tipo].append(escena)

    resumenes: list[ResumenTipoEscena] = []
    for tipo in (TIPO_APERTURA, TIPO_DESARROLLO, TIPO_CIERRE):
        escenas = escenas_por_tipo.get(tipo, [])
        if not escenas:
            continue
        resumenes.append(
            ResumenTipoEscena(
                tipo=tipo,
                num_escenas=len(escenas),
                palabras_totales=sum(escena.palabras for escena in escenas),
                duracion_estimada_total_segundos=sum(
                    escena.duracion_estimada_segundos for escena in escenas
                ),
                duracion_real_total_segundos=sum(
                    escena.duracion_real_segundos or 0.0 for escena in escenas
                ),
            )
        )
    return tuple(resumenes)


def calcular_calibracion(
    evidencias: list[EvidenciaGuion], configuracion: Configuracion | None = None
) -> InformeCalibracion:
    """Punto de entrada de R-04: contrasta estimada/objetivo/real por escena y
    en total (requisito 1), propone un ppm calibrado con la evidencia
    acumulada de todos los guiones de entrada sin aplicarlo nunca por su
    cuenta (requisito 2), y agrega la desviación por tipo de escena
    (requisito 3). La skill no la invoca sola: es Claude quien reúne la
    evidencia de los guiones ya grabados (`ResultadoTiempos` +
    `EstadoProyecto.tomas` de cada uno) y llama a esta función dentro de la
    sesión, mismo patrón que `salidas.generar_salidas_seleccionadas`."""
    configuracion = configuracion or Configuracion()
    guiones = tuple(_contraste_guion(evidencia) for evidencia in evidencias)
    return InformeCalibracion(
        guiones=guiones,
        propuesta_ppm=_propuesta_ppm(guiones, configuracion),
        resumen_por_tipo=_resumen_por_tipo(guiones),
    )
