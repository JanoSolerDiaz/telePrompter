# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-11-04 (ciclo de Product Manager). R-45 (Oleada v33) llevaba
`COMPLETADA` en §1 de `SEGUIMIENTO.md` desde el 2026-11-04 (ciclo de Programador posterior a P-12),
reconfirmada en verde en varias pasadas sucesivas del Programador sin que ningún ciclo de PM la
archivara todavía. Este ciclo archiva la Oleada v33 en `ROADMAP_HISTORICO.md` y abre R-46 (Oleada
v34) en §1, sin implementarla: el criterio de una sola R-XX pendiente de código a la vez (vigente
desde R-19) queda respetado porque no había ninguna otra R-XX pendiente antes de abrir esta.

`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (única fila, plantilla vacía): no hay
historia de rodaje real que incorporar — el bloqueo #7 de `SEGUIMIENTO.md` §3 (grabar un curso
completo) sigue abierto, ahora 62 días desde que T-32 lo dejó listo para grabar (2026-09-03).
`auditoriacontinua.md` revisado entero antes de elegir tarea, hasta su pasada del 2026-11-04: cero
hallazgos nuevos desde el ciclo de PM anterior. Esa misma pasada cierra `#39` y `#41` (P-10 y P-11,
ambos reverificados en código/documentación), aplica el remedio que el propio `#38` proponía
(condensar `#24`/`#30` en la narrativa, ya cerrado) y pasa `#36` a `ASUMIDO` (riesgo aceptado por el
auditor, sin acción pendiente). Solo quedan `ABIERTO`: `#24`/`#30`, de proceso/gobernanza pura,
pendientes solo de la respuesta del dueño a las preguntas #11/#12 de `SEGUIMIENTO.md` §6 (49/25 días
sin respuesta); y `#40` (baja, rotación por trimestre de `DECISIONES_TECNICAS.md`), ya resuelto en
código por **P-12** en esta misma jornada, pendiente solo de que la próxima pasada del auditor lo
reverifique y lo cierre. Ninguno de los tres es de severidad alta en las categorías que exigirían una
P-XX urgente (pérdida de texto del guion, corrupción de estado, rotura del reproductor o de su
auto-contención, seguridad), y ninguno es convertible en una R-XX de producto.

