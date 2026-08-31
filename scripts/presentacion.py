"""Unica capa autorizada a escribir en la salida estandar (regla §0.2, tarea T-02).

El resto del codigo NUNCA usa print(): pide a este modulo que muestre algo. Asi la
salida al usuario queda en un solo sitio, se puede silenciar, redirigir o traducir,
y el linter (regla T20 de ruff) impide que se cuele un print de depuracion.
"""

from __future__ import annotations

import sys
from enum import Enum


class Nivel(Enum):
    """Tono del mensaje. Determina el prefijo y el canal de salida."""

    OK = "OK"
    INFO = "  "
    AVISO = "AVISO"
    ERROR = "ERROR"


_PREFIJOS = {
    Nivel.OK: "OK   ",
    Nivel.INFO: "     ",
    Nivel.AVISO: "AVISO",
    Nivel.ERROR: "ERROR",
}


def mostrar(mensaje: str, nivel: Nivel = Nivel.INFO) -> None:
    """Muestra un mensaje al usuario. Los errores y avisos van por stderr."""
    canal = sys.stderr if nivel in (Nivel.ERROR, Nivel.AVISO) else sys.stdout
    print(f"{_PREFIJOS[nivel]} {mensaje}", file=canal)


def titulo(texto: str) -> None:
    """Encabezado de seccion, para separar bloques de salida largos."""
    print(f"\n{texto}\n{'-' * len(texto)}")
