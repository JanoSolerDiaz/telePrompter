---
name: teleprompter
description: Convierte un guion de produccion en .md en tarjetas de locucion y un teleprompter web autocontenido con resaltado tipo karaoke. Usala cuando el usuario hable de "tarjetas de locucion", "teleprompter", "guion para grabar", "bloques de respiracion", "que tengo que recitar", o cuando pida preparar la locucion de un video a partir de un guion en Markdown, o generar subtitulos .srt borrador desde ese guion.
---

# teleprompter — del guion a la camara

> **BORRADOR (T-00).** Este archivo se completa en T-31, que exige que toda opcion por
> defecto del codigo aparezca aqui documentada, con un test que falla si divergen.
> De momento describe el flujo previsto y lo ya decidido.

Tres pasos: **guion → validacion → salidas**.

1. **Guion.** Le pasas un `.md`. La skill lo trocea en escenas, separa lo que se recita de lo que no, lo parte en bloques de respiracion y estima tiempos.
2. **Validacion.** Genera `guion-escenas.md` con todo anotado. Lo revisas **de una sola pasada en tu editor**, editas lo que quieras y dices «validado».
3. **Salidas.** Te pregunta cada vez cuales generar: el reproductor `.html` (principal), `.pptx` con marca 480, `.pdf` y `.srt` borrador.

## Reglas que esta skill no rompe nunca

- **Nada se descarta en silencio:** todo bloque del guion queda clasificado con su motivo a la vista.
- **El texto del dueno manda:** las reescrituras se proponen marcadas, el original siempre es recuperable y una edicion manual jamas se sobrescribe al revalidar.
- **El reproductor es UN archivo `.html`**, sin dependencias ni CDN, que funciona offline con doble clic.
- **Cero red y cero dependencias en ejecucion:** solo biblioteca estandar de Python 3.
- **Todo se escribe dentro de la carpeta de salida del guion**, nunca fuera, y nada se sobrescribe sin copia `.bak`.

## Convencion de guion (contractual, con aviso)

Los rotulos mandan. Cuando faltan, la skill infiere y **avisa** de la desviacion; nunca falla por ello.

| Elemento | Marca |
|----------|-------|
| Escena | `## BLOQUE N — <titulo> (m:ss – m:ss)` |
| Texto a recitar | `**LOCUCIÓN**` y el cuerpo en cita de bloque (`> `) |
| No recitable | `**EN PANTALLA**`, `**NOTA**` |
| Secciones auxiliares | `Capítulos`, `Preparación antes de grabar`, `Notas de producción` |

## Normalizacion a forma dicha (T-13)

El texto de la tarjeta es exactamente lo que hay que decir: nunca hay que traducir mentalmente una cifra o una sigla al leer en voz alta. Cada familia de regla propone una reescritura marcada (original y propuesta a la vez, nunca se pierde el texto de partida); el diccionario del dueno manda siempre sobre cualquiera de ellas.

| Familia | Ejemplo | Por defecto |
|---------|---------|-------------|
| Cardinales y anios | `2026` → «dos mil veintiséis» | Lectura completa en espanol; apocope («un»/«veintiún») y concordancia de genero solo si hay un sustantivo justo detras, por heuristica de sufijo (`config.py`, sin lista exhaustiva) |
| Ordinales | `1ª` → «primera», `3er` → «tercer» | Del 1º al 10º; fuera de ese rango no se propone nada |
| Porcentajes | `15 %` → «quince por ciento» | — |
| Monedas | `1.500 €` → «mil quinientos euros» | `SIMBOLOS_MONEDA` (`€`, `$`); con decimales, «con N céntimos» |
| Unidades abreviadas | `10 km` → «diez kilómetros» | `UNIDADES_ABREVIADAS` (km, kg, cm, mm, min, seg, h, m) |
| Rangos y fracciones | `10-250` → «diez a doscientos cincuenta»; `3/4` → «tres partido por cuatro» | — |
| Simbolos sueltos | `+` → «más», `>` → «mayor que» | `/` solo se lee dentro de una fraccion (ambiguo suelto, no se toca) |
| Siglas | `SVG` → «ese uve ge» | Deletreo letra a letra si no hay entrada en el diccionario del dueno |
| Conjunciones | `Fernando y Iker` → «Fernando e Iker»; `siete o ocho` → «siete u ocho» | Regla estandar del espanol, con la excepcion del diptongo `hie-`/`hia-` |
| Diccionario del dueno | `diccionario-locucion.json` en la carpeta de salida | Prioridad sobre cualquier regla automatica de esta tabla; ausente por defecto |

