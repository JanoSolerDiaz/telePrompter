# ROADMAP HISTÓRICO — teleprompter

> Archivo de oleadas y fases **100 % entregadas** de `ROADMAP_PRODUCTO.md` (ver su cabecera y la
> §0.4 de `HOJA_DE_RUTA.md`). El PM mueve aquí una oleada completa cuando todas sus R-XX están
> COMPLETADA en §1 de `SEGUIMIENTO.md` y no queda ningún hito de negocio propio de la oleada sin
> cumplir. Documento de consulta, no se vuelve a tocar salvo para corregir un error de trascripción.
>
> El estado de cada R-XX se sigue verificando en §1 de `SEGUIMIENTO.md` (fuente autoritativa); este
> documento no lo duplica ni lo actualiza — es una fotografía de la spec en el momento del archivo.

**Movido a histórico el:** 2026-09-03, ciclo de Product Manager. Motivo: las tres oleadas/fases de
abajo tenían, en ese momento, todas sus R-XX en COMPLETADA en §1 de `SEGUIMIENTO.md` y ningún hito
de negocio propio pendiente (a diferencia de la oleada v1, que sigue viva en `ROADMAP_PRODUCTO.md`
porque su criterio de salida —grabar un vídeo de curso entero con la skill— todavía no se ha
cumplido, aunque todo su código esté entregado desde antes de este ciclo).

**Movido a histórico el:** 2026-09-04, ciclo de Product Manager. Se añade la Fase transversal F-E
(R-10), con su única R-XX ya COMPLETADA y sin ningún hito de negocio propio pendiente — mismo
criterio que el movimiento anterior.

**Movido a histórico el:** 2026-09-04 (segundo ciclo de PM del día). Se añade la Fase transversal
F-F (R-11), con su única R-XX ya COMPLETADA y sin ningún hito de negocio propio pendiente — mismo
criterio que los dos movimientos anteriores.

**Movido a histórico el:** 2026-09-10, ciclo de Product Manager. Se añade la Oleada v4 (R-12), con
su única R-XX ya COMPLETADA (2026-09-10) y sin ningún hito de negocio propio pendiente — mismo
criterio que los tres movimientos anteriores.

**Movido a histórico el:** 2026-09-11, ciclo de Product Manager. Se añaden la Oleada v5 (R-13) y la
Fase transversal F-G (R-14), ambas COMPLETADA por el Programador el mismo día (2026-09-11) y sin
ningún hito de negocio propio pendiente — mismo criterio que los cuatro movimientos anteriores.

**Movido a histórico el:** 2026-09-14, ciclo de Product Manager. Se añaden la Fase transversal F-H
(R-15) y la Oleada v6 (R-16), ambas COMPLETADA por el Programador el mismo día (2026-09-14) y sin
ningún hito de negocio propio pendiente — mismo criterio que los cinco movimientos anteriores.

**Movido a histórico el:** 2026-09-15, ciclo de Product Manager. Se añade la Fase transversal F-I
(R-17), COMPLETADA por el Programador el mismo día en que se abrió (2026-09-14) y sin ningún hito
de negocio propio pendiente — mismo criterio que los seis movimientos anteriores.

**Movido a histórico el:** 2026-09-17, ciclo de Product Manager. Se añade la Oleada v7 (R-18),
COMPLETADA por el Programador el mismo día en que se abrió (2026-09-16→17) y sin ningún hito de
negocio propio pendiente — mismo criterio que los siete movimientos anteriores. Este movimiento
corrige además la prosa de "Cola de producto" de `ROADMAP_PRODUCTO.md`, que llevaba listando R-18
como pendiente pese a estar ya `COMPLETADA` en §1 de `SEGUIMIENTO.md` — el mismo patrón de latencia
que `auditoriacontinua.md` registra como hallazgo `#24`.

---

## Oleada v2 — Rodaje real: cerrar el bucle entre lo estimado y lo grabado

Todo lo de v1 trabaja con **estimaciones**. En cuanto haya tomas reales, el producto tiene una
fuente de verdad que antes desaprovechaba: cuánto se tardó de verdad, dónde se repitió, dónde el
locutor se trabó. Esta oleada convierte esos datos en mejoras del propio guión y del ritmo.
Contenía R-01 a R-04. **Entregada 2026-09-03.**

### R-01 — Persistencia verificada de preferencias, con plan B
**Oleada / Fase:** v2 · **Migración:** No · **Depende de:** T-26
**Origen:** auditoría #5

**Objetivo:** que la promesa de «retomar la grabación entre sesiones» sea real y no dependa de una
suposición sobre el navegador. Hoy T-26 confía en que `localStorage` persiste al abrir el
reproductor desde `file://`, y eso no está comprobado en el navegador con el que se graba.

**Requisitos:**
1. Comprobación real en el navegador de grabación: guardar preferencias, cerrar, reabrir el
   archivo y verificar que siguen ahí. Dejar constancia del resultado por navegador.
2. Si no persisten, plan B sin red y sin dependencias: **exportar e importar las preferencias como
   un archivo** (o como texto que el reproductor pueda leer), de modo que retomar sea un gesto y
   no una reconfiguración.
3. Aviso honesto en el propio reproductor cuando detecte que el almacenamiento no persiste, en vez
   de fallar en silencio y perder los ajustes del dueño.

**Criterio de aceptación:** existe evidencia escrita del comportamiento en el navegador de
grabación; si no persiste, el ciclo exportar → reabrir → importar restaura tamaño, velocidad por
escena y última escena vista.

**Cómo se entregó:** comprobación real con Playwright/Chromium (mismo perfil de navegador persiste
entre cierre y reapertura, uno nuevo no) más detección en código de que `localStorage` no funciona
en absoluto; exportar/importar como `.json` que lee siempre de variables en memoria (nunca de
`localStorage` en el momento del clic); aviso `.aviso-almacenamiento` en el propio reproductor.

### R-02 — Registro de tomas por escena
**Oleada / Fase:** v2 · **Migración:** Sí (`002_tomas`) · **Depende de:** T-19, T-23, T-26
**Origen:** roadmap

**Objetivo:** que el índice de escenas deje de ser una lista y pase a ser el parte de rodaje. Hoy
T-19 muestra un estado por escena pero nada registra qué pasó en cada toma, y esa información es
justo la que hace falta al día siguiente y en el montaje.

**Requisitos:**
1. Por escena: número de tomas, duración real de cada una (del cronómetro de T-23) y marca de cuál
   es la buena.
2. Nota rápida por toma, escribible sin salir del modo de grabación y con el mínimo de teclas.
3. Volcado a un archivo de la carpeta de salida, legible por la fase de montaje y por el dueño.
4. El índice muestra de un vistazo qué está grabado, qué se repitió y qué falta.

**Criterio de aceptación:** tras un rodaje simulado de tres escenas con repeticiones, el parte
refleja tomas, duraciones y toma buena, y sobrevive al cierre del navegador.

**Cómo se entregó:** `scripts/tomas.py` + migración `002_tomas` (`estado.json` gana el contenedor
`tomas`); como mucho una toma «buena» por escena; exportación a `.json` desde el reproductor,
verificada con Playwright que sobrevive a cerrar y reabrir el mismo perfil de navegador y que el
archivo exportado se recarga tal cual por el lado Python (`tomas.cargar_parte_de_rodaje`).

### R-03 — Marcar tropiezos durante la toma
**Oleada / Fase:** v2 · **Migración:** No · **Depende de:** R-02
**Origen:** roadmap

**Objetivo:** capturar en caliente el dato más valioso para mejorar el guión: dónde se traba el
locutor. Hoy ese conocimiento se pierde entre la grabación y la siguiente revisión.

**Requisitos:**
1. Una tecla que marque el bloque actual como problemático, sin interrumpir la toma.
2. Los bloques marcados se vuelcan a `FEEDBACK.md` como entradas `nuevo`, con escena, bloque y
   texto exacto.
