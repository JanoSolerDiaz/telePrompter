"""Tests del exportador de subtitulos `.srt` borrador (tarea T-27).

`test_srt_generado_respeta_el_limite_de_caracteres_por_linea` reemplaza al talon
del mismo nombre en `tests/test_logica_pendiente.py` (T-03): es su criterio de
aceptacion literal, no una nota aparte.
"""

from __future__ import annotations

from itertools import pairwise
from pathlib import Path

from config import Configuracion
from deteccion import detectar_problemas_guion
from documento_revision import generar_documento_revision
from estado import estado_inicial
from normalizacion import normalizar_guion
from parser import parsear_guion
from reescrituras import fusionar_con_estado, guardar_en_estado, recopilar_propuestas
from revalidacion import revalidar_guion
from srt import (
    exportar_srt,
    formatear_marca_tiempo,
    generar_entradas_srt,
    guardar_srt,
    validar_srt,
)
from tiempos import calcular_tiempos
from troceo import trocear_guion


def _guion_dos_escenas(palabras_escena_1: int, palabras_escena_2: int) -> str:
    """Guion sintetico minimo de dos escenas, cada una con `num_palabras`
    palabras de locucion sin puntuacion intermedia, listas para trocear."""
    palabras_1 = " ".join(["palabra"] * palabras_escena_1)
    palabras_2 = " ".join(["palabra"] * palabras_escena_2)
    return f"""# Titulo

## BLOQUE 1 — Primera (0:00 – 0:10)

**LOCUCIÓN**

> {palabras_1}

## BLOQUE 2 — Segunda (0:10 – 0:20)

**LOCUCIÓN**

> {palabras_2}
"""


# --- Formato de la marca de tiempo --------------------------------------------------


def test_formatear_marca_tiempo_compone_horas_minutos_segundos_milisegundos() -> None:
    assert formatear_marca_tiempo(0.0) == "00:00:00,000"
    assert formatear_marca_tiempo(3725.678) == "01:02:05,678"


def test_formatear_marca_tiempo_redondea_al_milisegundo_mas_cercano() -> None:
    assert formatear_marca_tiempo(1.2344) == "00:00:01,234"
    assert formatear_marca_tiempo(1.2346) == "00:00:01,235"


# --- Requisito 5: consumible por ffmpeg (validador estricto) ------------------------


def test_srt_de_guiones_reales_pasa_el_validador_estricto_sin_solapes(
    texto_guiones_reales: dict[str, str],
) -> None:
    """Criterio de aceptacion de T-27: el `.srt` de la fixture pasa el
    validador estricto, no tiene solapes y sus tiempos suman la duracion
    estimada del video."""
    configuracion = Configuracion()
    for nombre, texto in texto_guiones_reales.items():
        resultado = parsear_guion(texto)
        tiempos = calcular_tiempos(resultado, configuracion)
        contenido = exportar_srt(tiempos, configuracion)

        problemas = validar_srt(contenido, configuracion)
        assert not problemas, f"{nombre}: {problemas}"

        entradas = generar_entradas_srt(tiempos, configuracion)
        assert entradas, f"{nombre}: no se genero ningun subtitulo"
        assert entradas[-1].fin_segundos == tiempos.duracion_total_segundos


def test_validar_srt_detecta_indice_no_secuencial() -> None:
    contenido = (
        "1\n00:00:00,000 --> 00:00:01,000\nHola\n\n3\n00:00:01,000 --> 00:00:02,000\nAdiós\n"
    )
    problemas = validar_srt(contenido)
    assert any("secuencial" in problema for problema in problemas)


def test_validar_srt_detecta_marca_de_tiempo_mal_formada() -> None:
    contenido = "1\n00:00:00.000 -> 00:00:01,000\nHola\n"
    problemas = validar_srt(contenido)
    assert any("mal formada" in problema for problema in problemas)


def test_validar_srt_detecta_solape_entre_subtitulos_consecutivos() -> None:
    contenido = (
        "1\n00:00:00,000 --> 00:00:02,000\nHola\n\n"
        "2\n00:00:01,000 --> 00:00:03,000\nAdiós\n"
    )
    problemas = validar_srt(contenido)
    assert any("empieza antes" in problema for problema in problemas)


