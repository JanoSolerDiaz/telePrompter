# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-10-01 (ciclo de PM). **R-20 (Oleada v9) está `COMPLETADA`** (§1 de
`SEGUIMIENTO.md`) desde el ciclo de Programador del mismo día que la abrió (2026-09-30); esta prosa
seguía describiéndola como "EN CURSO"/`PENDIENTE` durante las nueve reconfirmaciones posteriores del
Programador (mismo patrón ya trazado por el hallazgo `#24` de `auditoriacontinua.md`, no corregido
antes porque este ciclo es el primero de PM desde entonces). Movida a `roadmap/ROADMAP_HISTORICO.md`
(Oleada v9) junto con el resto de oleadas y fases 100 % entregadas. La nota de gobernanza sobre cómo
se justificó abrir R-19 (hallazgo `#26`) viaja con ella, ya cerrada por el ciclo de PM anterior y
verificada `RESUELTO` por el auditor (2026-10-01) — no se repite aquí.

**Se abre R-21** (Fase transversal F-J): el hallazgo `#27` de `auditoriacontinua.md` (media,
`ABIERTO`, detectado 2026-10-01 por la propia auditoría reproduciendo código, no solo leyéndolo) es
el único hallazgo de esta pasada que convertir en tarea — es de robustez de una salida real
(`concat-ffmpeg.txt`, R-19), no gobernanza ni prosa, así que entra como R-XX con `origen: auditoría
#27` en vez de quedar solo anotado. Resumen del hallazgo: `scripts/concat_ffmpeg.py` trae su propio
validador del formato del demuxer `concat` de ffmpeg, pero `scripts/salidas.py::
_generar_concat_ffmpeg` nunca lo invoca antes de escribir a disco — solo lo ejercita
`verificar_salidas.py --fixture`, un chequeo de salud aparte de la ruta real de generación.
Reproducido por el auditor con código, no solo leído: un `archivo_video` de solo espacios (tecleable
sin querer en el `window.prompt` de `V`/`v`) genera una línea `file '   '` que el validador acepta
pero ffmpeg no puede abrir; un `archivo_video` con un salto de línea incrustado (alcanzable editando
a mano el `.json` del parte de rodaje exportado, flujo que R-02 soporta explícitamente) parte una
entrada en dos líneas mal formadas que el validador sí detecta, pero nunca llega a ejecutarse en la
ruta real. Ningún invariante de §0.2 se rompe (salida derivada y regenerable, la generación nunca
falla), por eso es severidad `media`, no `alta`, y no urgente por §0.3 — pero es exactamente el tipo
de deuda de calidad sobre una entrega ya hecha que este roadmap existe para no dejar perdida.
Detalle completo en "Fase transversal F-J" más abajo.

`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (única fila, plantilla vacía): no hay
historia de rodaje real que incorporar este ciclo. El hallazgo `#24` (prosa de "Cola de producto"
desactualizada entre ciclos de PM) sigue enrutado a la pregunta de gobernanza #11 de
`SEGUIMIENTO.md` §6, `(pendiente)` de respuesta del dueño — no es una R-XX, es la misma corrección
de prosa que este propio ciclo acaba de aplicar.

Revisión propia de este ciclo: releído `scripts/concat_ffmpeg.py` (`validar_lista_concat_ffmpeg`,
`_escapar_ruta_ffmpeg`, `calcular_lista_concat_ffmpeg`), `scripts/salidas.py::
_generar_concat_ffmpeg` y `scripts/tomas.py` (`_toma_desde_dict`, validación de `archivo_video`)
para confirmar de primera mano que el hallazgo describe el código real: el validador existe, está
probado, y en efecto no se invoca desde la ruta de generación — mismo patrón de verificación (código
real, no prosa) que las R-XX anteriores. Este ciclo es de PM, no de Programador: no se ha ejecutado
la verificación de las cuatro redes; la spec de R-21 queda lista para que el siguiente ciclo de
Programador la implemente y verifique.

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

### Fase transversal F-J — EN CURSO

> No es una oleada de producto nueva: es deuda de calidad sobre una salida ya entregada (R-19,
> `concat-ffmpeg.txt`), detectada por la auditoría reproduciendo código, no solo leyéndolo. Mismo
> tratamiento que F-D/F-G/F-H/F-I: se cierra antes de reanudar la cola de producto principal.

#### R-21 — Validar `concat-ffmpeg.txt` en la ruta real de generación y sanear `archivo_video` en el origen

**Migración:** No (saneamiento de entrada y una llamada de validación nuevos; ningún campo de
`estado.json` ni de `Configuracion` cambia de forma) · **Depende de:** R-19 · **Origen:** auditoría
`#27` (media, 2026-10-01), reproducido con código por el propio auditor, no solo observado.

