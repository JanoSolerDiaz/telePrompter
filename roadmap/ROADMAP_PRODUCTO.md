# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-10-07 (ciclo de PM). **R-24 (Oleada v12) está `COMPLETADA`** (§1 de
`SEGUIMIENTO.md`) desde el ciclo de Programador del 2026-10-07 que la implementó (diagnóstico real de
un fallo al generar una salida, en vez de la traza cruda de la excepción). Nueve reconfirmaciones del
Programador el mismo día la dejaron en este documento como `PENDIENTE` en vez de archivarla (mismo
patrón que el hallazgo `#24` de `auditoriacontinua.md`, pendiente de la respuesta del dueño a la
pregunta de gobernanza #11 de `SEGUIMIENTO.md` §6 sobre quién puede corregir esa prosa). Movida a
`roadmap/ROADMAP_HISTORICO.md` (Oleada v12) junto con el resto de oleadas 100 % entregadas.

**Se abre R-25** (Oleada v13): no por hallazgo de auditoría ni entrada de `FEEDBACK.md` — ninguna de
las dos fuentes aporta nada nuevo este ciclo (ver abajo) — sino por **grieta de arquitectura
verificada sobre código ya construido**, el mismo criterio que abrió R-12 a R-24. Verificación propia
más un subagente de exploración independiente, ambos leyendo el código línea a línea (no solo nombres
ni docstrings) antes de especificar la tarea, coinciden en que `scripts/convencion.py::
generar_convencion_guiones`/`guardar_convencion_guiones` (T-10, 2026-09-01) no tienen ningún
consumidor fuera de sus propios tests: `grep -rn "generar_convencion_guiones\|guardar_convencion_guiones"
scripts/*.py SKILL.md` no devuelve ningún resultado fuera de `scripts/convencion.py` y
`tests/test_convencion*.py`. La función genera, según su propio docstring, un documento de una
página pensado explícitamente para que el dueño lo "pegue en su plantilla de guiones" y así sus
futuros guiones ya nazcan sin desviaciones de la convención contractual — pero nunca se ofrece: no
está entre las seis salidas seleccionables de `scripts/salidas.py::TipoSalida` (T-30/R-18/R-19) ni
ningún paso del flujo documentado en `SKILL.md` le dice a Claude cuándo generarla. R-23 (2026-10-06)
acaba de hacer visibles las desviaciones de convención al pie de cada escena de `guion-escenas.md` y
en `tarjetas.json`; sin este documento conectado, el dueño ve la desviación pero no tiene a mano,
dentro del propio flujo de la skill, la herramienta que se la evitaría la próxima vez. Dos candidatas
alternativas quedaron descartadas tras la misma verificación, ambas documentadas en el detalle de
R-25: `scripts/calibracion.py::calcular_calibracion` (R-04) tiene la misma falta de gancho en
`SKILL.md`, pero conectarla de verdad exigiría descubrir "guiones hermanos" entre proyectos
distintos — pieza de arquitectura nueva que hoy no existe (§0.2: aislamiento por proyecto de guión) y
que no hace falta construir por adelantado mientras el bloqueo #7 de `SEGUIMIENTO.md` §3 (cero curso
grabado todavía) siga abierto; `scripts/reescrituras.py::revertir_reescrituras` (T-15, deshacer
global) también carece de disparador documentado, pero su valor es menor y revierte decisiones ya
tomadas del dueño, frente al beneficio inmediato y de bajo riesgo de entregar la convención. Detalle
completo en "Oleada v13" más abajo.

`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (única fila, plantilla vacía): no hay
historia de rodaje real que incorporar este ciclo — el bloqueo #7 de `SEGUIMIENTO.md` §3 (grabar un
curso completo) sigue abierto. El registro de hallazgos de `auditoriacontinua.md` no trae ningún
`ABIERTO` nuevo de producto/arquitectura esta pasada: quedan dos `ABIERTO`, ambos de proceso/entorno y
ya enrutados sin necesitar una R-XX — `#24` (baja, prosa de "Cola de producto" desactualizada entre
ciclos de PM) sigue pendiente de la respuesta del dueño a la pregunta de gobernanza #11 de
`SEGUIMIENTO.md` §6 (es la misma corrección de prosa que este propio ciclo acaba de aplicar de nuevo,
esta vez sobre R-24); `#28` (baja, el `pip` pelado de los contenedores de nube instala contra el
intérprete equivocado) ya tiene su recomendación de cierre aplicada por `P-06` (§5 de
`SEGUIMIENTO.md`, completada el mismo día que se abrió el hallazgo) — el cierre a `RESUELTO` en
`auditoriacontinua.md` queda para la siguiente pasada del auditor, que es quien escribe ese registro.

Este ciclo es de PM, no de Programador: no se ha ejecutado la verificación de las cuatro redes; la
spec de R-25 queda lista para que el siguiente ciclo de Programador la implemente y verifique.

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

### Oleada v13 — EN CURSO

#### R-25 — Entregar `convencion-guiones.md` de verdad al dueño: conectar `convencion.py` (T-10) al selector real de salidas (T-30)