## Detector de problemas de lectura en voz alta (T-14)

Avisa de lo que va a costar decir antes de grabar. **Solo avisa, no reescribe** (salvo la excepcion de la primera fila): severidad y recomendacion por bloque de respiracion, nunca un texto sustituido en su lugar.

| Familia | Ejemplo de aviso | Por defecto |
|---------|-------------------|-------------|
| Frase sin punto de respiracion | Bloque largo sin coma ni guion dentro | ≥ 15 palabras sin puntuacion intermedia; unica familia que puede sugerir una particion (no la aplica: T-15 decide) |
| Cacofonias | «de» encadenado, silaba inicial repetida, rima involuntaria | Ventana de 6 palabras; heuristica de prefijo/sufijo de caracteres, no un silabeador real |
| Trabalenguas | Grupo de 4+ consonantes seguidas, o 3+ palabras de 10+ caracteres seguidas | `config.py` |
| Anglicismos | `feedback` → «retroalimentacion» | `ANGLICISMOS_COMUNES` (email, link, online, workshop...) |
| Estructuras dificiles | Incisos acumulados, subordinadas encadenadas, doble negacion, voz pasiva larga | `config.py` |

## Reescrituras marcadas y reversibles (T-15)

Toda propuesta de T-13 (forma dicha) y la particion de T-14 (frase sin punto de respiracion) se marca igual, con original y propuesta a la vez, para que el dueno decida sin perder nada:

```
<!-- reescritura id=... -->
> **Original:** 2026
> **Propuesta:** dos mil veintiséis
> **Motivo:** cifra: se lee en letras
> **Decisión:** PENDIENTE
<!-- /reescritura -->
```

El dueno sobrescribe `PENDIENTE` con `ACEPTAR` o `RECHAZAR` a mano, sin sintaxis fragil (la lectura ignora mayusculas y espacios de mas). Al revalidar, una reescritura ya decidida no se vuelve a proponer; solo aparecen las nuevas. Un rechazo nunca borra el original, que queda registrado en `estado.json` (append-only) por si se quiere reconsiderar. Deshacer todas las reescrituras de una escena o del guion completo es una operacion aparte que no toca el resto.

## Documento de revisión de una sola pasada (T-16)

`guion-escenas.md` es el archivo que revisas: todas las escenas en orden, con instrucciones al principio, un resumen global (escenas, palabras, duración, ritmo, avisos, reescrituras pendientes) y, por escena, sus bloques de respiración numerados con las reescrituras y avisos localizados junto a cada uno, más las indicaciones no recitables al pie con su motivo. Se edita a mano en cualquier editor de texto plano:

- Corrige el texto de un bloque de locución libremente; la revalidación respetará tu edición.
- Acepta o rechaza una reescritura sobreescribiendo su `PENDIENTE` (ver T-15).
- Para forzar la clasificación de un bloque marcado `REVISAR`, añade el rótulo (`**LOCUCIÓN**`/`**EN PANTALLA**`/`**NOTA**`) que corresponda en el guion de origen.
- Cuando termines de revisar todo el documento, cambia la marca final de más abajo de `PENDIENTE` a `VALIDADO`:

```
**Estado de la revisión:** PENDIENTE
```

Si ya existía una versión previa del archivo, se copia antes a `<nombre>.bak-<marca_de_tiempo>`: nunca se sobrescribe sin dejar rastro de lo que había.

## Reproductor: esqueleto autocontenido (T-18) e índice con pantalla completa (T-19)

`reproductor.html` es el artefacto principal: un único archivo, sin dependencias ni CDN, que funciona con doble clic desde `file://`, offline, en cualquier maquina. Embebe las escenas, los bloques de respiración y los tiempos ya calculados, más su CSS y su JS, en una sola pieza. El escapado es seguro por dos vías a la vez: los datos viajan como JSON dentro de un `<script>` y se vuelcan al DOM solo con `textContent`, nunca con marcado interpretado — ni una cita, un `<`, un `&` o una tilde del guion pueden romper la página ni ejecutarse.

El reproductor **prioriza legibilidad sobre branding**: neutro y oscuro, sin identidad corporativa, solo fuentes del sistema. Al abrirlo se ve un **índice de escenas** (título, duración estimada y estado pendiente/grabada/revisada), navegable con `Tab`, flechas y clic; elegir una entra en **pantalla completa** directamente en esa escena, con un contador "N/total" visible, y "Volver al índice" regresa sin recargar la página. El avance automático llega en T-20; el autoscroll, en T-22.

