# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-10-15 (ciclo de PM). **R-30 (Oleada v18) está `COMPLETADA`** (§1 de
`SEGUIMIENTO.md`) desde el ciclo de Programador del propio 2026-10-14 que la implementó (encadenado
en `comandos-montaje.md` de los tres comandos `ffmpeg` reales de montaje, reutilizando tal cual las
piezas ya construidas por R-05/R-19/R-22, octava opción del selector de salidas). Movida a
`roadmap/ROADMAP_HISTORICO.md` (Oleada v18) junto con el resto de oleadas 100 % entregadas. §1 de
`SEGUIMIENTO.md` llevaba desde esa misma madrugada sin ninguna fila `PENDIENTE` — nueve
reconfirmaciones horarias del Programador a lo largo del día sin tarea que ejecutar, el mismo coste
que señala el hallazgo `#30`/pregunta `#12` (aún sin respuesta del dueño).

`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (única fila, plantilla vacía): no hay
historia de rodaje real que incorporar este ciclo — el bloqueo #7 de `SEGUIMIENTO.md` §3 (grabar un
curso completo) sigue abierto. El registro de hallazgos de `auditoriacontinua.md` trae un hallazgo
nuevo de proceso puro (`#31`, baja: la apertura de R-30 no dejó su fila en `DECISIONES_TECNICAS.md`
— corregida en este mismo ciclo, ver nota de gobernanza en `ROADMAP_HISTORICO.md`, Oleada v18) y
reconfirma los dos ya conocidos (`#24`, prosa de "Cola de producto" desactualizada entre ciclos de
PM; `#30`, cadencia de la rutina "Programador"), los tres de severidad baja/media, sin relación con
el código, pendientes solo de la respuesta del dueño a las preguntas de gobernanza #11/#12 de
`SEGUIMIENTO.md` §6 — ninguno de producto/arquitectura que convertir en R-XX nueva por esta vía.

