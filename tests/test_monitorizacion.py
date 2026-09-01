"""Tests de la monitorizacion de errores local (T-05).

Cubren el criterio de aceptacion literal ("un fallo provocado en un test produce
mensaje accionable + archivo de diagnostico, y el proceso termina con codigo de
salida distinto de 0"), que el diagnostico nunca arrastra el contenido integro del
guion de entrada, y el resumen final de la ejecucion.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from monitorizacion import ResumenEjecucion, ejecutar_con_diagnostico, ruta_diagnostico


def test_funcion_sin_errores_propaga_su_codigo_de_salida(tmp_path: Path) -> None:
    assert ejecutar_con_diagnostico(lambda: 0, tmp_path) == 0
    assert not list(tmp_path.glob("diagnostico-*.log"))


def test_excepcion_no_controlada_produce_codigo_de_salida_distinto_de_cero(
    tmp_path: Path,
) -> None:
    def falla() -> int:
        raise RuntimeError("fallo provocado para el test")

    assert ejecutar_con_diagnostico(falla, tmp_path) != 0


def test_excepcion_no_controlada_vuelca_archivo_de_diagnostico(tmp_path: Path) -> None:
    def falla() -> int:
        raise RuntimeError("fallo provocado para el test")

    ejecutar_con_diagnostico(falla, tmp_path)

    archivos = list(tmp_path.glob("diagnostico-*.log"))
    assert len(archivos) == 1
    contenido = archivos[0].read_text(encoding="utf-8")
    assert "RuntimeError" in contenido
    assert "fallo provocado para el test" in contenido


def test_excepcion_no_controlada_muestra_mensaje_accionable_sin_traza_cruda(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    def falla() -> int:
        raise RuntimeError("fallo provocado para el test")

    ejecutar_con_diagnostico(falla, tmp_path)

    salida = capsys.readouterr().err
    assert "error inesperado" in salida.lower()
    assert "Traceback" not in salida
    assert "RuntimeError" not in salida


def test_diagnostico_no_incluye_el_contenido_integro_del_guion(tmp_path: Path) -> None:
    """El volcado no debe arrastrar variables locales: si el guion completo esta en
    una variable local del marco donde salta la excepcion, no debe aparecer en el
    archivo de diagnostico (regla dura de T-05: solo referencias de posicion)."""
    texto_guion_secreto = "LOCUCIÓN de un guion real que jamas deberia salir en un log"

    def falla() -> int:
        contenido_del_guion = texto_guion_secreto  # noqa: F841 - variable local a propósito
        raise RuntimeError("fallo generico, sin detalle de posicion")

    ejecutar_con_diagnostico(falla, tmp_path)

    archivos = list(tmp_path.glob("diagnostico-*.log"))
    contenido = archivos[0].read_text(encoding="utf-8")
    assert texto_guion_secreto not in contenido


def test_ruta_diagnostico_usa_el_prefijo_configurado(tmp_path: Path) -> None:
    ruta = ruta_diagnostico(tmp_path, instante="20260901T000000000000")
    assert ruta.name == "diagnostico-20260901T000000000000.log"
    assert ruta.parent == tmp_path


def test_resumen_ejecucion_por_defecto_esta_en_cero() -> None:
    resumen = ResumenEjecucion()
    assert resumen.escenas_procesadas == 0
    assert resumen.bloques == 0
    assert resumen.avisos == 0
    assert resumen.reescrituras == 0
    assert resumen.salidas_generadas == ()


def test_resumen_ejecucion_muestra_los_recuentos(capsys: pytest.CaptureFixture[str]) -> None:
    resumen = ResumenEjecucion(
        escenas_procesadas=5,
        bloques=42,
        avisos=2,
        reescrituras=1,
        salidas_generadas=("reproductor.html", "guion.srt"),
    )
    resumen.mostrar_resumen()

    salida = capsys.readouterr().out
    assert "5" in salida
    assert "42" in salida
    assert "reproductor.html" in salida
    assert "guion.srt" in salida


def test_resumen_ejecucion_sin_salidas_lo_dice_explicitamente(
    capsys: pytest.CaptureFixture[str],
) -> None:
    ResumenEjecucion().mostrar_resumen()
    salida = capsys.readouterr().out
    assert "ninguna" in salida.lower()
