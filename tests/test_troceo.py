"""Tests del troceo en bloques de respiracion (tarea T-11).

`test_troceo_respeta_el_rango_de_palabras_configurado` reemplaza al talon del
mismo nombre en `tests/test_logica_pendiente.py` (T-03): es su criterio de
aceptacion literal, no una nota aparte.
"""

from __future__ import annotations

import re

from clasificador import TIPO_LOCUCION, BloqueClasificado, clasificar_guion
from config import Configuracion
from parser import parsear_guion
from troceo import (
    BloqueRespiracion,
    trocear_bloque_locucion,
    trocear_guion,
    trocear_texto,
)

# --- Criterio de aceptacion sobre los tres guiones reales -------------------------


def test_troceo_respeta_el_rango_de_palabras_configurado(
    texto_guiones_reales: dict[str, str],
) -> None:
    """Cada bloque de respiracion queda entre `palabras_por_bloque_min` y
    `palabras_por_bloque_max` (config.py), salvo que la locucion completa sea mas
    corta. Criterio de aceptacion de T-11: >=90% de los bloques en rango."""
    configuracion = Configuracion()
    dentro_de_rango = 0
    total = 0
    for texto in texto_guiones_reales.values():
        resultado = parsear_guion(texto)
        bloques = trocear_guion(resultado, configuracion)
        assert bloques, "un guion real no puede producir cero bloques de respiracion"
        for bloque in bloques:
            total += 1
            if (
                configuracion.palabras_por_bloque_min
                <= bloque.num_palabras
                <= configuracion.palabras_por_bloque_max
            ):
                dentro_de_rango += 1

    assert total > 0
    proporcion = dentro_de_rango / total
    assert proporcion >= 0.90, (
        f"solo {proporcion:.0%} de los bloques de respiracion caen en el rango "
        f"[{configuracion.palabras_por_bloque_min}, {configuracion.palabras_por_bloque_max}]"
    )


def test_troceo_es_determinista_en_los_guiones_reales(
    texto_guiones_reales: dict[str, str],
) -> None:
    """Misma entrada, mismo troceo, dos veces seguidas (requisito 5)."""
    for texto in texto_guiones_reales.values():
        resultado = parsear_guion(texto)
        primera = trocear_guion(resultado)
        segunda = trocear_guion(resultado)
        assert [(b.texto, b.corte_forzado) for b in primera] == [
            (b.texto, b.corte_forzado) for b in segunda
        ]


_MARCA_CITA = re.compile(r"^>\s?")


def _palabras_locucion_sin_marca_de_cita(bloque: BloqueClasificado) -> int:
    """Cuenta palabras del bloque `locucion` quitando la marca `> ` de cada
    linea antes de partir por espacios: `bloque.contenido.split()` contaria el
    propio `>` como una palabra mas, que es sintaxis Markdown, no locucion."""
    return sum(len(_MARCA_CITA.sub("", linea).split()) for linea in bloque.contenido.split("\n"))


def test_todo_el_texto_locucion_aparece_troceado(texto_guiones_reales: dict[str, str]) -> None:
    """El troceo no pierde palabras: la union de todos los bloques de
    respiracion de una escena contiene las mismas palabras que sus bloques
    `locucion` ya clasificados (variante de la invariante (a) de §0.2,
    aplicada a la unidad de resaltado en vez de al bloque clasificado)."""
    for texto in texto_guiones_reales.values():
        resultado = parsear_guion(texto)
        clasificacion = clasificar_guion(resultado)
        palabras_locucion = sum(
            _palabras_locucion_sin_marca_de_cita(bloque)
            for bloque in clasificacion.bloques
            if bloque.tipo == TIPO_LOCUCION
        )
        bloques_respiracion = trocear_guion(resultado)
        palabras_respiracion = sum(bloque.num_palabras for bloque in bloques_respiracion)
        assert palabras_respiracion == palabras_locucion


# --- Unidad: `trocear_texto` sobre texto sintetico --------------------------------


def test_texto_corto_no_se_trocea() -> None:
    """Una locucion mas corta que el minimo se queda en un unico bloque, sin
    forzar nada ni intentar fundir con un vecino que no existe."""
    configuracion = Configuracion(palabras_por_bloque_min=6, palabras_por_bloque_max=12)
    fragmentos = trocear_texto("Hola, esto es corto.", configuracion)
    assert fragmentos == [("Hola, esto es corto.", False)]


def test_corta_por_puntuacion_fuerte_antes_que_por_nexos() -> None:
    """Dos oraciones cortas separadas por punto no se funden en un solo bloque
    aunque el resultado quepa entero por debajo del maximo: el punto ya basta
    para separarlas, no hace falta bajar a la prioridad de nexos."""
    configuracion = Configuracion(
        palabras_por_bloque_min=2, palabras_por_bloque_objetivo=4, palabras_por_bloque_max=6
    )
    fragmentos = trocear_texto("Esto es una oracion. Y esto es otra oracion.", configuracion)
    assert [texto for texto, _forzado in fragmentos] == [
        "Esto es una oracion.",
        "Y esto es otra oracion.",
    ]
    assert all(not forzado for _texto, forzado in fragmentos)


