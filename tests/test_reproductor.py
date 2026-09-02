"""Tests del esqueleto del reproductor autocontenido (tarea T-18).

`test_reproductor_cubre_todas_las_escenas_y_bloques_en_guiones_reales` y
`test_reproductor_es_autocontenido_en_guiones_reales` son el criterio de
aceptacion literal de T-18 sobre los tres guiones reales (mismo tratamiento
que T-08 a T-16): cobertura total y auto-contencion, sin perder nada ni
depender de nada externo.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest

from config import Configuracion
from parser import ResultadoParseo, parsear_guion
from reproductor import generar_reproductor_html, guardar_reproductor
from tiempos import ResultadoTiempos, calcular_tiempos
from verificar_salidas import buscar_recursos_externos

_GUION_DOS_ESCENAS = """# Guion de prueba

## BLOQUE 0 — Arranque (0:00 – 0:10)

**LOCUCIÓN**

> Esta es la primera frase del bloque. Y esta la segunda, ya con más ritmo.

**EN PANTALLA**

Título del vídeo en pantalla.

## BLOQUE 1 — Cierre (0:10 – 0:20)

**LOCUCIÓN**

> Segunda escena, con su propia frase de cierre para la locución.
"""

_PATRON_DATOS_JSON = re.compile(
    r'<script type="application/json" id="datos-reproductor">(.*?)</script>', re.DOTALL
)


def _pipeline(
    texto: str, configuracion: Configuracion | None = None
) -> tuple[ResultadoParseo, ResultadoTiempos]:
    configuracion = configuracion or Configuracion()
    resultado = parsear_guion(texto, configuracion=configuracion)
    tiempos = calcular_tiempos(resultado, configuracion)
    return resultado, tiempos


def _extraer_datos(pagina_html: str) -> dict[str, Any]:
    coincidencia = _PATRON_DATOS_JSON.search(pagina_html)
    assert coincidencia is not None, "no se encontro el bloque de datos embebido"
    resultado: dict[str, Any] = json.loads(coincidencia.group(1))
    return resultado


# --- Criterio de aceptacion sobre los tres guiones reales --------------------------


def test_reproductor_cubre_todas_las_escenas_y_bloques_en_guiones_reales(
    texto_guiones_reales: dict[str, str],
) -> None:
    for nombre, texto in texto_guiones_reales.items():
        resultado, tiempos = _pipeline(texto)
        pagina = generar_reproductor_html(resultado, tiempos, nombre_guion=nombre)
        datos = _extraer_datos(pagina)

        assert len(datos["escenas"]) == len(resultado.escenas), (
            f"{nombre}: faltan escenas en los datos embebidos"
        )
        total_bloques_datos = sum(len(escena["bloques"]) for escena in datos["escenas"])
        assert total_bloques_datos == len(tiempos.bloques), (
            f"{nombre}: el reproductor no cubre el 100% de los bloques de respiracion "
            f"({total_bloques_datos} de {len(tiempos.bloques)})"
        )
        for escena, tiempo_escena in zip(datos["escenas"], tiempos.escenas, strict=True):
            assert escena["numero"] == tiempo_escena.numero
            assert escena["duracion_estimada_segundos"] == tiempo_escena.duracion_estimada_segundos


def test_reproductor_es_autocontenido_en_guiones_reales(
    texto_guiones_reales: dict[str, str],
) -> None:
    for nombre, texto in texto_guiones_reales.items():
        resultado, tiempos = _pipeline(texto)
        pagina = generar_reproductor_html(resultado, tiempos, nombre_guion=nombre)
        assert buscar_recursos_externos(pagina) == [], (
            f"{nombre}: el reproductor generado depende de un recurso externo"
        )


def test_reproductor_es_html_valido_de_una_pieza() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="prueba")
    assert pagina.startswith("<!doctype html>")
    assert pagina.count("<html") == 1
    assert "<style>" in pagina
    assert "<script>" in pagina


# --- Escapado seguro (requisito 3) --------------------------------------------------


def test_texto_con_marcado_html_no_rompe_la_pagina() -> None:
    guion_hostil = """# Guion hostil

## BLOQUE 0 — Prueba (0:00 – 0:10)

**LOCUCIÓN**

