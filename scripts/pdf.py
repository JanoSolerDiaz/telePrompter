"""Exportador `.pdf` con identidad 480 (tarea T-28).

Documento de repaso antes de grabar y, llegado el caso, entregable presentable
a terceros: el guion de locucion completo, una escena por pagina, con la
identidad visual de la casa (`references/marca-480.md`). Este modulo no
recalcula nada por su cuenta -- consume `ResultadoTiempos` tal cual, mismo
patron que `srt.exportar_srt` (T-27): el texto de cada bloque ya es el
LOCUTADO FINAL (reescrituras aceptadas materializadas si `resultado_tiempos`
viene de una revalidacion, T-17). Por eso este modulo, a diferencia de
`documento_revision` (T-16), nunca muestra el aparato de reescrituras
(`<!-- reescritura ... -->`, original/propuesta/decision): esa vista de
edicion ya vive en `guion-escenas.md`; aqui solo hay texto ya decidido, en
prosa legible, en las dos variantes del documento (repaso y entregable).

Auto-contencion (regla dura de §0.2): el logotipo se incrusta como
`data:image/png;base64,...` -- una referencia de archivo local, aunque no sea
remota, tambien la rechaza `verificar_salidas.buscar_recursos_externos` (regla
deliberada: un `.html` autocontenido no depende de NINGUN archivo aparte, ni
siquiera local). Sin fuentes descargadas: se resuelven por nombre del sistema
con la pila de respaldo de `Configuracion` (requisito 2).

Notas internas vs. indicaciones de pantalla (requisito 6, modo
`--para-terceros`): una indicacion no recitable (`**EN PANTALLA**`/`**NOTA**`,
T-09) se omite solo si su motivo de clasificacion identifica el rotulo `NOTA`
-- las etiquetadas `EN PANTALLA`, o las ambiguas sin senal clara (`revisar`),
se mantienen siempre, porque no hay forma de saber que una indicacion sin
rotulo es "interna" y no una instruccion de pantalla real (T-09, requisito 5:
nunca se decide en silencio). `Configuracion.incluir_notas_internas` es el
mismo interruptor que usara T-29: `False` es el modo `--para-terceros`.

Logotipo (requisito 3): la relacion de aspecto se mide leyendo la cabecera
`IHDR` del PNG en tiempo de generacion -- la constante `668/376` de la guia de
marca NO se usa en ninguna parte de este codigo (deforma los archivos reales,
ver `references/marca-480.md`). Si el archivo no existe o no es un PNG valido,
el PDF sale sin logotipo y la generacion no falla.

Conversion a PDF (requisito 4): Chrome/Edge en modo headless
(`--print-to-pdf`), detectado por nombre conocido en el `PATH` o rutas de
instalacion estandar de Windows/macOS (`Configuracion.pdf_chrome_ejecutable_manual`
tiene prioridad si el dueno la fija). Sin ejecutable disponible, se deja el
HTML de impresion listo con instrucciones de Ctrl+P: nunca se falla por su
ausencia.
"""

from __future__ import annotations

import base64
import html
import os
import shutil
import struct
import subprocess
from dataclasses import dataclass
from pathlib import Path

from clasificador import TIPO_LOCUCION, BloqueClasificado, ResultadoClasificacion, clasificar_guion
from config import (
    NOMBRE_ARCHIVO_HTML_IMPRESION,
    NOMBRE_ARCHIVO_PDF,
    Configuracion,
)
from parser import Escena, ResultadoParseo
from tiempos import BloqueConTiempo, ResultadoTiempos

RAIZ = Path(__file__).resolve().parent.parent
_CARPETA_PLANTILLAS = RAIZ / "assets" / "pdf"
_FIRMA_PNG = b"\x89PNG\r\n\x1a\n"

# Mismo criterio que `documento_revision._SENALES_ESTRUCTURALES`: el encabezado
# de escena y el rotulo suelto ya se muestran en otro sitio del documento, y una
# linea en blanco no tiene contenido que listar como indicacion.
_SENALES_ESTRUCTURALES = frozenset({"encabezado", "blank", "rotulo"})