**Se abre R-31** (Oleada v19): tampoco por auditoría ni por `FEEDBACK.md`, sino por el mismo tercer
criterio que abrió R-12 a R-30 — una **grieta de arquitectura verificada sobre código ya
construido**, esta vez en la propia salida que R-30 acaba de entregar. `comandos-montaje.md` calcula
sus tres comandos como una función pura de `tomas_por_escena` (R-30, por diseño: "nunca relee del
disco lo que otras salidas ya hayan escrito"), así que puede generarse seleccionando SOLO
`COMANDOS_MONTAJE` en el selector de salidas, sin seleccionar también `CONCAT_FFMPEG`/`SRT`/
`CAPITULOS_YOUTUBE` (generación independiente, T-30 requisito 3) — en ese caso el documento referencia
`concat-ffmpeg.txt`/el `.srt` elegido/`capitulos-ffmpeg.txt` por su nombre fijo aunque esos archivos
no existan todavía en la carpeta de salida. No es una hipótesis: el propio test de R-30
(`tests/test_salidas.py::test_comandos_montaje_es_independiente_de_que_tambien_se_seleccione_concat_ffmpeg`)
fija y prueba exactamente ese caso — `not (tmp_path / NOMBRE_ARCHIVO_CONCAT_FFMPEG).exists()` a la vez
que `"concat-ffmpeg.txt" in archivo.ruta.read_text(...)`. El dueño que siga ese documento al pie de la
letra la primera vez se encontraría con un `ffmpeg`: `concat-ffmpeg.txt: No such file or directory`.
Detalle completo en "Oleada v19" más abajo.

Este ciclo es de PM, no de Programador: no se ha ejecutado la verificación de las cuatro redes; la
spec de R-31 queda lista para que el siguiente ciclo de Programador la implemente y verifique.

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

### Oleada v19 — EN CURSO

#### R-31 — Advertir en `comandos-montaje.md` cuando el documento referencia un archivo que no existe todavía en esta carpeta de salida, en vez de dar por hecho que las demás salidas de las que depende ya se generaron

**Migración:** No (ningún campo nuevo en `estado.json`; mismo módulo y misma salida de R-30, solo
gana una comprobación adicional antes de formatear el texto) · **Depende de:** R-30 (`COMPLETADA`) ·
**Origen:** observación de arquitectura del PM (2026-10-15) — grieta de arquitectura verificada sobre
código ya construido (mismo tercer criterio que abrió R-12 a R-30), esta vez en la propia salida que
R-30 acaba de entregar, no en código heredado de tareas anteriores.

**Objetivo:** `comandos_montaje.calcular_comandos_montaje` (R-30) es, por diseño deliberado, una
función **pura** de `tomas_por_escena`: nunca relee del disco lo que `concat-ffmpeg.txt`,
`guion.srt`/`guion-alineado.srt` o `capitulos-ffmpeg.txt` ya hayan escrito, precisamente para no
depender de que el dueño haya seleccionado también esas otras salidas en la misma pasada (generación
independiente, T-30 requisito 3). Esa misma independencia es la que abre la grieta: el selector de
salidas (`scripts/salidas.py`) deja elegir **solo** `COMANDOS_MONTAJE` sin elegir también
`CONCAT_FFMPEG`/`SRT`/`CAPITULOS_YOUTUBE`, y en ese caso `comandos-montaje.md` se genera igual,
citando esos tres archivos por su nombre fijo como si ya existieran en la carpeta de salida. No es
una hipótesis del PM: el propio test de R-30
(`tests/test_salidas.py::test_comandos_montaje_es_independiente_de_que_tambien_se_seleccione_concat_ffmpeg`)
fija y prueba exactamente este caso —selecciona solo `COMANDOS_MONTAJE`, confirma con
`not (tmp_path / NOMBRE_ARCHIVO_CONCAT_FFMPEG).exists()` que `concat-ffmpeg.txt` NO está en disco, y
a la vez confirma que `"concat-ffmpeg.txt" in archivo.ruta.read_text(...)`—. Un dueño que, sin
conocer ese matiz, copie el primer comando de `comandos-montaje.md` tal cual la primera vez se
encuentra con `ffmpeg: concat-ffmpeg.txt: No such file or directory`, exactamente el tipo de
fricción manual silenciosa que el resto del producto (y la propia R-30) existe para eliminar.

Decisiones de diseño ya tomadas para acotar el alcance:
- **Comprobación de existencia en disco, no de contenido.** Los tres archivos referenciados
  (`concat-ffmpeg.txt`, el `.srt` que corresponda, `capitulos-ffmpeg.txt`) ya tienen su propio
  validador de formato en su propia ruta de generación (R-21/R-28): esta tarea solo necesita saber
  si el archivo **está** en `carpeta_salida` (de esta misma pasada o de una anterior), no releer ni
  revalidar su contenido.
- **El orden de `TODAS_LAS_SALIDAS` ya resuelve el caso favorable.** `COMANDOS_MONTAJE` es la octava
  y última opción que procesa `scripts/salidas.py::generar_salidas_seleccionadas`; si el dueño
  selecciona también `CONCAT_FFMPEG`/`SRT`/`CAPITULOS_YOUTUBE` en la misma pasada, esos archivos ya
  estarán escritos en disco cuando le toque el turno a `COMANDOS_MONTAJE` — la comprobación de
  existencia no necesita ningún orden especial ni forzar nada, solo mirar el disco real en el
  momento en que a ella le toca generarse.
- **Nunca bloquea ni degrada la generación.** Mismo principio que ya fijó R-30 ("cada paso es
  opcional y el encadenado nunca se rompe por un hueco"): un archivo ausente en disco es un hueco
  más que reportar con una nota visible, igual que ya hace el documento con las escenas sin toma
  buena o sin archivo anotado — nunca un motivo para que la salida entera quede omitida o en fallo.
- **No se fuerza ninguna selección conjunta.** Seleccionar `COMANDOS_MONTAJE` sigue sin exigir
  seleccionar también las otras tres opciones (generación independiente, T-30 requisito 3 — pilar
  del selector desde T-30, no se toca); el remedio es avisar, no acoplar.

**Requisitos:**
1. `scripts/comandos_montaje.py::calcular_comandos_montaje` (o, si encaja mejor con cómo ya recibe
   `carpeta_salida`, `scripts/salidas.py::_generar_comandos_montaje`) comprueba, tras construir los
   pasos, si `concat-ffmpeg.txt`, el `.srt` elegido (`guion-alineado.srt` si hay alineación, si no
   `guion.srt`) y, solo cuando el tercer paso está incluido, `capitulos-ffmpeg.txt` existen de
   verdad en `carpeta_salida`.
2. `formatear_comandos_montaje` añade, por cada archivo referenciado que falte, una nota visible
   (bajo el paso que lo usa, o agrupada en una sección propia antes de los pasos) citando el nombre
   del archivo que falta y la opción exacta del selector que hay que marcar para generarlo (el mismo
   texto de `DESCRIPCION_SALIDA` en `scripts/salidas.py`), para que el dueño sepa qué seleccionar la
   próxima vez antes de ejecutar el comando.
3. Ningún archivo faltante bloquea la generación de `comandos-montaje.md` ni lo degrada a
   `SalidaOmitida`/fallo: el documento se genera igual, con la nota añadida.
4. Si los tres archivos referenciados ya existen en `carpeta_salida` (de esta misma pasada o de una
   anterior), el documento no gana ninguna línea nueva respecto al comportamiento actual de R-30 —
   sin falso positivo.
5. Fuera de alcance, explícito: no se valida el CONTENIDO de los archivos referenciados (ya lo hacen
   sus propios validadores en su propia ruta de generación, R-21/R-28); no se fuerza a generarlos
   automáticamente ni se cambia la generación independiente de T-30 requisito 3; no se cambia ninguna
   regla de `concat_ffmpeg.py`, `srt.py`/`srt_alineado.py` ni `capitulos_youtube.py` en sí.

**Criterio de aceptación:** seleccionando solo `COMANDOS_MONTAJE` (sin `CONCAT_FFMPEG`/`SRT`/
`CAPITULOS_YOUTUBE`) sobre un guion con parte de rodaje completo, `comandos-montaje.md` trae los
tres comandos de siempre MÁS una nota visible por cada uno de los tres archivos referenciados que no
está en la carpeta de salida; seleccionando las cuatro opciones a la vez en la misma pasada, el
documento no trae ninguna nota (todos ya en disco cuando le toca el turno a `COMANDOS_MONTAJE`);
seleccionando solo `COMANDOS_MONTAJE` tras una pasada anterior que ya dejó esos tres archivos en esa
misma carpeta, tampoco aparece ninguna nota (existencia real en disco, no "seleccionado en esta
pasada"). Test nuevo que reproduce el escenario ya fijado por
`test_comandos_montaje_es_independiente_de_que_tambien_se_seleccione_concat_ffmpeg` verificando que
ahora SÍ aparece el aviso. Cuatro redes en verde.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