3. En la siguiente validación, esos bloques aparecen destacados en `guion-escenas.md` para
   reescribirlos a mano o con propuesta de la skill, dentro del alcance permitido en §0.2.

**Criterio de aceptación:** marcar dos bloques en una toma produce dos entradas de feedback
localizadas, y la siguiente validación las muestra sin que el dueño tenga que buscarlas.

**Cómo se entregó:** tecla `T` alterna el tropiezo del bloque activo; `scripts/feedback.py` fusiona
la exportación en el `FEEDBACK.md` **de la carpeta de salida del guion** (no `roadmap/FEEDBACK.md`);
destacado por texto exacto del bloque en la siguiente revisión, con deduplicación al reexportar.

### R-04 — Recalibrar el ritmo con tiempos reales
**Oleada / Fase:** v2 · **Migración:** No · **Depende de:** R-02, T-12
**Origen:** roadmap

**Objetivo:** cerrar el bucle del ritmo. T-12 deduce el ppm de las duraciones **objetivo**, que
son una intención del guionista; R-02 aporta las duraciones **reales**. Con las dos se puede saber
cuánto se desvía la intención de la realidad y afinar las estimaciones futuras.

**Requisitos:**
1. Comparar, por escena y en total, duración estimada, duración objetivo y duración real.
2. Proponer un ppm personal calibrado con la evidencia acumulada de varios guiones, que el dueño
   acepta o rechaza; nunca se aplica solo.
3. Informe corto y legible: en qué tipo de escena se acelera y en cuál se frena.

**Criterio de aceptación:** con dos guiones grabados, la skill propone un ppm calibrado y muestra
la desviación por escena que lo justifica.

**Cómo se entregó:** `scripts/calibracion.py`; duración real exclusivamente de la toma «buena»
(nunca promediada ni estimada); tipo de escena por posición (apertura/desarrollo/cierre), no por
título; ppm calibrado exige evidencia de ≥2 guiones y ≥150 palabras; la propuesta se devuelve como
datos para que Claude se la formule al dueño, nunca escribe `Configuracion.ppm_manual` por su
cuenta.

---

## Oleada v3 — Continuidad con el montaje

Hacer que lo que sale de aquí no haya que volver a tocarlo en la fase de ffmpeg. Contenía R-05 y
R-07. **Entregada 2026-09-03.**

### R-05 — `.srt` alineado con la toma buena
**Oleada / Fase:** v3 · **Migración:** No · **Depende de:** R-02, T-27, T-33
**Origen:** roadmap

**Objetivo:** que el `.srt` deje de ser un borrador estimado y pase a estar alineado con lo que se
grabó de verdad, para que el montaje empiece con subtítulos casi finales en vez de con una
aproximación que hay que rehacer entera.

**Requisitos:**
1. Reescalar los tiempos de los bloques a la duración real de la toma buena de cada escena.
2. Mantener el `.srt` estimado como salida independiente: el estimado sirve antes de grabar, el
   alineado después.
3. Validar el resultado con las mismas reglas estrictas de T-27.

**Criterio de aceptación:** con una toma real cronometrada, el `.srt` alineado no tiene solapes y
su duración total coincide con la de la toma dentro de la tolerancia documentada.

**Cómo se entregó:** `scripts/srt_alineado.py`; reescala palabras y pausa de cada bloque con el
mismo factor; una escena sin toma buena conserva su estimación sin tocar; escribe `guion-alineado.srt`,
nunca sobrescribe `guion.srt`; reutiliza `srt.validar_srt` de T-27 sin reglas nuevas.

### R-07 — Capítulos de YouTube con marcas de tiempo reales
**Oleada / Fase:** v3 · **Migración:** No · **Depende de:** R-02, T-08
**Origen:** roadmap

**Objetivo:** T-08 ya detecta y conserva íntegra la sección auxiliar `## Capítulos (para la
descripción del vídeo)` que aparece en los tres guiones reales, pero hoy ese contenido no sale
de ahí: el formador tiene que volver a cronometrar el vídeo ya montado a mano para pegar los
capítulos en la descripción de YouTube. Con R-02 (registro de tomas) existe ya el dato que hace
falta — cuánto duró de verdad cada escena buena — así que generar el listado es una unión de dos
datos que el producto ya tiene, no una funcionalidad nueva desde cero.

**Requisitos:**
1. Leer los títulos de capítulo de la sección auxiliar `Capítulos` (T-08) y emparejarlos con la
   escena a la que corresponden, en el mismo orden en que aparecen ambos.
2. Con R-02 disponible, calcular el tiempo acumulado de inicio de cada escena a partir de la
   duración real de la toma marcada como buena; sin R-02 o sin tomas registradas todavía, usar
   las duraciones estimadas de T-12 y decirlo explícitamente en la propia salida (nunca mezclar
   tiempos reales y estimados sin avisar de cuál es cuál).
3. Generar `capitulos-youtube.txt` en la carpeta de salida del guión, con el formato exacto que
   exige YouTube: primera marca `0:00`, una línea `M:SS Título` por capítulo en orden creciente,
   sin dos marcas a menos de 10 segundos entre sí (mínimo de la propia plataforma).
4. Si el guión no trae sección `Capítulos`, no se genera el archivo y se informa del motivo
   (invariante (a): nunca inventar contenido que el guionista no ha escrito).
5. Regenerable en cada revalidación o tras cerrar tomas nuevas, sin intervención manual.

**Criterio de aceptación:** sobre un guión real con sección `Capítulos` y tomas registradas
(R-02), el archivo generado respeta el formato de YouTube, empieza en `0:00` y sus marcas
coinciden con el inicio real de cada escena grabada; sin tomas registradas, usa las duraciones
estimadas y la primera línea del archivo lo advierte.

**Cómo se entregó:** `scripts/capitulos_youtube.py`; emparejamiento estrictamente posicional
(nunca por texto ni número de escena); mezcla honesta real/estimado por escena (mismo criterio que
R-05), avisando en la primera línea cuando el resultado mezcla ambas; deliberadamente fuera del
contrato de montaje de T-33 por ser texto para la descripción de YouTube, no un insumo de ffmpeg.

---

## Fase transversal F-D — Deuda y coherencia

Lo que el auditor levantó y no encajaba en una oleada de producto. Contenía R-06, R-08 y R-09.
**Entregada 2026-09-03.**

### R-06 — Coherencia de nomenclatura y separación de `assets/`
**Oleada / Fase:** F-D · **Migración:** Sí (`00N_renombrado_salida`) · **Depende de:** T-32
**Origen:** auditoría #6

**Objetivo:** quitar la deuda de nombres antes de que se fosilice en carpetas de guiones reales.

**Requisitos:**
1. Decidir y aplicar el nombre definitivo de la carpeta de salida, hoy `<nombre-guion>-tarjetas/`,
   heredado del nombre anterior del proyecto.
2. Migración que renombre las carpetas de proyectos de guión ya existentes sin perder estado ni
   ediciones, con `.bak` previo.
3. Separar `assets/` en dos espacios con propósitos distintos: los logotipos y recursos de marca
   por un lado, las plantillas HTML/CSS/JS del reproductor por otro.

**Criterio de aceptación:** un proyecto de guión creado antes del cambio se abre después sin
pérdidas; ninguna ruta del código mezcla marca y plantillas.

**Cómo se entregó:** sufijo `-tarjetas` → `-teleprompter`; migración de carpetas heredadas dentro
de `entrada.py` (no en `scripts/migraciones/`, por no ser una migración de esquema de `estado.json`),
con copia `.bak-<marca>` antes de renombrar; logotipos movidos a `assets/marca/`.

### R-08 — Deuda técnica menor: números mágicos, documentación desactualizada y versión de Python
**Oleada / Fase:** F-D · **Migración:** No · **Depende de:** —
**Origen:** auditoría #10, #11, #12

**Objetivo:** cerrar tres deudas menores de la auditoría de 2026-09-02 que no piden rediseño,
solo disciplina de mantenimiento — quedarían fosilizadas si nadie las agenda explícitamente.

