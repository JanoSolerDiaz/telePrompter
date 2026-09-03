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


def test_estilo_usa_colores_de_estado_del_indice_configurables() -> None:
    configuracion = Configuracion(
        color_estado_grabada_reproductor="#00ff00",
        color_estado_revisada_reproductor="#0000ff",
    )
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(
        resultado, tiempos, nombre_guion="guion", configuracion=configuracion
    )
    assert "#00ff00" in pagina
    assert "#0000ff" in pagina
    assert "__COLOR_ESTADO_GRABADA__" not in pagina
    assert "__COLOR_ESTADO_REVISADA__" not in pagina


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


# --- Atajos de teclado y clicker Bluetooth (T-24) -----------------------------------


def test_datos_incrustados_incluyen_antirrebote_espacio_y_mapa_de_teclas() -> None:
    configuracion = Configuracion(antirrebote_clicker_ms=200, espacio_avanza_bloque=True)
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS, configuracion)
    pagina = generar_reproductor_html(
        resultado, tiempos, nombre_guion="guion", configuracion=configuracion
    )
    datos = _extraer_datos(pagina)
    assert datos["antirrebote_clicker_ms"] == 200
    assert datos["espacio_avanza_bloque"] is True
    # El mapa viaja como objeto JSON (accion -> lista de teclas), no como el
    # array de pares que usa `Configuracion.mapa_teclas_reproductor` en Python.
    assert datos["mapa_teclas"]["bloque_siguiente"] == ["ArrowRight", "PageDown"]
    assert datos["mapa_teclas"]["bloque_anterior"] == ["ArrowLeft", "PageUp"]
    assert datos["mapa_teclas"]["pausa_avanza"] == [" ", "Spacebar"]
    assert datos["mapa_teclas"]["salir_pantalla_completa"] == ["Escape"]
    assert datos["mapa_teclas"]["ayuda"] == ["?"]


def test_mapa_de_teclas_es_configurable_en_la_generacion() -> None:
    configuracion = Configuracion(
        mapa_teclas_reproductor=(("bloque_siguiente", ("PageDown",)),)
    )
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS, configuracion)
    pagina = generar_reproductor_html(
        resultado, tiempos, nombre_guion="guion", configuracion=configuracion
    )
    datos = _extraer_datos(pagina)
    assert datos["mapa_teclas"] == {"bloque_siguiente": ["PageDown"]}


def test_guion_js_resuelve_las_teclas_a_traves_del_mapa_configurable() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    # El switch de acciones reemplaza al switch de teclas literales de T-20/T-21:
    # ninguna tecla se compara a mano dentro de `manejarTeclaReproductor`.
    assert "var accion = teclaAAccion[evento.key]" in pagina
    assert "case \"bloque_siguiente\":" in pagina
    assert "case \"salir_pantalla_completa\":" in pagina
    assert "case \"ayuda\":" in pagina
    assert "function salirPantallaCompleta" in pagina


def test_guion_js_aplica_antirrebote_por_accion() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert "function pulsacionPermitida" in pagina
    assert "antirrebote_clicker_ms" in pagina


def test_guion_js_expone_la_ayuda_de_teclado_construida_desde_el_mapa_vigente() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert "function construirListaAyudaTeclado" in pagina
    assert "function alternarAyuda" in pagina
    assert "ayuda-teclado-lista" in pagina
    # Requisito 3: la ayuda lee `datos.mapa_teclas`, nunca una copia aparte.
    assert "datos.mapa_teclas[accion]" in pagina


def test_estilo_define_el_panel_de_ayuda_de_teclado() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert ".ayuda-teclado" in pagina
    assert ".ayuda-teclado-panel" in pagina


# --- Modo espejo (T-25) --------------------------------------------------------------


def test_datos_incrustados_incluyen_el_alcance_del_modo_espejo() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina_por_defecto = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert _extraer_datos(pagina_por_defecto)["espejo_incluye_indicadores"] is False

    configuracion = Configuracion(espejo_incluye_indicadores=True)
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS, configuracion)
    pagina = generar_reproductor_html(
        resultado, tiempos, nombre_guion="guion", configuracion=configuracion
    )
    assert _extraer_datos(pagina)["espejo_incluye_indicadores"] is True


