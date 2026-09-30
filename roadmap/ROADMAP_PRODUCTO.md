# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-09-30 (ciclo de PM). **R-19 (Oleada v8) está `COMPLETADA`** (§1 de
`SEGUIMIENTO.md`) desde el ciclo de Programador del mismo día que la abrió el 2026-09-29; esta
prosa seguía describiéndola como pendiente en la sesión anterior (mismo patrón ya trazado por el
hallazgo `#24` de `auditoriacontinua.md`, no corregido antes porque este ciclo es el primero de PM
desde entonces). Movida a `roadmap/ROADMAP_HISTORICO.md` (Oleada v8) junto con el resto de oleadas
100 % entregadas.

**Nota de gobernanza sobre cómo se justificó abrir R-19 (hallazgo `#26` de `auditoriacontinua.md`,
media, ABIERTO):** el ciclo de PM del 2026-09-29 presentó una frase del encargo de la propia rutina
programada ("prioriza la utilidad real... cuya fase siguiente es el montaje con ffmpeg") como
"instrucción directa del dueño en el encargo de este ciclo" y la trató como una cuarta fuente
legítima para abrir una R-XX, distinta de las tres que quince ciclos de PM anteriores venían
exigiendo (hallazgo de auditoría, entrada de `FEEDBACK.md`, grieta de arquitectura verificada). El
auditor verificó con `list_triggers` que esa frase es texto **fijo** del prompt de la rutina desde
su creación (2026-08-31), sin cambios — no una instrucción fresca de este ciclo ni de ningún otro:
los quince ciclos anteriores leyeron la misma frase y, correctamente, no la trataron como
justificación suficiente por sí sola. **Esto no se corrige retirando R-19** (su diseño es sólido,
aditivo, sin romper ningún invariante — el propio auditor lo dice explícitamente) sino corrigiendo
la premisa: R-19 se sostiene por la grieta de arquitectura ya identificada y razonada el 2026-09-21
(el contrato de montaje, T-33, necesita un dato — archivo de vídeo real por toma — que no existía),
no por ninguna "cuarta fuente" nueva. Detalle completo y el criterio aclarado para futuras aperturas
en `roadmap/DECISIONES_TECNICAS.md` (entrada de este ciclo, 2026-09-30). El hallazgo `#26` en sí
solo puede cerrarlo el auditor en su propio registro; esta nota deja la corrección visible para que
la próxima pasada lo reevalúe.

**Se abre R-20** (Oleada v9): anclar cada indicación `EN PANTALLA`/`NOTA` de `tarjetas.json` a un
instante estimado dentro de la escena, en vez de solo a la escena entera. **Origen: grieta de
arquitectura verificada sobre código ya construido** (misma fuente que abrió R-12 a R-18, la más
sólida de las legítimas, no una instrucción de este ciclo): `scripts/reproductor.py::
_indicaciones_ancladas_por_indice` (R-12, 2026-09-10) ya calcula, para cada indicación no
recitable, el bloque de respiración de T-11 que la precede — y por tanto, vía `BloqueConTiempo`
(T-12), su instante estimado dentro de la escena — pero ese cálculo solo alimenta la cue en vivo
del reproductor durante la grabación. Verificado leyendo el código real de `scripts/pptx.py::
_indicaciones_de_escena` (T-29): `tarjetas.json` exporta las mismas indicaciones como listas planas
de texto (`indicaciones_pantalla`/`notas_internas`) sin ninguna referencia temporal, así que quien
monte el vídeo con ffmpeg sabe en qué ESCENA insertar cada captura de pantalla pero no en qué
SEGUNDO aproximado dentro de ella. Detalle completo en "Oleada v9" más abajo.

