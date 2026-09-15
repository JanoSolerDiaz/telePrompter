# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-09-15 (ciclo de PM). §1 de `SEGUIMIENTO.md` (fuente autoritativa)
confirma que el Programador completó **R-17** el mismo día en que se abrió (2026-09-14) y encadenó
nueve pasadas de reconfirmación sin ningún trabajo de código pendiente: la cola de este documento
llevaba desde entonces listando R-17 como pendiente pese a estar ya `COMPLETADA`, prosa
desactualizada del mismo tipo que ya había señalado el propio Programador en siete
reconfirmaciones antes de la corrección del 2026-09-14. Se corrige aquí y la fase transversal F-I
se mueve a `ROADMAP_HISTORICO.md`, mismo criterio que F-D/F-E/F-F/F-G/F-H. `auditoriacontinua.md`
(registro de hallazgos íntegro releído en este ciclo) no conserva ningún hallazgo `ABIERTO`
pendiente de enrutar: el único que quedaba, `#19`, sigue formalmente `ABIERTO` en el registro del
auditor a la espera de que su propia siguiente pasada lo cierre a `RESUELTO` (solo el auditor
edita ese documento, §0.4), pero ya tiene R-17 asignada y entregada — no requiere ninguna R-XX
nueva. `roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (bloqueo #7 de `SEGUIMIENTO.md` §3
— grabar un curso completo — sigue sin resolverse, es la fuente de fricciones reales de rodaje que
más haría avanzar este roadmap). Revisados también `references/contrato-montaje.md` y
`references/contrato-tarjetas.md` en busca de otra grieta de arquitectura del mismo tipo que abrió
R-12/R-13/R-14/R-16: el contrato de montaje queda cerrado por R-16 (límites absolutos de escena ya
resueltos, nada que un consumidor externo deba recalcular a mano). Sin feedback real de rodaje ni
hallazgo nuevo, este ciclo no encuentra motivo para abrir ninguna R-XX de producto especulativa.

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

---

### Cola de producto

`ROADMAP_PRODUCTO.md` no tiene, en este ciclo, ninguna R-XX `PENDIENTE` ni `EN CURSO`: la última,
R-17, quedó `COMPLETADA` el 2026-09-14 y se archiva arriba. `roadmap/FEEDBACK.md` no tiene ninguna
entrada `nuevo` y el registro de hallazgos de `auditoriacontinua.md` no tiene ningún `ABIERTO`
pendiente de enrutar (el único que quedaba, `#19`, ya tiene R-17 asignada y entregada; su cierre a
`RESUELTO` en el registro del auditor es tarea exclusiva del auditor, §0.4). El roadmap sigue a la
espera de una entrada real en `FEEDBACK.md`, de un nuevo hallazgo de `auditoriacontinua.md`, o de
que el dueño complete el criterio de salida de la oleada v1 (grabar un curso entero, bloqueo #7 de
`SEGUIMIENTO.md` §3) y aporte fricciones reales de rodaje — la fuente de valor más alta para las
próximas R-XX, y la que este roadmap lleva más tiempo sin poder aprovechar. Sin ese input, este
ciclo no abre ninguna R-XX de producto especulativa: revisados `references/contrato-montaje.md` y
`references/contrato-tarjetas.md` en busca de otra grieta de arquitectura del mismo tipo que ya dio
R-12/R-13/R-14/R-16, no aparece ninguna pendiente — el contrato con la fase de montaje queda
cerrado desde R-16.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
