# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-10-19 (ciclo de PM + Programador en la misma sesión). R-32 (Oleada
v20) llevaba `COMPLETADA` en §1 de `SEGUIMIENTO.md` desde el 2026-10-16 (reconfirmada en verde tres
veces sin tarea nueva, sesiones 187-189) sin que ningún ciclo de PM la archivara todavía. Este ciclo
archiva la Oleada v20 en `ROADMAP_HISTORICO.md`, abre R-33 (Oleada v21, ya especificada desde el
2026-10-18) en §1 y la implementa en la misma sesión: el criterio de una sola R-XX pendiente de
código a la vez (vigente desde R-19) queda respetado en todo momento porque ambos pasos — abrir e
implementar — ocurrieron sin que hubiera ninguna otra R-XX pendiente entremedias.

`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (única fila, plantilla vacía): no hay
historia de rodaje real que incorporar — el bloqueo #7 de `SEGUIMIENTO.md` §3 (grabar un curso
completo) sigue abierto. `auditoriacontinua.md` revisado antes de elegir tarea: solo dos `ABIERTO`
(`#24`, baja; `#30`, media), ambos de proceso/gobernanza puro y pendientes solo de la respuesta del
dueño a las preguntas #11/#12 de `SEGUIMIENTO.md` §6 — ninguno de severidad alta, ninguno
convertible en R-XX nueva.

**Oleada v20 (R-32) archivada.** Spec completa y "Cómo se entregó" en `ROADMAP_HISTORICO.md`.

**Oleada v21 (R-33) abierta e implementada.** Ficha completa más abajo, ahora con su "Cómo se
entregó". Origen: observación de producto del propio PM (2026-10-18), verificada con grep, no de
auditoría ni de feedback de rodaje.

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

### Oleada v16 — entregada

La oleada v16 (conectar a su ruta real de generación los tres validadores de contrato que quedaban
huérfanos — `pptx.validar_tarjetas`, `srt.validar_srt`/`srt_alineado.validar_srt_alineado`,
`capitulos_youtube.validar_capitulos_youtube` —, mismo patrón ya cerrado por R-21/R-22, R-28) tiene
su única R-XX en **COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin ningún hito de negocio propio
pendiente. Se movió a `ROADMAP_HISTORICO.md` en este ciclo de PM (2026-10-13). Su spec completa y
cómo se entregó viven ahí.

### Oleada v17 — entregada

La oleada v17 (unificar en `revalidacion.py` la reimplementación privada de la materialización de
particiones aceptadas con la función pública ya existente de `reescrituras.py`, R-29) tiene su única
R-XX en **COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin ningún hito de negocio propio pendiente. Se
movió a `ROADMAP_HISTORICO.md` en este ciclo de PM (2026-10-14). Su spec completa y cómo se entregó
viven ahí.

### Oleada v18 — entregada

La oleada v18 (encadenar en `comandos-montaje.md` los comandos `ffmpeg` reales de montaje —
concatenación de tomas buenas + subtítulos + capítulos—, R-30) tiene su única R-XX en **COMPLETADA**
en §1 de `SEGUIMIENTO.md`, sin ningún hito de negocio propio pendiente. Se movió a
`ROADMAP_HISTORICO.md` en este ciclo de PM (2026-10-15), junto con la nota de gobernanza sobre cómo
se corrigió el hallazgo `#31` (fila de apertura faltante en `DECISIONES_TECNICAS.md`). Su spec
completa y cómo se entregó viven ahí.

### Oleada v19 — entregada

La oleada v19 (avisar en `comandos-montaje.md` de archivos referenciados que no existen todavía en
la carpeta de salida real, R-31) tiene su única R-XX en **COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin
ningún hito de negocio propio pendiente. Se movió a `ROADMAP_HISTORICO.md` en este ciclo de PM
(2026-10-16). Su spec completa y cómo se entregó viven ahí.

### Oleada v20 — entregada

