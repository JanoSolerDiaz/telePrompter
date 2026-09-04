"""Test de integracion del encaje con la cadena de montaje (T-33, requisito 3).

Ata en un unico test las dos piezas que documenta
`references/contrato-montaje.md`: `.srt` (T-27) y `tarjetas.json` (T-29),
generadas a partir del MISMO `ResultadoTiempos` de un guion real, y comprueba
que son consistentes entre si -- no solo que cada una, por separado, ya pasa
su propio validador (eso ya lo cubren `tests/test_srt.py` y
`tests/test_pptx.py`)."""

from __future__ import annotations

import json

import pytest

from capitulos_youtube import calcular_capitulos
from clasificador import clasificar_guion
from config import Configuracion
from convencion import detectar_desviaciones
from parser import parsear_guion
from pptx import generar_tarjetas, tarjetas_a_diccionario, validar_tarjetas
from srt import exportar_srt, formatear_srt, generar_entradas_srt, validar_srt
from srt_alineado import reescalar_a_toma_buena
from tiempos import calcular_tiempos


def test_srt_y_tarjetas_json_son_consistentes_sobre_los_guiones_reales(
    texto_guiones_reales: dict[str, str],
) -> None:
    """Criterio de aceptacion literal de T-33: el `.srt` de la fixture se valida
    sin avisos. Se comprueba ademas, sobre los tres guiones reales, que
    `tarjetas.json` pasa su propio esquema y que ambas salidas describen
    exactamente la misma duracion total y el mismo orden de escenas -- la base
    con la que la cadena de montaje casa tomas con escenas sin ambiguedad."""
    configuracion = Configuracion()
    for nombre, texto in texto_guiones_reales.items():
        resultado = parsear_guion(texto)
        clasificacion = clasificar_guion(resultado)
        resultado_tiempos = calcular_tiempos(resultado, configuracion)

        # Cero desviaciones de numeracion de escena: el requisito 2 de T-33
        # ("nombres y orden de escenas estables y predecibles") se cumple de
        # verdad en los guiones reales, no solo sobre el papel.
        desviaciones = detectar_desviaciones(resultado, clasificacion, configuracion)
        tipos_numero = {d.tipo for d in desviaciones if d.tipo.startswith("numero_escena_")}
        assert tipos_numero == set(), f"{nombre}: numeracion de escena ambigua {tipos_numero}"

        # `.srt`: se valida sin avisos (criterio de aceptacion literal).
        entradas = generar_entradas_srt(resultado_tiempos, configuracion)
        contenido_srt = formatear_srt(entradas)
        assert contenido_srt == exportar_srt(resultado_tiempos, configuracion)
        problemas_srt = validar_srt(contenido_srt, configuracion)
        assert problemas_srt == [], f"{nombre}: .srt con avisos {problemas_srt}"
        assert entradas, f"{nombre}: el .srt no genero ningun subtitulo"

        # `tarjetas.json`: pasa su propio esquema (requisito 3).
        resultado_tarjetas = generar_tarjetas(resultado, resultado_tiempos, nombre, configuracion)
        datos_tarjetas = tarjetas_a_diccionario(resultado_tarjetas)
        problemas_tarjetas = validar_tarjetas(datos_tarjetas)
        assert problemas_tarjetas == [], f"{nombre}: tarjetas.json invalido {problemas_tarjetas}"
        # Sigue siendo JSON serializable de verdad, no solo un dict en memoria
        # con la forma correcta (round-trip completo, como lo escribiria
        # `pptx.guardar_tarjetas` antes de que lo lea la cadena de montaje).
        datos_tarjetas = json.loads(json.dumps(datos_tarjetas, ensure_ascii=False))

        # Consistencia cruzada: el fin del ultimo subtitulo del .srt coincide
        # exactamente con la duracion total que declara tarjetas.json (misma
        # fuente unica de tiempos, T-12) -- la propiedad que
        # `references/contrato-montaje.md` documenta para derivar el instante
        # de inicio/fin de cada escena sumando `duracion_estimada_segundos`.
        fin_ultimo_subtitulo = entradas[-1].fin_segundos
        duracion_total_tarjetas = datos_tarjetas["metadatos"]["duracion_total_segundos"]
        assert fin_ultimo_subtitulo == duracion_total_tarjetas

        suma_duraciones_escena = sum(
            escena["duracion_estimada_segundos"] for escena in datos_tarjetas["escenas"]
        )
        assert suma_duraciones_escena == duracion_total_tarjetas

        # Orden de escenas: el mismo en tarjetas.json que en el guion de
        # origen, y estrictamente creciente (requisito 2).
        numeros_tarjetas = [escena["numero"] for escena in datos_tarjetas["escenas"]]
        numeros_guion = [escena.numero for escena in resultado.escenas]
        assert numeros_tarjetas == numeros_guion
        assert numeros_tarjetas == sorted(set(numeros_tarjetas))


