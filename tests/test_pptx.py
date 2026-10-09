"""Tests del adaptador `.pptx` con identidad 480 (tarea T-29)."""

from __future__ import annotations

import json
import re
from pathlib import Path

from clasificador import clasificar_guion
from config import NOMBRE_ARCHIVO_BRIEF_PPTX, NOMBRE_ARCHIVO_TARJETAS_JSON, Configuracion
from convencion import detectar_desviaciones
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
from reproductor import generar_reproductor_html
from tiempos import ResultadoTiempos, calcular_tiempos

RAIZ = Path(__file__).resolve().parent.parent

_PATRON_DATOS_JSON_REPRODUCTOR = re.compile(
    r'<script type="application/json" id="datos-reproductor">(.*?)</script>', re.DOTALL
)

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


# --- desviaciones de la convencion (R-23) ---------------------------------------------

_GUION_CON_ESCENA_SIN_ROTULO = """# Guion de prueba

## BLOQUE 0 — Arranque (0:00 – 0:10)

**LOCUCIÓN**

> Esta es la primera frase del bloque.

## BLOQUE 1 — Sin rótulo (0:10 – 0:20)

Esto es locución sin marcar con ningún rótulo, solo texto suelto.
"""


def test_generar_tarjetas_sin_desviaciones_lista_vacia() -> None:
    """Criterio de aceptacion de R-23: sin desviaciones conocidas,
    `desviaciones_convencion` sale `[]` -- caso de los tres guiones reales."""
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    tarjetas = generar_tarjetas(resultado, tiempos)
    assert tarjetas.desviaciones_convencion == ()


def test_generar_tarjetas_con_desviacion_expone_la_misma_descripcion() -> None:
    """R-23, requisito 3: `desviaciones_convencion` reutiliza tal cual las
    descripciones de `convencion.detectar_desviaciones` sobre el MISMO
    `resultado`/`clasificacion` que ya recibe el resto de la tarjeta -- ningun
    parseo ni clasificacion nuevos, ningun texto reformateado."""
    configuracion = Configuracion()
    resultado, tiempos = _pipeline(_GUION_CON_ESCENA_SIN_ROTULO, configuracion)
    clasificacion = clasificar_guion(resultado, configuracion)
    esperadas = tuple(
        d.descripcion for d in detectar_desviaciones(resultado, clasificacion, configuracion)
    )
    assert esperadas != ()

    tarjetas = generar_tarjetas(resultado, tiempos, configuracion=configuracion)
    assert tarjetas.desviaciones_convencion == esperadas


def test_generar_tarjetas_modo_para_terceros_omite_desviaciones_convencion() -> None:
    """R-23, requisito 4: `--para-terceros` excluye `desviaciones_convencion`
    del contrato, igual que ya excluye `notas_internas` -- son avisos para el
    dueño y la cadena de montaje, no contenido para un tercero."""
    configuracion = Configuracion(incluir_notas_internas=False)
    resultado, tiempos = _pipeline(_GUION_CON_ESCENA_SIN_ROTULO, configuracion)
    tarjetas = generar_tarjetas(resultado, tiempos, configuracion=configuracion)
    assert tarjetas.para_terceros is True
    assert tarjetas.desviaciones_convencion == ()


# --- diccionario del dueño aplicado (R-26) -------------------------------------------


def test_generar_tarjetas_entradas_diccionario_aplicadas_por_defecto_cero() -> None:
    """Sin pasar nada nuevo (R-26), el comportamiento es identico al de antes
    de la tarea: `0`, ningun cambio para el selector automatico de T-30, que
    no conoce ninguna `Reescritura`."""
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    tarjetas = generar_tarjetas(resultado, tiempos)
    assert tarjetas.entradas_diccionario_aplicadas == 0


def test_generar_tarjetas_entradas_diccionario_aplicadas_se_pasa_tal_cual() -> None:
    """R-26, requisito 1: el recuento que ya calcula quien genera
    `guion-escenas.md` se expone tal cual en `tarjetas.json`, sin que
    `generar_tarjetas` lo recalcule ni conozca las `Reescritura`."""
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    tarjetas = generar_tarjetas(resultado, tiempos, entradas_diccionario_aplicadas=3)
    assert tarjetas.entradas_diccionario_aplicadas == 3


# --- duracion real por escena (R-13) --------------------------------------------------


