---
name: teleprompter
description: Convierte un guion de produccion en .md en tarjetas de locucion y un teleprompter web autocontenido con resaltado tipo karaoke. Usala cuando el usuario hable de "tarjetas de locucion", "teleprompter", "guion para grabar", "bloques de respiracion", "que tengo que recitar", o cuando pida preparar la locucion de un video a partir de un guion en Markdown, generar subtitulos .srt borrador desde ese guion, exportarlo a .pdf con la marca 480, o convertirlo en una presentacion .pptx con la marca 480.
---

# teleprompter — del guion a la camara

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

Detalle completo, casos límite y cómo se resuelven los conflictos entre señales:
`references/convencion-guion.md`.

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

Formato completo del documento (anclas de bloque, sintaxis de reescritura, qué se puede editar a mano): `references/formato-guion-escenas.md`.

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

Mapa completo, por qué un clicker Bluetooth funciona sin código especial y cómo calibrar uno físico: `references/mapa-teclas.md`.

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

## Copia de seguridad de preferencias, con aviso de persistencia (R-01)

T-26 confía en que `localStorage` sobrevive a cerrar el navegador y reabrir el archivo, algo que no estaba comprobado en el navegador real de grabación (`origen: auditoría #5`). Esta tarea aporta las tres piezas que faltaban:

1. **Comprobación real**, no solo teórica: al cargar la página, el reproductor escribe y relee una clave de prueba en `localStorage`. Verificado con Playwright headless (Chromium) sobre el reproductor real: reabrir el **mismo perfil** de navegador tras cerrarlo mantiene las preferencias intactas; un perfil nuevo (u otro navegador) empieza sin nada, porque `localStorage` está particionado por perfil/origen — es el comportamiento esperado, no un fallo. El límite real de este mecanismo es que ningún código puede saber, dentro de una sola carga de página, si sobrevivirá a un cierre futuro: solo puede detectar que `localStorage` **no funciona aquí en absoluto** (navegación privada, cuota agotada, `file://` restringido).
2. **Aviso honesto**: si esa comprobación falla, el índice muestra un mensaje visible en vez de perder los ajustes en silencio (como hacía T-26, con el `try/catch` ya existente pero sin ningún aviso).
3. **Plan B sin red ni dependencias**: los botones **"Exportar preferencias"** e **"Importar preferencias"** en el índice empaquetan tamaño de texto, velocidad por escena, modo espejo, indicadores y última escena vista en un `.json` descargable (o, si el navegador no permite disparar la descarga, un texto para copiar a mano) y los restauran de vuelta, escena y bloque incluidos. La exportación lee siempre de las variables en memoria — no solo de `localStorage` — así que funciona igual de bien cuando el almacenamiento está completamente bloqueado.

| Opción | Por defecto | Nota |
|--------|-------------|------|
| Exportar preferencias | botón en el índice | Descarga `teleprompter-preferencias-<guion>.json`; si el navegador no permite la descarga, ofrece el mismo texto para copiar |
| Importar preferencias | botón en el índice | Selector de archivo `.json`; valida que sea del mismo guión antes de aplicar nada |
| Aviso de almacenamiento no disponible | automático | Comprueba escritura/lectura real de `localStorage` al cargar la página |

## Registro de tomas por escena (R-02)

El índice deja de ser solo una lista y pasa a ser el parte de rodaje: cada escena recuerda cuántas tomas se grabaron, cuánto duró realmente cada una (el mismo cronómetro de las ayudas de grabación, congelado en pausa) y cuál quedó marcada como la buena. Una toma se cierra al volver al índice, al pasar a otra escena sin pasar por el índice (flechas arriba/abajo), o al reiniciar la escena en curso (`R`) — reiniciar es la forma natural de decir "esta toma no vale, repito": cierra la que se abandona y arranca el cronómetro de cero para la siguiente, sin heredarle tiempo de la fallida.

Sin salir del modo de grabación y con una sola tecla cada vez (requisito de "mínimo de teclas"): `G` marca la toma en curso como la buena (como mucho una por escena; marcar otra desmarca la anterior) y `N` abre un cuadro de diálogo para una nota rápida. El estado de cada escena en el índice (Pendiente / Grabada / Revisada) se deriva de estos datos reales, no de si se visitó una vez: sin ninguna toma es Pendiente, con tomas pero ninguna marcada como buena es Grabada, con una toma buena es Revisada — así se ve de un vistazo qué falta, qué se repitió y qué ya está resuelto. Persistido en `localStorage` con clave por escena (mismo mecanismo que T-26): sobrevive a cerrar el navegador, y "Restablecer preferencias" (T-26) nunca lo borra, porque el registro de tomas no es una preferencia de lectura.

El botón **"Exportar parte de rodaje"** del índice vuelca el registro completo (todas las escenas con al menos una toma) a un `.json` independiente — el reproductor no puede escribir directamente en la carpeta de salida del guión (cero red en tiempo de ejecución). Ese archivo es legible tal cual por el dueño y por la fase de montaje; cuando se entrega de vuelta, `scripts/tomas.py` (`cargar_parte_de_rodaje`/`registrar_tomas`) lo valida y lo fusiona en `estado.json` (contenedor `tomas`, esquema versión 2), para que quede disponible sin depender de reabrir el reproductor. Forma exacta del archivo y de `estado.json["tomas"]`: `references/contrato-tomas.md`.

