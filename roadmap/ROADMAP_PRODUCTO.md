# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-10-06 (ciclo de PM). **R-23 (Oleada v11) está `COMPLETADA`** (§1 de
`SEGUIMIENTO.md`) desde el ciclo de Programador del 2026-10-06 que la implementó (desviaciones de
convención en `guion-escenas.md`/`tarjetas.json`). Nueve reconfirmaciones del Programador el mismo
día la dejaron en este documento como `PENDIENTE` en vez de archivarla (mismo patrón que el hallazgo
`#24` de `auditoriacontinua.md`, pendiente de la respuesta del dueño a la pregunta de gobernanza #11
de `SEGUIMIENTO.md` §6 sobre quién puede corregir esa prosa). Movida a `roadmap/ROADMAP_HISTORICO.md`
(Oleada v11) junto con el resto de oleadas 100 % entregadas.

**Se abre R-24** (Oleada v12): no por hallazgo de auditoría ni entrada de `FEEDBACK.md` — ninguna de
las dos fuentes aporta nada nuevo este ciclo (ver abajo) — sino por **grieta de arquitectura
verificada sobre código ya construido**, el mismo criterio que abrió R-12 a R-23. Un subagente de
exploración propuso tres candidatas (`convencion.generar_convencion_guiones`/`guardar_convencion_guiones`
sin ningún consumidor; `reescrituras.revertir_reescrituras` sin disparador documentado; la
infraestructura de diagnóstico de T-02/T-05 sin consumidor real); verificación independiente propia,
leyendo el código línea a línea antes de especificar la tarea: `scripts/logger.py` (T-02) y
`scripts/monitorizacion.py` (T-05) se construyeron el primer día del proyecto (2026-09-01)
anticipando un futuro "punto de entrada real" que las usara — su propio docstring de entonces lo dice
literalmente: *"todavía no hay un `main()` real que envolver... esta tarea deja la mecánica lista y
probada para que cada punto de entrada futuro la use en vez de inventar su propio manejo de
errores"*. Ese punto de entrada real llegó después, no como un `main()` único sino como
`scripts/salidas.py::generar_salidas_seleccionadas` (T-30/R-18), que hoy genera de verdad las salidas
seleccionables del dueño — y su manejo de errores (línea ~499) es exactamente ese "manejo de errores
inventado por su cuenta" que T-05 quería evitar: `except Exception as excepcion:
omitidas.append(SalidaOmitida(tipo, f"fallo al generar: {excepcion}"))`, sin volcar ningún diagnóstico
y mostrando al dueño el `repr` crudo de la excepción en vez de un mensaje accionable en español —
contradice directamente dos reglas de §0.2 ("Logger centralizado", "Errores accionables en español,
nunca trazas crudas"). Detalle completo en "Oleada v12" más abajo.

`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (única fila, plantilla vacía): no hay
historia de rodaje real que incorporar este ciclo — el bloqueo #7 de `SEGUIMIENTO.md` §3 (grabar un
curso completo) sigue abierto. El registro de hallazgos de `auditoriacontinua.md` no trae ningún
`ABIERTO` nuevo de producto/arquitectura esta pasada: el único `ABIERTO` (`#24`, baja, prosa de "Cola
de producto" desactualizada entre ciclos de PM) sigue enrutado a la pregunta de gobernanza #11 de
`SEGUIMIENTO.md` §6, `(pendiente)` de respuesta del dueño — no es una R-XX, es la misma corrección de
prosa que este propio ciclo acaba de aplicar de nuevo, esta vez sobre R-23.

Este ciclo es de PM, no de Programador: no se ha ejecutado la verificación de las cuatro redes; la
spec de R-24 queda lista para que el siguiente ciclo de Programador la implemente y verifique.

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
pendiente. Se movió a `ROADMAP_HISTORICO.md` en este ciclo de PM (2026-10-06). Su spec completa y
cómo se entregó viven ahí.

### Oleada v12 — EN CURSO

#### R-24 — Diagnóstico real de un fallo al generar una salida, en vez de la traza cruda de la excepción

**Migración:** No (cambio interno de manejo de errores dentro de una función ya existente;
promoción de visibilidad de una función privada a pública; ningún campo de `estado.json` ni de
`Configuracion` cambia de forma) · **Depende de:** T-02, T-05, T-30 (las tres ya `COMPLETADA`) ·
**Origen:** observación de arquitectura del PM (2026-10-06) — grieta de arquitectura verificada
sobre código ya construido (mismo criterio que abrió R-12 a R-23), no hallazgo de auditoría ni
entrada de `FEEDBACK.md`.

**Objetivo:** `scripts/logger.py` (T-02) y `scripts/monitorizacion.py` (T-05) se construyeron el
primer día del proyecto (2026-09-01) como la única capa autorizada para diagnóstico técnico y para
capturar un fallo no controlado, anticipando explícitamente un futuro "punto de entrada real" que
las usara en vez de inventar su propio manejo de errores (cita literal del docstring de la época:
*"todavía no hay un `main()` real que envolver... esta tarea deja la mecánica lista y probada para
que cada punto de entrada futuro la use"*). Ese punto de entrada real llegó después, no como un único
`main()` de CLI sino como `scripts/salidas.py::generar_salidas_seleccionadas` (T-30, ampliada por
R-18): la función que hoy genera de verdad cada salida seleccionable del dueño (reproductor, `.srt`,
`.pdf`, `.pptx`, capítulos, concat). Verificado leyendo el código, no solo la documentación: su
manejo de errores (línea ~499) es exactamente el "manejo de errores inventado por su cuenta" que T-05
quería evitar — `except Exception as excepcion: omitidas.append(SalidaOmitida(tipo, f"fallo al
generar: {excepcion}"))`, sin volcar ningún diagnóstico a disco ni pasar por el logger centralizado,
y mostrando al dueño el `repr` crudo de la excepción de Python en el `motivo` de la salida omitida en
vez de un mensaje accionable en español. Contradice dos reglas explícitas de §0.2 de
`HOJA_DE_RUTA.md` ("Logger centralizado — nunca dejar `print()` de depuración... los diagnósticos
por el logger" y "Errores accionables en español, nunca trazas crudas"). Para un formador en
solitario sin conocimientos técnicos, un fallo real durante una grabación (el propio bloqueo #7 de
`SEGUIMIENTO.md` §3, cuando por fin ocurra) dejaría hoy un mensaje como `fallo al generar:
KeyError('x')` sin ningún rastro recuperable para depurarlo después — exactamente el escenario que
T-05 se construyó para evitar. Mismo patrón de "infraestructura ya construida y probada, pero no
conectada a su consumidor real" que abrió R-12 a R-23.

**Requisitos:**
1. `scripts/monitorizacion.py::_volcar_diagnostico` se promueve a pública (`volcar_diagnostico`,
   mismo patrón de promoción de visibilidad que `tomas.toma_buena`/R-19 y
   `reproductor.anclar_indicaciones_a_bloques`/R-20: cambio de nombre/visibilidad, no de firma ni de
   ubicación, cero riesgo sobre su regla dura ya probada de nunca volcar variables locales).
2. `scripts/salidas.py::generar_salidas_seleccionadas` importa `logger.obtener_logger` y
   `monitorizacion.ruta_diagnostico`/`volcar_diagnostico` (ya construidas y probadas por T-02/T-05,
   sin reimplementar nada). En el `except Exception as excepcion` (requisito 3 de T-30, que no se
   toca: el alcance del `try`/`except` sigue siendo por tipo de salida, una salida rota nunca impide
   las demás), antes de construir la `SalidaOmitida`: vuelca el diagnóstico técnico completo a
   `<carpeta_salida>/diagnostico-<timestamp>.log` (`volcar_diagnostico`, reutilizada tal cual) y
   registra la excepción en el logger centralizado (`obtener_logger().error(...,
   exc_info=excepcion)`), exactamente igual que ya hace `ejecutar_con_diagnostico` para el fallo no
   controlado de su propio punto de entrada — la diferencia es que aquí NO se aborta el bucle ni se
   devuelve ningún código de salida, porque esta ruta sigue siendo una de varias salidas
   independientes entre sí.
3. El `motivo` de la `SalidaOmitida` deja de llevar `str(excepcion)` crudo (que puede ser una traza
   técnica en inglés, un nombre de variable interna o la ruta de un archivo del sistema) y pasa a ser
   un mensaje accionable en español que remite al archivo de diagnóstico recién escrito (p. ej.
   `f"fallo al generar: revisa el diagnóstico técnico en {ruta}"`), mismo criterio de "nunca trazas
   crudas" que ya aplica `ejecutar_con_diagnostico` al mensaje que muestra `presentacion.py`.
4. `obtener_logger()` nunca lanza ni necesita que `configurar_logger` se haya llamado antes en el
   mismo proceso (ya documentado así en `logger.py`: sin configurar, devuelve un logger sin
   manejadores) — esta tarea no exige cablear `configurar_logger` en ningún punto nuevo, solo dejar
   que el logger ya existente reciba el error cuando el proceso que lo invoque lo haya configurado.
5. `DEVELOPERS.md` (secciones "Monitorización de errores (T-05)" y "Selector de salidas por
   validación (T-30)") documenta que, desde esta tarea, un fallo real al generar una salida
   seleccionable deja constancia recuperable (`teleprompter.log` si el proceso configuró el logger,
   `diagnostico-<timestamp>.log` siempre) en vez de perderse solo en el texto libre de
   `SalidaOmitida.motivo`.
6. Fuera de alcance, explícito: no se diseña ningún `main()` de CLI nuevo ni se cablea
   `ejecutar_con_diagnostico` (pensada para abortar un proceso entero con código de salida, semántica
   que no encaja con "una salida rota nunca tumba las demás") — esta tarea conecta las piezas de
   T-02/T-05 que sí encajan (el volcado de diagnóstico y el logger), no todas.

**Criterio de aceptación:** test que fuerza (monkeypatch, mismo patrón que `test_salidas.py` ya usa
para forzar el fallo de validación de `concat-ffmpeg.txt` en R-21) una excepción dentro de una de las
ramas de `generar_salidas_seleccionadas` confirma que: (a) la salida rota queda `SalidaOmitida` con
un motivo en español que cita la ruta del diagnóstico, nunca el `repr`/mensaje crudo de la excepción;
(b) aparece un archivo `diagnostico-<timestamp>.log` en `carpeta_salida` con el traceback completo,
sin ninguna variable local del guion de entrada; (c) el logger centralizado registra la entrada de
error cuando el proceso ya lo configuró; (d) las demás salidas seleccionadas de la misma pasada se
generan con normalidad (regresión del requisito 3 de T-30, ya cubierta por tests existentes, debe
seguir en verde). Cuatro redes en verde.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
