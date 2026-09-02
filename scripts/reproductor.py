"""Esqueleto del reproductor autocontenido (tarea T-18).

Genera el artefacto principal de la skill: un unico `.html` que funciona con
doble clic, offline, en cualquier maquina. No vuelve a calcular nada por su
cuenta -- toma el resultado ya calculado por el parseo (T-08) y el motor de
tiempos (T-12) y lo compone en una pagina, mismo patron que ya sigue
`documento_revision.generar_documento_revision` (T-16) con sus propias
entradas.

Auto-contencion (regla dura de §0.2): las plantillas de `assets/reproductor/`
(HTML, CSS, JS) no referencian nada externo, y el propio `verificar_salidas.py`
comprueba ademas, a nivel de bytes, que la salida generada tampoco lo hace --
defensa en profundidad, no solo disciplina de plantilla.

Escapado seguro (requisito 3): el contenido del guion viaja como JSON dentro
de un `<script type="application/json">`, nunca interpolado directamente en
el marcado. Sigue habiendo un riesgo real ahi -- un bloque de locucion cuyo
texto contuviera literalmente `</script>` cerraria la etiqueta igualmente,
porque el analizador HTML no mira el `type` del script para decidir donde
termina -- asi que `_json_seguro_para_script` neutraliza `<`, `>` y `&` con
sus escapes Unicode antes de incrustar el JSON. Las tildes y enes se dejan tal
cual (UTF-8, sin `ensure_ascii`): la pagina declara su `charset` y no hay
ningun motivo para escaparlas. Ademas, `guion.js` solo usa `textContent` para
volcar ese texto al DOM, nunca `innerHTML`: aunque el escapado de arriba
fallara, no hay via de inyeccion de marcado en el render.
"""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from config import NOMBRE_ARCHIVO_REPRODUCTOR, Configuracion
from parser import ResultadoParseo
from tiempos import BloqueConTiempo, ResultadoTiempos

_CARPETA_PLANTILLAS = Path(__file__).resolve().parent.parent / "assets" / "reproductor"

# Caracteres que podrian cerrar prematuramente la etiqueta <script> que envuelve
# el JSON incrustado (p. ej. un bloque de locucion con el texto literal
# "</script>"), sustituidos por su escape Unicode equivalente dentro de la cadena
# JSON. El propio `json.dumps` ya se encarga de comillas y barras invertidas.
_ESCAPES_JSON_EN_SCRIPT: tuple[tuple[str, str], ...] = (
    ("<", "\\u003c"),
    (">", "\\u003e"),
    ("&", "\\u0026"),
)


def _leer_plantilla(nombre: str) -> str:
    return (_CARPETA_PLANTILLAS / nombre).read_text(encoding="utf-8")


def _luminancia_relativa(color_hex: str) -> float:
    """Luminancia relativa WCAG de un color `#rrggbb` (sin alfa ni forma corta)."""
    color_hex = color_hex.lstrip("#")
    componentes = (int(color_hex[i : i + 2], 16) / 255 for i in (0, 2, 4))
    linealizados = [
        c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in componentes
    ]
    rojo, verde, azul = linealizados
    return 0.2126 * rojo + 0.7152 * verde + 0.0722 * azul


def contraste_relativo(color_a: str, color_b: str) -> float:
    """Ratio de contraste WCAG (1.0 a 21.0) entre dos colores `#rrggbb`.

    Usado para verificar la regla dura de T-21 (requisito 3, "contraste AAA
    para el bloque activo"): AAA de texto normal exige un ratio >= 7.0.
    """
    l1 = _luminancia_relativa(color_a) + 0.05
    l2 = _luminancia_relativa(color_b) + 0.05
    return max(l1, l2) / min(l1, l2)


def _json_seguro_para_script(datos: dict[str, Any]) -> str:
    texto = json.dumps(datos, ensure_ascii=False)
    for caracter, escape in _ESCAPES_JSON_EN_SCRIPT:
        texto = texto.replace(caracter, escape)
    return texto


