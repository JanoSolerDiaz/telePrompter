# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-09-14 (ciclo de PM). §1 de `SEGUIMIENTO.md` (fuente autoritativa)
confirma que el Programador completó tanto **R-15** como **R-16** el 2026-09-14: la cola de este
documento, que llevaba desde el 2026-09-13 sin corregir pese a que siete reconfirmaciones sucesivas
del Programador ya lo habían señalado como prosa desactualizada, queda ahora al día. Las dos oleadas
entregadas (F-H y v6) se mueven a `ROADMAP_HISTORICO.md`. `auditoriacontinua.md` conserva un único
hallazgo `ABIERTO` sin enrutar todavía: `#19` (baja, invariantes/revalidación), abierto desde
2026-09-04 y reconfirmado sin cambios en las diez pasadas siguientes del auditor, siempre con la
misma nota: es una asimetría teórica en `_incidencias_anclas_desajustadas`
(`scripts/revalidacion.py`) sin escenario reproducido. Diez pasadas de reconfirmación sin que nadie
lo convierta en tarea es más que suficiente para que se pierda de vista; se abre **R-17** (fase
transversal **F-I** nueva) para cerrarlo formalmente, con el mismo criterio de deuda técnica menor
agrupada que ya usaron F-D/F-F/F-G/F-H. `roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo`
(bloqueo #7 de `SEGUIMIENTO.md` §3 — grabar un curso completo — sigue sin resolverse); sin feedback
real de rodaje, este ciclo no encuentra motivo para abrir ninguna R-XX de producto especulativa más
allá de R-17.

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

### Fase transversal F-I — Deuda técnica menor (revalidación)

Agrupa hallazgos de calidad menores, sin hito de producto propio, con el mismo criterio que ya
usaron F-D (R-08/R-09), F-F (R-11), F-G (R-14) y F-H (R-15). Contiene R-17, su única R-XX por
ahora.

#### R-17 — Endurecer o cerrar formalmente la asimetría teórica de `_incidencias_anclas_desajustadas`
**Oleada / Fase:** F-I · **Migración:** No · **Depende de:** ninguna
**Origen:** auditoría `#19` (2026-09-04), reconfirmada sin cambios en las diez pasadas siguientes del auditor

**Objetivo:** `_incidencias_anclas_desajustadas` (`scripts/revalidacion.py`, defensa en profundidad
de P-04 sobre el hallazgo #14) compara, escena a escena, el **conjunto** de índices de ancla
previstos contra los realmente leídos del documento (`previstas != escenas_leidas[numero_escena]`,
ambos `set[int]`). El hallazgo `#19` señala una asimetría teórica: esta comparación por conjunto
detecta un índice de más, de menos o distinto, pero nunca se ha verificado si existe algún camino
por el que dos disposiciones distintas de anclas pudieran producir el mismo conjunto de índices por
escena sin que el aviso salte — el propio auditor lleva diez pasadas (2026-09-04 a 2026-09-14)
reconfirmándolo como "sin escenario reproducido", nunca como un fallo real. Diez reconfirmaciones
sin resolución es ya más caro en atención de sesión futura que cerrarlo una vez, en cualquiera de
los dos sentidos posibles.

**Requisitos:**
1. Investigar, leyendo `identidad_por_ancla`/`texto_editado_por_ancla` y sus dos únicos
   productores (`tiempos.bloques_respiracion_marcados`, `troceo.trocear_guion`, ambos ya revisados
   por la auditoría de R-14), si existe una secuencia real de ediciones/particiones que produzca,
   para una misma escena, dos disposiciones de anclas distintas con el mismo conjunto de índices.
   No asumir la respuesta de partida en ningún sentido.
2. **Si se encuentra un escenario real:** endurecer la comparación para que compruebe la identidad
   exacta de cada ancla (no solo la cardinalidad/conjunto de índices por escena), añadiendo un test
   de regresión que reproduzca el escenario encontrado (falla sin el fix, pasa con él), mismo patrón
   que los tests de `#9`/`#14`.
3. **Si se confirma que es inalcanzable** dado el resto de invariantes del módulo (p. ej. porque la
   identidad `(escena, índice_original, mitad)` es inyectiva por construcción): añadir un test que
   deje esa prueba por escrito (no solo una nota en un docstring) y actualizar el registro de
   `auditoriacontinua.md` — a través del propio informe de esta tarea, nunca editando el documento
   del auditor directamente (§0.4: es el único archivo que modifica el auditor) — para que la
   siguiente pasada del auditor pueda cerrar `#19` a `RESUELTO` en vez de reconfirmarlo indefinidamente.
4. Cualquiera de los dos caminos es una tarea de calidad interna: cero cambio de esquema de
   `estado.json` ni de `Configuracion`, y ningún cambio de comportamiento observable por el dueño
   fuera de la propia corrección si el escenario resulta real.

**Criterio de aceptación:** la incertidumbre queda resuelta con evidencia en código (test nuevo) en
uno de los dos sentidos — comparación endurecida con regresión que la ejercita, o prueba explícita
de que el escenario es inalcanzable —, documentado en `DECISIONES_TECNICAS.md` con el razonamiento
seguido; la siguiente pasada del auditor puede cerrar `#19` sin tener que seguir reconfirmando la
misma nota teórica.

---

### Cola de producto

`ROADMAP_PRODUCTO.md` tiene una única R-XX pendiente en este ciclo: **R-17** (F-I), origen directo
de un hallazgo del auditor (`#19`) que llevaba diez pasadas sin convertirse en tarea. No hay
ninguna otra R-XX `PENDIENTE` ni `EN CURSO`: el resto del roadmap sigue a la espera de una entrada
real en `FEEDBACK.md`, de un nuevo hallazgo de `auditoriacontinua.md`, o de que el dueño complete el
criterio de salida de la oleada v1 (grabar un curso entero, bloqueo #7 de `SEGUIMIENTO.md` §3) y
aporte fricciones reales de rodaje.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
