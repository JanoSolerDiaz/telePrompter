"""Tests del selector de salidas por validacion (tarea T-30)."""

from __future__ import annotations

from pathlib import Path

import pytest

from config import Configuracion
from estado import cargar_estado, estado_inicial, guardar_estado
from parser import ResultadoParseo, parsear_guion
from salidas import (
    TODAS_LAS_SALIDAS,
    ArchivoGenerado,
    SalidaLatente,
    SalidaOmitida,
    SeleccionSalidas,
    TipoSalida,
    construir_pregunta_salidas,
    generar_salidas_seleccionadas,
    registrar_generacion,
)
from tiempos import ResultadoTiempos, calcular_tiempos

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


def _pipeline(
    texto: str, configuracion: Configuracion | None = None
) -> tuple[ResultadoParseo, ResultadoTiempos]:
    configuracion = configuracion or Configuracion()
    resultado = parsear_guion(texto, configuracion=configuracion)
    tiempos = calcular_tiempos(resultado, configuracion)
    return resultado, tiempos


def _guion_temporal(tmp_path: Path, texto: str = _GUION_DOS_ESCENAS) -> Path:
    ruta = tmp_path / "guion.md"
    ruta.write_text(texto, encoding="utf-8")
    return ruta


# --- construir_pregunta_salidas -----------------------------------------------------


def test_pregunta_sugiere_las_cuatro_salidas_sin_historico(tmp_path: Path) -> None:
    estado = estado_inicial(_guion_temporal(tmp_path), Configuracion())
    pregunta = construir_pregunta_salidas(estado)
    assert [opcion.tipo for opcion in pregunta.opciones] == list(TODAS_LAS_SALIDAS)
    assert pregunta.sugerencia == TODAS_LAS_SALIDAS
    assert all(opcion.sugerida for opcion in pregunta.opciones)


def test_pregunta_sugiere_la_ultima_seleccion_registrada(tmp_path: Path) -> None:
    estado = estado_inicial(_guion_temporal(tmp_path), Configuracion())
    seleccion = SeleccionSalidas((TipoSalida.HTML, TipoSalida.SRT))
    resumen = generar_salidas_seleccionadas(
        seleccion, *_pipeline(_GUION_DOS_ESCENAS), tmp_path, nombre_guion="prueba"
    )
    registrar_generacion(estado, seleccion, resumen)

    pregunta = construir_pregunta_salidas(estado)
    assert pregunta.sugerencia == (TipoSalida.HTML, TipoSalida.SRT)
    sugeridas = {opcion.tipo: opcion.sugerida for opcion in pregunta.opciones}
    assert sugeridas[TipoSalida.HTML] is True
    assert sugeridas[TipoSalida.SRT] is True
    assert sugeridas[TipoSalida.PDF] is False
    assert sugeridas[TipoSalida.PPTX] is False


def test_pregunta_ignora_entradas_de_estado_sin_seleccion(tmp_path: Path) -> None:
    """Un `estado.salidas_generadas` con entradas ajenas (formato futuro
    sin clave `seleccion`) no rompe la busqueda de la ultima sugerencia."""
    estado = estado_inicial(_guion_temporal(tmp_path), Configuracion())
    estado.salidas_generadas.append({"algo": "no relacionado"})
    pregunta = construir_pregunta_salidas(estado)
    assert pregunta.sugerencia == TODAS_LAS_SALIDAS


# --- generar_salidas_seleccionadas: independencia (requisito 3) --------------------


def test_no_seleccionadas_quedan_omitidas_sin_generar_archivo(tmp_path: Path) -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    seleccion = SeleccionSalidas((TipoSalida.HTML,))
    resumen = generar_salidas_seleccionadas(
        seleccion, resultado, tiempos, tmp_path, nombre_guion="prueba"
    )
    assert {a.tipo for a in resumen.generadas} == {TipoSalida.HTML}
    tipos_omitidos = {o.tipo for o in resumen.omitidas}
    assert tipos_omitidos == {TipoSalida.SRT, TipoSalida.PDF, TipoSalida.PPTX}
    for omitida in resumen.omitidas:
        assert "no seleccionada" in omitida.motivo


