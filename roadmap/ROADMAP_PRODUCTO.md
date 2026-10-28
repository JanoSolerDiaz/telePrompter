# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-10-28 (ciclo de Product Manager). R-40 (Oleada v28) llevaba
`COMPLETADA` en §1 de `SEGUIMIENTO.md` desde el mismo día (ciclo de Programador), reconfirmada en
verde en pasadas sucesivas sin que ningún ciclo de PM la archivara todavía. Este ciclo archiva la
Oleada v28 en `ROADMAP_HISTORICO.md` y abre R-41 (Oleada v29) en §1, sin implementarla: el criterio
de una sola R-XX pendiente de código a la vez (vigente desde R-19) queda respetado porque no había
ninguna otra R-XX pendiente antes de abrir esta.

`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (única fila, plantilla vacía): no hay
historia de rodaje real que incorporar — el bloqueo #7 de `SEGUIMIENTO.md` §3 (grabar un curso
completo) sigue abierto, ahora más de 50 días desde que T-32 lo dejó listo para grabar (2026-09-03).
`auditoriacontinua.md` revisado antes de elegir tarea: solo dos `ABIERTO` (`#24`, baja; `#30`,
media), ambos de proceso/gobernanza puro y pendientes solo de la respuesta del dueño a las preguntas
#11/#12 de `SEGUIMIENTO.md` §6 (42 y 18 días sin respuesta) — ninguno de severidad alta, ninguno
convertible en R-XX nueva ni en deuda técnica de backlog.

**Nota de producto de este ciclo (no es una R-XX, es una llamada de atención sobre el ritmo del
propio roadmap):** van 40 R-XX completadas desde que T-32 dejó la skill instalada y verificada en la
máquina real del dueño (2026-09-03), y ninguna de ellas viene todavía de un rodaje real — todas
tienen `origen: auditoría #N` o `observación de arquitectura/producto del PM`. Es trabajo de buena
calidad (cuatro redes en verde, 752 tests, invariantes reverificados en cada auditoría), pero el
propio principio de producto que guía este documento —"utilidad real para un formador que graba
vídeos de curso"— solo se confirma grabando, no leyendo código. El bloqueo #7 es una acción del
dueño, no una tarea que el equipo pueda ejecutar por su cuenta, así que este ciclo no lo repite como
pregunta nueva; se deja constancia aquí para que quede explícito que el criterio de salida de la
Oleada v1 ("grabar un vídeo de curso entero") sigue siendo, con diferencia, el hito de mayor valor
pendiente del proyecto, por delante de cualquier R-XX nueva. R-41 (más abajo) sigue el mismo criterio
que R-39/R-40: una mejora pequeña y de bajo riesgo del propio reproductor, directamente útil para esa
primera sesión real cuando ocurra, no otra grieta de arquitectura interna entre salidas de montaje.

**Oleada v28 (R-40) archivada.** Spec completa y "Cómo se entregó" en `ROADMAP_HISTORICO.md`.

**Oleada v29 (R-41) abierta, sin implementar.** Ficha completa más abajo. Origen: observación de
producto del propio PM (2026-10-28), continuación directa de R-40: el botón "Grabar siguiente
pendiente" ya lleva al dueño a la siguiente escena que falta por grabar, pero solo si lo alcanza con
`Tab` desde el principio del índice o con el ratón; en el momento real en que más se usa —acabar de
cerrar una toma buena y querer seguir encadenando sin pausa— el foco de teclado sigue cayendo por
defecto en la fila de la escena que se acaba de abandonar.

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

### Oleada v29 — Foco automático en "Grabar siguiente pendiente" al cerrar una toma buena

#### R-41 — Al volver al índice tras marcar una toma como buena, el foco de teclado pasa directo al botón "Grabar siguiente pendiente" (si lo hay)

**Migración:** No (decisión de foco puramente en memoria; ningún campo nuevo en `estado.json` ni en
el JSON embebido del reproductor, ningún `localStorage` nuevo) · **Depende de:** T-19
(`volverAlIndice`, `reproducirEscena`), T-23 (marcar la toma como buena con `G`, variable
`tomaBuenaEnCurso`), R-02 (estado `grabada`/`revisada` derivado de las tomas reales), R-40 (botón
`#btn-siguiente-pendiente` que `renderizarIndice` ya construye) — todas `COMPLETADA` · **Origen:**
observación de producto del PM (2026-10-28), continuación directa de R-40: verificado contra el
código real (`assets/reproductor/guion.js::volverAlIndice`) que, tras `finalizarTomaActual()` (que
ya deja registrada la toma recién cerrada y ya ha vuelto a dibujar el índice con el botón de R-40 al
día), el foco se asigna siempre a `botonesEscena[indice]` — la fila de la escena que se acaba de
abandonar —, nunca al botón que ya apunta a la siguiente pendiente, obligando a un `Tab` manual justo
en el momento en que más prisa corre seguir grabando.

