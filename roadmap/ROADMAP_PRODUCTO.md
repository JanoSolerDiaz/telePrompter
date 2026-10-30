# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-10-30 (ciclo de Product Manager). R-42 (Oleada v30) llevaba
`COMPLETADA` en §1 de `SEGUIMIENTO.md` desde el mismo día (ciclo de Programador), reconfirmada en
verde en varias pasadas sucesivas del Programador (incluida la que cerró P-09, hallazgo `#35`) sin
que ningún ciclo de PM la archivara todavía. Este ciclo archiva la Oleada v30 en
`ROADMAP_HISTORICO.md` y abre R-43 (Oleada v31) en §1, sin implementarla: el criterio de una sola
R-XX pendiente de código a la vez (vigente desde R-19) queda respetado porque no había ninguna otra
R-XX pendiente antes de abrir esta.

`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (única fila, plantilla vacía): no hay
historia de rodaje real que incorporar — el bloqueo #7 de `SEGUIMIENTO.md` §3 (grabar un curso
completo) sigue abierto, ahora más de 57 días desde que T-32 lo dejó listo para grabar (2026-09-03).
`auditoriacontinua.md` revisado antes de elegir tarea: `#24` (baja) y `#30` (media) siguen `ABIERTO`
de proceso/gobernanza puro, pendientes solo de la respuesta del dueño a las preguntas #11/#12 de
`SEGUIMIENTO.md` §6 (44 y 20 días sin respuesta cuando se registraron); `#35` (baja, cabecera "PARA
EL DUEÑO") ya tiene su remedio aplicado por P-09 (2026-10-30), pendiente solo de que el Auditor lo
verifique y lo cierre (escritura exclusiva suya); `#36` (baja, apertura en inglés de un commit) es
puramente observacional, sin remedio retroactivo razonable. Ninguno de severidad alta, ninguno
convertible en R-XX nueva ni en deuda técnica de backlog.

**Nota de producto de este ciclo (no es una R-XX, es una llamada de atención sobre el ritmo del
propio roadmap):** van 42 R-XX completadas desde que T-32 dejó la skill instalada y verificada en la
máquina real del dueño (2026-09-03), y ninguna de ellas viene todavía de un rodaje real — todas
tienen `origen: auditoría #N` o `observación de arquitectura/producto del PM`. Es trabajo de buena
calidad (cuatro redes en verde, 763 tests, invariantes reverificados en cada auditoría), pero el
propio principio de producto que guía este documento —"utilidad real para un formador que graba
vídeos de curso"— solo se confirma grabando, no leyendo código. El bloqueo #7 es una acción del
dueño, no una tarea que el equipo pueda ejecutar por su cuenta, así que este ciclo no lo repite como
pregunta nueva; se deja constancia aquí para que quede explícito que el criterio de salida de la
Oleada v1 ("grabar un vídeo de curso entero") sigue siendo, con diferencia, el hito de mayor valor
pendiente del proyecto, por delante de cualquier R-XX nueva. R-43 (más abajo) sigue el mismo criterio
que R-39/R-40/R-41/R-42: una mejora pequeña y de bajo riesgo del propio reproductor, directamente útil
para esa primera sesión real cuando ocurra — y además cierra un hueco real entre dos piezas ya
construidas (R-37/R-38) que resuelven el mismo cruce de datos pero solo lo muestran al exportar, no
durante la propia grabación, que es el momento en que la decisión de repetir una toma todavía es
barata.

**Oleada v30 (R-42) archivada.** Spec completa y "Cómo se entregó" en `ROADMAP_HISTORICO.md`.

**Oleada v31 (R-43) abierta, sin implementar.** Ficha completa más abajo. Origen: observación de
arquitectura del PM (2026-10-30): R-37 (`scripts/feedback.py`) y R-38 (`scripts/comandos_montaje.py`)
ya resuelven, del lado de Python, el cruce "¿el tropiezo marcado cayó dentro de la toma que se usó
como buena?" — pero los dos solo se ven al exportar (`FEEDBACK.md`, `comandos-montaje.md`),
normalmente al final de la sesión de rodaje o incluso del guión entero. El propio `assets/
reproductor/guion.js` ya tiene en memoria, en el índice de escenas, los mismos dos datos que hacen
falta para el mismo cruce (tomas con `buena`/`numero` de R-02, tropiezos con `numero_toma` ya
persistido desde R-36), así que mostrar el aviso ahí mismo, sin exportar nada, adelanta la decisión
al momento en que el dueño todavía puede volver a grabar la toma con el resto del material fresco.

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

### Oleada v31 — Avisar en el índice cuando la toma buena de una escena trae un tropiezo marcado dentro

#### R-43 — El índice de escenas avisa, de un vistazo, cuando la toma marcada como buena de una escena tiene uno o más tropiezos marcados dentro de ella

**Migración:** No (lectura pura de datos que ya existen en `localStorage`: `tomasEscena[indice]`
con `buena`/`numero` de R-02, `tropiezosEscena[indice]` con `numero_toma` ya persistido desde R-36;
ningún campo nuevo, ninguna escritura nueva, sin cambio en `scripts/reproductor.py` ni en el
contrato embebido) · **Depende de:** T-19 (índice de escenas, `renderizarIndice`), R-02 (registro de
tomas, campo `buena`), R-03 (marcar tropiezos), R-34 (instante de toma del tropiezo), R-36 (número
de toma asociado a cada tropiezo, ya persistido en el propio `localStorage` del reproductor, no solo
en `FEEDBACK.md`), R-37 y R-38 (mismo cruce «¿cayó dentro de la toma buena?» ya resuelto del lado de
Python, en `scripts/feedback.py` y `scripts/comandos_montaje.py` respectivamente) — todas
`COMPLETADA` · **Origen:** observación de arquitectura del PM (2026-10-30). R-37 y R-38 resuelven el
mismo cruce dos veces, en dos documentos de salida distintos, pero los dos se generan al exportar —
normalmente al final de toda la sesión de rodaje. `guion.js` ya tiene en memoria, en el momento
exacto en que el dueño marca una toma como buena (o revisa el índice más tarde), los dos datos que
hacen falta para el mismo cruce, sin tocar ningún archivo ni esperar a exportar nada; hoy esa
coincidencia queda invisible en el propio índice, el sitio donde el dueño decide, escena a escena, si
seguir grabando o volver atrás.

**Objetivo:** que el dueño vea, sin salir del índice y sin exportar nada, que la toma que acaba de
marcar (o ya tenía marcada) como buena de una escena contiene un tropiezo señalado dentro de ella —
para decidir en el momento, con el resto del material todavía fresco, si volver a grabar esa toma o
aceptarla sabiendo que el montaje con ffmpeg tendrá que cortar en ese instante exacto (ya calculado
por R-34 y ya citado en `comandos-montaje.md` por R-38).

**Requisitos:**
1. En `renderizarIndice` (`assets/reproductor/guion.js`), en el bloque donde ya se calcula
   `resumenTropiezos`, reutilizar tal cual las variables `tomaBuena` y `tropiezosDeEscena` ya
   calculadas más arriba en la misma función (sin segunda consulta a `localStorage`) para filtrar los
   tropiezos cuyo `numero_toma` coincida con `tomaBuena.numero` — solo cuando `tomaBuena` existe; sin
   toma buena, ningún tropiezo puede estar "dentro" de ella por definición y el requisito no se
   activa. Mismo criterio de comparación que ya usan `scripts/feedback.py` (R-37) y
   `scripts/comandos_montaje.py` (R-38), ahora reflejado del lado del cliente.
2. Si ese filtrado da uno o más tropiezos, añadir al `<span class="escena-tropiezos">` ya existente
   (o un `<span>` hermano inmediato, `escena-tropiezos-en-buena`) el aviso "⚠ N en la toma buena"
   (singular "⚠ 1 en la toma buena", mismo criterio singular/plural que el resto de resúmenes de la
   fila) — nunca sustituyendo el recuento total de tropiezos de la escena que R-03 ya muestra, solo
   añadiendo el matiz de cuáles caen dentro de la toma que de verdad se usaría en el montaje.
3. CSS nuevo en `assets/reproductor/estilo.css`, reutilizando el lenguaje visual de aviso que ya usa
   `.indicador-tropiezo` (R-03: color de acento, negrita) en vez del gris discreto de
   `.escena-tropiezos`/`.escena-tomas`/`.escena-indicaciones` — es la única de las líneas de resumen
   de la fila que puede exigir una decisión del dueño, no solo informar, así que merece distinguirse
   sin llegar a competir con el título de la escena ni con la insignia de estado (principio de
   producto 5: legibilidad por encima de todo).
4. Sin elemento interactivo nuevo (`<span>`, nunca un control — `fila` ya es un `<button>`, mismo
   criterio que R-02/R-03/R-42); sin `localStorage` nuevo; sin cambio en `scripts/reproductor.py`,
   `scripts/feedback.py`, `scripts/comandos_montaje.py` ni en el contrato embebido — mejora
   enteramente de lectura y presentación sobre datos que ya existen en el propio `guion.js`.
5. El aviso se recalcula solo (mismo patrón que R-39/R-40/R-41/R-42, sin heurística de refresco
   nueva): `finalizarTomaActual`/`alternarTropiezoBloqueActual` ya llaman a `renderizarIndice()`, así
   que la siguiente vuelta al índice recalcula el filtrado sin cableado adicional.

**Criterio de aceptación:** sobre una fixture con al menos tres escenas de prueba — (a) una sin
ninguna toma, (b) una con una toma buena y ningún tropiezo marcado con ese mismo `numero_toma`
(puede tener tropiezos de tomas anteriores descartadas), y (c) una con una toma buena que sí tiene
uno o más tropiezos marcados con ese `numero_toma` — el índice no muestra ningún aviso en (a) ni en
(b) (en (b), el resumen de tropiezos sigue mostrando su recuento total si lo hay, simplemente sin el
añadido de aviso) y muestra "⚠ 1 en la toma buena" (o el plural correspondiente) en (c), con el
estilo de `.indicador-tropiezo` reutilizado. El JSON embebido por `scripts/reproductor.py` no gana
ningún campo nuevo (mismo contrato que antes de R-43, verificado por diff contra la salida de
referencia). Verificado también visualmente con Playwright/Chromium real, mismo criterio que
R-37/R-38/R-39/R-40/R-41/R-42.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
