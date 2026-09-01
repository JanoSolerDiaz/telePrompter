"""Clasificador locucion / no locucion (tarea T-09).

Separa dentro de cada escena (T-08) el texto que se recita del que no
(indicaciones de pantalla, notas de produccion, timestamps...).

Senal primaria (ruta rapida), manda siempre que este presente (requisito 1 de
T-09): el rotulo de seccion dentro de la escena. Por defecto `**LOCUCIÓN**`
frente a `**EN PANTALLA**`/`**NOTA**` (`Configuracion.rotulo_locucion` /
`.rotulos_no_locucion`, configurables). Dentro de una seccion `**LOCUCIÓN**`,
el texto en cita de bloque (`> `) es lo recitable; cualquier otro texto suelto
en la misma seccion se marca `revisar` (requisito 3): es el caso ambiguo mas
probable en los guiones reales (acotaciones de ritmo, un encargo de ejemplo
fuera de cita).

Senales de respaldo (inferencia), solo para texto sin rotulo activo -- guiones
que no usan la convencion, o el tramo de una escena anterior al primer rotulo
(requisito 2). La cita de bloque (`> `) por si sola ya es señal suficiente de
locucion incluso sin el rotulo: es la misma convencion que usa `**LOCUCIÓN**`
("el texto recitable va... en cita de bloque", HOJA_DE_RUTA T-09) y es lo que
permite alcanzar el ≥95% de precision del criterio de aceptacion sobre los
guiones reales despojados de sus rotulos (`tests/test_clasificador.py`): sus
secciones `**EN PANTALLA**` nunca usan cita de bloque, asi que la señal no
produce falsos positivos en esos tres guiones. El resto de heuristicas
(timestamps, acotaciones, mayusculas, prefijos, codigo, tablas, enlaces) cubre
guiones sin ninguna convencion de citas. Sin señal clara, el bloque se marca
`revisar`: nunca se decide en silencio (requisito 5, invariante (a) de §0.2).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from config import Configuracion
from parser import Escena, ResultadoParseo

TIPO_LOCUCION = "locucion"
TIPO_NO_LOCUCION = "no_locucion"
TIPO_REVISAR = "revisar"

_PREFIJOS_NO_LOCUCION = ("PANTALLA:", "B-ROLL:", "NOTA:", "IMAGEN:", "TÍTULO:")
_PATRON_VALLA_CODIGO = re.compile(r"^(```|~~~)")
_PATRON_TIMESTAMP = re.compile(r"\b\d{1,2}:\d{2}\b")
_PATRON_ENLACE_SUELTO = re.compile(r"^(https?://\S+|\[[^\]]+\]\(\S+\))$")


@dataclass
class BloqueClasificado:
    """Un tramo del `.md` con su clasificacion, motivo, senal y rango de lineas.

    `linea_inicio`/`linea_fin` son 1-indexadas e inclusivas, igual que en
    `parser.Bloque` (T-08): concatenar el `contenido` de todos los bloques de
    un guion, ordenados por `linea_inicio`, reconstruye el `.md` completo sin
    perdida (invariante (a) de §0.2, ver `reconstruir`).
    """

    tipo: str
    contenido: str
    linea_inicio: int
    linea_fin: int
    motivo: str
    senal: str


@dataclass
class ResumenEscena:
    """Cuanto texto de la escena se excluyo de la locucion, y por que (requisito 7)."""

    numero: int
    titulo: str
    palabras_totales: int
    palabras_locucion: int
    palabras_excluidas: int
    motivos_exclusion: dict[str, int] = field(default_factory=dict)


@dataclass
class ResultadoClasificacion:
    """Clasificacion completa de un guion ya parseado (T-08): nada se pierde."""

    bloques: list[BloqueClasificado]
    resumenes: list[ResumenEscena]


def _bloque(
    tipo: str, lineas: list[str], linea_inicio: int, motivo: str, senal: str
) -> BloqueClasificado:
    contenido = "\n".join(lineas)
    return BloqueClasificado(
        tipo=tipo,
        contenido=contenido,
        linea_inicio=linea_inicio,
        linea_fin=linea_inicio + len(lineas) - 1,
        motivo=motivo,
        senal=senal,
    )


def _dividir_en_parrafos(lineas: list[str]) -> list[list[int]]:
    """Particion completa en parrafos: rachas de lineas no en blanco, con las
    lineas en blanco pegadas al parrafo anterior (o al siguiente si son las
    primeras). Cubre todos los indices de `lineas`, sin huecos ni solapes."""
    grupos: list[list[int]] = []
    for indice, linea in enumerate(lineas):
        if not linea.strip():
            if grupos:
                grupos[-1].append(indice)
            else:
                grupos.append([indice])
            continue
        if grupos and not any(lineas[i].strip() for i in grupos[-1]):
            grupos[-1].append(indice)
        else:
            grupos.append([indice])
    return grupos


def _agrupar_cita_suelto(lineas: list[str]) -> list[tuple[str, list[int]]]:
    """Particion completa de una seccion **LOCUCIÓN** en tramos de cita de
    bloque (`> `) y texto suelto (requisito 3), fusionando lineas en blanco con
    el tramo contiguo. Mismo invariante de cobertura que `_dividir_en_parrafos`."""
    grupos: list[tuple[str, list[int]]] = []
    for indice, linea in enumerate(lineas):
        texto = linea.strip()
        if not texto:
            if grupos:
                grupos[-1][1].append(indice)
            else:
                grupos.append(("blank", [indice]))
            continue
        tipo = "cita" if texto.startswith(">") else "suelto"
        if grupos and grupos[-1][0] in (tipo, "blank"):
            indices_actuales = grupos[-1][1]
            indices_actuales.append(indice)
            grupos[-1] = (tipo, indices_actuales)
        else:
            grupos.append((tipo, [indice]))
    return grupos


def _inferir_tipo_parrafo(lineas: list[str]) -> tuple[str, str, str]:
    """Heuristicas de respaldo (requisito 2) sobre un parrafo sin rotulo activo."""
    no_blancas = [linea for linea in lineas if linea.strip()]
    if not no_blancas:
        return TIPO_NO_LOCUCION, "linea en blanco, sin contenido que revisar", "blank"

    if all(linea.strip().startswith(">") for linea in no_blancas):
        return (
            TIPO_LOCUCION,
            "cita de bloque, misma convencion que el rotulo de locucion",
            "cita_bloque",
        )
    if any(_PATRON_VALLA_CODIGO.match(linea.strip()) for linea in no_blancas):
        return TIPO_NO_LOCUCION, "bloque de codigo", "codigo"

    texto_junto = " ".join(linea.strip() for linea in no_blancas)

    if _PATRON_TIMESTAMP.search(texto_junto):
        return TIPO_NO_LOCUCION, "marca de tiempo", "timestamp"
    if (texto_junto.startswith("(") and texto_junto.endswith(")")) or (
        texto_junto.startswith("[") and texto_junto.endswith("]")
    ):
        return TIPO_NO_LOCUCION, "acotacion entre parentesis o corchetes", "acotacion"

    prefijo = next(
        (p for p in _PREFIJOS_NO_LOCUCION if texto_junto.upper().startswith(p)), None
    )
    if prefijo is not None:
        return TIPO_NO_LOCUCION, f"prefijo '{prefijo}'", "prefijo"

    if all(linea.strip().startswith(("- ", "* ", "+ ", "-[", "*[")) for linea in no_blancas):
        return TIPO_NO_LOCUCION, "vineta de checklist", "vineta"
    if any("|" in linea for linea in no_blancas):
        return TIPO_NO_LOCUCION, "tabla", "tabla"
    if texto_junto.startswith("#"):
        return TIPO_NO_LOCUCION, "encabezado interno", "encabezado_interno"
    if (texto_junto.startswith("**") and texto_junto.endswith("**")) or (
        texto_junto.startswith("*")
        and texto_junto.endswith("*")
        and not texto_junto.startswith("**")
    ):
        return (
            TIPO_NO_LOCUCION,
            "texto en negrita o cursiva de linea completa",
            "negrita_cursiva",
        )

    letras = [caracter for caracter in texto_junto if caracter.isalpha()]
    if letras and all(caracter.isupper() for caracter in letras):
        return TIPO_NO_LOCUCION, "linea en mayusculas", "mayusculas"
    if _PATRON_ENLACE_SUELTO.match(texto_junto):
        return TIPO_NO_LOCUCION, "enlace suelto", "enlace"

    return (
        TIPO_REVISAR,
        "sin senal de inferencia clara: no se puede clasificar con confianza",
        "sin_senal",
    )


def _inferir_parrafos(lineas: list[str], base: int) -> list[BloqueClasificado]:
    if not lineas:
        return []
    bloques = []
    for indices in _dividir_en_parrafos(lineas):
        contenido_lineas = [lineas[i] for i in indices]
        tipo, motivo, senal = _inferir_tipo_parrafo(contenido_lineas)
        bloques.append(_bloque(tipo, contenido_lineas, base + indices[0], motivo, senal))
    return bloques


def _clasificar_seccion_locucion(
    seccion: list[str], base: int, texto_rotulo: str
) -> list[BloqueClasificado]:
    bloques = []
    for tipo_grupo, indices in _agrupar_cita_suelto(seccion):
        lineas_grupo = [seccion[i] for i in indices]
        linea_inicio = base + indices[0]
        if tipo_grupo == "cita":
            bloques.append(
                _bloque(
                    TIPO_LOCUCION,
                    lineas_grupo,
                    linea_inicio,
                    f"cita de bloque bajo el rotulo {texto_rotulo}",
                    "cita_bloque",
                )
            )
        elif tipo_grupo == "suelto":
            bloques.append(
                _bloque(
                    TIPO_REVISAR,
                    lineas_grupo,
                    linea_inicio,
                    f"texto suelto fuera de la cita de bloque dentro de {texto_rotulo}",
                    "texto_suelto_en_locucion",
                )
            )
        else:
            bloques.append(
                _bloque(
                    TIPO_REVISAR,
                    lineas_grupo,
                    linea_inicio,
                    f"seccion {texto_rotulo} sin contenido reconocible",
                    "seccion_vacia",
                )
            )
    return bloques


def _localizar_rotulos(
    cuerpo: list[str], configuracion: Configuracion
) -> list[tuple[int, str, str]]:
    encontrados: list[tuple[int, str, str]] = []
    for indice, linea in enumerate(cuerpo):
        texto = linea.strip()
        if texto == configuracion.rotulo_locucion:
            encontrados.append((indice, texto, TIPO_LOCUCION))
        elif texto in configuracion.rotulos_no_locucion:
            encontrados.append((indice, texto, TIPO_NO_LOCUCION))
    return encontrados


def clasificar_escena(
    escena: Escena, configuracion: Configuracion | None = None
) -> list[BloqueClasificado]:
    """Clasifica el contenido de una escena en bloques locucion/no_locucion/revisar.

    Cobertura total (requisito 6): la union ordenada de los bloques devueltos,
    unida con `\\n`, reconstruye `escena.contenido` sin perdida.
    """
    configuracion = configuracion or Configuracion()
    # `.split("\n")`, no `.splitlines()`: `escena.contenido` ya viene de un
    # `"\n".join(...)` (T-08). Si la ultima linea es una cadena vacia (una linea
    # en blanco real antes del siguiente encabezado), `.splitlines()` la pierde
    # ("a\nb\n".splitlines() == ["a", "b"]); `.split("\n")` es el inverso exacto
    # de ese `join` y la conserva.
    lineas = escena.contenido.split("\n")
    if not lineas or escena.contenido == "":
        return []

    bloques = [
        _bloque(
            TIPO_NO_LOCUCION,
            lineas[:1],
            escena.linea_inicio,
            "encabezado de escena, no se recita",
            "encabezado",
        )
    ]
    cuerpo = lineas[1:]
    if not cuerpo:
        return bloques
    base_cuerpo = escena.linea_inicio + 1

    rotulos = _localizar_rotulos(cuerpo, configuracion)
    if not rotulos:
        bloques.extend(_inferir_parrafos(cuerpo, base_cuerpo))
        return bloques

    primer_indice = rotulos[0][0]
    if primer_indice > 0:
        bloques.extend(_inferir_parrafos(cuerpo[:primer_indice], base_cuerpo))

    limites = [indice for indice, _texto, _tipo in rotulos] + [len(cuerpo)]
    for posicion, (indice, texto_rotulo, tipo_rotulo) in enumerate(rotulos):
        linea_rotulo = base_cuerpo + indice
        bloques.append(
            _bloque(
                TIPO_NO_LOCUCION,
                cuerpo[indice : indice + 1],
                linea_rotulo,
                "rotulo de seccion, no se recita",
                "rotulo",
            )
        )
        fin = limites[posicion + 1]
        seccion = cuerpo[indice + 1 : fin]
        if not seccion:
            continue
        base_seccion = linea_rotulo + 1
        if tipo_rotulo == TIPO_LOCUCION:
            bloques.extend(_clasificar_seccion_locucion(seccion, base_seccion, texto_rotulo))
        else:
            bloques.append(
                _bloque(
                    TIPO_NO_LOCUCION,
                    seccion,
                    base_seccion,
                    f"rotulo '{texto_rotulo}': contenido no recitable",
                    "rotulo_no_locucion",
                )
            )
    return bloques


def _resumir_escena(escena: Escena, bloques: list[BloqueClasificado]) -> ResumenEscena:
    totales = 0
    locucion = 0
    motivos: dict[str, int] = {}
    for bloque in bloques:
        n_palabras = len(bloque.contenido.split())
        totales += n_palabras
        if bloque.tipo == TIPO_LOCUCION:
            locucion += n_palabras
        else:
            motivos[bloque.motivo] = motivos.get(bloque.motivo, 0) + n_palabras
    return ResumenEscena(
        numero=escena.numero,
        titulo=escena.titulo,
        palabras_totales=totales,
        palabras_locucion=locucion,
        palabras_excluidas=totales - locucion,
        motivos_exclusion=motivos,
    )


def clasificar_guion(
    resultado: ResultadoParseo, configuracion: Configuracion | None = None
) -> ResultadoClasificacion:
    """Clasifica un guion ya parseado (T-08) por completo: preambulo, secciones
    auxiliares y el interior de cada escena. Cobertura total (invariante (a) de
    §0.2): `reconstruir(resultado.bloques)` reproduce el `.md` de origen entero.
    """
    configuracion = configuracion or Configuracion()
    bloques: list[BloqueClasificado] = []

    if resultado.preambulo:
        lineas_preambulo = resultado.preambulo.split("\n")
        bloques.append(
            _bloque(
                TIPO_NO_LOCUCION,
                lineas_preambulo,
                1,
                "preambulo, antes del primer encabezado",
                "preambulo",
            )
        )

    for auxiliar in resultado.secciones_auxiliares:
        bloques.append(
            BloqueClasificado(
                tipo=TIPO_NO_LOCUCION,
                contenido=auxiliar.contenido,
                linea_inicio=auxiliar.linea_inicio,
                linea_fin=auxiliar.linea_fin,
                motivo=auxiliar.motivo,
                senal="seccion_auxiliar",
            )
        )

    resumenes: list[ResumenEscena] = []
    for escena in resultado.escenas:
        bloques_escena = clasificar_escena(escena, configuracion)
        bloques.extend(bloques_escena)
        resumenes.append(_resumir_escena(escena, bloques_escena))

    bloques.sort(key=lambda b: b.linea_inicio)
    return ResultadoClasificacion(bloques=bloques, resumenes=resumenes)


def reconstruir(bloques: list[BloqueClasificado]) -> str:
    """Reconstruye el texto de origen a partir de bloques ya clasificados,
    ordenados por `linea_inicio`. Test de reconstruccion del requisito 6."""
    ordenados = sorted(bloques, key=lambda b: b.linea_inicio)
    return "\n".join(bloque.contenido for bloque in ordenados)