def test_subdivide_por_puntuacion_debil_cuando_la_oracion_no_cabe() -> None:
    configuracion = Configuracion(
        palabras_por_bloque_min=2, palabras_por_bloque_objetivo=5, palabras_por_bloque_max=6
    )
    texto = "Primero pon el agua a hervir, despues anade la sal y remueve bien."
    fragmentos = trocear_texto(texto, configuracion)
    assert len(fragmentos) > 1
    for texto_fragmento, _forzado in fragmentos:
        assert len(texto_fragmento.split()) <= configuracion.palabras_por_bloque_max


def test_fusiona_bloques_por_debajo_del_minimo_con_el_vecino_mas_afin() -> None:
    configuracion = Configuracion(
        palabras_por_bloque_min=4, palabras_por_bloque_objetivo=6, palabras_por_bloque_max=8
    )
    texto = "Una frase larga que ocupa bastantes palabras en total. Ya."
    fragmentos = trocear_texto(texto, configuracion)
    for texto_fragmento, _forzado in fragmentos:
        assert len(texto_fragmento.split()) >= configuracion.palabras_por_bloque_min


def test_corte_forzado_cuando_no_hay_ninguna_senal_natural() -> None:
    """Una racha de palabras sin puntuacion, nexos ni prepositivos que la
    corten (todo sustantivos/adjetivos pegados) obliga a un corte forzado."""
    configuracion = Configuracion(
        palabras_por_bloque_min=2, palabras_por_bloque_objetivo=3, palabras_por_bloque_max=4
    )
    texto = "gato azul rapido feliz enorme brillante veloz"
    fragmentos = trocear_texto(texto, configuracion)
    assert any(forzado for _texto, forzado in fragmentos)
    assert sum(len(t.split()) for t, _f in fragmentos) == len(texto.split())


def test_nunca_corta_dentro_de_una_fecha() -> None:
    """'15 de marzo de 2026' no se parte aunque 'de' sea nexo/sintagma y el
    texto completo supere el maximo configurado."""
    configuracion = Configuracion(
        palabras_por_bloque_min=1, palabras_por_bloque_objetivo=2, palabras_por_bloque_max=2
    )
    texto = "Nos vemos el 15 de marzo de 2026 sin falta."
    fragmentos = trocear_texto(texto, configuracion)
    fecha_completa = "15 de marzo de 2026"
    texto_reconstruido = " ".join(t for t, _f in fragmentos)
    assert fecha_completa in texto_reconstruido
    for texto_fragmento, _forzado in fragmentos:
        # ninguna palabra de la fecha aparece aislada al final o al principio
        # de un fragmento distinto del que contiene la fecha completa
        if "marzo" in texto_fragmento:
            assert texto_fragmento.strip() == fecha_completa or fecha_completa in texto_fragmento


def test_nunca_corta_dentro_de_un_numero_con_unidad() -> None:
    configuracion = Configuracion(
        palabras_por_bloque_min=1, palabras_por_bloque_objetivo=1, palabras_por_bloque_max=1
    )
    texto = "Cuesta 1.500 € en total."
    fragmentos = trocear_texto(texto, configuracion)
    textos = [t for t, _f in fragmentos]
    assert any("1.500 €" in t for t in textos)


def test_reconstruccion_exacta_de_palabras_sin_perdida() -> None:
    """La concatenacion en orden de todos los fragmentos reproduce exactamente
    las mismas palabras que el texto de origen, sin perder ni duplicar ninguna."""
    configuracion = Configuracion(
        palabras_por_bloque_min=3, palabras_por_bloque_objetivo=6, palabras_por_bloque_max=9
    )
    texto = (
        "Un analisis de competencia con fuentes citadas en el tiempo que tardas "
        "en tomarte un cafe, sin perder ni una palabra por el camino."
    )
    fragmentos = trocear_texto(texto, configuracion)
    palabras_reconstruidas = " ".join(t for t, _f in fragmentos).split()
    assert palabras_reconstruidas == texto.split()


def test_texto_vacio_no_produce_bloques() -> None:
    assert trocear_texto("") == []


# --- trocear_bloque_locucion -------------------------------------------------------


def test_trocear_bloque_locucion_quita_la_marca_de_cita() -> None:
    bloque = BloqueClasificado(
        tipo=TIPO_LOCUCION,
        contenido="> Primera linea de la cita.\n> Segunda linea, mas larga todavia.",
        linea_inicio=10,
        linea_fin=11,
        motivo="cita de bloque",
        senal="cita_bloque",
    )
    resultado = trocear_bloque_locucion(bloque, numero_escena=3)
    assert resultado
    assert all(isinstance(b, BloqueRespiracion) for b in resultado)
    assert all(b.numero_escena == 3 for b in resultado)
    assert all(b.linea_inicio == 10 and b.linea_fin == 11 for b in resultado)
    assert all(">" not in b.texto for b in resultado)


def test_trocear_bloque_locucion_rechaza_bloques_no_locucion() -> None:
    bloque = BloqueClasificado(
        tipo="no_locucion",
        contenido="**EN PANTALLA**",
        linea_inicio=1,
        linea_fin=1,
        motivo="rotulo",
        senal="rotulo",
    )
    try:
        trocear_bloque_locucion(bloque, numero_escena=1)
    except ValueError:
        pass
    else:
        raise AssertionError("trocear_bloque_locucion deberia rechazar un bloque no-locucion")
