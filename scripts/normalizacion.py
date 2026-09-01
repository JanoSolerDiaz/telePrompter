"""Normalizacion a forma dicha (tarea T-13): que el texto de la tarjeta sea
exactamente lo que hay que decir, sin traducir mentalmente al leer.

Cubre el requisito 1 (cifras cardinales y ordinales, anios, horas, unidades,
porcentajes, monedas, rangos, fracciones, simbolos sueltos -- `>`, `+`, `/` -- y
siglas) y el requisito 2 (apocope de "uno"/"veintiuno", concordancia de genero
en la lectura de numeros, conjunciones "y"/"e" y "o"/"u"), con el diccionario
del dueno (requisito 3, `diccionario-locucion.json`) siempre por delante de
cualquier regla automatica.

Toda normalizacion es una `Normalizacion`: conserva el `original` y la
`propuesta` a la vez (invariante (b) de §0.2, "original siempre recuperable"),
con la familia de regla que la genero, un motivo legible y su rango de
caracteres en el texto de entrada. `normalizar_texto` NO modifica el texto por
su cuenta -- devuelve la lista de propuestas para que quien la use (T-15,
cuando exista el aparato de aceptar/rechazar reescrituras del `.md` anotado)
decida; `aplicar_normalizaciones` es una utilidad de previsualizacion que las
aplica todas sobre una copia, usada por los tests y por el informe.

Alcance deliberado (razonado en `roadmap/DECISIONES_TECNICAS.md`, T-13): la
concordancia de genero se resuelve con una heuristica por sufijo mas una lista
corta de excepciones frecuentes, no con un analizador morfologico real; los
ordinales cubren del 1º al 10º -- lo que basta para pasos y enumeraciones de
un guion de produccion, no la serie completa del espanol; las siglas sin
entrada en el diccionario se deletrean letra a letra por defecto, nunca se
"adivina" si se leen como palabra. Cualquier caso que las heuristicas no
acierten lo corrige el dueno en `diccionario-locucion.json`, que siempre gana
(requisito 3): por eso ninguna de estas heuristicas necesita ser perfecta.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from config import (
    NOMBRE_ARCHIVO_DICCIONARIO_LOCUCION,
    SIMBOLOS_MONEDA,
    UNIDADES_ABREVIADAS,
    Configuracion,
)
from troceo import BloqueRespiracion

FAMILIA_DICCIONARIO = "diccionario"
FAMILIA_MONEDA = "moneda"
FAMILIA_PORCENTAJE = "porcentaje"
FAMILIA_UNIDAD = "unidad"
FAMILIA_RANGO = "rango"
FAMILIA_FRACCION = "fraccion"
FAMILIA_ORDINAL = "ordinal"
FAMILIA_CARDINAL = "cardinal"
FAMILIA_SIGLA = "sigla"
FAMILIA_SIMBOLO = "simbolo"
FAMILIA_CONJUNCION = "conjuncion"


class NormalizacionError(Exception):
    """Fallo accionable al cargar el diccionario de locucion del dueno (requisito 3)."""


# --- Lectura de numeros en espanol -------------------------------------------------

_UNIDADES = (
    "cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
)
_UNIDADES_FEM = {1: "una"}
_DIEZ_DIECINUEVE = (
    "diez", "once", "doce", "trece", "catorce", "quince", "dieciséis", "diecisiete",
    "dieciocho", "diecinueve",
)
_VEINTI = (
    "veinte", "veintiuno", "veintidós", "veintitrés", "veinticuatro", "veinticinco",
    "veintiséis", "veintisiete", "veintiocho", "veintinueve",
)
_VEINTI_FEM = {1: "veintiuna"}
_DECENAS = (
    "", "diez", "veinte", "treinta", "cuarenta", "cincuenta", "sesenta", "setenta",
    "ochenta", "noventa",
)
_CENTENAS_MASC = (
    "", "ciento", "doscientos", "trescientos", "cuatrocientos", "quinientos",
    "seiscientos", "setecientos", "ochocientos", "novecientos",
)
_CENTENAS_FEM = (
    "", "ciento", "doscientas", "trescientas", "cuatrocientas", "quinientas",
    "seiscientas", "setecientas", "ochocientas", "novecientas",
)


def _unidad_texto(digito: int, femenino: bool) -> str:
    if femenino and digito in _UNIDADES_FEM:
        return _UNIDADES_FEM[digito]
    return _UNIDADES[digito]


def _menor_que_mil(n: int, femenino: bool) -> str:
    """Lee un numero de 0 a 999. `n == 0` devuelve cadena vacia (uso interno:
    el 0 real se resuelve aparte en `numero_a_cardinal`, como en los grupos de
    miles/millones, donde un grupo vacio no debe aportar la palabra "cero")."""
    if n == 0:
        return ""
    if n == 100:
        return "cien"
    centena, resto = divmod(n, 100)
    partes = []
    if centena:
        partes.append((_CENTENAS_FEM if femenino else _CENTENAS_MASC)[centena])
    if resto:
        if resto < 10:
            partes.append(_unidad_texto(resto, femenino))
        elif resto < 20:
            partes.append(_DIEZ_DIECINUEVE[resto - 10])
        elif resto < 30:
            unidad = resto - 20
            if femenino and unidad in _VEINTI_FEM:
                partes.append(_VEINTI_FEM[unidad])
            else:
                partes.append(_VEINTI[unidad])
        else:
            decena, unidad = divmod(resto, 10)
            if unidad == 0:
                partes.append(_DECENAS[decena])
            else:
                partes.append(f"{_DECENAS[decena]} y {_unidad_texto(unidad, femenino)}")
    return " ".join(partes)


def _aplicar_apocope(texto: str, femenino: bool) -> str:
    """"uno"/"veintiuno" pierden la "-o" final ante un sustantivo masculino
    ("un coche", "veintiún años"); en femenino "una"/"veintiuna" ya son
    correctas tal cual, no hay apocope que aplicar (requisito 2 de T-13)."""
    if femenino:
        return texto
    if texto.endswith("veintiuno"):
        return texto[: -len("veintiuno")] + "veintiún"
    if texto == "uno" or texto.endswith(" uno"):
        return texto[: -len("uno")] + "un"
    return texto


def numero_a_cardinal(n: int, femenino: bool = False, apocope: bool = False) -> str:
    """Lee un entero en espanol. `femenino` fuerza la concordancia de genero
    (una/veintiuna/doscientas...); `apocope` aplica la perdida de la "-o" final
    de "uno"/"veintiuno" cuando el numero precede a un sustantivo (requisito 2).
    Sin sustantivo detras (un anio, un recuento suelto...) no debe pedirse
    apocope: "leimos el 21" es "veintiuno", no "veintiún"."""
    if n < 0:
        return f"menos {numero_a_cardinal(-n, femenino, apocope)}"
    if n == 0:
        return "cero"
    partes = []
    millones, resto = divmod(n, 1_000_000)
    miles, unidades_resto = divmod(resto, 1000)
    if millones:
        texto_millones = _menor_que_mil(millones, False)
        partes.append("un millón" if millones == 1 else f"{texto_millones} millones")
    if miles:
        partes.append("mil" if miles == 1 else f"{_menor_que_mil(miles, False)} mil")
    if unidades_resto:
        partes.append(_menor_que_mil(unidades_resto, femenino))
    texto = " ".join(partes)
    return _aplicar_apocope(texto, femenino) if apocope else texto


_ORDINALES_MASC = {
    1: "primero", 2: "segundo", 3: "tercero", 4: "cuarto", 5: "quinto",
    6: "sexto", 7: "séptimo", 8: "octavo", 9: "noveno", 10: "décimo",
}
_ORDINALES_FEM = {
    1: "primera", 2: "segunda", 3: "tercera", 4: "cuarta", 5: "quinta",
    6: "sexta", 7: "séptima", 8: "octava", 9: "novena", 10: "décima",
}
_ORDINALES_APOCOPE_MASC = {1: "primer", 3: "tercer"}


def numero_a_ordinal(n: int, femenino: bool = False, apocope: bool = False) -> str | None:
    """Lee un ordinal del 1º al 10º (alcance documentado del modulo); `None`
    fuera de ese rango para que quien llame decida como degradar (no se
    inventa una forma para ordinales que este modulo no cubre)."""
    if n not in _ORDINALES_MASC:
        return None
    if femenino:
        return _ORDINALES_FEM[n]
    if apocope and n in _ORDINALES_APOCOPE_MASC:
        return _ORDINALES_APOCOPE_MASC[n]
    return _ORDINALES_MASC[n]


# --- Concordancia de genero por heuristica (requisito 2) ---------------------------

_SUSTANTIVOS_MASCULINOS_EN_A = {
    "día", "mapa", "planeta", "problema", "sistema", "tema", "programa",
    "idioma", "clima", "poema", "dato", "esquema", "panorama", "drama",
}
_SUSTANTIVOS_FEMENINOS_EN_O = {"mano", "foto", "moto", "radio"}


def _forma_singular_aprox(palabra: str) -> str:
    if palabra.endswith("es") and len(palabra) > 3:
        return palabra[:-2]
    if palabra.endswith("s") and len(palabra) > 2:
        return palabra[:-1]
    return palabra


def _genero_por_sustantivo(palabra: str) -> bool:
    """`True` = femenino. Heuristica por sufijo con una lista corta de
    excepciones frecuentes; por defecto masculino (la forma no marcada del
    espanol), igual que hace cualquier hablante ante un sustantivo que no
    reconoce. El dueno corrige los fallos con una entrada literal en
    `diccionario-locucion.json` (requisito 3), que siempre gana sobre esto."""
    limpio = re.sub(r"[^\wÁÉÍÓÚÑáéíóúñ]", "", palabra, flags=re.UNICODE).lower()
    singular = _forma_singular_aprox(limpio)
    if singular in _SUSTANTIVOS_MASCULINOS_EN_A:
        return False
    if singular in _SUSTANTIVOS_FEMENINOS_EN_O:
        return True
    if singular.endswith(("ción", "sión", "dad", "tud", "umbre", "a")):
        return True
    return False


def _siguiente_palabra(texto: str, desde: int) -> str | None:
    coincidencia = re.match(r"\s+([A-Za-zÁÉÍÓÚÑáéíóúñ]+)", texto[desde:])
    return coincidencia.group(1) if coincidencia else None


# --- Parseo de numeros con convencion hispana (punto de millar, coma decimal) ------


def _parsear_numero_hispano(numero_texto: str) -> tuple[int, str | None]:
    """`"1.500,50"` -> `(1500, "50")`; `"2026"` -> `(2026, None)`. Convencion
    hispana consciente (punto = millar, coma = decimal), la misma que usan los
    ejemplos del criterio de aceptacion de T-13."""
    limpio = numero_texto.strip()
    if "," in limpio:
        entero_str, _, decimal_str = limpio.partition(",")
    else:
        entero_str, decimal_str = limpio, None
    entero_str = entero_str.replace(".", "") or "0"
    return int(entero_str), decimal_str


def _leer_decimal(decimal_str: str) -> str:
    """Parte decimal leida digito a digito tras "coma" (convencion habitual al
    dictar numeros en espanol: "3,14" -> "tres coma uno cuatro")."""
    return " ".join(_UNIDADES[int(digito)] for digito in decimal_str)


# --- Deletreo de siglas (requisito 1) -----------------------------------------------

_NOMBRES_LETRAS = {
    "A": "a", "B": "be", "C": "ce", "D": "de", "E": "e", "F": "efe", "G": "ge",
    "H": "hache", "I": "i", "J": "jota", "K": "ka", "L": "ele", "M": "eme",
    "N": "ene", "Ñ": "eñe", "O": "o", "P": "pe", "Q": "cu", "R": "erre",
    "S": "ese", "T": "te", "U": "u", "V": "uve", "W": "uve doble", "X": "equis",
    "Y": "i griega", "Z": "zeta",
    "Á": "a", "É": "e", "Í": "i", "Ó": "o", "Ú": "u",
}


def deletrear_sigla(sigla: str) -> str:
    """Lectura letra a letra de una sigla, por defecto para cualquiera que no
    tenga entrada en `diccionario-locucion.json` (requisito 1: "deletreadas o
    leidas segun diccionario"). Nunca se adivina si suena mejor como palabra."""
    return " ".join(_NOMBRES_LETRAS.get(letra, letra.lower()) for letra in sigla)


# --- Patrones de reconocimiento -----------------------------------------------------

_PATRON_MONEDA_SUFIJO = re.compile(r"(?P<num>\d[\d.,]*\d|\d)\s?(?P<sim>[€$])")
_PATRON_MONEDA_PREFIJO = re.compile(r"(?P<sim>[€$])\s?(?P<num>\d[\d.,]*\d|\d)")
_PATRON_PORCENTAJE = re.compile(r"(?P<num>\d[\d.,]*\d|\d)\s?%")
_PATRON_UNIDAD = re.compile(
    r"(?P<num>\d[\d.,]*\d|\d)\s?(?P<unidad>"
    + "|".join(re.escape(abrev) for abrev in sorted(UNIDADES_ABREVIADAS, key=len, reverse=True))
    + r")\b"
)
_GUION_LARGO = "\u2013"  # mismo caracter que usan los rangos horarios reales (T-08)
_PATRON_RANGO = re.compile(
    rf"(?P<a>\d[\d.,]*\d|\d)\s*[{_GUION_LARGO}-]\s*(?P<b>\d[\d.,]*\d|\d)"
)
_PATRON_FRACCION = re.compile(r"(?P<a>\d+)\s*/\s*(?P<b>\d+)")
_PATRON_ORDINAL = re.compile(r"\b(?P<num>\d{1,2})(?P<suf>ª|º|er)\b")
_PATRON_CARDINAL = re.compile(r"\b\d{1,3}(?:\.\d{3})+(?:,\d+)?\b|\b\d+(?:,\d+)?\b")
_PATRON_SIGLA = re.compile(r"\b[A-ZÁÉÍÓÚÑ]{2,}\b")
_PATRON_SIMBOLO_SUELTO = re.compile(r"[>+]")
_PATRON_CONJUNCION = re.compile(r"\b([Yy]|[Oo])\b")
_NOMBRES_SIMBOLO_SUELTO = {">": "mayor que", "+": "más"}


@dataclass(frozen=True)
class Normalizacion:
    """Una propuesta de reescritura a forma dicha. `original`/`propuesta`
    conservan ambas versiones a la vez (invariante (b), original siempre
    recuperable); `inicio`/`fin` son offsets de caracter en el texto de
    entrada, 0-indexados, `fin` exclusivo -- `texto[inicio:fin] == original`."""

    original: str
    propuesta: str
    familia: str
    motivo: str
    inicio: int
    fin: int


@dataclass
class ResultadoNormalizacionBloque:
    """Las normalizaciones propuestas para un `BloqueRespiracion` (T-11), sin
    tocar su texto original."""

    bloque: BloqueRespiracion
    normalizaciones: list[Normalizacion] = field(default_factory=list)

    @property
    def texto_propuesto(self) -> str:
        """El texto del bloque con todas las propuestas aplicadas (previsualizacion;
        la aceptacion/rechazo individual por reescritura es alcance de T-15)."""
        return aplicar_normalizaciones(self.bloque.texto, self.normalizaciones)


def aplicar_normalizaciones(texto: str, normalizaciones: list[Normalizacion]) -> str:
    """Reconstruye `texto` sustituyendo cada tramo `[inicio, fin)` por su
    `propuesta`. Inversa de la reconstruccion: sustituir cada tramo del
    resultado por su `original` reproduce `texto` de forma exacta (verificado
    en `tests/test_normalizacion.py`, invariante (b) de §0.2)."""
    ordenadas = sorted(normalizaciones, key=lambda normalizacion: normalizacion.inicio)
    partes = []
    cursor = 0
    for normalizacion in ordenadas:
        partes.append(texto[cursor : normalizacion.inicio])
        partes.append(normalizacion.propuesta)
        cursor = normalizacion.fin
    partes.append(texto[cursor:])
    return "".join(partes)


def deshacer_normalizaciones(texto_propuesto: str, normalizaciones: list[Normalizacion]) -> str:
    """Inversa de `aplicar_normalizaciones`: reconstruye el texto original a
    partir del propuesto y la misma lista de `Normalizacion` que lo produjo
    (invariante (b) de §0.2, "original siempre recuperable"). Los offsets de
    `normalizaciones` son los del texto ORIGINAL (los que devuelve
    `normalizar_texto`); esta funcion los recorre en orden, avanzando por la
    longitud de cada tramo sin cambios -- identica en original y propuesto,
    porque ese tramo no se toco -- y luego por la longitud de cada `propuesta`
    para saltarsela en `texto_propuesto` y sustituirla por su `original`."""
    ordenadas = sorted(normalizaciones, key=lambda normalizacion: normalizacion.inicio)
    partes = []
    cursor_original = 0
    cursor_propuesto = 0
    for normalizacion in ordenadas:
        longitud_sin_cambios = normalizacion.inicio - cursor_original
        partes.append(texto_propuesto[cursor_propuesto : cursor_propuesto + longitud_sin_cambios])
        cursor_propuesto += longitud_sin_cambios + len(normalizacion.propuesta)
        cursor_original = normalizacion.fin
        partes.append(normalizacion.original)
    partes.append(texto_propuesto[cursor_propuesto:])
    return "".join(partes)


def _libre(ocupado: bytearray, inicio: int, fin: int) -> bool:
    return not any(ocupado[inicio:fin])


def _marcar(ocupado: bytearray, inicio: int, fin: int) -> None:
    for indice in range(inicio, fin):
        ocupado[indice] = 1


def normalizar_texto(
    texto: str,
    configuracion: Configuracion | None = None,
    diccionario: dict[str, str] | None = None,
) -> list[Normalizacion]:
    """Detecta y propone la forma dicha de `texto`, sin modificarlo. Procesa
    las familias de regla en orden de prioridad estricto -- el diccionario del
    dueno primero (requisito 3), despues moneda/porcentaje/unidad/rango/
    fraccion/ordinal/cardinal/sigla/simbolo suelto, y por ultimo las
    conjunciones "y"/"o" -- marcando cada tramo ya resuelto como ocupado para
    que ninguna familia posterior lo reinterprete."""
    configuracion = configuracion or Configuracion()
    diccionario = diccionario or {}
    ocupado = bytearray(len(texto))
    normalizaciones: list[Normalizacion] = []

    def agregar(inicio: int, fin: int, familia: str, motivo: str, propuesta: str | None) -> None:
        if propuesta is None or not _libre(ocupado, inicio, fin):
            return
        original = texto[inicio:fin]
        if propuesta == original:
            return
        normalizaciones.append(Normalizacion(original, propuesta, familia, motivo, inicio, fin))
        _marcar(ocupado, inicio, fin)

    # 1. Diccionario del dueno: manda sobre cualquier regla automatica (requisito 3).
    # Claves mas largas primero, para que una entrada de varias palabras no quede
    # partida por una entrada de una sola palabra contenida en ella.
    for clave in sorted(diccionario, key=len, reverse=True):
        if not clave:
            continue
        patron_clave = re.compile(rf"\b{re.escape(clave)}\b")
        for coincidencia in patron_clave.finditer(texto):
            agregar(
                coincidencia.start(),
                coincidencia.end(),
                FAMILIA_DICCIONARIO,
                f"diccionario del dueño: {clave!r}",
                diccionario[clave],
            )

    # 2. Moneda: "1.500 €" / "€ 1.500" -> cardinal + euro(s)/dolar(es).
    for patron in (_PATRON_MONEDA_SUFIJO, _PATRON_MONEDA_PREFIJO):
        for coincidencia in patron.finditer(texto):
            simbolo = coincidencia.group("sim")
            singular, plural = SIMBOLOS_MONEDA.get(simbolo, (None, None))
            if singular is None or plural is None:
                continue
            entero, decimal = _parsear_numero_hispano(coincidencia.group("num"))
            forma = plural if entero != 1 else singular
            propuesta = f"{numero_a_cardinal(entero)} {forma}"
            if decimal:
                centimos = int((decimal + "00")[:2])
                forma_centimo = "céntimo" if centimos == 1 else "céntimos"
                propuesta += f" con {numero_a_cardinal(centimos)} {forma_centimo}"
            agregar(
                coincidencia.start(),
                coincidencia.end(),
                FAMILIA_MONEDA,
                f"cantidad en {simbolo}: se lee en {plural}",
                propuesta,
            )

    # 3. Porcentaje: "15%" -> "quince por ciento".
    for coincidencia in _PATRON_PORCENTAJE.finditer(texto):
        entero, decimal = _parsear_numero_hispano(coincidencia.group("num"))
        propuesta = numero_a_cardinal(entero)
        if decimal:
            propuesta += f" coma {_leer_decimal(decimal)}"
        agregar(
            coincidencia.start(), coincidencia.end(), FAMILIA_PORCENTAJE,
            "porcentaje: se lee 'por ciento'", f"{propuesta} por ciento",
        )

    # 4. Unidad abreviada: "10 km" -> "diez kilómetros".
    for coincidencia in _PATRON_UNIDAD.finditer(texto):
        entero, decimal = _parsear_numero_hispano(coincidencia.group("num"))
        propuesta = numero_a_cardinal(entero)
        if decimal:
            propuesta += f" coma {_leer_decimal(decimal)}"
        unidad_dicha = UNIDADES_ABREVIADAS[coincidencia.group("unidad")]
        agregar(
            coincidencia.start(), coincidencia.end(), FAMILIA_UNIDAD,
            f"unidad abreviada '{coincidencia.group('unidad')}'", f"{propuesta} {unidad_dicha}",
        )

    # 5. Rango: "10-250" -> "diez a doscientos cincuenta".
    for coincidencia in _PATRON_RANGO.finditer(texto):
        entero_a, decimal_a = _parsear_numero_hispano(coincidencia.group("a"))
        entero_b, decimal_b = _parsear_numero_hispano(coincidencia.group("b"))
        texto_a = numero_a_cardinal(entero_a)
        if decimal_a:
            texto_a += f" coma {_leer_decimal(decimal_a)}"
        texto_b = numero_a_cardinal(entero_b)
        if decimal_b:
            texto_b += f" coma {_leer_decimal(decimal_b)}"
        agregar(
            coincidencia.start(), coincidencia.end(), FAMILIA_RANGO,
            "rango numerico: se lee '<a> a <b>'", f"{texto_a} a {texto_b}",
        )

    # 6. Fraccion: "3/4" -> "tres partido por cuatro".
    for coincidencia in _PATRON_FRACCION.finditer(texto):
        propuesta = (
            f"{numero_a_cardinal(int(coincidencia.group('a')))} partido por "
            f"{numero_a_cardinal(int(coincidencia.group('b')))}"
        )
        agregar(
            coincidencia.start(), coincidencia.end(), FAMILIA_FRACCION,
            "fraccion: se lee '<a> partido por <b>'", propuesta,
        )

    # 7. Ordinal: "1ª" -> "primera", "3er" -> "tercer", "1º" -> "primero".
    for coincidencia in _PATRON_ORDINAL.finditer(texto):
        numero = int(coincidencia.group("num"))
        sufijo = coincidencia.group("suf")
        femenino = sufijo == "ª"
        apocope = sufijo == "er"
        propuesta_ordinal = numero_a_ordinal(numero, femenino=femenino, apocope=apocope)
        if propuesta_ordinal is None:
            continue
        agregar(
            coincidencia.start(), coincidencia.end(), FAMILIA_ORDINAL,
            f"ordinal '{sufijo}': se lee '{propuesta_ordinal}'", propuesta_ordinal,
        )

    # 8. Cardinal suelto: anios, recuentos, cifras sin simbolo. Concordancia de
    # genero y apocope (requisito 2) solo si hay un sustantivo justo detras;
    # sin el, se lee como numero suelto ("el 21" -> "veintiuno", no "veintiún").
    for coincidencia in _PATRON_CARDINAL.finditer(texto):
        entero, decimal = _parsear_numero_hispano(coincidencia.group())
        siguiente = _siguiente_palabra(texto, coincidencia.end())
        femenino = False
        apocope = False
        if siguiente is not None and decimal is None:
            femenino = _genero_por_sustantivo(siguiente)
            apocope = True
        propuesta = numero_a_cardinal(entero, femenino=femenino, apocope=apocope)
        if decimal:
            propuesta += f" coma {_leer_decimal(decimal)}"
        agregar(
            coincidencia.start(), coincidencia.end(), FAMILIA_CARDINAL,
            "cifra: se lee en letras", propuesta,
        )

    # 9. Sigla: por diccionario ya resuelta arriba; el resto se deletrea.
    for coincidencia in _PATRON_SIGLA.finditer(texto):
        sigla = coincidencia.group()
        agregar(
            coincidencia.start(), coincidencia.end(), FAMILIA_SIGLA,
            "sigla sin entrada en el diccionario: se deletrea letra a letra",
            deletrear_sigla(sigla),
        )

    # 10. Simbolo suelto: '>', '+' (el '%'/'€'/'$'/'/' ya se resuelven arriba,
    # siempre pegados a una cifra; sueltos son ambiguos y no se tocan).
    for coincidencia in _PATRON_SIMBOLO_SUELTO.finditer(texto):
        agregar(
            coincidencia.start(), coincidencia.end(), FAMILIA_SIMBOLO,
            "simbolo: se lee la palabra equivalente",
            _NOMBRES_SIMBOLO_SUELTO.get(coincidencia.group()),
        )

    # 11. Conjunciones "y"/"e", "o"/"u" (requisito 2), independiente de cifras.
    for coincidencia in _PATRON_CONJUNCION.finditer(texto):
        conjuncion = coincidencia.group()
        siguiente = _siguiente_palabra(texto, coincidencia.end())
        if siguiente is None:
            continue
        siguiente_min = siguiente.lower()
        if conjuncion.lower() == "y":
            if siguiente_min.startswith(("hie", "hia")):
                continue
            if not siguiente_min.startswith(("i", "hi")):
                continue
            propuesta = "E" if conjuncion.isupper() else "e"
            motivo = "conjuncion 'y' -> 'e' ante sonido /i/"
        else:
            if not siguiente_min.startswith(("o", "ho")):
                continue
            propuesta = "U" if conjuncion.isupper() else "u"
            motivo = "conjuncion 'o' -> 'u' ante sonido /o/"
        agregar(coincidencia.start(), coincidencia.end(), FAMILIA_CONJUNCION, motivo, propuesta)

    normalizaciones.sort(key=lambda normalizacion: normalizacion.inicio)
    return normalizaciones


def normalizar_bloque(
    bloque: BloqueRespiracion,
    configuracion: Configuracion | None = None,
    diccionario: dict[str, str] | None = None,
) -> ResultadoNormalizacionBloque:
    """Normaliza un `BloqueRespiracion` (T-11) ya trozado. Se normaliza sobre
    el bloque final, no antes del troceo, para que ninguna propuesta quede
    partida por un corte de respiracion (T-11, requisito 2: "nunca cortar...
    una expresion normalizada por T-13")."""
    normalizaciones = normalizar_texto(bloque.texto, configuracion, diccionario)
    return ResultadoNormalizacionBloque(bloque=bloque, normalizaciones=normalizaciones)


def normalizar_guion(
    bloques: list[BloqueRespiracion],
    configuracion: Configuracion | None = None,
    diccionario: dict[str, str] | None = None,
) -> list[ResultadoNormalizacionBloque]:
    """Normaliza todos los bloques de respiracion de un guion ya trozado
    (T-11). Un resultado por bloque, incluso sin normalizaciones propuestas
    (cobertura total, invariante (a) de §0.2: nada se descarta en silencio)."""
    return [normalizar_bloque(bloque, configuracion, diccionario) for bloque in bloques]


def cargar_diccionario_locucion(carpeta_salida: Path) -> dict[str, str]:
    """Lee `diccionario-locucion.json` de la carpeta de salida del guion, si
    existe (requisito 3). Ausente -> `{}`: sin el, solo actuan las reglas
    automaticas. Presente pero invalido -> `NormalizacionError` accionable,
    nunca una traza cruda (regla de validacion de entradas, §0.2)."""
    ruta = carpeta_salida / NOMBRE_ARCHIVO_DICCIONARIO_LOCUCION
    if not ruta.is_file():
        return {}
    try:
        contenido = ruta.read_text(encoding="utf-8")
    except OSError as error:
        mensaje = f"No se pudo leer el diccionario de locucion '{ruta}': {error}"
        raise NormalizacionError(mensaje) from error
    try:
        datos = json.loads(contenido)
    except json.JSONDecodeError as error:
        mensaje = f"El diccionario de locucion '{ruta}' no es JSON valido: {error}"
        raise NormalizacionError(mensaje) from error
    if not isinstance(datos, dict) or not all(
        isinstance(clave, str) and isinstance(valor, str) for clave, valor in datos.items()
    ):
        mensaje = (
            f"El diccionario de locucion '{ruta}' debe ser un objeto JSON de texto a "
            "texto (\"termino\": \"forma dicha\")."
        )
        raise NormalizacionError(mensaje)
    return datos
