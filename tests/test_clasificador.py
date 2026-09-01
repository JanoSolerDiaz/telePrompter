"""Tests del clasificador locucion / no locucion (tarea T-09).

`test_ruta_rapida_clasifica_correctamente_los_guiones_reales` y
`test_reconstruccion_no_pierde_nada_del_guion_real` reemplazan a los talones del
mismo nombre en `tests/test_logica_pendiente.py` (T-03), que quedaban pendientes
hasta que T-09 existiera: son su criterio de aceptacion literal, no una nota
aparte.
"""

from __future__ import annotations

import re

from clasificador import (
    TIPO_LOCUCION,
    TIPO_NO_LOCUCION,
    TIPO_REVISAR,
    clasificar_escena,
    clasificar_guion,
    reconstruir,
)
from config import ROTULO_LOCUCION, ROTULOS_NO_LOCUCION, Configuracion
from parser import Escena, parsear_guion

# --- Criterio de aceptacion sobre los tres guiones reales -------------------------


def test_ruta_rapida_clasifica_correctamente_los_guiones_reales(
    texto_guiones_reales: dict[str, str],
) -> None:
    """Ruta rapida (rotulo): 100% correcta. Ningun texto de LOCUCIÓN se pierde,
    ninguna linea de EN PANTALLA/NOTA se cuela como locucion, 0 bloques sin
    clasificar (todo bloque tiene un `tipo` de los tres validos)."""
    for nombre, texto in texto_guiones_reales.items():
        resultado = parsear_guion(texto)
        clasificacion = clasificar_guion(resultado)

        for bloque in clasificacion.bloques:
            assert bloque.tipo in (TIPO_LOCUCION, TIPO_NO_LOCUCION, TIPO_REVISAR), (
                f"{nombre}: bloque sin clasificar en linea {bloque.linea_inicio}"
            )

        for escena in resultado.escenas:
            lineas_escena = texto.splitlines()[escena.linea_inicio - 1 : escena.linea_fin]
            texto_escena = "\n".join(lineas_escena)
            bloques_escena = clasificar_escena(escena)

            # Ninguna linea de cita de bloque bajo **LOCUCIÓN** se pierde: toda
            # linea que empieza por "> " dentro de la escena aparece integra en
            # algun bloque de tipo locucion.
            lineas_cita_originales = [
                linea for linea in texto_escena.splitlines() if linea.strip().startswith(">")
            ]
            lineas_cita_clasificadas = [
                linea
                for bloque in bloques_escena
                if bloque.tipo == TIPO_LOCUCION
                for linea in bloque.contenido.splitlines()
                if linea.strip().startswith(">")
            ]
            assert sorted(lineas_cita_originales) == sorted(lineas_cita_clasificadas), (
                f"{nombre}, escena {escena.numero}: se perdio texto de **LOCUCIÓN**"
            )

            # Ninguna linea de las secciones EN PANTALLA / NOTA aparece en un
            # bloque de tipo locucion.
            for bloque in bloques_escena:
                if bloque.senal == "rotulo_no_locucion":
                    assert bloque.tipo == TIPO_NO_LOCUCION


def test_reconstruccion_no_pierde_nada_del_guion_real(
    texto_guiones_reales: dict[str, str],
) -> None:
    """Invariante (a) de §0.2: la union de todos los bloques clasificados (en
    todo el documento: preambulo, secciones auxiliares y escenas) reconstruye
    el `.md` de origen sin perdida."""
    for texto in texto_guiones_reales.values():
        resultado = parsear_guion(texto)
        clasificacion = clasificar_guion(resultado)
        assert reconstruir(clasificacion.bloques) == "\n".join(texto.splitlines())


def test_resumen_por_escena_cuadra_con_los_bloques(
    texto_guiones_reales: dict[str, str],
) -> None:
    """Requisito 7: el resumen por escena (palabras excluidas y por que) es
    consistente con los propios bloques que lo generan."""
    for texto in texto_guiones_reales.values():
        resultado = parsear_guion(texto)
        clasificacion = clasificar_guion(resultado)
        assert len(clasificacion.resumenes) == len(resultado.escenas)
        for resumen in clasificacion.resumenes:
            suma = resumen.palabras_locucion + resumen.palabras_excluidas
            assert suma == resumen.palabras_totales
            assert resumen.palabras_locucion > 0, (
                f"escena {resumen.numero} no tiene nada de locucion detectada"
            )
            assert sum(resumen.motivos_exclusion.values()) == resumen.palabras_excluidas


