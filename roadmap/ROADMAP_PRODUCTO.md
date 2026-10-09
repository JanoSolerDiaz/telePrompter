# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-10-09 (ciclo de PM). **R-26 (Oleada v14) está `COMPLETADA`** (§1 de
`SEGUIMIENTO.md`) desde el ciclo de Programador del 2026-10-09 que la implementó (el diccionario del
dueño, `diccionario-locucion.json`, queda conectado de verdad a la generación y a la revalidación).
Igual que R-25, la fila de §1 se añadió en el mismo commit que la implementó, así que no hay prosa
desactualizada que corregir. Movida a `roadmap/ROADMAP_HISTORICO.md` (Oleada v14) junto con el resto
de oleadas 100 % entregadas.

**Se abre R-27** (Oleada v15): no por hallazgo de auditoría ni entrada de `FEEDBACK.md` — ninguna de
las dos fuentes aporta nada nuevo este ciclo (ver abajo) — sino por **grieta de arquitectura
verificada sobre código ya construido**, el mismo criterio que abrió R-12 a R-26. Verificación propia,
leyendo el código línea a línea: `scripts/estado.py::avisar_si_guion_modificado` (T-07, 2026-09-01)
existe exactamente para avisar al dueño cuando el guion de origen cambió desde la última pasada
("se recalcularán escenas, clasificación y tiempos en la próxima pasada", en vez de dejarlo
descubrirlo por sorpresa) — pero no tiene **ningún** llamador fuera de sus propios tests, confirmado
con `grep -rn "guion_modificado" scripts/*.py`: solo aparece en su propia definición y en su propia
llamada interna a `guion_modificado(...)`. `SKILL.md` no menciona esta función en ningún punto del
flujo documentado (confirmado con `grep -n "guion_modificado" SKILL.md`, sin resultado), así que ni
siquiera está como paso de la receta que sigue la sesión que orquesta la skill — el mismo tipo de hueco
de instrucción, no solo de código, que ya cerró R-26. Peor aún: aunque se llamara hoy mismo, el aviso
quedaría roto por un segundo defecto — `estado.guion.hash_sha256`/`tamano_bytes` (`InfoGuion`) solo se
escriben una vez, en `estado_inicial` (`scripts/estado.py:121-135`), y ningún punto del código los
vuelve a actualizar después (confirmado con `grep -rn "InfoGuion(" scripts/*.py`: un único resultado
fuera de `desde_dict`, el de `estado_inicial`). El resultado práctico: en cuanto el guion cambia una
vez, el aviso —si se wireara tal cual, sin más— se repetiría en TODAS las pasadas futuras para
siempre, incluso después de que el dueño ya lo haya visto y vuelto a generar/revalidar, porque nada
refresca el hash guardado contra el que se compara. No es una salida huérfana sin consumidor (patrón
de R-18 a R-25): es, igual que R-26, una garantía de transparencia explícita en el propio docstring de
la función y en `DEVELOPERS.md` que hoy no se sostiene en el flujo real, y que de conectarse mal
degradaría en ruido permanente en vez de señal. Detalle completo en "Oleada v15" más abajo.

`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (única fila, plantilla vacía): no hay
historia de rodaje real que incorporar este ciclo — el bloqueo #7 de `SEGUIMIENTO.md` §3 (grabar un
curso completo) sigue abierto. El registro de hallazgos de `auditoriacontinua.md` no trae ningún
`ABIERTO` nuevo de producto/arquitectura esta pasada: queda un único `ABIERTO` (`#24`, prosa de "Cola
de producto" desactualizada entre ciclos de PM, de proceso y severidad baja), que no necesita una
R-XX — sigue pendiente solo de la respuesta del dueño a la pregunta de gobernanza #11 de
`SEGUIMIENTO.md` §6.

Este ciclo es de PM, no de Programador: no se ha ejecutado la verificación de las cuatro redes; la
spec de R-27 queda lista para que el siguiente ciclo de Programador la implemente y verifique.

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

### Oleada v15 — EN CURSO

