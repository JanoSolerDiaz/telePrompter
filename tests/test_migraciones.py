"""Tests del mecanismo de migraciones de `estado.json` (T-07).

Criterio de aceptacion literal: aplicar la migracion 001 sobre un `estado.json` de
version anterior no pierde validaciones ni ediciones ya presentes.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import migraciones
from migraciones import aplicar_migraciones

_m001 = importlib.import_module("migraciones.001_estado_inicial")
_m002 = importlib.import_module("migraciones.002_tomas")


def _estado_version_anterior_con_datos() -> dict[str, Any]:
    """Simula un `estado.json` de antes de que el esquema tuviera version: sin la
    clave `version_esquema`, pero ya con validaciones y ediciones del dueno que no
    se pueden perder al migrar."""
    return {
        "guion": {"ruta": "/guiones/mi-guion.md", "hash_sha256": "abc123", "tamano_bytes": 42},
        "escenas": [{"id": 1, "titulo": "Apertura", "clasificacion": "locucion"}],
        "reescrituras": [{"original": "vale", "propuesta": "de acuerdo", "aceptada": True}],
        "validacion": {"1": "validada a mano por el dueno"},
        "creado_en": "2026-08-31T10:00:00+00:00",
        "actualizado_en": "2026-08-31T10:00:00+00:00",
    }


def test_migracion_001_anade_version_esquema() -> None:
    migrado = _m001.aplicar(_estado_version_anterior_con_datos())
    assert migrado["version_esquema"] == _m001.VERSION_DESTINO


def test_migracion_001_no_pierde_escenas_reescrituras_ni_validaciones() -> None:
    original = _estado_version_anterior_con_datos()
    migrado = _m001.aplicar(original)

    assert migrado["escenas"] == original["escenas"]
    assert migrado["reescrituras"] == original["reescrituras"]
    assert migrado["validacion"] == original["validacion"]
    assert migrado["guion"] == original["guion"]


def test_migracion_001_completa_las_claves_que_faltan_con_defectos() -> None:
    migrado = _m001.aplicar(_estado_version_anterior_con_datos())
    assert migrado["separador_escena"] == {"nivel": None, "patron": None}
    assert migrado["salidas_generadas"] == []
    assert migrado["configuracion_efectiva"] == {}


def test_migracion_001_es_idempotente() -> None:
    una_vez = _m001.aplicar(_estado_version_anterior_con_datos())
    dos_veces = _m001.aplicar(dict(una_vez))
    assert una_vez == dos_veces


def test_migracion_001_no_muta_el_dict_original() -> None:
    original = _estado_version_anterior_con_datos()
    copia = dict(original)
    _m001.aplicar(original)
    assert original == copia


def test_aplicar_migraciones_deja_intacto_un_estado_ya_al_dia() -> None:
    datos = aplicar_migraciones(_estado_version_anterior_con_datos())
    assert aplicar_migraciones(dict(datos)) == datos


def test_aplicar_migraciones_desde_dict_vacio_produce_esquema_completo() -> None:
    migrado = aplicar_migraciones({})
    assert migrado["version_esquema"] == 2
    for clave in (
        "configuracion_efectiva",
        "separador_escena",
        "escenas",
        "reescrituras",
        "validacion",
        "salidas_generadas",
        "tomas",
    ):
        assert clave in migrado


def test_hay_al_menos_una_migracion_registrada_en_el_paquete() -> None:
    carpeta = Path(migraciones.__file__).resolve().parent
    archivos_migracion = [p for p in carpeta.iterdir() if p.name[0].isdigit()]
    assert archivos_migracion, "no hay ninguna migracion NNN_<nombre>.py en el paquete"


# --- Migracion 002: contenedor `tomas` (R-02) ---------------------------------------


def test_migracion_002_anade_el_contenedor_tomas_vacio() -> None:
    migrado = _m002.aplicar(_m001.aplicar(_estado_version_anterior_con_datos()))
    assert migrado["tomas"] == {}
    assert migrado["version_esquema"] == _m002.VERSION_DESTINO


def test_migracion_002_no_pierde_nada_de_lo_que_ya_migro_001() -> None:
    tras_001 = _m001.aplicar(_estado_version_anterior_con_datos())
    migrado = _m002.aplicar(tras_001)
    assert migrado["escenas"] == tras_001["escenas"]
    assert migrado["reescrituras"] == tras_001["reescrituras"]
    assert migrado["validacion"] == tras_001["validacion"]


def test_migracion_002_no_pisa_un_contenedor_tomas_ya_presente() -> None:
    datos = _m001.aplicar(_estado_version_anterior_con_datos())
    datos["tomas"] = {"1": {"titulo": "Apertura", "tomas": []}}
    migrado = _m002.aplicar(datos)
    assert migrado["tomas"] == {"1": {"titulo": "Apertura", "tomas": []}}


def test_migracion_002_es_idempotente() -> None:
    una_vez = _m002.aplicar(_m001.aplicar(_estado_version_anterior_con_datos()))
    dos_veces = _m002.aplicar(dict(una_vez))
    assert una_vez == dos_veces


def test_migracion_002_no_muta_el_dict_original() -> None:
    original = _m001.aplicar(_estado_version_anterior_con_datos())
    copia = dict(original)
    _m002.aplicar(original)
    assert original == copia