def test_validar_srt_detecta_fin_anterior_o_igual_al_inicio() -> None:
    contenido = "1\n00:00:02,000 --> 00:00:01,000\nHola\n"
    problemas = validar_srt(contenido)
    assert any("no es posterior" in problema for problema in problemas)


def test_srt_generado_respeta_el_limite_de_caracteres_por_linea(
    texto_guiones_reales: dict[str, str],
) -> None:
    """Ninguna linea del `.srt` supera `Configuracion.srt_caracteres_por_linea_max`
    (criterio de aceptacion literal del talon de T-03/T-27)."""
    configuracion = Configuracion()
    for texto in texto_guiones_reales.values():
        resultado = parsear_guion(texto)
        tiempos = calcular_tiempos(resultado, configuracion)
        for entrada in generar_entradas_srt(tiempos, configuracion):
            for linea in entrada.lineas:
                assert len(linea) <= configuracion.srt_caracteres_por_linea_max


# --- Requisito 1: un subtitulo por bloque, agrupable si es muy corto ----------------


def test_bloque_normal_produce_un_subtitulo_propio_por_bloque() -> None:
    configuracion = Configuracion()
    resultado = parsear_guion(_guion_dos_escenas(9, 9))
    tiempos = calcular_tiempos(resultado, configuracion)
    bloques = trocear_guion(resultado, configuracion)

    entradas = generar_entradas_srt(tiempos, configuracion)
    assert len(entradas) == len(bloques)


def test_bloques_muy_cortos_se_agrupan_sin_cruzar_fin_de_escena() -> None:
    """A ritmo muy rapido (30 palabras/segundo, sin pausas), una escena entera
    de 24 palabras dura 0.8s -- por debajo del minimo configurado -- sea cual
    sea el numero de bloques de respiracion en que T-11 la haya troceado: debe
    fundirse en un unico subtitulo. El ultimo bloque de cada escena cierra su
    propio grupo siempre, aunque sea corto, porque nunca cruza un fin de
    escena (requisito 1): dos escenas nunca comparten subtitulo."""
    configuracion = Configuracion(
        ppm_manual=1800,  # 30 palabras/segundo
        pausa_coma_segundos=0.0,
        pausa_punto_segundos=0.0,
        pausa_fin_parrafo_segundos=0.0,
        pausa_fin_escena_segundos=0.0,
        srt_duracion_minima_segundos=1.2,
        # Ancho generoso para aislar la agrupacion (requisito 1) de la particion
        # limpia (requisito 3, cubierta aparte): toda una escena fundida debe
        # caber en una unica linea sin disparar una paginacion adicional.
        srt_caracteres_por_linea_max=250,
    )
    resultado = parsear_guion(_guion_dos_escenas(24, 24))
    tiempos = calcular_tiempos(resultado, configuracion)
    bloques = trocear_guion(resultado, configuracion)
    assert len(bloques) > 2  # T-11 trocea cada escena en varios bloques de respiracion

    entradas = generar_entradas_srt(tiempos, configuracion)
    # Cada escena funde sus bloques en un unico subtitulo (menos de 1.2s en total
    # a este ritmo): dos subtitulos en total, uno por escena, nunca uno que
    # mezcle texto de las dos escenas.
    assert len(entradas) == 2
    palabras_escena_1 = sum(len(linea.split()) for linea in entradas[0].lineas)
    palabras_escena_2 = sum(len(linea.split()) for linea in entradas[1].lineas)
    assert palabras_escena_1 == 24
    assert palabras_escena_2 == 24


# --- Requisito 3: particion limpia cuando el texto no cabe --------------------------


