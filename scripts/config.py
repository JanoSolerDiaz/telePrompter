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

# --- Normalizacion a forma dicha (T-13) --------------------------------------------
# Diccionario de excepciones editable por el dueno (requisito 3), con prioridad sobre
# toda regla automatica de `normalizacion.py`. Vive dentro de la carpeta de salida del
# guion (regla de aislamiento, §0.2): "<carpeta-del-guion>/<nombre-guion>-tarjetas/
# diccionario-locucion.json". Ausente por defecto: sin el, solo actuan las reglas
# automaticas.
NOMBRE_ARCHIVO_DICCIONARIO_LOCUCION: str = "diccionario-locucion.json"
# Simbolo de moneda -> (forma singular, forma plural). Cualquier entrada que el dueno
# necesite y no este aqui se cubre con el diccionario de excepciones, que gana siempre.
SIMBOLOS_MONEDA: dict[str, tuple[str, str]] = {
    "€": ("euro", "euros"),
    "$": ("dólar", "dólares"),
}
# Abreviatura de unidad -> forma dicha en plural (requisito 1). Ampliable por el dueno
# via el diccionario de excepciones (una entrada "10 km" en el diccionario gana a esta
# tabla igual que a cualquier otra regla automatica).
UNIDADES_ABREVIADAS: dict[str, str] = {
    "km": "kilómetros",
    "kg": "kilogramos",
    "cm": "centímetros",
    "mm": "milímetros",
    "min": "minutos",
    "seg": "segundos",
    "h": "horas",
    "m": "metros",
}

# --- Detector de problemas de lectura en voz alta (T-14) --------------------------
# Requisito 1: frase sin punto de respiracion (sin puntuacion intermedia) por encima
# de este numero de palabras. Deliberadamente por encima de
# `PALABRAS_POR_BLOQUE_MAX` (T-11): solo un bloque de respiracion inusualmente largo
# (p. ej. un corte forzado) dispara este aviso, no cualquier bloque normal.
UMBRAL_PALABRAS_SIN_PUNTUACION: int = 15
# Requisito 2: cacofonias y repeticiones fonicas proximas. Ventana de palabras en la
# que se buscan silabas repetidas/rima/"de" encadenados, y el minimo de repeticiones
# de "de" dentro de esa ventana para avisar.
VENTANA_CACOFONIA_PALABRAS: int = 6
REPETICIONES_DE_MINIMAS: int = 3
# Longitud (en caracteres) del prefijo/sufijo que se compara para detectar silaba
# inicial repetida o rima involuntaria entre dos palabras. Heuristica de caracteres,
# no un silabeador real del espanol (igual de deliberado que la heuristica de genero
# de T-13: no perfecta, solo un aviso).
LONGITUD_SILABA_COMPARADA: int = 3
LONGITUD_MINIMA_PALABRA_RIMA: int = 5
# Requisito 3: trabalenguas. Palabra "dificil" = longitud en caracteres por encima de
# este umbral, o un grupo de consonantes seguidas por encima de este otro. Tres o mas
# palabras dificiles seguidas disparan el aviso de acumulacion.
LONGITUD_PALABRA_DIFICIL: int = 10
CONSONANTES_SEGUIDAS_DIFICIL: int = 4
PALABRAS_DIFICILES_SEGUIDAS_MINIMAS: int = 3
# Requisito 4: anglicismos y extranjerismos frecuentes en guiones de produccion ->
# equivalente o pista de pronunciacion en espanol. No se refleja en `Configuracion`
# (mismo razonamiento que `SIMBOLOS_MONEDA`/`UNIDADES_ABREVIADAS` en T-13: es una
# tabla completa, no una entrada individual sobreescribible).
ANGLICISMOS_COMUNES: dict[str, str] = {
    "email": "correo electrónico",
    "feedback": "retroalimentación (o «comentarios»)",
    "link": "enlace",
    "online": "en línea",
    "workshop": "taller",
    "briefing": "informe (o «reunión informativa»)",
    "startup": "empresa emergente",
    "engagement": "interacción (o «compromiso»)",
    "insights": "hallazgos (o «datos clave»)",
    "roadmap": "hoja de ruta",
}
# Requisito 5: estructuras dificiles. Nexos subordinantes cuya acumulacion senala
# subordinadas encadenadas; palabras de negacion cuya acumulacion senala doble
# negacion; umbral de incisos (parentesis, guiones largos o comas de inciso) para
# "incisos anidados"; longitud minima (en palabras del bloque) para que una voz
# pasiva detectada cuente como "larga".
SUBORDINANTES: tuple[str, ...] = (
    "que", "porque", "aunque", "cuando", "donde", "como", "si", "mientras",
)
UMBRAL_SUBORDINADAS_ENCADENADAS: int = 2
NEGACIONES: tuple[str, ...] = ("no", "nunca", "jamás", "nadie", "ninguno", "ninguna", "tampoco")
UMBRAL_NEGACIONES_DOBLES: int = 2
UMBRAL_INCISOS: int = 2
UMBRAL_PALABRAS_VOZ_PASIVA_LARGA: int = 8

