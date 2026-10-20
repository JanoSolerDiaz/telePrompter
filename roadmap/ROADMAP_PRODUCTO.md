# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-10-20 (ciclo de Product Manager). R-34 (Oleada v22) llevaba
`COMPLETADA` en §1 de `SEGUIMIENTO.md` desde el ciclo de Programador de esta misma jornada (commit
`91b4c66`), reconfirmada en verde nueve veces seguidas sin que ningún ciclo de PM la archivara
todavía. Este ciclo archiva la Oleada v22 en `ROADMAP_HISTORICO.md` y abre R-35 (Oleada v23) en §1,
sin implementarla: el criterio de una sola R-XX pendiente de código a la vez (vigente desde R-19)
queda respetado porque no había ninguna otra R-XX pendiente antes de abrir esta.

`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (única fila, plantilla vacía): no hay
historia de rodaje real que incorporar — el bloqueo #7 de `SEGUIMIENTO.md` §3 (grabar un curso
completo) sigue abierto. `auditoriacontinua.md` revisado antes de elegir tarea: solo dos `ABIERTO`
(`#24`, baja; `#30`, media), ambos de proceso/gobernanza puro y pendientes solo de la respuesta del
dueño a las preguntas #11/#12 de `SEGUIMIENTO.md` §6 — ninguno de severidad alta, ninguno
convertible en R-XX nueva ni en deuda técnica de backlog.

**Oleada v22 (R-34) archivada.** Spec completa y "Cómo se entregó" en `ROADMAP_HISTORICO.md`.

**Oleada v23 (R-35) abierta, sin implementar.** Ficha completa más abajo. Origen: observación de
producto del propio PM (2026-10-20), verificada contra `assets/reproductor/guion.js` y
`references/contrato-tropiezos.md`: el propio contrato ya exige emparejar un tropiezo con su bloque
"por texto, no por índice" (`indice_bloque` puede desplazarse entre la grabación y la siguiente
revisión si una partición de respiración se acepta antes de él en la misma escena), pero ese criterio
solo se aplica del lado Python (`scripts/feedback.py`); `cargarTropiezosGuardados` (`guion.js`), que
relee `localStorage` al reabrir un reproductor regenerado, sigue confiando en `indice_bloque` tal
cual.

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

### Oleada v23 — Robustez del indicador de tropiezo frente a un troceo que cambia entre grabación y revisión

#### R-35 — Relocalizar por texto, no por índice, un tropiezo guardado en `localStorage` cuando el troceo de la escena cambió desde que se marcó, para que el indicador "⚠ Tropiezo" nunca señale el bloque equivocado

