"""Revalidacion: releer, respetar y recalcular (tarea T-17).

Cierra el ciclo iterable que T-16 dejo preparado -- validar, pedir cambios,
revalidar -- sin perder nunca un ajuste anterior. No vuelve a disenar la
canalizacion de T-08 a T-16: la reutiliza dos veces con datos distintos.

1. Sobre el guion de origen SIN TOCAR (`ResultadoParseo`, inmutable mientras
   el `.md` no cambie), recalcula los bloques de respiracion "de origen"
   (`tiempos.bloques_respiracion_marcados`, la misma reclasificacion que ya
   hacia T-12) y, con ellos, las propuestas frescas de normalizacion (T-13) y
   deteccion (T-14). `reescrituras.fusionar_con_estado` (T-15) las combina con
   el historial de `estado.json`: ninguna decision ya tomada se pierde ni se
   vuelve a proponer como pendiente (requisito 4).
2. Relee `guion-escenas.md` del disco (invariante (c) de §0.2: la edicion
   manual del dueno es autoritativa) con las mismas funciones de T-15/T-16
   (`extraer_decisiones`, `extraer_texto_bloques`, `extraer_estado_revision`):
   ninguna funcion nueva de lectura, solo composicion.
3. Materializa las particiones aceptadas (T-15) sobre los bloques de origen y
   superpone el texto editado a mano encima -- nunca al reves: una edicion
   manual jamas se sobrescribe con una propuesta o con el texto derivado.
4. Recalcula tiempos sobre ESE resultado con
   `tiempos.calcular_tiempos_desde_marcados` (nucleo de T-12, parametrizado),
   y compone el informe de incidencias (requisito 3): solo lo roto, nada de
   repetir lo que ya esta bien.

Identidad estable entre pases (requisito 2, "nunca reescribe el texto del
dueno"): una particion aceptada puede cambiar CUANTOS bloques tiene una
escena de un pase al siguiente, asi que el numero de ancla
(`escena=N indice=K`) que ve `guion-escenas.md` no es identidad fiable por si
solo. Cada bloque de origen (antes de cualquier particion) aporta su indice
0-based dentro de la escena, estable mientras el `.md` de origen no cambie;
una particion aceptada reparte ese indice en dos mitades (`'a'`/`'b'`). Esa
tripleta -- `(numero_escena, indice_original, mitad)` -- es la clave que usa
`_edicion_manual_de` para saber si el texto que el dueno dejo en un ancla es
una edicion real o solo el texto que el propio sistema habria derivado, y por
tanto no hace falta preservar como especial.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime
from typing import Any

from config import Configuracion
from deteccion import ResultadoDeteccionBloque, detectar_problemas_guion
from documento_revision import (
    MARCA_ESTADO_VALIDADO,
    extraer_estado_revision,
    extraer_texto_bloques,
)
from estado import EstadoProyecto
from normalizacion import normalizar_guion
from parser import ResultadoParseo
from reescrituras import (
    DECISION_ACEPTADA,
    FAMILIA_PARTICION_RESPIRACION,
    SEPARADOR_MITADES,
    Reescritura,
    aplicar_decisiones,
    extraer_decisiones,
    fusionar_con_estado,
    guardar_en_estado,
    recopilar_propuestas,
    texto_con_reescrituras_aceptadas,
)
from tiempos import ResultadoTiempos, bloques_respiracion_marcados, calcular_tiempos_desde_marcados
from troceo import BloqueRespiracion

# (numero_escena, indice_original 0-based en la escena, mitad de particion o None)
_Identidad = tuple[int, int, str | None]

_Marcado = tuple[BloqueRespiracion, bool, bool]
_MarcadoConIdentidad = tuple[BloqueRespiracion, bool, bool, tuple[int, str | None]]


@dataclass(frozen=True)
class Incidencia:
    """Una unica linea del informe de revalidacion (requisito 3): solo lo
    roto o inconsistente, nunca una repeticion de lo que ya esta bien."""

    numero_escena: int | None
    mensaje: str


@dataclass
class ResultadoRevalidacion:
    """Salida completa de `revalidar_guion`. `reescrituras` ya incluye las
    decisiones leidas del documento (requisito 1) fusionadas con el
    historial (requisito 4); quien llama la persiste con
    `reescrituras.guardar_en_estado` + `estado.guardar_estado`, y puede pasar
    `resultado_tiempos`/`detecciones`/`reescrituras` tal cual a
    `documento_revision.generar_documento_revision` para el siguiente ciclo."""

    resultado_tiempos: ResultadoTiempos
    detecciones: list[ResultadoDeteccionBloque]
    reescrituras: list[Reescritura]
    incidencias: list[Incidencia]
    validado: bool


def _marca_de_tiempo() -> str:
    return datetime.now(UTC).isoformat()


def _particiones_pospuestas_previas(estado: EstadoProyecto) -> dict[int, frozenset[int]]:
    """Lee de `estado.validacion` (contenedor generico reservado desde T-07,
    sin migracion nueva -- mismo patron que `estado.salidas_generadas` en
    T-30) el conjunto de bloques cuya particion quedo pospuesta por un
    conflicto con una edicion manual (hallazgo #9/P-02) EN LA PASADA
    ANTERIOR. Hace falta para interpretar el documento actual: si la pasada
    anterior poospuso la particion, el `guion-escenas.md` vigente todavia
    tiene un unico ancla `(indice_original, None)` para ese bloque, no dos
    (`'a'`/`'b'`) -- sin este conjunto, `identidad_por_ancla` asumiria por
    defecto que TODAS las particiones aceptadas ya se materializaron, lo que
    desincroniza el esquema de anclas del calculado contra el real y produce
    la duplicacion de contenido del hallazgo #14."""
    crudo = estado.validacion.get("particiones_pospuestas", {})
    return {
        int(numero_escena): frozenset(int(indice) for indice in indices)
        for numero_escena, indices in crudo.items()
    }


def _guardar_particiones_pospuestas(
    estado: EstadoProyecto, pospuestas_por_escena: dict[int, frozenset[int]]
) -> None:
    """Persiste el conjunto de bloques pospuestos de ESTA pasada (requisito 2,
    identidad estable entre pases) para que la PROXIMA pasada sepa como
    interpretar las anclas del documento que esta misma pasada va a
    regenerar. Sustituye el valor anterior por completo -- nunca se acumula
    -- porque solo importa el estado vigente, igual que `estado.validacion["ultima"]`."""
    estado.validacion["particiones_pospuestas"] = {
        str(numero_escena): sorted(indices)
        for numero_escena, indices in pospuestas_por_escena.items()
        if indices
    }


def _con_texto(bloque: BloqueRespiracion, texto: str) -> BloqueRespiracion:
    return replace(bloque, texto=texto, num_palabras=len(texto.split()))


def _reescrituras_de_bloque(
    bloque: BloqueRespiracion, reescrituras: list[Reescritura]
) -> list[Reescritura]:
    """Las reescrituras que de verdad aplican a `bloque.texto` tal cual esta
    ahora -- mismo guardian que ya usa `documento_revision._reescrituras_de_bloque`
    (T-16): comprobar `texto[inicio:fin] == original` evita aplicar una
    normalizacion calculada sobre el bloque ENTERO a una de sus dos mitades
    tras una particion aceptada, donde los offsets ya no corresponden a nada
    (T-13 y T-15 solo calculan offsets sobre el bloque de origen sin partir)."""
    return [
        reescritura
        for reescritura in reescrituras
        if reescritura.numero_escena == bloque.numero_escena
        and reescritura.linea_inicio == bloque.linea_inicio
        and reescritura.linea_fin == bloque.linea_fin
        and bloque.texto[reescritura.inicio : reescritura.fin] == reescritura.original
    ]


def _texto_derivado(bloque: BloqueRespiracion, reescrituras: list[Reescritura]) -> str:
    """El texto que el sistema propondria para `bloque` con las
    normalizaciones ya aceptadas aplicadas (T-15), sin ninguna edicion manual
    todavia superpuesta."""
    return texto_con_reescrituras_aceptadas(bloque, _reescrituras_de_bloque(bloque, reescrituras))


def _particion_aceptada_de(
    bloque: BloqueRespiracion, reescrituras: list[Reescritura]
) -> tuple[str, str] | None:
    """La particion aceptada (T-15) que corresponde exactamente a `bloque`
    sin partir, si existe, como sus dos mitades de texto."""
    for reescritura in reescrituras:
        if (
            reescritura.familia == FAMILIA_PARTICION_RESPIRACION
            and reescritura.decision == DECISION_ACEPTADA
            and reescritura.numero_escena == bloque.numero_escena
            and reescritura.linea_inicio == bloque.linea_inicio
            and reescritura.linea_fin == bloque.linea_fin
            and reescritura.original == bloque.texto
        ):
            mitad_a, _separador, mitad_b = reescritura.propuesta.partition(SEPARADOR_MITADES)
            return mitad_a, mitad_b
    return None


def _materializar_marcados(
    marcados: list[_Marcado],
    reescrituras: list[Reescritura],
    indices_con_edicion_previa_a_particion: frozenset[int] = frozenset(),
) -> list[_MarcadoConIdentidad]:
    """Aplica las particiones aceptadas (T-15) sobre los bloques "de origen"
    de una escena, conservando para cada bloque resultante su identidad
    estable -- `(indice_original, mitad)` -- y el `fin_de_parrafo`/
    `fin_de_escena` que le corresponde: la primera mitad de una particion
    nunca es fin de nada (el texto sigue en la segunda mitad), la segunda
    hereda el valor del bloque de origen sin partir.

    `indices_con_edicion_previa_a_particion` es la salvaguarda del invariante
    (c) para el cruce del hallazgo #9 (`auditoriacontinua.md`): si el dueno
    edito a mano el bloque `indice_original` ANTES de partirlo (identidad
    `(indice_original, None)`) y en esta misma revalidacion se acepta ademas
    la particion sobre ese bloque, partirlo ahora tiraria la edicion a la
    basura -- ninguna de las dos mitades resultantes conservaria la identidad
    `None` bajo la que se guardo. Se prefiere no aplicar la particion (queda
    para una revalidacion posterior, cuando ya no haya conflicto) antes que
    perder en silencio el texto del dueno."""
    resultado: list[_MarcadoConIdentidad] = []
    for indice_original, (bloque, fin_de_parrafo, fin_de_escena) in enumerate(marcados):
        particion = None
        if indice_original not in indices_con_edicion_previa_a_particion:
            particion = _particion_aceptada_de(bloque, reescrituras)
        if particion is None:
            resultado.append((bloque, fin_de_parrafo, fin_de_escena, (indice_original, None)))
            continue
        mitad_a, mitad_b = particion
        resultado.append((_con_texto(bloque, mitad_a), False, False, (indice_original, "a")))
        resultado.append(
            (_con_texto(bloque, mitad_b), fin_de_parrafo, fin_de_escena, (indice_original, "b"))
        )
    return resultado


def _incidencias_conflicto_edicion_particion(
    numero_escena: int,
    marcados: list[_Marcado],
    reescrituras: list[Reescritura],
    indices_con_edicion_previa_a_particion: frozenset[int],
) -> list[Incidencia]:
    """Avisa (nunca en silencio) del cruce del hallazgo #9: una edicion
    manual y una particion de respiracion aceptada coincidiendo sobre el
    mismo bloque en la misma revalidacion. La particion no se aplica esta
    vez; queda pendiente de una revalidacion posterior sin conflicto."""
    return [
        Incidencia(
            numero_escena,
            f"Escena {numero_escena}, bloque {indice_original}: hay una edición manual y una "
            "partición de respiración aceptada sobre el mismo bloque en esta misma "
            "revalidación; se conserva la edición manual (invariante (c) de §0.2) y la "
            "partición no se aplica todavía. Vuelve a revalidar sin tocar ese bloque si "
            "quieres que la partición se materialice.",
        )
        for indice_original in sorted(indices_con_edicion_previa_a_particion)
        if _particion_aceptada_de(marcados[indice_original][0], reescrituras) is not None
    ]


def _incidencias_bloques_fuera_de_rango(
    bloques: list[BloqueRespiracion], configuracion: Configuracion
) -> list[Incidencia]:
    return [
        Incidencia(
            bloque.numero_escena,
            f"Escena {bloque.numero_escena}, líneas {bloque.linea_inicio}-{bloque.linea_fin}: "
            f"{bloque.num_palabras} palabras, fuera del rango "
            f"[{configuracion.palabras_por_bloque_min}, {configuracion.palabras_por_bloque_max}]: "
            f'"{bloque.texto}"',
        )
        for bloque in bloques
        if not (
            configuracion.palabras_por_bloque_min
            <= bloque.num_palabras
            <= configuracion.palabras_por_bloque_max
        )
    ]


def _incidencias_escenas_sin_locucion(
    resultado: ResultadoParseo, marcados_finales_por_escena: dict[int, list[_Marcado]]
) -> list[Incidencia]:
    return [
        Incidencia(escena.numero, f"La escena {escena.numero} — {escena.titulo} no tiene locución.")
        for escena in resultado.escenas
        if not marcados_finales_por_escena.get(escena.numero)
    ]


def _incidencias_marcas_ambiguas(
    decisiones_documento: dict[str, str], reescrituras: list[Reescritura]
) -> list[Incidencia]:
    ids_conocidos = {reescritura.id for reescritura in reescrituras}
    return [
        Incidencia(
            None,
            f"Marca de decisión sobre un id de reescritura desconocido: {id_}. "
            "Puede que el bloque haya cambiado de sitio o el id se haya editado por error.",
        )
        for id_ in decisiones_documento
        if id_ not in ids_conocidos
    ]


def _incidencias_indicaciones_en_locucion(
    bloques: list[BloqueRespiracion], configuracion: Configuracion
) -> list[Incidencia]:
    marcadores = (configuracion.rotulo_locucion, *configuracion.rotulos_no_locucion)
    return [
        Incidencia(
            bloque.numero_escena,
            f"Escena {bloque.numero_escena}, líneas {bloque.linea_inicio}-{bloque.linea_fin}: "
            f'el texto de locución contiene un rótulo del guion ("{marcador}"); revisa si una '
            f'indicación no recitable se coló dentro del bloque: "{bloque.texto}"',
        )
        for bloque in bloques
        for marcador in marcadores
        if marcador in bloque.texto
    ]


def _incidencias_duracion_disparada(resultado_tiempos: ResultadoTiempos) -> list[Incidencia]:
    incidencias = [
        Incidencia(tiempo_escena.numero, tiempo_escena.aviso)
        for tiempo_escena in resultado_tiempos.escenas
        if tiempo_escena.aviso is not None
    ]
    if resultado_tiempos.aviso_total is not None:
        incidencias.append(Incidencia(None, resultado_tiempos.aviso_total))
    return incidencias


def revalidar_guion(
    resultado: ResultadoParseo,
    texto_documento: str,
    estado: EstadoProyecto,
    configuracion: Configuracion | None = None,
    diccionario: dict[str, str] | None = None,
) -> ResultadoRevalidacion:
    """Revalida un guion ya parseado (T-08) contra su `guion-escenas.md`
    editado a mano (T-16). No relee el guion de origen del disco -- eso sigue
    siendo trabajo de `entrada.py`/`parser.py` -- ni escribe nada: deja
    `estado.reescrituras`/`estado.validacion` listos en memoria y devuelve el
    resultado completo para que quien llame haga
    `estado.guardar_estado(estado, carpeta_salida)` y, si quiere, regenere
    `guion-escenas.md` con `documento_revision.generar_documento_revision`."""
    configuracion = configuracion or Configuracion()

    marcados_originales_por_escena: dict[int, list[_Marcado]] = {
        escena.numero: bloques_respiracion_marcados(escena, configuracion)
        for escena in resultado.escenas
    }
    bloques_originales = [
        bloque
        for marcados in marcados_originales_por_escena.values()
        for bloque, _fin_de_parrafo, _fin_de_escena in marcados
    ]
    detecciones_de_origen = detectar_problemas_guion(bloques_originales, configuracion)
    normalizaciones_de_origen = normalizar_guion(bloques_originales, configuracion, diccionario)
    propuestas = recopilar_propuestas(normalizaciones_de_origen, detecciones_de_origen)
    reescrituras_previas = fusionar_con_estado(estado, propuestas)

    # Estado "esperado" del documento actual: si el dueno no edito nada a
    # mano, el ancla (escena, indice) de guion-escenas.md deberia contener
    # exactamente este texto derivado. Cualquier diferencia es una edicion
    # real (invariante (c)). El esquema de anclas debe coincidir con el que
    # tenia el documento cuando se escribio -- por eso se materializa con la
    # MISMA posposicion de particiones que dejo la pasada anterior (#14),
    # nunca asumiendo que toda particion aceptada ya esta materializada.
    pospuestas_previas = _particiones_pospuestas_previas(estado)
    texto_esperado_por_ancla: dict[tuple[int, int], str] = {}
    identidad_por_ancla: dict[tuple[int, int], _Identidad] = {}
    for numero_escena, marcados in marcados_originales_por_escena.items():
        for indice, (bloque, _fp, _fe, identidad_local) in enumerate(
            _materializar_marcados(
                marcados, reescrituras_previas, pospuestas_previas.get(numero_escena, frozenset())
            ),
            start=1,
        ):
            ancla = (numero_escena, indice)
            texto_esperado_por_ancla[ancla] = _texto_derivado(bloque, reescrituras_previas)
            identidad_por_ancla[ancla] = (numero_escena, *identidad_local)

    texto_editado_por_ancla = extraer_texto_bloques(texto_documento)
    decisiones_documento = extraer_decisiones(texto_documento)
    marca_estado_documento = extraer_estado_revision(texto_documento)

    ediciones_manuales: dict[_Identidad, str] = {}
    for ancla, texto_en_documento in texto_editado_por_ancla.items():
        identidad_ancla = identidad_por_ancla.get(ancla)
        if identidad_ancla is None:
            continue  # ancla que ya no corresponde a ningun bloque conocido: se ignora
        if texto_en_documento != texto_esperado_por_ancla.get(ancla):
            ediciones_manuales[identidad_ancla] = texto_en_documento

    reescrituras_actualizadas = aplicar_decisiones(reescrituras_previas, decisiones_documento)

    marcados_finales_por_escena: dict[int, list[_Marcado]] = {}
    incidencias_conflicto_particion: list[Incidencia] = []
    pospuestas_de_esta_pasada: dict[int, frozenset[int]] = {}
    for escena in resultado.escenas:
        marcados = marcados_originales_por_escena[escena.numero]
        indices_con_edicion_previa_a_particion = frozenset(
            indice_original
            for (numero_escena_edicion, indice_original, mitad) in ediciones_manuales
            if numero_escena_edicion == escena.numero and mitad is None
        )
        incidencias_conflicto_particion.extend(
            _incidencias_conflicto_edicion_particion(
                escena.numero,
                marcados,
                reescrituras_actualizadas,
                indices_con_edicion_previa_a_particion,
            )
        )
        finales: list[_Marcado] = []
        for bloque, fin_de_parrafo, fin_de_escena, identidad in _materializar_marcados(
            marcados, reescrituras_actualizadas, indices_con_edicion_previa_a_particion
        ):
            clave_identidad = (escena.numero, *identidad)
            texto_manual = ediciones_manuales.get(clave_identidad)
            texto_final = (
                texto_manual
                if texto_manual is not None
                else _texto_derivado(bloque, reescrituras_actualizadas)
            )
            finales.append((_con_texto(bloque, texto_final), fin_de_parrafo, fin_de_escena))
        marcados_finales_por_escena[escena.numero] = finales
        pospuestas_de_esta_pasada[escena.numero] = indices_con_edicion_previa_a_particion

    resultado_tiempos = calcular_tiempos_desde_marcados(
        resultado, marcados_finales_por_escena, configuracion
    )
    bloques_finales = [
        bloque
        for marcados in marcados_finales_por_escena.values()
        for bloque, _fp, _fe in marcados
    ]
    detecciones_finales = detectar_problemas_guion(bloques_finales, configuracion)

    incidencias = [
        *_incidencias_bloques_fuera_de_rango(bloques_finales, configuracion),
        *_incidencias_escenas_sin_locucion(resultado, marcados_finales_por_escena),
        *_incidencias_marcas_ambiguas(decisiones_documento, reescrituras_actualizadas),
        *_incidencias_indicaciones_en_locucion(bloques_finales, configuracion),
        *_incidencias_duracion_disparada(resultado_tiempos),
        *incidencias_conflicto_particion,
    ]

    validado = marca_estado_documento == MARCA_ESTADO_VALIDADO
    guardar_en_estado(estado, reescrituras_actualizadas)
    _guardar_particiones_pospuestas(estado, pospuestas_de_esta_pasada)
    _registrar_validacion(estado, validado=validado, incidencias=incidencias)

    return ResultadoRevalidacion(
        resultado_tiempos=resultado_tiempos,
        detecciones=detecciones_finales,
        reescrituras=reescrituras_actualizadas,
        incidencias=incidencias,
        validado=validado,
    )


def _registrar_validacion(
    estado: EstadoProyecto, *, validado: bool, incidencias: list[Incidencia]
) -> None:
    """Deja en `estado.validacion` (contenedor reservado desde T-07, sin
    cambio de esquema) un registro con marca de tiempo por cada revalidacion
    (requisito 4), ademas de la ultima a mano para no tener que recorrer el
    historial en el caso comun."""
    registro: dict[str, Any] = {
        "marca_tiempo": _marca_de_tiempo(),
        "validado": validado,
        "incidencias": [incidencia.mensaje for incidencia in incidencias],
    }
    historial = estado.validacion.setdefault("historial", [])
    historial.append(registro)
    estado.validacion["ultima"] = registro