# --- Reproductor (T-18 a T-26) ----------------------------------------------------
TAMANO_TEXTO_BASE_PX: int = 48
# Motor de avance hibrido (T-20): la velocidad es un multiplicador sobre la duracion
# estimada de cada bloque (T-12); 1.0 = ritmo calculado tal cual, sin acelerar ni frenar.
PASO_VELOCIDAD: float = 0.1
VELOCIDAD_MINIMA: float = 0.5
VELOCIDAD_MAXIMA: float = 2.0
CUENTA_ATRAS_SEGUNDOS: int = 3
ANTIRREBOTE_CLICKER_MS: int = 120
# Neutro y oscuro, sin identidad corporativa (regla de §0.2: el reproductor prioriza
# legibilidad sobre branding; la marca 480 solo aparece en `.pptx` y `.pdf`).
COLOR_FONDO_REPRODUCTOR: str = "#0b0b0d"
COLOR_TEXTO_REPRODUCTOR: str = "#f5f5f5"
COLOR_TEXTO_SECUNDARIO_REPRODUCTOR: str = "#9a9a9a"
# Solo fuentes del sistema, con pila de respaldo (requisito 2 de T-18): nada remoto.
PILA_TIPOGRAFICA_REPRODUCTOR: tuple[str, ...] = (
    "-apple-system",
    "BlinkMacSystemFont",
    "Segoe UI",
    "Roboto",
    "Helvetica",
    "Arial",
    "sans-serif",
)
# Nombre del reproductor generado dentro de la carpeta de salida del guion.
NOMBRE_ARCHIVO_REPRODUCTOR: str = "reproductor.html"

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