| Opción | Por defecto | Nota |
|--------|-------------|------|
| Color de fondo | `#0b0b0d` | Neutro y oscuro |
| Color de texto | `#f5f5f5` | — |
| Tamaño de letra base | 48 px | Legibilidad a distancia de cámara; ajustable en vivo, ver T-21 |
| Tipografía | fuentes del sistema | Pila de respaldo, nada remoto |

## Resaltado, tipografía y tema de grabación (T-21)

El bloque activo se lee a distancia y el contexto no compite con él: el bloque que toca decir queda a opacidad plena con un borde de acento; los bloques anteriores y posteriores se atenúan según su distancia al activo, siguiendo un gradiente configurable con un suelo mínimo (el contexto nunca desaparece del todo). El contraste del bloque activo frente al fondo es AAA (≥ 7:1, verificado por test). Márgenes seguros alrededor del contenido y cursor oculto en pantalla completa tras un tiempo de inactividad, para que no quede nada que distraiga delante de la cámara.

| Opción | Por defecto | Nota |
|--------|-------------|------|
| Gradiente de atenuación del contexto | `0.75, 0.5, 0.35` (por distancia) | Estrictamente decreciente |
| Suelo de atenuación | `0.2` | Nunca por debajo, nunca por encima del último nivel |
| Color de acento | `#f5c542` | Foco visible, indicador de pausa, borde del bloque activo |
| Paso / límites de tamaño de texto en vivo | 4 px · 24–96 px | Teclas `[` / `]` dentro del reproductor |
| Margen seguro | 64 px | Alrededor de todo el contenido |
| Inactividad antes de ocultar el cursor | 3000 ms | Solo con pantalla completa activa |

## Autoscroll con bloque centrado (T-22)

El bloque activo se mantiene siempre visible sin que quien graba tenga que tocar el ratón ni la rueda: si el texto de la escena no cabe entero en pantalla, la página se desplaza para dejarlo centrado en vertical, con una transición suave (nunca un salto brusco). Si el texto cabe entero, no se desplaza nada. Avanzar rápido a mano no produce rebotes: cada nuevo desplazamiento cancela el anterior y continúa desde la posición real en ese instante, nunca desde el objetivo antiguo. Se recentra también tras cambiar el tamaño de texto en vivo (`[`/`]`) y al redimensionar la ventana (este último, sin animación).

| Opción | Por defecto | Nota |
|--------|-------------|------|
| Duración del desplazamiento suave | 400 ms | Avance/retroceso y cambio de tamaño de texto; el redimensionado recentra al instante |

## Ayudas de grabación (T-23)

Grabar sin ayudante ni cronómetro externo: al pulsar play, una cuenta atrás 3-2-1 avisa antes de que arranque el automático (desactivable). Durante la toma, un cronómetro muestra el tiempo real transcurrido frente a la duración estimada de la escena, y una barra de progreso marca cuánto queda por recuento de bloques (llega al 100 % justo con el último). Todos estos indicadores son discretos y se ocultan y muestran de nuevo con la tecla `H`.

| Opción | Por defecto | Nota |
|--------|-------------|------|
| Duración de la cuenta atrás | 3 s | Desactivable con `cuenta_atras_activada` |
| Cuenta atrás activada | Sí | `False` la omite: el automático arranca al instante |

## Atajos de teclado y clicker Bluetooth (T-24)

Toda la escena se puede recorrer solo con `Espacio`, `Re Pág` y `Av Pág` — las tres teclas que un clicker Bluetooth de presentaciones envía (se identifica ante el sistema como un teclado corriente). El mapa completo: `Espacio` pausa/reanuda (o avanza el bloque, según configuración), `→`/`Av Pág` y `←`/`Re Pág` avanzan y retroceden un bloque, `↑`/`↓` cambian de escena, `+`/`-` ajustan la velocidad, `[`/`]` el tamaño de texto, `R` reinicia la escena, `H` oculta los indicadores, `Esc` sale de pantalla completa y `?` muestra u oculta la ayuda con el mapa vigente. Ninguna tecla depende de un modificador (`Ctrl`/`Alt`/`Mayús`), porque un clicker no puede enviarlos. El mapa completo es configurable en la generación (`mapa_teclas_reproductor`) y la ayuda en pantalla se construye leyendo ese mismo mapa, nunca una copia aparte.

