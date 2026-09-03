"""Tests de la CI local (T-04): `scripts/ci.py`."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from ci import (
    ETAPAS,
    Etapa,
    avisar_si_version_python_diverge,
    codigo_salida_agregado,
    ejecutar_etapa,
    version_minima_declarada,
)


def test_etapas_cubren_las_cuatro_verificaciones_del_protocolo() -> None:
    comandos = [" ".join(etapa.comando) for etapa in ETAPAS]
    assert any("mypy" in comando for comando in comandos)
    assert any("ruff" in comando and "check" in comando for comando in comandos)
    assert any("pytest" in comando for comando in comandos)
    assert any("verificar_salidas.py" in comando and "--fixture" in comando for comando in comandos)


def test_etapas_se_ejecutan_en_el_orden_del_protocolo() -> None:
    """Orden de §0.1: tipos, estilo, tests, extremo a extremo."""
    nombres = [etapa.nombre.lower() for etapa in ETAPAS]
    indice_mypy = next(i for i, n in enumerate(nombres) if "mypy" in n)
    indice_ruff = next(i for i, n in enumerate(nombres) if "ruff" in n)
    indice_pytest = next(i for i, n in enumerate(nombres) if "pytest" in n)
    indice_e2e = next(i for i, n in enumerate(nombres) if "verificar_salidas" in n)
    assert indice_mypy < indice_ruff < indice_pytest < indice_e2e


def test_codigo_salida_agregado_es_cero_solo_si_todo_pasa() -> None:
    assert codigo_salida_agregado([True, True, True, True]) == 0
    assert codigo_salida_agregado([True, False, True, True]) == 1
    assert codigo_salida_agregado([]) == 0


def test_ejecutar_etapa_devuelve_true_si_el_comando_sale_con_cero() -> None:
    etapa = Etapa("etapa de prueba (ok)", (sys.executable, "-c", "import sys; sys.exit(0)"))
    assert ejecutar_etapa(etapa) is True


def test_ejecutar_etapa_devuelve_false_si_el_comando_falla() -> None:
    etapa = Etapa("etapa de prueba (fallo)", (sys.executable, "-c", "import sys; sys.exit(1)"))
    assert ejecutar_etapa(etapa) is False


def test_version_minima_declarada_reconoce_el_especificador_de_pyproject() -> None:
    assert version_minima_declarada(">=3.12") == (3, 12)
    assert version_minima_declarada(">= 3.9") == (3, 9)


def test_version_minima_declarada_ignora_especificadores_no_reconocidos() -> None:
    assert version_minima_declarada("") is None
    assert version_minima_declarada("==3.12.*") is None


def test_avisar_si_version_python_diverge_avisa_cuando_el_real_no_alcanza(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """`pyproject.toml` real declara `>=3.12` (R-08, requisito 3, ver DECISIONES_TECNICAS.md):
    un interprete real 3.11 no lo cumple y debe avisar sin lanzar excepcion."""
    avisar_si_version_python_diverge(real=(3, 11))
    salida = capsys.readouterr()
    assert "AVISO" in salida.err
    assert "3.11" in salida.err


def test_avisar_si_version_python_diverge_no_avisa_cuando_el_real_cumple(
    capsys: pytest.CaptureFixture[str],
) -> None:
    avisar_si_version_python_diverge(real=(3, 99))
    salida = capsys.readouterr()
    assert salida.err == ""