**Requisitos:**
1. Los dos colores de estado del índice del reproductor que quedaron fuera del barrido de T-21
   (`.escena-estado--grabada` `#4ade80`, `.escena-estado--revisada` `#60a5fa`, hoy literales en
   `estilo.css`) pasan a `Configuracion`, documentados en la tabla de `SKILL.md` (T-31), mismo
   patrón que el color de acento ya migrado.
2. El glosario de `PROYECTO.md` deja de decir «ritmo por defecto 120 ppm»: el ritmo base es el
   deducido de las duraciones objetivo del propio guión, 120 ppm es solo el respaldo (§0.2, T-12).
3. Resolver el desajuste entre `pyproject.toml` (`requires-python`/`target-version = "py312"`) y
   el intérprete real de las sesiones de nube (3.11.15, ya documentado en `DECISIONES_TECNICAS.md`
   desde T-06): o se baja la versión declarada a la real, o —si el dueño prefiere mantener 3.12
   como objetivo deliberado— se dice explícitamente y se añade una comprobación en `scripts/ci.py`
   que avise cuando el intérprete real diverja, en vez de dejarlo solo en una nota suelta.

**Criterio de aceptación:** ningún color de estado del índice queda fuera de `Configuracion`;
`PROYECTO.md` coincide con §0.2; el desajuste de versión de Python queda resuelto o vigilado por
la CI, nunca solo anotado.

**Cómo se entregó:** los dos colores migrados a `Configuracion`; `PROYECTO.md` corregido palabra
por palabra con §0.2; `pyproject.toml` mantiene 3.12 como objetivo deliberado y
`ci.avisar_si_version_python_diverge` avisa (no bloquea) cuando el intérprete real diverge.

### R-09 — Endurecer el validador de auto-contención
**Oleada / Fase:** F-D · **Migración:** No · **Depende de:** —
**Origen:** auditoría #13

**Objetivo:** «salida autocontenida» (§0.2) es uno de los invariantes más sensibles del producto
—un único archivo `.html`, cero red— pero el validador de `verificar_salidas.py` no cubre todos
los vectores por los que un HTML puede llamar a una red. Hoy ninguna plantilla los usa: es un
cierre preventivo, antes de que un cambio futuro en `guion.js`/`estilo.css` cuele uno sin que la
CI lo note.

**Requisitos:**
1. Ampliar el validador para detectar, con el mismo criterio de bloqueo que ya aplica a
   `http(s)://`/`@import`/`fetch`, seis patrones adicionales: `<object>`, `<embed src>`,
   `<base href>`, `WebSocket`, `EventSource`/`sendBeacon` y `url(...)` de CSS fuera de `@import`.
2. Un test que confirme que un HTML de prueba con cada uno de los seis patrones falla el
   validador, y que el reproductor real generado (fixture) sigue pasando sin ninguno de ellos.
3. Documentar la lista completa de patrones vigilados (los ya existentes más estos seis) en
   `DECISIONES_TECNICAS.md` o en la referencia técnica que corresponda, para que quien amplíe el
   reproductor sepa qué evitar sin tener que leer el código del validador.

**Criterio de aceptación:** los seis patrones nuevos hacen fallar el validador sobre un HTML de
prueba construido para cada uno; el reproductor real (`fixtures/guion-ejemplo.md`) sigue
validando en verde sin ninguno de ellos.

**Cómo se entregó:** seis patrones nuevos en `PATRONES_RECURSO_EXTERNO` (con límite de palabra
`\b` delante de `url(` para no confundir `URL.createObjectURL`/`revokeObjectURL`, ya en uso desde
R-01); documentación completa en `references/validador-autocontencion.md` (nuevo).

---

## Fase transversal F-E — Robustez en el entorno real del dueño

La primera vez que el proyecto corrió de verdad fuera de un contenedor de nube (sesión local de
T-32, en el Windows del dueño) aparecieron fallos que ninguna sesión de nube podía ver, porque
ninguna corre en Windows. Contenía R-10, su única R-XX. **Entregada 2026-09-04.**

### R-10 — Robustez multiplataforma detectada al correr en Windows por primera vez
**Oleada / Fase:** F-E · **Migración:** No · **Depende de:** T-06
**Origen:** hallazgo de sesión (T-32 local, máquina del dueño, 2026-09-03 — no es hallazgo del
auditor, que audita desde sesiones de nube sin acceso a esa máquina)

**Objetivo:** la primera vez que la suite completa corrió en la máquina real del dueño (Windows,
no un contenedor de nube) aparecieron cuatro tests en rojo, documentados en
`roadmap/HISTORIAL_SESIONES.md` (sesión "T-32 desbloqueada + P-04"). Tres son ruido de plataforma
sin riesgo real para el producto; el cuarto sí lo tiene: cualquier guión que el dueño escriba y
guarde en Windows llevará fin de línea `\r\n`, y `entrada.leer_guion` no lo normalizaba — el `\r`
llegaba intacto a todo el pipeline de parseo, troceo y revalidación, con riesgo de comparaciones de
texto que fallan en silencio exactamente donde el invariante (c) («la edición manual manda»)
depende de que dos textos idénticos se reconozcan como idénticos.

**Requisitos:**
1. `entrada.leer_guion` normaliza cualquier fin de línea (`\r\n`, `\r` suelto) a `\n` en el mismo
   punto donde ya decodifica UTF-8, antes de que ninguna capa posterior vea el texto.
2. Diagnosticar la causa exacta de `test_nombre_guion_seguro_nunca_vacio` en Windows antes de
   tocar código y corregir `nombre_guion_seguro` solo si el diagnóstico confirma un caso real.
3. `test_instalar_hook_copia_y_da_permiso_de_ejecucion` pasa a `skip` explícito cuando
   `os.name != "posix"`, en vez de quedar en rojo.
4. Verificar que ninguna salida generada (`.srt`, `.pdf`, `tarjetas.json`, reproductor) reintroduce
   `\r\n` en su propio proceso de escritura.

**Criterio de aceptación:** un guión guardado con `\r\n` produce exactamente el mismo
`guion-escenas.md` que el mismo guión guardado con `\n`; los cuatro tests que la sesión de T-32
marcó en rojo en Windows quedan en verde o correctamente `skip`, con la causa raíz de cada uno
documentada en `DECISIONES_TECNICAS.md`; la suite sigue en verde en las sesiones de nube (Linux).

**Cómo se entregó:** `entrada.leer_guion` normaliza `\r\n`/`\r` a `\n` justo tras decodificar;
`nombre_guion_seguro` diagnosticado sin cambio de código (`PureWindowsPath`/`PurePosixPath` parten
`"....md"` igual, la hipótesis original no se sostenía) y su parámetro pasa de `Path` a `PurePath`;
`test_instalar_hook_...` gana su `skipif` no-POSIX; los doce `Path.write_text(...)` de `scripts/`
fijan `newline="\n"` (hallazgo real de la comprobación puntual del requisito 4).

---

## Fase transversal F-F — Robustez de los datos derivados del rodaje real

La auditoría de 2026-09-04, la primera pasada tras completarse toda la oleada R (rodaje real,
R-01 a R-07), encontró tres huecos menores en cómo esos datos de rodaje se propagan a las salidas
derivadas — ninguno reproducido como bug hoy sobre material real, los tres cierres preventivos del
mismo tipo que ya motivó F-D. Contenía R-11, su única R-XX. **Entregada 2026-09-04.**

### R-11 — Robustez de datos derivados del rodaje (toma buena ambigua, capítulos sobrantes, cobertura cruzada)
**Oleada / Fase:** F-F · **Migración:** No · **Depende de:** R-02, R-05, R-07
**Origen:** auditoría #16, #17, #18

