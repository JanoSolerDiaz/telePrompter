"""T-31: ninguna clave de `Configuracion` puede quedar sin documentar en `SKILL.md`.

Criterio de aceptacion literal de T-31: "no queda ningun valor por defecto en el
codigo que no este en la tabla del SKILL.md; test que compara las claves del modulo
de configuracion con las documentadas y falla si divergen". Compara los nombres de
campo del dataclass `Configuracion` (la superficie de configuracion que el dueno
puede sobreescribir en cualquier nivel de la precedencia, T-31 requisito 3) contra
las claves citadas entre backticks en la seccion "Valores por defecto — tabla
completa" de `SKILL.md`. Falla en cualquier sentido: un campo nuevo sin documentar,
o una fila de tabla que cita un campo que ya no existe.

Las tablas de constantes que la propia `DECISIONES_TECNICAS.md` decidio dejar fuera
de `Configuracion` (T-13: `SIMBOLOS_MONEDA`/`UNIDADES_ABREVIADAS`; T-14:
`ANGLICISMOS_COMUNES`; el patron de encabezado de escena, contractual con el dueno)
no son campos del dataclass y por tanto no entran en esta comparacion; siguen
documentadas por nombre en `SKILL.md`, solo que no como fila de esta tabla.
"""

from __future__ import annotations

import dataclasses
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from config import Configuracion

RAIZ = Path(__file__).resolve().parent.parent
SKILL_MD = RAIZ / "SKILL.md"
_ENCABEZADO_TABLA = "## Valores por defecto — tabla completa"
_PATRON_CAMPO = re.compile(r"`([a-z][a-z0-9_]*)`")
# Un encabezado de nivel 2 real ("## Foo"), no de nivel 3 o mas ("### Foo"): el
# espacio tiene que venir justo despues de EXACTAMENTE dos almohadillas.
_PATRON_SIGUIENTE_H2 = re.compile(r"\n##(?!#) ")


def _seccion_tabla_completa() -> str:
    texto = SKILL_MD.read_text(encoding="utf-8")
    inicio = texto.index(_ENCABEZADO_TABLA)
    resto = texto[inicio:]
    coincidencia = _PATRON_SIGUIENTE_H2.search(resto, 1)
    fin = coincidencia.start() if coincidencia else len(resto)
    return resto[:fin]


def _claves_citadas_en_tabla_completa() -> set[str]:
    return set(_PATRON_CAMPO.findall(_seccion_tabla_completa()))


def test_skill_md_tiene_la_seccion_de_tabla_completa() -> None:
    assert _ENCABEZADO_TABLA in SKILL_MD.read_text(encoding="utf-8")


def test_toda_clave_de_configuracion_esta_documentada_en_skill_md() -> None:
    claves_codigo = {campo.name for campo in dataclasses.fields(Configuracion)}
    claves_documentadas = _claves_citadas_en_tabla_completa()
    faltantes = sorted(claves_codigo - claves_documentadas)
    assert not faltantes, (
        "Campos de Configuracion sin documentar en la tabla completa de SKILL.md: "
        f"{faltantes}"
    )


def test_skill_md_no_documenta_una_clave_que_ya_no_existe_en_configuracion() -> None:
    claves_codigo = {campo.name for campo in dataclasses.fields(Configuracion)}
    claves_documentadas = _claves_citadas_en_tabla_completa()
    obsoletas = sorted(claves_documentadas - claves_codigo)
    assert not obsoletas, (
        "SKILL.md documenta claves que ya no son campos de Configuracion (renombradas "
        f"o eliminadas sin actualizar la tabla): {obsoletas}"
    )


def test_precedencia_de_configuracion_esta_documentada() -> None:
    texto = SKILL_MD.read_text(encoding="utf-8")
    assert "valores por defecto" in texto.lower()
    assert (
        "configuración del usuario" in texto.lower()
        or "configuracion del usuario" in texto.lower()
    )
    assert (
        "configuración del proyecto de guion" in texto.lower()
        or "configuracion del proyecto de guion" in texto.lower()
    )
    assert (
        "argumentos de la invocación" in texto.lower()
        or "argumentos de la invocacion" in texto.lower()
    )
