"""Suite minima (T-03): talones de la logica de producto que todavia no existe.

T-03 depende solo de T-01 y se ejecuta antes que T-07 a T-27 en el orden de §1 de
SEGUIMIENTO: para cuando corre esta sesion, el parser, el clasificador, el troceador,
el motor de tiempos, el normalizador y el exportador de `.srt` no estan implementados
todavia. En vez de fingir que estan cubiertos o de omitir la mencion, cada capacidad
pendiente tiene aqui un test marcado `skip` que nombra la tarea que lo desbloquea
(mismo tratamiento que "NO APLICABLE" en `verificar_salidas.py`, para T-00). Cuando esa
tarea aterrice, quitar el `skip` e implementar el test descrito en el motivo es parte
de su criterio de aceptacion, no una nota aparte.
"""

from __future__ import annotations

import pytest


@pytest.mark.skip(reason="T-08: el parser de escenas no existe todavia.")
def test_parser_reconoce_toda_escena_del_guion_real() -> None:
    """El parser debe devolver una escena por cada encabezado `## BLOQUE N — ...`."""


@pytest.mark.skip(reason="T-09: el clasificador locucion/no locucion no existe todavia.")
def test_clasificador_distingue_locucion_de_no_locucion() -> None:
    """Todo bloque bajo `**LOCUCIÓN**` es locucion; bajo los rotulos de
    `ROTULOS_NO_LOCUCION` no lo es. Un bloque sin rotulo se infiere y se marca
    como desviacion de la convencion (§0.2), nunca como error."""


@pytest.mark.skip(reason="T-11: el troceador en bloques de respiracion no existe todavia.")
def test_troceo_respeta_el_rango_de_palabras_configurado() -> None:
    """Cada bloque de respiracion queda entre `palabras_por_bloque_min` y
    `palabras_por_bloque_max` (config.py), salvo que la locucion completa sea mas corta."""


@pytest.mark.skip(reason="T-12: el motor de tiempos no existe todavia.")
def test_motor_de_tiempos_deduce_el_ppm_del_guion() -> None:
    """El ppm de referencia se deduce de las duraciones objetivo del guion real; si no
    hay duraciones o el valor cae fuera de `PPM_BANDA_PLAUSIBLE`, usa `PPM_RESPALDO`."""


@pytest.mark.skip(reason="T-13: la normalizacion a forma dicha no existe todavia.")
def test_normalizacion_a_forma_dicha_es_reversible() -> None:
    """Toda normalizacion conserva el texto original junto a la propuesta
    (invariante (b) de §0.2: original siempre recuperable)."""


@pytest.mark.skip(reason="T-27: el exportador de .srt no existe todavia.")
def test_srt_generado_respeta_el_limite_de_caracteres_por_linea() -> None:
    """Ninguna linea del `.srt` supera `SRT_CARACTERES_POR_LINEA_MAX` (config.py)."""


@pytest.mark.skip(
    reason="T-08/T-09: necesita el parser y el clasificador para reconstruir el guion."
)
def test_invariante_cobertura_total_del_guion() -> None:
    """Invariante (a) de §0.2: todo bloque del `.md` de origen queda clasificado
    (locucion o no locucion) con su motivo visible; nada se descarta en silencio. Un
    test de reconstruccion debe comparar el guion original contra la union de todos
    los bloques clasificados."""


@pytest.mark.skip(reason="T-17: la revalidacion que respeta ediciones no existe todavia.")
def test_invariante_idempotencia_de_la_revalidacion() -> None:
    """Invariante (c) de §0.2: revalidar dos veces seguidas sin tocar
    `guion-escenas.md` produce el mismo resultado, y el texto editado a mano por el
    dueno nunca se sobrescribe."""
