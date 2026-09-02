"""Tests de humo del esqueleto (T-00).

La suite de verdad es T-03. Aqui solo se comprueba que el andamiaje se sostiene: que la
configuracion es coherente, que la capa de presentacion funciona y que el validador de
auto-contencion —la regla dura de §0.2— detecta lo que tiene que detectar. Ese ultimo
test es el que evita que la regla se degrade sin que nadie se entere.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from config import Configuracion
from verificar_salidas import buscar_recursos_externos, verificar_autocontencion


def test_configuracion_por_defecto_es_coherente() -> None:
    configuracion = Configuracion()
    assert configuracion.palabras_por_bloque_min <= configuracion.palabras_por_bloque_max
    assert configuracion.ppm_respaldo > 0


def test_configuracion_rechaza_rango_de_bloque_imposible() -> None:
    with pytest.raises(ValueError, match="minimo de palabras"):
        Configuracion(palabras_por_bloque_min=15, palabras_por_bloque_max=6)


def test_configuracion_rechaza_paso_de_velocidad_no_positivo() -> None:
    with pytest.raises(ValueError, match="paso de velocidad"):
        Configuracion(paso_velocidad=0)


def test_configuracion_rechaza_limites_de_velocidad_decrecientes() -> None:
    with pytest.raises(ValueError, match="Los limites de velocidad"):
        Configuracion(velocidad_minima=2.0, velocidad_maxima=0.5)


def test_configuracion_rechaza_rango_de_velocidad_que_no_incluye_el_ritmo_base() -> None:
    with pytest.raises(ValueError, match="incluir 1\\.0"):
        Configuracion(velocidad_minima=1.2, velocidad_maxima=1.5)


def test_configuracion_rechaza_tamano_de_texto_base_fuera_de_sus_limites() -> None:
    with pytest.raises(ValueError, match="tamano de texto base"):
        Configuracion(tamano_texto_base_px=10, tamano_texto_minimo_px=24, tamano_texto_maximo_px=96)


def test_configuracion_rechaza_atenuacion_sin_niveles() -> None:
    with pytest.raises(ValueError, match="al menos un nivel"):
        Configuracion(atenuacion_niveles=())


def test_configuracion_rechaza_niveles_de_atenuacion_no_decrecientes() -> None:
    with pytest.raises(ValueError, match="estrictamente decrecientes"):
        Configuracion(atenuacion_niveles=(0.5, 0.5))


def test_configuracion_rechaza_atenuacion_minima_por_encima_del_ultimo_nivel() -> None:
    with pytest.raises(ValueError, match="atenuacion minima"):
        Configuracion(atenuacion_niveles=(0.75, 0.5), atenuacion_minima=0.6)


def test_configuracion_rechaza_margen_seguro_negativo() -> None:
    with pytest.raises(ValueError, match="margen seguro"):
        Configuracion(margen_seguro_px=-1)


def test_html_autocontenido_no_dispara_hallazgos() -> None:
    html = """<!doctype html><html><head><style>body{color:#fff}</style></head>
    <body><script>const escenas=[];</script></body></html>"""
    assert buscar_recursos_externos(html) == []


@pytest.mark.parametrize(
    "html",
    [
        '<script src="https://cdn.jsdelivr.net/x.js"></script>',
        '<link rel="stylesheet" href="estilos.css">',
        "<style>@import url(otro.css);</style>",
        "<script>fetch('/datos')</script>",
        "<script>new XMLHttpRequest()</script>",
        '<img src="logo.png">',
    ],
)
def test_html_con_recurso_externo_se_detecta(html: str) -> None:
    assert buscar_recursos_externos(html), f"no se detecto el recurso externo en: {html}"


def test_imagen_incrustada_en_data_uri_esta_permitida() -> None:
    assert buscar_recursos_externos('<img src="data:image/png;base64,iVBORw0KGgo=">') == []


def test_verificacion_sin_reproductor_es_no_aplicable(tmp_path: Path) -> None:
    resultado = verificar_autocontencion(tmp_path / "no-existe.html")
    assert resultado.estado == "NO APLICABLE"
    assert not resultado.es_fallo
