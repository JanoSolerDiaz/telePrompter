"""Tests del motor de tiempos (tarea T-12).

`test_ppm_deducido_dentro_de_banda_en_guiones_reales` reemplaza al talon del
mismo nombre en `tests/test_logica_pendiente.py` (T-03): es su criterio de
aceptacion literal, no una nota aparte.
"""

from __future__ import annotations

import pytest

from config import Configuracion
from parser import parsear_guion
from tiempos import ORIGEN_DEDUCIDO, ORIGEN_MANUAL, ORIGEN_RESPALDO, calcular_tiempos


def _guion_una_escena(num_palabras: int, rango_encabezado: str | None) -> str:
    """Guion sintetico minimo: una escena con `num_palabras` palabras de locucion
    sin puntuacion, y el rango horario que se le pida (o ninguno) en el encabezado."""
    titulo = f"Escena ({rango_encabezado})" if rango_encabezado else "Escena"
    palabras = " ".join(["palabra"] * num_palabras)
    return f"""# Titulo

## BLOQUE 0 — {titulo}

**LOCUCIÓN**

> {palabras}
"""


# --- Criterio de aceptacion sobre los tres guiones reales -------------------------


def test_ppm_deducido_dentro_de_banda_en_guiones_reales(
    texto_guiones_reales: dict[str, str],
) -> None:
    """Sobre los tres guiones reales se deduce un ppm dentro de la banda de
    plausibilidad, se aplica como base, y el contraste estimado/objetivo se
    emite por escena y en total (criterio de aceptacion de T-12)."""
    configuracion = Configuracion()
    for nombre, texto in texto_guiones_reales.items():
        resultado = parsear_guion(texto)
        tiempos = calcular_tiempos(resultado, configuracion)

        assert tiempos.ritmo.origen == ORIGEN_DEDUCIDO, (
            f"{nombre}: se esperaba ppm deducido, se aplico '{tiempos.ritmo.origen}' "
            f"({tiempos.ritmo.motivo})"
        )
        minimo, maximo = configuracion.ppm_banda_plausible
        assert minimo <= tiempos.ritmo.ppm_aplicado <= maximo

        assert len(tiempos.escenas) == len(resultado.escenas)
        for tiempo_escena in tiempos.escenas:
            assert tiempo_escena.duracion_objetivo_segundos is not None
            # El campo `aviso` (str | None) existe siempre; su valor depende del
            # guion real, no lo fija este test.
            assert tiempo_escena.aviso is None or isinstance(tiempo_escena.aviso, str)


def test_suma_de_bloques_igual_a_escena_igual_a_total_en_guiones_reales(
    texto_guiones_reales: dict[str, str],
) -> None:
    """Sin descuadres de redondeo: la suma de los bloques de una escena es su
    duracion, y la suma de las escenas es el total (criterio de aceptacion de T-12)."""
    for texto in texto_guiones_reales.values():
        resultado = parsear_guion(texto)
        tiempos = calcular_tiempos(resultado)

        for tiempo_escena in tiempos.escenas:
            suma_bloques = sum(
                b.duracion_palabras_segundos + b.pausa_segundos
                for b in tiempos.bloques
                if b.bloque.numero_escena == tiempo_escena.numero
            )
            assert suma_bloques == pytest.approx(tiempo_escena.duracion_estimada_segundos, abs=1e-6)

        suma_escenas = sum(e.duracion_estimada_segundos for e in tiempos.escenas)
        assert suma_escenas == pytest.approx(tiempos.duracion_total_segundos, abs=1e-6)


# --- Unidad: ritmo deducido/respaldo/manual sobre guiones sinteticos --------------


