# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-09-16 (ciclo de PM). `auditoriacontinua.md` (registro de hallazgos
íntegro releído en este ciclo) cierra `#19` en la pasada de auditoría del mismo día y queda con un
único hallazgo `ABIERTO`: `#24` (baja, puramente de proceso — latencia entre "completado en
código" y "prosa de este documento actualizada"). No es un hallazgo de producto ni de arquitectura
del código, así que no se enruta a una R-XX: es una pregunta de gobernanza sobre quién puede
escribir en qué documento (§0.4 de `HOJA_DE_RUTA.md`, protocolo que solo cambia el dueño), y queda
como pregunta abierta nueva en §6 de `SEGUIMIENTO.md` (#11). `roadmap/FEEDBACK.md` sigue sin
ninguna entrada `nuevo` (bloqueo #7 de `SEGUIMIENTO.md` §3 — grabar un curso completo — sigue sin
resolverse, y sigue siendo la fuente de fricciones reales de rodaje que más haría avanzar este
roadmap). Releyendo esta vez `scripts/salidas.py` (T-30, el selector de salidas que el dueño usa de
verdad en cada validación) junto con `references/contrato-montaje.md`/`contrato-tarjetas.md`, sí
aparece una grieta de arquitectura del mismo tipo que ya motivó R-12/R-13/R-14/R-16: las salidas que
usan tomas reales de rodaje (`guion-alineado.srt` de R-05, `capitulos-youtube.txt` de R-07, y
`duracion_real_segundos`/`inicio_segundos`/`fin_segundos` de R-13/R-16 en `tarjetas.json`) están
completas, probadas y estables, pero **huérfanas del flujo real**: `scripts/salidas.py` nunca lee
`estado.tomas` ni se lo pasa a `pptx.exportar_pptx`, y `capitulos_youtube.py` ni siquiera es una
opción del selector — solo se ejercitan con `tomas_por_escena={}` dentro del health check de
`verificar_salidas.py --fixture`, deliberadamente vacío. Se abre **R-18** (oleada v7 nueva) para
cerrar esa grieta antes de que el dueño grabe el primer curso completo (bloqueo #7) y dependa de
verdad de que estas salidas reflejen sus tomas reales sin invocar nada a mano.

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

---

### Oleada v7 — Cerrar el hueco entre el registro de tomas reales y el selector de salidas

Las tomas registradas durante el rodaje (R-02/R-03) ya alimentan tres salidas completas y probadas
desde hace semanas — `guion-alineado.srt` (R-05), `capitulos-youtube.txt` (R-07) y los campos reales
de `tarjetas.json` (R-13/R-16) — pero ninguna de las tres es alcanzable hoy a través del único punto
de entrada real que usa el dueño: el selector de salidas de cada validación (T-30,
`scripts/salidas.py`). Esta oleada las conecta. Su estado se sigue en §1 de `SEGUIMIENTO.md`.

### R-18 — Integrar en el selector de salidas (T-30) las salidas que dependen de tomas reales

**Oleada / Fase:** v7 · **Migración:** No · **Depende de:** T-30, R-02, R-05, R-07, R-13, R-16
**Origen:** observación de arquitectura del PM (2026-09-16), releyendo `scripts/salidas.py` a la luz
de que la fase siguiente del propio dueño es el montaje con ffmpeg

**Objetivo:** `scripts/salidas.py` (T-30) es el único sitio donde el dueño pide de verdad que se
generen salidas — la pregunta de opción múltiple de cada validación. Hoy, sin embargo, ignora por
completo `estado.tomas` (el registro de tomas de R-02, ya persistido sin migración): `_generar_pptx`
llama a `exportar_pptx` sin `tomas_por_escena`, así que `tarjetas.json` nunca lleva
`duracion_real_segundos`/`inicio_segundos`/`fin_segundos` reales aunque el dueño ya haya marcado
tomas buenas; `_generar_srt` solo produce el `.srt` estimado (T-27), nunca `guion-alineado.srt`
(R-05); y `capitulos_youtube.py` (R-07) ni siquiera es una opción de `TipoSalida` — la única ruta
que hoy lo ejercita es la fixture de `verificar_salidas.py --fixture`, deliberadamente con
`tomas_por_escena={}`. El dueño tendría que saber que existen tres módulos más y saber invocarlos
aparte, justo en el momento — después de grabar, camino del montaje con ffmpeg — en que más importa
que la skill entregue solos los datos reales sin que nadie se lo pida a mano. Es la misma clase de
grieta que ya motivó R-12/R-13/R-14/R-16: la funcionalidad ya existe, está probada y el contrato la
documenta, pero no llega al único flujo real por el que el dueño interactúa con la skill.

**Requisitos:**
1. `scripts/salidas.py` lee `estado.tomas` (tal cual, mismo contenedor que ya consumen
   `srt_alineado.py`/`capitulos_youtube.py`/`pptx.py` desde R-05/R-07/R-13) y lo pasa como
   `tomas_por_escena` allí donde haga falta — quien llama a `generar_salidas_seleccionadas` (la
   sesión que ya tiene el `EstadoProyecto` cargado) se lo entrega, sin que este módulo necesite abrir
   ni conocer `estado.json` por su cuenta.
2. Seleccionar `SRT` sigue generando siempre `guion.srt` (T-27, estimado, comportamiento actual
   intacto); además, en cuanto `tomas_por_escena` contenga al menos una toma marcada `buena`, la
   misma pasada genera también `guion-alineado.srt` (R-05) como un segundo `ArchivoGenerado` bajo el
   mismo `TipoSalida.SRT` — mismo patrón que ya usan `_generar_pdf`/`_generar_pptx`, que hoy devuelven
   más de un archivo bajo un mismo tipo. Sin tomas registradas, se genera exactamente lo mismo que
   hoy (solo `guion.srt`): cambio aditivo, nunca una regresión.
3. Seleccionar `PPTX` pasa `tomas_por_escena` a `exportar_pptx`, de modo que `tarjetas.json` incluya
   duración real y límites absolutos reales (R-13/R-16) en cuanto haya tomas registradas, sin
   ninguna acción manual del dueño. Sin tomas, comportamiento idéntico al actual.
4. `TipoSalida` gana una quinta opción, `CAPITULOS_YOUTUBE` ("Capítulos de YouTube con marcas de
   tiempo (`.txt`)"), añadida a `TODAS_LAS_SALIDAS`/`DESCRIPCION_SALIDA` junto a las cuatro ya
   existentes (requisito 1 de T-30: sigue siendo una única pregunta de opción múltiple, ahora con
   cinco filas en vez de cuatro). Se genera con `capitulos_youtube.generar_capitulos_youtube`,
   pasando `tomas_por_escena` (usa marcas reales si hay tomas, estimadas si no — igual que ya hace
   `verificar_salidas.py --fixture`). Cuando el guion no trae sección `Capítulos` o no llega a una
   sola marca por encima de `capitulos_youtube_marca_minima_segundos`, la salida queda como
   `SalidaOmitida` con el motivo exacto que ya devuelve `formatear_capitulos_youtube` al dar `None`
   — nunca como fallo ni como `SalidaLatente` (no depende de nada externo ausente, a diferencia de
   `.pdf`/`.pptx`).
5. `ResumenSalidas`/`registrar_generacion`/`estado.salidas_generadas` no cambian de forma: la nueva
   ruta solo añade entradas a `generadas`/`omitidas` con los tipos ya definidos, sin romper la
   serialización ni la sugerencia de la próxima pregunta (requisito 2 de T-30).
6. Sin migración de `estado.json` (usa `estado.tomas`, presente desde R-02 sin cambio de esquema) y
   sin campo nuevo de `Configuracion` (son datos derivados de lo ya registrado por el dueño durante
   el rodaje, no un ajuste suyo).

**Criterio de aceptación:** sobre un guion sintético con al menos una escena con una toma marcada
`buena` en `estado.tomas` (mismo patrón de fixture que ya usan R-13/R-16 en
`tests/test_integracion_montaje.py`), llamar a `generar_salidas_seleccionadas` con `SRT`
seleccionado produce tanto `guion.srt` como `guion-alineado.srt`, y con `PPTX` seleccionado
`tarjetas.json` trae `duracion_real_segundos`/`inicio_segundos`/`fin_segundos` reales para esa
escena. `CAPITULOS_YOUTUBE` aparece como quinta opción de `construir_pregunta_salidas` y, generado,
coincide con lo que hoy produce `verificar_salidas.py --fixture` en las mismas condiciones. Sobre
los tres guiones reales de `fixtures/reales/` **sin ninguna toma registrada**, el resultado completo
de `generar_salidas_seleccionadas` (archivos generados, bytes, omitidas) es idéntico al de antes de
R-18 — test de regresión explícito, no solo ausencia de error.

---

### Cola de producto

`ROADMAP_PRODUCTO.md` tiene, en este ciclo, una única R-XX `PENDIENTE`: **R-18** (oleada v7, arriba),
abierta por observación de arquitectura del PM al releer `scripts/salidas.py`, sin relación con
ningún hallazgo de auditoría ni entrada de `FEEDBACK.md` (ambos sin nada más que enrutar este
ciclo — ver cabecera). `roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo`; el bloqueo #7 de
`SEGUIMIENTO.md` §3 (grabar un curso completo) sigue sin resolverse y sigue siendo la fricción real
de rodaje que más haría avanzar este roadmap más allá de lo que la propia arquitectura ya revela.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
