# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-10-22 (ciclo de Product Manager). R-36 (Oleada v24) llevaba
`COMPLETADA` en §1 de `SEGUIMIENTO.md` desde el ciclo de Programador de esta misma jornada,
reconfirmada en verde nueve veces seguidas sin que ningún ciclo de PM la archivara todavía. Este
ciclo archiva la Oleada v24 en `ROADMAP_HISTORICO.md` y abre R-37 (Oleada v25) en §1, sin
implementarla: el criterio de una sola R-XX pendiente de código a la vez (vigente desde R-19) queda
respetado porque no había ninguna otra R-XX pendiente antes de abrir esta.

`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (única fila, plantilla vacía): no hay
historia de rodaje real que incorporar — el bloqueo #7 de `SEGUIMIENTO.md` §3 (grabar un curso
completo) sigue abierto. `auditoriacontinua.md` revisado antes de elegir tarea: solo dos `ABIERTO`
(`#24`, baja; `#30`, media), ambos de proceso/gobernanza puro y pendientes solo de la respuesta del
dueño a las preguntas #11/#12 de `SEGUIMIENTO.md` §6 — ninguno de severidad alta, ninguno
convertible en R-XX nueva ni en deuda técnica de backlog. (El hallazgo documental `#33`, cerrado por
P-07 el 2026-10-21, ya lo reconfirmó `RESUELTO` la auditoría del 2026-10-22.)

**Oleada v24 (R-36) archivada.** Spec completa y "Cómo se entregó" en `ROADMAP_HISTORICO.md`.

**Oleada v25 (R-37) abierta, sin implementar.** Ficha completa más abajo. Origen: observación de
producto del propio PM (2026-10-22), que cierra el hueco que la propia R-36 dejó anotado como fuera
de alcance explícito en su requisito 7: "no se cruza automáticamente «Toma» contra el registro de
tomas para anotar en el propio `FEEDBACK.md`... el dueño hace el cruce a mano con el número de toma
que ya tiene en el parte de rodaje". Ese cruce manual, repetido por cada fila de cada guion, es
exactamente el tipo de dato que la skill ya tiene en memoria por partida doble (número de toma de
cada tropiezo desde R-36, toma marcada `buena` de cada escena desde R-02/R-11) sin fusionarlo
todavía — mismo criterio que ya aplicaron R-19/R-20/R-22 al montaje.

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

### Oleada v25 — Cruzar automáticamente «Toma» con la toma buena registrada en el parte de rodaje

#### R-37 — Marcar en `FEEDBACK.md`, de un vistazo y sin cruce manual, qué tropiezos pertenecen a la toma que el parte de rodaje ya tiene marcada como buena

