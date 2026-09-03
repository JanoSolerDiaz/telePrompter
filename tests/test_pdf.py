"""Tests del exportador `.pdf` con identidad 480 (tarea T-28)."""

from __future__ import annotations

from pathlib import Path

import pytest

from config import Configuracion
from parser import ResultadoParseo, parsear_guion
from pdf import (
    ResultadoPdf,
    convertir_html_a_pdf,
    detectar_ejecutable_chrome,
    dimensiones_png,
    exportar_pdf,
    generar_html_impresion,
    guardar_html_impresion,
)
from tiempos import ResultadoTiempos, calcular_tiempos
from verificar_salidas import buscar_recursos_externos

RAIZ = Path(__file__).resolve().parent.parent
LOGO_REAL = RAIZ / "assets" / "marca" / "480_Gris.png"
CHROMIUM_SANDBOX = Path("/opt/pw-browsers/chromium")

_GUION_DOS_ESCENAS = """# Guion de prueba

## BLOQUE 0 — Arranque (0:00 – 0:10)

**LOCUCIÓN**

> Esta es la primera frase del bloque. Y esta la segunda, ya con más ritmo.

**EN PANTALLA**

Título del vídeo en pantalla.

**NOTA**

Recordatorio interno: no mencionar el precio antiguo en la locución.

## BLOQUE 1 — Cierre (0:10 – 0:20)

**LOCUCIÓN**

> Segunda escena, con su propia frase de cierre para la locución.
"""


def _pipeline(
    texto: str, configuracion: Configuracion | None = None
) -> tuple[ResultadoParseo, ResultadoTiempos]:
    configuracion = configuracion or Configuracion()
    resultado = parsear_guion(texto, configuracion=configuracion)
    tiempos = calcular_tiempos(resultado, configuracion)
    return resultado, tiempos


def _chrome_disponible() -> Path | None:
    """Un Chrome/Edge real para los tests que necesitan convertir de verdad.

    Usa la misma deteccion del modulo y, si no encuentra nada (maquina de
    desarrollo o CI sin Chrome instalado), recurre al Chromium que trae este
    entorno para Playwright -- no es una dependencia del proyecto, solo hace
    que el test no se quede sin ninguna maquina real donde ejecutarse."""
    detectado = detectar_ejecutable_chrome(Configuracion())
    if detectado is not None:
        return detectado
    return CHROMIUM_SANDBOX if CHROMIUM_SANDBOX.exists() else None


# --- Medicion de la relacion de aspecto del logo (requisito 3) ---------------------


def test_dimensiones_png_lee_ihdr_del_logo_real() -> None:
    """El logotipo real mide 1993x805 (ratio 2.4758), no el 668/376 de la guia
    de marca (`references/marca-480.md`): la relacion se mide siempre del
    archivo, nunca se codifica una constante."""
    assert dimensiones_png(LOGO_REAL) == (1993, 805)


def test_dimensiones_png_ausente_devuelve_none(tmp_path: Path) -> None:
    assert dimensiones_png(tmp_path / "no-existe.png") is None


def test_dimensiones_png_no_valido_devuelve_none(tmp_path: Path) -> None:
    ruta = tmp_path / "no-es-un-png.png"
    ruta.write_bytes(b"esto no es un PNG, le falta hasta la firma")
    assert dimensiones_png(ruta) is None


# --- Estructura del HTML de impresion -----------------------------------------------


def test_una_pagina_por_escena_mas_portada_en_guiones_reales(
    texto_guiones_reales: dict[str, str],
) -> None:
    """Criterio de aceptacion literal: tantas paginas como escenas mas la portada."""
    for nombre, texto in texto_guiones_reales.items():
        resultado, tiempos = _pipeline(texto)
        pagina = generar_html_impresion(resultado, tiempos, nombre_guion=nombre)
        assert pagina.count('class="pagina') == len(resultado.escenas) + 1, (
            f"{nombre}: el numero de paginas no coincide con escenas + portada"
        )


def test_es_autocontenido_en_guiones_reales(texto_guiones_reales: dict[str, str]) -> None:
    """El logotipo incrustado como `data:` no debe disparar el validador de
    recursos externos (regla dura de §0.2: ni un archivo local aparte)."""
    for nombre, texto in texto_guiones_reales.items():
        resultado, tiempos = _pipeline(texto)
        pagina = generar_html_impresion(resultado, tiempos, nombre_guion=nombre)
        assert buscar_recursos_externos(pagina) == [], (
            f"{nombre}: el HTML de impresion depende de un recurso externo"
        )


def test_incluye_el_logotipo_incrustado_cuando_el_archivo_existe() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_html_impresion(resultado, tiempos, nombre_guion="g")
    assert "data:image/png;base64," in pagina


def test_sin_logotipo_no_rompe_la_generacion(tmp_path: Path) -> None:
    configuracion = Configuracion(ruta_logo_pdf=str(tmp_path / "no-existe.png"))
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS, configuracion)
    pagina = generar_html_impresion(
        resultado, tiempos, nombre_guion="g", configuracion=configuracion
    )
    assert "data:image/png;base64," not in pagina
    assert "<img" not in pagina


def test_prosa_no_trocea_el_texto_en_lista() -> None:
    """Requisito 5: legible como prosa, limites de bloque marcados de forma
    discreta -- nunca como lista de tarjetas."""
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_html_impresion(resultado, tiempos, nombre_guion="g")
    inicio = pagina.index('<p class="prosa">')
    fin = pagina.index("</p>", inicio)
    prosa = pagina[inicio:fin]
    assert "<li>" not in prosa
    assert "<ul>" not in prosa
    assert 'class="bloque"' in prosa