La oleada v20 (distinguir, en el exportador `.pdf`, un fallo real de la conversión de Chrome/Edge
de la simple ausencia de Chrome/Edge, R-32) tiene su única R-XX en **COMPLETADA** en §1 de
`SEGUIMIENTO.md` desde el 2026-10-16, sin ningún hito de negocio propio pendiente. Se movió a
`ROADMAP_HISTORICO.md` en este ciclo de PM (2026-10-19). Su spec completa y cómo se entregó viven
ahí.

### Oleada v21 — entregada

#### R-33 — Mostrar la sección "Preparación antes de grabar" del guión como checklist reabrible en el reproductor, en vez de descartar su contenido tras la validación de convención

**Migración:** No (ningún campo nuevo en `estado.json`; un campo aditivo en el payload embebido del
reproductor y una tecla nueva en `mapa_teclas_reproductor`) · **Depende de:** T-08, T-09, T-18, R-12
(todas `COMPLETADA`) · **Origen:** observación de producto del PM (2026-10-18), no de auditoría ni
de feedback de rodaje (`roadmap/FEEDBACK.md` sigue vacío) — grieta funcional verificada con grep: la
sección auxiliar "Preparación antes de grabar" (`config.SECCIONES_AUXILIARES[1]`) se reconoce en
`scripts/parser.py`/`scripts/clasificador.py` únicamente para no clasificarla como escena, y en
`scripts/convencion.py` únicamente para no señalarla como desviación; su `SeccionAuxiliar.contenido`
no se propaga a ninguna salida real (`scripts/reproductor.py::_construir_datos` no la lee; tampoco
`scripts/pptx.py::generar_tarjetas` ni `scripts/pdf.py`) — grep de `preparacion_antes_grabar` y de
`notas_produc` en todo el repositorio no encuentra ningún consumidor fuera de la propia validación
de convención.

**Objetivo:** cuando el guión trae una sección `## Preparación antes de grabar`, su contenido debe
llegar íntegro al reproductor y mostrarse como un panel de comprobación reutilizable — mismo patrón
ya usado para la ayuda de teclado (`ayuda-teclado`, `guion.js`): overlay centrado, nunca bloqueante,
reabrible en cualquier momento, nunca interpuesto durante una cuenta atrás o el registro de una
toma. Encaja con el principio de producto 5 (legibilidad y utilidad en el momento de grabar por
encima de todo): un formador en solitario, a pie de cámara, no tiene a nadie detrás que le recuerde
revisar encuadre, audio o luz antes de rodar una escena — si lo escribió en su propio guión, el
reproductor no debe dejarlo tirado en el documento fuente.