| Opción | Por defecto | Nota |
|--------|-------------|------|
| Marcar toma buena / nota rápida | teclas `G` / `N` | Parte del mapa configurable, `mapa_teclas_reproductor` |
| Exportar parte de rodaje | botón en el índice | Descarga `teleprompter-tomas-<guion>.json`; mismo plan B de copiar a mano si la descarga falla |
| Fusión en `estado.json` | `scripts/tomas.registrar_tomas` | Reemplaza por escena con lo más reciente exportado; nunca borra tomas de una escena que la exportación no menciona |

## Marcar tropiezos durante la toma (R-03)

Una tecla marca el bloque EN PANTALLA como problemático sin interrumpir la toma: `T` alterna la marca del bloque activo, sin abrir ningún diálogo ni pausar el automático — a diferencia de `nota_toma` (R-02), es un interruptor inmediato. El indicador de la cabecera ("⚠ Tropiezo") y el resumen junto a cada escena del índice muestran de un vistazo qué hay marcado, sin tener que abrir ningún archivo.

El botón **"Exportar tropiezos"** del índice vuelca todos los bloques marcados (todas las escenas con al menos uno) a un `.json` independiente, mismo mecanismo de descarga que "Exportar parte de rodaje". Cuando se entrega de vuelta, `scripts/feedback.py` (`cargar_registro_tropiezos`/`registrar_tropiezos_en_feedback`) lo valida y añade una fila `nuevo` por cada tropiezo a `FEEDBACK.md` **dentro de la carpeta de salida del guion** — no confundir con `roadmap/FEEDBACK.md`, la bandeja de historias de usuario del propio proyecto teleprompter, que vive en otro sitio con otro propósito. R-03 no añade ningún contenedor a `estado.json` (migración: no): `FEEDBACK.md` ya es en sí mismo el registro persistente.

Mientras una fila siga en estado `nuevo`, la siguiente vez que se regenere `guion-escenas.md` (`documento_revision.generar_documento_revision(..., tropiezos_por_escena=feedback.tropiezos_marcados_por_escena(carpeta_salida))`) ese bloque aparece destacado con una línea `🎬 **Tropiezo marcado en grabación**`, para reescribirlo a mano o pedir una propuesta a la skill. El emparejamiento es por **texto exacto del bloque**, no por índice — sobrevive a que una partición de respiración desplace los índices posteriores entre la grabación y la revisión; si el dueño reescribe el bloque, deja de coincidir y el aviso desaparece solo. Cambiar la palabra `nuevo` de una fila por cualquier otra (p. ej. `resuelto`) también apaga el aviso sin tocar el texto — útil cuando el problema era la lectura de esa toma, no el guion.

| Opción | Por defecto | Nota |
|--------|-------------|------|
| Marcar/desmarcar tropiezo | tecla `T` | Parte del mapa configurable, `mapa_teclas_reproductor` |
| Exportar tropiezos | botón en el índice | Descarga `teleprompter-tropiezos-<guion>.json`; mismo plan B de copiar a mano si la descarga falla |
| Volcado a `FEEDBACK.md` | `scripts/feedback.registrar_tropiezos_en_feedback` | Añade filas `nuevo`, nunca borra ni reescribe una fila existente; copia de seguridad `.bak-<marca>` si el archivo ya existía |
| Destacado en la siguiente revisión | `scripts/feedback.tropiezos_marcados_por_escena` + `documento_revision.generar_documento_revision(..., tropiezos_por_escena=...)` | Casa por texto exacto del bloque, no por índice; solo mientras la fila siga en `nuevo` |

## Recalibrar el ritmo con tiempos reales (R-04)

Cierra el bucle del ritmo: T-12 deduce el ppm de las duraciones **objetivo** de cabecera (una intención del guionista) y calcula con ese ppm la duración **estimada** de cada bloque; R-02 aporta la duración **real** de la toma marcada como buena de cada escena. `scripts/calibracion.py` (`calcular_calibracion`) junta ambas fuentes — nunca recalcula tiempos por su cuenta, lee el `ResultadoTiempos` ya calculado y `estado.tomas` ya fusionado — y produce, por cada guion de entrada, un contraste escena a escena con las tres duraciones una al lado de otra. Una escena con tomas pero ninguna marcada buena no aporta evidencia real todavía: mezclar una toma fallida sin marcar habría contaminado la calibración con un tiempo que el dueño no validó como representativo.

Cada escena se clasifica por **posición**, no por título — apertura (la primera de cada guion), cierre (la última), desarrollo (el resto) — porque el título de la última escena no siempre dice literalmente "Cierre" (mismo criterio posicional que ya usó T-10 para el subtítulo entrecomillado). El informe agrega la desviación real-frente-a-estimada por tipo entre todos los guiones de entrada, para decir de un vistazo en qué tipo de escena el locutor se acelera y en cuál se frena.

