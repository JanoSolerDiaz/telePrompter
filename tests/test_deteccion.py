"""Tests del detector de problemas de lectura en voz alta (tarea T-14).

Una familia por requisito (1 a 5), cada una con un caso que dispara el aviso y
un contraejemplo que no lo hace (criterio de aceptacion literal de T-14).
`test_cobertura_total_guiones_reales` reemplaza al talon del mismo nombre en
`tests/test_logica_pendiente.py` (mismo tratamiento que T-08 a T-13).
"""

from __future__ import annotations

import pytest

from config import Configuracion
from deteccion import (
    FAMILIA_ANGLICISMO,
    FAMILIA_CACOFONIA,
    FAMILIA_ESTRUCTURA_DIFICIL,
    FAMILIA_SIN_PUNTO_RESPIRACION,
    FAMILIA_TRABALENGUAS,
    detectar_problemas_bloque,
    detectar_problemas_guion,
)
from parser import parsear_guion
from troceo import BloqueRespiracion, trocear_guion


def _bloque(texto: str) -> BloqueRespiracion:
    return BloqueRespiracion(
        texto=texto,
        numero_escena=1,
        linea_inicio=1,
        linea_fin=1,
        num_palabras=len(texto.split()),
        corte_forzado=False,
    )


def _familias(avisos: list) -> set[str]:  # type: ignore[type-arg]
    return {aviso.familia for aviso in avisos}


# --- Requisito 1: frase sin punto de respiracion ------------------------------------


def test_frase_larga_sin_puntuacion_dispara_aviso() -> None:
    texto = (
        "Esta es una frase deliberadamente larga sin ninguna coma ni pausa "
        "que la corte en absoluto"
    )
    resultado = detectar_problemas_bloque(_bloque(texto))
    avisos = [a for a in resultado.avisos if a.familia == FAMILIA_SIN_PUNTO_RESPIRACION]
    assert len(avisos) == 1
    aviso = avisos[0]
    assert aviso.severidad == "alta"
    assert aviso.admite_particion is True
    assert aviso.particion_sugerida is not None
    primera_mitad, segunda_mitad = aviso.particion_sugerida
    assert primera_mitad and segunda_mitad
    assert f"{primera_mitad} {segunda_mitad}" == texto


def test_frase_larga_con_coma_no_dispara_aviso() -> None:
    texto = (
        "Esta es una frase, deliberadamente larga, sin ninguna coma ni pausa "
        "que la corte en absoluto"
    )
    resultado = detectar_problemas_bloque(_bloque(texto))
    assert FAMILIA_SIN_PUNTO_RESPIRACION not in _familias(resultado.avisos)


def test_frase_corta_sin_puntuacion_no_dispara_aviso() -> None:
    resultado = detectar_problemas_bloque(_bloque("Vamos a grabar la escena ahora"))
    assert FAMILIA_SIN_PUNTO_RESPIRACION not in _familias(resultado.avisos)


# --- Requisito 2: cacofonias y repeticiones fonicas proximas ------------------------


def test_de_encadenados_dispara_aviso() -> None:
    resultado = detectar_problemas_bloque(_bloque("Fuimos al museo de arte de la ciudad de moda"))
    assert FAMILIA_CACOFONIA in _familias(resultado.avisos)


def test_rima_involuntaria_dispara_aviso() -> None:
    resultado = detectar_problemas_bloque(
        _bloque("Es un momento realmente brillante y constante para todos")
    )
    assert FAMILIA_CACOFONIA in _familias(resultado.avisos)


def test_sin_repeticiones_fonicas_no_dispara_aviso() -> None:
    resultado = detectar_problemas_bloque(
        _bloque("Hoy vamos a grabar la primera escena del video")
    )
    assert FAMILIA_CACOFONIA not in _familias(resultado.avisos)


# --- Requisito 3: trabalenguas -------------------------------------------------------


def test_consonantes_seguidas_dispara_aviso() -> None:
    resultado = detectar_problemas_bloque(_bloque("La obstrucción del transporte complica todo"))
    avisos = [a for a in resultado.avisos if a.familia == FAMILIA_TRABALENGUAS]
    assert avisos
    assert "obstrucción" in avisos[0].fragmento


def test_palabras_largas_seguidas_dispara_aviso() -> None:
    resultado = detectar_problemas_bloque(
        _bloque("Analizaremos detalladamente procedimientos administrativos pendientes")
    )
    assert FAMILIA_TRABALENGUAS in _familias(resultado.avisos)


