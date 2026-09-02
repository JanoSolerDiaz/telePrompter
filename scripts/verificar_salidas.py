"""Cuarta red de la verificacion (§0.1): comprobacion extremo a extremo de las salidas.

Sustituye al `build` de un proyecto convencional. Ejecuta la skill sobre el guion de
ejemplo y comprueba que lo generado es valido; sobre todo, que el reproductor `.html`
es **autocontenido** (regla dura de §0.2).

ESTADO ACTUAL (T-18, T-27, T-28, T-29): el reproductor, el exportador de `.srt`, el
exportador `.pdf` y el adaptador `.pptx` ya existen (`scripts/reproductor.py`,
`scripts/srt.py`, `scripts/pdf.py`, `scripts/pptx.py`), asi que "Generación del
reproductor", "Auto-contención del reproductor", "Generación del .srt", "Validez del
.srt", "Generación del HTML de impresión (.pdf)", "Auto-contención del HTML de
impresión", "Generación de tarjetas.json y brief (.pptx)" y "Validez de
tarjetas.json" dejan de ser NO APLICABLE: se generan de verdad, sobre el primer
guion real de calibracion a falta de `fixtures/guion-ejemplo.md` (T-32), y se
validan (a nivel de bytes el `.html` del reproductor y el de impresion, con las
reglas de ffmpeg el `.srt`, contra el contrato de `references/contrato-tarjetas.md`
el `tarjetas.json`). La conversion a `.pdf` de verdad depende de que haya un
Chrome/Edge instalado en la maquina que ejecuta la verificacion (T-28, requisito
4): cuando no lo hay, la etapa de generacion sigue en OK (el HTML de impresion se
genera igual, sin fallar) y lo dice en el detalle. La generacion real del `.pptx`
nunca la hace este codigo (T-29: la delega Claude en `480-branded-pptx` dentro de
la sesion), asi que su etapa de generacion sigue en OK con la salida `.pptx`
LATENTE mientras esa skill no este instalada -- nunca falla por su ausencia.
"Guion de ejemplo" y "Generación de salidas" (la canalizacion completa) siguen NO
APLICABLE hasta T-32 y T-30 respectivamente. Cada etapa se declara NO APLICABLE
nombrando la tarea que la implementara, para que la cuarta red diga siempre algo
verdadero y vaya cobrando sentido sola segun avanza el backlog. Responde al
hallazgo #4 del auditor.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import NOMBRE_ARCHIVO_HTML_IMPRESION, NOMBRE_ARCHIVO_SRT, NOMBRE_ARCHIVO_TARJETAS_JSON
from logger import configurar_logger
from parser import parsear_guion
from pdf import exportar_pdf
from pptx import exportar_pptx, validar_tarjetas
from presentacion import Nivel, mostrar, titulo
from reproductor import generar_reproductor_html, guardar_reproductor
from srt import exportar_srt, guardar_srt, validar_srt
from tiempos import calcular_tiempos

RAIZ = Path(__file__).resolve().parent.parent
FIXTURE_EJEMPLO = RAIZ / "fixtures" / "guion-ejemplo.md"
CARPETA_SALIDA_FIXTURE = RAIZ / "fixtures" / "salida"
CARPETA_GUIONES_REALES = RAIZ / "fixtures" / "reales"
RUTA_REPRODUCTOR_FIXTURE = CARPETA_SALIDA_FIXTURE / "reproductor.html"
RUTA_SRT_FIXTURE = CARPETA_SALIDA_FIXTURE / NOMBRE_ARCHIVO_SRT
RUTA_HTML_IMPRESION_FIXTURE = CARPETA_SALIDA_FIXTURE / NOMBRE_ARCHIVO_HTML_IMPRESION
RUTA_TARJETAS_JSON_FIXTURE = CARPETA_SALIDA_FIXTURE / NOMBRE_ARCHIVO_TARJETAS_JSON

# Patrones prohibidos en cualquier salida .html (§0.2, "salida autocontenida").
PATRONES_RECURSO_EXTERNO: tuple[tuple[str, str], ...] = (
    (r"https?://", "referencia a una URL http(s)"),
    (r"//cdn\.", "referencia a un CDN"),
    (r"""<link[^>]+rel=["']?stylesheet""", "hoja de estilos enlazada"),
    (r"@import\s", "@import de CSS"),
    (r"\bfetch\s*\(", "llamada a fetch()"),
    (r"XMLHttpRequest", "uso de XMLHttpRequest"),
    (
        r"""<(?:script|img|iframe|video|audio|source)[^>]+src=["']?(?!data:)[a-zA-Z0-9./]""",
        "recurso externo en un atributo src",
    ),
)


