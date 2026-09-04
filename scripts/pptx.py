"""Adaptador `.pptx` con identidad 480 por delegacion (tarea T-29).

Entregar el guion de locucion como presentacion de marca **sin reinventar
estilos**. Verificado con el `SKILL.md` de `480-branded-pptx` (2026-08-31,
`references/marca-480.md`): esa skill son instrucciones para Claude, no un
ejecutable -- genera el `.pptx` con Node + `pptxgenjs` apoyandose a su vez en
la skill `pptx`, y exige QA visual. Por eso este modulo **no invoca nada como
subproceso**: produce el contrato de intercambio `tarjetas.json` (documentado
en `references/contrato-tarjetas.md`) y un brief de invocacion en Markdown;
el `.pptx` lo genera Claude delegando en esa skill dentro de la misma sesion,
leyendo ambos archivos. Este modulo no escribe ni una linea de estilo de
marca -- ni siquiera compone HTML/CSS como `pdf.py` -- solo datos y texto.

Reutiliza sin duplicar la logica ya escrita para el `.pdf` (T-28): el mismo
criterio de "nota interna vs. indicacion de pantalla" (`pdf.es_nota_interna`,
`pdf.indicaciones_no_recitables`) y la misma medicion de la relacion de
aspecto del logotipo desde la cabecera `IHDR` (`pdf.dimensiones_png`), las
tres promovidas de privadas a publicas en esta tarea porque `pptx.py` es su
segundo consumidor (mismo patron que `tiempos.PAUSA_FIN_ESCENA` en T-27).
`Configuracion.incluir_notas_internas` es el mismo interruptor que usa el
`.pdf`: `False` es el modo `--para-terceros` (requisito 3), y aqui vacia
directamente la lista `notas_internas` de cada escena en el JSON exportado,
en vez de solo ocultarla en la presentacion.

Deteccion de disponibilidad (requisito 4): si `480-branded-pptx` o su
dependencia `pptx` no estan instaladas en esta maquina, la generacion de
`tarjetas.json` y el brief **nunca falla** -- solo se marca la salida
`.pptx` como latente en el mensaje devuelto, para que quien orquesta la
skill (T-30) lo refleje en el resumen final.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from clasificador import BloqueClasificado, clasificar_guion
from config import (
    NOMBRE_ARCHIVO_BRIEF_PPTX,
    NOMBRE_ARCHIVO_TARJETAS_JSON,
    VERSION_CONTRATO_TARJETAS,
    Configuracion,
)
from parser import Escena, ResultadoParseo
from pdf import dimensiones_png, es_nota_interna, indicaciones_no_recitables
from tiempos import ResultadoTiempos

RAIZ = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Tarjeta:
    """Una escena convertida a tarjeta de intercambio (requisito 1): todo lo
    que necesita una diapositiva de contenido, sin decidir todavia su
    maquetacion -- eso lo hace el brief y, en ultima instancia, la skill de
    marca."""

    numero: int
    titulo: str
    duracion_estimada_segundos: float
    duracion_objetivo_segundos: float | None
    aviso_desviacion: str | None
    bloques: tuple[str, ...]
    texto_locucion: str
    indicaciones_pantalla: tuple[str, ...]
    notas_internas: tuple[str, ...]


@dataclass(frozen=True)
class ResultadoTarjetas:
    """El contrato completo antes de serializar: metadatos de cabecera
    (requisito 1) mas una tarjeta por escena, en orden."""

    titulo: str
    para_terceros: bool
    duracion_total_segundos: float
    duracion_objetivo_total_segundos: tuple[int, int] | None
    palabras_locucion_total: int
    tarjetas: tuple[Tarjeta, ...]


def _extracto(texto: str, limite: int) -> str:
    extracto = " ".join(texto.split())
    if len(extracto) > limite:
        extracto = extracto[: limite - 1].rstrip() + "…"
    return extracto


def _indicaciones_de_escena(
    escena: Escena,
    bloques_clasificados: list[BloqueClasificado],
    configuracion: Configuracion,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Indicaciones no recitables de una escena, ya separadas en pantalla y
    notas internas (requisito 1: el contrato declara ambas listas por
    separado, nunca mezcladas bajo un unico membrete como hace `guion-
    escenas.md`, T-16). Con `incluir_notas_internas=False` (modo
    `--para-terceros`, requisito 3) las notas internas salen vacias del
    propio `tarjetas.json` exportado -- no solo ocultas en la presentacion."""
    indicaciones = indicaciones_no_recitables(escena, bloques_clasificados)
    limite = configuracion.longitud_extracto_indicacion_max
    pantalla = tuple(
        _extracto(bloque.contenido, limite)
        for bloque in indicaciones
        if not es_nota_interna(bloque)
    )
    if not configuracion.incluir_notas_internas:
        return pantalla, ()
    notas = tuple(
        _extracto(bloque.contenido, limite) for bloque in indicaciones if es_nota_interna(bloque)
    )
    return pantalla, notas