def test_mapa_de_teclas_incluye_espejo_por_defecto() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert _extraer_datos(pagina)["mapa_teclas"]["espejo"] == ["m", "M"]


def test_guion_js_activa_el_modo_espejo_por_tecla_y_por_boton() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    # Requisito 1: activable con tecla (el mapa configurable ya cubre "m"/"M")
    # y desde los controles (un boton dedicado, no solo el atajo).
    assert 'case "espejo":' in pagina
    assert "function alternarEspejo" in pagina
    assert 'btn-espejo' in pagina
    assert "botonEspejo.addEventListener(\"click\", alternarEspejo)" in pagina


def test_guion_js_aplica_el_volteo_solo_al_texto_salvo_configuracion_contraria() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    # Requisito 1 ("sin afectar a la orientacion de los indicadores si asi se
    # configura"): dos clases distintas segun `espejo_incluye_indicadores`,
    # nunca una unica que siempre voltee todo el reproductor.
    assert "function aplicarClaseEspejo" in pagina
    assert '"espejo-texto"' in pagina
    assert '"espejo-completo"' in pagina


def test_estilo_voltea_solo_la_escena_por_defecto_y_todo_si_se_configura() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert "#vista-reproductor.espejo-texto .escena {" in pagina
    assert "#vista-reproductor.espejo-completo {" in pagina


def test_guion_js_persiste_el_ajuste_de_espejo_con_clave_derivada_del_guion() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    # Requisito 3 y criterio de aceptacion ("persiste tras recargar"): via
    # `localStorage`, con clave derivada del guion (mismo patron que exigira
    # T-26) y protegido con `try/catch` (hallazgo #5, `file://` no verificado).
    assert "function claveAlmacenamiento" in pagina
    assert 'return "teleprompter:" + datos.guion + ":" + preferencia' in pagina
    assert "window.localStorage.getItem" in pagina
    assert "window.localStorage.setItem" in pagina
    assert "leerPreferencia(\"espejo\") === \"1\"" in pagina
    assert "guardarPreferencia(\"espejo\"" in pagina


# --- Persistencia local de preferencias (T-26) ----------------------------------------


def test_guion_js_restaura_el_tamano_de_texto_guardado() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    # Requisito 1: se lee "tamano_texto" con la misma pareja
    # leerPreferencia/guardarPreferencia de T-25, acotado a los limites
    # configurados, y se aplica de inmediato a la variable CSS --tamano-base
    # (no solo al cambiarlo con [ / ]).
    assert 'leerPreferencia("tamano_texto")' in pagina
    assert 'guardarPreferencia("tamano_texto", String(nuevo))' in pagina
    assert (
        'document.documentElement.style.setProperty("--tamano-base", '
        "tamanoTextoActualPx + \"px\")"
    ) in pagina


def test_guion_js_restaura_la_velocidad_por_escena_con_clave_por_numero() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    # Requisitos 1 y 5: la clave usa el NUMERO de escena, no su indice, para
    # sobrevivir a un troceo distinto en una regeneracion posterior.
    assert 'leerPreferencia("velocidad_escena_" + escena.numero)' in pagina
    assert (
        'guardarPreferencia("velocidad_escena_" + datos.escenas[escenaActual].numero, '
        "String(nueva))"
    ) in pagina


def test_guion_js_restaura_la_visibilidad_de_indicadores() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert 'leerPreferencia("indicadores_ocultos") === "1"' in pagina
    assert '"indicadores_ocultos",' in pagina
    assert 'vistaReproductor.classList.contains("indicadores-ocultos") ? "1" : "0"' in pagina


def test_guion_js_guarda_y_reencuentra_la_ultima_escena_vista() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert "function guardarUltimaEscenaVista" in pagina
    assert 'guardarPreferencia("ultima_escena_numero", String(escena.numero))' in pagina
    assert (
        'guardarPreferencia("ultima_escena_inicio_segundos", String(bloque.inicio_segundos))'
        in pagina
    )
    # Requisito 5: se reencuentra el bloque MAS CERCANO por inicio_segundos,
    # no por indice, para sobrevivir a un troceo distinto.
    assert "function calcularReanudacion" in pagina
    assert "Math.abs(bloque.inicio_segundos - inicioGuardado)" in pagina


