# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-09-10 (ciclo de PM). **R-12 (oleada v4) quedó COMPLETADA** el mismo
día por el ciclo de Programador que la implementó; se archiva entera en `ROADMAP_HISTORICO.md` en
este ciclo, tal como fija §0.4 de `HOJA_DE_RUTA.md` (mover a histórico las oleadas 100 % entregadas).
`auditoriacontinua.md` sigue sin ningún hallazgo `ABIERTO` de producto/arquitectura sin enrutar:
`#19` (baja, límite teórico de `revalidacion.py`) sigue sin R-XX propia por lo ya razonado el
2026-09-04 (sin escenario reproducido, mismo criterio reconfirmado por el auditor el 2026-09-10);
`#20` (media, ASUMIDO) es infraestructura/cuenta del dueño, correctamente enrutada en
`SEGUIMIENTO.md` §3 bloqueo #8. `roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (bloqueo #7
— grabar un curso completo — sigue sin resolverse, así que la calibración de ppm de R-04 y el propio
ciclo de mejora de producto siguen sin evidencia de rodaje real). **Cambios de este ciclo:** se
abren **R-13** (oleada v5) y **R-14** (fase transversal F-G). Ninguna de las dos es una
funcionalidad especulativa: ambas parten de un hueco ya verificado en el código, siguiendo el mismo
criterio que ya justificó R-12 (no construir sin evidencia real de fricción, salvo que el hallazgo
sea arquitectura confirmada, no una idea nueva). **R-13** — leyendo `references/contrato-montaje.md`
junto con `scripts/pptx.py`, `scripts/capitulos_youtube.py` y `scripts/srt_alineado.py` — encuentra
que `tarjetas.json` (uno de los dos "CONTRATO DE MONTAJE" documentados) es el único de los tres
consumidores de `tomas.duracion_toma_buena` que NO la usa: sigue exponiendo solo la duración
**estimada** por escena, mientras que `guion-alineado.srt` (R-05) y los capítulos de YouTube (R-07)
ya prefieren la duración **real** de la toma buena cuando existe, con el mismo patrón de aviso
explícito si se mezclan escenas con y sin toma real. Consecuencia directa: la fórmula de
`contrato-montaje.md` para derivar el rango de tiempo de cada escena a partir de `tarjetas.json` solo
es coherente con `guion.srt` (estimado), nunca con `guion-alineado.srt` (real) una vez el dueño tiene
partes de rodaje — justo el caso que más importa según se acumulen tomas reales. **R-14** promueve a
tarea el hallazgo cosmético que la propia sesión de R-12 (2026-09-10) dejó documentado como
observación no urgente: un separador de escena `---` puede colarse al final del texto de una
indicación `EN PANTALLA`/`NOTA` en tres salidas (`guion-escenas.md`, `tarjetas.json` y ahora también
la cue del reproductor), porque las tres reutilizan el mismo `bloque.contenido` sin filtrar de
`scripts/clasificador.py`. Es deuda técnica menor, no producto nuevo — mismo criterio que ya agrupó
`R-08` (deuda técnica) y `R-11` (robustez de datos de rodaje) como fases transversales en vez de
diluirlas en tres R-XX triviales.

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

### Oleada v5 — Coherencia de datos derivados para el montaje real

Cierra un hueco de coherencia entre las dos salidas que `references/contrato-montaje.md` documenta
como "CONTRATO DE MONTAJE" (`guion.srt`/`guion-alineado.srt` y `tarjetas.json`): cuando existe un
parte de rodaje con toma buena, el `.srt` alineado (R-05) y los capítulos de YouTube (R-07) ya usan
la duración real de la escena; `tarjetas.json` todavía no, así que la fórmula de derivación de
rango que el propio contrato enseña a la fase de montaje deja de ser fiable justo cuando hay
grabación real que aprovechar. Contiene R-13, su única R-XX por ahora.