def test_bloque_que_no_cabe_se_reparte_en_varias_entradas_sin_perder_palabras() -> None:
    """Con un limite de lineas/caracteres muy ajustado, un bloque normal de
    T-11 (6-12 palabras) no cabe en un unico subtitulo: se reparte en varias
    entradas consecutivas -- "particion limpia" -- sin truncar ni descartar
    ninguna palabra (invariante (a), §0.2) y sin solapar sus tiempos."""
    configuracion = Configuracion(srt_lineas_max_por_subtitulo=1, srt_caracteres_por_linea_max=10)
    resultado = parsear_guion(_guion_dos_escenas(12, 6))
    tiempos = calcular_tiempos(resultado, configuracion)
    bloques = trocear_guion(resultado, configuracion)

    entradas = generar_entradas_srt(tiempos, configuracion)
    assert len(entradas) > len(bloques)  # al menos un bloque se partio en varias entradas

    palabras_reconstruidas = " ".join(
        linea for entrada in entradas for linea in entrada.lineas
    ).split()
    palabras_originales = " ".join(bloque.texto for bloque in bloques).split()
    assert palabras_reconstruidas == palabras_originales

    for anterior, siguiente in pairwise(entradas):
        assert anterior.fin_segundos <= siguiente.inicio_segundos
    assert entradas[0].indice == 1
    assert [entrada.indice for entrada in entradas] == list(range(1, len(entradas) + 1))


# --- Requisito 4: texto locutado final (reescrituras aceptadas), no el original -----


def test_srt_usa_el_texto_locutado_final_con_reescrituras_aceptadas(tmp_path: Path) -> None:
    """El `.srt` se exporta sobre `ResultadoTiempos` de una revalidacion con
    una reescritura de forma dicha ya aceptada: debe llevar la propuesta
    ('dos mil veintiséis'), nunca la cifra original ('2026')."""
    texto_guion = """# Guion de prueba

## BLOQUE 1 — Escena unica (0:00 – 0:10)

**LOCUCIÓN**

> Hemos ahorrado 2026 euros con el nuevo proceso.
"""
    ruta_guion = tmp_path / "guion.md"
    ruta_guion.write_text(texto_guion, encoding="utf-8")
    configuracion = Configuracion()
    estado = estado_inicial(ruta_guion, configuracion)
    resultado = parsear_guion(texto_guion, configuracion=configuracion)

    bloques = trocear_guion(resultado, configuracion)
    tiempos = calcular_tiempos(resultado, configuracion)
    detecciones = detectar_problemas_guion(bloques, configuracion)
    normalizaciones = normalizar_guion(bloques, configuracion)
    propuestas = recopilar_propuestas(normalizaciones, detecciones)
    reescrituras = fusionar_con_estado(estado, propuestas)
    guardar_en_estado(estado, reescrituras)
    documento = generar_documento_revision(
        resultado, tiempos, detecciones, reescrituras, configuracion, nombre_guion="prueba"
    )
    assert "2026" in documento  # la propuesta pendiente esta en el documento

    documento_aceptado = documento.replace(
        "> **Decisión:** PENDIENTE", "> **Decisión:** ACEPTAR"
    )
    revalidacion = revalidar_guion(resultado, documento_aceptado, estado, configuracion)

    contenido_srt = exportar_srt(revalidacion.resultado_tiempos, configuracion)
    assert "dos mil veintiséis" in contenido_srt
    assert "2026" not in contenido_srt


# --- Escritura a disco ---------------------------------------------------------------


def test_guardar_srt_escribe_utf8_sin_bom_por_defecto(tmp_path: Path) -> None:
    destino = guardar_srt("1\n00:00:00,000 --> 00:00:01,000\nHola\n", tmp_path)
    assert destino.exists()
    contenido_bytes = destino.read_bytes()
    assert not contenido_bytes.startswith(b"\xef\xbb\xbf")
    assert destino.read_text(encoding="utf-8").startswith("1\n")


def test_guardar_srt_con_bom_antepone_marca_de_orden_de_bytes(tmp_path: Path) -> None:
    configuracion = Configuracion(srt_con_bom=True)
    destino = guardar_srt(
        "1\n00:00:00,000 --> 00:00:01,000\nHola\n", tmp_path, configuracion
    )
    assert destino.read_bytes().startswith(b"\xef\xbb\xbf")
