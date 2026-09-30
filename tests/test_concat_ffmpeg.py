"""Tests de la lista de concatenacion de ffmpeg (tarea R-19).

Mismo patron que `tests/test_srt_alineado.py`/`tests/test_capitulos_youtube.py`:
guiones sinteticos minimos con control total sobre el numero de escenas, mas
un mapa `{numero_escena: dict_de_escena}` de tomas buenas.
"""

from __future__ import annotations

from pathlib import Path

from concat_ffmpeg import (
    EscenaPendiente,
    calcular_lista_concat_ffmpeg,
    generar_lista_concat_ffmpeg,
    guardar_lista_concat_ffmpeg,
    validar_lista_concat_ffmpeg,
)
from config import NOMBRE_ARCHIVO_CONCAT_FFMPEG, Configuracion
from parser import parsear_guion
from tiempos import ResultadoTiempos, calcular_tiempos


def _mmss(segundos: int) -> str:
    return f"{segundos // 60}:{segundos % 60:02d}"


def _guion_n_escenas(n: int, duracion_por_escena_segundos: int = 10) -> str:
    partes = ["# Titulo\n"]
    inicio = 0
    for indice in range(n):
        fin = inicio + duracion_por_escena_segundos
        partes.append(
            f"\n## BLOQUE {indice} - Escena {indice} ({_mmss(inicio)} - {_mmss(fin)})\n\n"
            f"**LOCUCIÓN**\n\n> Una frase cualquiera para la escena {indice}.\n"
        )
        inicio = fin
    return "".join(partes)


def _tiempos(n_escenas: int) -> ResultadoTiempos:
    resultado = parsear_guion(_guion_n_escenas(n_escenas))
    return calcular_tiempos(resultado, Configuracion())


def _toma_buena(archivo_video: str = "", numero_toma: int = 1) -> dict[str, object]:
    return {
        "numero": numero_toma,
        "duracion_segundos": 4.0,
        "nota": "",
        "buena": True,
        "archivo_video": archivo_video,
    }


def _toma_no_buena(numero_toma: int = 1) -> dict[str, object]:
    return {"numero": numero_toma, "duracion_segundos": 4.0, "nota": "", "buena": False}


def _escena(titulo: str, *tomas: dict[str, object]) -> dict[str, object]:
    return {"titulo": titulo, "tomas": list(tomas)}


def _tomas_por_escena(escenas: dict[int, dict[str, object]]) -> dict[str, object]:
    """`escenas` mapea numero de escena -> el dict de escena tal cual
    (`{"titulo": ..., "tomas": [...]}`), mismo contenedor que
    `EstadoProyecto.tomas`."""
    return {str(numero): valor for numero, valor in escenas.items()}


# --- Requisito 3: orden real de escenas, linea `file` o comentario por cada una ----


def test_escena_con_archivo_anotado_genera_linea_file() -> None:
    tiempos = _tiempos(1)
    tomas = _tomas_por_escena({0: _escena("Escena 0", _toma_buena("CLIP0001.MP4"))})
    resultado = calcular_lista_concat_ffmpeg(tiempos, tomas)
    assert resultado.motivo_sin_generar is None
    assert resultado.lineas == ("file 'CLIP0001.MP4'",)
    assert resultado.escenas_pendientes == ()


def test_escena_sin_toma_buena_genera_comentario_con_motivo() -> None:
    tiempos = _tiempos(1)
    tomas = _tomas_por_escena({0: _escena("Escena 0", _toma_no_buena())})
    resultado = calcular_lista_concat_ffmpeg(tiempos, tomas)
    assert resultado.lineas == ("# ESCENA 0: sin_toma_buena",)
    assert resultado.escenas_pendientes == (EscenaPendiente(0, "sin_toma_buena"),)


def test_escena_con_toma_buena_sin_archivo_genera_comentario_con_motivo() -> None:
    tiempos = _tiempos(1)
    tomas = _tomas_por_escena({0: _escena("Escena 0", _toma_buena(""))})
    resultado = calcular_lista_concat_ffmpeg(tiempos, tomas)
    assert resultado.lineas == ("# ESCENA 0: sin_archivo_anotado",)
    assert resultado.escenas_pendientes == (EscenaPendiente(0, "sin_archivo_anotado"),)


def test_orden_de_lineas_coincide_con_el_orden_real_de_escenas() -> None:
    tiempos = _tiempos(3)
    tomas = _tomas_por_escena(
        {
            0: _escena("Escena 0", _toma_buena("a.mp4")),
            1: _escena("Escena 1", _toma_buena("")),
            2: _escena("Escena 2", _toma_buena("c.mp4")),
        }
    )
    resultado = calcular_lista_concat_ffmpeg(tiempos, tomas)
    assert resultado.lineas == (
        "file 'a.mp4'",
        "# ESCENA 1: sin_archivo_anotado",
        "file 'c.mp4'",
    )
    assert resultado.escenas_pendientes == (EscenaPendiente(1, "sin_archivo_anotado"),)