Con la evidencia acumulada de **varios guiones** (nunca de uno solo, para no sobreajustar a sus particularidades) se propone un ppm calibrado — palabras reales entre minutos reales de toma buena, sujeto a la misma banda de plausibilidad que el ppm deducido de T-12 —, pero **nunca se aplica sola**: es una propuesta que Claude formula al dueño dentro de la sesión (mismo patrón que la pregunta de salidas de T-30), y solo si el dueño la acepta se fija `Configuracion.ppm_manual` en una próxima pasada. Sin evidencia suficiente (menos de `calibracion_guiones_minimos` guiones, menos de `calibracion_palabras_minimas` palabras, o un ppm deducido fuera de banda) no hay propuesta, con el motivo explícito.

| Opción | Por defecto | Nota |
|--------|-------------|------|
| Evidencia mínima | 2 guiones, 150 palabras | `calibracion_guiones_minimos` / `calibracion_palabras_minimas` |
| Fuente de la duración real | toma marcada `buena` (R-02) | Una escena sin toma buena no aporta evidencia, nunca se estima |
| Ppm calibrado propuesto | nunca automático | El dueño lo acepta o lo rechaza; se aplicaría a mano en `ppm_manual` |

## Exportador `.srt` borrador (T-27)

Arranca los subtítulos en la fase de montaje sin partir de cero: un subtítulo por bloque de respiración, con los tiempos ya calculados por el motor de tiempos, sobre el **texto locutado final** (con las reescrituras aceptadas ya aplicadas, nunca el original del guión). Un bloque muy corto se funde con el siguiente de la misma escena para no parpadear en pantalla — nunca funde bloques de escenas distintas —, y un bloque cuyo texto no cabe en el límite de líneas configurado se reparte en varios subtítulos consecutivos sin cortar ninguna palabra ni perder texto. Formato `.srt` estándar (índice, marca de tiempo, texto), UTF-8, validado con las mismas reglas que aplica ffmpeg.

| Opción | Por defecto | Nota |
|--------|-------------|------|
| Duración mínima de un subtítulo | 1,2 s | Por debajo, se funde con el siguiente bloque de la misma escena; `0` desactiva la agrupación |
| Caracteres por línea | 42 | — |
| Líneas por subtítulo | 2 | Un bloque que no cabe se reparte en varios subtítulos, con el tiempo repartido según las palabras de cada reparto |
| BOM (marca de orden de bytes) | No | `srt_con_bom=True` antepone el BOM; UTF-8 sin él por defecto |

## `.srt` alineado con la toma buena (R-05)

El `.srt` de arriba es un borrador con tiempos **estimados** a partir del ritmo deducido del guion; una vez grabada la toma buena de cada escena (registro de tomas, R-02), `scripts/srt_alineado.py` (`generar_srt_alineado`) reescala los bloques de esa escena a su duración **real** — el mismo factor (`duración real / duración estimada`) se aplica a la palabra hablada y a la pausa de cada bloque, así que el reparto relativo entre ellos se conserva y solo cambia la escala. Una escena sin toma buena todavía conserva su duración estimada sin tocar: nunca se inventa un tiempo real que no existe, con el detalle disponible en `escenas_sin_toma_buena` para que quien lo lea sepa exactamente cuáles faltan. El `.srt` estimado sigue siendo una salida independiente (`guion.srt`); el alineado se escribe en un archivo aparte (`guion-alineado.srt`) — ni se genera uno solo a partir del otro ni se sobrescriben entre sí. Reutiliza tal cual la agrupación, partición limpia, formato y validador estricto de T-27: ninguna regla nueva de subtítulos.

| Opción | Por defecto | Nota |
|--------|-------------|------|
| Tolerancia de duración | 0,05 s | Umbral documentado para comprobar que la escena alineada dura lo mismo que la toma buena (redondeo a milisegundos al serializar, no del reescalado en sí) |

## Capítulos de YouTube con marcas de tiempo reales (R-07)

`scripts/capitulos_youtube.py` cierra el ciclo entre lo que ya se escribe en el guion y lo que hay que pegar en la descripción del vídeo: T-08 ya conserva íntegra la sección auxiliar `## Capítulos (para la descripción del vídeo)` que traen los guiones reales (una tabla `| Marca | Capítulo |`); este módulo lee los títulos de su columna «Capítulo» y los empareja, **por orden de aparición** (nunca por texto ni por número de escena), con las escenas del guion.

El tiempo acumulado de inicio de cada escena usa la duración **real** de su toma buena (registro de tomas, R-02) cuando existe; una escena sin toma buena todavía cae a su duración **estimada** de T-12 — el cursor se acumula de forma continua escena a escena, igual que el `.srt` alineado (R-05). Si alguna de las marcas del archivo depende de una duración estimada, la **primera línea** de `capitulos-youtube.txt` lo advierte explícitamente en vez de mezclar tiempos reales y estimados en silencio.

Formato exacto de YouTube (requisito de la propia plataforma): la primera marca es siempre `0:00`, una línea `M:SS Título` por capítulo en orden creciente, y ninguna marca a menos del mínimo configurado de la anterior — la marca demasiado cercana se omite (el capítulo sigue íntegro en el guion, solo no aparece como marca propia en este archivo derivado). Si el guion no trae la sección `Capítulos`, no se genera ningún archivo y se informa del motivo — nunca se inventa contenido que el guionista no ha escrito.

