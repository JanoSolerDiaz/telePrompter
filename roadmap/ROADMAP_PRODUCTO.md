# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-10-14 (ciclo de PM). **R-29 (Oleada v17) está `COMPLETADA`** (§1 de
`SEGUIMIENTO.md`) desde el ciclo de Programador del propio 2026-10-14 que la implementó (unificada la
materialización de particiones aceptadas de `revalidacion.py` con `reescrituras.py`, sin divergencia
real encontrada). Movida a `roadmap/ROADMAP_HISTORICO.md` (Oleada v17) junto con el resto de oleadas
100 % entregadas. §1 de `SEGUIMIENTO.md` llevaba desde esa misma madrugada sin ninguna fila
`PENDIENTE` — nueve reconfirmaciones horarias del Programador a lo largo del día sin tarea que
ejecutar, el mismo coste que señala el hallazgo `#30`/pregunta `#12` (aún sin respuesta del dueño).

`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (única fila, plantilla vacía): no hay
historia de rodaje real que incorporar este ciclo — el bloqueo #7 de `SEGUIMIENTO.md` §3 (grabar un
curso completo) sigue abierto. El registro de hallazgos de `auditoriacontinua.md` no trae ningún
`ABIERTO` nuevo de producto/arquitectura esta pasada: quedan los dos mismos `ABIERTO` que el ciclo
anterior (`#24`, prosa de "Cola de producto" desactualizada entre ciclos de PM; `#30`, cadencia de la
rutina "Programador"), ambos de proceso puro y severidad baja/media, sin relación con el código,
pendientes solo de la respuesta del dueño a las preguntas de gobernanza #11/#12 de `SEGUIMIENTO.md`
§6 — nada nuevo que convertir en tarea por esta vía.