**Objetivo:** que, en el instante exacto en que más se usa —acabar de grabar una toma buena (`G`) y
pulsar `Esc` para volver al índice con intención de seguir encadenando escenas sin pausa—, un único
`Intro`/`Espacio` (o la pulsación del clicker Bluetooth, T-24) entre directamente en la siguiente
escena `pendiente`, sin `Tab` de por medio y sin tener que soltar el teclado para hacer clic con el
ratón.

**Requisitos:**
1. En `volverAlIndice(indice)` (`assets/reproductor/guion.js`), justo después de la llamada ya
   existente a `finalizarTomaActual()` (que deja `tomaBuenaEnCurso` con el valor de la toma que se
   acaba de cerrar — no se reinicia hasta `iniciarMotor`/`reiniciarEscenaActual`, en una escena
   posterior — y que ya ha vuelto a renderizar el índice con el botón de R-40 actualizado), decidir
   el destino del foco en vez de asignarlo siempre a `botonesEscena[indice]`.
2. Si `tomaBuenaEnCurso` es `true` (la toma que se acaba de cerrar quedó marcada como la buena) **y**
   existe en el DOM `#btn-siguiente-pendiente` (R-40; su sola presencia ya significa que queda al
   menos una escena `pendiente`), el foco va a ese botón. En cualquier otro caso —no se marcó
   ninguna toma como buena antes de salir (p. ej. salir a mitad de una toma para descansar, o
   reiniciarla con `R` y salir sin volver a marcar) o no queda ninguna escena `pendiente`— el foco se
   mantiene exactamente como hoy: la fila de la propia escena (`botonesEscena[indice]`), para
   revisar o retomar donde se dejó.
3. Sin heurística nueva de qué escena es "la siguiente": el botón de R-40 ya decide ese destino por
   su cuenta (`estadosEscena.indexOf("pendiente")`); este requisito solo mueve el foco de teclado
   hacia un control que ya existe, nunca cambia a qué escena apunta ni añade una segunda forma de
   calcularlo.
4. `.focus()` sobre un `<button>` nativo ya renderizado, mismo mecanismo que usan hoy T-19/T-26/R-40
   para enfocar sus propios botones — sin `tabindex` nuevo, sin región `aria-live`, sin cambio de
   `requestFullscreen` (ya se ha abandonado la pantalla completa en `volverAlIndice` antes de decidir
   el foco, igual que hoy).
5. Sin `localStorage` nuevo, sin cambio en `scripts/reproductor.py` ni en el contrato de datos
   embebido: la decisión es enteramente de `guion.js` sobre estado que ya existe en memoria
   (`tomaBuenaEnCurso`) y el propio DOM que R-40 ya mantiene.

**Criterio de aceptación:** sobre una fixture con al menos dos escenas `pendiente` y una tercera ya
`revisada`, entrar en la primera `pendiente`, marcar la toma como buena (`G`) y volver al índice
(`Esc`) deja el foco directamente en `#btn-siguiente-pendiente`, ya apuntando a la segunda escena
`pendiente`; un `Intro` inmediato, sin ningún `Tab`, entra en esa segunda escena. Repitiendo sobre la
última escena `pendiente` de la fixture (de modo que, al marcarla buena, no quede ninguna pendiente),
el foco al volver al índice cae en la fila de esa misma escena (el botón ya no existe), sin excepción
de script ni foco perdido en `<body>`. Entrando en una escena y saliendo con `Esc` sin haber marcado
ninguna toma como buena en esa visita (por ejemplo, reiniciar con `R` y salir sin volver a marcar)
mantiene el comportamiento actual: el foco vuelve a la fila de esa misma escena, nunca al botón de
R-40, aunque queden escenas `pendiente`. Verificado también visualmente con Playwright/Chromium
real, mismo criterio que R-39/R-40.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