def test_texto_sin_puntuacion_fuerte_estima_60s_con_el_respaldo() -> None:
    """120 palabras sin puntuacion fuerte, sin duracion objetivo (cae al ritmo de
    respaldo, 120 ppm): 120 / (120/60) = 60s exactos de palabras. La unica
    tolerancia es la pausa de fin de escena (documentada aqui): incluso sin
    ninguna puntuacion, el ultimo bloque de la unica escena SIEMPRE lleva esa
    pausa, porque marca el final del guion, no una marca de puntuacion."""
    configuracion = Configuracion()
    resultado = parsear_guion(_guion_una_escena(120, rango_encabezado=None))
    tiempos = calcular_tiempos(resultado, configuracion)

    assert tiempos.ritmo.origen == ORIGEN_RESPALDO
    assert tiempos.ritmo.ppm_aplicado == configuracion.ppm_respaldo
    assert "no trae duracion objetivo" in tiempos.ritmo.motivo

    tolerancia = configuracion.pausa_fin_escena_segundos
    assert tiempos.duracion_total_segundos == pytest.approx(60.0, abs=tolerancia + 1e-6)
    assert tiempos.duracion_total_segundos >= 60.0


def test_ppm_deducido_con_numeros_exactos() -> None:
    """150 palabras frente a 60s de duracion objetivo (una sola escena, `0:00 - 1:00`)
    deducen exactamente 150 ppm, dentro de la banda de plausibilidad."""
    configuracion = Configuracion()
    resultado = parsear_guion(_guion_una_escena(150, rango_encabezado="0:00 - 1:00"))
    tiempos = calcular_tiempos(resultado, configuracion)

    assert tiempos.ritmo.origen == ORIGEN_DEDUCIDO
    assert tiempos.ritmo.ppm_deducido == pytest.approx(150.0)
    assert tiempos.ritmo.ppm_aplicado == 150


def test_ppm_deducido_fuera_de_banda_cae_al_respaldo() -> None:
    """500 palabras frente a 60s de objetivo deducirian 500 ppm, muy por encima
    de la banda plausible: se descarta y se avisa del motivo, pero el valor
    deducido (aunque no se use) sigue disponible para forzarlo a mano."""
    configuracion = Configuracion()
    resultado = parsear_guion(_guion_una_escena(500, rango_encabezado="0:00 - 1:00"))
    tiempos = calcular_tiempos(resultado, configuracion)

    assert tiempos.ritmo.origen == ORIGEN_RESPALDO
    assert tiempos.ritmo.ppm_aplicado == configuracion.ppm_respaldo
    assert tiempos.ritmo.ppm_deducido == pytest.approx(500.0)
    assert "banda plausible" in tiempos.ritmo.motivo


def test_ppm_manual_tiene_prioridad_sobre_deducido_y_respaldo() -> None:
    """Requisito 8: una calibracion manual con toma real manda sobre el resto."""
    configuracion = Configuracion(ppm_manual=90)
    resultado = parsear_guion(_guion_una_escena(150, rango_encabezado="0:00 - 1:00"))
    tiempos = calcular_tiempos(resultado, configuracion)

    assert tiempos.ritmo.origen == ORIGEN_MANUAL
    assert tiempos.ritmo.ppm_aplicado == 90


def test_transparencia_del_ritmo_incluye_el_valor_alternativo() -> None:
    """Requisito 7: siempre se puede ver que otro valor habria aplicado."""
    configuracion = Configuracion()

    resultado_deducido = parsear_guion(_guion_una_escena(150, rango_encabezado="0:00 - 1:00"))
    ritmo_deducido = calcular_tiempos(resultado_deducido, configuracion).ritmo
    assert ritmo_deducido.origen == ORIGEN_DEDUCIDO
    assert ritmo_deducido.ppm_alternativo == pytest.approx(float(configuracion.ppm_respaldo))

    resultado_respaldo = parsear_guion(_guion_una_escena(120, rango_encabezado=None))
    ritmo_respaldo = calcular_tiempos(resultado_respaldo, configuracion).ritmo
    assert ritmo_respaldo.origen == ORIGEN_RESPALDO
    # Sin duracion objetivo no hay ppm deducido que ofrecer como alternativa: el
    # unico valor disponible es el propio respaldo que ya se esta aplicando.
    assert ritmo_respaldo.ppm_alternativo == pytest.approx(float(configuracion.ppm_respaldo))