@dataclass
class Resultado:
    """Resultado de una etapa de verificacion."""

    etapa: str
    estado: str  # "OK" | "FALLO" | "NO APLICABLE"
    detalle: str

    @property
    def es_fallo(self) -> bool:
        return self.estado == "FALLO"


def buscar_recursos_externos(html: str) -> list[str]:
    """Devuelve la lista de recursos externos encontrados en un HTML. Vacia = autocontenido."""
    hallazgos: list[str] = []
    for patron, descripcion in PATRONES_RECURSO_EXTERNO:
        if re.search(patron, html, flags=re.IGNORECASE):
            hallazgos.append(descripcion)
    return hallazgos


def verificar_autocontencion(
    ruta_html: Path, etapa: str = "Auto-contencion del reproductor"
) -> Resultado:
    """Comprueba que un `.html` generado (reproductor o impresion) no depende de nada externo."""
    if not ruta_html.exists():
        return Resultado(
            etapa,
            "NO APLICABLE",
            f"no se ha generado ningun archivo en {ruta_html}.",
        )
    hallazgos = buscar_recursos_externos(ruta_html.read_text(encoding="utf-8"))
    if hallazgos:
        return Resultado(
            etapa,
            "FALLO",
            "el HTML depende de recursos externos: " + "; ".join(hallazgos),
        )
    return Resultado(etapa, "OK", f"{ruta_html.name} es autocontenido.")


def verificar_fixture() -> Resultado:
    """Comprueba que existe el guion de ejemplo sobre el que se hace el extremo a extremo."""
    if not FIXTURE_EJEMPLO.exists():
        return Resultado(
            "Guion de ejemplo",
            "NO APLICABLE",
            "`fixtures/guion-ejemplo.md` se crea en T-32.",
        )
    if not FIXTURE_EJEMPLO.read_text(encoding="utf-8").strip():
        return Resultado("Guion de ejemplo", "FALLO", "el guion de ejemplo esta vacio.")
    return Resultado("Guion de ejemplo", "OK", "presente y con contenido.")


def generar_reproductor_fixture() -> Resultado:
    """Genera el reproductor (T-18) sobre el primer guion real de calibracion.

    A falta de `fixtures/guion-ejemplo.md` (T-32, todavia no existe), usa el mismo
    material de `fixtures/reales/` que ya calibra T-08 a T-17, para que la
    comprobacion de auto-contencion tenga un archivo de verdad que validar en vez
    de quedarse NO APLICABLE indefinidamente."""
    guiones = sorted(CARPETA_GUIONES_REALES.glob("*.md"))
    if not guiones:
        return Resultado(
            "Generación del reproductor",
            "NO APLICABLE",
            "no hay guiones reales en fixtures/reales/ con los que generarlo.",
        )
    ruta_guion = guiones[0]
    try:
        texto = ruta_guion.read_text(encoding="utf-8")
        resultado = parsear_guion(texto)
        tiempos = calcular_tiempos(resultado)
        pagina = generar_reproductor_html(resultado, tiempos, nombre_guion=ruta_guion.stem)
        guardar_reproductor(pagina, CARPETA_SALIDA_FIXTURE)
    except Exception as excepcion:  # se informa en el resultado, nunca se oculta
        return Resultado(
            "Generación del reproductor",
            "FALLO",
            f"no se pudo generar el reproductor sobre {ruta_guion.name}: {excepcion}",
        )
    return Resultado(
        "Generación del reproductor", "OK", f"generado sobre {ruta_guion.name}."
    )


def verificar_generacion() -> Resultado:
    """Ejecuta la skill sobre el guion de ejemplo. Pendiente hasta que exista la canalizacion."""
    return Resultado(
        "Generacion de salidas",
        "NO APLICABLE",
        "la canalizacion completa se cierra en T-30; se activara aqui sin tocar el protocolo.",
    )


