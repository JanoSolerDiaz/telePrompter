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

# Pausas por bloque de respiracion segun su puntuacion final (requisito 2 de T-12),
# en orden creciente: coma < punto < fin de parrafo < fin de escena.
PAUSA_COMA_SEGUNDOS: float = 0.15
PAUSA_PUNTO_SEGUNDOS: float = 0.35
PAUSA_FIN_PARRAFO_SEGUNDOS: float = 0.6
PAUSA_FIN_ESCENA_SEGUNDOS: float = 1.0

# Umbral relativo (0.15 = 15 %) de desviacion entre la duracion estimada y la
# objetivo (por escena y en total) a partir del cual se avisa (requisito 6 de T-12).
UMBRAL_DESVIACION_TIEMPOS: float = 0.15

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
    ppm_banda_plausible: tuple[int, int] = field(default=PPM_BANDA_PLAUSIBLE)
    # Calibracion opcional con toma real (requisito 8 de T-12): si el dueno la fija,
    # tiene prioridad sobre el ppm deducido y sobre el respaldo. Se persiste sola,
    # como el resto de `Configuracion`, dentro de `configuracion_efectiva` en
    # `estado.json` (T-07): no hace falta un mecanismo de persistencia nuevo.
    ppm_manual: int | None = None
    pausa_coma_segundos: float = PAUSA_COMA_SEGUNDOS
    pausa_punto_segundos: float = PAUSA_PUNTO_SEGUNDOS
    pausa_fin_parrafo_segundos: float = PAUSA_FIN_PARRAFO_SEGUNDOS
    pausa_fin_escena_segundos: float = PAUSA_FIN_ESCENA_SEGUNDOS
    umbral_desviacion_tiempos: float = UMBRAL_DESVIACION_TIEMPOS
    palabras_por_bloque_min: int = PALABRAS_POR_BLOQUE_MIN
    palabras_por_bloque_objetivo: int = PALABRAS_POR_BLOQUE_OBJETIVO
    palabras_por_bloque_max: int = PALABRAS_POR_BLOQUE_MAX
    tipografia_marca: str = TIPOGRAFIA_MARCA
    incluir_notas_internas: bool = INCLUIR_NOTAS_INTERNAS
    secciones_auxiliares: tuple[str, ...] = field(default=SECCIONES_AUXILIARES)
    rotulo_locucion: str = ROTULO_LOCUCION
    rotulos_no_locucion: tuple[str, ...] = field(default=ROTULOS_NO_LOCUCION)

    def __post_init__(self) -> None:
        if self.palabras_por_bloque_min > self.palabras_por_bloque_max:
            mensaje = (
                "El minimo de palabras por bloque no puede superar al maximo "
                f"({self.palabras_por_bloque_min} > {self.palabras_por_bloque_max})."
            )
            raise ValueError(mensaje)
        if not (
            self.palabras_por_bloque_min
            <= self.palabras_por_bloque_objetivo
            <= self.palabras_por_bloque_max
        ):
            mensaje = (
                "El objetivo de palabras por bloque debe estar entre el minimo y el "
                f"maximo ({self.palabras_por_bloque_min} <= "
                f"{self.palabras_por_bloque_objetivo} <= {self.palabras_por_bloque_max})."
            )
            raise ValueError(mensaje)
        if self.ppm_respaldo <= 0:
            raise ValueError("El ritmo de respaldo debe ser un numero positivo de palabras/minuto.")
        banda_min, banda_max = self.ppm_banda_plausible
        if banda_min > banda_max or banda_min <= 0:
            mensaje = (
                "La banda de plausibilidad del ppm debe ser un rango positivo y creciente "
                f"({self.ppm_banda_plausible})."
            )
            raise ValueError(mensaje)
        if self.ppm_manual is not None and self.ppm_manual <= 0:
            raise ValueError(
                "El ppm calibrado a mano debe ser un numero positivo de palabras/minuto."
            )
        for nombre, valor in (
            ("pausa_coma_segundos", self.pausa_coma_segundos),
            ("pausa_punto_segundos", self.pausa_punto_segundos),
            ("pausa_fin_parrafo_segundos", self.pausa_fin_parrafo_segundos),
            ("pausa_fin_escena_segundos", self.pausa_fin_escena_segundos),
        ):
            if valor < 0:
                raise ValueError(f"La pausa '{nombre}' no puede ser negativa ({valor}).")
        if not (0 < self.umbral_desviacion_tiempos <= 1):
            mensaje = (
                "El umbral de desviacion de tiempos debe estar entre 0 (exclusivo) y 1 "
                f"(inclusive), como fraccion ({self.umbral_desviacion_tiempos})."
            )
            raise ValueError(mensaje)