| Opción | Por defecto | Nota |
|--------|-------------|------|
| Título de la sección de capítulos | `Capítulos` | Prefijo con el que se reconoce la sección auxiliar (T-08) que trae la tabla |
| Marca mínima entre capítulos | 10 s | Mínimo de la propia plataforma YouTube; una marca más cercana a la anterior se omite |

## Exportador `.pdf` con identidad 480 (T-28)

Documento de repaso antes de grabar y, llegado el caso, entregable presentable a terceros: el guion completo con la identidad visual de la casa (`references/marca-480.md`), una **escena por página** — título, duración objetivo y estimada, y el texto de locución **legible como prosa** (los límites de bloque se marcan de forma discreta, nunca como lista de tarjetas), con las indicaciones no recitables al pie. Portada con el título, la duración total y objetivo, el número de escenas y de palabras.

El logotipo (variante Gris, para fondo claro) se incrusta en el propio HTML como `data:image/png;base64,...`: ni siquiera un archivo local aparte cuenta como autocontenido. Su relación de aspecto **se mide de la cabecera `IHDR` del PNG en el momento de generar**, nunca de una constante — la guía de marca dice 668/376, pero los archivos reales miden 1993×805 (ratio 2,4758); usar la constante de la guía los habría deformado un 39 %. Si el archivo no existe o no es un PNG válido, el PDF sale sin logotipo y no falla.

La conversión a `.pdf` usa Chrome o Edge en modo headless (`--print-to-pdf`), detectado por nombre en el `PATH` o por las rutas de instalación estándar de Windows/macOS (`pdf_chrome_ejecutable_manual` fija una ruta a mano si la detección no la encuentra). **Sin Chrome/Edge disponible, la skill deja listo el HTML de impresión con instrucciones para exportarlo a mano con Ctrl+P — nunca falla por su ausencia.**

`Configuracion.incluir_notas_internas` (el mismo interruptor que usará T-29) es el modo **`--para-terceros`**: en `False` omite las indicaciones marcadas como nota interna de producción (rótulo `**NOTA**`), y deja solo el texto de locución final y las indicaciones de pantalla (`**EN PANTALLA**`, y cualquier indicación ambigua sin rótulo claro: nunca se decide en silencio que algo es prescindible).

| Opción | Por defecto | Nota |
|--------|-------------|------|
| Tipografía de marca | Poppins | Respaldo Montserrat → Calibri → sans del sistema (`respaldo_tipografico`), resuelto por nombre del sistema |
| Ruta del logotipo | `assets/marca/480_Gris.png` | Variante Gris (fondo claro); ausente → PDF sin logotipo, no falla |
| Ancho del logotipo (portada / pie de página) | 2,4" / 0,7" | El alto se calcula siempre del ratio medido del PNG |
| Márgenes (lateral / superior) | 0,6" / 0,5" | Mínimo de la guía de marca |
| Interlineado del cuerpo | 1,4 | Dentro del rango 1,3–1,5 de la guía de marca |
| Notas internas incluidas | Sí | `incluir_notas_internas=False` es el modo `--para-terceros` |
| Ruta manual de Chrome/Edge | ninguna | `pdf_chrome_ejecutable_manual`; si no se fija, detección automática |

## Adaptador `.pptx` con identidad 480 (T-29)

Entrega el guion de locución como presentación de marca **sin reinventar estilos**: la skill `480-branded-pptx` (Node + `pptxgenjs`, apoyada a su vez en la skill `pptx`) son instrucciones **para Claude**, no un ejecutable, así que esta skill no la invoca como subproceso. En su lugar produce dos archivos en la carpeta de salida — `tarjetas.json` (el contrato de intercambio, documentado en `references/contrato-tarjetas.md`) y `brief-pptx.md` (el brief de invocación en Markdown) — y es Claude quien genera el `.pptx` de verdad, delegando en esa skill dentro de la misma sesión, leyendo ambos archivos.

`tarjetas.json` trae, por escena: número, título, duración objetivo y estimada, aviso de desviación si lo hay, los bloques de respiración (texto **locutado final**, con las reescrituras aceptadas ya materializadas), la prosa unida, y las indicaciones no recitables ya separadas en `indicaciones_pantalla` y `notas_internas` — mismo criterio que el `.pdf` (T-28) para distinguir una de otra. El modo `--para-terceros` (el mismo `incluir_notas_internas=False` de T-28) vacía `notas_internas` en el propio JSON, no solo en la presentación. El brief describe la estructura de deck que la skill de marca ya impone (portada DARK, índice LIGHT solo si hay 4+ diapositivas de contenido, una diapositiva de contenido por escena — agrupación configurable —, cierre DARK) y corrige por escrito dos discrepancias conocidas de su `SKILL.md` frente a los assets reales de este proyecto: usar Poppins en vez de Figtree, y la relación de aspecto del logotipo medida del PNG (con una tabla de alturas ya calculada) en vez de la constante `668/376` de la guía de marca.

Si `480-branded-pptx` o su dependencia, la skill `pptx`, no están instaladas en esta máquina, `tarjetas.json` y el brief se generan igual y la generación **nunca falla**: el mensaje devuelto marca la salida `.pptx` como latente y dice exactamente qué falta.

