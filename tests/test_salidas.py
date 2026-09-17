"""Tests del selector de salidas por validacion (tarea T-30)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from capitulos_youtube import generar_capitulos_youtube
from config import (
    NOMBRE_ARCHIVO_SRT_ALINEADO,
    NOMBRE_ARCHIVO_TARJETAS_JSON,
    Configuracion,
)
from estado import cargar_estado, estado_inicial, guardar_estado
from parser import ResultadoParseo, parsear_guion
from pdf import exportar_pdf
from pptx import exportar_pptx
from reproductor import generar_reproductor_html, guardar_reproductor
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
from srt import exportar_srt
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

# Mismo guion de dos escenas, con una seccion `Capítulos` (R-07) delante -- para
# probar `TipoSalida.CAPITULOS_YOUTUBE` (R-18) sin tocar el resto de guiones de
# este archivo, que deliberadamente no traen esa seccion (regresion: sin ella,
# la salida queda omitida, nunca es un fallo).
_GUION_DOS_ESCENAS_CON_CAPITULOS = """# Guion de prueba

## Capítulos (para la descripción del vídeo)

| Marca | Capítulo |
|---|---|
| 0:00 | Primero |
| 0:00 | Segundo |
""" + _GUION_DOS_ESCENAS.split("\n", 1)[1]

# Toma `buena` registrada para la escena 0 (`BLOQUE 0`) de los dos guiones de
# arriba -- mismo contenedor que `EstadoProyecto.tomas` (R-02), reutilizado tal
# cual por `srt_alineado.py`/`pptx.py`/`capitulos_youtube.py` desde R-05/R-13/R-07.
_TOMAS_ESCENA_0_BUENA = {
    "0": {
        "titulo": "Arranque",
        "tomas": [{"numero": 1, "duracion_segundos": 4.0, "nota": "", "buena": True}],
    },
}


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


def test_pregunta_sugiere_las_cinco_salidas_sin_historico(tmp_path: Path) -> None:
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
    assert tipos_omitidos == {
        TipoSalida.SRT,
        TipoSalida.PDF,
        TipoSalida.PPTX,
        TipoSalida.CAPITULOS_YOUTUBE,
    }
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


def test_pptx_latente_no_impide_las_demas(tmp_path: Path) -> None:
    """Criterio de aceptacion literal de T-30: con la salida `.pptx`
    latente (skill de marca ausente en esta maquina), las demas se generan
    igualmente y el resumen lo refleja. `_GUION_DOS_ESCENAS` no trae seccion
    `Capítulos` a propósito: `CAPITULOS_YOUTUBE` queda omitida por ese
    motivo (requisito 4 de R-18) sin que eso afecte a ninguna otra salida ni
    se confunda con un fallo real."""
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    resumen = generar_salidas_seleccionadas(
        SeleccionSalidas(TODAS_LAS_SALIDAS), resultado, tiempos, tmp_path, nombre_guion="prueba"
    )

    tipos_generados = {a.tipo for a in resumen.generadas}
    assert tipos_generados == {TipoSalida.HTML, TipoSalida.SRT, TipoSalida.PDF, TipoSalida.PPTX}
    assert any(latente.tipo is TipoSalida.PPTX for latente in resumen.latentes)
    assert len(resumen.omitidas) == 1
    omitida_capitulos = resumen.omitidas[0]
    assert omitida_capitulos.tipo is TipoSalida.CAPITULOS_YOUTUBE
    assert not omitida_capitulos.motivo.startswith("fallo al generar")
    archivos_pptx = [a for a in resumen.generadas if a.tipo is TipoSalida.PPTX]
    assert len(archivos_pptx) == 2  # tarjetas.json + brief-pptx.md, ambos ya en disco
    for archivo in resumen.generadas:
        assert archivo.ruta.exists()
        assert archivo.tamano_bytes == archivo.ruta.stat().st_size


# --- R-18: tomas_por_escena conecta el selector con el parte de rodaje real -------


def test_srt_sin_tomas_genera_solo_el_estimado(tmp_path: Path) -> None:
    """Sin `tomas_por_escena` (o vacio), seleccionar `SRT` sigue generando
    exactamente un archivo -- el estimado de siempre, comportamiento
    identico al de antes de R-18 (requisito 2)."""
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    resumen = generar_salidas_seleccionadas(
        SeleccionSalidas((TipoSalida.SRT,)), resultado, tiempos, tmp_path, nombre_guion="prueba"
    )
    archivos_srt = [a for a in resumen.generadas if a.tipo is TipoSalida.SRT]
    assert len(archivos_srt) == 1
    assert archivos_srt[0].ruta.name != NOMBRE_ARCHIVO_SRT_ALINEADO


def test_srt_con_toma_buena_genera_tambien_el_alineado(tmp_path: Path) -> None:
    """Requisito 2 de R-18: en cuanto `tomas_por_escena` trae al menos una
    toma `buena`, seleccionar `SRT` genera ademas `guion-alineado.srt`
    (R-05) como un segundo `ArchivoGenerado` bajo el mismo `TipoSalida.SRT`."""
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS_CON_CAPITULOS)
    resumen = generar_salidas_seleccionadas(
        SeleccionSalidas((TipoSalida.SRT,)),
        resultado,
        tiempos,
        tmp_path,
        nombre_guion="prueba",
        tomas_por_escena=_TOMAS_ESCENA_0_BUENA,
    )
    archivos_srt = sorted(
        (a for a in resumen.generadas if a.tipo is TipoSalida.SRT), key=lambda a: a.ruta.name
    )
    assert len(archivos_srt) == 2
    nombres = {a.ruta.name for a in archivos_srt}
    assert NOMBRE_ARCHIVO_SRT_ALINEADO in nombres
    for archivo in archivos_srt:
        assert archivo.ruta.exists()
        assert archivo.tamano_bytes == archivo.ruta.stat().st_size


def test_srt_con_tomas_sin_ninguna_buena_no_genera_el_alineado(tmp_path: Path) -> None:
    """Un `tomas_por_escena` no vacio pero sin ninguna toma marcada `buena`
    (todas en curso o descartadas) se comporta igual que sin tomas: solo se
    genera el `.srt` estimado, nunca un alineado que no reflejaria ninguna
    evidencia real."""
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS_CON_CAPITULOS)
    tomas_sin_buena = {
        "0": {
            "titulo": "Arranque",
            "tomas": [{"numero": 1, "duracion_segundos": 4.0, "nota": "", "buena": False}],
        },
    }
    resumen = generar_salidas_seleccionadas(
        SeleccionSalidas((TipoSalida.SRT,)),
        resultado,
        tiempos,
        tmp_path,
        nombre_guion="prueba",
        tomas_por_escena=tomas_sin_buena,
    )
    archivos_srt = [a for a in resumen.generadas if a.tipo is TipoSalida.SRT]
    assert len(archivos_srt) == 1


def test_pptx_con_tomas_incluye_duracion_real(tmp_path: Path) -> None:
    """Requisito 3 de R-18: seleccionar `PPTX` con `tomas_por_escena` hace
    que `tarjetas.json` traiga duracion real y limites absolutos reales
    (R-13/R-16) para la escena con toma buena, sin ninguna accion manual."""
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS_CON_CAPITULOS)
    resumen = generar_salidas_seleccionadas(
        SeleccionSalidas((TipoSalida.PPTX,)),
        resultado,
        tiempos,
        tmp_path,
        nombre_guion="prueba",
        tomas_por_escena=_TOMAS_ESCENA_0_BUENA,
    )
    archivo_tarjetas = next(
        a
        for a in resumen.generadas
        if a.tipo is TipoSalida.PPTX and a.ruta.name == NOMBRE_ARCHIVO_TARJETAS_JSON
    )
    datos = json.loads(archivo_tarjetas.ruta.read_text(encoding="utf-8"))
    assert datos["metadatos"]["mezcla_duracion_real_y_estimada"] is True
    escena_0 = next(e for e in datos["escenas"] if e["numero"] == 0)
    assert escena_0["duracion_real_segundos"] == pytest.approx(4.0)
    assert escena_0["inicio_segundos"] == 0.0
    assert escena_0["fin_segundos"] == pytest.approx(4.0)


def test_capitulos_youtube_es_la_quinta_opcion_de_la_pregunta() -> None:
    """Requisito 4 de R-18: `TipoSalida` gana una quinta opcion,
    `CAPITULOS_YOUTUBE`, presente en `TODAS_LAS_SALIDAS`/`DESCRIPCION_SALIDA`
    junto a las cuatro ya existentes."""
    assert TODAS_LAS_SALIDAS[-1] is TipoSalida.CAPITULOS_YOUTUBE
    assert len(TODAS_LAS_SALIDAS) == 5


def test_capitulos_youtube_generado_coincide_con_la_llamada_directa(tmp_path: Path) -> None:
    """Requisito 4 de R-18: seleccionar `CAPITULOS_YOUTUBE` produce
    exactamente el mismo contenido que la llamada directa a
    `capitulos_youtube.generar_capitulos_youtube` en las mismas condiciones
    -- mismo criterio que ya ejercita `verificar_salidas.py --fixture`."""
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS_CON_CAPITULOS)
    resumen = generar_salidas_seleccionadas(
        SeleccionSalidas((TipoSalida.CAPITULOS_YOUTUBE,)),
        resultado,
        tiempos,
        tmp_path,
        nombre_guion="prueba",
        tomas_por_escena=_TOMAS_ESCENA_0_BUENA,
    )
    archivo = next(a for a in resumen.generadas if a.tipo is TipoSalida.CAPITULOS_YOUTUBE)
    contenido_directo, _ = generar_capitulos_youtube(resultado, tiempos, _TOMAS_ESCENA_0_BUENA)
    assert contenido_directo is not None
    assert archivo.ruta.read_text(encoding="utf-8") == contenido_directo


def test_capitulos_youtube_sin_seccion_queda_omitida_nunca_latente_ni_fallo(
    tmp_path: Path,
) -> None:
    """Requisito 4 de R-18: sin seccion `Capítulos` en el guion, la salida
    queda como `SalidaOmitida` con el motivo exacto de
    `formatear_capitulos_youtube`/`calcular_capitulos` -- nunca como fallo
    ni como `SalidaLatente` (no depende de nada externo ausente)."""
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    resumen = generar_salidas_seleccionadas(
        SeleccionSalidas((TipoSalida.CAPITULOS_YOUTUBE,)),
        resultado,
        tiempos,
        tmp_path,
        nombre_guion="prueba",
    )
    assert resumen.generadas == ()
    assert not resumen.latentes
    omitida = next(o for o in resumen.omitidas if o.tipo is TipoSalida.CAPITULOS_YOUTUBE)
    assert not omitida.motivo.startswith("fallo al generar")
    assert "no seleccionada" not in omitida.motivo


def test_regresion_guiones_reales_sin_tomas_identica_a_antes_de_r18(
    tmp_path: Path, texto_guiones_reales: dict[str, str]
) -> None:
    """Criterio de aceptacion literal de R-18: sobre los tres guiones reales
    de `fixtures/reales/`, sin ninguna toma registrada, el resultado de
    `generar_salidas_seleccionadas` para HTML/SRT/PDF/PPTX es identico —
    byte a byte — al de llamar directamente a cada generador de bajo nivel,
    tal como se comportaba antes de R-18. Test de regresion explicito, no
    solo ausencia de error."""
    for nombre, texto in texto_guiones_reales.items():
        resultado, tiempos = _pipeline(texto)
        carpeta_via_selector = tmp_path / nombre / "selector"
        carpeta_directa = tmp_path / nombre / "directa"

        resumen = generar_salidas_seleccionadas(
            SeleccionSalidas(TODAS_LAS_SALIDAS),
            resultado,
            tiempos,
            carpeta_via_selector,
            nombre_guion=nombre,
        )

        archivo_html = next(a for a in resumen.generadas if a.tipo is TipoSalida.HTML)
        pagina = generar_reproductor_html(resultado, tiempos, nombre)
        ruta_html_directa = guardar_reproductor(pagina, carpeta_directa)
        assert archivo_html.ruta.read_text(
            encoding="utf-8"
        ) == ruta_html_directa.read_text(encoding="utf-8"), f"{nombre}: HTML difiere"

        archivos_srt = [a for a in resumen.generadas if a.tipo is TipoSalida.SRT]
        assert len(archivos_srt) == 1, f"{nombre}: debe generar solo el .srt estimado"
        assert archivos_srt[0].ruta.read_text(encoding="utf-8") == exportar_srt(
            tiempos
        ), f"{nombre}: .srt difiere"

        resultado_pdf_directo = exportar_pdf(resultado, tiempos, carpeta_directa, nombre)
        archivo_pdf_html = next(
            a
            for a in resumen.generadas
            if a.tipo is TipoSalida.PDF and a.ruta.suffix == ".html"
        )
        assert archivo_pdf_html.ruta.read_text(
            encoding="utf-8"
        ) == resultado_pdf_directo.ruta_html.read_text(
            encoding="utf-8"
        ), f"{nombre}: HTML de impresion difiere"

        resultado_pptx_directo = exportar_pptx(resultado, tiempos, carpeta_directa, nombre)
        archivo_tarjetas = next(
            a
            for a in resumen.generadas
            if a.tipo is TipoSalida.PPTX and a.ruta.name == NOMBRE_ARCHIVO_TARJETAS_JSON
        )
        assert archivo_tarjetas.ruta.read_text(
            encoding="utf-8"
        ) == resultado_pptx_directo.ruta_tarjetas_json.read_text(
            encoding="utf-8"
        ), f"{nombre}: tarjetas.json difiere"


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
