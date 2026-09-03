"""Tests de robustez de entrada (T-06): bateria de entradas hostiles.

Cubren el criterio de aceptacion literal: ninguna entrada provoca bucle infinito,
consumo desbocado ni escritura fuera de la carpeta de salida; todas degradan con un
`EntradaError` accionable.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import entrada
from entrada import (
    EntradaError,
    carpeta_salida_para,
    ejecutar_con_limite_de_tiempo,
    leer_guion,
    nombre_guion_seguro,
    validar_ruta_guion,
    verificar_estructura_minima,
)

GUION_VALIDO = (
    "**Duración objetivo:** 1:00\n\n"
    "## BLOQUE 1 — Apertura (0:00 - 0:15)\n\n"
    "**LOCUCIÓN**\n\n"
    "> Hola.\n\n"
    "**EN PANTALLA**\n\n"
    "- Logo\n"
)


# --- validar_ruta_guion ------------------------------------------------------------


def test_ruta_inexistente_levanta_error_entrada(tmp_path: Path) -> None:
    with pytest.raises(EntradaError, match="No existe"):
        validar_ruta_guion(tmp_path / "no-existe.md")


def test_ruta_que_es_carpeta_levanta_error_entrada(tmp_path: Path) -> None:
    carpeta = tmp_path / "una-carpeta.md"
    carpeta.mkdir()
    with pytest.raises(EntradaError, match="carpeta"):
        validar_ruta_guion(carpeta)


def test_guion_vacio_levanta_error_entrada(tmp_path: Path) -> None:
    ruta = tmp_path / "vacio.md"
    ruta.write_text("", encoding="utf-8")
    with pytest.raises(EntradaError, match="vacio"):
        validar_ruta_guion(ruta)


def test_guion_por_encima_del_tamano_maximo_levanta_error_entrada(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(entrada, "TAMANO_GUION_MAX_BYTES", 10)
    ruta = tmp_path / "grande.md"
    ruta.write_text("## BLOQUE 1 — Título (0:00 - 0:10)\n" * 5, encoding="utf-8")
    with pytest.raises(EntradaError, match="TAMANO_GUION_MAX_BYTES"):
        validar_ruta_guion(ruta)


def test_ruta_valida_se_resuelve_a_absoluta(tmp_path: Path) -> None:
    ruta = tmp_path / "guion.md"
    ruta.write_text(GUION_VALIDO, encoding="utf-8")
    resultado = validar_ruta_guion(ruta)
    assert resultado.is_absolute()
    assert resultado == ruta.resolve()


# --- leer_guion: codificacion -------------------------------------------------------


def test_lee_guion_utf8_normal(tmp_path: Path) -> None:
    ruta = tmp_path / "guion.md"
    ruta.write_text(GUION_VALIDO, encoding="utf-8")
    assert leer_guion(ruta) == GUION_VALIDO


def test_lee_guion_utf8_con_bom(tmp_path: Path) -> None:
    ruta = tmp_path / "guion.md"
    ruta.write_bytes(GUION_VALIDO.encode("utf-8-sig"))
    texto = leer_guion(ruta)
    assert texto == GUION_VALIDO
    assert not texto.startswith("﻿")


def test_guion_no_utf8_levanta_error_entrada(tmp_path: Path) -> None:
    ruta = tmp_path / "guion.md"
    # Secuencia de bytes invalida en UTF-8 (0xff no es un inicio de secuencia valido).
    ruta.write_bytes(b"## BLOQUE 1 \xff\xfe invalido\n")
    with pytest.raises(EntradaError, match="UTF-8"):
        leer_guion(ruta)


def test_guion_solo_espacios_en_blanco_levanta_error_entrada(tmp_path: Path) -> None:
    ruta = tmp_path / "guion.md"
    ruta.write_text("   \n\t\n   ", encoding="utf-8")
    with pytest.raises(EntradaError, match="vacio"):
        leer_guion(ruta)


def test_ruta_con_acentos_y_espacios_se_lee_bien(tmp_path: Path) -> None:
    ruta = tmp_path / "guión de producción número 1.md"
    ruta.write_text(GUION_VALIDO, encoding="utf-8")
    assert leer_guion(ruta) == GUION_VALIDO


# --- verificar_estructura_minima ----------------------------------------------------


def test_guion_sin_encabezados_levanta_error_entrada() -> None:
    with pytest.raises(EntradaError, match="encabezado"):
        verificar_estructura_minima("Solo texto suelto, sin ningun encabezado Markdown.\n")


def test_guion_con_demasiados_encabezados_levanta_error_entrada(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(entrada, "ESCENAS_MAX", 3)
    texto = "\n\n".join(f"## BLOQUE {n} — Título (0:00 - 0:10)" for n in range(1, 10))
    with pytest.raises(EntradaError, match="ESCENAS_MAX"):
        verificar_estructura_minima(texto)


def test_guion_con_encabezados_dentro_del_limite_no_falla() -> None:
    verificar_estructura_minima(GUION_VALIDO)


# --- nombre_guion_seguro / carpeta_salida_para --------------------------------------


def test_nombre_guion_seguro_conserva_un_nombre_normal() -> None:
    assert nombre_guion_seguro(Path("guion-08-busqueda-investigacion.md")) == (
        "guion-08-busqueda-investigacion"
    )


def test_nombre_guion_seguro_neutraliza_secuencias_de_puntos() -> None:
    resultado = nombre_guion_seguro(Path("..guion..raro..md"))
    assert ".." not in resultado


def test_nombre_guion_seguro_nunca_vacio() -> None:
    assert nombre_guion_seguro(Path("....md")) == "guion"


def test_carpeta_salida_para_queda_dentro_de_la_carpeta_del_guion(tmp_path: Path) -> None:
    ruta = tmp_path / "mi guion.md"
    ruta.write_text(GUION_VALIDO, encoding="utf-8")
    carpeta = carpeta_salida_para(ruta)
    assert carpeta.parent == tmp_path.resolve()
    assert carpeta.name == "mi guion-teleprompter"


def test_carpeta_salida_para_con_acentos(tmp_path: Path) -> None:
    ruta = tmp_path / "guión número 1.md"
    ruta.write_text(GUION_VALIDO, encoding="utf-8")
    carpeta = carpeta_salida_para(ruta)
    assert carpeta.parent == tmp_path.resolve()
    carpeta.relative_to(tmp_path.resolve())


# --- migracion de la carpeta de salida heredada (R-06) ------------------------------


def test_carpeta_salida_para_migra_una_carpeta_heredada_con_sufijo_antiguo(
    tmp_path: Path,
) -> None:
    ruta = tmp_path / "mi guion.md"
    ruta.write_text(GUION_VALIDO, encoding="utf-8")
    carpeta_antigua = tmp_path / "mi guion-tarjetas"
    carpeta_antigua.mkdir()
    (carpeta_antigua / "estado.json").write_text('{"version_esquema": 2}', encoding="utf-8")
    (carpeta_antigua / "guion-escenas.md").write_text("edicion del dueno", encoding="utf-8")

    carpeta = carpeta_salida_para(ruta)

    assert carpeta.name == "mi guion-teleprompter"
    assert carpeta.is_dir()
    assert (carpeta / "estado.json").read_text(encoding="utf-8") == '{"version_esquema": 2}'
    assert (carpeta / "guion-escenas.md").read_text(encoding="utf-8") == "edicion del dueno"
    assert not carpeta_antigua.exists()


def test_carpeta_salida_para_migracion_deja_copia_de_seguridad(tmp_path: Path) -> None:
    ruta = tmp_path / "mi guion.md"
    ruta.write_text(GUION_VALIDO, encoding="utf-8")
    carpeta_antigua = tmp_path / "mi guion-tarjetas"
    carpeta_antigua.mkdir()
    (carpeta_antigua / "estado.json").write_text('{"version_esquema": 2}', encoding="utf-8")

    carpeta_salida_para(ruta)

    copias = list(tmp_path.glob("mi guion-tarjetas.bak-*"))
    assert len(copias) == 1
    assert (copias[0] / "estado.json").read_text(encoding="utf-8") == '{"version_esquema": 2}'


def test_carpeta_salida_para_sin_carpeta_heredada_no_migra_nada(tmp_path: Path) -> None:
    ruta = tmp_path / "mi guion.md"
    ruta.write_text(GUION_VALIDO, encoding="utf-8")

    carpeta = carpeta_salida_para(ruta)

    assert not carpeta.exists()
    assert list(tmp_path.iterdir()) == [ruta]


def test_carpeta_salida_para_no_pisa_una_carpeta_nueva_ya_existente(tmp_path: Path) -> None:
    ruta = tmp_path / "mi guion.md"
    ruta.write_text(GUION_VALIDO, encoding="utf-8")
    carpeta_nueva = tmp_path / "mi guion-teleprompter"
    carpeta_nueva.mkdir()
    (carpeta_nueva / "estado.json").write_text(
        '{"version_esquema": 2, "vivo": true}', encoding="utf-8"
    )
    carpeta_antigua = tmp_path / "mi guion-tarjetas"
    carpeta_antigua.mkdir()
    (carpeta_antigua / "estado.json").write_text('{"version_esquema": 1}', encoding="utf-8")

    carpeta = carpeta_salida_para(ruta)

    assert carpeta == carpeta_nueva
    assert (carpeta / "estado.json").read_text(encoding="utf-8") == (
        '{"version_esquema": 2, "vivo": true}'
    )
    assert carpeta_antigua.exists()


def test_carpeta_salida_para_con_sufijo_explicito_no_dispara_migracion(tmp_path: Path) -> None:
    ruta = tmp_path / "mi guion.md"
    ruta.write_text(GUION_VALIDO, encoding="utf-8")
    carpeta_antigua = tmp_path / "mi guion-tarjetas"
    carpeta_antigua.mkdir()

    carpeta = carpeta_salida_para(ruta, sufijo="-tarjetas")

    assert carpeta == carpeta_antigua
    assert carpeta_antigua.exists()
    assert not (tmp_path / "mi guion-teleprompter").exists()


# --- ejecutar_con_limite_de_tiempo ---------------------------------------------------


def test_ejecutar_con_limite_de_tiempo_devuelve_el_resultado_si_termina_a_tiempo() -> None:
    assert ejecutar_con_limite_de_tiempo(lambda: 42, segundos=1) == 42


def test_ejecutar_con_limite_de_tiempo_corta_una_funcion_que_no_termina() -> None:
    def nunca_termina() -> int:
        time.sleep(5)
        return 1

    inicio = time.monotonic()
    with pytest.raises(EntradaError, match="tiempo maximo"):
        ejecutar_con_limite_de_tiempo(nunca_termina, segundos=0.1)
    transcurrido = time.monotonic() - inicio

    assert transcurrido < 2.0
