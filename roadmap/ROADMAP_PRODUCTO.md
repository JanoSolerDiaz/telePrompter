# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-10-13 (ciclo de PM). **R-28 (Oleada v16) está `COMPLETADA`** (§1 de
`SEGUIMIENTO.md`) desde el ciclo de Programador del 2026-10-13 que la implementó (los tres
validadores de contrato restantes — `tarjetas.json`, `guion.srt`/`guion-alineado.srt`,
`capitulos-youtube.txt` — quedan conectados de verdad a su ruta real de generación). Movida a
`roadmap/ROADMAP_HISTORICO.md` (Oleada v16) junto con el resto de oleadas 100 % entregadas.

**Se abre R-29** (Oleada v17): no por hallazgo de auditoría ni entrada de `FEEDBACK.md` — ninguna de
las dos fuentes aporta nada nuevo este ciclo (ver abajo) — sino por **grieta de arquitectura
verificada sobre código ya construido**, el mismo criterio que abrió R-12 a R-28, pero de una forma
distinta a las diez repeticiones anteriores: no es una pieza sin ningún llamador, sino una pieza
construida, probada y **documentada explícitamente como la solución a reutilizar** que la ruta real
ignora, reimplementando en privado el mismo cálculo. `scripts/reescrituras.py:61-63` deja un
comentario al definir `SEPARADOR_MITADES`: «Público (no `_`) porque T-17 (revalidacion) necesita
partir `propuesta` en sus dos mitades para materializar particiones con la misma identidad que
`aplicar_particion_aceptada`, sin duplicar el separador como constante propia». Pero
`revalidacion.py::_particion_aceptada_de`/`_materializar_marcados` (`revalidacion.py:190-244`) solo
importan esa constante y reimplementan a mano, con las mismas cuatro condiciones, el emparejamiento
bloque↔reescritura que `reescrituras.py::aplicar_particion_aceptada`/`aplicar_particiones_aceptadas`
(`reescrituras.py:322-369`) ya calculan — sin invocarlas nunca. Localizada con ayuda de un agente
Explore (instruido para no repetir candidatas ya descartadas en ciclos anteriores) y verificada
después línea a línea de forma independiente antes de escribir la ficha. Detalle completo, con cada
cita de archivo:línea, en "Oleada v17" más abajo.

`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (única fila, plantilla vacía): no hay
historia de rodaje real que incorporar este ciclo — el bloqueo #7 de `SEGUIMIENTO.md` §3 (grabar un
curso completo) sigue abierto. El registro de hallazgos de `auditoriacontinua.md` no trae ningún
`ABIERTO` nuevo de producto/arquitectura esta pasada: quedan dos `ABIERTO` (`#24`, prosa de "Cola de
producto" desactualizada entre ciclos de PM; `#30`, cadencia de la rutina "Programador"), ambos de
proceso puro y severidad baja/media, sin relación con el código, pendientes solo de la respuesta del
dueño a las preguntas de gobernanza #11/#12 de `SEGUIMIENTO.md` §6.

Este ciclo es de PM, no de Programador: no se ha ejecutado la verificación de las cuatro redes; la
spec de R-29 queda lista para que el siguiente ciclo de Programador la implemente y verifique.

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

### Oleada v17 — EN CURSO

#### R-29 — `revalidacion.py` reimplementa en privado, en vez de reutilizar, la materialización de particiones aceptadas que `reescrituras.py::aplicar_particion_aceptada`/`aplicar_particiones_aceptadas` ya construyó y documentó exactamente para este consumidor

**Migración:** No (ningún campo nuevo en `estado.json` ni en ningún contrato; cambio interno de qué
función calcula una materialización que el flujo real ya hace hoy, sin tocar su resultado para
ningún guion real) · **Depende de:** T-14, T-15, T-17, P-02, P-04 (todas ya `COMPLETADA`) ·
**Origen:** observación de arquitectura del PM (2026-10-13) — grieta de arquitectura verificada sobre
código ya construido (mismo criterio que abrió R-12 a R-28), con una primera pasada de localización
delegada a un agente Explore y verificada de forma independiente, leyendo el código citado línea a
línea, antes de escribir esta ficha.

**Objetivo:** `scripts/reescrituras.py:61-63` deja un comentario explícito, escrito al definir
`SEPARADOR_MITADES`: «Público (no `_`) porque T-17 (revalidacion) necesita partir `propuesta` en sus
dos mitades para materializar particiones con la misma identidad que `aplicar_particion_aceptada`,
sin duplicar el separador como constante propia». La intención de diseño, por tanto, es que
`revalidacion.py` REUTILICE `aplicar_particion_aceptada`/`aplicar_particiones_aceptadas`
(`reescrituras.py:322,358`, públicas, con sus propios tests en `tests/test_reescrituras.py`). En la
práctica, `revalidacion.py` solo importa la constante `SEPARADOR_MITADES` (`revalidacion.py:59`) y
reimplementa por su cuenta, en `_particion_aceptada_de` (`revalidacion.py:190-205`) y
`_materializar_marcados` (`revalidacion.py:210-244`), el mismo criterio de emparejamiento bloque↔
reescritura — las cuatro condiciones exactas (`numero_escena`, `linea_inicio`, `linea_fin`, texto
igual al `original`) que ya calcula `aplicar_particion_aceptada` (`reescrituras.py:342-347`) — en vez
de llamarla. `grep -rn "aplicar_particion" scripts/` confirma que ninguna de las dos funciones
públicas tiene hoy ningún invocador real fuera de `tests/test_reescrituras.py`.

