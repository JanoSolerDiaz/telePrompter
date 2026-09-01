"""Migraciones idempotentes del esquema de `estado.json` (tarea T-07).

Cada migracion vive en su propio archivo `NNN_<nombre>.py` dentro de este paquete,
con dos nombres fijos a nivel de modulo:

- `VERSION_DESTINO: int` -- la version de esquema a la que deja los datos.
- `aplicar(datos: dict) -> dict` -- transforma los datos de la version anterior a
  `VERSION_DESTINO`, PRESERVANDO cualquier clave ya presente (validaciones y
  ediciones del dueno incluidas, invariante (c) de §0.2) y completando solo lo que
  falte con valores por defecto. Debe ser idempotente: aplicarla sobre datos que ya
  estan en `VERSION_DESTINO` los devuelve sin tocar nada mas.

`aplicar_migraciones` descubre los archivos por convencion de nombre (prefijo
numerico), los ordena y aplica en cadena solo los que faltan, segun la clave
`version_esquema` de los datos (0 si no existe: un `estado.json` de antes de que
existiera versionado, o un dict recien creado a mano).

El prefijo numerico hace que el nombre de archivo no sea un identificador Python
valido (`001_estado_inicial` no se puede usar tras `import`); se cargan por eso con
`importlib.import_module`, que no exige esa restriccion -- mismo mecanismo que usan
las migraciones de Django.
"""

from __future__ import annotations

import importlib
import re
from pathlib import Path
from typing import Any

_PATRON_ARCHIVO_MIGRACION = re.compile(r"^(\d+)_[a-z0-9_]+\.py$")


def _migraciones_disponibles() -> list[tuple[int, Any]]:
    """Importa y ordena por numero de version todas las migraciones del paquete."""
    carpeta = Path(__file__).resolve().parent
    migraciones: list[tuple[int, Any]] = []
    for ruta in sorted(carpeta.iterdir()):
        if not _PATRON_ARCHIVO_MIGRACION.match(ruta.name):
            continue
        modulo = importlib.import_module(f"{__name__}.{ruta.stem}")
        migraciones.append((modulo.VERSION_DESTINO, modulo.aplicar))
    migraciones.sort(key=lambda par: par[0])
    return migraciones


def aplicar_migraciones(datos: dict[str, Any]) -> dict[str, Any]:
    """Aplica en cadena, y en orden, las migraciones pendientes sobre `datos`.

    Nunca muta el dict recibido: cada migracion devuelve un dict nuevo (o el mismo
    sin cambios si ya esta al dia).
    """
    version_actual = datos.get("version_esquema", 0)
    for version_destino, aplicar_migracion in _migraciones_disponibles():
        if version_destino > version_actual:
            datos = aplicar_migracion(datos)
            version_actual = version_destino
    return datos