_NOMBRES_EJECUTABLES_CHROME: tuple[str, ...] = (
    "google-chrome-stable",
    "google-chrome",
    "chromium-browser",
    "chromium",
    "microsoft-edge-stable",
    "microsoft-edge",
    "msedge",
)
_RUTAS_INSTALACION_ESTANDAR: tuple[str, ...] = (
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
)


def _leer_plantilla(nombre: str) -> str:
    return (_CARPETA_PLANTILLAS / nombre).read_text(encoding="utf-8")


def _dimensiones_png(ruta: Path) -> tuple[int, int] | None:
    """Ancho y alto de un PNG leidos de su cabecera `IHDR` (requisito 3): la
    relacion de aspecto se mide siempre del archivo, nunca se codifica una
    constante (ver `references/marca-480.md`). `None` si el archivo no existe,
    no es legible o no es un PNG valido -- el logotipo se omite sin romper la
    generacion, nunca una excepcion."""
    try:
        cabecera = ruta.open("rb").read(24)
    except OSError:
        return None
    if len(cabecera) < 24 or cabecera[:8] != _FIRMA_PNG or cabecera[12:16] != b"IHDR":
        return None
    ancho, alto = struct.unpack(">II", cabecera[16:24])
    if ancho <= 0 or alto <= 0:
        return None
    return ancho, alto


def _logo_html(ancho_pulgadas: float, clase_css: str, configuracion: Configuracion) -> str:
    """El logotipo incrustado como `data:` (auto-contencion) con su alto
    calculado a partir de la relacion de aspecto medida (requisito 3):
    `alto = ancho / ratio`. Cadena vacia si el archivo no esta disponible o no
    es un PNG legible -- el PDF sale sin logotipo, nunca falla."""
    ruta_configurada = Path(configuracion.ruta_logo_pdf)
    ruta = ruta_configurada if ruta_configurada.is_absolute() else RAIZ / ruta_configurada
    dimensiones = _dimensiones_png(ruta)
    if dimensiones is None:
        return ""
    ancho_px, alto_px = dimensiones
    alto_pulgadas = ancho_pulgadas / (ancho_px / alto_px)
    contenido = base64.b64encode(ruta.read_bytes()).decode("ascii")
    return (
        f'<img class="{clase_css}" alt="480" '
        f'style="width:{ancho_pulgadas:.3f}in;height:{alto_pulgadas:.3f}in" '
        f'src="data:image/png;base64,{contenido}">'
    )


def _mmss(segundos: float) -> str:
    total = max(round(segundos), 0)
    minutos, resto = divmod(total, 60)
    return f"{minutos}:{resto:02d}"


def _rango_mmss(inicio_segundos: float, fin_segundos: float) -> str:
    return f"{_mmss(inicio_segundos)} — {_mmss(fin_segundos)}"


def _pila_tipografica(configuracion: Configuracion) -> str:
    fuentes = (configuracion.tipografia_marca, *configuracion.respaldo_tipografico)
    return ", ".join(f'"{fuente}"' if " " in fuente else fuente for fuente in fuentes)


def _prosa_escena(bloques: list[BloqueConTiempo]) -> str:
    """El texto de locucion de una escena como prosa continua (requisito 5):
    cada bloque de respiracion en su propio `<span>`, con el limite marcado de
    forma discreta por CSS (`.bloque:not(:last-child)::after`), nunca como
    lista de tarjetas. `html.escape` es la unica proteccion necesaria: este
    documento no incrusta datos en un `<script>` como el reproductor (T-18),
    asi que no hace falta el escapado Unicode de `_json_seguro_para_script`."""
    if not bloques:
        return "<em>(sin locución en esta escena)</em>"
    spans = "\n".join(
        f'<span class="bloque">{html.escape(bloque.bloque.texto)}</span>' for bloque in bloques
    )
    return f'<p class="prosa">{spans}</p>'