#### R-27 — El aviso de guion modificado (`avisar_si_guion_modificado`, T-07) no tiene ningún llamador real, y el hash guardado en `estado.json` nunca se refresca para que el aviso no se repita sin motivo

**Migración:** No (ningún campo nuevo en `estado.json`; refresca valores ya existentes de `InfoGuion`
tras cada pasada, mismo esquema) · **Depende de:** T-07, T-16 (ambas ya `COMPLETADA`) · **Origen:**
observación de arquitectura del PM (2026-10-09) — grieta de arquitectura verificada sobre código ya
construido (mismo criterio que abrió R-12 a R-26).

**Objetivo:** T-07 (2026-09-01) construyó `scripts/estado.py::guion_modificado`/
`avisar_si_guion_modificado` con un propósito explícito, documentado en su propio docstring y en
`DEVELOPERS.md`: comparar el hash del guion de origen contra el que quedó guardado en `estado.json` la
última vez, y avisar al dueño por `presentacion.py` cuando difieren — "en vez de fallar en silencio con
datos desactualizados", eco literal del principio de producto nº 1 ("nada se descarta en silencio").
Verificado leyendo el código, no solo el docstring: `grep -rn "guion_modificado" scripts/*.py` solo
devuelve la propia definición de las dos funciones y la llamada interna de
`avisar_si_guion_modificado` a `guion_modificado` — ningún otro módulo de `scripts/` las importa ni las
invoca. `grep -n "guion_modificado" SKILL.md` no devuelve ningún resultado: el paso no está ni siquiera
mencionado en la receta que sigue la sesión que orquesta la skill, a diferencia de otros pasos
explícitos ya documentados (el diccionario del dueño, R-26; `tropiezos_por_escena`, R-03). El dueño
puede editar el guion de origen entre una pasada y la siguiente (corregir una frase, añadir una
escena) y hoy no recibe ninguna señal de que eso ocurrió, pese a que la función que se la daría ya
existe, está probada (`tests/test_estado.py`) y documentada.

El hueco tiene una segunda capa que agrava el wiring ingenuo: `InfoGuion.hash_sha256`/`tamano_bytes`
(el valor contra el que se compara) solo se escriben una vez, en `estado_inicial`
(`scripts/estado.py:121-135`) — confirmado con `grep -rn "InfoGuion(" scripts/*.py`, que solo
devuelve esa construcción y la de `desde_dict` (reconstrucción desde el JSON ya guardado, no una
escritura nueva). Ningún punto del código actualiza esos dos campos después de la primera vez. Si
`avisar_si_guion_modificado` se llamara tal cual, sin más, en cada generación/revalidación: la primera
vez que el guion cambiara el aviso sería correcto, pero **todas las pasadas futuras volverían a avisar
igual**, aunque el dueño ya lo haya visto y haya vuelto a generar o revalidar sobre el guion ya
cambiado — el hash guardado nunca se pone al día, así que la comparación sigue siendo contra el
original de hace semanas. Eso convertiría una señal útil en ruido permanente, el mismo tipo de defecto
de diseño que esta tarea debe prevenir, no solo el wiring que falta. A diferencia de las grietas de
R-18 a R-25 (una salida o un cálculo sin consumidor, valor perdido pero sin promesa incumplida), esta
es, igual que R-26, una garantía de transparencia explícita del propio código y de `DEVELOPERS.md` que
hoy no se sostiene en el flujo real.

Candidata alternativa descartada tras la misma pasada de verificación:
`scripts/entrada.py::ejecutar_con_limite_de_tiempo` (T-06, tope de tiempo de proceso) tampoco tiene
llamador real fuera de sus propios tests ni mención en `SKILL.md`. Se descarta por menor severidad y
menor evidencia de riesgo real: a diferencia del aviso de guion modificado (que el dueño notaría
directamente al no ver la señal prometida la próxima vez que edite su guion), el límite de tiempo es
una defensa en profundidad contra un escenario que las guardas ya activas de T-06
(`TAMANO_GUION_MAX_BYTES`, `ESCENAS_MAX`, aplicadas ANTES de parsear) hacen poco probable en la
práctica, y `roadmap/SEGUIMIENTO.md` §4 (incidentes de deploy) no registra ningún episodio de proceso
descontrolado en las más de cien sesiones que lleva el proyecto. Queda anotado aquí por si una futura
pasada encuentra evidencia que cambie esta valoración.

