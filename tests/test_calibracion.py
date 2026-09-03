"""Tests de la recalibracion de ritmo con tiempos reales (tarea R-04).

Sigue el mismo patron que `tests/test_srt.py`: guiones sinteticos minimos
construidos a mano (control total sobre el numero de palabras y la duracion
objetivo) en vez de reparsear los guiones reales, cuyo ppm/tomas no estan
calibrados para probar los umbrales de este modulo.
"""

from __future__ import annotations

import pytest

from calibracion import (
    TIPO_APERTURA,
    TIPO_CIERRE,
    TIPO_DESARROLLO,
    EvidenciaGuion,
    calcular_calibracion,
)
from config import Configuracion
from parser import parsear_guion
from tiempos import calcular_tiempos


def _mmss(segundos: int) -> str:
    return f"{segundos // 60}:{segundos % 60:02d}"


def _guion_n_escenas(palabras_por_escena: list[int], duracion_por_escena_segundos: int = 10) -> str:
    """Guion sintetico con una escena por entrada de `palabras_por_escena`,
    cada una con esa cantidad de palabras de locucion sin puntuacion
    intermedia y una duracion objetivo de cabecera fija."""
    partes = ["# Titulo\n"]
    inicio = 0
    for indice, num_palabras in enumerate(palabras_por_escena, start=1):
        fin = inicio + duracion_por_escena_segundos
        palabras = " ".join(["palabra"] * num_palabras)
        partes.append(
            f"\n## BLOQUE {indice} - Escena {indice} ({_mmss(inicio)} - {_mmss(fin)})\n\n"
            f"**LOCUCIÓN**\n\n> {palabras}\n"
        )
        inicio = fin
    return "".join(partes)


def _evidencia(
    nombre_guion: str,
    palabras_por_escena: list[int],
    tomas_buenas_segundos: dict[int, float],
    configuracion: Configuracion | None = None,
) -> EvidenciaGuion:
    """Construye una `EvidenciaGuion` a partir de un guion sintetico y un
    mapa {numero_escena: duracion_real_segundos} de tomas buenas -- las
    escenas que no aparecen en el mapa se quedan sin toma buena."""
    configuracion = configuracion or Configuracion()
    resultado = parsear_guion(_guion_n_escenas(palabras_por_escena))
    tiempos = calcular_tiempos(resultado, configuracion)
    tomas_por_escena = {
        str(numero): {
            "titulo": f"Escena {numero}",
            "tomas": [
                {"numero": 1, "duracion_segundos": duracion, "nota": "", "buena": True}
            ],
        }
        for numero, duracion in tomas_buenas_segundos.items()
    }
    return EvidenciaGuion(nombre_guion, tiempos, tomas_por_escena)


# --- Requisito 1: contraste por escena y en total -----------------------------------


def test_contraste_trae_las_tres_duraciones_por_escena() -> None:
    evidencia = _evidencia("guion-a", [10, 10, 10], {1: 5.0, 3: 8.0})
    informe = calcular_calibracion([evidencia])

    (guion,) = informe.guiones
    assert len(guion.escenas) == 3
    escena_1, escena_2, escena_3 = guion.escenas

    assert escena_1.duracion_real_segundos == 5.0
    assert escena_1.duracion_objetivo_segundos == 10.0
    assert escena_1.duracion_estimada_segundos > 0

    # Escena 2 no tiene ninguna toma buena: nunca se inventa un valor.
    assert escena_2.duracion_real_segundos is None

    assert escena_3.duracion_real_segundos == 8.0


def test_escena_con_tomas_pero_ninguna_marcada_buena_no_aporta_real() -> None:
    resultado = parsear_guion(_guion_n_escenas([10]))
    tiempos = calcular_tiempos(resultado, Configuracion())
    tomas_por_escena = {
        "1": {
            "titulo": "Escena 1",
            "tomas": [
                {"numero": 1, "duracion_segundos": 12.0, "nota": "mal", "buena": False},
                {"numero": 2, "duracion_segundos": 11.0, "nota": "", "buena": False},
            ],
        }
    }
    informe = calcular_calibracion([EvidenciaGuion("guion", tiempos, tomas_por_escena)])
    (guion,) = informe.guiones
    assert guion.escenas[0].duracion_real_segundos is None


