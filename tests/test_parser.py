"""Tests del parser de Markdown y del separador de escenas (tarea T-08).

`test_parser_reconoce_toda_escena_del_guion_real` reemplaza al talon del mismo
nombre en `tests/test_logica_pendiente.py` (T-03), que quedaba pendiente hasta
que T-08 existiera: es su criterio de aceptacion literal, no una nota aparte.
"""

from __future__ import annotations

import pytest

from config import PATRON_ENCABEZADO_ESCENA, Configuracion
from estado import SeparadorEscena
from parser import (
    DeteccionEscenasAmbiguaError,
    dividir_en_bloques,
    elegir_separador,
    extraer_metadatos,
    parsear_guion,
)

_NUMERO_ESCENAS_ESPERADO = {
    "guion-08-busqueda-investigacion.md": 7,
    "guion-09-proyectos.md": 8,
    "guion-artefactos-lienzo.md": 8,
}


def test_parser_reconoce_toda_escena_del_guion_real(
    texto_guiones_reales: dict[str, str],
) -> None:
    """Criterio de aceptacion de T-08: 7, 8 y 8 escenas en los tres guiones reales."""
    for nombre, texto in texto_guiones_reales.items():
        resultado = parsear_guion(texto)
        numeros = [escena.numero for escena in resultado.escenas]
        assert len(resultado.escenas) == _NUMERO_ESCENAS_ESPERADO[nombre], nombre
        assert numeros == list(range(len(numeros))), f"{nombre}: numeracion con huecos"


def test_ninguna_seccion_auxiliar_entra_como_escena(
    texto_guiones_reales: dict[str, str],
) -> None:
    titulos_auxiliares_prohibidos = (
        "Capítulos",
        "Preparación antes de grabar",
        "Notas de producción",
    )
    for texto in texto_guiones_reales.values():
        resultado = parsear_guion(texto)
        titulos_escena = [e.titulo for e in resultado.escenas]
        for prohibido in titulos_auxiliares_prohibidos:
            assert not any(t.startswith(prohibido) for t in titulos_escena)


def test_secciones_auxiliares_se_conservan_no_se_descartan(
    texto_guiones_reales: dict[str, str],
) -> None:
    """Requisito 4: las secciones auxiliares aparecen en el resultado, con motivo."""
    for nombre, texto in texto_guiones_reales.items():
        resultado = parsear_guion(texto)
        assert resultado.secciones_auxiliares, nombre
        for seccion in resultado.secciones_auxiliares:
            assert seccion.motivo
            assert seccion.contenido


def test_guion_08_tiene_exactamente_estas_secciones_auxiliares(
    texto_guiones_reales: dict[str, str],
) -> None:
    resultado = parsear_guion(texto_guiones_reales["guion-08-busqueda-investigacion.md"])
    titulos = {s.titulo for s in resultado.secciones_auxiliares}
    assert any(t.startswith("Capítulos") for t in titulos)
    assert any(t.startswith("Preparación antes de grabar") for t in titulos)
    assert any(t.startswith("Notas de producción") for t in titulos)
    # El subtitulo entrecomillado tras el "#" tambien es auxiliar, no escena.
    assert any(t.startswith('"') for t in titulos)


def test_metadatos_de_cabecera_se_extraen(texto_guiones_reales: dict[str, str]) -> None:
    """Requisito 7: duracion objetivo, formato y promesa/idea unica, por guion."""
    metadatos_08 = parsear_guion(
        texto_guiones_reales["guion-08-busqueda-investigacion.md"]
    ).metadatos
    assert metadatos_08["Duración objetivo"] == "3:40 – 3:55"
    assert "Formato" in metadatos_08
    assert "Idea única del vídeo" in metadatos_08

    metadatos_lienzo = parsear_guion(
        texto_guiones_reales["guion-artefactos-lienzo.md"]
    ).metadatos
    assert metadatos_lienzo["Duración objetivo"] == "4:00 – 4:25"
    assert "Promesa del vídeo" in metadatos_lienzo