def _tarjeta_de_escena(
    escena: Escena,
    resultado_tiempos: ResultadoTiempos,
    bloques_clasificados: list[BloqueClasificado],
    configuracion: Configuracion,
) -> Tarjeta:
    tiempo_escena = next(t for t in resultado_tiempos.escenas if t.numero == escena.numero)
    bloques_escena = [
        b for b in resultado_tiempos.bloques if b.bloque.numero_escena == escena.numero
    ]
    textos_bloques = tuple(b.bloque.texto for b in bloques_escena)
    pantalla, notas = _indicaciones_de_escena(escena, bloques_clasificados, configuracion)
    return Tarjeta(
        numero=escena.numero,
        titulo=escena.titulo,
        duracion_estimada_segundos=tiempo_escena.duracion_estimada_segundos,
        duracion_objetivo_segundos=tiempo_escena.duracion_objetivo_segundos,
        aviso_desviacion=tiempo_escena.aviso or None,
        bloques=textos_bloques,
        texto_locucion=" ".join(textos_bloques),
        indicaciones_pantalla=pantalla,
        notas_internas=notas,
    )


def generar_tarjetas(
    resultado: ResultadoParseo,
    resultado_tiempos: ResultadoTiempos,
    nombre_guion: str = "guion",
    configuracion: Configuracion | None = None,
) -> ResultadoTarjetas:
    """Construye el contrato completo (requisito 1) a partir de un guion ya
    parseado y con tiempos calculados -- mismo patron que `pdf.py`/`srt.py`:
    no recalcula nada, consume `ResultadoTiempos` tal cual, asi que el texto
    de cada bloque ya es el LOCUTADO FINAL cuando `resultado_tiempos` viene
    de una revalidacion (T-17, reescrituras aceptadas materializadas)."""
    configuracion = configuracion or Configuracion()
    clasificacion = clasificar_guion(resultado, configuracion)
    palabras_totales = sum(resumen.palabras_locucion for resumen in clasificacion.resumenes)
    tarjetas = tuple(
        _tarjeta_de_escena(escena, resultado_tiempos, clasificacion.bloques, configuracion)
        for escena in resultado.escenas
    )
    return ResultadoTarjetas(
        titulo=nombre_guion,
        para_terceros=not configuracion.incluir_notas_internas,
        duracion_total_segundos=resultado_tiempos.duracion_total_segundos,
        duracion_objetivo_total_segundos=resultado_tiempos.duracion_objetivo_total_segundos,
        palabras_locucion_total=palabras_totales,
        tarjetas=tarjetas,
    )


def tarjetas_a_diccionario(resultado_tarjetas: ResultadoTarjetas) -> dict[str, Any]:
    """Serializa `ResultadoTarjetas` a la forma exacta del contrato
    documentado en `references/contrato-tarjetas.md` -- la unica funcion que
    conoce esa forma; `validar_tarjetas` valida contra la misma."""
    return {
        "version_contrato": VERSION_CONTRATO_TARJETAS,
        "metadatos": {
            "titulo": resultado_tarjetas.titulo,
            "para_terceros": resultado_tarjetas.para_terceros,
            "numero_escenas": len(resultado_tarjetas.tarjetas),
            "palabras_locucion_total": resultado_tarjetas.palabras_locucion_total,
            "duracion_total_segundos": resultado_tarjetas.duracion_total_segundos,
            "duracion_objetivo_total_segundos": (
                list(resultado_tarjetas.duracion_objetivo_total_segundos)
                if resultado_tarjetas.duracion_objetivo_total_segundos is not None
                else None
            ),
        },
        "escenas": [
            {
                "numero": tarjeta.numero,
                "titulo": tarjeta.titulo,
                "duracion_estimada_segundos": tarjeta.duracion_estimada_segundos,
                "duracion_objetivo_segundos": tarjeta.duracion_objetivo_segundos,
                "aviso_desviacion": tarjeta.aviso_desviacion,
                "bloques": list(tarjeta.bloques),
                "texto_locucion": tarjeta.texto_locucion,
                "indicaciones_pantalla": list(tarjeta.indicaciones_pantalla),
                "notas_internas": list(tarjeta.notas_internas),
            }
            for tarjeta in resultado_tarjetas.tarjetas
        ],
    }