| Opción | Por defecto | Nota |
|--------|-------------|------|
| Escenas por diapositiva de contenido | 1 | `pptx_escenas_por_diapositiva`: agrupación configurable |
| Umbral de diapositiva de índice | 4 diapositivas de contenido | `pptx_umbral_indice_secciones`, según `references/marca-480.md` |
| Logotipo sobre fondo oscuro | `assets/marca/480_Blanco.png` | Portada y cierre; el de fondo claro reutiliza `ruta_logo_pdf` (T-28) |
| Ancho del logotipo (portada / contenido / cierre) | 2,4" / 0,7" / 2,8" | El alto se calcula siempre del ratio medido del PNG, igual que el `.pdf` |
| Rutas de las skills de marca | `~/.claude/skills/480-branded-pptx` y `~/.claude/skills/pptx` | Solo se comprueba que la carpeta existe; ausentes → salida `.pptx` latente, nunca falla |
| Notas internas en `tarjetas.json` | incluidas | `--para-terceros` las vacía del propio JSON, no solo del deck |

## Selector de salidas por validación (T-30)

Cada vez que se valida, la skill pregunta cuáles de las cuatro salidas generar (reproductor `.html`, `.pptx`, `.pdf`, `.srt`) en una única pregunta de opción múltiple — nunca decide en silencio. La última selección se recuerda en `estado.json` como **sugerencia** marcada en la propia pregunta, no como una decisión que se aplica sola; sin ninguna selección previa, sugiere las cuatro.

Las salidas seleccionadas se generan de forma independiente: el fallo o la latencia de una (Chrome/Edge ausente para el `.pdf` real, la skill de marca ausente para el `.pptx` real) nunca impide las demás. El resumen final lista la ruta y el tamaño de cada archivo generado, y el motivo de cada salida omitida (no seleccionada, o fallida) o latente (seleccionada, con lo generable ya en disco, pendiente de una dependencia externa).

| Opción | Por defecto | Nota |
|--------|-------------|------|
| Salidas seleccionadas | pregunta cada vez | Sin selección previa, sugiere las cuatro; con histórico, sugiere la última selección registrada en `estado.json` |

## Precedencia de configuración (T-31)

```
valores por defecto  →  configuración del usuario  →  configuración del proyecto de guion  →  argumentos de la invocación
```

- **Valores por defecto:** los de la tabla de abajo, escritos una sola vez en `scripts/config.py` (`Configuracion`, dataclass congelado — "sin números mágicos", §0.2). Ningún otro módulo lleva una constante de comportamiento escrita a mano.
- **Configuración del usuario:** preferencias del dueño que valen para todos sus guiones (p. ej. "yo siempre grabo a 0.9x"). Hoy no hay un archivo de configuración de usuario propio: el dueño se lo dice a Claude en la conversación y Claude lo traslada al nivel siguiente.
- **Configuración del proyecto de guion:** ajustes que valen solo para un guion concreto y persisten junto a él — `configuracion_efectiva` dentro de su `estado.json` (T-07) es exactamente esto: la `Configuracion` con la que se procesó esa carpeta de salida, para que una revalidación (T-17) reutilice el mismo criterio sin que el dueño tenga que repetirlo.
- **Argumentos de la invocación:** lo que el dueño pide para esta sesión en concreto (p. ej. "genera el PDF para terceros"). Es el nivel más específico y gana siempre sobre los tres anteriores.

Mecánicamente, cada nivel es un `Configuracion(**overrides)`: esta skill no tiene ni tendrá una CLI de terminal con `argparse` propia (ver `DECISIONES_TECNICAS.md`, T-30) — es Claude quien construye la `Configuracion` efectiva de la sesión combinando estos niveles antes de llamar a cada módulo, nunca el propio código con un `input()`.

## Valores por defecto — tabla completa (T-31)

Todo valor de esta tabla vive en `scripts/config.py`, único lugar del código donde puede
haber un valor por defecto, como campo de `Configuracion` (columna "Clave"). Un test
(`tests/test_skill_md.py`) compara los campos reales de `Configuracion` contra las
claves citadas aquí y falla si divergen en cualquier sentido — ninguno de los dos puede
adelantarse al otro.

### Ritmo y tiempos (T-12)

| Clave | Por defecto | Nota |
|-------|-------------|------|
| `ppm_respaldo` | 120 ppm | Respaldo si el guion no trae duraciones objetivo o el valor deducido no es plausible |
| `ppm_banda_plausible` | 90–180 ppm | Fuera de esta banda se descarta el ppm deducido del guion, avisando |
| `ppm_manual` | ninguno | Calibración con toma real; si se fija, gana al deducido y al respaldo |
| `pausa_coma_segundos` | 0,15 s | Pausa tras una coma |
| `pausa_punto_segundos` | 0,35 s | Pausa tras un punto |
| `pausa_fin_parrafo_segundos` | 0,6 s | Pausa al final de un párrafo |
| `pausa_fin_escena_segundos` | 1,0 s | Pausa al final de una escena |
| `umbral_desviacion_tiempos` | 0,15 (15 %) | A partir de aquí se avisa de la desviación entre duración estimada y objetivo |
| `calibracion_guiones_minimos` | 2 | Guiones con al menos una toma buena necesarios para proponer un ppm calibrado (R-04) |
| `calibracion_palabras_minimas` | 150 | Palabras de evidencia real mínimas para proponer un ppm calibrado (R-04) |

