"""Parser de Markdown y deteccion del separador de escenas (tarea T-08).

Convierte el `.md` de un guion en una estructura fiable de escenas, conservando
todo lo que no es escena (metadatos de cabecera, secciones auxiliares) en vez de
descartarlo en silencio (invariante (a) de §0.2, "cobertura total del guion").

Evidencia de los tres guiones reales (`fixtures/reales/`): el separador de escena
es el nivel `##`, con el patron contractual `PATRON_ENCABEZADO_ESCENA` de
`config.py` (`## BLOQUE N — <titulo> (m:ss-m:ss)`). Ese mismo nivel `##` tambien
alberga secciones que NO son escena: el subtitulo entrecomillado tras el `#`
inicial, `## Capitulos (...)`, `## Preparacion antes de grabar` y
`## Notas de produccion`. Este modulo distingue escena de seccion auxiliar dentro
de ese mismo nivel (requisito 3 de T-08) en vez de asumir que todo `##` es escena.

Senales de clasificacion por encabezado del nivel elegido, en orden:
1. Primaria: el encabezado casa con el patron de escena -> es escena, sin mas.
2. Si no casa: se miran a la vez la lista negra (`configuracion.secciones_auxiliares`,
   senal terciaria) y el rotulo de locucion en el cuerpo (`ROTULO_LOCUCION`, senal
   secundaria).
   - Ninguna de las dos aplica -> seccion auxiliar (caso claro y mayoritario en
     los tres guiones reales: el subtitulo entrecomillado, por ejemplo).
   - Solo la lista negra aplica -> seccion auxiliar (`Capitulos`, `Preparacion
     antes de grabar`, `Notas de produccion`).
   - Solo el rotulo de locucion aplica -> es escena: un titulo que se desvia del
     patron pero tiene contenido recitable no puede tratarse como auxiliar sin
     perder locucion (invariante (a)).
   - **Las dos aplican a la vez (conflicto real)** -> ambiguo: se propone la
     eleccion al dueno en vez de decidir en silencio (requisito 6).

El nivel del separador se deriva del propio `PATRON_ENCABEZADO_ESCENA` (cuenta los
`#` iniciales), no esta escrito a mano aqui: si el dueno cambia el patron en
`config.py`, el nivel efectivo cambia con el. Si ningun encabezado del `.md` casa
con ese patron a ese nivel, la deteccion tambien es ambigua: se proponen
alternativas por nivel candidato (`#`, `##`, `###`) usando una senal mas laxa
(contiene "BLOQUE N" y/o un rango de marcas de tiempo) para que el dueno elija.

En ambos casos la excepcion `DeteccionEscenasAmbiguaError` lleva las alternativas
con sus consecuencias (numero de escenas y duracion media resultantes). Quien la
capture (hoy: un test; manana, la CLI de T-16/T-17) decide y persiste la
respuesta: la eleccion de nivel/patron en `estado.separador_escena` (T-07), y un
ajuste de `secciones_auxiliares` para el caso de conflicto -- ver
`tests/test_parser.py::test_conflicto_de_senales_se_resuelve_ajustando_la_lista_negra`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from config import PATRON_ENCABEZADO_ESCENA, ROTULO_LOCUCION, Configuracion
from estado import SeparadorEscena

_PATRON_ENCABEZADO = re.compile(r"^(?P<marcadores>#{1,6})[ \t]+(?P<titulo>\S.*?)\s*$")
_PATRON_VALLA_CODIGO = re.compile(r"^(```|~~~)")
_PATRON_METADATO = re.compile(r"^\*\*(?P<clave>[^*]+?):\*\*\s*(?P<valor>.*)$")
# Los guiones reales separan los extremos del rango horario con un guion largo
# (U+2013), no con el guion corto del teclado: se referencia por escape unicode
# en vez de como caracter literal para no disparar la regla RUF001 de ruff (que
# marca el guion largo como "ambiguo" por su parecido visual con el corto).
_GUION_LARGO = "\u2013"
_NIVELES_CANDIDATOS = (1, 2, 3)
_PATRON_SENAL_LAXA = re.compile(
    rf"BLOQUE\s+\d+|\(\s*\d{{1,2}}:\d{{2}}\s*[{_GUION_LARGO}-]\s*\d{{1,2}}:\d{{2}}\s*\)",
    re.IGNORECASE,
)
_PATRON_RANGO_TIEMPO = re.compile(
    rf"(\d{{1,2}}):(\d{{2}})\s*[{_GUION_LARGO}-]\s*(\d{{1,2}}):(\d{{2}})"
)


@dataclass
class Bloque:
    """Un tramo del `.md` bajo un encabezado (o el preambulo, con `nivel=0`).

    `linea_inicio`/`linea_fin` son 1-indexadas e inclusivas sobre el texto de
    origen (requisito 1 de T-08). `contenido` incluye la propia linea de
    encabezado: concatenar los `contenido` de todos los bloques de un guion, en
    orden, reconstruye el `.md` completo sin perdida.
    """

    nivel: int
    titulo: str
    contenido: str
    linea_inicio: int
    linea_fin: int


@dataclass
class Escena:
    """Una escena: un encabezado del nivel separador reconocido como recitable."""

    numero: int
    titulo: str
    contenido: str
    linea_inicio: int
    linea_fin: int


@dataclass
class SeccionAuxiliar:
    """Un encabezado que NO es escena. Se conserva integro, nunca se descarta."""

    titulo: str
    contenido: str
    linea_inicio: int
    linea_fin: int
    motivo: str


@dataclass
class AlternativaSeparador:
    """Una opcion de separador (o de clasificacion) con sus consecuencias."""

    nivel: str
    patron: str
    numero_escenas: int
    duracion_media_segundos: float | None
    descripcion: str


class DeteccionEscenasAmbiguaError(Exception):
    """La deteccion de escenas no puede decidir sola: hace falta el dueno.

    Cubre dos causas (requisito 6 de T-08): ningun encabezado casa con el patron
    configurado al nivel esperado (ambiguedad de nivel), o un encabezado tiene
    senales contradictorias -- esta en la lista negra de secciones auxiliares y
    a la vez tiene el rotulo de locucion en el cuerpo (ambiguedad de
    clasificacion). `alternativas` trae, por cada opcion, cuantas escenas y que
    duracion media resultarian de elegirla.
    """

    def __init__(self, alternativas: list[AlternativaSeparador]) -> None:
        self.alternativas = alternativas
        resumen = "\n".join(
            f"  - nivel {alt.nivel!r} ({alt.patron}): {alt.numero_escenas} escenas"
            + (
                f", duracion media {alt.duracion_media_segundos:.0f}s"
                if alt.duracion_media_segundos is not None
                else ""
            )
            + f" — {alt.descripcion}"
            for alt in alternativas
        )
        super().__init__(
            "No se puede elegir el separador de escenas en automatico: la senal es "
            f"ambigua. Alternativas:\n{resumen}\nConfirma cual usar; la respuesta se "
            "guarda en estado.json y no se vuelve a preguntar mientras el guion no cambie."
        )


@dataclass
class ResultadoParseo:
    """Resultado completo de analizar un `.md`: nada del guion original se pierde."""

    metadatos: dict[str, str]
    preambulo: str
    escenas: list[Escena]
    secciones_auxiliares: list[SeccionAuxiliar]
    separador: SeparadorEscena
    distribucion_por_nivel: dict[int, int] = field(default_factory=dict)


def dividir_en_bloques(texto: str) -> list[Bloque]:
    """Trocea el `.md` en un bloque por encabezado, mas el preambulo si lo hay.

    Ignora las lineas que empiezan por `#` dentro de una valla de codigo (``` o
    ~~~) para no confundir un comentario de codigo con un encabezado.
    """
    lineas = texto.splitlines()
    encabezados: list[tuple[int, int, str]] = []
    dentro_de_codigo = False
    for indice, linea in enumerate(lineas):
        if _PATRON_VALLA_CODIGO.match(linea):
            dentro_de_codigo = not dentro_de_codigo
            continue
        if dentro_de_codigo:
            continue
        coincidencia = _PATRON_ENCABEZADO.match(linea)
        if coincidencia:
            nivel = len(coincidencia.group("marcadores"))
            encabezados.append((indice, nivel, coincidencia.group("titulo")))

    if not encabezados:
        return []

    bloques: list[Bloque] = []
    primer_inicio = encabezados[0][0]
    if primer_inicio > 0:
        bloques.append(
            Bloque(
                nivel=0,
                titulo="",
                contenido="\n".join(lineas[:primer_inicio]),
                linea_inicio=1,
                linea_fin=primer_inicio,
            )
        )

    limites = [inicio for inicio, _nivel, _titulo in encabezados] + [len(lineas)]
    for indice_encabezado, (inicio, nivel, titulo) in enumerate(encabezados):
        fin = limites[indice_encabezado + 1]
        bloques.append(
            Bloque(
                nivel=nivel,
                titulo=titulo,
                contenido="\n".join(lineas[inicio:fin]),
                linea_inicio=inicio + 1,
                linea_fin=fin,
            )
        )
    return bloques


def extraer_metadatos(texto: str) -> dict[str, str]:
    """Extrae los pares `**Clave:** valor` de la cabecera del guion (requisito 7).

    Generico a proposito: los tres guiones reales no usan las mismas claves
    (`Idea unica del video` frente a `Promesa del video`), asi que no hay un
    esquema fijo de claves esperadas. Se descartan las lineas con valor vacio
    (encabezados en negrita que terminan en `:` pero cuyo contenido real esta en
    el parrafo o cita siguiente, no en la misma linea).
    """
    metadatos: dict[str, str] = {}
    for linea in texto.splitlines():
        coincidencia = _PATRON_METADATO.match(linea.strip())
        if not coincidencia:
            continue
        valor = coincidencia.group("valor").strip()
        if valor:
            metadatos[coincidencia.group("clave").strip()] = valor
    return metadatos


def _nivel_desde_patron(patron: str) -> int:
    coincidencia = re.match(r"^\^?(#+)", patron)
    return len(coincidencia.group(1)) if coincidencia else 2


def _patron_para_nivel(nivel: int) -> str:
    """Sugiere el patron contractual trasladado a otro nivel de encabezado.

    Solo cambia los `#` iniciales; el resto del patron (marcador `BLOQUE N` y
    rango horario) se mantiene. Es una sugerencia para las alternativas de
    `DeteccionEscenasAmbiguaError`, nunca se aplica sin que el dueno la elija.
    """
    nivel_actual = "^" + "#" * _nivel_desde_patron(PATRON_ENCABEZADO_ESCENA)
    return PATRON_ENCABEZADO_ESCENA.replace(nivel_actual, "^" + "#" * nivel, 1)


def _rango_segundos(texto_encabezado: str) -> tuple[int, int] | None:
    coincidencia = _PATRON_RANGO_TIEMPO.search(texto_encabezado)
    if not coincidencia:
        return None
    inicio_min, inicio_seg, fin_min, fin_seg = (int(g) for g in coincidencia.groups())
    inicio, fin = inicio_min * 60 + inicio_seg, fin_min * 60 + fin_seg
    return (inicio, fin) if fin > inicio else None


def _duracion_media_segundos(titulos: list[str]) -> float | None:
    duraciones = [rango[1] - rango[0] for t in titulos if (rango := _rango_segundos(t))]
    return sum(duraciones) / len(duraciones) if duraciones else None


def _en_lista_negra(titulo: str, configuracion: Configuracion) -> bool:
    titulo_normalizado = titulo.strip()
    return any(
        titulo_normalizado.startswith(entrada) for entrada in configuracion.secciones_auxiliares
    )


@dataclass
class _Clasificacion:
    escenas: list[Bloque]
    auxiliares: list[tuple[Bloque, str]]
    conflictivos: list[Bloque]


def _clasificar_bloques_nivel(
    bloques_nivel: list[Bloque],
    patron_compilado: re.Pattern[str],
    configuracion: Configuracion,
) -> _Clasificacion:
    escenas: list[Bloque] = []
    auxiliares: list[tuple[Bloque, str]] = []
    conflictivos: list[Bloque] = []
    for bloque in bloques_nivel:
        linea_encabezado = "#" * bloque.nivel + " " + bloque.titulo
        if patron_compilado.match(linea_encabezado):
            escenas.append(bloque)
            continue

        en_lista_negra = _en_lista_negra(bloque.titulo, configuracion)
        tiene_locucion = ROTULO_LOCUCION in bloque.contenido
        if en_lista_negra and tiene_locucion:
            conflictivos.append(bloque)
        elif tiene_locucion:
            escenas.append(bloque)
        elif en_lista_negra:
            auxiliares.append(
                (bloque, "titulo en la lista negra de secciones auxiliares (secciones_auxiliares)")
            )
        else:
            auxiliares.append(
                (bloque, "no coincide con el patron de escena ni contiene el rotulo de locucion")
            )
    return _Clasificacion(escenas=escenas, auxiliares=auxiliares, conflictivos=conflictivos)


def _alternativas_por_nivel_sin_coincidencias(
    bloques: list[Bloque],
) -> list[AlternativaSeparador]:
    """Ningun encabezado casa con el patron configurado: propone por nivel.

    Usa la senal laxa (contiene "BLOQUE N" y/o un rango de tiempo) solo para
    estimar cuantas escenas resultarian de cada nivel candidato, nunca para
    decidir en su lugar.
    """
    alternativas = []
    for nivel in _NIVELES_CANDIDATOS:
        candidatos = [b for b in bloques if b.nivel == nivel]
        if not candidatos:
            continue
        con_senal = [b for b in candidatos if _PATRON_SENAL_LAXA.search(b.titulo)]
        alternativas.append(
            AlternativaSeparador(
                nivel="#" * nivel,
                patron=_patron_para_nivel(nivel),
                numero_escenas=len(con_senal),
                duracion_media_segundos=_duracion_media_segundos([b.titulo for b in con_senal]),
                descripcion=(
                    f"nivel {'#' * nivel}: {len(candidatos)} encabezados, "
                    f"{len(con_senal)} con marcador de bloque o rango horario"
                ),
            )
        )
    return alternativas


def _alternativas_por_conflicto(
    clasificacion: _Clasificacion, nivel_str: str, patron: str
) -> list[AlternativaSeparador]:
    titulos_claros = [b.titulo for b in clasificacion.escenas]
    titulos_conflicto = [b.titulo for b in clasificacion.conflictivos]
    lista_conflicto = ", ".join(f"'{t}'" for t in titulos_conflicto)
    return [
        AlternativaSeparador(
            nivel=nivel_str,
            patron=patron,
            numero_escenas=len(clasificacion.escenas),
            duracion_media_segundos=_duracion_media_segundos(titulos_claros),
            descripcion=(
                f"mantener en secciones_auxiliares: {lista_conflicto} (no cuentan como escena "
                f"pese al rotulo {ROTULO_LOCUCION})"
            ),
        ),
        AlternativaSeparador(
            nivel=nivel_str,
            patron=patron,
            numero_escenas=len(clasificacion.escenas) + len(clasificacion.conflictivos),
            duracion_media_segundos=_duracion_media_segundos(titulos_claros + titulos_conflicto),
            descripcion=(
                f"quitar de secciones_auxiliares: {lista_conflicto} (tienen {ROTULO_LOCUCION} "
                "en el cuerpo, pasarian a tratarse como escena)"
            ),
        ),
    ]


def elegir_separador(texto: str, configuracion: Configuracion | None = None) -> SeparadorEscena:
    """Decide el nivel y patron de separador de escena para este guion.

    Devuelve la eleccion cuando la senal es clara. Levanta
    `DeteccionEscenasAmbiguaError` cuando no lo es, en vez de adivinar
    (requisito 6 de T-08).
    """
    configuracion = configuracion or Configuracion()
    bloques = dividir_en_bloques(texto)
    nivel = _nivel_desde_patron(PATRON_ENCABEZADO_ESCENA)
    nivel_str = "#" * nivel
    patron_compilado = re.compile(PATRON_ENCABEZADO_ESCENA, re.MULTILINE)

    bloques_nivel = [b for b in bloques if b.nivel == nivel]
    clasificacion = _clasificar_bloques_nivel(bloques_nivel, patron_compilado, configuracion)

    if not clasificacion.escenas:
        raise DeteccionEscenasAmbiguaError(_alternativas_por_nivel_sin_coincidencias(bloques))
    if clasificacion.conflictivos:
        raise DeteccionEscenasAmbiguaError(
            _alternativas_por_conflicto(clasificacion, nivel_str, PATRON_ENCABEZADO_ESCENA)
        )
    return SeparadorEscena(nivel=nivel_str, patron=PATRON_ENCABEZADO_ESCENA)


def parsear_guion(
    texto: str,
    *,
    configuracion: Configuracion | None = None,
    separador: SeparadorEscena | None = None,
) -> ResultadoParseo:
    """Analiza el `.md` completo: escenas, secciones auxiliares y metadatos.

    Si `separador` ya trae `nivel`/`patron` (decision persistida en
    `estado.json` de una sesion anterior, requisito 6 de T-08), se usa tal cual
    en vez de volver a preguntar que nivel elegir. Los conflictos de
    clasificacion (requisito 3) se comprueban siempre, persistido o no, porque
    dependen de `configuracion.secciones_auxiliares`, que puede cambiar entre
    pasadas sin que cambie el separador.
    """
    configuracion = configuracion or Configuracion()
    if separador is None or separador.nivel is None or separador.patron is None:
        separador = elegir_separador(texto, configuracion)

    nivel_str, patron = separador.nivel, separador.patron
    assert nivel_str is not None
    assert patron is not None
    nivel = len(nivel_str)
    patron_compilado = re.compile(patron, re.MULTILINE)

    bloques = dividir_en_bloques(texto)
    bloques_nivel = [b for b in bloques if b.nivel == nivel]
    clasificacion = _clasificar_bloques_nivel(bloques_nivel, patron_compilado, configuracion)

    if not clasificacion.escenas:
        raise DeteccionEscenasAmbiguaError(_alternativas_por_nivel_sin_coincidencias(bloques))
    if clasificacion.conflictivos:
        raise DeteccionEscenasAmbiguaError(
            _alternativas_por_conflicto(clasificacion, nivel_str, patron)
        )

    escenas: list[Escena] = []
    for indice, bloque in enumerate(clasificacion.escenas):
        linea_encabezado = "#" * bloque.nivel + " " + bloque.titulo
        coincidencia = patron_compilado.match(linea_encabezado)
        grupos = coincidencia.groupdict() if coincidencia else {}
        valor_numero = grupos.get("numero")
        numero = int(valor_numero) if valor_numero is not None else indice
        titulo_escena = grupos.get("titulo") or bloque.titulo
        escenas.append(
            Escena(
                numero=numero,
                titulo=titulo_escena,
                contenido=bloque.contenido,
                linea_inicio=bloque.linea_inicio,
                linea_fin=bloque.linea_fin,
            )
        )
    escenas.sort(key=lambda e: e.linea_inicio)

    auxiliares: list[SeccionAuxiliar] = []
    for bloque in bloques:
        if bloque.nivel not in (0, nivel):
            auxiliares.append(
                SeccionAuxiliar(
                    titulo=bloque.titulo,
                    contenido=bloque.contenido,
                    linea_inicio=bloque.linea_inicio,
                    linea_fin=bloque.linea_fin,
                    motivo=(
                        f"encabezado de nivel {'#' * bloque.nivel}, "
                        f"distinto del separador ({nivel_str})"
                    ),
                )
            )
    for bloque, motivo in clasificacion.auxiliares:
        auxiliares.append(
            SeccionAuxiliar(
                titulo=bloque.titulo,
                contenido=bloque.contenido,
                linea_inicio=bloque.linea_inicio,
                linea_fin=bloque.linea_fin,
                motivo=motivo,
            )
        )
    auxiliares.sort(key=lambda s: s.linea_inicio)

    preambulo = next((b.contenido for b in bloques if b.nivel == 0), "")
    primera_linea_escena = min((e.linea_inicio for e in escenas), default=None)
    texto_cabecera = (
        "\n".join(texto.splitlines()[: primera_linea_escena - 1])
        if primera_linea_escena is not None
        else texto
    )
    metadatos = extraer_metadatos(texto_cabecera)

    distribucion: dict[int, int] = {}
    for bloque in bloques:
        if bloque.nivel != 0:
            distribucion[bloque.nivel] = distribucion.get(bloque.nivel, 0) + 1

    return ResultadoParseo(
        metadatos=metadatos,
        preambulo=preambulo,
        escenas=escenas,
        secciones_auxiliares=auxiliares,
        separador=separador,
        distribucion_por_nivel=distribucion,
    )
