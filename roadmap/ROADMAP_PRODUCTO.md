# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-10-02 (ciclo de PM). **R-21 (Fase transversal F-J) está
`COMPLETADA`** (§1 de `SEGUIMIENTO.md`) desde el ciclo de Programador del mismo día que la abrió el
ciclo de PM anterior (2026-10-01→2026-10-02, cierra el hallazgo `#27` de `auditoriacontinua.md`).
Movida a `roadmap/ROADMAP_HISTORICO.md` (Fase transversal F-J) junto con el resto de fases 100 %
entregadas.

**Se abre R-22** (Oleada v10): no por hallazgo de auditoría ni entrada de `FEEDBACK.md` — ninguna de
las dos fuentes aporta nada nuevo este ciclo (ver abajo) — sino por **grieta de arquitectura
verificada sobre código ya construido**, el mismo criterio que abrió R-12 a R-20. `scripts/
capitulos_youtube.py::calcular_capitulos` ya empareja cada escena con su título de capítulo y
calcula su instante de inicio acumulado (real, de la toma buena, o estimado de T-12), probado desde
R-07 — pero ese cálculo solo se expone hoy en un formato pensado para pegar en la descripción de
YouTube (`capitulos-youtube.txt`, texto `M:SS Título`), nunca en un formato que la propia fase de
montaje con ffmpeg (la siguiente de esta skill, T-33) pueda **incrustar directamente en el vídeo
final** como capítulos reales del archivo. Verificado leyendo `calcular_capitulos`/
`formatear_capitulos_youtube` línea a línea (no solo `references/contrato-montaje.md`) antes de
especificar la tarea, mismo rigor que R-20 ya aplicó para no repetir el error de `#26`. Detalle
completo en "Oleada v10" más abajo.

`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (única fila, plantilla vacía): no hay
historia de rodaje real que incorporar este ciclo — el bloqueo #7 de `SEGUIMIENTO.md` §3 (grabar un
curso completo) sigue abierto. El registro de hallazgos de `auditoriacontinua.md` no trae ningún
`ABIERTO` nuevo de producto/arquitectura esta pasada: el único `ABIERTO` (`#24`, baja, prosa de "Cola
de producto" desactualizada entre ciclos de PM) sigue enrutado a la pregunta de gobernanza #11 de
`SEGUIMIENTO.md` §6, `(pendiente)` de respuesta del dueño — no es una R-XX, es la misma corrección de
prosa que este propio ciclo acaba de aplicar de nuevo.

Este ciclo es de PM, no de Programador: no se ha ejecutado la verificación de las cuatro redes; la
spec de R-22 queda lista para que el siguiente ciclo de Programador la implemente y verifique.

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

### Oleada v10 — EN CURSO

#### R-22 — Capítulos reales incrustables en el vídeo final (`capitulos-ffmpeg.txt`, formato `FFMETADATA1` de ffmpeg)

**Migración:** No (archivo derivado nuevo y un campo aditivo en `ResultadoCapitulos`; ningún campo
de `estado.json` ni de `Configuracion` cambia de forma) · **Depende de:** R-07 · **Origen:**
observación de arquitectura del PM (2026-10-02) — grieta de arquitectura verificada sobre código ya
construido (mismo criterio que abrió R-12 a R-20), no hallazgo de auditoría ni entrada de
`FEEDBACK.md`.

**Objetivo:** `scripts/capitulos_youtube.py::calcular_capitulos` ya empareja cada título de la
sección `Capítulos` del guion con su escena y calcula el instante de inicio acumulado de cada una
(real, de la toma buena — R-02 —, o estimado del ritmo deducido del guion — T-12 —, con aviso
explícito si se mezclan ambos). Hoy ese cálculo solo se expone en `capitulos-youtube.txt`, pensado
para pegarse a mano en la descripción de un vídeo de YouTube — útil, pero texto para un humano, no
un archivo que la fase de montaje (la siguiente de esta skill, T-33, que ya cierra con
`concat-ffmpeg.txt` de R-19 y `guion-alineado.srt` de R-05) pueda pasarle a ffmpeg para que los
capítulos queden **incrustados de verdad en el `.mp4` final** — el formador no tiene hoy ninguna
salida de esta skill que, al unirla en el montaje, le deje un vídeo navegable por capítulos nada más
exportarlo. ffmpeg soporta esto de forma nativa con su propio formato de metadatos (`FFMETADATA1`,
`ffmpeg -i video.mp4 -i capitulos-ffmpeg.txt -map_metadata 1 -codec copy video-final.mp4`): esta
tarea genera ese archivo reutilizando tal cual el emparejamiento y los tiempos que R-07 ya calcula y
prueba, sin inventar ningún cálculo nuevo.