def test_titulo_de_escena_cae_al_numero_si_no_hay_registro_de_tomas() -> None:
    evidencia = _evidencia("guion-a", [10], {})
    informe = calcular_calibracion([evidencia])
    assert informe.guiones[0].escenas[0].titulo == "Escena 1"


# --- Clasificacion posicional (apertura / desarrollo / cierre) ----------------------


def test_tipo_de_escena_es_posicional_no_por_titulo() -> None:
    evidencia = _evidencia("guion-a", [5, 5, 5, 5], {})
    (guion,) = calcular_calibracion([evidencia]).guiones
    tipos = [escena.tipo for escena in guion.escenas]
    assert tipos == [TIPO_APERTURA, TIPO_DESARROLLO, TIPO_DESARROLLO, TIPO_CIERRE]


def test_guion_de_una_sola_escena_es_apertura() -> None:
    evidencia = _evidencia("guion-a", [5], {})
    (guion,) = calcular_calibracion([evidencia]).guiones
    assert guion.escenas[0].tipo == TIPO_APERTURA


# --- Requisito 2: ppm calibrado propuesto, nunca aplicado sola ----------------------


def test_sin_ninguna_toma_buena_no_hay_propuesta() -> None:
    evidencia = _evidencia("guion-a", [10, 10], {})
    propuesta = calcular_calibracion([evidencia]).propuesta_ppm
    assert propuesta.ppm_calibrado is None
    assert "ningún guion" in propuesta.motivo


def test_con_un_solo_guion_con_evidencia_no_hay_propuesta_aunque_sobren_palabras() -> None:
    """`calibracion_guiones_minimos` (2 por defecto) exige evidencia de varios
    guiones, literal del requisito 2 ("evidencia acumulada de varios guiones")."""
    evidencia = _evidencia("guion-a", [200], {1: 80.0})  # 200 palabras / (80/60) = 150 ppm
    propuesta = calcular_calibracion([evidencia]).propuesta_ppm
    assert propuesta.ppm_calibrado is None
    assert "1 guion" in propuesta.motivo


def test_con_pocas_palabras_de_evidencia_no_hay_propuesta() -> None:
    evidencia_a = _evidencia("guion-a", [20], {1: 8.0})
    evidencia_b = _evidencia("guion-b", [20], {1: 8.0})
    propuesta = calcular_calibracion([evidencia_a, evidencia_b]).propuesta_ppm
    assert propuesta.ppm_calibrado is None
    assert "palabras" in propuesta.motivo


def test_con_evidencia_de_dos_guiones_propone_ppm_calibrado() -> None:
    """Criterio de aceptacion literal de R-04: con dos guiones grabados, la
    skill propone un ppm calibrado y muestra la desviacion por escena que lo
    justifica."""
    # guion A: 120 palabras / 48s = 150 ppm. guion B: 60 palabras / 24s = 150 ppm.
    evidencia_a = _evidencia("guion-a", [120], {1: 48.0})
    evidencia_b = _evidencia("guion-b", [60], {1: 24.0})
    informe = calcular_calibracion([evidencia_a, evidencia_b])

    propuesta = informe.propuesta_ppm
    assert propuesta.ppm_calibrado == 150
    assert propuesta.ppm_deducido == pytest.approx(150.0)
    assert propuesta.num_guiones_con_evidencia == 2
    assert propuesta.num_escenas_con_evidencia == 2
    assert propuesta.palabras_totales == 180

    # La desviacion por escena que lo justifica (requisito 1) sigue disponible.
    for guion in informe.guiones:
        assert guion.escenas[0].duracion_real_segundos is not None


