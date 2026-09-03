"""Tests del estado persistente del proyecto de guion (T-07).

Cubren el criterio de aceptacion literal: un proceso interrumpido a mitad de
escritura y relanzado reanuda sin perder el `estado.json` anterior, y la deteccion
de guion modificado por hash.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from config import Configuracion
from estado import (
    EstadoError,
    EstadoProyecto,
    avisar_si_guion_modificado,
    calcular_hash_guion,
    cargar_estado,
    estado_inicial,
    guardar_estado,
    guion_modificado,
    ruta_estado,
)
from presentacion import Nivel

GUION_MINIMO = "## BLOQUE 1 — Apertura (0:00 - 0:15)\n\n**LOCUCIÓN**\n\n> Hola.\n"


@pytest.fixture
def guion(tmp_path: Path) -> Path:
    ruta = tmp_path / "guion.md"
    ruta.write_text(GUION_MINIMO, encoding="utf-8")
    return ruta


@pytest.fixture
def carpeta_salida(tmp_path: Path) -> Path:
    return tmp_path / "guion-tarjetas"


# --- estado_inicial / calcular_hash_guion -------------------------------------------


def test_estado_inicial_recoge_ruta_hash_y_tamano_del_guion(guion: Path) -> None:
    estado = estado_inicial(guion, Configuracion())

    assert estado.guion.ruta == str(guion)
    assert estado.guion.hash_sha256 == calcular_hash_guion(guion)
    assert estado.guion.tamano_bytes == guion.stat().st_size


def test_estado_inicial_usa_la_version_de_esquema_actual(guion: Path) -> None:
    estado = estado_inicial(guion, Configuracion())
    assert estado.version_esquema == 2


def test_estado_inicial_arranca_con_colecciones_vacias(guion: Path) -> None:
    estado = estado_inicial(guion, Configuracion())
    assert estado.escenas == []
    assert estado.reescrituras == []
    assert estado.validacion == {}
    assert estado.salidas_generadas == []
    assert estado.tomas == {}
    assert estado.separador_escena.nivel is None


def test_estado_inicial_congela_la_configuracion_efectiva(guion: Path) -> None:
    configuracion = Configuracion(ppm_respaldo=100)
    estado = estado_inicial(guion, configuracion)
    assert estado.configuracion_efectiva["ppm_respaldo"] == 100


def test_hash_cambia_si_cambia_el_contenido_del_guion(guion: Path) -> None:
    hash_original = calcular_hash_guion(guion)
    guion.write_text(GUION_MINIMO + "\nMas texto.\n", encoding="utf-8")
    assert calcular_hash_guion(guion) != hash_original


# --- guardar_estado / cargar_estado (round-trip) ------------------------------------


def test_guardar_y_cargar_estado_conserva_todos_los_campos(
    guion: Path, carpeta_salida: Path
) -> None:
    original = estado_inicial(guion, Configuracion())
    original.escenas.append({"id": 1, "titulo": "Apertura"})
    original.validacion["1"] = "pendiente"

    guardar_estado(original, carpeta_salida)
    recargado = cargar_estado(carpeta_salida)

    assert recargado.guion == original.guion
    assert recargado.escenas == original.escenas
    assert recargado.validacion == original.validacion
    assert recargado.version_esquema == original.version_esquema


def test_guardar_estado_crea_la_carpeta_de_salida_si_no_existe(
    guion: Path, carpeta_salida: Path
) -> None:
    assert not carpeta_salida.exists()
    guardar_estado(estado_inicial(guion, Configuracion()), carpeta_salida)
    assert carpeta_salida.exists()


def test_guardar_estado_escribe_json_legible_por_humanos(
    guion: Path, carpeta_salida: Path
) -> None:
    ruta = guardar_estado(estado_inicial(guion, Configuracion()), carpeta_salida)
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    assert datos["version_esquema"] == 2
    assert "guion" in datos


def test_guardar_estado_no_deja_archivo_temporal_tras_escribir(
    guion: Path, carpeta_salida: Path
) -> None:
    guardar_estado(estado_inicial(guion, Configuracion()), carpeta_salida)
    assert not (carpeta_salida / "estado.json.tmp").exists()


def test_cargar_estado_sin_archivo_levanta_estado_error(carpeta_salida: Path) -> None:
    with pytest.raises(EstadoError, match="No existe"):
        cargar_estado(carpeta_salida)


def test_cargar_estado_json_corrupto_levanta_estado_error(carpeta_salida: Path) -> None:
    carpeta_salida.mkdir(parents=True)
    ruta_estado(carpeta_salida).write_text("{no es json valido", encoding="utf-8")
    with pytest.raises(EstadoError, match="corrupto"):
        cargar_estado(carpeta_salida)


def test_cargar_estado_con_estructura_incompleta_levanta_estado_error(
    carpeta_salida: Path,
) -> None:
    carpeta_salida.mkdir(parents=True)
    # `version_esquema` ya al dia pero sin la clave `guion`: la migracion no
    # necesita completarlo (ya esta en VERSION_DESTINO) y `desde_dict` debe fallar
    # con un error accionable, no con un KeyError crudo.
    ruta_estado(carpeta_salida).write_text(
        json.dumps({"version_esquema": 1}), encoding="utf-8"
    )
    with pytest.raises(EstadoError, match="incompleta"):
        cargar_estado(carpeta_salida)


# --- escritura atomica: interrupcion a mitad de escritura ---------------------------


def test_estado_anterior_sobrevive_si_falla_el_reemplazo(
    guion: Path, carpeta_salida: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Simula un corte justo antes de `os.replace`: el estado.json anterior no
    debe perderse ni quedar a medio escribir, y el temporal se limpia."""
    primero = estado_inicial(guion, Configuracion())
    primero.escenas.append({"id": 1, "titulo": "Version buena"})
    guardar_estado(primero, carpeta_salida)
    contenido_bueno = ruta_estado(carpeta_salida).read_text(encoding="utf-8")

    def replace_que_falla(_self: Path, _destino: object) -> None:
        raise OSError("corte simulado a mitad de escritura")

    monkeypatch.setattr(Path, "replace", replace_que_falla)

    segundo = estado_inicial(guion, Configuracion())
    segundo.escenas.append({"id": 1, "titulo": "Version que se pierde en el corte"})
    with pytest.raises(OSError, match="corte simulado"):
        guardar_estado(segundo, carpeta_salida)

    assert ruta_estado(carpeta_salida).read_text(encoding="utf-8") == contenido_bueno
    assert not (carpeta_salida / "estado.json.tmp").exists()