def test_palabras_cortas_no_disparan_trabalenguas() -> None:
    resultado = detectar_problemas_bloque(_bloque("Vamos a ver el video hoy"))
    assert FAMILIA_TRABALENGUAS not in _familias(resultado.avisos)


# --- Requisito 4: anglicismos --------------------------------------------------------


def test_anglicismo_conocido_dispara_aviso_con_equivalente() -> None:
    resultado = detectar_problemas_bloque(_bloque("Enviame el feedback por email cuando puedas"))
    avisos = [a for a in resultado.avisos if a.familia == FAMILIA_ANGLICISMO]
    assert len(avisos) == 2  # feedback y email
    assert any("correo electrónico" in aviso.recomendacion for aviso in avisos)


def test_sin_anglicismos_no_dispara_aviso() -> None:
    resultado = detectar_problemas_bloque(_bloque("Enviame el resumen por correo cuando puedas"))
    assert FAMILIA_ANGLICISMO not in _familias(resultado.avisos)


# --- Requisito 5: estructuras dificiles ----------------------------------------------


def test_doble_negacion_dispara_aviso() -> None:
    resultado = detectar_problemas_bloque(_bloque("No hay nadie que nunca lo haya visto"))
    assert FAMILIA_ESTRUCTURA_DIFICIL in _familias(resultado.avisos)


def test_subordinadas_encadenadas_disparan_aviso() -> None:
    resultado = detectar_problemas_bloque(
        _bloque("Creo que aunque llueva porque el cielo esta gris iremos")
    )
    assert FAMILIA_ESTRUCTURA_DIFICIL in _familias(resultado.avisos)


def test_incisos_acumulados_disparan_aviso() -> None:
    resultado = detectar_problemas_bloque(
        _bloque("El proyecto (que empezó tarde) — según nos dijeron — fue un éxito")
    )
    assert FAMILIA_ESTRUCTURA_DIFICIL in _familias(resultado.avisos)


def test_voz_pasiva_larga_dispara_aviso() -> None:
    resultado = detectar_problemas_bloque(
        _bloque("El informe final fue revisado cuidadosamente por todo el equipo directivo")
    )
    assert FAMILIA_ESTRUCTURA_DIFICIL in _familias(resultado.avisos)


def test_frase_simple_no_dispara_estructura_dificil() -> None:
    resultado = detectar_problemas_bloque(_bloque("Manana repasamos el guion antes de grabar"))
    assert FAMILIA_ESTRUCTURA_DIFICIL not in _familias(resultado.avisos)


# --- Cobertura total (invariante (a) de §0.2) y no reescritura ----------------------


def test_cobertura_total_guiones_reales(texto_guiones_reales: dict[str, str]) -> None:
    """Un resultado por bloque de respiracion, incluso sin avisos; nada se
    descarta en silencio y ninguna familia toca el texto original del bloque."""
    configuracion = Configuracion()
    for nombre, texto in texto_guiones_reales.items():
        resultado_parseo = parsear_guion(texto)
        bloques = trocear_guion(resultado_parseo, configuracion)
        resultados = detectar_problemas_guion(bloques, configuracion)
        assert len(resultados) == len(bloques), nombre
        for resultado, bloque in zip(resultados, bloques, strict=True):
            assert resultado.bloque is bloque
            assert bloque.texto == resultado.bloque.texto  # el original no se toca


def test_ninguna_familia_salvo_sin_punto_admite_particion(
    texto_guiones_reales: dict[str, str],
) -> None:
    configuracion = Configuracion()
    for texto in texto_guiones_reales.values():
        resultado_parseo = parsear_guion(texto)
        bloques = trocear_guion(resultado_parseo, configuracion)
        for resultado in detectar_problemas_guion(bloques, configuracion):
            for aviso in resultado.avisos:
                if aviso.familia != FAMILIA_SIN_PUNTO_RESPIRACION:
                    assert aviso.admite_particion is False
                    assert aviso.particion_sugerida is None


# --- Validacion de configuracion (§0.2, validacion de entradas) ---------------------


def test_umbral_no_positivo_es_rechazado() -> None:
    with pytest.raises(ValueError, match="umbral_palabras_sin_puntuacion"):
        Configuracion(umbral_palabras_sin_puntuacion=0)
