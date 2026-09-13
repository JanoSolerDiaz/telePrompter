# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-09-13 (ciclo de PM). `auditoriacontinua.md` no deja ningún hallazgo
`ABIERTO` nuevo sin enrutar (`#22`, media, ya enrutado a R-15 el 2026-09-12, sigue `PENDIENTE` de
implementar por el programador; `#19`, baja, reconfirmado sin cambios en la pasada del auditor de
hoy, mantiene su decisión razonada de no convertirse en R-XX especulativa). `roadmap/FEEDBACK.md`
sigue sin ninguna entrada `nuevo` (bloqueo #7 de `SEGUIMIENTO.md` §3 — grabar un curso completo —
sigue sin resolverse). Con los hallazgos de auditoría ya agotados y sin feedback real de rodaje,
este ciclo repasa de nuevo `references/contrato-montaje.md` y `references/contrato-tarjetas.md`
—el contrato exacto con la fase siguiente del propio dueño, el montaje con ffmpeg— y esta vez sí
encuentra una inconsistencia de arquitectura real, del mismo tipo que ya motivó R-12/R-13/R-14: el
propio `contrato-montaje.md` **obliga a la cadena de montaje a reimplementar a mano** la fórmula de
acumulación de duraciones (sumar `duracion_estimada_segundos`/`duracion_real_segundos` en orden)
solo para saber dónde empieza y termina cada escena, en vez de leerlo ya calculado — exactamente el
cálculo que T-12/R-13 ya hacen una vez, de forma correcta y probada, dentro de esta skill. Se abre
**R-16** (oleada v6 nueva) para cerrar esa grieta: añadir `inicio_segundos`/`fin_segundos` ya
resueltos a cada escena de `tarjetas.json`, antes de que exista una skill de montaje real que
tenga que descubrir la discrepancia con datos de producción.

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

### Fase transversal F-H — Deuda técnica menor (entorno de verificación)

Agrupa hallazgos de calidad/infraestructura menores, sin hito de producto propio, con el mismo
criterio que ya usaron F-D (R-08/R-09), F-F (R-11) y F-G (R-14). Contiene R-15, su única R-XX por
ahora.

#### R-15 — Advertir explícitamente contra el binario "pelado" de `ruff`/`mypy`/`pytest` en un contenedor de nube
**Oleada / Fase:** F-H · **Migración:** No · **Depende de:** ninguna
**Origen:** auditoría `#22` (2026-09-12)

**Objetivo:** este contenedor de nube trae, además de las versiones exactas que instala `pip
install -r requirements-dev.txt` (`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`, resueltas en
`sys.executable`), un segundo juego de los mismos tres binarios preinstalado en
`/root/.local/bin` (`mypy 1.19.1`, `ruff 0.15.8`, `pytest 9.0.2`), con esa ruta por delante en el
`PATH`. Las cuatro verificaciones reales del protocolo (`scripts/ci.py`, el hook de pre-commit) son
inmunes porque invocan siempre `sys.executable -m <herramienta>`, nunca el nombre pelado — pero un
humano o una sesión que teclee `ruff check .`, `mypy scripts tests` o `pytest` a mano en la
terminal recibe una señal distinta y, en el caso de `mypy`, activamente engañosa: 34 errores falsos
de `import-not-found` (ese entorno aislado no ve el `pytest` instalado en `dist-packages`), más los
`Untyped decorator` en cascada que provoca cada decorador de test sin tipos resueltos. El objetivo
es dejar una advertencia explícita en los dos sitios que cualquier sesión futura consulta antes de
tocar código, para que nadie pierda tiempo investigando una "regresión de tipos" que no existe.

**Requisitos:**
1. Añadir una nota breve y visible en `DEVELOPERS.md` (sección de verificación/desarrollo): la
   única verificación válida es `python scripts/ci.py` (o `python -m mypy`/`python -m ruff`/
   `python -m pytest` si se ejecutan sueltos); nunca el binario pelado (`ruff`, `mypy`, `pytest`
   sin `python -m` por delante), porque un contenedor de nube puede traer un segundo juego
   preinstalado, más nuevo que el pineado en `requirements-dev.txt` y por delante en el `PATH`, que
   da una señal distinta y en el caso de `mypy` puede devolver errores de `import-not-found` que no
   existen en la verificación real.
2. Añadir la misma advertencia, en una frase, a la sección de verificación de `SKILL.md` si la
   tiene, o como mínimo una referencia a `DEVELOPERS.md` desde ahí.
3. Tarea puramente documental: sin cambio de comportamiento en `scripts/ci.py` ni en ningún otro
   módulo — el propio hallazgo `#22` confirma que el protocolo real ya es inmune al binario pelado.
4. Sin cambio de esquema de `estado.json` ni de `Configuracion`.

**Criterio de aceptación:** `DEVELOPERS.md` contiene la advertencia explícita citando
`scripts/ci.py` (o `python -m <herramienta>`) como única fuente de verdad de la verificación y
mencionando el riesgo del binario pelado en un contenedor de nube; cero cambio en `scripts/`,
`tests/` o `assets/`; la siguiente pasada del auditor verifica la nota y cierra `#22` a `RESUELTO`.

---

