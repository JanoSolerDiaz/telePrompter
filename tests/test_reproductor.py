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
from reproductor import contraste_relativo, generar_reproductor_html, guardar_reproductor
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


# --- Resaltado, tipografia y tema de grabacion (T-21) -------------------------------


def test_contraste_del_bloque_activo_cumple_aaa() -> None:
    configuracion = Configuracion()
    ratio = contraste_relativo(
        configuracion.color_texto_reproductor, configuracion.color_fondo_reproductor
    )
    assert ratio >= 7.0, f"contraste {ratio:.2f}:1 por debajo del minimo AAA (7:1)"


def test_contraste_relativo_es_simetrico_y_maximo_para_blanco_sobre_negro() -> None:
    assert contraste_relativo("#ffffff", "#000000") == pytest.approx(21.0, abs=0.01)
    assert contraste_relativo("#ffffff", "#000000") == contraste_relativo("#000000", "#ffffff")
    assert contraste_relativo("#abcdef", "#abcdef") == pytest.approx(1.0)


def test_datos_incrustados_incluyen_gradiente_de_atenuacion_y_limites_de_tamano() -> None:
    configuracion = Configuracion(
        atenuacion_niveles=(0.8, 0.4),
        atenuacion_minima=0.15,
        tamano_texto_base_px=50,
        paso_tamano_texto_px=5,
        tamano_texto_minimo_px=20,
        tamano_texto_maximo_px=90,
        tiempo_inactividad_cursor_ms=2500,
    )
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS, configuracion)
    pagina = generar_reproductor_html(
        resultado, tiempos, nombre_guion="guion", configuracion=configuracion
    )
    datos = _extraer_datos(pagina)
    assert datos["atenuacion_niveles"] == [pytest.approx(0.8), pytest.approx(0.4)]
    assert datos["atenuacion_minima"] == pytest.approx(0.15)
    assert datos["tamano_texto_base_px"] == 50
    assert datos["paso_tamano_texto_px"] == 5
    assert datos["tamano_texto_minimo_px"] == 20
    assert datos["tamano_texto_maximo_px"] == 90
    assert datos["tiempo_inactividad_cursor_ms"] == 2500


def test_estilo_usa_color_de_acento_y_margen_seguro_configurables() -> None:
    configuracion = Configuracion(color_acento_reproductor="#ff00ff", margen_seguro_px=80)
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(
        resultado, tiempos, nombre_guion="guion", configuracion=configuracion
    )
    assert "#ff00ff" in pagina
    assert "80px" in pagina


def test_guion_js_calcula_atenuacion_de_contexto_por_distancia() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert "function opacidadPorDistancia" in pagina
    assert "atenuacion_niveles" in pagina
    assert "atenuacion_minima" in pagina


def test_guion_js_permite_ajustar_tamano_de_texto_en_vivo() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert "function ajustarTamanoTexto" in pagina
    assert '"]"' in pagina
    assert '"["' in pagina
    assert "--tamano-base" in pagina


def test_guion_js_oculta_el_cursor_tras_inactividad_en_pantalla_completa() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert "cursor-oculto" in pagina
    assert "fullscreenchange" in pagina


# --- Autoscroll con bloque centrado (T-22) ------------------------------------------


def test_datos_incrustados_incluyen_duracion_de_autoscroll() -> None:
    configuracion = Configuracion(duracion_autoscroll_ms=750)
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS, configuracion)
    pagina = generar_reproductor_html(
        resultado, tiempos, nombre_guion="guion", configuracion=configuracion
    )
    datos = _extraer_datos(pagina)
    assert datos["duracion_autoscroll_ms"] == 750


def test_guion_js_centra_el_bloque_activo_con_scroll_cancelable() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert "function centrarBloqueActivo" in pagina
    assert "cancelAnimationFrame" in pagina
    assert "requestAnimationFrame" in pagina
    assert "duracion_autoscroll_ms" in pagina


def test_guion_js_recentra_al_redimensionar_la_ventana() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert '"resize"' in pagina


# --- Ayudas de grabacion (T-23) -----------------------------------------------------


def test_datos_incrustados_incluyen_cuenta_atras() -> None:
    configuracion = Configuracion(cuenta_atras_segundos=5, cuenta_atras_activada=False)
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS, configuracion)
    pagina = generar_reproductor_html(
        resultado, tiempos, nombre_guion="guion", configuracion=configuracion
    )
    datos = _extraer_datos(pagina)
    assert datos["cuenta_atras_segundos"] == 5
    assert datos["cuenta_atras_activada"] is False


def test_reproductor_incluye_cronometro_y_barra_de_progreso() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert '"cronometro-toma"' in pagina
    assert "barra-progreso-contenedor" in pagina
    assert "barra-progreso-relleno" in pagina
    assert "cuenta-atras" in pagina


def test_guion_js_expone_cuenta_atras_cronometro_y_barra_de_progreso() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    # Requisito 1: cuenta atras 3-2-1 antes de arrancar, desactivable.
    assert "function iniciarCuentaAtras" in pagina
    assert "cuenta_atras_activada" in pagina
    # Requisito 2: cronometro de la toma frente a la duracion estimada.
    assert "function actualizarCronometro" in pagina
    assert "function iniciarCronometro" in pagina
    # Requisito 3: barra de progreso de la escena por bloques.
    assert "function actualizarBarraProgreso" in pagina


def test_motor_permite_ocultar_los_indicadores_con_una_tecla() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert "function alternarIndicadores" in pagina
    assert "indicadores-ocultos" in pagina
    for tecla in ('"h"', '"H"'):
        assert tecla in pagina


def test_estilo_oculta_cabecera_y_barra_de_progreso_cuando_se_alternan_indicadores() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert "#vista-reproductor.indicadores-ocultos .reproductor-cabecera" in pagina
    assert "#vista-reproductor.indicadores-ocultos .barra-progreso-contenedor" in pagina


def test_pausa_congela_el_cronometro_de_la_toma() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    # requisito 2: el cronometro es tiempo de reloj real, se congela en pausa
    # igual que el reloj del bloque (T-20), no sigue corriendo de fondo.
    assert "cronometroMsAcumulados += Date.now() - cronometroInicioMarca" in pagina


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