def formatear_tarjetas_json(resultado_tarjetas: ResultadoTarjetas) -> str:
    """Contenido completo de `tarjetas.json`, legible (indentado) porque el
    dueno puede querer inspeccionarlo a mano antes de invocar la skill."""
    datos = tarjetas_a_diccionario(resultado_tarjetas)
    return json.dumps(datos, ensure_ascii=False, indent=2) + "\n"


def guardar_tarjetas_json(contenido: str, carpeta_salida: Path) -> Path:
    """Escribe `tarjetas.json` en la carpeta de salida del guion (regla de
    aislamiento, §0.2)."""
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    destino = carpeta_salida / NOMBRE_ARCHIVO_TARJETAS_JSON
    destino.write_text(contenido, encoding="utf-8", newline="\n")
    return destino


_CLAVES_METADATOS: dict[str, type | tuple[type, ...]] = {
    "titulo": str,
    "para_terceros": bool,
    "numero_escenas": int,
    "palabras_locucion_total": int,
    "duracion_total_segundos": (int, float),
}
_CLAVES_ESCENA: dict[str, type | tuple[type, ...]] = {
    "numero": int,
    "titulo": str,
    "duracion_estimada_segundos": (int, float),
    "bloques": list,
    "texto_locucion": str,
    "indicaciones_pantalla": list,
    "notas_internas": list,
}


def validar_tarjetas(datos: dict[str, Any]) -> list[str]:
    """Valida `datos` (ya deserializados de `tarjetas.json`) contra el
    contrato de `references/contrato-tarjetas.md` (requisito 1, "el contrato
    esta documentado y testeado contra un esquema"): claves de cabecera y de
    cada escena presentes con el tipo esperado, `numero_escenas` coincide con
    la lista real, y ninguna escena queda completamente vacia (ni locucion ni
    indicaciones, seria una tarjeta sin contenido que mostrar). Sin depender
    de `jsonschema` (§0.2, sin dependencias de terceros) -- mismo patron a
    mano que `srt.validar_srt`. Lista vacia == valido."""
    problemas: list[str] = []
    if "version_contrato" not in datos:
        problemas.append("Falta la clave 'version_contrato'.")

    metadatos = datos.get("metadatos")
    if not isinstance(metadatos, dict):
        problemas.append("Falta el objeto 'metadatos' o no es un objeto.")
        metadatos = {}
    for clave, tipo in _CLAVES_METADATOS.items():
        if clave not in metadatos:
            problemas.append(f"metadatos: falta la clave '{clave}'.")
        elif not isinstance(metadatos[clave], tipo):
            problemas.append(
                f"metadatos.{clave}: tipo incorrecto ({type(metadatos[clave]).__name__})."
            )

    escenas = datos.get("escenas")
    if not isinstance(escenas, list) or not escenas:
        problemas.append("Falta la lista 'escenas' o esta vacia.")
        escenas = []
    numero_declarado = metadatos.get("numero_escenas")
    if isinstance(numero_declarado, int) and numero_declarado != len(escenas):
        problemas.append(
            f"metadatos.numero_escenas ({numero_declarado}) no coincide con el numero "
            f"real de escenas ({len(escenas)})."
        )

    for indice, escena in enumerate(escenas, start=1):
        if not isinstance(escena, dict):
            problemas.append(f"Escena {indice}: no es un objeto.")
            continue
        for clave, tipo in _CLAVES_ESCENA.items():
            if clave not in escena:
                problemas.append(f"Escena {indice}: falta la clave '{clave}'.")
            elif not isinstance(escena[clave], tipo):
                problemas.append(
                    f"Escena {indice}.{clave}: tipo incorrecto ({type(escena[clave]).__name__})."
                )
        if not escena.get("bloques") and not escena.get("indicaciones_pantalla"):
            problemas.append(
                f"Escena {indice}: no tiene ni bloques de locucion ni indicaciones de pantalla."
            )
    return problemas


