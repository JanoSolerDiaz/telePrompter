# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-10-17 (ciclo de PM, sin apertura de R-XX nueva). **R-32 (Oleada v20)
sigue `PENDIENTE`** (§1 de `SEGUIMIENTO.md`): ningún ciclo de Programador la ha tocado todavía desde
que se abrió el 2026-10-16 — confirmado con `git log` sobre `scripts/pdf.py`/`scripts/salidas.py`,
sin ningún commit desde entonces.

`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (única fila, plantilla vacía): no hay
historia de rodaje real que incorporar este ciclo — el bloqueo #7 de `SEGUIMIENTO.md` §3 (grabar un
curso completo) sigue abierto. La auditoría del propio día (`auditoriacontinua.md`, 2026-10-17)
revisó de forma independiente tanto R-31 como la apertura de R-32 y no trae hallazgos nuevos: solo
reconfirma los dos ya conocidos (`#24`, prosa de "Cola de producto" desactualizada entre ciclos de
PM; `#30`, cadencia de la rutina "Programador"), ambos de proceso/gobernanza puro, pendientes solo
de la respuesta del dueño a las preguntas #11/#12 de `SEGUIMIENTO.md` §6 — ninguno de
producto/arquitectura que convertir en R-XX nueva por esta vía.

**No se abre ninguna R-XX nueva este ciclo.** R-32 es la única fila `PENDIENTE` de §1, y el criterio
establecido desde R-19 es nunca tener más de una R-XX pendiente de código a la vez sin evidencia real
que lo justifique. Su spec completa sigue vigente, sin cambios, en "Oleada v20" más abajo, lista para
el siguiente ciclo de Programador que la implemente y verifique.

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

### Oleada v20 — EN CURSO

#### R-32 — Distinguir, en el exportador `.pdf` (T-28), un fallo real de la conversión de Chrome/Edge (detectado pero la conversión revienta) de la simple ausencia de Chrome/Edge, y dejar el mismo rastro de diagnóstico que ya reciben las demás salidas cuando fallan de verdad

**Migración:** No (ningún campo nuevo en `estado.json`; un campo aditivo en `ResultadoPdf` y un
tercer elemento en la tupla de retorno de `_generar_pdf`) · **Depende de:** T-05, T-28, R-24 (todas
`COMPLETADA`) · **Origen:** observación de arquitectura del PM (2026-10-16) — grieta de arquitectura
verificada sobre código ya construido (mismo tercer criterio que abrió R-12 a R-31), esta vez en el
único generador de salidas que aísla sus propios fallos reales sin pasar por el patrón de
diagnóstico que R-24 ya construyó para el resto.

