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

*(El detalle de verificación de cada entrega —commits, tests, decisiones— está en
`roadmap/HISTORIAL_SESIONES.md` y `roadmap/DECISIONES_TECNICAS.md`, ambos con fecha 2026-09-03.)*