def _es_nota_interna(bloque: BloqueClasificado) -> bool:
    """`True` si la indicacion viene de un rotulo/senal `NOTA` (nota interna
    de produccion, requisito 6): se detecta por el nombre del rotulo dentro
    del motivo de clasificacion (T-09), que siempre lo cita literalmente
    (`"rotulo 'NOTA': ..."`, `"prefijo 'NOTA:'"`). Cualquier otra indicacion
    -- `EN PANTALLA`, o ambigua sin senal clara -- se trata como indicacion de
    pantalla y se mantiene siempre: nunca se decide en silencio (T-09,
    requisito 5) que algo sin marcar como nota es prescindible."""
    return "nota" in bloque.motivo.lower()


def _indicaciones_no_recitables(
    escena: Escena, bloques_clasificados: list[BloqueClasificado]
) -> list[BloqueClasificado]:
    return [
        bloque
        for bloque in bloques_clasificados
        if escena.linea_inicio <= bloque.linea_inicio <= escena.linea_fin
        and bloque.tipo != TIPO_LOCUCION
        and bloque.senal not in _SENALES_ESTRUCTURALES
        and bloque.contenido.strip()
    ]


def _formatear_indicaciones_html(
    bloques: list[BloqueClasificado], configuracion: Configuracion
) -> str:
    """Indicaciones no recitables al pie de la escena (requisito 5), omitiendo
    las notas internas de produccion cuando `incluir_notas_internas=False`
    (requisito 6, modo `--para-terceros`)."""
    visibles = [
        bloque
        for bloque in bloques
        if configuracion.incluir_notas_internas or not _es_nota_interna(bloque)
    ]
    if not visibles:
        return '<p class="sin-indicaciones">(ninguna)</p>'
    limite = configuracion.longitud_extracto_indicacion_max
    items = []
    for bloque in visibles:
        extracto = " ".join(bloque.contenido.split())
        if len(extracto) > limite:
            extracto = extracto[: limite - 1].rstrip() + "…"
        items.append(f"<li>{html.escape(extracto)}</li>")
    return "<ul>" + "".join(items) + "</ul>"


def _pagina_portada(
    resultado: ResultadoParseo,
    resultado_tiempos: ResultadoTiempos,
    clasificacion: ResultadoClasificacion,
    nombre_guion: str,
    configuracion: Configuracion,
) -> str:
    """Portada (requisito 7): titulo, duracion objetivo y total, numero de
    escenas y de palabras de locucion."""
    logo = _logo_html(
        configuracion.pdf_ancho_logo_portada_pulgadas, "logo logo-portada", configuracion
    )
    objetivo = resultado_tiempos.duracion_objetivo_total_segundos
    objetivo_texto = (
        f" (objetivo: {_mmss(objetivo[0])} — {_mmss(objetivo[1])})" if objetivo is not None else ""
    )
    palabras_totales = sum(resumen.palabras_locucion for resumen in clasificacion.resumenes)
    return (
        '<section class="pagina portada">'
        f"{logo}"
        f"<h1>{html.escape(nombre_guion)}</h1>"
        f'<p class="subtitulo">Duración estimada: '
        f"{_mmss(resultado_tiempos.duracion_total_segundos)}{objetivo_texto}</p>"
        f'<p class="meta">{len(resultado.escenas)} escenas · {palabras_totales} palabras '
        "de locución</p>"
        "</section>"
    )


def _pagina_escena(
    escena: Escena,
    resultado_tiempos: ResultadoTiempos,
    bloques_clasificados: list[BloqueClasificado],
    nombre_guion: str,
    configuracion: Configuracion,
) -> str:
    tiempo_escena = next(t for t in resultado_tiempos.escenas if t.numero == escena.numero)
    bloques_escena = [
        b for b in resultado_tiempos.bloques if b.bloque.numero_escena == escena.numero
    ]
    objetivo_texto = (
        f" · Objetivo: {_mmss(tiempo_escena.duracion_objetivo_segundos)}"
        if tiempo_escena.duracion_objetivo_segundos is not None
        else ""
    )
    aviso_html = (
        f' <span class="aviso-desviacion">⚠ {html.escape(tiempo_escena.aviso)}</span>'
        if tiempo_escena.aviso
        else ""
    )
    indicaciones = _indicaciones_no_recitables(escena, bloques_clasificados)
    logo_pie = _logo_html(configuracion.pdf_ancho_logo_pie_pulgadas, "logo-pie", configuracion)
    return (
        '<section class="pagina escena">'
        f"<h2>BLOQUE {escena.numero} — {html.escape(escena.titulo)}</h2>"
        '<div class="linea-acento"></div>'
        f'<p class="meta-escena">Duración estimada: '
        f"{_mmss(tiempo_escena.duracion_estimada_segundos)}{objetivo_texto}{aviso_html}</p>"
        f"{_prosa_escena(bloques_escena)}"
        '<div class="pie-escena"><h3>Indicaciones no recitables</h3>'
        f"{_formatear_indicaciones_html(indicaciones, configuracion)}</div>"
        f'<footer class="pie-pagina">{logo_pie}<span>{html.escape(nombre_guion)}</span></footer>'
        "</section>"
    )