**Migración:** No (ninguna clave nueva en el `.json` que exporta "Exportar tropiezos":
`references/contrato-tropiezos.md` no sube de versión — la columna nueva de `FEEDBACK.md` se calcula
en el momento de escribir la fila, cruzando el registro de tropiezos recién exportado contra
`estado.tomas` ya fusionado por R-02, sin guardar el resultado en ningún `.json`) · **Depende de:**
R-02 (parte de rodaje, toma marcada `buena`), R-03 (tropiezos marcados), R-36 (número de toma de
cada tropiezo) — todas `COMPLETADA` · **Origen:** observación de producto del PM (2026-10-22), no de
auditoría ni de feedback de rodaje (`roadmap/FEEDBACK.md` sigue vacío) — cierra el hueco que la
propia R-36 dejó anotado como fuera de alcance explícito (su requisito 7: "no se cruza
automáticamente «Toma» contra el registro de tomas para anotar en el propio `FEEDBACK.md`... el
dueño hace el cruce a mano con el número de toma que ya tiene en el parte de rodaje"), ahora que
ambos datos (número de toma de cada tropiezo, toma marcada buena de cada escena) ya existen en
código construido y verificado.

**Objetivo:** R-36 resolvió la ambigüedad de A QUÉ TOMA pertenece cada tropiezo, pero dejó sobre el
dueño la responsabilidad de, cada vez que abre `FEEDBACK.md`, comparar a mano la columna «Toma» de
cada fila contra el número que el parte de rodaje tiene marcado como la toma buena de esa escena —
un cruce mecánico, repetido por cada fila de cada guion, con la misma fuente de error que motivó
R-34/R-35/R-36 en primer lugar: un dato que ya existe en dos archivos distintos y que nadie fusiona
todavía. El principio de producto 1 ("nada se descarta en silencio") se extiende aquí por el mismo
criterio que ya aplicaron R-19/R-20/R-22 al montaje: si la skill ya tiene en memoria los dos datos
que hacen falta para la respuesta, no debe dejar que el dueño la reconstruya a mano para cada fila.

**Requisitos:**
1. `scripts/feedback.py::registrar_tropiezos_en_feedback` gana un parámetro opcional
   `tomas_por_escena: dict[str, Any] | None = None` — mismo contenedor, sin transformarlo, que
   `EstadoProyecto.tomas` (claves de número de escena en texto), para quien ya tiene `estado.json`
   cargado al llamar. Con el valor por defecto (`None`), el comportamiento es idéntico al de hoy:
   ninguna llamada existente (ni ningún test ya escrito) se rompe por no pasarlo.
2. Por cada tropiezo con `numero_toma` no `None` (R-36): si `tomas_por_escena` trae esa escena,
   reutilizar tal cual `tomas.toma_buena(tomas_por_escena.get(str(numero_escena)), numero_escena)`
   (ya construida por R-02/R-11, sin una segunda implementación de la regla de exclusividad "como
   mucho una toma buena por escena") para obtener la toma marcada `buena`, si la hay, y comparar su
   `numero` con `tropiezo.numero_toma`.
3. Columna nueva «¿Toma buena?» en `FEEDBACK.md`, entre «Toma» e «Instante» (agrupa las dos pistas de
   fiabilidad del instante — qué toma y si es la buena — antes del propio segundo): `"sí"` si los
   números coinciden, `"no"` si no coinciden, vacía en cualquier otro caso (no se pasó
   `tomas_por_escena`; la escena no tiene ninguna toma marcada `buena` todavía; o el tropiezo no trae
   `numero_toma` por ser de una versión del contrato anterior a R-36) — nunca un valor inventado
   cuando falta el dato.
4. `_PATRON_FILA` gana un cuarto grupo opcional en la propia expresión regular (mismo patrón ya
   usado para «toma»/«instante» desde R-34/R-36), para que una fila de la versión de formato
   anterior (7 columnas, sin esta) se siga reconociendo exactamente igual — ninguna fila ya marcada
   a mano por el dueño (`nuevo`/`resuelto`) deja de encontrarse por el cambio de formato.
5. Cabecera de `FEEDBACK.md` (`_ENCABEZADO_FEEDBACK`) documenta la columna nueva y dice
   explícitamente que reemplaza el cruce manual que hasta ahora exigía abrir el parte de rodaje
   aparte — conservando el aviso ya existente para cuando la columna queda vacía (sigue haciendo
   falta el cruce a mano en ese caso, p. ej. antes de que el dueño marque ninguna toma como buena).
6. `references/contrato-tropiezos.md` NO sube de versión (nada cambia en el `.json` que exporta el
   reproductor: la comparación vive enteramente en Python, al volcar a `FEEDBACK.md`, no en
   `guion.js` ni en el contrato exportado); su sección "`FEEDBACK.md` (carpeta de salida): la misma
   información, en una tabla legible" se actualiza para documentar la columna nueva, de dónde sale y
   cuándo queda vacía.
7. **Fuera de alcance, explícito:** no se recalculan ni se reescriben las filas ya existentes de una
   ejecución anterior a esta tarea (invariante ya establecido: "nunca borra ni reescribe una fila
   existente") — solo las filas nuevas que añada una exportación posterior llevan la columna
   calculada; no se toca `assets/reproductor/guion.js` ni el `.json` exportado por "Exportar
   tropiezos" (ningún campo nuevo que calcular ni que guardar ahí); no se fusiona `tomas_por_escena`
   dentro de `RegistroTropiezos` ni se persiste en ningún sitio nuevo — se consulta y se descarta en
   el momento de formatear cada fila, igual que ya hace `fecha` (parámetro opcional, no estado).

**Criterio de aceptación:** con `estado.tomas` trayendo, para la escena 3, una toma marcada `buena`
con `numero: 2`, y un registro de tropiezos de esa escena con dos tropiezos (uno con
`numero_toma: 2`, otro con `numero_toma: 1`), `registrar_tropiezos_en_feedback(carpeta_salida,
registro, tomas_por_escena=estado.tomas)` escribe la primera fila con «¿Toma buena?» = `sí` y la
segunda con `no`; llamando sin `tomas_por_escena` (o con `None`, el valor por defecto) ambas filas
quedan con la columna vacía, exactamente igual que hoy. Una fila ya existente de antes de esta tarea
(7 columnas, sin «¿Toma buena?») se sigue reconociendo exactamente igual al volver a exportar el
mismo registro, sin perder su estado `nuevo`/`resuelto`. Cuatro redes en verde.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