| Opción | Por defecto | Nota |
|--------|-------------|------|
| `Espacio` pausa/reanuda o avanza | Pausa/reanuda | `espacio_avanza_bloque=True` lo cambia a "avanzar", para clickers cuyo botón principal envía `Espacio` |
| Antirrebote del clicker | 120 ms | Descarta una repetición de la misma acción antes de este tiempo; `0` lo desactiva |
| Mapa de teclas | ver arriba | `mapa_teclas_reproductor`: nombre de acción → teclas que la disparan |

## Modo espejo (T-25)

Para leer contra el cristal de un teleprompter físico: la tecla `M`/`m` (o el botón "Espejo" de la cabecera) voltea el texto en horizontal. Por defecto solo se voltea el título y los bloques de la escena, nunca la cabecera, la barra de progreso ni la ayuda; con `espejo_incluye_indicadores=True` se voltea el reproductor entero, para montajes donde el cristal cubre toda la pantalla. Compatible con el autoscroll, el resaltado y el cambio de tamaño de texto sin ningún ajuste extra. El ajuste persiste tras recargar (ver T-26).

| Opción | Por defecto | Nota |
|--------|-------------|------|
| Espejo incluye indicadores | No | `espejo_incluye_indicadores=True` voltea también la cabecera y el resto de indicadores |

## Persistencia local de preferencias (T-26)

Cerrar el navegador y reabrir el archivo retoma la grabación sin reconfigurar nada: `localStorage` recuerda el tamaño de texto, la velocidad ajustada por escena, el modo espejo, la visibilidad de indicadores y la última escena vista (escena y bloque). La clave se deriva del nombre del guión, así que dos guiones no se pisan las preferencias entre sí. Toda lectura y escritura está protegida con `try/catch`: si `localStorage` no está disponible (`file://` restringido, navegación privada), el reproductor funciona igual con los valores por defecto, sin errores.

En vez de relanzar automáticamente el reproductor al cargar la página (que fallaría en silencio: entrar en pantalla completa exige un gesto de usuario real), el índice ofrece un botón **"Continuar: escena N — título"** cuando hay una sesión anterior que retomar; un clic entra directamente en esa escena, en el bloque más cercano al que se dejó. Si el guión se regenera con un troceo distinto, la velocidad de cada escena se conserva (se guarda por número de escena) y la posición se reajusta al bloque cuyo instante de inicio esté más cerca del guardado, no al mismo índice. La ayuda del reproductor (`?`) incluye un botón **"Restablecer preferencias"** que borra todo lo guardado para ese guión y repone los valores por defecto sin recargar la página.

| Opción | Por defecto | Nota |
|--------|-------------|------|
| Preferencias persistidas | tamaño de texto, velocidad por escena, modo espejo, indicadores, última escena vista | Clave `teleprompter:<guion>:<preferencia>` |
| Restablecer preferencias | botón en la ayuda (`?`) | Borra solo las claves de este guión |

## Valores por defecto (extracto — la tabla completa la cierra T-31)

Todos viven en `scripts/config.py`, unico lugar del codigo donde puede haber un valor por defecto.

| Opcion | Por defecto | Nota |
|--------|-------------|------|
| Ritmo | **deducido del guion** | Del total de palabras frente a las duraciones objetivo de los encabezados |
| Ritmo de respaldo | 120 ppm | Si el guion no trae duraciones o el valor deducido no es plausible |
| Banda plausible de ritmo | 90–180 ppm | Fuera de ella se descarta el deducido, avisando |
| Bloque de respiracion | 6–12 palabras (objetivo 9) | Unidad de resaltado de todas las salidas |
| Alcance de reescrituras | forma dicha + respiracion | Cacofonias, anglicismos y estilo solo se **avisan** |
| Tipografia de marca | Poppins | Solo `.pdf` y `.pptx`; el reproductor es neutro |
| Notas internas en las salidas | incluidas | `--para-terceros` las omite |

**Precedencia:** valores por defecto → configuracion del usuario → configuracion del proyecto de guion → argumentos de la invocacion.

## Donde encaja

Es el **paso previo al montaje**. Entrega un `.srt` borrador estandar (consumible por ffmpeg) y
`tarjetas.json`, para que la fase de edicion de video no empiece de cero. Ver T-33.

## Verificacion

```
python -m mypy                                 # tipos
python -m ruff check scripts/ tests/           # estilo
python -m pytest                               # tests
python scripts/verificar_salidas.py --fixture  # extremo a extremo + auto-contencion del HTML
```

Las herramientas son **solo de desarrollo** (`requirements-dev.txt`): la skill se ejecuta sin ellas.