**Requisitos:**
1. `scripts/capitulos_youtube.py` gana `formatear_capitulos_ffmpeg(resultado: ResultadoCapitulos,
   configuracion: Configuracion | None = None) -> str | None`, hermana de
   `formatear_capitulos_youtube` y con la misma condición de `None` (sin capítulos que generar).
   Reutiliza `resultado.capitulos` (título + `inicio_segundos` de cada capítulo) **tal cual**, sin
   reproducir el emparejamiento ni el cálculo de tiempos de `calcular_capitulos`.
2. **`ResultadoCapitulos` gana un campo aditivo, `duracion_total_segundos: float`** (la suma
   acumulada tras procesar el último capítulo, el mismo `cursor_segundos` final que ya calcula el
   bucle de `calcular_capitulos` — ninguna cuenta nueva, solo exponer un valor que el bucle ya
   produce y hoy descarta). Es el único dato que falta para poder cerrar el último capítulo sin
   inventar una duración: el `END` del último capítulo del `.mp4` es este valor.
3. **Formato `FFMETADATA1` exacto:** primera línea `;FFMETADATA1`; un bloque `[CHAPTER]` por
   capítulo con `TIMEBASE=1/1000`, `START=<ms>`, `END=<ms>` (ambos enteros, redondeando igual que
   `_formatear_mm_ss` ya redondea hacia abajo para no adelantar nunca una marca) y `title=<título>`;
   `END` de un capítulo es el `START` del siguiente, y el del último es `duracion_total_segundos`
   (requisito 2) convertido a milisegundos. Separar los bloques con una línea en blanco, igual que
   exige el propio formato de ffmpeg.
4. **Sin la "marca mínima" de `capitulos_youtube_marca_minima_segundos`:** a diferencia de
   `capitulos-youtube.txt` (pensado para que una lista de texto no amontone marcas casi seguidas,
   requisito 3 de R-07), unos capítulos incrustados en el archivo no compiten por espacio de
   lectura — cada escena emparejada con un título se convierte en su propio capítulo, sin filtrar
   ninguno por cercanía con el anterior. Documentar esta diferencia deliberada en el propio
   docstring de `formatear_capitulos_ffmpeg`, para que nadie la confunda con un olvido del filtro de
   R-07.
5. **Escapado del título según el formato `FFMETADATA1` de ffmpeg:** los caracteres `\`, `=`, `;`,
   `#` y el salto de línea se escapan con `\` por delante (igual que ya hace `_escapar_ruta_ffmpeg`
   de R-19 para la ruta de vídeo, mismo patrón, formato distinto) antes de escribir `title=...`.
6. **Transparencia real/estimado:** si alguna de las marcas conservadas depende de una duración
   estimada en vez de la toma buena real (mismo criterio y mismo texto que ya calcula
   `formatear_capitulos_youtube`), la primera línea tras `;FFMETADATA1` es un comentario `;` con ese
   mismo aviso — ffmpeg ignora cualquier línea de nivel superior que empiece por `;` o `#`, así que
   el aviso no interfiere con el `-map_metadata` real.
7. **Validar antes de escribir, desde el primer día** (lección del hallazgo `#27`/R-21, para no
   repetir la misma deuda con una salida nueva): `scripts/capitulos_youtube.py` gana
   `validar_capitulos_ffmpeg(contenido: str) -> list[str]`, hermana de `validar_capitulos_youtube`,
   que exige la primera línea `;FFMETADATA1`, cada `START`/`END` entero no negativo, `START`
   estrictamente creciente entre capítulos consecutivos y `END` de cada capítulo `<=` `START` del
   siguiente (sin solapes). `scripts/salidas.py::_generar_capitulos_youtube` invoca este validador
   sobre el contenido de `capitulos-ffmpeg.txt` antes de guardarlo — si falla, esa mitad de la
   salida se degrada a `SalidaOmitida` con el motivo exacto (mismo patrón `try`/`except` que R-21 ya
   dejó listo para `concat-ffmpeg.txt`), sin impedir que `capitulos-youtube.txt` se genere igual si
   ese validador pasa.
