"""Tests de los capitulos de YouTube con marcas de tiempo reales (tarea R-07).

Mismo patron que `tests/test_srt_alineado.py` (R-05): guiones sinteticos
minimos con control total sobre el numero de palabras y la duracion objetivo,
mas un mapa `{numero_escena: duracion_real_segundos}` de tomas buenas, y los
tres guiones reales de calibracion para el criterio de aceptacion literal.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from capitulos_youtube import (
    calcular_capitulos,
    formatear_capitulos_ffmpeg,
    formatear_capitulos_youtube,
    generar_capitulos_youtube,
    guardar_capitulos_ffmpeg,
    guardar_capitulos_youtube,
    validar_capitulos_ffmpeg,
    validar_capitulos_youtube,
)
from config import (
    NOMBRE_ARCHIVO_CAPITULOS_FFMPEG,
    NOMBRE_ARCHIVO_CAPITULOS_YOUTUBE,
    Configuracion,
)
from parser import ResultadoParseo, parsear_guion
from tiempos import ResultadoTiempos, calcular_tiempos


def _mmss(segundos: int) -> str:
    return f"{segundos // 60}:{segundos % 60:02d}"


def _guion_con_capitulos(
    titulos_capitulos: list[str],
    palabras_por_escena: list[int],
    duracion_por_escena_segundos: int = 15,
) -> str:
    """Guion sintetico con una seccion `Capítulos` (una fila por titulo) y una
    escena por entrada de `palabras_por_escena`, en el mismo orden."""
    filas = "\n".join(f"| 0:00 | {titulo} |" for titulo in titulos_capitulos)
    partes = [
        "# Titulo\n",
        "\n## Capítulos (para la descripción del vídeo)\n\n"
        f"| Marca | Capítulo |\n|---|---|\n{filas}\n",
    ]
    inicio = 0
    for indice, num_palabras in enumerate(palabras_por_escena):
        fin = inicio + duracion_por_escena_segundos
        palabras = " ".join(["palabra"] * num_palabras)
        partes.append(
            f"\n## BLOQUE {indice} - Escena {indice} ({_mmss(inicio)} - {_mmss(fin)})\n\n"
            f"**LOCUCIÓN**\n\n> {palabras}. Otra frase, con coma, aqui.\n"
        )
        inicio = fin
    return "".join(partes)


def _guion_sin_capitulos(palabras_por_escena: list[int]) -> str:
    partes = ["# Titulo\n"]
    inicio = 0
    for indice, num_palabras in enumerate(palabras_por_escena):
        fin = inicio + 10
        palabras = " ".join(["palabra"] * num_palabras)
        partes.append(
            f"\n## BLOQUE {indice} - Escena {indice} ({_mmss(inicio)} - {_mmss(fin)})\n\n"
            f"**LOCUCIÓN**\n\n> {palabras}. Otra frase, con coma, aqui.\n"
        )
        inicio = fin
    return "".join(partes)


def _analizar(texto: str) -> tuple[ResultadoParseo, ResultadoTiempos]:
    resultado = parsear_guion(texto)
    return resultado, calcular_tiempos(resultado, Configuracion())


def _tomas_por_escena(tomas_buenas_segundos: dict[int, float]) -> dict[str, object]:
    return {
        str(numero): {
            "titulo": f"Escena {numero}",
            "tomas": [{"numero": 1, "duracion_segundos": duracion, "nota": "", "buena": True}],
        }
        for numero, duracion in tomas_buenas_segundos.items()
    }


# --- Requisito 1: emparejar titulos de capitulo con escenas, por orden -------------


def test_titulos_se_emparejan_posicionalmente_con_las_escenas() -> None:
    resultado, tiempos = _analizar(
        _guion_con_capitulos(["Primero", "Segundo", "Tercero"], [8, 8, 8])
    )
    calculo = calcular_capitulos(resultado, tiempos, {})

    assert [c.titulo for c in calculo.capitulos] == ["Primero", "Segundo", "Tercero"]
    assert [c.numero_escena for c in calculo.capitulos] == [0, 1, 2]


def test_menos_titulos_que_escenas_empareja_solo_hasta_el_mas_corto() -> None:
    resultado, tiempos = _analizar(_guion_con_capitulos(["Unico"], [8, 8, 8]))
    calculo = calcular_capitulos(resultado, tiempos, {})

    assert [c.titulo for c in calculo.capitulos] == ["Unico"]
    assert calculo.motivo_sin_generar is None
    assert calculo.titulos_sobrantes == ()


def test_mas_titulos_que_escenas_deja_constancia_de_los_sobrantes() -> None:
    """Reproduce el hallazgo #17 (R-11): con mas titulos de capitulo que
    escenas, los sobrantes no deben desaparecer sin rastro -- a diferencia del
    caso simetrico de arriba, que ya emparejaba "hasta el mas corto"."""
    resultado, tiempos = _analizar(
        _guion_con_capitulos(["Primero", "Segundo", "Tercero"], [8])
    )
    calculo = calcular_capitulos(resultado, tiempos, {})

    assert [c.titulo for c in calculo.capitulos] == ["Primero"]
    assert calculo.titulos_sobrantes == ("Segundo", "Tercero")
    assert calculo.motivo_sin_generar is None


def test_titulos_se_leen_de_los_guiones_reales_que_traen_la_seccion(
    texto_guiones_reales: dict[str, str],
) -> None:
    con_capitulos = 0
    for nombre, texto in texto_guiones_reales.items():
        resultado, tiempos = _analizar(texto)
        calculo = calcular_capitulos(resultado, tiempos, {})
        if calculo.motivo_sin_generar is not None:
            continue  # guion-artefactos-lienzo.md no trae la seccion (evidencia real)
        con_capitulos += 1
        assert len(calculo.capitulos) == len(tiempos.escenas), nombre
    assert con_capitulos == 2, "se esperaban exactamente dos guiones reales con Capítulos"


# --- Requisito 4: sin seccion Capitulos, no se genera nada en silencio -------------


def test_sin_seccion_capitulos_no_se_genera_nada() -> None:
    resultado, tiempos = _analizar(_guion_sin_capitulos([8, 8]))
    calculo = calcular_capitulos(resultado, tiempos, {})

    assert calculo.capitulos == ()
    assert calculo.motivo_sin_generar is not None
    assert formatear_capitulos_youtube(calculo) is None


def test_seccion_capitulos_sin_filas_legibles_tampoco_genera_nada() -> None:
    texto = (
        "# Titulo\n\n## Capítulos (para la descripción del vídeo)\n\nSin tabla aqui.\n"
        + _guion_sin_capitulos([8])[len("# Titulo\n") :]
    )
    resultado, tiempos = _analizar(texto)
    calculo = calcular_capitulos(resultado, tiempos, {})

    assert calculo.capitulos == ()
    assert calculo.motivo_sin_generar is not None


def test_guion_real_sin_seccion_capitulos_no_genera_nada(
    texto_guiones_reales: dict[str, str],
) -> None:
    # `guion-artefactos-lienzo.md` no trae seccion `Capítulos` (evidencia real).
    texto = texto_guiones_reales["guion-artefactos-lienzo.md"]
    resultado, tiempos = _analizar(texto)
    calculo = calcular_capitulos(resultado, tiempos, {})

    assert calculo.capitulos == ()
    assert calculo.motivo_sin_generar is not None


# --- Requisito 2: tiempo real si hay toma buena, estimado si no, nunca mezclado ----


def test_sin_tomas_usa_la_duracion_estimada_de_cada_escena() -> None:
    resultado, tiempos = _analizar(
        _guion_con_capitulos(["Uno", "Dos", "Tres"], [8, 8, 8], duracion_por_escena_segundos=15)
    )
    calculo = calcular_capitulos(resultado, tiempos, {})

    assert calculo.escenas_sin_toma_buena == (0, 1, 2)
    cursor = 0.0
    for capitulo, tiempo_escena in zip(calculo.capitulos, tiempos.escenas, strict=True):
        assert capitulo.inicio_segundos == pytest.approx(cursor, abs=1e-6)
        cursor += tiempo_escena.duracion_estimada_segundos


def test_con_toma_buena_usa_la_duracion_real_para_las_escenas_siguientes() -> None:
    resultado, tiempos = _analizar(
        _guion_con_capitulos(["Uno", "Dos", "Tres"], [8, 8, 8], duracion_por_escena_segundos=15)
    )
    duracion_estimada_0 = tiempos.escenas[0].duracion_estimada_segundos
    calculo = calcular_capitulos(resultado, tiempos, _tomas_por_escena({0: 40.0}))

    assert calculo.escenas_sin_toma_buena == (1, 2)
    assert calculo.capitulos[0].inicio_segundos == pytest.approx(0.0, abs=1e-6)
    # La escena 1 arranca donde termino la duracion REAL de la escena 0 (40s), no
    # la estimada -- confirma que el cursor usa la fuente correcta por escena.
    assert calculo.capitulos[1].inicio_segundos == pytest.approx(40.0, abs=1e-6)
    assert duracion_estimada_0 != pytest.approx(40.0, abs=1e-6)


def test_primera_marca_es_0_00_y_sin_nota_cuando_todas_las_escenas_tienen_toma_buena() -> None:
    resultado, tiempos = _analizar(_guion_con_capitulos(["Uno", "Dos"], [8, 8]))
    calculo = calcular_capitulos(resultado, tiempos, _tomas_por_escena({0: 30.0, 1: 30.0}))
    contenido = formatear_capitulos_youtube(calculo)

    assert contenido is not None
    lineas = contenido.splitlines()
    assert lineas[0] == "0:00 Uno"
    assert not any(linea.startswith("Nota: ") for linea in lineas)


def test_sin_ninguna_toma_buena_la_primera_linea_advierte_de_tiempos_estimados() -> None:
    resultado, tiempos = _analizar(_guion_con_capitulos(["Uno", "Dos"], [8, 8]))
    calculo = calcular_capitulos(resultado, tiempos, {})
    contenido = formatear_capitulos_youtube(calculo)

    assert contenido is not None
    lineas = contenido.splitlines()
    assert lineas[0].startswith("Nota: ")
    assert "ESTIMADOS" in lineas[0]
    assert lineas[1] == "0:00 Uno"


def test_mezcla_de_tiempos_reales_y_estimados_se_advierte_con_el_detalle() -> None:
    resultado, tiempos = _analizar(
        _guion_con_capitulos(["Uno", "Dos", "Tres"], [8, 8, 8], duracion_por_escena_segundos=15)
    )
    calculo = calcular_capitulos(resultado, tiempos, _tomas_por_escena({0: 30.0}))
    contenido = formatear_capitulos_youtube(calculo)

    assert contenido is not None
    nota = contenido.splitlines()[0]
    assert nota.startswith("Nota: ")
    assert "1" in nota and "2" in nota  # escenas 1 y 2 sin toma buena


# --- Requisito 3: formato exacto de YouTube -----------------------------------------


def test_formatear_omite_una_marca_demasiado_cercana_a_la_anterior() -> None:
    configuracion = Configuracion()
    resultado, tiempos = _analizar(
        _guion_con_capitulos(["Uno", "Dos", "Tres"], [8, 8, 8], duracion_por_escena_segundos=15)
    )
    # "Dos" arranca a los 3s de "Uno" (menos del minimo de la plataforma, se
    # omite); "Tres" arranca a los 3+8=11s de "Uno" (>= el minimo, se conserva).
    calculo = calcular_capitulos(
        resultado, tiempos, _tomas_por_escena({0: 3.0, 1: 8.0, 2: 5.0})
    )
    contenido = formatear_capitulos_youtube(calculo, configuracion)

    assert contenido is not None
    lineas = [linea for linea in contenido.splitlines() if not linea.startswith("Nota: ")]
    # La marca de "Dos" (a 3s de "Uno") se omite; "Tres" si se conserva.
    assert [linea.split(" ", 1)[1] for linea in lineas] == ["Uno", "Tres"]
    assert validar_capitulos_youtube(contenido, configuracion) == []


def test_capitulos_youtube_de_los_guiones_reales_pasa_el_validador_estricto(
    texto_guiones_reales: dict[str, str],
) -> None:
    configuracion = Configuracion()
    alguno_generado = False
    for nombre, texto in texto_guiones_reales.items():
        resultado, tiempos = _analizar(texto)
        contenido, calculo = generar_capitulos_youtube(resultado, tiempos, {}, configuracion)
        if calculo.motivo_sin_generar is not None:
            continue
        alguno_generado = True
        assert contenido is not None
        assert validar_capitulos_youtube(contenido, configuracion) == [], (
            f"capitulos-youtube.txt de {nombre} no pasa el validador estricto."
        )
    assert alguno_generado, "ningun guion real trae seccion Capítulos: el test no prueba nada."


# --- Validador independiente --------------------------------------------------------


def test_validar_detecta_marca_por_debajo_del_minimo() -> None:
    contenido = "0:00 Uno\n0:05 Dos\n"
    problemas = validar_capitulos_youtube(contenido)
    assert problemas


def test_validar_detecta_que_la_primera_marca_no_es_0_00() -> None:
    contenido = "0:15 Uno\n0:30 Dos\n"
    problemas = validar_capitulos_youtube(contenido)
    assert any("0:00" in p for p in problemas)


def test_validar_ignora_la_linea_de_nota() -> None:
    contenido = "Nota: tiempos ESTIMADOS.\n0:00 Uno\n0:20 Dos\n"
    assert validar_capitulos_youtube(contenido) == []


# --- Requisito 5 / guardado ----------------------------------------------------------


def test_generar_y_guardar_capitulos_youtube(tmp_path: Path) -> None:
    resultado, tiempos = _analizar(_guion_con_capitulos(["Uno", "Dos"], [8, 8]))
    contenido, calculo = generar_capitulos_youtube(resultado, tiempos, {})
    assert contenido is not None
    assert calculo.motivo_sin_generar is None

    destino = guardar_capitulos_youtube(contenido, tmp_path)
    assert destino.name == NOMBRE_ARCHIVO_CAPITULOS_YOUTUBE
    assert destino.read_text(encoding="utf-8") == contenido


# --- R-22: capitulos-ffmpeg.txt (FFMETADATA1) ---------------------------------------


def test_duracion_total_segundos_es_el_cursor_final_tras_el_ultimo_capitulo() -> None:
    resultado, tiempos = _analizar(
        _guion_con_capitulos(["Uno", "Dos", "Tres"], [8, 8, 8], duracion_por_escena_segundos=15)
    )
    calculo = calcular_capitulos(resultado, tiempos, _tomas_por_escena({0: 10.0, 1: 20.0}))

    cursor = 10.0 + 20.0 + tiempos.escenas[2].duracion_estimada_segundos
    assert calculo.duracion_total_segundos == pytest.approx(cursor, abs=1e-6)


def test_duracion_total_segundos_es_cero_sin_ningun_capitulo() -> None:
    resultado, tiempos = _analizar(_guion_sin_capitulos([8, 8]))
    calculo = calcular_capitulos(resultado, tiempos, {})

    assert calculo.capitulos == ()
    assert calculo.duracion_total_segundos == 0.0
    assert formatear_capitulos_ffmpeg(calculo) is None


def test_formatear_ffmpeg_primera_linea_y_un_bloque_chapter_por_capitulo() -> None:
    resultado, tiempos = _analizar(_guion_con_capitulos(["Uno", "Dos"], [8, 8]))
    calculo = calcular_capitulos(resultado, tiempos, _tomas_por_escena({0: 30.0, 1: 30.0}))
    contenido = formatear_capitulos_ffmpeg(calculo)

    assert contenido is not None
    assert contenido.startswith(";FFMETADATA1\n")
    assert contenido.count("[CHAPTER]") == 2
    assert "TIMEBASE=1/1000" in contenido
    assert "START=0" in contenido
    assert "END=30000" in contenido
    assert "title=Uno" in contenido
    assert "title=Dos" in contenido


def test_formatear_ffmpeg_end_de_cada_capitulo_es_el_start_del_siguiente() -> None:
    resultado, tiempos = _analizar(_guion_con_capitulos(["Uno", "Dos", "Tres"], [8, 8, 8]))
    calculo = calcular_capitulos(
        resultado, tiempos, _tomas_por_escena({0: 12.5, 1: 7.25, 2: 20.0})
    )
    contenido = formatear_capitulos_ffmpeg(calculo)
    assert contenido is not None

    starts = [int(v) for v in re.findall(r"START=(\d+)", contenido)]
    ends = [int(v) for v in re.findall(r"END=(\d+)", contenido)]
    assert starts == [0, 12500, 19750]
    assert ends == [12500, 19750, int(calculo.duracion_total_segundos * 1000)]
    assert ends[:-1] == starts[1:]  # END de un capitulo es el START del siguiente


def test_formatear_ffmpeg_no_filtra_por_marca_minima_a_diferencia_de_youtube() -> None:
    """Requisito 4: dos escenas a solo 3s una de otra -- YouTube la omitiria
    (test_formatear_omite_una_marca_demasiado_cercana_a_la_anterior), el
    formato FFMETADATA1 la conserva como su propio capitulo."""
    resultado, tiempos = _analizar(_guion_con_capitulos(["Uno", "Dos"], [8, 8]))
    calculo = calcular_capitulos(resultado, tiempos, _tomas_por_escena({0: 3.0, 1: 8.0}))
    contenido = formatear_capitulos_ffmpeg(calculo)

    assert contenido is not None
    assert contenido.count("[CHAPTER]") == 2
    assert "title=Uno" in contenido
    assert "title=Dos" in contenido


def test_formatear_ffmpeg_escapa_caracteres_especiales_del_titulo() -> None:
    resultado, tiempos = _analizar(
        _guion_con_capitulos([r"Antes\Despues; Capitulo #1 = Final"], [8])
    )
    calculo = calcular_capitulos(resultado, tiempos, _tomas_por_escena({0: 10.0}))
    contenido = formatear_capitulos_ffmpeg(calculo)

    assert contenido is not None
    assert r"title=Antes\\Despues\; Capitulo \#1 \= Final" in contenido
    assert validar_capitulos_ffmpeg(contenido) == []


def test_formatear_ffmpeg_sin_ninguna_toma_buena_advierte_con_comentario() -> None:
    resultado, tiempos = _analizar(_guion_con_capitulos(["Uno", "Dos"], [8, 8]))
    calculo = calcular_capitulos(resultado, tiempos, {})
    contenido = formatear_capitulos_ffmpeg(calculo)

    assert contenido is not None
    lineas = contenido.splitlines()
    assert lineas[0] == ";FFMETADATA1"
    assert lineas[1].startswith(";")
    assert "ESTIMADOS" in lineas[1]


def test_formatear_ffmpeg_con_toma_buena_en_todas_las_escenas_no_lleva_nota() -> None:
    resultado, tiempos = _analizar(_guion_con_capitulos(["Uno", "Dos"], [8, 8]))
    calculo = calcular_capitulos(resultado, tiempos, _tomas_por_escena({0: 30.0, 1: 30.0}))
    contenido = formatear_capitulos_ffmpeg(calculo)

    assert contenido is not None
    comentarios_extra = [
        linea
        for linea in contenido.splitlines()
        if linea.startswith(";") and linea != ";FFMETADATA1"
    ]
    assert comentarios_extra == []


def test_capitulos_ffmpeg_de_los_guiones_reales_cumple_el_criterio_de_aceptacion(
    texto_guiones_reales: dict[str, str],
) -> None:
    alguno_generado = False
    for nombre, texto in texto_guiones_reales.items():
        resultado, tiempos = _analizar(texto)
        calculo = calcular_capitulos(resultado, tiempos, {})
        contenido = formatear_capitulos_ffmpeg(calculo)
        if calculo.motivo_sin_generar is not None:
            assert contenido is None
            continue
        alguno_generado = True
        assert contenido is not None
        assert validar_capitulos_ffmpeg(contenido) == [], (
            f"capitulos-ffmpeg.txt de {nombre} no pasa el validador estricto."
        )
        starts = [int(v) for v in re.findall(r"START=(\d+)", contenido)]
        ends = [int(v) for v in re.findall(r"END=(\d+)", contenido)]
        assert len(starts) == len(calculo.capitulos) == len(ends)
        assert ends[:-1] == starts[1:]
        assert ends[-1] == int(calculo.duracion_total_segundos * 1000)
    assert alguno_generado, "ningun guion real trae seccion Capítulos: el test no prueba nada."


# --- Validador FFMETADATA1 independiente ---------------------------------------------


def test_validar_ffmpeg_exige_primera_linea_ffmetadata1() -> None:
    problemas = validar_capitulos_ffmpeg("[CHAPTER]\nSTART=0\nEND=1000\ntitle=Uno\n")
    assert any("FFMETADATA1" in p for p in problemas)


def test_validar_ffmpeg_detecta_start_no_creciente() -> None:
    contenido = (
        ";FFMETADATA1\n\n[CHAPTER]\nSTART=0\nEND=1000\ntitle=Uno\n\n"
        "[CHAPTER]\nSTART=0\nEND=2000\ntitle=Dos\n"
    )
    problemas = validar_capitulos_ffmpeg(contenido)
    assert problemas


def test_validar_ffmpeg_detecta_solape_entre_capitulos() -> None:
    contenido = (
        ";FFMETADATA1\n\n[CHAPTER]\nSTART=0\nEND=2000\ntitle=Uno\n\n"
        "[CHAPTER]\nSTART=1000\nEND=3000\ntitle=Dos\n"
    )
    problemas = validar_capitulos_ffmpeg(contenido)
    assert problemas


def test_validar_ffmpeg_detecta_valor_negativo() -> None:
    contenido = ";FFMETADATA1\n\n[CHAPTER]\nSTART=-5\nEND=1000\ntitle=Uno\n"
    problemas = validar_capitulos_ffmpeg(contenido)
    assert problemas


def test_validar_ffmpeg_ignora_el_comentario_de_nota() -> None:
    contenido = (
        ";FFMETADATA1\n;tiempos ESTIMADOS\n\n[CHAPTER]\nSTART=0\nEND=1000\ntitle=Uno\n"
    )
    assert validar_capitulos_ffmpeg(contenido) == []


def test_validar_ffmpeg_sin_ningun_bloque_chapter() -> None:
    problemas = validar_capitulos_ffmpeg(";FFMETADATA1\n")
    assert problemas


# --- Guardado --------------------------------------------------------------------------


def test_guardar_capitulos_ffmpeg(tmp_path: Path) -> None:
    resultado, tiempos = _analizar(_guion_con_capitulos(["Uno", "Dos"], [8, 8]))
    calculo = calcular_capitulos(resultado, tiempos, _tomas_por_escena({0: 10.0, 1: 10.0}))
    contenido = formatear_capitulos_ffmpeg(calculo)
    assert contenido is not None

    destino = guardar_capitulos_ffmpeg(contenido, tmp_path)
    assert destino.name == NOMBRE_ARCHIVO_CAPITULOS_FFMPEG
    assert destino.read_text(encoding="utf-8") == contenido
