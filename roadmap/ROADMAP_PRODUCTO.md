# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-10-23 (ciclo de Product Manager). R-37 (Oleada v25) llevaba
`COMPLETADA` en §1 de `SEGUIMIENTO.md` desde el ciclo de Programador de esta misma jornada (06:15),
reconfirmada en verde nueve veces seguidas sin que ningún ciclo de PM la archivara todavía. Este
ciclo archiva la Oleada v25 en `ROADMAP_HISTORICO.md` y abre R-38 (Oleada v26) en §1, sin
implementarla: el criterio de una sola R-XX pendiente de código a la vez (vigente desde R-19) queda
respetado porque no había ninguna otra R-XX pendiente antes de abrir esta.

`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (única fila, plantilla vacía): no hay
historia de rodaje real que incorporar — el bloqueo #7 de `SEGUIMIENTO.md` §3 (grabar un curso
completo) sigue abierto. `auditoriacontinua.md` revisado antes de elegir tarea: solo dos `ABIERTO`
(`#24`, baja; `#30`, media), ambos de proceso/gobernanza puro y pendientes solo de la respuesta del
dueño a las preguntas #11/#12 de `SEGUIMIENTO.md` §6 — ninguno de severidad alta, ninguno
convertible en R-XX nueva ni en deuda técnica de backlog.

**Oleada v25 (R-37) archivada.** Spec completa y "Cómo se entregó" en `ROADMAP_HISTORICO.md`.

**Oleada v26 (R-38) abierta, sin implementar.** Ficha completa más abajo. Origen: observación de
producto del propio PM (2026-10-23), que cierra el hueco que deja la propia R-37: ahora
`FEEDBACK.md` dice de un vistazo qué tropiezos ocurrieron dentro de la toma que de verdad se usó
(columna «¿Toma buena?»), pero esa respuesta vive en un documento distinto del que el dueño abre en
el momento real de montar (`comandos-montaje.md`, R-30) — así que, antes de concatenar, tendría que
volver a `FEEDBACK.md`, filtrar las filas con «¿Toma buena?» = «sí» y traducir su «Instante» a mano
a un punto de revisión. Mismo tipo de cruce mecánico entre dos documentos que la skill ya genera por
separado, y mismo criterio que ya aplicaron R-19/R-20/R-22/R-36/R-37 al mismo tipo de hueco.

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

### Oleada v26 — Avisar en los comandos de montaje de los tropiezos ocurridos dentro de la toma buena

#### R-38 — Añadir a `comandos-montaje.md` los instantes exactos que conviene revisar antes de concatenar, cuando un tropiezo marcado cayó dentro de la toma que se usó como buena

**Migración:** No (ningún campo nuevo en `estado.json` ni en el `.json` exportado por "Exportar
tropiezos" — `references/contrato-tropiezos.md` sigue en la versión 3; `comandos-montaje.md` sigue
siendo un documento calculado, nunca releído del disco, mismo patrón que R-30/R-31) · **Depende
de:** R-30 (`comandos-montaje.md`, cadena real de comandos `ffmpeg`), R-31 (avisos de archivos
faltantes en el mismo documento), R-34 (`instante_toma_segundos` de cada tropiezo), R-36
(`numero_toma` de cada tropiezo), R-37 (cruce «¿Toma buena?» en `FEEDBACK.md`) — todas `COMPLETADA`
· **Origen:** observación de producto del PM (2026-10-23), no de auditoría ni de feedback de rodaje
(`roadmap/FEEDBACK.md` sigue vacío) — cierra el hueco que deja la propia R-37: ahora `FEEDBACK.md`
dice de un vistazo qué tropiezos ocurrieron dentro de la toma buena, pero esa respuesta vive en un
documento distinto del que el dueño abre para montar (`comandos-montaje.md`, R-30), así que antes de
concatenar tendría que volver a `FEEDBACK.md`, filtrar las filas con «¿Toma buena?» = «sí» y
traducir su «Instante» a mano a un punto de revisión — el mismo tipo de cruce mecánico y repetido,
entre dos archivos que la skill ya genera por separado, que motivó R-19/R-20/R-22/R-36/R-37.

**Objetivo:** que `comandos-montaje.md` —el documento que el dueño abre en el momento real de
montar, justo después de grabar— diga, sin tener que consultar `FEEDBACK.md` aparte, en qué segundo
exacto de cada archivo de vídeo real conviene revisar antes de ejecutar el primer comando (la
concatenación), porque ahí hubo un tropiezo marcado durante la toma que efectivamente se usó. Es una
nota informativa, igual que el aviso de archivo referenciado ausente de R-31: nunca un comando de
recorte, nunca una ejecución de `ffmpeg` (sigue fuera de alcance, fijado por R-30 requisito 5 y
reafirmado por R-31).

