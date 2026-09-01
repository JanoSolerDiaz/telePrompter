"""Logger centralizado de diagnostico (regla "logger centralizado", §0.2, tarea T-02).

Distinto de `presentacion.py`: aquel es la unica capa autorizada a hablarle al dueno
(mensajes en espanol, resultado de la ejecucion). Este modulo es la unica capa
autorizada a diagnosticar la ejecucion (trazas tecnicas, tiempos, decisiones internas),
pensado para depurar un fallo, no para leerse en caliente. Nunca se usa `logging`
directamente fuera de aqui, igual que nunca se usa `print()` fuera de `presentacion.py`.

El log siempre se escribe dentro de la carpeta de salida del guion (regla de
aislamiento, §0.2): nunca en una ruta ajena a ese proyecto. `--verbose` no cambia
donde se escribe, solo si ademas se ve por consola mientras el proceso corre.
"""

from __future__ import annotations

import logging
from pathlib import Path

from config import NOMBRE_ARCHIVO_LOG

NOMBRE_LOGGER = "teleprompter"

_FORMATO_ARCHIVO = "%(asctime)s %(levelname)-7s %(name)s: %(message)s"
_FORMATO_CONSOLA = "%(levelname)-7s %(message)s"


def configurar_logger(carpeta_salida: Path, *, verbose: bool = False) -> logging.Logger:
    """Configura el logger de diagnostico y lo deja listo para usar.

    Crea (si hace falta) `carpeta_salida` y escribe siempre en
    `<carpeta_salida>/teleprompter.log`, en nivel DEBUG, para que el archivo sirva de
    diagnostico completo aunque la ejecucion no se lanzara con `--verbose`. Con
    `verbose=True` se anade ademas un segundo canal por stderr (nivel INFO) para seguir
    la ejecucion en vivo.

    Idempotente: puede llamarse varias veces en el mismo proceso (p. ej. entre tests)
    sin acumular manejadores duplicados.
    """
    logger = logging.getLogger(NOMBRE_LOGGER)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    for manejador in list(logger.handlers):
        logger.removeHandler(manejador)
        manejador.close()

    carpeta_salida.mkdir(parents=True, exist_ok=True)
    manejador_archivo = logging.FileHandler(carpeta_salida / NOMBRE_ARCHIVO_LOG, encoding="utf-8")
    manejador_archivo.setLevel(logging.DEBUG)
    manejador_archivo.setFormatter(logging.Formatter(_FORMATO_ARCHIVO))
    logger.addHandler(manejador_archivo)

    if verbose:
        manejador_consola = logging.StreamHandler()
        manejador_consola.setLevel(logging.INFO)
        manejador_consola.setFormatter(logging.Formatter(_FORMATO_CONSOLA))
        logger.addHandler(manejador_consola)

    return logger


def obtener_logger() -> logging.Logger:
    """Devuelve el logger de diagnostico ya configurado.

    Si nadie llamo antes a `configurar_logger`, devuelve un logger sin manejadores
    (no escribe a ningun sitio pero tampoco falla): protege al codigo que registra
    diagnosticos de tener que comprobar si la configuracion ya ocurrio.
    """
    return logging.getLogger(NOMBRE_LOGGER)
