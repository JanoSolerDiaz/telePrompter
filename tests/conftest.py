"""Fixtures compartidas de la suite (T-03).

Punto unico donde vive el acceso a los guiones reales de calibracion
(`fixtures/reales/`) para que T-08 a T-13 y T-27 no repitan la ruta ni la carga.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

RAIZ = Path(__file__).resolve().parent.parent
CARPETA_GUIONES_REALES = RAIZ / "fixtures" / "reales"
RUTA_GUION_EJEMPLO = RAIZ / "fixtures" / "guion-ejemplo.md"
RUTA_GUION_EJEMPLO_ESPERADO = RAIZ / "fixtures" / "guion-ejemplo-esperado.md"


@pytest.fixture
def guiones_reales() -> list[Path]:
    """Los guiones de produccion reales aportados por el dueno para calibracion.

    Tres guiones (`origen: bloqueo #3 de SEGUIMIENTO, resuelto 2026-08-31`) que fijan
    la convencion contractual de §0.2. Cualquier test que necesite texto de guion real
    en vez de un `.md` inventado debe usar esta fixture, no rutas sueltas.
    """
    rutas = sorted(CARPETA_GUIONES_REALES.glob("*.md"))
    assert rutas, f"no hay guiones reales en {CARPETA_GUIONES_REALES}"
    return rutas


@pytest.fixture
def texto_guiones_reales(guiones_reales: list[Path]) -> dict[str, str]:
    """Contenido de cada guion real, indexado por nombre de archivo."""
    return {ruta.name: ruta.read_text(encoding="utf-8") for ruta in guiones_reales}


@pytest.fixture
def texto_guion_ejemplo() -> str:
    """Contenido de `fixtures/guion-ejemplo.md` (T-32): guion de curso sintetico,
    con locucion mezclada con indicaciones de pantalla, B-roll, una nota interna
    y timestamps, usado como fixture estable de `verificar_salidas.py --fixture`
    y de la instalacion de la skill."""
    assert RUTA_GUION_EJEMPLO.exists(), f"no existe {RUTA_GUION_EJEMPLO}"
    return RUTA_GUION_EJEMPLO.read_text(encoding="utf-8")


@pytest.fixture
def texto_guion_ejemplo_esperado() -> str:
    """Version anotada esperada (`guion-escenas.md` de referencia) de
    `fixtures/guion-ejemplo.md`, regenerada a mano cuando cambie deliberadamente
    el pipeline de T-08 a T-15 -- nunca a ciegas para hacer pasar un test."""
    assert RUTA_GUION_EJEMPLO_ESPERADO.exists(), f"no existe {RUTA_GUION_EJEMPLO_ESPERADO}"
    return RUTA_GUION_EJEMPLO_ESPERADO.read_text(encoding="utf-8")
