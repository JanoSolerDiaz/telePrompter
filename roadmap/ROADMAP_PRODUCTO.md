# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-11-03 (ciclo de Product Manager). R-44 (Oleada v32) llevaba
`COMPLETADA` en §1 de `SEGUIMIENTO.md` desde el 2026-11-03 (ciclo de Programador), reconfirmada en
verde en varias pasadas sucesivas del Programador sin que ningún ciclo de PM la archivara todavía.
Este ciclo archiva la Oleada v32 en `ROADMAP_HISTORICO.md` y abre R-45 (Oleada v33) en §1, sin
implementarla: el criterio de una sola R-XX pendiente de código a la vez (vigente desde R-19) queda
respetado porque no había ninguna otra R-XX pendiente antes de abrir esta.

`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (única fila, plantilla vacía): no hay
historia de rodaje real que incorporar — el bloqueo #7 de `SEGUIMIENTO.md` §3 (grabar un curso
completo) sigue abierto, ahora 61 días desde que T-32 lo dejó listo para grabar (2026-09-03).
`auditoriacontinua.md` revisado entero antes de elegir tarea (no solo la narrativa más reciente):
`#24` (baja) y `#30` (escalada de media a alta en esta misma pasada del auditor, por el volumen y
persistencia del coste de cómputo que describe, no por ningún riesgo nuevo de producto) siguen
`ABIERTO` de proceso/gobernanza puro, pendientes solo de la respuesta del dueño a las preguntas
#11/#12 de `SEGUIMIENTO.md` §6 (48 y 24 días sin respuesta); `#36` (baja, apertura en inglés de un
commit ya publicado) sigue puramente observacional, sin remedio retroactivo razonable. Tres hallazgos
nuevos de esta pasada del auditor, los tres de proceso/documentación pura, sin ninguno convertible en
R-XX de producto: `#38` (baja, el propio registro de `auditoriacontinua.md` debería condensar sus
filas más repetidas) es terreno exclusivo del auditor, que ya lo deja como remedio propuesto en su
propia fila, no de este roadmap; `#39` (media, `SEGUIMIENTO.md` había vuelto a acumular narrativa de
sesión en su cabecera) ya fue corregido en código por el Programador (P-10, commit `822295d`) antes
de este ciclo, pendiente solo de que el auditor lo reverifique; `#40` (baja, `DECISIONES_TECNICAS.md`
supera el umbral de rotación por trimestre que su propia cabecera declara) es una tarea de archivado
puro, sin ningún hito de producto ni urgencia — candidata a una futura P-XX del Programador cuando su
cola esté vacía, igual que P-06/P-07/P-08 resolvieron hallazgos de documentación equivalentes; no se
abre como pregunta nueva en §6 porque no depende de ninguna decisión del dueño, solo de ejecutarla.
Ninguno de los siete hallazgos abiertos es de severidad alta en las categorías que exigirían una P-XX
urgente (pérdida de texto del guion, corrupción de estado, rotura del reproductor o de su
auto-contención, seguridad); `#41` (baja, hueco de `srcset=` en el validador de auto-contención) ya
fue corregido en código por el Programador (P-11) antes de este ciclo, también pendiente solo de
reverificación del auditor.

