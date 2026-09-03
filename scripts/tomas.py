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

`duracion_toma_buena` (publica, no `_`) es el criterio ya establecido por R-04
para leer "la" duracion real de una escena a partir de `estado.tomas`: la de la
toma marcada `buena`, `None` si ninguna lo esta todavia (una escena con tomas
sin marcar no aporta evidencia real, nunca se estima ni se promedia entre
tomas sin validar). R-04 (`calibracion.py`) y R-05 (`srt_alineado.py`)
comparten esta misma funcion en vez de cada uno reimplementar el mismo
criterio por su cuenta.

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
    return Toma(
        numero=numero,
        duracion_segundos=duracion,
        nota=nota,
        buena=bool(bruto.get("buena", False)),
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
    }


def duracion_toma_buena(tomas_escena: dict[str, Any] | None) -> float | None:
    """Duracion real (segundos) de la toma marcada `buena` de una escena, tal
    como viene fusionada en `EstadoProyecto.tomas` (claves de escena en texto,
    ver `references/contrato-tomas.md`). `None` si la escena no tiene tomas
    todavia o ninguna esta marcada `buena` -- nunca se elige una toma sin
    marcar ni se promedia entre varias."""
    if tomas_escena is None:
        return None
    for toma in tomas_escena.get("tomas", []):
        if toma.get("buena"):
            duracion = toma.get("duracion_segundos")
            return float(duracion) if duracion is not None else None
    return None


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