def _mmss(segundos: int) -> str:
    return f"{segundos // 60}:{segundos % 60:02d}"


def _guion_con_capitulos_y_tomas(
    titulos_capitulos: list[str], palabras_por_escena: list[int]
) -> str:
    """Guion sintetico con una seccion `Capítulos` (una fila por titulo, mismo
    orden que las escenas) y una escena por entrada de `palabras_por_escena` --
    mismo generador que usan `tests/test_capitulos_youtube.py` y
    `tests/test_srt_alineado.py`, unificado aqui para que ambas salidas partan
    EXACTAMENTE del mismo guion."""
    filas = "\n".join(f"| 0:00 | {titulo} |" for titulo in titulos_capitulos)
    partes = [
        "# Titulo\n",
        "\n## Capítulos (para la descripción del vídeo)\n\n"
        f"| Marca | Capítulo |\n|---|---|\n{filas}\n",
    ]
    inicio = 0
    for indice, num_palabras in enumerate(palabras_por_escena, start=1):
        fin = inicio + 15
        palabras = " ".join(["palabra"] * num_palabras)
        partes.append(
            f"\n## BLOQUE {indice} - Escena {indice} ({_mmss(inicio)} - {_mmss(fin)})\n\n"
            f"**LOCUCIÓN**\n\n> {palabras}. Otra frase, con coma, aqui.\n"
        )
        inicio = fin
    return "".join(partes)


def test_srt_alineado_y_capitulos_youtube_son_coherentes_entre_si() -> None:
    """Cierra el hallazgo #18 (R-11): `guion-alineado.srt` (R-05) y
    `capitulos-youtube.txt` (R-07) comparten `tomas.duracion_toma_buena`, asi
    que su coherencia hoy es "por construccion" -- este test la verifica por
    regresion en vez de darla por sentada, alimentando ambos con el MISMO
    `ResultadoTiempos` + `tomas_por_escena` (dos escenas con toma buena real,
    una sin ella que cae a la duracion estimada, igual que documentan
    `ResultadoAlineacion.escenas_sin_toma_buena` y
    `ResultadoCapitulos.escenas_sin_toma_buena`)."""
    resultado = parsear_guion(
        _guion_con_capitulos_y_tomas(["Primero", "Segundo", "Tercero"], [10, 10, 10])
    )
    tiempos = calcular_tiempos(resultado, Configuracion())
    tomas_por_escena = {
        "1": {
            "titulo": "Escena 1",
            "tomas": [{"numero": 1, "duracion_segundos": 5.0, "nota": "", "buena": True}],
        },
        "3": {
            "titulo": "Escena 3",
            "tomas": [{"numero": 1, "duracion_segundos": 30.0, "nota": "", "buena": True}],
        },
    }

    alineacion = reescalar_a_toma_buena(tiempos, tomas_por_escena)
    calculo = calcular_capitulos(resultado, tiempos, tomas_por_escena)

    # Las dos salidas coinciden en que exactamente la escena 2 se apoya en la
    # duracion estimada -- ninguna mezcla en silencio real con estimado sin
    # decir cual es cual (mismo criterio de honestidad de R-04/R-05/R-07).
    assert alineacion.escenas_sin_toma_buena == (2,)
    assert calculo.escenas_sin_toma_buena == (2,)
    assert alineacion.escenas_alineadas == (1, 3)

    # Coherencia cruzada: el instante de inicio acumulado de cada capitulo de
    # R-07 coincide con el instante de inicio acumulado de la misma escena en
    # el `.srt` alineado de R-05 -- ambos avanzan el cursor con la MISMA
    # duracion por escena (real si existe toma buena, estimada si no).
    duracion_acumulada = 0.0
    for tiempo_escena, capitulo in zip(
        alineacion.resultado_tiempos.escenas, calculo.capitulos, strict=True
    ):
        assert capitulo.numero_escena == tiempo_escena.numero
        assert capitulo.inicio_segundos == pytest.approx(duracion_acumulada, abs=1e-6)
        duracion_acumulada += tiempo_escena.duracion_estimada_segundos

    # Duracion total identica: el `.srt` alineado termina exactamente donde
    # deberia empezar un capitulo hipotetico "despues de la ultima escena".
    assert alineacion.resultado_tiempos.duracion_total_segundos == pytest.approx(
        duracion_acumulada, abs=1e-6
    )