def test_fallo_de_una_salida_no_impide_las_demas(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import salidas as modulo_salidas

    def _reventar(*_args: object, **_kwargs: object) -> None:
        raise RuntimeError("fallo simulado del exportador de .srt")

    monkeypatch.setattr(modulo_salidas, "exportar_srt", _reventar)

    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    seleccion = SeleccionSalidas((TipoSalida.HTML, TipoSalida.SRT))
    resumen = generar_salidas_seleccionadas(
        seleccion, resultado, tiempos, tmp_path, nombre_guion="prueba"
    )

    assert {a.tipo for a in resumen.generadas} == {TipoSalida.HTML}
    omitida_srt = next(o for o in resumen.omitidas if o.tipo is TipoSalida.SRT)
    assert "fallo simulado" in omitida_srt.motivo


def test_pptx_latente_no_impide_las_otras_tres(tmp_path: Path) -> None:
    """Criterio de aceptacion literal de T-30: con la salida `.pptx`
    latente (skill de marca ausente en esta maquina), las otras tres se
    generan igualmente y el resumen lo refleja."""
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    resumen = generar_salidas_seleccionadas(
        SeleccionSalidas(TODAS_LAS_SALIDAS), resultado, tiempos, tmp_path, nombre_guion="prueba"
    )

    tipos_generados = {a.tipo for a in resumen.generadas}
    assert tipos_generados == {TipoSalida.HTML, TipoSalida.SRT, TipoSalida.PDF, TipoSalida.PPTX}
    assert not resumen.omitidas
    assert any(latente.tipo is TipoSalida.PPTX for latente in resumen.latentes)
    archivos_pptx = [a for a in resumen.generadas if a.tipo is TipoSalida.PPTX]
    assert len(archivos_pptx) == 2  # tarjetas.json + brief-pptx.md, ambos ya en disco
    for archivo in resumen.generadas:
        assert archivo.ruta.exists()
        assert archivo.tamano_bytes == archivo.ruta.stat().st_size


# --- dos validaciones seguidas preguntan las dos veces (criterio de aceptacion) -----


def test_dos_validaciones_seguidas_preguntan_las_dos_veces(tmp_path: Path) -> None:
    ruta_guion = _guion_temporal(tmp_path)
    configuracion = Configuracion()
    estado = estado_inicial(ruta_guion, configuracion)
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)

    primera_pregunta = construir_pregunta_salidas(estado)
    assert primera_pregunta.sugerencia == TODAS_LAS_SALIDAS
    primera_seleccion = SeleccionSalidas((TipoSalida.HTML,))
    primer_resumen = generar_salidas_seleccionadas(
        primera_seleccion, resultado, tiempos, tmp_path, nombre_guion="prueba"
    )
    registrar_generacion(estado, primera_seleccion, primer_resumen)
    guardar_estado(estado, tmp_path)

    estado_recargado = cargar_estado(tmp_path)
    segunda_pregunta = construir_pregunta_salidas(estado_recargado)
    assert segunda_pregunta.sugerencia == (TipoSalida.HTML,)

    segunda_seleccion = SeleccionSalidas(TODAS_LAS_SALIDAS)
    segundo_resumen = generar_salidas_seleccionadas(
        segunda_seleccion, resultado, tiempos, tmp_path, nombre_guion="prueba"
    )
    registrar_generacion(estado_recargado, segunda_seleccion, segundo_resumen)
    guardar_estado(estado_recargado, tmp_path)

    assert len(cargar_estado(tmp_path).salidas_generadas) == 2
    tercera_pregunta = construir_pregunta_salidas(cargar_estado(tmp_path))
    assert tercera_pregunta.sugerencia == TODAS_LAS_SALIDAS


# --- registrar_generacion / como_dict -----------------------------------------------


def test_registrar_generacion_es_append_only(tmp_path: Path) -> None:
    estado = estado_inicial(_guion_temporal(tmp_path), Configuracion())
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)

    for seleccion in (
        SeleccionSalidas((TipoSalida.HTML,)),
        SeleccionSalidas((TipoSalida.SRT,)),
    ):
        resumen = generar_salidas_seleccionadas(
            seleccion, resultado, tiempos, tmp_path, nombre_guion="prueba"
        )
        registrar_generacion(estado, seleccion, resumen)

    assert len(estado.salidas_generadas) == 2
    assert estado.salidas_generadas[0]["seleccion"] == ["html"]
    assert estado.salidas_generadas[1]["seleccion"] == ["srt"]


def test_como_dict_incluye_generadas_omitidas_y_latentes() -> None:
    from salidas import ResumenSalidas

    resumen = ResumenSalidas(
        generadas=(ArchivoGenerado(TipoSalida.HTML, Path("x.html"), 10),),
        omitidas=(SalidaOmitida(TipoSalida.SRT, "no seleccionada por el dueño en esta pasada."),),
        latentes=(SalidaLatente(TipoSalida.PPTX, "skill de marca ausente."),),
    )
    datos = resumen.como_dict()
    assert datos["generadas"] == [{"tipo": "html", "ruta": "x.html", "tamano_bytes": 10}]
    assert datos["omitidas"][0]["tipo"] == "srt"
    assert datos["latentes"][0]["tipo"] == "pptx"