> Esto incluye </script> y <b>etiquetas</b> & "comillas" que no deben romper nada.
"""
    resultado, tiempos = _pipeline(guion_hostil)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="hostil")

    assert "</script> y <b>etiquetas</b> & \"comillas\"" not in pagina
    assert pagina.count("<script") == 2  # el de datos y el del comportamiento, ninguno mas

    datos = _extraer_datos(pagina)
    texto_recuperado = datos["escenas"][0]["bloques"][0]["texto"]
    assert "</script>" in texto_recuperado
    assert "<b>etiquetas</b>" in texto_recuperado
    assert '"comillas"' in texto_recuperado


def test_titulo_con_caracteres_especiales_se_escapa() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion='Guion <raro> & "cosas"')
    assert "<title>Guion &lt;raro&gt; &amp; &quot;cosas&quot;</title>" in pagina
    assert "<raro>" not in pagina


def test_acentos_se_conservan_legibles_en_el_json() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    datos = _extraer_datos(pagina)
    assert "locución" in datos["escenas"][1]["bloques"][0]["texto"]
    assert "\\u00f3" not in pagina  # UTF-8 tal cual, sin escapar de mas


# --- Configuracion (colores, tipografia, tamano) ------------------------------------


def test_configuracion_de_estilo_se_aplica() -> None:
    configuracion = Configuracion(
        color_fondo_reproductor="#123456",
        color_texto_reproductor="#abcdef",
        tamano_texto_base_px=64,
    )
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(
        resultado, tiempos, nombre_guion="guion", configuracion=configuracion
    )
    assert "#123456" in pagina
    assert "#abcdef" in pagina
    assert "64px" in pagina


def test_ninguna_plantilla_deja_un_marcador_sin_sustituir() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert "__" not in pagina


# --- Guardado en la carpeta de salida (aislamiento, §0.2) ---------------------------


def test_guardar_reproductor_escribe_en_la_carpeta_de_salida(tmp_path: Path) -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    carpeta_salida = tmp_path / "guion-tarjetas"

    destino = guardar_reproductor(pagina, carpeta_salida)

    assert destino == carpeta_salida / "reproductor.html"
    assert destino.read_text(encoding="utf-8") == pagina


# --- Indice de escenas y pantalla completa (T-19) -----------------------------------


def test_indice_incluye_fila_navegable_por_escena_con_titulo_duracion_y_estado() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")

    assert '"escena-fila-"' in pagina  # id de cada fila, construido como "escena-fila-" + indice
    assert "Reproducir escena " in pagina  # prefijo del aria-label de cada fila
    assert "escena-numero" in pagina and "escena-titulo" in pagina and "escena-duracion" in pagina
    # Estado inicial de toda escena: pendiente (T-19, requisito 1); "grabada" y
    # "revisada" son estados alcanzables desde el navegador, no desde el HTML
    # generado, asi que solo se comprueba que las tres etiquetas existen para
    # cuando el JS las necesite en tiempo de ejecucion.
    assert "pendiente: \"Pendiente\"" in pagina
    assert "grabada: \"Grabada\"" in pagina
    assert "revisada: \"Revisada\"" in pagina


def test_reproductor_incluye_contador_de_escena_y_boton_volver_al_indice() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert '"contador-escena"' in pagina
    assert '"btn-volver-indice"' in pagina
    assert "Volver al índice" in pagina


def test_reproductor_solicita_pantalla_completa_al_reproducir_una_escena() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert "requestFullscreen" in pagina
    assert "exitFullscreen" in pagina


def test_indice_admite_navegacion_por_flechas_entre_filas() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert "ArrowDown" in pagina
    assert "ArrowUp" in pagina


def test_estilo_define_foco_visible_para_elementos_navegables() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert ":focus-visible" in pagina


# --- Motor de avance hibrido (T-20) --------------------------------------------------


def test_datos_incrustados_incluyen_paso_y_limites_de_velocidad() -> None:
    configuracion = Configuracion(paso_velocidad=0.2, velocidad_minima=0.6, velocidad_maxima=1.8)
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS, configuracion)
    pagina = generar_reproductor_html(
        resultado, tiempos, nombre_guion="guion", configuracion=configuracion
    )
    datos = _extraer_datos(pagina)
    assert datos["paso_velocidad"] == pytest.approx(0.2)
    assert datos["velocidad_minima"] == pytest.approx(0.6)
    assert datos["velocidad_maxima"] == pytest.approx(1.8)


def test_bloques_llevan_tiempos_para_que_el_motor_calcule_su_duracion() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    datos = _extraer_datos(pagina)
    for escena in datos["escenas"]:
        for bloque in escena["bloques"]:
            assert bloque["fin_segundos"] >= bloque["inicio_segundos"]


def test_reproductor_incluye_indicadores_de_velocidad_y_pausa() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert '"velocidad-escena"' in pagina
    assert '"estado-pausa"' in pagina


def test_motor_expone_pausa_avance_manual_y_ajuste_de_velocidad() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    # Requisito 2: velocidad ajustable en vivo, aplicada desde el bloque siguiente.
    assert "function ajustarVelocidad" in pagina
    # Requisito 3: avance manual que reinicia el reloj del bloque sin reiniciar la escena.
    assert "function bloqueSiguienteManual" in pagina
    assert "function bloqueAnteriorManual" in pagina
    assert "function iniciarTemporizadorBloque" in pagina
    # Requisito 4: pausa/reanudar, reiniciar escena, escena anterior/siguiente.
    assert "function togglePausa" in pagina
    assert "function reiniciarEscenaActual" in pagina
    assert "function escenaAdyacente" in pagina


def test_motor_escucha_teclas_de_control_en_el_reproductor() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert '"keydown", manejarTeclaReproductor' in pagina
    for tecla in ('"ArrowRight"', '"ArrowLeft"', '"PageDown"', '"PageUp"', '"+"', '"-"'):
        assert tecla in pagina


def test_estilo_define_bloque_activo_para_el_resaltado_del_motor() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert ".bloque--activo" in pagina


def test_escena_sin_locucion_no_rompe_la_generacion() -> None:
    guion_sin_locucion = """# Guion

## BLOQUE 0 — Solo pantalla (0:00 – 0:05)

**EN PANTALLA**

Nada que decir en esta escena.
"""
    resultado, tiempos = _pipeline(guion_sin_locucion)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    datos = _extraer_datos(pagina)

    assert len(datos["escenas"]) == 1
    escena = datos["escenas"][0]
    assert escena["numero"] == 0
    assert escena["bloques"] == []
    assert escena["duracion_estimada_segundos"] == 0.0
    assert escena["duracion_objetivo_segundos"] == pytest.approx(5.0)
