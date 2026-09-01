"""Tests de la normalizacion a forma dicha (tarea T-13).

`test_bateria_criterio_de_aceptacion` y `test_diccionario_sobrescribe_regla_automatica`
son el criterio de aceptacion literal de T-13. `test_normalizacion_es_reversible`
reemplaza al talon del mismo nombre en `tests/test_logica_pendiente.py`: es su
criterio de aceptacion, no una nota aparte (mismo tratamiento que T-08 a T-12).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from config import Configuracion
from normalizacion import (
    Normalizacion,
    NormalizacionError,
    aplicar_normalizaciones,
    cargar_diccionario_locucion,
    deletrear_sigla,
    deshacer_normalizaciones,
    normalizar_bloque,
    normalizar_guion,
    normalizar_texto,
    numero_a_cardinal,
    numero_a_ordinal,
)
from parser import parsear_guion
from troceo import BloqueRespiracion, trocear_guion


def _unica(normalizaciones: list[Normalizacion], familia: str) -> Normalizacion:
    coincidencias = [n for n in normalizaciones if n.familia == familia]
    mensaje = f"se esperaba una normalizacion '{familia}', hubo {coincidencias}"
    assert len(coincidencias) == 1, mensaje
    return coincidencias[0]


# --- Criterio de aceptacion literal de T-13 -----------------------------------------


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("En 2026 grabamos el vídeo.", "dos mil veintiséis"),
        ("El 15 % de los casos.", "quince por ciento"),
        ("Cuesta 1.500 € en total.", "mil quinientos euros"),
        ("Es la 1ª vez que lo probamos.", "primera"),
    ],
)
def test_bateria_criterio_de_aceptacion(texto: str, esperado: str) -> None:
    normalizaciones = normalizar_texto(texto)
    assert len(normalizaciones) == 1
    assert normalizaciones[0].propuesta == esperado


def test_diccionario_sobrescribe_regla_automatica() -> None:
    texto = "En 2026 grabamos el vídeo."
    sin_diccionario = normalizar_texto(texto)
    assert sin_diccionario[0].propuesta == "dos mil veintiséis"

    con_diccionario = normalizar_texto(texto, diccionario={"2026": "el año que viene"})
    assert len(con_diccionario) == 1
    assert con_diccionario[0].propuesta == "el año que viene"
    assert con_diccionario[0].familia == "diccionario"


# --- Lectura de cifras: cardinales, ordinales, apocope y concordancia --------------


def test_numero_a_cardinal_casos_basicos() -> None:
    assert numero_a_cardinal(0) == "cero"
    assert numero_a_cardinal(15) == "quince"
    assert numero_a_cardinal(21) == "veintiuno"
    assert numero_a_cardinal(100) == "cien"
    assert numero_a_cardinal(101) == "ciento uno"
    assert numero_a_cardinal(1500) == "mil quinientos"
    assert numero_a_cardinal(2026) == "dos mil veintiséis"
    assert numero_a_cardinal(1_000_000) == "un millón"
    assert numero_a_cardinal(2_000_000) == "dos millones"


def test_numero_a_cardinal_femenino_y_apocope() -> None:
    assert numero_a_cardinal(1, femenino=True) == "una"
    assert numero_a_cardinal(21, femenino=True) == "veintiuna"
    assert numero_a_cardinal(200, femenino=True) == "doscientas"
    assert numero_a_cardinal(1, apocope=True) == "un"
    assert numero_a_cardinal(21, apocope=True) == "veintiún"
    # Sin apocope (numero suelto, sin sustantivo detras): forma plena.
    assert numero_a_cardinal(21, apocope=False) == "veintiuno"
    # El apocope no toca la forma femenina, que ya es correcta tal cual.
    assert numero_a_cardinal(21, femenino=True, apocope=True) == "veintiuna"


def test_apocope_y_genero_se_aplican_solo_con_sustantivo_detras() -> None:
    # "21" seguido de un sustantivo masculino -> apocope.
    normalizaciones = normalizar_texto("Hay 21 alumnos apuntados.")
    assert _unica(normalizaciones, "cardinal").propuesta == "veintiún"

    # "21" seguido de un sustantivo femenino -> concordancia sin apocope.
    normalizaciones = normalizar_texto("Hay 21 personas apuntadas.")
    assert _unica(normalizaciones, "cardinal").propuesta == "veintiuna"

    # "21" sin nada detras (fin de frase) -> forma plena, sin apocope.
    normalizaciones = normalizar_texto("El total es 21.")
    assert _unica(normalizaciones, "cardinal").propuesta == "veintiuno"

    # "1 hora" -> concordancia femenina ("hora" termina en 'a').
    normalizaciones = normalizar_texto("Dedica 1 hora a repasar.")
    assert _unica(normalizaciones, "cardinal").propuesta == "una"

    # Excepcion de la heuristica: "día" termina en 'a' pero es masculino.
    normalizaciones = normalizar_texto("Pasa 1 día entero.")
    assert _unica(normalizaciones, "cardinal").propuesta == "un"


def test_numero_a_ordinal() -> None:
    assert numero_a_ordinal(1) == "primero"
    assert numero_a_ordinal(1, femenino=True) == "primera"
    assert numero_a_ordinal(1, apocope=True) == "primer"
    assert numero_a_ordinal(3, apocope=True) == "tercer"
    assert numero_a_ordinal(10) == "décimo"
    assert numero_a_ordinal(11) is None  # fuera del alcance documentado del modulo


# --- Simbolos, monedas, unidades, rangos, fracciones y siglas -----------------------


def test_moneda_con_decimales_lee_centimos() -> None:
    normalizaciones = normalizar_texto("Son 1.500,50 € en total.")
    esperado = "mil quinientos euros con cincuenta céntimos"
    assert _unica(normalizaciones, "moneda").propuesta == esperado


def test_unidad_abreviada() -> None:
    normalizaciones = normalizar_texto("Corrimos 10 km esta mañana.")
    assert _unica(normalizaciones, "unidad").propuesta == "diez kilómetros"


def test_fraccion() -> None:
    normalizaciones = normalizar_texto("Queda 3/4 del trabajo.")
    assert _unica(normalizaciones, "fraccion").propuesta == "tres partido por cuatro"


def test_rango_numerico() -> None:
    normalizaciones = normalizar_texto("Para pymes (10-250 empleados).")
    assert _unica(normalizaciones, "rango").propuesta == "diez a doscientos cincuenta"


def test_simbolos_sueltos_mayor_y_mas() -> None:
    normalizaciones = normalizar_texto("3 + 2 son cinco, y cinco > cuatro.")
    familias = {n.familia for n in normalizaciones}
    assert "simbolo" in familias
    propuestas = {n.original: n.propuesta for n in normalizaciones if n.familia == "simbolo"}
    assert propuestas == {"+": "más", ">": "mayor que"}


def test_sigla_se_deletrea_por_defecto() -> None:
    assert deletrear_sigla("SVG") == "ese uve ge"
    assert deletrear_sigla("IA") == "i a"
    normalizaciones = normalizar_texto("Revisa el SVG final.")
    assert _unica(normalizaciones, "sigla").propuesta == "ese uve ge"


def test_diccionario_puede_dar_lectura_distinta_a_una_sigla() -> None:
    normalizaciones = normalizar_texto(
        "La IA ayuda a escribir.", diccionario={"IA": "inteligencia artificial"}
    )
    assert _unica(normalizaciones, "diccionario").propuesta == "inteligencia artificial"


# --- Conjunciones y/e, o/u -----------------------------------------------------------


def test_conjuncion_y_se_convierte_en_e_ante_sonido_i() -> None:
    normalizaciones = normalizar_texto("Fernando y Iker llegan tarde.")
    assert _unica(normalizaciones, "conjuncion").propuesta == "e"

    normalizaciones = normalizar_texto("Trae hilo y aguja.")
    assert not any(n.familia == "conjuncion" for n in normalizaciones)


def test_conjuncion_y_respeta_la_excepcion_del_diptongo_hie() -> None:
    normalizaciones = normalizar_texto("Nieve y hielo por la mañana.")
    assert not any(n.familia == "conjuncion" for n in normalizaciones)


def test_conjuncion_o_se_convierte_en_u_ante_sonido_o() -> None:
    normalizaciones = normalizar_texto("Siete o ocho personas.")
    assert _unica(normalizaciones, "conjuncion").propuesta == "u"

    normalizaciones = normalizar_texto("Tres o cuatro personas.")
    assert not any(n.familia == "conjuncion" for n in normalizaciones)


# --- Diccionario de excepciones (requisito 3) ---------------------------------------


def test_cargar_diccionario_locucion_ausente_devuelve_vacio(tmp_path: Path) -> None:
    assert cargar_diccionario_locucion(tmp_path) == {}


def test_cargar_diccionario_locucion_valido(tmp_path: Path) -> None:
    (tmp_path / "diccionario-locucion.json").write_text(
        '{"IA": "inteligencia artificial"}', encoding="utf-8"
    )
    assert cargar_diccionario_locucion(tmp_path) == {"IA": "inteligencia artificial"}


def test_cargar_diccionario_locucion_json_invalido_es_accionable(tmp_path: Path) -> None:
    (tmp_path / "diccionario-locucion.json").write_text("no es json", encoding="utf-8")
    with pytest.raises(NormalizacionError, match=r"diccionario-locucion\.json"):
        cargar_diccionario_locucion(tmp_path)


def test_cargar_diccionario_locucion_estructura_invalida_es_accionable(tmp_path: Path) -> None:
    ruta = tmp_path / "diccionario-locucion.json"
    ruta.write_text('["no", "es", "un", "objeto"]', encoding="utf-8")
    with pytest.raises(NormalizacionError, match="objeto JSON"):
        cargar_diccionario_locucion(tmp_path)


# --- Invariante (b) de §0.2: original siempre recuperable ---------------------------


def test_normalizacion_es_reversible() -> None:
    """Toda normalizacion conserva el texto original junto a la propuesta:
    aplicar todas las propuestas y deshacerlas reproduce el texto de partida
    exacto, letra a letra (invariante (b), criterio de aceptacion de T-13)."""
    texto = (
        "Fernando y Iker llegan tarde. Siete o ocho SVG con 3 + 2 > 4 y "
        "10-250 pymes, 1.500,50 € y 3/4 del trabajo en 2026, en su 1ª y 3er intento."
    )
    normalizaciones = normalizar_texto(texto)
    assert normalizaciones, "el texto de prueba deberia disparar varias familias de regla"
    for normalizacion in normalizaciones:
        assert normalizacion.original == texto[normalizacion.inicio : normalizacion.fin]

    propuesto = aplicar_normalizaciones(texto, normalizaciones)
    assert propuesto != texto
    reconstruido = deshacer_normalizaciones(propuesto, normalizaciones)
    assert reconstruido == texto


def test_normalizacion_sin_cambios_no_propone_nada() -> None:
    texto = "Esta frase no tiene ninguna cifra ni sigla que normalizar."
    assert normalizar_texto(texto) == []
    assert aplicar_normalizaciones(texto, []) == texto


# --- Integracion con T-11 (troceo) y los guiones reales -----------------------------


def test_normalizar_bloque_no_toca_el_bloque_original() -> None:
    bloque = BloqueRespiracion(
        texto="En 2026 grabamos.", numero_escena=0, linea_inicio=1, linea_fin=1,
        num_palabras=3, corte_forzado=False,
    )
    resultado = normalizar_bloque(bloque)
    assert resultado.bloque is bloque
    assert bloque.texto == "En 2026 grabamos."  # el original no se muta
    assert resultado.texto_propuesto == "En dos mil veintiséis grabamos."


def test_normalizar_guion_cubre_todos_los_bloques_de_los_guiones_reales(
    texto_guiones_reales: dict[str, str],
) -> None:
    """Cobertura total (invariante (a)): un resultado por bloque de respiracion,
    incluso los que no proponen ninguna normalizacion (nada se descarta en
    silencio). Sobre los guiones reales, además, localiza los dos casos
    conocidos: "80%" (guion-09) y "SVG" (guion-artefactos-lienzo)."""
    configuracion = Configuracion()
    propuestas_encontradas: set[str] = set()
    for nombre, texto in texto_guiones_reales.items():
        resultado = parsear_guion(texto)
        bloques = trocear_guion(resultado, configuracion)
        resultados = normalizar_guion(bloques, configuracion)

        assert len(resultados) == len(bloques)
        for resultado_bloque, bloque in zip(resultados, bloques, strict=True):
            assert resultado_bloque.bloque is bloque
            for normalizacion in resultado_bloque.normalizaciones:
                original_esperado = bloque.texto[normalizacion.inicio : normalizacion.fin]
                assert normalizacion.original == original_esperado
                clave = f"{nombre}:{normalizacion.familia}:{normalizacion.original}"
                propuestas_encontradas.add(clave)

    assert any(clave.endswith(":porcentaje:80%") for clave in propuestas_encontradas)
    assert any(clave.endswith(":sigla:SVG") for clave in propuestas_encontradas)


def test_reconstruccion_no_se_rompe_tras_normalizar_guion_real(
    texto_guiones_reales: dict[str, str],
) -> None:
    """La reversibilidad (invariante (b)) se sostiene tambien sobre texto real,
    no solo sobre casos sintéticos."""
    configuracion = Configuracion()
    for texto in texto_guiones_reales.values():
        resultado = parsear_guion(texto)
        bloques = trocear_guion(resultado, configuracion)
        for resultado_bloque in normalizar_guion(bloques, configuracion):
            propuesto = resultado_bloque.texto_propuesto
            reconstruido = deshacer_normalizaciones(propuesto, resultado_bloque.normalizaciones)
            assert reconstruido == resultado_bloque.bloque.texto