def _alto_logo_pulgadas(ruta: Path, ancho_pulgadas: float) -> float | None:
    dimensiones = dimensiones_png(ruta)
    if dimensiones is None:
        return None
    ancho_px, alto_px = dimensiones
    return ancho_pulgadas / (ancho_px / alto_px)


def _tabla_alturas_logo_markdown(configuracion: Configuracion) -> str:
    """Tabla de alturas correctas del logotipo para el brief (requisito 2:
    corregir por escrito la relacion de aspecto fija 668/376 del `SKILL.md`
    de la skill de marca), calculada con la MISMA funcion que ya usa el
    `.pdf` (`pdf.dimensiones_png`) -- nunca una constante copiada a mano."""
    ruta_claro = RAIZ / configuracion.ruta_logo_pdf
    ruta_oscuro = RAIZ / configuracion.ruta_logo_pptx_oscuro
    filas = (
        ("Portada (DARK)", configuracion.pptx_ancho_logo_portada_pulgadas, ruta_oscuro),
        (
            "Header en diapositivas de contenido (LIGHT)",
            configuracion.pptx_ancho_logo_contenido_pulgadas,
            ruta_claro,
        ),
        ("Cierre (DARK)", configuracion.pptx_ancho_logo_cierre_pulgadas, ruta_oscuro),
    )
    lineas = ["| Diapositiva | Ancho | Alto correcto (medido del PNG real) |", "|---|---|---|"]
    for etiqueta, ancho, ruta in filas:
        alto = _alto_logo_pulgadas(ruta, ancho)
        alto_texto = (
            f'{alto:.3f}"' if alto is not None else "*(logotipo no disponible en este entorno)*"
        )
        lineas.append(f'| {etiqueta} | {ancho}" | {alto_texto} |')
    return "\n".join(lineas)


def _relacion_aspecto_texto(configuracion: Configuracion) -> str:
    dimensiones = dimensiones_png(RAIZ / configuracion.ruta_logo_pdf)
    if dimensiones is None:
        return (
            "no medible en este entorno (logotipo ausente); mide la relacion "
            "del PNG real antes de maquetar"
        )
    ancho_px, alto_px = dimensiones
    return f"{ancho_px}x{alto_px} px -> {ancho_px / alto_px:.4f}:1"


def _agrupar_tarjetas(
    tarjetas: tuple[Tarjeta, ...], tamano_grupo: int
) -> list[tuple[Tarjeta, ...]]:
    return [tarjetas[i : i + tamano_grupo] for i in range(0, len(tarjetas), tamano_grupo)]


def _diapositiva_markdown(indice: int, grupo: tuple[Tarjeta, ...]) -> str:
    numeros = ", ".join(str(tarjeta.numero) for tarjeta in grupo)
    secciones = []
    for tarjeta in grupo:
        objetivo = (
            f" (objetivo {tarjeta.duracion_objetivo_segundos:.0f} s)"
            if tarjeta.duracion_objetivo_segundos is not None
            else ""
        )
        aviso = f" — ⚠ {tarjeta.aviso_desviacion}" if tarjeta.aviso_desviacion else ""
        indicaciones = (
            "\n".join(f"  - {indicacion}" for indicacion in tarjeta.indicaciones_pantalla)
            if tarjeta.indicaciones_pantalla
            else "  - (ninguna)"
        )
        secciones.append(
            f"**BLOQUE {tarjeta.numero} — {tarjeta.titulo}**\n"
            f"- Duración estimada: {tarjeta.duracion_estimada_segundos:.0f} s{objetivo}{aviso}\n"
            "- Texto de locución (como prosa legible en el cuerpo de la diapositiva):\n\n"
            f"  {tarjeta.texto_locucion}\n\n"
            f"- Indicaciones de pantalla (en la propia diapositiva):\n{indicaciones}\n"
            "- Notas del orador: el texto de locución completo de esta escena, íntegro "
            "(el mismo de arriba)."
        )
    return (
        f"### Diapositiva {indice} — contenido (LIGHT), escena(s) {numeros}\n\n"
        + "\n\n".join(secciones)
    )