**Objetivo:** `scripts/pdf.py::convertir_html_a_pdf` nunca lanza una excepción (decisión ya tomada y
documentada en `DECISIONES_TECNICAS.md`, T-28: "cualquier fallo... se devuelve como mensaje
accionable"): cuando el ejecutable de Chrome/Edge no se encuentra, o cuando se encuentra pero la
conversión falla de verdad (código de salida distinto de cero, `OSError`, tiempo agotado — p. ej. un
guion muy largo, o un sandbox que exige `--no-sandbox` en un entorno distinto al ya contemplado),
devuelve en ambos casos `(False, mensaje)`. `scripts/salidas.py::_generar_pdf` (el consumidor real)
no distingue entre los dos: los dos acaban como `SalidaLatente`, exactamente el mismo contenedor que
usa el caso "la skill de marca 480-branded-pptx no está instalada" (T-29). Eso contradice el propio
contrato documentado de `SalidaLatente` — "nunca se confunde con un fallo: el motivo es siempre la
falta de una dependencia externa, no un error del código" (docstring de `scripts/salidas.py`) — y
dista de cómo se trata un fallo real en cualquier otra salida desde R-24: ni `volcar_diagnostico` ni
`obtener_logger().error(...)` se invocan nunca en esta ruta, verificado con `grep`
(`scripts/pdf.py` no importa `logger` ni `monitorizacion` en absoluto). Un Chrome que revienta en el
entorno real del dueño queda así indistinguible, en el resumen final y en los registros, de "no
tengo Chrome instalado" (que no requiere ninguna acción) — sin ningún `diagnostico-<timestamp>.log`
que investigar, pese a que T-05/R-24 construyeron esa infraestructura precisamente para este tipo de
consumidor.

Decisiones de diseño ya tomadas para acotar el alcance:
- **No se toca `convertir_html_a_pdf`.** Sigue sin lanzar nunca una excepción (decisión ya tomada en
  T-28); la distinción y el diagnóstico viven solo en `_generar_pdf` (`scripts/salidas.py`), el mismo
  sitio donde ya vive el patrón de diagnóstico de R-24 para las demás salidas.
- **El HTML de impresión nunca se pierde de vista.** Se genera con éxito siempre, se clasifique el
  resto como latente o como fallo real (requisito 4 de T-28: "nunca falla por la ausencia de
  Chrome"); sigue apareciendo en `generadas` exactamente igual que hoy en los tres desenlaces.
- **El caso "Chrome no encontrado" no cambia en absoluto.** Sigue siendo `SalidaLatente` con el mismo
  mensaje de Ctrl+P, sin ningún diagnóstico — es exactamente la dependencia externa opcional que
  `SalidaLatente` documenta, no un fallo.
- **Reutilizar tal cual `volcar_diagnostico`/`ruta_diagnostico`/`obtener_logger`** (`monitorizacion.py`/
  `logger.py`, R-24): mismo mensaje de `SalidaOmitida` ("fallo al generar: revisa el diagnóstico
  técnico en {ruta}") que ya usan las demás salidas, para que el resumen final no tenga un formato
  distinto para el `.pdf`.

**Requisitos:**
1. `ResultadoPdf` (`scripts/pdf.py`) gana el campo `chrome_detectado: bool`: `True` siempre que
   `detectar_ejecutable_chrome` haya encontrado un ejecutable, con independencia de si la conversión
   tuvo éxito; `False` solo cuando no se encontró ninguno. Cero cambio en `convertir_html_a_pdf` (sigue
   devolviendo `(bool, str)`, nunca lanza).
2. `_generar_pdf` distingue tres desenlaces en vez de dos: éxito (sin cambios); `chrome_detectado=False`
   → `SalidaLatente` (sin cambios, mismo mensaje); `chrome_detectado=True` y conversión fallida →
   fallo real: vuelca diagnóstico con `volcar_diagnostico`/`ruta_diagnostico` (con una excepción
   construida a partir del mensaje de `convertir_html_a_pdf`, para dejar tipo+mensaje+traceback real
   tal como exige T-05), registra en el logger con `obtener_logger().error(...)` y devuelve
   `SalidaOmitida(TipoSalida.PDF, f"fallo al generar: revisa el diagnóstico técnico en {ruta}")` —
   mismo mensaje exacto que usa el `except Exception` genérico de `generar_salidas_seleccionadas`
   para las demás salidas.
3. `_generar_pdf` cambia su firma de retorno de `(generadas, latentes)` a
   `(generadas, latentes, omitidas)`; `generar_salidas_seleccionadas` actualiza su único punto de
   llamada para repartir la tercera lista en `omitidas`, igual que ya hace con otras salidas de tres
   vías.
4. El HTML de impresión sigue apareciendo siempre en `generadas`, tanto en el caso latente como en el
   de fallo real — nunca se pierde ni se oculta silenciosamente.
5. Fuera de alcance, explícito: no se cambia `convertir_html_a_pdf` ni su contrato de "nunca lanza";
   no se reintenta la conversión; no se cambia la detección de Chrome/Edge ni el flag
   `--no-sandbox`; no se toca `verificar_salidas.py` (su propia etapa de PDF ya trata el resultado
   como informativo, sin ninguna clasificación latente/omitida que corregir).

**Criterio de aceptación:** forzando (vía monkeypatch de test, mismo patrón que R-21/R-28) que
`convertir_html_a_pdf` devuelva éxito `False` con un ejecutable de Chrome detectado, `_generar_pdf`
deja un `diagnostico-<timestamp>.log` en la carpeta de salida, registra el fallo en el logger y
clasifica el `.pdf` como `SalidaOmitida` (no `SalidaLatente`), con el HTML de impresión intacto en
`generadas`; sin Chrome detectado en absoluto, el comportamiento es idéntico al de antes de R-32
(test de regresión): `SalidaLatente` con el mismo mensaje, sin ningún diagnóstico. Cuatro redes en
verde.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