**Requisitos:**
1. `scripts/estado.py` gana una función nueva (el nombre exacto lo decide quien implemente, p. ej.
   `actualizar_info_guion(estado, ruta_guion)`) que refresca `estado.guion.hash_sha256`/`tamano_bytes`
   al contenido actual del archivo. Se llama justo antes de `guardar_estado`, en cualquier pasada que
   regenere o revalide sobre un guion con `estado.json` ya existente — así el aviso compara siempre
   contra el estado real de la última vez que se procesó, no contra el de la primera vez que se creó
   `estado.json`.
2. `documento_revision.generar_documento_revision` gana un parámetro opcional
   `guion_modificado: bool = False` (mismo patrón que `tropiezos_por_escena` de R-03): cuando es
   `True`, la cabecera del resumen global añade una línea visible avisando de que el guion de origen
   cambió desde la última pasada y que escenas, clasificación y tiempos se recalcularon desde cero —
   mismo criterio de transparencia que ya aplican el ppm (T-12), el diccionario del dueño (R-26) y las
   desviaciones de convención (R-23). El dueño revisa `guion-escenas.md` "de una sola pasada"
   (principio de producto nº 2); un aviso que solo aparece en la consola de la sesión y no en el
   documento que de verdad revisa se pierde con facilidad.
3. `SKILL.md` dedica una instrucción explícita, con el fragmento de código exacto a invocar (mismo
   patrón ya usado para el diccionario del dueño en R-26): tras cargar `estado.json` y ANTES de
   re-parsear/regenerar, llamar a `estado.avisar_si_guion_modificado(estado, ruta_guion)` — su valor de
   retorno se pasa tal cual a `generar_documento_revision(..., guion_modificado=...)` — y llamar a la
   función del requisito 1 justo antes de `guardar_estado`. No una mención en una tabla de valores por
   defecto: un paso nombrado del flujo que Claude no pueda pasar por alto, igual que exige R-26
   (requisito 3) para el diccionario.
4. Fuera de alcance, explícito: no se construye recálculo incremental (T-07 ya documenta que no existe
   todavía, y esta tarea no es quien debe construirlo); no cambia el formato ni el esquema de
   `estado.json` (solo refresca valores ya existentes de `InfoGuion`, sin migración); `revalidar_guion`
   no gana ningún parámetro nuevo ni lee el guion de origen por su cuenta — sigue intacto el invariante
   explícito de su propio docstring ("no relee el guion de origen del disco"); `tarjetas.json.metadatos`
   no gana ningún campo nuevo por esta tarea (a diferencia del recuento del diccionario en R-26, que sí
   afecta al contenido locutado de las tarjetas, este aviso es sobre el propio `guion-escenas.md` que el
   dueño ya revisa antes de llegar a generar salidas); no se toca `ejecutar_con_limite_de_tiempo` ni
   ninguna pieza de T-06.

**Criterio de aceptación:** test que confirma que la función del requisito 1 deja
`estado.guion.hash_sha256`/`tamano_bytes` iguales al hash/tamaño actuales del archivo tras llamarla;
test que confirma que, tras esa actualización y sin que el guion vuelva a cambiar,
`avisar_si_guion_modificado` devuelve `False` (cierra el bucle: el aviso aparece una vez, no en todas
las pasadas siguientes); test que confirma que la cabecera de `guion-escenas.md` incluye la línea de
aviso cuando `guion_modificado=True` y ninguna línea nueva cuando es `False` (el valor por defecto);
regresión de los tests existentes de T-07/T-16 sin cambios de comportamiento. Cuatro redes en verde.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