def test_ppm_deducido_fuera_de_banda_plausible_no_se_propone() -> None:
    configuracion = Configuracion()
    # 400 palabras en 20s = 1200 ppm, muy por encima de la banda [90, 180].
    evidencia_a = _evidencia("guion-a", [400], {1: 10.0}, configuracion)
    evidencia_b = _evidencia("guion-b", [400], {1: 10.0}, configuracion)
    propuesta = calcular_calibracion([evidencia_a, evidencia_b], configuracion).propuesta_ppm
    assert propuesta.ppm_calibrado is None
    assert propuesta.ppm_deducido is not None
    assert "banda plausible" in propuesta.motivo


def test_calcular_calibracion_nunca_muta_la_configuracion() -> None:
    """Requisito 2 ("nunca se aplica sola"): la propuesta es un dato de
    salida, no un efecto secundario sobre `Configuracion.ppm_manual`."""
    configuracion = Configuracion()
    evidencia_a = _evidencia("guion-a", [120], {1: 48.0}, configuracion)
    evidencia_b = _evidencia("guion-b", [60], {1: 24.0}, configuracion)
    calcular_calibracion([evidencia_a, evidencia_b], configuracion)
    assert configuracion.ppm_manual is None


# --- Requisito 3: informe corto por tipo de escena -----------------------------------


def test_resumen_por_tipo_agrega_evidencia_de_varios_guiones() -> None:
    evidencia_a = _evidencia("guion-a", [10, 10, 10], {1: 3.0, 2: 4.0, 3: 5.0})
    evidencia_b = _evidencia("guion-b", [10, 10], {1: 3.0, 2: 4.0})
    informe = calcular_calibracion([evidencia_a, evidencia_b])

    tipos = {resumen.tipo: resumen for resumen in informe.resumen_por_tipo}
    # Apertura: escena 1 de A + escena 1 de B = 2 escenas.
    assert tipos[TIPO_APERTURA].num_escenas == 2
    # Cierre: escena 3 de A + escena 2 de B = 2 escenas.
    assert tipos[TIPO_CIERRE].num_escenas == 2
    # Desarrollo: solo la escena 2 de A (guion B no tiene escena intermedia).
    assert tipos[TIPO_DESARROLLO].num_escenas == 1


def test_desviacion_relativa_negativa_cuando_la_toma_real_es_mas_corta() -> None:
    evidencia = _evidencia("guion-a", [10], {1: 1.0})  # toma muy corta frente a la estimada
    informe = calcular_calibracion([evidencia])
    (resumen,) = informe.resumen_por_tipo
    assert resumen.desviacion_relativa < 0


def test_tipo_sin_evidencia_real_no_aparece_en_el_resumen() -> None:
    evidencia = _evidencia("guion-a", [10, 10, 10], {})  # ninguna toma buena
    informe = calcular_calibracion([evidencia])
    assert informe.resumen_por_tipo == ()


# --- El informe se puede mostrar sin fallar, con o sin propuesta --------------------


def test_mostrar_informe_no_falla_con_o_sin_propuesta(capsys: pytest.CaptureFixture[str]) -> None:
    evidencia = _evidencia("guion-a", [10, 10], {1: 4.0})
    calcular_calibracion([evidencia]).mostrar_informe()
    salida = capsys.readouterr()
    assert "Sin propuesta todavía" in salida.err or "ppm" in salida.out

    evidencia_a = _evidencia("guion-a", [120], {1: 48.0})
    evidencia_b = _evidencia("guion-b", [60], {1: 24.0})
    calcular_calibracion([evidencia_a, evidencia_b]).mostrar_informe()
    salida = capsys.readouterr()
    assert "150 ppm" in salida.out


# --- Configuracion: validacion de los nuevos campos ----------------------------------


def test_configuracion_rechaza_minimo_de_guiones_no_positivo() -> None:
    with pytest.raises(ValueError, match="minimo de guiones"):
        Configuracion(calibracion_guiones_minimos=0)


def test_configuracion_rechaza_minimo_de_palabras_no_positivo() -> None:
    with pytest.raises(ValueError, match="minimo de palabras"):
        Configuracion(calibracion_palabras_minimas=-1)
