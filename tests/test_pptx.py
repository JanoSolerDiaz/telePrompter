"""Tests del adaptador `.pptx` con identidad 480 (tarea T-29)."""

from __future__ import annotations

import json
from pathlib import Path

from config import NOMBRE_ARCHIVO_BRIEF_PPTX, NOMBRE_ARCHIVO_TARJETAS_JSON, Configuracion
from parser import ResultadoParseo, parsear_guion
from pptx import (
    ResultadoPptx,
    detectar_skill_pptx_disponible,
    exportar_pptx,
    formatear_tarjetas_json,
    generar_brief,
    generar_tarjetas,
    guardar_brief,
    guardar_tarjetas_json,
    tarjetas_a_diccionario,
    validar_tarjetas,
)
from tiempos import ResultadoTiempos, calcular_tiempos

RAIZ = Path(__file__).resolve().parent.parent

_GUION_DOS_ESCENAS = """# Guion de prueba

## BLOQUE 0 — Arranque (0:00 – 0:10)

**LOCUCIÓN**

> Esta es la primera frase del bloque. Y esta la segunda, ya con más ritmo.

**EN PANTALLA**

Título del vídeo en pantalla.

**NOTA**

Recordatorio interno: no mencionar el precio antiguo en la locución.

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


# --- generar_tarjetas ---------------------------------------------------------------


def test_generar_tarjetas_una_por_escena() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    tarjetas = generar_tarjetas(resultado, tiempos, nombre_guion="prueba")
    assert len(tarjetas.tarjetas) == 2
    assert [t.numero for t in tarjetas.tarjetas] == [0, 1]
    assert tarjetas.titulo == "prueba"
    assert tarjetas.para_terceros is False


def test_generar_tarjetas_separa_pantalla_y_notas_internas() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    tarjetas = generar_tarjetas(resultado, tiempos)
    primera = tarjetas.tarjetas[0]
    assert primera.indicaciones_pantalla == ("Título del vídeo en pantalla.",)
    assert primera.notas_internas == (
        "Recordatorio interno: no mencionar el precio antiguo en la locución.",
    )


def test_generar_tarjetas_texto_locucion_es_bloques_unidos() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    tarjetas = generar_tarjetas(resultado, tiempos)
    primera = tarjetas.tarjetas[0]
    assert primera.texto_locucion == " ".join(primera.bloques)
    assert primera.bloques


def test_generar_tarjetas_modo_para_terceros_omite_notas_internas() -> None:
    configuracion = Configuracion(incluir_notas_internas=False)
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS, configuracion)
    tarjetas = generar_tarjetas(resultado, tiempos, configuracion=configuracion)
    assert tarjetas.para_terceros is True
    for tarjeta in tarjetas.tarjetas:
        assert tarjeta.notas_internas == ()
    # las indicaciones de pantalla se mantienen siempre, con o sin --para-terceros
    assert tarjetas.tarjetas[0].indicaciones_pantalla == ("Título del vídeo en pantalla.",)


# --- serializacion y validacion del contrato -----------------------------------------


def test_tarjetas_a_diccionario_produce_json_valido_segun_el_contrato() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    tarjetas = generar_tarjetas(resultado, tiempos, nombre_guion="prueba")
    datos = tarjetas_a_diccionario(tarjetas)
    assert validar_tarjetas(datos) == []
    assert datos["metadatos"]["numero_escenas"] == 2
    assert datos["metadatos"]["titulo"] == "prueba"


def test_formatear_tarjetas_json_es_json_serializable_y_valido() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    tarjetas = generar_tarjetas(resultado, tiempos)
    contenido = formatear_tarjetas_json(tarjetas)
    datos = json.loads(contenido)
    assert validar_tarjetas(datos) == []


def test_validar_tarjetas_detecta_clave_de_metadatos_ausente() -> None:
    datos = {"version_contrato": 1, "metadatos": {}, "escenas": []}
    problemas = validar_tarjetas(datos)
    assert any("metadatos: falta la clave 'titulo'" in p for p in problemas)


def test_validar_tarjetas_detecta_tipo_incorrecto() -> None:
    datos = {
        "version_contrato": 1,
        "metadatos": {
            "titulo": "x",
            "para_terceros": "no",
            "numero_escenas": 1,
            "palabras_locucion_total": 1,
            "duracion_total_segundos": 1.0,
        },
        "escenas": [
            {
                "numero": 0,
                "titulo": "x",
                "duracion_estimada_segundos": 1.0,
                "bloques": ["hola"],
                "texto_locucion": "hola",
                "indicaciones_pantalla": [],
                "notas_internas": [],
            }
        ],
    }
    problemas = validar_tarjetas(datos)
    assert any("metadatos.para_terceros" in p for p in problemas)


def test_validar_tarjetas_detecta_numero_de_escenas_inconsistente() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    tarjetas = generar_tarjetas(resultado, tiempos)
    datos = tarjetas_a_diccionario(tarjetas)
    datos["metadatos"]["numero_escenas"] = 99
    problemas = validar_tarjetas(datos)
    assert any("numero_escenas" in p for p in problemas)


def test_validar_tarjetas_detecta_escena_totalmente_vacia() -> None:
    datos = {
        "version_contrato": 1,
        "metadatos": {
            "titulo": "x",
            "para_terceros": False,
            "numero_escenas": 1,
            "palabras_locucion_total": 0,
            "duracion_total_segundos": 0.0,
        },
        "escenas": [
            {
                "numero": 0,
                "titulo": "vacia",
                "duracion_estimada_segundos": 0.0,
                "bloques": [],
                "texto_locucion": "",
                "indicaciones_pantalla": [],
                "notas_internas": [],
            }
        ],
    }
    problemas = validar_tarjetas(datos)
    assert any("no tiene ni bloques" in p for p in problemas)


def test_guardar_tarjetas_json_escribe_en_carpeta_salida(tmp_path: Path) -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    tarjetas = generar_tarjetas(resultado, tiempos)
    destino = guardar_tarjetas_json(formatear_tarjetas_json(tarjetas), tmp_path)
    assert destino == tmp_path / NOMBRE_ARCHIVO_TARJETAS_JSON
    assert destino.exists()
    assert validar_tarjetas(json.loads(destino.read_text(encoding="utf-8"))) == []


# --- brief de invocacion ---------------------------------------------------------------


def test_generar_brief_describe_tantas_diapositivas_de_contenido_como_escenas() -> None:
    """Criterio de aceptacion literal de T-29."""
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    tarjetas = generar_tarjetas(resultado, tiempos)
    brief = generar_brief(tarjetas)
    assert brief.count("### Diapositiva") == len(tarjetas.tarjetas) == 2


def test_generar_brief_corrige_tipografia_y_relacion_de_aspecto() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    tarjetas = generar_tarjetas(resultado, tiempos)
    brief = generar_brief(tarjetas)
    assert "Poppins, no Figtree" in brief
    assert "668/376" in brief


def test_generar_brief_indice_solo_si_supera_el_umbral() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    tarjetas = generar_tarjetas(resultado, tiempos)
    configuracion_bajo_umbral = Configuracion(pptx_umbral_indice_secciones=5)
    brief_sin_indice = generar_brief(tarjetas, configuracion_bajo_umbral)
    assert "Sin diapositiva de índice" in brief_sin_indice

    configuracion_con_indice = Configuracion(pptx_umbral_indice_secciones=2)
    brief_con_indice = generar_brief(tarjetas, configuracion_con_indice)
    assert "**Índice (LIGHT).**" in brief_con_indice


def test_generar_brief_agrupa_escenas_por_diapositiva_segun_configuracion() -> None:
    configuracion = Configuracion(pptx_escenas_por_diapositiva=2)
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS, configuracion)
    tarjetas = generar_tarjetas(resultado, tiempos, configuracion=configuracion)
    brief = generar_brief(tarjetas, configuracion)
    # las dos escenas caben en una unica diapositiva de contenido
    assert brief.count("### Diapositiva") == 1
    assert "escena(s) 0, 1" in brief


def test_generar_brief_modo_para_terceros_lo_dice_explicitamente() -> None:
    configuracion = Configuracion(incluir_notas_internas=False)
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS, configuracion)
    tarjetas = generar_tarjetas(resultado, tiempos, configuracion=configuracion)
    brief = generar_brief(tarjetas, configuracion)
    assert "ENTREGABLE A TERCEROS" in brief
    assert "Se omiten las notas internas" in brief


def test_guardar_brief_escribe_en_carpeta_salida(tmp_path: Path) -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    tarjetas = generar_tarjetas(resultado, tiempos)
    destino = guardar_brief(generar_brief(tarjetas), tmp_path)
    assert destino == tmp_path / NOMBRE_ARCHIVO_BRIEF_PPTX
    assert destino.exists()


# --- deteccion de disponibilidad y punto de entrada -----------------------------------


def test_detectar_skill_pptx_disponible_falso_por_defecto() -> None:
    # En esta maquina (sesion de nube) no existen las carpetas de skill.
    assert detectar_skill_pptx_disponible() is False


def test_detectar_skill_pptx_disponible_true_si_las_dos_carpetas_existen(
    tmp_path: Path,
) -> None:
    marca = tmp_path / "480-branded-pptx"
    base = tmp_path / "pptx"
    marca.mkdir()
    base.mkdir()
    configuracion = Configuracion(
        ruta_skill_marca_pptx=str(marca), ruta_skill_pptx_base=str(base)
    )
    assert detectar_skill_pptx_disponible(configuracion) is True


def test_detectar_skill_pptx_disponible_false_si_falta_una_de_las_dos(
    tmp_path: Path,
) -> None:
    marca = tmp_path / "480-branded-pptx"
    marca.mkdir()
    configuracion = Configuracion(
        ruta_skill_marca_pptx=str(marca), ruta_skill_pptx_base=str(tmp_path / "no-existe")
    )
    assert detectar_skill_pptx_disponible(configuracion) is False


def test_exportar_pptx_nunca_falla_sin_skill_de_marca(tmp_path: Path) -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    resultado_pptx = exportar_pptx(resultado, tiempos, tmp_path, nombre_guion="prueba")
    assert isinstance(resultado_pptx, ResultadoPptx)
    assert resultado_pptx.skill_disponible is False
    assert "LATENTE" in resultado_pptx.mensaje
    assert resultado_pptx.ruta_tarjetas_json.exists()
    assert resultado_pptx.ruta_brief.exists()


def test_exportar_pptx_mensaje_positivo_con_skill_disponible(tmp_path: Path) -> None:
    marca = tmp_path / "480-branded-pptx"
    base = tmp_path / "pptx"
    marca.mkdir()
    base.mkdir()
    configuracion = Configuracion(
        ruta_skill_marca_pptx=str(marca), ruta_skill_pptx_base=str(base)
    )
    carpeta_salida = tmp_path / "salida"
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS, configuracion)
    resultado_pptx = exportar_pptx(
        resultado, tiempos, carpeta_salida, nombre_guion="prueba", configuracion=configuracion
    )
    assert resultado_pptx.skill_disponible is True
    assert "LATENTE" not in resultado_pptx.mensaje


# --- sobre los tres guiones reales -----------------------------------------------------


def test_exportar_pptx_sobre_guiones_reales(
    texto_guiones_reales: dict[str, str], tmp_path: Path
) -> None:
    for nombre, texto in texto_guiones_reales.items():
        resultado, tiempos = _pipeline(texto)
        resultado_pptx = exportar_pptx(
            resultado, tiempos, tmp_path / nombre, nombre_guion=nombre
        )
        datos = json.loads(resultado_pptx.ruta_tarjetas_json.read_text(encoding="utf-8"))
        assert validar_tarjetas(datos) == [], f"{nombre}: {validar_tarjetas(datos)}"
        assert datos["metadatos"]["numero_escenas"] == len(resultado.escenas)
        brief = resultado_pptx.ruta_brief.read_text(encoding="utf-8")
        assert brief.count("### Diapositiva") == len(resultado.escenas)
