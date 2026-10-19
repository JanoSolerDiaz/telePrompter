# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-10-19 (tercer ciclo del día, ciclo de Product Manager). R-33 (Oleada
v21) llevaba `COMPLETADA` en §1 de `SEGUIMIENTO.md` desde el ciclo combinado de PM + Programador de
la sesión 190, el mismo día, sin que ningún ciclo de PM la archivara todavía. Este ciclo archiva la
Oleada v21 en `ROADMAP_HISTORICO.md` y abre R-34 (Oleada v22) en §1, sin implementarla: el criterio
de una sola R-XX pendiente de código a la vez (vigente desde R-19) queda respetado porque no había
ninguna otra R-XX pendiente antes de abrir esta.

`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (única fila, plantilla vacía): no hay
historia de rodaje real que incorporar — el bloqueo #7 de `SEGUIMIENTO.md` §3 (grabar un curso
completo) sigue abierto. `auditoriacontinua.md` revisado antes de elegir tarea: solo dos `ABIERTO`
(`#24`, baja; `#30`, media), ambos de proceso/gobernanza puro y pendientes solo de la respuesta del
dueño a las preguntas #11/#12 de `SEGUIMIENTO.md` §6 — ninguno de severidad alta, ninguno
convertible en R-XX nueva ni en deuda técnica de backlog.

**Oleada v21 (R-33) archivada.** Spec completa y "Cómo se entregó" en `ROADMAP_HISTORICO.md`.

**Oleada v22 (R-34) abierta, sin implementar.** Ficha completa más abajo. Origen: observación de
producto del propio PM (2026-10-19), verificada contra `assets/reproductor/guion.js` y
`scripts/feedback.py`: ningún llamador real guarda hoy ningún instante de tiempo junto a un tropiezo
marcado, pese a que el cronómetro de la toma (T-23) ya calcula ese dato para otro consumidor
(`finalizarTomaActual`, R-02) en el mismo archivo.

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

### Oleada v22 — Instante exacto de cada tropiezo dentro de la toma

#### R-34 — Capturar el instante real (segundos desde el inicio de la toma) en que se marca un tropiezo, para saltar directo al punto de corte en el montaje con ffmpeg

**Migración:** No (ningún campo nuevo en `estado.json`: los tropiezos no se persisten ahí, igual que
fijó R-03; cambio aditivo en el `.json` exportado por "Exportar tropiezos" y en el `FEEDBACK.md` de
la carpeta de salida — `references/contrato-tropiezos.md` sube a versión 2) · **Depende de:** T-23
(cronómetro de la toma), R-02 (parte de rodaje), R-03 (tropiezos marcados) — todas `COMPLETADA` ·
**Origen:** observación de producto del PM (2026-10-19), no de auditoría ni de feedback de rodaje
(`roadmap/FEEDBACK.md` sigue vacío) — grieta de producto verificada sobre código ya construido:
`assets/reproductor/guion.js::finalizarTomaActual` (R-02) ya calcula el tiempo real transcurrido
desde el inicio de la toma en curso (`cronometroMsAcumulados` + lo corrido desde
`cronometroInicioMarca` si no está en pausa) para guardar `duracion_segundos` de la toma, pero
`alternarTropiezoBloqueActual` (R-03), que vive en el mismo archivo y se dispara con la misma tecla
`T` mientras esa toma está en marcha, no reutiliza ese cálculo: un tropiezo marcado hoy solo guarda
`indice_bloque` y `texto`, nunca CUÁNDO ocurrió dentro de la toma. `scripts/feedback.py` (el lado
Python del volcado) confirma la misma ausencia: `TropiezoBloque` no tiene ningún campo de tiempo.

**Objetivo:** cuando el dueño marca con `T` un bloque como tropiezo mientras graba, el reproductor ya
sabe en qué segundo de la toma en curso ocurre (es el mismo cronómetro que ya muestra en pantalla,
T-23) — hoy ese dato se descarta en el momento de marcar. Capturarlo y llevarlo hasta el `FEEDBACK.md`
de la carpeta de salida (y hasta ahí llega hoy, sin ningún apoyo del reproductor) ahorra al dueño,
en la fase de montaje con ffmpeg (T-33) que viene justo después, tener que reproducir la toma entera
para encontrar a ojo el segundo exacto del archivo de vídeo real donde se trabó — el mismo principio
de producto que ya justificó R-19 (enlazar la toma con su archivo de vídeo) y R-22 (capítulos
incrustables): dar al montaje datos que ya existen en memoria durante la grabación, en vez de
obligar al dueño a reconstruirlos a mano después.