# --- Requisito 4: nunca falla por pendientes; sin parte de rodaje, no genera nada --


def test_mezcla_de_pendientes_y_anotadas_nunca_falla() -> None:
    """Ninguna combinacion de escenas pendientes hace que el calculo lance
    una excepcion: el archivo se genera siempre que haya al menos un parte
    de rodaje, mezclando lineas `file` y comentarios segun haga falta."""
    tiempos = _tiempos(2)
    tomas = _tomas_por_escena({0: _escena("Escena 0", _toma_buena("a.mp4"))})
    resultado = calcular_lista_concat_ffmpeg(tiempos, tomas)
    assert resultado.motivo_sin_generar is None
    assert len(resultado.lineas) == 2
    assert len(resultado.escenas_pendientes) == 1


def test_sin_ningun_parte_de_rodaje_no_genera_nada() -> None:
    tiempos = _tiempos(2)
    resultado = calcular_lista_concat_ffmpeg(tiempos, {})
    assert resultado.lineas == ()
    assert resultado.escenas_pendientes == ()
    assert resultado.motivo_sin_generar is not None

    contenido, _ = generar_lista_concat_ffmpeg(tiempos, {})
    assert contenido is None


def test_sin_parametro_tomas_por_escena_equivale_a_vacio() -> None:
    tiempos = _tiempos(1)
    contenido, resultado = generar_lista_concat_ffmpeg(tiempos)
    assert contenido is None
    assert resultado.motivo_sin_generar is not None


# --- Requisito 6 de la criteria de aceptacion: escapado de comillas simples --------


def test_archivo_con_comilla_simple_se_escapa_correctamente() -> None:
    tiempos = _tiempos(1)
    tomas = _tomas_por_escena(
        {0: _escena("Escena 0", _toma_buena("carpeta d'el dueño/CLIP01.MP4"))}
    )
    contenido, _ = generar_lista_concat_ffmpeg(tiempos, tomas)
    assert contenido is not None
    assert "file 'carpeta d'\\''el dueño/CLIP01.MP4'" in contenido
    assert validar_lista_concat_ffmpeg(contenido) == []


# --- Criterio de aceptacion literal: formato exacto de `ffmpeg -f concat` ----------


def test_generado_con_todas_las_escenas_anotadas_pasa_el_validador() -> None:
    tiempos = _tiempos(3)
    tomas = _tomas_por_escena(
        {
            0: _escena("Escena 0", _toma_buena("a.mp4")),
            1: _escena("Escena 1", _toma_buena("b.mp4")),
            2: _escena("Escena 2", _toma_buena("c.mp4")),
        }
    )
    contenido, resultado = generar_lista_concat_ffmpeg(tiempos, tomas)
    assert contenido is not None
    assert resultado.escenas_pendientes == ()
    assert validar_lista_concat_ffmpeg(contenido) == []
    assert contenido == "file 'a.mp4'\nfile 'b.mp4'\nfile 'c.mp4'\n"


def test_mezcla_de_escenas_anotadas_sin_anotar_y_sin_toma_buena_pasa_el_validador() -> None:
    tiempos = _tiempos(3)
    tomas = _tomas_por_escena(
        {
            0: _escena("Escena 0", _toma_buena("a.mp4")),
            1: _escena("Escena 1", _toma_buena("")),
            2: _escena("Escena 2", _toma_no_buena()),
        }
    )
    contenido, resultado = generar_lista_concat_ffmpeg(tiempos, tomas)
    assert contenido is not None
    assert len(resultado.escenas_pendientes) == 2
    assert {p.motivo for p in resultado.escenas_pendientes} == {
        "sin_archivo_anotado",
        "sin_toma_buena",
    }
    assert validar_lista_concat_ffmpeg(contenido) == []


def test_validador_rechaza_una_linea_con_comilla_simple_sin_escapar() -> None:
    problemas = validar_lista_concat_ffmpeg("file 'carpeta'del dueño/CLIP01.MP4'\n")
    assert problemas


def test_validador_rechaza_una_linea_sin_el_formato_file() -> None:
    problemas = validar_lista_concat_ffmpeg("CLIP0001.MP4\n")
    assert problemas


def test_validador_acepta_comentarios_y_lineas_vacias() -> None:
    assert validar_lista_concat_ffmpeg("# ESCENA 0: sin_toma_buena\n\nfile 'a.mp4'\n") == []


# --- Guardado en disco --------------------------------------------------------------


def test_guardar_lista_concat_ffmpeg_escribe_el_archivo(tmp_path: Path) -> None:
    tiempos = _tiempos(1)
    tomas = _tomas_por_escena({0: _escena("Escena 0", _toma_buena("a.mp4"))})
    contenido, _ = generar_lista_concat_ffmpeg(tiempos, tomas)
    assert contenido is not None
    destino = guardar_lista_concat_ffmpeg(contenido, tmp_path)
    assert destino.name == NOMBRE_ARCHIVO_CONCAT_FFMPEG
    assert destino.read_text(encoding="utf-8") == contenido
