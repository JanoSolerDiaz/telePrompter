"""Migracion 001: establece el esquema de `estado.json` version 1 (tarea T-07).

No parte de una version anterior real con su propio numero: es la primera vez que
`estado.json` tiene esquema versionado, asi que cualquier dict sin `version_esquema`
(o con ese valor por debajo de `VERSION_DESTINO`) se trata como "version anterior" --
puede ser un `estado.json` vacio o uno con datos parciales que ya existieran antes de
que este esquema se formalizara. En ambos casos `aplicar` PRESERVA cualquier clave ya
presente (invariante (c) de §0.2: la edicion manual del dueno manda) y solo completa
las que faltan con los valores por defecto de la version 1.
"""

from __future__ import annotations

from typing import Any

VERSION_DESTINO = 1

_CLAVES_POR_DEFECTO: dict[str, Any] = {
    "configuracion_efectiva": {},
    "separador_escena": {"nivel": None, "patron": None},
    "escenas": [],
    "reescrituras": [],
    "validacion": {},
    "salidas_generadas": [],
}


def aplicar(datos: dict[str, Any]) -> dict[str, Any]:
    """Completa `datos` hasta el esquema version 1 sin perder lo que ya trae.

    Idempotente: si `datos` ya esta en `VERSION_DESTINO`, lo devuelve tal cual.
    """
    if datos.get("version_esquema") == VERSION_DESTINO:
        return datos

    migrado = dict(datos)
    for clave, valor_por_defecto in _CLAVES_POR_DEFECTO.items():
        migrado.setdefault(clave, valor_por_defecto)
    migrado["version_esquema"] = VERSION_DESTINO
    return migrado