**Requisitos:**
1. `guion.js`: extraer el cálculo de tiempo transcurrido que hoy vive solo dentro de
   `finalizarTomaActual` (`cronometroMsAcumulados` + lo corrido desde `cronometroInicioMarca` si
   `!pausado`) a una función compartida, y que `alternarTropiezoBloqueActual` la reutilice tal cual
   — nunca una segunda implementación del mismo cálculo (mismo criterio ya aplicado en R-19/R-20:
   "promover la función que ya existe, no duplicarla").
2. Al marcar un bloque como tropiezo (no al desmarcarlo), el objeto guardado en `tropiezosEscena`
   gana `instante_toma_segundos` (número, segundos desde el inicio de la toma en curso en ese
   instante, con el mismo redondeo a un decimal que ya usa el cronómetro visible). Si se desmarca el
   tropiezo antes de exportar, se pierde entero (el elemento se elimina del array), igual que hoy se
   pierde `texto`/`indice_bloque`: no hay historial de tropiezos retirados, fuera de alcance.
3. **Límite documentado, no resuelto con heurística:** `instante_toma_segundos` describe el momento
   dentro de la toma que estaba en marcha cuando se pulsó `T`, no se re-ancla si después se repite la
   escena y se marca una toma distinta como "buena" (`G`) sin volver a marcar el mismo tropiezo en
   ella. `references/contrato-tropiezos.md` documenta explícitamente esta limitación: el dato es
   fiable sin más cuando se sigue grabando sin cortar tras el tropiezo (el caso más común al empujar
   una toma larga), y deja de serlo si se regraba la escena desde cero; no se intenta adivinar a cuál
   toma pertenece cada tropiezo, porque eso exigiría inventar una asociación que el dueño no dio.
4. `scripts/feedback.py`: `TropiezoBloque` gana el campo opcional `instante_toma_segundos: float |
   None = None`; `_tropiezo_desde_dict` lo admite si está presente (numérico, ≥ 0) y lo deja en
   `None` si falta — un `.json` de tropiezos exportado por una versión anterior del reproductor
   (sin el campo) se sigue cargando sin error, igual que R-19 con `archivo_video` ausente.
5. `_ENCABEZADO_FEEDBACK`/`_PATRON_FILA`/`registrar_tropiezos_en_feedback`: columna nueva «Instante»
   en la tabla de `FEEDBACK.md` (carpeta de salida), con el valor formateado `mm:ss` (vacía si
   `instante_toma_segundos` es `None`). La detección de fila duplicada (misma escena + mismo índice
   de bloque + mismo texto) no cambia: el instante es informativo, no forma parte de la clave.
6. `references/contrato-tropiezos.md` sube a **versión 2** (cambio aditivo): documenta el campo
   nuevo, su ausencia en archivos de la versión 1, el formato `mm:ss` de la columna nueva y la
   limitación del requisito 3, con el mismo nivel de detalle que ya tiene el resto del contrato.
7. **Fuera de alcance, explícito:** no se genera ningún comando `ffmpeg` de salto automático a partir
   de este instante (construir sobre un dato sin verificación de rodaje real todavía sería
   adelantarse; candidata a una R-XX futura si el primer rodaje real lo pide); no se toca
   `documento_revision.py` más allá de lo que ya hace hoy (sigue destacando el bloque por texto, T-15);
   no se persiste nada en `estado.json` (mismo criterio ya fijado por R-03); no se añade ninguna
   tecla nueva (se reutiliza `T`, ya asignada); no se cambia la convención de marcado ni la identidad
   visual 480.

**Criterio de aceptación:** con un test que controla el reloj (doble de `Date.now`, sin depender de
tiempo real de ejecución), marcar un tropiezo a los 47,0 s de una toma en curso exporta
`instante_toma_segundos: 47.0`; la fila correspondiente de `FEEDBACK.md` (carpeta de salida) muestra
`00:47` en la columna nueva; un `.json` de tropiezos sin el campo (fixture de la versión 1 del
contrato) se sigue cargando sin error, con la columna vacía para esas filas; exportar el mismo
registro dos veces no duplica filas (mismo criterio ya exigido por R-03). Cuatro redes en verde.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