def generar_brief(
    resultado_tarjetas: ResultadoTarjetas,
    configuracion: Configuracion | None = None,
) -> str:
    """Brief de invocacion en Markdown (requisito 2): estructura de deck que
    `480-branded-pptx` ya impone (`references/marca-480.md`), sin repetir
    estilos de marca -- eso lo hace esa skill. Corrige por escrito las dos
    discrepancias conocidas de su `SKILL.md` con los assets reales de este
    proyecto: tipografia (Poppins, no Figtree) y relacion de aspecto del
    logotipo (medida del PNG, no la constante 668/376 de la guia)."""
    configuracion = configuracion or Configuracion()
    grupos = _agrupar_tarjetas(
        resultado_tarjetas.tarjetas, configuracion.pptx_escenas_por_diapositiva
    )
    incluir_indice = len(grupos) >= configuracion.pptx_umbral_indice_secciones
    modo = (
        "ENTREGABLE A TERCEROS"
        if resultado_tarjetas.para_terceros
        else "documento de repaso completo"
    )
    objetivo = resultado_tarjetas.duracion_objetivo_total_segundos
    objetivo_texto = f" (objetivo {objetivo[0]}-{objetivo[1]} s)" if objetivo is not None else ""

    if incluir_indice:
        diapositiva_indice = (
            "2. **Índice (LIGHT).** Lista de escenas por número y título — hay "
            f"{len(grupos)} diapositivas de contenido, igual o por encima del umbral "
            f"de {configuracion.pptx_umbral_indice_secciones} que fija "
            "`references/marca-480.md`: se incluye índice.\n"
        )
    else:
        diapositiva_indice = (
            f"*(Sin diapositiva de índice: hay {len(grupos)} diapositiva(s) de "
            f"contenido, por debajo del umbral de {configuracion.pptx_umbral_indice_secciones}.)*\n"
        )

    diapositivas_contenido = "\n\n".join(
        _diapositiva_markdown(indice, grupo) for indice, grupo in enumerate(grupos, start=1)
    )

    notas_internas_texto = (
        "Se omiten las notas internas de producción: el deck sale listo para un tercero."
        if resultado_tarjetas.para_terceros
        else (
            "Incluye las notas internas de producción tal como aparecen en "
            f"`{NOMBRE_ARCHIVO_TARJETAS_JSON}`, salvo el aparato de reescrituras "
            "(original/propuesta/decisión), que esta skill nunca muestra en ningún "
            "modo — esa vista de edición ya vive en `guion-escenas.md`."
        )
    )

    return f"""# Brief de invocación — `.pptx` con marca 480 para «{resultado_tarjetas.titulo}»

> Genera el `.pptx` invocando la skill `480-branded-pptx` (que a su vez usa la skill
> `pptx` con Node + `pptxgenjs`) sobre los datos de `{NOMBRE_ARCHIVO_TARJETAS_JSON}`,
> en esta misma carpeta. La skill `teleprompter` **no genera el `.pptx` por su
> cuenta**: eres tú, Claude, quien lo genera delegando en esa skill dentro de esta
> misma sesión. No reinventes estilos de marca — para eso está la skill de marca;
> este brief solo describe qué contenido va en cada diapositiva.

## Modo: {modo}

{notas_internas_texto}

## Dos correcciones OBLIGATORIAS sobre el `SKILL.md` de `480-branded-pptx`

Su código lleva estos dos valores fijos y, con los assets reales de este proyecto,
producen un resultado incorrecto (detalle completo en `references/marca-480.md`):

1. **Tipografía: usa Poppins, no Figtree.** El `SKILL.md` de la skill de marca dice
   Figtree («familia obligatoria»); el dueño de este proyecto decidió Poppins (manda
   `references/brand-guide.md`, no el `SKILL.md` de esa skill). Poppins está
   instalada en la máquina del dueño.
2. **Relación de aspecto del logotipo: {_relacion_aspecto_texto(configuracion)}, no
   668/376 (1.7766).** La guía de marca fija 668/376 como «inviolable», pero los
   archivos reales de este proyecto miden otra cosa; aplicar 668/376 estira el
   logotipo un 39 % en vertical — exactamente el error que la propia guía marca como
   fallo. Usa la tabla de abajo, calculada con la relación real del archivo.

{_tabla_alturas_logo_markdown(configuracion)}

## Estructura del deck (`references/marca-480.md`; respétala tal cual, no la reinventes)

1. **Portada (DARK).** Título «{resultado_tarjetas.titulo}», subtítulo con la
   duración total ({resultado_tarjetas.duracion_total_segundos:.0f} s{objetivo_texto}),
   fecha de generación, logotipo prominente (variante sobre fondo oscuro,
   `{configuracion.ruta_logo_pptx_oscuro}`).
{diapositiva_indice}
{diapositivas_contenido}

*(Sin diapositivas separadoras: esta skill no agrupa las escenas en bloques mayores
que la propia escena — `references/marca-480.md` solo las pide «entre bloques
mayores, solo si hay 3+», y aquí no existe esa agrupación adicional.)*

**Cierre (DARK).** Resumen: {len(resultado_tarjetas.tarjetas)} escena(s), duración
total {resultado_tarjetas.duracion_total_segundos:.0f} s. Sin datos de contacto
conocidos por esta skill — si el guión los trae en alguna sección auxiliar, inclúyelos;
si no, deja un cierre sobrio con el título y la duración. Logotipo centrado (variante
sobre fondo oscuro).

## Contrato de datos

Los datos completos (títulos, bloques, duraciones, indicaciones, notas internas) están
en `{NOMBRE_ARCHIVO_TARJETAS_JSON}`, documentado en `references/contrato-tarjetas.md`.
Este brief resume su contenido para la invocación; ante cualquier duda de detalle, el
JSON manda.
"""


