# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-10-12 (ciclo de PM). **R-27 (Oleada v15) está `COMPLETADA`** (§1 de
`SEGUIMIENTO.md`) desde el ciclo de Programador del 2026-10-12 que la implementó (el aviso de guion
modificado, `avisar_si_guion_modificado`, queda conectado de verdad y el hash guardado se refresca
para que no se repita sin motivo). Movida a `roadmap/ROADMAP_HISTORICO.md` (Oleada v15) junto con el
resto de oleadas 100 % entregadas.

**Se abre R-28** (Oleada v16): no por hallazgo de auditoría ni entrada de `FEEDBACK.md` — ninguna de
las dos fuentes aporta nada nuevo este ciclo (ver abajo) — sino por **grieta de arquitectura
verificada sobre código ya construido**, el mismo criterio que abrió R-12 a R-27, esta vez localizada
con ayuda de un agente Explore y verificada después `grep` por `grep` de forma independiente antes de
escribir la ficha. Tres validadores de contrato ya construidos y probados —
`pptx.py::validar_tarjetas` (`tarjetas.json`, el contrato directo con el montaje ffmpeg),
`srt.py::validar_srt` (`guion.srt`/`guion-alineado.srt`, cuyo propio docstring dice que imita "un
lector estricto tipo ffmpeg") y `capitulos_youtube.py::validar_capitulos_youtube`
(`capitulos-youtube.txt`) — nunca se invocan en la ruta real de generación de `scripts/salidas.py`,
solo desde `verificar_salidas.py --fixture` (la red de desarrollo, nunca sobre el guion real del
dueño). Es exactamente la misma forma de grieta que el propio proyecto ya reconoció y cerró dos veces
(R-21 para `concat-ffmpeg.txt`, R-22 para `capitulos-ffmpeg.txt`) — aquí quedaron sin corregir sus
tres gemelos. Detalle completo, con cada cita de archivo:línea verificada, en "Oleada v16" más abajo.

`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (única fila, plantilla vacía): no hay
historia de rodaje real que incorporar este ciclo — el bloqueo #7 de `SEGUIMIENTO.md` §3 (grabar un
curso completo) sigue abierto. El registro de hallazgos de `auditoriacontinua.md` no trae ningún
`ABIERTO` nuevo de producto/arquitectura esta pasada: quedan dos `ABIERTO` (`#24`, prosa de "Cola de
producto" desactualizada entre ciclos de PM; `#30`, cadencia de la rutina "Programador"), ambos de
proceso puro y severidad baja/media, sin relación con el código, pendientes solo de la respuesta del
dueño a las preguntas de gobernanza #11/#12 de `SEGUIMIENTO.md` §6.

Este ciclo es de PM, no de Programador: no se ha ejecutado la verificación de las cuatro redes; la
spec de R-28 queda lista para que el siguiente ciclo de Programador la implemente y verifique.

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

### Oleada v13 — entregada

La oleada v13 (entregar `convencion-guiones.md` de verdad al dueño, conectando `convencion.py` al
selector real de salidas de T-30, R-25) tiene su única R-XX en **COMPLETADA** en §1 de
`SEGUIMIENTO.md`, sin ningún hito de negocio propio pendiente. Se movió a `ROADMAP_HISTORICO.md` en
este ciclo de PM (2026-10-08). Su spec completa y cómo se entregó viven ahí.

### Oleada v14 — entregada

La oleada v14 (conectar el diccionario del dueño, `diccionario-locucion.json`, al flujo real de
generación y revalidación, R-26) tiene su única R-XX en **COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin
ningún hito de negocio propio pendiente. Se movió a `roadmap/ROADMAP_HISTORICO.md` en este ciclo de
PM (2026-10-09). Su spec completa y cómo se entregó viven ahí.

### Oleada v15 — entregada

La oleada v15 (cerrar el bucle del aviso de guion modificado, conectando
`estado.py::avisar_si_guion_modificado`, T-07, al flujo real y refrescando el hash guardado para que
el aviso no se repita sin motivo, R-27) tiene su única R-XX en **COMPLETADA** en §1 de
`SEGUIMIENTO.md`, sin ningún hito de negocio propio pendiente. Se movió a `ROADMAP_HISTORICO.md` en
este ciclo de PM (2026-10-12). Su spec completa y cómo se entregó viven ahí.

### Oleada v16 — EN CURSO

#### R-28 — Tres validadores de contrato ya construidos (`tarjetas.json`, `guion.srt`/`guion-alineado.srt`, `capitulos-youtube.txt`) nunca se invocan en la ruta real de generación, solo desde `verificar_salidas.py --fixture`

**Migración:** No (ningún campo nuevo en `estado.json` ni en ningún contrato; mismo patrón mecánico
que R-21/R-22, invocar un validador que ya existe antes de escribir a disco) · **Depende de:** T-27,
T-29, R-05, R-07, R-19, R-21, R-22 (todas ya `COMPLETADA`) · **Origen:** observación de arquitectura
del PM (2026-10-12) — grieta de arquitectura verificada sobre código ya construido (mismo criterio
que abrió R-12 a R-27), con una primera pasada de localización de candidatos delegada a un agente
Explore y verificada de forma independiente, `grep` por `grep`, antes de escribir esta ficha.

**Objetivo:** El propio proyecto ya reconoció y cerró esta forma exacta de grieta dos veces
(`DECISIONES_TECNICAS.md`, apertura de R-21: «`concat_ffmpeg.py` traía su propio validador...
pero `salidas.py::_generar_concat_ffmpeg` nunca lo invocaba antes de escribir... solo lo ejercitaba
`verificar_salidas.py --fixture`, un chequeo de salud aparte de la generación real» — y R-22 repitió
el patrón correctamente para `capitulos-ffmpeg.txt`, con el comentario explícito en el propio código,
`capitulos_youtube.py`, "validado antes de escribir desde el primer día... misma lección que el
hallazgo #27/R-21"). Verificado con `grep` dirigido que la misma frase es cierta **hoy** para otros
tres validadores que nadie corrigió cuando se corrigió el de `concat-ffmpeg.txt`:

1. **`pptx.py:482::validar_tarjetas`** (contrato de `tarjetas.json`, el que alimenta el montaje:
   `SKILL.md:610` — "la fase de montaje lee `inicio_segundos`/`fin_segundos` directamente, sin sumar
   nada por su cuenta"). `pptx.py:760-795::exportar_pptx` construye `resultado_tarjetas` y llama
   `guardar_tarjetas_json(formatear_tarjetas_json(resultado_tarjetas), carpeta_salida)` **sin
   invocar `validar_tarjetas` en ningún punto intermedio**. `grep -rn "validar_tarjetas"
   scripts/*.py` solo devuelve su propia definición, sus tres menciones en comentarios/docstrings de
   `pptx.py` y el único invocador real: `verificar_salidas.py:105,631` — la red de desarrollo, sobre
   el guion de fixture, nunca sobre el guion real del dueño. `scripts/salidas.py:117` importa
   `exportar_pptx` sin importar `validar_tarjetas`, a diferencia de `concat_ffmpeg`/
   `capitulos_youtube`, cuyos validadores sí entraron en el `import` real (`salidas.py:98-109`).
2. **`srt.py:218::validar_srt`** (contrato de `guion.srt`/`guion-alineado.srt` — su propio docstring,
   `srt.py:27`, dice literalmente que aplica "las mismas reglas que un lector estricto tipo ffmpeg").
   `salidas.py:295-317::_generar_srt` genera y guarda tanto el `.srt` estimado
   (`exportar_srt`/`guardar_srt`) como el alineado (`generar_srt_alineado`/`guardar_srt_alineado`,
   R-05) **sin pasar ninguno de los dos por `validar_srt`** (ni por su alias
   `srt_alineado.py:70::validar_srt_alineado`). Único invocador real: `verificar_salidas.py:109,645,660`.
3. **`capitulos_youtube.py:355::validar_capitulos_youtube`** (contrato de `capitulos-youtube.txt`,
   reglas literales de YouTube: primera marca `0:00`, orden estrictamente creciente, separación
   mínima). `salidas.py:371-397::_generar_capitulos_youtube` valida la mitad hermana
   `capitulos-ffmpeg.txt` con `validar_capitulos_ffmpeg` desde R-22 (comentario explícito en el propio
   código citando el hallazgo `#27`/R-21) **pero nunca valida `capitulos-youtube.txt`, la salida
   principal, antes de escribirla** — `salidas.py:98-104` importa `validar_capitulos_ffmpeg` pero no
   `validar_capitulos_youtube`. Evidencia de que es un descuido y no una decisión:
   `SEGUIMIENTO.md:2144-2147` registra que, al abrir R-22, se releyó línea a línea
   `capitulos_youtube.py` —incluida `validar_capitulos_youtube`— "antes de especificar la tarea": el
   propio ciclo de PM tuvo esta función delante y solo corrigió el formato ffmpeg, sin notar que el
   validador de YouTube seguía sin enganchar.

El riesgo real para el formador: si una pasada futura (un parte de rodaje corrupto, un borde no
cubierto por los tests actuales) produce un `tarjetas.json`, un `.srt` o un `capitulos-youtube.txt`
estructuralmente inválido, hoy se escribe igual a disco sin ningún aviso — el error solo se
descubriría durante el montaje con ffmpeg o al subir el vídeo a YouTube, el peor momento posible para
un formador en solitario sin red de producción detrás. Es exactamente el mismo riesgo que R-21 ya
cerró para `concat-ffmpeg.txt` y R-22 para `capitulos-ffmpeg.txt`; esta tarea cierra los tres huecos
gemelos que quedaron sin tocar.

Candidatas descartadas en la misma pasada (falsos positivos ya resueltos por el propio proyecto, no
se repiten): `verificar_salidas.py::verificar_autocontencion` (es la propia herramienta de
verificación, mismo descarte que `contraste_relativo`/`deshacer_normalizaciones` en R-27);
`calibracion.py::calcular_calibracion` (ya evaluado y descartado como falso positivo al abrir R-25:
la invoca directamente la sesión que usa la skill, no un consumidor interno de `scripts/`);
`convencion.py::medir_consistencia_senales`/`proponer_convenciones` (mecanismo latente a propósito
por el propio docstring del módulo, condicionado a una señal de inferencia nueva que los tres guiones
reales de calibración todavía no presentan — infraestructura declarada condicional, no una garantía
incumplida).

**Requisitos:**
1. `scripts/pptx.py::exportar_pptx` invoca `validar_tarjetas` sobre los datos ya construidos (p. ej.
   reutilizando `tarjetas_a_diccionario(resultado_tarjetas)`, que `formatear_tarjetas_json` ya calcula
   por dentro) antes de `guardar_tarjetas_json`. Si devuelve problemas, `tarjetas.json` **no se
   escribe** con contenido inválido.
2. `scripts/salidas.py::_generar_srt` invoca `validar_srt` sobre el contenido de `exportar_srt` antes
   de `guardar_srt`, y sobre el contenido de `generar_srt_alineado` antes de `guardar_srt_alineado`
   (mismo validador, `srt_alineado.validar_srt_alineado` es su alias) — ambos subtítulos protegidos,
   no solo uno.
3. `scripts/salidas.py::_generar_capitulos_youtube` invoca `validar_capitulos_youtube` sobre el
   contenido de `generar_capitulos_youtube` antes de `guardar_capitulos_youtube`, exactamente el
   mismo punto donde ya se valida `capitulos-ffmpeg.txt` desde R-22, unas líneas más abajo en la misma
   función.
4. Propagación del fallo: mismo criterio ya establecido por R-24 para cualquier fallo real de
   generación — el bucle de `generar_salidas_seleccionadas` ya envuelve cada tipo de salida en su
   propio `try`/`except` que vuelca diagnóstico y degrada a `SalidaOmitida` con un motivo accionable
   en español (nunca una traza cruda, nunca un archivo escrito a medias). Un validador que señala
   problemas debe entrar por esa misma puerta — el diseño exacto (una excepción que la propagación ya
   captura, o una `SalidaOmitida` construida a mano con el motivo exacto, mismo patrón literal de
   `_generar_concat_ffmpeg`/R-21) lo decide quien implemente, documentado en `DECISIONES_TECNICAS.md`.
   En cualquier caso: nunca se escribe a disco un archivo que su propio validador ya conocido rechaza.
5. Fuera de alcance, explícito: no se endurece ni se cambia ninguna regla de los tres validadores en
   sí (siguen exactamente las mismas reglas de `references/contrato-tarjetas.md` y el formato `.srt`/
   YouTube ya documentados); no se añade ningún validador nuevo; no se toca `concat_ffmpeg.py` ni
   `capitulos_youtube.py::validar_capitulos_ffmpeg` (ya conectados desde R-21/R-22); no se cambia el
   comportamiento de ninguna salida cuando el contenido generado es válido (que es el caso de los tres
   guiones reales de fixture/calibración hoy, confirmado por las dieciocho etapas en verde de
   `verificar_salidas.py --fixture`) — esta tarea es una red de seguridad para el caso borde, no un
   cambio de comportamiento del caso normal.

**Criterio de aceptación:** tres tests de integración (uno por salida) que fuerzan, por
`monkeypatch` o construcción directa, un contenido estructuralmente inválido para cada contrato
(`tarjetas.json` con `numero_escenas` inconsistente; `.srt` con índice no secuencial; `capitulos-
youtube.txt` con una marca fuera de orden) y comprueban que (a) el archivo correspondiente **no se
escribe** a disco con ese contenido y (b) el dueño recibe un motivo accionable en español, nunca una
traza cruda sin capturar; regresión completa de los tests existentes de T-27/T-29/R-05/R-07/R-19
sin cambio de comportamiento sobre contenido válido; las dieciocho etapas de
`verificar_salidas.py --fixture` siguen en `OK` sobre los tres guiones reales. Cuatro redes en verde.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