def test_guion_js_ofrece_un_boton_continuar_en_el_indice_sin_lanzar_solo_al_cargar() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert "btn-continuar" in pagina
    assert "var reanudacion = calcularReanudacion();" in pagina
    assert "reproducirEscena(reanudacion.indiceEscena, reanudacion.indiceBloque)" in pagina
    # El boton "Continuar" es la unica via de reanudacion: `renderizarIndice()`
    # (que construye ese boton) es la ultima llamada del script, sin ningun
    # `reproducirEscena`/`iniciarMotor` automatico justo antes del cierre --
    # `requestFullscreen` exige un gesto de usuario real y un intento
    # automatico fallaria en silencio (ver `solicitarPantallaCompleta`).
    coincidencia_cierre = re.search(r"([\s\S]*?)\n\s*\}\)\(\);\s*</script>", pagina)
    assert coincidencia_cierre is not None
    ultima_sentencia = coincidencia_cierre.group(1).rstrip().splitlines()[-1].strip()
    assert ultima_sentencia == "renderizarIndice();"


def test_guion_js_restablece_preferencias_desde_la_ayuda() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    # Requisito 4: un boton dentro del panel de ayuda, no un atajo de teclado
    # aparte, que borra toda clave de este guion y repone los valores por
    # defecto en memoria sin recargar la pagina.
    assert "btn-restablecer-preferencias" in pagina
    assert "function restablecerPreferencias" in pagina
    assert "function limpiarPreferenciasAlmacenadas" in pagina
    assert 'prefijo = "teleprompter:" + datos.guion + ":"' in pagina
    assert "window.localStorage.removeItem(clave)" in pagina


def test_guion_js_pasa_el_bloque_inicial_a_iniciarmotor() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    # Requisito 5: reproducirEscena/iniciarMotor aceptan un bloque de arranque
    # distinto de 0, para que el boton "Continuar" pueda entrar directamente
    # en el bloque mas cercano en vez de siempre en el primero.
    assert "function reproducirEscena(indice, bloqueInicial)" in pagina
    assert "function iniciarMotor(indice, bloqueInicial)" in pagina
    assert "bloqueActual = bloqueInicial || 0;" in pagina
    assert "marcarBloqueActivo(bloqueActual);" in pagina


# --- Persistencia verificada de preferencias, con plan B (R-01) --------------------
#
# `origen: auditoría #5`. Verificado ademas a mano con Playwright headless
# (Chromium, no es dependencia del proyecto) sobre `fixtures/salida/reproductor.html`,
# generado a partir de `fixtures/guion-ejemplo.md`: (1) escribir preferencias, cerrar el
# contexto y reabrir el MISMO perfil de Chromium (mismo directorio de datos de usuario,
# no una recarga de pagina) las mantiene intactas; un perfil NUEVO empieza vacio, tal
# como cabria esperar de `localStorage` particionado por perfil/origen -- resultado
# documentado en `DECISIONES_TECNICAS.md`. (2) El ciclo completo exportar -> "Continuar"
# ausente en un perfil nuevo -> importar el archivo descargado -> "Continuar" ya
# disponible con la escena/bloque correctos, funciona de punta a punta, incluida la
# exportacion cuando `localStorage` esta bloqueado del todo (se simulo lanzando en el
# propio getter). (3) El aviso `.aviso-almacenamiento` aparece cuando `localStorage`
# lanza al leer/escribir, y el reproductor sigue funcionando con normalidad.


def test_guion_js_detecta_si_localstorage_no_esta_disponible() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    # Requisito 3: comprobacion real (escribe y relee una clave de prueba), no un
    # try/catch silencioso -- distingue "no funciona aqui" del limite ya conocido de
    # si sobrevive a cerrar y reabrir el archivo (eso no se puede saber dentro de una
    # sola carga de pagina).
    assert "function comprobarAlmacenamientoDisponible" in pagina
    assert "var almacenamientoDisponible = comprobarAlmacenamientoDisponible();" in pagina
    assert "aviso-almacenamiento" in pagina