def generar_html_impresion(
    resultado: ResultadoParseo,
    resultado_tiempos: ResultadoTiempos,
    nombre_guion: str = "guion",
    configuracion: Configuracion | None = None,
) -> str:
    """Compone el HTML de impresion completo (requisito 1): portada +
    una pagina por escena (criterio de aceptacion: tantas paginas como
    escenas mas la portada). Autocontenido de principio a fin -- sin
    dependencias de terceros, fuentes por nombre del sistema (requisito 8)."""
    configuracion = configuracion or Configuracion()
    clasificacion = clasificar_guion(resultado, configuracion)

    estilo = (
        _leer_plantilla("estilo.css")
        .replace("__MARGEN_SUPERIOR_IN__", str(configuracion.pdf_margen_superior_pulgadas))
        .replace("__MARGEN_LATERAL_IN__", str(configuracion.pdf_margen_lateral_pulgadas))
        .replace("__COLOR_FONDO__", configuracion.pdf_color_fondo)
        .replace("__COLOR_TEXTO_SECUNDARIO__", configuracion.pdf_color_texto_secundario)
        .replace("__COLOR_TEXTO__", configuracion.pdf_color_texto)
        .replace("__COLOR_ACENTO__", configuracion.pdf_color_acento)
        .replace("__COLOR_ALERTA__", configuracion.pdf_color_alerta)
        .replace("__COLOR_BORDE__", configuracion.pdf_color_borde)
        .replace("__INTERLINEADO__", str(configuracion.pdf_interlineado))
        .replace("__PILA_TIPOGRAFICA__", _pila_tipografica(configuracion))
    )

    paginas = [
        _pagina_portada(resultado, resultado_tiempos, clasificacion, nombre_guion, configuracion)
    ]
    for escena in resultado.escenas:
        paginas.append(
            _pagina_escena(
                escena, resultado_tiempos, clasificacion.bloques, nombre_guion, configuracion
            )
        )

    return (
        _leer_plantilla("plantilla.html")
        .replace("__ESTILO__", estilo)
        .replace("__TITULO__", html.escape(nombre_guion, quote=True))
        .replace("__CUERPO__", "\n".join(paginas))
    )


def guardar_html_impresion(html_impresion: str, carpeta_salida: Path) -> Path:
    """Escribe el HTML de impresion en la carpeta de salida del guion (regla
    de aislamiento, §0.2)."""
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    destino = carpeta_salida / NOMBRE_ARCHIVO_HTML_IMPRESION
    destino.write_text(html_impresion, encoding="utf-8")
    return destino


def detectar_ejecutable_chrome(configuracion: Configuracion) -> Path | None:
    """Localiza un ejecutable de Chrome/Edge (requisito 4). Prioridad: la
    ruta manual del dueno si la fija; si no, nombres conocidos en el `PATH`
    (cubre Linux/macOS con Chrome o Chromium instalados de forma estandar);
    si no, las rutas de instalacion estandar de Windows y macOS. `None` si
    no se encuentra ninguno -- nunca una excepcion."""
    if configuracion.pdf_chrome_ejecutable_manual:
        ruta_manual = Path(configuracion.pdf_chrome_ejecutable_manual)
        return ruta_manual if ruta_manual.is_file() else None
    for nombre in _NOMBRES_EJECUTABLES_CHROME:
        encontrado = shutil.which(nombre)
        if encontrado:
            return Path(encontrado)
    for ruta_texto in _RUTAS_INSTALACION_ESTANDAR:
        ruta = Path(ruta_texto)
        if ruta.is_file():
            return ruta
    local_appdata = os.environ.get("LOCALAPPDATA")
    if local_appdata:
        for subruta in (
            ("Google", "Chrome", "Application", "chrome.exe"),
            ("Microsoft", "Edge", "Application", "msedge.exe"),
        ):
            ruta_usuario = Path(local_appdata).joinpath(*subruta)
            if ruta_usuario.is_file():
                return ruta_usuario
    return None