**Nota de producto de este ciclo (no es una R-XX, es una llamada de atención sobre el ritmo del
propio roadmap, repetida desde ciclos anteriores porque el hecho que la motiva no ha cambiado):** van
45 R-XX completadas desde que T-32 dejó la skill instalada y verificada en la máquina real del dueño
(2026-09-03), y ninguna de ellas viene todavía de un rodaje real — todas tienen `origen: auditoría
#N` o `observación de arquitectura/producto del PM`. Es trabajo de buena calidad (cuatro redes en
verde, 790 tests, invariantes reverificados en cada auditoría), pero el propio principio de producto
que guía este documento —"utilidad real para un formador que graba vídeos de curso"— solo se
confirma grabando, no leyendo código. El bloqueo #7 es una acción del dueño, no una tarea que el
equipo pueda ejecutar por su cuenta, así que este ciclo no lo repite como pregunta nueva; se deja
constancia aquí para que quede explícito que el criterio de salida de la Oleada v1 ("grabar un vídeo
de curso entero") sigue siendo, con diferencia, el hito de mayor valor pendiente del proyecto, por
delante de cualquier R-XX nueva. R-46 (más abajo) sigue el mismo criterio que R-39 a R-45: una mejora
pequeña y de bajo riesgo del propio reproductor, directamente útil para esa primera sesión real
cuando ocurra — en vez de otro resumen de lectura en el índice (ya hay varios: progreso, indicaciones,
tropiezos, ritmo), esta vez da margen de reacción ante una indicación `EN PANTALLA`/`NOTA` (R-12),
anticipándola en el bloque anterior para que cambiar de ventana o preparar una diapositiva no exija
cortar la locución en seco.

**Oleada v33 (R-45) archivada.** Spec completa y "Cómo se entregó" en `ROADMAP_HISTORICO.md`.

**Oleada v34 (R-46) abierta, sin implementar.** Ficha completa más abajo. Origen: observación de
arquitectura del PM (2026-11-04): `anclar_indicaciones_a_bloques`/`_indicaciones_ancladas_por_indice`
(R-12/R-20) ya ancla cada indicación `EN PANTALLA`/`NOTA` al bloque de locución que la precede y la
muestra en cuanto ese bloque se vuelve activo — pero para un formador en solitario, ejecutar esa
indicación (cambiar de ventana, mostrar una diapositiva, abrir una demo) rara vez es instantáneo, y
hoy el aviso llega justo cuando toca actuar, sin ningún margen para prepararlo sin cortar el ritmo de
la locución. R-46 reutiliza el mismo array ya anclado, un bloque antes, mismo principio que R-39 a
R-45: reutilizar un dato ya calculado, sin segunda implementación.

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

### Oleada v18 — entregada

La oleada v18 (encadenar en `comandos-montaje.md` los comandos `ffmpeg` reales de montaje —
concatenación de tomas buenas + subtítulos + capítulos—, R-30) tiene su única R-XX en **COMPLETADA**
en §1 de `SEGUIMIENTO.md`, sin ningún hito de negocio propio pendiente. Se movió a
`ROADMAP_HISTORICO.md` en este ciclo de PM (2026-10-15), junto con la nota de gobernanza sobre cómo
se corrigió el hallazgo `#31` (fila de apertura faltante en `DECISIONES_TECNICAS.md`). Su spec
completa y cómo se entregó viven ahí.

### Oleada v19 — entregada

La oleada v19 (avisar en `comandos-montaje.md` de archivos referenciados que no existen todavía en
la carpeta de salida real, R-31) tiene su única R-XX en **COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin
ningún hito de negocio propio pendiente. Se movió a `ROADMAP_HISTORICO.md` en este ciclo de PM
(2026-10-16). Su spec completa y cómo se entregó viven ahí.

### Oleada v20 — entregada

La oleada v20 (distinguir, en el exportador `.pdf`, un fallo real de la conversión de Chrome/Edge
de la simple ausencia de Chrome/Edge, R-32) tiene su única R-XX en **COMPLETADA** en §1 de
`SEGUIMIENTO.md` desde el 2026-10-16, sin ningún hito de negocio propio pendiente. Se movió a
`ROADMAP_HISTORICO.md` en este ciclo de PM (2026-10-19). Su spec completa y cómo se entregó viven
ahí.

### Oleada v21 — entregada

La oleada v21 (checklist reabrible de "Preparación antes de grabar" en el índice del reproductor,
R-33) tiene su única R-XX en **COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin ningún hito de negocio
propio pendiente. Se movió a `ROADMAP_HISTORICO.md` en este ciclo de PM (2026-10-19, tercer ciclo
del día). Su spec completa y cómo se entregó viven ahí.

### Oleada v22 — entregada

La oleada v22 (capturar el instante real, en segundos desde el inicio de la toma, en que se marca un
tropiezo durante la grabación, para saltar directo al punto de corte en el montaje con ffmpeg, R-34)
tiene su única R-XX en **COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin ningún hito de negocio propio
pendiente. Se movió a `ROADMAP_HISTORICO.md` en este ciclo de PM (2026-10-20). Su spec completa y
cómo se entregó viven ahí.

### Oleada v23 — entregada

La oleada v23 (relocalizar por texto, no por índice, un tropiezo guardado en `localStorage` cuando
el troceo de la escena cambió desde que se marcó, para que el indicador "⚠ Tropiezo" nunca señale el
bloque equivocado, R-35) tiene su única R-XX en **COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin ningún
hito de negocio propio pendiente. Se movió a `ROADMAP_HISTORICO.md` en este ciclo de PM (2026-10-21).
Su spec completa y cómo se entregó viven ahí.

### Oleada v24 — entregada

La oleada v24 (vincular cada tropiezo marcado con el número de la toma en que se marcó, R-36) tiene
su única R-XX en **COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin ningún hito de negocio propio
pendiente. Se movió a `ROADMAP_HISTORICO.md` en este ciclo de PM (2026-10-22). Su spec completa y
cómo se entregó viven ahí.

### Oleada v25 — entregada

La oleada v25 (cruzar automáticamente «Toma» con la toma buena ya registrada en el parte de rodaje,
para que `FEEDBACK.md` diga de un vistazo qué tropiezos son de fiar como punto de corte real, R-37)
tiene su única R-XX en **COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin ningún hito de negocio propio
pendiente. Se movió a `ROADMAP_HISTORICO.md` en este ciclo de PM (2026-10-23). Su spec completa y
cómo se entregó viven ahí.

### Oleada v27 — entregada

La oleada v27 (progreso de grabación visible en el índice de escenas, R-39) tiene su única R-XX en
**COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin ningún hito de negocio propio pendiente. Se movió a
`ROADMAP_HISTORICO.md` en este ciclo de PM (2026-10-27). Su spec completa y cómo se entregó viven
ahí.

### Oleada v28 — entregada

La oleada v28 (botón "Grabar siguiente pendiente" en el índice de escenas, R-40) tiene su única R-XX
en **COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin ningún hito de negocio propio pendiente. Se movió a
`ROADMAP_HISTORICO.md` en este ciclo de PM (2026-10-28). Su spec completa y cómo se entregó viven
ahí.

### Oleada v29 — entregada

La oleada v29 (foco automático en "Grabar siguiente pendiente" al cerrar una toma buena, R-41) tiene
su única R-XX en **COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin ningún hito de negocio propio
pendiente. Se movió a `ROADMAP_HISTORICO.md` en este ciclo de PM (2026-10-29). Su spec completa y
cómo se entregó viven ahí.

### Oleada v31 — entregada

La oleada v31 (avisar en el índice cuando la toma buena de una escena trae un tropiezo marcado
dentro, R-43) tiene su única R-XX en **COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin ningún hito de
negocio propio pendiente. Se movió a `ROADMAP_HISTORICO.md` en este ciclo de PM (2026-11-02). Su spec
completa y cómo se entregó viven ahí.

### Oleada v32 — entregada

La oleada v32 (resumen agregado, en la cabecera del índice, de cuántas escenas tienen la toma buena
con un tropiezo dentro, R-44) tiene su única R-XX en **COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin
ningún hito de negocio propio pendiente. Se movió a `ROADMAP_HISTORICO.md` en este ciclo de PM
(2026-11-03). Su spec completa y cómo se entregó viven ahí.

### Oleada v33 — entregada

La oleada v33 (aviso de desviación de ritmo de T-12, visible por fila y agregado en la cabecera del
índice, R-45) tiene su única R-XX en **COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin ningún hito de
negocio propio pendiente. Se movió a `ROADMAP_HISTORICO.md` en este ciclo de PM (2026-11-04). Su spec
completa y cómo se entregó viven ahí.

### Oleada v34 — Anticipar, en el bloque anterior, una indicación EN PANTALLA/NOTA próxima

#### R-46 — Mostrar en el bloque inmediatamente anterior un anticipo de la indicación anclada al bloque siguiente, para dar tiempo a prepararla sin cortar la locución

**Migración:** No (sin campo nuevo en el JSON embebido ni cambio de contrato; se calcula enteramente
en `assets/reproductor/guion.js` a partir del array `bloque.indicaciones` que R-12/R-20 ya incrustan
por bloque) · **Depende de:** R-12 (`anclar_indicaciones_a_bloques`/`_indicaciones_ancladas_por_indice`,
cue `.cue-indicacion` por bloque en `renderizarReproductor`), R-20 (extensión del mismo anclaje a
`tarjetas.json`, sin tocar esta ficha), T-19/T-20 (índice y motor de bloques), T-23 (patrón de
indicadores ocultables, `indicadores-ocultos`) — todas `COMPLETADA` · **Origen:** observación de
arquitectura del PM (2026-11-04). R-12 ancla cada indicación `EN PANTALLA`/`NOTA` al bloque de
locución que la precede y la muestra en cuanto ese bloque se vuelve activo — pero para un formador en
solitario, ejecutar esa indicación (cambiar de ventana, mostrar una diapositiva, abrir una demo) rara
vez es instantáneo: exige dejar de mirar la cámara, actuar sobre el ordenador y volver. Hoy el aviso
llega en el mismo instante en que toca actuar, sin ningún margen para prepararlo sin cortar el ritmo
de la locución. Mismo principio que R-39/R-42/R-44/R-45: reutilizar un dato ya calculado y ya
probado, sin segunda implementación del anclaje.

**Objetivo:** que el formador, mientras recita el bloque inmediatamente anterior a una indicación de
pantalla, sepa que se aproxima y qué dice exactamente, para poder prepararla (cambiar de ventana,
tener la diapositiva a mano) sin interrumpir la locución ni descubrir la indicación tarde.

**Requisitos:**
1. En `renderizarReproductor` (`assets/reproductor/guion.js`), en el mismo `escena.bloques.forEach`
   donde ya se añade un `<p class="cue-indicacion">` por cada elemento de `bloque.indicaciones` al
   propio bloque que la ancla (R-12), añadir también, al bloque INMEDIATAMENTE ANTERIOR dentro de la
   misma escena (si existe), un `<p class="cue-proxima-indicacion">` por cada indicación del bloque
   siguiente, con el texto `"Después: "` seguido del texto ya formateado que trae
   `bloque.indicaciones` (reutilizado tal cual, sin releer el JSON de otra forma ni tocar
   `scripts/reproductor.py`, `scripts/pdf.py` ni `scripts/pptx.py`).
2. El primer bloque de una escena nunca recibe un anticipo "hacia atrás" desde la escena anterior
   (ámbito limitado a la escena actual, igual que el motor de avance no cruza de una escena a otra sin
   paso manual por el índice); el ÚLTIMO bloque de una escena nunca anticipa una indicación anclada al
   primer bloque de la escena siguiente, por el mismo motivo.
3. CSS nuevo en `assets/reproductor/estilo.css`: `.cue-proxima-indicacion` reutiliza la misma regla de
   visibilidad que `.cue-indicacion` (oculta por defecto, visible solo mientras el bloque que la
   contiene tiene la clase `.bloque--activo`, y plegada junto con el resto de indicadores bajo
   `#vista-reproductor.indicadores-ocultos`), pero con un peso visual todavía más subordinado
   (opacidad o tamaño de fuente menor que `.cue-indicacion`) para que nunca se confunda con la cue del
   bloque activo, que es la que exige una acción inmediata — principio de producto 5.
4. Cuando el bloque siguiente tiene varias indicaciones ancladas, el anticipo las lista todas en el
   mismo orden en que `.cue-indicacion` las mostrará cuando ese bloque pase a ser el activo, sin
   fusionar ni resumir su texto.
5. Sin campo nuevo en el JSON embebido (verificado por diff de claves contra la salida de referencia
   anterior a R-46), sin cambio en `scripts/reproductor.py`, `scripts/pdf.py`, `scripts/pptx.py`,
   `scripts/documento_revision.py` ni en `anclar_indicaciones_a_bloques`/
   `_indicaciones_ancladas_por_indice` — mejora enteramente del lado cliente sobre un array ya
   embebido por R-12/R-20.
6. Sin elemento interactivo nuevo, sin tecla nueva, sin `localStorage` nuevo, sin migración. El
   anticipo se recalcula solo al reconstruir la vista de la escena (misma `renderizarReproductor` ya
   existente), sin ningún disparador adicional.

**Criterio de aceptación:** sobre una fixture con al menos tres bloques consecutivos de una misma
escena donde el bloque del medio ancla una indicación `Pantalla:` y ningún otro bloque ancla ninguna
— mientras el bloque ANTERIOR al del medio está activo, su `<li>` contiene un
`<p class="cue-proxima-indicacion">` visible con el texto `"Después: "` + el texto exacto que trae
`bloque.indicaciones` del bloque del medio; al avanzar al bloque del medio, ese anticipo deja de estar
visible (ya no es el bloque activo) y la cue real (`.cue-indicacion`) de ese mismo bloque, sin el
prefijo `"Después:"`, aparece en su lugar. En el primer bloque de cualquier escena no aparece nunca un
anticipo de la escena anterior, y en el último bloque de una escena no aparece nunca un anticipo de
la primera de la siguiente, aunque ambas existan y tengan indicaciones ancladas. El JSON embebido por
`scripts/reproductor.py` no gana ningún campo nuevo. Verificado también visualmente con
Playwright/Chromium real, mismo criterio que R-39 a R-45.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