**Requisitos:**
1. `scripts/reproductor.py::_construir_datos` añade al payload un campo nuevo
   `preparacion_antes_grabar: str | None`: el `contenido` (tal cual, sin reescritura) de la
   `SeccionAuxiliar` cuyo `titulo` coincide con `config.SECCIONES_AUXILIARES[1]` ("Preparación antes
   de grabar"), o `None` si el guión no trae esa sección. Sin sección en el guión → sin panel, nunca
   se inventa contenido (invariante (a): nada se descarta, pero tampoco se fabrica).
2. `guion.js` añade un panel nuevo (`preparacion-grabacion`), mismo esqueleto CSS/JS que
   `ayuda-teclado`: contenido volcado con `textContent` (nunca `innerHTML`, mismo patrón de
   seguridad ya establecido para todo el reproductor), cerrable con `Esc` o con su propia tecla.
3. El panel se abre solo una vez, la primera vez que el reproductor se carga en ese navegador para
   ese guión (mismo mecanismo de flag en `localStorage` que ya usa el reproductor para "ya visto"),
   y solo si `preparacion_antes_grabar` no es `None`. En cargas posteriores no se abre solo; se
   reabre a mano con su tecla o con un botón visible en el índice de escenas.
4. Tecla propia nueva en `mapa_teclas_reproductor` (`scripts/config.py`), documentada en `SKILL.md`
   igual que las demás, sin colisionar con ninguna ya asignada (Espacio, RePág/AvPág, flechas, +/-,
   `[`/`]`, R, H, Esc, ?) y sin modificadores (§0.2: compatible con clicker Bluetooth genérico).
5. El panel nunca se abre ni se superpone mientras hay una cuenta atrás activa o mientras se está
   registrando una toma (teclas G/T/V) — misma prioridad que ya respeta `ayuda-teclado`.
6. Contenido largo: el panel hace scroll interno, nunca se trunca en silencio.
7. **Fuera de alcance, explícito:** no se toca la sección "Notas de producción" (sigue descartada
   tras la validación de convención, como hoy — su contenido es más heterogéneo y sin consumidor
   claro todavía; candidata a una R-XX futura si el rodaje real revela que hace falta); no se cambia
   la lista negra de secciones auxiliares ni la detección de desviaciones de convención
   (`scripts/convencion.py`); no se añade ninguna sección nueva reconocida por el parser; no se toca
   `tarjetas.json` ni el flujo de `.pptx`/`.pdf`; no se cambia la convención de marcado acordada
   (§0.3.1) ni la identidad visual 480.

**Criterio de aceptación:** un guión fixture con `## Preparación antes de grabar` genera un
reproductor cuyo HTML embebe el contenido íntegro de esa sección en el JSON
(`preparacion_antes_grabar`), visible la primera vez que se abre en un navegador nuevo y reabrible
después sin recargar; un guión fixture sin esa sección genera un reproductor sin el campo (o `null`)
y sin ningún panel que se abra solo. `verificar_salidas.py` sigue confirmando la auto-contención a
nivel de bytes del HTML resultante (regla dura de §0.2: ningún `http://`/`https://`/`//cdn`/`fetch`
nuevo). Cuatro redes en verde.

**Cómo se entregó:** `Configuracion` gana `titulo_seccion_preparacion` (`"Preparación antes de
grabar"` por defecto) — campo propio en vez de asumir el índice 1 de `SECCIONES_AUXILIARES`, mismo
criterio ya usado por `titulo_seccion_capitulos` (R-07), que esa lista es la lista negra completa de
T-08/T-10, no un índice de "cuál es la de preparación". `reproductor.py` gana
`_buscar_seccion_preparacion` (mismo patrón de búsqueda por prefijo que
`capitulos_youtube._buscar_seccion_capitulos`) y `_construir_datos` incorpora el campo
`preparacion_antes_grabar: str | None` al payload. En `guion.js`, el panel vive en el **índice de
escenas**, no en la vista de reproducción — decisión de diseño que satisface el requisito 5 ("nunca
se abre... durante una cuenta atrás o el registro de una toma") **por construcción**, no con una
comprobación de estado: esas dos situaciones solo existen dentro de una escena en reproducción, a la
que este panel no tiene acceso. Reutiliza tal cual el overlay `.ayuda-teclado`/`.ayuda-teclado-panel`
(T-24); la tecla nueva (`preparacion_grabacion`, `P`/`p`) se gestiona en un manejador de teclado
propio (`manejarTeclaIndice`), separado del de la vista de reproducción, activo solo con el índice
visible; `Esc` cierra el panel desde el mismo manejador. Primera apertura automática, una sola vez,
mediante una bandera de "primera renderización del índice" (no encadenada tras la llamada inicial a
`renderizarIndice()`, para no alterar el invariante — ya protegido por un test existente — de que
nada se dispara automáticamente después de esa llamada). Botón propio «Preparación antes de grabar»
en el índice como segunda vía de reapertura. 5 tests nuevos en `tests/test_reproductor.py` (699→704).
Cuatro redes en verde. Detalle completo en `DEVELOPERS.md` y `DECISIONES_TECNICAS.md`.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