### Troceo en bloques de respiración (T-11)

| Clave | Por defecto | Nota |
|-------|-------------|------|
| `palabras_por_bloque_min` | 6 | Mínimo de palabras de un bloque de respiración |
| `palabras_por_bloque_objetivo` | 9 | Tamaño al que aspira el troceador |
| `palabras_por_bloque_max` | 12 | Máximo antes de forzar un corte |

### Convención de guion (T-08, T-09)

| Clave | Por defecto | Nota |
|-------|-------------|------|
| `rotulo_locucion` | `**LOCUCIÓN**` | Rótulo del texto a recitar |
| `rotulos_no_locucion` | `**EN PANTALLA**`, `**NOTA**` | Rótulos de lo no recitable |
| `secciones_auxiliares` | `Capítulos`, `Preparación antes de grabar`, `Notas de producción` | Títulos que nunca son escena aunque casen con el nivel de encabezado |

`PATRON_ENCABEZADO_ESCENA` (el patrón `## BLOQUE N — <título> (m:ss – m:ss)`) es
también un valor de `scripts/config.py`, pero no es un campo de `Configuracion`
sobreescribible en la invocación: cambiar el formato de escena es una decisión
contractual con el dueño (§0.2), no un ajuste de sesión. Detalle completo en
`references/convencion-guion.md`.

### Detector de problemas de lectura en voz alta (T-14)

| Clave | Por defecto | Nota |
|-------|-------------|------|
| `umbral_palabras_sin_puntuacion` | 15 | Frase sin punto de respiración a partir de esta longitud |
| `ventana_cacofonia_palabras` | 6 | Ventana de palabras para detectar cacofonías/rima |
| `repeticiones_de_minimas` | 3 | Repeticiones de «de» dentro de la ventana para avisar |
| `longitud_silaba_comparada` | 3 | Caracteres de prefijo/sufijo comparados para sílaba inicial repetida o rima |
| `longitud_minima_palabra_rima` | 5 | Longitud mínima de palabra para que cuente en la detección de rima |
| `longitud_palabra_dificil` | 10 | Caracteres a partir de los cuales una palabra cuenta como "difícil" |
| `consonantes_seguidas_dificil` | 4 | Consonantes seguidas que marcan una palabra como trabalenguas |
| `palabras_dificiles_seguidas_minimas` | 3 | Palabras difíciles seguidas que disparan el aviso de acumulación |
| `subordinantes` | que, porque, aunque, cuando, donde, como, si, mientras | Nexos que cuentan para "subordinadas encadenadas" |
| `umbral_subordinadas_encadenadas` | 2 | Repeticiones de un subordinante para avisar |
| `negaciones` | no, nunca, jamás, nadie, ninguno, ninguna, tampoco | Palabras que cuentan para "doble negación" |
| `umbral_negaciones_dobles` | 2 | Negaciones en el mismo bloque para avisar |
| `umbral_incisos` | 2 | Incisos (paréntesis, guiones largos, comas de inciso) para "incisos anidados" |
| `umbral_palabras_voz_pasiva_larga` | 8 | Palabras mínimas del bloque para que una voz pasiva cuente como "larga" |

`ANGLICISMOS_COMUNES` es una tabla completa (anglicismo → equivalente en español), no
un campo individual de `Configuracion` — misma decisión que las tablas de
normalización de abajo. Documentada por nombre en la sección de detección de arriba.

### Normalización a forma dicha (T-13) — tablas, no campos individuales

`SIMBOLOS_MONEDA` y `UNIDADES_ABREVIADAS` son tablas completas (símbolo/abreviatura →
forma dicha), no un campo `Configuracion` por entrada: ampliarlas es editar la tabla
en `scripts/config.py`, o añadir la excepción puntual al diccionario del dueño
(`diccionario-locucion.json`, que siempre gana). Documentadas por nombre en la sección
de normalización más arriba.

### Documento de revisión (T-16)

| Clave | Por defecto | Nota |
|-------|-------------|------|
| `longitud_extracto_indicacion_max` | 120 caracteres | Longitud máxima del extracto de una indicación no recitable al pie de escena |

### Reproductor: tema, resaltado y velocidad (T-18, T-20, T-21)

