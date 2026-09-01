"""`guion-escenas.md`: el documento de revision de una sola pasada (tarea T-16).

Objetivo (HOJA_DE_RUTA T-16): que el dueno revise TODO el guion de una sentada en
su editor de texto plano, sin ping-pong en el chat. Este modulo no vuelve a
calcular nada por su cuenta -- toma los resultados ya calculados por las tareas
anteriores (parseo T-08, clasificacion T-09, tiempos T-12, deteccion T-14,
reescrituras T-15) y los compone en un unico `.md` legible, exactamente el mismo
patron que ya sigue `reescrituras.recopilar_propuestas` con `normalizar_guion`/
`detectar_problemas_guion`.

Estructura del documento, escena a escena:
- Cabecera con el mismo encabezado `## BLOQUE N -- <titulo>` del guion de origen
  (T-08), mas duracion estimada/objetivo, palabras y numero de bloques
  (requisito 1).
- Los bloques de respiracion (T-11) numerados dentro de la escena, cada uno
  delimitado por un ancla `<!-- bloque escena=N indice=K -->` (requisito 2):
  la misma idea que el ancla `<!-- reescritura id=... -->` de T-15, para que una
  edicion a mano del texto siga siendo localizable por posicion logica y no por
  columna o indentacion (requisito 7). Dentro de cada bloque, sus reescrituras
  propuestas (formato marcado de T-15) y sus avisos de locutabilidad (T-14) que
  no dieron ya lugar a una reescritura de particion, para no repetir el mismo
  aviso dos veces.
- Al pie de cada escena, las indicaciones no recitables (`**EN PANTALLA**`,
  `**NOTA**`, texto sin rotulo marcado `revisar`) con su motivo (requisito 4).
- Cabecera global con el resumen agregado de todo el guion (requisito 5) e
  instrucciones breves de edicion, incluida la marca de estado de la revision
  completa (requisito 6, ver `extraer_estado_revision`): el mismo mecanismo de
  "una palabra que el dueno sobrescribe" que ya usa T-15 para aceptar/rechazar.

Todo lo que no cabe dentro de una escena (preambulo, secciones auxiliares del
guion) no se repite aqui: ese texto no es locucion de una escena y ya vive
integro en el guion de origen; este documento es la vista de revision de lo que
se recita, no una copia completa del `.md` de entrada.
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from pathlib import Path

from clasificador import TIPO_LOCUCION, BloqueClasificado, clasificar_guion
from config import NOMBRE_ARCHIVO_GUION_ESCENAS, Configuracion
from deteccion import Aviso, ResultadoDeteccionBloque
from parser import Escena, ResultadoParseo
from reescrituras import Reescritura, formatear_reescritura, pendientes
from tiempos import BloqueConTiempo, ResultadoTiempos
from troceo import BloqueRespiracion

MARCA_ESTADO_PENDIENTE = "PENDIENTE"
MARCA_ESTADO_VALIDADO = "VALIDADO"

# Motivos de clasificacion (T-09) que son estructura del documento, no una
# "indicacion no recitable" que el dueno tenga que revisar: el propio rotulo
# (`**EN PANTALLA**` suelto) y el encabezado de escena ya se muestran en otro
# sitio, y una linea en blanco no tiene contenido que mostrar.
_SENALES_ESTRUCTURALES = frozenset({"encabezado", "blank", "rotulo"})

_PATRON_BLOQUE_TEXTO = re.compile(
    r"<!-- bloque escena=(?P<escena>\d+) indice=(?P<indice>\d+) -->"
    r"(?P<cuerpo>.*?)"
    r"<!-- /bloque -->",
    re.DOTALL,
)
_PATRON_ENCABEZADO_BLOQUE = re.compile(r"\A\s*\*\*Bloque\s+\d+\*\*[^\n]*\n*")
_PATRON_SUBBLOQUE_REESCRITURA = re.compile(
    r"<!-- reescritura id=[0-9a-f]+ -->.*?<!-- /reescritura -->", re.DOTALL
)
_PATRON_LINEA_AVISO = re.compile(r"^> .*$\n?", re.MULTILINE)
_PATRON_ESTADO_REVISION = re.compile(
    r"Estado de la revisi[oó]n\W*(PENDIENTE|VALIDADO)", re.IGNORECASE
)

_INSTRUCCIONES = """\
> Documento generado automáticamente (T-16) para revisar el guion completo de
> una sola sentada, en cualquier editor de texto plano, sin ir y venir en el
> chat.
>
> **Cómo editar:**
> - El texto de cada bloque de locución (bajo «Locución» en cada escena) se
>   puede corregir libremente: la próxima revalidación respeta tu edición y
>   nunca la sobrescribe.
> - Para **aceptar** o **rechazar** una reescritura propuesta, sustituye la
>   palabra `PENDIENTE` de su línea `**Decisión:**` por `ACEPTAR` o
>   `RECHAZAR`.
> - Para **forzar la clasificación** de un bloque marcado `REVISAR`, añade en
>   el guion de origen el rótulo `**LOCUCIÓN**`, `**EN PANTALLA**` o
>   `**NOTA**` que corresponda, siguiendo la convención del proyecto.
> - Cuando termines de revisar todo el documento, cambia la marca de más
>   abajo de `PENDIENTE` a `VALIDADO`.
>
> **Estado de la revisión:** PENDIENTE\
"""


def extraer_estado_revision(texto: str) -> str:
    """Lee la marca de estado de la revision completa (requisito 6): una sola
    palabra (`PENDIENTE`/`VALIDADO`) que el dueno sobrescribe a mano, con la
    misma tolerancia de lectura que `reescrituras.extraer_decisiones` (T-15).
    Si no se encuentra la marca -- el dueno la borro, o el texto no viene de
    este generador -- se asume `PENDIENTE`: nunca se da una revision por
    validada en silencio."""
    coincidencia = _PATRON_ESTADO_REVISION.search(texto)
    if coincidencia is None:
        return MARCA_ESTADO_PENDIENTE
    return coincidencia.group(1).upper()


def _mmss(segundos: float) -> str:
    total = max(round(segundos), 0)
    minutos, resto = divmod(total, 60)
    return f"{minutos}:{resto:02d}"


def _rango_mmss(inicio_segundos: float, fin_segundos: float) -> str:
    return f"{_mmss(inicio_segundos)} — {_mmss(fin_segundos)}"


def _bloques_de_escena(
    resultado_tiempos: ResultadoTiempos, numero_escena: int
) -> list[BloqueConTiempo]:
    return [b for b in resultado_tiempos.bloques if b.bloque.numero_escena == numero_escena]


def _reescrituras_de_bloque(
    bloque: BloqueRespiracion, reescrituras: list[Reescritura]
) -> list[Reescritura]:
    """Las reescrituras (T-15) que corresponden exactamente a este bloque de
    respiracion, no solo a su rango de lineas de origen: varios bloques de
    respiracion pueden compartir `linea_inicio`/`linea_fin` (T-11 no trackea
    posicion mas fina que el parrafo de origen), asi que la comprobacion final
    -- `texto[inicio:fin] == original` -- es la misma que ya garantiza
    `Normalizacion` (T-13) y la que hace unica la coincidencia."""
    return [
        reescritura
        for reescritura in reescrituras
        if reescritura.numero_escena == bloque.numero_escena
        and reescritura.linea_inicio == bloque.linea_inicio
        and reescritura.linea_fin == bloque.linea_fin
        and bloque.texto[reescritura.inicio : reescritura.fin] == reescritura.original
    ]


def _deteccion_de_bloque(
    bloque: BloqueRespiracion, detecciones: list[ResultadoDeteccionBloque]
) -> ResultadoDeteccionBloque | None:
    return next((deteccion for deteccion in detecciones if deteccion.bloque == bloque), None)


def _avisos_visibles(deteccion: ResultadoDeteccionBloque | None) -> list[Aviso]:
    """Avisos de un bloque que no se muestran ya como una reescritura de
    particion (requisito 3: no repetir el mismo problema dos veces). Solo la
    familia `sin_punto_respiracion` puede admitir particion (T-14, requisito
    6); cuando lo hace, `reescrituras.recopilar_propuestas` ya la convirtio en
    la `Reescritura` que se muestra junto al bloque."""
    if deteccion is None:
        return []
    return [
        aviso
        for aviso in deteccion.avisos
        if not (aviso.admite_particion and aviso.particion_sugerida is not None)
    ]


def formatear_aviso(aviso: Aviso) -> str:
    """Un aviso de locutabilidad (T-14) como linea de cita, igual de visible
    que una reescritura pero sin marca de decision: esta familia no se
    reescribe (alcance decidido por el dueno, §0.2), solo se senala."""
    return f"> ⚠ **Aviso ({aviso.familia}):** {aviso.mensaje} {aviso.recomendacion}"


def formatear_bloque_respiracion(
    numero_escena: int,
    indice: int,
    bloque_con_tiempo: BloqueConTiempo,
    reescrituras: list[Reescritura],
    detecciones: list[ResultadoDeteccionBloque],
) -> str:
    """Un bloque de respiracion numerado (requisito 2), con su franja horaria,
    sus reescrituras marcadas (T-15) y sus avisos localizados (T-14, requisito
    3). El ancla HTML delimita el texto editable para una futura revalidacion
    (T-17, requisito 7): tolera cualquier edicion dentro de ella."""
    bloque = bloque_con_tiempo.bloque
    rango = _rango_mmss(bloque_con_tiempo.inicio_segundos, bloque_con_tiempo.fin_segundos)
    aviso_corte = " *(corte forzado, sin puntuación natural cerca)*" if bloque.corte_forzado else ""
    partes = [
        f"<!-- bloque escena={numero_escena} indice={indice} -->",
        f"**Bloque {indice}** ({rango}){aviso_corte}",
        bloque.texto,
    ]
    for reescritura in _reescrituras_de_bloque(bloque, reescrituras):
        partes.append(formatear_reescritura(reescritura))
    for aviso in _avisos_visibles(_deteccion_de_bloque(bloque, detecciones)):
        partes.append(formatear_aviso(aviso))
    partes.append("<!-- /bloque -->")
    return "\n\n".join(partes)


def extraer_texto_bloques(texto: str) -> dict[tuple[int, int], str]:
    """Lee de vuelta el texto de cada bloque de respiracion (editado a mano o
    no) a partir de sus anclas `<!-- bloque escena=N indice=K -->`, indexado
    por `(numero_escena, indice)` (requisito 7: sigue siendo reprocesable tras
    una edicion arbitraria). Descarta la cabecera `**Bloque N** (...)` y
    cualquier reescritura o aviso insertado junto al texto -- ninguno de los
    dos es el texto de locucion en si -- y conserva solo lo que el dueno pueda
    haber corregido a mano."""
    resultado: dict[tuple[int, int], str] = {}
    for coincidencia in _PATRON_BLOQUE_TEXTO.finditer(texto):
        clave = (int(coincidencia.group("escena")), int(coincidencia.group("indice")))
        cuerpo = coincidencia.group("cuerpo")
        cuerpo = _PATRON_ENCABEZADO_BLOQUE.sub("", cuerpo, count=1)
        cuerpo = _PATRON_SUBBLOQUE_REESCRITURA.sub("", cuerpo)
        cuerpo = _PATRON_LINEA_AVISO.sub("", cuerpo)
        resultado[clave] = cuerpo.strip()
    return resultado


def _indicaciones_no_recitables(
    escena: Escena, bloques_clasificados: list[BloqueClasificado]
) -> list[BloqueClasificado]:
    """Las indicaciones no recitables de una escena (requisito 4): todo lo que
    T-09 clasifico como `no_locucion` o `revisar` dentro de su rango de
    lineas, salvo el propio encabezado de la escena y el rotulo suelto (ya
    visibles en otro sitio del documento) y las lineas en blanco (sin
    contenido que revisar)."""
    return [
        bloque
        for bloque in bloques_clasificados
        if escena.linea_inicio <= bloque.linea_inicio <= escena.linea_fin
        and bloque.tipo != TIPO_LOCUCION
        and bloque.senal not in _SENALES_ESTRUCTURALES
        and bloque.contenido.strip()
    ]


def formatear_indicaciones(
    bloques: list[BloqueClasificado], configuracion: Configuracion | None = None
) -> str:
    """Formatea las indicaciones no recitables al pie de una escena (requisito
    4), con la decision de clasificacion (`NO_LOCUCION`/`REVISAR`) y el motivo
    de T-09 a la vista, incluidos los bloques `revisar`."""
    configuracion = configuracion or Configuracion()
    if not bloques:
        return "*(ninguna)*"
    limite = configuracion.longitud_extracto_indicacion_max
    lineas = []
    for bloque in bloques:
        rango = (
            f"línea {bloque.linea_inicio}"
            if bloque.linea_inicio == bloque.linea_fin
            else f"líneas {bloque.linea_inicio}-{bloque.linea_fin}"
        )
        extracto = " ".join(bloque.contenido.split())
        if len(extracto) > limite:
            extracto = extracto[: limite - 1].rstrip() + "…"
        lineas.append(f'- **[{bloque.tipo.upper()}]** ({rango}): "{extracto}" — {bloque.motivo}')
    return "\n".join(lineas)


def _formatear_resumen_global(
    resultado: ResultadoParseo,
    resultado_tiempos: ResultadoTiempos,
    palabras_locucion: int,
    palabras_excluidas: int,
    total_avisos: int,
    reescrituras: list[Reescritura],
) -> str:
    """Cabecera con el resumen global del guion completo (requisito 5): total
    de escenas, palabras, duracion estimada, avisos y reescrituras pendientes,
    ritmo aplicado -- todo tomado de `calcular_tiempos` (T-12), la unica
    fuente de tiempos del proyecto, nunca recalculado aqui."""
    objetivo = resultado_tiempos.duracion_objetivo_total_segundos
    objetivo_texto = (
        f" (objetivo: {_mmss(objetivo[0])} — {_mmss(objetivo[1])})" if objetivo is not None else ""
    )
    aviso_total = f"\n- ⚠ {resultado_tiempos.aviso_total}" if resultado_tiempos.aviso_total else ""
    ritmo = resultado_tiempos.ritmo
    total_pendientes = len(pendientes(reescrituras))
    return (
        "## Resumen global\n\n"
        f"- **Escenas:** {len(resultado.escenas)}\n"
        f"- **Palabras de locución:** {palabras_locucion} (excluidas: {palabras_excluidas})\n"
        f"- **Duración estimada:** {_mmss(resultado_tiempos.duracion_total_segundos)}"
        f"{objetivo_texto}{aviso_total}\n"
        f"- **Ritmo aplicado:** {ritmo.ppm_aplicado} ppm (origen: {ritmo.origen}) — "
        f"{ritmo.motivo}\n"
        f"- **Avisos de locutabilidad:** {total_avisos}\n"
        f"- **Reescrituras:** {total_pendientes} pendientes de decidir, de "
        f"{len(reescrituras)} en total"
    )


def formatear_escena(
    escena: Escena,
    resultado_tiempos: ResultadoTiempos,
    palabras_locucion: int,
    palabras_excluidas: int,
    bloques_clasificados: list[BloqueClasificado],
    reescrituras: list[Reescritura],
    detecciones: list[ResultadoDeteccionBloque],
) -> str:
    """Una escena completa del documento de revision: cabecera (requisito 1),
    bloques de respiracion numerados (requisito 2) con sus reescrituras y
    avisos (requisito 3), e indicaciones no recitables al pie (requisito 4)."""
    tiempo_escena = next(t for t in resultado_tiempos.escenas if t.numero == escena.numero)
    bloques_escena = _bloques_de_escena(resultado_tiempos, escena.numero)

    objetivo_texto = (
        f" (objetivo: {_mmss(tiempo_escena.duracion_objetivo_segundos)})"
        if tiempo_escena.duracion_objetivo_segundos is not None
        else ""
    )
    aviso_texto = f"\n> ⚠ {tiempo_escena.aviso}" if tiempo_escena.aviso else ""

    cuerpo_bloques = "\n\n".join(
        formatear_bloque_respiracion(escena.numero, indice, bloque, reescrituras, detecciones)
        for indice, bloque in enumerate(bloques_escena, start=1)
    )
    if not cuerpo_bloques:
        cuerpo_bloques = "*(sin locución en esta escena)*"

    indicaciones = _indicaciones_no_recitables(escena, bloques_clasificados)

    return (
        f"## BLOQUE {escena.numero} — {escena.titulo}\n\n"
        f"**Duración estimada:** {_mmss(tiempo_escena.duracion_estimada_segundos)}"
        f"{objetivo_texto}{aviso_texto}\n\n"
        f"**Palabras:** {palabras_locucion} de locución / {palabras_excluidas} excluidas\n\n"
        f"**Bloques de respiración:** {len(bloques_escena)}\n\n"
        "### Locución\n\n"
        f"{cuerpo_bloques}\n\n"
        "### Indicaciones no recitables\n\n"
        f"{formatear_indicaciones(indicaciones)}"
    )


def generar_documento_revision(
    resultado: ResultadoParseo,
    resultado_tiempos: ResultadoTiempos,
    detecciones: list[ResultadoDeteccionBloque],
    reescrituras: list[Reescritura],
    configuracion: Configuracion | None = None,
    nombre_guion: str = "guion",
) -> str:
    """Genera el `.md` de revision completo de una sola pasada (T-16): todas
    las escenas del guion, en orden, con cobertura total de sus bloques de
    respiracion (criterio de aceptacion literal). No recalcula nada por su
    cuenta -- compone los resultados que ya calcularon T-08 a T-15."""
    configuracion = configuracion or Configuracion()
    clasificacion = clasificar_guion(resultado, configuracion)

    total_avisos = sum(len(deteccion.avisos) for deteccion in detecciones)
    palabras_locucion_total = sum(r.palabras_locucion for r in clasificacion.resumenes)
    palabras_excluidas_total = sum(r.palabras_excluidas for r in clasificacion.resumenes)

    cabecera_global = _formatear_resumen_global(
        resultado,
        resultado_tiempos,
        palabras_locucion_total,
        palabras_excluidas_total,
        total_avisos,
        reescrituras,
    )

    escenas_formateadas = []
    for escena in resultado.escenas:
        resumen = next(r for r in clasificacion.resumenes if r.numero == escena.numero)
        escenas_formateadas.append(
            formatear_escena(
                escena,
                resultado_tiempos,
                resumen.palabras_locucion,
                resumen.palabras_excluidas,
                clasificacion.bloques,
                reescrituras,
                detecciones,
            )
        )

    cuerpo_escenas = "\n\n---\n\n".join(escenas_formateadas)
    return (
        f"# Guion de revisión — {nombre_guion}\n\n"
        f"{_INSTRUCCIONES}\n\n"
        "---\n\n"
        f"{cabecera_global}\n\n"
        "---\n\n"
        f"{cuerpo_escenas}\n"
    )


def guardar_documento_revision(texto: str, carpeta_salida: Path) -> Path:
    """Escribe `guion-escenas.md` en la carpeta de salida del guion. Si ya
    existia una version previa -- casi siempre editada a mano por el dueno --
    se copia antes a `<nombre>.bak-<marca_de_tiempo>` (invariante (d) de §0.2:
    sin borrado destructivo). No es la escritura atomica de `estado.json`
    (T-07): aqui lo que protege el trabajo del dueno es la copia de seguridad,
    no que un corte a mitad de escritura sea imposible."""
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    destino = carpeta_salida / NOMBRE_ARCHIVO_GUION_ESCENAS
    if destino.exists():
        marca = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        copia_seguridad = destino.with_name(f"{destino.name}.bak-{marca}")
        copia_seguridad.write_bytes(destino.read_bytes())
    destino.write_text(texto, encoding="utf-8")
    return destino