def generar_srt_fixture() -> Resultado:
    """Genera el .srt borrador (T-27) sobre el mismo guion real que usa el reproductor.

    Mismo criterio que `generar_reproductor_fixture`: a falta de
    `fixtures/guion-ejemplo.md` (T-32), usa el primer guion real de
    `fixtures/reales/`."""
    guiones = sorted(CARPETA_GUIONES_REALES.glob("*.md"))
    if not guiones:
        return Resultado(
            "Generación del .srt",
            "NO APLICABLE",
            "no hay guiones reales en fixtures/reales/ con los que generarlo.",
        )
    ruta_guion = guiones[0]
    try:
        texto = ruta_guion.read_text(encoding="utf-8")
        resultado = parsear_guion(texto)
        tiempos = calcular_tiempos(resultado)
        contenido = exportar_srt(tiempos)
        guardar_srt(contenido, CARPETA_SALIDA_FIXTURE)
    except Exception as excepcion:  # se informa en el resultado, nunca se oculta
        return Resultado(
            "Generación del .srt",
            "FALLO",
            f"no se pudo generar el .srt sobre {ruta_guion.name}: {excepcion}",
        )
    return Resultado("Generación del .srt", "OK", f"generado sobre {ruta_guion.name}.")


def generar_pdf_fixture() -> Resultado:
    """Genera el HTML de impresion y, si hay Chrome/Edge, el `.pdf` (T-28) sobre
    el mismo guion real que usan el reproductor y el .srt.

    Mismo criterio que `generar_reproductor_fixture`/`generar_srt_fixture`: a
    falta de `fixtures/guion-ejemplo.md` (T-32), usa el primer guion real de
    `fixtures/reales/`. La ausencia de Chrome/Edge en la maquina de
    verificacion no es un fallo (requisito 4 de T-28: la skill nunca falla
    por su ausencia), asi que esta etapa sigue en OK sin el `.pdf` real."""
    guiones = sorted(CARPETA_GUIONES_REALES.glob("*.md"))
    if not guiones:
        return Resultado(
            "Generación del HTML de impresión (.pdf)",
            "NO APLICABLE",
            "no hay guiones reales en fixtures/reales/ con los que generarlo.",
        )
    ruta_guion = guiones[0]
    try:
        texto = ruta_guion.read_text(encoding="utf-8")
        resultado = parsear_guion(texto)
        tiempos = calcular_tiempos(resultado)
        resultado_pdf = exportar_pdf(
            resultado, tiempos, CARPETA_SALIDA_FIXTURE, nombre_guion=ruta_guion.stem
        )
    except Exception as excepcion:  # se informa en el resultado, nunca se oculta
        return Resultado(
            "Generación del HTML de impresión (.pdf)",
            "FALLO",
            f"no se pudo generar el HTML de impresion sobre {ruta_guion.name}: {excepcion}",
        )
    detalle = f"generado sobre {ruta_guion.name}. {resultado_pdf.mensaje}"
    return Resultado("Generación del HTML de impresión (.pdf)", "OK", detalle)


def generar_pptx_fixture() -> Resultado:
    """Genera `tarjetas.json` y el brief de invocacion (T-29) sobre el mismo
    guion real que usan el reproductor, el .srt y el HTML de impresion.

    Mismo criterio que las demas etapas: a falta de
    `fixtures/guion-ejemplo.md` (T-32), usa el primer guion real de
    `fixtures/reales/`. La ausencia de la skill de marca `480-branded-pptx`
    en la maquina de verificacion no es un fallo (requisito 4 de T-29: la
    skill nunca falla por su ausencia), asi que esta etapa sigue en OK con
    la salida .pptx marcada como latente en el detalle."""
    guiones = sorted(CARPETA_GUIONES_REALES.glob("*.md"))
    if not guiones:
        return Resultado(
            "Generación de tarjetas.json y brief (.pptx)",
            "NO APLICABLE",
            "no hay guiones reales en fixtures/reales/ con los que generarlo.",
        )
    ruta_guion = guiones[0]
    try:
        texto = ruta_guion.read_text(encoding="utf-8")
        resultado = parsear_guion(texto)
        tiempos = calcular_tiempos(resultado)
        resultado_pptx = exportar_pptx(
            resultado, tiempos, CARPETA_SALIDA_FIXTURE, nombre_guion=ruta_guion.stem
        )
    except Exception as excepcion:  # se informa en el resultado, nunca se oculta
        return Resultado(
            "Generación de tarjetas.json y brief (.pptx)",
            "FALLO",
            f"no se pudo generar sobre {ruta_guion.name}: {excepcion}",
        )
    detalle = f"generado sobre {ruta_guion.name}. {resultado_pptx.mensaje}"
    return Resultado("Generación de tarjetas.json y brief (.pptx)", "OK", detalle)


