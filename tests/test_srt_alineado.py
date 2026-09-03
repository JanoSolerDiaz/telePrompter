"""Tests del `.srt` alineado con la toma buena (tarea R-05).

Mismo patron que `tests/test_calibracion.py` (R-04): guiones sinteticos
minimos con control total sobre el numero de palabras y la duracion objetivo,
mas un mapa `{numero_escena: duracion_real_segundos}` de tomas buenas.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from config import NOMBRE_ARCHIVO_SRT, NOMBRE_ARCHIVO_SRT_ALINEADO, Configuracion
from parser import parsear_guion
from srt import validar_srt
from srt_alineado import (
    exportar_srt_alineado,
    generar_srt_alineado,
    guardar_srt_alineado,
    reescalar_a_toma_buena,
)
from tiempos import ResultadoTiempos, calcular_tiempos


def _mmss(segundos: int) -> str:
    return f"{segundos // 60}:{segundos % 60:02d}"


def _guion_n_escenas(palabras_por_escena: list[int], duracion_por_escena_segundos: int = 10) -> str:
    partes = ["# Titulo\n"]
    inicio = 0
    for indice, num_palabras in enumerate(palabras_por_escena, start=1):
        fin = inicio + duracion_por_escena_segundos
        palabras = " ".join(["palabra"] * num_palabras)
        partes.append(
            f"\n## BLOQUE {indice} - Escena {indice} ({_mmss(inicio)} - {_mmss(fin)})\n\n"
            f"**LOCUCIÓN**\n\n> {palabras}. Otra frase, con coma, aqui.\n"
        )
        inicio = fin
    return "".join(partes)


def _tiempos(palabras_por_escena: list[int]) -> ResultadoTiempos:
    resultado = parsear_guion(_guion_n_escenas(palabras_por_escena))
    return calcular_tiempos(resultado, Configuracion())


def _tomas_por_escena(tomas_buenas_segundos: dict[int, float]) -> dict[str, object]:
    return {
        str(numero): {
            "titulo": f"Escena {numero}",
            "tomas": [{"numero": 1, "duracion_segundos": duracion, "nota": "", "buena": True}],
        }
        for numero, duracion in tomas_buenas_segundos.items()
    }


# --- Requisito 1: reescalar a la duracion real de la toma buena --------------------


def test_escena_con_toma_buena_se_reescala_a_su_duracion_real() -> None:
    tiempos = _tiempos([12, 12, 12])
    alineacion = reescalar_a_toma_buena(tiempos, _tomas_por_escena({1: 5.0, 3: 20.0}))

    assert alineacion.escenas_alineadas == (1, 3)
    assert alineacion.escenas_sin_toma_buena == (2,)

    escena_1, escena_2, escena_3 = alineacion.resultado_tiempos.escenas
    assert escena_1.duracion_estimada_segundos == pytest.approx(5.0, abs=1e-6)
    assert escena_3.duracion_estimada_segundos == pytest.approx(20.0, abs=1e-6)
    # Escena 2 no tiene toma buena: conserva su estimacion original sin tocar.
    tiempos_originales = {e.numero: e.duracion_estimada_segundos for e in tiempos.escenas}
    assert escena_2.duracion_estimada_segundos == pytest.approx(tiempos_originales[2], abs=1e-6)


def test_sin_ninguna_toma_buena_el_resultado_alineado_es_identico_al_estimado() -> None:
    tiempos = _tiempos([10, 10])
    alineacion = reescalar_a_toma_buena(tiempos, {})

    assert alineacion.escenas_alineadas == ()
    assert alineacion.escenas_sin_toma_buena == (1, 2)
    assert alineacion.resultado_tiempos.duracion_total_segundos == pytest.approx(
        tiempos.duracion_total_segundos, abs=1e-6
    )


def test_reescalado_conserva_una_linea_de_tiempo_continua_sin_huecos_ni_solapes() -> None:
    tiempos = _tiempos([12, 12, 12])
    alineacion = reescalar_a_toma_buena(tiempos, _tomas_por_escena({1: 3.0, 2: 30.0}))

    bloques = alineacion.resultado_tiempos.bloques
    cursor = 0.0
    for bloque in bloques:
        assert bloque.inicio_segundos == pytest.approx(cursor, abs=1e-6)
        cursor = bloque.fin_segundos
    assert cursor == pytest.approx(alineacion.resultado_tiempos.duracion_total_segundos, abs=1e-6)


# --- Requisito 2: el .srt estimado sigue siendo una salida independiente -----------


def test_nombres_de_archivo_del_srt_estimado_y_del_alineado_son_distintos() -> None:
    assert NOMBRE_ARCHIVO_SRT_ALINEADO != NOMBRE_ARCHIVO_SRT


def test_guardar_srt_alineado_escribe_en_su_propio_archivo(tmp_path: Path) -> None:
    tiempos = _tiempos([10, 10])
    _contenido, alineacion = generar_srt_alineado(tiempos, _tomas_por_escena({1: 4.0}))
    contenido = exportar_srt_alineado(alineacion)

    destino = guardar_srt_alineado(contenido, tmp_path)
    assert destino.name == NOMBRE_ARCHIVO_SRT_ALINEADO
    assert destino.read_text(encoding="utf-8") == contenido
    assert not (tmp_path / NOMBRE_ARCHIVO_SRT).exists()


# --- Requisito 3 y criterio de aceptacion: mismas reglas estrictas que T-27 --------


def test_srt_alineado_de_una_toma_real_no_tiene_solapes_y_dura_lo_que_la_toma(
    texto_guiones_reales: dict[str, str],
) -> None:
    configuracion = Configuracion()
    _nombre, texto = next(iter(texto_guiones_reales.items()))
    resultado = parsear_guion(texto)
    tiempos = calcular_tiempos(resultado, configuracion)

    primera_escena = tiempos.escenas[0]
    duracion_toma_real = primera_escena.duracion_estimada_segundos * 1.4
    tomas_por_escena = _tomas_por_escena({primera_escena.numero: duracion_toma_real})

    contenido, alineacion = generar_srt_alineado(tiempos, tomas_por_escena, configuracion)

    assert validar_srt(contenido, configuracion) == []
    assert alineacion.escenas_alineadas == (primera_escena.numero,)

    escena_alineada = alineacion.resultado_tiempos.escenas[0]
    assert escena_alineada.duracion_estimada_segundos == pytest.approx(
        duracion_toma_real, abs=configuracion.srt_alineado_tolerancia_segundos
    )


def test_srt_alineado_de_los_guiones_reales_pasa_el_validador_estricto(
    texto_guiones_reales: dict[str, str],
) -> None:
    configuracion = Configuracion()
    for nombre, texto in texto_guiones_reales.items():
        resultado = parsear_guion(texto)
        tiempos = calcular_tiempos(resultado, configuracion)
        # Sin parte de rodaje todavia: ninguna escena tiene toma buena, y el
        # resultado sigue siendo un .srt valido (nunca falla por falta de
        # evidencia real, mismo criterio de honestidad que R-04).
        contenido, alineacion = generar_srt_alineado(tiempos, {}, configuracion)
        assert validar_srt(contenido, configuracion) == [], (
            f"El .srt alineado de {nombre} no pasa el validador estricto sin ninguna "
            "toma buena registrada."
        )
        assert alineacion.escenas_sin_toma_buena == tuple(e.numero for e in tiempos.escenas)