# --- Requisito 3: texto suelto dentro de una seccion **LOCUCIÓN** -----------------


def test_texto_suelto_en_locucion_se_marca_revisar() -> None:
    escena = Escena(
        numero=0,
        titulo="BLOQUE 0 — Prueba (0:00 – 0:10)",
        contenido=(
            "## BLOQUE 0 — Prueba (0:00 – 0:10)\n"
            "\n"
            "**LOCUCIÓN**\n"
            "> Primera frase citada.\n"
            "\n"
            "*(una acotacion suelta, fuera de cita)*\n"
            "\n"
            "> Segunda frase citada.\n"
            "\n"
            "**EN PANTALLA**\n"
            "Descripcion de plano.\n"
        ),
        linea_inicio=10,
        linea_fin=20,
    )
    bloques = clasificar_escena(escena)

    revisar = [b for b in bloques if b.tipo == TIPO_REVISAR]
    assert len(revisar) == 1
    assert "acotacion" in revisar[0].contenido
    assert "texto suelto" in revisar[0].motivo

    citas = [b for b in bloques if b.tipo == TIPO_LOCUCION]
    assert len(citas) == 2
    assert "Primera frase" in citas[0].contenido
    assert "Segunda frase" in citas[1].contenido

    pantalla = [b for b in bloques if b.senal == "rotulo_no_locucion"]
    assert len(pantalla) == 1
    assert pantalla[0].tipo == TIPO_NO_LOCUCION

    # cobertura total de la escena (mismo criterio que T-08: reconstruir con
    # `.split("\n")`, el inverso exacto del `"\n".join` con el que se construyo
    # `escena.contenido`; `.splitlines()` perderia una linea en blanco final)
    assert reconstruir(bloques) == "\n".join(escena.contenido.split("\n"))


def test_configuracion_de_rotulos_es_sobreescribible() -> None:
    """Requisito 1: rotulos configurables, no fijados a fuego en el codigo."""
    escena = Escena(
        numero=0,
        titulo="BLOQUE 0",
        contenido=(
            "## BLOQUE 0\n"
            "\n"
            "**VOZ**\n"
            "> Texto citado.\n"
            "\n"
            "**PANTALLA**\n"
            "Otra cosa.\n"
        ),
        linea_inicio=1,
        linea_fin=7,
    )
    configuracion_personalizada = Configuracion(
        rotulo_locucion="**VOZ**", rotulos_no_locucion=("**PANTALLA**",)
    )
    bloques = clasificar_escena(escena, configuracion_personalizada)
    locucion = [b for b in bloques if b.tipo == TIPO_LOCUCION]
    assert len(locucion) == 1
    assert "Texto citado" in locucion[0].contenido


# --- Requisito 2: inferencia de respaldo sin rotulos ------------------------------


def _texto_sin_rotulos(texto: str) -> str:
    """Sustituye cada linea de rotulo por una linea en blanco (misma cuenta de
    lineas, mismas posiciones) para simular un guion sin la convencion de
    rotulos, sin desplazar la numeracion de lineas del resto del documento."""
    rotulos = {ROTULO_LOCUCION, *ROTULOS_NO_LOCUCION}
    lineas = [("" if linea.strip() in rotulos else linea) for linea in texto.splitlines()]
    return "\n".join(lineas)


