"""Migracion 002: anade el contenedor `tomas` a `estado.json` (tarea R-02).

Registro de tomas por escena (numero, duracion real, nota, marca de "buena"),
fusionado desde el parte de rodaje que exporta el reproductor tras una sesion de
grabacion (`scripts/tomas.py`). Mismo patron que el resto de contenedores
genericos reservados en la migracion 001 (`validacion`, `salidas_generadas`): un
dict vacio hasta que exista un productor de datos real.
"""

from __future__ import annotations

from typing import Any

VERSION_DESTINO = 2


def aplicar(datos: dict[str, Any]) -> dict[str, Any]:
    """Completa `datos` hasta el esquema version 2 sin perder lo que ya trae.

    Idempotente: si `datos` ya esta en `VERSION_DESTINO`, lo devuelve tal cual.
    """
    if datos.get("version_esquema") == VERSION_DESTINO:
        return datos

    migrado = dict(datos)
    migrado.setdefault("tomas", {})
    migrado["version_esquema"] = VERSION_DESTINO
    return migrado
