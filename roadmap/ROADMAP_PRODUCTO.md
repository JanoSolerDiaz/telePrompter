# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-09-29 (ciclo de PM). **Se abre R-19** (Oleada v8): enlazar la toma
buena de cada escena (R-02) con su archivo de vídeo real y generar la lista de concatenación de
ffmpeg (`concat-ffmpeg.txt`), cerrando el hueco explícito entre el parte de rodaje y la fase de
montaje que la propia visión de producto señala como el paso siguiente al reproductor. Es la
primera R-XX nueva desde R-18 (2026-09-17): quince ciclos de PM consecutivos habían reconfirmado la
cola vacía razonando —correctamente, con la información disponible entonces— que esta misma idea
(candidata registrada el 2026-09-21) exigía diseñar superficie de producto nueva sin que ninguna de
las tres fuentes ya establecidas (hallazgo de auditoría, entrada de `FEEDBACK.md`, grieta de
arquitectura verificada) la respaldara, así que quedó aparcada hasta que el bloqueo #7 (grabar un
curso completo) aportara evidencia real.

**Este ciclo cambia esa conclusión por un motivo nuevo, no por descartar el razonamiento
anterior:** el propio encargo de esta rutina programada del dueño (2026-09-29) instruye
explícitamente evolucionar el roadmap hacia el objetivo de producto —"convertir un guión... en
tarjetas... cuya fase siguiente es el montaje con ffmpeg"— priorizando la utilidad real para el
rodaje. Es una cuarta fuente legítima de apertura, distinta de las tres ya establecidas: instrucción
directa del dueño sobre la dirección de producto, no una conjetura del PM. Con esa base, la única
razón que quedaba para aparcarla —ausencia de mecanismo de asociación toma↔archivo— se resuelve con
un diseño acotado que no exige adivinar nada del flujo de grabación del dueño: un campo de texto
opcional, tecleado a mano (el reproductor no tiene ni puede tener acceso al nombre de archivo que
pone la cámara), con degradado explícito y sin fallos cuando falte anotar. Detalle completo de R-19
en "Oleada v8" más abajo; decisión registrada en `DECISIONES_TECNICAS.md`.

