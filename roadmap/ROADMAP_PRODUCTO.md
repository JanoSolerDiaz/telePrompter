# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-10-21 (ciclo de Product Manager). R-35 (Oleada v23) llevaba
`COMPLETADA` en §1 de `SEGUIMIENTO.md` desde el ciclo de Programador de esta misma jornada,
reconfirmada en verde nueve veces seguidas sin que ningún ciclo de PM la archivara todavía. Este
ciclo archiva la Oleada v23 en `ROADMAP_HISTORICO.md` y abre R-36 (Oleada v24) en §1, sin
implementarla: el criterio de una sola R-XX pendiente de código a la vez (vigente desde R-19) queda
respetado porque no había ninguna otra R-XX pendiente antes de abrir esta.

`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (única fila, plantilla vacía): no hay
historia de rodaje real que incorporar — el bloqueo #7 de `SEGUIMIENTO.md` §3 (grabar un curso
completo) sigue abierto. `auditoriacontinua.md` revisado antes de elegir tarea: solo dos `ABIERTO`
(`#24`, baja; `#30`, media), ambos de proceso/gobernanza puro y pendientes solo de la respuesta del
dueño a las preguntas #11/#12 de `SEGUIMIENTO.md` §6 — ninguno de severidad alta, ninguno
convertible en R-XX nueva ni en deuda técnica de backlog. (El hallazgo documental `#33`, cerrado por
P-07 el 2026-10-21, queda pendiente solo de que el auditor lo reconfirme `RESUELTO` en su siguiente
pasada — archivo de escritura exclusiva suya.)

**Oleada v23 (R-35) archivada.** Spec completa y "Cómo se entregó" en `ROADMAP_HISTORICO.md`.

**Oleada v24 (R-36) abierta, sin implementar.** Ficha completa más abajo. Origen: observación de
producto del propio PM (2026-10-21), verificada contra `assets/reproductor/guion.js` y
`scripts/feedback.py`: los tropiezos de una escena se guardan en una única lista plana por escena
(`tropiezosEscena[escena]`), acumulada a través de TODAS las tomas que el dueño grabe de ella —
nunca se separa por toma ni se reinicia al cerrar una y empezar la siguiente, a diferencia de
`tomasEscena[escena]` (R-02), que sí numera cada toma por separado y guarda cuál quedó marcada
`buena`. El `instante_toma_segundos` que R-34 añadió para "saltar directo al punto de corte en el
montaje con ffmpeg" se calcula siempre sobre el cronómetro de la toma en curso en el momento de
marcar, pero una vez guardado nada dice a cuál toma pertenece: en cuanto el dueño graba más de una
toma de la misma escena (el caso de uso para el que existe el propio registro de tomas de R-02, no
una excepción rara), un tropiezo de una toma descartada y uno de la toma buena conviven en la misma
lista con instantes que pertenecen a archivos de vídeo reales distintos.

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

### Oleada v24 — Vincular cada tropiezo con la toma en que se marcó

#### R-36 — Vincular cada tropiezo marcado con el número de la toma en que se marcó, para que el instante de R-34 no se confunda entre tomas distintas de la misma escena

**Migración:** No (ningún campo nuevo en `estado.json`: los tropiezos nunca se han persistido ahí,
igual que fijaron R-03/R-34; cambio aditivo en el `.json` exportado por "Exportar tropiezos" y en
`FEEDBACK.md` — `references/contrato-tropiezos.md` sube a versión 3) · **Depende de:** R-02 (parte
de rodaje, varias tomas por escena), R-03 (tropiezos marcados), R-34 (instante dentro de la toma) —
todas `COMPLETADA` · **Origen:** observación de producto del PM (2026-10-21), no de auditoría ni de
feedback de rodaje (`roadmap/FEEDBACK.md` sigue vacío) — grieta de arquitectura verificada sobre
código ya construido: `tropiezosEscena[escena]` (`assets/reproductor/guion.js`) es una única lista
plana por escena que se acumula a través de TODAS las tomas que el dueño grabe de ella — nunca se
reinicia ni se separa al cerrar una toma con `finalizarTomaActual` ni al empezar la siguiente —
mientras que `tomasEscena[escena]` sí numera cada toma por separado y guarda cuál quedó marcada
`buena` (R-02). Un tropiezo marcado con `T` durante la toma 1 (descartada después) y otro marcado
durante la toma 3 (la que el dueño termina marcando como buena, y la que de verdad llega al archivo
de vídeo real del montaje, R-19) quedan en la misma lista, indistinguibles salvo por
`indice_bloque`/`texto`; el `instante_toma_segundos` que R-34 guarda para cada uno (segundos desde
el inicio de "la toma en curso" en el momento de marcar) se calcula siempre sobre el cronómetro de
esa toma concreta, pero una vez guardado nada dice a cuál de ellas pertenece.