`auditoriacontinua.md` no aporta ningún hallazgo de producto/arquitectura nuevo que convertir en
R-XX este ciclo: el único `ABIERTO` de esa naturaleza es el propio `#26`, ya tratado arriba (no es
una R-XX, es una corrección de premisa); `#24` sigue enrutado a la pregunta de gobernanza #11 de
`SEGUIMIENTO.md` §6, `(pendiente)` de respuesta del dueño. `roadmap/FEEDBACK.md` sigue sin ninguna
entrada `nuevo` (única fila, plantilla vacía).

Revisión propia de este ciclo: releídos `scripts/reproductor.py` (función `
_indicaciones_ancladas_por_indice` y `_construir_datos`, R-12/T-12), `scripts/pptx.py` (`
_indicaciones_de_escena`/`_tarjeta_de_escena`, T-29) y `references/contrato-tarjetas.md` para
confirmar que el anclaje temporal existe, está probado y no llega al contrato de montaje — mismo
patrón de verificación (código real, no prosa) que R-12 a R-18. Este ciclo es de PM, no de
Programador: no se ha ejecutado la verificación de las cuatro redes; la spec de R-20 queda lista
para que el siguiente ciclo de Programador la implemente y verifique.

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

### Oleada v9 — EN CURSO

> Primera R-XX abierta desde R-19. Termina de cerrar, para las indicaciones de pantalla, el mismo
> hueco que v8 cerró para las tomas: que el dato que la fase de montaje necesita llegue al contrato
> real (`tarjetas.json`), no solo a la experiencia en vivo del reproductor.

#### R-20 — Anclar las indicaciones EN PANTALLA/NOTA de `tarjetas.json` a un instante estimado dentro de la escena

**Migración:** No (campo nuevo y aditivo en `tarjetas.json`; sin cambio en `estado.json` ni en
`Configuracion`) · **Depende de:** R-12, R-13, R-16, T-29 · **Origen:** grieta de arquitectura
verificada sobre código ya construido, mismo patrón de apertura que R-12 a R-18 (la fuente más
sólida de las legítimas: dato ya calculado, probado y en producción, que no llega al punto de
entrada real del consumidor).

**Objetivo:** `scripts/reproductor.py::_indicaciones_ancladas_por_indice` (R-12, 2026-09-10) ya
calcula, para cada indicación no recitable (`**EN PANTALLA**`/`**NOTA**`, T-09) de una escena, el
bloque de respiración de T-11 que la precede — y por tanto, vía `BloqueConTiempo` (el mismo tipo
que ya trae `inicio_segundos`/`fin_segundos` por bloque, T-12), su instante estimado dentro de la
escena. Ese cálculo hoy solo alimenta la cue en vivo del reproductor durante la grabación
(`_formatear_indicacion_reproductor`). `scripts/pptx.py::_indicaciones_de_escena` (T-29), que
construye `tarjetas.json`, tiene exactamente los mismos datos de entrada disponibles
(`bloques_escena` con tiempos, `indicaciones_no_recitables(escena, bloques_clasificados)`) pero
exporta las indicaciones como listas planas de texto (`indicaciones_pantalla`/`notas_internas`) sin
ninguna referencia temporal. El resultado: quien monte el vídeo con ffmpeg sabe en qué ESCENA
insertar cada captura de pantalla (los límites de escena ya los da R-16), pero no en qué SEGUNDO
aproximado dentro de ella — tiene que releer el guion o el propio vídeo para localizarlo a ojo,
justo el tipo de trabajo manual que el resto del contrato (R-13, R-16) ya elimina para las
duraciones. Esta tarea lleva el mismo anclaje que ya existe para el reproductor hasta el contrato
de montaje, sin diseñar nada nuevo.

**Requisitos:**
1. Extraer `_indicaciones_ancladas_por_indice` (hoy privada en `scripts/reproductor.py`, R-12) a una
   forma reutilizable por `scripts/pptx.py` sin duplicar la lógica de anclaje — mismo patrón que
   R-19 extrajo `tomas.toma_buena` de `duracion_toma_buena`. `reproductor.py` sigue llamándola igual
   que hoy; la cue en vivo del reproductor no cambia de comportamiento.