8. `scripts/config.py` gana `NOMBRE_ARCHIVO_CAPITULOS_FFMPEG: str = "capitulos-ffmpeg.txt"` (mismo
   patrón de constante de módulo que `NOMBRE_ARCHIVO_CAPITULOS_YOUTUBE`/
   `NOMBRE_ARCHIVO_CONCAT_FFMPEG`, no un campo de `Configuracion`: no es un valor que el dueño deba
   poder cambiar). Se genera junto a `capitulos-youtube.txt`, bajo la misma opción
   `TipoSalida.CAPITULOS_YOUTUBE` del selector de T-30 (mismo patrón que `guion.srt`/
   `guion-alineado.srt` bajo `TipoSalida.SRT`) — no es una séptima opción nueva del selector, son
   dos archivos de la misma salida.
9. `references/contrato-montaje.md` documenta `capitulos-ffmpeg.txt`: qué es, cuándo se genera (la
   misma condición que `capitulos-youtube.txt`: el guion trae sección `Capítulos`), el comando de
   ffmpeg de ejemplo (`-map_metadata`) y que, como `concat-ffmpeg.txt`, nunca llega a disco sin
   pasar por su propio validador. `references/contrato-tomas.md` no cambia (no toca el parte de
   rodaje).
10. Fuera de alcance, explícitamente: extender esta misma validación-antes-de-escribir a `srt.py` o
    a la ruta de generación ya existente de `capitulos-youtube.txt` — ya decidido fuera de alcance
    de R-21 (`DECISIONES_TECNICAS.md`, 2026-10-01) por no tener evidencia real que lo justifique;
    esta tarea no reabre esa decisión, solo aplica el patrón correcto a la salida nueva que ella
    misma crea.

**Criterio de aceptación:** sobre los tres guiones reales de `fixtures/reales/` (los tres traen
sección `Capítulos`), `capitulos-ffmpeg.txt` generado tiene un bloque `[CHAPTER]` por título
emparejado, `START`/`END` contiguos sin huecos ni solapes y el `END` del último capítulo coincide
exactamente con `duracion_total_segundos`; un guion sin sección `Capítulos` deja la salida omitida
con el mismo motivo que ya usa `capitulos-youtube.txt`, nunca un archivo vacío ni un fallo; un título
con `;`/`#`/`=`/`\` o un salto de línea se escapa correctamente y el archivo generado sigue siendo
`FFMETADATA1` válido; test que fuerza a `validar_capitulos_ffmpeg` a fallar (contenido inválido
inyectado) y confirma que `_generar_capitulos_youtube` degrada esa mitad a `SalidaOmitida` sin
impedir la generación de `capitulos-youtube.txt`; con una mezcla de escenas con y sin toma buena, la
primera línea tras `;FFMETADATA1` avisa de la mezcla con el mismo texto que ya usa
`formatear_capitulos_youtube`.

---

### Cola de producto

`ROADMAP_PRODUCTO.md` tiene, en este ciclo (2026-10-02), una única R-XX `PENDIENTE`: **R-22**
(Oleada v10, detalle completo arriba), abierta por grieta de arquitectura verificada —
`capitulos_youtube.py` ya calcula el emparejamiento título↔escena y sus tiempos reales/estimados
(R-07), pero solo los expone en formato de descripción de YouTube, nunca en el formato nativo de
capítulos de ffmpeg que la fase de montaje (T-33) necesita para incrustarlos de verdad en el vídeo
final. `roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo`; el único hallazgo `ABIERTO` de
`auditoriacontinua.md`, `#24` (baja, prosa de "Cola de producto" desactualizada entre ciclos de PM),
sigue enrutado a la pregunta de gobernanza #11 de `SEGUIMIENTO.md` §6, `(pendiente)` de respuesta
del dueño — no es una R-XX. Próximo ciclo de PM: reconfirmar R-22 tras su implementación y, si el
dueño responde entre tanto a la pregunta #11 de §6, aplicar esa respuesta.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
