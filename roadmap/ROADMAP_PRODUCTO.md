# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-09-11 (ciclo de PM). **R-13 (oleada v5) y R-14 (fase transversal
F-G) quedaron COMPLETADA** el mismo día por el Programador que las implementó; ambas oleadas se
archivan enteras en `ROADMAP_HISTORICO.md` en este ciclo, tal como fija §0.4 de `HOJA_DE_RUTA.md`
(mover a histórico las oleadas 100 % entregadas). Con esto, **la cola de R-XX de este documento
queda vacía**: no hay ninguna R-XX `PENDIENTE` ni `EN CURSO` en §1 de `SEGUIMIENTO.md`. Revisión de
este ciclo antes de declarar la cola vacía: `auditoriacontinua.md` no tiene ningún hallazgo
`ABIERTO` de producto/arquitectura sin enrutar — de los 21 hallazgos registrados, 20 están
`RESUELTO` y el único que sigue `ABIERTO` (`#19`, baja, límite teórico y sin escenario reproducido
de `revalidacion.py`) tiene ya, desde el ciclo de PM del 2026-09-04, la decisión razonada de NO
abrir una R-XX especulativa mientras no se reproduzca un caso real (`DECISIONES_TECNICAS.md`,
reconfirmada por el auditor en cada pasada desde entonces sin cambios); este ciclo no encuentra
motivo para revisar esa decisión. `roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (bloqueo
#7 de `SEGUIMIENTO.md` §3 — grabar un curso completo — sigue sin resolverse, así que ni la
calibración de ppm de R-04 ni el ciclo de mejora de producto tienen todavía evidencia real de
rodaje). Este ciclo repasa además, con lectura directa del código ya entregado por R-13
(`scripts/pptx.py`, `references/contrato-tarjetas.md`), si queda alguna inconsistencia de
arquitectura del mismo tipo que ya motivó R-12/R-13/R-14: ninguna encontrada (el campo
`duracion_real_segundos` y el aviso `mezcla_duracion_real_y_estimada` de `tarjetas.json` son
coherentes entre el código y los dos documentos de contrato; la ausencia deliberada de un aviso
equivalente en `capitulos-youtube.txt` —texto público para YouTube, no JSON interno— ya está
razonada en `DECISIONES_TECNICAS.md` desde R-11, no es una discrepancia nueva). **No se abre
ninguna R-XX nueva en este ciclo**: no hay hallazgo de auditoría sin enrutar, no hay feedback real
de rodaje, y no se ha verificado ningún hueco de arquitectura nuevo — inventar una R-XX sin uno de
esos tres motivos violaría el propio criterio que ya aplicaron los ciclos de PM del 2026-09-02 y el
2026-09-04 ("no abrir ninguna R-XX especulativa... sin esa evidencia"). El próximo trabajo de
producto sale de la primera entrada real de `FEEDBACK.md`, de un hallazgo de auditoría nuevo, o de
que el dueño grabe el primer curso completo (bloqueo #7) y aporte fricciones reales de rodaje.

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

### Cola de producto — vacía en este ciclo

No hay ninguna R-XX `PENDIENTE` ni `EN CURSO` en `ROADMAP_PRODUCTO.md` a fecha de este ciclo (ver
nota de cabecera). Es un estado legítimo, no un vacío que rellenar por rellenar: el próximo trabajo
de producto sale de una entrada real en `FEEDBACK.md`, de un hallazgo de `auditoriacontinua.md` sin
enrutar, o de que el dueño complete el criterio de salida de la oleada v1 (grabar un curso entero,
bloqueo #7 de `SEGUIMIENTO.md` §3) y aporte fricciones reales de rodaje.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