**Objetivo:** el propio motivo con el que se construyó R-34 era ahorrar al dueño, en el montaje con
ffmpeg que viene justo después de grabar, tener que reproducir la toma entera para encontrar a ojo
el segundo exacto donde se trabó. Ese ahorro solo es de fiar si el instante pertenece al ARCHIVO DE
VÍDEO REAL que de verdad se usa en el montaje — el de la toma marcada `buena` — y hoy no hay forma
de saberlo con el dato ya disponible: si el dueño graba dos o tres tomas de la misma escena (el caso
para el que existe el propio registro de tomas de R-02, no una excepción rara), `FEEDBACK.md` mezcla
instantes de tomas distintas en las mismas filas, sin avisar de cuál es cuál. Usar a ciegas el
instante de un tropiezo de una toma descartada busca un corte en un segundo que, en el archivo de
vídeo real de la toma buena, no significa nada — o, peor, coincide por azar con un instante distinto
del que de verdad falló.

**Requisitos:**
1. `alternarTropiezoBloqueActual` (`guion.js`): al AÑADIR un tropiezo (no al quitarlo — mismo
   criterio ya fijado por R-34 requisito 2), guardar también `numero_toma`: el número de la toma en
   curso en ese instante, mismo cálculo ya usado por `actualizarIndicadorToma`
   (`tomasEscena[escena].length + 1`), sin una segunda implementación del mismo número.
2. `cargarTropiezosGuardados`: tolerar la ausencia de `numero_toma` en un tropiezo ya guardado de una
   sesión anterior a esta tarea (mismo patrón de opcionalidad que ya aplica a
   `instante_toma_segundos` desde R-34) y conservarlo al construir el objeto normalizado — mismo
   punto de transformación que R-35 ya usa para `instante_toma_segundos`, sin tocar la lógica de
   relocalización por texto de R-35 (ortogonal: a qué toma pertenece un tropiezo no cambia según si
   su texto sigue siendo exacto o no).
3. `scripts/feedback.py`: `TropiezoBloque` gana `numero_toma: int | None = None` (entero ≥ 1 o
   `None`, mismo patrón de validación que `instante_toma_segundos`). `FEEDBACK.md` gana la columna
   «Toma», entre «Texto exacto» e «Instante» (agrupa el contexto de grabación — qué toma, qué
   segundo dentro de ella — en vez de intercalarlo con la identidad del bloque).
4. Mismo patrón que `_PATRON_FILA` ya usa para «Instante» (R-34): el grupo de «Toma» también opcional
   en la propia expresión regular, no solo en el valor, para que una fila de la versión 2 del
   contrato (sin «Toma», 6 columnas) o de la versión 1 (sin ninguna de las dos, 5 columnas) se sigan
   reconociendo exactamente igual que una de 7 columnas — ninguna fila ya marcada a mano por el
   dueño (`nuevo`/`resuelto`) deja de encontrarse por el cambio de formato.
5. Cabecera de `FEEDBACK.md` (`_ENCABEZADO_FEEDBACK`) explica la columna nueva y avisa explícitamente:
   el instante solo es un punto de corte de fiar en el vídeo final cuando «Toma» coincide con el
   número que el parte de rodaje (R-02) tiene marcado como la toma buena de esa escena — cruce que
   el dueño hace a mano con el parte de rodaje que ya tiene, igual que ya hace hoy para saber qué
   `archivo_video` corresponde a cada escena.
6. `version` del `.json` exportado sube a 3 (aditivo); `references/contrato-tropiezos.md` documenta
   el campo nuevo y la misma advertencia de uso del requisito 5.
7. **Fuera de alcance, explícito:** no se cruza automáticamente «Toma» contra el registro de tomas
   para anotar en el propio `FEEDBACK.md`, de forma automática, cuál fila pertenece a la toma buena —
   tomas y tropiezos siguen siendo dos archivos exportados por separado (mismo diseño ya decidido
   para R-02/R-03), y fusionarlos de verdad sería un cambio de alcance mayor, no pedido por esta
   ficha; el dueño hace el cruce a mano con el número de toma que ya tiene en el parte de rodaje.
   Tampoco se toca `cargarTomasGuardadas`/`tomasEscena` (R-02/R-19 intactos), ni la lógica de
   relocalización por texto de R-35 (sigue casando por texto exacto, independiente de a qué toma
   pertenezca cada tropiezo), ni se renumera retroactivamente ningún tropiezo ya exportado en una
   versión anterior del contrato (sin `numero_toma`, sigue mostrando la columna vacía, igual que ya
   hace «Instante» con los archivos de la versión 1).

**Criterio de aceptación:** con una escena grabada dos veces (toma 1, con un tropiezo marcado en el
bloque 0; toma 2, marcada `buena`, con un tropiezo marcado en el bloque 2), al pulsar "Exportar
tropiezos" el `.json` trae `numero_toma: 1` en el primer tropiezo y `numero_toma: 2` en el segundo;
`FEEDBACK.md` muestra la columna «Toma» con esos valores junto al «Instante» de cada fila; una fila
ya existente de la versión 2 del contrato (sin «Toma») se sigue reconociendo exactamente igual que
antes (camino feliz intacto, sin perder su estado `nuevo`/`resuelto`); `references/contrato-
tropiezos.md` sube a versión 3 documentando el campo y la advertencia de uso. Cuatro redes en verde.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
