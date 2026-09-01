"""Robustez de entrada (equivalente al rate limiting, §0.1, tarea T-06).

No hay endpoints que proteger: el equivalente es blindar la unica puerta de entrada
real, el `.md` del guion, antes de que nada lo procese. Esta capa se situa delante
del parser (T-08, que todavia no existe): valida ruta, tamano, codificacion y
estructura minima, deriva de forma segura la carpeta de salida y ofrece un tope de
tiempo de proceso, para que ninguna entrada hostil pueda provocar un bucle
infinito, un consumo desbocado ni una escritura fuera de la carpeta de salida del
guion (regla de aislamiento, §0.2).

Alcance deliberado: decidir si un encabezado es una escena de verdad o una seccion
auxiliar es trabajo del parser (T-08), que puede preguntar al dueno ante ambiguedad.
Esta capa no lo intenta: solo descarta los dos extremos hostiles antes de llegar
ahi -- cero encabezados (nada que procesar) y un numero de encabezados que
dispararia un consumo desbocado en las etapas siguientes.

Todos los fallos se comunican con `EntradaError`, cuyo mensaje ya es el mensaje
accionable en espanol que debe ver el dueno: quien la capture solo tiene que
mostrarlo, nunca interpretar una traza cruda.
"""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as ErrorTiempoAgotado
from pathlib import Path
from typing import TypeVar

from config import (
    ESCENAS_MAX,
    TAMANO_GUION_MAX_BYTES,
    TIEMPO_PROCESO_MAX_SEGUNDOS,
)

# `def f[T](...)` (PEP 695) no es una opcion aqui: el `python` real de este entorno
# es 3.11 pese a que `pyproject.toml` fija `requires-python = ">=3.12"` (ver
# DECISIONES_TECNICAS.md, T-06) y esa sintaxis ni siquiera analiza bajo 3.11.
_T = TypeVar("_T")

# Cualquier encabezado Markdown, del nivel que sea (T-08 decide despues cual es el
# separador de escena real).
_PATRON_ENCABEZADO_MD = re.compile(r"^#{1,6}[ \t]+\S.*$", re.MULTILINE)


class EntradaError(Exception):
    """Entrada invalida u hostil detectada antes de procesar el guion.

    El mensaje del propio error ya es el texto accionable en espanol: quien la
    capture solo tiene que mostrarlo, nunca su traza.
    """


def validar_ruta_guion(ruta: Path) -> Path:
    """Comprueba que `ruta` es un fichero legible y de tamano razonable.

    No lee el contenido (eso es cosa de `leer_guion`): solo lo que se puede saber
    sin abrir el archivo, para descartar rutas hostiles o desmesuradas lo antes
    posible. Devuelve la ruta resuelta (absoluta).
    """
    if not ruta.exists():
        raise EntradaError(f"No existe el guion indicado: {ruta}")
    if ruta.is_dir():
        raise EntradaError(f"La ruta indicada es una carpeta, no un guion: {ruta}")
    if not ruta.is_file():
        raise EntradaError(f"La ruta indicada no es un fichero regular: {ruta}")

    try:
        tamano = ruta.stat().st_size
    except OSError as excepcion:
        raise EntradaError(
            f"No se puede leer el guion indicado ({ruta}): {excepcion}"
        ) from excepcion

    if tamano == 0:
        raise EntradaError(f"El guion esta vacio: {ruta}")
    if tamano > TAMANO_GUION_MAX_BYTES:
        limite_mb = TAMANO_GUION_MAX_BYTES / (1024 * 1024)
        tamano_mb = tamano / (1024 * 1024)
        raise EntradaError(
            f"El guion pesa {tamano_mb:.1f} MB, por encima del limite configurado "
            f"({limite_mb:.1f} MB, TAMANO_GUION_MAX_BYTES en config.py): {ruta}"
        )
    return ruta.resolve()


def leer_guion(ruta: Path) -> str:
    """Lee el guion validando ruta, codificacion UTF-8 y estructura minima.

    Acepta UTF-8 con o sin BOM (algunos editores de Windows lo anaden al guardar)
    pero rechaza cualquier otra codificacion con un error accionable en vez de
    dejar que un `UnicodeDecodeError` se propague como traza cruda.
    """
    ruta_validada = validar_ruta_guion(ruta)
    bytes_guion = ruta_validada.read_bytes()
    try:
        texto = bytes_guion.decode("utf-8-sig")
    except UnicodeDecodeError as excepcion:
        raise EntradaError(
            f"El guion no esta en UTF-8 (revisa la codificacion del archivo): {ruta}. "
            f"Detalle: {excepcion}"
        ) from excepcion

    if not texto.strip():
        raise EntradaError(f"El guion esta vacio o solo contiene espacios en blanco: {ruta}")

    verificar_estructura_minima(texto, origen=ruta)
    return texto