def test_inferencia_sin_rotulos_alcanza_precision_minima_en_locucion(
    texto_guiones_reales: dict[str, str],
) -> None:
    """Criterio de aceptacion de T-09: con los guiones reales despojados de sus
    rotulos, la inferencia alcanza >=95% de precision en bloques de locucion
    (de las PALABRAS que la inferencia marca como locucion, al menos el 95% lo
    son de verdad segun la clasificacion por rotulo del guion original).

    Medido en palabras, no en lineas: una linea en blanco no aporta ninguna
    palabra recitable, asi que a que lado de un limite de parrafo caiga una
    linea vacia no debe contar ni a favor ni en contra de la precision."""
    for nombre, texto in texto_guiones_reales.items():
        resultado_original = parsear_guion(texto)
        clasificacion_original = clasificar_guion(resultado_original)
        lineas_locucion_reales: set[int] = set()
        for bloque in clasificacion_original.bloques:
            if bloque.tipo == TIPO_LOCUCION:
                lineas_locucion_reales.update(range(bloque.linea_inicio, bloque.linea_fin + 1))

        texto_despojado = _texto_sin_rotulos(texto)
        resultado_inferido = parsear_guion(texto_despojado, separador=resultado_original.separador)
        clasificacion_inferida = clasificar_guion(resultado_inferido)

        palabras_totales = 0
        palabras_correctas = 0
        for bloque in clasificacion_inferida.bloques:
            if bloque.tipo != TIPO_LOCUCION:
                continue
            for indice, linea in enumerate(bloque.contenido.split("\n")):
                n_palabras = len(linea.split())
                if n_palabras == 0:
                    continue
                palabras_totales += n_palabras
                if (bloque.linea_inicio + indice) in lineas_locucion_reales:
                    palabras_correctas += n_palabras

        assert palabras_totales, f"{nombre}: la inferencia no detecto nada de locucion"
        precision = palabras_correctas / palabras_totales
        assert precision >= 0.95, f"{nombre}: precision de inferencia {precision:.2%} < 95%"


def test_inferencia_reconoce_marca_de_tiempo_como_no_locucion() -> None:
    escena = Escena(
        numero=0,
        titulo="BLOQUE 0",
        contenido=("## BLOQUE 0\n" "\n" "00:12 corte a plano general\n"),
        linea_inicio=1,
        linea_fin=3,
    )
    bloques = clasificar_escena(escena)
    cuerpo = [b for b in bloques if b.senal != "encabezado"]
    assert len(cuerpo) == 1
    assert cuerpo[0].tipo == TIPO_NO_LOCUCION
    assert cuerpo[0].senal == "timestamp"


def test_inferencia_reconoce_prefijo_pantalla_como_no_locucion() -> None:
    escena = Escena(
        numero=0,
        titulo="BLOQUE 0",
        contenido=("## BLOQUE 0\n" "\n" "PANTALLA: recorrido de menus.\n"),
        linea_inicio=1,
        linea_fin=3,
    )
    bloques = clasificar_escena(escena)
    cuerpo = [b for b in bloques if b.senal != "encabezado"]
    assert cuerpo[0].tipo == TIPO_NO_LOCUCION
    assert cuerpo[0].senal == "prefijo"


def test_inferencia_sin_senal_clara_se_marca_revisar() -> None:
    escena = Escena(
        numero=0,
        titulo="BLOQUE 0",
        contenido=("## BLOQUE 0\n" "\n" "Un parrafo cualquiera sin ninguna senal reconocible.\n"),
        linea_inicio=1,
        linea_fin=3,
    )
    bloques = clasificar_escena(escena)
    cuerpo = [b for b in bloques if b.senal != "encabezado"]
    assert cuerpo[0].tipo == TIPO_REVISAR
    assert cuerpo[0].senal == "sin_senal"


def test_clasificar_escena_vacia_no_falla() -> None:
    escena_vacia = Escena(numero=0, titulo="", contenido="", linea_inicio=1, linea_fin=1)
    assert clasificar_escena(escena_vacia) == []

    escena = Escena(numero=0, titulo="X", contenido="## X", linea_inicio=1, linea_fin=1)
    bloques = clasificar_escena(escena)
    assert len(bloques) == 1
    assert bloques[0].tipo == TIPO_NO_LOCUCION


def test_patron_encabezado_no_interfiere_con_rotulos(texto_guiones_reales: dict[str, str]) -> None:
    """Sanity check: el patron de escena sigue vivo (regresion de T-08)."""
    patron = re.compile(r"^##\s+BLOQUE", re.MULTILINE)
    for texto in texto_guiones_reales.values():
        assert patron.search(texto)