def test_generar_tarjetas_sin_tomas_duracion_real_es_none_para_todas() -> None:
    """Sin `tomas_por_escena` (el caso del selector automatico de T-30), el
    comportamiento es identico al de antes de R-13: ninguna escena trae
    duracion real y no hay mezcla que senalar."""
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    tarjetas = generar_tarjetas(resultado, tiempos)
    assert all(t.duracion_real_segundos is None for t in tarjetas.tarjetas)
    assert tarjetas.mezcla_duracion_real_y_estimada is False


def test_generar_tarjetas_con_toma_buena_incluye_duracion_real() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    tomas_por_escena = {
        "0": {"tomas": [{"numero": 1, "duracion_segundos": 12.5, "nota": "", "buena": True}]},
    }
    tarjetas = generar_tarjetas(resultado, tiempos, tomas_por_escena=tomas_por_escena)
    escena_0 = next(t for t in tarjetas.tarjetas if t.numero == 0)
    escena_1 = next(t for t in tarjetas.tarjetas if t.numero == 1)
    assert escena_0.duracion_real_segundos == 12.5
    assert escena_1.duracion_real_segundos is None
    # duracion_estimada_segundos nunca se sustituye (requisito 2 de R-13).
    assert escena_0.duracion_estimada_segundos != 12.5


def test_generar_tarjetas_mezcla_duracion_real_y_estimada_solo_si_hay_ambas() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)

    # Ninguna escena con toma buena: sin mezcla.
    sin_tomas = generar_tarjetas(resultado, tiempos)
    assert sin_tomas.mezcla_duracion_real_y_estimada is False

    # Solo una de las dos escenas con toma buena: mezcla.
    mezclada = generar_tarjetas(
        resultado,
        tiempos,
        tomas_por_escena={
            "0": {"tomas": [{"numero": 1, "duracion_segundos": 9.0, "nota": "", "buena": True}]}
        },
    )
    assert mezclada.mezcla_duracion_real_y_estimada is True

    # Las dos escenas con toma buena: sin mezcla (todas reales).
    todas_reales = generar_tarjetas(
        resultado,
        tiempos,
        tomas_por_escena={
            "0": {"tomas": [{"numero": 1, "duracion_segundos": 9.0, "nota": "", "buena": True}]},
            "1": {"tomas": [{"numero": 1, "duracion_segundos": 11.0, "nota": "", "buena": True}]},
        },
    )
    assert todas_reales.mezcla_duracion_real_y_estimada is False


def test_generar_tarjetas_toma_buena_duracion_no_positiva_se_ignora() -> None:
    """Dato degenerado (duracion 0 o negativa): se trata igual que "sin toma
    buena todavia", nunca como una duracion real de cero segundos."""
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    tarjetas = generar_tarjetas(
        resultado,
        tiempos,
        tomas_por_escena={
            "0": {"tomas": [{"numero": 1, "duracion_segundos": 0.0, "nota": "", "buena": True}]}
        },
    )
    escena_0 = next(t for t in tarjetas.tarjetas if t.numero == 0)
    assert escena_0.duracion_real_segundos is None
    assert tarjetas.mezcla_duracion_real_y_estimada is False


# --- limites absolutos de escena (R-16) ------------------------------------------------


def test_generar_tarjetas_limites_absolutos_sin_toma_buena_acumulan_estimada() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    tarjetas = generar_tarjetas(resultado, tiempos)
    escena_0 = next(t for t in tarjetas.tarjetas if t.numero == 0)
    escena_1 = next(t for t in tarjetas.tarjetas if t.numero == 1)
    assert escena_0.inicio_segundos == 0.0
    assert escena_0.fin_segundos == escena_0.duracion_estimada_segundos
    # Sin hueco ni solape: el fin de una escena es el inicio de la siguiente.
    assert escena_1.inicio_segundos == escena_0.fin_segundos
    assert escena_1.fin_segundos == escena_1.inicio_segundos + escena_1.duracion_estimada_segundos


