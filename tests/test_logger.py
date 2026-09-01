"""Tests del logger centralizado de diagnostico (T-02).

Cubren lo que pide la tarea: el log se escribe dentro de la carpeta de salida
indicada (nunca fuera), `--verbose` es lo unico que decide si ademas se ve por
consola, y configurar el logger varias veces (como ocurre entre tests) no acumula
manejadores ni duplica lineas.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from config import NOMBRE_ARCHIVO_LOG
from logger import configurar_logger, obtener_logger


def test_configurar_logger_crea_el_archivo_dentro_de_la_carpeta_de_salida(
    tmp_path: Path,
) -> None:
    carpeta = tmp_path / "mi-guion-tarjetas"
    log = configurar_logger(carpeta, verbose=False)
    log.info("mensaje de prueba")

    archivo = carpeta / NOMBRE_ARCHIVO_LOG
    assert archivo.exists()
    assert "mensaje de prueba" in archivo.read_text(encoding="utf-8")


def test_configurar_logger_crea_la_carpeta_si_no_existe(tmp_path: Path) -> None:
    carpeta = tmp_path / "no-existe-todavia"
    assert not carpeta.exists()
    configurar_logger(carpeta)
    assert carpeta.is_dir()


def test_nivel_debug_llega_al_archivo_aunque_no_haya_verbose(tmp_path: Path) -> None:
    log = configurar_logger(tmp_path, verbose=False)
    log.debug("detalle tecnico solo para el archivo")

    contenido = (tmp_path / NOMBRE_ARCHIVO_LOG).read_text(encoding="utf-8")
    assert "detalle tecnico solo para el archivo" in contenido


def _manejadores_de_consola(log: logging.Logger) -> list[logging.Handler]:
    return [
        h
        for h in log.handlers
        if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)
    ]


def test_verbose_anade_un_manejador_de_consola(tmp_path: Path) -> None:
    log_sin_verbose = configurar_logger(tmp_path, verbose=False)
    assert _manejadores_de_consola(log_sin_verbose) == []

    log_con_verbose = configurar_logger(tmp_path, verbose=True)
    assert len(_manejadores_de_consola(log_con_verbose)) == 1


def test_configurar_logger_es_idempotente_no_acumula_manejadores(tmp_path: Path) -> None:
    configurar_logger(tmp_path, verbose=True)
    configurar_logger(tmp_path, verbose=True)
    log = configurar_logger(tmp_path, verbose=True)

    assert len(log.handlers) == 2  # un FileHandler + un StreamHandler, nunca mas


def test_obtener_logger_devuelve_el_mismo_logger_configurado(tmp_path: Path) -> None:
    configurado = configurar_logger(tmp_path)
    assert obtener_logger() is configurado


def test_acentos_y_ees_se_escriben_correctamente_en_utf8(tmp_path: Path) -> None:
    log = configurar_logger(tmp_path)
    log.info("Guión con eñes y acentos: canción, mañana, revisión")

    contenido = (tmp_path / NOMBRE_ARCHIVO_LOG).read_text(encoding="utf-8")
    assert "Guión con eñes y acentos: canción, mañana, revisión" in contenido
