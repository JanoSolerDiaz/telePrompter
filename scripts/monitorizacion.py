"""Monitorizacion de errores local (§0.2: cero red, ningun servicio externo, tarea T-05).

No hay Sentry ni servicio equivalente: la red de seguridad es local. Dos piezas:

- `ejecutar_con_diagnostico` envuelve el punto de entrada real de la CLI. Si lanza una
  excepcion no controlada, vuelca el diagnostico tecnico completo (tipo, mensaje,
  traceback con archivo/linea/funcion) a `<carpeta_salida>/diagnostico-<timestamp>.log`,
  muestra al dueno un mensaje accionable en espanol por `presentacion.py` (nunca la
  traza cruda) y devuelve un codigo de salida distinto de cero.
- `ResumenEjecucion` es el recuento final que la CLI muestra al terminar sin errores:
  escenas procesadas, bloques, avisos, reescrituras y salidas generadas.

Regla dura de esta tarea: el diagnostico nunca incluye el contenido integro del guion
de entrada, solo referencias de posicion (escena, bloque, linea). Por eso el volcado usa
`traceback.format_exception` sin captura de variables locales: un futuro fallo dentro del
parser no arrastra el texto del guion al archivo de diagnostico solo por estar en una
variable local del marco donde salto la excepcion.
"""

from __future__ import annotations

import traceback
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

from config import PREFIJO_ARCHIVO_DIAGNOSTICO
from logger import obtener_logger
from presentacion import Nivel, mostrar, titulo


def _marca_de_tiempo() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%S%f")


def ruta_diagnostico(carpeta_salida: Path, *, instante: str | None = None) -> Path:
    """Ruta del archivo de diagnostico de esta ejecucion, con marca de tiempo."""
    return carpeta_salida / f"{PREFIJO_ARCHIVO_DIAGNOSTICO}{instante or _marca_de_tiempo()}.log"


def _volcar_diagnostico(ruta: Path, excepcion: BaseException) -> None:
    """Escribe el diagnostico tecnico completo de una excepcion no controlada.

    Solo tipo, mensaje y traceback (archivo/linea/funcion): nunca valores de variables
    locales, para no arrastrar el contenido del guion de entrada al archivo aunque
    estuviera en una variable local del marco donde salto la excepcion.
    """
    ruta.parent.mkdir(parents=True, exist_ok=True)
    cuerpo = "".join(
        traceback.format_exception(type(excepcion), excepcion, excepcion.__traceback__)
    )
    ruta.write_text(
        f"Diagnostico teleprompter — {_marca_de_tiempo()}\n{'=' * 60}\n{cuerpo}",
        encoding="utf-8",
        newline="\n",
    )


def ejecutar_con_diagnostico(funcion: Callable[[], int], carpeta_salida: Path) -> int:
    """Ejecuta `funcion` (el punto de entrada real de la CLI) con captura de errores.

    Si `funcion` termina normalmente, propaga su codigo de salida tal cual. Si lanza una
    excepcion no controlada: vuelca el diagnostico completo a
    `<carpeta_salida>/diagnostico-<timestamp>.log`, muestra al dueno un mensaje accionable
    en espanol (sin traza tecnica) y devuelve 1.
    """
    try:
        return funcion()
    except Exception as excepcion:
        ruta = ruta_diagnostico(carpeta_salida)
        _volcar_diagnostico(ruta, excepcion)
        obtener_logger().error(
            "Excepcion no controlada. Diagnostico en %s", ruta, exc_info=excepcion
        )
        mostrar(
            "Ha ocurrido un error inesperado y el proceso se ha detenido. "
            f"Revisa el diagnostico tecnico en: {ruta}",
            Nivel.ERROR,
        )
        return 1


@dataclass
class ResumenEjecucion:
    """Recuento final de una ejecucion sin errores, para el resumen que ve el dueno."""

    escenas_procesadas: int = 0
    bloques: int = 0
    avisos: int = 0
    reescrituras: int = 0
    salidas_generadas: tuple[str, ...] = field(default_factory=tuple)

    def mostrar_resumen(self) -> None:
        """Muestra el resumen final por `presentacion.py` (nunca por print directo)."""
        titulo("Resumen de la ejecucion")
        mostrar(f"Escenas procesadas: {self.escenas_procesadas}")
        mostrar(f"Bloques: {self.bloques}")
        mostrar(f"Avisos: {self.avisos}")
        mostrar(f"Reescrituras: {self.reescrituras}")
        salidas = ", ".join(self.salidas_generadas) if self.salidas_generadas else "ninguna"
        mostrar(f"Salidas generadas: {salidas}")