def test_generar_tarjetas_limites_absolutos_usan_duracion_real_cuando_existe() -> None:
    """Requisito 1 de R-16: la acumulacion usa `duracion_real_segundos`
    cuando la escena tiene toma buena, en vez de `duracion_estimada_
    segundos` -- misma regla que ya elige `mezcla_duracion_real_y_estimada`
    (R-13), no una segunda implementacion."""
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    tomas_por_escena = {
        "0": {"tomas": [{"numero": 1, "duracion_segundos": 12.5, "nota": "", "buena": True}]},
    }
    tarjetas = generar_tarjetas(resultado, tiempos, tomas_por_escena=tomas_por_escena)
    escena_0 = next(t for t in tarjetas.tarjetas if t.numero == 0)
    escena_1 = next(t for t in tarjetas.tarjetas if t.numero == 1)
    assert escena_0.duracion_real_segundos == 12.5
    assert escena_0.fin_segundos == 12.5
    assert escena_1.inicio_segundos == 12.5


# --- indicaciones ancladas a un instante estimado (R-20) -------------------------------


def test_generar_tarjetas_indicaciones_ancladas_mismo_conjunto_que_pantalla_y_notas() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    tarjetas = generar_tarjetas(resultado, tiempos)
    for tarjeta in tarjetas.tarjetas:
        assert len(tarjeta.indicaciones_ancladas) == len(tarjeta.indicaciones_pantalla) + len(
            tarjeta.notas_internas
        )
    primera = tarjetas.tarjetas[0]
    textos_ancladas = {i.texto for i in primera.indicaciones_ancladas}
    assert textos_ancladas == set(primera.indicaciones_pantalla) | set(primera.notas_internas)
    notas_ancladas = {i.texto for i in primera.indicaciones_ancladas if i.es_nota_interna}
    assert notas_ancladas == set(primera.notas_internas)


def test_generar_tarjetas_indicaciones_ancladas_para_terceros_omite_notas_internas() -> None:
    configuracion = Configuracion(incluir_notas_internas=False)
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS, configuracion)
    tarjetas = generar_tarjetas(resultado, tiempos, configuracion=configuracion)
    primera = tarjetas.tarjetas[0]
    assert all(not indicacion.es_nota_interna for indicacion in primera.indicaciones_ancladas)
    assert len(primera.indicaciones_ancladas) == len(primera.indicaciones_pantalla)


def test_generar_tarjetas_indicaciones_ancladas_escena_sin_bloques_se_ancla_al_inicio() -> None:
    """Caso sin ejemplo en los guiones reales (siempre llevan LOCUCION
    primero), pero valido en la convencion -- `validar_tarjetas` ya lo
    contempla (una escena sin bloques pero con indicaciones no esta vacia).
    Sin ningun bloque al que anclar, la indicacion se ancla al inicio de la
    escena en vez de perderse (invariante (a) extendido)."""
    guion = """# Guion

## BLOQUE 0 — Solo pantalla (0:00 – 0:05)

**EN PANTALLA**

Logotipo de apertura sin ninguna locución en esta escena.

## BLOQUE 1 — Cierre (0:05 – 0:10)

**LOCUCIÓN**

> Frase de cierre.
"""
    resultado, tiempos = _pipeline(guion)
    tarjetas = generar_tarjetas(resultado, tiempos)
    escena_0 = next(t for t in tarjetas.tarjetas if t.numero == 0)
    assert escena_0.bloques == ()
    assert len(escena_0.indicaciones_ancladas) == 1
    assert escena_0.indicaciones_ancladas[0].instante_estimado_segundos == escena_0.inicio_segundos


def test_generar_tarjetas_indicaciones_ancladas_coincide_con_la_cue_del_reproductor() -> None:
    """Criterio de aceptacion de R-20: el bloque ancla de una indicacion
    conocida es el mismo que ya calcula R-12 para la cue en vivo del
    reproductor -- mismo guion, mismo anclaje, dos consumidores. Sin ninguna
    toma real de por medio, el acumulado absoluto de `tarjetas.json` (R-16)
    coincide con el acumulado de T-12 que ya usa el reproductor, asi que los
    dos instantes deben ser identicos, no solo compatibles."""
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    tarjetas = generar_tarjetas(resultado, tiempos, nombre_guion="guion")
    pagina = generar_reproductor_html(resultado, tiempos, nombre_guion="guion")
    coincidencia = _PATRON_DATOS_JSON_REPRODUCTOR.search(pagina)
    assert coincidencia is not None
    datos_reproductor = json.loads(coincidencia.group(1))

    texto_indicacion = "Título del vídeo en pantalla."
    bloque_ancla = next(
        bloque
        for bloque in datos_reproductor["escenas"][0]["bloques"]
        if any(texto_indicacion in indicacion for indicacion in bloque["indicaciones"])
    )
    indicacion_anclada = next(
        i for i in tarjetas.tarjetas[0].indicaciones_ancladas if i.texto == texto_indicacion
    )
    assert indicacion_anclada.instante_estimado_segundos == bloque_ancla["inicio_segundos"]


