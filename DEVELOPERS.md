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
- `tests/` — suite de pytest.
- `fixtures/` — guiones de calibración y de ejemplo para las verificaciones.
- `assets/` — logotipos de marca 480 y, más adelante, plantillas del reproductor.
- `references/` — documentación de referencia (marca 480, contratos de datos).
- `roadmap/` — el registro de gobierno del proyecto: `SEGUIMIENTO.md` es el hub.

## Convenciones de rama

Se trabaja siempre en `develop`. `master` es del dueño del proyecto: nunca se commitea,
mergea ni empuja ahí. Ver `roadmap/HOJA_DE_RUTA.md` §0.1 para el protocolo completo.