| Clave | Por defecto | Nota |
|-------|-------------|------|
| `tamano_texto_base_px` | 48 px | Tamaño de letra inicial |
| `paso_velocidad` | 0,1 | Incremento de velocidad por pulsación |
| `velocidad_minima` | 0,5× | Límite inferior de velocidad |
| `velocidad_maxima` | 2,0× | Límite superior de velocidad |
| `color_fondo_reproductor` | `#0b0b0d` | Neutro y oscuro, sin identidad corporativa |
| `color_texto_reproductor` | `#f5f5f5` | — |
| `color_texto_secundario_reproductor` | `#9a9a9a` | Indicadores secundarios (cabecera, contadores) |
| `pila_tipografica_reproductor` | fuentes del sistema | `-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif`; nada remoto |
| `atenuacion_niveles` | 0,75 / 0,5 / 0,35 | Opacidad del contexto por distancia al bloque activo, estrictamente decreciente |
| `atenuacion_minima` | 0,2 | Suelo de atenuación: el contexto nunca desaparece del todo |
| `paso_tamano_texto_px` | 4 px | Incremento del tamaño de texto en vivo (`[`/`]`) |
| `tamano_texto_minimo_px` | 24 px | — |
| `tamano_texto_maximo_px` | 96 px | — |
| `color_acento_reproductor` | `#f5c542` | Foco visible, indicador de pausa, borde del bloque activo |
| `color_estado_grabada_reproductor` | `#4ade80` | Insignia de estado "Grabada" del índice (T-19) |
| `color_estado_revisada_reproductor` | `#60a5fa` | Insignia de estado "Revisada" del índice (T-19) |
| `margen_seguro_px` | 64 px | Alrededor de todo el contenido |
| `tiempo_inactividad_cursor_ms` | 3000 ms | Antes de ocultar el cursor en pantalla completa |

### Autoscroll (T-22)

| Clave | Por defecto | Nota |
|-------|-------------|------|
| `duracion_autoscroll_ms` | 400 ms | Duración del desplazamiento suave al recentrar el bloque activo |

### Ayudas de grabación (T-23)

| Clave | Por defecto | Nota |
|-------|-------------|------|
| `cuenta_atras_segundos` | 3 s | Duración de la cuenta atrás antes de arrancar el automático |
| `cuenta_atras_activada` | Sí | `False` la omite: el automático arranca al instante |

### Atajos de teclado y clicker Bluetooth (T-24)

| Clave | Por defecto | Nota |
|-------|-------------|------|
| `antirrebote_clicker_ms` | 120 ms | Descarta una repetición de la misma acción antes de este tiempo; `0` lo desactiva |
| `espacio_avanza_bloque` | No | `True`: `Espacio` avanza el bloque en vez de pausar/reanudar |
| `mapa_teclas_reproductor` | ver `references/mapa-teclas.md` | Acción → teclas que la disparan; ninguna con modificador |

### Modo espejo (T-25)

| Clave | Por defecto | Nota |
|-------|-------------|------|
| `espejo_incluye_indicadores` | No | `True` voltea también cabecera, barra de progreso y ayuda |

### Exportador `.srt` borrador (T-27)

| Clave | Por defecto | Nota |
|-------|-------------|------|
| `srt_caracteres_por_linea_max` | 42 | — |
| `srt_lineas_max_por_subtitulo` | 2 | Un grupo que no cabe se reparte en varios subtítulos consecutivos |
| `srt_duracion_minima_segundos` | 1,2 s | Por debajo, el bloque se funde con el siguiente de la misma escena; `0` desactiva la agrupación |
| `srt_con_bom` | No | `True` antepone la marca de orden de bytes (BOM) |
| `srt_alineado_tolerancia_segundos` | 0,05 s | `.srt` alineado (R-05): tolerancia documentada para que la escena reescalada dure lo mismo que la toma buena |

### Capítulos de YouTube (R-07)

| Clave | Por defecto | Nota |
|-------|-------------|------|
| `titulo_seccion_capitulos` | `Capítulos` | Prefijo con el que se reconoce la sección auxiliar (T-08) que trae la tabla de capítulos |
| `capitulos_youtube_marca_minima_segundos` | 10 s | Mínimo de la propia plataforma YouTube entre dos marcas consecutivas; una marca más cercana a la anterior se omite |

### Exportador `.pdf` con identidad 480 (T-28)

| Clave | Por defecto | Nota |
|-------|-------------|------|
| `tipografia_marca` | Poppins | Compartida con el `.pptx`; el reproductor es neutro y no la usa |
| `respaldo_tipografico` | Montserrat → Calibri → sans-serif | Si Poppins no está instalada en el sistema |
| `incluir_notas_internas` | Sí | `False` es el modo `--para-terceros`; compartida con el `.pptx` |
| `ruta_logo_pdf` | `assets/marca/480_Gris.png` | Variante sobre fondo claro; ausente → PDF sin logotipo, no falla |
| `pdf_ancho_logo_portada_pulgadas` | 2,4" | El alto se calcula siempre del ratio medido del PNG |
| `pdf_ancho_logo_pie_pulgadas` | 0,7" | — |
| `pdf_margen_lateral_pulgadas` | 0,6" | Mínimo de la guía de marca |
| `pdf_margen_superior_pulgadas` | 0,5" | — |
| `pdf_interlineado` | 1,4 | Dentro del rango 1,3–1,5 de la guía de marca |
| `pdf_color_texto` | `#333333` | — |
| `pdf_color_texto_secundario` | `#888888` | — |
| `pdf_color_acento` | `#39FE90` | Línea bajo los títulos |
| `pdf_color_alerta` | `#FF4950` | — |
| `pdf_color_fondo` | `#FFFFFF` | Versión clara, para impresión en papel |
| `pdf_color_borde` | `#E5E7EB` | Borde sutil de las tarjetas |
| `pdf_chrome_ejecutable_manual` | ninguno | Ruta a mano si la detección automática de Chrome/Edge no lo encuentra |
| `pdf_timeout_conversion_segundos` | 30 s | Tope de tiempo del subproceso de conversión a `.pdf` |

