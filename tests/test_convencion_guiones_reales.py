"""Suite minima (T-03): la convencion de guion declarada en `config.py` frente a los
tres guiones reales de calibracion.

El parser de escenas (T-08) y el clasificador locucion/no locucion (T-09) todavia no
existen, pero el contrato que van a implementar ya esta escrito en `config.py`
(patron de encabezado y rotulos, decision del dueno registrada en §0.2 y §6.3). Estos
tests comprueban que ese contrato describe de verdad a los guiones reales, para que un
cambio futuro en el patron o en los rotulos no rompa la calibracion en silencio.
"""

from __future__ import annotations

import re
from pathlib import Path

from config import PATRON_ENCABEZADO_ESCENA, ROTULO_LOCUCION, ROTULOS_NO_LOCUCION


def test_hay_guiones_reales_para_calibrar(guiones_reales: list[Path]) -> None:
    assert len(guiones_reales) == 3


def test_todo_guion_real_tiene_al_menos_una_escena(texto_guiones_reales: dict[str, str]) -> None:
    patron = re.compile(PATRON_ENCABEZADO_ESCENA, re.MULTILINE)
    for nombre, texto in texto_guiones_reales.items():
        escenas = patron.findall(texto)
        assert escenas, f"{nombre} no tiene ninguna escena que case con el patron contractual"


def test_numeracion_de_escenas_no_tiene_huecos(texto_guiones_reales: dict[str, str]) -> None:
    patron = re.compile(PATRON_ENCABEZADO_ESCENA, re.MULTILINE)
    for nombre, texto in texto_guiones_reales.items():
        numeros = [int(numero) for numero, _titulo in patron.findall(texto)]
        assert numeros == sorted(numeros), f"{nombre}: las escenas no estan en orden"
        assert numeros == list(range(numeros[0], numeros[0] + len(numeros))), (
            f"{nombre}: la numeracion de escenas tiene huecos: {numeros}"
        )


def test_todo_guion_real_usa_el_rotulo_de_locucion(texto_guiones_reales: dict[str, str]) -> None:
    for nombre, texto in texto_guiones_reales.items():
        assert ROTULO_LOCUCION in texto, (
            f"{nombre} no usa el rotulo contractual {ROTULO_LOCUCION!r}"
        )


def test_todo_guion_real_usa_al_menos_un_rotulo_de_no_locucion(
    texto_guiones_reales: dict[str, str],
) -> None:
    for nombre, texto in texto_guiones_reales.items():
        assert any(rotulo in texto for rotulo in ROTULOS_NO_LOCUCION), (
            f"{nombre} no usa ninguno de los rotulos de no locucion {ROTULOS_NO_LOCUCION!r}"
        )