**Se abre R-30** (Oleada v18): tampoco por auditoría ni por `FEEDBACK.md`, sino por el mismo tercer
criterio que abrió R-12 a R-29 — una **grieta de arquitectura verificada sobre código ya
construido**, esta vez en el propio límite declarado del producto hacia la fase siguiente.
`references/contrato-montaje.md` (T-33) documenta con precisión qué archivos deja preparados esta
skill para el montaje (`guion.srt`/`guion-alineado.srt`, `tarjetas.json`, `concat-ffmpeg.txt`,
`capitulos-ffmpeg.txt`) y da, como ilustración, fragmentos de comando `ffmpeg` sueltos con nombres de
archivo de ejemplo (`video.mp4`, `video-final.mp4`) — pero nadie encadena esos tres fragmentos en una
secuencia real, con los nombres de archivo reales del guion concreto que el dueño acaba de procesar.
El propio objetivo de producto citado en el encargo de esta sesión ("cuya fase siguiente es el
montaje con ffmpeg") queda hoy a medio cerrar: el dueño, sin equipo de producción ni apuntador, tiene
que **traducir él mismo** la documentación de referencia a comandos reales cada vez que termina de
grabar, exactamente el tipo de fricción manual que el resto del producto (selector de salidas,
`concat-ffmpeg.txt`, `capitulos-ffmpeg.txt`) ya eliminó para cada pieza por separado. Detalle
completo en "Oleada v18" más abajo.

Este ciclo es de PM, no de Programador: no se ha ejecutado la verificación de las cuatro redes; la
spec de R-30 queda lista para que el siguiente ciclo de Programador la implemente y verifique.

---

## Visión y misión

Convertir un guión de producción en `.md` en las tarjetas con el texto exacto que hay que recitar
ante la cámara, entregadas como un teleprompter web autocontenido con resaltado de karaoke, para
que grabar un vídeo de curso deje de exigir memorizar, improvisar o repetir tomas.

## Cliente objetivo y segmentos

**ICP:** Jano (Cuatroochenta) y, por extensión, cualquier formador o divulgador que graba vídeos de
curso en español a partir de guiones escritos por él mismo, sin equipo de producción ni apuntador.

**Segmentos prioritarios:** creadores en solitario que graban con guiones mixtos (locución mezclada
con indicaciones de pantalla) y que ya tienen una cadena de montaje posterior con ffmpeg, donde
esta skill es el paso previo.

## Principios de producto (innegociables; extienden §0.2 de la hoja de ruta)

1. **Nada se descarta en silencio.** Todo bloque del guión se clasifica con su motivo a la vista; si el agente duda, lo marca para revisar, no lo elimina.
2. **Una sola pasada de revisión.** El `guion-escenas.md` es el contrato con el locutor: se revisa entero en el editor, de una sentada. Nada de ping-pong escena por escena.
3. **El texto del dueño manda.** Las mejoras se proponen, nunca se imponen; el original siempre es recuperable y una edición manual jamás se sobrescribe.
4. **Un solo archivo, offline.** El reproductor abre con doble clic en cualquier máquina, sin red, sin dependencias, sin CDN. Si algo no cabe en el archivo, no entra en el producto.
5. **Legibilidad a distancia de cámara por encima de todo.** En el reproductor, cualquier disyuntiva entre estética, branding o funcionalidad y legibilidad se resuelve siempre a favor de la legibilidad.

---

## OLEADAS Y FASES

> Organización por oleadas. El **backlog inicial completo (T-00 a T-33) es la oleada v1** y su
> spec vive en `HOJA_DE_RUTA.md`; el PM no la duplica aquí. Las R-XX de este documento son lo que
> viene **después** de tener un teleprompter funcionando, más lo que entra por auditoría o por
> feedback de rodaje. El estado de todas ellas está en §1 de `SEGUIMIENTO.md`.

### Oleada v1 — Que exista y se pueda grabar con ello  *(T-00…T-33, spec en la hoja de ruta)*

Del guión al reproductor: análisis, locutabilidad, ciclo de validación, reproductor, salidas y
empaquetado. Criterio de salida de la oleada: **grabar un vídeo de curso entero usando la skill**,
que es también el criterio que conmuta el modo de operación a PRODUCCIÓN.

### Oleadas v2, v3 y fase F-D — entregadas

Las oleadas v2 (rodaje real, R-01 a R-04), v3 (continuidad con el montaje, R-05 y R-07) y la fase
transversal F-D (deuda y coherencia, R-06/R-08/R-09) tienen las nueve R-XX en **COMPLETADA** en §1
de `SEGUIMIENTO.md`, sin ningún hito de negocio propio pendiente. Se movieron a
`ROADMAP_HISTORICO.md` en el ciclo de PM del 2026-09-03; su spec completa y cómo se entregó cada
una vive ahí.

### Fases transversales F-E y F-F — entregadas

La fase F-E (robustez detectada al correr por primera vez en el Windows real del dueño, R-10) y la
fase F-F (robustez de los datos derivados del rodaje real, R-11) tienen sus R-XX en **COMPLETADA**
en §1 de `SEGUIMIENTO.md`, sin ningún hito de negocio propio pendiente. F-E se movió a
`ROADMAP_HISTORICO.md` en el ciclo de PM del 2026-09-04; F-F se movió en el segundo ciclo de PM de
ese mismo día. Su spec completa y cómo se entregó cada una vive ahí.

### Oleada v4 — entregada

La oleada v4 (señalización de las indicaciones de pantalla en el reproductor, R-12) tiene su única
R-XX en **COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin ningún hito de negocio propio pendiente. Se
movió a `ROADMAP_HISTORICO.md` en el ciclo de PM del 2026-09-10. Su spec completa y cómo se
entregó viven ahí.

### Oleada v5 y Fase transversal F-G — entregadas

La oleada v5 (coherencia de `tarjetas.json` con `guion-alineado.srt`, R-13) y la fase transversal
F-G (deuda técnica menor del separador de escena, R-14) tienen sus R-XX en **COMPLETADA** en §1 de
`SEGUIMIENTO.md`, sin ningún hito de negocio propio pendiente. Se movieron a
`ROADMAP_HISTORICO.md` en el ciclo de PM del 2026-09-11. Su spec completa y cómo se entregó cada
una vive ahí.

### Fase transversal F-H y Oleada v6 — entregadas

La fase F-H (advertencia sobre el binario "pelado" en un contenedor de nube, R-15) y la oleada v6
(límites absolutos de escena en `tarjetas.json`, R-16) tienen sus R-XX en **COMPLETADA** en §1 de
`SEGUIMIENTO.md`, sin ningún hito de negocio propio pendiente. Se movieron a
`ROADMAP_HISTORICO.md` en el ciclo de PM del 2026-09-14. Su spec completa y cómo se entregó cada
una vive ahí.

### Fase transversal F-I — entregada

La fase F-I (deuda técnica menor sobre la asimetría teórica de `_incidencias_anclas_desajustadas`,
R-17) tiene su única R-XX en **COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin ningún hito de negocio
propio pendiente. Se movió a `ROADMAP_HISTORICO.md` en este ciclo de PM (2026-09-15). Su spec
completa y cómo se entregó viven ahí.

### Oleada v7 — entregada

La oleada v7 (integrar en el selector de salidas real, T-30, las salidas que dependen de tomas
reales de rodaje: `guion-alineado.srt` de R-05, `capitulos-youtube.txt` de R-07 y los campos reales
de `tarjetas.json` de R-13/R-16, todas huérfanas del flujo real hasta entonces) tiene su única R-XX
(R-18) en **COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin ningún hito de negocio propio pendiente. Se
movió a `ROADMAP_HISTORICO.md` en este ciclo de PM (2026-09-17). Su spec completa y cómo se entregó
viven ahí.

### Oleada v8 — entregada

La oleada v8 (enlazar el parte de rodaje con el archivo de vídeo real y generar la lista de
concatenación de ffmpeg, R-19) tiene su única R-XX en **COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin
ningún hito de negocio propio pendiente. Se movió a `ROADMAP_HISTORICO.md` en este ciclo de PM
(2026-09-30). Su spec completa, cómo se entregó y la nota de gobernanza sobre cómo se justificó
abrirla (hallazgo `#26` de `auditoriacontinua.md`) viven ahí.

### Oleada v9 — entregada

La oleada v9 (anclar cada indicación `EN PANTALLA`/`NOTA` de `tarjetas.json` a un instante estimado
dentro de la escena, R-20) tiene su única R-XX en **COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin
ningún hito de negocio propio pendiente. Se movió a `ROADMAP_HISTORICO.md` en este ciclo de PM
(2026-10-01), junto con la nota de gobernanza sobre cómo se justificó abrir R-19 (hallazgo `#26` de
`auditoriacontinua.md`, ya `RESUELTO`). Su spec completa y cómo se entregó viven ahí.

### Fase transversal F-J — entregada

La fase F-J (validar `concat-ffmpeg.txt` en la ruta real de generación invocando su validador antes
de escribir a disco, y sanear `archivo_video` en el origen, R-21) tiene su única R-XX en
**COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin ningún hito de negocio propio pendiente. Se movió a
`ROADMAP_HISTORICO.md` en este ciclo de PM (2026-10-02); cierra el hallazgo `#27` de
`auditoriacontinua.md`. Su spec completa y cómo se entregó viven ahí.

### Oleada v10 — entregada

La oleada v10 (capítulos reales incrustables en el vídeo final, `capitulos-ffmpeg.txt` en formato
`FFMETADATA1` de ffmpeg, R-22) tiene su única R-XX en **COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin
ningún hito de negocio propio pendiente. Se movió a `ROADMAP_HISTORICO.md` en este ciclo de PM
(2026-10-05). Su spec completa y cómo se entregó viven ahí.

### Oleada v11 — entregada

La oleada v11 (desviaciones de convención visibles en `guion-escenas.md` y `tarjetas.json`, R-23)
tiene su única R-XX en **COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin ningún hito de negocio propio
pendiente. Se movió a `ROADMAP_HISTORICO.md` en el ciclo de PM del 2026-10-06. Su spec completa y
cómo se entregó viven ahí.

### Oleada v12 — entregada

La oleada v12 (diagnóstico real de un fallo al generar una salida, conectando el logger/diagnóstico
de T-02/T-05 a su consumidor real de `scripts/salidas.py`, R-24) tiene su única R-XX en
**COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin ningún hito de negocio propio pendiente. Se movió a
`ROADMAP_HISTORICO.md` en este ciclo de PM (2026-10-07). Su spec completa y cómo se entregó viven
ahí.

### Oleada v13 — entregada

La oleada v13 (entregar `convencion-guiones.md` de verdad al dueño, conectando `convencion.py` al
selector real de salidas de T-30, R-25) tiene su única R-XX en **COMPLETADA** en §1 de
`SEGUIMIENTO.md`, sin ningún hito de negocio propio pendiente. Se movió a `ROADMAP_HISTORICO.md` en
este ciclo de PM (2026-10-08). Su spec completa y cómo se entregó viven ahí.

### Oleada v14 — entregada

La oleada v14 (conectar el diccionario del dueño, `diccionario-locucion.json`, al flujo real de
generación y revalidación, R-26) tiene su única R-XX en **COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin
ningún hito de negocio propio pendiente. Se movió a `roadmap/ROADMAP_HISTORICO.md` en este ciclo de
PM (2026-10-09). Su spec completa y cómo se entregó viven ahí.

### Oleada v15 — entregada

La oleada v15 (cerrar el bucle del aviso de guion modificado, conectando
`estado.py::avisar_si_guion_modificado`, T-07, al flujo real y refrescando el hash guardado para que
el aviso no se repita sin motivo, R-27) tiene su única R-XX en **COMPLETADA** en §1 de
`SEGUIMIENTO.md`, sin ningún hito de negocio propio pendiente. Se movió a `ROADMAP_HISTORICO.md` en
este ciclo de PM (2026-10-12). Su spec completa y cómo se entregó viven ahí.

### Oleada v16 — entregada

La oleada v16 (conectar a su ruta real de generación los tres validadores de contrato que quedaban
huérfanos — `pptx.validar_tarjetas`, `srt.validar_srt`/`srt_alineado.validar_srt_alineado`,
`capitulos_youtube.validar_capitulos_youtube` —, mismo patrón ya cerrado por R-21/R-22, R-28) tiene
su única R-XX en **COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin ningún hito de negocio propio
pendiente. Se movió a `ROADMAP_HISTORICO.md` en este ciclo de PM (2026-10-13). Su spec completa y
cómo se entregó viven ahí.

### Oleada v17 — entregada

La oleada v17 (unificar en `revalidacion.py` la reimplementación privada de la materialización de
particiones aceptadas con la función pública ya existente de `reescrituras.py`, R-29) tiene su única
R-XX en **COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin ningún hito de negocio propio pendiente. Se
movió a `ROADMAP_HISTORICO.md` en este ciclo de PM (2026-10-14). Su spec completa y cómo se entregó
viven ahí.

### Oleada v18 — EN CURSO

#### R-30 — Encadenar en un único documento `comandos-montaje.md` los comandos `ffmpeg` reales (concatenación + subtítulos + capítulos) del guion concreto, en vez de dejar que el dueño traduzca a mano la documentación de referencia cada vez que termina de grabar

**Migración:** No (ningún campo nuevo en `estado.json`; nueva salida derivada de archivos que ya
existen, sin tocar ningún contrato existente) · **Depende de:** T-27, T-30, R-05, R-19, R-22
(todas ya `COMPLETADA`) · **Origen:** observación de arquitectura del PM (2026-10-14) — grieta de
arquitectura verificada sobre el propio límite declarado del producto hacia la fase de montaje (mismo
tercer criterio que abrió R-12 a R-29), no sobre una función concreta esta vez sino sobre un
documento de referencia.

**Objetivo:** `references/contrato-montaje.md` (T-33) ya documenta con precisión qué archivos deja
preparados esta skill (`guion.srt`/`guion-alineado.srt`, `tarjetas.json`, `concat-ffmpeg.txt`,
`capitulos-ffmpeg.txt`) y da, como ilustración para quien integre una futura skill de montaje,
fragmentos de comando `ffmpeg` sueltos con nombres de archivo de ejemplo (`video.mp4`,
`video-final.mp4`): uno para incrustar capítulos (línea 191) y la invocación del demuxer `concat`
(línea 235), cada uno aislado, sin encadenar, y sin ningún paso de subtítulos. Son correctos y están
bien probados por separado (R-19, R-21, R-22), pero nadie los une en la secuencia real —concatenar
las tomas buenas → añadir pista de subtítulos → incrustar capítulos— con los nombres de archivo
reales de un guion concreto. El dueño, formador en solitario sin equipo de producción, tiene hoy que
**traducir a mano** esa documentación de referencia a comandos ejecutables cada vez que termina de
grabar — justo el tipo de fricción manual que el resto del producto (`concat-ffmpeg.txt`,
`capitulos-ffmpeg.txt`, el propio selector de salidas de T-30) ya eliminó pieza a pieza. Cerrar este
último tramo es relevante precisamente ahora: es el primer eslabón real hacia "la fase siguiente es
el montaje con ffmpeg" que todavía exige trabajo manual fuera de la skill.

Decisiones de diseño ya tomadas para acotar el alcance:
- **Documento, no script ejecutado por la skill.** Mismo patrón que `convencion-guiones.md` (R-25) o
  `brief-pptx.md` (T-29): texto para que el dueño copie y pegue en su terminal, nunca una invocación
  real de `ffmpeg`/subproceso desde Python — la skill no gana ninguna dependencia nueva ni ejecuta
  nada fuera de su propia carpeta de salida (§0.2: cero red, runtime solo biblioteca estándar).
- **`.md`, no `.sh`/`.bat`.** El dueño instaló la skill en Windows (T-32); un documento en Markdown
  con bloques de código es legible y copiable igual en cualquier terminal (PowerShell, cmd, WSL,
  bash), sin comprometerse a la sintaxis de un intérprete de scripts concreto.
- **Subtítulos como pista blanda (`mov_text`) por defecto, con la alternativa de incrustado
  ("quemado") documentada pero comentada.** Quemar subtítulos exige recodificar vídeo (coste de
  tiempo y calidad); una pista blanda es reversible y de copia directa (`-c copy`), coherente con que
  el resto de la cadena tampoco recodifica. Queda como comentario explícito en el documento generado
  para quien lo prefiera, nunca como comando activo por defecto.
- **Usa `guion-alineado.srt` si existe, si no `guion.srt`** (mismo criterio ya establecido por R-05 /
  `references/contrato-montaje.md`: tiempos reales por delante de los estimados en cuanto hay al
  menos una toma buena).
- **Cada paso es opcional y el encadenado nunca se rompe por un hueco.** Sin `concat-ffmpeg.txt` (sin
  ningún parte de rodaje con toma buena) no hay nada real que montar todavía: la salida entera se
  omite con el motivo exacto, igual que hoy hace `concat-ffmpeg.txt` en el mismo caso. Con
  `concat-ffmpeg.txt` presente pero sin `capitulos-ffmpeg.txt` (guion sin sección «Capítulos»), la
  cadena de comandos se detiene en el paso de subtítulos y lo dice explícitamente — nunca inventa un
  paso con un archivo que no existe.

**Requisitos:**
1. Nueva función en un módulo propio (p. ej. `scripts/comandos_montaje.py`) que, a partir de la
   `Configuracion` vigente y de qué archivos existen realmente para este guion
   (`concat-ffmpeg.txt`, `guion-alineado.srt`/`guion.srt`, `capitulos-ffmpeg.txt`, los mismos nombres
   que ya usa `references/contrato-montaje.md`), construye la secuencia de 1 a 3 comandos `ffmpeg`
   encadenados: la salida de cada paso es literalmente la entrada del siguiente, sin renombrados
   intermedios que el dueño tenga que hacer a mano.
2. El documento generado (`comandos-montaje.md`, constante de módulo nueva en `config.py`, mismo
   patrón que `NOMBRE_ARCHIVO_CAPITULOS_FFMPEG`) explica en una frase qué hace cada paso, muestra el
   comando en un bloque de código listo para copiar tal cual (ninguna ruta de ejemplo, solo nombres
   de archivo reales de esta carpeta de salida), y señala con una nota expresa qué escenas de
   `concat-ffmpeg.txt` siguen con `# ESCENA N: sin_toma_buena`/`sin_archivo_anotado` (si las hay),
   para que el dueño sepa que el resultado no estará completo hasta grabar o anotar esas escenas.
3. Integrarlo como octava opción del selector de salidas (`scripts/salidas.py`, `TipoSalida`), mismo
   patrón de `try`/`except`/diagnóstico de R-24: sin `concat-ffmpeg.txt`, `SalidaOmitida` con el
   motivo exacto («aún no hay ningún parte de rodaje con una toma buena»); con él, se genera siempre,
   con o sin subtítulos/capítulos disponibles.
4. Actualizar `references/contrato-montaje.md` para que remita a esta salida como la forma real de
   obtener los comandos (los fragmentos sueltos ya documentados quedan como referencia de cómo se
   construyen, no como lo que el dueño debe copiar a mano).
5. Fuera de alcance, explícito: no se ejecuta `ffmpeg` desde la skill, ni se verifica que esté
   instalado (a diferencia de T-28 con Chrome/Edge, aquí no hace falta: el documento es texto, el
   dueño decide cuándo y con qué `ffmpeg` correrlo); no se añade recodificación, normalización de
   audio, cortes ni transiciones — solo concatenar, adjuntar subtítulos y metadatos de capítulos, las
   mismas tres piezas que la skill ya calcula; no se cambia ninguna regla de `concat_ffmpeg.py`,
   `srt.py`/`srt_alineado.py` ni `capitulos_youtube.py` en sí.

**Criterio de aceptación:** sobre un guion con parte de rodaje completo (tomas buenas anotadas con
`archivo_video` y sección «Capítulos»), `comandos-montaje.md` contiene exactamente tres comandos
`ffmpeg` encadenados en el orden concat → subtítulos → capítulos, cada uno con los nombres de archivo
reales de esa carpeta de salida y sin ninguna ruta de ejemplo; sobre el mismo guion sin sección
«Capítulos», contiene solo los dos primeros y lo dice explícitamente; sin ningún parte de rodaje, la
salida se omite con el motivo exacto y el resto de salidas se genera igual (generación independiente,
T-30 requisito 3); `references/contrato-montaje.md` remite a esta salida. Cuatro redes en verde.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
