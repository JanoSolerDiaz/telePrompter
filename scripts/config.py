"""Unico lugar donde vive un valor por defecto (regla "sin numeros magicos", §0.2).

Ningun otro modulo puede llevar una constante de comportamiento escrita a mano. Todo lo
que hay aqui es sobreescribible por el dueno y debe estar documentado en `SKILL.md`
(tarea T-31, que incluye un test que compara estas claves con las documentadas).

Precedencia prevista (T-31): valores por defecto -> configuracion del usuario ->
configuracion del proyecto de guion -> argumentos de la invocacion.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# --- Ritmo y tiempos (T-12) -------------------------------------------------------
# Decision del dueno (2026-08-31): el ritmo se DEDUCE de las duraciones objetivo del
# guion. 120 ppm es solo el respaldo cuando el guion no las trae o el valor deducido
# no es plausible.
PPM_RESPALDO: int = 120
PPM_BANDA_PLAUSIBLE: tuple[int, int] = (90, 180)

# --- Troceo en bloques de respiracion (T-11) --------------------------------------
PALABRAS_POR_BLOQUE_MIN: int = 6
PALABRAS_POR_BLOQUE_OBJETIVO: int = 9
PALABRAS_POR_BLOQUE_MAX: int = 12

# --- Convencion de guion (T-08, T-09; contractual con aviso, §0.2) ----------------
PATRON_ENCABEZADO_ESCENA: str = r"^##\s+BLOQUE\s+(?P<numero>\d+)\s*[—-]\s*(?P<titulo>.+)$"
ROTULO_LOCUCION: str = "**LOCUCIÓN**"
ROTULOS_NO_LOCUCION: tuple[str, ...] = ("**EN PANTALLA**", "**NOTA**")
SECCIONES_AUXILIARES: tuple[str, ...] = (
    "Capítulos",
    "Preparación antes de grabar",
    "Notas de producción",
)

# --- Salidas (T-27, T-28, T-29, T-30) ---------------------------------------------
TIPOGRAFIA_MARCA: str = "Poppins"  # decision del dueno 2026-08-31; ver §6.8 y auditoria #3
RESPALDO_TIPOGRAFICO: tuple[str, ...] = ("Montserrat", "Calibri", "sans-serif")
INCLUIR_NOTAS_INTERNAS: bool = True  # `--para-terceros` lo pone en False
SRT_CARACTERES_POR_LINEA_MAX: int = 42

# --- Reproductor (T-18 a T-26) ----------------------------------------------------
TAMANO_TEXTO_BASE_PX: int = 48
PASO_VELOCIDAD: float = 0.1
CUENTA_ATRAS_SEGUNDOS: int = 3
ANTIRREBOTE_CLICKER_MS: int = 120

# --- Limites de entrada (T-06) ----------------------------------------------------
TAMANO_GUION_MAX_BYTES: int = 5 * 1024 * 1024
ESCENAS_MAX: int = 200
# Tope de tiempo (segundos) para una etapa de proceso arrancada sobre el guion. No hay
# `signal.alarm` (el dueno trabaja en Windows, sin SIGALRM); ver `entrada.py`.
TIEMPO_PROCESO_MAX_SEGUNDOS: float = 60.0

# --- Diagnostico (T-02, T-05) ------------------------------------------------------
# Nombre del archivo de log dentro de la carpeta de salida del guion. El logger nunca
# escribe fuera de esa carpeta (regla de aislamiento, §0.2).
NOMBRE_ARCHIVO_LOG: str = "teleprompter.log"
# Prefijo del archivo de diagnostico que vuelca una excepcion no controlada (T-05).
# Se completa con una marca de tiempo: "<PREFIJO><timestamp>.log".
PREFIJO_ARCHIVO_DIAGNOSTICO: str = "diagnostico-"

# --- Estado del proyecto de guion (T-07) -------------------------------------------
# Nombre del archivo de estado dentro de la carpeta de salida del guion.
NOMBRE_ARCHIVO_ESTADO: str = "estado.json"
# Version del esquema de `estado.json` que escribe esta version de la skill. Sube en
# cada migracion nueva (`scripts/migraciones/NNN_<nombre>.py`); nunca se decrementa.
VERSION_ESQUEMA_ESTADO: int = 1


@dataclass(frozen=True)
class Configuracion:
    """Configuracion efectiva de una ejecucion. Se congela para que nadie la mute a medias."""

    ppm_respaldo: int = PPM_RESPALDO
    palabras_por_bloque_min: int = PALABRAS_POR_BLOQUE_MIN
    palabras_por_bloque_max: int = PALABRAS_POR_BLOQUE_MAX
    tipografia_marca: str = TIPOGRAFIA_MARCA
    incluir_notas_internas: bool = INCLUIR_NOTAS_INTERNAS
    secciones_auxiliares: tuple[str, ...] = field(default=SECCIONES_AUXILIARES)

    def __post_init__(self) -> None:
        if self.palabras_por_bloque_min > self.palabras_por_bloque_max:
            mensaje = (
                "El minimo de palabras por bloque no puede superar al maximo "
                f"({self.palabras_por_bloque_min} > {self.palabras_por_bloque_max})."
            )
            raise ValueError(mensaje)
        if self.ppm_respaldo <= 0:
            raise ValueError("El ritmo de respaldo debe ser un numero positivo de palabras/minuto.")
