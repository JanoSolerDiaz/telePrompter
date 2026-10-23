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
    assert escena_1.tropiezos[0].instante_toma_segundos is None
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


# --- instante_toma_segundos (R-34) ------------------------------------------------------


def test_carga_el_instante_de_toma_cuando_esta_presente(tmp_path: Path) -> None:
    contenido = _registro_valido()
    contenido["escenas"][0]["tropiezos"][0]["instante_toma_segundos"] = 47.0
    ruta = _escribir_registro(tmp_path, contenido)
    registro = cargar_registro_tropiezos(ruta, nombre_guion="mi-guion")
    assert registro.escenas[0].tropiezos[0].instante_toma_segundos == 47.0
    # El segundo tropiezo del fixture no trae el campo (archivo version 1).
    assert registro.escenas[0].tropiezos[1].instante_toma_segundos is None


def test_rechaza_instante_de_toma_negativo(tmp_path: Path) -> None:
    contenido = _registro_valido()
    contenido["escenas"][0]["tropiezos"][0]["instante_toma_segundos"] = -1.0
    ruta = _escribir_registro(tmp_path, contenido)
    with pytest.raises(RegistroFeedbackError, match="negativo"):
        cargar_registro_tropiezos(ruta, nombre_guion="mi-guion")


def test_rechaza_instante_de_toma_que_no_es_numerico(tmp_path: Path) -> None:
    contenido = _registro_valido()
    contenido["escenas"][0]["tropiezos"][0]["instante_toma_segundos"] = "no numerico"
    ruta = _escribir_registro(tmp_path, contenido)
    with pytest.raises(RegistroFeedbackError, match="instante_toma_segundos"):
        cargar_registro_tropiezos(ruta, nombre_guion="mi-guion")


# --- numero_toma (R-36) -------------------------------------------------------------------


def test_carga_el_numero_de_toma_cuando_esta_presente(tmp_path: Path) -> None:
    contenido = _registro_valido()
    contenido["escenas"][0]["tropiezos"][0]["numero_toma"] = 2
    ruta = _escribir_registro(tmp_path, contenido)
    registro = cargar_registro_tropiezos(ruta, nombre_guion="mi-guion")
    assert registro.escenas[0].tropiezos[0].numero_toma == 2
    # El segundo tropiezo del fixture no trae el campo (archivo anterior a R-36).
    assert registro.escenas[0].tropiezos[1].numero_toma is None


def test_rechaza_numero_de_toma_menor_que_uno(tmp_path: Path) -> None:
    contenido = _registro_valido()
    contenido["escenas"][0]["tropiezos"][0]["numero_toma"] = 0
    ruta = _escribir_registro(tmp_path, contenido)
    with pytest.raises(RegistroFeedbackError, match="al menos 1"):
        cargar_registro_tropiezos(ruta, nombre_guion="mi-guion")


def test_rechaza_numero_de_toma_que_no_es_numerico(tmp_path: Path) -> None:
    contenido = _registro_valido()
    contenido["escenas"][0]["tropiezos"][0]["numero_toma"] = "no numerico"
    ruta = _escribir_registro(tmp_path, contenido)
    with pytest.raises(RegistroFeedbackError, match="numero_toma"):
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
    assert (
        "| Fecha | Escena | Bloque | Texto exacto | Toma | ¿Toma buena? | Instante | Estado |"
        in contenido
    )
    # Sin numero_toma ni instante_toma_segundos (no se pasaron al fixture): columnas vacias.
    assert "| 2026-09-03 | 1 | 0 | Texto dificil. |  |  |  | nuevo |" in contenido


def test_registrar_tropiezos_formatea_el_instante_de_toma_en_mm_ss(tmp_path: Path) -> None:
    registro = RegistroTropiezos(
        guion="mi-guion",
        escenas=(
            EscenaTropiezos(
                numero_escena=1,
                titulo="Apertura",
                tropiezos=(
                    TropiezoBloque(
                        indice_bloque=0, texto="Texto dificil.", instante_toma_segundos=47.0
                    ),
                ),
            ),
        ),
    )

    registrar_tropiezos_en_feedback(tmp_path, registro, fecha="2026-09-03")

    contenido = (tmp_path / "FEEDBACK.md").read_text(encoding="utf-8")
    # Sin numero_toma (no se paso): columnas «Toma»/«¿Toma buena?» vacias, «Instante» con el valor.
    assert "| 2026-09-03 | 1 | 0 | Texto dificil. |  |  | 00:47 | nuevo |" in contenido


