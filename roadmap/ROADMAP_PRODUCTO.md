# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-09-12 (ciclo de PM). Se abre **R-15** (fase transversal F-H nueva):
único hallazgo `ABIERTO` sin enrutar de `auditoriacontinua.md` en esta pasada, `#22` (media,
2026-09-12) — el contenedor de nube trae un segundo juego de `ruff`/`mypy`/`pytest` preinstalado,
más nuevo que el pineado en `requirements-dev.txt` y por delante en el `PATH`, que da una señal
distinta y, en el caso de `mypy`, activamente engañosa (34 errores falsos) a quien lo invoque
pelado en vez de con `python scripts/ci.py`. Es un hallazgo de calidad/infraestructura, no de
producto, pero el propio auditor señala que merece una nota explícita en la documentación para que
ninguna sesión futura pierda tiempo con esa falsa señal — mismo criterio que ya usaron F-D
(R-08/R-09) y F-F (R-11) para agrupar deuda técnica menor en una R-XX. El otro hallazgo `ABIERTO`,
`#19` (baja, límite teórico y sin escenario reproducido de `revalidacion.py`), se reconfirma sin
cambios: sigue con la decisión razonada del ciclo de PM del 2026-09-04 de NO abrir una R-XX
especulativa mientras no se reproduzca un caso real, reconfirmada por el auditor en cada pasada
desde entonces (incluida la de hoy) sin novedad; este ciclo no encuentra motivo para revisarla.
`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (bloqueo #7 de `SEGUIMIENTO.md` §3 — grabar
un curso completo — sigue sin resolverse, así que ni la calibración de ppm de R-04 ni el ciclo de
mejora de producto tienen todavía evidencia real de rodaje). Este ciclo repasa también, con lectura
directa de `references/contrato-montaje.md` y `references/contrato-tarjetas.md` a la luz de R-13/
R-14 ya entregadas, si queda alguna inconsistencia de arquitectura del mismo tipo que ya motivó
R-12/R-13/R-14: ninguna encontrada. No se abre ninguna R-XX de producto especulativa: R-15 es la
única apertura de este ciclo y tiene origen trazable en un hallazgo real del auditor, no en una
mejora inventada.

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

### Cola de producto

`ROADMAP_PRODUCTO.md` tiene una única R-XX pendiente en este ciclo: **R-15** (F-H, arriba), origen
directo de un hallazgo real del auditor (`#22`). No hay ninguna otra R-XX `PENDIENTE` ni `EN CURSO`:
el resto del roadmap sigue a la espera de una entrada real en `FEEDBACK.md`, de un nuevo hallazgo de
`auditoriacontinua.md`, o de que el dueño complete el criterio de salida de la oleada v1 (grabar un
curso entero, bloqueo #7 de `SEGUIMIENTO.md` §3) y aporte fricciones reales de rodaje.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`. El formato de ficha de una R-XX nueva
—Oleada/Fase, Migración, Depende de, Origen, Objetivo, Requisitos, Criterio de aceptación— es el
mismo que se ve en el detalle de cualquier R-XX ya archivada en `ROADMAP_HISTORICO.md`.)*