**Objetivo:** `scripts/concat_ffmpeg.py` trae su propio validador del formato del demuxer `concat`
de ffmpeg (`validar_lista_concat_ffmpeg`, criterio de aceptación de R-19), pero
`scripts/salidas.py::_generar_concat_ffmpeg` nunca lo invoca antes de escribir `concat-ffmpeg.txt` a
disco — solo lo ejercita `verificar_salidas.py --fixture`, un chequeo de salud aparte de la
generación real. Esto deja pasar sin aviso dos entradas que `archivo_video` admite hoy sin ningún
saneamiento (`tomas.py` solo comprueba `isinstance(..., str)`): una cadena de solo espacios
(tecleable por accidente en el `window.prompt` de `V`/`v`) y un salto de línea incrustado
(alcanzable editando a mano el `.json` del parte de rodaje exportado, flujo que R-02 soporta
explícitamente), que rompen el archivo final de formas que el validador ya sabe detectar pero que
nunca llega a ejecutarse en la ruta real. R-19 es la primera salida de la cadena de montaje cuyo
contenido es texto libre tecleado por el dueño (a diferencia de `srt.py`/`capitulos_youtube.py`,
derivados internamente), lo que le da a este hueco arquitectónico preexistente consecuencias reales
por primera vez.

**Requisitos:**
1. `scripts/salidas.py::_generar_concat_ffmpeg` invoca `concat_ffmpeg.validar_lista_concat_ffmpeg`
   sobre el contenido generado antes de escribirlo; si la validación falla, la salida se degrada a
   `SalidaOmitida` con el motivo exacto del fallo — mismo patrón `try`/`except` que ya aplica
   `generar_salidas_seleccionadas` a otros fallos de generación, nunca una excepción sin capturar.
2. `archivo_video` se sanea en el origen, en los dos puntos donde el dueño lo teclea o lo edita:
   `assets/reproductor/guion.js` (captura de `V`/`v` y edición desde el índice) recorta espacios y
   rechaza un valor vacío tras el recorte o con un salto de línea, tratándolo como "sin anotar";
   `scripts/tomas.py::_toma_desde_dict` aplica el mismo recorte y rechazo al leer un parte de rodaje
   editado a mano (R-02), nunca como error fatal — un valor inválido se normaliza a `""`, igual que
   si nunca se hubiera anotado.
3. `references/contrato-tomas.md` documenta la regla de saneamiento de `archivo_video` (recortado,
   sin saltos de línea); `references/contrato-montaje.md` deja constancia de que
   `concat-ffmpeg.txt` nunca llega a disco sin pasar por `validar_lista_concat_ffmpeg`.
4. Fuera de alcance, explícitamente: extender el mismo patrón de validación-antes-de-escribir a
   `srt.py`/`capitulos_youtube.py` (la misma deuda arquitectónica preexistente, pero sin las
   consecuencias reales que le da a R-19 ser texto libre) — se deja anotado aquí como candidata
   futura, no se amplía el alcance de esta tarea para cubrirlo.
5. Invariantes (a)/(d) de §0.2 intactos: sanear o degradar `concat-ffmpeg.txt` nunca toca
   `estado.json["tomas"]` ni ningún campo existente de una toma; es una salida derivada y
   regenerable, igual que antes de R-21.

**Criterio de aceptación:** un `archivo_video` de solo espacios tecleado en el reproductor se
guarda como `""` (sin archivo anotado), nunca como `'   '` en `concat-ffmpeg.txt`; un `archivo_video`
con un salto de línea incrustado en un parte de rodaje editado a mano se normaliza al cargarlo, sin
llegar nunca a producir una línea mal formada en el archivo final; test que fuerza a
`validar_lista_concat_ffmpeg` a fallar (contenido inválido inyectado) y confirma que
`_generar_concat_ffmpeg` degrada a `SalidaOmitida` en vez de escribir el archivo o lanzar una
excepción sin capturar; sobre los tres guiones reales de `fixtures/reales/` con parte de rodaje
sintético, `concat-ffmpeg.txt` generado sigue siendo exactamente el mismo que antes de R-21 cuando
`archivo_video` ya viene limpio (sin regresión).

---

### Cola de producto

`ROADMAP_PRODUCTO.md` tiene, en este ciclo (2026-10-01), una única R-XX `PENDIENTE`: **R-21** (Fase
transversal F-J, detalle completo arriba), abierta por el hallazgo `#27` de `auditoriacontinua.md`
(media, deuda de calidad sobre la salida `concat-ffmpeg.txt` de R-19, ya entregada y archivada).
`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo`; el único otro hallazgo `ABIERTO`, `#24`
(baja, prosa de "Cola de producto" desactualizada entre ciclos de PM), sigue enrutado a la pregunta
de gobernanza #11 de `SEGUIMIENTO.md` §6, `(pendiente)` de respuesta del dueño — no es una R-XX.
Próximo ciclo de PM: reconfirmar R-21 tras su implementación y, si el dueño responde entre tanto a
la pregunta #11 de §6, aplicar esa respuesta.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
