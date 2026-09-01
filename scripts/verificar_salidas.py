"""Cuarta red de la verificacion (§0.1): comprobacion extremo a extremo de las salidas.

Sustituye al `build` de un proyecto convencional. Ejecuta la skill sobre el guion de
ejemplo y comprueba que lo generado es valido; sobre todo, que el reproductor `.html`
es **autocontenido** (regla dura de §0.2).

ESTADO ACTUAL (T-00): las etapas que verifica todavia no existen. En lugar de fingir
que pasa o de fallar siempre, cada etapa se declara NO APLICABLE nombrando la tarea que
la implementara. Asi la cuarta red dice siempre algo verdadero y va cobrando sentido
sola segun avanza el backlog. Responde al hallazgo #4 del auditor.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from logger import configurar_logger
from presentacion import Nivel, mostrar, titulo

RAIZ = Path(__file__).resolve().parent.parent
FIXTURE_EJEMPLO = RAIZ / "fixtures" / "guion-ejemplo.md"
CARPETA_SALIDA_FIXTURE = RAIZ / "fixtures" / "salida"

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


def verificar_autocontencion(ruta_html: Path) -> Resultado:
    """Comprueba que un reproductor generado no depende de nada externo."""
    if not ruta_html.exists():
        return Resultado(
            "Auto-contencion del reproductor",
            "NO APLICABLE",
            "el generador del reproductor no existe todavia (T-18).",
        )
    hallazgos = buscar_recursos_externos(ruta_html.read_text(encoding="utf-8"))
    if hallazgos:
        return Resultado(
            "Auto-contencion del reproductor",
            "FALLO",
            "el HTML depende de recursos externos: " + "; ".join(hallazgos),
        )
    return Resultado("Auto-contencion del reproductor", "OK", f"{ruta_html.name} es autocontenido.")


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


def verificar_generacion() -> Resultado:
    """Ejecuta la skill sobre el guion de ejemplo. Pendiente hasta que exista la canalizacion."""
    return Resultado(
        "Generacion de salidas",
        "NO APLICABLE",
        "la canalizacion completa se cierra en T-30; se activara aqui sin tocar el protocolo.",
    )


def verificar_srt() -> Resultado:
    """Valida el .srt generado con las mismas reglas que aplica ffmpeg."""
    return Resultado("Validez del .srt", "NO APLICABLE", "el exportador de subtitulos es T-27.")


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
        verificar_autocontencion(RAIZ / "fixtures" / "salida" / "reproductor.html"),
        verificar_srt(),
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