def convertir_html_a_pdf(
    ruta_html: Path, ruta_pdf: Path, ejecutable_chrome: Path, configuracion: Configuracion
) -> tuple[bool, str]:
    """Invoca Chrome/Edge en modo headless para convertir `ruta_html` a
    `ruta_pdf` (requisito 4). Nunca lanza una excepcion: cualquier fallo
    (ejecutable roto, tiempo agotado, codigo de salida distinto de cero) se
    devuelve como mensaje accionable."""
    argumentos = [
        str(ejecutable_chrome),
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={ruta_pdf}",
    ]
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        # Chrome se niega a arrancar como root sin este flag (verificado en esta
        # sesion, sandbox de nube ejecutandose como root); en la maquina del
        # dueno, sin privilegios de administrador, este bloque no se activa.
        argumentos.append("--no-sandbox")
    argumentos.append(ruta_html.resolve().as_uri())
    try:
        proceso = subprocess.run(
            argumentos,
            capture_output=True,
            timeout=configuracion.pdf_timeout_conversion_segundos,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as excepcion:
        return False, f"No se pudo ejecutar Chrome/Edge ({ejecutable_chrome}): {excepcion}"
    if proceso.returncode != 0 or not ruta_pdf.exists():
        lineas_error = proceso.stderr.decode("utf-8", errors="replace").strip().splitlines()
        detalle = lineas_error[-1] if lineas_error else f"código de salida {proceso.returncode}"
        return False, f"Chrome/Edge no pudo generar el PDF: {detalle}"
    return True, f"PDF generado en {ruta_pdf}."


@dataclass(frozen=True)
class ResultadoPdf:
    """Resultado de `exportar_pdf`: el HTML de impresion siempre existe; el
    PDF solo si se encontro y funciono un Chrome/Edge headless (requisito 4).
    `mensaje` es siempre accionable, se haya generado el PDF o no."""

    ruta_html: Path
    ruta_pdf: Path | None
    mensaje: str


def exportar_pdf(
    resultado: ResultadoParseo,
    resultado_tiempos: ResultadoTiempos,
    carpeta_salida: Path,
    nombre_guion: str = "guion",
    configuracion: Configuracion | None = None,
) -> ResultadoPdf:
    """Punto de entrada normal del modulo: genera el HTML de impresion, lo
    guarda y, si hay un Chrome/Edge disponible, lo convierte a `.pdf`. Nunca
    falla por la ausencia de Chrome (requisito 4): deja el HTML listo con
    instrucciones de Ctrl+P."""
    configuracion = configuracion or Configuracion()
    html_impresion = generar_html_impresion(
        resultado, resultado_tiempos, nombre_guion, configuracion
    )
    ruta_html = guardar_html_impresion(html_impresion, carpeta_salida)

    ejecutable = detectar_ejecutable_chrome(configuracion)
    if ejecutable is None:
        mensaje = (
            f"Chrome/Edge no encontrado: abre {ruta_html.name} en el navegador y usa "
            "Ctrl+P (Imprimir → Guardar como PDF) para exportarlo a mano."
        )
        return ResultadoPdf(ruta_html, None, mensaje)

    ruta_pdf = carpeta_salida / NOMBRE_ARCHIVO_PDF
    exito, mensaje = convertir_html_a_pdf(ruta_html, ruta_pdf, ejecutable, configuracion)
    if not exito:
        mensaje += f" El HTML de impresión queda listo en {ruta_html.name} para exportar a mano."
        return ResultadoPdf(ruta_html, None, mensaje)
    return ResultadoPdf(ruta_html, ruta_pdf, mensaje)
