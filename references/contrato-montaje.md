# Encaje con la cadena de montaje de vídeo (T-33)

> Esta skill termina donde empieza la fase de montaje (recorte y edición con
> ffmpeg u otra herramienta): esta página documenta el contrato exacto que le
> deja preparado — qué archivos, con qué nombre, en qué carpeta, y qué puede y
> qué NO puede asumir todavía la skill de montaje sobre ellos.

## Carpeta y nombres de archivo

Todas las salidas de un guion viven en una única carpeta, siempre dentro de la
carpeta del propio guion (`scripts/entrada.carpeta_salida_para`, regla de
aislamiento, §0.2 de `HOJA_DE_RUTA.md`):

```
<carpeta-del-guion>/<nombre-guion>-teleprompter/
├── estado.json              # estado del proyecto (T-07); no lo consume el montaje
├── guion-escenas.md         # documento de revisión (T-16/T-17); no lo consume el montaje
├── reproductor.html         # teleprompter (T-18+); no lo consume el montaje
├── guion.srt                # subtítulos borrador (T-27) — CONTRATO DE MONTAJE
├── guion-alineado.srt       # subtítulos alineados con la toma buena (R-05), si existe parte de rodaje
├── guion-impresion.html     # HTML de impresión (T-28)
├── guion.pdf                # si hubo Chrome/Edge disponible (T-28)
├── tarjetas.json            # contrato de tarjetas (T-29) — CONTRATO DE MONTAJE
├── brief-pptx.md            # brief de invocación a 480-branded-pptx (T-29)
├── capitulos-youtube.txt    # capítulos con marcas de tiempo reales (R-07), si el guion trae la sección
├── capitulos-ffmpeg.txt     # capítulos FFMETADATA1 incrustables (R-22), misma condición que el anterior
├── concat-ffmpeg.txt        # lista de concatenación de ffmpeg (R-19), si existe parte de rodaje
├── diccionario-locucion.json  # opcional, del dueño (T-13)
└── teleprompter.log         # diagnóstico técnico (T-02); no lo consume el montaje
```

El sufijo (`config.NOMBRE_SUFIJO_CARPETA_SALIDA`) y el resto de nombres
(`config.NOMBRE_ARCHIVO_*`) son los que produce hoy el código — la skill de
montaje no debe fijarse en el sufijo en sí, solo en que es la misma carpeta que
contiene `guion.srt` y `tarjetas.json` de un mismo guion. **R-06** cerró el
hallazgo #6 de `auditoriacontinua.md`: hasta esa tarea el sufijo era
`-tarjetas`, heredado de antes de renombrar el proyecto a `teleprompter`.
`entrada.carpeta_salida_para` migra sola, la primera vez que procesa un guion,
cualquier carpeta de salida que todavía lleve el sufijo antiguo (con copia de
seguridad `.bak-<marca>` previa, sin borrado destructivo) — una carpeta creada
antes de R-06 no requiere ningún paso manual del dueño ni de la skill de
montaje.

De todo lo anterior, **la fase de montaje solo necesita leer dos archivos**:
`guion.srt` y `tarjetas.json`. El resto es documentación y herramientas de
producción para el dueño, no entrada de la cadena de montaje. Cuando existe un
parte de rodaje con al menos una toma buena (R-02/R-05), `guion-alineado.srt`
es una tercera opción con tiempos más fieles a la toma real — sigue siendo
opcional: si no existe, `guion.srt` (estimado) es la única fuente de tiempos.

## Nombres y orden de escenas (requisito 2 de T-33)

El `numero` de cada escena es el capturado del encabezado del guion de origen
(`## BLOQUE N — <título>`, `references/convencion-guion.md`) y **es la única
clave que permite casar una toma grabada con su escena sin ambigüedad**: no hay
ningún otro identificador de escena en el sistema.

Para que ese emparejamiento sea seguro, la cadena de montaje puede asumir que,
en un guion sin desviaciones señaladas:

1. **`numero` es único** dentro del guion (ninguna escena repite el número de otra).
2. **`numero` es estrictamente creciente** en el mismo orden en que aparecen las
   escenas en el documento — el mismo orden en el que aparecen en `tarjetas.json`
   (`escenas`, T-29) y en el que se generan los bloques del `.srt` (T-27).