**Nota de producto de este ciclo (no es una R-XX, es una llamada de atención sobre el ritmo del
propio roadmap, repetida desde ciclos anteriores porque el hecho que la motiva no ha cambiado):** van
44 R-XX completadas desde que T-32 dejó la skill instalada y verificada en la máquina real del dueño
(2026-09-03), y ninguna de ellas viene todavía de un rodaje real — todas tienen `origen: auditoría
#N` o `observación de arquitectura/producto del PM`. Es trabajo de buena calidad (cuatro redes en
verde, 777 tests, invariantes reverificados en cada auditoría), pero el propio principio de producto
que guía este documento —"utilidad real para un formador que graba vídeos de curso"— solo se
confirma grabando, no leyendo código. El bloqueo #7 es una acción del dueño, no una tarea que el
equipo pueda ejecutar por su cuenta, así que este ciclo no lo repite como pregunta nueva; se deja
constancia aquí para que quede explícito que el criterio de salida de la Oleada v1 ("grabar un vídeo
de curso entero") sigue siendo, con diferencia, el hito de mayor valor pendiente del proyecto, por
delante de cualquier R-XX nueva. R-45 (más abajo) sigue el mismo criterio que R-39 a R-44: una mejora
pequeña y de bajo riesgo del propio reproductor, directamente útil para esa primera sesión real
cuando ocurra — en vez de agregar otro resumen sobre datos de rodaje (tomas, tropiezos), esta vez trae
al reproductor un aviso que T-12 ya calcula desde el primer día del proyecto (desviación del ritmo
estimado frente a la duración objetivo marcada en el guion) y que hoy solo es visible releyendo
`guion-escenas.md` en el editor, nunca en la propia pantalla que el dueño tiene delante al grabar.

**Oleada v32 (R-44) archivada.** Spec completa y "Cómo se entregó" en `ROADMAP_HISTORICO.md`.

**Oleada v33 (R-45) abierta, sin implementar.** Ficha completa más abajo. Origen: observación de
arquitectura del PM (2026-11-03): `scripts/tiempos.py::TiempoEscena.aviso` (T-12) ya compara, escena
a escena, la duración estimada por ppm contra la duración objetivo marcada en el guion, y ya
formatea un texto accionable en palabras a ajustar cuando la desviación supera el umbral configurado
— usado hoy en `guion-escenas.md`, `tarjetas.json`, el `.pdf` y la revalidación, pero nunca en el
reproductor en vivo. R-45 aplica el mismo principio que R-39/R-44 (reutilizar un dato ya calculado,
sin segunda implementación) para mostrarlo por fila y agregado en la cabecera del índice.

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

### Oleada v33 — Avisar cuando el ritmo estimado de una escena se desvía de la duración objetivo marcada en el guion

#### R-45 — Mostrar en el índice de escenas, por fila y agregado en la cabecera, el aviso de desviación de ritmo que T-12 ya calcula por escena

**Migración:** No (campo aditivo en el JSON embebido por `scripts/reproductor.py::_construir_datos`,
que no lleva versión de contrato propia; ningún cambio en `scripts/tiempos.py`, que ya calcula y
formatea el aviso completo desde T-12) · **Depende de:** T-12 (`tiempos.calcular_tiempos`/
`calcular_tiempos_desde_marcados`, `TiempoEscena.aviso` vía `_aviso_desviacion`), T-19 (índice de
escenas, `renderizarIndice`), R-39 (`.resumen-progreso-grabacion`, el bloque agregado de cabecera,
mismo patrón a seguir) — todas `COMPLETADA` · **Origen:** observación de arquitectura del PM
(2026-11-03). `TiempoEscena.aviso` (T-12) ya compara, escena a escena, la duración estimada por ppm
contra la duración objetivo que el propio guion fija en la cabecera de cada escena, y ya formatea un
texto accionable ("sobran/faltan unas P palabras para encajar en el objetivo") cuando la desviación
supera el umbral configurado (`Configuracion.umbral_desviacion_tiempos`) — hoy se usa en
`guion-escenas.md` (`documento_revision.py`), `tarjetas.json` (`pptx.py`), el `.pdf` (`pdf.py`) y en
la revalidación (`revalidacion.py`), pero nunca llega al JSON embebido del reproductor: la única
vista que el dueño tiene delante mientras graba es la única que no lo muestra. Mismo principio que
R-39/R-42/R-43/R-44: reutilizar un dato ya calculado y ya probado, sin segunda implementación del
criterio.

**Objetivo:** que el dueño vea, en el índice de escenas y sin volver a abrir `guion-escenas.md` en el
editor, qué escenas concretas se desvían de la duración objetivo marcada en el guion y por cuántas
palabras, para decidir antes de grabar si recorta, alarga o deja el texto tal cual — y, de un vistazo
en la cabecera, cuántas escenas en total necesitan esa revisión antes de cerrar la sesión.

**Requisitos:**
1. `scripts/reproductor.py::_construir_datos` añade, de forma aditiva, `"aviso": tiempo_escena.aviso`
   a cada entrada de `escenas_datos` (junto a `duracion_estimada_segundos`/`duracion_objetivo_segundos`,
   ya presentes desde T-12/R-16) — reutiliza tal cual el texto ya formateado por
   `tiempos._aviso_desviacion`, sin tocar `scripts/tiempos.py` ni reformular el mensaje. `None` cuando
   no hay desviación (sin objetivo marcado, o desviación dentro del umbral), igual que hoy en
   `TiempoEscena.aviso`.
2. En `renderizarIndice` (`assets/reproductor/guion.js`), añadir un `<span class="escena-aviso-ritmo">`
   en la fila de cada escena, inmediatamente después de `.escena-duracion` y antes de
   `.escena-indicaciones` (R-42), con el texto exacto de `escena.aviso` cuando no es `null` — sin
   reformatear ni truncar, mismo criterio de reutilización exacta que el resto de la ficha. Sin
   `<span>` cuando `escena.aviso` es `null`.
3. En el mismo `forEach` sobre `datos.escenas` donde R-39/R-44 ya calculan sus contadores (pendientes/
   grabadas/revisadas/segundosPendientes/escenasConTropiezoEnBuena), sumar un contador nuevo,
   `escenasConAvisoRitmo`, incrementado por cada escena cuyo `aviso` no sea `null` — mismo bucle ya
   existente, sin segundo recorrido de `datos.escenas`.
4. Si `escenasConAvisoRitmo` es mayor que 0, añadir un `<p class="resumen-aviso-ritmo">` nuevo
   inmediatamente después de `.resumen-progreso-grabacion` (R-39) y antes de
   `.resumen-tropiezos-en-buena` (R-44) cuando este exista — el aviso de ritmo es una revisión previa
   a grabar, el de tropiezos una revisión posterior a una toma, así que el orden de lectura sigue el
   orden natural de la sesión de rodaje — con el texto "⚠ 1 escena se desvía del ritmo objetivo
   marcado" (singular) o "⚠ N escenas se desvían del ritmo objetivo marcado" (plural, N = escenas),
   mismo criterio singular/plural que el resto de resúmenes. Con el contador en 0, no se añade ningún
   elemento.
5. CSS nuevo en `assets/reproductor/estilo.css` para `.escena-aviso-ritmo` y `.resumen-aviso-ritmo`,
   reutilizando el mismo lenguaje visual de aviso que `.escena-tropiezos-en-buena`/
   `.resumen-tropiezos-en-buena` (R-43/R-44: color de acento, negrita) en vez del tono neutro de
   `.resumen-guion`/`.resumen-progreso-grabacion` — es un aviso que puede exigir una decisión del
   dueño antes de grabar, no solo informar (principio de producto 5: legibilidad por encima de todo).
6. Sin elemento interactivo nuevo (`<span>`/`<p>`, nunca un control); sin `localStorage` nuevo; sin
   cambio en `scripts/tiempos.py`, `scripts/feedback.py`, `scripts/comandos_montaje.py` ni en ningún
   otro consumidor ya existente del aviso (`documento_revision.py`/`pptx.py`/`pdf.py`/
   `revalidacion.py`) — mejora enteramente de lectura y presentación en el reproductor sobre un dato
   que T-12 ya calcula y ya usan otras cuatro salidas.
7. El resumen y el aviso por fila se recalculan solos (mismo patrón que R-39/R-42/R-43/R-44, sin
   heurística de refresco nueva): cualquier llamada ya existente a `renderizarIndice()` reconstruye
   ambos desde cero sin cableado adicional — el aviso no cambia durante la sesión de rodaje en sí
   (depende solo del guion y la configuración, no de tomas ni tropiezos), así que no hace falta
   ningún disparador nuevo más allá de la propia carga del reproductor.

**Criterio de aceptación:** sobre una fixture con al menos tres escenas de prueba — (a) sin duración
objetivo marcada en la cabecera de la escena, (b) con duración objetivo marcada y una estimación
dentro del umbral configurado, y (c) con duración objetivo marcada y una estimación que lo supera —
el índice no muestra ningún `<span class="escena-aviso-ritmo">` en (a) ni en (b), y en (c) muestra el
texto exacto que ya produce `tiempos._aviso_desviacion` para esa escena (verificado por comparación
literal, no por un nuevo cálculo en el test). Con una sola escena en el caso (c), la cabecera muestra
"⚠ 1 escena se desvía del ritmo objetivo marcado"; con dos o más, el plural con el recuento correcto
de escenas. El JSON embebido por `scripts/reproductor.py` gana únicamente el campo aditivo `aviso`
por escena (verificado por diff de claves contra la salida de referencia anterior a R-45); ningún
otro consumidor del aviso (`guion-escenas.md`, `tarjetas.json`, el `.pdf`, la revalidación) cambia de
comportamiento. Verificado también visualmente con Playwright/Chromium real, mismo criterio que
R-39 a R-44.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
