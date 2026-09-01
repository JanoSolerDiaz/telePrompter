"""Troceo en bloques de respiracion (tarea T-11).

Produce la unidad de resaltado de todas las salidas: fragmentos de locucion de
`palabras_por_bloque_min`-`palabras_por_bloque_max` palabras (config.py) que se
puedan decir de una respiracion, a partir de los bloques `locucion` que ya
entrega el clasificador (T-09).

Cortar por prioridad (requisito 1): puntuacion fuerte (`.?!;:`) primero; si un
tramo resultante sigue por encima del maximo, se subdivide por puntuacion
debil (`,`, guion, apertura de parentesis/interrogacion/exclamacion); si
sigue sin caber, por conjunciones y nexos (`y`, `o`, `pero`, `que`, `porque`,
`aunque`, `mientras`); y en ultimo lugar por limites de sintagma (antes de una
preposicion o un determinante). Un tramo que no necesita cortarse (ya esta
dentro del maximo) no se toca aunque contenga puntuacion o nexos: la funcion
`_refinar` solo desciende de nivel cuando el nivel anterior no basta.

Un corte que no puede evitar superar el maximo con ninguna senal natural se
fuerza al punto mas cercano al objetivo (`_forzar_particion`), registrando
`corte_forzado=True` (requisito 3). Los tramos por debajo del minimo se
funden con el vecino mas afin -- el que deja el bloque combinado mas cerca
del objetivo -- en `_fusionar_bajo_minimo`, salvo que la locucion completa ya
sea mas corta que el minimo (entonces no hay vecino con quien fundir).

Ningun corte, ni siquiera uno forzado, puede caer dentro de una cifra, una
fecha o una sigla puenteada (requisito 2): `_gaps_protegidos` marca esas
posiciones como no cortables antes de que cualquier nivel de prioridad las
proponga. La normalizacion a forma dicha (T-13) no existe todavia, asi que no
hay "expresion normalizada por T-13" que proteger aun; queda para cuando esa
tarea aterrice.

Determinista (requisito 5): ninguna eleccion depende de aleatoriedad ni de
orden de iteracion no determinista (los conjuntos de indices se recorren
siempre ordenados), asi que la misma entrada produce siempre el mismo troceo.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from clasificador import TIPO_LOCUCION, BloqueClasificado, clasificar_escena
from config import Configuracion
from parser import ResultadoParseo

_FUERTE, _DEBIL, _NEXO, _SINTAGMA = 0, 1, 2, 3
_ORDEN_PRIORIDAD: tuple[int, ...] = (_FUERTE, _DEBIL, _NEXO, _SINTAGMA)

_PUNTUACION_FUERTE = frozenset(".?!;:")
_PUNTUACION_DEBIL = frozenset(",—-")
_APERTURAS_DEBILES = frozenset("(¿¡")
_CIERRES_A_IGNORAR = "\"'”»)]"

# Requisito 1: exactamente los nexos que enumera la tarea, ni mas ni menos.
_NEXOS = frozenset({"y", "o", "pero", "que", "porque", "aunque", "mientras"})
_PREPOSICIONES = frozenset(
    {
        "a", "ante", "bajo", "con", "contra", "de", "desde", "en", "entre",
        "hacia", "hasta", "para", "por", "según", "sin", "sobre", "tras",
    }
)
_DETERMINANTES = frozenset(
    {
        "el", "la", "los", "las", "un", "una", "unos", "unas", "su", "sus",
        "este", "esta", "estos", "estas", "ese", "esa", "esos", "esas",
    }
)

_PATRON_NUCLEO_ALFABETICO = re.compile(r"[^\W\d_]+", re.UNICODE)
_PATRON_MARCA_CITA = re.compile(r"^>\s?")

# Requisito 2: expresiones que nunca se parten, aunque su corte quede a mano
# en un nivel de prioridad. Cubren los casos que de verdad aparecen en
# locucion (numero+unidad, fecha con "de", sigla puenteada); no hay una
# expresion normalizada por T-13 todavia porque esa tarea no existe aun.
_PATRON_FECHA = re.compile(
    r"\b\d{1,2}\s+de\s+[A-Za-zÁÉÍÓÚáéíóúÑñ]+(?:\s+de\s+\d{3,4})?\b"
)
_PATRON_NUMERO_UNIDAD = re.compile(r"\b\d{1,3}(?:[.,]\d+)*\s*(?:%|€|\$|º|ª|°)")
_PATRON_SIGLA_PUNTEADA = re.compile(r"(?:\b[A-ZÁÉÍÓÚÑ]\.\s*){2,}")
_PATRONES_PROTEGIDOS = (_PATRON_FECHA, _PATRON_NUMERO_UNIDAD, _PATRON_SIGLA_PUNTEADA)


@dataclass
class BloqueRespiracion:
    """Un fragmento de locucion listo para resaltar de una respiracion.

    `linea_inicio`/`linea_fin` son las del bloque `locucion` de origen
    (T-09): el troceo no trackea posicion palabra a palabra, la misma
    granularidad que ya usa `BloqueClasificado` para motivo/senal.
    """

    texto: str
    numero_escena: int
    linea_inicio: int
    linea_fin: int
    num_palabras: int
    corte_forzado: bool


def _texto_plano(contenido: str) -> str:
    """Quita la marca de cita de bloque (`> `) y reune las lineas en una sola.

    El troceo trabaja sobre las palabras que se van a decir, no sobre la
    sintaxis Markdown que las envuelve; la normalizacion de espacios (varias
    lineas de cita pasan a un unico espacio) no cambia ninguna palabra.
    """
    lineas = (_PATRON_MARCA_CITA.sub("", linea).strip() for linea in contenido.split("\n"))
    return " ".join(linea for linea in lineas if linea)


def categoria_puntuacion_final(texto: str) -> str:
    """Categoria de la puntuacion final de un fragmento ya trabajado por el troceo.

    Publica (no `_`) porque T-12 (motor de tiempos) la reutiliza para decidir la
    pausa aplicable tras cada bloque de respiracion (coma/punto/ninguna; fin de
    parrafo y fin de escena los decide T-12 por posicion, no por puntuacion).
    Devuelve `'fuerte'`, `'debil'` o `'ninguna'`, reusando los mismos conjuntos de
    caracteres que ya usa el propio troceo para decidir donde cortar.
    """
    nucleo = texto.rstrip().rstrip(_CIERRES_A_IGNORAR)
    if nucleo and nucleo[-1] in _PUNTUACION_FUERTE:
        return "fuerte"
    if nucleo and nucleo[-1] in _PUNTUACION_DEBIL:
        return "debil"
    return "ninguna"


def _nucleo_alfabetico(palabra: str) -> str:
    coincidencias = _PATRON_NUCLEO_ALFABETICO.findall(palabra.lower())
    return coincidencias[0] if coincidencias else ""


def _prioridad_gap(palabras: list[str], indice: int) -> int | None:
    """Prioridad del corte entre `palabras[indice]` y `palabras[indice + 1]`."""
    actual = palabras[indice]
    siguiente = palabras[indice + 1]

    nucleo_actual = actual.rstrip(_CIERRES_A_IGNORAR)
    if nucleo_actual and nucleo_actual[-1] in _PUNTUACION_FUERTE:
        return _FUERTE
    if nucleo_actual and nucleo_actual[-1] in _PUNTUACION_DEBIL:
        return _DEBIL
    if siguiente[:1] in _APERTURAS_DEBILES:
        return _DEBIL

    nucleo_siguiente = _nucleo_alfabetico(siguiente)
    if nucleo_siguiente in _NEXOS:
        return _NEXO
    if nucleo_siguiente in _PREPOSICIONES or nucleo_siguiente in _DETERMINANTES:
        return _SINTAGMA
    return None


def _calcular_prioridades(palabras: list[str]) -> dict[int, int]:
    prioridades = {}
    for indice in range(len(palabras) - 1):
        prioridad = _prioridad_gap(palabras, indice)
        if prioridad is not None:
            prioridades[indice] = prioridad
    return prioridades


def _gaps_protegidos(texto: str, palabras_spans: list[tuple[str, int, int]]) -> set[int]:
    """Indices de corte prohibidos porque caerian dentro de una cifra, fecha
    o sigla que cruza varias palabras (requisito 2)."""
    spans_protegidos = [
        (coincidencia.start(), coincidencia.end())
        for patron in _PATRONES_PROTEGIDOS
        for coincidencia in patron.finditer(texto)
    ]
    if not spans_protegidos:
        return set()
    prohibidos = set()
    for indice in range(len(palabras_spans) - 1):
        fin_actual = palabras_spans[indice][2]
        inicio_siguiente = palabras_spans[indice + 1][1]
        for inicio_p, fin_p in spans_protegidos:
            if inicio_p < inicio_siguiente and fin_p > fin_actual:
                prohibidos.add(indice)
                break
    return prohibidos


def _forzar_particion(
    inicio: int, fin: int, protegidos: set[int], configuracion: Configuracion
) -> list[tuple[int, int, bool]]:
    """Ultimo recurso (requisito 3): sin ninguna senal natural disponible,
    corta lo mas cerca posible del objetivo, saltandose siempre los gaps
    protegidos. Si ni eso es posible (un span protegido mas largo que el
    maximo configurado), el tramo se deja entero, por encima del maximo."""
    segmentos: list[tuple[int, int, bool]] = []
    cursor = inicio
    while fin - cursor > configuracion.palabras_por_bloque_max:
        objetivo_abs = cursor + configuracion.palabras_por_bloque_objetivo
        limite = min(fin - 1, cursor + configuracion.palabras_por_bloque_max)
        ventana = [g for g in range(cursor, limite) if g not in protegidos]
        if not ventana:
            break
        elegido = min(ventana, key=lambda g: abs((g + 1) - objetivo_abs))
        segmentos.append((cursor, elegido + 1, True))
        cursor = elegido + 1
    segmentos.append((cursor, fin, bool(segmentos)))
    return segmentos


def _refinar(
    inicio: int,
    fin: int,
    prioridades: dict[int, int],
    protegidos: set[int],
    configuracion: Configuracion,
    niveles_restantes: tuple[int, ...],
) -> list[tuple[int, int, bool]]:
    if fin - inicio <= configuracion.palabras_por_bloque_max:
        return [(inicio, fin, False)]
    if not niveles_restantes:
        return _forzar_particion(inicio, fin, protegidos, configuracion)

    nivel, *resto = niveles_restantes
    nivel_actual = nivel
    niveles_siguientes = tuple(resto)
    candidatos = sorted(
        g
        for g, prioridad in prioridades.items()
        if prioridad == nivel_actual and inicio <= g < fin - 1 and g not in protegidos
    )
    if not candidatos:
        return _refinar(inicio, fin, prioridades, protegidos, configuracion, niveles_siguientes)

    segmentos: list[tuple[int, int]] = []
    cursor = inicio
    while cursor < fin:
        restante = fin - cursor
        if restante <= configuracion.palabras_por_bloque_max:
            segmentos.append((cursor, fin))
            break
        objetivo_abs = cursor + configuracion.palabras_por_bloque_objetivo
        limite = min(fin - 1, cursor + configuracion.palabras_por_bloque_max)
        ventana = [g for g in candidatos if cursor <= g < limite]
        if ventana:
            elegido = min(ventana, key=lambda g: abs((g + 1) - objetivo_abs))
        else:
            # Ningun candidato de este nivel cabe dentro del maximo desde `cursor`
            # (el siguiente esta mas lejos). En vez de renunciar a este nivel para
            # todo lo que queda de texto -- lo que arrastraria el resto entero del
            # parrafo hasta el nivel de prioridad forzado --, se usa el candidato
            # mas cercano por delante aunque el tramo resultante supere el maximo:
            # ese tramo de sobra se refina despues con el siguiente nivel de
            # prioridad (recursion mas abajo), y el resto del texto sigue
            # intentando este mismo nivel desde el nuevo cursor.
            candidatos_adelante = [g for g in candidatos if g >= cursor]
            if not candidatos_adelante:
                segmentos.append((cursor, fin))
                break
            elegido = min(candidatos_adelante)
        segmentos.append((cursor, elegido + 1))
        cursor = elegido + 1

    resultado: list[tuple[int, int, bool]] = []
    for sub_inicio, sub_fin in segmentos:
        if sub_fin - sub_inicio > configuracion.palabras_por_bloque_max:
            resultado.extend(
                _refinar(
                    sub_inicio, sub_fin, prioridades, protegidos, configuracion, niveles_siguientes
                )
            )
        else:
            resultado.append((sub_inicio, sub_fin, False))
    return resultado


def _dividir_fusion(
    inicio: int,
    fin: int,
    prioridades: dict[int, int],
    protegidos: set[int],
    configuracion: Configuracion,
    forzado: bool,
) -> list[tuple[int, int, bool]]:
    """Reparte el resultado de fundir un tramo corto con su vecino cuando la
    union supera el maximo: nunca se deja un bloque fusionado por encima del
    maximo pudiendo evitarlo repartiendolo en dos, con el mismo orden de
    prioridad de corte que el resto del troceo (requisito 1), eligiendo entre
    los candidatos validos el mas cercano al punto medio."""
    minimo, maximo = configuracion.palabras_por_bloque_min, configuracion.palabras_por_bloque_max
    if fin - inicio <= maximo:
        return [(inicio, fin, forzado)]

    # Un punto de corte valido deja ambos lados dentro de [minimo, maximo].
    rango_valido = range(max(inicio + minimo, fin - maximo), min(fin - minimo, inicio + maximo) + 1)
    objetivo_punto = (inicio + fin) / 2

    punto = None
    for nivel in _ORDEN_PRIORIDAD:
        candidatos = [
            g + 1
            for g, prioridad in prioridades.items()
            if prioridad == nivel and g not in protegidos and (g + 1) in rango_valido
        ]
        if candidatos:
            punto = min(candidatos, key=lambda p: abs(p - objetivo_punto))
            break
    if punto is None:
        sin_proteger = [p for p in rango_valido if (p - 1) not in protegidos]
        punto = (
            min(sin_proteger, key=lambda p: abs(p - objetivo_punto))
            if sin_proteger
            else round(objetivo_punto)
        )
    return [(inicio, punto, forzado), (punto, fin, forzado)]


def _fusionar_bajo_minimo(
    segmentos: list[tuple[int, int, bool]],
    prioridades: dict[int, int],
    protegidos: set[int],
    configuracion: Configuracion,
) -> list[tuple[int, int, bool]]:
    """Funde cada tramo por debajo del minimo con el vecino mas afin --el que
    deja el bloque combinado mas cerca del objetivo-- hasta que ninguno quede
    corto (requisito 3), salvo que solo quede un tramo (la locucion completa
    es mas corta que el minimo: no hay vecino con quien fundir). Si la union
    supera el maximo, `_dividir_fusion` la reparte en dos en vez de dejar un
    bloque de mas de `palabras_por_bloque_max` palabras pudiendo evitarlo."""
    resultado = list(segmentos)
    cambiado = True
    while cambiado and len(resultado) > 1:
        cambiado = False
        for indice, (inicio, fin, forzado) in enumerate(resultado):
            if fin - inicio >= configuracion.palabras_por_bloque_min:
                continue
            vecinos = [j for j in (indice - 1, indice + 1) if 0 <= j < len(resultado)]

            def coste(vecino: int, _inicio: int = inicio, _fin: int = fin) -> tuple[int, int]:
                # Primero minimizar cuanto se pasa del maximo (preferir un vecino
                # que quepa sin sobrepasarlo, si alguno lo permite); solo como
                # desempate, acercarse al objetivo. "Mas afin" no puede significar
                # "mas cerca del objetivo" a secas si eso elige un vecino que se
                # pasa del maximo pudiendo evitarlo con el otro.
                otro_inicio, otro_fin, _ = resultado[vecino]
                nuevo_inicio, nuevo_fin = min(_inicio, otro_inicio), max(_fin, otro_fin)
                tamano = nuevo_fin - nuevo_inicio
                exceso = max(0, tamano - configuracion.palabras_por_bloque_max)
                return (exceso, abs(tamano - configuracion.palabras_por_bloque_objetivo))

            elegido = min(vecinos, key=coste)
            otro_inicio, otro_fin, forzado_vecino = resultado[elegido]
            nuevo_inicio, nuevo_fin = min(inicio, otro_inicio), max(fin, otro_fin)
            fusionados = _dividir_fusion(
                nuevo_inicio,
                nuevo_fin,
                prioridades,
                protegidos,
                configuracion,
                forzado or forzado_vecino,
            )
            pos_a, pos_b = sorted((indice, elegido))
            resultado[pos_a : pos_b + 1] = fusionados
            cambiado = True
            break
    return resultado


def trocear_texto(
    texto: str, configuracion: Configuracion | None = None
) -> list[tuple[str, bool]]:
    """Trocea un texto de locucion ya "aplanado" (sin marcas de cita) en
    fragmentos de respiracion. Devuelve pares `(texto_fragmento, corte_forzado)`.

    Funcion de bajo nivel, testeable sin pasar por `BloqueClasificado`; es la
    que usan `trocear_bloque_locucion` y `trocear_guion`.
    """
    configuracion = configuracion or Configuracion()
    palabras_spans = [(m.group(), m.start(), m.end()) for m in re.finditer(r"\S+", texto)]
    if not palabras_spans:
        return []

    palabras = [palabra for palabra, _inicio, _fin in palabras_spans]
    protegidos = _gaps_protegidos(texto, palabras_spans)
    prioridades = _calcular_prioridades(palabras)

    segmentos = _refinar(0, len(palabras), prioridades, protegidos, configuracion, _ORDEN_PRIORIDAD)
    segmentos = _fusionar_bajo_minimo(segmentos, prioridades, protegidos, configuracion)

    return [(" ".join(palabras[inicio:fin]), forzado) for inicio, fin, forzado in segmentos]


def trocear_bloque_locucion(
    bloque: BloqueClasificado,
    numero_escena: int,
    configuracion: Configuracion | None = None,
) -> list[BloqueRespiracion]:
    """Trocea un `BloqueClasificado` de tipo `locucion` (T-09) en bloques de
    respiracion, con su referencia a la escena y a la posicion de origen."""
    if bloque.tipo != TIPO_LOCUCION:
        mensaje = (
            f"trocear_bloque_locucion solo procesa bloques '{TIPO_LOCUCION}', "
            f"recibido '{bloque.tipo}'"
        )
        raise ValueError(mensaje)
    configuracion = configuracion or Configuracion()
    texto_plano = _texto_plano(bloque.contenido)
    return [
        BloqueRespiracion(
            texto=texto_fragmento,
            numero_escena=numero_escena,
            linea_inicio=bloque.linea_inicio,
            linea_fin=bloque.linea_fin,
            num_palabras=len(texto_fragmento.split()),
            corte_forzado=corte_forzado,
        )
        for texto_fragmento, corte_forzado in trocear_texto(texto_plano, configuracion)
    ]


def trocear_guion(
    resultado: ResultadoParseo, configuracion: Configuracion | None = None
) -> list[BloqueRespiracion]:
    """Trocea toda la locucion de un guion ya parseado (T-08) escena a escena.

    Reclasifica cada escena con el clasificador de T-09 en vez de recibir un
    `ResultadoClasificacion` ya construido: `BloqueClasificado` no lleva el
    numero de escena (esa granularidad vive en `Escena`), y clasificar de
    nuevo escena a escena evita anadir un campo a T-09 solo para este caso.
    """
    configuracion = configuracion or Configuracion()
    bloques_respiracion: list[BloqueRespiracion] = []
    for escena in resultado.escenas:
        for bloque in clasificar_escena(escena, configuracion):
            if bloque.tipo != TIPO_LOCUCION:
                continue
            bloques_respiracion.extend(
                trocear_bloque_locucion(bloque, escena.numero, configuracion)
            )
    return bloques_respiracion
