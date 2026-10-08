# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-10-08 (ciclo de PM). **R-25 (Oleada v13) está `COMPLETADA`** (§1 de
`SEGUIMIENTO.md`) desde el ciclo de Programador del 2026-10-08 que la implementó (séptima salida
seleccionable, `convencion-guiones.md`, conectada de verdad al selector de T-30). A diferencia de
R-24, esta vez la fila de §1 se añadió en el mismo commit que abrió la tarea (resolviendo de paso el
hallazgo `#29` de `auditoriacontinua.md`), así que no hay prosa desactualizada que corregir. Movida a
`roadmap/ROADMAP_HISTORICO.md` (Oleada v13) junto con el resto de oleadas 100 % entregadas.

**Se abre R-26** (Oleada v14): no por hallazgo de auditoría ni entrada de `FEEDBACK.md` — ninguna de
las dos fuentes aporta nada nuevo este ciclo (ver abajo) — sino por **grieta de arquitectura
verificada sobre código ya construido**, el mismo criterio que abrió R-12 a R-25, esta vez de
severidad mayor que las anteriores: no es una salida huérfana sin consumidor, es una **garantía
contractual que hoy no se cumple en el flujo real**. Verificación propia, leyendo el código línea a
línea, no solo nombres ni docstrings: `scripts/normalizacion.py::cargar_diccionario_locucion` (T-13,
requisito 3 — "Diccionario de excepciones editable por el dueño... con prioridad sobre las reglas
automáticas", repetido en `SKILL.md`: "el diccionario del dueño manda siempre sobre cualquiera de
ellas") no tiene **ningún** llamador fuera de sus propios tests — confirmado con `grep -rn
"cargar_diccionario_locucion" scripts/*.py`, único resultado la propia definición. Peor aún: los
cuatro puntos reales donde se aplicaría (`normalizar_guion`, `reescrituras.recopilar_propuestas`,
`documento_revision.generar_documento_revision`, `revalidacion.revalidar_guion`) tampoco tienen,
fuera de sus tests, ningún llamador que construya y pase un `diccionario` cargado de disco — todos
reciben `diccionario=None` por omisión en cualquier uso real, confirmado con el mismo `grep` sobre
`normalizar_guion\(\|recopilar_propuestas\(\|generar_documento_revision\(\|revalidar_guion\(` en
`scripts/*.py`. Los tests de T-13 prueban por separado que "cargar el archivo" funciona y que "un
diccionario ya cargado en memoria sobrescribe la regla automática" — nunca las dos cosas juntas sobre
un `diccionario-locucion.json` real en la carpeta de salida de un guion real, que es exactamente el
uso que promete el requisito 3. Candidata alternativa descartada tras la misma verificación:
`scripts/reescrituras.py::revertir_reescrituras` (T-15, deshacer global) sigue siendo un orfanato de
consumidor documentado — ya se consideró y descartó al abrir R-25 por menor valor y mayor riesgo de
diseño (no existe hoy ninguna superficie por la que el dueño dispare un "deshacer global"), y nada ha
cambiado ese análisis esta pasada. Detalle completo en "Oleada v14" más abajo.

`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (única fila, plantilla vacía): no hay
historia de rodaje real que incorporar este ciclo — el bloqueo #7 de `SEGUIMIENTO.md` §3 (grabar un
curso completo) sigue abierto. El registro de hallazgos de `auditoriacontinua.md` no trae ningún
`ABIERTO` nuevo de producto/arquitectura esta pasada: quedan dos `ABIERTO`, ambos de proceso y de
severidad baja, ninguno de los cuales necesita una R-XX — `#24` (prosa de "Cola de producto"
desactualizada entre ciclos de PM, sin repetirse esta vez: ver arriba) sigue pendiente de la
respuesta del dueño a la pregunta de gobernanza #11 de `SEGUIMIENTO.md` §6; `#29` (la fila de R-25
faltaba en §1 al abrirse) ya quedó resuelto por el propio ciclo de Programador que implementó R-25, el
cierre a `RESUELTO` en `auditoriacontinua.md` queda para la siguiente pasada del auditor.

Este ciclo es de PM, no de Programador: no se ha ejecutado la verificación de las cuatro redes; la
spec de R-26 queda lista para que el siguiente ciclo de Programador la implemente y verifique.

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

### Oleada v14 — EN CURSO

#### R-26 — El diccionario del dueño (`diccionario-locucion.json`, T-13) no está conectado al flujo real: su garantía contractual ("manda siempre") no se cumple salvo que la sesión recuerde cargarlo a mano

**Migración:** No (ningún campo de `estado.json` cambia; cambio de visibilidad/composición dentro de
módulos ya existentes) · **Depende de:** T-13, T-16, T-17 (todas ya `COMPLETADA`) · **Origen:**
observación de arquitectura del PM (2026-10-08) — grieta de arquitectura verificada sobre código ya
construido (mismo criterio que abrió R-12 a R-25).

**Objetivo:** T-13 (2026-09-01) especifica, como requisito 3, que el dueño puede corregir cualquier
normalización automática con una entrada literal en `diccionario-locucion.json`, dentro de la carpeta
de salida del guion, y que esa entrada **"siempre gana"** sobre cualquier regla automática —
repetido palabra por palabra en `SKILL.md` ("el diccionario del dueño manda siempre sobre cualquiera
de ellas") y en `references/convencion-guion.md`. Verificado leyendo el código, no solo la
documentación: `scripts/normalizacion.py::cargar_diccionario_locucion` (la función que lee ese
archivo de disco) no tiene **ningún** llamador fuera de sus propios tests —
`grep -rn "cargar_diccionario_locucion" scripts/*.py` solo devuelve su propia definición. El fallo no
se queda ahí: los cuatro puntos reales donde el diccionario debería aplicarse —
`normalizacion.normalizar_guion`, `reescrituras.recopilar_propuestas` (que ni siquiera tiene un
parámetro `diccionario`), `documento_revision.generar_documento_revision` (la generación del primer
`guion-escenas.md`) y `revalidacion.revalidar_guion` (el único punto de entrada de la revalidación,
documentado así en `DEVELOPERS.md`) — tampoco tienen, fuera de sus tests, ningún llamador real que
construya un diccionario cargado de disco y lo pase: todos reciben `diccionario=None` por omisión en
cualquier uso sobre un guion real, confirmado con el mismo `grep` sobre las cuatro funciones en
`scripts/*.py`. La prueba más clara de la grieta: `tests/test_normalizacion.py` solo verifica (a) que
`cargar_diccionario_locucion` lee bien el JSON del disco, por separado, y (b) que un diccionario ya
construido a mano en memoria (`diccionario={"2026": "el año que viene"}`) sobrescribe la regla
automática — nunca las dos cosas juntas, que es exactamente el camino real: el dueño escribe
`diccionario-locucion.json` en la carpeta de salida esperando que la siguiente generación o
revalidación lo respete sin tener que pedirlo explícitamente cada vez. A diferencia de las grietas que
abrieron R-12 a R-25 (una salida o un cálculo sin consumidor, valor perdido pero sin promesa
incumplida), esta es una **garantía contractual del propio documento de especificación que hoy no se
sostiene en el flujo real** — el dueño podría escribir una corrección en el diccionario, no verla
aplicada, y no tener ninguna señal de que algo falló: el requisito 3 no se cumple en silencio, sin
ningún aviso, justo lo que el principio de producto nº 1 ("nada se descarta en silencio") prohíbe.
Candidata alternativa descartada tras la misma verificación: `scripts/reescrituras.py::
revertir_reescrituras` (T-15, deshacer global) sigue sin disparador documentado, pero ya se consideró
y descartó al abrir R-25 por menor valor y mayor riesgo de diseño (no existe hoy ninguna superficie
por la que el dueño dispare un "deshacer global"); nada ha cambiado ese análisis esta pasada.

**Requisitos:**
1. El recuento de entradas del diccionario efectivamente aplicado (0 si no hay archivo o si no se
   cargó) se hace **visible** en la cabecera del resumen global de `guion-escenas.md` (T-16) y en
   `tarjetas.json.metadatos` (T-29/pptx), mismo criterio de transparencia que T-12 ya aplica al ppm
   ("de dónde sale y cuál sería el otro valor"): nunca más una omisión silenciosa de un archivo que el
   dueño sí escribió.
2. `documento_revision.generar_documento_revision` y `revalidacion.revalidar_guion` — los dos puntos
   reales de generación/revalidación — ganan la responsabilidad de cargar el diccionario del dueño
   cuando se les indica la carpeta de salida, reutilizando tal cual `normalizacion.
   cargar_diccionario_locucion` (cero segunda implementación, cero cambio en su propia lectura de
   disco ni en `normalizar_guion`/`normalizar_texto`, que siguen aceptando un `diccionario` explícito
   para sus propios tests unitarios sin tocar disco). El diseño exacto de la firma (parámetro nuevo,
   valor por defecto, orden de prioridad frente a un `diccionario` ya explícito) lo decide quien
   implemente, documentado en `DECISIONES_TECNICAS.md`.
3. `SKILL.md` dedica una instrucción explícita, con el fragmento de código exacto a invocar (mismo
   patrón ya usado para `tropiezos_por_escena` en la sección de R-03: "la siguiente vez que se
   regenere `guion-escenas.md` ..."), para que generar o revalidar sobre un guion real **siempre**
   pase por la carga del diccionario — no una mención en una tabla de valores por defecto, sino un
   paso nombrado del flujo que Claude no pueda pasar por alto.
4. `reescrituras.recopilar_propuestas` gana un parámetro `resultados_normalizacion` ya calculado con
   el diccionario correspondiente (no cambia su propia lógica de unión de propuestas) — se limita a
   dejar de ser, sin saberlo, el punto donde el diccionario se pierde si quien llama no lo propaga.
5. Fuera de alcance, explícito: no se cambia el formato de `diccionario-locucion.json` ni las reglas
   de prioridad ya fijadas por T-13 (diccionario > familias automáticas); no se añade ningún campo
   nuevo a `Configuracion` ni a `estado.json`; no se construye ningún `main()` de CLI nuevo que
   orqueste todo el ciclo de punta a punta (sigue siendo responsabilidad de la sesión que usa la
   skill, como documenta T-16/T-17) — esta tarea cierra la grieta del diccionario específicamente,
   no diseña la orquestación general que todavía falta.

**Criterio de aceptación:** test de integración que escribe un `diccionario-locucion.json` real en
una carpeta de salida y comprueba que generar `guion-escenas.md`/revalidar sobre un guion real aplica
la entrada sin que el test construya el diccionario a mano en memoria (a diferencia de los tests
actuales de T-13); test que confirma que la cabecera de `guion-escenas.md` y `tarjetas.json.metadatos`
muestran el recuento correcto (0 sin archivo, N con N entradas); regresión de los tests existentes de
T-13/T-16/T-17 sin cambios de comportamiento cuando no hay diccionario. Cuatro redes en verde.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