El riesgo real: hoy las dos implementaciones coinciden (mismas cuatro condiciones, verificado línea a
línea), pero nada lo garantiza hacia delante — son dos copias de la misma regla de negocio
mantenidas a mano en dos archivos, sin ningún test que las compare entre sí. Es precisamente el área
de código que ya produjo dos incidencias de severidad alta en este proyecto (P-02 y P-04, el cruce
edición-manual/partición-aceptada, invariante (c) — «la edición manual manda»): una futura corrección
de la regla de emparejamiento en un solo sitio (el más visible, probablemente
`aplicar_particion_aceptada`, que es la función pública y documentada) dejaría al otro sitio
(`revalidacion.py`, la ruta REAL que usa el dueño) con el criterio antiguo, sin que ningún test lo
detectara — el mismo patrón de "la ruta real queda huérfana", pero en vez de faltar una llamada,
sobra una reimplementación que puede divergir en silencio.

Candidatas descartadas en la misma pasada del agente Explore (no son grietas nuevas):
`monitorizacion.py::ejecutar_con_diagnostico` — ya evaluada y descartada explícitamente al abrir
R-24 (`DECISIONES_TECNICAS.md`, 2026-10-06: «pensada para abortar un proceso entero con código de
salida... exactamente lo contrario del requisito 3 de T-30»), no es una conexión olvidada sino una
decisión de diseño ya tomada y documentada. `monitorizacion.py::ResumenEjecucion` — infraestructura
genérica de T-05 (recuento de escenas/bloques/avisos/reescrituras/salidas de toda la ejecución),
funcionalmente sustituida para el consumidor real por `salidas.py::ResumenSalidas` (T-30, con su
propio `mostrar_resumen`, categorías `generadas`/`omitidas`/`latentes` más precisas que exige T-30
requisito 4); candidata más débil, queda para una futura pasada si el dueño confirma que echa en
falta el recuento genérico de `ResumenEjecucion` en algún punto del flujo real.
`normalizacion.py::deshacer_normalizaciones` — inversa exacta de `aplicar_normalizaciones`, usada hoy
solo como prueba de propiedad en sus propios tests; la ruta real nunca reconstruye el original por
cálculo (lo guarda directamente en `Reescritura.original`), así que no tiene hueco real de consumidor
que llenar.

**Requisitos:**
1. Investigar primero, con evidencia (tests nuevos si hace falta), si `_materializar_marcados`/
   `_particion_aceptada_de` (`revalidacion.py`) y `aplicar_particiones_aceptadas`
   (`reescrituras.py`) producen HOY el mismo resultado en todo escenario sin conflicto
   edición/partición (es decir, en todo caso donde `indices_con_edicion_previa_a_particion` está
   vacío) — un test que, para los bloques y reescrituras aceptadas de los tres guiones reales (y los
   casos ya cubiertos por `tests/test_revalidacion.py`), compare ambas rutas bloque a bloque.
2. Si son equivalentes (caso esperado, dada la lectura línea a línea de esta ficha): eliminar la
   duplicación haciendo que `revalidacion.py` llame a `aplicar_particion_aceptada`/
   `aplicar_particiones_aceptadas` como único cálculo de la materialización, conservando intacta la
   salvaguarda de `indices_con_edicion_previa_a_particion` (P-02/P-04, hallazgo #9) — que la función
   pública no contempla hoy — filtrando antes de llamarla la lista de reescrituras a aplicar (excluir
   las que correspondan a un índice con edición previa), o extendiendo la función pública con ese
   mismo parámetro opcional, lo que resulte más limpio a quien implemente; decisión documentada en
   `DECISIONES_TECNICAS.md`. En cualquier caso, al terminar debe quedar UNA sola implementación de la
   regla de emparejamiento bloque↔reescritura, no dos.
3. Si la investigación del requisito 1 revela una divergencia real (un escenario donde las dos
   implementaciones no coinciden hoy): tratarlo como lo que sería, un hallazgo de severidad alta sobre
   el invariante (c), corregir la ruta real (`revalidacion.py`, la que usa el dueño) a la regla
   correcta y dejarlo documentado como tal en `DECISIONES_TECNICAS.md` y en el registro de
   `auditoriacontinua.md` si procede, antes de unificar.
4. Fuera de alcance, explícito: no se cambia ninguna regla de negocio del emparejamiento en sí (ambas
   implementaciones de hoy codifican la misma regla, verificado); no se toca la salvaguarda de
   P-02/P-04 en su comportamiento, solo en dónde vive; no se amplía a otras reimplementaciones
   paralelas que no sean esta (p. ej. `ejecutar_con_diagnostico`, ya evaluada y descartada como no
   conectable por R-24 con razón documentada, no se repite aquí).

**Criterio de aceptación:** test nuevo que demuestra, sobre los tres guiones reales y sobre los casos
ya cubiertos de `tests/test_revalidacion.py`, que la materialización de `revalidacion.py` coincide
bloque a bloque con `aplicar_particiones_aceptadas` siempre que no haya conflicto edición/partición
pendiente; tras el requisito 2, una única función calcula el emparejamiento (no dos copias
mantenidas a mano); los tests existentes de T-15/T-17/P-02/P-04 (incluido el que fija el
comportamiento del hallazgo #9) pasan sin cambio de comportamiento. Cuatro redes en verde.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