**Migración:** No (ningún campo nuevo en `estado.json` ni en el `.json` exportado por "Exportar
tropiezos": `references/contrato-tropiezos.md` no sube de versión, el cambio es puramente interno a
cómo `guion.js` interpreta lo que ya guarda en `localStorage`) · **Depende de:** R-03 (tropiezos
marcados), T-15/T-17 (particiones de respiración que pueden desplazar `indice_bloque`) — todas
`COMPLETADA` · **Origen:** observación de producto del PM (2026-10-20), no de auditoría ni de
feedback de rodaje (`roadmap/FEEDBACK.md` sigue vacío) — grieta de arquitectura verificada sobre
código y documentación ya construidos: `references/contrato-tropiezos.md` (§"Por qué se casa por
texto, no por índice") documenta explícitamente que `indice_bloque` puede desplazarse entre la
grabación y la siguiente revisión si una partición de respiración se acepta antes de él en la misma
escena, y que por eso `scripts/feedback.py` empareja cada tropiezo del `.json` exportado con su
bloque por **texto exacto**, nunca por índice. Ese mismo criterio no se aplica, sin embargo, cuando
`guion.js::cargarTropiezosGuardados` relee `localStorage` al abrir un reproductor regenerado: la
clave de almacenamiento es estable por guion (`teleprompter:<guion>:tropiezos_escena_N`, nunca
invalidada por un cambio de troceo), así que un tropiezo marcado antes de una revalidación que
desplazó los bloques de esa escena sigue leyéndose con su `indice_bloque` antiguo —
`actualizarIndicadorTropiezo`/`alternarTropiezoBloqueActual` lo comparan tal cual contra
`bloqueActual`, nunca contra el `texto` guardado.

**Objetivo:** un formador que graba en varias sesiones (la persistencia de tomas y tropiezos en
`localStorage` existe precisamente para eso, mismo mecanismo que T-26) puede marcar un tropiezo con
`T`, pausar, revisar y aceptar una reescritura con partición en un bloque anterior de esa misma
escena, regenerar el reproductor y seguir grabando en el mismo navegador: hoy el indicador "⚠
Tropiezo" de la cabecera puede entonces encenderse sobre un bloque que el dueño nunca marcó, o no
encenderse sobre el que sí marcó — justo durante una grabación, donde la fiabilidad de lo que se ve
en pantalla es la base de toda la skill (principio de producto 5, legibilidad por encima de todo). El
`.json` exportado y `FEEDBACK.md` nunca llegan a mentir (`texto` siempre fue correcto y
`scripts/feedback.py` ya empareja por texto), pero el reproductor sí puede hacerlo mientras tanto,
contradiciendo el propio criterio que su contrato documenta.

**Requisitos:**
1. `cargarTropiezosGuardados(escena)`: para cada tropiezo ya filtrado como estructuralmente válido
   (como hoy), comprobar si `escena.bloques[tropiezo.indice_bloque]` existe y su `.texto` coincide
   exactamente con el `texto` guardado. Si coincide, se conserva tal cual — camino feliz idéntico al
   actual, sin cambio de comportamiento cuando el troceo de la escena no cambió desde que se marcó.
2. Si no coincide (índice fuera de rango, o el bloque en ese índice tiene otro texto), buscar el
   mismo `texto` exacto entre TODOS los bloques de la escena — mismo criterio de "texto exacto" que
   ya aplica `scripts/feedback.py`, nunca una segunda regla de emparejamiento inventada aquí. Si hay
   exactamente una coincidencia, relocalizar el tropiezo a ese nuevo `indice_bloque`. Si hay cero o
   más de una coincidencia (texto reescrito, o duplicado en la escena), descartar la entrada — mismo
   comportamiento que el contrato ya documenta para el lado Python ("si se reescribió, el tropiezo
   marcado sobre el texto viejo ya no tiene sentido destacarlo").
3. El resultado ya corregido (reubicado o descartado) se vuelve a guardar en `localStorage` de
   inmediato con `guardarTropiezosEscena`, para que la corrección quede fijada en el primer reinicio
   y no se repita el recálculo, ni queden índices obsoletos acumulándose, en cada apertura posterior.
4. `actualizarIndicadorTropiezo`/`alternarTropiezoBloqueActual` no cambian: consumen
   `tropiezosEscena[escena]` ya corregido en el momento de la carga, así que su comparación por
   `indice_bloque` vuelve a ser segura sin tocar su propio código.
5. **Fuera de alcance, explícito:** no se toca `tomasEscena` (`cargarTomasGuardadas`) — verificado
   que ningún campo de una toma persistida referencia `indice_bloque`, así que no sufre este
   problema; no se sube `version` de `references/contrato-tropiezos.md` (el `.json` exportado no
   cambia de forma, solo cómo se interpreta lo ya guardado al cargar); no se toca
   `scripts/feedback.py` ni `documento_revision.py` (ya casan por texto, intactos); no se persiste
   ningún historial de relocalizaciones — la corrección es silenciosa y determinista, no un aviso
   nuevo al dueño.

**Criterio de aceptación:** con un `localStorage` simulado que trae un tropiezo guardado en
`indice_bloque=0` con un texto dado, y una escena regenerada donde ese MISMO texto vive ahora en
`indice_bloque=1` (una partición aceptada se insertó antes de él), al cargar el reproductor el
indicador "⚠ Tropiezo" se enciende sobre el bloque 1, nunca sobre el bloque 0; un tropiezo cuyo texto
ya no existe en ningún bloque de la escena (reescrito) se descarta sin error y sin dejar ningún
indicador fantasma; un tropiezo cuyo índice y texto siguen coincidiendo tal cual no cambia de
comportamiento (camino feliz intacto, mismo resultado que antes de R-35); el `.json` exportado con
"Exportar tropiezos" tras la relocalización sigue teniendo exactamente la misma forma que documenta
`references/contrato-tropiezos.md` versión 2, sin cambios. Cuatro redes en verde.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
