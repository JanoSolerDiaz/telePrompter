"""Tests del registro de tomas por escena (tarea R-02).

Cubren el lado Python del requisito 3 ("volcado a un archivo... legible por la
fase de montaje y por el dueno"): validar el `.json` que exporta el boton
"Exportar parte de rodaje" del reproductor y fusionarlo en `estado.json`. El
lado del navegador (cronometrar la toma, marcarla como buena, la nota rapida,
persistir en `localStorage`) no tiene aqui un ejecutor de JavaScript: se cubre
con aserciones sobre el HTML generado en `tests/test_reproductor.py`, mismo
tratamiento que el resto de logica de `guion.js` en la suite.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from config import Configuracion
from estado import estado_inicial
from tomas import (
    ParteDeRodaje,
    RegistroTomasError,
    Toma,
    TomasEscena,
    cargar_parte_de_rodaje,
    duracion_toma_buena,
    registrar_tomas,
)

GUION_MINIMO = "## BLOQUE 1 — Apertura (0:00 - 0:15)\n\n**LOCUCIÓN**\n\n> Hola.\n"


@pytest.fixture
def guion(tmp_path: Path) -> Path:
    ruta = tmp_path / "guion.md"
    ruta.write_text(GUION_MINIMO, encoding="utf-8")
    return ruta


def _parte_valido(guion_nombre: str = "mi-guion") -> dict[str, Any]:
    return {
        "version": 1,
        "guion": guion_nombre,
        "generado": "2026-09-03T10:00:00.000Z",
        "escenas": [
            {
                "numero": 1,
                "titulo": "Apertura",
                "tomas": [
                    {"numero": 1, "duracion_segundos": 12.3, "nota": "muy rapido", "buena": False},
                    {"numero": 2, "duracion_segundos": 14.1, "nota": "", "buena": True},
                ],
            },
            {"numero": 2, "titulo": "Cierre", "tomas": []},
        ],
    }


def _escribir_parte(tmp_path: Path, contenido: object, nombre: str = "tomas.json") -> Path:
    ruta = tmp_path / nombre
    ruta.write_text(json.dumps(contenido), encoding="utf-8")
    return ruta


# --- cargar_parte_de_rodaje ----------------------------------------------------------


def test_carga_un_parte_valido(tmp_path: Path) -> None:
    ruta = _escribir_parte(tmp_path, _parte_valido())
    parte = cargar_parte_de_rodaje(ruta, nombre_guion="mi-guion")

    assert parte.guion == "mi-guion"
    assert len(parte.escenas) == 2
    escena_1 = parte.escenas[0]
    assert escena_1.numero_escena == 1
    assert escena_1.titulo == "Apertura"
    assert escena_1.tomas == (
        Toma(numero=1, duracion_segundos=12.3, nota="muy rapido", buena=False),
        Toma(numero=2, duracion_segundos=14.1, nota="", buena=True),
    )
    assert parte.escenas[1].tomas == ()


def test_rechaza_archivo_inexistente(tmp_path: Path) -> None:
    with pytest.raises(RegistroTomasError, match="No existe"):
        cargar_parte_de_rodaje(tmp_path / "no-existe.json", nombre_guion="mi-guion")


def test_rechaza_json_invalido(tmp_path: Path) -> None:
    ruta = tmp_path / "tomas.json"
    ruta.write_text("{esto no es json", encoding="utf-8")
    with pytest.raises(RegistroTomasError, match="JSON valido"):
        cargar_parte_de_rodaje(ruta, nombre_guion="mi-guion")


def test_rechaza_un_parte_de_otro_guion(tmp_path: Path) -> None:
    ruta = _escribir_parte(tmp_path, _parte_valido(guion_nombre="otro-guion"))
    with pytest.raises(RegistroTomasError, match="otro guion"):
        cargar_parte_de_rodaje(ruta, nombre_guion="mi-guion")


def test_sin_clave_escenas_se_asume_parte_vacio(tmp_path: Path) -> None:
    contenido = _parte_valido()
    del contenido["escenas"]
    ruta = _escribir_parte(tmp_path, contenido)
    parte = cargar_parte_de_rodaje(ruta, nombre_guion="mi-guion")
    assert parte.escenas == ()


def test_rechaza_escenas_que_no_es_una_lista(tmp_path: Path) -> None:
    contenido = _parte_valido()
    contenido["escenas"] = "no es una lista"
    ruta = _escribir_parte(tmp_path, contenido)
    with pytest.raises(RegistroTomasError, match="lista"):
        cargar_parte_de_rodaje(ruta, nombre_guion="mi-guion")


def test_rechaza_toma_sin_numero(tmp_path: Path) -> None:
    contenido = _parte_valido()
    del contenido["escenas"][0]["tomas"][0]["numero"]
    ruta = _escribir_parte(tmp_path, contenido)
    with pytest.raises(RegistroTomasError, match="numero"):
        cargar_parte_de_rodaje(ruta, nombre_guion="mi-guion")


def test_rechaza_toma_con_duracion_negativa(tmp_path: Path) -> None:
    contenido = _parte_valido()
    contenido["escenas"][0]["tomas"][0]["duracion_segundos"] = -1
    ruta = _escribir_parte(tmp_path, contenido)
    with pytest.raises(RegistroTomasError, match="negativa"):
        cargar_parte_de_rodaje(ruta, nombre_guion="mi-guion")


def test_rechaza_toma_con_numero_no_positivo(tmp_path: Path) -> None:
    contenido = _parte_valido()
    contenido["escenas"][0]["tomas"][0]["numero"] = 0
    ruta = _escribir_parte(tmp_path, contenido)
    with pytest.raises(RegistroTomasError, match="positivo"):
        cargar_parte_de_rodaje(ruta, nombre_guion="mi-guion")


def test_rechaza_nota_que_no_es_texto(tmp_path: Path) -> None:
    contenido = _parte_valido()
    contenido["escenas"][0]["tomas"][0]["nota"] = 123
    ruta = _escribir_parte(tmp_path, contenido)
    with pytest.raises(RegistroTomasError, match="nota"):
        cargar_parte_de_rodaje(ruta, nombre_guion="mi-guion")


def test_toma_sin_nota_ni_buena_usa_defectos(tmp_path: Path) -> None:
    contenido = _parte_valido()
    del contenido["escenas"][0]["tomas"][0]["nota"]
    del contenido["escenas"][0]["tomas"][0]["buena"]
    ruta = _escribir_parte(tmp_path, contenido)
    parte = cargar_parte_de_rodaje(ruta, nombre_guion="mi-guion")
    assert parte.escenas[0].tomas[0].nota == ""
    assert parte.escenas[0].tomas[0].buena is False


# --- registrar_tomas ------------------------------------------------------------------


def test_registrar_tomas_anade_las_escenas_con_tomas(guion: Path) -> None:
    estado = estado_inicial(guion, Configuracion())
    parte = ParteDeRodaje(
        guion="guion",
        escenas=(
            TomasEscena(
                numero_escena=1,
                titulo="Apertura",
                tomas=(Toma(numero=1, duracion_segundos=10.0, nota="", buena=True),),
            ),
        ),
    )

    registrar_tomas(estado, parte)

    assert estado.tomas == {
        "1": {
            "titulo": "Apertura",
            "tomas": [{"numero": 1, "duracion_segundos": 10.0, "nota": "", "buena": True}],
        }
    }


def test_registrar_tomas_ignora_escenas_sin_tomas(guion: Path) -> None:
    estado = estado_inicial(guion, Configuracion())
    parte = ParteDeRodaje(
        guion="guion",
        escenas=(TomasEscena(numero_escena=1, titulo="Apertura", tomas=()),),
    )

    registrar_tomas(estado, parte)

    assert estado.tomas == {}


def test_registrar_tomas_reemplaza_solo_la_escena_exportada(guion: Path) -> None:
    estado = estado_inicial(guion, Configuracion())
    estado.tomas = {
        "1": {
            "titulo": "Apertura",
            "tomas": [{"numero": 1, "duracion_segundos": 5.0, "nota": "", "buena": False}],
        },
        "2": {
            "titulo": "Cierre",
            "tomas": [{"numero": 1, "duracion_segundos": 8.0, "nota": "", "buena": True}],
        },
    }
    parte = ParteDeRodaje(
        guion="guion",
        escenas=(
            TomasEscena(
                numero_escena=1,
                titulo="Apertura",
                tomas=(
                    Toma(numero=1, duracion_segundos=5.0, nota="", buena=False),
                    Toma(numero=2, duracion_segundos=6.0, nota="mejor", buena=True),
                ),
            ),
        ),
    )

    registrar_tomas(estado, parte)

    # La escena 1 se reemplaza con el historial completo recien exportado...
    assert len(estado.tomas["1"]["tomas"]) == 2
    assert estado.tomas["1"]["tomas"][1]["buena"] is True
    # ...y la escena 2, que este parte ni menciona, se conserva intacta.
    assert estado.tomas["2"]["tomas"] == [
        {"numero": 1, "duracion_segundos": 8.0, "nota": "", "buena": True}
    ]


def test_registrar_tomas_es_el_dato_persistido_por_guardar_y_cargar_estado(
    guion: Path, tmp_path: Path
) -> None:
    from estado import cargar_estado, guardar_estado

    estado = estado_inicial(guion, Configuracion())
    parte = ParteDeRodaje(
        guion="guion",
        escenas=(
            TomasEscena(
                numero_escena=1,
                titulo="Apertura",
                tomas=(Toma(numero=1, duracion_segundos=10.0, nota="", buena=True),),
            ),
        ),
    )
    registrar_tomas(estado, parte)

    carpeta_salida = tmp_path / "guion-tarjetas"
    guardar_estado(estado, carpeta_salida)
    recargado = cargar_estado(carpeta_salida)

    assert recargado.tomas == estado.tomas


# --- `duracion_toma_buena`: criterio compartido por R-04 y R-05 --------------------


def test_duracion_toma_buena_devuelve_la_marcada_buena() -> None:
    tomas_escena = {
        "titulo": "Apertura",
        "tomas": [
            {"numero": 1, "duracion_segundos": 24.1, "nota": "repetir", "buena": False},
            {"numero": 2, "duracion_segundos": 26.3, "nota": "", "buena": True},
        ],
    }
    assert duracion_toma_buena(tomas_escena) == 26.3


def test_duracion_toma_buena_es_none_sin_ninguna_marcada() -> None:
    tomas_escena = {
        "titulo": "Apertura",
        "tomas": [{"numero": 1, "duracion_segundos": 24.1, "nota": "", "buena": False}],
    }
    assert duracion_toma_buena(tomas_escena) is None


def test_duracion_toma_buena_es_none_sin_escena_registrada() -> None:
    assert duracion_toma_buena(None) is None