def test_proceso_relanzado_reanuda_desde_el_ultimo_guardado(
    guion: Path, carpeta_salida: Path
) -> None:
    """Criterio de aceptacion de T-07: interrumpir y relanzar no pierde progreso."""
    primera_sesion = estado_inicial(guion, Configuracion())
    primera_sesion.escenas.append({"id": 1, "titulo": "Apertura"})
    primera_sesion.validacion["1"] = "validada"
    guardar_estado(primera_sesion, carpeta_salida)

    # "Relanzar" = una nueva llamada a cargar_estado, sin memoria del proceso previo.
    estado_reanudado = cargar_estado(carpeta_salida)
    assert estado_reanudado.escenas == [{"id": 1, "titulo": "Apertura"}]
    assert estado_reanudado.validacion == {"1": "validada"}

    estado_reanudado.escenas.append({"id": 2, "titulo": "Desarrollo"})
    guardar_estado(estado_reanudado, carpeta_salida)

    estado_final = cargar_estado(carpeta_salida)
    assert len(estado_final.escenas) == 2
    assert estado_final.validacion == {"1": "validada"}


# --- guion_modificado / avisar_si_guion_modificado ----------------------------------


def test_guion_modificado_es_falso_si_no_cambio(guion: Path) -> None:
    estado = estado_inicial(guion, Configuracion())
    assert guion_modificado(estado, guion) is False


def test_guion_modificado_es_verdadero_si_cambio_el_contenido(guion: Path) -> None:
    estado = estado_inicial(guion, Configuracion())
    guion.write_text(GUION_MINIMO + "\nEscena nueva.\n", encoding="utf-8")
    assert guion_modificado(estado, guion) is True


def test_avisar_si_guion_modificado_no_avisa_si_no_cambio(
    guion: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    estado = estado_inicial(guion, Configuracion())
    assert avisar_si_guion_modificado(estado, guion) is False
    assert capsys.readouterr().err == ""


def test_avisar_si_guion_modificado_avisa_y_menciona_recalculo(
    guion: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    estado = estado_inicial(guion, Configuracion())
    guion.write_text(GUION_MINIMO + "\nEscena nueva.\n", encoding="utf-8")

    assert avisar_si_guion_modificado(estado, guion) is True
    salida = capsys.readouterr().err
    assert Nivel.AVISO.value in salida or "AVISO" in salida
    assert "recalcular" in salida


def test_a_dict_y_desde_dict_son_inversas(guion: Path) -> None:
    original = estado_inicial(guion, Configuracion())
    reconstruido = EstadoProyecto.desde_dict(original.a_dict())
    assert reconstruido == original