def verificar_estructura_minima(texto: str, *, origen: Path | None = None) -> None:
    """Guarda ante un `.md` sin ningun encabezado o con demasiados para procesar.

    No decide que encabezado es escena (T-08): cuenta encabezados de cualquier
    nivel para acotar los dos extremos hostiles antes del parser real.
    """
    referencia = f" ({origen})" if origen else ""
    encabezados = _PATRON_ENCABEZADO_MD.findall(texto)

    if not encabezados:
        raise EntradaError(
            f"El guion no tiene ningun encabezado Markdown (#, ## o ###){referencia}. "
            "Sin encabezados no hay escenas que detectar."
        )

    if len(encabezados) > ESCENAS_MAX:
        raise EntradaError(
            f"El guion tiene {len(encabezados)} encabezados, por encima del limite "
            f"configurado (ESCENAS_MAX={ESCENAS_MAX} en config.py){referencia}."
        )


def nombre_guion_seguro(ruta_guion: Path) -> str:
    """Deriva un nombre de proyecto seguro a partir del nombre del guion.

    Se usa para construir `<carpeta-del-guion>/<nombre-guion>-tarjetas/` (T-07).
    `Path.stem` ya descarta cualquier componente de carpeta (`../`) del nombre;
    esta funcion, ademas, normaliza unicode y sustituye separadores de ruta y
    caracteres de control por si el nombre de archivo en si fuera hostil, para que
    la carpeta de salida derivada nunca pueda caer fuera de la carpeta del guion
    (regla de aislamiento, §0.2).
    """
    base = unicodedata.normalize("NFC", ruta_guion.stem).strip()
    limpio = re.sub(r"[\\/\x00-\x1f]", "-", base)
    limpio = re.sub(r"\.{2,}", "-", limpio)
    limpio = limpio.strip("-. ")
    return limpio or "guion"


def carpeta_salida_para(ruta_guion: Path, *, sufijo: str = "-tarjetas") -> Path:
    """Carpeta de salida derivada del guion, siempre dentro de su propia carpeta.

    Defensa en profundidad: levanta `EntradaError` si, pese a la sanitizacion de
    `nombre_guion_seguro`, el resultado no quedara dentro de la carpeta del guion.
    """
    ruta_validada = validar_ruta_guion(ruta_guion)
    carpeta_base = ruta_validada.parent
    carpeta = carpeta_base / f"{nombre_guion_seguro(ruta_validada)}{sufijo}"
    try:
        carpeta.resolve().relative_to(carpeta_base.resolve())
    except ValueError as excepcion:
        raise EntradaError(
            f"La carpeta de salida calculada queda fuera de la carpeta del guion: {carpeta}"
        ) from excepcion
    return carpeta


def ejecutar_con_limite_de_tiempo(  # noqa: UP047 - ver nota de _T mas arriba
    funcion: Callable[[], _T], *, segundos: float = TIEMPO_PROCESO_MAX_SEGUNDOS
) -> _T:
    """Ejecuta `funcion` con un tope de tiempo.

    No usa `signal.alarm`: el dueno trabaja en Windows, que no tiene `SIGALRM`. Si
    `funcion` no termina dentro de `segundos`, levanta `EntradaError` y el proceso
    principal recupera el control de inmediato (no se espera al hilo huerfano);
    Python no permite matar un hilo desde fuera, asi que esto es una garantia sobre
    el tiempo del dueno, no una cancelacion real del trabajo en curso.
    """
    ejecutor = ThreadPoolExecutor(max_workers=1)
    futuro = ejecutor.submit(funcion)
    try:
        resultado = futuro.result(timeout=segundos)
    except ErrorTiempoAgotado as excepcion:
        ejecutor.shutdown(wait=False)
        raise EntradaError(
            f"El proceso ha superado el tiempo maximo configurado ({segundos} s, "
            "TIEMPO_PROCESO_MAX_SEGUNDOS en config.py) y se ha detenido."
        ) from excepcion
    ejecutor.shutdown(wait=False)
    return resultado