### Fase transversal F-G — Deuda técnica menor

Agrupa hallazgos de calidad menores, sin hito de producto propio, con el mismo criterio que ya usaron
F-D (R-08/R-09) y F-F (R-11): correcciones acotadas y ya verificadas en el código, no ideas nuevas.
Contiene R-14, su única R-XX por ahora.

---

## DETALLE DE TAREAS R-XX

> Formato de cada R-XX (mismo rigor que una T-XX). Numeración secuencial, nunca reutilizada.
> Ninguna R-XX puede empezar antes de que la oleada v1 esté entregada, salvo que se diga lo
> contrario en su ficha.

### R-13 — Duración real por escena en `tarjetas.json`, coherente con `guion-alineado.srt`
**Oleada / Fase:** v5 · **Migración:** No · **Depende de:** T-12, T-29, R-02, R-04, R-05
**Origen:** observación de arquitectura del PM (2026-09-10), verificada contra `references/contrato-montaje.md`, `scripts/pptx.py`, `scripts/capitulos_youtube.py` y `scripts/srt_alineado.py`

**Objetivo:** `references/contrato-montaje.md` documenta dos "CONTRATO DE MONTAJE":
`guion.srt`/`guion-alineado.srt` y `tarjetas.json`. Desde R-05 y R-07, tanto `srt_alineado.py` como
`capitulos_youtube.py` prefieren la duración **real** de la toma buena de una escena
(`tomas.duracion_toma_buena`) sobre la **estimada** (T-12) cuando existe parte de rodaje, avisando
explícitamente si el conjunto mezcla escenas con y sin toma real (requisito 2 de R-07). `pptx.py`
(T-29, `tarjetas.json`) es el único de los tres consumidores de `duracion_toma_buena` que no lo
hace: expone solo `duracion_estimada_segundos`. La propia `contrato-montaje.md` enseña a la fase de
montaje a derivar el rango `[inicio_escena, fin_escena)` de cada escena sumando
`duracion_estimada_segundos` — una fórmula que solo es coherente con `guion.srt` (estimado). En
cuanto el dueño graba tomas reales y genera `guion-alineado.srt`, esa misma fórmula deja de
coincidir con los límites de escena reales, y la cadena de montaje no tiene en `tarjetas.json` ningún
campo con el que recalcularlos: tiene que adivinar o reimplementar por su cuenta la misma lógica que
`srt_alineado.py` ya resolvió, justo lo que el contrato dice que no debe hacer.

**Requisitos:**
1. `tarjetas.json` (`scripts/pptx.py`) incorpora, por escena, un campo de duración real (p. ej.
   `duracion_real_segundos`, `null`/ausente si la escena no tiene toma buena) usando
   `tomas.duracion_toma_buena` — mismo dato que ya calculan `srt_alineado.py` y
   `capitulos_youtube.py`. Si conviene extraer la selección real/estimado a una función compartida
   para no triplicar la lógica, es una decisión técnica del programador (a registrar en
   `DECISIONES_TECNICAS.md`), no un requisito de esta ficha.
2. `duracion_estimada_segundos` no se toca ni se sustituye: sigue siendo la única fuente para
   `guion.srt` (T-27) y `guion-escenas.md`. El campo de duración real es un dato **adicional**,
   nunca una sustitución en silencio del existente.
3. `tarjetas.json` señala si el conjunto de escenas mezcla duración real y estimada (mismo aviso
   que ya resuelve R-07 para los capítulos de YouTube, requisito 2), para que la fase de montaje
   sepa antes de fiarse del campo si hay huecos.
4. `references/contrato-montaje.md` y `references/contrato-tarjetas.md` se actualizan con la
   fórmula correcta de derivación de rango cuando existe `guion-alineado.srt`: duración real si está
   presente, estimada si no — coherente con la propia sección "Qué puede y qué NO puede asumir el
   montaje" que ya existe para el `.srt`.
