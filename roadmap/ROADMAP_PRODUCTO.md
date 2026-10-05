# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-10-05 (ciclo de PM). **R-22 (Oleada v10) está `COMPLETADA`** (§1 de
`SEGUIMIENTO.md`) desde el ciclo de Programador del 2026-10-05 que la implementó (`capitulos-ffmpeg.txt`,
formato `FFMETADATA1`). Nueve reconfirmaciones del Programador el mismo día la dejaron en este
documento como "EN CURSO"/`PENDIENTE` en vez de archivarla (mismo patrón que el hallazgo `#24` de
`auditoriacontinua.md`, pendiente de la respuesta del dueño a la pregunta de gobernanza #11 de
`SEGUIMIENTO.md` §6 sobre quién puede corregir esa prosa). Movida a `roadmap/ROADMAP_HISTORICO.md`
(Oleada v10) junto con el resto de oleadas 100 % entregadas.

**Se abre R-23** (Oleada v11): no por hallazgo de auditoría ni entrada de `FEEDBACK.md` — ninguna de
las dos fuentes aporta nada nuevo este ciclo (ver abajo) — sino por **grieta de arquitectura
verificada sobre código ya construido**, el mismo criterio que abrió R-12 a R-22. `scripts/
convencion.py::detectar_desviaciones` (T-10, ampliada en T-33 con `numero_escena_duplicado`/
`numero_escena_no_creciente`) calcula, correctamente y con tests, las desviaciones de la convención
de marcado que más le importan a la cadena de montaje — pero verificado leyendo el código (no solo
la documentación), **no se llama desde ningún punto de la generación real**: ni
`scripts/documento_revision.py` (el `guion-escenas.md` que el dueño de verdad revisa) ni
`scripts/pptx.py` (`tarjetas.json`, el contrato de montaje) la invocan; solo la ejercitan sus propios
tests. `references/contrato-montaje.md` le dice hoy a la cadena de montaje que la numeración de
escena "ya NO se da por supuesta en silencio" citando literalmente esta función — una afirmación que
el código no respalda en ningún archivo generado real. Detalle completo en "Oleada v11" más abajo.

`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (única fila, plantilla vacía): no hay
historia de rodaje real que incorporar este ciclo — el bloqueo #7 de `SEGUIMIENTO.md` §3 (grabar un
curso completo) sigue abierto. El registro de hallazgos de `auditoriacontinua.md` no trae ningún
`ABIERTO` nuevo de producto/arquitectura esta pasada: el único `ABIERTO` (`#24`, baja, prosa de "Cola
de producto" desactualizada entre ciclos de PM) sigue enrutado a la pregunta de gobernanza #11 de
`SEGUIMIENTO.md` §6, `(pendiente)` de respuesta del dueño — no es una R-XX, es la misma corrección de
prosa que este propio ciclo acaba de aplicar de nuevo, esta vez sobre R-22.

Este ciclo es de PM, no de Programador: no se ha ejecutado la verificación de las cuatro redes; la
spec de R-23 queda lista para que el siguiente ciclo de Programador la implemente y verifique.

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

### Oleada v11 — EN CURSO

#### R-23 — Desviaciones de convención visibles donde de verdad hacen falta: `guion-escenas.md` y `tarjetas.json`

**Migración:** No (aditivo: una sección nueva en el documento de revisión y una clave nueva en
`tarjetas.json.metadatos`; ningún campo de `estado.json` ni de `Configuracion` cambia de forma) ·
**Depende de:** T-10, T-16, T-29 (las tres ya `COMPLETADA`) · **Origen:** observación de
arquitectura del PM (2026-10-05) — grieta de arquitectura verificada sobre código ya construido
(mismo criterio que abrió R-12 a R-22), no hallazgo de auditoría ni entrada de `FEEDBACK.md`.

**Objetivo:** `scripts/convencion.py::detectar_desviaciones` (T-10, ampliada en T-33 con
`numero_escena_duplicado`/`numero_escena_no_creciente`, requisito 2 de T-33) calcula, de forma
correcta y probada por `tests/test_convencion.py`, exactamente las señales que más le importan a
este proyecto: una escena sin rótulo de locución, un rótulo desconocido, una sección auxiliar no
reconocida y —la más grave para la fase de montaje— un número de escena duplicado o no creciente,
que es "la única clave que permite casar una toma grabada con su escena sin ambigüedad"
(`references/contrato-montaje.md`). Verificado leyendo el código, no solo la documentación: **esta
función no se llama desde ningún punto de la generación real.** Ni `scripts/documento_revision.py`
(que construye `guion-escenas.md`, el único archivo que el dueño de verdad revisa de una sentada,
T-16) ni `scripts/pptx.py` (que construye `tarjetas.json`, el contrato de montaje, T-29) la
importan; solo la ejercitan sus propios tests y `tests/test_integracion_montaje.py`. El efecto
práctico es doble: (a) el dueño puede validar y grabar un guion con una escena sin rótulo o con un
número de escena duplicado sin que absolutamente nada se lo señale en el documento que revisa, y
(b) `references/contrato-montaje.md` le dice hoy a la futura cadena de montaje, con esta función
citada por su nombre, que la numeración de escena "ya NO se da por supuesta en silencio" — una
afirmación que ningún archivo generado real respalda todavía. Es el mismo patrón de "cálculo ya
construido y probado, pero no conectado a su consumidor real" que abrió R-12 a R-22, con el matiz de
que aquí la falta de conexión contradice además la propia documentación del contrato.