def test_guion_js_ofrece_exportar_e_importar_preferencias_en_el_indice() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    # Requisito 2: el plan B vive en el indice, el mismo punto de entrada/salida de una
    # sesion de grabacion que ya usa el boton "Continuar" (T-26).
    assert "btn-exportar-preferencias" in pagina
    assert "btn-importar-preferencias" in pagina
    assert "entrada-importar-preferencias" in pagina
    assert "function exportarPreferencias" in pagina
    assert "function manejarArchivoImportado" in pagina


def test_guion_js_exporta_preferencias_desde_variables_en_memoria() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    # Requisitos 2 y 3: nunca depende solo de `localStorage` -- si nunca llego a
    # funcionar esta sesion, `leerPreferencia` devolveria vacio y el plan B se
    # quedaria sin nada que exportar. Se lee de las mismas variables que ya reflejan
    # el ajuste vigente en memoria.
    assert "function construirExportacionPreferencias" in pagina
    assert "tamano_texto_px: tamanoTextoActualPx" in pagina
    assert "espejo: espejoActivado" in pagina
    assert "velocidad_por_escena: velocidadPorEscena" in pagina
    assert "ultima_escena: ultimaEscenaVistaEnMemoria" in pagina


def test_guion_js_valida_el_guion_de_origen_al_importar() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    # No aplica sin avisar unas preferencias exportadas de OTRO guion.
    assert "function aplicarPreferenciasImportadas" in pagina
    assert "objeto.guion !== undefined && objeto.guion !== datos.guion" in pagina


def test_guion_js_nunca_falla_en_silencio_al_exportar() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    # Requisito 3: si el navegador no permite disparar la descarga programada
    # (Blob/URL.createObjectURL), se ofrece el mismo contenido para copiar a mano en
    # vez de perder la exportacion sin decir nada.
    assert 'window.prompt("Copia este texto y guardalo en un archivo .json:", contenido)' in pagina


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


# --- Registro de tomas por escena (R-02) ----------------------------------------------


def test_mapa_de_teclas_incluye_marcar_toma_buena_y_nota_toma_por_defecto() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    datos = _extraer_datos(pagina)
    assert datos["mapa_teclas"]["marcar_toma_buena"] == ["g", "G"]
    assert datos["mapa_teclas"]["nota_toma"] == ["n", "N"]


def test_guion_js_registra_tomas_por_escena_con_duracion_real() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    # Requisito 1: numero de tomas y duracion real (del cronometro de T-23) de
    # cada una, cerradas al salir de la escena o al reiniciarla.
    assert "function finalizarTomaActual" in pagina
    assert "function cargarTomasGuardadas" in pagina
    assert "tomasEscena[indice].push({" in pagina
    assert "duracion_segundos: Math.round((transcurridoMs / 1000) * 10) / 10" in pagina
    assert "case \"marcar_toma_buena\":" in pagina
    assert "case \"nota_toma\":" in pagina


def test_guion_js_persiste_las_tomas_con_clave_derivada_del_guion_y_la_escena() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    # Sobrevive al cierre del navegador (criterio de aceptacion): mismo mecanismo
    # de `localStorage` por escena que T-26 ya uso para la velocidad.
    assert "function guardarTomasEscena" in pagina
    assert '"tomas_escena_" + datos.escenas[indice].numero' in pagina


def test_guion_js_solo_permite_una_toma_buena_por_escena() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert "toma.buena = false;" in pagina


def test_guion_js_reiniciar_escena_cierra_la_toma_en_curso_como_repeticion() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    # Requisito de rodaje: "R" no solo reinicia el bloque, cierra la toma
    # fallida y arranca el cronometro de cero para la siguiente (una toma no
    # puede heredar tiempo de la que se acaba de descartar).
    coincidencia = pagina.index("function reiniciarEscenaActual")
    fragmento = pagina[coincidencia : coincidencia + 500]
    assert "finalizarTomaActual();" in fragmento
    assert "cronometroMsAcumulados = 0;" in fragmento