def _construir_datos(
    resultado: ResultadoParseo,
    resultado_tiempos: ResultadoTiempos,
    nombre_guion: str,
    configuracion: Configuracion,
) -> dict[str, Any]:
    """Escenas, bloques y tiempos en la forma que consume `guion.js`.

    `resultado_tiempos.escenas` trae exactamente una `TiempoEscena` por cada
    `Escena` de `resultado.escenas`, en el mismo orden (asi la construye
    `tiempos.calcular_tiempos_desde_marcados`): `zip(strict=True)` deja que
    cualquier futura ruptura de esa garantia falle alto y claro, en vez de
    silenciarse con una escena sin tiempos.
    """
    bloques_por_escena: dict[int, list[BloqueConTiempo]] = {}
    for bloque_con_tiempo in resultado_tiempos.bloques:
        bloques_por_escena.setdefault(bloque_con_tiempo.bloque.numero_escena, []).append(
            bloque_con_tiempo
        )

    escenas_datos = [
        {
            "numero": escena.numero,
            "titulo": escena.titulo,
            "duracion_estimada_segundos": tiempo_escena.duracion_estimada_segundos,
            "duracion_objetivo_segundos": tiempo_escena.duracion_objetivo_segundos,
            "bloques": [
                {
                    "texto": bloque_con_tiempo.bloque.texto,
                    "num_palabras": bloque_con_tiempo.bloque.num_palabras,
                    "inicio_segundos": bloque_con_tiempo.inicio_segundos,
                    "fin_segundos": bloque_con_tiempo.fin_segundos,
                }
                for bloque_con_tiempo in bloques_por_escena.get(escena.numero, [])
            ],
        }
        for escena, tiempo_escena in zip(
            resultado.escenas, resultado_tiempos.escenas, strict=True
        )
    ]

    return {
        "guion": nombre_guion,
        "ritmo_ppm": resultado_tiempos.ritmo.ppm_aplicado,
        "duracion_total_segundos": resultado_tiempos.duracion_total_segundos,
        "escenas": escenas_datos,
        # Motor de avance hibrido (T-20): limites y paso de la velocidad en vivo,
        # configurables (§0.2, "sin numeros magicos"); nunca escritos a mano en guion.js.
        "paso_velocidad": configuracion.paso_velocidad,
        "velocidad_minima": configuracion.velocidad_minima,
        "velocidad_maxima": configuracion.velocidad_maxima,
        # Resaltado y tema de grabacion (T-21): gradiente de atenuacion del contexto
        # (requisito 1) y limites/paso del tamano de texto en vivo (requisito 2),
        # todo configurable -- `guion.js` no trae ninguno de estos valores a mano.
        "atenuacion_niveles": configuracion.atenuacion_niveles,
        "atenuacion_minima": configuracion.atenuacion_minima,
        "tamano_texto_base_px": configuracion.tamano_texto_base_px,
        "paso_tamano_texto_px": configuracion.paso_tamano_texto_px,
        "tamano_texto_minimo_px": configuracion.tamano_texto_minimo_px,
        "tamano_texto_maximo_px": configuracion.tamano_texto_maximo_px,
        "tiempo_inactividad_cursor_ms": configuracion.tiempo_inactividad_cursor_ms,
        # Autoscroll con bloque centrado (T-22): duracion del desplazamiento suave,
        # configurable -- `guion.js` no la trae escrita a mano.
        "duracion_autoscroll_ms": configuracion.duracion_autoscroll_ms,
    }


def generar_reproductor_html(
    resultado: ResultadoParseo,
    resultado_tiempos: ResultadoTiempos,
    nombre_guion: str = "guion",
    configuracion: Configuracion | None = None,
) -> str:
    """Compone el reproductor completo en una unica cadena `.html`.

    Requisito 1: embebe datos (escenas, bloques, tiempos), CSS y JS en un
    unico archivo a partir de las plantillas de `assets/reproductor/`.
    Requisito 2: fuentes del sistema con pila de respaldo, colores neutros y
    oscuros -- todo configurable via `Configuracion`, nada remoto.
    """
    configuracion = configuracion or Configuracion()
    datos = _construir_datos(resultado, resultado_tiempos, nombre_guion, configuracion)

    estilo = (
        _leer_plantilla("estilo.css")
        .replace("__COLOR_FONDO__", configuracion.color_fondo_reproductor)
        .replace("__COLOR_TEXTO__", configuracion.color_texto_reproductor)
        .replace("__COLOR_TEXTO_SECUNDARIO__", configuracion.color_texto_secundario_reproductor)
        .replace("__COLOR_ACENTO__", configuracion.color_acento_reproductor)
        .replace("__TAMANO_TEXTO_BASE_PX__", str(configuracion.tamano_texto_base_px))
        .replace("__MARGEN_SEGURO_PX__", str(configuracion.margen_seguro_px))
        .replace(
            "__PILA_TIPOGRAFICA__",
            ", ".join(
                f'"{fuente}"' if " " in fuente else fuente
                for fuente in configuracion.pila_tipografica_reproductor
            ),
        )
    )
    guion_js = _leer_plantilla("guion.js")

    return (
        _leer_plantilla("plantilla.html")
        .replace("__ESTILO__", estilo)
        .replace("__SCRIPT__", guion_js)
        .replace("__TITULO__", html.escape(nombre_guion, quote=True))
        .replace("__DATOS_JSON__", _json_seguro_para_script(datos))
    )


def guardar_reproductor(pagina_html: str, carpeta_salida: Path) -> Path:
    """Escribe el reproductor en la carpeta de salida del guion (aislamiento, §0.2)."""
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    destino = carpeta_salida / NOMBRE_ARCHIVO_REPRODUCTOR
    destino.write_text(pagina_html, encoding="utf-8")
    return destino