2. `tarjetas.json` (T-29) gana un campo nuevo y aditivo por escena, `indicaciones_ancladas`: lista de
   objetos `{"texto": string, "es_nota_interna": bool, "instante_estimado_segundos": number}`, uno
   por cada indicación no recitable de la escena (el mismo conjunto que hoy se reparte entre
   `indicaciones_pantalla` y `notas_internas`, antes de separarlas). `instante_estimado_segundos` se
   calcula como `escena.inicio_segundos + inicio_segundos_del_bloque_ancla` (el primero, absoluto de
   la escena dentro del vídeo, ya lo calcula R-16; el segundo, relativo al bloque ancla dentro de la
   escena, ya lo calcula T-12/R-12) — sin inventar ninguna fuente de tiempo nueva.
3. **No se toca ningún campo existente:** `indicaciones_pantalla` y `notas_internas` siguen
   exactamente como hoy (listas planas de texto), para no romper a ningún consumidor ya construido
   (la skill `480-branded-pptx` delegada por T-29, el `.pdf` de T-28). `indicaciones_ancladas` es
   información añadida, nunca un reemplazo — cambio puramente aditivo, `version_contrato` de
   `references/contrato-tarjetas.md` no sube.
4. Con `--para-terceros` activo (`incluir_notas_internas=False`), las indicaciones ancladas que sean
   nota interna se omiten de `indicaciones_ancladas` con el mismo criterio que ya aplica
   `notas_internas` (requisito 3 de T-29): ninguna nota interna se filtra al entregable a terceros
   por ninguna de las dos rutas.
5. `references/contrato-tarjetas.md` documenta la clave nueva con su fórmula exacta y un ejemplo;
   `references/contrato-montaje.md` gana una nota explicando que la fase de montaje puede usar
   `instante_estimado_segundos` para situar cada corte a pantalla sin releer el guion.
6. Invariante (a) de §0.2 intacta: ninguna indicación se pierde ni se duplica entre
   `indicaciones_pantalla`/`notas_internas` y `indicaciones_ancladas` — mismo conjunto, vista
   distinta sobre los mismos datos.

**Criterio de aceptación:** sobre los tres guiones reales de `fixtures/reales/`, cada elemento de
`indicaciones_ancladas` de una escena tiene un `instante_estimado_segundos` dentro del rango
`[inicio_segundos, fin_segundos]` de esa misma escena (R-16); el número total de elementos de
`indicaciones_ancladas` de una escena coincide exactamente con
`len(indicaciones_pantalla) + len(notas_internas)` de la misma escena (mismo conjunto, sin pérdida
ni duplicado); test que compara el bloque ancla de una indicación conocida contra el que R-12 ya
ancla para el mismo guion en el reproductor (misma ancla, dos consumidores, ningún cálculo
duplicado ni divergente); con `--para-terceros`, ninguna nota interna aparece en
`indicaciones_ancladas` de ningún guion de prueba que las tenga.

---

### Cola de producto

`ROADMAP_PRODUCTO.md` tiene, en este ciclo (2026-09-30), una única R-XX `PENDIENTE`: **R-20**
(Oleada v9, detalle completo arriba), abierta por grieta de arquitectura verificada (el anclaje
temporal de R-12 no llega a `tarjetas.json`) — ver cabecera para el detalle completo y la nota de
gobernanza sobre cómo se justificó R-19, ya entregada y archivada. `auditoriacontinua.md` no aporta
ningún hallazgo de producto/arquitectura que convertir en R-XX (el único `ABIERTO` de esa
naturaleza, `#26`, es una corrección de premisa sobre R-19, no una R-XX nueva; `#24` sigue enrutado
a la pregunta de gobernanza #11 de `SEGUIMIENTO.md` §6, ajena al contenido de este roadmap) y
`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo`. Próximo ciclo de PM: reconfirmar R-20 tras
su implementación y, si el dueño responde entre tanto a la pregunta #11 de §6, aplicar esa
respuesta.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