def test_generar_tarjetas_indicaciones_ancladas_instante_dentro_del_rango_de_la_escena(
    texto_guiones_reales: dict[str, str],
) -> None:
    for nombre, texto in texto_guiones_reales.items():
        resultado, tiempos = _pipeline(texto)
        tarjetas = generar_tarjetas(resultado, tiempos)
        for tarjeta in tarjetas.tarjetas:
            for indicacion in tarjeta.indicaciones_ancladas:
                assert (
                    tarjeta.inicio_segundos
                    <= indicacion.instante_estimado_segundos
                    <= tarjeta.fin_segundos
                ), f"{nombre}, escena {tarjeta.numero}: {indicacion}"


def test_generar_tarjetas_indicaciones_ancladas_no_se_pierden_en_los_guiones_reales(
    texto_guiones_reales: dict[str, str],
) -> None:
    for nombre, texto in texto_guiones_reales.items():
        resultado, tiempos = _pipeline(texto)
        tarjetas = generar_tarjetas(resultado, tiempos)
        for tarjeta in tarjetas.tarjetas:
            assert len(tarjeta.indicaciones_ancladas) == len(
                tarjeta.indicaciones_pantalla
            ) + len(tarjeta.notas_internas), f"{nombre}, escena {tarjeta.numero}"


# --- serializacion y validacion del contrato -----------------------------------------


def test_tarjetas_a_diccionario_produce_json_valido_segun_el_contrato() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    tarjetas = generar_tarjetas(resultado, tiempos, nombre_guion="prueba")
    datos = tarjetas_a_diccionario(tarjetas)
    assert validar_tarjetas(datos) == []
    assert datos["metadatos"]["numero_escenas"] == 2
    assert datos["metadatos"]["titulo"] == "prueba"


def test_tarjetas_a_diccionario_incluye_duracion_real_y_aviso_de_mezcla() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    tarjetas = generar_tarjetas(
        resultado,
        tiempos,
        tomas_por_escena={
            "0": {"tomas": [{"numero": 1, "duracion_segundos": 9.0, "nota": "", "buena": True}]}
        },
    )
    datos = tarjetas_a_diccionario(tarjetas)
    assert validar_tarjetas(datos) == []
    assert datos["metadatos"]["mezcla_duracion_real_y_estimada"] is True
    escena_0 = next(e for e in datos["escenas"] if e["numero"] == 0)
    escena_1 = next(e for e in datos["escenas"] if e["numero"] == 1)
    assert escena_0["duracion_real_segundos"] == 9.0
    assert escena_1["duracion_real_segundos"] is None
    # inicio_segundos/fin_segundos (R-16) tambien pasan por el serializador.
    assert escena_0["inicio_segundos"] == 0.0
    assert escena_0["fin_segundos"] == 9.0
    assert escena_1["inicio_segundos"] == 9.0


def test_tarjetas_a_diccionario_incluye_desviaciones_convencion() -> None:
    configuracion = Configuracion()
    resultado, tiempos = _pipeline(_GUION_CON_ESCENA_SIN_ROTULO, configuracion)
    tarjetas = generar_tarjetas(resultado, tiempos, configuracion=configuracion)
    datos = tarjetas_a_diccionario(tarjetas)
    assert validar_tarjetas(datos) == []
    assert datos["metadatos"]["desviaciones_convencion"] == list(tarjetas.desviaciones_convencion)
    assert datos["metadatos"]["desviaciones_convencion"] != []


def test_tarjetas_a_diccionario_incluye_entradas_diccionario_aplicadas() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    tarjetas = generar_tarjetas(resultado, tiempos, entradas_diccionario_aplicadas=2)
    datos = tarjetas_a_diccionario(tarjetas)
    assert validar_tarjetas(datos) == []
    assert datos["metadatos"]["entradas_diccionario_aplicadas"] == 2