def guardar_brief(contenido: str, carpeta_salida: Path) -> Path:
    """Escribe el brief de invocacion en la carpeta de salida del guion
    (regla de aislamiento, §0.2), junto a `tarjetas.json`."""
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    destino = carpeta_salida / NOMBRE_ARCHIVO_BRIEF_PPTX
    destino.write_text(contenido, encoding="utf-8", newline="\n")
    return destino


def detectar_skill_pptx_disponible(configuracion: Configuracion | None = None) -> bool:
    """`True` si tanto `480-branded-pptx` como su dependencia, la skill
    `pptx`, estan instaladas en esta maquina (requisito 4): solo comprueba
    que la carpeta existe, nunca su contenido -- validar eso es
    responsabilidad de esas skills, no de esta. En una sesion de nube, sin
    `~/.claude/skills/`, esto es siempre `False`; la salida `.pptx` queda
    latente sin que la generacion falle."""
    configuracion = configuracion or Configuracion()
    ruta_marca = Path(configuracion.ruta_skill_marca_pptx).expanduser()
    ruta_base = Path(configuracion.ruta_skill_pptx_base).expanduser()
    return ruta_marca.is_dir() and ruta_base.is_dir()


@dataclass(frozen=True)
class ResultadoPptx:
    """Resultado de `exportar_pptx`: `tarjetas.json` y el brief siempre
    existen; `skill_disponible` dice si la generacion real del `.pptx` es
    posible ahora mismo o queda latente (requisito 4). `mensaje` es siempre
    accionable."""

    ruta_tarjetas_json: Path
    ruta_brief: Path
    skill_disponible: bool
    mensaje: str


def exportar_pptx(
    resultado: ResultadoParseo,
    resultado_tiempos: ResultadoTiempos,
    carpeta_salida: Path,
    nombre_guion: str = "guion",
    configuracion: Configuracion | None = None,
) -> ResultadoPptx:
    """Punto de entrada normal del modulo: genera y guarda `tarjetas.json` y
    el brief SIEMPRE (requisito 4), sea cual sea la disponibilidad de la
    skill de marca -- nunca falla por su ausencia. La generacion real del
    `.pptx` no la hace este codigo (ver docstring del modulo): la hace
    Claude delegando en `480-branded-pptx` dentro de la misma sesion,
    leyendo el brief devuelto aqui."""
    configuracion = configuracion or Configuracion()
    resultado_tarjetas = generar_tarjetas(
        resultado, resultado_tiempos, nombre_guion, configuracion
    )
    ruta_json = guardar_tarjetas_json(
        formatear_tarjetas_json(resultado_tarjetas), carpeta_salida
    )
    ruta_brief = guardar_brief(generar_brief(resultado_tarjetas, configuracion), carpeta_salida)

    disponible = detectar_skill_pptx_disponible(configuracion)
    if disponible:
        mensaje = (
            f"{ruta_json.name} y {ruta_brief.name} generados. Invoca la skill "
            "480-branded-pptx con este brief, dentro de esta sesion, para producir el .pptx."
        )
    else:
        mensaje = (
            f"{ruta_json.name} y {ruta_brief.name} generados; la salida .pptx queda "
            "LATENTE porque la skill 480-branded-pptx (o su dependencia, la skill pptx) "
            f"no esta instalada en {configuracion.ruta_skill_marca_pptx}. Instalala y "
            "vuelve a validar para producir el .pptx real."
        )
    return ResultadoPptx(ruta_json, ruta_brief, disponible, mensaje)
