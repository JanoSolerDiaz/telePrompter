"""Tests del guion de ejemplo y su version anotada esperada (tarea T-32).

`fixtures/guion-ejemplo.md` es el guion sintetico que usan `verificar_salidas.py
--fixture` y `instalar_skill.py` para dejar la skill verificable sin depender de
los guiones reales de calibracion del dueno (que son suyos, no un ejemplo
publico). Este modulo comprueba dos cosas que no cubre ningun otro test: que el
guion de ejemplo mezcla de verdad locucion, indicaciones de pantalla, B-roll,
una nota interna y timestamps (requisito 2 de T-32), y que la canalizacion
completa de T-08 a T-16 produce exactamente la version anotada guardada como
referencia (regresion: si el pipeline cambia el formato de salida sin querer,
este test lo detecta antes que un guion real del dueno).
"""

from __future__ import annotations

from config import Configuracion
from deteccion import detectar_problemas_bloque
from documento_revision import generar_documento_revision
from normalizacion import normalizar_bloque
from parser import parsear_guion
from reescrituras import recopilar_propuestas
from tiempos import calcular_tiempos
from troceo import trocear_guion


def _generar_documento_ejemplo(texto: str) -> str:
    configuracion = Configuracion()
    resultado = parsear_guion(texto, configuracion=configuracion)
    bloques = trocear_guion(resultado, configuracion)
    tiempos = calcular_tiempos(resultado, configuracion)
    detecciones = [detectar_problemas_bloque(b, configuracion) for b in bloques]
    normalizaciones = [normalizar_bloque(b, configuracion) for b in bloques]
    reescrituras = recopilar_propuestas(normalizaciones, detecciones)
    return generar_documento_revision(
        resultado, tiempos, detecciones, reescrituras, configuracion, nombre_guion="guion-ejemplo"
    )


def test_guion_ejemplo_mezcla_locucion_pantalla_nota_y_timestamps(
    texto_guion_ejemplo: str,
) -> None:
    """Requisito 2 de T-32 literal: locucion + indicaciones de pantalla + B-roll
    + nota interna + timestamps, todo en el mismo guion."""
    assert "**LOCUCIÓN**" in texto_guion_ejemplo
    assert "**EN PANTALLA**" in texto_guion_ejemplo
    assert "**NOTA**" in texto_guion_ejemplo
    assert "B-roll" in texto_guion_ejemplo
    assert "## BLOQUE 0" in texto_guion_ejemplo
    # Al menos una escena con timestamps "m:ss - m:ss" en el propio encabezado.
    assert "(0:00 – 0:20)" in texto_guion_ejemplo


def test_guion_ejemplo_sin_avisos_de_desviacion_de_tiempos(texto_guion_ejemplo: str) -> None:
    """El guion de ejemplo esta calibrado a proposito (a diferencia de un
    guion real cualquiera) para que la version esperada no arrastre un aviso
    de desviacion de ritmo, que solo anadiria ruido a un fixture pensado para
    ensenar el formato de salida, no para probar ese aviso en concreto (eso ya
    lo cubre `tests/test_tiempos.py`)."""
    configuracion = Configuracion()
    resultado = parsear_guion(texto_guion_ejemplo, configuracion=configuracion)
    tiempos = calcular_tiempos(resultado, configuracion)
    assert tiempos.aviso_total is None
    for escena in tiempos.escenas:
        assert escena.aviso is None, f"escena {escena.numero}: {escena.aviso}"


def test_guion_ejemplo_genera_exactamente_la_version_esperada(
    texto_guion_ejemplo: str, texto_guion_ejemplo_esperado: str
) -> None:
    """Test de regresion (golden file): la canalizacion completa de T-08 a
    T-16 sobre `guion-ejemplo.md` debe producir byte a byte
    `guion-ejemplo-esperado.md`. Si este test falla tras un cambio deliberado
    de formato, regenera el fixture esperado en la misma sesion -- nunca
    ajustes el test para que pase sin mirar el contenido."""
    documento = _generar_documento_ejemplo(texto_guion_ejemplo)
    assert documento == texto_guion_ejemplo_esperado


def test_guion_ejemplo_cubre_todos_sus_bloques_de_respiracion(texto_guion_ejemplo: str) -> None:
    """Mismo criterio de cobertura total que T-16 exige sobre los guiones
    reales (invariante (a), §0.2): ningun bloque de respiracion del guion de
    ejemplo se queda fuera del documento anotado."""
    from documento_revision import extraer_texto_bloques

    configuracion = Configuracion()
    resultado = parsear_guion(texto_guion_ejemplo, configuracion=configuracion)
    tiempos = calcular_tiempos(resultado, configuracion)
    documento = _generar_documento_ejemplo(texto_guion_ejemplo)
    extraidos = extraer_texto_bloques(documento)
    assert len(extraidos) == len(tiempos.bloques)
