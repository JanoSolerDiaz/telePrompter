# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-09-09 (ciclo de PM). `auditoriacontinua.md` sigue sin ningún hallazgo `ABIERTO` de producto/arquitectura sin enrutar: `#19` (baja, límite teórico de `revalidacion.py`) sigue sin R-XX propia por lo ya razonado el 2026-09-04; `#20` (media, rutinas duplicadas) y `#21` (alta, investigado por el programador y confirmado falso positivo de clon superficial — ver `DECISIONES_TECNICAS.md` 2026-09-09) son ambos de infraestructura/cuenta del dueño, no de código ni de producto, y siguen correctamente enrutados en `SEGUIMIENTO.md` §3 bloqueo #8. `roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (bloqueo #7 — grabar un curso completo — sigue sin resolverse). **Cambio de este ciclo:** se abre **R-12**, primera tarea de la nueva **oleada v4**. Convierte en tarea la observación de arquitectura que el ciclo de PM del 2026-09-08 dejó registrada sin R-XX propia (las indicaciones `**EN PANTALLA**`/`**NOTA**` no llegan al reproductor interactivo): seis pasadas consecutivas de PM reafirmaron la política de no construir sin evidencia real de fricción, pero el hallazgo es un hueco de arquitectura ya verificado en el código (no una funcionalidad inventada), ataca directamente el segmento central del producto (guiones que mezclan locución con indicaciones de pantalla) y bloqueo #7 sigue sin fecha prevista de resolución. Se especifica con el requisito de legibilidad como límite explícito (principio de producto #5): cue subordinada, sin atajo nuevo, con caída explícita para no perder ninguna indicación — el riesgo que motivaba la cautela queda acotado en la propia ficha, no delegado a la implementación.

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

### Oleada v4 — Señalización de las indicaciones de pantalla en el reproductor

Todo lo entregado hasta ahora (v1 a F-F) resuelve la locución: el texto que hay que decir, cuándo y
a qué ritmo. Pero el segmento objetivo de este producto (§ Cliente objetivo) graba guiones que
**mezclan** locución con indicaciones de pantalla (`**EN PANTALLA**`, `**NOTA**`), y esas
indicaciones, aunque T-09 ya las clasifica con posición exacta, hoy solo llegan al locutor por el
`.pdf`/`guion-escenas.md` — nunca al propio reproductor, que es donde está mirando mientras graba.
Esta oleada cierra ese hueco. Contiene R-12, su única R-XX por ahora.

---

## DETALLE DE TAREAS R-XX

> Formato de cada R-XX (mismo rigor que una T-XX). Numeración secuencial, nunca reutilizada.
> Ninguna R-XX puede empezar antes de que la oleada v1 esté entregada, salvo que se diga lo
> contrario en su ficha.

### R-12 — Cue discreta de indicaciones EN PANTALLA/NOTA en el reproductor
**Oleada / Fase:** v4 · **Migración:** No · **Depende de:** T-09, T-11, T-19, T-21, T-23
**Origen:** observación de arquitectura del PM (ciclo 2026-09-08), convertida en tarea en este ciclo

**Objetivo:** hoy, `scripts/clasificador.py` (T-09) clasifica cada tramo de una escena como
`locucion` o `no_locucion` con `linea_inicio`/`linea_fin` exactos, y `scripts/documento_revision.py`
(T-16, `_indicaciones_no_recitables`/`formatear_indicaciones`) ya lista las indicaciones
`**EN PANTALLA**`/`**NOTA**` al pie de cada escena en `guion-escenas.md`. Pero esa información nunca
llega a `scripts/reproductor.py`: el JSON que embebe en el `.html` solo lleva escenas → bloques de
locución (T-18/T-19). Para un guion que mezcla locución con instrucciones de pantalla —el caso
central de este producto (§ Cliente objetivo)— eso significa que durante la grabación, en pantalla
completa, no hay ninguna señal de cuándo cambiar de aplicación, diapositiva o encuadre: hay que
memorizarlo de antemano o consultar el `.pdf` aparte, rompiendo el propio motivo de ser de un
teleprompter. El objetivo es cerrar ese hueco sin inventar clasificación nueva (reutiliza
`linea_inicio`/`linea_fin` ya calculados) y sin que la cue compita nunca con la legibilidad del
bloque de locución activo (principio de producto #5, límite explícito de esta ficha, no una
sugerencia).

**Requisitos:**
1. `scripts/reproductor.py` (`_construir_datos` o equivalente) incorpora, para cada bloque de
   respiración (T-11) de una escena, las indicaciones `no_locucion` cuya `linea_inicio` cae
   inmediatamente después de la `linea_fin` de ese bloque y antes de la `linea_inicio` del
   siguiente bloque de locución de la misma escena — es decir, se ancla la indicación al bloque de
   locución que la PRECEDE en el guion de origen, para que el locutor la vea con margen antes de
   tener que actuar, mientras aún está recitando la línea anterior. Sin lógica de clasificación
   nueva: solo reutiliza el resultado ya calculado por T-09/T-11.
2. El reproductor muestra esa indicación como una cue discreta y subordinada: tipografía más
   pequeña que el bloque activo, nunca el mismo tamaño ni contraste — el bloque de locución activo
   sigue siendo, en todo momento, el elemento dominante de la pantalla. Visible mientras el bloque
   de respiración al que está anclada está activo; se oculta al avanzar al siguiente bloque de
   locución.
3. La cue se pliega en el mismo grupo de indicadores que ya oculta la tecla `H` (T-23,
   `indicadores-ocultos` en `guion.js`) — no añade atajo nuevo ni preferencia de configuración
   aparte; reutiliza el mecanismo ya entregado y ya persistido (T-26).
4. Ninguna indicación se pierde en silencio (invariante (a) de §0.2, extendido de "el parser no
   descarta texto" a "el reproductor no descarta ninguna cue que el parser sí clasificó"): si una
   indicación no tiene bloque de locución posterior en la misma escena (es la última de la escena),
   se ancla al último bloque de respiración de esa escena en vez de quedar sin mostrar.
5. `guion-escenas.md` (T-16) no cambia de formato: las indicaciones siguen listadas al pie tal
   como hoy, como referencia de revisión de una sola pasada (principio de producto #2). Este
   requisito es exclusivamente del reproductor interactivo.
6. Distingue `**EN PANTALLA**` de `**NOTA**` con un prefijo textual mínimo (p. ej. «Pantalla:» /
   «Nota:»), sin iconografía gráfica ni recursos adicionales que arriesguen la auto-contención del
   `.html` (principio de producto #4) ni la legibilidad a distancia de cámara (principio #5).

**Criterio de aceptación:** en un guion con al menos una indicación `EN PANTALLA` o `NOTA` (los tres
guiones reales de `fixtures/reales/` sirven de fixture), el reproductor generado muestra el texto de
cada indicación anclado al bloque de respiración correcto, sin que el locutor tenga que abrir el
`.pdf` ni memorizarla de antemano; el bloque activo de locución sigue siendo en todo momento el
elemento visualmente dominante (verificable por contraste/tamaño, igual que T-21 verifica el
contraste AAA del bloque activo); ocultar indicadores con `H` también oculta la cue; ninguna de las
indicaciones que hoy lista `guion-escenas.md` al pie de cada escena deja de aparecer en el
reproductor; cero indicaciones nuevas o recalculadas respecto a lo que T-09 ya clasificaba —
únicamente se muestra lo que ya existía, donde antes no se mostraba.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`.)*