# --- Documento de revision (T-16) --------------------------------------------------
# Nombre del documento de revision de una sola pasada, dentro de la carpeta de salida
# del guion. Es el archivo que el dueno edita a mano; T-17 lo relee como autoritativo.
NOMBRE_ARCHIVO_GUION_ESCENAS: str = "guion-escenas.md"
# Longitud maxima del extracto de una indicacion no recitable mostrado al pie de cada
# escena, para que una nota larga no desborde la lectura de una sola sentada.
LONGITUD_EXTRACTO_INDICACION_MAX: int = 120

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
    umbral_palabras_sin_puntuacion: int = UMBRAL_PALABRAS_SIN_PUNTUACION
    ventana_cacofonia_palabras: int = VENTANA_CACOFONIA_PALABRAS
    repeticiones_de_minimas: int = REPETICIONES_DE_MINIMAS
    longitud_silaba_comparada: int = LONGITUD_SILABA_COMPARADA
    longitud_minima_palabra_rima: int = LONGITUD_MINIMA_PALABRA_RIMA
    longitud_palabra_dificil: int = LONGITUD_PALABRA_DIFICIL
    consonantes_seguidas_dificil: int = CONSONANTES_SEGUIDAS_DIFICIL
    palabras_dificiles_seguidas_minimas: int = PALABRAS_DIFICILES_SEGUIDAS_MINIMAS
    subordinantes: tuple[str, ...] = field(default=SUBORDINANTES)
    umbral_subordinadas_encadenadas: int = UMBRAL_SUBORDINADAS_ENCADENADAS
    negaciones: tuple[str, ...] = field(default=NEGACIONES)
    umbral_negaciones_dobles: int = UMBRAL_NEGACIONES_DOBLES
    umbral_incisos: int = UMBRAL_INCISOS
    umbral_palabras_voz_pasiva_larga: int = UMBRAL_PALABRAS_VOZ_PASIVA_LARGA
    longitud_extracto_indicacion_max: int = LONGITUD_EXTRACTO_INDICACION_MAX
    tamano_texto_base_px: int = TAMANO_TEXTO_BASE_PX
    paso_velocidad: float = PASO_VELOCIDAD
    velocidad_minima: float = VELOCIDAD_MINIMA
    velocidad_maxima: float = VELOCIDAD_MAXIMA
    color_fondo_reproductor: str = COLOR_FONDO_REPRODUCTOR
    color_texto_reproductor: str = COLOR_TEXTO_REPRODUCTOR
    color_texto_secundario_reproductor: str = COLOR_TEXTO_SECUNDARIO_REPRODUCTOR
    pila_tipografica_reproductor: tuple[str, ...] = field(default=PILA_TIPOGRAFICA_REPRODUCTOR)

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
        if self.paso_velocidad <= 0:
            raise ValueError("El paso de velocidad debe ser un numero positivo.")
        if self.velocidad_minima <= 0 or self.velocidad_minima > self.velocidad_maxima:
            mensaje = (
                "Los limites de velocidad deben ser positivos y crecientes "
                f"({self.velocidad_minima} <= {self.velocidad_maxima})."
            )
            raise ValueError(mensaje)
        if not (self.velocidad_minima <= 1.0 <= self.velocidad_maxima):
            mensaje = (
                "El rango de velocidad debe incluir 1.0 (ritmo sin acelerar ni frenar) "
                f"({self.velocidad_minima} <= 1.0 <= {self.velocidad_maxima})."
            )
            raise ValueError(mensaje)
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
        for nombre, valor_entero in (
            ("umbral_palabras_sin_puntuacion", self.umbral_palabras_sin_puntuacion),
            ("ventana_cacofonia_palabras", self.ventana_cacofonia_palabras),
            ("repeticiones_de_minimas", self.repeticiones_de_minimas),
            ("longitud_silaba_comparada", self.longitud_silaba_comparada),
            ("longitud_minima_palabra_rima", self.longitud_minima_palabra_rima),
            ("longitud_palabra_dificil", self.longitud_palabra_dificil),
            ("consonantes_seguidas_dificil", self.consonantes_seguidas_dificil),
            ("palabras_dificiles_seguidas_minimas", self.palabras_dificiles_seguidas_minimas),
            ("umbral_subordinadas_encadenadas", self.umbral_subordinadas_encadenadas),
            ("umbral_negaciones_dobles", self.umbral_negaciones_dobles),
            ("umbral_incisos", self.umbral_incisos),
            ("umbral_palabras_voz_pasiva_larga", self.umbral_palabras_voz_pasiva_larga),
            ("longitud_extracto_indicacion_max", self.longitud_extracto_indicacion_max),
            ("tamano_texto_base_px", self.tamano_texto_base_px),
        ):
            if valor_entero <= 0:
                mensaje = f"El umbral '{nombre}' debe ser un entero positivo ({valor_entero})."
                raise ValueError(mensaje)