3. Ese orden de documento es también el orden de grabación previsto: la escena
   `numero=0` se graba primero, y así sucesivamente.

Estas dos primeras propiedades ya NO se dan siempre por supuestas en silencio:
`convencion.detectar_desviaciones` (T-10, ampliada en T-33) señala
`numero_escena_duplicado` y `numero_escena_no_creciente` como desviaciones —
nunca bloquean el proceso (la escena se sigue generando con el número tal cual
viene del encabezado, igual que el resto de desviaciones de esa función), pero
si aparecen, la cadena de montaje no debe confiar en el número de escena para
casar tomas hasta que el guion de origen se corrija. Los tres guiones reales de
`fixtures/reales/` y el guion de ejemplo de `fixtures/guion-ejemplo.md` (T-32)
numeran sus escenas `0, 1, 2, …` sin huecos ni repeticiones — la convención que
`references/convencion-guion.md` ya documenta como recomendada, ahora también
verificada.

## `guion.srt` — qué puede y qué NO puede asumir el montaje

- Es **un único archivo para el guion completo**, con una línea de tiempo
  continua desde `00:00:00,000` (T-27, requisito 1-2): no hay un `.srt` por
  escena.
- Los tiempos son **estimados** a partir del ritmo deducido del guion (T-12),
  no del tiempo real de una toma grabada. Una vez existe un parte de rodaje
  con al menos una toma buena (R-02), `guion-alineado.srt` (R-05, ver más
  abajo) trae esas mismas escenas con tiempos reescalados a la toma real; las
  que aún no tienen toma buena siguen ahí con su duración estimada.
- El propio texto del `.srt` **no lleva ninguna marca de escena** (ni número ni
  separador): un lector de subtítulos solo ve índice, marca de tiempo y texto.
  Para saber a qué escena pertenece un subtítulo concreto, la cadena de montaje
  debe cruzarlo con `tarjetas.json` (ver siguiente sección) — nunca intentar
  adivinarlo por el contenido del texto. `guion-alineado.srt` comparte esta
  misma limitación.
- `srt.validar_srt` ya aplica las mismas reglas que un lector estricto tipo
  ffmpeg (índice secuencial desde 1, marca de tiempo bien formada, sin solapes
  ni tiempos decrecientes, ninguna línea por encima de
  `Configuracion.srt_caracteres_por_linea_max`): un `.srt` que pase esa
  validación es, por construcción, consumible por ffmpeg sin avisos.
  `guion-alineado.srt` pasa exactamente el mismo validador (`srt_alineado.
  validar_srt_alineado`, sin ninguna regla nueva).

## `tarjetas.json` — cómo derivar el tiempo de cada escena

Desde **R-16**, `tarjetas.json` (`references/contrato-tarjetas.md`, T-29) trae
ya resuelto el rango absoluto `[inicio_segundos, fin_segundos)` de cada
escena: la cadena de montaje **lee esas dos claves directamente**, sin
reproducir ningún cálculo propio. Cualquier subtítulo de `guion.srt` (o de
`guion-alineado.srt`, si existe) cuyo intervalo cae dentro de ese rango
pertenece a esa escena, sin ambigüedad, mientras no haya desviaciones de
numeración (sección anterior). `fin_segundos` de una escena coincide siempre
con `inicio_segundos` de la siguiente (sin huecos ni solapes), y el
`fin_segundos` de la última escena coincide con `metadatos.
duracion_total_segundos` cuando ninguna escena tiene toma buena, o con el fin
del último subtítulo de `guion-alineado.srt` cuando alguna la tiene.
`metadatos.mezcla_duracion_real_y_estimada` sigue avisando si el conjunto
mezcla escenas con toma buena y sin ella, para que la cadena de montaje sepa
si hay huecos sin evidencia real detrás de esos límites.

**Cómo se calculan** (transparencia, no instrucción a seguir — la propia
skill ya hace esta cuenta una sola vez dentro de `scripts/pptx.py`,
`_con_limites_absolutos`): acumulando en el mismo orden en que las escenas
aparecen en el guion la duración real de cada escena (`duracion_real_segundos`,
R-13) si tiene toma buena, o su duración estimada (`duracion_estimada_segundos`,
T-12) si no —