**Migración:** No (aditiva: una séptima opción en el enum `TipoSalida` ya existente; ningún campo de
`estado.json` ni de `Configuracion` cambia) · **Depende de:** T-10, T-30 (ambas ya `COMPLETADA`) ·
**Origen:** observación de arquitectura del PM (2026-10-07) — grieta de arquitectura verificada
sobre código ya construido (mismo criterio que abrió R-12 a R-24), no hallazgo de auditoría ni
entrada de `FEEDBACK.md`.

**Objetivo:** `scripts/convencion.py::generar_convencion_guiones`/`guardar_convencion_guiones`
(T-10, 2026-09-01) generan un documento de una página — "Convención de guiones" — que, según su
propio docstring, está pensado explícitamente para que el dueño lo "pegue en su plantilla de guiones"
y así sus futuros guiones ya nazcan siguiendo la convención contractual (encabezado de escena,
rótulos de locución/no locución, numeración), en vez de inferirla y avisar de la desviación cada vez.
Verificado leyendo el código, no solo el docstring: `grep -rn
"generar_convencion_guiones\|guardar_convencion_guiones" scripts/*.py SKILL.md` no devuelve ningún
resultado fuera de `scripts/convencion.py` y sus propios tests — ningún script de producción la
importa, no está entre las seis opciones de `scripts/salidas.py::TipoSalida` (T-30/R-18/R-19) y
ningún paso del flujo documentado en `SKILL.md` le dice a Claude cuándo ofrecerla. R-23 (2026-10-06)
acaba de conectar `convencion.detectar_desviaciones` a sus dos consumidores reales (`guion-escenas.md`
y `tarjetas.json`), así que el dueño ya ve la desviación cuando ocurre; sin esta tarea, no tiene a
mano, dentro del propio flujo de la skill, el documento que se la evitaría la próxima vez — tendría
que saber que `convencion.py` existe y pedir explícitamente que se genere. Dos candidatas se
descartaron tras la misma verificación: `scripts/calibracion.py::calcular_calibracion` (R-04) tiene
la misma falta de gancho en `SKILL.md`, pero conectarla de verdad exigiría descubrir "guiones
hermanos" entre proyectos distintos — una pieza de arquitectura nueva (hoy todo opera aislado por
proyecto de guión, §0.2) para un escenario que el bloqueo #7 de `SEGUIMIENTO.md` §3 confirma que
todavía no se ha dado (cero curso grabado hasta hoy); se deja para cuando ese bloqueo se resuelva, en
vez de construir por adelantado. `scripts/reescrituras.py::revertir_reescrituras` (T-15, deshacer
global) también carece de disparador documentado, pero revierte decisiones ya tomadas por el dueño y
su valor es menor que el de prevenir una desviación futura con coste y riesgo mínimos.

**Requisitos:**
1. `TipoSalida` (`scripts/salidas.py`) gana una séptima opción, `CONVENCION_GUIONES`, al final del
   orden ya establecido en `construir_pregunta_salidas`/`_DESCRIPCIONES`/`ResumenSalidas` (mismo
   patrón que añadió `CAPITULOS_YOUTUBE` en R-18 y `CONCAT_FFMPEG` en R-19: nunca se reordenan las
   seis existentes).
2. `generar_salidas_seleccionadas` llama a `convencion.guardar_convencion_guiones(carpeta_salida,
   configuracion)` reutilizada tal cual (cero segunda implementación, cero cambio en
   `generar_convencion_guiones`/`guardar_convencion_guiones` en sí). A diferencia de las seis salidas
   actuales, esta no depende del parseo ni de la clasificación del guion de entrada — solo de
   `Configuracion` —, así que nunca puede quedar `SalidaOmitida` por un problema del guion; el único
   fallo posible es de escritura a disco, cubierto por el mismo patrón `except`/diagnóstico que ya
   protege a las demás salidas desde R-24.
3. A diferencia de las salidas condicionadas a tomas de rodaje (SRT alineado, capítulos, concat),
   `CONVENCION_GUIONES` se ofrece siempre en `construir_pregunta_salidas`, sin depender de
   `estado.salidas_generadas` ni de ningún parte de rodaje — no cambia de un guion a otro salvo que
   el dueño edite `Configuracion`, pero es el propio dueño quien decide cada vez si quiere
   regenerarla (p. ej. tras cambiar alguna clave de convención).
4. `references/contrato-montaje.md`, `DEVELOPERS.md` y `SKILL.md` documentan la nueva salida
   seleccionable, aclarando que complementa a R-23 (prevención de desviaciones futuras) en vez de
   sustituir su detección (desviaciones ya ocurridas en el guion actual).
5. Fuera de alcance, explícito: no se añade ninguna lógica nueva a
   `generar_convencion_guiones`/`guardar_convencion_guiones` (T-10 ya las especifica, genera y prueba
   correctamente); no se auto-genera sin que el dueño la seleccione, igual que las demás salidas.

**Criterio de aceptación:** test que confirma que seleccionar `CONVENCION_GUIONES` en
`generar_salidas_seleccionadas` escribe `convencion-guiones.md` en `carpeta_salida` con el mismo
contenido byte a byte que una llamada directa a `generar_convencion_guiones`; test que confirma que
se sigue ofreciendo en la pregunta de selección incluso sin ningún parte de rodaje ni toma marcada
(a diferencia de las salidas condicionadas); regresión de las seis salidas existentes sin cambios
(mismo patrón que R-18/R-19 ya verifican sobre los tres guiones reales). Cuatro redes en verde.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