**Requisitos:**
1. `scripts/comandos_montaje.py::calcular_comandos_montaje` gana un parámetro opcional
   `registro_tropiezos: RegistroTropiezos | None = None` (el mismo tipo que exporta "Exportar
   tropiezos" y que ya carga `scripts/feedback.cargar_registro_tropiezos`). Con el valor por defecto
   (`None`), el comportamiento y el documento generado son idénticos a los de hoy — ninguna llamada
   existente (ni ningún test ya escrito) se rompe por no pasarlo.
2. Por cada escena de `registro_tropiezos.escenas` con al menos un tropiezo cuyo `numero_toma`
   (R-36) coincide con el número de la toma marcada `buena` de esa escena en `tomas_por_escena` —
   reutilizando tal cual la misma comparación que ya hace `feedback._es_toma_buena` contra
   `tomas.toma_buena` (R-02/R-11), sin una segunda implementación de la regla de exclusividad "como
   mucho una toma buena por escena" — reunir los `instante_toma_segundos` (R-34) de esos tropiezos,
   formateados `mm:ss` con el mismo criterio que `feedback._formatear_instante` (minutos a dos
   dígitos).
3. Nueva sección al final del documento generado por `formatear_comandos_montaje` —después de los
   pasos numerados, después del aviso de «sin sección Capítulos» si aplica, y después de la nota de
   «escenas todavía sin toma buena» si aplica (la nota de archivos referenciados faltantes de R-31
   sigue yendo al principio, sin cambios; esta sección nueva es la última pieza del documento, no
   antes de ninguna de las existentes)—: «**Puntos a revisar antes de concatenar**», con una línea
   por escena afectada: número de escena, título y la lista de instantes `mm:ss` (ordenados),
   citando que esos segundos corresponden a la toma que `concat-ffmpeg.txt` va a usar de verdad para
   esa escena.
4. Un tropiezo con `numero_toma` o `instante_toma_segundos` en `None` (archivo exportado de una
   versión del contrato anterior a R-34/R-36) se ignora para esta sección sin avisar de nada
   adicional — no hay instante que listar ni toma que comparar; sigue siendo el caso ya cubierto por
   el valor vacío de «¿Toma buena?» en `FEEDBACK.md` (R-37).
5. Sin `registro_tropiezos` (valor por defecto `None`), la sección nueva no aparece y el documento es
   byte a byte el de antes de esta tarea. Con `registro_tropiezos` pero sin ninguna escena con un
   tropiezo cruzado como de la toma buena, tampoco aparece la sección — nunca un encabezado vacío.
6. `scripts/salidas.py::generar_salidas_seleccionadas` gana el mismo parámetro opcional
   `registro_tropiezos: RegistroTropiezos | None = None`, propagado a
   `_generar_comandos_montaje`/`generar_comandos_montaje` igual que ya se propaga
   `tomas_por_escena` (R-18/R-30); sin valor, sin cambio de comportamiento en ninguna salida.
7. `references/contrato-montaje.md` documenta la sección nueva de `comandos-montaje.md` y de dónde
   sale (cruce con el registro de tropiezos exportado, cuando se aporta); `references/contrato-tropiezos.md`
   NO sube de versión (nada cambia en el `.json` exportado ni en `guion.js`: el cruce vuelve a vivir
   enteramente en Python, al formatear `comandos-montaje.md`, mismo patrón que R-37 fijó para
   `FEEDBACK.md`).
8. **Fuera de alcance, explícito:** no se genera ningún comando `ffmpeg` de recorte, silencio o
   transición real, ni se ejecuta `ffmpeg` desde la skill (ya fuera de alcance desde R-30/R-31); no
   se persiste `registro_tropiezos` en `estado.json` ni en ningún sitio nuevo — se consulta y se
   descarta al formatear el documento, igual que `tomas_por_escena`; no se cambia ninguna regla de
   `tomas.toma_buena` ni de `feedback.py`; no se extiende la carga de `registro_tropiezos` a ninguna
   otra salida (`concat-ffmpeg.txt`, `.srt`, capítulos siguen exactamente igual); no se avisa de
   tropiezos de tomas que NO son la buena (esos ya los puede ver el dueño en `FEEDBACK.md` con
   «¿Toma buena?» = «no», sin que afecten al vídeo final).

**Criterio de aceptación:** con `tomas_por_escena` trayendo, para la escena 3, una toma marcada
`buena` con `numero: 2`, y un `registro_tropiezos` de esa escena con un tropiezo con
`numero_toma: 2` e `instante_toma_segundos: 47.0`, y otro con `numero_toma: 1` (toma descartada) en
la escena 5, `calcular_comandos_montaje(..., tomas_por_escena=..., registro_tropiezos=...)` produce
un documento con la sección «Puntos a revisar antes de concatenar» citando exactamente la escena 3
con el instante `00:47`, sin ninguna línea para la escena 5; llamando sin `registro_tropiezos` (o
con `None`, el valor por defecto) el documento es idéntico, byte a byte, al que genera hoy la misma
llamada; con `registro_tropiezos` pasado pero ningún tropiezo cruzando como de la toma buena en
ninguna escena, la sección tampoco aparece. Cuatro redes en verde.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