Se corrige además, en el mismo ciclo, el hallazgo `#25` de `auditoriacontinua.md` (baja, prosa): la
cifra de "pasadas de auditoría consecutivas esperando la pregunta #11 de §6" que el ciclo de PM del
2026-09-28 dejó en **quince** por error aritmético pasa a la cifra correcta a fecha de hoy
(**trece**: `2026-09-17 a 2026-09-29`, mismo recuento que ya dejó por escrito la propia auditoría
de hoy en `auditoriacontinua.md` #25). El hallazgo `#24` que
motiva esa pregunta sigue `ABIERTO` sin cambios, todavía `(pendiente)` de respuesta del dueño — no
es un hallazgo de producto o arquitectura que este roadmap deba convertir en R-XX.
`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (única fila, plantilla vacía).

Revisión propia de este ciclo: releídos `references/contrato-tomas.md`,
`references/contrato-montaje.md` y `scripts/tomas.py` para especificar R-19 sin adivinar el formato existente;
`scripts/salidas.py` (`TipoSalida`) confirmado como el punto de extensión correcto, mismo patrón
que R-18 usó para añadir `CAPITULOS_YOUTUBE`. Este ciclo es de PM, no de Programador: no se ha
ejecutado la verificación de las cuatro redes; la spec de R-19 queda lista para que el siguiente
ciclo de Programador la implemente y verifique.

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

### Oleada v8 — EN CURSO

> Primera R-XX abierta desde R-18. Cierra el hueco entre el parte de rodaje (R-02) y la fase de
> montaje con ffmpeg que la visión de producto señala como el paso siguiente al reproductor.

#### R-19 — Enlazar la toma buena con su archivo de vídeo real y generar la lista de concatenación de ffmpeg

**Migración:** No (campo opcional con valor por defecto `""`, mismo patrón tolerante que `nota` en
`references/contrato-tomas.md`; `tomas.py` ya lee cada toma campo a campo, no exige un esquema
cerrado) · **Depende de:** R-02, R-05, T-33 · **Origen:** instrucción directa del dueño en el
encargo de este ciclo de PM (2026-09-29) de evolucionar el roadmap hacia la fase siguiente al
reproductor — "el montaje con ffmpeg" —, sobre la candidata ya identificada por observación de
arquitectura del PM el 2026-09-21 (`DECISIONES_TECNICAS.md`).

**Objetivo:** hoy `estado.json["tomas"]` sabe qué escena tiene una toma buena (R-02) y cuánto duró,
pero no qué archivo de la tarjeta de la cámara le corresponde: el dueño tiene que reconstruirlo a
mano, por orden y duración, antes de poder concatenar nada con ffmpeg. Esta tarea añade la única
pieza que falta —el nombre de archivo, tecleado por el propio dueño— y usa lo que ya existe
(R-02, R-05, el contrato de montaje de T-33) para producir directamente la lista de concatenación
lista para `ffmpeg -f concat`, sin que el dueño tenga que escribirla a mano.

**Requisitos:**
1. En el reproductor (`assets/reproductor/guion.js`), cada toma cerrada gana un campo de texto
   opcional "archivo de vídeo" — mismo patrón de edición que la nota rápida de R-03 (tecla
   configurable en `Configuracion.mapa_teclas_reproductor`, por defecto `V`/`v`), editable desde el
   índice en cualquier momento, sin tener que volver a grabar la toma. Vacío por defecto; nunca
   obligatorio para cerrar una toma ni para marcarla `buena`.
2. `references/contrato-tomas.md`: cada toma gana la clave opcional `archivo_video` (string, `""`
   si no se ha anotado), documentada junto a `nota` con el mismo tratamiento; `version` del
   contrato sube a 2 (cambio aditivo, ninguna clave existente cambia de significado).
   `scripts/tomas.py::cargar_parte_de_rodaje` la valida igual que `nota` (texto opcional) y la
   fusiona en `estado.json["tomas"]`; un parte de rodaje o un `estado.json` de antes de R-19 sin
   esta clave se lee igual, con `""` por defecto (sin migración, ver arriba).
3. Nuevo módulo `scripts/concat_ffmpeg.py`: a partir de `EstadoProyecto.tomas` y el orden real de
   escenas del guion (mismo orden que `tarjetas.json`/`guion.srt`,
   `references/contrato-montaje.md`), por cada escena busca su toma `buena` (reutilizando
   `tomas.duracion_toma_buena` tal cual, sin reimplementar la regla de exclusividad de R-11/#16):
   - Si existe y tiene `archivo_video` no vacío → línea `file '<archivo_video>'` en el formato
     exacto del demuxer `concat` de ffmpeg (comillas simples; una comilla simple dentro de la ruta
     se escapa con la secuencia estándar `'\''`).
   - Si la escena no tiene toma buena, o la tiene pero sin `archivo_video` anotado → **nunca** se
     inventa una ruta ni se silencia la escena: se escribe un comentario `# ESCENA <numero>:
     <motivo>` (el demuxer de ffmpeg ignora líneas que empiezan por `#`), con motivo exacto
     (`sin_toma_buena` / `sin_archivo_anotado`), y la escena se cuenta en
     `escenas_pendientes` del resultado devuelto.
4. `TipoSalida` (`scripts/salidas.py`) gana `CONCAT_FFMPEG` como sexta opción — mismo patrón que
   R-18 añadió `CAPITULOS_YOUTUBE`: seleccionable en la pregunta de T-30 solo cuando hay al menos
   una toma registrada (si no hay ningún parte de rodaje, no aparece como opción, igual que
   `CAPITULOS_YOUTUBE` sin sección `Capítulos`); nunca falla por escenas pendientes de anotar — el
   archivo se genera siempre que se seleccione, con esas escenas documentadas como comentario, y
   `ResumenSalidas` informa cuántas quedan pendientes y de qué motivo.
5. Salida nueva `concat-ffmpeg.txt` (`config.NOMBRE_ARCHIVO_CONCAT_FFMPEG`) en la carpeta de salida
   del guion. `references/contrato-montaje.md` documenta el archivo (opcional; solo existe si se
   seleccionó con al menos una toma) y deja explícito que la cadena de montaje debe tratar
   cualquier línea que empiece por `#` como escena todavía sin archivo real, nunca como error de
   formato.
6. Invariantes (a)/(d) de §0.2 intactas: anotar, editar o borrar un `archivo_video` nunca descarta
   la toma ni ninguno de sus campos existentes (`duracion_segundos`, `nota`, `buena`); es un campo
   más que se fusiona igual que el resto de `tomas.py`, nunca un reemplazo destructivo.

**Criterio de aceptación:** con un parte de rodaje donde todas las escenas con toma buena tienen
`archivo_video` anotado, `concat-ffmpeg.txt` generado es exactamente el formato que espera
`ffmpeg -f concat -safe 0 -i concat-ffmpeg.txt`, verificado con un test que lo parsea con esas
mismas reglas; con una mezcla de escenas anotadas, sin anotar y sin toma buena, el archivo se
genera igual, cada pendiente aparece como comentario con su motivo exacto y `ResumenSalidas` cuenta
las pendientes; sin ningún parte de rodaje registrado, `CONCAT_FFMPEG` no aparece como opción
seleccionable (mismo patrón de test que R-18 verificó para `CAPITULOS_YOUTUBE`); una ruta con una
comilla simple se escapa correctamente y el archivo resultante sigue siendo válido para el demuxer
`concat`.

---

### Cola de producto

`ROADMAP_PRODUCTO.md` tiene, en este ciclo (2026-09-29), una única R-XX `PENDIENTE`: **R-19**
(Oleada v8, detalle completo arriba), recién abierta por instrucción directa del dueño en el
encargo de este ciclo de PM — ver cabecera para el razonamiento completo de por qué se abre ahora
y no en los quince ciclos anteriores. `auditoriacontinua.md` no aporta ningún otro hallazgo que
enrutar (único `ABIERTO` restante, `#24`, ya enrutado como pregunta de gobernanza en §6 #11 de
`SEGUIMIENTO.md`, ajena al contenido de este roadmap; `#25` corregido en este mismo ciclo, ver
cabecera) y `roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo`. Próximo ciclo de PM: reconfirmar
R-19 tras su implementación y, si el dueño responde entre tanto a la pregunta #11 de §6, aplicar esa
respuesta.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