def test_guion_js_estado_de_escena_se_deriva_de_las_tomas_registradas() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    # Requisito 4: pendiente sin tomas, grabada con tomas sin ninguna buena,
    # revisada en cuanto hay una toma marcada como la buena.
    assert "function calcularEstadoEscena" in pagina
    assert 'return "pendiente";' in pagina
    assert '? "revisada"\n      : "grabada";' in pagina


def test_guion_js_ofrece_exportar_el_parte_de_rodaje_en_el_indice() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    # Requisito 3: volcado a un archivo, legible por la fase de montaje y por
    # el dueno, sin depender de reabrir el reproductor.
    assert "btn-exportar-tomas" in pagina
    assert "function construirParteDeRodaje" in pagina
    assert "function exportarParteDeRodaje" in pagina
    assert '"teleprompter-tomas-" + base' in pagina


def test_guion_js_restablecer_preferencias_no_borra_el_registro_de_tomas() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    # "Restablecer preferencias" (T-26) comparte prefijo de clave de
    # localStorage con el registro de tomas (R-02, sesion aparte): no debe
    # poder borrarlo de rebote.
    assert 'var prefijoTomas = prefijo + "tomas_escena_";' in pagina
    assert "clave.indexOf(prefijoTomas) !== 0" in pagina


def test_guion_js_muestra_resumen_de_tomas_junto_a_cada_escena() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert "escena-tomas" in pagina
    assert '" · buena: " + tomaBuena.numero' in pagina


# --- Marcar tropiezos durante la toma (R-03) -------------------------------------------


def test_mapa_de_teclas_incluye_marcar_tropiezo_por_defecto() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    datos = _extraer_datos(pagina)
    assert datos["mapa_teclas"]["marcar_tropiezo"] == ["t", "T"]


def test_guion_js_alterna_el_tropiezo_del_bloque_en_pantalla_sin_dialogo() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    # Requisito 1: una tecla, sin interrumpir la toma -- a diferencia de
    # `pedirNotaToma` (R-02), nunca abre `window.prompt`.
    coincidencia = pagina.index("function alternarTropiezoBloqueActual")
    fragmento = pagina[coincidencia : coincidencia + 700]
    assert "window.prompt" not in fragmento
    assert 'case "marcar_tropiezo":' in pagina
    assert "alternarTropiezoBloqueActual();" in pagina


def test_guion_js_persiste_los_tropiezos_con_clave_derivada_del_guion_y_la_escena() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert "function cargarTropiezosGuardados" in pagina
    assert "function guardarTropiezosEscena" in pagina
    assert '"tropiezos_escena_" + datos.escenas[indice].numero' in pagina


def test_guion_js_registra_indice_de_bloque_y_texto_exacto_del_tropiezo() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    # Requisito 2: "escena, bloque y texto exacto" -- el texto se lee del
    # mismo bloque activo, no se reescribe a mano en ningun sitio.
    assert (
        "lista.push({ indice_bloque: bloqueActual, texto: bloques[bloqueActual].texto });"
        in pagina
    )


def test_guion_js_indicador_de_tropiezo_sigue_al_bloque_activo() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert "indicador-tropiezo" in pagina
    coincidencia = pagina.index("function marcarBloqueActivo")
    fragmento = pagina[coincidencia : coincidencia + 400]
    assert "actualizarIndicadorTropiezo();" in fragmento


def test_guion_js_ofrece_exportar_los_tropiezos_en_el_indice() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    # Requisito 2: volcado a un archivo, del que el lado Python (R-03,
    # `scripts/feedback.py`) alimenta `FEEDBACK.md`.
    assert "btn-exportar-tropiezos" in pagina
    assert "function construirRegistroTropiezos" in pagina
    assert "function exportarRegistroTropiezos" in pagina
    assert '"teleprompter-tropiezos-" + base' in pagina


def test_guion_js_restablecer_preferencias_no_borra_los_tropiezos_marcados() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert 'var prefijoTropiezos = prefijo + "tropiezos_escena_";' in pagina
    assert "clave.indexOf(prefijoTropiezos) !== 0" in pagina


def test_guion_js_muestra_resumen_de_tropiezos_junto_a_cada_escena() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    assert "escena-tropiezos" in pagina