def verificar_tarjetas_json(ruta_json: Path) -> Resultado:
    """Valida `tarjetas.json` contra el contrato de
    `references/contrato-tarjetas.md` (T-29, requisito 1)."""
    if not ruta_json.exists():
        return Resultado(
            "Validez de tarjetas.json",
            "NO APLICABLE",
            f"no se ha generado ningun tarjetas.json en {ruta_json}.",
        )
    try:
        datos = json.loads(ruta_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError as excepcion:
        return Resultado("Validez de tarjetas.json", "FALLO", f"JSON invalido: {excepcion}")
    problemas = validar_tarjetas(datos)
    if problemas:
        return Resultado("Validez de tarjetas.json", "FALLO", "; ".join(problemas))
    return Resultado("Validez de tarjetas.json", "OK", f"{ruta_json.name} cumple el contrato.")


def verificar_srt(ruta_srt: Path) -> Resultado:
    """Valida el .srt generado con las mismas reglas que aplica ffmpeg (T-27, requisito 5)."""
    if not ruta_srt.exists():
        return Resultado(
            "Validez del .srt",
            "NO APLICABLE",
            f"no se ha generado ningun .srt en {ruta_srt}.",
        )
    problemas = validar_srt(ruta_srt.read_text(encoding="utf-8"))
    if problemas:
        return Resultado("Validez del .srt", "FALLO", "; ".join(problemas))
    return Resultado("Validez del .srt", "OK", f"{ruta_srt.name} pasa el validador estricto.")


def main() -> int:
    analizador = argparse.ArgumentParser(
        description="Verificacion extremo a extremo de las salidas de la skill teleprompter.",
    )
    analizador.add_argument(
        "--fixture",
        action="store_true",
        help="Ejecuta la verificacion sobre el guion de ejemplo del repositorio.",
    )
    analizador.add_argument(
        "--verbose",
        action="store_true",
        help="Ademas de al archivo de log, vuelca el diagnostico tecnico por stderr.",
    )
    argumentos = analizador.parse_args()
    if not argumentos.fixture:
        mostrar("Indica --fixture para verificar sobre el guion de ejemplo.", Nivel.ERROR)
        return 2

    log = configurar_logger(CARPETA_SALIDA_FIXTURE, verbose=argumentos.verbose)
    log.info("Arranca la verificacion extremo a extremo sobre el guion de ejemplo.")

    titulo("Verificacion de salidas (cuarta red)")
    resultados = [
        verificar_fixture(),
        verificar_generacion(),
        generar_reproductor_fixture(),
        verificar_autocontencion(RUTA_REPRODUCTOR_FIXTURE),
        generar_srt_fixture(),
        verificar_srt(RUTA_SRT_FIXTURE),
        generar_pdf_fixture(),
        verificar_autocontencion(
            RUTA_HTML_IMPRESION_FIXTURE, etapa="Auto-contención del HTML de impresión"
        ),
        generar_pptx_fixture(),
        verificar_tarjetas_json(RUTA_TARJETAS_JSON_FIXTURE),
    ]

    for resultado in resultados:
        nivel = {
            "OK": Nivel.OK,
            "FALLO": Nivel.ERROR,
            "NO APLICABLE": Nivel.AVISO,
        }[resultado.estado]
        mostrar(f"{resultado.etapa}: {resultado.estado} — {resultado.detalle}", nivel)
        log.debug("Etapa %r: %s — %s", resultado.etapa, resultado.estado, resultado.detalle)

    fallos = [r for r in resultados if r.es_fallo]
    pendientes = [r for r in resultados if r.estado == "NO APLICABLE"]

    if fallos:
        log.error("Verificacion fallida: %d etapa(s) rotas.", len(fallos))
        mostrar(f"Verificacion FALLIDA: {len(fallos)} etapa(s) rotas. No commitear.", Nivel.ERROR)
        return 1

    if pendientes:
        mostrar(
            f"OK con {len(pendientes)} etapa(s) aun no aplicables "
            "(el backlog las ira activando). Nada roto.",
            Nivel.OK,
        )
    else:
        mostrar("OK — todas las etapas verificadas.", Nivel.OK)
    log.info("Verificacion completada sin fallos (%d etapa(s) pendiente(s)).", len(pendientes))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