### Oleada v6 — Cierre del contrato de montaje: límites de escena listos para ffmpeg

Convierte en tarea una inconsistencia de arquitectura verificada en el código y en la documentación
del propio contrato, con el mismo criterio que ya usaron R-12/R-13/R-14 (observación del PM,
confirmada leyendo el módulo real antes de escribir la ficha). Contiene R-16, su única R-XX por
ahora.

#### R-16 — Límites absolutos de escena (`inicio_segundos`/`fin_segundos`) en `tarjetas.json`
**Oleada / Fase:** v6 · **Migración:** No · **Depende de:** T-33, R-13
**Origen:** observación de arquitectura del PM (2026-09-13), releyendo `references/contrato-montaje.md`
a la luz de que la fase siguiente del propio dueño es el montaje con ffmpeg

**Objetivo:** hoy `references/contrato-montaje.md` (T-33) le pide **a la cadena de montaje** que
derive el rango `[inicio_escena, fin_escena)` de cada escena sumando a mano, en orden,
`duracion_real_segundos` si existe o si no `duracion_estimada_segundos` (la misma regla que ya
implementa `mezcla_duracion_real_y_estimada` de R-13) — es la única forma documentada de saber a
qué escena pertenece un subtítulo de `guion.srt`/`guion-alineado.srt`, y la propia página advierte
de que esa fórmula deja de ser válida en cuanto existe parte de rodaje. Es exactamente el tipo de
cálculo que esta skill ya resuelve una sola vez, de forma correcta y probada (T-12
`tiempos.calcular_tiempos`, R-05, R-13): pedirle a un consumidor externo —hoy sin implementar
todavía, mañana la propia skill de montaje con ffmpeg— que la reproduzca bit a bit es aceptar un
punto de deriva silenciosa (redondeos, elegir real vs. estimada escena a escena, un futuro cambio
en T-12 que la cadena de montaje no se entera de seguir) justo en el borde entre dos sistemas, que
es donde este tipo de errores es más caro de diagnosticar. Cerrar la grieta ahora —antes de que
exista una skill de montaje real que la sufra con datos de producción— es más barato que
descubrirla después.

**Requisitos:**
1. `Tarjeta` (`scripts/pptx.py`) gana dos campos nuevos, `inicio_segundos`/`fin_segundos` (float),
   calculados **una sola vez** con la misma regla que ya usa R-13 para elegir real vs. estimada
   escena a escena, acumulando en el mismo orden en que las escenas aparecen en
   `resultado.escenas` — nunca una segunda implementación de la lógica de T-12/R-13, reutilizar la
   que ya exista o extraerla si hace falta compartirla.
2. `tarjetas_a_diccionario`/`validar_tarjetas` y `references/contrato-tarjetas.md` documentan las
   dos claves nuevas en la tabla de cada escena. Cambio **aditivo y retrocompatible** (mismo
   criterio que R-13): no sube `version_contrato`.
3. `references/contrato-montaje.md` deja de pedirle a la cadena de montaje que "sume las
   duraciones anteriores": la sección de cómo derivar el tiempo de cada escena pasa a decir que se
   lean `inicio_segundos`/`fin_segundos` directamente de `tarjetas.json`, dejando la fórmula de
   acumulación como nota de cómo se calculan (transparencia), no como instrucción a seguir.
4. Test de integración nuevo o ampliado en `tests/test_integracion_montaje.py`: `inicio_segundos`
   de la primera escena es `0`; `fin_segundos` de una escena coincide con `inicio_segundos` de la
   siguiente (sin huecos ni solapes); `fin_segundos` de la última escena coincide con el fin del
   último subtítulo de `guion.srt` (caso sin parte de rodaje) y de `guion-alineado.srt` (caso con
   parte de rodaje que mezcla real/estimado, reutilizando el guion sintético que ya prueba R-13).
5. Sin migración de `estado.json`, sin campo nuevo de `Configuracion` (son datos derivados de T-12,
   no un valor configurable por el dueño).

**Criterio de aceptación:** sobre los tres guiones reales de `fixtures/reales/`,
`inicio_segundos`/`fin_segundos` de `tarjetas.json` reconstruyen exactamente los límites de escena
que hoy exige calcular a mano `contrato-montaje.md`, tanto con todas las escenas estimadas como con
un parte de rodaje que mezcla real/estimado; el test de integración cruzada nuevo pasa;
`contrato-montaje.md` y `contrato-tarjetas.md` quedan actualizados.

---

### Cola de producto

`ROADMAP_PRODUCTO.md` tiene dos R-XX pendientes en este ciclo: **R-15** (F-H), origen directo de un
hallazgo real del auditor (`#22`), y **R-16** (oleada v6), origen en una inconsistencia de
arquitectura verificada por el PM en el contrato de montaje. No hay ninguna otra R-XX `PENDIENTE`
ni `EN CURSO`: el resto del roadmap sigue a la espera de una entrada real en `FEEDBACK.md`, de un
nuevo hallazgo de `auditoriacontinua.md`, o de que el dueño complete el criterio de salida de la
oleada v1 (grabar un curso entero, bloqueo #7 de `SEGUIMIENTO.md` §3) y aporte fricciones reales de
rodaje.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