def test_posicion_de_bloques_es_trazable(texto_guiones_reales: dict[str, str]) -> None:
    """Requisito 1: cada bloque conoce su rango de lineas en el guion original."""
    texto = texto_guiones_reales["guion-08-busqueda-investigacion.md"]
    resultado = parsear_guion(texto)
    lineas = texto.splitlines()
    primera_escena = min(resultado.escenas, key=lambda e: e.linea_inicio)
    assert lineas[primera_escena.linea_inicio - 1].startswith("## BLOQUE 0")


def test_dividir_en_bloques_reconstruye_el_texto_sin_perdida(
    texto_guiones_reales: dict[str, str],
) -> None:
    """La particion en bloques es exhaustiva: no hay huecos ni solapes.

    Se compara linea a linea (via `splitlines`), no caracter a caracter: un
    salto de linea final en el archivo no se pierde como contenido (no hay
    ninguna linea despues de el), es una particularidad de `str.splitlines`.
    """
    for texto in texto_guiones_reales.values():
        bloques = dividir_en_bloques(texto)
        reconstruido = "\n".join(b.contenido for b in bloques)
        assert reconstruido == "\n".join(texto.splitlines())


def test_dividir_en_bloques_ignora_encabezados_dentro_de_valla_de_codigo() -> None:
    texto = "\n".join(
        [
            "## BLOQUE 0 — Arranque (0:00 – 0:10)",
            "**LOCUCIÓN**",
            "> hola",
            "```",
            "# esto no es un encabezado, es un comentario de codigo",
            "```",
            "## BLOQUE 1 — Cierre (0:10 – 0:20)",
            "**LOCUCIÓN**",
            "> adios",
        ]
    )
    bloques = dividir_en_bloques(texto)
    assert [b.titulo for b in bloques if b.nivel == 2] == [
        "BLOQUE 0 — Arranque (0:00 – 0:10)",
        "BLOQUE 1 — Cierre (0:10 – 0:20)",
    ]


def test_extraer_metadatos_ignora_negrita_sin_valor_en_la_misma_linea() -> None:
    texto = "\n".join(
        [
            "**Duración objetivo:** 3:40 – 3:55",
            "**Regla del criterio de producción — qué tarea mejora y cuánto:**",
            "> cita larga aparte",
        ]
    )
    metadatos = extraer_metadatos(texto)
    assert metadatos == {"Duración objetivo": "3:40 – 3:55"}


def test_separador_persistido_se_reutiliza_sin_redetectar(
    texto_guiones_reales: dict[str, str],
) -> None:
    texto = texto_guiones_reales["guion-09-proyectos.md"]
    separador_previo = elegir_separador(texto)
    resultado = parsear_guion(texto, separador=separador_previo)
    assert resultado.separador == separador_previo
    assert len(resultado.escenas) == 8


def test_sin_ningun_encabezado_que_case_el_patron_pide_confirmacion() -> None:
    """Ningun encabezado casa el patron NI tiene el rotulo de locucion: sin
    ninguna senal a favor de ser escena, no hay nada que clasificar como tal, y
    la deteccion de nivel/patron queda genuinamente sin resolver."""
    texto = "\n".join(
        [
            "# Guion sin la convencion contractual",
            "",
            "## Primera parte",
            "Texto libre sin rotulos de ningun tipo.",
            "",
            "## Segunda parte",
            "Mas texto libre, tampoco recitable segun ningun rotulo conocido.",
        ]
    )
    with pytest.raises(DeteccionEscenasAmbiguaError) as excepcion:
        elegir_separador(texto)
    alternativas = excepcion.value.alternativas
    assert alternativas, "debe proponer al menos una alternativa"
    assert all(alt.numero_escenas >= 0 for alt in alternativas)
    assert "ambigua" in str(excepcion.value).lower()


