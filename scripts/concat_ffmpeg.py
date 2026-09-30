"""Lista de concatenacion de ffmpeg a partir de la toma buena real (tarea R-19).

Cierra el hueco entre el parte de rodaje (R-02) y la fase de montaje con
ffmpeg que la visión de producto señala como el paso siguiente al
reproductor: hoy `estado.json["tomas"]` sabe qué escena tiene una toma buena
y cuánto duró (R-04/R-05/R-07 ya leen esa duración con
`tomas.duracion_toma_buena`), pero no qué archivo de la tarjeta de la cámara
le corresponde -- el dueño tenía que reconstruirlo a mano, por orden y
duración, antes de poder concatenar nada. `archivo_video` (R-19, campo nuevo
y opcional de `Toma`) añade esa única pieza que faltaba, tecleada por el
propio dueño; este módulo produce directamente la lista de concatenación
lista para `ffmpeg -f concat -safe 0 -i concat-ffmpeg.txt`.

Requisito 3: recorre las escenas en el mismo orden real del guion
(`resultado_tiempos.escenas`, el que también usan `tarjetas.json`/`guion.srt`,
`references/contrato-montaje.md`) y, por cada una, busca su toma buena
reutilizando `tomas.toma_buena` tal cual (no reimplementa la regla de
exclusividad de R-11/#16, la misma que ya usan R-04/R-05/R-07). Si existe y
trae `archivo_video` anotado, escribe la línea `file '<archivo_video>'` en el
formato exacto del demuxer `concat` de ffmpeg. Si la escena no tiene toma
buena, o la tiene pero sin anotar, **nunca** se inventa una ruta ni se
silencia la escena: se escribe un comentario `# ESCENA <numero>: <motivo>`
(el demuxer de ffmpeg ignora líneas que empiezan por `#`) y la escena se
cuenta en `escenas_pendientes`.

Requisito 4 (nunca falla por escenas pendientes de anotar): con al menos un
parte de rodaje registrado, el archivo se genera siempre, mezclando líneas
`file` y comentarios según haga falta -- nunca una excepción por datos
incompletos. Sin ningún parte de rodaje (`tomas_por_escena` vacío), no hay
nada real que concatenar todavía: `generar_lista_concat_ffmpeg` devuelve
`None` con `motivo_sin_generar` explícito (mismo patrón que
`capitulos_youtube.calcular_capitulos` sin sección `Capítulos`), para que
`scripts/salidas.py` la refleje como `SalidaOmitida`, nunca como archivo con
todo comentado.

Requisito 6 (invariantes (a)/(d) de §0.2): este módulo es de solo lectura
sobre `EstadoProyecto.tomas` -- nunca modifica una toma ni descarta ningún
campo existente; anotar `archivo_video` es cosa de `guion.js`/`tomas.py`.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from config import NOMBRE_ARCHIVO_CONCAT_FFMPEG
from tiempos import ResultadoTiempos
from tomas import toma_buena

_SIN_TOMA_BUENA = "sin_toma_buena"
_SIN_ARCHIVO_ANOTADO = "sin_archivo_anotado"


@dataclass(frozen=True)
class EscenaPendiente:
    """Una escena sin línea `file` real en la lista de concatenación."""

    numero_escena: int
    motivo: str  # "sin_toma_buena" | "sin_archivo_anotado"


@dataclass(frozen=True)
class ResultadoConcatFfmpeg:
    """Salida de `calcular_lista_concat_ffmpeg`.

    `lineas` vacío junto con `motivo_sin_generar` (no `None`) es la señal de
    "no generar el archivo" (requisito 4): ningún parte de rodaje registrado
    todavía. `escenas_pendientes` son las escenas sin `archivo_video`
    aprovechable (sin toma buena, o con ella pero sin anotar) -- vacío
    significa que todas las escenas con toma buena ya tienen su archivo real.
    """

    lineas: tuple[str, ...]
    escenas_pendientes: tuple[EscenaPendiente, ...]
    motivo_sin_generar: str | None


def _escapar_ruta_ffmpeg(ruta: str) -> str:
    """Escapa `ruta` para una línea `file '...'` del demuxer `concat` de
    ffmpeg: comillas simples alrededor, cada comilla simple interna sustituida
    por la secuencia estándar `'\\''` (cierra la comilla abierta, un carácter
    de comilla simple literal ya fuera de comillas, la reabre)."""
    return "'" + ruta.replace("'", "'\\''") + "'"


def calcular_lista_concat_ffmpeg(
    resultado_tiempos: ResultadoTiempos,
    tomas_por_escena: dict[str, Any] | None = None,
) -> ResultadoConcatFfmpeg:
    """Recorre las escenas en su orden real (requisito 3) y arma, por cada
    una, la línea `file '...'` o el comentario `# ESCENA N: motivo`."""
    tomas_por_escena = tomas_por_escena or {}
    if not tomas_por_escena:
        return ResultadoConcatFfmpeg(
            lineas=(),
            escenas_pendientes=(),
            motivo_sin_generar="no hay ningún parte de rodaje registrado todavía (R-02).",
        )

    lineas: list[str] = []
    pendientes: list[EscenaPendiente] = []
    for tiempo_escena in resultado_tiempos.escenas:
        numero = tiempo_escena.numero
        toma = toma_buena(tomas_por_escena.get(str(numero)), numero)
        if toma is None:
            lineas.append(f"# ESCENA {numero}: {_SIN_TOMA_BUENA}")
            pendientes.append(EscenaPendiente(numero, _SIN_TOMA_BUENA))
            continue
        archivo = toma.get("archivo_video") or ""
        if not archivo:
            lineas.append(f"# ESCENA {numero}: {_SIN_ARCHIVO_ANOTADO}")
            pendientes.append(EscenaPendiente(numero, _SIN_ARCHIVO_ANOTADO))
            continue
        lineas.append(f"file {_escapar_ruta_ffmpeg(archivo)}")

    return ResultadoConcatFfmpeg(
        lineas=tuple(lineas), escenas_pendientes=tuple(pendientes), motivo_sin_generar=None
    )


def formatear_lista_concat_ffmpeg(resultado: ResultadoConcatFfmpeg) -> str | None:
    """Texto final de `concat-ffmpeg.txt`. `None` si `resultado` no trae
    ninguna línea (requisito 4: nada que generar todavía)."""
    if not resultado.lineas:
        return None
    return "\n".join(resultado.lineas) + "\n"


def generar_lista_concat_ffmpeg(
    resultado_tiempos: ResultadoTiempos,
    tomas_por_escena: dict[str, Any] | None = None,
) -> tuple[str | None, ResultadoConcatFfmpeg]:
    """Punto de entrada de R-19: calcula y formatea en un solo paso, mismo
    patrón que `capitulos_youtube.generar_capitulos_youtube`. `contenido` es
    `None` cuando no hay nada que generar (requisito 4): no llamar a
    `guardar_lista_concat_ffmpeg` en ese caso."""
    resultado = calcular_lista_concat_ffmpeg(resultado_tiempos, tomas_por_escena)
    return formatear_lista_concat_ffmpeg(resultado), resultado


def validar_lista_concat_ffmpeg(contenido: str) -> list[str]:
    """Mismas reglas que exige el demuxer `concat` de ffmpeg (criterio de
    aceptación de R-19): cada línea no vacía es un comentario (`#...`, una
    escena todavía sin archivo real) o una directiva `file '<ruta>'` con la
    ruta entre comillas simples y cualquier comilla simple interna escapada
    con la secuencia estándar `'\\''`."""
    problemas: list[str] = []
    for indice, linea in enumerate(contenido.splitlines()):
        if not linea.strip() or linea.startswith("#"):
            continue
        if not linea.startswith("file '") or not linea.endswith("'"):
            problemas.append(
                f"línea {indice + 1} no tiene el formato \"file '<ruta>'\": {linea!r}"
            )
            continue
        cuerpo = linea[len("file '") : -1]
        if not cuerpo:
            problemas.append(f"línea {indice + 1}: ruta vacía en {linea!r}.")
            continue
        # Ninguna comilla simple suelta: toda comilla dentro de la ruta solo
        # puede aparecer como parte de la secuencia de escape estandar
        # `'\''` (cierra la comilla abierta, comilla literal, la reabre);
        # quitar cada aparicion valida de esa secuencia no debe dejar ninguna
        # comilla suelta detras.
        if "'" in cuerpo.replace("'\\''", ""):
            problemas.append(
                f"línea {indice + 1}: comilla simple sin escapar en la ruta: {linea!r}"
            )
    return problemas


def guardar_lista_concat_ffmpeg(contenido: str, carpeta_salida: Path) -> Path:
    """Escribe `concat-ffmpeg.txt` en la carpeta de salida del guion. Nunca
    fuera de `carpeta_salida` (regla de aislamiento, §0.2). No llamar con
    `contenido=None` (requisito 4): quien orquesta decide no escribir nada."""
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    destino = carpeta_salida / NOMBRE_ARCHIVO_CONCAT_FFMPEG
    destino.write_text(contenido, encoding="utf-8", newline="\n")
    return destino
