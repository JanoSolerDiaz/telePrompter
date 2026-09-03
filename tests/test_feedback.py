"""Tests de los tropiezos marcados en grabacion (tarea R-03).

Cubren el lado Python del requisito 2 ("volcado a FEEDBACK.md... con escena,
bloque y texto exacto") y del requisito 3 ("destacados en la siguiente
validacion"): validar el `.json` que exporta el boton "Exportar tropiezos" del
reproductor, volcarlo a `FEEDBACK.md` (carpeta de salida del guion, distinto
de `roadmap/FEEDBACK.md`) y releerlo para saber que bloques destacar. El lado
del navegador (marcar/desmarcar el bloque, persistir en `localStorage`,
exportar) no tiene aqui un ejecutor de JavaScript: se cubre con aserciones
sobre el HTML generado en `tests/test_reproductor.py`, mismo tratamiento que
el resto de logica de `guion.js` en la suite.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from feedback import (
    EscenaTropiezos,
    RegistroFeedbackError,
    RegistroTropiezos,
    TropiezoBloque,
    cargar_registro_tropiezos,
    registrar_tropiezos_en_feedback,
    tropiezos_marcados_por_escena,
)


def _registro_valido(guion_nombre: str = "mi-guion") -> dict[str, Any]:
    return {
        "version": 1,
        "guion": guion_nombre,
        "generado": "2026-09-03T10:00:00.000Z",
        "escenas": [
            {
                "numero": 1,
                "titulo": "Apertura",
                "tropiezos": [
                    {"indice_bloque": 0, "texto": "Texto dificil de decir."},
                    {"indice_bloque": 2, "texto": "Otro trabalenguas."},
                ],
            },
            {"numero": 2, "titulo": "Cierre", "tropiezos": []},
        ],
    }


def _escribir_registro(tmp_path: Path, contenido: object, nombre: str = "tropiezos.json") -> Path:
    ruta = tmp_path / nombre
    ruta.write_text(json.dumps(contenido), encoding="utf-8")
    return ruta


# --- cargar_registro_tropiezos ---------------------------------------------------------


def test_carga_un_registro_valido(tmp_path: Path) -> None:
    ruta = _escribir_registro(tmp_path, _registro_valido())
    registro = cargar_registro_tropiezos(ruta, nombre_guion="mi-guion")

    assert registro.guion == "mi-guion"
    assert len(registro.escenas) == 2
    escena_1 = registro.escenas[0]
    assert escena_1.numero_escena == 1
    assert escena_1.titulo == "Apertura"
    assert escena_1.tropiezos == (
        TropiezoBloque(indice_bloque=0, texto="Texto dificil de decir."),
        TropiezoBloque(indice_bloque=2, texto="Otro trabalenguas."),
    )
    assert registro.escenas[1].tropiezos == ()


def test_rechaza_archivo_inexistente(tmp_path: Path) -> None:
    with pytest.raises(RegistroFeedbackError, match="No existe"):
        cargar_registro_tropiezos(tmp_path / "no-existe.json", nombre_guion="mi-guion")


def test_rechaza_json_invalido(tmp_path: Path) -> None:
    ruta = tmp_path / "tropiezos.json"
    ruta.write_text("{esto no es json", encoding="utf-8")
    with pytest.raises(RegistroFeedbackError, match="JSON valido"):
        cargar_registro_tropiezos(ruta, nombre_guion="mi-guion")


def test_rechaza_un_registro_de_otro_guion(tmp_path: Path) -> None:
    ruta = _escribir_registro(tmp_path, _registro_valido(guion_nombre="otro-guion"))
    with pytest.raises(RegistroFeedbackError, match="otro guion"):
        cargar_registro_tropiezos(ruta, nombre_guion="mi-guion")


def test_sin_clave_escenas_se_asume_registro_vacio(tmp_path: Path) -> None:
    contenido = _registro_valido()
    del contenido["escenas"]
    ruta = _escribir_registro(tmp_path, contenido)
    registro = cargar_registro_tropiezos(ruta, nombre_guion="mi-guion")
    assert registro.escenas == ()


def test_rechaza_escenas_que_no_es_una_lista(tmp_path: Path) -> None:
    contenido = _registro_valido()
    contenido["escenas"] = "no es una lista"
    ruta = _escribir_registro(tmp_path, contenido)
    with pytest.raises(RegistroFeedbackError, match="lista"):
        cargar_registro_tropiezos(ruta, nombre_guion="mi-guion")


def test_rechaza_tropiezo_sin_indice_bloque(tmp_path: Path) -> None:
    contenido = _registro_valido()
    del contenido["escenas"][0]["tropiezos"][0]["indice_bloque"]
    ruta = _escribir_registro(tmp_path, contenido)
    with pytest.raises(RegistroFeedbackError, match="indice_bloque"):
        cargar_registro_tropiezos(ruta, nombre_guion="mi-guion")


def test_rechaza_indice_bloque_negativo(tmp_path: Path) -> None:
    contenido = _registro_valido()
    contenido["escenas"][0]["tropiezos"][0]["indice_bloque"] = -1
    ruta = _escribir_registro(tmp_path, contenido)
    with pytest.raises(RegistroFeedbackError, match="negativo"):
        cargar_registro_tropiezos(ruta, nombre_guion="mi-guion")


def test_rechaza_texto_vacio(tmp_path: Path) -> None:
    contenido = _registro_valido()
    contenido["escenas"][0]["tropiezos"][0]["texto"] = "   "
    ruta = _escribir_registro(tmp_path, contenido)
    with pytest.raises(RegistroFeedbackError, match="texto"):
        cargar_registro_tropiezos(ruta, nombre_guion="mi-guion")


def test_rechaza_texto_con_pipe(tmp_path: Path) -> None:
    contenido = _registro_valido()
    contenido["escenas"][0]["tropiezos"][0]["texto"] = "rompe | la tabla"
    ruta = _escribir_registro(tmp_path, contenido)
    with pytest.raises(RegistroFeedbackError, match=r"\|"):
        cargar_registro_tropiezos(ruta, nombre_guion="mi-guion")


def test_rechaza_texto_que_no_es_string(tmp_path: Path) -> None:
    contenido = _registro_valido()
    contenido["escenas"][0]["tropiezos"][0]["texto"] = 123
    ruta = _escribir_registro(tmp_path, contenido)
    with pytest.raises(RegistroFeedbackError, match="texto"):
        cargar_registro_tropiezos(ruta, nombre_guion="mi-guion")


# --- registrar_tropiezos_en_feedback ----------------------------------------------------


def test_registrar_tropiezos_crea_feedback_con_cabecera(tmp_path: Path) -> None:
    registro = RegistroTropiezos(
        guion="mi-guion",
        escenas=(
            EscenaTropiezos(
                numero_escena=1,
                titulo="Apertura",
                tropiezos=(TropiezoBloque(indice_bloque=0, texto="Texto dificil."),),
            ),
        ),
    )

    n = registrar_tropiezos_en_feedback(tmp_path, registro, fecha="2026-09-03")

    assert n == 1
    contenido = (tmp_path / "FEEDBACK.md").read_text(encoding="utf-8")
    assert "# FEEDBACK — mi-guion" in contenido
    assert "| 2026-09-03 | 1 | 0 | Texto dificil. | nuevo |" in contenido


def test_registrar_tropiezos_no_duplica_en_una_segunda_pasada(tmp_path: Path) -> None:
    registro = RegistroTropiezos(
        guion="mi-guion",
        escenas=(
            EscenaTropiezos(
                numero_escena=1,
                titulo="Apertura",
                tropiezos=(TropiezoBloque(indice_bloque=0, texto="Texto dificil."),),
            ),
        ),
    )
    registrar_tropiezos_en_feedback(tmp_path, registro, fecha="2026-09-03")

    n_segunda = registrar_tropiezos_en_feedback(tmp_path, registro, fecha="2026-09-04")

    assert n_segunda == 0
    contenido = (tmp_path / "FEEDBACK.md").read_text(encoding="utf-8")
    assert contenido.count("Texto dificil.") == 1


def test_registrar_tropiezos_anade_solo_las_filas_nuevas(tmp_path: Path) -> None:
    primero = RegistroTropiezos(
        guion="mi-guion",
        escenas=(
            EscenaTropiezos(
                numero_escena=1,
                titulo="Apertura",
                tropiezos=(TropiezoBloque(indice_bloque=0, texto="Primer tropiezo."),),
            ),
        ),
    )
    registrar_tropiezos_en_feedback(tmp_path, primero, fecha="2026-09-03")

    segundo = RegistroTropiezos(
        guion="mi-guion",
        escenas=(
            EscenaTropiezos(
                numero_escena=1,
                titulo="Apertura",
                tropiezos=(
                    TropiezoBloque(indice_bloque=0, texto="Primer tropiezo."),
                    TropiezoBloque(indice_bloque=1, texto="Segundo tropiezo."),
                ),
            ),
        ),
    )
    n = registrar_tropiezos_en_feedback(tmp_path, segundo, fecha="2026-09-04")

    assert n == 1
    contenido = (tmp_path / "FEEDBACK.md").read_text(encoding="utf-8")
    assert "Primer tropiezo." in contenido
    assert "Segundo tropiezo." in contenido


def test_registrar_tropiezos_hace_copia_de_seguridad_si_ya_existia(tmp_path: Path) -> None:
    registro = RegistroTropiezos(
        guion="mi-guion",
        escenas=(
            EscenaTropiezos(
                numero_escena=1,
                titulo="Apertura",
                tropiezos=(TropiezoBloque(indice_bloque=0, texto="Primer tropiezo."),),
            ),
        ),
    )
    registrar_tropiezos_en_feedback(tmp_path, registro, fecha="2026-09-03")

    otro = RegistroTropiezos(
        guion="mi-guion",
        escenas=(
            EscenaTropiezos(
                numero_escena=1,
                titulo="Apertura",
                tropiezos=(TropiezoBloque(indice_bloque=1, texto="Segundo tropiezo."),),
            ),
        ),
    )
    registrar_tropiezos_en_feedback(tmp_path, otro, fecha="2026-09-04")

    copias = list(tmp_path.glob("FEEDBACK.md.bak-*"))
    assert len(copias) == 1
    assert "Primer tropiezo." in copias[0].read_text(encoding="utf-8")


def test_registrar_tropiezos_sin_filas_nuevas_no_toca_el_archivo(tmp_path: Path) -> None:
    registro = RegistroTropiezos(
        guion="mi-guion",
        escenas=(
            EscenaTropiezos(
                numero_escena=1,
                titulo="Apertura",
                tropiezos=(TropiezoBloque(indice_bloque=0, texto="Primer tropiezo."),),
            ),
        ),
    )
    registrar_tropiezos_en_feedback(tmp_path, registro, fecha="2026-09-03")
    escrito_en = (tmp_path / "FEEDBACK.md").stat().st_mtime

    registrar_tropiezos_en_feedback(tmp_path, registro, fecha="2026-09-04")

    assert (tmp_path / "FEEDBACK.md").stat().st_mtime == escrito_en
    assert not list(tmp_path.glob("FEEDBACK.md.bak-*"))


def test_registrar_tropiezos_de_un_registro_sin_tropiezos_no_anade_nada(tmp_path: Path) -> None:
    registro = RegistroTropiezos(guion="mi-guion", escenas=())
    n = registrar_tropiezos_en_feedback(tmp_path, registro, fecha="2026-09-03")
    assert n == 0
    assert not (tmp_path / "FEEDBACK.md").exists()


# --- tropiezos_marcados_por_escena ------------------------------------------------------


def test_sin_feedback_md_no_hay_nada_marcado(tmp_path: Path) -> None:
    assert tropiezos_marcados_por_escena(tmp_path) == {}


def test_tropiezos_marcados_agrupa_por_escena(tmp_path: Path) -> None:
    registro = RegistroTropiezos(
        guion="mi-guion",
        escenas=(
            EscenaTropiezos(
                numero_escena=1,
                titulo="Apertura",
                tropiezos=(
                    TropiezoBloque(indice_bloque=0, texto="Uno."),
                    TropiezoBloque(indice_bloque=1, texto="Dos."),
                ),
            ),
            EscenaTropiezos(
                numero_escena=3,
                titulo="Cierre",
                tropiezos=(TropiezoBloque(indice_bloque=0, texto="Tres."),),
            ),
        ),
    )
    registrar_tropiezos_en_feedback(tmp_path, registro, fecha="2026-09-03")

    marcados = tropiezos_marcados_por_escena(tmp_path)

    assert marcados == {1: frozenset({"Uno.", "Dos."}), 3: frozenset({"Tres."})}


def test_fila_marcada_como_resuelto_deja_de_destacarse(tmp_path: Path) -> None:
    registro = RegistroTropiezos(
        guion="mi-guion",
        escenas=(
            EscenaTropiezos(
                numero_escena=1,
                titulo="Apertura",
                tropiezos=(TropiezoBloque(indice_bloque=0, texto="Texto dificil."),),
            ),
        ),
    )
    registrar_tropiezos_en_feedback(tmp_path, registro, fecha="2026-09-03")
    ruta = tmp_path / "FEEDBACK.md"
    ruta.write_text(ruta.read_text(encoding="utf-8").replace("| nuevo |", "| resuelto |"))

    assert tropiezos_marcados_por_escena(tmp_path) == {}


def test_edicion_manual_de_una_fila_nueva_se_respeta(tmp_path: Path) -> None:
    """El dueno puede anadir filas a mano (mismo espiritu que
    `roadmap/FEEDBACK.md`, que cualquiera puede editar): una fila `nuevo`
    escrita a mano, no exportada por el reproductor, tambien se destaca."""
    ruta = tmp_path / "FEEDBACK.md"
    ruta.write_text(
        "# FEEDBACK — mi-guion\n\n"
        "| Fecha | Escena | Bloque | Texto exacto | Estado |\n"
        "|-------|--------|--------|---------------|--------|\n"
        "| 2026-09-03 | 5 | 1 | Anadido a mano por el dueno. | nuevo |\n",
        encoding="utf-8",
    )

    esperado = {5: frozenset({"Anadido a mano por el dueno."})}
    assert tropiezos_marcados_por_escena(tmp_path) == esperado