def test_portada_incluye_titulo_duracion_escenas_y_palabras() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_html_impresion(resultado, tiempos, nombre_guion="mi-guion")
    inicio = pagina.index('class="pagina portada"')
    fin = pagina.index("</section>", inicio)
    portada = pagina[inicio:fin]
    assert "mi-guion" in portada
    assert "2 escenas" in portada
    assert "palabras de locución" in portada


def test_para_terceros_omite_notas_internas_pero_conserva_indicaciones_de_pantalla() -> None:
    """Requisito 6: `incluir_notas_internas=False` (`--para-terceros`) omite
    las notas internas de produccion, nunca las indicaciones de pantalla."""
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    normal = generar_html_impresion(resultado, tiempos, nombre_guion="g")
    configuracion_terceros = Configuracion(incluir_notas_internas=False)
    terceros = generar_html_impresion(
        resultado, tiempos, nombre_guion="g", configuracion=configuracion_terceros
    )
    assert "Recordatorio interno" in normal
    assert "Recordatorio interno" not in terceros
    assert "Título del vídeo en pantalla" in normal
    assert "Título del vídeo en pantalla" in terceros


def test_guardar_html_impresion_escribe_en_carpeta_salida(tmp_path: Path) -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_html_impresion(resultado, tiempos, nombre_guion="g")
    destino = guardar_html_impresion(pagina, tmp_path)
    assert destino.parent == tmp_path
    assert destino.read_text(encoding="utf-8") == pagina


# --- Deteccion de Chrome/Edge y conversion -------------------------------------------


def test_detectar_ejecutable_chrome_respeta_la_ruta_manual(tmp_path: Path) -> None:
    ejecutable_falso = tmp_path / "chrome-de-prueba"
    ejecutable_falso.write_text("#!/bin/sh\n")
    configuracion = Configuracion(pdf_chrome_ejecutable_manual=str(ejecutable_falso))
    assert detectar_ejecutable_chrome(configuracion) == ejecutable_falso


def test_detectar_ejecutable_chrome_manual_inexistente_devuelve_none(tmp_path: Path) -> None:
    configuracion = Configuracion(pdf_chrome_ejecutable_manual=str(tmp_path / "no-existe"))
    assert detectar_ejecutable_chrome(configuracion) is None


def test_convertir_html_a_pdf_ejecutable_invalido_no_lanza(tmp_path: Path) -> None:
    ruta_html = tmp_path / "impresion.html"
    ruta_html.write_text("<html><body>hola</body></html>", encoding="utf-8")
    exito, mensaje = convertir_html_a_pdf(
        ruta_html, tmp_path / "salida.pdf", tmp_path / "no-existe-chrome", Configuracion()
    )
    assert exito is False
    assert mensaje


def test_exportar_pdf_sin_chrome_deja_html_con_mensaje_accionable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import pdf as modulo_pdf

    monkeypatch.setattr(modulo_pdf, "detectar_ejecutable_chrome", lambda configuracion: None)
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    resultado_pdf = modulo_pdf.exportar_pdf(resultado, tiempos, tmp_path, nombre_guion="g")

    assert isinstance(resultado_pdf, ResultadoPdf)
    assert resultado_pdf.ruta_html.exists()
    assert resultado_pdf.ruta_pdf is None
    assert "Ctrl+P" in resultado_pdf.mensaje


@pytest.mark.skipif(_chrome_disponible() is None, reason="no hay Chrome/Edge disponible")
def test_exportar_pdf_con_chrome_genera_pdf_con_paginas_correctas(tmp_path: Path) -> None:
    """Criterio de aceptacion: con Chrome disponible se genera el PDF y su
    numero de paginas coincide con escenas + portada."""
    ejecutable = _chrome_disponible()
    assert ejecutable is not None
    configuracion = Configuracion(pdf_chrome_ejecutable_manual=str(ejecutable))
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS, configuracion)

    resultado_pdf = exportar_pdf(
        resultado, tiempos, tmp_path, nombre_guion="g", configuracion=configuracion
    )

    assert resultado_pdf.ruta_pdf is not None
    assert resultado_pdf.ruta_pdf.exists()
    contenido = resultado_pdf.ruta_pdf.read_bytes()
    coincidencia = None
    for candidato in contenido.split(b"/Count "):
        if candidato[:1].isdigit():
            coincidencia = int(candidato.split()[0].rstrip(b">"))
            break
    assert coincidencia == len(resultado.escenas) + 1


@pytest.mark.skipif(_chrome_disponible() is None, reason="no hay Chrome/Edge disponible")
def test_exportar_pdf_para_terceros_no_deja_notas_internas_en_el_html_fuente(
    tmp_path: Path,
) -> None:
    """El PDF se genera a partir del HTML de impresion (WYSIWYG de Chrome): si
    la nota interna no esta en el HTML fuente, tampoco puede estar en el PDF."""
    ejecutable = _chrome_disponible()
    assert ejecutable is not None
    configuracion = Configuracion(
        pdf_chrome_ejecutable_manual=str(ejecutable), incluir_notas_internas=False
    )
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS, configuracion)

    resultado_pdf = exportar_pdf(
        resultado, tiempos, tmp_path, nombre_guion="g", configuracion=configuracion
    )

    assert resultado_pdf.ruta_pdf is not None
    html_fuente = resultado_pdf.ruta_html.read_text(encoding="utf-8")
    assert "Recordatorio interno" not in html_fuente
