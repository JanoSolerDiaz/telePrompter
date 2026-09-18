# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-09-18 (ciclo de PM). **Reconfirmación de cola vacía, sin R-XX
nueva.** Desde el ciclo anterior (2026-09-17, que archivó R-18/oleada v7 a `ROADMAP_HISTORICO.md`)
no hay ningún commit de código nuevo — solo diez reconfirmaciones sucesivas del Programador y una
auditoría en profundidad, ambas sin novedad (ver `SEGUIMIENTO.md`). Releído el registro de
hallazgos íntegro de `auditoriacontinua.md`: un único `ABIERTO` (`#24`, baja, de proceso), ya
enrutado correctamente a la pregunta #11 de §6 de `SEGUIMIENTO.md` — es una pregunta de gobernanza
sobre quién puede corregir la prosa de este documento, no un hallazgo de producto o arquitectura
que este roadmap deba convertir en R-XX. `roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo`.

Revisada de nuevo la arquitectura del encaje con el rodaje real y el montaje —`scripts/salidas.py`
(ya con R-18 integrada), `scripts/calibracion.py` y `scripts/tomas.py`— en busca de una grieta del
mismo tipo que motivó R-12 a R-18: sin encontrar ninguna. `salidas.py` reparte las cinco salidas de
forma independiente con las tomas reales ya conectadas; `calibracion.py` (R-04) sigue
deliberadamente fuera del selector automático, por diseño explícito de su propia ficha (una
propuesta de ppm que exige aceptación expresa del dueño en una pasada aparte, no un artefacto de
montaje que deba generarse solo); `tomas.py` ya rechaza con error el único dato corrupto conocido
(más de una toma `buena` por escena, R-11). **No se abre ninguna R-XX nueva en este ciclo** — el
bloqueo #7 de `SEGUIMIENTO.md` §3 (grabar un curso completo) sigue sin resolverse y sigue siendo la
única fuente de fricción real de rodaje capaz de motivar la siguiente mejora genuina, mismo
criterio ya razonado por los ciclos de PM del 2026-09-11, el 2026-09-15 y el 2026-09-17 en
`DECISIONES_TECNICAS.md`.

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

---

### Cola de producto

`ROADMAP_PRODUCTO.md` no tiene, en este ciclo, ninguna R-XX `PENDIENTE`. `auditoriacontinua.md` no
aporta ningún hallazgo nuevo que enrutar (único `ABIERTO`, `#24`, ya enrutado como pregunta de
gobernanza en §6 #11 de `SEGUIMIENTO.md`, ajena al contenido de este roadmap) y `roadmap/
FEEDBACK.md` sigue sin ninguna entrada `nuevo`. Revisada de nuevo la arquitectura del encaje con el
rodaje real y el montaje (`scripts/salidas.py`, `scripts/calibracion.py`, `scripts/tomas.py`,
`references/contrato-montaje.md`) en busca de una grieta del mismo tipo que motivó R-12 a R-18: no
se encuentra ninguna. Sin un hallazgo de auditoría, una entrada de feedback real o una grieta de
arquitectura verificada —los tres motivos legítimos de apertura de una R-XX ya establecidos por
ciclos anteriores (`DECISIONES_TECNICAS.md`, 2026-09-11 y 2026-09-15)—, abrir una R-XX especulativa
solo para no dejar la cola vacía iría contra el principio de producto de no diseñar sobre hipótesis
sin evidencia real de rodaje. El bloqueo #7 de `SEGUIMIENTO.md` §3 (grabar un curso completo) sigue
sin resolverse y sigue siendo la única fuente capaz de motivar la siguiente mejora genuina.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
