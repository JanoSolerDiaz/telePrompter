"""Detector de problemas de lectura en voz alta (tarea T-14).

Avisa de lo que va a costar decir antes de estar delante de la camara, sobre
los `BloqueRespiracion` que ya entrega el troceo (T-11). Cinco familias, una
por requisito de la tarea:

1. `sin_punto_respiracion` -- bloque largo (por encima de un umbral
   configurable) sin puntuacion intermedia (coma, guion, parentesis...).
2. `cacofonia` -- "de" encadenados, silaba inicial repetida o rima
   involuntaria entre palabras proximas.
3. `trabalenguas` -- palabra con un grupo de consonantes seguidas dificil de
   pronunciar, o varias palabras largas seguidas.
4. `anglicismo` -- extranjerismo frecuente con equivalente en espanol.
5. `estructura_dificil` -- incisos acumulados, subordinadas encadenadas,
   doble negacion o voz pasiva larga.

Ninguna familia reescribe el texto (alcance decidido por el dueno, §0.2): solo
`sin_punto_respiracion` marca `admite_particion=True` y adjunta una
`particion_sugerida`, porque es la unica que afecta al troceo (requisito 6);
la particion en si (aceptarla, aplicarla) es alcance de T-15, no de esta
tarea. Cobertura total (invariante (a) de §0.2): un resultado por bloque de
respiracion, incluso sin avisos.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from config import ANGLICISMOS_COMUNES, Configuracion
from troceo import BloqueRespiracion

FAMILIA_SIN_PUNTO_RESPIRACION = "sin_punto_respiracion"
FAMILIA_CACOFONIA = "cacofonia"
FAMILIA_TRABALENGUAS = "trabalenguas"
FAMILIA_ANGLICISMO = "anglicismo"
FAMILIA_ESTRUCTURA_DIFICIL = "estructura_dificil"

SEVERIDAD_ALTA = "alta"
SEVERIDAD_MEDIA = "media"
SEVERIDAD_BAJA = "baja"

_PATRON_PALABRA = re.compile(r"[^\W\d_]+", re.UNICODE)
_PATRON_PUNTUACION_INTERMEDIA = re.compile(r"[,;:—\-()¿¡]")
_CONSONANTES = "bcdfghjklmnñpqrstvwxyz"
_PATRON_CONSONANTES_SEGUIDAS = re.compile(f"[{_CONSONANTES}]+", re.IGNORECASE)
# Requisito 5: "es/fue/ha sido..." + participio, con un "por" opcional de agente.
_PATRON_VOZ_PASIVA = re.compile(
    r"\b(?:es|son|fue|fueron|será|serán|ha sido|han sido|había sido|habían sido)\s+"
    r"\w*(?:ad[oa]s?|id[oa]s?)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Aviso:
    """Un problema de locucion detectado. `fragmento` es el texto exacto que lo
    dispara (invariante (a): nunca se descarta en silencio, siempre localizable).
    `admite_particion`/`particion_sugerida` solo los rellena la familia
    `sin_punto_respiracion` (requisito 6); el resto los deja en `False`/`None`."""

    familia: str
    severidad: str
    mensaje: str
    recomendacion: str
    fragmento: str
    admite_particion: bool = False
    particion_sugerida: tuple[str, str] | None = None


@dataclass
class ResultadoDeteccionBloque:
    """Los avisos detectados para un `BloqueRespiracion` (T-11), sin tocar su texto."""

    bloque: BloqueRespiracion
    avisos: list[Aviso] = field(default_factory=list)


def _palabras(texto: str) -> list[str]:
    return _PATRON_PALABRA.findall(texto)


def _sufijo_normalizado(palabra: str, longitud: int) -> str:
    return palabra[-longitud:].lower() if len(palabra) >= longitud else ""


def _prefijo_normalizado(palabra: str, longitud: int) -> str:
    return palabra[:longitud].lower() if len(palabra) >= longitud else ""


def _mejor_punto_particion(palabras: list[str], configuracion: Configuracion) -> int:
    """Indice de palabra (1-indexado desde el principio) donde partir en dos si
    hiciera falta: el nexo subordinante mas cercano al centro, o el centro
    exacto si no hay ninguno. Solo se usa para `particion_sugerida`, una
    propuesta de datos -- no reescribe nada (T-15 decide si actuar)."""
    centro = len(palabras) / 2
    candidatos = [
        indice
        for indice, palabra in enumerate(palabras, start=1)
        if palabra.lower() in configuracion.subordinantes
    ]
    if not candidatos:
        return round(centro)
    return min(candidatos, key=lambda indice: abs(indice - centro))


def _detectar_sin_punto_respiracion(
    bloque: BloqueRespiracion, configuracion: Configuracion
) -> list[Aviso]:
    palabras = _palabras(bloque.texto)
    if len(palabras) <= configuracion.umbral_palabras_sin_puntuacion:
        return []
    if _PATRON_PUNTUACION_INTERMEDIA.search(bloque.texto.rstrip(".?!")):
        return []
    punto = _mejor_punto_particion(palabras, configuracion)
    particion = (" ".join(palabras[:punto]), " ".join(palabras[punto:]))
    return [
        Aviso(
            familia=FAMILIA_SIN_PUNTO_RESPIRACION,
            severidad=SEVERIDAD_ALTA,
            mensaje=(
                f"Frase de {len(palabras)} palabras sin ninguna puntuacion intermedia "
                "(coma, guion, parentesis...): no hay donde respirar antes del final."
            ),
            recomendacion="Añade una coma o divide la frase en dos.",
            fragmento=bloque.texto,
            admite_particion=True,
            particion_sugerida=particion,
        )
    ]


def _detectar_cacofonia(bloque: BloqueRespiracion, configuracion: Configuracion) -> list[Aviso]:
    palabras = _palabras(bloque.texto)
    avisos: list[Aviso] = []
    ventana = configuracion.ventana_cacofonia_palabras
    longitud = configuracion.longitud_silaba_comparada

    for inicio in range(len(palabras) - ventana + 1):
        tramo = palabras[inicio : inicio + ventana]
        repeticiones_de = sum(1 for palabra in tramo if palabra.lower() == "de")
        if repeticiones_de >= configuracion.repeticiones_de_minimas:
            avisos.append(
                Aviso(
                    familia=FAMILIA_CACOFONIA,
                    severidad=SEVERIDAD_MEDIA,
                    mensaje=f"«de» encadenado {repeticiones_de} veces en pocas palabras.",
                    recomendacion="Reformula para no repetir «de» tan seguido.",
                    fragmento=" ".join(tramo),
                )
            )
            break  # una vez por bloque basta; no inundar de avisos redundantes

    for indice in range(len(palabras) - 1):
        actual, siguiente = palabras[indice], palabras[indice + 1]
        if actual.lower() == siguiente.lower():
            continue
        prefijo = _prefijo_normalizado(actual, longitud)
        if prefijo and prefijo == _prefijo_normalizado(siguiente, longitud):
            avisos.append(
                Aviso(
                    familia=FAMILIA_CACOFONIA,
                    severidad=SEVERIDAD_BAJA,
                    mensaje=f"Silaba inicial repetida entre «{actual}» y «{siguiente}».",
                    recomendacion="Sustituye una de las dos palabras por un sinonimo.",
                    fragmento=f"{actual} {siguiente}",
                )
            )
            break

    for inicio in range(len(palabras) - ventana + 1):
        tramo = palabras[inicio : inicio + ventana]
        vistos: dict[str, str] = {}
        for palabra in tramo:
            if len(palabra) < configuracion.longitud_minima_palabra_rima:
                continue
            sufijo = _sufijo_normalizado(palabra, longitud)
            if not sufijo:
                continue
            anterior = vistos.get(sufijo)
            if anterior and anterior.lower() != palabra.lower():
                avisos.append(
                    Aviso(
                        familia=FAMILIA_CACOFONIA,
                        severidad=SEVERIDAD_BAJA,
                        mensaje=f"Rima involuntaria entre «{anterior}» y «{palabra}».",
                        recomendacion="Sustituye una de las dos palabras por un sinonimo.",
                        fragmento=f"{anterior} ... {palabra}",
                    )
                )
                return avisos
            vistos[sufijo] = palabra
    return avisos


def _detectar_trabalenguas(bloque: BloqueRespiracion, configuracion: Configuracion) -> list[Aviso]:
    palabras = _palabras(bloque.texto)
    avisos: list[Aviso] = []

    for palabra in palabras:
        grupo_mas_largo = max(
            (len(grupo) for grupo in _PATRON_CONSONANTES_SEGUIDAS.findall(palabra)), default=0
        )
        if grupo_mas_largo >= configuracion.consonantes_seguidas_dificil:
            avisos.append(
                Aviso(
                    familia=FAMILIA_TRABALENGUAS,
                    severidad=SEVERIDAD_MEDIA,
                    mensaje=f"«{palabra}» acumula {grupo_mas_largo} consonantes seguidas.",
                    recomendacion="Ensaya esta palabra en voz alta antes de grabar.",
                    fragmento=palabra,
                )
            )

    racha = 0
    for palabra in palabras:
        if len(palabra) >= configuracion.longitud_palabra_dificil:
            racha += 1
        else:
            racha = 0
        if racha == configuracion.palabras_dificiles_seguidas_minimas:
            avisos.append(
                Aviso(
                    familia=FAMILIA_TRABALENGUAS,
                    severidad=SEVERIDAD_MEDIA,
                    mensaje=(
                        f"{racha} palabras largas seguidas (≥"
                        f"{configuracion.longitud_palabra_dificil} caracteres)."
                    ),
                    recomendacion="Reparte estas palabras en frases distintas si puedes.",
                    fragmento=bloque.texto,
                )
            )
            break
    return avisos


def _detectar_anglicismos(bloque: BloqueRespiracion) -> list[Aviso]:
    palabras = _palabras(bloque.texto)
    avisos: list[Aviso] = []
    for palabra in palabras:
        equivalente = ANGLICISMOS_COMUNES.get(palabra.lower())
        if equivalente is None:
            continue
        avisos.append(
            Aviso(
                familia=FAMILIA_ANGLICISMO,
                severidad=SEVERIDAD_BAJA,
                mensaje=f"«{palabra}» es un extranjerismo frecuente.",
                recomendacion=f"Equivalente en español: {equivalente}.",
                fragmento=palabra,
            )
        )
    return avisos


def _detectar_estructura_dificil(
    bloque: BloqueRespiracion, configuracion: Configuracion
) -> list[Aviso]:
    palabras = _palabras(bloque.texto)
    avisos: list[Aviso] = []

    incisos = bloque.texto.count("(") + bloque.texto.count(")") + bloque.texto.count("—")
    if incisos >= configuracion.umbral_incisos:
        avisos.append(
            Aviso(
                familia=FAMILIA_ESTRUCTURA_DIFICIL,
                severidad=SEVERIDAD_MEDIA,
                mensaje=f"{incisos} marcas de inciso (parentesis/guion largo) en el mismo bloque.",
                recomendacion="Simplifica o separa los incisos en frases propias.",
                fragmento=bloque.texto,
            )
        )

    subordinantes_encontrados = [p for p in palabras if p.lower() in configuracion.subordinantes]
    if len(subordinantes_encontrados) >= configuracion.umbral_subordinadas_encadenadas:
        avisos.append(
            Aviso(
                familia=FAMILIA_ESTRUCTURA_DIFICIL,
                severidad=SEVERIDAD_MEDIA,
                mensaje=(
                    f"{len(subordinantes_encontrados)} nexos subordinantes "
                    f"({', '.join(subordinantes_encontrados)}) en el mismo bloque."
                ),
                recomendacion="Divide la frase para no encadenar tantas subordinadas.",
                fragmento=bloque.texto,
            )
        )

    negaciones_encontradas = [p for p in palabras if p.lower() in configuracion.negaciones]
    if len(negaciones_encontradas) >= configuracion.umbral_negaciones_dobles:
        avisos.append(
            Aviso(
                familia=FAMILIA_ESTRUCTURA_DIFICIL,
                severidad=SEVERIDAD_MEDIA,
                mensaje=f"Doble negacion ({', '.join(negaciones_encontradas)}) en el mismo bloque.",
                recomendacion="Reformula en positivo o con una sola negacion.",
                fragmento=bloque.texto,
            )
        )

    if _PATRON_VOZ_PASIVA.search(
        bloque.texto
    ) and len(palabras) >= configuracion.umbral_palabras_voz_pasiva_larga:
        avisos.append(
            Aviso(
                familia=FAMILIA_ESTRUCTURA_DIFICIL,
                severidad=SEVERIDAD_BAJA,
                mensaje=f"Voz pasiva larga ({len(palabras)} palabras).",
                recomendacion="Prueba la voz activa: suele sonar mas natural al hablar.",
                fragmento=bloque.texto,
            )
        )
    return avisos


def detectar_problemas_bloque(
    bloque: BloqueRespiracion, configuracion: Configuracion | None = None
) -> ResultadoDeteccionBloque:
    """Detecta los problemas de lectura en voz alta de un `BloqueRespiracion`
    (T-11) ya trozado. No modifica el bloque (alcance decidido por el dueno,
    §0.2): solo avisa."""
    configuracion = configuracion or Configuracion()
    avisos = [
        *_detectar_sin_punto_respiracion(bloque, configuracion),
        *_detectar_cacofonia(bloque, configuracion),
        *_detectar_trabalenguas(bloque, configuracion),
        *_detectar_anglicismos(bloque),
        *_detectar_estructura_dificil(bloque, configuracion),
    ]
    return ResultadoDeteccionBloque(bloque=bloque, avisos=avisos)


def detectar_problemas_guion(
    bloques: list[BloqueRespiracion], configuracion: Configuracion | None = None
) -> list[ResultadoDeteccionBloque]:
    """Detecta los problemas de lectura en voz alta de todos los bloques de
    respiracion de un guion ya trozado (T-11). Un resultado por bloque, incluso
    sin avisos (cobertura total, invariante (a) de §0.2)."""
    return [detectar_problemas_bloque(bloque, configuracion) for bloque in bloques]
