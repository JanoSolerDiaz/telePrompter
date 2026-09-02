"""Test de integracion del encaje con la cadena de montaje (T-33, requisito 3).

Ata en un unico test las dos piezas que documenta
`references/contrato-montaje.md`: `.srt` (T-27) y `tarjetas.json` (T-29),
generadas a partir del MISMO `ResultadoTiempos` de un guion real, y comprueba
que son consistentes entre si -- no solo que cada una, por separado, ya pasa
su propio validador (eso ya lo cubren `tests/test_srt.py` y
`tests/test_pptx.py`)."""

from __future__ import annotations

import json

from clasificador import clasificar_guion
from config import Configuracion
from convencion import detectar_desviaciones
from parser import parsear_guion
from pptx import generar_tarjetas, tarjetas_a_diccionario, validar_tarjetas
from srt import exportar_srt, formatear_srt, generar_entradas_srt, validar_srt
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
