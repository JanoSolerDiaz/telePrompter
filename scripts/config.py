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
# Milisegundos minimos entre dos pulsaciones aceptadas de la MISMA accion del
# reproductor (T-24, requisito 2, "antirrebote configurable"): un clicker Bluetooth
# barato puede enviar la misma tecla dos veces por un unico clic fisico (rebote de
# contacto); una pulsacion que llega antes de este tiempo desde la anterior de la
# misma accion se descarta en silencio. `0` desactiva el antirrebote. Reservada
# desde T-20 (mismo patron que `PASO_VELOCIDAD` en T-18: la constante ya existia
# antes de que la tarea que la usa llegara a la cola), cableada a `Configuracion`
# y al JSON incrustado en esta tarea.
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
# --- Resaltado, tipografia y tema de grabacion (T-21) -----------------------------
# Gradiente de atenuacion del contexto (bloques distintos al activo, requisito 1):
# opacidad por distancia al bloque activo (posicion 0 = un bloque de distancia,
# posicion 1 = dos bloques...), estrictamente decreciente. Mas alla del ultimo
# nivel se aplica ATENUACION_MINIMA como suelo: el contexto nunca desaparece del
# todo, solo se atenua mas.
ATENUACION_NIVELES: tuple[float, ...] = (0.75, 0.5, 0.35)
ATENUACION_MINIMA: float = 0.2
# Control en vivo del tamano de texto (requisito 2), mismo patron paso/minimo/maximo
# que ya uso la velocidad en T-20.
PASO_TAMANO_TEXTO_PX: int = 4
TAMANO_TEXTO_MINIMO_PX: int = 24
TAMANO_TEXTO_MAXIMO_PX: int = 96
# Color de acento del reproductor (foco visible, indicador de pausa, borde del
# bloque activo): antes escrito a mano tres veces en `estilo.css`, ahora
# configurable como el resto del tema.
COLOR_ACENTO_REPRODUCTOR: str = "#f5c542"
# Margen seguro entre el borde de la pantalla y el contenido (requisito 4): que
# nada quede cortado por el marco de un cristal de teleprompter ni por el borde
# de la pantalla de grabacion.
MARGEN_SEGURO_PX: int = 64
# Cursor oculto en pantalla completa tras esta inactividad del raton (requisito 4).
TIEMPO_INACTIVIDAD_CURSOR_MS: int = 3000

# --- Autoscroll con bloque centrado (T-22) ----------------------------------------
# Duracion del desplazamiento suave que recentra el bloque activo (requisito 2). Se
# aplica tanto al avance/retroceso como al recalculo tras cambiar el tamano de texto;
# el redimensionado de ventana recentra de forma instantanea, sin animacion.
DURACION_AUTOSCROLL_MS: int = 400

# --- Ayudas de grabacion (T-23) ----------------------------------------------------
# Cuenta atras antes de arrancar el automatico (requisito 1): duracion en segundos y
# si esta activada. "Desactivable" es el booleano, no poner la duracion a cero -- el
# mismo patron paso/activable que ya usa el resto del reproductor.
CUENTA_ATRAS_ACTIVADA: bool = True

# --- Atajos de teclado y clicker Bluetooth (T-24) -----------------------------------
# Un clicker Bluetooth se identifica ante el sistema operativo como un teclado
# corriente: no hay API que lo distinga de una pulsacion real, asi que la
# "compatibilidad" (requisito 2) es enteramente cuestion del mapa de teclas de abajo
# y de tolerar el rebote de contacto tipico de un mando barato (`ANTIRREBOTE_CLICKER_MS`,
# ya reservada mas arriba junto al resto de constantes del reproductor).
# Requisito 1: `Espacio` puede pausar/reanudar (por defecto, para quien opera desde
# teclado) o avanzar al bloque siguiente (util si el boton principal del clicker
# envia Espacio en vez de PageDown/flecha derecha, como hacen algunos mandos de
# presentaciones). Decision del dueno, no una heuristica: no hay forma de saber
# desde el navegador que boton fisico disparo la tecla.
ESPACIO_AVANZA_BLOQUE: bool = False
# Mapa de teclas del reproductor (requisitos 1 y 3): nombre de accion -> teclas que
# la disparan (varias teclas por accion, nunca una combinacion con modificador --
# requisito 4, "ningun atajo depende de combinaciones que un clicker no puede
# enviar"). Vive aqui, no escrito a mano en `guion.js`, para que sea "configurable en
# la generacion" tal cual pide el requisito 3; viaja al JSON incrustado como
# cualquier otro valor de `Configuracion` y la ayuda en pantalla (tecla `?`) se
# construye leyendo este mismo mapa, nunca uno paralelo. Tupla de pares (no un
# `dict`) para que el valor por defecto siga siendo inmutable como el resto de
# `Configuracion` (regla del dataclass congelado).
MAPA_TECLAS_REPRODUCTOR: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("pausa_avanza", (" ", "Spacebar")),
    ("bloque_siguiente", ("ArrowRight", "PageDown")),
    ("bloque_anterior", ("ArrowLeft", "PageUp")),
    ("escena_anterior", ("ArrowUp",)),
    ("escena_siguiente", ("ArrowDown",)),
    ("velocidad_mas", ("+", "=")),
    ("velocidad_menos", ("-",)),
    ("tamano_mas", ("]",)),
    ("tamano_menos", ("[",)),
    ("reiniciar_escena", ("r", "R")),
    ("ocultar_indicadores", ("h", "H")),
    ("salir_pantalla_completa", ("Escape",)),
    ("ayuda", ("?",)),
    ("espejo", ("m", "M")),
)