def test_tarjetas_a_diccionario_incluye_indicaciones_ancladas() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    tarjetas = generar_tarjetas(resultado, tiempos)
    datos = tarjetas_a_diccionario(tarjetas)
    assert validar_tarjetas(datos) == []
    escena_0 = next(e for e in datos["escenas"] if e["numero"] == 0)
    assert escena_0["indicaciones_ancladas"] == [
        {
            "texto": "Título del vídeo en pantalla.",
            "es_nota_interna": False,
            "instante_estimado_segundos": escena_0["indicaciones_ancladas"][0][
                "instante_estimado_segundos"
            ],
        },
        {
            "texto": "Recordatorio interno: no mencionar el precio antiguo en la locución.",
            "es_nota_interna": True,
            "instante_estimado_segundos": escena_0["indicaciones_ancladas"][1][
                "instante_estimado_segundos"
            ],
        },
    ]
    # Ambas indicaciones de esta escena se anclan al mismo (unico) bloque.
    assert (
        escena_0["indicaciones_ancladas"][0]["instante_estimado_segundos"]
        == escena_0["indicaciones_ancladas"][1]["instante_estimado_segundos"]
    )


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
    configuracion = Configuracion(ruta_skill_marca_pptx=str(marca), ruta_skill_pptx_base=str(base))
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
    configuracion = Configuracion(ruta_skill_marca_pptx=str(marca), ruta_skill_pptx_base=str(base))
    carpeta_salida = tmp_path / "salida"
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS, configuracion)
    resultado_pptx = exportar_pptx(
        resultado, tiempos, carpeta_salida, nombre_guion="prueba", configuracion=configuracion
    )
    assert resultado_pptx.skill_disponible is True
    assert "LATENTE" not in resultado_pptx.mensaje


def test_exportar_pptx_entradas_diccionario_aplicadas_llega_a_tarjetas_json(
    tmp_path: Path,
) -> None:
    """R-26: el mismo recuento que ya ve `guion-escenas.md` llega hasta
    `tarjetas.json.metadatos` a traves de `exportar_pptx`, sin recalcularse."""
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)
    resultado_pptx = exportar_pptx(
        resultado,
        tiempos,
        tmp_path,
        nombre_guion="prueba",
        entradas_diccionario_aplicadas=4,
    )
    datos = json.loads(resultado_pptx.ruta_tarjetas_json.read_text(encoding="utf-8"))
    assert datos["metadatos"]["entradas_diccionario_aplicadas"] == 4


# --- sobre los tres guiones reales -----------------------------------------------------


def test_exportar_pptx_sobre_guiones_reales(
    texto_guiones_reales: dict[str, str], tmp_path: Path
) -> None:
    for nombre, texto in texto_guiones_reales.items():
        resultado, tiempos = _pipeline(texto)
        resultado_pptx = exportar_pptx(resultado, tiempos, tmp_path / nombre, nombre_guion=nombre)
        datos = json.loads(resultado_pptx.ruta_tarjetas_json.read_text(encoding="utf-8"))
        assert validar_tarjetas(datos) == [], f"{nombre}: {validar_tarjetas(datos)}"
        assert datos["metadatos"]["numero_escenas"] == len(resultado.escenas)
        brief = resultado_pptx.ruta_brief.read_text(encoding="utf-8")
        assert brief.count("### Diapositiva") == len(resultado.escenas)


def test_tarjetas_json_ninguna_indicacion_termina_en_separador_de_escena(
    texto_guiones_reales: dict[str, str], tmp_path: Path
) -> None:
    """R-14: el separador `---` de fin de escena no debe colarse pegado al
    texto de una indicacion de pantalla o nota en `tarjetas.json`, verificado
    sobre los tres guiones reales (criterio de aceptacion de R-14)."""
    for nombre, texto in texto_guiones_reales.items():
        resultado, tiempos = _pipeline(texto)
        resultado_pptx = exportar_pptx(resultado, tiempos, tmp_path / nombre, nombre_guion=nombre)
        datos = json.loads(resultado_pptx.ruta_tarjetas_json.read_text(encoding="utf-8"))
        for tarjeta in datos["escenas"]:
            for indicacion in tarjeta["indicaciones_pantalla"] + tarjeta["notas_internas"]:
                assert not indicacion.rstrip().endswith("---"), (
                    f"{nombre}: indicacion con separador de escena colado: {indicacion!r}"
                )