```
duracion_usada[k]  = duracion_real_segundos de escenas[k] si no es null,
                      duracion_estimada_segundos de escenas[k] si lo es
inicio_segundos[k] = suma(duracion_usada de escenas[0..k-1])
fin_segundos[k]    = inicio_segundos[k] + duracion_usada[k]
```

Antes de R-16, `tarjetas.json` no traía estos dos campos y este documento le
pedía a la cadena de montaje que reprodujera esta misma acumulación a mano —
un cálculo que la propia skill ya resolvía correctamente y con tests (T-12,
R-05, R-13), reproducido bit a bit por un tercero. R-16 cierra esa grieta:
verificado por `tests/test_integracion_montaje.py::
test_inicio_y_fin_segundos_de_tarjetas_json_no_dejan_huecos_ni_solapes` y
`test_fin_segundos_de_la_ultima_escena_coincide_con_el_fin_del_srt_correspondiente`.

## `indicaciones_ancladas` — en qué segundo insertar cada captura de pantalla (R-20)

Cada escena de `tarjetas.json` trae, desde R-20, `indicaciones_ancladas`: el
mismo conjunto de `indicaciones_pantalla`/`notas_internas` de esa escena, pero
con un `instante_estimado_segundos` absoluto del vídeo (mismo eje que
`inicio_segundos`/`fin_segundos` de la sección anterior). La cadena de
montaje puede leer esa clave directamente para situar cada corte a pantalla
sin releer el guion ni el propio vídeo a ojo — es una estimación (el nombre
lo deja explícito), basada en el ritmo deducido del guion (T-12), no en un
instante medido sobre la toma real.

## `capitulos-ffmpeg.txt` — capítulos incrustables de verdad en el vídeo final (R-22)

`capitulos-youtube.txt` (R-07, ver "Qué quedaba fuera de esta tarea" más
abajo) es texto pensado para pegar a mano en la descripción de un vídeo de
YouTube — útil, pero no algo que ffmpeg pueda consumir. `capitulos-ffmpeg.txt`
reutiliza exactamente el mismo emparejamiento título↔escena y los mismos
tiempos real/estimado que ya calcula `capitulos_youtube.calcular_capitulos`
(misma condición de generación: el guion trae sección `Capítulos`), pero
formateados en `FFMETADATA1`, el formato nativo de metadatos de ffmpeg:

```
;FFMETADATA1
[;Nota de tiempos estimados, si aplica — ffmpeg ignora toda línea que empiece por ';' o '#']

[CHAPTER]
TIMEBASE=1/1000
START=0
END=12500
title=Título del primer capítulo

[CHAPTER]
TIMEBASE=1/1000
START=12500
END=...
title=Título del segundo capítulo
```

La cadena de montaje puede incrustar este archivo en el `.mp4` final sin
tocar nada más:

```
ffmpeg -i video.mp4 -i capitulos-ffmpeg.txt -map_metadata 1 -codec copy video-final.mp4
```

Diferencias deliberadas con `capitulos-youtube.txt`, ambas documentadas en el
docstring de `capitulos_youtube.formatear_capitulos_ffmpeg`:

- **Sin la "marca mínima" de `capitulos_youtube_marca_minima_segundos`:** un
  archivo de metadatos incrustado no compite por espacio de lectura como una
  lista de texto — cada escena emparejada con un título es su propio
  capítulo, sin filtrar ninguno por cercanía con el anterior.
- **`END` de cada capítulo es el `START` del siguiente**, y el del último es
  `ResultadoCapitulos.duracion_total_segundos` (el mismo cursor de tiempo
  acumulado que ya calculaba `calcular_capitulos` y hasta R-22 descartaba)
  convertido a milisegundos — sin huecos ni solapes entre capítulos
  consecutivos.