# --- Modo espejo (T-25) -------------------------------------------------------------
# Volteo horizontal del texto para leer contra el cristal de un teleprompter
# fisico (requisito 1). Por defecto el volteo afecta solo a la escena (titulo y
# bloques): la cabecera, la barra de progreso, la cuenta atras y la ayuda de
# teclado son indicadores para quien opera el reproductor, no texto que el
# cristal deba reflejar, y volteados de mas solo estorbarian al operador que
# mira la pantalla directamente. Con `True`, el volteo cubre tambien esos
# indicadores -- util si el montaje fisico deja SOLO el cristal entre la
# camara y toda la pantalla, indicadores incluidos.
ESPEJO_INCLUYE_INDICADORES: bool = False

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
    atenuacion_niveles: tuple[float, ...] = field(default=ATENUACION_NIVELES)
    atenuacion_minima: float = ATENUACION_MINIMA
    paso_tamano_texto_px: int = PASO_TAMANO_TEXTO_PX
    tamano_texto_minimo_px: int = TAMANO_TEXTO_MINIMO_PX
    tamano_texto_maximo_px: int = TAMANO_TEXTO_MAXIMO_PX
    color_acento_reproductor: str = COLOR_ACENTO_REPRODUCTOR
    margen_seguro_px: int = MARGEN_SEGURO_PX
    tiempo_inactividad_cursor_ms: int = TIEMPO_INACTIVIDAD_CURSOR_MS
    duracion_autoscroll_ms: int = DURACION_AUTOSCROLL_MS
    cuenta_atras_segundos: int = CUENTA_ATRAS_SEGUNDOS
    cuenta_atras_activada: bool = CUENTA_ATRAS_ACTIVADA
    antirrebote_clicker_ms: int = ANTIRREBOTE_CLICKER_MS
    espacio_avanza_bloque: bool = ESPACIO_AVANZA_BLOQUE
    mapa_teclas_reproductor: tuple[tuple[str, tuple[str, ...]], ...] = field(
        default=MAPA_TECLAS_REPRODUCTOR
    )
    espejo_incluye_indicadores: bool = ESPEJO_INCLUYE_INDICADORES

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
            ("paso_tamano_texto_px", self.paso_tamano_texto_px),
            ("tamano_texto_minimo_px", self.tamano_texto_minimo_px),
            ("tamano_texto_maximo_px", self.tamano_texto_maximo_px),
            ("tiempo_inactividad_cursor_ms", self.tiempo_inactividad_cursor_ms),
            ("duracion_autoscroll_ms", self.duracion_autoscroll_ms),
            ("cuenta_atras_segundos", self.cuenta_atras_segundos),
        ):
            if valor_entero <= 0:
                mensaje = f"El umbral '{nombre}' debe ser un entero positivo ({valor_entero})."
                raise ValueError(mensaje)
        if self.margen_seguro_px < 0:
            raise ValueError(f"El margen seguro no puede ser negativo ({self.margen_seguro_px}).")
        if not (
            self.tamano_texto_minimo_px
            <= self.tamano_texto_base_px
            <= self.tamano_texto_maximo_px
        ):
            mensaje = (
                "El tamano de texto base debe estar entre el minimo y el maximo "
                f"({self.tamano_texto_minimo_px} <= {self.tamano_texto_base_px} <= "
                f"{self.tamano_texto_maximo_px})."
            )
            raise ValueError(mensaje)
        if not self.atenuacion_niveles:
            raise ValueError("La atenuacion de contexto necesita al menos un nivel.")
        nivel_anterior = 1.0
        for nivel in self.atenuacion_niveles:
            if not (0 < nivel <= 1):
                mensaje = (
                    "Cada nivel de atenuacion debe estar entre 0 (exclusivo) y 1 "
                    f"(inclusive) ({nivel})."
                )
                raise ValueError(mensaje)
            if nivel >= nivel_anterior:
                raise ValueError(
                    "Los niveles de atenuacion deben ser estrictamente decrecientes "
                    f"({self.atenuacion_niveles})."
                )
            nivel_anterior = nivel
        if not (0 < self.atenuacion_minima <= self.atenuacion_niveles[-1]):
            mensaje = (
                "La atenuacion minima debe ser positiva y no superar el ultimo nivel "
                f"({self.atenuacion_minima} <= {self.atenuacion_niveles[-1]})."
            )
            raise ValueError(mensaje)
        if self.antirrebote_clicker_ms < 0:
            mensaje = (
                "El antirrebote del clicker no puede ser negativo "
                f"({self.antirrebote_clicker_ms})."
            )
            raise ValueError(mensaje)
        if not self.mapa_teclas_reproductor:
            raise ValueError("El mapa de teclas del reproductor no puede estar vacio.")
        for accion, teclas in self.mapa_teclas_reproductor:
            if not teclas:
                mensaje = (
                    f"La accion '{accion}' del mapa de teclas no tiene ninguna tecla asignada."
                )
                raise ValueError(mensaje)