**Requisitos:**
1. `scripts/documento_revision.py::generar_documento_revision` llama una vez a
   `convencion.detectar_desviaciones(resultado_parseo, resultado_clasificacion, configuracion)`
   (misma firma que ya usan sus tests), igual que ya hace con los avisos de T-14. El resultado
   (`list[Desviacion]`) se reparte en `guion-escenas.md` por el mismo criterio que ya separa avisos
   e indicaciones: las que caen dentro del rango `[linea_inicio, linea_fin]` de una escena se listan
   al pie de esa escena (mismo bloque visual que las indicaciones no recitables, requisito 4 de
   T-16, con su propio encabezado "Desviaciones de la convención" para no mezclarse con ellas); las
   que no pertenecen a ninguna escena (p. ej. `seccion_auxiliar_no_reconocida`) van en una sección
   propia tras el resumen global de cabecera.
2. La cabecera de `guion-escenas.md` (requisito 5 de T-16) gana un recuento más: "Desviaciones de la
   convención: N", junto a los que ya existen (avisos, reescrituras pendientes). `N = 0` no añade
   ninguna sección nueva al documento — mismo criterio de "nada que no aporte" que ya sigue el resto
   del documento con avisos y reescrituras vacíos.
3. `scripts/pptx.py::ResultadoTarjetas` gana un campo aditivo a nivel de `metadatos` (no por
   tarjeta, porque una desviación como el número de escena duplicado implica a más de una escena a
   la vez): `desviaciones_convencion: list[str]`, los textos de `Desviacion.descripcion` tal cual
   (sin reformatearlos ni reinventar redacción), lista vacía si `detectar_desviaciones` no encuentra
   ninguna. `generar_tarjetas` llama a `detectar_desviaciones` una sola vez, reutilizando el mismo
   `resultado_parseo`/`resultado_clasificacion` que ya recibe para el resto de la tarjeta — ningún
   parseo ni clasificación nuevos.
4. `--para-terceros` (bandera ya existente de T-28/T-29) excluye `desviaciones_convencion` del
   `tarjetas.json` exportado a terceros y de cualquier brief derivado, igual que ya excluye el resto
   del aparato de producción interno (son avisos para el dueño y la cadena de montaje, no contenido
   para el espectador ni para un tercero). El `.pdf`/`guion-escenas.md` de repaso completo (sin esa
   bandera) sí los muestra.
5. `references/contrato-tarjetas.md` documenta la clave nueva de `metadatos`.
   `references/contrato-montaje.md` deja de afirmar en abstracto que la numeración "ya NO se da por
   supuesta en silencio" y pasa a decir exactamente dónde mirar:
   `tarjetas.json.metadatos.desviaciones_convencion`.
6. Sin ningún cambio en `convencion.detectar_desviaciones` en sí (T-10/T-33 ya la especifican,
   calculan y prueban correctamente) — esta tarea es pura exposición/cableado hacia los dos
   consumidores reales, no nueva lógica de detección.

**Criterio de aceptación:** sobre los tres guiones reales de `fixtures/reales/` (sin desviaciones
conocidas hoy), `guion-escenas.md` no muestra ninguna sección de desviaciones y
`tarjetas.json.metadatos.desviaciones_convencion` sale `[]`; con una fixture modificada a mano con
una escena sin rótulo de locución y otra que repite el número de una anterior, ambas desviaciones
aparecen localizadas correctamente en `guion-escenas.md` (al pie de la escena que corresponda) y en
`tarjetas.json.metadatos.desviaciones_convencion`, con el mismo texto en los dos sitios; con
`--para-terceros`, la lista no aparece en el `tarjetas.json` exportado; test de regresión que
reproduce el estado anterior a esta tarea (mismo guion con desviaciones, ningún archivo generado las
muestra) para dejar constancia del hallazgo que motivó la tarea.

---

### Cola de producto

`ROADMAP_PRODUCTO.md` tiene, en este ciclo (2026-10-05), una única R-XX `PENDIENTE`: **R-23**
(Oleada v11, detalle completo arriba), abierta por grieta de arquitectura verificada —
`convencion.detectar_desviaciones` calcula correctamente las desviaciones de convención (incluida la
numeración de escena duplicada/no creciente, crítica para la cadena de montaje) pero no se llama
desde ningún punto de la generación real, pese a que `references/contrato-montaje.md` afirma lo
contrario citando esa misma función. `roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo`; el
único hallazgo `ABIERTO` de `auditoriacontinua.md`, `#24` (baja, prosa de "Cola de producto"
desactualizada entre ciclos de PM), sigue enrutado a la pregunta de gobernanza #11 de
`SEGUIMIENTO.md` §6, `(pendiente)` de respuesta del dueño — no es una R-XX. Próximo ciclo de PM:
reconfirmar R-23 tras su implementación y, si el dueño responde entre tanto a la pregunta #11 de §6,
aplicar esa respuesta.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
