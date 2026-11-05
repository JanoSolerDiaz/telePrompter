# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-11-05 (ciclo de Product Manager). R-46 (Oleada v34) llevaba
`COMPLETADA` en §1 de `SEGUIMIENTO.md` desde el 2026-11-05 (ciclo de Programador), reconfirmada en
verde por varias pasadas sucesivas sin que ningún ciclo de PM la archivara todavía. Este ciclo
archiva la Oleada v34 en `ROADMAP_HISTORICO.md` y abre R-47 (Oleada v35) en §1, sin implementarla: el
criterio de una sola R-XX pendiente de código a la vez (vigente desde R-19) queda respetado porque no
había ninguna otra R-XX pendiente antes de abrir esta.

`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (única fila, plantilla vacía): no hay
historia de rodaje real que incorporar — el bloqueo #7 de `SEGUIMIENTO.md` §3 (grabar un curso
completo) sigue abierto, ahora 63 días desde que T-32 lo dejó listo para grabar (2026-09-03).
`auditoriacontinua.md` revisado entero antes de elegir tarea, hasta su pasada del 2026-11-05: tres
hallazgos nuevos esa pasada — `#42` (alta: `SKILL.md` no invocaba `scripts/entrada.py`/T-06), ya
cerrado en código por **P-13** (urgente, la misma jornada), pendiente solo de que la próxima pasada
del auditor lo reverifique; `#43` (baja: hueco de regex en el validador de auto-contención para
protocolo relativo fuera de `cdn.`), deuda técnica pura sin ningún hito de producto, dejada como
candidata a una futura P-XX del Programador, mismo patrón que `#28`/`#33`/`#34`/`#35`/`#39`/`#40`/
`#41`/`#44` — no se abre ninguna R-XX para ella, porque no lo es; y `#44` (baja: rotación pendiente de
`HISTORIAL_SESIONES.md`), ya resuelto en código por **P-14** la misma jornada, pendiente también solo
de reverificación. Siguen `ABIERTO` únicamente `#24`/`#30`, de proceso/gobernanza pura, a la espera de
la respuesta del dueño a las preguntas #11/#12 de `SEGUIMIENTO.md` §6 (50/26 días sin respuesta).
Ninguno de los cinco hallazgos abiertos o recién cerrados es convertible en una R-XX de producto.