5. Sin migración de `estado.json`: el dato de origen ya vive en `estado.json["tomas"]`;
   `tarjetas.json` es una salida derivada que se regenera en cada validación (T-30).
6. Test de integración que cruza `tarjetas.json` y `guion-alineado.srt` sobre un guion con al menos
   una toma buena registrada (mismo patrón que
   `test_srt_alineado_y_capitulos_youtube_son_coherentes_entre_si`, R-11 / hallazgo #18): la
   coherencia queda probada, no solo documentada.

**Criterio de aceptación:** sobre un guion con al menos una escena con toma buena registrada,
`tarjetas.json` trae el campo de duración real para esa escena y ausente/`null` para las que no la
tienen; sumando esas duraciones (real cuando existe, estimada si no) se reconstruyen exactamente los
límites de escena de `guion-alineado.srt`; sobre un guion sin ninguna toma buena registrada,
`tarjetas.json` y la fórmula de derivación de rango se comportan exactamente igual que hoy, sin
regresión sobre los tres guiones reales de `fixtures/reales/`.

### R-14 — El separador de escena no debe colarse en el texto de una indicación
**Oleada / Fase:** F-G · **Migración:** No · **Depende de:** T-09
**Origen:** observación de arquitectura de R-12 (2026-09-10), registrada como hallazgo cosmético no urgente en `HISTORIAL_SESIONES.md` y `SEGUIMIENTO.md`, promovida a R-XX en este ciclo por afectar tres salidas y estar ya localizada en código

**Objetivo:** `scripts/clasificador.py` (T-09) incluye, dentro del `contenido` de la última sección
`no_locucion` de una escena, el separador `---` que el guion de origen usa entre escenas
(`references/convencion-guion.md`) cuando esa sección es la última antes del siguiente
`## BLOQUE N`. Ese `contenido` se reutiliza sin filtrar en `documento_revision.py` (T-16, pie de
escena), `pptx.py` (T-29, `tarjetas.json`) y, desde R-12, en la cue del reproductor: en las tres
salidas, el separador aparece pegado al final del texto mostrado como indicación `EN
PANTALLA`/`NOTA`. Es un defecto de presentación, no de datos: no pierde texto ni compromete la
cobertura total del guion (invariante (a)), pero se repite ya en tres salidas distintas, lo que
justifica corregirlo en el origen (`clasificador.py`) en vez de parchearlo tres veces en cada
consumidor.

**Requisitos:**
1. `clasificador.py` deja de incluir la línea de separador de escena (`---` u otro marcador de fin
   de escena que documente `references/convencion-guion.md`) dentro del `contenido` mostrado de la
   sección `no_locucion` que la precede — sin perder cobertura total: la línea del separador sigue
   contabilizada por el propio parser (T-08) como parte del límite entre escenas, nunca descartada
   en silencio (invariante (a)).
2. `clasificador.reconstruir()` sigue reconstruyendo el guion de origen sin pérdida byte a byte tras
   el cambio: el test de reconstrucción existente (T-09) se extiende con un caso que cubra
   explícitamente una escena que termina en indicación seguida de separador.
3. `guion-escenas.md`, `tarjetas.json` y la cue del reproductor (R-12) dejan de mostrar el `---`
   pegado al texto de la indicación, verificado sobre los tres guiones reales de
   `fixtures/reales/` (el separador aparece entre `BLOQUE N` y `BLOQUE N+1` en los tres).
4. Sin cambio de esquema de `estado.json` (no aplica migración): es una corrección de clasificación
   sobre datos derivados, no sobre datos persistidos.

**Criterio de aceptación:** sobre los tres guiones reales, ninguna indicación no-locución mostrada
en `guion-escenas.md`, `tarjetas.json` o el reproductor generado termina en `---`; el test de
cobertura total (reconstrucción, T-09) sigue en verde; cero regresión en la suite de tests existente.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`.)*
