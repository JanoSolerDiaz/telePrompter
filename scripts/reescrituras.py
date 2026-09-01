"""Reescrituras marcadas, aceptables y reversibles (tarea T-15).

Une las dos fuentes de propuesta de reescritura que ya existen -- la
normalizacion a forma dicha (T-13, `normalizacion.Normalizacion`) y la
particion sugerida para una frase sin punto de respiracion (T-14,
`deteccion.Aviso.particion_sugerida`) -- en un unico tipo, `Reescritura`, con
un ciclo de vida completo: proponer, marcar en texto legible, leer la
decision que el dueno escribe a mano, aplicarla o no, y deshacerla en bloque.

Alcance (decision del dueno, §0.2): solo forma dicha (T-13) y respiracion
(la particion de T-14). Las demas familias de avisos de T-14 (cacofonia,
trabalenguas, anglicismo, estructura dificil) nunca generan `Reescritura` --
se quedan en aviso, tal como fija esa tarea.

Formato de marca (requisito 1): cada reescritura es un bloque de texto con
`original`, `propuesta` y `motivo` visibles a la vez, delimitado por
comentarios HTML con su identificador estable (`formatear_reescritura`).
Ese formato es intencionadamente independiente de la estructura completa de
`guion-escenas.md` (T-16, todavia pendiente): es el bloque que T-16 insertara
dentro de cada escena, no el documento entero -- mismo patron que T-02/T-04/
T-05/T-07 aplicaron a infraestructura sin productor/consumidor final
todavia.

Decision individual (requisito 2): una sola palabra en mayusculas
(`PENDIENTE`/`ACEPTAR`/`RECHAZAR`) que el dueno sobrescribe a mano sobre la
linea "Decision"; `extraer_decisiones` la lee de vuelta con una busqueda
tolerante a mayusculas/espacios, no con una posicion de columna fragil.

Persistencia (requisito 3): `Reescritura` conserva siempre `original` y
`propuesta` a la vez (invariante (b) de §0.2); `fusionar_con_estado` nunca
descarta una reescritura ya registrada en `estado.json`, aunque el guion
cambie y deje de generarla en la pasada actual.

Revalidacion (requisito 4): `fusionar_con_estado` conserva la decision ya
tomada para una reescritura que ya existia (identificada por `id`, no por
posicion) y anade como `pendiente` solo las que son nuevas.

Deshacer global (requisito 5): `revertir_reescrituras` fuerza a `rechazada`
todas las reescrituras de una escena o del guion completo, sin perder el
original.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass, replace
from typing import Any

from deteccion import FAMILIA_SIN_PUNTO_RESPIRACION, Aviso, ResultadoDeteccionBloque
from estado import EstadoProyecto
from normalizacion import Normalizacion, ResultadoNormalizacionBloque, aplicar_normalizaciones
from troceo import BloqueRespiracion

FAMILIA_PARTICION_RESPIRACION = "particion_respiracion"

DECISION_PENDIENTE = "pendiente"
DECISION_ACEPTADA = "aceptada"
DECISION_RECHAZADA = "rechazada"

_SEPARADOR_MITADES = "\n\n"

_MARCA_PENDIENTE = "PENDIENTE"
_MARCA_ACEPTAR = "ACEPTAR"
_MARCA_RECHAZAR = "RECHAZAR"

_MARCA_A_DECISION = {
    _MARCA_PENDIENTE: DECISION_PENDIENTE,
    _MARCA_ACEPTAR: DECISION_ACEPTADA,
    _MARCA_RECHAZAR: DECISION_RECHAZADA,
}
_DECISION_A_MARCA = {valor: clave for clave, valor in _MARCA_A_DECISION.items()}


@dataclass(frozen=True)
class Reescritura:
    """Una propuesta de reescritura con su decision (T-15).

    `id` identifica la ocasion concreta (escena + posicion + familia +
    texto original), no el contenido de la propuesta: si una regla mejora y
    cambia la `propuesta` sugerida para el mismo `original` en el mismo
    sitio, sigue siendo "la misma" reescritura a efectos de revalidacion
    (requisito 4). `inicio`/`fin` son offsets de caracter dentro de
    `BloqueRespiracion.texto`, igual que en `Normalizacion` (T-13); para una
    particion (T-14) cubren el bloque entero.
    """

    id: str
    numero_escena: int
    linea_inicio: int
    linea_fin: int
    familia: str
    motivo: str
    original: str
    propuesta: str
    inicio: int
    fin: int
    decision: str = DECISION_PENDIENTE


def _calcular_id(
    numero_escena: int, linea_inicio: int, linea_fin: int, familia: str,
    inicio: int, fin: int, original: str,
) -> str:
    clave = f"{numero_escena}|{linea_inicio}|{linea_fin}|{familia}|{inicio}|{fin}|{original}"
    return hashlib.sha256(clave.encode("utf-8")).hexdigest()[:16]


def _reescritura_desde_normalizacion(
    bloque: BloqueRespiracion, normalizacion: Normalizacion
) -> Reescritura:
    id_ = _calcular_id(
        bloque.numero_escena, bloque.linea_inicio, bloque.linea_fin,
        normalizacion.familia, normalizacion.inicio, normalizacion.fin, normalizacion.original,
    )
    return Reescritura(
        id=id_,
        numero_escena=bloque.numero_escena,
        linea_inicio=bloque.linea_inicio,
        linea_fin=bloque.linea_fin,
        familia=normalizacion.familia,
        motivo=normalizacion.motivo,
        original=normalizacion.original,
        propuesta=normalizacion.propuesta,
        inicio=normalizacion.inicio,
        fin=normalizacion.fin,
    )


def _reescritura_desde_particion(bloque: BloqueRespiracion, aviso: Aviso) -> Reescritura | None:
    """Solo produce `Reescritura` la familia
    `sin_punto_respiracion` con particion sugerida (unica excepcion de T-14,
    requisito 6). El resto de familias de T-14 nunca llegan aqui con
    `admite_particion=True`, pero se comprueba explicitamente para no atarse
    a esa invariante ajena sin verificarla."""
    if aviso.familia != FAMILIA_SIN_PUNTO_RESPIRACION:
        return None
    if not aviso.admite_particion or aviso.particion_sugerida is None:
        return None
    mitad_a, mitad_b = aviso.particion_sugerida
    propuesta = _SEPARADOR_MITADES.join((mitad_a, mitad_b))
    id_ = _calcular_id(
        bloque.numero_escena, bloque.linea_inicio, bloque.linea_fin,
        FAMILIA_PARTICION_RESPIRACION, 0, len(bloque.texto), bloque.texto,
    )
    return Reescritura(
        id=id_,
        numero_escena=bloque.numero_escena,
        linea_inicio=bloque.linea_inicio,
        linea_fin=bloque.linea_fin,
        familia=FAMILIA_PARTICION_RESPIRACION,
        motivo=aviso.mensaje,
        original=bloque.texto,
        propuesta=propuesta,
        inicio=0,
        fin=len(bloque.texto),
    )


def recopilar_propuestas(
    resultados_normalizacion: list[ResultadoNormalizacionBloque],
    resultados_deteccion: list[ResultadoDeteccionBloque] | None = None,
) -> list[Reescritura]:
    """Une las propuestas de T-13 (normalizacion) y T-14 (particion por falta
    de punto de respiracion) en la lista unica de `Reescritura` que gobierna
    esta tarea. `resultados_deteccion` es opcional porque una llamada puede
    querer solo forma dicha sin volver a ejecutar el detector."""
    propuestas: list[Reescritura] = []
    for resultado_normalizacion in resultados_normalizacion:
        for normalizacion in resultado_normalizacion.normalizaciones:
            propuestas.append(
                _reescritura_desde_normalizacion(resultado_normalizacion.bloque, normalizacion)
            )
    for resultado_deteccion in resultados_deteccion or []:
        for aviso in resultado_deteccion.avisos:
            reescritura = _reescritura_desde_particion(resultado_deteccion.bloque, aviso)
            if reescritura is not None:
                propuestas.append(reescritura)
    return propuestas


# --- Formato marcado en texto (requisitos 1 y 2) ------------------------------------

_PATRON_BLOQUE = re.compile(
    r"<!-- reescritura id=(?P<id>[0-9a-f]+) -->(?P<cuerpo>.*?)<!-- /reescritura -->",
    re.DOTALL,
)
_PATRON_DECISION = re.compile(
    r"Decisi[oó]n\W*(ACEPTAR|RECHAZAR|PENDIENTE)", re.IGNORECASE
)


def formatear_reescritura(reescritura: Reescritura) -> str:
    """Bloque de texto legible con original y propuesta a la vez (requisito
    1) y una marca de decision en una sola palabra (requisito 2): el dueno la
    sobrescribe con `ACEPTAR`/`RECHAZAR` a mano, sin sintaxis fragil. La
    marca refleja la decision actual (`ACEPTAR`/`RECHAZAR` si ya estaba
    decidida), para que revisar el documento muestre lo que ya se eligio."""
    marca = _DECISION_A_MARCA[reescritura.decision]
    return (
        f"<!-- reescritura id={reescritura.id} -->\n"
        f"> **Original:** {reescritura.original}\n"
        f"> **Propuesta:** {reescritura.propuesta}\n"
        f"> **Motivo:** {reescritura.motivo}\n"
        f"> **Decisión:** {marca}\n"
        "<!-- /reescritura -->"
    )


def extraer_decisiones(texto: str) -> dict[str, str]:
    """Lee de vuelta, de un texto que contiene bloques `formatear_reescritura`
    (editados o no a mano por el dueno), la decision marcada para cada `id`.
    Un bloque sin marca reconocible se ignora (no se puede aplicar ninguna
    decision sin ambiguedad) en vez de levantar un error: el dueno puede
    haber tocado el bloque de formas que esta funcion no anticipa, y no es
    su culpa que quede sin decision."""
    decisiones: dict[str, str] = {}
    for coincidencia in _PATRON_BLOQUE.finditer(texto):
        marca_decision = _PATRON_DECISION.search(coincidencia.group("cuerpo"))
        if marca_decision is None:
            continue
        decisiones[coincidencia.group("id")] = _MARCA_A_DECISION[marca_decision.group(1).upper()]
    return decisiones


def aplicar_decisiones(
    reescrituras: list[Reescritura], decisiones: dict[str, str]
) -> list[Reescritura]:
    """Devuelve una copia de `reescrituras` con la decision de `decisiones`
    aplicada a las que tienen `id` presente ahi; las demas conservan su
    decision anterior sin cambios."""
    return [
        replace(reescritura, decision=decisiones[reescritura.id])
        if reescritura.id in decisiones
        else reescritura
        for reescritura in reescrituras
    ]


# --- Persistencia en estado.json (requisitos 3 y 4) ----------------------------------


def _reescritura_a_dict(reescritura: Reescritura) -> dict[str, Any]:
    return asdict(reescritura)


def _reescritura_desde_dict(datos: dict[str, Any]) -> Reescritura:
    return Reescritura(**datos)


def fusionar_con_estado(
    estado: EstadoProyecto, propuestas: list[Reescritura]
) -> list[Reescritura]:
    """Combina las propuestas recalculadas en esta pasada con las decisiones
    ya guardadas en `estado.reescrituras` (requisito 4): una propuesta cuyo
    `id` ya existia conserva la decision guardada -- no se vuelve a proponer
    como pendiente aunque la regla que la genero vuelva a dispararse -- y una
    propuesta nueva se anade como `pendiente`. Ninguna reescritura ya
    registrada desaparece (invariante (b)), ni siquiera si el guion cambio y
    esta pasada ya no la genera: sigue en el resultado con su decision
    intacta."""
    existentes = {
        datos["id"]: _reescritura_desde_dict(datos) for datos in estado.reescrituras
    }
    resultado: list[Reescritura] = []
    ids_vistos: set[str] = set()
    for propuesta in propuestas:
        resultado.append(existentes.get(propuesta.id, propuesta))
        ids_vistos.add(propuesta.id)
    for id_, reescritura in existentes.items():
        if id_ not in ids_vistos:
            resultado.append(reescritura)
    return resultado


def guardar_en_estado(estado: EstadoProyecto, reescrituras: list[Reescritura]) -> EstadoProyecto:
    """Persiste `reescrituras` (ya fusionadas con `fusionar_con_estado`) en
    `estado.reescrituras`. Quien llama sigue siendo responsable de invocar
    `estado.guardar_estado` para escribirlo a disco."""
    estado.reescrituras = [_reescritura_a_dict(reescritura) for reescritura in reescrituras]
    return estado


def pendientes(reescrituras: list[Reescritura]) -> list[Reescritura]:
    """Las reescrituras que todavia esperan una decision del dueno -- las
    unicas que hace falta volver a mostrar (requisito 4)."""
    return [
        reescritura for reescritura in reescrituras if reescritura.decision == DECISION_PENDIENTE
    ]


# --- Aplicacion sobre el texto y el troceo (requisitos 1 y 6 de T-14) ----------------


def texto_con_reescrituras_aceptadas(
    bloque: BloqueRespiracion, reescrituras_bloque: list[Reescritura]
) -> str:
    """El texto de `bloque` con las reescrituras de normalizacion aceptadas
    ya aplicadas (las rechazadas o pendientes dejan el original intacto,
    invariante (b)). Las de la familia `particion_respiracion` no son un
    reemplazo de caracteres dentro del bloque -- se materializan aparte con
    `aplicar_particiones_aceptadas`, que sustituye el bloque completo por
    dos -- asi que se excluyen aqui."""
    normalizaciones = [
        Normalizacion(
            reescritura.original, reescritura.propuesta, reescritura.familia,
            reescritura.motivo, reescritura.inicio, reescritura.fin,
        )
        for reescritura in reescrituras_bloque
        if reescritura.decision == DECISION_ACEPTADA
        and reescritura.familia != FAMILIA_PARTICION_RESPIRACION
        and reescritura.numero_escena == bloque.numero_escena
        and reescritura.linea_inicio == bloque.linea_inicio
        and reescritura.linea_fin == bloque.linea_fin
    ]
    return aplicar_normalizaciones(bloque.texto, normalizaciones)


def aplicar_particion_aceptada(
    bloques: list[BloqueRespiracion], reescritura: Reescritura
) -> list[BloqueRespiracion]:
    """Materializa una particion aceptada (T-14 requisito 6, "aplicarla de
    verdad sigue siendo alcance de T-15"): sustituye, dentro de `bloques`, el
    `BloqueRespiracion` cuyo texto coincide exactamente con el `original` de
    la reescritura por los dos bloques resultantes de partirlo. Ambos heredan
    `numero_escena`/`linea_inicio`/`linea_fin`/`corte_forzado` del bloque de
    origen -- el troceo (T-11) no trackea posicion mas fina que el bloque, y
    esta particion no vuelve a pasar por el algoritmo de corte de T-11, asi
    que no hay una `corte_forzado` mas precisa que calcular. No hace nada si
    la reescritura no es una particion aceptada, o si el bloque de origen ya
    no esta presente (p. ej. porque el guion cambio)."""
    if reescritura.familia != FAMILIA_PARTICION_RESPIRACION:
        return bloques
    if reescritura.decision != DECISION_ACEPTADA:
        return bloques
    mitad_a, _, mitad_b = reescritura.propuesta.partition(_SEPARADOR_MITADES)
    resultado: list[BloqueRespiracion] = []
    for bloque in bloques:
        coincide = (
            bloque.numero_escena == reescritura.numero_escena
            and bloque.linea_inicio == reescritura.linea_inicio
            and bloque.linea_fin == reescritura.linea_fin
            and bloque.texto == reescritura.original
        )
        if not coincide:
            resultado.append(bloque)
            continue
        for mitad in (mitad_a, mitad_b):
            resultado.append(
                replace(bloque, texto=mitad, num_palabras=len(mitad.split()))
            )
    return resultado


def aplicar_particiones_aceptadas(
    bloques: list[BloqueRespiracion], reescrituras: list[Reescritura]
) -> list[BloqueRespiracion]:
    """Aplica `aplicar_particion_aceptada` para cada reescritura de la lista,
    en orden: cada particion opera sobre el resultado de la anterior, asi que
    dos particiones aceptadas sobre bloques distintos del mismo guion se
    materializan ambas."""
    resultado = bloques
    for reescritura in reescrituras:
        resultado = aplicar_particion_aceptada(resultado, reescritura)
    return resultado


# --- Deshacer global (requisito 5) ---------------------------------------------------


def revertir_reescrituras(
    reescrituras: list[Reescritura], numero_escena: int | None = None
) -> list[Reescritura]:
    """Fuerza a `rechazada` todas las reescrituras (o solo las de
    `numero_escena`, si se indica) sin perder el original -- invariante (b):
    `Reescritura.original` sigue en el resultado, solo cambia `decision`."""
    return [
        replace(reescritura, decision=DECISION_RECHAZADA)
        if numero_escena is None or reescritura.numero_escena == numero_escena
        else reescritura
        for reescritura in reescrituras
    ]