**Nota de producto de este ciclo (no es una R-XX, es una llamada de atención sobre el ritmo del
propio roadmap, repetida desde ciclos anteriores porque el hecho que la motiva no ha cambiado):** van
46 R-XX completadas desde que T-32 dejó la skill instalada y verificada en la máquina real del dueño
(2026-09-03), y ninguna de ellas viene todavía de un rodaje real — todas tienen `origen: auditoría
#N` o `observación de arquitectura/producto del PM`. Es trabajo de buena calidad (cuatro redes en
verde, 798 tests, invariantes reverificados en cada auditoría), pero el propio principio de producto
que guía este documento —"utilidad real para un formador que graba vídeos de curso"— solo se
confirma grabando, no leyendo código. El bloqueo #7 es una acción del dueño, no una tarea que el
equipo pueda ejecutar por su cuenta, así que este ciclo no lo repite como pregunta nueva; se deja
constancia aquí para que quede explícito que el criterio de salida de la Oleada v1 ("grabar un vídeo
de curso entero") sigue siendo, con diferencia, el hito de mayor valor pendiente del proyecto, por
delante de cualquier R-XX nueva. R-47 (más abajo) cambia ligeramente de ángulo respecto a R-39 a R-46
(todas ellas "qué falta antes/durante de grabar"): en vez de otro dato más a la vista mientras se
graba, cierra el otro extremo de la sesión — el momento en que ya no falta nada — señalando
explícitamente el siguiente paso real (salir del reproductor y generar las salidas de montaje), para
que esa primera sesión real, cuando ocurra, termine con una acción clara en vez de con una ausencia
(el botón de R-40 que simplemente deja de aparecer).

**Oleada v34 (R-46) archivada.** Spec completa y "Cómo se entregó" en `ROADMAP_HISTORICO.md`.

**Oleada v35 (R-47) abierta, sin implementar.** Ficha completa más abajo. Origen: observación de
producto del PM (2026-11-05): R-39 a R-46 han ido añadiendo al índice, una tras otra, formas de saber
"qué falta antes de grabar" (progreso, indicaciones, ritmo, tropiezos), pero ninguna responde la
pregunta inversa que de verdad cierra la sesión de rodaje: "¿ya terminé?". Hoy, cuando la última
escena queda con una toma buena marcada, el único cambio visible en el índice es que el botón
"Grabar siguiente pendiente" (R-40) deja de aparecer — un vacío, no una confirmación — y el paso
siguiente real (generar `comandos-montaje.md`/`concat-ffmpeg.txt`, T-33) vive fuera del reproductor,
en el selector de salidas (T-30) de la propia skill, sin ningún puente entre las dos pantallas.

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

### Oleada v35 — Cerrar la sesión de grabación: avisar cuando el guion ya no tiene ninguna escena pendiente

#### R-47 — Avisar en el índice, cuando todas las escenas ya tienen una toma marcada como buena, de que el guion está listo para generar las salidas de montaje

**Migración:** No (sin campo nuevo en el JSON embebido ni cambio de contrato; se calcula enteramente
en `assets/reproductor/guion.js` a partir de `pendientes`/`grabadas`, ya agregados por R-39 en el
mismo `forEach` que recorre `datos.escenas`) · **Depende de:** T-19 (índice de escenas,
`renderizarIndice`), R-02 (`tomasEscena`/`calcularEstadoEscena`), R-39 (`pendientes`/`grabadas` ya
agregados en el `forEach` de cabecera), R-40 (mismo hueco del índice donde hoy se renderiza "Grabar
siguiente pendiente", lugar natural del aviso simétrico) — todas `COMPLETADA` · **Origen:**
observación de producto del PM (2026-11-05). R-39 a R-46 han ido añadiendo al índice, una tras otra,
formas de saber "qué falta antes de grabar" (progreso, indicaciones, ritmo, tropiezos) — pero ninguna
responde la pregunta inversa, la que de verdad cierra la sesión de rodaje: "¿ya terminé?". Hoy, cuando
la última escena pasa a tener una toma `buena` marcada, el único cambio visible en el índice es que el
botón "Grabar siguiente pendiente" (R-40) deja de renderizarse — un vacío, no una confirmación. El
dueño graba en solitario, sin nadie que le diga "ya está"; el siguiente paso real (generar
`comandos-montaje.md`/`concat-ffmpeg.txt` y pasar a ffmpeg, T-33) vive fuera del reproductor, en el
selector de salidas (T-30) de la propia skill, y hoy no hay ningún puente entre las dos pantallas.

**Objetivo:** que el dueño sepa, sin ambigüedad y sin tener que fijarse en la ausencia de un botón, el
momento exacto en que el guion entero tiene ya una toma buena por escena, y que el índice se lo diga
señalando el siguiente paso real (volver a ejecutar la skill y elegir las salidas de montaje), para
cerrar la sesión de grabación con una acción clara en vez de con una duda.

**Requisitos:**
1. En `renderizarIndice` (`assets/reproductor/guion.js`), en el mismo punto donde hoy se decide si se
   renderiza el botón "Grabar siguiente pendiente" (R-40, `indiceSiguientePendiente ===
   estadosEscena.indexOf("pendiente")`), añadir la rama simétrica: cuando no queda ninguna escena
   `pendiente` **y tampoco ninguna `grabada`** (es decir, `pendientes === 0 && grabadas === 0`,
   reutilizando tal cual los dos contadores que R-39 ya agrega en el mismo `forEach`, sin una segunda
   noción de "terminado"), insertar un `<p id="aviso-guion-completo" class="aviso-guion-completo">`
   en el mismo lugar donde habría ido el botón. El requisito exige toma **buena** en cada escena
   (`revisada`), no solo alguna toma (`grabada`): es la condición real para que `concat-ffmpeg.txt`
   (R-19) no deje ninguna escena con el comentario `# ESCENA N: sin toma buena` en vez de un archivo
   real.
2. Texto fijo, sin interpolar ningún dato nuevo del JSON: "✓ Guion completo: todas las escenas tienen
   ya una toma buena. Vuelve a ejecutar la skill y elige «Comandos de montaje» en el selector de
   salidas (T-30) para continuar con ffmpeg." — sin enlace ni ruta de archivo (el reproductor es un
   `.html` offline, sin forma de invocar la skill ni de saber dónde vive la carpeta de salida en la
   máquina de quien lo abre).
3. El aviso no sustituye nunca al resumen de progreso (R-39, `.resumen-progreso-grabacion`, que sigue
   mostrando "0 pendientes · 0 grabadas · N revisadas · 0 min estimados por grabar" tal cual) ni a los
   resúmenes agregados de ritmo (R-45) o tropiezos en toma buena (R-44): es un elemento adicional,
   nunca un reemplazo de ninguno existente.
4. Con alguna escena todavía `pendiente` o `grabada` sin toma buena, el aviso no aparece nunca
   (comportamiento idéntico al de antes de esta tarea).
5. CSS nuevo en `assets/reproductor/estilo.css`: `.aviso-guion-completo` con el mismo tratamiento
   visual de énfasis positivo que ya tienen los botones de acción del índice (`.btn-continuar`), pero
   sin ser un botón — no dispara ninguna acción ni tiene manejador de evento, es puramente
   informativo.
6. Sin campo nuevo en el JSON embebido (verificado por diff de claves contra la salida de referencia
   anterior a R-47), sin cambio en `scripts/reproductor.py`, `scripts/pdf.py`, `scripts/pptx.py` ni
   `scripts/documento_revision.py`, sin tecla nueva, sin `localStorage` nuevo, sin migración.

**Criterio de aceptación:** sobre una fixture con al menos dos escenas — con una de ellas todavía
`pendiente` (sin ninguna toma), el índice muestra el botón "Grabar siguiente pendiente" (R-40) y nunca
el aviso `#aviso-guion-completo`; con esa misma escena ya `grabada` (toma registrada pero ninguna
`buena`) tampoco aparece el aviso, aunque el botón de R-40 ya no se renderice (ninguna `pendiente`);
solo cuando TODAS las escenas quedan `revisada` (toma `buena` marcada en cada una) aparece
`#aviso-guion-completo` con el texto exacto fijado en el requisito 2, en el mismo lugar donde antes
iba el botón de R-40. El resumen de progreso (R-39) sigue mostrando "0 pendientes · 0 grabadas · N
revisadas" sin ningún cambio de comportamiento. El JSON embebido por `scripts/reproductor.py` no gana
ningún campo nuevo. Verificado también visualmente con Playwright/Chromium real, mismo criterio que
R-39 a R-46.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