def test_conflicto_de_senales_pide_confirmacion_y_no_decide_en_silencio() -> None:
    """Un titulo en la lista negra con rotulo de locucion es un conflicto real."""
    texto = "\n".join(
        [
            "# Guion",
            "",
            "## Notas de producción",
            "**LOCUCIÓN**",
            "> esto no deberia pasar en un guion real, pero si pasa hay que preguntar",
            "",
            "## BLOQUE 0 — Arranque (0:00 – 0:10)",
            "**LOCUCIÓN**",
            "> hola",
        ]
    )
    with pytest.raises(DeteccionEscenasAmbiguaError) as excepcion:
        parsear_guion(texto)
    alternativas = excepcion.value.alternativas
    assert len(alternativas) == 2
    numeros_de_escenas = {alt.numero_escenas for alt in alternativas}
    assert numeros_de_escenas == {1, 2}


def test_conflicto_de_senales_se_resuelve_ajustando_la_lista_negra() -> None:
    """La respuesta a la ambiguedad de conflicto se persiste en la configuracion.

    No hay CLI todavia (T-08 es capa de analisis, no punto de entrada): esta
    prueba simula la persistencia de la respuesta del dueno tal y como la
    consumiria una sesion futura, ajustando `secciones_auxiliares` de la
    configuracion efectiva (que ya viaja dentro de `estado.json`, T-07).
    """
    texto = "\n".join(
        [
            "# Guion",
            "",
            "## Notas de producción",
            "**LOCUCIÓN**",
            "> el dueno decide que esto SI es escena",
            "",
            "## BLOQUE 0 — Arranque (0:00 – 0:10)",
            "**LOCUCIÓN**",
            "> hola",
        ]
    )
    with pytest.raises(DeteccionEscenasAmbiguaError):
        parsear_guion(texto)

    configuracion_ajustada = Configuracion(secciones_auxiliares=())
    resultado = parsear_guion(texto, configuracion=configuracion_ajustada)
    assert len(resultado.escenas) == 2


def test_separador_ambiguo_persistido_no_evita_conflicto_de_clasificacion() -> None:
    """El separador persistido salta la pregunta de nivel, no la de conflicto.

    Requisito 6: el conflicto depende de `secciones_auxiliares`, que puede
    cambiar sin que cambie el separador, asi que se revisa en cada pasada.
    """
    texto = "\n".join(
        [
            "# Guion",
            "",
            "## Notas de producción",
            "**LOCUCIÓN**",
            "> conflicto",
            "",
            "## BLOQUE 0 — Arranque (0:00 – 0:10)",
            "**LOCUCIÓN**",
            "> hola",
        ]
    )
    separador_ya_decidido = SeparadorEscena(nivel="##", patron=PATRON_ENCABEZADO_ESCENA)
    with pytest.raises(DeteccionEscenasAmbiguaError):
        parsear_guion(texto, separador=separador_ya_decidido)


def test_preambulo_antes_del_primer_encabezado_se_conserva() -> None:
    """Requisito 8: soporta preambulo antes del primer encabezado."""
    texto = "\n".join(
        [
            "Este texto no tiene ningun encabezado por delante todavia.",
            "",
            "## BLOQUE 0 — Arranque (0:00 – 0:10)",
            "**LOCUCIÓN**",
            "> hola",
        ]
    )
    resultado = parsear_guion(texto)
    assert "Este texto no tiene ningun encabezado" in resultado.preambulo
    assert len(resultado.escenas) == 1


def test_distribucion_por_nivel_cuenta_encabezados(texto_guiones_reales: dict[str, str]) -> None:
    """Requisito 2: analiza la distribucion de encabezados por nivel."""
    texto = texto_guiones_reales["guion-08-busqueda-investigacion.md"]
    resultado = parsear_guion(texto)
    assert resultado.distribucion_por_nivel[1] == 1
    assert resultado.distribucion_por_nivel[2] >= _NUMERO_ESCENAS_ESPERADO[
        "guion-08-busqueda-investigacion.md"
    ]


def test_dividir_en_bloques_de_texto_vacio_no_falla() -> None:
    assert dividir_en_bloques("") == []


def test_dividir_en_bloques_sin_encabezados_devuelve_lista_vacia() -> None:
    assert dividir_en_bloques("solo texto, sin ningun encabezado markdown") == []