### Adaptador `.pptx` con identidad 480 (T-29)

| Clave | Por defecto | Nota |
|-------|-------------|------|
| `ruta_skill_marca_pptx` | `~/.claude/skills/480-branded-pptx` | Solo se comprueba que la carpeta existe; ausente → salida latente, nunca falla |
| `ruta_skill_pptx_base` | `~/.claude/skills/pptx` | Dependencia de la anterior |
| `pptx_escenas_por_diapositiva` | 1 | Agrupación configurable de escenas por diapositiva de contenido |
| `pptx_umbral_indice_secciones` | 4 diapositivas de contenido | A partir de aquí el deck lleva diapositiva de índice |
| `ruta_logo_pptx_oscuro` | `assets/marca/480_Blanco.png` | Variante sobre fondo oscuro (portada y cierre) |
| `pptx_ancho_logo_portada_pulgadas` | 2,4" | — |
| `pptx_ancho_logo_contenido_pulgadas` | 0,7" | — |
| `pptx_ancho_logo_cierre_pulgadas` | 2,8" | — |

## Donde encaja: la cadena de montaje de vídeo (T-33)

Esta skill es el **paso previo limpio** de la skill de montaje con ffmpeg — no la sustituye ni graba nada, solo le deja preparado lo que necesita para no empezar de cero. El contrato completo, con ejemplos y las garantías exactas sobre orden y numeración de escenas, vive en `references/contrato-montaje.md`; aquí solo el resumen operativo.

De toda la carpeta de salida (`<nombre-guion><sufijo>/`, sufijo configurable en `config.NOMBRE_SUFIJO_CARPETA_SALIDA`, por defecto `-teleprompter` desde R-06 — antes `-tarjetas`, nombre heredado del proyecto anterior a renombrarlo), la fase de montaje solo necesita leer **dos archivos**:

- **`guion.srt`** — subtítulos borrador (T-27), un único archivo para el guion completo, ya validado con las mismas reglas que aplica un lector estricto tipo ffmpeg (índice secuencial, marca de tiempo bien formada, sin solapes). Los tiempos son **estimados** a partir del ritmo deducido del guion (T-12), no de una toma grabada real.
- **`guion-alineado.srt`** — mismo formato y misma validación, pero con los tiempos de cada escena ya reescalados a la duración real de su toma buena cuando existe (`.srt` alineado, R-05); una escena sin toma buena todavía conserva ahí su duración estimada. Archivo aparte, nunca sobrescribe a `guion.srt`.
- **`tarjetas.json`** — contrato de intercambio con la generación del `.pptx` (T-29, `references/contrato-tarjetas.md`), pero reutilizable por cualquier consumidor: trae `duracion_estimada_segundos` por escena en el mismo orden que el guion, con lo que la fase de montaje puede calcular el instante de inicio/fin de cada escena sumando duraciones (el `.srt` no lleva ninguna marca de escena en su propio texto).

**Nombres y orden de escenas, estables y predecibles (requisito 2 de T-33):** el `numero` de cada escena (`## BLOQUE N — <título>`) es la única clave para casar una toma grabada con su escena sin ambigüedad. Debe ser único y estrictamente creciente en el orden del documento — el mismo orden en que aparecen en `tarjetas.json` y en el que se generan los subtítulos del `.srt`. `convencion.detectar_desviaciones` (T-10, ampliada en T-33) señala `numero_escena_duplicado` y `numero_escena_no_creciente` sin bloquear el proceso; si aparecen, la cadena de montaje no debe fiarse del número de escena hasta corregir el guion de origen.

**Proyectos creados antes de R-06:** si un guion ya tenía una carpeta de salida con el sufijo antiguo `-tarjetas`, la primera vez que esta versión la vuelve a procesar la renombra sola a `-teleprompter` — sin perder `estado.json`, `guion-escenas.md` ni ningún otro archivo, y dejando antes una copia de seguridad completa (`<nombre-guion>-tarjetas.bak-<marca>`, junto a la carpeta) por si hiciera falta consultar el estado previo a la migración. No hace falta ningún paso manual del dueño ni de la skill de montaje.

**Ver también:** `references/contrato-montaje.md` (contrato completo, con la fórmula para derivar el rango de tiempo de cada escena) y `references/contrato-tarjetas.md` (forma exacta de `tarjetas.json`).

## Verificacion

```
python -m mypy                                 # tipos
python -m ruff check scripts/ tests/           # estilo
python -m pytest                               # tests
python scripts/verificar_salidas.py --fixture  # extremo a extremo + auto-contencion del HTML
```

Las herramientas son **solo de desarrollo** (`requirements-dev.txt`): la skill se ejecuta sin ellas.

**Ver también:** `references/validador-autocontencion.md` (lista completa de patrones que rechaza la comprobación de auto-contención, R-09) — consultarla antes de añadir a `assets/reproductor/` o `assets/pdf/` cualquier cosa que hable con una red.
