"""Suite minima (T-03): talones de la logica de producto que todavia no existe.

T-03 depende solo de T-01 y se ejecuta antes que T-07 a T-27 en el orden de §1 de
SEGUIMIENTO: para cuando corre esta sesion, el exportador de `.srt` no esta
implementado todavia (el parser de T-08, el clasificador de T-09, el troceador de
T-11, el motor de tiempos de T-12 y la normalizacion a forma dicha de T-13 ya
existen, ver `tests/test_parser.py`, `tests/test_clasificador.py`,
`tests/test_troceo.py`, `tests/test_tiempos.py` y `tests/test_normalizacion.py`).
En vez de fingir que estan cubiertos o de omitir la mencion, cada capacidad
pendiente tiene aqui un test marcado `skip` que nombra la tarea que lo desbloquea
(mismo tratamiento que "NO APLICABLE" en `verificar_salidas.py`, para T-00). Cuando
esa tarea aterrice, quitar el `skip` e implementar el test descrito en el motivo es
parte de su criterio de aceptacion, no una nota aparte.
"""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.mark.skip(reason="T-27: el exportador de .srt no existe todavia.")
def test_srt_generado_respeta_el_limite_de_caracteres_por_linea() -> None:
    """Ninguna linea del `.srt` supera `SRT_CARACTERES_POR_LINEA_MAX` (config.py)."""


def test_invariante_idempotencia_de_la_revalidacion(tmp_path: Path) -> None:
    """Invariante (c) de §0.2: revalidar dos veces seguidas sin tocar
    `guion-escenas.md` produce el mismo resultado, y el texto editado a mano por el
    dueno nunca se sobrescribe.

    T-17 (`scripts/revalidacion.py`) es quien cierra este hueco: `revalidar_guion`
    relee el documento, respeta las decisiones y ediciones ya presentes y solo
    recalcula lo derivado (troceo, tiempos, avisos). Revalidar dos veces sobre el
    MISMO texto en disco -- sin que el dueno haya tocado nada -- debe devolver
    tiempos, detecciones, reescrituras e incidencias identicos: no hay nada nuevo
    que decidir la segunda vez.
    """
    from config import Configuracion
    from deteccion import detectar_problemas_guion
    from documento_revision import generar_documento_revision
    from estado import estado_inicial
    from normalizacion import normalizar_guion
    from parser import parsear_guion
    from reescrituras import fusionar_con_estado, guardar_en_estado, recopilar_propuestas
    from revalidacion import revalidar_guion
    from tiempos import calcular_tiempos
    from troceo import trocear_guion

    texto_guion = """# Guion de prueba

## BLOQUE 1 — Escena unica (0:00 – 0:10)

**LOCUCIÓN**

> Hemos ahorrado 20 euros con el nuevo proceso de revisión.

**NOTA**

Comprobar tono en grabación.
"""
    ruta_guion = tmp_path / "guion.md"
    ruta_guion.write_text(texto_guion, encoding="utf-8")
    configuracion = Configuracion()
    estado = estado_inicial(ruta_guion, configuracion)
    resultado = parsear_guion(texto_guion, configuracion=configuracion)

    bloques = trocear_guion(resultado, configuracion)
    tiempos = calcular_tiempos(resultado, configuracion)
    detecciones = detectar_problemas_guion(bloques, configuracion)
    normalizaciones = normalizar_guion(bloques, configuracion)
    propuestas = recopilar_propuestas(normalizaciones, detecciones)
    reescrituras = fusionar_con_estado(estado, propuestas)
    guardar_en_estado(estado, reescrituras)
    documento = generar_documento_revision(
        resultado, tiempos, detecciones, reescrituras, configuracion, nombre_guion="prueba"
    )

    primera = revalidar_guion(resultado, documento, estado, configuracion)
    segunda = revalidar_guion(resultado, documento, estado, configuracion)

    textos_primera = [b.bloque.texto for b in primera.resultado_tiempos.bloques]
    textos_segunda = [b.bloque.texto for b in segunda.resultado_tiempos.bloques]
    assert textos_primera == textos_segunda
    assert primera.resultado_tiempos.duracion_total_segundos == (
        segunda.resultado_tiempos.duracion_total_segundos
    )
    assert [(r.id, r.decision) for r in primera.reescrituras] == [
        (r.id, r.decision) for r in segunda.reescrituras
    ]
    assert [i.mensaje for i in primera.incidencias] == [i.mensaje for i in segunda.incidencias]
    assert not primera.validado
    assert not segunda.validado

    # El texto de origen -- lo que el dueno escribio a mano -- sigue intacto en
    # disco: revalidar nunca reescribe el `.md` de entrada, solo lee y deriva.
    assert ruta_guion.read_text(encoding="utf-8") == texto_guion