**Objetivo:** cerrar tres huecos de robustez de menor entidad alrededor de los datos de rodaje real
(R-02) y sus dos consumidores derivados (`.srt` alineado de R-05, capítulos de YouTube de R-07),
detectados por el auditor sin bug reproducido hoy sobre material real — cierre preventivo, no
corrección de una regresión. (1) `tomas.duracion_toma_buena` no validaba que como mucho una toma
estuviera marcada `buena` por escena — esa exclusividad solo la garantizaba el lado JS
(`finalizarTomaActual`); un `.json` con dos tomas `buena` para la misma escena (edición manual,
fusión de exportaciones, un futuro bug de `guion.js`) hacía que la función Python eligiera la
primera en silencio, sin ninguna señal de ambigüedad, propagándose sin aviso a R-04/R-05/R-07
(#16). (2) `capitulos_youtube.calcular_capitulos` empareja títulos de capítulo con escenas
posicionalmente "hasta la más corta"; cuando sobraban títulos de capítulo (más títulos que
escenas), los sobrantes se descartaban de `capitulos-youtube.txt` sin ningún aviso ni
`motivo_sin_generar` — el caso simétrico (menos títulos que escenas) ya estaba cubierto (#17). (3)
no existía ningún test de integración cruzada, en el espíritu de `tests/test_integracion_montaje.py`
(T-33), entre `guion-alineado.srt` (R-05) y `capitulos-youtube.txt` (R-07): ambos comparten
`tomas.duracion_toma_buena`, así que la coherencia era "por construcción", no verificada por
regresión (#18).

**Requisitos:**
1. `tomas.duracion_toma_buena` (o quien la invoque desde `scripts/tomas.py`) detecta más de una
   toma `buena` en la misma escena y lo señala como una incidencia explícita — nunca elige la
   primera en silencio. Test que reproduce exactamente el escenario del hallazgo #16 (dos tomas
   `buena: true` en la misma escena).
2. `capitulos_youtube.calcular_capitulos` deja constancia explícita (aviso o campo equivalente al
   `motivo_sin_generar` ya existente) cuando hay títulos de capítulo sin escena correspondiente, en
   vez de descartarlos sin rastro. Test que reproduce el escenario del hallazgo #17 (más títulos de
   capítulo que escenas).
3. Un test nuevo (no necesariamente un módulo nuevo) que, a partir del mismo `ResultadoTiempos` +
   `tomas_por_escena`, genere `guion-alineado.srt` y `capitulos-youtube.txt` y confirme que sus
   marcas de tiempo son mutuamente coherentes — cierra el hallazgo #18.

**Criterio de aceptación:** un `.json` de tomas con dos tomas `buena` en la misma escena produce
una incidencia visible en vez de una elección silenciosa; un guion con más títulos de capítulo que
escenas no pierde ningún título sin dejar rastro explícito; existe al menos un test de integración
que verifica la coherencia cruzada entre el `.srt` alineado y los capítulos de YouTube sobre el
mismo dato de partida.

**Cómo se entregó:** `tomas.duracion_toma_buena` gana un parámetro opcional `numero_escena` (para
mensajes de error más precisos) y rechaza con `RegistroTomasError` en cuanto encuentra más de una
toma `buena` en la misma escena, comprobado en el punto de LECTURA (no en `cargar_parte_de_rodaje`,
el punto de CARGA) para cubrir también un `estado.json` editado a mano o una fusión de
exportaciones; `ResultadoCapitulos` gana el campo `titulos_sobrantes` (mismo patrón que
`motivo_sin_generar`/`escenas_sin_toma_buena`), deliberadamente sin nota en
`capitulos-youtube.txt` (esos títulos no tienen marca de tiempo que anunciar); nuevo test en
`tests/test_integracion_montaje.py` que alimenta `reescalar_a_toma_buena` y `calcular_capitulos`
con el mismo `ResultadoTiempos`+`tomas_por_escena` y confirma que el inicio acumulado de cada
capítulo coincide con el inicio acumulado de la misma escena en el `.srt` alineado (test de
regresión: ya pasaba antes del cambio, la coherencia era "por construcción").

---

## Oleada v4 — Señalización de las indicaciones de pantalla en el reproductor

Todo lo entregado hasta v1-F-F resuelve la locución: el texto que hay que decir, cuándo y a qué
ritmo. Pero el segmento objetivo de este producto (§ Cliente objetivo) graba guiones que
**mezclan** locución con indicaciones de pantalla (`**EN PANTALLA**`, `**NOTA**`), y esas
indicaciones, aunque T-09 ya las clasifica con posición exacta, solo llegaban al locutor por el
`.pdf`/`guion-escenas.md` — nunca al propio reproductor, que es donde está mirando mientras graba.
Contenía R-12, su única R-XX. **Entregada 2026-09-10.**

### R-12 — Cue discreta de indicaciones EN PANTALLA/NOTA en el reproductor
**Oleada / Fase:** v4 · **Migración:** No · **Depende de:** T-09, T-11, T-19, T-21, T-23
**Origen:** observación de arquitectura del PM (ciclo 2026-09-08), convertida en tarea en el ciclo del 2026-09-09

**Objetivo:** hoy, `scripts/clasificador.py` (T-09) clasifica cada tramo de una escena como
`locucion` o `no_locucion` con `linea_inicio`/`linea_fin` exactos, y `scripts/documento_revision.py`
(T-16, `_indicaciones_no_recitables`/`formatear_indicaciones`) ya lista las indicaciones
`**EN PANTALLA**`/`**NOTA**` al pie de cada escena en `guion-escenas.md`. Pero esa información nunca
llega a `scripts/reproductor.py`: el JSON que embebe en el `.html` solo lleva escenas → bloques de
locución (T-18/T-19). Para un guion que mezcla locución con instrucciones de pantalla —el caso
central de este producto (§ Cliente objetivo)— eso significa que durante la grabación, en pantalla
completa, no hay ninguna señal de cuándo cambiar de aplicación, diapositiva o encuadre: hay que
memorizarlo de antemano o consultar el `.pdf` aparte, rompiendo el propio motivo de ser de un
teleprompter. El objetivo es cerrar ese hueco sin inventar clasificación nueva (reutiliza
`linea_inicio`/`linea_fin` ya calculados) y sin que la cue compita nunca con la legibilidad del
bloque de locución activo (principio de producto #5, límite explícito de esta ficha, no una
sugerencia).

**Requisitos:**
1. `scripts/reproductor.py` (`_construir_datos` o equivalente) incorpora, para cada bloque de
   respiración (T-11) de una escena, las indicaciones `no_locucion` cuya `linea_inicio` cae
   inmediatamente después de la `linea_fin` de ese bloque y antes de la `linea_inicio` del
   siguiente bloque de locución de la misma escena — es decir, se ancla la indicación al bloque de
   locución que la PRECEDE en el guion de origen, para que el locutor la vea con margen antes de
   tener que actuar, mientras aún está recitando la línea anterior. Sin lógica de clasificación
   nueva: solo reutiliza el resultado ya calculado por T-09/T-11.
2. El reproductor muestra esa indicación como una cue discreta y subordinada: tipografía más
   pequeña que el bloque activo, nunca el mismo tamaño ni contraste — el bloque de locución activo
   sigue siendo, en todo momento, el elemento dominante de la pantalla. Visible mientras el bloque
   de respiración al que está anclada está activo; se oculta al avanzar al siguiente bloque de
   locución.
3. La cue se pliega en el mismo grupo de indicadores que ya oculta la tecla `H` (T-23,
   `indicadores-ocultos` en `guion.js`) — no añade atajo nuevo ni preferencia de configuración
   aparte; reutiliza el mecanismo ya entregado y ya persistido (T-26).
4. Ninguna indicación se pierde en silencio (invariante (a) de §0.2, extendido de "el parser no
   descarta texto" a "el reproductor no descarta ninguna cue que el parser sí clasificó"): si una
   indicación no tiene bloque de locución posterior en la misma escena (es la última de la escena),
   se ancla al último bloque de respiración de esa escena en vez de quedar sin mostrar.
5. `guion-escenas.md` (T-16) no cambia de formato: las indicaciones siguen listadas al pie tal
   como hoy, como referencia de revisión de una sola pasada (principio de producto #2). Este
   requisito es exclusivamente del reproductor interactivo.
6. Distingue `**EN PANTALLA**` de `**NOTA**` con un prefijo textual mínimo (p. ej. «Pantalla:» /
   «Nota:»), sin iconografía gráfica ni recursos adicionales que arriesguen la auto-contención del
   `.html` (principio de producto #4) ni la legibilidad a distancia de cámara (principio #5).

**Criterio de aceptación:** en un guion con al menos una indicación `EN PANTALLA` o `NOTA` (los tres
guiones reales de `fixtures/reales/` sirven de fixture), el reproductor generado muestra el texto de
cada indicación anclado al bloque de respiración correcto, sin que el locutor tenga que abrir el
`.pdf` ni memorizarla de antemano; el bloque activo de locución sigue siendo en todo momento el
elemento visualmente dominante (verificable por contraste/tamaño, igual que T-21 verifica el
contraste AAA del bloque activo); ocultar indicadores con `H` también oculta la cue; ninguna de las
indicaciones que hoy lista `guion-escenas.md` al pie de cada escena deja de aparecer en el
reproductor; cero indicaciones nuevas o recalculadas respecto a lo que T-09 ya clasificaba —
únicamente se muestra lo que ya existía, donde antes no se mostraba.

**Cómo se entregó:** `reproductor._indicaciones_ancladas_por_indice` ancla cada indicación al
ÚLTIMO bloque de respiración que la precede (sin bloque precedente, al primero — requisito 4),
reutilizando tal cual la clasificación de T-09 y el filtro pantalla/nota de T-28/T-29
(`pdf.indicaciones_no_recitables`/`es_nota_interna`). `guion.js`/`estilo.css`: cue subordinada
(`.cue-indicacion`, visible solo bajo `.bloque--activo`), plegada con el resto de indicadores en
`H` (T-23), sin atajo nuevo. Prefijos `Pantalla:`/`Nota:` configurables. 7 tests nuevos
(550→557); verificado también visualmente con Playwright/Chromium real. Observación no urgente
dejada para una futura revisión de `clasificador.py`: un separador de escena `---` puede quedar
pegado al final del texto de una indicación cuando esta es la última de la escena (preexistente a
R-12, no pierde texto ni rompe invariantes) — promovida a `R-14` en el ciclo de PM del 2026-09-10.

---

## Oleada v5 — Coherencia de datos derivados para el montaje real

Cierra un hueco de coherencia entre las dos salidas que `references/contrato-montaje.md` documenta
como "CONTRATO DE MONTAJE" (`guion.srt`/`guion-alineado.srt` y `tarjetas.json`): desde R-05 y R-07,
el `.srt` alineado y los capítulos de YouTube ya preferían la duración real de la toma buena sobre
la estimada cuando existía parte de rodaje; `tarjetas.json` era el único de los tres consumidores
de `tomas.duracion_toma_buena` que no lo hacía. Contenía R-13, su única R-XX. **Entregada
2026-09-11.**

### R-13 — Duración real por escena en `tarjetas.json`, coherente con `guion-alineado.srt`
**Oleada / Fase:** v5 · **Migración:** No · **Depende de:** T-12, T-29, R-02, R-04, R-05
**Origen:** observación de arquitectura del PM (2026-09-10), verificada contra
`references/contrato-montaje.md`, `scripts/pptx.py`, `scripts/capitulos_youtube.py` y
`scripts/srt_alineado.py`

**Objetivo:** que `tarjetas.json` deje de ser el único de los tres consumidores de
`tomas.duracion_toma_buena` que expone solo la duración estimada, para que la fórmula de derivación
de rango de `contrato-montaje.md` siga siendo coherente con `guion-alineado.srt` una vez el dueño
tiene partes de rodaje reales.

**Requisitos:**
1. `tarjetas.json` (`scripts/pptx.py`) incorpora, por escena, un campo de duración real
   (`duracion_real_segundos`, `null`/ausente si la escena no tiene toma buena) usando
   `tomas.duracion_toma_buena` — mismo dato que ya calculan `srt_alineado.py` y
   `capitulos_youtube.py`.
2. `duracion_estimada_segundos` no se toca ni se sustituye: sigue siendo la única fuente para
   `guion.srt` (T-27) y `guion-escenas.md`. El campo de duración real es un dato adicional, nunca
   una sustitución en silencio del existente.
3. `tarjetas.json` señala si el conjunto de escenas mezcla duración real y estimada (mismo aviso
   que ya resuelve R-07 para los capítulos de YouTube).
4. `references/contrato-montaje.md` y `references/contrato-tarjetas.md` se actualizan con la
   fórmula correcta de derivación de rango cuando existe `guion-alineado.srt`.
5. Sin migración de `estado.json`: el dato de origen ya vive en `estado.json["tomas"]`;
   `tarjetas.json` es una salida derivada que se regenera en cada validación (T-30).
6. Test de integración que cruza `tarjetas.json` y `guion-alineado.srt` sobre un guion con al menos
   una toma buena registrada (mismo patrón que R-11 / hallazgo #18).

**Criterio de aceptación:** sobre un guion con al menos una escena con toma buena registrada,
`tarjetas.json` trae el campo de duración real para esa escena y ausente/`null` para las que no la
tienen; sumando esas duraciones (real cuando existe, estimada si no) se reconstruyen exactamente
los límites de escena de `guion-alineado.srt`; sobre un guion sin ninguna toma buena registrada,
`tarjetas.json` y la fórmula de derivación de rango se comportan exactamente igual que antes, sin
regresión sobre los tres guiones reales de `fixtures/reales/`.

**Cómo se entregó:** `Tarjeta.duracion_real_segundos` (`None` si la escena no tiene toma buena,
reutilizando tal cual `tomas.duracion_toma_buena`) y `ResultadoTarjetas.mezcla_duracion_real_y_estimada`
(booleano de cabecera, `true` solo si el conjunto mezcla ambos casos); `duracion_estimada_segundos`
intacta. `generar_tarjetas`/`exportar_pptx` ganan `tomas_por_escena` opcional (mismo patrón que
`srt_alineado.py`/`capitulos_youtube.py`, no integrado en el selector automático de T-30); sin él,
comportamiento idéntico a antes de R-13. `references/contrato-tarjetas.md` y `contrato-montaje.md`
actualizados con la fórmula de rango correcta. 7 tests nuevos (557→564), incluido el cruce con
`guion-alineado.srt` en `test_integracion_montaje.py`.

---

## Fase transversal F-G — Deuda técnica menor

Agrupa hallazgos de calidad menores, sin hito de producto propio, con el mismo criterio que ya
usaron F-D (R-08/R-09) y F-F (R-11). Contenía R-14, su única R-XX. **Entregada 2026-09-11.**

### R-14 — El separador de escena no debe colarse en el texto de una indicación
**Oleada / Fase:** F-G · **Migración:** No · **Depende de:** T-09
**Origen:** observación de arquitectura de R-12 (2026-09-10), registrada como hallazgo cosmético no
urgente, promovida a R-XX por afectar tres salidas y estar ya localizada en código

**Objetivo:** `scripts/clasificador.py` (T-09) incluía, dentro del `contenido` de la última sección
`no_locucion` de una escena, el separador `---` que el guion de origen usa entre escenas, cuando
esa sección era la última antes del siguiente `## BLOQUE N`. Ese `contenido` se reutilizaba sin
filtrar en `documento_revision.py` (T-16), `pptx.py` (T-29) y la cue del reproductor (R-12): en las
tres salidas, el separador aparecía pegado al final del texto mostrado como indicación `EN
PANTALLA`/`NOTA`.

**Requisitos:**
1. `clasificador.py` deja de incluir la línea de separador de escena dentro del `contenido`
   mostrado de la sección `no_locucion` que la precede, sin perder cobertura total.
2. `clasificador.reconstruir()` sigue reconstruyendo el guion de origen sin pérdida byte a byte;
   test de reconstrucción extendido con un caso que cubra una escena que termina en indicación
   seguida de separador.
3. `guion-escenas.md`, `tarjetas.json` y la cue del reproductor dejan de mostrar el `---` pegado al
   texto de la indicación, verificado sobre los tres guiones reales.
4. Sin cambio de esquema de `estado.json`.

**Criterio de aceptación:** sobre los tres guiones reales, ninguna indicación no-locución mostrada
en `guion-escenas.md`, `tarjetas.json` o el reproductor generado termina en `---`; el test de
cobertura total sigue en verde; cero regresión en la suite de tests existente.

**Cómo se entregó:** `_separar_marcador_fin_escena` extrae el `---` de fin de escena (con las
líneas en blanco que lo acompañan) en su propio bloque `no_locucion` (`senal="separador_escena"`)
antes de clasificar rótulos/inferencia, en vez de dejarlo pegado al `contenido` de la última
indicación. Nueva señal añadida a los tres sitios que la necesitan para no colarse como una
"indicación" propia ni proponerse como convención: `pdf._SENALES_ESTRUCTURALES`,
`documento_revision._SENALES_ESTRUCTURALES` y `convencion._SENALES_CONTRACTUALES`.
`references/convencion-guion.md` documenta ahora el separador. Fixture golden
`fixtures/guion-ejemplo-esperado.md` regenerado a mano. 5 tests nuevos (564→569). Verificado sobre
los tres guiones reales: cero indicación termina en `---` en `guion-escenas.md`, `tarjetas.json` ni
la cue del reproductor; reconstrucción íntegra (invariante (a)) intacta.

---

## Fase transversal F-H — Deuda técnica menor (entorno de verificación)

Agrupa hallazgos de calidad/infraestructura menores, sin hito de producto propio, con el mismo
criterio que ya usaron F-D (R-08/R-09), F-F (R-11) y F-G (R-14). Contenía R-15, su única R-XX.
**Entregada 2026-09-14.**

### R-15 — Advertir explícitamente contra el binario "pelado" de `ruff`/`mypy`/`pytest` en un contenedor de nube
**Oleada / Fase:** F-H · **Migración:** No · **Depende de:** ninguna
**Origen:** auditoría `#22` (2026-09-12)

**Objetivo:** este contenedor de nube trae, además de las versiones exactas que instala `pip
install -r requirements-dev.txt` (`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`, resueltas en
`sys.executable`), un segundo juego de los mismos tres binarios preinstalado en
`/root/.local/bin` (`mypy 1.19.1`, `ruff 0.15.8`, `pytest 9.0.2`), con esa ruta por delante en el
`PATH`. Las cuatro verificaciones reales del protocolo (`scripts/ci.py`, el hook de pre-commit) son
inmunes porque invocan siempre `sys.executable -m <herramienta>`, nunca el nombre pelado — pero un
humano o una sesión que teclee `ruff check .`, `mypy scripts tests` o `pytest` a mano en la
terminal recibe una señal distinta y, en el caso de `mypy`, activamente engañosa: 34 errores falsos
de `import-not-found` (ese entorno aislado no ve el `pytest` instalado en `dist-packages`), más los
`Untyped decorator` en cascada que provoca cada decorador de test sin tipos resueltos. El objetivo
es dejar una advertencia explícita en los dos sitios que cualquier sesión futura consulta antes de
tocar código, para que nadie pierda tiempo investigando una "regresión de tipos" que no existe.

**Requisitos:**
1. Añadir una nota breve y visible en `DEVELOPERS.md` (sección de verificación/desarrollo): la
   única verificación válida es `python scripts/ci.py` (o `python -m mypy`/`python -m ruff`/
   `python -m pytest` si se ejecutan sueltos); nunca el binario pelado (`ruff`, `mypy`, `pytest`
   sin `python -m` por delante), porque un contenedor de nube puede traer un segundo juego
   preinstalado, más nuevo que el pineado en `requirements-dev.txt` y por delante en el `PATH`, que
   da una señal distinta y en el caso de `mypy` puede devolver errores de `import-not-found` que no
   existen en la verificación real.
2. Añadir la misma advertencia, en una frase, a la sección de verificación de `SKILL.md` si la
   tiene, o como mínimo una referencia a `DEVELOPERS.md` desde ahí.
3. Tarea puramente documental: sin cambio de comportamiento en `scripts/ci.py` ni en ningún otro
   módulo — el propio hallazgo `#22` confirma que el protocolo real ya es inmune al binario pelado.
4. Sin cambio de esquema de `estado.json` ni de `Configuracion`.

**Criterio de aceptación:** `DEVELOPERS.md` contiene la advertencia explícita citando
`scripts/ci.py` (o `python -m <herramienta>`) como única fuente de verdad de la verificación y
mencionando el riesgo del binario pelado en un contenedor de nube; cero cambio en `scripts/`,
`tests/` o `assets/`; la siguiente pasada del auditor verifica la nota y cierra `#22` a `RESUELTO`.

**Cómo se entregó:** tarea puramente documental — nota visible en `DEVELOPERS.md` (bloque de cita
bajo "Verificación manual") y frase con remisión en la sección "Verificación" de `SKILL.md`,
explicando que la única verificación válida es `python scripts/ci.py` / `python -m <herramienta>`,
nunca el binario pelado. Cero cambio en `scripts/`, `tests/` o `assets/`; cuatro redes en verde
(569 tests).

---

## Oleada v6 — Cierre del contrato de montaje: límites de escena listos para ffmpeg

Convierte en tarea una inconsistencia de arquitectura verificada en el código y en la documentación
del propio contrato, con el mismo criterio que ya usaron R-12/R-13/R-14 (observación del PM,
confirmada leyendo el módulo real antes de escribir la ficha). Contenía R-16, su única R-XX.
**Entregada 2026-09-14.**

### R-16 — Límites absolutos de escena (`inicio_segundos`/`fin_segundos`) en `tarjetas.json`
**Oleada / Fase:** v6 · **Migración:** No · **Depende de:** T-33, R-13
**Origen:** observación de arquitectura del PM (2026-09-13), releyendo `references/contrato-montaje.md`
a la luz de que la fase siguiente del propio dueño es el montaje con ffmpeg

**Objetivo:** hoy `references/contrato-montaje.md` (T-33) le pide **a la cadena de montaje** que
derive el rango `[inicio_escena, fin_escena)` de cada escena sumando a mano, en orden,
`duracion_real_segundos` si existe o si no `duracion_estimada_segundos` (la misma regla que ya
implementa `mezcla_duracion_real_y_estimada` de R-13) — es la única forma documentada de saber a
qué escena pertenece un subtítulo de `guion.srt`/`guion-alineado.srt`, y la propia página advierte
de que esa fórmula deja de ser válida en cuanto existe parte de rodaje. Es exactamente el tipo de
cálculo que esta skill ya resuelve una sola vez, de forma correcta y probada (T-12
`tiempos.calcular_tiempos`, R-05, R-13): pedirle a un consumidor externo —hoy sin implementar
todavía, mañana la propia skill de montaje con ffmpeg— que la reproduzca bit a bit es aceptar un
punto de deriva silenciosa (redondeos, elegir real vs. estimada escena a escena, un futuro cambio
en T-12 que la cadena de montaje no se entera de seguir) justo en el borde entre dos sistemas, que
es donde este tipo de errores es más caro de diagnosticar. Cerrar la grieta ahora —antes de que
exista una skill de montaje real que la sufra con datos de producción— es más barato que
descubrirla después.

**Requisitos:**
1. `Tarjeta` (`scripts/pptx.py`) gana dos campos nuevos, `inicio_segundos`/`fin_segundos` (float),
   calculados **una sola vez** con la misma regla que ya usa R-13 para elegir real vs. estimada
   escena a escena, acumulando en el mismo orden en que las escenas aparecen en
   `resultado.escenas` — nunca una segunda implementación de la lógica de T-12/R-13, reutilizar la
   que ya exista o extraerla si hace falta compartirla.
2. `tarjetas_a_diccionario`/`validar_tarjetas` y `references/contrato-tarjetas.md` documentan las
   dos claves nuevas en la tabla de cada escena. Cambio **aditivo y retrocompatible** (mismo
   criterio que R-13): no sube `version_contrato`.
3. `references/contrato-montaje.md` deja de pedirle a la cadena de montaje que "sume las
   duraciones anteriores": la sección de cómo derivar el tiempo de cada escena pasa a decir que se
   lean `inicio_segundos`/`fin_segundos` directamente de `tarjetas.json`, dejando la fórmula de
   acumulación como nota de cómo se calculan (transparencia), no como instrucción a seguir.
4. Test de integración nuevo o ampliado en `tests/test_integracion_montaje.py`: `inicio_segundos`
   de la primera escena es `0`; `fin_segundos` de una escena coincide con `inicio_segundos` de la
   siguiente (sin huecos ni solapes); `fin_segundos` de la última escena coincide con el fin del
   último subtítulo de `guion.srt` (caso sin parte de rodaje) y de `guion-alineado.srt` (caso con
   parte de rodaje que mezcla real/estimado, reutilizando el guion sintético que ya prueba R-13).
5. Sin migración de `estado.json`, sin campo nuevo de `Configuracion` (son datos derivados de T-12,
   no un valor configurable por el dueño).

**Criterio de aceptación:** sobre los tres guiones reales de `fixtures/reales/`,
`inicio_segundos`/`fin_segundos` de `tarjetas.json` reconstruyen exactamente los límites de escena
que hoy exige calcular a mano `contrato-montaje.md`, tanto con todas las escenas estimadas como con
un parte de rodaje que mezcla real/estimado; el test de integración cruzada nuevo pasa;
`contrato-montaje.md` y `contrato-tarjetas.md` quedan actualizados.

**Cómo se entregó:** `Tarjeta` (`scripts/pptx.py`) gana `inicio_segundos`/`fin_segundos` por
escena, calculados una sola vez (`_con_limites_absolutos`) acumulando en el orden de las escenas
con la misma regla real-vs-estimada que ya elige `duracion_real_segundos` (R-13);
`references/contrato-tarjetas.md` documenta las dos claves nuevas (aditivo, `version_contrato` no
sube) y `references/contrato-montaje.md` deja de pedirle a la cadena de montaje que sume las
duraciones a mano — ahora lee los dos campos directamente, con la fórmula de acumulación como
transparencia, no como instrucción. 5 tests nuevos (569→574): 2 unitarios en `test_pptx.py` y 3 de
integración en `test_integracion_montaje.py` (primera escena empieza en `0` y no hay hueco/solape
entre escenas sobre los tres guiones reales; el `fin_segundos` de la última escena coincide con el
fin de `guion.srt` sin parte de rodaje y con el de `guion-alineado.srt` con parte de rodaje
mezclando real/estimado).

---

## Fase transversal F-I — Deuda técnica menor (revalidación)

Agrupa hallazgos de calidad menores, sin hito de producto propio, con el mismo criterio que ya
usaron F-D (R-08/R-09), F-F (R-11), F-G (R-14) y F-H (R-15). Contenía R-17, su única R-XX.
**Entregada 2026-09-14** (COMPLETADA el mismo día en que se abrió).

### R-17 — Endurecer o cerrar formalmente la asimetría teórica de `_incidencias_anclas_desajustadas`
**Oleada / Fase:** F-I · **Migración:** No · **Depende de:** ninguna
**Origen:** auditoría `#19` (2026-09-04), reconfirmada sin cambios en las diez pasadas siguientes del auditor

**Objetivo:** `_incidencias_anclas_desajustadas` (`scripts/revalidacion.py`, defensa en profundidad
de P-04 sobre el hallazgo #14) compara, escena a escena, el **conjunto** de índices de ancla
previstos contra los realmente leídos del documento (`previstas != escenas_leidas[numero_escena]`,
ambos `set[int]`). El hallazgo `#19` señala una asimetría teórica: esta comparación por conjunto
detecta un índice de más, de menos o distinto, pero nunca se ha verificado si existe algún camino
por el que dos disposiciones distintas de anclas pudieran producir el mismo conjunto de índices por
escena sin que el aviso salte — el propio auditor lleva diez pasadas (2026-09-04 a 2026-09-14)
reconfirmándolo como "sin escenario reproducido", nunca como un fallo real. Diez reconfirmaciones
sin resolución es ya más caro en atención de sesión futura que cerrarlo una vez, en cualquiera de
los dos sentidos posibles.

**Requisitos:**
1. Investigar, leyendo `identidad_por_ancla`/`texto_editado_por_ancla` y sus dos únicos
   productores (`tiempos.bloques_respiracion_marcados`, `troceo.trocear_guion`, ambos ya revisados
   por la auditoría de R-14), si existe una secuencia real de ediciones/particiones que produzca,
   para una misma escena, dos disposiciones de anclas distintas con el mismo conjunto de índices.
   No asumir la respuesta de partida en ningún sentido.
2. **Si se encuentra un escenario real:** endurecer la comparación para que compruebe la identidad
   exacta de cada ancla (no solo la cardinalidad/conjunto de índices por escena), añadiendo un test
   de regresión que reproduzca el escenario encontrado (falla sin el fix, pasa con él), mismo patrón
   que los tests de `#9`/`#14`.
3. **Si se confirma que es inalcanzable** dado el resto de invariantes del módulo (p. ej. porque la
   identidad `(escena, índice_original, mitad)` es inyectiva por construcción): añadir un test que
   deje esa prueba por escrito (no solo una nota en un docstring) y actualizar el registro de
   `auditoriacontinua.md` — a través del propio informe de esta tarea, nunca editando el documento
   del auditor directamente (§0.4: es el único archivo que modifica el auditor) — para que la
   siguiente pasada del auditor pueda cerrar `#19` a `RESUELTO` en vez de reconfirmarlo indefinidamente.
4. Cualquiera de los dos caminos es una tarea de calidad interna: cero cambio de esquema de
   `estado.json` ni de `Configuracion`, y ningún cambio de comportamiento observable por el dueño
   fuera de la propia corrección si el escenario resulta real.

**Criterio de aceptación:** la incertidumbre queda resuelta con evidencia en código (test nuevo) en
uno de los dos sentidos — comparación endurecida con regresión que la ejercita, o prueba explícita
de que el escenario es inalcanzable —, documentado en `DECISIONES_TECNICAS.md` con el razonamiento
seguido; la siguiente pasada del auditor puede cerrar `#19` sin tener que seguir reconfirmando la
misma nota teórica.

**Cómo se entregó:** investigada y cerrada por la vía del requisito 3 (con matiz): bajo operación
normal la identidad es inyectiva por construcción (`pospuestas_previas` siempre coincide con lo que
la pasada anterior persistió); el único escenario que rompe la comparación por cardinalidad exige
corromper `estado.validacion["particiones_pospuestas"]` a mano (misma precondición ya conocida de
P-04), y se verificó con test nuevo que incluso ahí el invariante (a) — nada se pierde ni se
duplica — sigue intacto, con un único efecto cosmético (número de bloque erróneo en la incidencia
de conflicto, escena correcta). 1 test nuevo (574→575) en `tests/test_revalidacion.py`. Cuatro
redes en verde. Detalle completo en `DECISIONES_TECNICAS.md`.

---

## Oleada v7 — Cerrar el hueco entre el registro de tomas reales y el selector de salidas

Las tomas registradas durante el rodaje (R-02/R-03) ya alimentaban tres salidas completas y
probadas desde hacía semanas — `guion-alineado.srt` (R-05), `capitulos-youtube.txt` (R-07) y los
campos reales de `tarjetas.json` (R-13/R-16) — pero ninguna de las tres era alcanzable a través del
único punto de entrada real que usa el dueño: el selector de salidas de cada validación (T-30,
`scripts/salidas.py`). Contenía R-18, su única R-XX. **Entregada 2026-09-17** (COMPLETADA el mismo
ciclo del Programador en que se implementó, tras abrirse el día anterior).

### R-18 — Integrar en el selector de salidas (T-30) las salidas que dependen de tomas reales
**Oleada / Fase:** v7 · **Migración:** No · **Depende de:** T-30, R-02, R-05, R-07, R-13, R-16
**Origen:** observación de arquitectura del PM (2026-09-16), releyendo `scripts/salidas.py` a la luz
de que la fase siguiente del propio dueño es el montaje con ffmpeg

**Objetivo:** `scripts/salidas.py` (T-30) es el único sitio donde el dueño pide de verdad que se
generen salidas — la pregunta de opción múltiple de cada validación. Hasta esta tarea, sin embargo,
ignoraba por completo `estado.tomas` (el registro de tomas de R-02, ya persistido sin migración):
`_generar_pptx` llamaba a `exportar_pptx` sin `tomas_por_escena`, así que `tarjetas.json` nunca
llevaba `duracion_real_segundos`/`inicio_segundos`/`fin_segundos` reales aunque el dueño ya hubiera
marcado tomas buenas; `_generar_srt` solo producía el `.srt` estimado (T-27), nunca
`guion-alineado.srt` (R-05); y `capitulos_youtube.py` (R-07) ni siquiera era una opción de
`TipoSalida` — la única ruta que lo ejercitaba era la fixture de `verificar_salidas.py --fixture`,
deliberadamente con `tomas_por_escena={}`. El dueño habría tenido que saber que existían tres
módulos más y saber invocarlos aparte, justo en el momento — después de grabar, camino del montaje
con ffmpeg — en que más importaba que la skill entregara sola los datos reales sin que nadie se lo
pidiera a mano. Es la misma clase de grieta que ya motivó R-12/R-13/R-14/R-16: la funcionalidad ya
existía, estaba probada y el contrato la documentaba, pero no llegaba al único flujo real por el
que el dueño interactúa con la skill.

**Requisitos:**
1. `scripts/salidas.py` lee `estado.tomas` (tal cual, mismo contenedor que ya consumen
   `srt_alineado.py`/`capitulos_youtube.py`/`pptx.py` desde R-05/R-07/R-13) y lo pasa como
   `tomas_por_escena` allí donde haga falta — quien llama a `generar_salidas_seleccionadas` (la
   sesión que ya tiene el `EstadoProyecto` cargado) se lo entrega, sin que este módulo necesite abrir
   ni conocer `estado.json` por su cuenta.
2. Seleccionar `SRT` sigue generando siempre `guion.srt` (T-27, estimado, comportamiento actual
   intacto); además, en cuanto `tomas_por_escena` contenga al menos una toma marcada `buena`, la
   misma pasada genera también `guion-alineado.srt` (R-05) como un segundo `ArchivoGenerado` bajo el
   mismo `TipoSalida.SRT` — mismo patrón que ya usan `_generar_pdf`/`_generar_pptx`, que ya devuelven
   más de un archivo bajo un mismo tipo. Sin tomas registradas, se genera exactamente lo mismo que
   antes (solo `guion.srt`): cambio aditivo, nunca una regresión.
3. Seleccionar `PPTX` pasa `tomas_por_escena` a `exportar_pptx`, de modo que `tarjetas.json` incluya
   duración real y límites absolutos reales (R-13/R-16) en cuanto haya tomas registradas, sin
   ninguna acción manual del dueño. Sin tomas, comportamiento idéntico al anterior.
4. `TipoSalida` gana una quinta opción, `CAPITULOS_YOUTUBE` ("Capítulos de YouTube con marcas de
   tiempo (`.txt`)"), añadida a `TODAS_LAS_SALIDAS`/`DESCRIPCION_SALIDA` junto a las cuatro ya
   existentes (requisito 1 de T-30: sigue siendo una única pregunta de opción múltiple, ahora con
   cinco filas en vez de cuatro). Se genera con `capitulos_youtube.generar_capitulos_youtube`,
   pasando `tomas_por_escena` (usa marcas reales si hay tomas, estimadas si no — igual que ya hacía
   `verificar_salidas.py --fixture`). Cuando el guion no trae sección `Capítulos` o no llega a una
   sola marca por encima de `capitulos_youtube_marca_minima_segundos`, la salida queda como
   `SalidaOmitida` con el motivo exacto que ya devuelve `formatear_capitulos_youtube` al dar `None`
   — nunca como fallo ni como `SalidaLatente` (no depende de nada externo ausente, a diferencia de
   `.pdf`/`.pptx`).
5. `ResumenSalidas`/`registrar_generacion`/`estado.salidas_generadas` no cambian de forma: la nueva
   ruta solo añade entradas a `generadas`/`omitidas` con los tipos ya definidos, sin romper la
   serialización ni la sugerencia de la próxima pregunta (requisito 2 de T-30).
6. Sin migración de `estado.json` (usa `estado.tomas`, presente desde R-02 sin cambio de esquema) y
   sin campo nuevo de `Configuracion` (son datos derivados de lo ya registrado por el dueño durante
   el rodaje, no un ajuste suyo).

**Criterio de aceptación:** sobre un guion sintético con al menos una escena con una toma marcada
`buena` en `estado.tomas` (mismo patrón de fixture que ya usan R-13/R-16 en
`tests/test_integracion_montaje.py`), llamar a `generar_salidas_seleccionadas` con `SRT`
seleccionado produce tanto `guion.srt` como `guion-alineado.srt`, y con `PPTX` seleccionado
`tarjetas.json` trae `duracion_real_segundos`/`inicio_segundos`/`fin_segundos` reales para esa
escena. `CAPITULOS_YOUTUBE` aparece como quinta opción de `construir_pregunta_salidas` y, generado,
coincide con lo que produce `verificar_salidas.py --fixture` en las mismas condiciones. Sobre los
tres guiones reales de `fixtures/reales/` **sin ninguna toma registrada**, el resultado completo de
`generar_salidas_seleccionadas` (archivos generados, bytes, omitidas) es idéntico al de antes de
R-18 — test de regresión explícito, no solo ausencia de error.

**Cómo se entregó:** `scripts/salidas.py` gana el parámetro opcional `tomas_por_escena` en
`generar_salidas_seleccionadas`; con al menos una toma `buena`, `SRT` genera también
`guion-alineado.srt` bajo el mismo `TipoSalida.SRT` (`_generar_srt` llama siempre a
`srt_alineado.generar_srt_alineado` cuando `tomas_por_escena` no está vacío y decide por
`ResultadoAlineacion.escenas_alineadas`, no por una inspección manual del diccionario crudo — misma
fuente de verdad que ya usan los tests de integración de R-11) y `PPTX` pasa las tomas a
`exportar_pptx` para duración real y límites absolutos reales (R-13/R-16). `TipoSalida` gana
`CAPITULOS_YOUTUBE` (quinta opción). Sin toma registrada, comportamiento idéntico al de antes de
R-18 (regresión byte a byte verificada sobre los tres guiones reales). `verificar_salidas.py::
verificar_generacion` distingue un fallo real de una omisión esperada por el prefijo
`"fallo al generar:"` del motivo, en vez de tratar cualquier `SalidaOmitida` como fallo de la etapa
(necesario porque `CAPITULOS_YOUTUBE` ya puede quedar omitida de forma legítima). 8 tests nuevos
(575→583). Cuatro redes en verde. Detalle completo en `DEVELOPERS.md` y `DECISIONES_TECNICAS.md`.

---

*(El detalle de verificación de cada entrega —commits, tests, decisiones— está en
`roadmap/HISTORIAL_SESIONES.md` y `roadmap/DECISIONES_TECNICAS.md`. La de v2/v3/F-D tiene fecha
2026-09-03; la de F-E, 2026-09-04; la de F-F, segundo ciclo del 2026-09-04; la de v4 (R-12),
2026-09-10; la de v5 (R-13) y F-G (R-14), 2026-09-11; la de F-H (R-15) y v6 (R-16), 2026-09-14; la
de F-I (R-17), 2026-09-15.)*