def test_registrar_tropiezos_incluye_el_numero_de_toma(tmp_path: Path) -> None:
    registro = RegistroTropiezos(
        guion="mi-guion",
        escenas=(
            EscenaTropiezos(
                numero_escena=1,
                titulo="Apertura",
                tropiezos=(
                    TropiezoBloque(
                        indice_bloque=0,
                        texto="Texto dificil.",
                        numero_toma=2,
                        instante_toma_segundos=47.0,
                    ),
                ),
            ),
        ),
    )

    registrar_tropiezos_en_feedback(tmp_path, registro, fecha="2026-09-03")

    contenido = (tmp_path / "FEEDBACK.md").read_text(encoding="utf-8")
    # Sin tomas_por_escena (no se paso): «¿Toma buena?» vacia aunque haya numero_toma.
    assert "| 2026-09-03 | 1 | 0 | Texto dificil. | 2 |  | 00:47 | nuevo |" in contenido


# --- ¿Toma buena? (R-37) -----------------------------------------------------------------


def _toma(numero: int, buena: bool) -> dict[str, object]:
    return {"numero": numero, "duracion_segundos": 4.0, "nota": "", "buena": buena}


def _tomas_por_escena(escenas: dict[int, dict[str, object]]) -> dict[str, object]:
    """Mismo contenedor que `EstadoProyecto.tomas` (claves de escena en texto)."""
    return {str(numero): valor for numero, valor in escenas.items()}


def test_registrar_tropiezos_marca_toma_buena_cuando_coincide(tmp_path: Path) -> None:
    registro = RegistroTropiezos(
        guion="mi-guion",
        escenas=(
            EscenaTropiezos(
                numero_escena=3,
                titulo="Escena",
                tropiezos=(
                    TropiezoBloque(indice_bloque=0, texto="Texto A.", numero_toma=2),
                    TropiezoBloque(indice_bloque=1, texto="Texto B.", numero_toma=1),
                ),
            ),
        ),
    )
    tomas = _tomas_por_escena({3: {"titulo": "Escena", "tomas": [_toma(1, False), _toma(2, True)]}})

    registrar_tropiezos_en_feedback(tmp_path, registro, fecha="2026-09-03", tomas_por_escena=tomas)

    contenido = (tmp_path / "FEEDBACK.md").read_text(encoding="utf-8")
    assert "| 2026-09-03 | 3 | 0 | Texto A. | 2 | sí |  | nuevo |" in contenido
    assert "| 2026-09-03 | 3 | 1 | Texto B. | 1 | no |  | nuevo |" in contenido


def test_registrar_tropiezos_toma_buena_vacia_sin_ninguna_toma_marcada_buena(
    tmp_path: Path,
) -> None:
    registro = RegistroTropiezos(
        guion="mi-guion",
        escenas=(
            EscenaTropiezos(
                numero_escena=3,
                titulo="Escena",
                tropiezos=(TropiezoBloque(indice_bloque=0, texto="Texto A.", numero_toma=1),),
            ),
        ),
    )
    tomas = _tomas_por_escena({3: {"titulo": "Escena", "tomas": [_toma(1, False)]}})

    registrar_tropiezos_en_feedback(tmp_path, registro, fecha="2026-09-03", tomas_por_escena=tomas)

    contenido = (tmp_path / "FEEDBACK.md").read_text(encoding="utf-8")
    assert "| 2026-09-03 | 3 | 0 | Texto A. | 1 |  |  | nuevo |" in contenido


def test_registrar_tropiezos_toma_buena_vacia_si_la_escena_no_esta_en_tomas_por_escena(
    tmp_path: Path,
) -> None:
    registro = RegistroTropiezos(
        guion="mi-guion",
        escenas=(
            EscenaTropiezos(
                numero_escena=3,
                titulo="Escena",
                tropiezos=(TropiezoBloque(indice_bloque=0, texto="Texto A.", numero_toma=1),),
            ),
        ),
    )

    registrar_tropiezos_en_feedback(
        tmp_path, registro, fecha="2026-09-03", tomas_por_escena=_tomas_por_escena({})
    )

    contenido = (tmp_path / "FEEDBACK.md").read_text(encoding="utf-8")
    assert "| 2026-09-03 | 3 | 0 | Texto A. | 1 |  |  | nuevo |" in contenido


