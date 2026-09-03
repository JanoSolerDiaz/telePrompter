# DEVELOPERS — teleprompter

> Notas para quien clone este repositorio y quiera trabajar en el código. No sustituye a
> `roadmap/SEGUIMIENTO.md` (el hub del proyecto): esto es solo lo mecánico de arrancar.

## Puesta en marcha

1. Requiere Python 3.12+.
2. Instala las herramientas de desarrollo (mypy, ruff, pytest). **Son solo de desarrollo**:
   la skill se ejecuta sin ellas, únicamente con la biblioteca estándar de Python 3.
   ```
   pip install -r requirements-dev.txt
   ```
3. Instala el hook de pre-commit (§0.1). No está en `.git/hooks/` tras clonar porque esa
   carpeta no se versiona; hay que instalarlo una vez por clon:
   ```
   python scripts/instalar_hooks.py
   ```
   A partir de ahí, cada `git commit` ejecuta la verificación completa (mypy, ruff, pytest,
   `verificar_salidas.py --fixture`) y aborta el commit si algo falla. Para saltarlo
   puntualmente: `git commit --no-verify` (bajo tu responsabilidad).

## CI local (T-04)

`scripts/ci.py` es el único sitio donde viven las cuatro verificaciones del protocolo
(antes duplicadas entre el hook y esta guía). El hook de pre-commit lo invoca; para
lanzarlas sueltas, sin pasar por un commit:
```
python scripts/ci.py
```
Ejecuta las cuatro etapas en orden y hasta el final aunque alguna falle, para que el
resumen final diga de una vez qué está roto y qué no; agrega el resultado en un único
código de salida (0 si las cuatro pasan, 1 si alguna falla).

No hay CI remota propia: el repositorio no tiene integración con un servicio externo.
Existe un workflow de GitHub Actions equivalente en `.github/workflows/ci.yml`
(`workflow_dispatch`, sin disparo automático en `push`/`pull_request`) preparado para el
día que el dueño decida activarlo sobre `origin/develop`; hasta entonces solo se lanza a
mano desde la pestaña "Actions" de GitHub.

## Verificación manual

Los mismos cuatro pasos que ejecuta `scripts/ci.py` (y, a través de él, el hook), por si
hace falta lanzarlos sueltos uno a uno:

```
python -m mypy scripts/ tests/
python -m ruff check scripts/ tests/
python -m pytest -q
python scripts/verificar_salidas.py --fixture
```

## Salida al usuario y diagnóstico (T-02)

Dos módulos, dos audiencias, ninguna se mezcla con la otra:

- `scripts/presentacion.py` — lo único autorizado a hablarle al dueño (mensajes en
  español sobre el resultado de la ejecución). `print()` fuera de este módulo está
  prohibido por lint (`ruff` regla `T20`).
- `scripts/logger.py` — diagnóstico técnico. `configurar_logger(carpeta_salida,
  verbose=...)` escribe siempre `<carpeta_salida>/teleprompter.log` en nivel DEBUG;
  `--verbose` solo decide si además se ve por stderr mientras el proceso corre. El
  archivo vive dentro de la carpeta de salida del guion (regla de aislamiento, §0.2),
  nunca fuera.

## Monitorización de errores (T-05)

`scripts/monitorizacion.py` es la red de seguridad ante fallos que el resto del
protocolo no cubre (no hay Sentry ni servicio externo: la regla de cero red aplica
también aquí). Dos piezas:

- `ejecutar_con_diagnostico(funcion, carpeta_salida)` — envuelve el punto de entrada
  real de la CLI. Si `funcion` lanza una excepción no controlada: vuelca tipo, mensaje
  y traceback a `<carpeta_salida>/diagnostico-<timestamp>.log` (nunca variables
  locales, para no arrastrar el contenido íntegro del guion al archivo), dejar
  constancia en el logger de T-02 y muestra al dueño un mensaje accionable genérico en
  español por `presentacion.py` — la traza técnica nunca llega a la consola del dueño.
  Devuelve un código de salida distinto de 0.
- `ResumenEjecucion` — dataclass con el recuento final que debe mostrarse al terminar
  sin errores: escenas procesadas, bloques, avisos, reescrituras y salidas generadas.

Como con el logger de T-02, todavía no hay un `main()` real que envolver (llega con
T-07 en adelante): esta tarea deja la mecánica lista y probada para que cada punto de
entrada futuro la use en vez de inventar su propio manejo de errores.

## Robustez de entrada (T-06)

`scripts/entrada.py` blinda la única puerta de entrada real (el `.md` del guion)
antes de que nada lo procese, delante del parser (`scripts/parser.py`, T-08):

- `validar_ruta_guion(ruta)` — existe, no es una carpeta, tamaño ≤
  `TAMANO_GUION_MAX_BYTES` (`config.py`). Devuelve la ruta resuelta.
- `leer_guion(ruta)` — lee validando la ruta, decodifica UTF-8 (con o sin BOM, vía
  `utf-8-sig`) y rechaza cualquier otra codificación o un contenido vacío/solo
  blancos, con un error accionable en vez de un `UnicodeDecodeError` crudo.
- `verificar_estructura_minima(texto)` — cuenta encabezados Markdown de **cualquier
  nivel** (no el patrón estricto de escena de `PATRON_ENCABEZADO_ESCENA`, a
  propósito: una entrada hostil podría evitarlo) y rechaza 0 encabezados o más de
  `ESCENAS_MAX`. No decide qué encabezado es escena — eso sigue siendo trabajo de
  T-08.
- `nombre_guion_seguro(ruta)` / `carpeta_salida_para(ruta)` — derivan
  `<carpeta-del-guion>/<nombre-guion>-tarjetas/` saneando el nombre (unicode NFC,
  sin separadores de ruta ni secuencias de puntos) y comprobando con
  `Path.relative_to` que el resultado nunca cae fuera de la carpeta del guion
  (regla de aislamiento, §0.2).
- `ejecutar_con_limite_de_tiempo(funcion, segundos=...)` — tope de tiempo con
  `ThreadPoolExecutor` en vez de `signal.alarm` (no existe en Windows, la máquina
  del dueño). Si se agota el tiempo, el proceso principal recupera el control de
  inmediato; el hilo huérfano no se puede matar desde Python.

Todos los fallos usan una única excepción, `EntradaError`, con el mensaje ya
accionable en español: el futuro `main()` (T-07 en adelante) solo tiene que
capturarla y mostrarla por `presentacion.py`, igual que hace ya
`ejecutar_con_diagnostico` (T-05) con cualquier otra excepción no controlada.

**Nota de entorno:** el `python` real de este contenedor es 3.11.15 pese a que
`pyproject.toml` fija `requires-python = ">=3.12"` (`python3.12` existe aparte, sin
usarse). Por eso `entrada.py` evita la sintaxis de generics de PEP 695
(`def f[T](...)`, que `ast.parse` de 3.11 ni siquiera analiza) y usa
`typing.TypeVar` clásico. Ver `DECISIONES_TECNICAS.md`, T-06.

## Estado del proyecto de guion (T-07)

`scripts/estado.py` da al proceso memoria entre sesiones: `estado.json`, dentro de la
carpeta de salida derivada del guion (`<carpeta-del-guion>/<nombre-guion>-tarjetas/`,
que deriva `entrada.carpeta_salida_para`). Piezas:

- `EstadoProyecto` (dataclass) — el contrato de datos: versión de esquema, `InfoGuion`
  (ruta, hash sha256, tamaño), configuración efectiva, `SeparadorEscena` (nivel/patrón
  elegidos por T-08, `None` hasta entonces), y los contenedores que T-08 en adelante
  rellenan (`escenas`, `reescrituras`, `validacion`, `salidas_generadas`), vacíos por
  ahora — mismo tratamiento que T-02/T-04/T-05: infraestructura sin productor de datos
  todavía.
- `estado_inicial(ruta_guion, configuracion)` — estado de partida para un guion sin
  `estado.json` previo.
- `guardar_estado(estado, carpeta_salida)` — escritura **atómica**: escribe a
  `estado.json.tmp` en la misma carpeta y hace `Path.replace()` (atómico en POSIX y
  Windows) sobre `estado.json`; si algo falla antes del reemplazo, el `estado.json`
  anterior queda intacto y el temporal se limpia. Así un proceso interrumpido a mitad
  de escritura y relanzado nunca encuentra un archivo a medias.
- `cargar_estado(carpeta_salida)` — lee `estado.json`, aplica las migraciones
  pendientes (ver abajo) y reconstruye `EstadoProyecto`. Cualquier fallo (archivo
  ausente, JSON corrupto, estructura incompleta) levanta `EstadoError` con mensaje ya
  accionable en español, mismo contrato que `EntradaError` (T-06).
- `guion_modificado(estado, ruta_guion)` / `avisar_si_guion_modificado(...)` — compara
  el hash guardado contra el hash actual del guion; si difiere, avisa por
  `presentacion.py` que la próxima pasada recalculará escenas, clasificación y tiempos
  (todavía no hay recálculo incremental).

**Migraciones (`scripts/migraciones/`).** Cada archivo `NNN_<nombre>.py` define
`VERSION_DESTINO: int` y `aplicar(datos: dict) -> dict`, debe ser idempotente y debe
**preservar** cualquier clave ya presente en `datos` (invariante (c) de §0.2: la
edición del dueño manda), completando solo lo que falte con valores por defecto.
`aplicar_migraciones` (en `migraciones/__init__.py`) descubre los archivos por el
prefijo numérico, los ordena y aplica en cadena los que falten según
`version_esquema` (0 si no existe). El prefijo numérico no es un identificador Python
válido, así que se cargan con `importlib.import_module` en vez de `import` (mismo
mecanismo que usa Django); `N999` de ruff está ignorado para esa carpeta a propósito
(ver `pyproject.toml`). La migración `001_estado_inicial.py` es la que establece el
esquema versión 1 por primera vez.

## Parser de escenas (T-08)

`scripts/parser.py` convierte el `.md` en escenas: `parsear_guion(texto)` es el punto
de entrada. Piezas:

- `dividir_en_bloques(texto)` — trocea el `.md` en un `Bloque` por encabezado (de
  cualquier nivel), más el preámbulo si lo hay, con la línea de inicio/fin sobre el
  texto original (trazabilidad). Ignora `#` dentro de vallas de código (` ``` `/`~~~`).
  Concatenar el `contenido` de todos los bloques, en orden, reconstruye el `.md` línea
  a línea sin pérdida.
- `elegir_separador(texto, configuracion)` — decide el nivel/patrón de escena
  (`estado.SeparadorEscena`). El nivel se deriva de los `#` iniciales de
  `PATRON_ENCABEZADO_ESCENA` (`config.py`), no está fijado a mano.
- `parsear_guion(texto, *, configuracion=None, separador=None)` — si `separador` ya
  trae `nivel`/`patrón` (una decisión persistida de una sesión anterior en
  `estado.json`, T-07), se usa tal cual sin volver a preguntar el nivel. Los
  conflictos de clasificación de un encabezado concreto **sí** se revisan siempre,
  persistido o no, porque dependen de `configuracion.secciones_auxiliares`, que puede
  cambiar entre pasadas sin que cambie el separador.
- `extraer_metadatos(texto)` — pares `**Clave:** valor` de la cabecera (duración
  objetivo, formato, promesa/idea única…), sin esquema fijo de claves: los tres
  guiones reales no usan las mismas.

**Clasificación de un encabezado del nivel elegido** (ni todo `##` es escena — ver el
docstring del módulo para el detalle completo):
1. Casa con el patrón → escena.
2. Si no: título en `secciones_auxiliares` (lista negra) y cuerpo con
   `**LOCUCIÓN**` **a la vez** → conflicto real, se levanta
   `DeteccionEscenasAmbiguaError` con las alternativas y sus consecuencias (nº de
   escenas, duración media) en vez de decidir en silencio (requisito 6 de T-08).
   Solo lista negra → auxiliar. Solo `**LOCUCIÓN**` → escena (señal secundaria).
   Ninguna de las dos → auxiliar (caso por defecto, mayoritario en los tres guiones
   reales: el subtítulo entrecomillado, por ejemplo).
3. Ningún encabezado del nivel esperado casa con el patrón → también
   `DeteccionEscenasAmbiguaError`, con una alternativa por nivel candidato (`#`, `##`,
   `###`).

Sin CLI todavía que capture la excepción y le pregunte de verdad al dueño (llega con
T-16/T-17): hoy la persistencia de la respuesta se demuestra en
`tests/test_parser.py::test_conflicto_de_senales_se_resuelve_ajustando_la_lista_negra`.

## Clasificador locución / no locución (T-09)

`scripts/clasificador.py` separa, dentro de cada escena ya parseada (T-08), el texto
que se recita del que no. Punto de entrada: `clasificar_guion(resultado_parseo,
configuracion)` clasifica el guion entero (preámbulo, secciones auxiliares y cada
escena) y devuelve `ResultadoClasificacion` (`bloques` + `resumenes` por escena,
requisito 7). Para una sola escena: `clasificar_escena(escena, configuracion)`.

**Señal primaria (ruta rápida), manda siempre que esté presente** (requisito 1):
el rótulo de sección — `Configuracion.rotulo_locucion`/`.rotulos_no_locucion`
(configurables, por defecto `**LOCUCIÓN**` frente a `**EN PANTALLA**`/`**NOTA**`).
Dentro de una sección `**LOCUCIÓN**`, el texto en cita de bloque (`> `) es
`locucion`; cualquier otro texto suelto en la misma sección se marca `revisar`
(requisito 3: es el caso ambiguo más probable en los guiones reales — una acotación
de ritmo entre dos citas, o un encargo de ejemplo fuera de cita).

**Señales de respaldo (inferencia)**, solo para texto sin rótulo activo (requisito
2): la propia cita de bloque (`> `) ya es señal suficiente de locución sin
necesidad del rótulo — es la misma convención ("recitable... en cita de bloque").
El resto: marca de tiempo, acotación entre paréntesis/corchetes, prefijo
(`PANTALLA:`, `B-ROLL:`, `NOTA:`, `IMAGEN:`, `TÍTULO:`), mayúsculas, negrita/cursiva
de línea completa, viñeta de checklist, tabla, enlace suelto, encabezado interno,
bloque de código. Sin señal clara → `revisar`, nunca se decide en silencio
(requisito 5).

Cada `BloqueClasificado` lleva `tipo` (`locucion`/`no_locucion`/`revisar`),
`motivo`, `senal` y su rango de líneas 1-indexado sobre el `.md` original
(requisito 4). Cobertura total (invariante (a) de §0.2, requisito 6):
`reconstruir(bloques)`, ordenados por `linea_inicio` y unidos con `\n`, reproduce
el `.md` de origen sin pérdida — igual que `dividir_en_bloques` en T-08, pero
también dentro de cada escena.

**Trampa de `str.splitlines()` con contenido ya unido por `"\n".join(...)`:** si la
última "línea" es una cadena vacía (una línea en blanco real justo antes del
siguiente encabezado — frecuente entre escenas, antes del `---`),
`"a\nb\n".splitlines()` devuelve `["a", "b"]` y esa línea en blanco desaparece.
`clasificador.py` usa `.split("\n")` en su lugar (el inverso exacto de ese
`join`) al re-trocear `escena.contenido`/`resultado.preambulo`; cualquier código
nuevo que vuelva a partir en líneas un `contenido` ya construido por T-08/T-09
debe hacer lo mismo, no asumir que `.splitlines()` es intercambiable.

## Convención de guiones (T-10)

`scripts/convencion.py` no descubre la convención (T-08/T-09 ya la implementan) ni
decide si adoptarla (el dueño ya lo hizo: contractual, con aviso — §6 pregunta 3 de
SEGUIMIENTO, §0.2 de HOJA_DE_RUTA). Formaliza tres cosas:

- **Documento para el guionista:** `generar_convencion_guiones(configuracion)` produce
  el texto de `convencion-guiones.md` (una página, generado a partir de
  `Configuracion` para no mantener un segundo texto a mano); `guardar_convencion_guiones
  (carpeta_salida, configuracion)` lo escribe en la carpeta de salida. Es un documento
  generado, no uno del dueño: no lleva copia `.bak` al regenerarse (esa regla es para
  `guion-escenas.md`, T-17).
- **Desviaciones de la convención (requisito 5), sin bloquear nunca el proceso:**
  `detectar_desviaciones(resultado_parseo, resultado_clasificacion, configuracion)`
  señala escena sin rótulo `**LOCUCIÓN**`, rótulo desconocido (una línea con forma
  `**Algo**` que no es ninguno de los rótulos configurados) y sección auxiliar no
  reconocida (un encabezado del nivel separador que no es escena ni está en
  `secciones_auxiliares`). El subtítulo entrecomillado justo tras el título del guión
  (evidencia de T-08: `# Título` + `## "Subtítulo"`) se reconoce como categoría
  auxiliar conocida por posición — es el primer encabezado del nivel separador de todo
  el guion —, no como desviación cada vez.
- **Consistencia y propuesta de convención explícita (requisitos 1-2):**
  `medir_consistencia_senales(resultados)` agrega cuántas veces aparece cada `senal` de
  `BloqueClasificado` (T-09) y si siempre decide el mismo tipo; acepta una lista para
  poder sumar el guion actual con el histórico de guiones ya procesados, sin que este
  módulo tenga que inventar su propio almacén de histórico — quien llama decide qué
  resultados anteriores pasar. `proponer_convenciones(consistencias, configuracion)`
  propone adoptar como convención explícita cada señal de inferencia 100% consistente
  que no sea ya contractual (`rotulo`, `cita_bloque`, `rotulo_no_locucion`,
  `encabezado`, `seccion_auxiliar`, `preambulo`, `blank`, `seccion_vacia`), con ejemplo
  antes/después y el ahorro que supondría. Sobre los tres guiones reales no genera
  ninguna propuesta: ya se clasifican enteros por la ruta rápida de rótulo, sin
  apoyarse en ninguna señal de inferencia de contenido — verificado por test.

## Troceo en bloques de respiración (T-11)

`scripts/troceo.py` parte cada bloque `locucion` ya clasificado (T-09) en fragmentos
de `palabras_por_bloque_min`-`palabras_por_bloque_max` palabras (`config.py`).

- **Cortar por prioridad (requisito 1):** `_refinar` desciende por cuatro niveles —
  puntuación fuerte (`.?!;:`) → débil (`,`, guion, apertura de paréntesis/interrogación)
  → nexos (`y`, `o`, `pero`, `que`, `porque`, `aunque`, `mientras`) → sintagma (antes de
  preposición o determinante) — y solo baja de nivel cuando el anterior no basta para
  caber en el máximo. **Gotcha real, encontrado contra los tres guiones reales:** el
  primer diseño abandonaba un nivel entero (volcando *todo* el resto del párrafo al
  siguiente nivel) en cuanto no encontraba un candidato dentro de la ventana de tamaño
  máximo desde el cursor actual — bastaba una sola oración larga sin puntuación fuerte
  cercana para que el resto de un párrafo de 100+ palabras cayera entero en corte
  forzado. La corrección: si no hay candidato *dentro* de la ventana, se usa el
  candidato más cercano *por delante* (aceptando un tramo de sobra que se refina con el
  siguiente nivel) y se sigue procesando el resto del texto con el mismo nivel, en vez
  de rendirse para todo lo que queda.
- **Nunca corta cifras, fechas ni siglas (requisito 2):** `_gaps_protegidos` marca como
  no cortables los huecos que caen dentro de un patrón de fecha (`15 de marzo de 2026`),
  número con unidad pegada tras un espacio (`1.500 €`) o sigla puenteada
  (`E. E. U. U.`). No hay overlap con T-13 (normalización a forma dicha) todavía: esa
  tarea no existe, así que no hay "expresión normalizada por T-13" que proteger aún.
- **Fusión de tramos cortos (requisito 3):** `_fusionar_bajo_minimo` funde cada tramo
  por debajo del mínimo con el vecino que deja el resultado más cerca del objetivo,
  priorizando no pasarse del máximo pudiendo evitarlo. Si la unión sí supera el máximo,
  `_dividir_fusion` la reparte en dos usando la misma jerarquía de prioridad en vez de
  dejar un bloque de más de `palabras_por_bloque_max` palabras — sin esto, sobre los
  tres guiones reales solo el 88.6% de los bloques quedaba en rango (por debajo del 90%
  del criterio de aceptación); con el reparto, el 100%.
- **`trocear_bloque_locucion`** quita la marca de cita (`> `) antes de trocear: contar
  palabras sobre `bloque.contenido` tal cual (como hace `bloque.contenido.split()`)
  cuenta el propio `>` de cada línea como una palabra más, inflando cualquier recuento
  de palabras de locución que se compare contra el troceo (ver el mismo cuidado que
  T-09 tuvo con `.split("\n")` frente a `.splitlines()`, más arriba).
- **`trocear_guion`** reclasifica escena a escena con `clasificador.clasificar_escena`
  en vez de recibir un `ResultadoClasificacion` ya construido: `BloqueClasificado` no
  lleva el número de escena (esa granularidad vive en `Escena`), así que reclasificar
  evita añadir un campo a T-09 solo para este caso.

## Motor de tiempos (T-12)

`scripts/tiempos.py::calcular_tiempos` es la única función que calcula tiempos
(requisito 4): informe, cabecera de `guion-escenas.md` (T-16), `.srt` (T-27) y
reproductor (T-18+) deben consumir su resultado (`ResultadoTiempos`), nunca
recalcular por su cuenta.

- **Dos semánticas distintas para el mismo patrón `(m:ss – m:ss)` — el punto más
  delicado de esta tarea.** El rango horario de un encabezado de escena
  (`## BLOQUE 4 — ... (1:55 – 3:10)`) son dos **marcas de tiempo del vídeo**: la
  escena dura `3:10 − 1:55 = 75s`, no "162s de media entre los dos instantes". El
  metadato de cabecera `**Duración objetivo:**` (`3:40 – 3:55`), en cambio, sí es
  una **horquilla real de duración total**. Un primer diseño trató ambos igual
  (tomando el punto medio del par), lo que deducía un ppm de ~40 en los tres
  guiones reales (muy fuera de la banda `[90, 180]`) simplemente porque sumaba
  marcas de tiempo como si fueran duraciones — ver la fila de T-12 en
  `DECISIONES_TECNICAS.md`. `parser.rango_segundos_titulo` (renombrada desde la
  privada `_rango_segundos` de T-08) devuelve el par crudo en ambos casos; quien
  llama decide qué hacer con él: `_duracion_objetivo_escena` resta los dos
  extremos, `_duracion_objetivo_metadato` deja el par tal cual.
- **Ritmo deducido (requisitos 1, 7, 8):** ppm único para todo el guion —
  `palabras_totales / (suma_de_duraciones_por_escena / 60)` — con respaldo a
  `ppm_respaldo` (120) si falta la duración objetivo de alguna escena o el valor
  cae fuera de `ppm_banda_plausible`. `RitmoAplicado` siempre lleva `origen`
  (`deducido`/`respaldo`/`manual`), `ppm_deducido` (aunque se descarte) y
  `ppm_alternativo` (el otro valor, para forzarlo a mano). `Configuracion.ppm_manual`
  (requisito 8) tiene prioridad sobre ambos; se persiste solo porque ya viaja en
  `configuracion_efectiva` dentro de `estado.json` (T-07), sin mecanismo nuevo.
- **Pausas por bloque (requisito 2):** `coma < punto < fin_parrafo < fin_escena`
  (`config.py`). "Fin de párrafo"/"fin de escena" se deciden por posición (último
  bloque de respiración de un `BloqueClasificado` de T-09, o de toda la escena),
  no por puntuación, y sustituyen a la pausa por puntuación cuando aplican
  (nunca se suman). `_bloques_respiracion_marcados` reclasifica escena a escena
  con `clasificador.clasificar_escena` en vez de ampliar `BloqueRespiracion`
  (T-11) con estos dos booleanos — mismo patrón que ya usó T-11 con T-09.
  `troceo.categoria_puntuacion_final` (nueva función pública) reutiliza los
  conjuntos de puntuación que ya tenía T-11 para decidir el corte.
- **Agregados sin descuadre (requisitos 3, 4):** un único `cursor_segundos` que se
  acumula bloque a bloque; la duración de una escena es la diferencia del cursor
  antes/después de sus bloques, así que escena y total telescopan exactamente,
  sin recalcular ni redondear en un paso aparte.
- **Contraste (requisito 6):** por escena, contra la duración objetivo de esa
  escena; en total, contra el metadato `**Duración objetivo:**` si está presente,
  o si no contra la suma de las duraciones por escena (par degenerado
  `(suma, suma)` para que el tipo del campo no cambie según el origen). Avisa
  cuando la desviación relativa supera `umbral_desviacion_tiempos`, con cuántas
  palabras sobran o faltan al ritmo aplicado.

## Normalización a forma dicha (T-13)

`scripts/normalizacion.py::normalizar_texto` detecta y propone la forma dicha
de un texto **sin modificarlo**: devuelve una lista de `Normalizacion`
(`original`, `propuesta`, `familia`, `motivo`, `inicio`, `fin`), nunca un
texto ya sustituido. `aplicar_normalizaciones`/`deshacer_normalizaciones` son
inversas exactas entre sí (invariante (b), original siempre recuperable) y
son las que usan los tests y el informe para previsualizar.

- **Orden de prioridad estricto, no una única regex.** Cada familia de regla
  (diccionario del dueño → moneda → porcentaje → unidad → rango → fracción →
  ordinal → cardinal → sigla → símbolo suelto → conjunción) se procesa en ese
  orden contra el texto completo, marcando cada tramo ya resuelto en un
  `bytearray` de "ocupado" para que ninguna familia posterior lo reinterprete.
  El diccionario del dueño (requisito 3) va primero siempre: cualquier entrada
  literal en `diccionario-locucion.json` gana a cualquier regla automática.
- **Apócope y concordancia de género solo con sustantivo detrás.** `"21"` a
  final de frase se lee "veintiuno"; `"21 alumnos"` se lee "veintiún alumnos"
  (apócope) y `"21 personas"` se lee "veintiuna" (concordancia femenina). La
  decisión mira la palabra que sigue inmediatamente al número en el propio
  texto (`_siguiente_palabra`), no el dígito final en solitario.
- **Género por heurística de sufijo, no un diccionario morfológico completo.**
  `_genero_por_sustantivo` usa terminaciones (`-a`, `-ción`, `-dad`...) más una
  lista corta de excepciones frecuentes (`día`, `mano`, `foto`...); por
  defecto masculino si no reconoce el sufijo. Deliberadamente no exhaustiva:
  el diccionario del dueño corrige cualquier fallo puntual sin tocar código.
- **Siglas: deletreo letra a letra por defecto** (`SVG` → "ese uve ge",
  `deletrear_sigla`), nunca se "adivina" si suena mejor como palabra. El dueño
  fija una lectura distinta (deletreada de otra forma, leída como palabra, o
  expandida) con una entrada literal en el diccionario.
- **Conjunciones "y"/"e", "o"/"u"** (`_PATRON_CONJUNCION`): regla estándar del
  español ante sonido /i/ u /o/, con la excepción del diptongo `hie-`/`hia-`
  (`"nieve y hielo"` no cambia). Independiente de las cifras, mismo mecanismo
  de "ocupado" para no pisar una normalización ya resuelta.
- **`normalizar_guion` opera sobre `BloqueRespiracion` (T-11) ya trozado, no
  antes del troceo.** El requisito 2 de T-11 pide no cortar "una expresión
  normalizada por T-13"; normalizar después de trocear evita el problema por
  construcción, porque los límites de bloque ya son estables cuando se
  normaliza. Un resultado (`ResultadoNormalizacionBloque`) por bloque, incluso
  sin normalizaciones propuestas (cobertura total, invariante (a)).
- **`SIMBOLOS_MONEDA`/`UNIDADES_ABREVIADAS` en `config.py` son diccionarios
  planos**, no campos de `Configuracion`: el diccionario de excepciones ya
  cubre la sobreescritura por el dueño entrada a entrada, así que espejarlas
  en el dataclass congelado (con la vuelta a tuplas de pares que exigiría la
  hashabilidad) habría sido una complicación de tipos sin caso de uso real.
- **Alcance deliberadamente acotado** (documentado en el docstring del módulo
  y en `DECISIONES_TECNICAS.md`): ordinales del 1º al 10º; `/` solo se lee
  dentro de una fracción dígito/dígito, nunca suelto (ambiguo: URLs,
  "y/o"...); convención hispana consciente para números (`.` = millar, `,` =
  decimal), la misma que usan los ejemplos del criterio de aceptación.

## Detector de problemas de lectura en voz alta (T-14)

`scripts/deteccion.py::detectar_problemas_bloque`/`detectar_problemas_guion`
avisan de lo que va a costar decir, sobre `BloqueRespiracion` (T-11) ya
trozado, **sin modificar nada**: devuelven `Aviso` (`familia`, `severidad`,
`mensaje`, `recomendacion`, `fragmento`) envueltos en
`ResultadoDeteccionBloque` (un resultado por bloque, cobertura total,
invariante (a)).

- **Cinco familias, una por requisito.** `sin_punto_respiracion` (frase larga
  sin puntuación intermedia), `cacofonia` ("de" encadenados, sílaba inicial
  repetida, rima involuntaria), `trabalenguas` (grupo de consonantes seguidas,
  o varias palabras largas seguidas), `anglicismo` (tabla
  `ANGLICISMOS_COMUNES` en `config.py`) y `estructura_dificil` (incisos
  acumulados, subordinadas encadenadas, doble negación, voz pasiva larga).
- **Ninguna familia reescribe, salvo una excepción parcial.** Solo
  `sin_punto_respiracion` marca `admite_particion=True` y adjunta
  `particion_sugerida` (una tupla de dos mitades de texto, partiendo por el
  nexo subordinante más cercano al centro o, si no hay ninguno, por el centro
  exacto): es la única familia que "afecta al troceo" (requisito 6 de T-14).
  Aplicar esa partición de verdad es alcance de T-15, no de este detector.
- **Heurísticas de caracteres, no un analizador lingüístico real** (mismo
  espíritu que el género por sufijo de T-13): "sílaba repetida" es un prefijo
  compartido de `longitud_silaba_comparada` caracteres entre palabras
  adyacentes; "rima" es un sufijo compartido entre palabras de al menos
  `longitud_minima_palabra_rima` caracteres dentro de una ventana; "trabalenguas"
  es un grupo de `consonantes_seguidas_dificil` consonantes seguidas dentro de
  una palabra, o `palabras_dificiles_seguidas_minimas` palabras de
  `longitud_palabra_dificil`+ caracteres en fila. Todas configurables en
  `Configuracion` (`config.py`), con validación de que sean enteros positivos.
- **`ANGLICISMOS_COMUNES` es un diccionario plano de módulo**, no un campo de
  `Configuracion`, mismo razonamiento que `SIMBOLOS_MONEDA`/`UNIDADES_ABREVIADAS`
  en T-13 (tabla completa sin caso de uso real que la exija por entrada).
- **La localización (escena/bloque) vive en `ResultadoDeteccionBloque.bloque`**
  (`numero_escena`, `linea_inicio`, `linea_fin` de `BloqueRespiracion`), no
  duplicada dentro de `Aviso`; mismo patrón que `ResultadoNormalizacionBloque`
  de T-13. El volcado al `.md` anotado es tarea de T-16 (`guion-escenas.md`),
  que no existe todavía: T-14 deja los datos listos, no genera el documento.

## Reescrituras marcadas, aceptables y reversibles (T-15)

`scripts/reescrituras.py` une las dos fuentes de propuesta que ya existían
-- `normalizacion.Normalizacion` (T-13) y `deteccion.Aviso.particion_sugerida`
(T-14, única familia con `admite_particion=True`) -- en un tipo único,
`Reescritura`, con ciclo de vida completo: proponer, marcar en texto legible,
leer la decisión escrita a mano, aplicarla o no, y deshacerla en bloque.

- **`recopilar_propuestas(resultados_normalizacion, resultados_deteccion)`**
  construye la lista de `Reescritura` a partir de los resultados de T-13/T-14
  ya calculados; solo la familia `sin_punto_respiracion` de T-14 produce una
  `Reescritura` (familia `particion_respiracion`), el resto de avisos de T-14
  se ignoran aquí a propósito (alcance de T-15, §0.2: solo forma dicha y
  respiración).
- **Identidad estable, no por contenido.** `Reescritura.id` es un hash de
  `(numero_escena, linea_inicio, linea_fin, familia, inicio, fin, original)`
  -- la ocasión concreta, no la propuesta -- para que revalidar con una regla
  mejorada siga reconociendo "la misma" reescritura (requisito 4) aunque la
  `propuesta` sugerida cambie de texto.
- **Formato marcado (`formatear_reescritura`/`extraer_decisiones`).** Un
  bloque delimitado por `<!-- reescritura id=... --> ... <!-- /reescritura -->`
  con `Original`/`Propuesta`/`Motivo`/`Decisión` visibles a la vez. La marca
  de decisión es una sola palabra (`PENDIENTE`/`ACEPTAR`/`RECHAZAR`) que el
  dueño sobrescribe a mano; `extraer_decisiones` la localiza con
  `Decisi[oó]n\W*(ACEPTAR|RECHAZAR|PENDIENTE)` (cualquier no-palabra entre
  "Decisión" y la marca: cubre `:`, `**` de negrita Markdown y espacios de
  más, sin depender de una columna exacta). Es el bloque que insertará T-16
  dentro de cada escena de `guion-escenas.md`, no el documento entero --
  mismo patrón de infraestructura sin consumidor final todavía que ya
  aplicaron T-02/T-04/T-05/T-07.
- **Persistencia append-only (`fusionar_con_estado`/`guardar_en_estado`).**
  `fusionar_con_estado` combina las propuestas recién calculadas con
  `estado.reescrituras` ya guardado: una propuesta con `id` ya presente
  conserva su decisión (no se vuelve a mostrar como pendiente); una nueva se
  añade como `pendiente`; una que ya no se genera (el guion cambió) se
  conserva igualmente al final de la lista, nunca desaparece.
- **Aplicación sobre el texto (`texto_con_reescrituras_aceptadas`).** Solo
  las reescrituras `aceptada` de un bloque se aplican (reconstruye
  `Normalizacion` a partir de la `Reescritura` y reutiliza
  `normalizacion.aplicar_normalizaciones`); `pendiente`/`rechazada` dejan el
  original intacto.
- **Materializar una partición aceptada
  (`aplicar_particion_aceptada`/`aplicar_particiones_aceptadas`).** T-14 dejó
  dicho que "aplicarla de verdad" era alcance de T-15: esta función sustituye,
  dentro de una lista de `BloqueRespiracion`, el bloque cuyo texto coincide
  exactamente con el `original` de la reescritura por los dos bloques
  resultantes de partirlo. Ambos heredan `numero_escena`/`linea_inicio`/
  `linea_fin`/`corte_forzado` del bloque de origen (T-11 no trackea posición
  más fina que el bloque, y esta partición no vuelve a pasar por el algoritmo
  de corte de T-11).
- **Deshacer global (`revertir_reescrituras`).** Fuerza a `rechazada` todas
  las reescrituras, o solo las de una escena si se pasa `numero_escena`, sin
  tocar `original` (invariante (b): sigue disponible aunque se revierta).
- **Sin migración de `estado.json`.** El contenedor `reescrituras: list[dict]`
  ya existía desde T-07; esta tarea solo fija la forma de esos `dict`
  (`asdict(Reescritura)`), sin tocar el esquema ni su versión.

## Documento de revisión de una sola pasada (T-16)

`scripts/documento_revision.py` compone `guion-escenas.md`: el documento que el
dueño revisa entero, de una sentada, en cualquier editor de texto plano. No
recalcula nada por su cuenta -- toma los resultados que ya calcularon T-08 a
T-15 (`ResultadoParseo`, `ResultadoTiempos`, `list[ResultadoDeteccionBloque]`,
`list[Reescritura]`) y los compone, el mismo patrón que ya sigue
`reescrituras.recopilar_propuestas` con `normalizar_guion`/
`detectar_problemas_guion`.

- **`generar_documento_revision(...)`** es el punto de entrada: cabecera con
  instrucciones y resumen global (requisito 5), y una sección por escena en
  orden, reproduciendo el mismo encabezado `## BLOQUE N — <título>` del guion
  de origen.
- **Bloques de respiración numerados y anclados
  (`formatear_bloque_respiracion`).** Cada bloque de `ResultadoTiempos.bloques`
  (T-12) se numera desde 1 dentro de su escena y se delimita con
  `<!-- bloque escena=N indice=K --> ... <!-- /bloque -->` -- la misma idea que
  el ancla `<!-- reescritura id=... -->` de T-15 -- para que una edición a mano
  del texto siga siendo localizable por `extraer_texto_bloques` sin depender de
  columna ni indentación (requisito 7). `extraer_texto_bloques` descarta la
  cabecera `**Bloque N** (...)` y cualquier reescritura o aviso incrustado,
  dejando solo el texto (editado o no) para una futura revalidación (T-17).
- **Reescrituras y avisos localizados junto a su bloque (requisito 3).** Una
  `Reescritura` se asocia a su `BloqueRespiracion` exacto comprobando
  `bloque.texto[reescritura.inicio:reescritura.fin] == reescritura.original`
  -- no solo el rango de líneas, porque varios bloques de respiración pueden
  compartir `linea_inicio`/`linea_fin` (T-11 no trackea posición más fina que
  el párrafo de origen). Un aviso de la familia `sin_punto_respiracion` con
  partición sugerida NO se repite como aviso plano: ya se muestra como la
  `Reescritura` de familia `particion_respiracion` que generó T-15, y
  mostrarlo dos veces sería redundante.
- **Indicaciones no recitables al pie de cada escena
  (`_indicaciones_no_recitables`/`formatear_indicaciones`, requisito 4).**
  Todo lo que T-09 clasificó como `no_locucion` o `revisar` dentro del rango de
  líneas de la escena, con su motivo, salvo el propio encabezado de escena, el
  rótulo suelto (`**EN PANTALLA**` sin cuerpo) y las líneas en blanco --ya
  visibles en otro sitio del documento y sin nada que revisar. Los extractos
  largos se truncan a `Configuracion.longitud_extracto_indicacion_max`.
- **Marca de estado de la revisión completa
  (`extraer_estado_revision`, requisito 6).** Mismo mecanismo que la marca de
  decisión de T-15 -- una sola palabra (`PENDIENTE`/`VALIDADO`) que el dueño
  sobrescribe a mano sobre la línea "Estado de la revisión", leída con
  `Estado de la revisi[oó]n\W*(PENDIENTE|VALIDADO)` -- para que T-17 sepa
  cuándo el dueño considera terminada la pasada. Sin marca reconocible se
  asume `PENDIENTE`: nunca se da una revisión por validada en silencio.
- **`guardar_documento_revision`.** Escribe `guion-escenas.md` en la carpeta de
  salida; si ya existía una versión previa, la copia antes a
  `<nombre>.bak-<marca_de_tiempo>` (invariante (d) de §0.2, sin borrado
  destructivo). No es la escritura atómica de `estado.json` (T-07): aquí lo que
  protege el trabajo del dueño es la copia de seguridad, no que un corte a
  mitad de escritura sea imposible.
- **Sin punto de entrada de CLI todavía.** Igual que T-02/T-04/T-05/T-07/T-15
  en su momento: esta tarea entrega el generador, no quien lo invoca sobre un
  guion real de principio a fin (eso llega con T-30, el selector de salidas).

## Revalidación: releer, respetar y recalcular (T-17)

`scripts/revalidacion.py` cierra el ciclo iterable que T-16 dejó preparado --
validar, pedir cambios, revalidar -- sin perder nunca un ajuste anterior.
`revalidar_guion(resultado, texto_documento, estado, configuracion=None,
diccionario=None)` es el único punto de entrada: relee `guion-escenas.md` con
las mismas funciones de lectura de T-15/T-16 (`extraer_decisiones`,
`extraer_texto_bloques`, `extraer_estado_revision`, ninguna nueva) y devuelve
un `ResultadoRevalidacion` (tiempos, detecciones, reescrituras e incidencias
recalculados) sin tocar el disco por su cuenta -- quien orqueste la sesión
decide cuándo llamar a `estado.guardar_estado` y a
`documento_revision.generar_documento_revision`/`guardar_documento_revision`
para el siguiente ciclo.

- **Identidad estable entre pasadas, no por número de ancla.** El ancla
  `escena=N indice=K` que ve el documento no es identidad fiable: aceptar una
  partición en la misma pasada cambia cuántos bloques tiene esa escena, así
  que el ancla K de un bloque posterior deja de apuntar a lo mismo. Cada
  bloque "de origen" (antes de cualquier partición) aporta su índice 0-based
  dentro de la escena -- estable mientras el `.md` de entrada no cambie,
  porque `trocear_texto` es determinista -- y una partición aceptada reparte
  ese índice en dos mitades (`'a'`/`'b'`, `_materializar_marcados`). Esa
  tripleta `(numero_escena, indice_original, mitad)` es la clave que usa todo
  el módulo para no confundir bloques entre pasadas.
- **Edición manual: se detecta, nunca se registra aparte.** Para cada ancla
  del documento leído, se compara su texto contra el que el sistema
  derivaría (guion de origen + decisiones ya guardadas en `estado.json` al
  empezar la pasada, ver `_texto_derivado`). Si difieren, es una edición real
  y se preserva verbatim en el resultado final (invariante (c), §0.2); si no,
  se usa el texto derivado con las decisiones más recientes ya aplicadas. No
  hay ningún campo en `estado.json` que diga "esto lo editó el dueño": la
  comparación es correcta por construcción en cualquier pasada futura,
  porque el guion de origen no cambia y las decisiones sí están persistidas.
- **Decisiones: se leen del documento y se funden con el historial.**
  `reescrituras.fusionar_con_estado` (T-15) trae el historial de
  `estado.reescrituras` tal cual; `reescrituras.aplicar_decisiones` superpone
  las marcas (`ACEPTAR`/`RECHAZAR`) que trae el documento leído. Ninguna
  decisión ya tomada se pierde ni vuelve a proponerse como pendiente
  (invariante (b)); ninguna función nueva de persistencia, las dos ya
  existían en T-15.
- **Informe de incidencias (`Incidencia`, requisito 3): solo lo roto.**
  Bloques fuera de `[palabras_por_bloque_min, palabras_por_bloque_max]`,
  escenas sin ningún bloque de respiración, marcas de decisión sobre un `id`
  de reescritura que ya no existe, texto de locución que contiene un rótulo
  del guion (`**LOCUCIÓN**`/`**EN PANTALLA**`/`**NOTA**`, señal de que una
  indicación se coló dentro de un bloque editado a mano) y los avisos de
  desviación de duración que ya calcula T-12 (`TiempoEscena.aviso`,
  `ResultadoTiempos.aviso_total`). Nada de repetir una escena o un bloque que
  ya está bien.
- **`tiempos.calcular_tiempos_desde_marcados`, el hueco que le faltaba a
  T-12.** `calcular_tiempos` (T-12) siempre reconstruía sus bloques
  reclasificando el `ResultadoParseo` original -- no había forma de pasarle
  bloques ya materializados/editados. Se extrajo el núcleo de cálculo
  (ritmo, pausas, agregados) a esta nueva función, parametrizada por
  `marcados_por_escena` en vez de derivarlo siempre; `calcular_tiempos` sigue
  siendo la única fuente de tiempos sobre el guion sin editar, ahora como un
  envoltorio de dos líneas alrededor del mismo núcleo. Sin cambio de
  comportamiento (ver `tests/test_tiempos.py`, sin tocar).
- **Límite de alcance aceptado, no un bug.** Si un mismo bloque de origen
  tiene a la vez una normalización (T-13) y una partición (T-14/T-15)
  aceptadas, la normalización no se materializa en ninguna de las dos
  mitades: sus offsets se calcularon sobre el bloque entero, y el guardián
  `bloque.texto[inicio:fin] == original` (mismo patrón que
  `documento_revision._reescrituras_de_bloque`) la excluye correctamente en
  vez de aplicarla mal. La decisión sigue intacta en `estado.json`
  (invariante (b)); solo no se aplica en ese cruce concreto. Ver la fila de
  T-17 en `DECISIONES_TECNICAS.md`.
- **Edición manual + partición aceptada en la MISMA pasada: sí era un bug
  (hallazgo #9, corregido por P-02).** La identidad de una edición manual se
  calcula ANTES de aplicar las decisiones que trae el propio documento
  (`identidad_por_ancla`, sobre `reescrituras_previas`); si esa misma pasada
  acepta una partición sobre el bloque editado, la identidad con la que se
  guardó la edición (`indice_original`, `None`) deja de existir tras
  materializar la partición (`indice_original`, `'a'`/`'b'`) y la búsqueda
  posterior fallaba en silencio. `_materializar_marcados` acepta ahora
  `indices_con_edicion_previa_a_particion`: para esos índices NO aplica la
  partición esa pasada (la decisión de aceptarla se conserva en
  `estado.reescrituras`, solo se pospone su materialización), y
  `_incidencias_conflicto_edicion_particion` deja constancia en el informe.
- **La posposición debe persistir entre pasadas, o la siguiente revalidación
  duplica contenido (hallazgo #14, corregido por P-03).** El límite que P-02
  dejó documentado ("revalidación posterior sin tocar el bloque, sin nuevo
  test") resultó ser más grave de lo que su propia nota describía: sin
  memoria de la posposición, la pasada SIGUIENTE recalculaba
  `identidad_por_ancla` asumiendo que la partición aceptada YA estaba
  materializada (dos anclas `'a'`/`'b'`) mientras el documento en disco
  seguía teniendo una sola ancla (`None`, sin partir) -- el desajuste de
  esquema atribuía el texto editado a la mitad `'a'` y el texto del bloque
  SIGUIENTE de la escena a la mitad `'b'`, duplicando contenido sin ningún
  aviso. `_particiones_pospuestas_previas`/`_guardar_particiones_pospuestas`
  cierran el hueco: `estado.validacion["particiones_pospuestas"]` (contenedor
  genérico ya reservado desde T-07, sin migración -- mismo patrón que
  `estado.salidas_generadas` en T-30) guarda, al final de cada pasada, qué
  índices de bloque quedaron pospuestos; la siguiente pasada usa ESE mismo
  conjunto para calcular `identidad_por_ancla`, así que el esquema de anclas
  con el que se interpreta el documento siempre coincide con el que tenía
  cuando se escribió. Consecuencia deliberada: mientras la edición manual
  siga en el documento, la partición queda pospuesta indefinidamente (nunca
  se pierde ni se duplica nada); solo se materializa cuando el texto del
  ancla vuelve a coincidir exactamente con lo que el sistema derivaría --
  ver `test_particion_pospuesta_se_materializa_cuando_se_retira_la_edicion`
  en `tests/test_revalidacion.py`, complementario de
  `test_revalidacion_posterior_al_conflicto_no_duplica_bloques` (reproduce
  #14 exactamente y confirma que ya no duplica). Ver la fila de P-03 en
  `DECISIONES_TECNICAS.md`.
- **Endurecimiento de ese cierre (P-04).** El mecanismo de P-03 es correcto;
  P-04 tapa tres grietas alrededor. (1) `_particiones_pospuestas_previas` lee
  un contenedor genérico que nadie valida al cargar, así que un `estado.json`
  con basura en `particiones_pospuestas` tiraba la revalidación entera con
  `AttributeError`/`ValueError`; ahora la entrada ilegible se ignora y la
  pasada la recalcula. (2) Se persistía el conjunto **sin filtrar** de bloques
  con edición manual, no el de particiones realmente pospuestas: mismo
  resultado al materializar (`_materializar_marcados` ignora un índice sin
  partición) pero `estado.json` acumulaba índices que nunca tuvieron nada que
  posponer; `_indices_con_particion_pospuesta` lo acota y lo comparte con la
  incidencia, que antes lo recalculaba. (3) `_incidencias_anclas_desajustadas`
  es la red que faltaba: si las anclas leídas no son las previstas, avisa en
  vez de emparejar a ciegas. Importa porque un `estado.json` anterior a P-03
  **sin** la clave, justo en mitad de un conflicto, reproduce el #14 tal cual;
  con el aviso, deja de ser silencioso. Y el mensaje del conflicto deja de
  invitar a "revalidar sin tocar ese bloque" para que la partición se
  materialice: eso es exactamente lo que **no** funciona -- lo materializa
  retirar la edición, como demuestra el propio test de P-03 --, y un aviso que
  promete algo que no ocurre enseña a ignorar el informe. Ver las filas de
  P-04 en `DECISIONES_TECNICAS.md`.

## Reproductor: esqueleto autocontenido (T-18)

`scripts/reproductor.py` genera el artefacto principal de la skill: un único
`.html` que abre con doble clic, offline. No calcula nada por su cuenta --
toma un `ResultadoParseo` (T-08) y un `ResultadoTiempos` (T-12) ya calculados
y los compone en una página, mismo patrón que `documento_revision` (T-16) con
sus propias entradas. `generar_reproductor_html(resultado, resultado_tiempos,
nombre_guion="guion", configuracion=None)` es el punto de entrada;
`guardar_reproductor(pagina_html, carpeta_salida)` la escribe como
`reproductor.html` dentro de la carpeta de salida del guion (aislamiento,
§0.2).

- **Plantillas, no f-strings gigantes.** `assets/reproductor/plantilla.html`,
  `estilo.css` y `guion.js` son archivos de verdad, no cadenas Python: se leen
  y se ensamblan sustituyendo marcadores (`__ESTILO__`, `__SCRIPT__`,
  `__TITULO__`, `__DATOS_JSON__`, y dentro del CSS los de color/tipografía/
  tamaño). `test_ninguna_plantilla_deja_un_marcador_sin_sustituir` es la red
  que evita que un marcador nuevo se quede sin reemplazar en el HTML final.
- **Los datos viajan como JSON, nunca interpolados en el marcado.** Todas las
  escenas y bloques de respiración se sirven en un
  `<script type="application/json" id="datos-reproductor">`, que `guion.js`
  lee con `JSON.parse` y vuelca al DOM con `textContent` exclusivamente --
  nunca `innerHTML`. Doble cinturón: aunque el escapado de abajo fallara, no
  hay vía de inyección de marcado en el render.
- **Escapado seguro (requisito 3 de T-18), el porqué exacto.** Un bloque de
  locución con el texto literal `</script>` cerraría la etiqueta igualmente
  aunque esté dentro de un `type="application/json"`: el analizador HTML
  decide dónde termina un `<script>` por el texto, no por su atributo `type`.
  `_json_seguro_para_script` sustituye `<`, `>` y `&` por su escape Unicode
  (`<`, `>`, `&`) **después** de `json.dumps`, así que el JSON
  sigue siendo válido y `JSON.parse` lo revierte sin que quien lo lee note
  nada. Las tildes y las eñes se dejan tal cual (`ensure_ascii=False`): el
  documento declara `charset="utf-8"` y no hay ningún motivo para escaparlas.
  Probado además contra un navegador real (Chromium vía Playwright, solo para
  esta verificación manual, no es una dependencia del proyecto): un bloque con
  `</script><script>alert(1)</script>` y un `<img onerror=...>` se renderiza
  como texto literal, sin diálogos ni errores de consola.
- **Config, no números mágicos.** Colores (`color_fondo_reproductor`,
  `color_texto_reproductor`, `color_texto_secundario_reproductor`), tamaño de
  letra base (`tamano_texto_base_px`) y pila tipográfica
  (`pila_tipografica_reproductor`) viven en `Configuracion` (`scripts/config.py`),
  con el criterio del dueño ya fijado en §0.2: neutro y oscuro, sin identidad
  corporativa, solo fuentes del sistema.
- **La auto-contención ya no es NO APLICABLE.** `verificar_salidas.py` genera
  ahora el reproductor de verdad sobre el primer guion de
  `fixtures/reales/` (a falta de `fixtures/guion-ejemplo.md`, que trae T-32) y
  valida el resultado con el mismo `buscar_recursos_externos` que ya
  comprobaba T-00. "Guion de ejemplo" y "Generación de salidas" (la
  canalización completa `.srt`/`.pdf`/`.pptx`) siguen NO APLICABLE hasta T-32
  y T-30 respectivamente: no es su tarea, cada etapa se activa cuando le toca.
- **Alcance deliberadamente mínimo.** El HTML lista escenas y bloques en
  orden, sin índice navegable, sin pantalla completa, sin resaltado ni
  autoscroll: eso es T-19 a T-22. Este módulo solo demuestra que la
  canalización de un único archivo autocontenido funciona de punta a punta.

## Índice de escenas y pantalla completa (T-19)

T-19 no toca `reproductor.py`: los datos que genera Python no cambian de
forma. Todo el trabajo está en `assets/reproductor/guion.js`, que pasa de
pintar una única página larga a dos "vistas" que se alternan dentro del mismo
`#app`, usando el atributo `hidden` -- sin `location.href`, sin recarga:

- **`vista-indice`**: una fila por escena (`escena-fila-N`), cada una un único
  `<button>` con número, título, duración estimada formateada y una insignia
  de estado (`escena-estado--pendiente|grabada|revisada`). La fila entera ES
  el botón de play: no hay un botón de play separado dentro de la fila
  (decisión en `DECISIONES_TECNICAS.md`, 2026-09-02). Eso da navegación con
  `Tab` gratis (orden natural de foco de un `<button>`), con `Enter`/`Espacio`
  gratis (disparan el `click` nativo) y con clic gratis. Las flechas
  (`ArrowUp`/`ArrowDown`/`Home`/`End`) se interceptan a mano en el `<ul>` para
  saltar entre filas.
- **`vista-reproductor`**: cabecera con el contador `N/total`
  (`contador-escena`) y el botón `btn-volver-indice`, seguida de la escena
  activa (mismo render de bloques que ya existía en T-18, ahora solo para una
  escena en vez de para todas).
- **Pantalla completa.** Pulsar una fila llama a
  `document.documentElement.requestFullscreen()`, con `.catch()` silencioso si
  el navegador la deniega -- el reproductor sigue funcionando en modo ventana,
  sin excepción no capturada ni error de consola. "Volver al índice" llama a
  `document.exitFullscreen()` si procede.
- **Foco tras la transición a pantalla completa, el detalle que no es obvio.**
  Chromium vacía el foco de la página (`document.activeElement` pasa a
  `<body>`) al completar la transición a pantalla completa, pisando cualquier
  `.focus()` llamado antes de pedirla. `solicitarPantallaCompleta` por eso
  recibe el botón "Volver al índice" y lo refoca dentro del `.then()` de la
  promesa, no antes de llamarla. Sin esto, el criterio de aceptación literal
  de T-19 (recorrido completo solo con teclado) se rompe justo al entrar en
  la escena. Verificado con Chromium vía Playwright headless (solo para esta
  comprobación manual, no es una dependencia del proyecto).
- **Estado por escena, deliberadamente efímero.** `estadosEscena` vive en
  memoria de `guion.js`, no en `datos` (que sigue siendo solo lo que genera
  Python) ni en ningún almacenamiento persistente. Toda escena arranca
  `pendiente` y pasa a `grabada` al reproducirse y volver al índice al menos
  una vez; `revisada` está definida en `ETIQUETAS_ESTADO` pero ninguna
  interacción de T-19 la alcanza todavía -- persistirlo de verdad (o
  sustituirlo por datos reales de rodaje) es T-26/R-02, no esta tarea.
- **Verificación del criterio de aceptación.** Al no ejecutar JS, la suite de
  `pytest` solo comprueba que el HTML/JS generado contiene las piezas
  esperadas (ids, textos, nombres de función) como texto -- igual que ya hacía
  T-18. El recorrido de teclado en sí (llegar a la escena 4 solo con `Tab` y
  flechas, arrancar en pantalla completa con `Enter`, volver al índice con
  `Enter` sin recargar) se verificó a mano con Playwright headless sobre el
  fixture real de `fixtures/salida/reproductor.html`, sin usar el ratón y sin
  errores de consola.

## Motor de avance híbrido (T-20)

Tampoco toca `reproductor.py` en lo esencial: los bloques ya traen
`inicio_segundos`/`fin_segundos` (T-12, vía T-18) y su diferencia es
exactamente la duración que hay que resaltarlos. Solo se añaden tres claves
nuevas al JSON incrustado -- `paso_velocidad`, `velocidad_minima`,
`velocidad_maxima` (config, sin números mágicos) -- para que `guion.js` no
tenga que traer sus límites de velocidad escritos a mano. Todo el motor vive
en `assets/reproductor/guion.js`:

- **Reloj por bloque, no por escena.** `iniciarTemporizadorBloque()` arma un
  único `setTimeout` con la duración del bloque activo
  (`fin_segundos - inicio_segundos`, que ya incluye la pausa tras el bloque)
  dividida por `velocidadesEscena[escenaActual]`. Al disparar,
  `avanzarAutomatico()` mueve el índice y vuelve a llamar a
  `iniciarTemporizadorBloque()`: es una cadena de temporizadores de un solo
  bloque, no un intervalo global. En el último bloque de la escena no hay más
  que encadenar y la función no hace nada.
- **Velocidad recordada por escena, no persistida (requisito 5).**
  `velocidadesEscena` es un array paralelo a `datos.escenas`, mismo patrón que
  `estadosEscena` de T-19: vive en memoria de la pestaña, arranca en `1.0` por
  escena y sobrevive mientras se navega de escena en escena desde el propio
  reproductor (`ArrowUp`/`ArrowDown`). Persistirla entre sesiones es T-26, no
  esta tarea -- mismo razonamiento que ya dejó T-19 para el estado de escena.
- **Cambiar de velocidad no toca el bloque en curso (requisito 2).**
  `ajustarVelocidad(delta)` solo actualiza `velocidadesEscena[escenaActual]`
  (con redondeo al paso configurado para evitar deriva de coma flotante) y el
  indicador visible; nunca cancela ni reprograma el temporizador activo. El
  cambio se nota la próxima vez que `iniciarTemporizadorBloque()` lo lea, es
  decir, desde el bloque siguiente -- literal al requisito ("sin cortes").
- **Avanzar a mano reinicia el reloj sin salir del automático (requisito 3).**
  `irABloque(indice)` (usada por `bloqueSiguienteManual`/`bloqueAnteriorManual`/
  `reiniciarEscenaActual`) mueve el índice y llama de nuevo a
  `iniciarTemporizadorBloque()`, que arranca un reloj nuevo para el bloque de
  destino con su propia duración completa. Si el motor no estaba en pausa,
  ese nuevo reloj empieza a correr inmediatamente: "avanzar a mano" nunca dejó
  de estar en modo automático, solo cambió qué bloque cuenta el tiempo.
- **Pausa exacta, no aproximada (requisito 4, "reanuda exactamente donde
  estaba").** `togglePausa()` no reinicia nada: al pausar, calcula
  `bloqueMsRestantes` restando el tiempo transcurrido desde que arrancó el
  reloj del bloque actual (`bloqueInicioMarca`) a su duración total, y cancela
  el `setTimeout` pendiente. Al reanudar, arma un `setTimeout` nuevo con
  exactamente ese resto. Pausar y reanudar varias veces seguidas es
  correcto por construcción: `bloqueMsRestantes` siempre es "lo que falta
  medido desde la última marca", nunca un valor absoluto que pueda desincronizarse.
- **Teclado del motor, adelantado de T-24 a propósito.** `manejarTeclaReproductor`
  (un único listener en `document`, activo solo si `vistaReproductor` no está
  oculta) ya usa el mapa final que describe T-24: `Espacio` pausa/reanuda,
  `+`/`-` (y `=` sin mayúscula, por si el teclado no la ofrece directo) ajustan
  velocidad, `→`/`PageDown` y `←`/`PageUp` avanzan/retroceden un bloque,
  `↑`/`↓` cambian de escena sin salir de pantalla completa, `R` reinicia la
  escena. T-24 no tiene que reasignar teclas, solo añadir el modal de ayuda
  (`?`), el antirrebote del clicker y la tolerancia de repeticiones rápidas.
- **Cambiar de escena sin volver a pedir pantalla completa.**
  `escenaAdyacente(delta)` reutiliza `reproducirEscena(destino)` tal cual (
  reconstruye la vista del reproductor entera, igual que "Volver al índice"
  seguido de reproducir otra escena), pero `solicitarPantallaCompleta` ahora
  comprueba `document.fullscreenElement` primero: si ya está en pantalla
  completa, solo refoca el botón "Volver al índice" en vez de volver a llamar
  a `requestFullscreen()` (evita un permiso denegado o un parpadeo por pedir
  algo que ya se tiene).
- **Resaltado mínimo a propósito.** `.bloque--activo` en `estilo.css` es un
  fondo y un borde discretos, lo justo para verificar el motor a ojo. El
  tratamiento real (contexto atenuado con gradiente configurable, contraste
  AAA) es T-21; no se adelanta aquí para no invadir su alcance.
- **Verificación.** `tests/test_reproductor.py` comprueba (como texto sobre el
  HTML/JS generado, igual que T-18/T-19) que las funciones y los datos
  esperados están presentes. El comportamiento real -- cadena de avances
  automáticos, avance manual que no detiene el automático, pausa/reanudación
  exacta, velocidad que acelera el ritmo, recuerdo de velocidad por escena,
  cambio de escena sin salir de pantalla completa -- se verificó a mano con
  Playwright headless sobre `fixtures/salida/reproductor.html` (Chromium, no
  es una dependencia del proyecto), incluyendo temporizadores reales
  (`wait_for_timeout`) contra las duraciones reales de los bloques del guion
  de calibración.

## Resaltado, tipografía y tema de grabación (T-21)

Tampoco toca `reproductor.py` en lo esencial más allá de sumar siete claves
nuevas al JSON incrustado (`atenuacion_niveles`, `atenuacion_minima`,
`tamano_texto_base_px`, `paso_tamano_texto_px`, `tamano_texto_minimo_px`,
`tamano_texto_maximo_px`, `tiempo_inactividad_cursor_ms`) y dos marcadores
nuevos en la plantilla de `estilo.css` (`__COLOR_ACENTO__`,
`__MARGEN_SEGURO_PX__`) -- mismo patrón que ya siguió T-20 para los límites
de velocidad. El resto vive en `assets/reproductor/guion.js` y
`estilo.css`:

- **Atenuación del contexto por distancia, no por clase fija (requisito 1).**
  `marcarBloqueActivo(indice)` ya no solo alterna `.bloque--activo`: para
  cada bloque que no es el activo, calcula `opacidadPorDistancia(distancia)`
  (`Math.abs(i - indice)`) y la aplica como `style.opacity` directamente,
  en vez de un número fijo de clases CSS. `distancia - 1` indexa
  `datos.atenuacion_niveles` (gradiente estrictamente decreciente,
  configurable); más allá del último nivel se usa `datos.atenuacion_minima`
  como suelo. Se optó por opacidad calculada en JS en vez de N clases CSS
  (`.bloque--atenuado-1`, `-2`...) porque el número de niveles es
  configurable: una clase por nivel obligaría a generar tantas reglas CSS
  como niveles trajera la configuración, acoplando la plantilla a un valor
  de `Configuracion`.
- **El bloque activo nunca se atenúa a sí mismo.** `esActivo` limpia
  `style.opacity` a `""` (deja que gane la opacidad `1` de `.bloque--activo`
  en `estilo.css`), en vez de asignarle `1` a mano -- así un futuro cambio
  de la opacidad base del bloque activo en CSS no queda pisado por un valor
  inline puesto aquí.
- **Contraste AAA verificado por test, no solo por ojo (requisito 3).**
  `reproductor.py` gana `contraste_relativo(color_a, color_b)`, una
  implementación directa de la fórmula de luminancia relativa WCAG (sin
  dependencia nueva: es aritmética de biblioteca estándar). No se usa para
  nada en tiempo de generación -- es una función de verificación, ejercida
  por `tests/test_reproductor.py::test_contraste_del_bloque_activo_cumple_aaa`,
  que falla si algún día los colores por defecto (`color_texto_reproductor`
  contra `color_fondo_reproductor`) bajan de la razón 7:1 que exige AAA para
  texto normal. Con los valores actuales (`#f5f5f5` sobre `#0b0b0d`) el
  ratio real es ~18.5:1, muy por encima del mínimo.
- **Color de acento centralizado, no repetido a mano (limpieza de alcance).**
  `#f5c542` aparecía tal cual en tres reglas de `estilo.css` (foco visible,
  indicador de pausa, borde del bloque activo) desde T-19/T-20, sin pasar
  por `Configuracion` -- una excepción a la regla "sin números mágicos"
  que este tema es la ocasión natural de cerrar. Ahora es
  `color_acento_reproductor` (`Configuracion`) → `--color-acento` (CSS) → las
  tres reglas lo referencian.
- **Margen seguro configurable, mismo patrón que el resto del tema.**
  `#app { padding: 2rem 1.5rem 6rem; }` (fijo, sin pasar por configuración)
  pasa a `padding: var(--margen-seguro);`, con `margen_seguro_px` en
  `Configuracion` (por defecto 64 px, uniforme en los cuatro lados).
- **Tamaño de texto en vivo, preferencia global, no por escena (requisito
  2).** `ajustarTamanoTexto(delta)` mueve `tamanoTextoActualPx` (un único
  valor de módulo, no un array paralelo a `datos.escenas` como
  `velocidadesEscena` de T-20) dentro de
  `[tamano_texto_minimo_px, tamano_texto_maximo_px]` y lo aplica con
  `document.documentElement.style.setProperty('--tamano-base', ...)`. Se
  decidió que NO sea por escena, a diferencia de la velocidad: el tamaño de
  letra es una preferencia de lectura de quien graba (su distancia a la
  cámara, su vista), no algo que dependa del contenido de una escena
  concreta -- cambiarlo una vez debe seguir aplicando al pasar a la escena
  siguiente. Teclas `[`/`]`, elegidas por estar libres en el mapa que T-20
  ya adelantó de T-24 (`Espacio`, `+`/`-`, flechas/`PageUp`/`PageDown`, `R`)
  y no chocar con `M`/`H`/`?`, ya reservadas por T-24 a modo espejo, ocultar
  indicadores y la ayuda.
- **Cursor oculto solo en pantalla completa, nunca en modo ventana
  (requisito 4).** `reprogramarOcultarCursor()` reinicia un `setTimeout`
  en cada `mousemove`; al dispararse, `ocultarCursor()` comprueba
  `document.fullscreenElement` antes de añadir la clase `cursor-oculto` a
  `#app` -- en modo ventana (pantalla completa denegada por el navegador)
  el cursor nunca desaparece, porque ahí no compite con ninguna cámara. El
  listener de `fullscreenchange` limpia la clase y el temporizador al salir
  de pantalla completa, para no dejar el cursor oculto por error al volver
  al índice.
- **Verificación.** `tests/test_reproductor.py` comprueba (como texto sobre
  el HTML/JS generado) las claves nuevas del JSON, la sustitución de los
  marcadores de acento/margen y la presencia de las funciones nuevas;
  `tests/test_esqueleto.py` cubre la validación de `Configuracion` (niveles
  de atenuación decrecientes, suelo dentro de rango, límites de tamaño
  coherentes, margen no negativo). El comportamiento real -- gradiente de
  opacidad aplicado bloque a bloque según distancia real al activo, tamaño
  de texto que cambia en vivo y persiste al cambiar de escena, cursor que se
  oculta tras la inactividad configurada y reaparece al mover el ratón, cero
  errores de consola -- se verificó a mano con Playwright headless sobre
  `fixtures/salida/reproductor.html` (Chromium, no es una dependencia del
  proyecto).

## Autoscroll con bloque centrado (T-22)

Tampoco toca `reproductor.py` en lo esencial más allá de sumar una clave nueva
al JSON incrustado (`duracion_autoscroll_ms`, config, sin números mágicos).
Todo el trabajo vive en `assets/reproductor/guion.js`:

- **El documento entero es el contenedor de scroll.** `#app` no tiene
  `overflow` propio (crece con la altura natural de la página), así que
  centrar el bloque activo es mover `window.scrollY`, no el `scrollTop` de un
  div interno. `centrarBloqueActivo(animado)` calcula el centro vertical del
  bloque activo (`getBoundingClientRect().top + window.scrollY +
  rect.height / 2`) y lo compara con el centro del viewport
  (`document.documentElement.clientHeight / 2`), acotando el resultado entre
  `0` y `scrollMaximo()` (`scrollHeight - clientHeight`, nunca negativo).
- **Requisito 3 (si cabe entero, no se desplaza) sale gratis del cálculo, sin
  rama aparte.** Cuando el contenido cabe en el viewport, `scrollMaximo()` es
  `0`, así que el objetivo siempre coincide con el origen (`0`) y la propia
  guarda `Math.abs(objetivo - origen) < 1` evita animar o saltar a ningún
  sitio. No hace falta comprobar "¿cabe entero?" como caso especial.
- **Animación propia con `requestAnimationFrame`, no
  `scrollIntoView({behavior:'smooth'})` (requisito 2).** Con el método nativo,
  dos llamadas seguidas (p. ej. avanzar dos bloques a mano muy rápido) se
  encolan o se interrumpen sin control sobre el punto de partida real -- el
  origen de la segunda animación podría no ser la posición visible en ese
  instante, produciendo un salto perceptible. La interpolación manual guarda
  `animacionScroll` (el identificador de `requestAnimationFrame` en curso);
  cada llamada nueva primero `cancelAnimationFrame` la anterior y calcula
  `origen = window.scrollY` en ESE momento -- la posición real, sea cual sea
  --, así que un avance rápido a mano nunca rebota ni retrocede: cada
  petición nueva continúa desde donde el scroll estaba de verdad. El
  suavizado es un ease-in-out cuadrático simétrico (`suavizarProgreso`), sin
  overshoot.
- **Instantáneo vs. animado, según qué lo dispara.** `centrarBloqueActivo`
  recibe un booleano: `true` (con transición, `duracion_autoscroll_ms`,
  400 ms por defecto) para el avance automático (`avanzarAutomatico`), el
  avance/retroceso manual y el reinicio de escena (todos pasan por
  `irABloque`), y el cambio de tamaño de texto en vivo (`ajustarTamanoTexto`,
  porque el reflow del bloque activo a otra altura de página sí debe
  notarse como un desplazamiento suave, no un tirón). `false` (sin
  transición, salto directo) para el arranque de una escena (`iniciarMotor`,
  no hay "posición anterior" que abandonar suavemente) y el listener de
  `resize` (redimensionar la ventana es un cambio estructural del lienzo, no
  un gesto de lectura -- animarlo mientras el usuario aún arrastra el borde
  de la ventana solo añadiría un desfase visible).
- **Bug real encontrado y corregido en la misma sesión: el foco de T-19 le
  ganaba la partida al centrado.** `solicitarPantallaCompleta` (T-19) refoca
  el botón "Volver al índice" dentro del `.then()` de la promesa de
  `requestFullscreen()`, porque Chromium vacía el foco al completar la
  transición. Verificado con Playwright (headless Chromium, la pantalla
  completa SÍ se concede en ese entorno): ese foco diferido llegaba DESPUÉS
  del centrado inicial de `iniciarMotor` y disparaba el scroll-into-view por
  defecto del navegador al enfocar un botón situado arriba de la página,
  devolviendo el scroll a `0` en cada entrada a una escena -- deshaciendo el
  trabajo de T-22 en el caso más común (pantalla completa concedida). Se
  corrige con `elemento.focus({ preventScroll: true })` en las dos llamadas
  de `solicitarPantallaCompleta` (la síncrona y la del `.then()`): el foco se
  sigue moviendo (el recorrido de teclado de T-19 no se pierde), pero ya no
  arrastra el scroll consigo. No se detectó escribiendo el código, sino
  verificando a mano contra el fixture real -- ver más abajo.
- **Verificación.** `tests/test_reproductor.py` comprueba (como texto sobre
  el HTML/JS generado) la clave nueva del JSON y la presencia de
  `centrarBloqueActivo`/`cancelAnimationFrame`/`requestAnimationFrame`/el
  listener de `resize`; `tests/test_esqueleto.py` cubre el rechazo de una
  duración de autoscroll no positiva. El comportamiento real se verificó a
  mano con Playwright headless (Chromium, no es una dependencia del
  proyecto) sobre `fixtures/salida/reproductor.html` (guion real de 7
  escenas, 4-21 bloques cada una): una escena de 4 bloques en un viewport
  donde cabe entera no se desplaza (`scrollY` permanece en `0`); en la
  escena de 21 bloques, el bloque activo permanece dentro del tercio central
  de la pantalla en las 20 transiciones manuales, tras dos aumentos y
  varias reducciones de tamaño de texto, tras cinco avances manuales
  seguidos sin esperar a que termine la animación anterior (sin rebote:
  termina exactamente centrado, sin oscilar) y tras redimensionar la
  ventana de 500 a 700 px de alto -- sin errores de consola en ningún paso.

## Ayudas de grabación (T-23)

Cuatro añadidos independientes a `assets/reproductor/guion.js`, todos sobre el
mismo `reproducirEscena`/`iniciarMotor`/`detenerMotor` de T-19/T-20 -- ninguno
introduce un modo nuevo, solo instrumentan el que ya existía. Dos claves
nuevas en el JSON incrustado (`cuenta_atras_segundos`, `cuenta_atras_activada`
en `Configuracion`, sin números mágicos).

- **Cuenta atrás (requisito 1), como una envoltura de `iniciarMotor`, no una
  parte de él.** `reproducirEscena` ya no llama a `iniciarMotor(indice)`
  directamente: llama a `iniciarCuentaAtras(function () { iniciarMotor(indice); })`.
  Si `cuenta_atras_activada` es `false` (o la duración es `0`), la cuenta
  atrás invoca el callback al instante -- "desactivable" es ese booleano, no
  poner la duración a cero, mismo patrón paso/activable del resto del
  reproductor. El overlay (`.cuenta-atras`, `position: fixed`) se crea de
  nuevo en cada `renderizarReproductor`, y `detenerMotor` (que ya se llama al
  principio de `reproducirEscena` y en `volverAlIndice`) cancela cualquier
  cuenta atrás pendiente con `detenerCuentaAtras` -- así, salir al índice a
  mitad de la cuenta atrás no deja un `setTimeout` colgado que dispare
  `iniciarMotor` sobre una escena que ya no está en pantalla.
- **Cronómetro de la toma (requisito 2): tiempo de reloj real, no tiempo de
  guion.** Mismo patrón que ya usa el reloj del bloque de T-20
  (`bloqueInicioMarca`/`bloqueMsRestantes`): `cronometroInicioMarca` +
  `cronometroMsAcumulados`, recalculado siempre desde marcas de tiempo
  absolutas (`Date.now()`), nunca acumulando por intervalo -- así la deriva
  del criterio de aceptación ("< 1 % en una toma de 3 minutos") es
  estructuralmente imposible, no un valor medido: un `setInterval` de 250 ms
  solo decide cada cuánto se REDIBUJA la cifra, el valor en sí sale siempre de
  restar dos marcas de reloj reales. `togglePausa` congela y reanuda el
  cronómetro exactamente donde ya congelaba y reanudaba el reloj del bloque,
  reutilizando la misma pareja de líneas en el mismo sitio. Formato con
  `formatearTiempo` (T-19): "transcurrido / estimado".
- **Barra de progreso por bloques (requisito 3), deliberadamente NO por
  tiempo.** `actualizarBarraProgreso` calcula `(bloqueActual + 1) / total`, no
  una fracción de `duracion_estimada_segundos`. Es la única forma de que el
  criterio de aceptación ("la barra llega al 100 % justo con el último
  bloque") se cumpla por construcción: con progreso por tiempo, una toma que
  se alarga o se acorta respecto a la estimación dejaría la barra en un punto
  distinto de 100 % justo cuando el locutor llega al último bloque. Se
  actualiza desde dentro de `marcarBloqueActivo` (ya se llama con el
  `bloqueActual` correcto desde `iniciarMotor`, `avanzarAutomatico` e
  `irABloque`), más una llamada explícita en `iniciarMotor` para el caso de
  escena sin bloques de locución (el `if (bloquesEscenaActual().length > 0)`
  de T-20 nunca llama a `marcarBloqueActivo` ahí, así que sin esa llamada
  extra la barra se quedaría con el ancho de la escena anterior).
- **Indicadores discretos, ocultables con una tecla (requisito 4): un único
  interruptor, no una lista de elementos que ocultar uno a uno.**
  `alternarIndicadores` alterna una sola clase (`indicadores-ocultos`) en
  `#vista-reproductor`; el CSS (`#vista-reproductor.indicadores-ocultos
  .reproductor-cabecera`, `...  .barra-progreso-contenedor`) decide qué
  desaparece. Como el toggle vive en `vistaReproductor.classList` y
  `renderizarReproductor` solo vacía `vistaReproductor.textContent`, el
  estado sobrevive a un cambio de escena -- ocultar los indicadores antes de
  arrancar a grabar una tanda de escenas seguidas no hay que repetirlo en
  cada una. Tecla `H`/`h`, mismo `switch` de `manejarTeclaReproductor` que ya
  usan el resto de atajos de T-20/T-21; T-24 la documentará en el mapa
  completo y en la ayuda `?`, no hace falta tocar nada aquí cuando llegue.
- **Verificación.** `tests/test_reproductor.py` comprueba (como texto sobre
  el HTML/JS generado) las dos claves nuevas del JSON, la presencia de
  `iniciarCuentaAtras`/`actualizarCronometro`/`actualizarBarraProgreso`/
  `alternarIndicadores` y las reglas CSS del toggle;
  `tests/test_esqueleto.py` cubre el rechazo de una `cuenta_atras_segundos`
  no positiva. El comportamiento real se verificó a mano con Playwright
  headless (Chromium, no es una dependencia del proyecto) sobre
  `fixtures/salida/reproductor.html`: al pulsar play aparece "3", cuenta
  hasta "1" y desaparece sin que el motor arranque antes de tiempo; con
  `cuenta_atras_activada=False` el motor arranca al instante sin overlay; el
  cronómetro avanza con el reloj real y se congela exactamente en pausa (dos
  lecturas separadas por 1.5 s de pausa, idénticas); la barra de progreso
  pasa de 25 % (bloque 1 de 4) a 100 % en el último bloque de una escena
  real; `H` oculta la cabecera y la barra y una segunda pulsación las
  devuelve -- sin errores de consola en ningún paso.

## Atajos de teclado y clicker Bluetooth (T-24)

Cierra el mapa de teclas del reproductor (T-19 a T-23 ya habían ido reservando
teclas sueltas sobre la marcha) y le añade dos piezas nuevas: un antirrebote
configurable y una ayuda en pantalla. Cambios en tres archivos: `config.py`
(cablea `ANTIRREBOTE_CLICKER_MS`, ya reservada desde T-20 sin usar, y suma
`ESPACIO_AVANZA_BLOQUE`/`MAPA_TECLAS_REPRODUCTOR`), `reproductor.py` (las
lleva al JSON incrustado) y `guion.js` (el propio motor de teclado).

- **El mapa de teclas deja de estar escrito a mano en el `switch` de
  `manejarTeclaReproductor` (requisito 3, "configurable en la generación").**
  Antes, cada `case` comparaba directamente un literal de tecla
  (`case "ArrowRight":`); ahora compara el NOMBRE DE UNA ACCIÓN
  (`case "bloque_siguiente":`), resuelto a partir de `evento.key` con una
  tabla `teclaAAccion` construida una vez, al cargar la página, recorriendo
  `datos.mapa_teclas` (que a su vez viene de
  `Configuracion.mapa_teclas_reproductor`, una tupla de pares
  `(accion, teclas)` -- tupla y no `dict`, para que el valor por defecto siga
  siendo inmutable como exige el dataclass congelado de `Configuracion`;
  `reproductor.py` la convierte a `dict()` una sola vez al construir el JSON,
  porque un objeto es más cómodo de recorrer desde `guion.js` que un array de
  pares). Remapear una tecla, o añadir una nueva, es cambiar
  `MAPA_TECLAS_REPRODUCTOR` en `config.py`; `guion.js` no cambia.
- **`Espacio` pausa/reanuda por defecto, pero puede avanzar el bloque en su
  lugar (requisito 1, "según configuración").** Decisión del dueño, no una
  heurística: no hay forma de saber desde el navegador qué botón físico de
  un clicker Bluetooth envió la tecla, y algunos mandos de presentaciones
  usan su botón principal para enviar `Espacio` con el significado de
  "avanzar", no de "pausar". `Configuracion.espacio_avanza_bloque` (`False`
  por defecto, sin tocar el comportamiento que ya tenían T-20 a T-23) decide
  cuál de las dos ramas toma la acción `pausa_avanza` dentro del `switch`.
- **Antirrebote por acción, no global (requisito 2, "tolerar pulsaciones
  repetidas rápidas... configurable").** `ultimaPulsacionPorAccion` guarda,
  por nombre de acción, la marca de `Date.now()` de la última pulsación
  ACEPTADA; `pulsacionPermitida(accion)` descarta una pulsación nueva si
  llega antes de que pasen `antirrebote_clicker_ms` (120 ms por defecto,
  `0` lo desactiva) desde esa marca. Es por acción y no un único cronómetro
  global para que pulsar rápido dos teclas DISTINTAS (p. ej. `PageDown`
  seguido de `+`) nunca se descarte por error -- solo se protege la MISMA
  acción contra el rebote de contacto de un clicker barato, que es el caso
  real que el requisito describe.
- **`evento.preventDefault()` se aplica a toda tecla reconocida ANTES del
  antirrebote (requisito 2, "evitar el desplazamiento nativo de la
  página").** Si el antirrebote descartara la pulsación antes de cancelar la
  acción por defecto, una repetición rápida de `PageDown` desplazaría la
  página igual, aunque la acción del reproductor se ignorara. El orden
  importa: primero se decide si la tecla pertenece al mapa (si no, se deja
  que el navegador haga lo que le corresponda con cualquier otra tecla),
  después se cancela su acción nativa, y solo entonces se aplica el
  antirrebote sobre la acción resuelta.
- **`Esc` sale de pantalla completa de forma explícita, además de lo que ya
  hace el propio navegador.** Los navegadores ya interceptan `Escape` para
  salir de pantalla completa sin que ningún script pueda evitarlo
  (`preventDefault` no tiene efecto sobre esa acción por defecto en
  concreto); `salirPantallaCompleta()` (ya existía desde T-19, la usa
  `volverAlIndice`) se llama aquí también, de forma explícita, para que el
  atajo quede documentado en el mapa configurable y en la ayuda `?` en vez
  de depender de un comportamiento implícito del navegador que el propio
  mapa no reflejaría. Es una llamada inocua si el navegador ya ha salido de
  pantalla completa por su cuenta (`salirPantallaCompleta` comprueba
  `document.fullscreenElement` antes de hacer nada).
- **Ayuda `?` construida leyendo el mismo `datos.mapa_teclas` que usa
  `manejarTeclaReproductor` (requisito 3, "visible... el mapa VIGENTE").**
  `construirListaAyudaTeclado()` recorre `Object.keys(datos.mapa_teclas)` y
  genera una fila por acción con sus teclas (pasadas por `ETIQUETAS_TECLA`
  para mostrar "Espacio"/"→"/"Re Pág" en vez de literales crudos como `" "`
  o `"PageUp"`) y su descripción (`ETIQUETAS_ACCION_TECLADO`, texto de
  interfaz fijo en español, no configurable -- a diferencia de las teclas,
  no tiene sentido que el dueño lo reconfigure). No hay una lista paralela
  escrita a mano que pudiera desincronizarse del mapa real: cambiar
  `MAPA_TECLAS_REPRODUCTOR` cambia la ayuda sin tocar `guion.js`.
  `alternarAyuda()` solo alterna `hidden` en el overlay (mismo patrón que
  `.cuenta-atras`, `position: fixed`), reconstruido en cada
  `renderizarReproductor` -- barato (una docena de elementos) y evita
  preocuparse de que sobreviva al vaciado de `vistaReproductor.textContent`.
- **Ningún atajo nuevo depende de una combinación con modificador
  (requisito 4).** Todas las entradas de `MAPA_TECLAS_REPRODUCTOR` son teclas
  sueltas (`evento.key` tal cual, sin comprobar `ctrlKey`/`shiftKey`/`altKey`
  en ningún punto del código); `Configuracion.__post_init__` valida que el
  mapa no esté vacío y que ninguna acción se quede sin ninguna tecla
  asignada, pero no impone la regla de "sin modificadores" en tiempo de
  ejecución -- es una convención de diseño, no una propiedad que el código
  pueda verificar sin inventar una sintaxis de combinación que hoy nadie usa.
- **Verificación.** `tests/test_reproductor.py` comprueba (como texto sobre
  el HTML/JS generado) las tres claves nuevas del JSON
  (`antirrebote_clicker_ms`, `espacio_avanza_bloque`, `mapa_teclas`), que el
  mapa configurado por el dueño se refleja tal cual en el JSON, la presencia
  de `pulsacionPermitida`/`construirListaAyudaTeclado`/`alternarAyuda` y las
  reglas CSS del panel de ayuda; `tests/test_esqueleto.py` cubre el rechazo
  de un antirrebote negativo (`0` sí se acepta: lo desactiva), de un mapa
  vacío y de una acción sin ninguna tecla asignada. El comportamiento real se
  verificó a mano con Playwright headless (Chromium, no es una dependencia
  del proyecto) sobre `fixtures/salida/reproductor.html` (guion real de 7
  escenas): con `Espacio` se pausa y se reanuda, `PageDown` recorre los 4
  bloques de la primera escena hasta el último y `PageUp` retrocede uno --
  las tres teclas del criterio de aceptación, sin tocar ninguna otra; dos
  `PageUp` pegados (sin esperar entre ellos) solo retroceden un bloque, no
  dos, confirmando el antirrebote; `?` abre un panel con las trece acciones
  del mapa por defecto (comprobado el texto: "Espacio", "Re Pág", "Av Pág",
  "Esc" aparecen legibles) y una segunda pulsación lo cierra; `Escape` sale
  de pantalla completa sin ocultar el reproductor. Con
  `espacio_avanza_bloque=True` en un reproductor generado aparte, `Espacio`
  avanza al bloque siguiente en vez de pausar -- verificado que NO deja
  "En pausa" en el indicador. Sin errores de consola en ningún paso.

## Modo espejo (T-25)

Volteo horizontal del texto para leer contra el cristal de un teleprompter
físico. Cambios en tres archivos: `config.py` (nueva acción `espejo` en
`MAPA_TECLAS_REPRODUCTOR` y campo `espejo_incluye_indicadores`),
`reproductor.py` (lo lleva al JSON incrustado) y `guion.js`/`estilo.css` (el
volteo en sí y su persistencia).

- **El volteo es un `transform: scaleX(-1)` de CSS sobre `.escena`, no una
  reescritura del texto ni una clase por bloque (requisito 1, "volteo
  horizontal del texto").** `aplicarClaseEspejo()` alterna una de dos clases
  en `#vista-reproductor`: `espejo-texto` (por defecto,
  `Configuracion.espejo_incluye_indicadores=False`) aplica el `transform`
  solo a `.escena` -- título y bloques, lo que el requisito llama "el
  texto" --, dejando la cabecera, la barra de progreso, la cuenta atrás y la
  ayuda de teclado sin voltear, porque son indicadores para quien opera el
  reproductor, no contenido que el cristal deba reflejar. Con
  `espejo_incluye_indicadores=True`, se aplica en su lugar `espejo-completo`
  sobre el propio `#vista-reproductor`, que voltea todo -- montaje físico
  donde el cristal cubre la pantalla entera, indicadores incluidos. Las dos
  reglas CSS conviven siempre en `estilo.css`; `guion.js` decide cuál
  activar leyendo `datos.espejo_incluye_indicadores`, nunca al revés.
- **Compatible gratis con el resaltado y el autoscroll (requisito 2), sin
  ningún ajuste en `marcarBloqueActivo`/`centrarBloqueActivo`.**
  `scaleX(-1)` solo invierte el eje horizontal: no cambia la posición ni la
  altura vertical que `getBoundingClientRect` devuelve para un elemento
  transformado, así que el cálculo de centrado de T-22 (que solo mira
  `rect.top`/`rect.height`) sigue centrando el bloque activo exactamente
  igual con el espejo activo o no. Verificado a mano con Playwright
  (viewport reducido a 800×300 para forzar scroll real): la posición
  vertical del bloque activo tras cada avance es la misma con y sin espejo
  activo, dentro del margen de la propia animación.
- **Activable con tecla y desde los controles (requisito 1, literal).** La
  tecla es una entrada más de `MAPA_TECLAS_REPRODUCTOR`
  (`("espejo", ("m", "M"))`), resuelta por el mismo `teclaAAccion` de T-24 --
  ningún cableado nuevo en `manejarTeclaReproductor`, solo un `case` más. El
  control es un botón nuevo (`#btn-espejo`, agrupado con "Volver al índice"
  dentro de `.reproductor-controles`, un `<div>` flex que sustituye al
  antiguo hijo único de `.reproductor-cabecera` para no romper su
  `justify-content: space-between` con un tercer elemento suelto) que llama
  a la misma función `alternarEspejo()` que el atajo de teclado -- una sola
  fuente de verdad para "activar/desactivar", nunca dos implementaciones
  paralelas. El botón refleja el estado con `aria-pressed` y con su propio
  texto ("Espejo: activado"/"desactivado"), y se resalta con el color de
  acento mientras está activo (`.btn-espejo[aria-pressed="true"]`).
- **Persistencia local mínima, adelantada de T-26 solo para este ajuste
  (requisito 3 y criterio de aceptación: "el ajuste persiste tras
  recargar").** T-26 (persistencia local de preferencias) todavía no existe,
  pero el propio criterio de aceptación de T-25 exige la recarga, y a
  diferencia del estado de escena de T-19 (que T-19 dejó deliberadamente en
  memoria, ver su fila en `DECISIONES_TECNICAS.md`), aquí no hay ninguna
  tarea futura cuyo trabajo se duplicara por adelantarlo: nada bloquea
  hacerlo ya. Se añaden tres funciones pequeñas y genéricas --
  `claveAlmacenamiento(preferencia)` (devuelve
  `"teleprompter:" + datos.guion + ":" + preferencia`, ya con la clave
  derivada del guion que el requisito 2 de T-26 va a pedir para el resto de
  preferencias), `leerPreferencia`/`guardarPreferencia` (envuelven
  `localStorage.getItem`/`setItem` en `try/catch`, mismo patrón que T-26
  fijará: si `localStorage` falla -- navegación privada, cuota agotada, o el
  propio `file://` sin soporte verificado, hallazgo #5 de
  `auditoriacontinua.md`, todavía abierto -- el reproductor sigue
  funcionando en memoria, solo sin recordar el ajuste). T-26 solo tiene que
  reutilizar estas tres funciones para el resto de preferencias (tamaño de
  texto, velocidad por escena, última escena vista, indicadores), no
  diseñar el mecanismo desde cero.
- **Verificación.** `tests/test_esqueleto.py` cubre el valor por defecto de
  la nueva acción y de `espejo_incluye_indicadores`;
  `tests/test_reproductor.py` comprueba las claves nuevas del JSON, que el
  mapa incluye `espejo` por defecto, la presencia de
  `aplicarClaseEspejo`/`alternarEspejo`/`claveAlmacenamiento` y de las dos
  reglas CSS. El comportamiento real se verificó a mano con Playwright
  headless (Chromium, no es una dependencia del proyecto) sobre
  `fixtures/reales/guion-08-busqueda-investigacion.md`: el botón y la tecla
  `M`/`m` activan y desactivan el modo por igual (mismo `aria-pressed` y
  mismo `transform` calculado, `matrix(-1, 0, 0, 1, 0, 0)`, sobre `.escena`);
  con `espejo_incluye_indicadores=True` el `transform` aparece en su lugar
  sobre `#vista-reproductor` completo; tras recargar la página con el modo
  activo, el botón sigue mostrando "activado" y el texto sigue volteado sin
  volver a pulsar nada; avanzar de bloque en bloque con el espejo activo
  sigue centrando el bloque activo verticalmente igual que sin él. Sin
  errores de consola en ningún paso.

## Persistencia local de preferencias (T-26)

Extiende el mecanismo mínimo que T-25 adelantó (`claveAlmacenamiento`/
`leerPreferencia`/`guardarPreferencia`) al resto de preferencias del
requisito 1: tamaño de texto, velocidad ajustada por escena, visibilidad de
indicadores y última escena vista. Ningún archivo Python cambia —
`config.py`/`reproductor.py` ya exponían todo lo necesario (límites de
tamaño y velocidad, `escena.numero`, `bloque.inicio_segundos`, `datos.guion`)
desde T-18/T-20/T-21 — todo el trabajo vive en `guion.js`/`estilo.css`.

- **Tamaño de texto y visibilidad de indicadores (requisito 1): mismo patrón
  que el espejo de T-25, una clave por preferencia.** `tamanoTextoActualPx`
  se inicializa leyendo `"tamano_texto"` (acotado a
  `tamano_texto_minimo_px`/`maximo_px`, igual que `ajustarTamanoTexto`) y
  aplica `--tamano-base` de inmediato, antes incluso de entrar en una
  escena, para que el índice ya se lea con el tamaño elegido. `ajustarTamanoTexto`
  guarda cada cambio. `indicadores_ocultos` se lee una vez, antes de la
  primera renderización, para decidir si `vistaReproductor` arranca con la
  clase `indicadores-ocultos`; `alternarIndicadores` guarda el nuevo estado
  en cada toggle.
- **Velocidad por escena (requisitos 1 y 5): la clave usa el NUMERO de
  escena, no su índice en el array.** `velocidadesEscena` se construye
  leyendo `"velocidad_escena_" + escena.numero` para cada escena (acotada a
  `velocidad_minima`/`maxima`); `ajustarVelocidad` guarda con la misma
  clave. Usar el número (estable) en vez del índice (que cambiaría si el
  parser detectara una escena de más o de menos en una regeneración) es lo
  que hace literal el requisito 5 ("si el troceo cambió, la velocidad por
  escena se conserva"): el troceo cambia bloques dentro de una escena, no
  el número de la escena en sí.
- **Última escena vista (requisitos 1 y 5): se guarda el `inicio_segundos`
  del bloque activo, no su índice, para poder reencontrar el bloque más
  cercano si el troceo cambia el número de bloques.**
  `guardarUltimaEscenaVista(indiceBloque)` se llama desde el final de
  `marcarBloqueActivo` — ya se invoca en todo cambio de bloque real (entrar
  en la escena, avance automático, avance/retroceso manual) — y persiste
  `"ultima_escena_numero"` (el número de la escena) y
  `"ultima_escena_inicio_segundos"` (el `inicio_segundos` de T-12 del bloque
  activo). `calcularReanudacion()` hace el camino inverso: busca la escena
  por número (`null` si ya no existe, p. ej. el guión perdió una escena) y,
  dentro de ella, el bloque cuyo `inicio_segundos` esté más cerca del
  guardado — no el mismo índice, que podría apuntar a un bloque distinto si
  el troceo cambió el número de bloques de esa escena. Verificado a mano
  (ver más abajo) regenerando el mismo guión con dos configuraciones de
  troceo distintas (8 y 17 bloques en la misma escena): la posición
  restaurada cae en el bloque de la segunda versión cuyo `inicio_segundos`
  es el más próximo al de la primera, y la velocidad de esa escena se
  conserva intacta.
- **Sin relanzamiento automático al cargar la página: un botón "Continuar"
  explícito en el índice (requisitos 1 y 5), no una decisión menor.**
  `document.documentElement.requestFullscreen()` exige un gesto de usuario
  real; una llamada automática a `reproducirEscena` al final del script (sin
  clic de por medio) habría entrado en la escena y el bloque correctos pero
  se habría quedado en modo ventana, con `solicitarPantallaCompleta`
  tragándose el rechazo del navegador en su `.catch()` — una "restauración"
  a medias, y además le habría quitado al índice de T-19 su papel de único
  punto de entrada. `renderizarIndice()` llama a `calcularReanudacion()` y,
  si no es `null`, añade un botón `#btn-continuar` con el rótulo "Continuar:
  escena N — título"; su `click` llama a
  `reproducirEscena(indiceEscena, indiceBloque)` con un gesto de usuario
  real detrás, así que la petición de pantalla completa sí prospera.
  `reproducirEscena`/`iniciarMotor` ganan un segundo parámetro
  `bloqueInicial` (por defecto `0`, así que todas las llamadas existentes —
  clic en una fila del índice, `escenaAdyacente` — siguen entrando siempre
  por el primer bloque, sin cambiar su comportamiento). De paso corrige un
  bug preexistente y sin efecto visible hasta ahora: `iniciarMotor` llamaba
  a `marcarBloqueActivo(0)` con un literal en vez de con la variable
  `bloqueActual` que la propia función acaba de fijar — daba igual mientras
  `bloqueActual` siempre arrancara en `0`, pero con `bloqueInicial` distinto
  de cero habría marcado el bloque equivocado como activo.
- **Restablecer preferencias (requisito 4): un botón dentro de la ayuda del
  reproductor (`?`), no un atajo de teclado nuevo** — el mapa de T-24 ya
  reserva todas las teclas sin modificador razonables, y esto no es algo
  que un clicker deba poder disparar por accidente.
  `limpiarPreferenciasAlmacenadas()` enumera todas las claves de
  `localStorage` con el prefijo `"teleprompter:" + datos.guion + ":"` (nunca
  borra las de otro guión) y las borra una a una, con el mismo `try/catch`
  que el resto de la persistencia. `restablecerPreferencias()` la llama y
  además repone en memoria cada valor a su por defecto — tamaño de texto,
  las velocidades por escena a `1.0`, espejo desactivado, indicadores
  visibles — sin recargar la página, para que el efecto se vea al instante
  dentro de la misma sesión de grabación.
- **Verificación.** `tests/test_reproductor.py` añade siete tests que
  comprueban, sobre el HTML generado: las claves de lectura/escritura de
  cada preferencia (tamaño, velocidad por escena con clave por número,
  indicadores, última escena vista), la presencia de
  `calcularReanudacion`/`guardarUltimaEscenaVista`/
  `restablecerPreferencias`/`limpiarPreferenciasAlmacenadas`, que
  `reproducirEscena`/`iniciarMotor` aceptan el nuevo `bloqueInicial`, y que
  la última sentencia del script sigue siendo `renderizarIndice();` (nunca
  un lanzamiento automático del reproductor). El comportamiento real se
  verificó a mano con Playwright headless (Chromium, no es una dependencia
  del proyecto) sobre `fixtures/reales/guion-08-busqueda-investigacion.md`
  (con `cuenta_atras_activada=False` para acelerar la verificación, sin
  tocar el criterio de aceptación): al abrir el archivo por primera vez no
  aparece el botón "Continuar"; tras entrar en una escena, avanzar bloques,
  subir la velocidad, aumentar el tamaño de texto, activar el espejo y
  ocultar los indicadores, `localStorage` recoge las seis claves esperadas;
  recargar la página aplica ya el tamaño de texto guardado en el propio
  índice y muestra "Continuar: escena 2 — ...", y pulsarlo entra
  directamente en esa escena con el tamaño, la velocidad, el espejo, los
  indicadores ocultos y el bloque activo restaurados; pulsando "Restablecer
  preferencias" en la ayuda, `localStorage` queda vacío para ese guión, el
  espejo se desactiva, los indicadores reaparecen y el tamaño vuelve al
  valor por defecto, y una recarga posterior ya no ofrece "Continuar"; con
  `localStorage` bloqueado (una `Proxy` que lanza al acceder, simulando
  `file://` restringido o navegación privada) el reproductor entra en una
  escena y avanza un bloque sin ningún error de página. Una segunda pasada,
  regenerando el mismo guión con dos configuraciones de troceo distintas
  (8 y 17 bloques en la escena 2), confirmó el requisito 5: la velocidad
  ajustada en la primera versión sobrevive intacta en la segunda, y el
  bloque restaurado es el de la segunda versión cuyo `inicio_segundos` está
  más cerca del guardado, no el mismo índice. Sin errores de consola en
  ningún paso.

## Persistencia verificada de preferencias, con plan B (R-01)

`origen: auditoría #5`. T-26 confiaba en que `localStorage` sobrevive a
cerrar el navegador y reabrir el archivo, sin comprobarlo en el navegador
real de grabación — el `try/catch` evitaba el error pero no verificaba la
persistencia real, y un fallo se ignoraba en silencio. Esta tarea cierra las
tres piezas que pedía su ficha, entera en `guion.js`/`estilo.css`: ningún
archivo Python cambia.

- **Comprobación real (requisito 1), con dos verificaciones distintas y
  complementarias.** `comprobarAlmacenamientoDisponible()` escribe y relee
  una clave de prueba (`"prueba_disponibilidad"`, sin guión bajo doble para
  no chocar con el test de marcadores sin sustituir de T-18) al cargar la
  página: detecta con certeza el caso "`localStorage` no funciona aquí en
  absoluto" (navegación privada, cuota agotada, `file://` restringido). Lo
  que NO puede saberse dentro de una sola carga de página es si sobrevivirá
  a un cierre futuro del navegador — eso se verificó aparte, a mano, con
  Playwright headless (Chromium, no es dependencia del proyecto) usando
  `launch_persistent_context` sobre `fixtures/salida/reproductor.html` real:
  cerrar el contexto y reabrir el MISMO perfil de datos de usuario mantiene
  las preferencias intactas; un perfil nuevo (otro navegador, otro usuario,
  datos de navegación borrados) aparece vacío — el comportamiento esperado
  de un almacenamiento particionado por origen/perfil, documentado en
  `DECISIONES_TECNICAS.md` en vez de asumido.
- **Aviso honesto (requisito 3).** Si `comprobarAlmacenamientoDisponible()`
  devuelve `false`, `renderizarIndice()` añade un párrafo
  `.aviso-almacenamiento` visible antes de cualquier otra interacción,
  señalando que las preferencias no van a recordarse y remitiendo al plan B.
  El reproductor sigue funcionando con normalidad sin `localStorage` —
  verificado bloqueándolo a propósito (un `Object.defineProperty` que lanza
  al leer `window.localStorage`, simulando el caso extremo).
- **Plan B sin red ni dependencias (requisito 2): exportar/importar
  preferencias como archivo `.json`.** Dos botones nuevos en el índice,
  junto al "Continuar" de T-26: `exportarPreferencias()` construye el JSON
  con `construirExportacionPreferencias()` y dispara una descarga real
  (`Blob` + `URL.createObjectURL` + `<a download>`, verificado que funciona
  desde una página `file://` en Chromium) o, si esa vía lanza, cae a
  `window.prompt()` con el mismo contenido para copiar a mano — nunca en
  silencio. `manejarArchivoImportado()` lee el archivo elegido con
  `FileReader`, valida que sea del mismo guión (`objeto.guion !==
  datos.guion` rechaza con un mensaje claro, sin aplicar nada) y aplica cada
  campo reconocido con `aplicarPreferenciasImportadas()`, acotando tamaño y
  velocidad a los mismos límites que sus ajustes en vivo. Tras importar,
  `renderizarIndice()` se vuelve a llamar (ahora limpia
  `vistaIndice.textContent` al empezar, para ser idempotente) así que el
  botón "Continuar" y el aviso de almacenamiento reflejan de inmediato lo
  importado, sin recargar la página.
- **La exportación lee de las variables en memoria, nunca de
  `localStorage` en el momento del clic.** `tamanoTextoActualPx`,
  `velocidadesEscena`, `espejoActivado` y la clase `indicadores-ocultos` ya
  son la fuente de verdad del ajuste vigente (son las que pinta la
  interfaz); la única pieza nueva es `ultimaEscenaVistaEnMemoria`, una copia
  en memoria que `guardarUltimaEscenaVista()` mantiene al día en cada
  cambio de bloque real, inicializada igual que `calcularReanudacion()` con
  lo que hubiera guardado antes. Verificado con Playwright bloqueando
  `localStorage` del todo: "Exportar preferencias" sigue produciendo un
  `.json` completo y correcto — el plan B funciona precisamente en el
  escenario que lo justifica, no solo cuando el almacenamiento ya iba bien.
- **Verificación.** `tests/test_reproductor.py` añade cinco tests que
  comprueban, sobre el HTML generado: la comprobación de disponibilidad y el
  aviso, los botones/función de exportar e importar, que la exportación lea
  de las variables en memoria, la validación del guión de origen al
  importar, y que la exportación nunca falle en silencio
  (`window.prompt` como red de seguridad). El comportamiento real se
  verificó de punta a punta con Playwright headless (Chromium) sobre
  `fixtures/salida/reproductor.html` (generado de `fixtures/guion-ejemplo.md`):
  cambiar tamaño/velocidad/espejo, volver al índice y exportar produce un
  `.json` con esos valores; en un perfil de navegador COMPLETAMENTE NUEVO
  (sin nada en `localStorage`) el botón "Continuar" no existe todavía;
  importar ese mismo archivo lo hace aparecer con la escena y el bloque
  correctos, y dejar las claves esperadas en el `localStorage` del nuevo
  perfil; con `localStorage` bloqueado, el aviso aparece, el reproductor
  sigue funcionando, y "Exportar preferencias" sigue produciendo un `.json`
  completo leyendo solo de memoria. Sin errores de consola en ningún paso.

## Registro de tomas por escena (R-02)

`origen: roadmap`, primera tarea de la oleada v2 tras R-01. El índice deja de
ser solo un estado por escena (T-19) y pasa a ser el parte de rodaje real:
número de tomas, duración real de cada una y cuál es la buena (requisito 1),
nota rápida sin salir del modo de grabación (requisito 2), volcado a un
archivo legible por el dueño y por la fase de montaje (requisito 3), e índice
que refleja de un vistazo qué falta, qué se repitió y qué está resuelto
(requisito 4). Casi entera en `guion.js`/`estilo.css`; el lado Python
(`scripts/tomas.py`) solo entra en juego cuando el dueño entrega de vuelta el
archivo exportado.

- **Cuándo se cierra una toma.** No hay un botón "empezar/parar toma" nuevo:
  la toma en curso se cierra sola cuando el presentador hace algo que ya
  hacía antes de esta tarea. `finalizarTomaActual()` centraliza el cálculo
  (mismo tiempo de reloj real que ya usaba `actualizarCronometro()` de T-23,
  congelado en pausa) y se llama desde tres sitios: `volverAlIndice()` (salir
  al índice), `reproducirEscena()` — ANTES de `detenerMotor()`, porque este
  reinicia `escenaActual` a `-1` y `finalizarTomaActual()` necesita leerlo
  todavía — para cubrir `escenaAdyacente()` (cambiar de escena con
  flechas arriba/abajo sin pasar por el índice), y `reiniciarEscenaActual()`
  (tecla `R`). Este último es el cambio de comportamiento deliberado: antes
  `R` solo volvía al bloque 0 sin tocar el cronómetro; ahora cierra la toma
  que se abandona (con el tiempo que llevaba) y arranca el cronómetro de cero
  para la siguiente — "repetir" es, literalmente, cerrar una toma y abrir
  otra, no seguir sumando tiempo a la que fracasó.
- **Marcar la buena y la nota, sin salir de grabación (requisito 2).** Dos
  teclas nuevas en `Configuracion.mapa_teclas_reproductor`, `marcar_toma_buena`
  (`G`/`g`) y `nota_toma` (`N`/`n`) — ningún campo nuevo en `Configuracion`,
  solo dos entradas más en la tupla que ya existía, así que
  `tests/test_skill_md.py` no necesita una fila nueva. `alternarTomaBuena()`
  solo cambia una variable en memoria (`tomaBuenaEnCurso`) y actualiza el
  indicador; `pedirNotaToma()` usa `window.prompt()` (mismo mecanismo que el
  plan B de R-01, reutilizado aquí por primera vez para algo que no es un
  plan B) — un cuadro de diálogo bloqueante, pero que no obliga a salir de la
  vista de reproducción ni a perder el sitio en el guion. Ninguno de los dos
  campos se aplica a ninguna toma ya cerrada: solo se usan cuando
  `finalizarTomaActual()` cierra la toma EN CURSO, y `iniciarMotor()` los
  reinicia (`""`/`false`) al empezar cada toma nueva.
- **Como mucho una toma buena por escena (requisito 1, "marca de CUÁL es la
  buena").** `finalizarTomaActual()` desmarca cualquier toma anterior de la
  misma escena antes de añadir la nueva si `tomaBuenaEnCurso` es `true` — no
  hay ninguna interfaz para desmarcar sin marcar otra en su lugar, decisión
  deliberada: si el dueño se equivocó, la corrección natural es marcar la
  toma correcta, no un tercer estado "sin decidir todavía" para una escena
  que ya se grabó.
- **Persistencia y por qué "Restablecer preferencias" no lo toca.** Mismo
  mecanismo que T-26: `localStorage` con clave
  `teleprompter:<guion>:tomas_escena_<numero>` (por NÚMERO de escena, no
  índice, mismo criterio que `velocidad_escena_<numero>`), `cargarTomasGuardadas()`
  tolerante ante JSON corrupto o con forma inesperada (devuelve `[]`, nunca
  rompe la carga de la página). Se descubrió, verificando a mano, que
  `limpiarPreferenciasAlmacenadas()` (el botón "Restablecer preferencias" de
  T-26) borra TODA clave con el prefijo `teleprompter:<guion>:` — que
  habría incluido el registro de tomas por compartir el mismo espacio de
  nombres, pese a no ser una "preferencia" en ningún sentido razonable
  (perder el parte de rodaje real por pulsar un botón pensado para
  "restablecer tamaño de texto y velocidad" habría sido una pérdida de datos
  silenciosa y sorprendente). Corregido excluyendo explícitamente el prefijo
  `tomas_escena_` de esa limpieza — cubierto por
  `test_guion_js_restablecer_preferencias_no_borra_el_registro_de_tomas`.
- **Estado de la escena, ahora con datos reales (requisito 4).** T-19 dejaba
  "revisada" reservado sin ningún productor real; esta tarea lo cablea:
  `calcularEstadoEscena()` deriva pendiente/grabada/revisada de
  `tomasEscena[indice]` (sin tomas / con tomas sin ninguna buena / con una
  toma buena) en vez del flip manual "pendiente → grabada al primer visitar"
  que tenía `volverAlIndice()` antes. El resumen `N tomas · buena: X` se
  añade como un `<span>` dentro de la fila de la escena — nunca un botón ni
  ningún otro elemento interactivo anidado, porque la fila entera ya es un
  `<button>` (T-19) y anidar controles dentro rompe la semántica HTML; marcar
  la buena solo se hace por teclado, durante la grabación.
- **Volcado a un archivo (requisito 3).** El reproductor no puede escribir en
  la carpeta de salida del guion (cero red en tiempo de ejecución, `file://`);
  el botón **"Exportar parte de rodaje"** (`exportarParteDeRodaje()`,
  `construirParteDeRodaje()`) reutiliza el mismo patrón de descarga que
  "Exportar preferencias" de R-01 (`Blob` + `URL.createObjectURL` +
  `<a download>`, con `window.prompt()` como red de seguridad si la descarga
  falla) — código duplicado a propósito en vez de refactorizado en una
  función común: son dos formatos de exportación distintos con evoluciones
  independientes (preferencias de UI vs. datos de rodaje), y forzar un
  compartido antes de que un segundo caso real lo pida habría sido
  abstracción prematura. Solo se incluyen escenas con al menos una toma. El
  lado Python, `scripts/tomas.py` (`cargar_parte_de_rodaje`/
  `registrar_tomas`), valida el archivo (JSON válido, mismo `guion`, tipos y
  rangos de cada toma) y lo fusiona en `estado.json["tomas"]` — reemplazando
  por escena con lo más reciente exportado, conservando intactas las escenas
  que esa exportación concreta no menciona (una exportación parcial nunca
  borra tomas de una sesión anterior). Contrato completo, con ejemplos:
  `references/contrato-tomas.md`.
- **Migración 002 (`estado.json` versión 2).** `EstadoProyecto` gana el
  contenedor genérico `tomas: dict` (mismo tratamiento que `validacion`
  en la migración 001): vacío hasta que `registrar_tomas` lo rellene. La
  migración solo añade la clave si falta (`setdefault`), así que un
  `estado.json` de un proyecto de guion ya existente la incorpora sin perder
  nada; `VERSION_ESQUEMA_ESTADO` sube de 1 a 2.
- **Verificación.** `tests/test_tomas.py` (nuevo, 15 tests) cubre
  `cargar_parte_de_rodaje` (parte válido, archivo inexistente, JSON inválido,
  guion distinto, escenas/tomas con forma o rangos inválidos, valores por
  defecto de `nota`/`buena`) y `registrar_tomas` (fusiona, ignora escenas sin
  tomas, reemplaza solo la escena exportada preservando el resto, sobrevive a
  un `guardar_estado`/`cargar_estado` real). `tests/test_migraciones.py` gana
  cinco tests para la migración 002 (mismo patrón que los de la 001:
  añade el contenedor, no pierde lo que ya migró la 001, no pisa un `tomas`
  ya presente, idempotente, no muta el dict original) y dos tests existentes
  se actualizan para la nueva versión de esquema. `tests/test_reproductor.py`
  gana nueve tests que comprueban, sobre el HTML generado: las teclas por
  defecto, el registro y su cálculo de duración, la persistencia con clave
  por escena, la regla de una sola toma buena, que reiniciar cierre la toma
  en curso, el estado derivado de las tomas, el botón de exportación, que
  "Restablecer preferencias" no borre las tomas, y el resumen junto a cada
  escena. Verificado de punta a punta con Playwright headless (Chromium, no
  es dependencia del proyecto) sobre un reproductor real generado de
  `fixtures/guion-ejemplo.md`: dos tomas en la escena 1 (la segunda marcada
  buena con la tecla `G` tras reiniciar con `R`), una toma sin marcar en la
  escena 2, el resumen `"2 tomas · buena: 2"` y el badge "Revisada" correctos
  en el índice, "Exportar parte de rodaje" descarga un `.json` válido con
  exactamente esas dos escenas, y reabriendo el MISMO perfil de navegador
  (cerrado y vuelto a abrir de verdad, no una recarga) el resumen de tomas
  sigue intacto — sin errores de consola en ningún paso. El `.json`
  descargado se volvió a cargar con `tomas.cargar_parte_de_rodaje` y a
  fusionar con `tomas.registrar_tomas` sobre un `estado.json` real, confirmando
  el extremo del contrato que la suite automática no puede cubrir sin un
  navegador real: el archivo que exporta el reproductor de verdad es
  aceptado tal cual por el lado Python.

## Marcar tropiezos durante la toma (R-03)

`origen: roadmap`, tercera tarea de la oleada v2, depende de R-02. Objetivo:
capturar en caliente dónde se traba el locutor (requisito 1), volcarlo a
`FEEDBACK.md` (requisito 2) y destacarlo en la siguiente revisión (requisito
3) — conocimiento que hoy se perdía entre la grabación y la revisión. Igual
que R-02, casi entera en `guion.js`/`estilo.css`; el lado Python nuevo,
`scripts/feedback.py`, solo entra en juego cuando el dueño entrega de vuelta
el archivo exportado y cuando se regenera `guion-escenas.md`.

- **Un interruptor inmediato, no un diálogo (requisito 1, "sin interrumpir la
  toma").** `alternarTropiezoBloqueActual()` marca/desmarca el bloque EN
  PANTALLA (`bloqueActual`) en `tropiezosEscena[escenaActual]`, sin pausar el
  automático ni abrir `window.prompt()` — a diferencia de `pedirNotaToma()`
  (R-02), que sí lo hace. Tecla `marcar_tropiezo` (`T`/`t`) nueva en
  `Configuracion.mapa_teclas_reproductor`, mismo patrón que `marcar_toma_buena`/
  `nota_toma`: ningún campo nuevo en `Configuracion`, así que
  `tests/test_skill_md.py` no necesita fila nueva.
- **Por bloque, no por toma.** A diferencia del registro de tomas (que se
  cierra al salir de la escena), un tropiezo marcado vive mientras dure la
  sesión del navegador — no se "cierra" en ningún punto del flujo, solo se
  persiste. El indicador de la cabecera (`#indicador-tropiezo`, "⚠ Tropiezo")
  se recalcula en `actualizarIndicadorTropiezo()`, llamada desde
  `marcarBloqueActivo()` — así sigue al bloque activo: al avanzar a un bloque
  sin marcar desaparece, al volver a uno marcado reaparece, sin estado
  duplicado en ningún otro sitio.
- **Persistencia y por qué "Restablecer preferencias" tampoco lo toca.** Mismo
  mecanismo exacto que R-02: `localStorage` con clave
  `teleprompter:<guion>:tropiezos_escena_<numero>` (por número de escena),
  `cargarTropiezosGuardados()` tolerante ante JSON corrupto o con forma
  inesperada. `limpiarPreferenciasAlmacenadas()` gana un segundo prefijo
  excluido (`prefijoTropiezos`, junto al `prefijoTomas` ya existente de R-02)
  — mismo razonamiento: son datos de grabación reales, no una preferencia de
  interfaz.
- **Resumen en el índice.** Un `<span class="escena-tropiezos">` junto a la
  fila de cada escena (mismo patrón que `.escena-tomas` de R-02), "N
  tropiezo(s)" — no forma parte de ningún requisito literal de R-03, pero es
  el mismo espíritu "de un vistazo" que ya pedía el requisito 4 de R-02;
  decisión de bajo riesgo documentada en `DECISIONES_TECNICAS.md`.
- **Volcado a un archivo (requisito 2), y a un `FEEDBACK.md` que NO es
  `roadmap/FEEDBACK.md`.** El botón **"Exportar tropiezos"**
  (`exportarRegistroTropiezos()`/`construirRegistroTropiezos()`) reutiliza el
  mismo patrón de descarga que R-01/R-02 (`Blob` + `URL.createObjectURL` +
  `<a download>` + `window.prompt()` de red de seguridad), duplicado a
  propósito por el mismo motivo que R-02 documentó (dos formatos de
  exportación con evoluciones independientes). El lado Python,
  `scripts/feedback.py` (`cargar_registro_tropiezos`/
  `registrar_tropiezos_en_feedback`), valida el archivo y añade filas `nuevo`
  a `FEEDBACK.md` **dentro de la carpeta de salida del guion** — un archivo
  distinto de `roadmap/FEEDBACK.md` (la bandeja de historias de usuario del
  propio proyecto teleprompter, gestionada por el ciclo de PM) pese a
  compartir nombre; ver el aviso explícito en
  `references/contrato-tropiezos.md` y en el docstring del módulo. Nunca
  borra ni reescribe una fila existente, solo añade las que faltan (dedup por
  `(escena, indice_bloque, texto)`); copia de seguridad `.bak-<marca>` si el
  archivo ya existía, antes de tocarlo — mismo tratamiento que
  `documento_revision.guardar_documento_revision` con `guion-escenas.md`.
- **"Migración: No" — decisión deliberada de no tocar `estado.json`.** A
  diferencia de R-02 (migración 002, contenedor `tomas`), R-03 no añade nada
  al esquema de estado: `FEEDBACK.md` (carpeta de salida) ES el registro
  persistente, igual que `guion-escenas.md` no necesita una copia en
  `estado.json` para sobrevivir entre sesiones. Ver la entrada correspondiente
  en `DECISIONES_TECNICAS.md` para las alternativas descartadas.
- **Destacado en la siguiente revisión (requisito 3), casado por texto exacto,
  no por índice.** `feedback.tropiezos_marcados_por_escena(carpeta_salida)`
  lee `FEEDBACK.md` y devuelve, por escena, el conjunto de textos todavía en
  estado `nuevo`. `documento_revision.generar_documento_revision` gana el
  parámetro opcional `tropiezos_por_escena` (por defecto `None`, sin cambiar
  el comportamiento de nadie que no lo pase), que se propaga a
  `formatear_escena`/`formatear_bloque_respiracion`: si `bloque.texto`
  coincide con alguno de los marcados de esa escena, se añade una línea
  `> 🎬 **Tropiezo marcado en grabación:**` (mismo tratamiento visual que un
  aviso de T-14, se señala, no se reescribe solo). Casar por texto, no por el
  índice `indice_bloque` que trae el `.json` exportado, es deliberado: el
  índice de un bloque puede desplazarse entre la grabación y la revisión si de
  por medio se acepta una partición de respiración (T-15) — el texto no
  cambia salvo que alguien lo reescriba a propósito, y si ya se reescribió,
  dejar de destacarlo es lo correcto, no un fallo. Cambiar la palabra `nuevo`
  de una fila por cualquier otra en `FEEDBACK.md` (mismo patrón "una palabra
  que el dueño sobrescribe" de T-15/T-16) también apaga el aviso sin tocar el
  texto del bloque.
- **Verificación.** `tests/test_feedback.py` (nuevo, 21 tests) cubre
  `cargar_registro_tropiezos` (registro válido, archivo inexistente, JSON
  inválido, guion distinto, tropiezos con forma o valores inválidos —
  incluido texto con `|` o vacío), `registrar_tropiezos_en_feedback` (crea el
  archivo con cabecera, no duplica en una segunda pasada, añade solo las
  filas nuevas, copia de seguridad si ya existía, no toca el archivo si no
  hay filas nuevas) y `tropiezos_marcados_por_escena` (agrupa por escena, una
  fila resuelta deja de destacarse, una fila añadida a mano por el dueño
  también se respeta). `tests/test_documento_revision.py` gana cuatro tests
  (bloque marcado se destaca, sin `tropiezos_por_escena` no cambia nada,
  tropiezo de otra escena no destaca esta, texto que ya no coincide no
  destaca nada). `tests/test_reproductor.py` gana ocho tests sobre el HTML
  generado (tecla por defecto, alterna sin diálogo, persistencia con clave
  por escena, índice y texto exacto registrados, el indicador sigue al bloque
  activo, botón de exportación, "Restablecer preferencias" no lo borra,
  resumen junto a cada escena). Verificado de punta a punta con Playwright
  headless (Chromium, no es dependencia del proyecto) sobre un reproductor
  real generado de `fixtures/guion-ejemplo.md`: marcar con `T` muestra "⚠
  Tropiezo", avanzar de bloque lo oculta, retroceder lo muestra de nuevo,
  desmarcar con la misma tecla lo quita, el índice muestra "2 tropiezos" tras
  marcar dos bloques, "Exportar tropiezos" descarga un `.json` con
  exactamente esos dos bloques (`indice_bloque` y `texto` correctos), y
  "Restablecer preferencias" no borra la marca — sin errores de consola en
  ningún paso. El `.json` descargado se volvió a cargar con
  `feedback.cargar_registro_tropiezos` y a fusionar con
  `feedback.registrar_tropiezos_en_feedback` sobre `fixtures/salida/`, y el
  bloque marcado apareció destacado al regenerar `guion-escenas.md` con
  `generar_documento_revision(..., tropiezos_por_escena=feedback.tropiezos_marcados_por_escena(...))`
  sobre el mismo guion real — cerrando el contrato de punta a punta, igual que
  hizo R-02 con el parte de rodaje.

## Exportador `.srt` borrador (T-27)

`scripts/srt.py` arranca los subtítulos en la fase de montaje sin partir de cero.
No calcula ningún tiempo por su cuenta: consume `tiempos.ResultadoTiempos.bloques`
tal cual — la única fuente de tiempos del proyecto (T-12, requisito 4) — igual que
ya hace `reproductor.py`. Es una librería pura, sin punto de entrada de CLI todavía
(mismo patrón que `tiempos.py`/`normalizacion.py`: T-30 orquestará cuándo se llama).

- **Texto locutado final, no el original (requisito 4).** `exportar_srt` recibe el
  `ResultadoTiempos` que quien llama ya tenga a mano. Si viene de
  `tiempos.calcular_tiempos` sobre el guion sin editar, el texto es el de origen;
  si viene de `revalidacion.revalidar_guion().resultado_tiempos` — el caso real
  tras un ciclo de revisión —, ya trae las reescrituras aceptadas materializadas
  (T-17). `srt.py` no distingue el origen a propósito: es quien orquesta la
  generación de salidas (T-30) quien decide sobre qué `ResultadoTiempos` exportar,
  el mismo reparto de responsabilidades que ya usan `reproductor.py` y
  `documento_revision.py`.
- **Un subtítulo por bloque, agrupable si es muy corto (requisito 1).**
  `_agrupar_bloques_cortos` funde bloques consecutivos de una misma escena
  mientras la duración acumulada del grupo (`fin_segundos - inicio_segundos`,
  que ya incluye cualquier pausa intermedia) no llegue a
  `Configuracion.srt_duracion_minima_segundos` (1.2 s por defecto) — nunca cruza
  un fin de escena, reconocido por `tiempos.PAUSA_FIN_ESCENA` (promovida de
  privada a pública en esta tarea: es parte del contrato público de
  `BloqueConTiempo.tipo_pausa`, y `srt.py` es su primer consumidor real fuera de
  `tiempos.py`). Con el umbral a `0` cada bloque cierra su propio grupo de
  inmediato: no hace falta un interruptor aparte para desactivar la agrupación.
- **Partición limpia cuando el texto no cabe (requisito 3).** Cada grupo se
  envuelve con `textwrap.wrap(..., break_long_words=False)` — nunca corta una
  palabra a la mitad — en líneas de `Configuracion.srt_caracteres_por_linea_max`
  caracteres (42 por defecto, ya reservada desde T-00) y se pagina en bloques de
  `Configuracion.srt_lineas_max_por_subtitulo` líneas (2 por defecto). Si salen
  más páginas que una, cada página se convierte en su propio subtítulo — nunca se
  trunca ni se descarta una palabra (invariante (a), §0.2) —, y el tiempo del
  grupo se reparte entre las páginas en proporción a sus palabras; la última
  página siempre cierra exactamente en el `fin_segundos` del grupo, sin deriva de
  coma flotante.
- **Formato estándar y consumible por ffmpeg (requisitos 2 y 5).**
  `formatear_marca_tiempo` compone `HH:MM:SS,mmm`; `formatear_srt` serializa
  índice + marca de tiempo + texto + línea en blanco. `guardar_srt` escribe en
  UTF-8 (`utf-8-sig` si `Configuracion.srt_con_bom=True`, pensado para editores de
  subtítulos en Windows que lo prefieren) dentro de la carpeta de salida del guion
  (`guion.srt`, regla de aislamiento). `validar_srt` aplica las mismas reglas que
  un lector estricto tipo ffmpeg — índice secuencial desde 1, marca de tiempo bien
  formada con el fin posterior al inicio, sin solapes ni tiempos decrecientes
  entre subtítulos consecutivos, ninguna línea por encima del límite configurado —
  y es la misma función que usan tanto la suite (`tests/test_srt.py`) como la
  cuarta red (`verificar_salidas.py`, ver más abajo).
- **Verificación.** `tests/test_srt.py` cubre: formato de la marca de tiempo
  (incluido el redondeo al milisegundo); el `.srt` de los tres guiones reales pasa
  `validar_srt` sin ningún problema, no solapa y su último subtítulo termina
  exactamente en `duracion_total_segundos` (criterio de aceptación de T-27);
  ninguna línea supera `srt_caracteres_por_linea_max` en los tres guiones reales
  (reemplaza al talón de T-03 en `test_logica_pendiente.py`); casos unitarios de
  `validar_srt` (índice no secuencial, marca mal formada, solape, fin anterior al
  inicio); agrupación de bloques cortos sin cruzar un fin de escena, a un ritmo
  deliberadamente rápido y sin pausas para aislar el efecto; partición limpia de
  un bloque que no cabe en el límite de líneas/caracteres, verificando que la
  reconstrucción de todas las palabras de todas las entradas coincide exactamente
  con el texto de origen y que los tiempos no solapan; el caso completo de
  requisito 4 (una cifra con una reescritura de forma dicha aceptada vía
  `revalidacion.revalidar_guion`: el `.srt` lleva "dos mil veintiséis", nunca
  "2026"); escritura a disco con y sin BOM. `verificar_salidas.py --fixture`
  genera y valida el `.srt` de verdad sobre el mismo guion real que usa el
  reproductor (`generar_srt_fixture`/`verificar_srt`, activadas en esta tarea:
  antes eran NO APLICABLE a la espera de T-27).

## Exportador `.pdf` con identidad 480 (T-28)

`scripts/pdf.py` genera el documento de repaso/entregable con la marca 480
(`references/marca-480.md`). Igual que `srt.py` (T-27), es una librería pura sin
punto de entrada de CLI todavía: consume `ResultadoParseo` + `ResultadoTiempos` tal
cual, sin recalcular nada — el texto de cada bloque ya es el locutado final si
`resultado_tiempos` viene de una revalidación (T-17). A diferencia de
`documento_revision.py` (T-16), este módulo **nunca** muestra el aparato de
reescrituras (`<!-- reescritura ... -->`, original/propuesta/decisión): esa vista
de edición vive en `guion-escenas.md`; aquí solo hay texto ya decidido, en prosa
legible, en las dos variantes del documento.

- **Plantillas en `assets/pdf/`, mismo patrón que el reproductor (T-18).**
  `plantilla.html` + `estilo.css` con marcadores `__EN_MAYUSCULAS__` sustituidos por
  `.replace()` desde `Configuracion` — nada de HTML/CSS escrito a mano en Python.
- **Logotipo autocontenido y con ratio medido (requisito 3).** `dimensiones_png`
  lee la cabecera `IHDR` del PNG (firma + longitud + tipo de chunk + ancho/alto en
  big-endian, bytes 16-24) sin ninguna dependencia de imagen; `_logo_html` calcula
  `alto = ancho_deseado / (ancho_px/alto_px)` y lo incrusta como
  `data:image/png;base64,...`. Es deliberado que sea `data:` y no una ruta relativa
  al archivo: `verificar_salidas.buscar_recursos_externos` rechaza **cualquier**
  `src=` que no sea `data:`, aunque apunte a un archivo local — un `.html`
  autocontenido no depende de ningún archivo aparte, ni siquiera del propio
  proyecto. Si el PNG no existe o su cabecera no es válida, `_logo_html` devuelve
  `""` (ningún `<img>` en el marcado) y la generación sigue sin fallar.
- **Notas internas vs. indicaciones de pantalla (requisito 6, modo
  `--para-terceros`).** `es_nota_interna` detecta el rótulo `NOTA` dentro del
  `motivo` de clasificación que ya calcula `clasificador.py` (T-09) — que siempre lo
  cita literalmente (`"rotulo 'NOTA': ..."`, `"prefijo 'NOTA:'"`) —; cualquier otra
  indicación (`EN PANTALLA`, o ambigua sin señal clara) se trata como indicación de
  pantalla y se mantiene siempre, para no decidir en silencio que algo sin marcar
  como nota es prescindible (T-09, requisito 5). `Configuracion.incluir_notas_internas`
  (reservada desde T-00, sin cablear hasta T-28) es el interruptor — el mismo que
  reutiliza T-29 —: `False` es el modo `--para-terceros`. `es_nota_interna` e
  `indicaciones_no_recitables` pasan de privadas a públicas en T-29, que las
  reutiliza tal cual en `pptx.py` en vez de duplicar la heurística — ver su propia
  sección más abajo.
- **Prosa continua, no lista (requisito 5).** `_prosa_escena` envuelve cada bloque
  de respiración en su propio `<span class="bloque">`; el límite entre bloques lo
  marca `estilo.css` con `.bloque:not(:last-child)::after { content: " · "; }` — un
  separador tipográfico discreto, nunca un `<li>` ni un salto de línea que rompa la
  lectura como prosa.
- **Una escena por página (criterio de aceptación).** `.pagina { page-break-after:
  always }` con `:last-child { page-break-after: auto }`; Chrome en modo impresión
  respeta el `@page` de `estilo.css` (tamaño, márgenes) al convertir a `.pdf`. El
  número de páginas resultante es siempre escenas + 1 (portada), verificado tanto
  contando `class="pagina"` en el HTML como — cuando hay Chrome disponible —
  contando `/Count N` en los bytes crudos del `.pdf` generado (el árbol de páginas
  de Chrome no usa flujos comprimidos para ese objeto).
- **Chrome/Edge headless, nunca obligatorio (requisito 4).**
  `detectar_ejecutable_chrome` prioriza `Configuracion.pdf_chrome_ejecutable_manual`
  si el dueño la fija; si no, nombres conocidos vía `shutil.which` (cubre Linux/macOS
  con Chrome o Chromium instalados de forma estándar) y las rutas de instalación
  estándar de Windows/macOS, incluida la instalación por usuario en
  `%LOCALAPPDATA%`. `convertir_html_a_pdf` invoca
  `chrome --headless --disable-gpu --no-pdf-header-footer --print-to-pdf=...`
  con un `subprocess.run` acotado en tiempo (`pdf_timeout_conversion_segundos`,
  mismo criterio que `TIEMPO_PROCESO_MAX_SEGUNDOS` de T-06); **decisión verificada
  en esta sesión** (sandbox de nube, root): Chrome se niega a arrancar como root sin
  `--no-sandbox` (`Running as root without --no-sandbox is not supported`), así que
  el argumento se añade solo cuando `os.geteuid() == 0` — en la máquina del dueño,
  sin privilegios de administrador, ese bloque nunca se activa. Sin ejecutable
  detectado, o si la conversión falla por cualquier motivo, `exportar_pdf` nunca
  lanza: deja el HTML de impresión listo y un mensaje accionable ("abre
  `guion-impresion.html` y usa Ctrl+P").
- **Verificación.** `tests/test_pdf.py` cubre: lectura de la cabecera `IHDR` del
  logotipo real (1993×805, ratio 2,4758) y de un PNG ausente/inválido; el número de
  páginas coincide con escenas + portada en los tres guiones reales; auto-contención
  de bytes en los tres guiones reales (incluido el logotipo incrustado); ausencia
  del logotipo sin romper la generación; la prosa nunca usa `<li>`/`<ul>`; portada
  con título/duración/escenas/palabras; el modo `--para-terceros` omite la nota
  interna real de `fixtures/reales/guion-artefactos-lienzo.md` sin tocar las
  indicaciones de pantalla; detección de Chrome con ruta manual válida/inválida;
  conversión con un ejecutable inexistente (no lanza); y, cuando hay un Chrome/Edge
  real disponible (detección automática o el Chromium de Playwright de este
  entorno, nunca una dependencia del proyecto), generación real del `.pdf` con el
  número de páginas correcto y sin la nota interna en modo `--para-terceros`.
  `verificar_salidas.py --fixture` genera el HTML de impresión (y el `.pdf` si hay
  Chrome) de verdad sobre el mismo guion real que usan el reproductor y el `.srt`
  (`generar_pdf_fixture`, activada en esta tarea), y `verificar_autocontencion` gana
  un parámetro `etapa` para reutilizarse también aquí, no solo con el reproductor.

## Adaptador `.pptx` con identidad 480 (T-29)

`scripts/pptx.py` **no genera ningún `.pptx`**. Verificado con el `SKILL.md` de
`480-branded-pptx`: esa skill son instrucciones para Claude, no un ejecutable —
genera el `.pptx` con Node + `pptxgenjs` apoyándose en la skill `pptx`, y exige QA
visual, así que invocarla como subproceso no es una opción. El reparto es: este
módulo produce `tarjetas.json` (el contrato, `references/contrato-tarjetas.md`) y
`brief-pptx.md` (el brief de invocación en Markdown); es Claude quien genera el
`.pptx` de verdad, delegando en esa skill dentro de la misma sesión, leyendo ambos
archivos. Mismo patrón de entrada que `srt.py`/`pdf.py`: consume `ResultadoParseo` +
`ResultadoTiempos` tal cual, sin recalcular nada.

- **Reutiliza `pdf.py` en vez de duplicar, tres funciones promovidas de privadas a
  públicas en esta tarea** (mismo patrón que `tiempos.PAUSA_FIN_ESCENA` en T-27):
  `dimensiones_png` (mide la relación de aspecto real del logotipo para la tabla de
  alturas del brief), `es_nota_interna` e `indicaciones_no_recitables` (separan
  indicaciones de pantalla y notas internas con el mismo criterio que el `.pdf`).
  `pptx.py` no importa nada privado (`_`) de otro módulo.
- **`Tarjeta`/`ResultadoTarjetas` → `tarjetas_a_diccionario` → JSON.** Los
  dataclasses son la representación tipada; `tarjetas_a_diccionario` es la única
  función que conoce la forma exacta del JSON (documentada en
  `references/contrato-tarjetas.md`), y `validar_tarjetas` valida contra esa misma
  forma — mismo patrón de "una función serializa, otra valida a mano" que
  `srt.validar_srt` (T-27), sin depender de `jsonschema` (§0.2, sin dependencias de
  terceros).
- **`--para-terceros` vacía `notas_internas` en el propio JSON, no solo en la
  presentación (requisito 3).** `_indicaciones_de_escena` devuelve `()` para las
  notas internas en cuanto `Configuracion.incluir_notas_internas` es `False`, antes
  de que el dato llegue a `Tarjeta` — a diferencia del `.pdf`, que solo las omite al
  maquetar. Decisión deliberada: el JSON es un contrato que puede consumir cualquier
  cosa, no solo esta skill; si las notas internas siguieran en el JSON "por si
  acaso", cualquier consumidor futuro del modo `--para-terceros` podría filtrarlas
  mal y exponerlas.
- **El brief corrige por escrito el `SKILL.md` de la skill de marca (requisito 2).**
  `_relacion_aspecto_texto` mide el ratio real del logotipo con `dimensiones_png`
  (mismo archivo que usa el `.pdf`, `ruta_logo_pdf`) y `_tabla_alturas_logo_markdown`
  calcula las alturas correctas para los tres anchos de referencia de
  `references/marca-480.md` (portada, header de contenido, cierre) — nunca la
  constante `668/376` de la guía. El texto de la corrección de tipografía (Poppins,
  no Figtree) es literal, no derivado de ningún dato.
- **Agrupación configurable (requisito 2) e índice condicional.**
  `_agrupar_tarjetas` reparte las tarjetas en grupos de
  `Configuracion.pptx_escenas_por_diapositiva` (1 por defecto — una diapositiva por
  escena, que es además el criterio de aceptación literal de la tarea: "el brief ...
  describe tantas diapositivas de contenido como escenas"); el brief solo incluye la
  diapositiva de índice si el número de grupos alcanza
  `Configuracion.pptx_umbral_indice_secciones` (4 por defecto, de
  `references/marca-480.md`: "solo si hay 4+ secciones"). No hay diapositivas
  separadoras: esta skill no agrupa escenas en bloques mayores que la propia
  escena, así que ese elemento de la estructura de deck simplemente no aplica —
  documentado como tal en el propio brief, nunca omitido en silencio.
- **Detección de disponibilidad, nunca un fallo (requisito 4).**
  `detectar_skill_pptx_disponible` solo comprueba que
  `Configuracion.ruta_skill_marca_pptx` y `ruta_skill_pptx_base` existen como
  carpetas (`Path.is_dir()`, con `expanduser()` para `~`) — nunca su contenido, eso
  es responsabilidad de esas skills. `exportar_pptx` genera y guarda
  `tarjetas.json`/el brief siempre, y solo cambia el mensaje devuelto
  (`ResultadoPptx.mensaje`, `skill_disponible`) según el resultado de esa detección.
  En una sesión de nube, sin `~/.claude/skills/`, es siempre `False`: la salida
  `.pptx` queda latente, tal como exige el criterio de aceptación de la tarea.
- **Verificación.** `tests/test_pptx.py` cubre: una tarjeta por escena; separación
  correcta de indicaciones de pantalla y notas internas; el modo `--para-terceros`
  vaciando `notas_internas` en el propio diccionario serializado; `validar_tarjetas`
  detectando clave ausente, tipo incorrecto, `numero_escenas` inconsistente y una
  escena totalmente vacía; el criterio de aceptación literal (tantas diapositivas de
  contenido como escenas) sobre un guion de prueba y sobre los tres guiones reales;
  las correcciones de Poppins/relación de aspecto presentes en el brief; el umbral
  de índice condicional en ambos sentidos; la agrupación configurable fundiendo dos
  escenas en una diapositiva; y `detectar_skill_pptx_disponible`/`exportar_pptx` en
  sus tres combinaciones (ninguna carpeta, una sola, las dos). `verificar_salidas.py
  --fixture` genera `tarjetas.json` y el brief de verdad sobre el mismo guion real
  que usan el reproductor, el `.srt` y el HTML de impresión
  (`generar_pptx_fixture`), y valida el JSON contra el contrato
  (`verificar_tarjetas_json`).

## Selector de salidas por validación (T-30)

`scripts/salidas.py` ata en una sola canalización los cuatro generadores ya
completos (`reproductor.py` T-18, `srt.py` T-27, `pdf.py` T-28, `pptx.py`
T-29) sin duplicar ni una línea de lo que cada uno ya hace — ni siquiera
recibe el guion en bruto: consume `ResultadoParseo` + `ResultadoTiempos` tal
cual, igual que los cuatro módulos que orquesta.

- **La pregunta es datos, no un `input()`.** `construir_pregunta_salidas`
  devuelve una `PreguntaSeleccionSalidas` (cuatro `OpcionSalida`, cada una con
  su `sugerida`) para que Claude la formule al dueño dentro de la sesión —
  mismo patrón que `parser.DeteccionEscenasAmbiguaError` (T-08): la
  ambigüedad/pregunta se deja como estructura de datos, nunca como una espera
  bloqueante de terminal, porque esta skill no tiene ni tendrá una CLI
  interactiva propia. La respuesta vuelve ya decidida como `SeleccionSalidas`.
- **La sugerencia lee el histórico, nunca decide en su lugar (requisito 2).**
  `_ultima_seleccion` recorre `estado.salidas_generadas` (contenedor genérico
  reservado desde T-07: T-30 no necesita migración) de atrás hacia delante
  buscando la última entrada con clave `"seleccion"`; sin ninguna, sugiere las
  cuatro salidas. Ignora sin romperse cualquier entrada ajena sin esa clave —
  el contenedor es compartido y su forma interna la va fijando cada tarea que
  lo usa.
- **Generación independiente (requisito 3): un `try`/`except` por salida.**
  `generar_salidas_seleccionadas` recorre las cuatro en orden fijo; la que no
  está en la selección queda `SalidaOmitida` con motivo neutro, y cualquier
  excepción real de un generador se captura y también se convierte en
  `SalidaOmitida` (con el mensaje de la excepción) en vez de propagarse y
  tumbar las demás. La latencia que ya devuelven `pdf.exportar_pdf`
  (`ruta_pdf is None`) y `pptx.exportar_pptx` (`skill_disponible=False`) se
  traduce en `SalidaLatente`, una categoría aparte que nunca se confunde con
  un fallo: el HTML de impresión y `tarjetas.json`/el brief son archivos
  reales ya en disco aunque el `.pdf`/`.pptx` final quede pendiente.
- **`ResumenSalidas` es el resumen final (requisito 4).** Tres listas —
  `generadas` (`ArchivoGenerado`: tipo, ruta, tamaño ya leído de disco),
  `omitidas` y `latentes` (ambas con motivo) — más `como_dict()` para anexar
  a `estado.salidas_generadas` (`registrar_generacion`, append-only) y
  `mostrar_resumen()` para pintarlo por `presentacion.py`. Un mismo `TipoSalida`
  puede aparecer a la vez en `generadas` y en `latentes` (el `.pdf` y el
  `.pptx` son los dos casos reales): son listas independientes, no una
  máquina de estados con un único resultado por tipo.
- **`verificar_salidas.py` gana la etapa "Generación de salidas" (antes NO
  APLICABLE, ver T-00/hallazgo #4).** Selecciona las cuatro salidas sobre el
  mismo guion real que usan las demás etapas; el detalle incluye cuántos
  archivos se generaron y, si las hay, las latencias con su motivo — nunca
  falla por una latencia esperada (Chrome/Edge o la skill de marca ausentes
  en la máquina de verificación), solo por un `SalidaOmitida` real (fallo de
  código) entre las cuatro seleccionadas.
- **Verificación.** `tests/test_salidas.py` cubre: la sugerencia por defecto
  (las cuatro) y tras un histórico; una entrada de estado sin clave
  `"seleccion"` no rompe la búsqueda; las no seleccionadas quedan omitidas sin
  generar archivo; el fallo simulado de un generador (monkeypatch) no impide
  las demás; el criterio de aceptación literal (con el `.pptx` latente, las
  otras tres se generan igualmente y el resumen lo refleja); dos validaciones
  seguidas sobre el mismo `estado.json` en disco (`guardar_estado`/
  `cargar_estado` de por medio) preguntan las dos veces, cada una sugiriendo
  la selección de la pasada anterior; y `registrar_generacion` como
  append-only sobre varias pasadas.

## `SKILL.md` y configuración completa (T-31)

`SKILL.md` deja de tener un extracto de valores por defecto y pasa a tener la tabla
completa de los 81 campos de `Configuracion` (`scripts/config.py`), agrupada por área
en la sección «Valores por defecto — tabla completa (T-31)».

- **El test que impide que el código y la documentación diverjan es
  `tests/test_skill_md.py`.** Compara, en las dos direcciones,
  `{campo.name for campo in dataclasses.fields(Configuracion)}` contra las claves
  citadas entre backticks dentro de esa sección (delimitada buscando el siguiente
  encabezado `## ` real — cuidado, no cualquier `###`, ver `_PATRON_SIGUIENTE_H2`).
  **Si añades un campo nuevo a `Configuracion`, añade su fila en esa tabla en el
  mismo commit** o `test_toda_clave_de_configuracion_esta_documentada_en_skill_md`
  falla; si renombras o quitas uno, quita también su fila o
  `test_skill_md_no_documenta_una_clave_que_ya_no_existe_en_configuracion` falla.
- **Qué NO entra en esa comparación.** `PATRON_ENCABEZADO_ESCENA` (contractual con el
  dueño, no una decisión de sesión) y las tablas completas de sustitución
  (`SIMBOLOS_MONEDA`, `UNIDADES_ABREVIADAS`, `ANGLICISMOS_COMUNES`) son constantes de
  módulo que nunca se mirroriaron como campo de `Configuracion` (decisión ya tomada en
  T-13/T-14, ver `DECISIONES_TECNICAS.md`): siguen documentadas por nombre en
  `SKILL.md`, pero fuera de esta tabla y de este test.
- **Documentación extensa movida a `references/` (requisito 4), no a `SKILL.md`.**
  Tres archivos nuevos: `convencion-guion.md` (T-08 a T-10), `formato-guion-escenas.md`
  (T-15 a T-17) y `mapa-teclas.md` (T-24). `SKILL.md` conserva solo el resumen y un
  enlace («Ver también») desde cada sección correspondiente; el detalle y los casos
  límite viven en el archivo de `references/`.
- **Precedencia de configuración (requisito 3) documentada, no implementada.** Esta
  skill no tiene un cargador de "configuración de usuario" ni de "configuración de
  proyecto" como archivo propio — no existe todavía una CLI (ver la decisión de T-30
  sobre por qué no habrá `argparse`/`input()`): los cuatro niveles son conceptuales,
  y el mecanismo real hoy es que Claude construye `Configuracion(**overrides)` en la
  sesión. `configuracion_efectiva` dentro de `estado.json` (T-07) ya cumple el papel
  de "configuración del proyecto de guion" sin necesitar nada nuevo.

## Instalación de la skill y guion de ejemplo (T-32)

El "deploy" de este proyecto (§0.1): no hay servidor que reiniciar, hay una carpeta
de skill que sincronizar en `~/.claude/skills/teleprompter/`.

- **`scripts/instalar_skill.py`** copia el paquete distribuible —`SKILL.md`,
  `scripts/`, `assets/`, `references/` y `fixtures/guion-ejemplo.md`, la constante
  `ENTRADAS_PAQUETE`— al destino (`--destino`, por defecto
  `config.RUTA_INSTALACION_SKILL`, `~/.claude/skills/teleprompter`). Fuera del
  paquete queda todo lo de desarrollo/gobierno del propio repositorio (`tests/`,
  `roadmap/`, `.github/`, `DEVELOPERS.md`): no tiene sentido en una copia instalada
  y ningún dueño lo ejecuta. Si `--destino` ya existe (una instalación previa), se
  renombra primero a `<nombre>.bak-<marca_de_tiempo>` en vez de sobrescribirse in
  situ (invariante (d) de §0.2, mismo patrón que
  `documento_revision.guardar_documento_revision`), y la copia nueva se escribe
  desde cero: **actualizar es respaldar y reinstalar completo, nunca un sync
  incremental** (más simple y sin estados intermedios que auditar).
- `RUTA_INSTALACION_SKILL` (`config.py`) es una constante de módulo, no un campo de
  `Configuracion`: no afecta al procesado de ningún guion, y ya es configurable con
  `--destino`. Mismo tratamiento que los `NOMBRE_ARCHIVO_*` — no todo default pasa
  por el dataclass ni por el test de completitud de T-31.
- **Nota de entorno (v1.3): una sesión de nube no alcanza el `~/.claude/skills/`
  real del dueño.** `tests/test_instalar_skill.py` prueba el mecanismo de verdad
  —qué copia, que hace copia de seguridad en vez de sobrescribir, y que la copia
  resultante ejecuta su propio health check como subproceso aislado
  (`test_health_check_funciona_ejecutado_desde_la_copia_instalada`, requisito 3 de
  T-32 literal)— pero siempre contra un `tmp_path`, nunca contra la ruta real. Una
  sesión local o el propio dueño son quienes ejecutan
  `python scripts/instalar_skill.py` de verdad; hacerlo aquí contra la ruta real no
  sería una instalación, solo su apariencia.
- **`fixtures/guion-ejemplo.md`** es el guion de curso sintético (locución + `EN
  PANTALLA` + `NOTA` interna + B-roll + timestamps) que usan tanto el health check
  como los tests de regresión, para no depender de los guiones reales de
  calibración del dueño (que son suyos, no un ejemplo público del paquete). Está
  calibrado a propósito para que su `Duración objetivo` no dispare el aviso de
  desviación de T-12: un fixture pensado para enseñar el formato de salida no debe
  arrastrar ruido de un aviso que ya prueba `tests/test_tiempos.py` por su cuenta.
  `fixtures/guion-ejemplo-esperado.md` es su versión anotada esperada (el
  `guion-escenas.md` que produce hoy la canalización completa de T-08 a T-16):
  `tests/test_fixture_ejemplo.py::test_guion_ejemplo_genera_exactamente_la_version_esperada`
  es un test de regresión byte a byte — si cambias a propósito el formato del
  documento de revisión, regenera este archivo en la misma sesión ejecutando la
  canalización a mano (ver el docstring del test para la receta exacta), nunca
  edites el test para que pase sin mirar el diff.
- **`verificar_salidas.py` usa ahora `fixtures/guion-ejemplo.md` como guion de
  verificación** (`_ruta_guion_para_verificar`), con el primer guion real de
  `fixtures/reales/` como respaldo si el de ejemplo no existiera. Antes de esta
  tarea usaba siempre el primer guion real porque `guion-ejemplo.md` no existía
  todavía (T-32 es quien lo crea); la etapa "Guion de ejemplo" pasa de NO
  APLICABLE a OK con este mismo cambio.

### Arquitectura y mapa de módulos

El pipeline es una cadena de funciones puras sobre dataclasses, sin clases con
estado ni un orquestador central: cada tarea añadió su propio módulo en
`scripts/` y el siguiente consume el resultado del anterior sin recalcular nada.
En orden real de dependencia:

```
entrada.py        valida ruta/tamaño/codificación del .md, deriva la carpeta de salida
estado.py         estado.json (persistencia entre sesiones, hash del guion, migraciones)
parser.py         separa el .md en Escena (encabezados ## BLOQUE N, secciones auxiliares)
clasificador.py   separa cada escena en locución / no-locución (rótulos + inferencia)
troceo.py         trocea la locución en BloqueRespiracion (bloques de respiración)
  ├── tiempos.py       calcula inicio/fin/pausa de cada bloque (ppm deducido o manual)
  ├── deteccion.py     avisa problemas de lectura en voz alta, por bloque
  └── normalizacion.py propone la forma dicha (cardinales, monedas, siglas...)
reescrituras.py   une detección + normalización en Reescritura (id estable, aceptar/rechazar)
documento_revision.py  compone todo lo anterior en guion-escenas.md (una sola pasada)
revalidacion.py   relee guion-escenas.md, respeta ediciones manuales, recalcula tiempos
reproductor.py / srt.py / pdf.py / pptx.py   generan cada salida a partir de
                                              ResultadoParseo + ResultadoTiempos
salidas.py        selector: las cuatro salidas a la vez, fallo/latencia aislados por salida
```

`config.py` es el único módulo sin lógica de negocio: todo valor por defecto vive
ahí (regla "sin números mágicos", §0.2), y `Configuracion` es el dataclass
congelado que viaja por toda la cadena. `presentacion.py` es la única capa
autorizada a escribir en la salida estándar; `logger.py` y `monitorizacion.py` son
infraestructura transversal (log a archivo, captura y resumen de excepciones), no
parte de la cadena de datos. `verificar_salidas.py` no es un módulo de la skill:
es la cuarta red de verificación, ejecuta la cadena completa sobre
`fixtures/guion-ejemplo.md` y comprueba las salidas.

### Cómo añadir una regla nueva

Las tres familias de "regla" del proyecto —clasificación, normalización, aviso de
detección— siguen el mismo patrón general: **constante(s) de comportamiento en
`config.py`, función pura que las aplica, y su fila nueva en la tabla de
`SKILL.md`** (o en la tabla dedicada de `references/` si la familia ya tiene su
propia tabla, como las de normalización y detección). Nunca una regla nueva vive
solo en el código: `tests/test_skill_md.py` falla si añades un campo a
`Configuracion` sin documentarlo.

- **Regla de normalización nueva** (`normalizacion.py`, familia `FAMILIA_*`): añade
  el patrón/tabla de sustitución como constante en `config.py` (mismo patrón que
  `SIMBOLOS_MONEDA`/`UNIDADES_ABREVIADAS`/`ANGLICISMOS_COMUNES`), define su
  constante `FAMILIA_<NOMBRE>` y añade un bloque numerado nuevo dentro de
  `normalizar_texto` —respetando el orden de prioridad ya documentado en su
  docstring: diccionario del dueño primero, después las familias automáticas, las
  conjunciones al final— que llame a `agregar(inicio, fin, familia, motivo,
  propuesta)`; `agregar` ya descarta solapes con lo que una familia anterior
  ocupó, así que una regla nueva no puede pisar a una con más prioridad. Añade la
  fila a la tabla de `SKILL.md` (sección de normalización) y tests con un caso
  positivo y un contraejemplo que no debe dispararla.
- **Regla de aviso/detección nueva** (`deteccion.py`, familia `FAMILIA_*`): añade
  sus umbrales a `config.py` y como campos de `Configuracion` (documentados en la
  tabla de `SKILL.md`), escribe una función `_detectar_<nombre>(bloque:
  BloqueRespiracion, configuracion: Configuracion) -> list[Aviso]` que **solo
  avisa, nunca reescribe** (alcance decidido por el dueño en §0.2 — la única
  excepción histórica es "sin punto de respiración", que puede sugerir partición
  porque afecta al troceo), añádela a la lista de `detectar_problemas_bloque`, y
  documenta la familia en la tabla de detección de `SKILL.md`. Criterio de
  aceptación de T-14, todavía vigente para cualquier familia nueva: un test que la
  detecta y un contraejemplo que no dispara falso positivo.
- **Regla de clasificación nueva** (`clasificador.py`): si es un **rótulo nuevo**
  explícito (como `**LOCUCIÓN**`/`**EN PANTALLA**`/`**NOTA**`), añádelo a
  `ROTULOS_NO_LOCUCION` (o crea su propia constante si necesita tratamiento
  distinto) en `config.py` y cablea su reconocimiento en `_localizar_rotulos`/
  `_clasificar_seccion_locucion`; documenta el rótulo en la tabla de convención de
  `SKILL.md` y en `references/convencion-guion.md`. Si es una **heurística de
  inferencia** nueva (para cuando el guion no trae rótulo explícito), extiende
  `_inferir_tipo_parrafo` sin romper la decisión permanente del dueño (§0.2,
  pregunta 3 de `SEGUIMIENTO.md`): los rótulos mandan siempre que existan, la
  inferencia solo entra en su ausencia, y una escena que se sale de la convención
  se marca como desviación (nunca como error) vía `detectar_desviaciones` de
  `convencion.py`.

## Encaje con la cadena de montaje de vídeo (T-33)

Tarea puramente de **contrato y verificación**: no añade ninguna salida nueva, solo
documenta y comprueba que las dos que ya existen (`.srt` de T-27, `tarjetas.json` de
T-29) son suficientes y consistentes entre sí para que una skill de montaje externa
las consuma sin ambigüedad. El contrato completo vive en
`references/contrato-montaje.md`; el resumen operativo, en la sección «Donde encaja»
de `SKILL.md`.

- **Numeración de escena estable y predecible (requisito 2):** hasta esta tarea,
  `parser.py` aceptaba el `numero` capturado del encabezado `## BLOQUE N — <título>`
  tal cual, sin comprobar que fuera único ni creciente — un guion con dos escenas
  `BLOQUE 2` habría generado igual, sin ningún aviso, dos tarjetas con el mismo
  número en `tarjetas.json`. `convencion._desviaciones_numero_escena` (nueva,
  llamada desde `detectar_desviaciones`) recorre `resultado.escenas` en orden de
  documento (ya vienen ordenadas por `linea_inicio`, T-08) y añade dos tipos de
  `Desviacion` — `numero_escena_duplicado` (el número ya apareció antes) y
  `numero_escena_no_creciente` (es menor o igual que el de la escena anterior, sin
  ser un duplicado exacto) — sin bloquear el proceso, mismo patrón que el resto de
  `detectar_desviaciones` (T-10): la escena se sigue generando con su número tal
  cual, solo se informa.
- **`tests/test_integracion_montaje.py`** (requisito 3) es el primer test que genera
  `.srt` y `tarjetas.json` a partir del **mismo** `ResultadoTiempos` de un guion real
  y comprueba que son consistentes entre sí, no solo que cada uno pasa su propio
  validador por separado (eso ya lo cubrían `test_srt.py`/`test_pptx.py`): cero
  desviaciones de numeración de escena, el `.srt` se valida sin avisos (criterio de
  aceptación literal), `tarjetas.json` cumple su esquema, el fin del último subtítulo
  coincide exactamente con `duracion_total_segundos` de `tarjetas.json`, y el orden
  de `numero` en ambas salidas es el mismo que en el guion de origen.
- **Por qué no se añadió un `inicio_segundos`/`fin_segundos` absoluto por escena a
  `tarjetas.json`:** ver la fila correspondiente de `DECISIONES_TECNICAS.md` — es
  derivable sin ambigüedad sumando `duracion_estimada_segundos` en orden, así que
  añadirlo habría sido una segunda fuente de verdad sobre el mismo dato que ya
  calcula `tiempos.calcular_tiempos` (T-12).
- Esta tarea **no** implementa tomas por escena, recalibrado con tiempos reales de
  grabación ni alineación real del `.srt` con la toma buena — eso es `R-02`, `R-04` y
  `R-05` de `roadmap/ROADMAP_PRODUCTO.md`, los tres todavía `PENDIENTE`.

## Suite de tests (T-03)

`tests/conftest.py` expone `guiones_reales` y `texto_guiones_reales`: acceso de una sola
vez a los tres guiones de calibración de `fixtures/reales/`. Úsalas en vez de rutas
sueltas si tu test necesita texto de guion real.

`tests/test_logica_pendiente.py` reúne, con `@pytest.mark.skip(reason=...)`, los tests
de la lógica de producto que T-03 debía cubrir pero que todavía no existe (por ahora,
solo el exportador `.srt` de T-27; el parser de T-08, el clasificador de T-09, el
troceador de T-11, el motor de tiempos de T-12 y la idempotencia de la revalidación de
T-17 ya no están aquí como `skip`, ver `tests/test_parser.py`,
`tests/test_clasificador.py`, `tests/test_troceo.py`, `tests/test_tiempos.py` y
`test_invariante_idempotencia_de_la_revalidacion` en este mismo archivo). Cada `skip`
nombra la tarea que lo desbloquea y describe, en el docstring, lo que el test debe
comprobar. Al implementar esa tarea: quita el `skip` y escribe el test descrito como
parte de su propio criterio de aceptación — no lo dejes como nota aparte.

## Estructura

- `scripts/` — código de la skill (biblioteca estándar únicamente).
- `scripts/hooks/` — plantillas de git hooks versionadas; instálalas con `instalar_hooks.py`.
- `scripts/migraciones/` — migraciones idempotentes del esquema de `estado.json`.
- `scripts/instalar_skill.py` — instala/actualiza la skill en `~/.claude/skills/teleprompter/` (T-32).
- `tests/` — suite de pytest.
- `fixtures/` — `fixtures/reales/` (guiones de calibración del dueño) y
  `fixtures/guion-ejemplo.md` + `fixtures/guion-ejemplo-esperado.md` (guion de
  ejemplo del paquete distribuible y su versión anotada esperada, T-32), ambos
  usados por `verificar_salidas.py --fixture`.
- `assets/` — logotipos de marca 480, `assets/reproductor/` (plantillas del reproductor: `plantilla.html`, `estilo.css`, `guion.js`) y `assets/pdf/` (plantillas del HTML de impresión).
- `references/` — documentación de referencia: marca 480 (`marca-480.md`), contrato `tarjetas.json` (`contrato-tarjetas.md`), contrato de encaje con la cadena de montaje (`contrato-montaje.md`, T-33), convención de marcado del guion (`convencion-guion.md`), formato de `guion-escenas.md` (`formato-guion-escenas.md`) y mapa de teclas del reproductor (`mapa-teclas.md`).
- `roadmap/` — el registro de gobierno del proyecto: `SEGUIMIENTO.md` es el hub.

## Convenciones de rama

Se trabaja siempre en `develop`. `master` es del dueño del proyecto: nunca se commitea,
mergea ni empuja ahí. Ver `roadmap/HOJA_DE_RUTA.md` §0.1 para el protocolo completo.
