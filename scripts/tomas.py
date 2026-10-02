"""Registro de tomas por escena (tarea R-02).

El reproductor (`assets/reproductor/guion.js`) cronometra cada toma con el mismo
reloj de pared que ya usaba el cronometro de T-23, la guarda en `localStorage`
(clave por escena, mismo mecanismo que T-26/R-01) y, cuando el dueno lo pide con
el boton "Exportar parte de rodaje" del indice, vuelca todo a un archivo `.json`
independiente -- el propio navegador `file://` no puede escribir directamente en
la carpeta de salida del guion (cero red en tiempo de ejecucion, §0.2).

Este modulo es el lado Python de ese volcado (requisito 3 de R-02, "legible por
la fase de montaje y por el dueno"): valida el archivo exportado y lo fusiona en
`estado.json` (`EstadoProyecto.tomas`), para que el registro de tomas quede
disponible sin depender de reabrir el reproductor -- tanto para que el dueno lo
consulte como para que una tarea futura (R-04, recalibrar el ritmo con tiempos
reales; R-05, `.srt` alineado con la toma buena) lo lea desde `estado.json` en
vez de tener que reparsear el archivo suelto. La skill no invoca esto sola: es
Claude quien llama a `cargar_parte_de_rodaje`/`registrar_tomas` cuando el dueno
entrega el archivo exportado tras una sesion de rodaje.

`toma_buena` (publica, no `_`) es el criterio ya establecido por R-04 para
leer "la" toma real de una escena a partir de `estado.tomas`: la marcada
`buena`, `None` si ninguna lo esta todavia (una escena con tomas sin marcar
no aporta evidencia real, nunca se estima ni se promedia entre tomas sin
validar). `duracion_toma_buena` es un atajo sobre ella para quien solo
necesita la duracion (R-04/`calibracion.py`, R-05/`srt_alineado.py`,
R-07/`capitulos_youtube.py`); R-19 (`concat_ffmpeg.py`) llama a `toma_buena`
directamente porque necesita ademas `archivo_video`, sin reimplementar la
regla de exclusividad de abajo.

R-11 (hallazgo #16): la exclusividad de "como mucho una toma buena por
escena" solo la garantizaba antes el lado JS (`finalizarTomaActual` desmarca
las demas antes de anadir la nueva) -- un `estado.tomas` con dos tomas
`buena` para la misma escena (edicion manual, fusion de dos exportaciones, un
futuro bug de `guion.js`) hacia que se eligiera la primera en silencio.
`toma_buena` rechaza ese dato con `RegistroTomasError` en vez de elegir: es
un dato corrupto, no una ambiguedad legitima que se pueda resolver sola, y de
ella dependen a la vez R-04/R-05/R-07/R-19.

R-19: cada toma gana el campo opcional `archivo_video` (string, `""` si no
se ha anotado) -- el nombre del archivo de video real de la camara que
`scripts/concat_ffmpeg.py` usa para generar `concat-ffmpeg.txt`. Campo
aditivo (`references/contrato-tomas.md` version 2): un parte de rodaje o un
`estado.json` de antes de R-19 se lee igual, con `""` por defecto.

R-21 (hallazgo #27): `_sanear_archivo_video` recorta espacios y descarta un
valor vacio tras el recorte o con un salto de linea al leer un parte de
rodaje editado a mano, normalizandolo a `""` (nunca error fatal) -- mismo
criterio que aplica `guion.js` al teclearlo, para que ninguno de los dos
puntos de entrada deje llegar a `concat_ffmpeg.py` un valor que su
validador tendria que rechazar en la ruta real de generacion.

Contrato del archivo exportado y de `estado.json["tomas"]`: `references/contrato-tomas.md`.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from estado import EstadoProyecto


class RegistroTomasError(Exception):
    """Parte de rodaje ilegible, de otro guion o con estructura invalida.

    El mensaje del propio error ya es el texto accionable en espanol (mismo
    contrato que `entrada.EntradaError`/`estado.EstadoError`).
    """


@dataclass(frozen=True)
class Toma:
    """Una toma real de una escena, tal como la cronometro el reproductor."""

    numero: int
    duracion_segundos: float
    nota: str
    buena: bool
    archivo_video: str = ""


@dataclass(frozen=True)
class TomasEscena:
    """Todas las tomas registradas para una escena en una sesion de rodaje."""

    numero_escena: int
    titulo: str
    tomas: tuple[Toma, ...]


@dataclass(frozen=True)
class ParteDeRodaje:
    """El archivo `.json` completo que exporta el boton "Exportar parte de rodaje"."""

    guion: str
    escenas: tuple[TomasEscena, ...]


def _requerido(bruto: dict[str, Any], clave: str, contexto: str) -> Any:
    if clave not in bruto:
        raise RegistroTomasError(f"{contexto}: falta la clave obligatoria '{clave}'.")
    return bruto[clave]


def _sanear_archivo_video(archivo_video: str) -> str:
    """Normaliza `archivo_video` al leer un parte de rodaje editado a mano
    (R-21, requisito 2): recorta espacios y, si queda vacio tras el recorte o
    contiene un salto de linea, se trata como "sin anotar" (`""`) en vez de
    como error fatal -- el dueno no pierde el parte de rodaje por una entrada
    invalida en un solo campo opcional. Mismo criterio que aplica
    `guion.js` al teclear el valor, para que ninguno de los dos puntos de
    entrada deje pasar un valor que `concat_ffmpeg.py` tendria luego que
    rechazar en la ruta real de generacion (hallazgo `#27`)."""
    recortado = archivo_video.strip()
    if not recortado or "\n" in recortado or "\r" in recortado:
        return ""
    return recortado


def _toma_desde_dict(bruto: Any, contexto: str) -> Toma:
    if not isinstance(bruto, dict):
        raise RegistroTomasError(
            f"{contexto}: cada toma debe ser un objeto, no {type(bruto).__name__}."
        )
    try:
        numero = int(_requerido(bruto, "numero", contexto))
        duracion = float(_requerido(bruto, "duracion_segundos", contexto))
    except (TypeError, ValueError) as excepcion:
        raise RegistroTomasError(
            f"{contexto}: 'numero'/'duracion_segundos' deben ser numericos ({excepcion})."
        ) from excepcion
    if numero <= 0:
        raise RegistroTomasError(f"{contexto}: el numero de toma debe ser positivo ({numero}).")
    if duracion < 0:
        raise RegistroTomasError(f"{contexto}: la duracion no puede ser negativa ({duracion}).")
    nota = bruto.get("nota", "")
    if not isinstance(nota, str):
        raise RegistroTomasError(f"{contexto}: la nota debe ser texto.")
    archivo_video = bruto.get("archivo_video", "")
    if not isinstance(archivo_video, str):
        raise RegistroTomasError(f"{contexto}: 'archivo_video' debe ser texto.")
    archivo_video = _sanear_archivo_video(archivo_video)
    return Toma(
        numero=numero,
        duracion_segundos=duracion,
        nota=nota,
        buena=bool(bruto.get("buena", False)),
        archivo_video=archivo_video,
    )


def _escena_desde_dict(bruto: Any, indice: int) -> TomasEscena:
    contexto_escena = f"Escena en la posicion {indice} del parte de rodaje"
    if not isinstance(bruto, dict):
        raise RegistroTomasError(
            f"{contexto_escena}: debe ser un objeto, no {type(bruto).__name__}."
        )
    try:
        numero = int(_requerido(bruto, "numero", contexto_escena))
    except (TypeError, ValueError) as excepcion:
        raise RegistroTomasError(
            f"{contexto_escena}: 'numero' debe ser numerico ({excepcion})."
        ) from excepcion
    titulo = bruto.get("titulo", "")
    if not isinstance(titulo, str):
        raise RegistroTomasError(f"Escena {numero}: el titulo debe ser texto.")
    tomas_bruto = bruto.get("tomas", [])
    if not isinstance(tomas_bruto, list):
        raise RegistroTomasError(f"Escena {numero}: 'tomas' debe ser una lista.")
    tomas = tuple(
        _toma_desde_dict(toma, f"Escena {numero}, toma en la posicion {i}")
        for i, toma in enumerate(tomas_bruto)
    )
    return TomasEscena(numero_escena=numero, titulo=titulo, tomas=tomas)


def cargar_parte_de_rodaje(ruta: Path, nombre_guion: str) -> ParteDeRodaje:
    """Lee y valida el `.json` exportado por "Exportar parte de rodaje".

    `nombre_guion` es el mismo identificador con el que se genero el reproductor
    (`generar_reproductor_html(..., nombre_guion=...)`, tambien `datos.guion` en
    `guion.js`): un archivo de otro guion se rechaza en vez de fusionarse por
    error, mismo criterio que ya usa la importacion de preferencias de R-01.
    """
    if not ruta.exists():
        raise RegistroTomasError(f"No existe el archivo de parte de rodaje: {ruta}")
    try:
        bruto = json.loads(ruta.read_text(encoding="utf-8"))
    except json.JSONDecodeError as excepcion:
        raise RegistroTomasError(
            f"El archivo de parte de rodaje no es JSON valido: {ruta}. Detalle: {excepcion}"
        ) from excepcion
    if not isinstance(bruto, dict):
        raise RegistroTomasError(f"El archivo de parte de rodaje debe contener un objeto: {ruta}")

    guion_archivo = bruto.get("guion")
    if guion_archivo != nombre_guion:
        raise RegistroTomasError(
            f'El parte de rodaje es de otro guion ("{guion_archivo}"), no de "{nombre_guion}".'
        )
    escenas_bruto = bruto.get("escenas", [])
    if not isinstance(escenas_bruto, list):
        raise RegistroTomasError(f"'escenas' debe ser una lista en {ruta}.")

    escenas = tuple(
        _escena_desde_dict(escena, indice) for indice, escena in enumerate(escenas_bruto)
    )
    return ParteDeRodaje(guion=guion_archivo, escenas=escenas)


def _toma_a_dict(toma: Toma) -> dict[str, Any]:
    return {
        "numero": toma.numero,
        "duracion_segundos": toma.duracion_segundos,
        "nota": toma.nota,
        "buena": toma.buena,
        "archivo_video": toma.archivo_video,
    }


def toma_buena(
    tomas_escena: dict[str, Any] | None, numero_escena: int | None = None
) -> dict[str, Any] | None:
    """La toma marcada `buena` de una escena, tal cual viene fusionada en
    `EstadoProyecto.tomas` (claves de escena en texto, ver
    `references/contrato-tomas.md`). `None` si la escena no tiene tomas
    todavia o ninguna esta marcada `buena` -- nunca se elige una toma sin
    marcar ni se promedia entre varias.

    `numero_escena` es opcional, solo para que el mensaje de error senale la
    escena exacta cuando quien llama ya lo sabe (R-04/R-05/R-07/R-19 lo
    conocen todos). Si hay MAS de una toma marcada `buena` (dato corrupto,
    hallazgo #16 de R-11), se rechaza con `RegistroTomasError` en vez de
    elegir la primera en silencio -- unica fuente de esta regla de
    exclusividad; `duracion_toma_buena` (R-04/R-05/R-07) y `concat_ffmpeg.py`
    (R-19, para leer `archivo_video`) la reutilizan tal cual, en vez de
    reimplementarla cada uno por su lado."""
    if tomas_escena is None:
        return None
    buenas = [toma for toma in tomas_escena.get("tomas", []) if toma.get("buena")]
    if len(buenas) > 1:
        contexto = f"la escena {numero_escena}" if numero_escena is not None else "una escena"
        numeros = ", ".join(str(toma.get("numero")) for toma in buenas)
        raise RegistroTomasError(
            f"Parte de rodaje ambiguo en {contexto}: {len(buenas)} tomas marcadas "
            f"'buena' a la vez (numeros {numeros}). Como mucho una toma puede ser la "
            "buena por escena -- corrige el dato (a mano en el .json exportado o "
            "en estado.json) antes de continuar."
        )
    return buenas[0] if buenas else None


def duracion_toma_buena(
    tomas_escena: dict[str, Any] | None, numero_escena: int | None = None
) -> float | None:
    """Duracion real (segundos) de la toma marcada `buena` de una escena
    (`toma_buena`, que resuelve la exclusividad); `None` si no hay ninguna
    toma buena todavia."""
    toma = toma_buena(tomas_escena, numero_escena)
    if toma is None:
        return None
    duracion = toma.get("duracion_segundos")
    return float(duracion) if duracion is not None else None


def registrar_tomas(estado: EstadoProyecto, parte: ParteDeRodaje) -> EstadoProyecto:
    """Fusiona `parte` en `estado.tomas`, escena a escena.

    El reproductor exporta siempre el historial completo de tomas que tiene en
    memoria en el momento de la exportacion, asi que la escena mas reciente
    reemplaza por completo a la anterior version guardada de esa MISMA escena
    (nunca se duplican tomas). Una escena que esta exportacion ni siquiera
    menciona (porque no se grabo en esa sesion) conserva intactas las tomas que
    ya tuviera de una sesion anterior -- nunca se borra en silencio lo que esta
    exportacion no toco.
    """
    tomas = dict(estado.tomas)
    for escena in parte.escenas:
        if not escena.tomas:
            continue
        tomas[str(escena.numero_escena)] = {
            "titulo": escena.titulo,
            "tomas": [_toma_a_dict(toma) for toma in escena.tomas],
        }
    estado.tomas = tomas
    return estado