def test_registrar_tropiezos_toma_buena_vacia_si_el_tropiezo_no_trae_numero_toma(
    tmp_path: Path,
) -> None:
    registro = RegistroTropiezos(
        guion="mi-guion",
        escenas=(
            EscenaTropiezos(
                numero_escena=3,
                titulo="Escena",
                tropiezos=(TropiezoBloque(indice_bloque=0, texto="Texto A."),),
            ),
        ),
    )
    tomas = _tomas_por_escena({3: {"titulo": "Escena", "tomas": [_toma(1, True)]}})

    registrar_tropiezos_en_feedback(tmp_path, registro, fecha="2026-09-03", tomas_por_escena=tomas)

    contenido = (tmp_path / "FEEDBACK.md").read_text(encoding="utf-8")
    assert "| 2026-09-03 | 3 | 0 | Texto A. |  |  |  | nuevo |" in contenido


def test_registrar_tropiezos_no_recalcula_una_fila_de_antes_de_r37(tmp_path: Path) -> None:
    # FEEDBACK.md escrito por R-36, antes de R-37: con columna Toma, sin ¿Toma buena?.
    ruta = tmp_path / "FEEDBACK.md"
    ruta.write_text(
        "# FEEDBACK — mi-guion\n\n"
        "| Fecha | Escena | Bloque | Texto exacto | Toma | Instante | Estado |\n"
        "|-------|--------|--------|---------------|------|----------|--------|\n"
        "| 2026-09-03 | 3 | 0 | Texto A. | 1 | 00:47 | nuevo |\n",
        encoding="utf-8",
    )
    registro = RegistroTropiezos(
        guion="mi-guion",
        escenas=(
            EscenaTropiezos(
                numero_escena=3,
                titulo="Escena",
                tropiezos=(
                    TropiezoBloque(
                        indice_bloque=0,
                        texto="Texto A.",
                        numero_toma=1,
                        instante_toma_segundos=47.0,
                    ),
                ),
            ),
        ),
    )
    tomas = _tomas_por_escena({3: {"titulo": "Escena", "tomas": [_toma(1, True)]}})

    n = registrar_tropiezos_en_feedback(
        tmp_path, registro, fecha="2026-09-04", tomas_por_escena=tomas
    )

    assert n == 0
    contenido = ruta.read_text(encoding="utf-8")
    assert contenido.count("Texto A.") == 1
    assert "sí" not in contenido


def test_registrar_tropiezos_sobre_un_feedback_de_la_version_2_no_duplica_filas(
    tmp_path: Path,
) -> None:
    # FEEDBACK.md escrito por R-34, antes de R-36: con columna Instante, sin Toma.
    ruta = tmp_path / "FEEDBACK.md"
    ruta.write_text(
        "# FEEDBACK — mi-guion\n\n"
        "| Fecha | Escena | Bloque | Texto exacto | Instante | Estado |\n"
        "|-------|--------|--------|---------------|----------|--------|\n"
        "| 2026-09-03 | 1 | 0 | Texto dificil. | 00:47 | nuevo |\n",
        encoding="utf-8",
    )
    registro = RegistroTropiezos(
        guion="mi-guion",
        escenas=(
            EscenaTropiezos(
                numero_escena=1,
                titulo="Apertura",
                tropiezos=(
                    TropiezoBloque(
                        indice_bloque=0, texto="Texto dificil.", instante_toma_segundos=47.0
                    ),
                ),
            ),
        ),
    )

    n = registrar_tropiezos_en_feedback(tmp_path, registro, fecha="2026-09-04")

    assert n == 0
    assert ruta.read_text(encoding="utf-8").count("Texto dificil.") == 1


def test_registrar_tropiezos_sobre_un_feedback_de_la_version_1_no_duplica_filas(
    tmp_path: Path,
) -> None:
    # FEEDBACK.md escrito por una version anterior a R-34: sin columna Instante.
    ruta = tmp_path / "FEEDBACK.md"
    ruta.write_text(
        "# FEEDBACK — mi-guion\n\n"
        "| Fecha | Escena | Bloque | Texto exacto | Estado |\n"
        "|-------|--------|--------|---------------|--------|\n"
        "| 2026-09-03 | 1 | 0 | Texto dificil. | nuevo |\n",
        encoding="utf-8",
    )
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

    n = registrar_tropiezos_en_feedback(tmp_path, registro, fecha="2026-09-04")

    assert n == 0
    assert ruta.read_text(encoding="utf-8").count("Texto dificil.") == 1


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