- Los caracteres `\`, `=`, `;`, `#` y el salto de línea de cada `title=...`
  se escapan con `\` por delante, igual que `concat_ffmpeg._escapar_ruta_ffmpeg`
  escapa la ruta de vídeo (R-19), mismo patrón, formato distinto.

Misma condición de ausencia que `capitulos-youtube.txt`: sin sección
`Capítulos` en el guion, este archivo no se genera — la cadena de montaje no
debe asumir que existe.

**Validado antes de llegar a disco, desde el primer día (misma lección que
`concat-ffmpeg.txt`, hallazgo `#27`/R-21):** `capitulos-ffmpeg.txt` nunca se
escribe sin pasar antes por `capitulos_youtube.validar_capitulos_ffmpeg`
sobre su propio contenido — exige la primera línea `;FFMETADATA1`, cada
`START`/`END` entero no negativo, `START` estrictamente creciente y `END` de
cada capítulo sin solaparse con el `START` del siguiente. Un contenido
inválido degrada esa mitad de la salida a omitida con el motivo exacto, sin
impedir que `capitulos-youtube.txt` se genere igual.

## `concat-ffmpeg.txt` — lista de concatenación lista para ffmpeg (R-19)

Cuando existe al menos un parte de rodaje registrado (R-02), `concat-ffmpeg.txt`
trae una línea por escena, en el mismo orden real del guion (misma garantía de
la sección anterior):

- `file '<archivo_video>'` (comillas simples, cualquier comilla simple interna
  escapada con la secuencia estándar `'\''`) para la escena cuya toma buena
  tiene `archivo_video` anotado (`references/contrato-tomas.md`).
- `# ESCENA <numero>: sin_toma_buena` o `# ESCENA <numero>: sin_archivo_anotado`
  para la que no — el demuxer `concat` de ffmpeg ignora las líneas que
  empiezan por `#`, así que la cadena de montaje puede pasar este archivo
  directamente a `ffmpeg -f concat -safe 0 -i concat-ffmpeg.txt` en cuanto
  todas las escenas tengan su línea `file`, o usarlo como lista de pendientes
  mientras tanto.

Sin ningún parte de rodaje en absoluto, este archivo no se genera (no hay
nada real que concatenar todavía) — la cadena de montaje no debe asumir que
existe hasta que el dueño haya grabado al menos una toma.

**Validado antes de llegar a disco (R-21, hallazgo `#27`):** `concat-ffmpeg.txt`
nunca se escribe sin pasar antes por `concat_ffmpeg.validar_lista_concat_ffmpeg`
sobre su propio contenido — hasta R-21 ese validador solo se ejercitaba desde
`verificar_salidas.py --fixture`, un chequeo de salud aparte de la generación
real. Si el contenido no cumple el formato del demuxer `concat`, la salida se
omite con el motivo exacto en vez de escribirse corrupta o lanzar una
excepción sin capturar. `archivo_video` llega ya saneado desde su origen
(recortado, sin saltos de línea; `references/contrato-tomas.md`), así que este
caso solo se da si esa garantía se rompe — nunca por una toma anotada con
normalidad.

## Qué quedaba fuera de esta tarea (T-33), ya completado por sesiones posteriores

Nota historica: en el momento de T-33 (2026-09-02), `R-02`, `R-04` y `R-05`
estaban `PENDIENTE`. Las tres se completaron en sesiones posteriores (oleadas
v2 y v3) y ya están reflejadas en el resto de este documento:

- **Registro de tomas por escena** (grabar más de una toma, marcar cuál es la
  buena): `R-02`, `COMPLETADA` — `estado.json["tomas"]`,
  `references/contrato-tomas.md`.
- **Recalibrar el ritmo con tiempos reales**: `R-04`, `COMPLETADA` —
  `scripts/calibracion.py`, informe en sesión, nunca aplicado solo sobre
  `Configuracion.ppm_manual`.
- **`.srt` alineado con la toma buena**: `R-05`, `COMPLETADA` —
  `guion-alineado.srt`, ver arriba.

T-33 no adelantó ninguna de las tres: solo dejó documentado y verificado el
contrato de lo que existía entonces (`.srt` + `tarjetas.json` + estructura de
carpetas), para que esas tareas futuras — y la skill de montaje que las
consuma — no tuvieran que averiguarlo leyendo código.
