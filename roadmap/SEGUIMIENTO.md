# SEGUIMIENTO — teleprompter — Hub / panel de control

> Hub del registro repartido (ver §0.4 de `HOJA_DE_RUTA.md`). Aquí viven el estado y lo
> transversal; el detalle vive en los documentos vivos de `roadmap/`.
> El dueño no revisa el código: revisa este documento.
>
> **Documentos hermanos:** las **decisiones técnicas** están en `DECISIONES_TECNICAS.md`
> (antiguo §2) y la **bitácora de sesiones** en `HISTORIAL_SESIONES.md` (antiguo §8). Las
> secciones no se renumeran para no romper referencias.

**Hoja de ruta de referencia:** `HOJA_DE_RUTA.md` v1.3 (2026-08-31)
**Modo de operación:** AUTONOMÍA TOTAL
**Última actualización:** 2026-10-14 — **Ciclo de Programador: R-29 implementada** (detalle en la
nota de esta sesión, más abajo).

**Ciclo de Programador (2026-10-14): R-29 implementada.** Revisión de entrada (protocolo):
`git checkout develop && git pull origin develop` sin sorpresas (rama local ya al día tras el
fast-forward hasta `8fc4106`, la auditoría del 2026-10-14 ya empujada); `git status` limpio.
Dependencia de desarrollo instalada con `python3 -m pip install -r requirements-dev.txt` (no el
`pip` desnudo del `PATH`, que sigue resolviendo contra el intérprete equivocado del contenedor —
síntoma ya documentado por `#28`/P-06).

Registro de hallazgos de `auditoriacontinua.md` (auditoría 2026-10-14): dos `ABIERTO`, ambos de
proceso puro y sin relación con el código (`#24`, prosa de "Cola de producto" desactualizada entre
ciclos; `#30`, cadencia del Programador) — ninguno de severidad alta que atender como P-XX urgente
antes de la cola normal. §1 (fuente autoritativa) traía **R-29 como única fila `PENDIENTE`**:
implementada en esta sesión siguiendo al pie de la letra su spec de `ROADMAP_PRODUCTO.md` (Oleada
v17, verificada contra `DECISIONES_TECNICAS.md` antes de tocar código, sin contradecir ninguna
decisión previa).

**Investigación (requisito 1).** Dos tests nuevos en `tests/test_revalidacion.py` comparan, bloque
a bloque, la materialización de `revalidacion._materializar_marcados` contra una llamada directa a
`reescrituras.aplicar_particiones_aceptadas` sobre los mismos bloques de origen, sin ningún
conflicto edición/partición pendiente: uno sobre los tres guiones reales (ninguno propone hoy
ninguna partición de respiración, verificado antes de escribir el test — T-11 ya los trocea sin
dejar frases candidatas) y otro sobre los guiones sintéticos ya existentes en el archivo que sí
proponen particiones de verdad (`_GUION`, una partición; `_GUION_ESCENA_DOS_PARTICIONES`, dos en la
misma escena). Las dos rutas coinciden exactamente en los tres casos: no hay divergencia real que
corregir (requisito 3 no aplica), tal como anticipaba la lectura línea a línea del commit de
apertura de R-29.

**Unificación (requisito 2).** `revalidacion._particion_aceptada_de` deja de reimplementar a mano
las cuatro condiciones de emparejamiento y pasa a invocar
`reescrituras.aplicar_particion_aceptada` sobre una lista de un único bloque: si el resultado tiene
longitud 2, coincidió y las dos mitades son su texto; si tiene longitud 1, no coincidió y el bloque
vuelve intacto. `revalidacion.py` deja de importar `SEPARADOR_MITADES`/`FAMILIA_PARTICION_RESPIRACION`/
`DECISION_ACEPTADA` de `reescrituras.py` (ya no los usa). La salvaguarda de
`indices_con_edicion_previa_a_particion` (P-02/P-04, hallazgo #9) no se tocó — sigue decidiendo,
antes de llamar a `_particion_aceptada_de`, si procede buscar partición para ese bloque; no hizo
falta ni filtrar la lista de reescrituras ni extender la función pública, porque esa salvaguarda ya
actuaba como guardia de entrada, no como parte del cálculo de emparejamiento en sí. Razonamiento
completo de las tres alternativas consideradas en `DECISIONES_TECNICAS.md`.

**Verificación.** 2 tests nuevos (673→675):
`test_materializacion_revalidacion_coincide_con_aplicar_particiones_tres_guiones_reales` y
`test_materializacion_revalidacion_coincide_con_aplicar_particiones_con_particiones_reales` en
`tests/test_revalidacion.py`. Los 20 tests ya existentes del archivo pasan sin cambio de
comportamiento, incluidos los dos que fijan el hallazgo #9
(`test_edicion_manual_y_particion_aceptada_misma_pasada_no_pierde_edicion`,
`test_revalidacion_posterior_al_conflicto_no_duplica_bloques`). Cuatro redes en verde (`mypy`,
`ruff`, 675 tests, dieciocho etapas de `verificar_salidas.py --fixture`).

Sin cambios en §3 (bloqueos) ni §7 (desviaciones). §5: sin ningún P-XX nuevo (la cola normal cubría
el trabajo de esta sesión). §6: preguntas `#11`/`#12` siguen `(pendiente)` de respuesta del dueño,
sin novedad de esta sesión. `ROADMAP_PRODUCTO.md` no se toca en esta sesión (su prosa de "Oleada
v17 — EN CURSO"/R-29 queda desactualizada hasta el próximo ciclo de PM que la archive — mismo
patrón ya descrito y aceptado como de bajo riesgo en el hallazgo `#24`, pendiente solo de la
respuesta de gobernanza del dueño a la pregunta `#11`).

**Ciclo de Product Manager (2026-10-13).** Revisión de entrada (protocolo): `git checkout develop
&& git pull origin develop` sin ninguna divergencia que resolver (fast-forward limpio hasta
`371e523`, la novena reconfirmación del Programador tras R-28, ya empujada); `git status` limpio.
Dependencias de desarrollo instaladas con `pip install -r requirements-dev.txt`.

Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: dos `ABIERTO`, ambos de
proceso puro y sin relación con el código (`#24`, baja; `#30`, media), ninguno de severidad alta que
atender antes de la cola normal — ambos siguen pendientes solo de la respuesta del dueño a las
preguntas de gobernanza `#11`/`#12` de §6, sin novedad. §1 (fuente autoritativa): R-28
`COMPLETADA` desde el ciclo de Programador de esta misma jornada (commit `b990a1c`), sin ningún
hito de negocio propio pendiente. `roadmap/FEEDBACK.md` revisado de nuevo: sigue con su única fila
de plantilla vacía, sin ninguna entrada `nuevo` — el bloqueo #7 (grabar un curso completo) sigue
abierto, así que no hay historia de rodaje real que incorporar este ciclo.

**Archiva Oleada v16 (R-28)** a `roadmap/ROADMAP_HISTORICO.md` (spec completa + "Cómo se
entregó"). `ROADMAP_PRODUCTO.md` corregido en el mismo ciclo que archiva.

**Abre R-29 (Oleada v17).** Grieta de arquitectura verificada, mismo criterio que abrió R-12 a
R-28, pero de una forma distinta a las diez repeticiones anteriores: no es una pieza huérfana sin
ningún llamador, sino una pieza construida y documentada exactamente para ser reutilizada por la
ruta real (`scripts/reescrituras.py:61-63`, comentario explícito: "Público... porque T-17
(revalidacion) necesita partir `propuesta`... con la misma identidad que `aplicar_particion_
aceptada`") que la ruta real **reimplementa en privado** en vez de invocar —
`revalidacion.py::_particion_aceptada_de`/`_materializar_marcados` calculan a mano, con las mismas
cuatro condiciones, el mismo emparejamiento bloque↔reescritura que ya ofrecen las funciones públicas
`reescrituras.py::aplicar_particion_aceptada`/`aplicar_particiones_aceptadas`, sin llamarlas nunca.
Riesgo real: es el área exacta de dos incidencias de severidad alta ya cerradas en este proyecto
(P-02, P-04, invariante (c) — "la edición manual manda") y hoy dos copias de la misma regla se
mantienen a mano en dos archivos sin ningún test que las compare entre sí. Localización delegada a
un agente Explore (instruido para no repetir candidatas ya descartadas en ciclos anteriores),
verificada después línea a línea de forma independiente (`grep -rn "aplicar_particion"
scripts/ tests/`, lectura directa de `reescrituras.py:322-369` y `revalidacion.py:190-244`) antes de
escribir la spec. Tres candidatas más del mismo agente descartadas en la misma pasada —
`monitorizacion.ejecutar_con_diagnostico` (ya evaluada y descartada explícitamente al abrir R-24,
2026-10-06: semántica de abortar el proceso que no encaja), `monitorizacion.ResumenEjecucion`
(sustituida para el consumidor real por `salidas.ResumenSalidas`, T-30) y
`normalizacion.deshacer_normalizaciones` (prueba de propiedad sin hueco real de consumidor) —. Detalle
completo, decisiones y candidatas descartadas en `ROADMAP_PRODUCTO.md` (Oleada v17) y
`DECISIONES_TECNICAS.md` ("PM (apertura de R-29)"). Fila añadida a §1 en este mismo ciclo.

Sin cambios en §3 (bloqueos) ni §5 (P-XX); §6 sin novedad (`#11`/`#12` siguen `(pendiente)`); sin
nueva desviación en §7. Este ciclo es de PM, no de Programador: no se ha ejecutado la verificación
de las cuatro redes ni se ha tocado `scripts/`, `tests/` ni `assets/`.

**Última actualización anterior (2026-10-13, ciclo de Programador): novena reconfirmación del día
tras R-28**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Ciclo de Programador (2026-10-13), novena reconfirmación del día tras R-28.** Revisión de
entrada (protocolo): `git checkout develop && git pull origin develop` encontró el contenedor de
nuevo con `HEAD` *detached* y la rama local nueve commits por detrás de `origin/develop`
(`7b178b8`, la octava reconfirmación de esta misma jornada, ya empujada); el `checkout` y el
`pull` avanzaron por fast-forward sin ninguna divergencia real que resolver (nada parecido al
artefacto de clon superficial del hallazgo `#21`). `git status` limpio antes y después.
Dependencias de desarrollo instaladas primero con el `pip` desnudo del `PATH` (mismo síntoma ya
documentado por `#28`/P-06: resuelve contra el intérprete equivocado y deja `mypy`/`ruff`/`pytest`
sin instalar) y reinstaladas con `python3 -m pip install -r requirements-dev.txt`, tras lo cual
las cuatro redes dieron `OK` (`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

Registro de hallazgos de `auditoriacontinua.md` (auditoría 2026-10-13, sin cambios desde la última
lectura): dos `ABIERTO`, ambos de proceso puro y sin relación con el código (`#24`, prosa de "Cola
de producto" desactualizada entre ciclos de PM; `#30`, cadencia de la rutina Programador) —
ninguno de severidad alta que atender como P-XX urgente antes de la cola normal, ambos pendientes
solo de la respuesta del dueño a las preguntas de gobernanza `#11`/`#12` de §6. §1 (fuente
autoritativa) **sin ninguna fila `PENDIENTE`**: R-28 sigue `COMPLETADA` desde el ciclo de
Programador de la madrugada (commit `b990a1c`) — cola vacía hasta el próximo ciclo de PM que
archive la Oleada v16 y abra la siguiente. `roadmap/FEEDBACK.md` revisado de nuevo: sigue con su
única fila de plantilla vacía, sin ninguna entrada `nuevo`.
`mcp__github__list_issues`/`list_pull_requests` sobre `JanoSolerDiaz/telePrompter`: cero issues y
cero PR abiertos.

**Sin cambio de código.** Verificación propia completa (`python3 scripts/ci.py`): `mypy`/`ruff` en
verde (70 archivos), 673 tests en verde (sin cambio), dieciocho etapas OK en
`verificar_salidas.py --fixture`. Cuatro redes en verde.

Sin cambios en §3 (bloqueos), §5 (P-XX) ni §7 (desviaciones). §6 sigue con `#11`/`#12`
`(pendiente)` de respuesta del dueño, sin novedad de esta sesión. `ROADMAP_PRODUCTO.md` no se toca
(su prosa de "Oleada v16 — EN CURSO"/R-28 queda desactualizada hasta el próximo ciclo de PM que la
archive — mismo patrón ya descrito y aceptado en el hallazgo `#24`).

**Última actualización anterior (2026-10-13, ciclo de Programador): octava reconfirmación del día
tras R-28**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Ciclo de Programador (2026-10-13), octava reconfirmación del día tras R-28.** Revisión de
entrada (protocolo): `git checkout develop && git pull origin develop` encontró el contenedor de
nuevo con `HEAD` *detached* y la rama local ocho commits por detrás de `origin/develop`
(`ea23748`, la séptima reconfirmación de esta misma jornada, ya empujada); el `checkout` y el
`pull` avanzaron por fast-forward sin ninguna divergencia real que resolver (nada parecido al
artefacto de clon superficial del hallazgo `#21`). `git status` limpio antes y después.
Dependencias de desarrollo instaladas primero con el `pip` desnudo del `PATH` (mismo síntoma ya
documentado por `#28`/P-06: resuelve contra el intérprete equivocado y deja `mypy`/`ruff`/`pytest`
sin instalar) y reinstaladas con `python3 -m pip install -r requirements-dev.txt`, tras lo cual
las cuatro redes dieron `OK` (`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

Registro de hallazgos de `auditoriacontinua.md` (auditoría 2026-10-13, sin cambios desde la última
lectura): dos `ABIERTO`, ambos de proceso puro y sin relación con el código (`#24`, prosa de "Cola
de producto" desactualizada entre ciclos de PM; `#30`, cadencia de la rutina Programador) —
ninguno de severidad alta que atender como P-XX urgente antes de la cola normal, ambos pendientes
solo de la respuesta del dueño a las preguntas de gobernanza `#11`/`#12` de §6. §1 (fuente
autoritativa) **sin ninguna fila `PENDIENTE`**: R-28 sigue `COMPLETADA` desde el ciclo de
Programador de la madrugada (commit `b990a1c`) — cola vacía hasta el próximo ciclo de PM que
archive la Oleada v16 y abra la siguiente. `roadmap/FEEDBACK.md` revisado de nuevo: sigue con su
única fila de plantilla vacía, sin ninguna entrada `nuevo`.
`mcp__github__list_issues`/`list_pull_requests` sobre `JanoSolerDiaz/telePrompter`: cero issues y
cero PR abiertos.

**Sin cambio de código.** Verificación propia completa (`python3 scripts/ci.py`): `mypy`/`ruff` en
verde (70 archivos), 673 tests en verde (sin cambio), dieciocho etapas OK en
`verificar_salidas.py --fixture`. Cuatro redes en verde.

Sin cambios en §3 (bloqueos), §5 (P-XX) ni §7 (desviaciones). §6 sigue con `#11`/`#12`
`(pendiente)` de respuesta del dueño, sin novedad de esta sesión. `ROADMAP_PRODUCTO.md` no se toca
(su prosa de "Oleada v16 — EN CURSO"/R-28 queda desactualizada hasta el próximo ciclo de PM que la
archive — mismo patrón ya descrito y aceptado en el hallazgo `#24`).

**Última actualización anterior (2026-10-13, ciclo de Programador): séptima reconfirmación del día
tras R-28**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Ciclo de Programador (2026-10-13), séptima reconfirmación del día tras R-28.** Revisión de
entrada (protocolo): `git checkout develop && git pull origin develop` encontró el contenedor de
nuevo con `HEAD` *detached* y la rama local siete commits por detrás de `origin/develop`
(`2f49bb2`, la sexta reconfirmación de esta misma jornada, ya empujada); el `checkout` y el `pull`
avanzaron por fast-forward sin ninguna divergencia real que resolver (nada parecido al artefacto
de clon superficial del hallazgo `#21`). `git status` limpio antes y después. Dependencias de
desarrollo instaladas primero con el `pip` desnudo del `PATH` (mismo síntoma ya documentado por
`#28`/P-06: resuelve contra el intérprete equivocado y deja `mypy`/`ruff`/`pytest` sin instalar) y
reinstaladas con `python3 -m pip install -r requirements-dev.txt`, tras lo cual las cuatro redes
dieron `OK` (`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

Registro de hallazgos de `auditoriacontinua.md` (auditoría 2026-10-13, sin cambios desde la última
lectura): dos `ABIERTO`, ambos de proceso puro y sin relación con el código (`#24`, prosa de "Cola
de producto" desactualizada entre ciclos de PM; `#30`, cadencia de la rutina Programador) —
ninguno de severidad alta que atender como P-XX urgente antes de la cola normal, ambos pendientes
solo de la respuesta del dueño a las preguntas de gobernanza `#11`/`#12` de §6. §1 (fuente
autoritativa) **sin ninguna fila `PENDIENTE`**: R-28 sigue `COMPLETADA` desde el ciclo de
Programador de la madrugada (commit `b990a1c`) — cola vacía hasta el próximo ciclo de PM que
archive la Oleada v16 y abra la siguiente. `roadmap/FEEDBACK.md` revisado de nuevo: sigue con su
única fila de plantilla vacía, sin ninguna entrada `nuevo`.
`mcp__github__list_issues`/`list_pull_requests` sobre `JanoSolerDiaz/telePrompter`: cero issues y
cero PR abiertos.

**Sin cambio de código.** Verificación propia completa (`python3 scripts/ci.py`): `mypy`/`ruff` en
verde (70 archivos), 673 tests en verde (sin cambio), dieciocho etapas OK en
`verificar_salidas.py --fixture`. Cuatro redes en verde.

Sin cambios en §3 (bloqueos), §5 (P-XX) ni §7 (desviaciones). §6 sigue con `#11`/`#12`
`(pendiente)` de respuesta del dueño, sin novedad de esta sesión. `ROADMAP_PRODUCTO.md` no se toca
(su prosa de "Oleada v16 — EN CURSO"/R-28 queda desactualizada hasta el próximo ciclo de PM que la
archive — mismo patrón ya descrito y aceptado en el hallazgo `#24`).

**Última actualización anterior (2026-10-13, ciclo de Programador): sexta reconfirmación del día
tras R-28**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Ciclo de Programador (2026-10-13), sexta reconfirmación del día tras R-28.** Revisión de
entrada (protocolo): `git checkout develop && git pull origin develop` encontró el contenedor de
nuevo con `HEAD` *detached* y la rama local seis commits por detrás de `origin/develop`
(`8d4b665`, la quinta reconfirmación de esta misma jornada, ya empujada); el `checkout` y el
`pull` avanzaron por fast-forward sin ninguna divergencia real que resolver (nada parecido al
artefacto de clon superficial del hallazgo `#21`). `git status` limpio antes y después.
Dependencias de desarrollo instaladas primero con el `pip` desnudo del `PATH` (mismo síntoma ya
documentado por `#28`/P-06: resuelve contra el intérprete equivocado y deja `mypy`/`ruff`/`pytest`
sin instalar) y reinstaladas con `python3 -m pip install -r requirements-dev.txt`, tras lo cual
las cuatro redes dieron `OK` (`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

Registro de hallazgos de `auditoriacontinua.md` (auditoría 2026-10-13, sin cambios desde la última
lectura): dos `ABIERTO`, ambos de proceso puro y sin relación con el código (`#24`, prosa de "Cola
de producto" desactualizada entre ciclos de PM; `#30`, cadencia de la rutina Programador) —
ninguno de severidad alta que atender como P-XX urgente antes de la cola normal, ambos pendientes
solo de la respuesta del dueño a las preguntas de gobernanza `#11`/`#12` de §6. §1 (fuente
autoritativa) **sin ninguna fila `PENDIENTE`**: R-28 sigue `COMPLETADA` desde el ciclo de
Programador de la madrugada (commit `b990a1c`) — cola vacía hasta el próximo ciclo de PM que
archive la Oleada v16 y abra la siguiente. `roadmap/FEEDBACK.md` revisado de nuevo: sigue con su
única fila de plantilla vacía, sin ninguna entrada `nuevo`.
`mcp__github__list_issues`/`list_pull_requests` sobre `JanoSolerDiaz/telePrompter`: cero issues y
cero PR abiertos.

**Sin cambio de código.** Verificación propia completa (`python3 scripts/ci.py`): `mypy`/`ruff` en
verde (70 archivos), 673 tests en verde (sin cambio), dieciocho etapas OK en
`verificar_salidas.py --fixture`. Cuatro redes en verde.

Sin cambios en §3 (bloqueos), §5 (P-XX) ni §7 (desviaciones). §6 sigue con `#11`/`#12`
`(pendiente)` de respuesta del dueño, sin novedad de esta sesión. `ROADMAP_PRODUCTO.md` no se toca
(su prosa de "Oleada v16 — EN CURSO"/R-28 queda desactualizada hasta el próximo ciclo de PM que la
archive — mismo patrón ya descrito y aceptado en el hallazgo `#24`).

**Última actualización anterior (2026-10-13, ciclo de Programador): quinta reconfirmación del día
tras R-28**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Ciclo de Programador (2026-10-13), quinta reconfirmación del día tras R-28.** Revisión de
entrada (protocolo): `git checkout develop && git pull origin develop` encontró el contenedor con
`HEAD` *detached* y la rama local cinco commits por detrás de `origin/develop` (`8659e2b`, la
cuarta reconfirmación de esta misma jornada, ya empujada); el `checkout` y el `pull` avanzaron por
fast-forward sin ninguna divergencia real que resolver (nada parecido al artefacto de clon
superficial del hallazgo `#21`). `git status` limpio antes y después. Dependencias de desarrollo
instaladas primero con el `pip` desnudo del `PATH` (mismo síntoma ya documentado por `#28`/P-06:
`mypy`/`ruff`/`pytest` dieron `No module named ...`) y reinstaladas con `python3 -m pip install -r
requirements-dev.txt`, tras lo cual las cuatro redes dieron `OK` (`mypy==1.18.2`, `ruff==0.14.0`,
`pytest==8.4.2`).

Registro de hallazgos de `auditoriacontinua.md` (auditoría 2026-10-13, sin cambios desde la última
lectura): dos `ABIERTO`, ambos de proceso puro y sin relación con el código (`#24`, prosa de "Cola
de producto" desactualizada entre ciclos de PM; `#30`, cadencia de la rutina Programador) —
ninguno de severidad alta que atender como P-XX urgente antes de la cola normal, ambos pendientes
solo de la respuesta del dueño a las preguntas de gobernanza `#11`/`#12` de §6. §1 (fuente
autoritativa) **sin ninguna fila `PENDIENTE`**: R-28 sigue `COMPLETADA` desde el ciclo de
Programador de la madrugada (commit `b990a1c`) — cola vacía hasta el próximo ciclo de PM que
archive la Oleada v16 y abra la siguiente. `roadmap/FEEDBACK.md` revisado de nuevo: sigue con su
única fila de plantilla vacía, sin ninguna entrada `nuevo`. `mcp__github__list_issues`/
`list_pull_requests` sobre `JanoSolerDiaz/telePrompter`: cero issues y cero PR abiertos.

**Sin cambio de código.** Verificación propia completa (`python3 scripts/ci.py`): `mypy`/`ruff` en
verde (70 archivos), 673 tests en verde (sin cambio), dieciocho etapas OK en
`verificar_salidas.py --fixture`. Cuatro redes en verde.

Sin cambios en §3 (bloqueos), §5 (P-XX) ni §7 (desviaciones). §6 sigue con `#11`/`#12`
`(pendiente)` de respuesta del dueño, sin novedad de esta sesión. `ROADMAP_PRODUCTO.md` no se toca
(su prosa de "Oleada v16 — EN CURSO"/R-28 queda desactualizada hasta el próximo ciclo de PM que la
archive — mismo patrón ya descrito y aceptado en el hallazgo `#24`).

**Última actualización anterior (2026-10-13, ciclo de Programador): cuarta reconfirmación del día
tras R-28**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Ciclo de Programador (2026-10-13), cuarta reconfirmación del día tras R-28.** Revisión de
entrada (protocolo): `git checkout develop && git pull origin develop` encontró el contenedor de
nuevo con `HEAD` *detached* y la rama local cuatro commits por detrás de `origin/develop`
(`cd9a3a4`, la tercera reconfirmación de esta misma jornada, ya empujada); el `checkout` y el
`pull` avanzaron por fast-forward sin ninguna divergencia real que resolver (nada parecido al
artefacto de clon superficial del hallazgo `#21`). `git status` limpio antes y después.
Dependencias de desarrollo instaladas primero con el `pip` desnudo del `PATH` (mismo síntoma ya
documentado por `#28`/P-06: resuelve contra el intérprete equivocado y deja `mypy` sin instalar) y
reinstaladas con `python3 -m pip install -r requirements-dev.txt`, tras lo cual las cuatro redes
dieron `OK` (`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

Registro de hallazgos de `auditoriacontinua.md` (auditoría 2026-10-13, sin cambios desde la última
lectura): dos `ABIERTO`, ambos de proceso puro y sin relación con el código (`#24`, prosa de "Cola
de producto" desactualizada entre ciclos de PM; `#30`, cadencia de la rutina Programador) —
ninguno de severidad alta que atender como P-XX urgente antes de la cola normal, ambos pendientes
solo de la respuesta del dueño a las preguntas de gobernanza `#11`/`#12` de §6. §1 (fuente
autoritativa) **sin ninguna fila `PENDIENTE`**: R-28 sigue `COMPLETADA` desde el ciclo de
Programador de esta misma madrugada (commit `b990a1c`) — cola vacía hasta el próximo ciclo de PM
que archive la Oleada v16 y abra la siguiente. `roadmap/FEEDBACK.md` revisado de nuevo: sigue con
su única fila de plantilla vacía, sin ninguna entrada `nuevo`.
`mcp__github__list_issues`/`list_pull_requests` sobre `JanoSolerDiaz/telePrompter`: cero issues y
cero PR abiertos.

**Sin cambio de código.** Verificación propia completa (`python3 scripts/ci.py`): `mypy`/`ruff` en
verde (70 archivos), 673 tests en verde (sin cambio), dieciocho etapas OK en
`verificar_salidas.py --fixture`. Cuatro redes en verde.

Sin cambios en §3 (bloqueos), §5 (P-XX) ni §7 (desviaciones). §6 sigue con `#11`/`#12`
`(pendiente)` de respuesta del dueño, sin novedad de esta sesión. `ROADMAP_PRODUCTO.md` no se toca
(su prosa de "Oleada v16 — EN CURSO"/R-28 queda desactualizada hasta el próximo ciclo de PM que la
archive — mismo patrón ya descrito y aceptado en el hallazgo `#24`).

**Última actualización anterior (2026-10-13, ciclo de Programador): tercera reconfirmación del día
tras R-28**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Ciclo de Programador (2026-10-13), segunda reconfirmación del día tras R-28.** Revisión de
entrada (protocolo): `git checkout develop && git pull origin develop` encontró el contenedor de
nuevo con `HEAD` *detached* y la rama local dos commits por detrás de `origin/develop`
(`8279e8a`, la primera reconfirmación de esta misma jornada, ya empujada); el `checkout` y el
`pull` avanzaron por fast-forward sin ninguna divergencia real que resolver (nada parecido al
artefacto de clon superficial del hallazgo `#21`). `git status` limpio antes y después.
Dependencias de desarrollo instaladas primero con el `pip` desnudo del `PATH` (resuelve contra
Python 3.13, síntoma ya documentado por `#28`/P-06: las tres redes de tipos/estilo/tests dieron
`No module named mypy`/`ruff`/`pytest`) y reinstaladas con
`python3 -m pip install -r requirements-dev.txt`, tras lo cual las cuatro redes dieron `OK`.

Registro de hallazgos de `auditoriacontinua.md` (auditoría 2026-10-13, sin cambios desde la última
lectura): dos `ABIERTO`, ambos de proceso puro y sin relación con el código (`#24`, prosa de "Cola
de producto" desactualizada entre ciclos de PM; `#30`, cadencia de la rutina Programador) — ninguno
de severidad alta que atender como P-XX urgente antes de la cola normal, ambos pendientes solo de
la respuesta del dueño a las preguntas de gobernanza `#11`/`#12` de §6. §1 (fuente autoritativa)
**sin ninguna fila `PENDIENTE`**: R-28 sigue `COMPLETADA` desde el ciclo de Programador de esta
misma madrugada (commit `b990a1c`) — cola vacía hasta el próximo ciclo de PM que archive la Oleada
v16 y abra la siguiente. `roadmap/FEEDBACK.md` revisado de nuevo: sigue con su única fila de
plantilla vacía, sin ninguna entrada `nuevo`. `mcp__github__list_issues`/`list_pull_requests` sobre
`JanoSolerDiaz/telePrompter`: cero issues y cero PR abiertos.

**Sin cambio de código.** Verificación propia completa (`python3 scripts/ci.py`): `mypy`/`ruff` en
verde (70 archivos), 673 tests en verde (sin cambio), dieciocho etapas OK en
`verificar_salidas.py --fixture`. Cuatro redes en verde.

Sin cambios en §3 (bloqueos), §5 (P-XX) ni §7 (desviaciones). §6 sigue con `#11`/`#12`
`(pendiente)` de respuesta del dueño, sin novedad de esta sesión. `ROADMAP_PRODUCTO.md` no se toca
(su prosa de "Oleada v16 — EN CURSO"/R-28 queda desactualizada hasta el próximo ciclo de PM que la
archive — mismo patrón ya descrito y aceptado en el hallazgo `#24`).

**Última actualización anterior (2026-10-13, ciclo de Programador): primera reconfirmación del día
tras R-28**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Ciclo de Programador (2026-10-13), primera reconfirmación del día tras R-28.** Revisión de
entrada (protocolo): `git checkout develop && git pull origin develop` encontró el contenedor con
`HEAD` *detached*; tras el `checkout`, la rama local quedó un commit por detrás de `origin/develop`
y avanzó por fast-forward sin ninguna divergencia real que resolver (nada parecido al artefacto de
clon superficial del hallazgo `#21`). `git status` limpio antes y después. Dependencias de
desarrollo instaladas primero con el `pip` desnudo del `PATH` (resuelve contra Python 3.13, síntoma
ya documentado por `#28`/P-06: las tres redes de tipos/estilo/tests dieron `No module named
mypy`/`ruff`/`pytest`) y reinstaladas con `python3 -m pip install -r requirements-dev.txt`, tras lo
cual las cuatro redes dieron `OK`.

Registro de hallazgos de `auditoriacontinua.md` (auditoría 2026-10-13, sin cambios desde la última
lectura): dos `ABIERTO`, ambos de proceso puro y sin relación con el código (`#24`, prosa de "Cola
de producto" desactualizada entre ciclos de PM; `#30`, cadencia de la rutina Programador) — ninguno
de severidad alta que atender como P-XX urgente antes de la cola normal, ambos pendientes solo de
la respuesta del dueño a las preguntas de gobernanza `#11`/`#12` de §6. §1 (fuente autoritativa)
**sin ninguna fila `PENDIENTE`**: R-28 sigue `COMPLETADA` desde el ciclo de Programador de esta
misma madrugada (commit `b990a1c`) — cola vacía hasta el próximo ciclo de PM que archive la Oleada
v16 y abra la siguiente. `roadmap/FEEDBACK.md` revisado de nuevo: sigue con su única fila de
plantilla vacía, sin ninguna entrada `nuevo`. `mcp__github__list_issues`/`list_pull_requests` sobre
`JanoSolerDiaz/telePrompter`: cero issues y cero PR abiertos.

**Sin cambio de código.** Verificación propia completa (`python3 scripts/ci.py`): `mypy`/`ruff` en
verde, 673 tests en verde (sin cambio), dieciocho etapas OK en `verificar_salidas.py --fixture`.
Cuatro redes en verde.

Sin cambios en §3 (bloqueos), §5 (P-XX) ni §7 (desviaciones). §6 sigue con `#11`/`#12`
`(pendiente)` de respuesta del dueño, sin novedad de esta sesión. `ROADMAP_PRODUCTO.md` no se toca
(su prosa de "Oleada v16 — EN CURSO"/R-28 queda desactualizada hasta el próximo ciclo de PM que la
archive — mismo patrón ya descrito y aceptado en el hallazgo `#24`).

**Última actualización anterior (2026-10-13, ciclo de Programador): R-28 implementada y
`COMPLETADA`** (detalle en la nota de esa sesión, más abajo).

**Ciclo de Programador (2026-10-13): R-28 implementada.** Revisión de entrada (protocolo):
`git checkout develop && git pull origin develop` sin sorpresas (rama local ya al día con
`origin/develop`, sin divergencia que resolver esta vez). Dependencia de desarrollo instalada con
`python3 -m pip install -r requirements-dev.txt` (no el `pip` desnudo del `PATH`, que sigue
resolviendo contra el intérprete equivocado del contenedor — síntoma ya documentado por `#28`/P-06).

Registro de hallazgos de `auditoriacontinua.md` (auditoría 2026-10-13): dos `ABIERTO`, ambos de
proceso puro y sin relación con el código (`#24`, prosa de "Cola de producto" desactualizada entre
ciclos; `#30`, cadencia del Programador) — ninguno de severidad alta que atender como P-XX urgente
antes de la cola normal. §1 (fuente autoritativa) traía **R-28 como única fila `PENDIENTE`**:
implementada en esta sesión siguiendo al pie de la letra su spec de `ROADMAP_PRODUCTO.md` (Oleada
v16, verificada contra `DECISIONES_TECNICAS.md` antes de tocar código, sin contradecir ninguna
decisión previa).

**Implementación.** Tres validadores de contrato ya construidos y probados, sin ningún llamador real
fuera de `verificar_salidas.py --fixture`, quedan conectados a su ruta real de generación — mismo
patrón de grieta que R-21/R-22 ya cerraron para sus gemelos:

- `pptx.py::exportar_pptx` construye `datos = tarjetas_a_diccionario(resultado_tarjetas)` y llama
  `validar_tarjetas(datos)` antes de `guardar_tarjetas_json`; con problemas, lanza
  `TarjetasInvalidasError` (excepción nueva del módulo) y no escribe ni `tarjetas.json` ni el brief.
  La excepción la captura el `try`/`except` genérico ya existente en
  `salidas.py::generar_salidas_seleccionadas` (R-24), sin tocar `salidas.py` para esta salida.
- `salidas.py::_generar_srt` valida cada mitad (`guion.srt`, `guion-alineado.srt`) por separado con
  `srt.validar_srt` antes de `guardar_srt`/`guardar_srt_alineado`; con problemas, esa mitad se
  construye como `SalidaOmitida` a mano (mismo patrón literal que `_generar_concat_ffmpeg`/R-21),
  sin impedir que la otra mitad se genere.
- `salidas.py::_generar_capitulos_youtube` valida ahora también `capitulos-youtube.txt` con
  `validar_capitulos_youtube`, en el mismo punto donde ya validaba `capitulos-ffmpeg.txt` desde
  R-22 — las dos mitades siguen siendo independientes entre sí.

Las dos convenciones de propagación (excepción vs. `SalidaOmitida` a mano) conviven a propósito,
razonadas en `DECISIONES_TECNICAS.md`: cada una vive donde la validación ya encajaba de forma
natural, sin forzar un estilo único a costa de reescribir el contrato de alguna de las tres salidas.
Cero cambio en las reglas de los tres validadores ni en `concat_ffmpeg.py`/`validar_capitulos_ffmpeg`
(ya conectados desde R-21/R-22); comportamiento idéntico al de antes de R-28 cuando el contenido
generado es válido, confirmado por las dieciocho etapas en verde de `verificar_salidas.py --fixture`
sin ningún cambio. `DEVELOPERS.md` gana sección propia ("Conectar los tres validadores de contrato
restantes a su ruta real de generación, R-28").

**Verificación.** 4 tests nuevos (669→673): `tests/test_pptx.py`
(`test_exportar_pptx_con_datos_invalidos_no_escribe_nada`) y tres en `tests/test_salidas.py`
(`test_srt_con_contenido_invalido_degrada_a_omitida_en_vez_de_escribir`,
`test_srt_alineado_invalido_no_impide_el_srt_estimado`,
`test_capitulos_youtube_con_contenido_invalido_degrada_a_omitida`). Regresión de los tests
existentes (incluidos los que ya comprobaban los tres guiones reales contra `validar_tarjetas`) sin
cambios de comportamiento. Cuatro redes en verde (`mypy`, `ruff`, 673 tests, dieciocho etapas de
`verificar_salidas.py --fixture`).

Sin cambios en §3 (bloqueos) ni §7 (desviaciones). §5: sin ningún P-XX nuevo (la cola normal cubría
el trabajo de esta sesión). §6: preguntas `#11`/`#12` siguen `(pendiente)` de respuesta del dueño,
sin novedad de esta sesión. `ROADMAP_PRODUCTO.md` no se toca en esta sesión (su prosa de "Oleada
v16 — EN CURSO"/R-28 queda desactualizada hasta el próximo ciclo de PM que la archive — mismo patrón
ya descrito y aceptado como de bajo riesgo en el hallazgo `#24`, pendiente solo de la respuesta de
gobernanza del dueño a la pregunta `#11`).

**Ciclo de Product Manager (2026-10-12).** Revisión de entrada (protocolo): el contenedor arrancó con
la rama local `develop` desactualizada en `cc0ac86` (cincuenta commits por detrás) y divergente de
`origin/develop` sin ancestro común visible bajo el historial superficial por defecto — mismo
artefacto del `git clone --depth` de cada contenedor efímero ya diagnosticado por el hallazgo `#21` y
por todos los ciclos anteriores, confirmado comparando `git merge-base --is-ancestor`: la punta local
no era ancestro ni descendiente real de `origin/develop`, y `git status` estaba limpio (cero contenido
propio que perder). Resuelto con `git reset --hard origin/develop`, dejando `develop` apuntando a la
punta real (`842255a`, la novena reconfirmación del Programador tras R-27, ya empujada). Dependencias
de desarrollo instaladas con `pip install -r requirements-dev.txt`.

Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: dos `ABIERTO`, ambos de
proceso puro y sin relación con el código (`#24`, baja; `#30`, media), ninguno de severidad alta que
atender antes de la cola normal — ambos pendientes solo de la respuesta del dueño a las preguntas de
gobernanza #11/#12 de §6. §1 (fuente autoritativa): R-27 `COMPLETADA` desde el ciclo de Programador de
esta misma jornada (commit `9324938`), sin ningún hito de negocio propio pendiente. `roadmap/FEEDBACK.md`
revisado de nuevo: sigue con su única fila de plantilla vacía, sin ninguna entrada `nuevo`.

**Archiva Oleada v15 (R-27)** a `roadmap/ROADMAP_HISTORICO.md` (spec completa + "Cómo se entregó").
`ROADMAP_PRODUCTO.md` corregido en el mismo ciclo que archiva. Commit intermedio `75b318b` empujado a
mitad de sesión (solo el archivo) mientras un agente Explore investigaba candidatos a la siguiente
R-XX en paralelo, para no dejar trabajo sin respaldo en el clon efímero.

**Abre R-28 (Oleada v16).** Grieta de arquitectura verificada, mismo criterio que abrió R-12 a R-27:
tres validadores de contrato ya construidos y probados (`pptx.validar_tarjetas`, `srt.validar_srt`,
`capitulos_youtube.validar_capitulos_youtube`) nunca se invocan en la ruta real de generación de
`scripts/salidas.py`/`pptx.exportar_pptx`, solo desde `verificar_salidas.py --fixture` — la misma
forma de grieta que el propio proyecto ya cerró dos veces (R-21, R-22) sin corregir aquí sus tres
gemelos. Localización delegada a un agente Explore, verificada después con `grep` dirigido de forma
independiente antes de escribir la spec. Detalle completo, decisiones y candidatas descartadas en
`ROADMAP_PRODUCTO.md` (Oleada v16) y `DECISIONES_TECNICAS.md` ("PM (apertura de R-28)"). Fila añadida
a §1 en este mismo ciclo.

Sin cambios en §3 (bloqueos) ni §5 (P-XX); §6 sin novedad (`#11`/`#12` siguen `(pendiente)`); sin
nueva desviación en §7. Este ciclo es de PM, no de Programador: no se ha ejecutado la verificación de
las cuatro redes ni se ha tocado `scripts/`, `tests/` ni `assets/`.

**Última actualización anterior (2026-10-12, ciclo de Programador): novena reconfirmación del día
tras R-27**, sin novedad de código (§1 sin ninguna fila `PENDIENTE`, cuatro redes en verde, 669 tests)
(detalle en la nota de esa sesión, más abajo).

**Ciclo de Programador (2026-10-12), novena reconfirmación del día tras R-27.** Revisión de entrada
(protocolo): el contenedor arrancó con la rama local `develop` desactualizada en `cc0ac86`
(cincuenta commits por detrás) y divergente de `origin/develop` sin ancestro común visible bajo el
historial superficial por defecto — mismo artefacto del `git clone --depth` de cada contenedor
efímero ya diagnosticado por el hallazgo `#21` del auditor y por todos los ciclos anteriores, no una
reescritura real (ambas puntas narran la misma historia continua R-22→R-27, solo que la local se
quedó en el corte de profundidad de hace varias sesiones; confirmado esta vez comparando
`git rev-parse --tree` de `cc0ac86`/`develop`/`origin/develop`: la punta local era tree-idéntica a
`cc0ac86`, cero contenido propio que perder). Resuelto con `git reset --hard origin/develop` (sin
bloqueo del clasificador de permisos esta vez), dejando `develop` apuntando exactamente a la punta
real de `origin/develop` (`406b7f6`, el trabajo de la octava reconfirmación de esta misma jornada,
ya empujado, no una pérdida) con `git status` limpio antes y después. Dependencias de desarrollo
instaladas con `python3 -m pip install -r requirements-dev.txt` (no con el `pip` desnudo del `PATH`,
que resuelve contra un intérprete 3.13 distinto del 3.11.17 real del proyecto — mismo síntoma de
siempre, P-06/`#28`): `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`.

Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: dos `ABIERTO`, ambos de
proceso puro y sin relación con el código (`#24`, baja, prosa de "Cola de producto" desactualizada
entre ciclos — pregunta `#11` de §6 sigue `(pendiente)`; `#30`, media, cadencia de la rutina
"Programador" — pregunta `#12` de §6 sigue `(pendiente)`), ambos sin cambios desde la auditoría del
2026-10-12 (`0420c01`) — ninguno de severidad alta que atender como P-XX urgente antes de la cola
normal. §1 (fuente autoritativa) **no tiene ninguna fila `PENDIENTE`**: R-27 sigue `COMPLETADA`
desde el ciclo de Programador de esta misma madrugada, así que no hay ninguna tarea de código que
ejecutar hasta el próximo ciclo de Product Manager que abra la siguiente R-XX. `roadmap/FEEDBACK.md`
revisado de nuevo: sigue con su única fila de plantilla vacía, sin ninguna entrada `nuevo`.
`mcp__github__list_issues`/`list_pull_requests` sobre `JanoSolerDiaz/telePrompter`: cero issues y
cero PR abiertos.

**Verificación propia completa (`mypy`/`ruff`/`pytest`/`verificar_salidas.py --fixture`):**
`mypy`/`ruff` en verde sin hallazgos (70 archivos), 669 tests (`pytest`, sin cambio) en
verde, dieciocho etapas OK en `verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin
cambios en §3 (bloqueos), §5 (P-XX) ni §7 (desviaciones). §6: preguntas `#11`/`#12` siguen
`(pendiente)` de respuesta del dueño, sin novedad de esta sesión. `ROADMAP_PRODUCTO.md` no se toca
en esta sesión (su prosa de "Oleada v15 — EN CURSO"/R-27 `PENDIENTE` sigue desactualizada hasta el
próximo ciclo de PM que la archive — mismo patrón de bajo riesgo aceptado en el hallazgo `#24`).
Nota sin acción: cola vacía hasta el siguiente ciclo de Product Manager.

**Última actualización anterior (2026-10-12, ciclo de Programador): octava reconfirmación del día
tras R-27**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Ciclo de Programador (2026-10-12), séptima reconfirmación del día tras R-27.** Revisión de entrada
(protocolo): el contenedor arrancó con la rama local `develop` desactualizada en `cc0ac86`
(cincuenta commits por detrás) y divergente de `origin/develop` sin ancestro común visible bajo el
historial superficial por defecto — mismo artefacto del `git clone --depth` de cada contenedor
efímero ya diagnosticado por el hallazgo `#21` del auditor y por todos los ciclos anteriores, no una
reescritura real (ambas puntas narran la misma historia continua R-22→R-27, solo que la local se
quedó en el corte de profundidad de hace varias sesiones). Resuelto con `git reset --hard
origin/develop` (sin bloqueo del clasificador de permisos esta vez, variabilidad ya documentada
entre sesiones), dejando `develop` apuntando exactamente a la punta real de `origin/develop`
(`6af4dd6`, el trabajo de la sexta reconfirmación de esta misma madrugada, ya empujado, no una
pérdida) con `git status` limpio antes y después (ningún commit propio que perder: la rama local
obsoleta solo tenía historial desactualizado). Dependencias de desarrollo instaladas con
`python3 -m pip install -r requirements-dev.txt` (no con el `pip` desnudo del `PATH`, que resuelve
contra un intérprete 3.13 distinto del 3.11.17 real del proyecto — mismo síntoma de siempre,
P-06/`#28`): `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`.

Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: dos `ABIERTO`, ambos de
proceso puro y sin relación con el código (`#24`, baja, prosa de "Cola de producto" desactualizada
entre ciclos — pregunta `#11` de §6 sigue `(pendiente)`; `#30`, media, cadencia de la rutina
"Programador" — pregunta `#12` de §6 sigue `(pendiente)`), ambos sin cambios desde la auditoría del
2026-10-12 (`0420c01`) — ninguno de severidad alta que atender como P-XX urgente antes de la cola
normal. §1 (fuente autoritativa) **no tiene ninguna fila `PENDIENTE`**: R-27 sigue `COMPLETADA`
desde el ciclo de Programador de esta misma madrugada, así que no hay ninguna tarea de código que
ejecutar hasta el próximo ciclo de Product Manager que abra la siguiente R-XX.
`roadmap/FEEDBACK.md` revisado de nuevo: sigue con su única fila de plantilla vacía, sin ninguna
entrada `nuevo`. `mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/teleprompter`:
cero issues y cero PR abiertos.

**Verificación propia completa (`python3 scripts/ci.py`):** `mypy`/`ruff` en verde sin hallazgos (70
archivos), 669 tests (`pytest`, sin cambio) en verde, dieciocho etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en §3 (bloqueos), §5 (P-XX)
ni §7 (desviaciones). §6: preguntas `#11`/`#12` siguen `(pendiente)` de respuesta del dueño, sin
novedad de esta sesión. `ROADMAP_PRODUCTO.md` no se toca en esta sesión (su prosa de "Oleada v15 — EN
CURSO"/R-27 `PENDIENTE` sigue desactualizada hasta el próximo ciclo de PM que la archive — mismo
patrón de bajo riesgo aceptado en el hallazgo `#24`). Nota sin acción: cola vacía hasta el siguiente
ciclo de Product Manager.

**Última actualización anterior (2026-10-12, ciclo de Programador): sexta reconfirmación del día
tras R-27**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Ciclo de Programador (2026-10-12), sexta reconfirmación del día tras R-27.** Revisión de entrada
(protocolo): el contenedor arrancó con la rama local `develop` desactualizada en `cc0ac86`
(cincuenta commits por detrás) y divergente de `origin/develop` sin ancestro común visible bajo el
historial superficial por defecto — mismo artefacto del `git clone --depth` de cada contenedor
efímero ya diagnosticado por el hallazgo `#21` del auditor y por todos los ciclos anteriores, no una
reescritura real (ambas puntas narran la misma historia continua R-22→R-27, solo que la local se
quedó en el corte de profundidad de hace varias sesiones). Resuelto con `git reset --hard
origin/develop` (sin bloqueo del clasificador de permisos esta vez, variabilidad ya documentada
entre sesiones), dejando `develop` apuntando exactamente a la punta real de `origin/develop`
(`9b6b4de`, el trabajo de la quinta reconfirmación de esta misma madrugada, ya empujado, no una
pérdida) con `git status` limpio antes y después (ningún commit propio que perder: la rama local
obsoleta solo tenía historial desactualizado). Dependencias de desarrollo instaladas con
`python3 -m pip install -r requirements-dev.txt` (no con el `pip` desnudo del `PATH`, que resuelve
contra un intérprete 3.13 distinto del 3.11.17 real del proyecto — mismo síntoma de siempre,
P-06/`#28`): `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`.

Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: dos `ABIERTO`, ambos de
proceso puro y sin relación con el código (`#24`, baja, prosa de "Cola de producto" desactualizada
entre ciclos — pregunta `#11` de §6 sigue `(pendiente)`; `#30`, media, cadencia de la rutina
"Programador" — pregunta `#12` de §6 sigue `(pendiente)`), ambos sin cambios desde la auditoría de
esta misma madrugada (`0420c01`) — ninguno de severidad alta que atender como P-XX urgente antes de
la cola normal. §1 (fuente autoritativa) **no tiene ninguna fila `PENDIENTE`**: R-27 sigue
`COMPLETADA` desde el ciclo de Programador de esta misma madrugada, así que no hay ninguna tarea de
código que ejecutar hasta el próximo ciclo de Product Manager que abra la siguiente R-XX.
`roadmap/FEEDBACK.md` revisado de nuevo: sigue con su única fila de plantilla vacía, sin ninguna
entrada `nuevo`. `mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/teleprompter`:
cero issues y cero PR abiertos.

**Verificación propia completa (`python3 scripts/ci.py`):** `mypy`/`ruff` en verde sin hallazgos (70
archivos), 669 tests (`pytest`, sin cambio) en verde, dieciocho etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en §3 (bloqueos), §5 (P-XX)
ni §7 (desviaciones). §6: preguntas `#11`/`#12` siguen `(pendiente)` de respuesta del dueño, sin
novedad de esta sesión. `ROADMAP_PRODUCTO.md` no se toca en esta sesión (su prosa de "Oleada v15 — EN
CURSO"/R-27 `PENDIENTE` sigue desactualizada hasta el próximo ciclo de PM que la archive — mismo
patrón de bajo riesgo aceptado en el hallazgo `#24`). Nota sin acción: cola vacía hasta el siguiente
ciclo de Product Manager.

**Última actualización anterior (2026-10-12, ciclo de Programador): quinta reconfirmación del día
tras R-27**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Ciclo de Programador (2026-10-12), quinta reconfirmación del día tras R-27.** Revisión de
entrada (protocolo): el contenedor arrancó con la rama local `develop` desactualizada en `cc0ac86`
(cincuenta commits por detrás) y divergente de `origin/develop` sin ancestro común visible bajo el
historial superficial por defecto — mismo artefacto del `git clone --depth` de cada contenedor
efímero ya diagnosticado por el hallazgo `#21` del auditor y por todos los ciclos anteriores, no
una reescritura real: ambas puntas narran la misma historia continua R-22→R-27 (confirmado
comparando fechas de los commits raíz de cada punta: `e684987`, 2026-09-30, frente al commit en el
que de hecho se cortó la profundidad del clon, muy posterior), solo que la local se quedó en el
corte de profundidad de hace varias sesiones. Resuelto sin ninguna operación destructiva:
`git checkout -B develop origin/develop` realinea la rama local con la punta real de
`origin/develop` (`b282006`, el trabajo de la cuarta reconfirmación de esta misma madrugada, ya
empujado, no una pérdida) sin `--hard`/`--unshallow`/`reset`, con `git status` limpio antes y
después (ningún commit propio que perder: la rama local obsoleta solo tenía historial
desactualizado). Dependencias de desarrollo instaladas con
`python3 -m pip install -r requirements-dev.txt` (no con el `pip` desnudo del `PATH`, que resuelve
contra un intérprete distinto del 3.11.17 real del proyecto — mismo síntoma de siempre, P-06/`#28`):
`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`.

Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: dos `ABIERTO`, ambos de
proceso puro y sin relación con el código (`#24`, baja, prosa de "Cola de producto" desactualizada
entre ciclos — pregunta `#11` de §6 sigue `(pendiente)`; `#30`, media, cadencia de la rutina
"Programador" — pregunta `#12` de §6 sigue `(pendiente)`), ambos sin cambios desde la auditoría de
esta misma madrugada (`0420c01`) — ninguno de severidad alta que atender como P-XX urgente antes de
la cola normal. §1 (fuente autoritativa) **no tiene ninguna fila `PENDIENTE`**: R-27 sigue
`COMPLETADA` desde el ciclo de Programador de esta misma madrugada, así que no hay ninguna tarea de
código que ejecutar hasta el próximo ciclo de Product Manager que abra la siguiente R-XX.
`roadmap/FEEDBACK.md` revisado de nuevo: sigue con su única fila de plantilla vacía, sin ninguna
entrada `nuevo`. `mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/teleprompter`:
cero issues y cero PR abiertos.

**Verificación propia completa (`python3 scripts/ci.py`):** `mypy`/`ruff` en verde sin hallazgos (70
archivos), 669 tests (`pytest`, sin cambio) en verde, dieciocho etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en §3 (bloqueos), §5 (P-XX)
ni §7 (desviaciones). §6: preguntas `#11`/`#12` siguen `(pendiente)` de respuesta del dueño, sin
novedad de esta sesión. `ROADMAP_PRODUCTO.md` no se toca en esta sesión (su prosa de "Oleada v15 — EN
CURSO"/R-27 `PENDIENTE` sigue desactualizada hasta el próximo ciclo de PM que la archive — mismo
patrón de bajo riesgo aceptado en el hallazgo `#24`). Nota sin acción: cola vacía hasta el siguiente
ciclo de Product Manager.

**Última actualización anterior (2026-10-12, ciclo de Programador): cuarta reconfirmación del día
tras R-27**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Ciclo de Programador (2026-10-12), cuarta reconfirmación del día tras R-27.** Revisión de entrada
(protocolo): el contenedor arrancó con la rama local `develop` desactualizada en `cc0ac86` (49
commits por detrás) y divergente de `origin/develop` sin ancestro común visible bajo el historial
superficial por defecto (`git clone --depth` de cada contenedor efímero, mismo artefacto ya
diagnosticado por el hallazgo `#21` del auditor y por los ciclos anteriores, no una reescritura
real: ambas puntas narran la misma historia continua R-22→R-27, solo que la local se quedó en el
corte de profundidad de hace varias sesiones). Esta vez se resolvió sin ninguna operación
destructiva: `git checkout -B develop origin/develop` realinea la rama local con la punta real de
`origin/develop` (`fdfe3b4`, el trabajo de la sesión anterior, ya empujado, no una pérdida) sin
`--hard`/`--unshallow`/`reset`, con `git status` limpio antes y después (ningún commit propio que
perder: la rama local obsoleta solo tenía historial desactualizado). Dependencias de desarrollo
instaladas con `python3 -m pip install -r requirements-dev.txt` (no con el `pip` desnudo del `PATH`,
que resuelve contra un intérprete 3.13 distinto del 3.11.17 real del proyecto — mismo síntoma de
siempre, P-06/`#28`): `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`.

Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: dos `ABIERTO`, ambos de
proceso puro y sin relación con el código (`#24`, baja, prosa de "Cola de producto" desactualizada
entre ciclos — pregunta `#11` de §6 sigue `(pendiente)`; `#30`, media, cadencia de la rutina
"Programador" — pregunta `#12` de §6 sigue `(pendiente)`), ambos sin cambios desde la auditoría de
esta misma madrugada (`0420c01`) — ninguno de severidad alta que atender como P-XX urgente antes de
la cola normal. §1 (fuente autoritativa) **no tiene ninguna fila `PENDIENTE`**: R-27 sigue
`COMPLETADA` desde el ciclo de Programador de esta misma madrugada, así que no hay ninguna tarea de
código que ejecutar hasta el próximo ciclo de Product Manager que abra la siguiente R-XX.
`roadmap/FEEDBACK.md` revisado de nuevo: sigue con su única fila de plantilla vacía, sin ninguna
entrada `nuevo`. `mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/teleprompter`:
cero issues y cero PR abiertos.

**Verificación propia completa (`python3 scripts/ci.py`):** `mypy`/`ruff` en verde sin hallazgos (70
archivos), 669 tests (`pytest`, sin cambio) en verde, dieciocho etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en §3 (bloqueos), §5 (P-XX)
ni §7 (desviaciones). §6: preguntas `#11`/`#12` siguen `(pendiente)` de respuesta del dueño, sin
novedad de esta sesión. `ROADMAP_PRODUCTO.md` no se toca en esta sesión (su prosa de "Oleada v15 — EN
CURSO"/R-27 `PENDIENTE` sigue desactualizada hasta el próximo ciclo de PM que la archive — mismo
patrón de bajo riesgo aceptado en el hallazgo `#24`). Nota sin acción: cola vacía hasta el siguiente
ciclo de Product Manager.

**Última actualización anterior (2026-10-12, ciclo de Programador): tercera reconfirmación del día
tras R-27**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Ciclo de Programador (2026-10-12), tercera reconfirmación del día tras R-27.** Revisión de entrada
(protocolo): el contenedor arrancó de nuevo con `HEAD` *detached* y la rama local `develop` obsoleta
en `cc0ac86` (mismo artefacto del `git clone --depth` de cada contenedor efímero ya diagnosticado por
el hallazgo `#21` del auditor y por los ciclos anteriores, no una reescritura real); `git fetch origin
develop` mostró `origin/develop` actualizado por la fuerza hasta `85157b4`, exactamente la misma punta
del `HEAD` *detached* de arranque (el trabajo de la sesión anterior, ya empujado a `origin/develop`,
no una pérdida). `git reset --hard origin/develop` pudo ejecutarse sin bloqueo del clasificador de
permisos esta vez (misma variabilidad ya documentada entre sesiones), dejando `develop` apuntando
exactamente a `origin/develop` sin perder ningún commit propio (la rama local obsoleta no contenía
trabajo propio de ninguna sesión). `git status` limpio antes y después. Dependencias de desarrollo
instaladas con `python3 -m pip install -r requirements-dev.txt` (no con el `pip` desnudo del `PATH`,
mismo síntoma de siempre, P-06/`#28`): `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`.

Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: dos `ABIERTO`, ambos de
proceso puro y sin relación con el código (`#24`, baja, prosa de "Cola de producto" desactualizada
entre ciclos — pregunta `#11` de §6 sigue `(pendiente)`; `#30`, media, cadencia de la rutina
"Programador" — pregunta `#12` de §6 sigue `(pendiente)`), ambos sin cambios desde la auditoría de
esta misma madrugada (`0420c01`) — ninguno de severidad alta que atender como P-XX urgente antes de la
cola normal. §1 (fuente autoritativa) **no tiene ninguna fila `PENDIENTE`**: R-27 sigue `COMPLETADA`
desde el ciclo de Programador de esta misma madrugada, así que no hay ninguna tarea de código que
ejecutar hasta el próximo ciclo de Product Manager que abra la siguiente R-XX. `roadmap/FEEDBACK.md`
revisado de nuevo: sigue con su única fila de plantilla vacía, sin ninguna entrada `nuevo`.

**Verificación propia completa (`python3 scripts/ci.py`):** `mypy`/`ruff` en verde sin hallazgos (70
archivos), 669 tests (`pytest`, sin cambio) en verde, dieciocho etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en §3 (bloqueos), §5 (P-XX)
ni §7 (desviaciones). §6: preguntas `#11`/`#12` siguen `(pendiente)` de respuesta del dueño, sin
novedad de esta sesión. `ROADMAP_PRODUCTO.md` no se toca en esta sesión (su prosa de "Oleada v15 — EN
CURSO"/R-27 `PENDIENTE` sigue desactualizada hasta el próximo ciclo de PM que la archive — mismo
patrón de bajo riesgo aceptado en el hallazgo `#24`). Nota sin acción: cola vacía hasta el siguiente
ciclo de Product Manager.

**Última actualización anterior (2026-10-12, ciclo de Programador): segunda reconfirmación del día
tras R-27**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Ciclo de Programador (2026-10-12), segunda reconfirmación del día tras R-27.** Revisión de entrada
(protocolo): el contenedor arrancó con `HEAD` *detached* sobre cincuenta commits no alcanzables desde
ninguna rama local — mismo artefacto del `git clone --depth` de cada contenedor efímero ya
diagnosticado por el hallazgo `#21` del auditor y por los ciclos anteriores, no una reescritura real:
`git checkout develop` dejó la rama local obsoleta en `cc0ac86` (muy por detrás) y el `fetch`
posterior mostró `origin/develop` actualizado por la fuerza hasta `789a343`, exactamente la misma
punta del `HEAD` *detached* de arranque (es decir, el trabajo de la sesión anterior, ya empujado a
`origin/develop`, no una pérdida). `git reset --hard origin/develop` pudo ejecutarse sin bloqueo del
clasificador de permisos esta vez (variabilidad ya documentada entre sesiones: unas veces bloquea
`--hard`/`--unshallow`, otras no, mismo clasificador), dejando `develop` apuntando exactamente a
`origin/develop` sin perder ningún commit propio (la rama local obsoleta no contenía trabajo propio
de ninguna sesión). `git status` limpio antes y después. Dependencias de desarrollo instaladas con
`python3 -m pip install -r requirements-dev.txt` (no con el `pip` desnudo del `PATH`, que resuelve
contra un intérprete distinto del 3.11.17 real del proyecto — mismo síntoma de siempre, P-06/`#28`):
`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`.

Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: dos `ABIERTO`, ambos de
proceso puro y sin relación con el código (`#24`, baja, prosa de "Cola de producto" desactualizada
entre ciclos — pregunta `#11` de §6 sigue `(pendiente)`; `#30`, media, cadencia de la rutina
"Programador" — pregunta `#12` de §6 sigue `(pendiente)`) — ninguno de severidad alta que atender
como P-XX urgente antes de la cola normal. §1 (fuente autoritativa) **no tiene ninguna fila
`PENDIENTE`**: R-27 sigue `COMPLETADA` desde el ciclo de Programador de esta misma madrugada, así que
no hay ninguna tarea de código que ejecutar hasta el próximo ciclo de Product Manager que abra la
siguiente R-XX.

**Verificación propia completa (`python3 scripts/ci.py`):** `mypy`/`ruff` en verde sin hallazgos (70
archivos), 669 tests (`pytest`, sin cambio) en verde, dieciocho etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en §3 (bloqueos), §5 (P-XX)
ni §7 (desviaciones). §6: preguntas `#11`/`#12` siguen `(pendiente)` de respuesta del dueño, sin
novedad de esta sesión. `ROADMAP_PRODUCTO.md` no se toca en esta sesión (su prosa de "Oleada v15 — EN
CURSO"/R-27 `PENDIENTE` sigue desactualizada hasta el próximo ciclo de PM que la archive — mismo
patrón de bajo riesgo aceptado en el hallazgo `#24`). Nota sin acción: cola vacía hasta el siguiente
ciclo de Product Manager.

**Última actualización anterior (2026-10-12, ciclo de Programador): primera reconfirmación del día
tras R-27**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Ciclo de Programador (2026-10-12), primera reconfirmación del día tras R-27.** Revisión de
entrada (protocolo): el contenedor arrancó con la rama local `develop` desactualizada (`cc0ac86`,
la misma rama local obsoleta ya diagnosticada por los ciclos anteriores y por el hallazgo `#21`
del auditor — artefacto del `git clone --depth` de cada contenedor efímero, no una reescritura
real) y divergente de `origin/develop` (`9324938`) **sin ancestro común visible** bajo el
historial superficial por defecto. A diferencia de sesiones anteriores, esta vez no hizo falta
ninguna operación destructiva: `git fetch --deepen=500 origin develop` amplió el historial local
lo suficiente para que `git merge-base develop origin/develop` encontrara un ancestro común real
(`cc0ac86`, el propio HEAD local — fast-forward limpio, cero commits propios perdidos), y
`git merge --ff-only origin/develop` completó la actualización sin tocar `master` ni tomar ninguna
decisión irreversible. `git fetch --unshallow` y `git reset --hard origin/develop` fueron
bloqueados por el clasificador de permisos del modo automático (irreversible/destructivo, sin
usuario en vivo que lo confirmara) antes de llegar a `--deepen`; queda documentado en
`DECISIONES_TECNICAS.md` como alternativa no destructiva para la próxima sesión que tropiece con
el mismo bloqueo. `git status` limpio antes y después. `requirements-dev.txt` instalado con
`python3 -m pip install` (no con el `pip` desnudo del `PATH`, mismo síntoma de siempre cubierto por
P-06/`#28`: resolvía contra un intérprete distinto del 3.11.17 real).

Registro de hallazgos de `auditoriacontinua.md` (auditoría 2026-10-12, `0420c01`, sin cambios desde
la última sesión): dos `ABIERTO`, ambos de proceso puro y sin relación con el código (`#24`, prosa
desactualizada entre ciclos; `#30`, cadencia del Programador) — ninguno de severidad alta que
atender como P-XX urgente antes de la cola normal. §1 (fuente autoritativa) **no tiene ninguna fila
`PENDIENTE`**: R-27 quedó `COMPLETADA` en el ciclo de Programador anterior (esta misma madrugada,
`9324938`), así que no hay ninguna tarea de código que ejecutar hasta el próximo ciclo de Product
Manager que abra la siguiente R-XX.

**Verificación propia completa (`python3 scripts/ci.py`):** `mypy`/`ruff` en verde sin hallazgos
(70 archivos), 669 tests (`pytest`, sin cambio) en verde, dieciocho etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en §3 (bloqueos), §5
(P-XX) ni §7 (desviaciones). §6: preguntas `#11`/`#12` siguen `(pendiente)` de respuesta del dueño,
sin novedad de esta sesión. `ROADMAP_PRODUCTO.md` no se toca en esta sesión (su prosa de "Oleada
v15 — EN CURSO"/R-27 `PENDIENTE` sigue desactualizada hasta el próximo ciclo de PM que la archive —
mismo patrón ya descrito y aceptado como de bajo riesgo en el hallazgo `#24`). Nota sin acción: cola
vacía hasta el siguiente ciclo de Product Manager.

**Última actualización anterior (2026-10-12, ciclo de Programador): R-27 implementada y verificada
con código** (cierra el bucle del aviso de guion modificado — `actualizar_info_guion` nuevo en
`scripts/estado.py`, `guion_modificado` propagado a la cabecera de `guion-escenas.md`, paso
explícito en `SKILL.md`; 4 tests nuevos, 665→669, cuatro redes en verde) (detalle en la nota de esa
sesión, más abajo).

**Ciclo de Programador (2026-10-12): R-27 implementada.** Revisión de entrada (protocolo):
`git checkout develop` encontró la rama local `develop` desactualizada y divergente de
`origin/develop` sin ancestro común (`cc0ac86`, la misma rama local obsoleta ya diagnosticada por
los ciclos de PM del 2026-10-10/11 y por el hallazgo `#21` del auditor — artefacto del `git clone`
de cada contenedor efímero, no una reescritura real); a diferencia de la sesión del 2026-10-11, en
esta sí fue posible ejecutar `git reset --hard origin/develop` (sin bloqueo del clasificador de
permisos esta vez), dejando `develop` apuntando exactamente a `origin/develop` (`0420c01`) sin
perder ningún commit real (la rama local obsoleta no contenía trabajo propio de ninguna sesión, solo
historial desactualizado). `git status` limpio antes y después. Dependencia de desarrollo instalada
con `python -m pip install -r requirements-dev.txt` (no con el `pip` desnudo del `PATH`, que resolvía
a un intérprete Python 3.13 distinto del `python`/`python3.11` que ejecuta el proyecto — las tres
herramientas quedaban instaladas pero invisibles para `scripts/ci.py`; detalle y decisión en
`DECISIONES_TECNICAS.md`).

Registro de hallazgos de `auditoriacontinua.md` (auditoría 2026-10-12, `0420c01`): dos `ABIERTO`,
ambos de proceso puro y sin relación con el código (`#24`, prosa de "Cola de producto" desactualizada
entre ciclos; `#30`, cadencia del Programador) — ninguno de severidad alta que atender como P-XX
urgente antes de la cola normal. §1 (fuente autoritativa) traía **R-27 como única fila
`PENDIENTE`**: implementada en esta sesión siguiendo al pie de la letra su spec de
`ROADMAP_PRODUCTO.md` (Oleada v15, verificada contra `DECISIONES_TECNICAS.md` antes de tocar código,
sin contradecir ninguna decisión previa).

**Implementación.** `scripts/estado.py` gana `actualizar_info_guion(estado, ruta_guion)`: refresca
`estado.guion.hash_sha256`/`tamano_bytes` al contenido actual del guion, mutando `estado` en el sitio
(mismo tratamiento que `actualizado_en` en `guardar_estado`), llamada justo antes de
`guardar_estado`. `documento_revision.generar_documento_revision` gana `guion_modificado: bool =
False` (mismo patrón que `tropiezos_por_escena` de R-03): con `True`, `_formatear_resumen_global`
añade una línea de aviso visible en la cabecera del resumen global, junto al resto de avisos de
transparencia ya existentes (ppm de T-12, diccionario del dueño de R-26, desviaciones de R-23).
`SKILL.md` dedica una instrucción explícita con el fragmento de código exacto (sección "Documento de
revisión de una sola pasada", mismo patrón que la instrucción del diccionario en R-26): tras cargar
`estado.json` y ANTES de re-parsear/regenerar, llamar a `estado.avisar_si_guion_modificado(estado,
ruta_guion)` y propagar su valor tal cual a `generar_documento_revision(...,
guion_modificado=...)`; llamar a `estado.actualizar_info_guion(estado, ruta_guion)` justo antes de
`guardar_estado`. Sin migración (solo se refrescan valores ya existentes de `InfoGuion`, mismo
esquema); `revalidar_guion` queda intacto, sin releer el guion de origen por su cuenta, tal como
exige el requisito 4 de la ficha. `DEVELOPERS.md` gana sección propia ("Cerrar el bucle del aviso de
guion modificado, R-27") con el mismo nivel de detalle que la de R-26.

**Verificación.** 4 tests nuevos (665→669): `tests/test_estado.py`
(`test_actualizar_info_guion_refresca_hash_y_tamano_al_contenido_actual`,
`test_actualizar_info_guion_cierra_el_aviso_de_guion_modificado` — confirma el criterio de
aceptación literal: tras refrescar, `avisar_si_guion_modificado` vuelve a `False` sin que el guion
cambie de nuevo, cerrando el bucle que motivó la tarea) y `tests/test_documento_revision.py`
(`test_guion_modificado_true_anade_linea_de_aviso_en_la_cabecera`,
`test_guion_modificado_false_por_defecto_no_anade_ninguna_linea`). Regresión de los tests existentes
de T-07/T-16 sin cambios de comportamiento. Cuatro redes en verde (`mypy`, `ruff`, 669 tests,
dieciocho etapas de `verificar_salidas.py --fixture`).

Sin cambios en §3 (bloqueos), §5 (P-XX) ni §7 (desviaciones). §6: preguntas `#11`/`#12` siguen
`(pendiente)` de respuesta del dueño, sin novedad de esta sesión. `ROADMAP_PRODUCTO.md` no se toca en
esta sesión (su prosa de "Oleada v15 — EN CURSO"/R-27 `PENDIENTE` queda desactualizada hasta el
próximo ciclo de PM que la archive — mismo patrón ya descrito y aceptado como de bajo riesgo en el
hallazgo `#24`, pendiente solo de la respuesta de gobernanza del dueño a la pregunta `#11`).

**Ciclo de Product Manager (2026-10-11): sin apertura de R-XX nueva.** Revisión de entrada
(protocolo): el contenedor arrancó con la rama local `develop` desactualizada (`cc0ac86`, muy por
detrás) y `HEAD` en un estado ajeno a cualquier rama local, con `origin/develop` en `48ae5f1` —
mismo síntoma ya diagnosticado y documentado por el ciclo de PM del 2026-10-10 (ref artefacto del
`git clone --depth` de cada contenedor efímero, no una reescritura real de `develop`; también
investigado en profundidad por el auditor como hallazgo `#21`, descartado). Esta sesión no pudo
usar `git reset --hard origin/develop` (el clasificador de permisos del modo automático bloqueó la
operación por destructiva, sin usuario en vivo que la confirmara); en su lugar se creó la rama
`work` apuntando a `origin/develop` (sin tocar ni descartar la rama local `develop`, que queda
simplemente obsoleta e inofensiva en este clon efímero) y todo el trabajo de esta sesión parte de
ahí, con push final a `work:develop`. `git status` limpio antes de tocar nada. No se instaló
`requirements-dev.txt` como dependencia de desarrollo para ejecutar las cuatro redes (ciclo de PM, no
toca código), solo para poder correr el reescaneo propio descrito abajo.

Registro de hallazgos de `auditoriacontinua.md` (commit `48ae5f1`, auditoría 2026-10-11, "cero
hallazgos nuevos"): dos `ABIERTO`, ambos reconfirmados sin cambio — `#24` (baja, proceso, pregunta
`#11` de §6 sigue `(pendiente)`, veinticinco pasadas) y `#30` (media, proceso, pregunta `#12` de §6
sigue `(pendiente)`, ya enrutada por el ciclo de PM anterior). Ninguno de severidad alta ni de
producto/arquitectura que convertir en R-XX. `roadmap/FEEDBACK.md` sigue con su única fila de
plantilla vacía, sin ninguna entrada `nuevo` — el bloqueo #7 de §3 (grabar un curso completo) sigue
sin resolverse, sin acción posible desde una sesión de nube.

§1 (fuente autoritativa) tiene a **R-27 como única fila `PENDIENTE`**, sin ningún ciclo de
Programador que la haya tocado desde que se abrió (2026-10-09): no es un síntoma del hallazgo `#30`
ni de ningún bloqueo nuevo, sino lo esperado — la rutina "Programador" dispara en cron de lunes a
viernes (`0 6-15 * * 1-5`, ver bloqueo histórico #8 de §3) y el 2026-10-10/11 caen en fin de semana
(sábado/domingo, verificado). No se abre ninguna R-XX nueva este ciclo: mismo criterio que los
ciclos de PM "sin apertura" anteriores, nunca más de una R-XX pendiente de código a la vez sin
evidencia real que lo justifique.

**Verificación propia añadida esta sesión (diligencia del PM, no exigida por protocolo pero sí por
buena práctica dado que llevan ya tres ciclos de PM seguidos sin encontrar nada nuevo):** se repite,
de forma independiente, el barrido de funciones públicas de `scripts/*.py` sin llamador real fuera
de sus propios tests que usó el ciclo de PM del 2026-10-09 para abrir R-27 (script de Python propio,
AST + `grep` por archivo y línea, excluyendo la propia línea de definición). Resultado: exactamente
las mismas seis candidatas que ya constan en el historial — `avisar_si_guion_modificado`/
`guion_modificado` (ya convertida en R-27, `PENDIENTE`), `cargar_estado` (descartada: primitiva de
orquestación invocada directamente por la sesión, no por otro módulo de `scripts/`),
`contraste_relativo` y `deshacer_normalizaciones` (descartadas: utilidades de verificación sin
producto perdido), `ejecutar_con_limite_de_tiempo` (reconfirmada como alternativa de menor severidad
a R-27, mismo análisis que en 2026-10-09, sin incidente nuevo en §4 que lo eleve) — más una séptima,
`InformeCalibracion.mostrar_informe` (`scripts/calibracion.py`), que el barrido marca por error como
huérfana porque es un **método** de clase (el AST no distingue función suelta de método) invocado
directamente por la sesión que orquesta la skill tras `calcular_calibracion(...)`, exactamente el
mismo patrón que `cargar_estado` y documentado tal cual en `DEVELOPERS.md:1889`: falso positivo, no
candidata real. Cero grieta nueva de severidad igual o mayor que R-27. Confirma, con evidencia
propia e independiente (no solo con la palabra del ciclo que abrió R-27), que la cola de una sola
R-XX pendiente sigue siendo la correcta y que no hay ningún hallazgo urgente escondido detrás de
tres ciclos de PM seguidos "sin apertura".

Sin cambios en §3 (bloqueos), §5 (P-XX), §6 (preguntas `#11`/`#12` siguen `(pendiente)`) ni §7
(desviaciones). `ROADMAP_PRODUCTO.md` no se toca: su prosa de "Oleada v15 — EN CURSO"/R-27
`PENDIENTE` ya es correcta. Este ciclo es de PM, no de Programador: no se ha ejecutado la
verificación de las cuatro redes ni se ha tocado `scripts/`, `tests/` ni `assets/` (el reescaneo de
esta sesión es de solo lectura).

**Última actualización anterior (2026-10-10, ciclo de Product Manager): sin apertura de R-XX
nueva**, enruta el hallazgo `#30` como pregunta `#12` de §6, sin tocar código (detalle en la nota de
esa sesión, más abajo).

**Ciclo de Product Manager (2026-10-10): sin apertura de R-XX nueva.** Revisión de entrada
(protocolo): `git checkout develop && git pull origin develop` trajo el repositorio hasta `fd34455`
en fast-forward limpio (la auditoría del 2026-10-10, posterior al ciclo de PM del 2026-10-09 que
abrió R-27). §1 (fuente autoritativa) tiene a **R-27 como única fila `PENDIENTE`**: no se abre
ninguna R-XX nueva este ciclo porque ya hay trabajo de código en cola sin empezar — mismo criterio
que los ciclos de PM "sin apertura" anteriores (p. ej. 2026-10-04 con R-22 `PENDIENTE`), nunca más
de una R-XX pendiente de código a la vez sin evidencia real que lo justifique.

Registro de hallazgos de `auditoriacontinua.md` (commit `fd34455`, pasada 2026-10-10): dos
`ABIERTO`. `#24` (baja, proceso, prosa de "Cola de producto" desactualizada entre ciclos de PM) se
reconfirma una vez más sin acción nueva — sigue enrutado a la pregunta `#11` de §6, todavía
`(pendiente)` de respuesta del dueño, y no aplica esta vez porque `ROADMAP_PRODUCTO.md` ya describe
correctamente "Oleada v15 — EN CURSO"/R-27 `PENDIENTE` desde su propio commit de apertura.
**`#30` (media, nuevo esta pasada) sí requiere acción del PM:** la rutina "Programador" dispara en
cron horario durante toda la jornada y repite el protocolo completo de verificación (clon,
`pip install`, las cuatro redes) en cada reconfirmación aunque no haya tarea pendiente en §1 —
patrón que el propio ciclo de Programador señaló dos veces seguidas (notas de la octava y novena
reconfirmación del 2026-10-09) sin que nadie le diera curso hasta esta pasada del auditor. No es un
hallazgo de código ni de arquitectura de producto: el propio auditor cita dos posibles remedios
(espaciar el cron, o añadir al protocolo una comprobación barata de "cola vacía" antes de ejecutar
las cuatro redes), y ambos son decisión de configuración de la rutina y de protocolo
(`HOJA_DE_RUTA.md` §0.1), reservada al dueño — ni el PM ni el Programador pueden concedérsela por su
cuenta. Se enruta como pregunta de gobernanza nueva, `#12` de §6 (ver abajo), mismo tratamiento que
ya recibió `#24` con la `#11`. Razonamiento completo en `DECISIONES_TECNICAS.md` (entrada de esta
fecha).

`roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin ninguna entrada `nuevo` que
incorporar — el bloqueo #7 de §3 (grabar un curso completo) sigue sin resolverse, sin acción posible
desde una sesión de nube.

Sin cambios en §3 (bloqueos) ni §5 (P-XX); §7 sin nueva desviación. Este ciclo es de PM, no de
Programador: no se ha ejecutado la verificación de las cuatro redes ni se ha tocado `scripts/`,
`tests/` ni `assets/`.

**Última actualización anterior (2026-10-09, ciclo de Product Manager): archiva Oleada v14 (R-26) y
abre R-27 (Oleada v15)**, sin tocar código (detalle en la nota de esa sesión, más abajo).

**Ciclo de Product Manager: archiva Oleada v14 (R-26) y abre R-27 (Oleada v15).** Revisión de
entrada (protocolo): `git checkout develop && git pull origin develop` trajo el repositorio hasta
`56501ea` en fast-forward limpio. Registro de hallazgos de `auditoriacontinua.md`: un único
`ABIERTO` (`#24`, baja severidad, puramente de proceso — la pregunta de gobernanza #11 de §6 sigue
`(pendiente)`, veintitrés pasadas consecutivas de auditoría) y ninguno de severidad alta ni de
producto/arquitectura que convertir en R-XX nueva este ciclo (la propia auditoría del 2026-10-09 lo
confirma: "cero hallazgos nuevos"). `roadmap/FEEDBACK.md` sigue con su única fila de plantilla
vacía, sin ninguna entrada `nuevo` que incorporar — el bloqueo #7 de §3 (grabar un curso completo)
sigue sin resolverse, sin acción posible desde una sesión de nube. §1 (fuente autoritativa) tenía a
R-26 como `COMPLETADA` desde el mismo commit del ciclo de Programador del 2026-10-09 que la abrió e
implementó (`cdafa5b`), sin ningún patrón de latencia que corregir. Este ciclo mueve Oleada v14
(R-26) íntegra a `roadmap/ROADMAP_HISTORICO.md` (spec completa + "Cómo se entregó", commit
`cdafa5b`, 13 tests nuevos 652→665) y corrige la cabecera y la prosa de `ROADMAP_PRODUCTO.md`.

**Se abre R-27** (Oleada v15) por grieta de arquitectura verificada, mismo criterio que abrió R-12 a
R-26: `scripts/estado.py::avisar_si_guion_modificado` (T-07) existe para avisar al dueño cuando el
guion de origen cambió desde la última pasada, pero no tiene ningún llamador real fuera de sus
propios tests (`grep -rn "guion_modificado" scripts/*.py`) ni mención en `SKILL.md` (`grep -n
"guion_modificado" SKILL.md`, sin resultado). Agrava el hueco un segundo defecto verificado en la
misma pasada: `InfoGuion.hash_sha256`/`tamano_bytes` solo se escriben una vez, en `estado_inicial`
(`grep -rn "InfoGuion(" scripts/*.py`), así que un wiring ingenuo haría que el aviso se repitiera en
todas las pasadas futuras tras el primer cambio real, en vez de aparecer una sola vez — ruido, no
señal. Candidata alternativa descartada tras la misma verificación:
`scripts/entrada.py::ejecutar_con_limite_de_tiempo` (T-06) tiene el mismo patrón de ausencia de
llamador real, pero de menor severidad (defensa en profundidad sin incidente registrado en §4, frente
a una señal de transparencia que el dueño notaría directamente). Spec completa de R-27 en
`ROADMAP_PRODUCTO.md` (Oleada v15), lista para que el siguiente ciclo de Programador la implemente y
verifique. Este ciclo es de PM, no de Programador: no se ha ejecutado la verificación de las cuatro
redes ni se ha tocado `scripts/`, `tests/` ni `assets/`.

Sin cambios en §3 (bloqueos) ni §5 (P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`); sin
nueva desviación en §7.

**Última actualización anterior (2026-10-09, ciclo de Programador): novena reconfirmación del día tras
R-26**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, novena reconfirmación del día tras R-26,
2026-10-09):** sin incidencia. `git status` limpio antes de tocar nada; el contenedor arrancó con
`HEAD` *detached*, resto de un contenedor anterior ya fusionado en `develop`; `git checkout develop`
dejó la rama local atrás; `git fetch`/`git pull origin develop` resolvió en fast-forward limpio
hasta `29d377b` (octava reconfirmación del día tras R-26), sin conflicto ni rama divergida. `pip
install -r requirements-dev.txt` pelado volvió a instalar contra Python 3.13 en vez del 3.11 real
del proyecto — mismo síntoma de siempre, ya cubierto por la documentación desde P-06 (hallazgo
`#28`); resuelto con `python3 -m pip install -r requirements-dev.txt` (Python 3.11.17,
`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador de esa sesión: novena reconfirmación del día tras R-26**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: un único
`ABIERTO` (`#24`, baja, proceso, pregunta de gobernanza #11 de §6 sigue `(pendiente)`, veintitrés
pasadas consecutivas). Ninguno de severidad alta que atender como P-XX urgente antes de esta
tarea. `roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin ninguna entrada
`nuevo`; `mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/teleprompter`: cero
issues y cero PR abiertos. §1 (fuente autoritativa) sigue sin ninguna R-XX/T-XX `PENDIENTE` (R-26
es la última, `COMPLETADA`): cola de la columna vertebral vacía, sin tarea de código que ejecutar
ni hallazgo nuevo que convertir en P-XX. `ROADMAP_PRODUCTO.md` sigue describiendo "Oleada v14 — EN
CURSO"/R-26 como prosa aún sin archivar — mismo patrón de `#24`, sin tocarlo (corresponde al
siguiente ciclo de PM, no al de Programador; la pregunta de gobernanza #11 sigue sin respuesta).
Verificación propia completa (`python scripts/ci.py`): `mypy`/`ruff` en verde sin hallazgos (70
archivos), 665 tests (`pytest`, sin cambio) en verde, dieciocho etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en §3 (bloqueos) ni §5
(P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`); sin nueva desviación en §7. Nota sin
acción: cola vacía hasta el siguiente ciclo de Product Manager. **Observación de esta sesión, fuera
del protocolo de estado:** van ya nueve reconfirmaciones consecutivas del Programador en el mismo
día (2026-10-09) sin ningún cambio de código, porque §1 lleva vacío desde que R-26 se completó esta
misma madrugada; no hay ninguna acción nueva que tomar por protocolo (la cola solo la rellena un
ciclo de PM o una respuesta del dueño a la pregunta #11), pero la cadencia de disparo de esta rutina
programada frente al ritmo real de trabajo pendiente sigue mereciendo una revisión del dueño —
misma observación ya registrada en la sesión anterior, aún sin respuesta.

**Última actualización anterior (2026-10-09, ciclo de Programador): octava reconfirmación del día
tras R-26**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, octava reconfirmación del día tras R-26,
2026-10-09):** sin incidencia. `git status` limpio antes de tocar nada; el contenedor arrancó con
`HEAD` *detached*, resto de un contenedor anterior ya fusionado en `develop`; `git checkout develop`
dejó la rama local atrás (`-B develop origin/develop`); `git fetch`/`git pull origin develop`
resolvió en fast-forward limpio hasta `3ebdf09` (séptima reconfirmación del día tras R-26), sin
conflicto ni rama divergida. `pip install -r requirements-dev.txt` pelado volvió a instalar contra
Python 3.13 en vez del 3.11 real del proyecto — mismo síntoma de siempre, ya cubierto por la
documentación desde P-06 (hallazgo `#28`); resuelto con `python3 -m pip install -r
requirements-dev.txt` (Python 3.11.17, `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador de esa sesión: octava reconfirmación del día tras R-26**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: un único
`ABIERTO` (`#24`, baja, proceso, pregunta de gobernanza #11 de §6 sigue `(pendiente)`, veintitrés
pasadas consecutivas). Ninguno de severidad alta que atender como P-XX urgente antes de esta
tarea. `roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin ninguna entrada
`nuevo`; `mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/teleprompter`: cero
issues y cero PR abiertos. §1 (fuente autoritativa) sigue sin ninguna R-XX/T-XX `PENDIENTE` (R-26
es la última, `COMPLETADA`): cola de la columna vertebral vacía, sin tarea de código que ejecutar
ni hallazgo nuevo que convertir en P-XX. `ROADMAP_PRODUCTO.md` sigue describiendo "Oleada v14 — EN
CURSO"/R-26 como prosa aún sin archivar — mismo patrón de `#24`, sin tocarlo (corresponde al
siguiente ciclo de PM, no al de Programador; la pregunta de gobernanza #11 sigue sin respuesta).
Verificación propia completa (`python scripts/ci.py`): `mypy`/`ruff` en verde sin hallazgos (70
archivos), 665 tests (`pytest`, sin cambio) en verde, dieciocho etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en §3 (bloqueos) ni §5
(P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`); sin nueva desviación en §7. Nota sin
acción: cola vacía hasta el siguiente ciclo de Product Manager. **Observación de esta sesión, fuera
del protocolo de estado:** van ya ocho reconfirmaciones consecutivas del Programador en el mismo
día (2026-10-09) sin ningún cambio de código, porque §1 lleva vacío desde que R-26 se completó esta
misma madrugada; no hay ninguna acción nueva que tomar por protocolo (la cola solo la rellena un
ciclo de PM o una respuesta del dueño a la pregunta #11), pero la cadencia de disparo de esta rutina
programada frente al ritmo real de trabajo pendiente puede merecer una revisión del dueño.

**Última actualización anterior (2026-10-09, ciclo de Programador): séptima reconfirmación del día
tras R-26**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, séptima reconfirmación del día tras R-26,
2026-10-09):** sin incidencia. `git status` limpio antes de tocar nada; el contenedor arrancó con
`HEAD` *detached*, resto de un contenedor anterior ya fusionado en `develop`; `git checkout develop`
dejó la rama local atrás; `git pull origin develop` resolvió en fast-forward limpio hasta `b652466`
(sexta reconfirmación del día tras R-26), sin conflicto ni rama divergida. `pip install -r
requirements-dev.txt` pelado volvió a instalar contra Python 3.13 en vez del 3.11 real del proyecto
— mismo síntoma de siempre, ya cubierto por la documentación desde P-06 (hallazgo `#28`); resuelto
con `python3 -m pip install -r requirements-dev.txt` (Python 3.11.17, `mypy==1.18.2`,
`ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador de esa sesión: séptima reconfirmación del día tras R-26**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: un único
`ABIERTO` (`#24`, baja, proceso, pregunta de gobernanza #11 de §6 sigue `(pendiente)`, veintitrés
pasadas consecutivas). Ninguno de severidad alta que atender como P-XX urgente antes de esta
tarea. `roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin ninguna entrada
`nuevo`; `mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/teleprompter`: cero
issues y cero PR abiertos. §1 (fuente autoritativa) sigue sin ninguna R-XX/T-XX `PENDIENTE` (R-26
es la última, `COMPLETADA`): cola de la columna vertebral vacía, sin tarea de código que ejecutar
ni hallazgo nuevo que convertir en P-XX. `ROADMAP_PRODUCTO.md` sigue describiendo "Oleada v14 — EN
CURSO"/R-26 como prosa aún sin archivar — mismo patrón de `#24`, sin tocarlo (corresponde al
siguiente ciclo de PM, no al de Programador; la pregunta de gobernanza #11 sigue sin respuesta).
Verificación propia completa (`python scripts/ci.py`): `mypy`/`ruff` en verde sin hallazgos (70
archivos), 665 tests (`pytest`, sin cambio) en verde, dieciocho etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en §3 (bloqueos) ni §5
(P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`); sin nueva desviación en §7. Nota sin
acción: cola vacía hasta el siguiente ciclo de Product Manager.

**Última actualización anterior (2026-10-09, ciclo de Programador): sexta reconfirmación del día
tras R-26**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, sexta reconfirmación del día tras R-26,
2026-10-09):** sin incidencia. `git status` limpio antes de tocar nada; `git checkout develop`
dejó la rama local atrás (el contenedor arrancó con `HEAD` *detached*, resto de un contenedor
anterior ya fusionado en `develop`); `git pull origin develop` resolvió en fast-forward limpio
hasta `bd5fd54` (quinta reconfirmación del día tras R-26), sin conflicto ni rama divergida. `pip
install -r requirements-dev.txt` pelado volvió a instalar contra Python 3.13 en vez del 3.11 real
del proyecto — mismo síntoma de siempre, ya cubierto por la documentación desde P-06 (hallazgo
`#28`); resuelto con `python3 -m pip install -r requirements-dev.txt` (Python 3.11.17,
`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador de esa sesión: sexta reconfirmación del día tras R-26**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: un único
`ABIERTO` (`#24`, baja, proceso, pregunta de gobernanza #11 de §6 sigue `(pendiente)`, veintitrés
pasadas consecutivas). Ninguno de severidad alta que atender como P-XX urgente antes de esta
tarea. `roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin ninguna entrada
`nuevo`; `mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/teleprompter`: cero
issues y cero PR abiertos. §1 (fuente autoritativa) sigue sin ninguna R-XX/T-XX `PENDIENTE` (R-26
es la última, `COMPLETADA`): cola de la columna vertebral vacía, sin tarea de código que ejecutar
ni hallazgo nuevo que convertir en P-XX. `ROADMAP_PRODUCTO.md` sigue describiendo "Oleada v14 — EN
CURSO"/R-26 como prosa aún sin archivar — mismo patrón de `#24`, sin tocarlo (corresponde al
siguiente ciclo de PM, no al de Programador; la pregunta de gobernanza #11 sigue sin respuesta).
Verificación propia completa (`python scripts/ci.py`): `mypy`/`ruff` en verde sin hallazgos (70
archivos), 665 tests (`pytest`, sin cambio) en verde, dieciocho etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en §3 (bloqueos) ni §5
(P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`); sin nueva desviación en §7. Nota sin
acción: cola vacía hasta el siguiente ciclo de Product Manager.

**Última actualización anterior (2026-10-09, ciclo de Programador): quinta reconfirmación del día
tras R-26**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, segunda reconfirmación del día tras R-26,
2026-10-09):** sin incidencia. `git status` limpio antes de tocar nada; el contenedor arrancó ya en
`develop`, sin *detached HEAD*; `git pull origin develop` resolvió en fast-forward limpio hasta
`e90323b` (primera reconfirmación del día tras R-26), sin conflicto ni rama divergida. `python3 -m
pip install -r requirements-dev.txt` resolvió directamente al intérprete correcto (Python 3.11,
`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`), sin reproducir esta vez el síntoma del `pip`
pelado del hallazgo `#28`.

**Ciclo de Programador de esa sesión: segunda reconfirmación del día tras R-26**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: un único
`ABIERTO` (`#24`, baja, proceso, pregunta de gobernanza #11 de §6 sigue `(pendiente)`, veintitrés
pasadas consecutivas). Ninguno de severidad alta que atender como P-XX urgente antes de esta
tarea. `roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin ninguna entrada
`nuevo`; `mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/teleprompter`: cero
issues y cero PR abiertos. §1 (fuente autoritativa) sigue sin ninguna R-XX/T-XX `PENDIENTE` (R-26
es la última, `COMPLETADA`): cola de la columna vertebral vacía, sin tarea de código que ejecutar
ni hallazgo nuevo que convertir en P-XX. `ROADMAP_PRODUCTO.md` sigue describiendo "Oleada v14 — EN
CURSO"/R-26 como prosa aún sin archivar — mismo patrón de `#24`, sin tocarlo (corresponde al
siguiente ciclo de PM, no al de Programador; la pregunta de gobernanza #11 sigue sin respuesta).
Verificación propia completa (`python scripts/ci.py`): `mypy`/`ruff` en verde sin hallazgos (70
archivos), 665 tests (`pytest`, sin cambio) en verde, dieciocho etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en §3 (bloqueos) ni §5
(P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`); sin nueva desviación en §7. Nota sin
acción: cola vacía hasta el siguiente ciclo de Product Manager.

**Última actualización anterior (2026-10-09, ciclo de Programador): primera reconfirmación del día
tras R-26**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, primera reconfirmación del día tras R-26,
2026-10-09):** sin incidencia. `git status` limpio antes de tocar nada; `git checkout develop`
dejó la rama local atrás (el contenedor arrancó en `develop`, sin *detached HEAD*); `git pull
origin develop` resolvió en fast-forward limpio hasta `cdafa5b` (R-26 implementada y
`COMPLETADA`), sin conflicto ni rama divergida. `pip install -r requirements-dev.txt` pelado
volvió a instalar contra Python 3.13 en vez del 3.11 real del proyecto — mismo síntoma de siempre,
ya cubierto por la documentación desde P-06 (hallazgo `#28`); resuelto con `python3 -m pip install
-r requirements-dev.txt`.

**Ciclo de Programador de esa sesión: primera reconfirmación del día tras R-26**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: un único
`ABIERTO` (`#24`, baja, proceso, pregunta de gobernanza #11 de §6 sigue `(pendiente)`, veintitrés
pasadas consecutivas). Ninguno de severidad alta que atender como P-XX urgente antes de esta
tarea. `roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin ninguna entrada
`nuevo`; `mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/teleprompter`: cero
issues y cero PR abiertos. §1 (fuente autoritativa) sigue sin ninguna R-XX/T-XX `PENDIENTE` (R-26
es la última, `COMPLETADA`): cola de la columna vertebral vacía, sin tarea de código que ejecutar
ni hallazgo nuevo que convertir en P-XX. Verificación propia completa (`python scripts/ci.py`):
`mypy`/`ruff` en verde sin hallazgos (70 archivos), 665 tests (`pytest`, sin cambio) en verde,
dieciocho etapas OK en `verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en
§3 (bloqueos) ni §5 (P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`); sin nueva
desviación en §7. Nota sin acción: cola vacía hasta el siguiente ciclo de Product Manager.

**Última actualización anterior (2026-10-09, ciclo de Programador): R-26 implementada y
`COMPLETADA`**, sin más novedad (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, implementación de R-26, 2026-10-09):**
sin incidencia. `git status` limpio antes de tocar nada; el contenedor arrancó con `HEAD`
*detached*, resto de un contenedor anterior ya fusionado en `develop`; `git checkout develop`
dejó la rama local atrás; `git pull origin develop` resolvió en fast-forward limpio hasta
`8f31c3c` (38 commits por detrás, la auditoría del 2026-10-09 y el resto de sesiones del día
anterior), sin conflicto ni rama divergida. `pip install -r requirements-dev.txt` pelado volvió a
instalar contra Python 3.13 en vez del 3.11 real del proyecto — mismo síntoma de siempre, ya
cubierto por la documentación desde P-06 (hallazgo `#28`); resuelto con `python3 -m pip install -r
requirements-dev.txt`. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder:
un único `ABIERTO` (`#24`, baja, proceso, pregunta de gobernanza #11 de §6 sigue `(pendiente)`),
ninguno de severidad alta que atender como P-XX urgente. §1 (fuente autoritativa) traía a R-26 como
única fila `PENDIENTE`: siguiente tarea de la cola, implementada esa sesión.

**Ciclo de Programador de esa sesión: R-26 implementada y `COMPLETADA`.** Cierra la grieta
verificada por el PM el 2026-10-08: el diccionario del dueño (`diccionario-locucion.json`, T-13)
no tenía ningún llamador real fuera de sus propios tests. `scripts/revalidacion.py::revalidar_guion`
gana `carpeta_salida: Path | None = None`: si no se pasa un `diccionario` explícito (uso típico de
un test unitario, sin tocar disco), lo carga por su cuenta con `normalizacion.
cargar_diccionario_locucion` antes de normalizar — un `diccionario` explícito siempre gana.
`scripts/documento_revision.py::generar_documento_revision` gana el mismo parámetro opcional, pero
sin recalcular nada (invariante del propio módulo desde T-16): cuenta cuántas `reescrituras` ya
recibidas vienen de la familia `diccionario` y lo muestra siempre en la cabecera ("Diccionario del
dueño aplicado: N entradas"); con `carpeta_salida`, además, si el archivo existe con entradas pero
ninguna se aplicó, añade un aviso explícito — la señal exacta de la grieta original, nunca una
omisión silenciosa. `scripts/pptx.py::generar_tarjetas`/`exportar_pptx` ganan
`entradas_diccionario_aplicadas: int = 0`, el mismo recuento pasado tal cual hasta
`tarjetas.json.metadatos` (cero segunda implementación: `pptx.py` no conoce `Reescritura`).
`SKILL.md` (sección T-13) documenta el paso obligatorio con el fragmento de código exacto, mismo
patrón que ya usa la instrucción de `tropiezos_por_escena` de R-03. `references/contrato-tarjetas.md`
documenta la clave nueva de metadatos. 13 tests nuevos (652→665): 5 en `tests/test_documento_revision.py`
(cabecera cuenta 0/N, sin `carpeta_salida` nunca hay aviso, con diccionario sin aplicar SÍ avisa,
con diccionario aplicado no avisa), 3 en `tests/test_revalidacion.py` (carga real desde disco sin
construirlo a mano, un `diccionario` explícito gana sobre `carpeta_salida`, sin cambio de
comportamiento si no se usa ninguno de los dos), 4 en `tests/test_pptx.py` (el campo se pasa tal
cual a `generar_tarjetas`/`exportar_pptx`/`tarjetas_a_diccionario`, por defecto en `0`) y 1 test de
integración en `tests/test_integracion_montaje.py` que escribe el diccionario real en disco y
comprueba el mismo recuento en `guion-escenas.md` y `tarjetas.json` a la vez — el criterio de
aceptación literal de la ficha, sin construir el diccionario a mano en memoria como sí hacían los
tests de T-13. Fixture dorada `fixtures/guion-ejemplo-esperado.md` regenerada (único cambio: la
línea nueva de cabecera, en 0 porque el guion de ejemplo no trae diccionario). Verificación
pre-push completa (`python scripts/ci.py`): `mypy`/`ruff` en verde sin hallazgos (70 archivos), 665
tests (`pytest`, 652→665) en verde, dieciocho etapas OK en `verificar_salidas.py --fixture` (sin
cambio: ninguna salida nueva, solo un campo más en una ya existente). Las cuatro redes en verde.
Sin cambios en §3
(bloqueos) ni §5 (P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`); sin nueva desviación
en §7. §1 pasa R-26 de `PENDIENTE` a `COMPLETADA` y queda sin ninguna R-XX/T-XX `PENDIENTE`: cola
vacía hasta el siguiente ciclo de Product Manager.

**Última actualización anterior (2026-10-08, ciclo de Product Manager): archiva Oleada v13 (R-25) y
abre R-26 (Oleada v14)**, sin tocar código (detalle en la nota de esa sesión, más abajo).

**Ciclo de Product Manager: archiva Oleada v13 (R-25) y abre R-26 (Oleada v14).** Revisión de
entrada (protocolo): registro de hallazgos de `auditoriacontinua.md` reconfirma dos `ABIERTO`, ambos
baja severidad y ya enrutados sin necesitar R-XX — `#24` (proceso, la pregunta de gobernanza #11 de
§6 sigue `(pendiente)`, veintidós pasadas consecutivas de auditoría) y `#29` (la fila de R-25 faltaba
en §1 al abrirse la tarea; ya resuelto por el propio ciclo de Programador que implementó R-25 el
mismo día en que se detectó, añadiendo la fila al §1 vigente — el cierre a `RESUELTO` en
`auditoriacontinua.md` queda para la siguiente pasada de auditoría). Ninguno de severidad alta ni de
producto/arquitectura que convertir en R-XX nueva este ciclo. `roadmap/FEEDBACK.md` sigue con su
única fila de plantilla vacía, sin ninguna entrada `nuevo` que incorporar — el bloqueo #7 de §3
(grabar un curso completo) sigue sin resolverse. §1 (fuente autoritativa) tenía a R-25 como
`COMPLETADA` desde el mismo commit del ciclo de Programador del 2026-10-08 que la abrió e implementó,
sin el patrón de latencia que motivó `#24` esta vez. Este ciclo corrige la cabecera y la prosa de
`ROADMAP_PRODUCTO.md`: Oleada v13 (R-25) se mueve íntegra a `roadmap/ROADMAP_HISTORICO.md` (spec
completa + "Cómo se entregó"), con su entrada de índice correspondiente.

**Se abre R-26** (Oleada v14) por grieta de arquitectura verificada, mismo criterio que abrió R-12 a
R-25, esta vez de severidad mayor: no una salida sin consumidor, sino una garantía contractual del
propio `SKILL.md`/T-13 ("el diccionario del dueño manda siempre") que hoy no se cumple en el flujo
real. Verificación propia, leyendo el código línea a línea: `scripts/normalizacion.py::
cargar_diccionario_locucion` (lee `diccionario-locucion.json` de disco) no tiene ningún llamador fuera
de sus propios tests (`grep -rn "cargar_diccionario_locucion" scripts/*.py`, único resultado la propia
definición); los cuatro puntos reales que deberían aplicar el diccionario
(`normalizacion.normalizar_guion`, `reescrituras.recopilar_propuestas`,
`documento_revision.generar_documento_revision`, `revalidacion.revalidar_guion`) tampoco tienen,
fuera de sus tests, ningún llamador que construya un diccionario cargado de disco y lo propague —
todos reciben `diccionario=None` por omisión en cualquier uso real sobre un guion real. Los propios
tests de T-13 prueban por separado "cargar el archivo" y "un diccionario en memoria sobrescribe la
regla automática", nunca las dos cosas juntas sobre un archivo real en la carpeta de salida de un
guion real — el camino que el dueño de verdad usaría. Candidata alternativa descartada tras la misma
verificación: `scripts/reescrituras.py::revertir_reescrituras` (T-15, deshacer global) sigue sin
disparador documentado, pero ya se consideró y descartó al abrir R-25 por menor valor y mayor riesgo
de diseño (ninguna superficie hoy por la que el dueño dispare un "deshacer global"); nada cambia ese
análisis esta pasada. Spec completa de R-26 en `ROADMAP_PRODUCTO.md` (Oleada v14), lista para que el
siguiente ciclo de Programador la implemente y verifique. Este ciclo es de PM, no de Programador: no
se ha ejecutado la verificación de las cuatro redes ni se ha tocado `scripts/`, `tests/` ni `assets/`.

Sin cambios en §3 (bloqueos) ni §5 (P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`); sin
nueva desviación en §7.

**Última actualización anterior (2026-10-08, ciclo de Programador): novena reconfirmación del día tras
R-25**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esta sesión (ciclo de Programador, novena reconfirmación del día tras R-25,
2026-10-08):** sin incidencia. `git status` limpio antes de tocar nada; el contenedor arrancó con
`HEAD` *detached* en `b15f852` (resto de un contenedor anterior, descartable: ya fusionado en
`develop`); `git checkout develop` dejó la rama local en `cc0ac86`; `git pull origin develop`
resolvió en fast-forward limpio hasta `b15f852` (la octava reconfirmación del día tras R-25, sin
ningún commit nuevo entre medias), sin conflicto ni rama divergida. El `pip` pelado de este
contenedor volvió a instalar contra Python 3.13 en vez del 3.11.17 real del proyecto (confirmado con
`pip --version`: `python 3.13`) — mismo síntoma del hallazgo `#28`, reproducido una vez más;
resuelto con `python3 -m pip install -r requirements-dev.txt`, que sí resuelve al intérprete
correcto (mismas versiones pineadas: `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador de esta sesión: novena reconfirmación del día tras R-25**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: dos `ABIERTO`,
ambos de severidad baja — `#24` (proceso, pregunta de gobernanza #11 de §6 sigue `(pendiente)`) y
`#29` (proceso, la fila de R-25 ya añadida a §1 por la sesión que la implementó, con la
recomendación de cierre de ese mismo hallazgo ya ejecutada; el cierre a `RESUELTO` en
`auditoriacontinua.md` queda para la siguiente pasada del auditor, que es quien modifica ese
archivo). Ninguno de severidad alta que atender como P-XX urgente antes de esta tarea.
`roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin ninguna entrada `nuevo`;
`mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/teleprompter`: cero issues y
cero PR abiertos. §1 (fuente autoritativa) sigue sin ninguna R-XX/T-XX `PENDIENTE` (R-25 es la
última, `COMPLETADA`): cola de la columna vertebral vacía, sin tarea de código que ejecutar ni
hallazgo nuevo que convertir en P-XX. Verificación propia completa (`python scripts/ci.py`):
`mypy`/`ruff` en verde sin hallazgos (70 archivos), 652 tests (`pytest`, sin cambio) en verde,
dieciocho etapas OK en `verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en
§3 (bloqueos) ni §5 (P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`); sin nueva
desviación en §7. Nota sin acción: cola vacía hasta el siguiente ciclo de Product Manager.

**Última actualización anterior (2026-10-08, ciclo de Programador): octava reconfirmación del día
tras R-25**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, sexta reconfirmación del día tras R-25,
2026-10-08):** sin incidencia. `git status` limpio antes de tocar nada; el contenedor arrancó con
`HEAD` *detached* en `ee86dd2` (resto de un contenedor anterior, descartable: ya fusionado en
`develop`); `git checkout develop` dejó la rama local en `cc0ac86`; `git pull origin develop`
resolvió en fast-forward limpio hasta `ee86dd2` (la quinta reconfirmación del día tras R-25, sin
ningún commit nuevo entre medias), sin conflicto ni rama divergida. `python3 -m pip install -r
requirements-dev.txt` resolvió directamente al intérprete correcto (mismas versiones pineadas:
`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`), sin reproducir esta vez el síntoma del `pip`
pelado del hallazgo `#28`.

**Ciclo de Programador de esa sesión: sexta reconfirmación del día tras R-25**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: dos `ABIERTO`,
ambos de severidad baja — `#24` (proceso, pregunta de gobernanza #11 de §6 sigue `(pendiente)`) y
`#29` (proceso, la fila de R-25 ya añadida a §1 por la sesión que la implementó, con la
recomendación de cierre de ese mismo hallazgo ya ejecutada; el cierre a `RESUELTO` en
`auditoriacontinua.md` queda para la siguiente pasada del auditor, que es quien modifica ese
archivo). Ninguno de severidad alta que atender como P-XX urgente antes de esta tarea.
`roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin ninguna entrada `nuevo`;
`mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/teleprompter`: cero issues y
cero PR abiertos. §1 (fuente autoritativa) sigue sin ninguna R-XX/T-XX `PENDIENTE` (R-25 es la
última, `COMPLETADA`): cola de la columna vertebral vacía, sin tarea de código que ejecutar ni
hallazgo nuevo que convertir en P-XX. Verificación propia completa (`python scripts/ci.py`):
`mypy`/`ruff` en verde sin hallazgos (70 archivos), 652 tests (`pytest`, sin cambio) en verde,
dieciocho etapas OK en `verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en
§3 (bloqueos) ni §5 (P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`); sin nueva
desviación en §7. Nota sin acción: cola vacía hasta el siguiente ciclo de Product Manager.

**Última actualización anterior (2026-10-08, ciclo de Programador): quinta reconfirmación del día
tras R-25**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, quinta reconfirmación del día tras R-25,
2026-10-08):** sin incidencia. `git status` limpio antes de tocar nada; el contenedor arrancó con
`HEAD` *detached* en `3f2e1b6` (resto de un contenedor anterior, descartable: ya fusionado en
`develop`); `git checkout develop` dejó la rama local en `cc0ac86`; `git pull origin develop`
resolvió en fast-forward limpio hasta `3f2e1b6` (la cuarta reconfirmación del día tras R-25, sin
ningún commit nuevo entre medias), sin conflicto ni rama divergida. `pip install -r
requirements-dev.txt` con el `pip` pelado de este contenedor instaló de nuevo contra Python 3.13 en
vez del 3.11.17 real del proyecto — mismo síntoma del hallazgo `#28`, reproducido una vez más;
resuelto con `python3 -m pip install -r requirements-dev.txt`, que sí resuelve al intérprete
correcto (mismas versiones pineadas: `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador de esa sesión: quinta reconfirmación del día tras R-25**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: dos `ABIERTO`,
ambos de severidad baja — `#24` (proceso, pregunta de gobernanza #11 de §6 sigue `(pendiente)`) y
`#29` (proceso, la fila de R-25 ya añadida a §1 por la sesión que la implementó, con la
recomendación de cierre de ese mismo hallazgo ya ejecutada; el cierre a `RESUELTO` en
`auditoriacontinua.md` queda para la siguiente pasada del auditor, que es quien modifica ese
archivo). Ninguno de severidad alta que atender como P-XX urgente antes de esta tarea.
`roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin ninguna entrada `nuevo`;
`mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/teleprompter`: cero issues y
cero PR abiertos. §1 (fuente autoritativa) sigue sin ninguna R-XX/T-XX `PENDIENTE` (R-25 es la
última, `COMPLETADA`): cola de la columna vertebral vacía, sin tarea de código que ejecutar ni
hallazgo nuevo que convertir en P-XX. Verificación propia completa (`python scripts/ci.py`):
`mypy`/`ruff` en verde sin hallazgos (70 archivos), 652 tests (`pytest`, sin cambio) en verde,
dieciocho etapas OK en `verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en
§3 (bloqueos) ni §5 (P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`); sin nueva
desviación en §7. Nota sin acción: cola vacía hasta el siguiente ciclo de Product Manager.

**Nota de arranque de esa sesión (ciclo de Programador, cuarta reconfirmación del día tras R-25,
2026-10-08):** sin incidencia. `git status` limpio antes de tocar nada; el contenedor arrancó con
`HEAD` *detached* en `795d5b4` (resto de un contenedor anterior, descartable: ya fusionado en
`develop`); `git checkout develop` dejó la rama local en `cc0ac86`; `git pull origin develop`
resolvió en fast-forward limpio hasta `795d5b4` (la tercera reconfirmación del día tras R-25), sin
conflicto ni rama divergida. `pip install -r requirements-dev.txt` con el `pip` pelado de este
contenedor instaló de nuevo contra Python 3.13 en vez del 3.11.17 real del proyecto — mismo
síntoma del hallazgo `#28`, reproducido una vez más; resuelto con `python3 -m pip install -r
requirements-dev.txt`, que sí resuelve al intérprete correcto (mismas versiones pineadas:
`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador de esta sesión: cuarta reconfirmación del día tras R-25**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: dos `ABIERTO`,
ambos de severidad baja — `#24` (proceso, pregunta de gobernanza #11 de §6 sigue `(pendiente)`) y
`#29` (proceso, la fila de R-25 ya añadida a §1 por la sesión que la implementó, con la
recomendación de cierre de ese mismo hallazgo ya ejecutada; el cierre a `RESUELTO` en
`auditoriacontinua.md` queda para la siguiente pasada del auditor, que es quien modifica ese
archivo). Ninguno de severidad alta que atender como P-XX urgente antes de esta tarea.
`roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin ninguna entrada `nuevo`;
`mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/teleprompter`: cero issues y
cero PR abiertos. §1 (fuente autoritativa) sigue sin ninguna R-XX/T-XX `PENDIENTE` (R-25 es la
última, `COMPLETADA`): cola de la columna vertebral vacía, sin tarea de código que ejecutar ni
hallazgo nuevo que convertir en P-XX. Verificación propia completa: `mypy`/`ruff` en verde sin
hallazgos (70 archivos), 652 tests (`pytest`, sin cambio) en verde, dieciocho etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en §3 (bloqueos) ni §5
(P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`); sin nueva desviación en §7. Nota sin
acción: cola vacía hasta el siguiente ciclo de Product Manager.

**Última actualización anterior (2026-10-08, ciclo de Programador): tercera reconfirmación del día
tras R-25**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, tercera reconfirmación del día tras R-25,
2026-10-08):** sin incidencia. `git status` limpio antes de tocar nada; el contenedor arrancó con
`HEAD` *detached* en `bd7cde5` (resto de un contenedor anterior, descartable: ya fusionado en
`develop`); `git checkout develop` dejó la rama local en `cc0ac86`; `git pull origin develop`
resolvió en fast-forward limpio hasta `bd7cde5` (la segunda reconfirmación del día tras R-25), sin
conflicto ni rama divergida. `pip install -r requirements-dev.txt` con el `pip` pelado de este
contenedor instaló de nuevo contra Python 3.13 en vez del 3.11.17 real del proyecto — mismo
síntoma del hallazgo `#28`, reproducido una vez más; resuelto con `python3 -m pip install -r
requirements-dev.txt`, que sí resuelve al intérprete correcto (mismas versiones pineadas:
`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador de esa sesión: tercera reconfirmación del día tras R-25**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: dos `ABIERTO`,
ambos de severidad baja — `#24` (proceso, pregunta de gobernanza #11 de §6 sigue `(pendiente)`) y
`#29` (proceso, la fila de R-25 ya añadida a §1 por la sesión que la implementó, con la
recomendación de cierre de ese mismo hallazgo ya ejecutada; el cierre a `RESUELTO` en
`auditoriacontinua.md` queda para la siguiente pasada del auditor, que es quien modifica ese
archivo). Ninguno de severidad alta que atender como P-XX urgente antes de esta tarea.
`roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin ninguna entrada `nuevo`;
`mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/teleprompter`: cero issues y
cero PR abiertos. §1 (fuente autoritativa) sigue sin ninguna R-XX/T-XX `PENDIENTE` (R-25 es la
última, `COMPLETADA`): cola de la columna vertebral vacía, sin tarea de código que ejecutar ni
hallazgo nuevo que convertir en P-XX. Verificación propia completa: `mypy`/`ruff` en verde sin
hallazgos (70 archivos), 652 tests (`pytest`, sin cambio) en verde, dieciocho etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en §3 (bloqueos) ni §5
(P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`); sin nueva desviación en §7. Nota sin
acción: cola vacía hasta el siguiente ciclo de Product Manager.

**Última actualización anterior (2026-10-08, ciclo de Programador): segunda reconfirmación del día
tras R-25**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, segunda reconfirmación del día tras R-25,
2026-10-08):** sin incidencia. `git status` limpio antes de tocar nada; el contenedor arrancó con
`HEAD` *detached* (resto de un contenedor anterior, descartable: ya fusionado en `develop`);
`git checkout develop` dejó la rama local en `cc0ac86`; `git pull origin develop` resolvió en
fast-forward limpio hasta `b6443f0` (la primera reconfirmación del día tras R-25), sin conflicto ni
rama divergida. `pip install -r requirements-dev.txt` con el `pip` pelado de este contenedor
instaló de nuevo contra Python 3.13 en vez del 3.11.17 real del proyecto — mismo síntoma del
hallazgo `#28`, reproducido una vez más; resuelto con `python3 -m pip install -r
requirements-dev.txt`, que sí resuelve al intérprete correcto (mismas versiones pineadas:
`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador de esa sesión: segunda reconfirmación del día tras R-25**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: dos `ABIERTO`,
ambos de severidad baja — `#24` (proceso, pregunta de gobernanza #11 de §6 sigue `(pendiente)`) y
`#29` (proceso, la fila de R-25 ya añadida a §1 por la sesión que la implementó, con la
recomendación de cierre de ese mismo hallazgo ya ejecutada; el cierre a `RESUELTO` en
`auditoriacontinua.md` queda para la siguiente pasada del auditor, que es quien modifica ese
archivo). Ninguno de severidad alta que atender como P-XX urgente antes de esta tarea.
`roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin ninguna entrada `nuevo`;
`mcp__github__list_issues`/`list_pull_requests` sobre `JanoSolerDiaz/telePrompter`: cero issues y
cero PR abiertos. §1 (fuente autoritativa) sigue sin ninguna R-XX/T-XX `PENDIENTE` (R-25 es la
última, `COMPLETADA`): cola de la columna vertebral vacía, sin tarea de código que ejecutar ni
hallazgo nuevo que convertir en P-XX. Verificación propia completa: `mypy`/`ruff` en verde sin
hallazgos (70 archivos), 652 tests (`pytest`, sin cambio) en verde, dieciocho etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en §3 (bloqueos) ni §5
(P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`); sin nueva desviación en §7. Nota sin
acción: cola vacía hasta el siguiente ciclo de Product Manager.

**Última actualización anterior (2026-10-08, ciclo de Programador): primera reconfirmación del día
tras R-25**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, primera reconfirmación del día tras R-25,
2026-10-08):** sin incidencia. `git status` limpio antes de tocar nada; el contenedor arrancó con
`HEAD` *detached* en `897c0ea` (resto de un contenedor anterior, descartable: ya fusionado en
`develop`); `git checkout develop` dejó la rama local en `cc0ac86`; `git pull origin develop`
resolvió en fast-forward limpio hasta `897c0ea` (R-25 implementada y `COMPLETADA`), sin conflicto
ni rama divergida. `pip install -r requirements-dev.txt` con el `pip` pelado de este contenedor
instaló de nuevo contra Python 3.13 en vez del 3.11.17 real del proyecto — mismo síntoma del
hallazgo `#28`, reproducido una vez más; resuelto con `python3 -m pip install -r
requirements-dev.txt`, que sí resuelve al intérprete correcto (mismas versiones pineadas:
`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador de esa sesión: primera reconfirmación del día tras R-25**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: dos `ABIERTO`,
ambos de severidad baja — `#24` (proceso, pregunta de gobernanza #11 de §6 sigue `(pendiente)`) y
`#29` (proceso, la fila de R-25 ya añadida a §1 por la sesión que la implementó, con la
recomendación de cierre de ese mismo hallazgo ya ejecutada; el cierre a `RESUELTO` en
`auditoriacontinua.md` queda para la siguiente pasada del auditor, que es quien modifica ese
archivo). Ninguno de severidad alta que atender como P-XX urgente antes de esta tarea.
`roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin ninguna entrada `nuevo`;
`mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/teleprompter`: cero issues y
cero PR abiertos. §1 (fuente autoritativa) sigue sin ninguna R-XX/T-XX `PENDIENTE` (R-25 es la
última, `COMPLETADA`): cola de la columna vertebral vacía, sin tarea de código que ejecutar ni
hallazgo nuevo que convertir en P-XX. Verificación propia completa: `mypy`/`ruff` en verde sin
hallazgos (70 archivos), 652 tests (`pytest`, sin cambio) en verde, dieciocho etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en §3 (bloqueos) ni §5
(P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`); sin nueva desviación en §7. Nota sin
acción: cola vacía hasta el siguiente ciclo de Product Manager.

**Última actualización anterior (2026-10-08, ciclo de Programador): R-25 implementada y
`COMPLETADA`.** `scripts/salidas.py` gana
`TipoSalida.CONVENCION_GUIONES` (séptima opción, al final del orden ya establecido en
`TODAS_LAS_SALIDAS`/`DESCRIPCION_SALIDA`, mismo patrón que `CAPITULOS_YOUTUBE`/R-18 y
`CONCAT_FFMPEG`/R-19) y `_generar_convencion_guiones`, que reutiliza tal cual
`convencion.guardar_convencion_guiones` (T-10, cero cambio en `convencion.py`). A diferencia de las
demás salidas, no recibe `resultado`/`resultado_tiempos`: no depende del parseo ni de la
clasificación del guion de entrada, solo de `Configuracion`, así que se ofrece siempre en
`construir_pregunta_salidas` sin ninguna condición (nunca omitida por falta de datos del guion o de
parte de rodaje, a diferencia de `CAPITULOS_YOUTUBE`/`CONCAT_FFMPEG`) y el único fallo posible es de
escritura a disco, cubierto por el mismo `try`/`except`/diagnóstico de R-24. 3 tests nuevos
(649→652) en `tests/test_salidas.py`: coincide byte a byte con la llamada directa a
`generar_convencion_guiones`, se sigue ofreciendo sin ningún parte de rodaje ni toma marcada, y
`TODAS_LAS_SALIDAS[-1]`/`len(...) == 7`; dos tests existentes actualizados
(`test_no_seleccionadas_quedan_omitidas_sin_generar_archivo`/`test_pptx_latente_no_impide_las_demas`)
para reflejar la séptima opción siempre generada, en vez de dejarlos en rojo o duplicarlos (detalle
en `DECISIONES_TECNICAS.md`). `references/contrato-montaje.md` documenta la salida nueva (no es
contrato de montaje, complementa a R-23); `SKILL.md` documenta la séptima opción en "Selector de
salidas por validación"; `DEVELOPERS.md` gana la sección "Entregar `convencion-guiones.md` de verdad
al dueño (R-25)". Verificación pre-push completa: `mypy`/`ruff` en verde sin hallazgos (70
archivos), 652 tests (`pytest`, 649→652), dieciocho etapas OK en `verificar_salidas.py --fixture`
(sin cambio: "Generación de salidas" ya ejercita `TODAS_LAS_SALIDAS` dinámicamente, sin necesitar
una etapa dedicada nueva para un documento sin validador propio de formato). Las cuatro redes en
verde. Sin cambios en §3 (bloqueos) ni §5 (P-XX); §6 sin novedad (la pregunta #11 sigue
`(pendiente)`); sin nueva desviación en §7. §1 gana la fila `R-25 | ... | COMPLETADA | 2026-10-08`
(resuelve de paso el hallazgo `#29`, que el auditor cerrará en su siguiente pasada) y ya no tiene
ninguna R-XX/T-XX `PENDIENTE`: cola vacía hasta el siguiente ciclo de Product Manager.

**Última actualización anterior (2026-10-07, ciclo de Product Manager): archiva Oleada v12 (R-24) y
abre R-25 (Oleada v13)**, sin tocar código (detalle en la nota de esa sesión, más abajo).

**Ciclo de Product Manager: archiva Oleada v12 (R-24) y abre R-25 (Oleada v13).** Revisión de
entrada (protocolo): registro de hallazgos de `auditoriacontinua.md` reconfirma dos `ABIERTO`, ambos
baja severidad y ya enrutados sin necesitar R-XX — `#24` (proceso, la pregunta de gobernanza #11 de
§6 sigue `(pendiente)`, veintiuna pasadas consecutivas de auditoría) y `#28` (el `pip` pelado de los
contenedores de nube instala contra el intérprete equivocado; su recomendación de cierre ya está
aplicada por `P-06`, completada el mismo día en que se abrió el hallazgo — el cierre a `RESUELTO` en
`auditoriacontinua.md` queda para la siguiente pasada del auditor, que es quien escribe ese
registro). Ninguno de severidad alta ni de producto/arquitectura que convertir en R-XX nueva este
ciclo. `roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin ninguna entrada `nuevo`
que incorporar — el bloqueo #7 de §3 (grabar un curso completo) sigue sin resolverse. §1 (fuente
autoritativa) tenía a R-24 como `COMPLETADA` desde el ciclo de Programador del mismo día (2026-10-07)
que la abrió el ciclo de PM anterior (2026-10-06), con nueve reconfirmaciones posteriores del
Programador dejando `ROADMAP_PRODUCTO.md` describiéndola como `PENDIENTE` en su prosa de "Cola de
producto" — el mismo patrón de latencia que motivó `#24`, repetido una sexta vez. Este ciclo corrige
esa prosa: Oleada v12 (R-24) se mueve íntegra a `roadmap/ROADMAP_HISTORICO.md` (spec completa + "Cómo
se entregó"), con su entrada de índice correspondiente.

**Se abre R-25** (Oleada v13) por grieta de arquitectura verificada, mismo criterio que abrió R-12 a
R-24. Se delegó una primera pasada de exploración a un subagente, en paralelo con verificación propia
directa (no solo delegada): ambas convergen en `scripts/convencion.py::
generar_convencion_guiones`/`guardar_convencion_guiones` (T-10) como la candidata más sólida —
confirmado con `grep -rn "generar_convencion_guiones\|guardar_convencion_guiones" scripts/*.py
SKILL.md`, cero resultado fuera de `scripts/convencion.py` y sus propios tests. La función genera,
según su propio docstring, un documento pensado para que el dueño lo "pegue en su plantilla de
guiones" y evite así desviaciones de convención en guiones futuros — complemento natural de R-23
(2026-10-06), que acaba de hacer visibles las desviaciones ya ocurridas. Nunca se ofrece: no está
entre las seis opciones de `scripts/salidas.py::TipoSalida` (T-30/R-18/R-19) ni ningún paso de
`SKILL.md` le dice a Claude cuándo generarla. Dos candidatas alternativas descartadas tras la misma
verificación: `scripts/calibracion.py::calcular_calibracion` (R-04) tiene la misma falta de gancho en
`SKILL.md`, pero conectarla de verdad exigiría descubrir "guiones hermanos" entre proyectos
distintos — pieza de arquitectura nueva que hoy no existe (aislamiento por proyecto de guión, §0.2) y
que no conviene construir por adelantado mientras el bloqueo #7 (cero curso grabado todavía) siga
abierto; `scripts/reescrituras.py::revertir_reescrituras` (T-15, deshacer global) también carece de
disparador documentado, pero revierte decisiones ya tomadas del dueño y su valor es menor que el de
prevenir una desviación futura con coste y riesgo mínimos. Spec completa de R-25 en
`ROADMAP_PRODUCTO.md` (Oleada v13), lista para que el siguiente ciclo de Programador la implemente y
verifique. Este ciclo es de PM, no de Programador: no se ha ejecutado la verificación de las cuatro
redes ni se ha tocado `scripts/`, `tests/` ni `assets/`.

Sin cambios en §3 (bloqueos) ni §5 (P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`); sin
nueva desviación en §7.

**Última actualización anterior (2026-10-07, ciclo de Programador): novena reconfirmación del día
tras R-24**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, novena reconfirmación del día tras R-24,
2026-10-07):** sin incidencia. `git status` limpio antes de tocar nada; el contenedor arrancó con
`HEAD` *detached* en `882b341` (resto de un contenedor anterior, descartable: ya fusionado en
`develop`); `git checkout develop` dejó la rama local en `cc0ac86`; `git pull origin develop`
resolvió en fast-forward limpio hasta `882b341` (la octava reconfirmación del día tras R-24), sin
conflicto ni rama divergida. `pip install -r requirements-dev.txt` con el `pip` pelado de este
contenedor instaló de nuevo contra Python 3.13 en vez del 3.11.17 real del proyecto — mismo
síntoma del hallazgo `#28`, reproducido una vez más (la decimoséptima repetición consecutiva);
resuelto con `python3 -m pip install -r requirements-dev.txt`, que sí resuelve al intérprete
correcto (mismas versiones pineadas: `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador de esa sesión: novena reconfirmación del día tras R-24**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: dos `ABIERTO`,
ambos de severidad baja — `#24` (proceso, pregunta de gobernanza #11 de §6 sigue `(pendiente)`) y
`#28` (infraestructura, mismo síntoma de `pip` pelado de este preámbulo, ya con su recomendación de
cierre aplicada por P-06; el cierre a `RESUELTO` en `auditoriacontinua.md` queda para la siguiente
pasada del auditor, que es quien modifica ese archivo). Ninguno de severidad alta que atender como
P-XX urgente antes de esta tarea. `roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía,
sin ninguna entrada `nuevo`; `mcp__github__list_issues`/`list_pull_requests` sobre
`janosolerdiaz/telePrompter`: cero issues y cero PR abiertos. §1 (fuente autoritativa) sigue sin
ninguna R-XX/T-XX `PENDIENTE` (R-24 es la última, `COMPLETADA`): cola de la columna vertebral
vacía, sin tarea de código que ejecutar ni hallazgo nuevo que convertir en P-XX. Verificación propia
completa: `mypy`/`ruff` en verde sin hallazgos (70 archivos), 649 tests (`pytest`, sin cambio) en
verde, dieciocho etapas OK en `verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin
cambios en §3 (bloqueos) ni §5 (P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`). Nota
sin acción, mismo patrón que motivó `#24`: `ROADMAP_PRODUCTO.md` (sección "Cola de producto")
seguirá describiendo R-24 como `PENDIENTE`/"EN CURSO" en su prosa hasta el siguiente ciclo de
Product Manager, que es quien archiva la oleada — no se corrige desde este ciclo de Programador (la
pregunta #11 de §6 sigue `(pendiente)` de respuesta del dueño).

**Última actualización anterior (2026-10-07, ciclo de Programador): octava reconfirmación del día
tras R-24**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, octava reconfirmación del día tras R-24,
2026-10-07):** sin incidencia. `git status` limpio antes de tocar nada; el contenedor arrancó con
`HEAD` *detached* en `7560fc9` (resto de un contenedor anterior, descartable: ya fusionado en
`develop`); `git checkout develop` dejó la rama local en `cc0ac86`; `git pull origin develop`
resolvió en fast-forward limpio hasta `7560fc9` (la séptima reconfirmación del día tras R-24), sin
conflicto ni rama divergida. `pip install -r requirements-dev.txt` con el `pip` pelado de este
contenedor instaló de nuevo contra Python 3.13 en vez del 3.11.17 real del proyecto — mismo
síntoma del hallazgo `#28`, reproducido una vez más (la decimosexta repetición consecutiva);
resuelto con `python3 -m pip install -r requirements-dev.txt`, que sí resuelve al intérprete
correcto (mismas versiones pineadas: `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador de esa sesión: octava reconfirmación del día tras R-24**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: dos `ABIERTO`,
ambos de severidad baja — `#24` (proceso, pregunta de gobernanza #11 de §6 sigue `(pendiente)`) y
`#28` (infraestructura, mismo síntoma de `pip` pelado de este preámbulo, ya con su recomendación de
cierre aplicada por P-06; el cierre a `RESUELTO` en `auditoriacontinua.md` queda para la siguiente
pasada del auditor, que es quien modifica ese archivo). Ninguno de severidad alta que atender como
P-XX urgente antes de esta tarea. `roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía,
sin ninguna entrada `nuevo`; `mcp__github__list_issues`/`list_pull_requests` sobre
`janosolerdiaz/telePrompter`: cero issues y cero PR abiertos. §1 (fuente autoritativa) sigue sin
ninguna R-XX/T-XX `PENDIENTE` (R-24 es la última, `COMPLETADA`): cola de la columna vertebral
vacía, sin tarea de código que ejecutar ni hallazgo nuevo que convertir en P-XX. Verificación propia
completa: `mypy`/`ruff` en verde sin hallazgos (70 archivos), 649 tests (`pytest`, sin cambio) en
verde, dieciocho etapas OK en `verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin
cambios en §3 (bloqueos) ni §5 (P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`). Nota
sin acción, mismo patrón que motivó `#24`: `ROADMAP_PRODUCTO.md` (sección "Cola de producto")
seguirá describiendo R-24 como `PENDIENTE`/"EN CURSO" en su prosa hasta el siguiente ciclo de
Product Manager, que es quien archiva la oleada — no se corrige desde este ciclo de Programador (la
pregunta #11 de §6 sigue `(pendiente)` de respuesta del dueño).

**Última actualización anterior (2026-10-07, ciclo de Programador): séptima reconfirmación del día
tras R-24**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, sexta reconfirmación del día tras R-24,
2026-10-07):** sin incidencia. `git status` limpio antes de tocar nada; `git checkout develop &&
git pull origin develop` resolvió en fast-forward limpio hasta `c043f4c` (la quinta reconfirmación
del día tras R-24), sin conflicto ni rama divergida. `pip install -r requirements-dev.txt` con el
`pip` pelado de este contenedor instaló de nuevo contra Python 3.13 en vez del 3.11.17 real del
proyecto — mismo síntoma del hallazgo `#28`, reproducido una vez más (la decimocuarta repetición
consecutiva); resuelto con `python3 -m pip install -r requirements-dev.txt`, que sí resuelve al
intérprete correcto (mismas versiones pineadas: `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador de esta sesión: sexta reconfirmación del día tras R-24**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: dos `ABIERTO`,
ambos de severidad baja — `#24` (proceso, pregunta de gobernanza #11 de §6 sigue `(pendiente)`) y
`#28` (infraestructura, mismo síntoma de `pip` pelado de este preámbulo, ya con su recomendación de
cierre aplicada por P-06; el cierre a `RESUELTO` en `auditoriacontinua.md` queda para la siguiente
pasada del auditor, que es quien modifica ese archivo). Ninguno de severidad alta que atender como
P-XX urgente antes de esta tarea. `roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía,
sin ninguna entrada `nuevo`; `mcp__github__list_issues`/`list_pull_requests` sobre
`JanoSolerDiaz/telePrompter`: cero issues y cero PR abiertos. §1 (fuente autoritativa) sigue sin
ninguna R-XX/T-XX `PENDIENTE` (R-24 es la última, `COMPLETADA`): cola de la columna vertebral
vacía, sin tarea de código que ejecutar ni hallazgo nuevo que convertir en P-XX. Verificación propia
completa: `mypy`/`ruff` en verde sin hallazgos (70 archivos), 649 tests (`pytest`, sin cambio) en
verde, dieciocho etapas OK en `verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin
cambios en §3 (bloqueos) ni §5 (P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`). Nota
sin acción, mismo patrón que motivó `#24`: `ROADMAP_PRODUCTO.md` (sección "Cola de producto")
seguirá describiendo R-24 como `PENDIENTE`/"EN CURSO" en su prosa hasta el siguiente ciclo de
Product Manager, que es quien archiva la oleada — no se corrige desde este ciclo de Programador (la
pregunta #11 de §6 sigue `(pendiente)` de respuesta del dueño).

**Última actualización anterior (2026-10-07, ciclo de Programador): quinta reconfirmación del día
tras R-24**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esta sesión (ciclo de Programador, quinta reconfirmación del día tras R-24,
2026-10-07):** sin incidencia. `git status` limpio antes de tocar nada; `git checkout develop`
dejó el contenedor en `HEAD` *detached* (resto de un contenedor anterior, descartable: ya fusionado
en `develop`); `git pull origin develop` resolvió en fast-forward limpio hasta `8278eec` (la cuarta
reconfirmación del día tras R-24), sin conflicto ni rama divergida. `pip install -r
requirements-dev.txt` con el `pip` pelado de este contenedor instaló de nuevo contra Python 3.13 en
vez del 3.11.x real del proyecto — mismo síntoma del hallazgo `#28`, reproducido una vez más (la
decimotercera repetición consecutiva); resuelto con `python3 -m pip install -r
requirements-dev.txt`, que sí resuelve al intérprete correcto (mismas versiones pineadas:
`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador de esta sesión: quinta reconfirmación del día tras R-24**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: dos `ABIERTO`,
ambos de severidad baja — `#24` (proceso, pregunta de gobernanza #11 de §6 sigue `(pendiente)`) y
`#28` (infraestructura, mismo síntoma de `pip` pelado de este preámbulo, ya con su recomendación de
cierre aplicada por P-06; el cierre a `RESUELTO` en `auditoriacontinua.md` queda para la siguiente
pasada del auditor, que es quien modifica ese archivo). Ninguno de severidad alta que atender como
P-XX urgente antes de esta tarea. `roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía,
sin ninguna entrada `nuevo`; `mcp__github__list_issues`/`list_pull_requests` sobre
`JanoSolerDiaz/telePrompter`: cero issues y cero PR abiertos. §1 (fuente autoritativa) sigue sin
ninguna R-XX/T-XX `PENDIENTE` (R-24 es la última, `COMPLETADA`): cola de la columna vertebral
vacía, sin tarea de código que ejecutar ni hallazgo nuevo que convertir en P-XX. Verificación propia
completa: `mypy`/`ruff` en verde sin hallazgos (70 archivos), 649 tests (`pytest`, sin cambio) en
verde, dieciocho etapas OK en `verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin
cambios en §3 (bloqueos) ni §5 (P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`). Nota
sin acción, mismo patrón que motivó `#24`: `ROADMAP_PRODUCTO.md` (sección "Cola de producto")
seguirá describiendo R-24 como `PENDIENTE`/"EN CURSO" en su prosa hasta el siguiente ciclo de
Product Manager, que es quien archiva la oleada — no se corrige desde este ciclo de Programador (la
pregunta #11 de §6 sigue `(pendiente)` de respuesta del dueño).

**Última actualización anterior (2026-10-07, ciclo de Programador): cuarta reconfirmación del día
tras R-24**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, cuarta reconfirmación del día tras R-24,
2026-10-07):** sin incidencia. `git status` limpio antes de tocar nada; `git checkout develop`
dejó el contenedor en `HEAD` *detached* (resto de un contenedor anterior, descartable: ya fusionado
en `develop`); `git pull origin develop` resolvió en fast-forward limpio hasta `0a8e90e` (P-06, la
tercera reconfirmación del día tras R-24), sin conflicto ni rama divergida. `pip install -r
requirements-dev.txt` con el `pip` pelado de este contenedor instaló de nuevo contra Python 3.13 en
vez del 3.11.x real del proyecto — mismo síntoma del hallazgo `#28`, reproducido una vez más (la
duodécima repetición consecutiva, ya documentada por P-06 en `DEVELOPERS.md`/`SKILL.md` esta misma
mañana); resuelto con `python3 -m pip install -r requirements-dev.txt`, que sí resuelve al
intérprete correcto (mismas versiones pineadas: `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador de esa sesión: cuarta reconfirmación del día tras R-24**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: dos `ABIERTO`,
ambos de severidad baja — `#24` (proceso, pregunta de gobernanza #11 de §6 sigue `(pendiente)`) y
`#28` (infraestructura, mismo síntoma de `pip` pelado de este preámbulo, ya con su recomendación de
cierre aplicada por P-06 en esta misma jornada; el cierre a `RESUELTO` en `auditoriacontinua.md`
queda para la siguiente pasada del auditor, que es quien modifica ese archivo). Ninguno de
severidad alta que atender como P-XX urgente antes de esta tarea. `roadmap/FEEDBACK.md` sigue con
su única fila de plantilla vacía, sin ninguna entrada `nuevo`; `mcp__github__list_issues`/
`list_pull_requests` sobre `JanoSolerDiaz/telePrompter`: cero issues y cero PR abiertos. §1 (fuente
autoritativa) sigue sin ninguna R-XX/T-XX `PENDIENTE` (R-24 es la última, `COMPLETADA`): cola de la
columna vertebral vacía, sin tarea de código que ejecutar ni hallazgo nuevo que convertir en P-XX
(P-06 ya agotó la recomendación de cierre de `#28` esta misma mañana). Verificación propia completa:
`mypy`/`ruff` en verde sin hallazgos (70 archivos), 649 tests (`pytest`, sin cambio) en verde,
dieciocho etapas OK en `verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en
§3 (bloqueos) ni §5 (P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`). Nota sin acción,
mismo patrón que motivó `#24`: `ROADMAP_PRODUCTO.md` (sección "Cola de producto") seguirá
describiendo R-24 como `PENDIENTE`/"EN CURSO" en su prosa hasta el siguiente ciclo de Product
Manager, que es quien archiva la oleada — no se corrige desde este ciclo de Programador (la pregunta
#11 de §6 sigue `(pendiente)` de respuesta del dueño).

**Última actualización anterior (2026-10-07, ciclo de Programador): tercera reconfirmación del día
tras R-24, con P-06** (extiende a la instalación de dependencias la nota de `DEVELOPERS.md`/`SKILL.md`
que ya cubría el binario "pelado"; cierra el hallazgo `#28` de documentación, código sin cambios —
detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, tercera reconfirmación del día tras R-24,
2026-10-07):** sin incidencia. `git status` limpio antes de tocar nada; `git checkout develop`
dejó el contenedor en `HEAD` *detached* (resto de un contenedor anterior, descartable: ya fusionado
en `develop`); `git pull origin develop` resolvió en fast-forward limpio hasta `f030cab` (la segunda
reconfirmación del día tras R-24), sin conflicto ni rama divergida. `pip install -r
requirements-dev.txt` con el `pip` pelado de este contenedor instaló de nuevo contra Python 3.13 en
vez del 3.11.17 real del proyecto — mismo síntoma del hallazgo `#28`, reproducido una vez más (la
undécima repetición consecutiva); resuelto con `python3 -m pip install -r requirements-dev.txt`, que
sí resuelve al intérprete correcto (mismas versiones pineadas: `mypy==1.18.2`, `ruff==0.14.0`,
`pytest==8.4.2`).

**Ciclo de Programador de esta sesión: tercera reconfirmación del día tras R-24, con P-06.**
Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: dos `ABIERTO`, ambos de
severidad baja — `#24` (proceso, pregunta de gobernanza #11 de §6 sigue `(pendiente)`) y `#28`
(infraestructura, el mismo síntoma de `pip` pelado de este preámbulo, reproducido ya once veces
seguidas sin quedar nunca documentado). Ninguno de severidad alta que atender como P-XX urgente
antes de esta tarea. `roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin ninguna
entrada `nuevo`; `mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/telePrompter`:
cero issues y cero PR abiertos. §1 (fuente autoritativa) sigue sin ninguna R-XX/T-XX `PENDIENTE`
(R-24 es la última, `COMPLETADA`): cola de la columna vertebral vacía. Con la tarea en curso
terminada y `#28` ya trayendo su propia recomendación de cierre escrita por el auditor, esta sesión
registra y ejecuta **P-06** (§5): extiende la nota de `DEVELOPERS.md`/`SKILL.md` que ya cubría el
binario "pelado" de `ruff`/`mypy`/`pytest` (R-15, `#22`) para que también cubra expresamente el
`pip install` pelado al instalar las dependencias de desarrollo, recomendando siempre `python3 -m
pip install -r requirements-dev.txt`. Alcance puramente documental: cero cambio en `scripts/`,
`tests/` ni `assets/`. Verificación propia completa tras el cambio: `mypy`/`ruff` en verde sin
hallazgos (70 archivos), 649 tests (`pytest`, sin cambio: P-06 no añade lógica) en verde, dieciocho
etapas OK en `verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en §3
(bloqueos); §6 sin novedad (la pregunta #11 sigue `(pendiente)`). El cierre de la fila `#28` a
`RESUELTO` en `auditoriacontinua.md` queda para la siguiente pasada del auditor (solo él modifica
ese archivo, §0.4): esta sesión deja el commit listo para que lo verifique de forma independiente.
Nota sin acción, mismo patrón que motivó `#24`: `ROADMAP_PRODUCTO.md` (sección "Cola de producto")
seguirá describiendo R-24 como `PENDIENTE`/"EN CURSO" en su prosa hasta el siguiente ciclo de
Product Manager, que es quien archiva la oleada — no se corrige desde este ciclo de Programador (la
pregunta #11 de §6 sigue `(pendiente)` de respuesta del dueño).

**Última actualización anterior (2026-10-07, ciclo de Programador): segunda reconfirmación del día
tras R-24**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esta sesión (ciclo de Programador, segunda reconfirmación del día tras R-24,
2026-10-07):** sin incidencia. `git status` limpio antes de tocar nada; `git checkout develop` dejó
el contenedor en `HEAD` *detached* (resto de un contenedor anterior, descartable: ya fusionado en
`develop`); `git pull origin develop` resolvió en fast-forward limpio hasta `79387f4` (la primera
reconfirmación del día tras R-24), sin conflicto ni rama divergida. `pip install -r
requirements-dev.txt` con el `pip` pelado de este contenedor instaló de nuevo contra Python 3.13 en
vez del 3.11.17 real del proyecto — mismo síntoma del hallazgo `#28`, reproducido una vez más;
resuelto con `python3 -m pip install -r requirements-dev.txt`, que sí resuelve al intérprete
correcto (mismas versiones pineadas: `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador de esta sesión: segunda reconfirmación del día tras R-24**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: dos `ABIERTO`,
ambos de severidad baja y sin coste real más allá de la repetición — `#24` (proceso, pregunta de
gobernanza #11 de §6 sigue `(pendiente)`) y `#28` (infraestructura, el mismo síntoma de `pip`
pelado de este preámbulo). Ninguno de severidad alta que atender como P-XX urgente antes de esta
tarea. `roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin ninguna entrada
`nuevo`; `mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero
issues y cero PR abiertos. §1 (fuente autoritativa) ya no tiene ninguna R-XX/T-XX `PENDIENTE` (R-24
es la última, `COMPLETADA`): cola vacía, sin tarea de código que ejecutar. Verificación propia
completa: `mypy`/`ruff` en verde sin hallazgos (70 archivos), 649 tests (`pytest`) en verde,
dieciocho etapas OK en `verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en
§3 (bloqueos) ni §5 (P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`). Nota sin acción,
mismo patrón que motivó `#24`: `ROADMAP_PRODUCTO.md` (sección "Cola de producto") seguirá
describiendo R-24 como `PENDIENTE`/"EN CURSO" en su prosa hasta el siguiente ciclo de Product
Manager, que es quien archiva la oleada — no se corrige desde este ciclo de Programador (la
pregunta #11 de §6 sigue `(pendiente)` de respuesta del dueño).

**Última actualización anterior (2026-10-07, ciclo de Programador): primera reconfirmación del día
tras R-24**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, primera reconfirmación del día tras R-24,
2026-10-07):** sin incidencia. `git status` limpio antes de tocar nada; `git checkout develop &&
git pull origin develop` ya estaba en `develop`, al día con `origin/develop` (sin fast-forward
necesario: este contenedor arrancó ya sobre `03c7aa1`, el commit de R-24). `pip install -r
requirements-dev.txt` con el `pip` pelado de este contenedor instaló de nuevo contra Python 3.13 en
vez del 3.11.17 real del proyecto — mismo síntoma del hallazgo `#28`, reproducido una vez más;
resuelto con `python3 -m pip install -r requirements-dev.txt`, que sí resuelve al intérprete
correcto (mismas versiones pineadas: `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador de esa sesión: primera reconfirmación del día tras R-24**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: dos `ABIERTO`,
ambos de severidad baja y sin coste real más allá de la repetición — `#24` (proceso, pregunta de
gobernanza #11 de §6 sigue `(pendiente)`) y `#28` (infraestructura, el mismo síntoma de `pip`
pelado de este preámbulo). Ninguno de severidad alta que atender como P-XX urgente antes de esta
tarea. `roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin ninguna entrada
`nuevo`; `mcp__github__list_issues`/`list_pull_requests` sobre `JanoSolerDiaz/telePrompter`: cero
issues y cero PR abiertos. §1 (fuente autoritativa) ya no tiene ninguna R-XX/T-XX `PENDIENTE` (R-24
es la última, `COMPLETADA`): cola vacía, sin tarea de código que ejecutar. Verificación propia
completa: `mypy`/`ruff` en verde sin hallazgos (70 archivos), 649 tests (`pytest`) en verde,
dieciocho etapas OK en `verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en
§3 (bloqueos) ni §5 (P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`). Nota sin acción,
mismo patrón que motivó `#24`: `ROADMAP_PRODUCTO.md` (sección "Cola de producto") seguirá
describiendo R-24 como `PENDIENTE`/"EN CURSO" en su prosa hasta el siguiente ciclo de Product
Manager, que es quien archiva la oleada — no se corrige desde este ciclo de Programador (la
pregunta #11 de §6 sigue `(pendiente)` de respuesta del dueño).

**Última actualización anterior (2026-10-07, ciclo de Programador): R-24 implementada y
`COMPLETADA`.** Diagnóstico real de un fallo al generar una salida, en vez del `repr` crudo de la
excepción (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, 2026-10-07):** sin incidencia. `git
status` limpio antes de tocar nada; `git checkout develop && git pull origin develop` resolvió en
fast-forward limpio hasta `bca7a2d` (la auditoría del 2026-10-07, hallazgo `#28` formalizado), sin
conflicto ni rama divergida. `pip install -r requirements-dev.txt` con el `pip` pelado de este
contenedor instaló de nuevo contra Python 3.13 en vez del 3.11.17 real del proyecto — exactamente
el síntoma que el hallazgo `#28` (recién formalizado por la auditoría de esta misma fecha) describe;
resuelto con `python3 -m pip install -r requirements-dev.txt`, que sí resuelve al intérprete
correcto (mismas versiones pineadas: `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Revisión de entrada (protocolo):** registro de hallazgos de `auditoriacontinua.md` reconfirma dos
`ABIERTO`, ambos de severidad baja y sin coste real más allá de la repetición: `#24` (proceso,
pregunta de gobernanza #11 de §6 sigue `(pendiente)`) y `#28` (infraestructura, el mismo síntoma de
`pip` pelado de este preámbulo, ya con la recomendación de cierre escrita en el propio hallazgo).
Ninguno de severidad alta que atender como P-XX urgente antes de esta tarea. §1 (fuente
autoritativa) tenía a R-24 como la única R-XX `PENDIENTE`, ya especificada por completo en
`ROADMAP_PRODUCTO.md` §"Oleada v12" por el ciclo de PM del 2026-10-06.

**Ciclo de Programador: R-24 implementada y `COMPLETADA`.** `scripts/monitorizacion.py::
_volcar_diagnostico` se promueve a pública (`volcar_diagnostico`, mismo patrón de promoción de
visibilidad que `tomas.toma_buena`/R-19 y `reproductor.anclar_indicaciones_a_bloques`/R-20: cambio
de nombre, cero cambio de firma). `scripts/salidas.py::generar_salidas_seleccionadas` importa
`logger.obtener_logger` y `monitorizacion.ruta_diagnostico`/`volcar_diagnostico`; dentro del
`except Exception` ya existente (requisito 3 de T-30, intacto: una salida rota nunca impide las
demás), antes de construir la `SalidaOmitida`, vuelca el diagnóstico técnico completo a
`<carpeta_salida>/diagnostico-<timestamp>.log` y registra la excepción en el logger centralizado
con `exc_info`. Deliberadamente NO se cablea `ejecutar_con_diagnostico` (pensada para abortar un
proceso entero con código de salida, semántica que no encaja aquí). El `motivo` de la
`SalidaOmitida` deja de llevar `str(excepcion)` crudo y pasa a `"fallo al generar: revisa el
diagnóstico técnico en <ruta>"`, mismo criterio de "nunca trazas crudas" que ya aplica
`ejecutar_con_diagnostico`. 3 tests nuevos (646→649): dos en `tests/test_salidas.py` (el motivo ya
no contiene la traza cruda ni el texto de la excepción simulada, cita la ruta real del
`diagnostico-<timestamp>.log`, que existe con el traceback completo sin arrastrar una variable
local con contenido de guion; con el logger ya configurado, `teleprompter.log` recoge la misma
entrada) y uno en `tests/test_monitorizacion.py` (`volcar_diagnostico` invocable fuera de
`ejecutar_con_diagnostico`). El test ya existente que comprobaba literalmente la traza cruda en el
motivo (`test_fallo_de_una_salida_no_impide_las_demas`) se actualiza al contrato nuevo en el mismo
commit, en vez de dejarlo en rojo o duplicarlo (detalle en `DECISIONES_TECNICAS.md`).
`DEVELOPERS.md` gana una sección nueva ("Diagnóstico real de un fallo al generar una salida
(R-24)") y una nota en "Monitorización de errores (T-05)" señalando el consumidor nuevo;
`SKILL.md` no cambia (R-24 no añade ni modifica ningún campo de `Configuracion` ni comportamiento
visible para el dueño más allá del mensaje de error, ya cubierto por el criterio de aceptación).
Verificación pre-push completa: `mypy`/`ruff` en verde sin hallazgos (70 archivos), 649 tests
(`pytest`, 646→649), dieciocho etapas OK en `verificar_salidas.py --fixture` (sin cambio: R-24 no
añade ninguna salida nueva). Las cuatro redes en verde. Sin cambios en §3 (bloqueos) ni §5 (P-XX);
§6 sin novedad (la pregunta #11 sigue `(pendiente)`); sin nueva desviación en §7. §1 ya no tiene
ninguna R-XX/T-XX `PENDIENTE`: cola vacía hasta el siguiente ciclo de Product Manager.

**Última actualización anterior (2026-10-06, ciclo de Product Manager): archiva Oleada v11 (R-23) y
abre R-24 (Oleada v12)** (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Product Manager, 2026-10-06):** sin incidencia. `git
status` limpio antes de tocar nada; `git checkout develop && git pull origin develop` resolvió en
fast-forward limpio hasta `8cbb4e4` (la novena reconfirmación del día de Programador tras R-23), sin
conflicto ni rama divergida. `pip install -r requirements-dev.txt` con el `pip` pelado de este
contenedor instaló contra Python 3.13 en vez del 3.11.17 real del proyecto — mismo síntoma ya
registrado (no un hallazgo nuevo, `#22`/R-15); resuelto con `python3 -m pip install -r
requirements-dev.txt`.

**Ciclo de Product Manager: archiva Oleada v11 (R-23) y abre R-24 (Oleada v12).** Revisión de
entrada (protocolo): registro de hallazgos de `auditoriacontinua.md` reconfirma un único `ABIERTO`,
`#24` (baja, proceso — la pregunta de gobernanza #11 de §6 sigue `(pendiente)`, veinte pasadas
consecutivas de auditoría), ninguno de severidad alta ni de producto/arquitectura que convertir en
R-XX nueva este ciclo — el propio `#24` ya está enrutado a la pregunta #11, no es una R-XX.
`roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin ninguna entrada `nuevo` que
incorporar — el bloqueo #7 de §3 (grabar un curso completo) sigue sin resolverse. §1 (fuente
autoritativa) tenía a R-23 como `COMPLETADA` desde el ciclo de Programador del mismo día (2026-10-06)
que la abrió el ciclo de PM anterior (2026-10-05), con nueve reconfirmaciones posteriores del
Programador dejando `ROADMAP_PRODUCTO.md` describiéndola como `PENDIENTE` en su prosa de "Cola de
producto" — el mismo patrón de latencia que motivó `#24`. Este ciclo corrige esa prosa: Oleada v11
(R-23) se mueve íntegra a `roadmap/ROADMAP_HISTORICO.md` (spec completa + "Cómo se entregó"), con su
entrada de índice correspondiente.

**Se abre R-24** (Oleada v12) por grieta de arquitectura verificada, mismo criterio que abrió R-12 a
R-23. Se delegó una primera pasada de exploración a un subagente, que propuso tres candidatas
(`convencion.generar_convencion_guiones`/`guardar_convencion_guiones` sin ningún consumidor real;
`reescrituras.revertir_reescrituras` sin disparador documentado para el dueño; la infraestructura de
diagnóstico de T-02/T-05 sin consumidor real). Verificación independiente propia, no delegada:
confirmada la tercera leyendo `scripts/logger.py`, `scripts/monitorizacion.py` y
`scripts/salidas.py::generar_salidas_seleccionadas` línea a línea — `logger.py`/`monitorizacion.py`
se construyeron el primer día del proyecto (T-02/T-05, 2026-09-01) anticipando explícitamente un
futuro "punto de entrada real" que los usara; ese punto de entrada llegó después como
`generar_salidas_seleccionadas` (T-30/R-18), y su manejo de errores (línea ~499) reinventa por su
cuenta exactamente lo que T-05 quería evitar: muestra al dueño el `repr` crudo de la excepción y no
vuelca ningún diagnóstico a disco ni pasa por el logger centralizado — contradice dos reglas
explícitas de §0.2 ("Logger centralizado", "Errores accionables en español, nunca trazas crudas").
Las otras dos candidatas se descartan por menor valor/mayor incertidumbre de diseño: la primera
(`convencion-guiones.md`) es un documento pensado para explicarle la convención a un guionista
distinto del locutor, pero en el ICP de este proyecto el guionista y el dueño son la misma persona,
que ya conoce la convención (documentada además de forma estable en `references/convencion-guion.md`
para cuando haga falta consultarla); la segunda
(`revertir_reescrituras`) no tiene un disparador de producto obvio (requeriría diseñar una superficie
nueva, no solo cablear un cálculo ya existente a un consumidor que ya existe). Spec completa de R-24
en `ROADMAP_PRODUCTO.md` (Oleada v12), lista para que el siguiente ciclo de Programador la implemente
y verifique. Este ciclo es de PM, no de Programador: no se ha ejecutado la verificación de las cuatro
redes ni se ha tocado `scripts/`, `tests/` ni `assets/`.

Sin cambios en §3 (bloqueos) ni §5 (P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`); sin
nueva desviación en §7.

**Nota de arranque de esta sesión (ciclo de Programador, novena reconfirmación del día tras R-23,
2026-10-06):** sin incidencia. `git status` limpio antes de tocar nada; `git checkout develop`
resolvió en `develop` sin problema; `git pull origin develop` resolvió en fast-forward limpio
hasta `4cbd13f` (la octava reconfirmación del día tras R-23), sin conflicto ni rama divergida. `pip
install -r requirements-dev.txt` con el `pip` pelado de este contenedor instaló contra Python 3.13
en vez del 3.11.17 real del proyecto — mismo síntoma ya registrado (no un hallazgo nuevo, `#22`/
R-15 ya documentan el riesgo de invocar herramientas sin pasar por el intérprete correcto en un
contenedor de nube con más de un Python instalado); resuelto con `python3 -m pip install -r
requirements-dev.txt`, que sí resuelve al intérprete correcto (mismas versiones pineadas:
`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador de esta sesión: novena reconfirmación del día tras R-23**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: único
`ABIERTO` sigue siendo `#24` (baja, proceso — la pregunta de gobernanza #11 de §6 sigue
`(pendiente)`, veinte pasadas consecutivas de auditoría según la cifra de la propia auditoría del
2026-10-06, sin cambio desde entonces por no haber corrido ningún ciclo de auditoría nuevo),
ninguno de severidad alta que atender como P-XX urgente antes de esta tarea. `roadmap/FEEDBACK.md`
sin ninguna entrada `nuevo`; `mcp__github__list_issues`/`list_pull_requests` sobre
`JanoSolerDiaz/telePrompter`: cero issues y cero PR abiertos. §1 (fuente autoritativa) ya no tiene
ninguna R-XX/T-XX `PENDIENTE` (R-23 es la última, `COMPLETADA`): cola vacía, sin tarea de código
que ejecutar. Verificación propia completa: `mypy`/`ruff` en verde sin hallazgos (70 archivos), 646
tests (`pytest`) en verde, dieciocho etapas OK en `verificar_salidas.py --fixture`. Las cuatro
redes en verde. Sin cambios en §3 (bloqueos) ni §5 (P-XX); §6 sin novedad (la pregunta #11 sigue
`(pendiente)`). Nota sin acción, mismo patrón que motivó `#24`: `ROADMAP_PRODUCTO.md` (sección
"Cola de producto") sigue describiendo R-23 como `PENDIENTE` en su prosa, pese a que §1 ya la
registra `COMPLETADA` — hasta el siguiente ciclo de Product Manager, que es quien archiva la
oleada, no se corrige desde este ciclo de Programador (la pregunta #11 de §6 sigue `(pendiente)`
de respuesta del dueño).

**Última actualización anterior (2026-10-06, ciclo de Programador): octava reconfirmación del día
tras R-23**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, segunda reconfirmación del día tras R-23,
2026-10-06):** sin incidencia. `git status` limpio antes de tocar nada; `git checkout develop`
dejó el contenedor en `HEAD` *detached* (resto de un contenedor anterior, descartable: ya
fusionado en `develop`); `git pull origin develop` resolvió en fast-forward limpio hasta `e71ceb9`
(la primera reconfirmación del día tras R-23), sin conflicto ni rama divergida. `pip install -r
requirements-dev.txt` con el `pip` pelado de este contenedor instaló contra Python 3.13 en vez del
3.11.17 real del proyecto — mismo síntoma ya registrado (no un hallazgo nuevo, `#22`/R-15 ya
documentan el riesgo de invocar herramientas sin pasar por el intérprete correcto en un contenedor
de nube con más de un Python instalado); resuelto con `python3 -m pip install -r
requirements-dev.txt`, que sí resuelve al intérprete correcto (mismas versiones pineadas:
`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador de esa sesión: segunda reconfirmación del día tras R-23**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: único
`ABIERTO` sigue siendo `#24` (baja, proceso — la pregunta de gobernanza #11 de §6 sigue
`(pendiente)`, veintiuna pasadas consecutivas, sin cambio desde la pasada anterior por no haber
corrido ningún ciclo de auditoría entre medias), ninguno de severidad alta que atender como P-XX
urgente antes de esta tarea. `roadmap/FEEDBACK.md` sin ninguna entrada `nuevo`;
`mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero issues y
cero PR abiertos. §1 (fuente autoritativa) ya no tiene ninguna R-XX/T-XX `PENDIENTE` (R-23 es la
última, `COMPLETADA`): cola vacía, sin tarea de código que ejecutar. Verificación propia completa:
`mypy`/`ruff` en verde sin hallazgos (70 archivos), 646 tests (`pytest`) en verde, dieciocho etapas
OK en `verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en §3 (bloqueos) ni
§5 (P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`). Nota sin acción, mismo patrón que
motivó `#24`: `ROADMAP_PRODUCTO.md` (líneas 246-256, "Cola de producto") sigue describiendo R-23
como `PENDIENTE` en su prosa, pese a que §1 ya la registra `COMPLETADA` — hasta el siguiente ciclo
de Product Manager, que es quien archiva la oleada, no se corrige desde este ciclo de Programador
(la pregunta #11 de §6 sigue `(pendiente)` de respuesta del dueño).

**Última actualización anterior (2026-10-06, ciclo de Programador): primera reconfirmación del día
tras R-23**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, primera reconfirmación del día tras R-23,
2026-10-06):** sin incidencia. `git status` limpio antes de tocar nada; `git checkout develop`
dejó el contenedor en `HEAD` *detached* (resto de un contenedor anterior, descartable: ya
fusionado en `develop`); `git pull origin develop` resolvió en fast-forward limpio hasta `791ec07`
(R-23 implementada y `COMPLETADA`), sin conflicto ni rama divergida. `pip install -r
requirements-dev.txt` con el `pip` pelado de este contenedor instaló contra Python 3.13 en vez del
3.11.17 real del proyecto — mismo síntoma ya registrado (no un hallazgo nuevo, `#22`/R-15 ya
documentan el riesgo de invocar herramientas sin pasar por el intérprete correcto en un contenedor
de nube con más de un Python instalado); resuelto con `python3 -m pip install -r
requirements-dev.txt`, que sí resuelve al intérprete correcto (mismas versiones pineadas:
`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador de esa sesión: primera reconfirmación del día tras R-23**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: único
`ABIERTO` sigue siendo `#24` (baja, proceso — la pregunta de gobernanza #11 de §6 sigue
`(pendiente)`, veintiuna pasadas consecutivas), ninguno de severidad alta que atender como P-XX
urgente antes de esta tarea. `roadmap/FEEDBACK.md` sin ninguna entrada `nuevo`;
`mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero issues y
cero PR abiertos. §1 (fuente autoritativa) ya no tiene ninguna R-XX/T-XX `PENDIENTE` (R-23 es la
última, `COMPLETADA`): cola vacía, sin tarea de código que ejecutar. Verificación propia completa:
`mypy`/`ruff` en verde sin hallazgos (70 archivos), 646 tests (`pytest`) en verde, dieciocho etapas
OK en `verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en §3 (bloqueos) ni
§5 (P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`). Nota sin acción, mismo patrón que
motivó `#24`: `ROADMAP_PRODUCTO.md` seguirá describiendo R-23 como "EN CURSO"/`PENDIENTE` en su
prosa de "Cola de producto" hasta el siguiente ciclo de Product Manager, que es quien archiva la
oleada — no se corrige desde este ciclo de Programador (la pregunta #11 de §6 sigue `(pendiente)`
de respuesta del dueño).

**Última actualización anterior (2026-10-06, ciclo de Programador): R-23 implementada y
`COMPLETADA`.** Las desviaciones de `convencion.detectar_desviaciones` (T-10/T-33) ya llegan a
`guion-escenas.md` y `tarjetas.json` (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, 2026-10-06):** sin incidencia. `git
status` limpio antes de tocar nada; `git checkout develop && git pull origin develop` resolvió en
fast-forward limpio hasta `48004a1` (la auditoría del 2026-10-06, "sin hallazgos nuevos"), sin
conflicto ni rama divergida. `pip install -r requirements-dev.txt` con el `pip` pelado de este
contenedor instaló contra Python 3.13 en vez del 3.11.17 real del proyecto — mismo síntoma ya
registrado por la auditoría del 2026-10-06 (no un hallazgo nuevo, `#22`/R-15 ya documentan el
riesgo de invocar herramientas sin pasar por el intérprete correcto en un contenedor de nube con
más de un Python instalado); resuelto con `python3 -m pip install -r requirements-dev.txt`, que sí
resuelve al intérprete correcto (mismas versiones pineadas: `mypy==1.18.2`, `ruff==0.14.0`,
`pytest==8.4.2`).

**Revisión de entrada (protocolo):** registro de hallazgos de `auditoriacontinua.md` reconfirma un
único `ABIERTO`, `#24` (baja, proceso — la pregunta de gobernanza #11 de §6 sigue `(pendiente)`,
veinte pasadas consecutivas), ninguno de severidad alta que atender como P-XX urgente antes de
esta tarea. §1 (fuente autoritativa) tenía a R-23 como la única R-XX `PENDIENTE`, ya especificada
por completo en `ROADMAP_PRODUCTO.md` §"Oleada v11" por el ciclo de PM del 2026-10-05.

**Ciclo de Programador: R-23 implementada y `COMPLETADA`.** `documento_revision.py` llama una vez
a `convencion.detectar_desviaciones` (reutilizando la misma `clasificacion` que ya calculaba) y
reparte cada desviación por rango de línea: al pie de la escena que corresponda
(`### Desviaciones de la convención`, sección propia separada de las indicaciones no recitables)
o, si no cae en ninguna escena (p. ej. una sección auxiliar no reconocida), en una sección aparte
tras el resumen global (`## Desviaciones de la convención (fuera de escena)`); la cabecera gana el
recuento "Desviaciones de la convención: N", siempre presente, sin que `N=0` añada ninguna sección
nueva (mismo criterio que ya sigue el resto del documento). `pptx.py::ResultadoTarjetas` gana el
campo aditivo `metadatos.desviaciones_convencion` (mismo `resultado`/`clasificacion` reutilizado,
ninguna segunda implementación que pudiera divergir), vacío con `--para-terceros` igual que
`notas_internas`. Cero cambio en `convencion.detectar_desviaciones` en sí (requisito 6 de la
ficha). `references/contrato-tarjetas.md` documenta la clave nueva; `references/contrato-
montaje.md:68-73` deja de afirmar en abstracto que la numeración "ya NO se da por supuesta en
silencio" y pasa a decir exactamente dónde mirar en los dos consumidores reales. 9 tests nuevos
(637→646): `tests/test_documento_revision.py` (localización correcta al pie de la escena que
corresponde, sección fuera de escena, recuento de cabecera, `N=0` no añade ninguna sección),
`tests/test_pptx.py` (lista vacía sin desviaciones, misma descripción que `detectar_desviaciones`,
exclusión con `--para-terceros`, serialización en `tarjetas_a_diccionario`) y
`tests/test_integracion_montaje.py` (el mismo texto de desviación aparece en `guion-escenas.md` y
`tarjetas.json` a la vez — el hallazgo concreto que motivó abrir la tarea). Fixture dorada
`fixtures/guion-ejemplo-esperado.md` regenerada tras revisar el diff a mano: el único cambio es la
línea nueva de cabecera en `0` (los tres guiones reales y el guion de ejemplo no tienen
desviaciones conocidas, confirmando el criterio de aceptación). Verificación pre-push completa:
`mypy`/`ruff` en verde sin hallazgos (70 archivos), 646 tests (`pytest`, 637→646), dieciocho etapas
OK en `verificar_salidas.py --fixture` (sin cambios: R-23 no añade ninguna salida nueva, solo
enriquece dos ya existentes). Las cuatro redes en verde. `DEVELOPERS.md` y `SKILL.md` (incluida
`references/formato-guion-escenas.md`) actualizados. Sin cambios en §3 (bloqueos) ni §5 (P-XX); §6
sin novedad (la pregunta #11 sigue `(pendiente)`); sin nueva desviación en §7. Nota sin acción,
mismo patrón que motivó `#24`: `ROADMAP_PRODUCTO.md` seguirá describiendo R-23 como "EN
CURSO"/`PENDIENTE` en su prosa de "Cola de producto" hasta el siguiente ciclo de Product Manager,
que es quien archiva la oleada — no se corrige desde este ciclo de Programador (la pregunta #11 de
§6 sigue `(pendiente)` de respuesta del dueño).

**Última actualización anterior (2026-10-05, ciclo de Product Manager): archiva Oleada v10 (R-22) y
abre R-23 (Oleada v11)** (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Product Manager, 2026-10-05):** sin incidencia. `git
status` limpio antes de tocar nada; `git checkout develop && git pull origin develop` resolvió en
fast-forward limpio hasta `5e42f6e` (la novena reconfirmación del día de Programador tras R-22), sin
conflicto ni rama divergida. `pip install -r requirements-dev.txt` limpio (mismas versiones
pineadas: `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Product Manager: archiva Oleada v10 (R-22) y abre R-23 (Oleada v11).** Revisión de
entrada (protocolo): registro de hallazgos de `auditoriacontinua.md` reconfirma un único `ABIERTO`,
`#24` (baja, proceso — la pregunta de gobernanza #11 de §6 sigue `(pendiente)`, diecinueve pasadas
consecutivas de auditoría), ninguno de severidad alta ni de producto/arquitectura que convertir en
R-XX nueva este ciclo — el propio `#24` ya está enrutado a la pregunta #11, no es una R-XX.
`roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin ninguna entrada `nuevo` que
incorporar — el bloqueo #7 de §3 (grabar un curso completo) sigue sin resolverse. §1 (fuente
autoritativa) tenía a R-22 como `COMPLETADA` desde el ciclo de Programador del mismo día
(2026-10-05) que la abrió el ciclo de PM anterior (2026-10-02), con nueve reconfirmaciones
posteriores del Programador dejando `ROADMAP_PRODUCTO.md` describiéndola como "EN CURSO"/`PENDIENTE`
en su prosa de "Cola de producto" — el mismo patrón de latencia que motivó `#24`. Este ciclo corrige
esa prosa: Oleada v10 (R-22) se mueve íntegra a `roadmap/ROADMAP_HISTORICO.md` (spec completa +
"Cómo se entregó"), con su entrada de índice correspondiente.

**Se abre R-23** (Oleada v11) por grieta de arquitectura verificada, mismo criterio que abrió R-12 a
R-22: `scripts/convencion.py::detectar_desviaciones` (T-10, ampliada en T-33 con
`numero_escena_duplicado`/`numero_escena_no_creciente`) calcula correctamente las desviaciones de
convención que más le importan a la cadena de montaje, pero —verificado leyendo el código, con
`grep -rn "detectar_desviaciones"` sobre el repositorio completo, no solo la documentación— **nunca
se llama desde `scripts/documento_revision.py` (el `guion-escenas.md` que el dueño revisa) ni desde
`scripts/pptx.py` (`tarjetas.json`, el contrato de montaje)**, solo desde sus propios tests y
`tests/test_integracion_montaje.py`. El agravante que distingue esta grieta de las quince anteriores
de su mismo tipo (R-12 a R-22): `references/contrato-montaje.md:68-73` ya le dice a la futura cadena
de montaje, citando esta función por su nombre, que la numeración de escena "ya NO se da por
supuesta en silencio" — una afirmación que hoy ningún archivo generado real respalda. Spec completa
de R-23 en `ROADMAP_PRODUCTO.md` (Oleada v11), lista para que el siguiente ciclo de Programador la
implemente y verifique. Este ciclo es de PM, no de Programador: no se ha ejecutado la verificación
de las cuatro redes ni se ha tocado `scripts/`, `tests/` ni `assets/`.

Sin cambios en §3 (bloqueos) ni §5 (P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`); sin
nueva desviación en §7.

**Última actualización anterior (2026-10-05, ciclo de Programador): novena reconfirmación del día
tras R-22**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, novena reconfirmación del día tras
R-22, 2026-10-05):** sin incidencia. `git status` limpio antes de tocar nada; `git checkout
develop` ya estaba en `develop` (contenedor con el repo preexistente, sin *detached HEAD*);
`git pull origin develop` resolvió en fast-forward limpio hasta `9d87944` (la octava
reconfirmación del día tras R-22), sin conflicto ni rama divergida. `pip install -r
requirements-dev.txt` limpio (mismas versiones pineadas: `mypy==1.18.2`, `ruff==0.14.0`,
`pytest==8.4.2`).

**Ciclo de Programador de esa sesión: novena reconfirmación del día tras R-22**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: único `ABIERTO`
sigue siendo `#24` (baja, proceso — la pregunta de gobernanza #11 de §6 sigue `(pendiente)`, veinticuatro
pasadas consecutivas), ninguno de severidad alta que atender como P-XX urgente antes de esta
tarea. `roadmap/FEEDBACK.md` sin ninguna entrada `nuevo`; `mcp__github__list_issues`/
`list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero issues y cero PR abiertos. §1 (fuente
autoritativa) ya no tiene ninguna R-XX/T-XX `PENDIENTE` (R-22 es la última, `COMPLETADA`): cola
vacía, sin tarea de código que ejecutar. Verificación propia completa: `mypy`/`ruff` en verde sin
hallazgos (70 archivos), 637 tests (`pytest`) en verde, dieciocho etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en §3 (bloqueos) ni §5
(P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`). Nota sin acción, mismo patrón que
motivó `#24`: `ROADMAP_PRODUCTO.md` seguirá describiendo R-22 como "EN CURSO"/`PENDIENTE` en su
prosa de "Cola de producto" hasta el siguiente ciclo de Product Manager, que es quien archiva la
oleada — no se corrige desde este ciclo de Programador (la pregunta #11 de §6 sigue `(pendiente)`
de respuesta del dueño).

**Última actualización anterior (2026-10-05, ciclo de Programador): octava reconfirmación del día
tras R-22**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, octava reconfirmación del día tras
R-22, 2026-10-05):** sin incidencia. `git status` limpio antes de tocar nada; `git checkout
develop` dejó el contenedor en `HEAD` *detached*, 37 commits por detrás sin rama asociada (resto
de un contenedor anterior, descartable: ya fusionados en `develop`); `git pull origin develop`
resolvió en fast-forward limpio hasta `0deb2b7` (la séptima reconfirmación del día tras R-22), sin
conflicto ni rama divergida. `pip install -r requirements-dev.txt` limpio (mismas versiones
pineadas: `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador de esa sesión: octava reconfirmación del día tras R-22**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: único `ABIERTO`
sigue siendo `#24` (baja, proceso — la pregunta de gobernanza #11 de §6 sigue `(pendiente)`, veintitrés
pasadas consecutivas), ninguno de severidad alta que atender como P-XX urgente antes de esta
tarea. `roadmap/FEEDBACK.md` sin ninguna entrada `nuevo`; `mcp__github__list_issues`/
`list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero issues y cero PR abiertos. §1 (fuente
autoritativa) ya no tiene ninguna R-XX/T-XX `PENDIENTE` (R-22 es la última, `COMPLETADA`): cola
vacía, sin tarea de código que ejecutar. Verificación propia completa: `mypy`/`ruff` en verde sin
hallazgos (70 archivos), 637 tests (`pytest`) en verde, dieciocho etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en §3 (bloqueos) ni §5
(P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`). Nota sin acción, mismo patrón que
motivó `#24`: `ROADMAP_PRODUCTO.md` seguirá describiendo R-22 como "EN CURSO"/`PENDIENTE` en su
prosa de "Cola de producto" hasta el siguiente ciclo de Product Manager, que es quien archiva la
oleada — no se corrige desde este ciclo de Programador (la pregunta #11 de §6 sigue `(pendiente)`
de respuesta del dueño).

**Última actualización anterior (2026-10-05, ciclo de Programador): séptima reconfirmación del día
tras R-22**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, séptima reconfirmación del día tras
R-22, 2026-10-05):** sin incidencia. `git status` limpio antes de tocar nada; `git checkout
develop` dejó el contenedor en `HEAD` *detached*, 36 commits por detrás sin rama asociada (resto
de un contenedor anterior, descartable: ya fusionados en `develop`); `git pull origin develop`
resolvió en fast-forward limpio hasta `285dfc6` (la sexta reconfirmación del día tras R-22), sin
conflicto ni rama divergida. `pip install -r requirements-dev.txt` limpio (mismas versiones
pineadas: `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador de esa sesión: séptima reconfirmación del día tras R-22**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: único `ABIERTO`
sigue siendo `#24` (baja, proceso — la pregunta de gobernanza #11 de §6 sigue `(pendiente)`, veintidós
pasadas consecutivas), ninguno de severidad alta que atender como P-XX urgente antes de esta
tarea. `roadmap/FEEDBACK.md` sin ninguna entrada `nuevo`; `mcp__github__list_issues`/
`list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero issues y cero PR abiertos. §1 (fuente
autoritativa) ya no tiene ninguna R-XX/T-XX `PENDIENTE` (R-22 es la última, `COMPLETADA`): cola
vacía, sin tarea de código que ejecutar. Verificación propia completa: `mypy`/`ruff` en verde sin
hallazgos (70 archivos), 637 tests (`pytest`) en verde, dieciocho etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en §3 (bloqueos) ni §5
(P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`). Nota sin acción, mismo patrón que
motivó `#24`: `ROADMAP_PRODUCTO.md` seguirá describiendo R-22 como "EN CURSO"/`PENDIENTE` en su
prosa de "Cola de producto" hasta el siguiente ciclo de Product Manager, que es quien archiva la
oleada — no se corrige desde este ciclo de Programador (la pregunta #11 de §6 sigue `(pendiente)`
de respuesta del dueño).

**Última actualización anterior (2026-10-05, ciclo de Programador): sexta reconfirmación del día
tras R-22**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, sexta reconfirmación del día tras
R-22, 2026-10-05):** sin incidencia. `git status` limpio antes de tocar nada; `git checkout
develop` dejó el contenedor en `HEAD` *detached*, 35 commits por detrás sin rama asociada (resto
de un contenedor anterior, descartable: ya fusionados en `develop`); `git pull origin develop`
resolvió en fast-forward limpio hasta `e3b09b4` (la quinta reconfirmación del día tras R-22), sin
conflicto ni rama divergida. `pip install -r requirements-dev.txt` limpio (mismas versiones
pineadas: `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador de esa sesión: sexta reconfirmación del día tras R-22**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: único `ABIERTO`
sigue siendo `#24` (baja, proceso — la pregunta de gobernanza #11 de §6 sigue `(pendiente)`, veintiuna
pasadas consecutivas), ninguno de severidad alta que atender como P-XX urgente antes de esta
tarea. `roadmap/FEEDBACK.md` sin ninguna entrada `nuevo`; `mcp__github__list_issues`/
`list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero issues y cero PR abiertos. §1 (fuente
autoritativa) ya no tiene ninguna R-XX/T-XX `PENDIENTE` (R-22 es la última, `COMPLETADA`): cola
vacía, sin tarea de código que ejecutar. Verificación propia completa: `mypy`/`ruff` en verde sin
hallazgos (70 archivos), 637 tests (`pytest`) en verde, dieciocho etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en §3 (bloqueos) ni §5
(P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`). Nota sin acción, mismo patrón que
motivó `#24`: `ROADMAP_PRODUCTO.md` seguirá describiendo R-22 como "EN CURSO"/`PENDIENTE` en su
prosa de "Cola de producto" hasta el siguiente ciclo de Product Manager, que es quien archiva la
oleada — no se corrige desde este ciclo de Programador (la pregunta #11 de §6 sigue `(pendiente)`
de respuesta del dueño).

**Última actualización anterior (2026-10-05, ciclo de Programador): quinta reconfirmación del día
tras R-22**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, quinta reconfirmación del día tras
R-22, 2026-10-05):** sin incidencia. `git status` limpio antes de tocar nada; `git checkout
develop` dejó el contenedor en `HEAD` *detached*, 34 commits por detrás sin rama asociada (resto
de un contenedor anterior, descartable: ya fusionados en `develop`); `git pull origin develop`
resolvió en fast-forward limpio hasta `9b7cfd4` (la cuarta reconfirmación del día tras R-22), sin
conflicto ni rama divergida. `pip install -r requirements-dev.txt` limpio (mismas versiones
pineadas: `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador de esa sesión: quinta reconfirmación del día tras R-22**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: único `ABIERTO`
sigue siendo `#24` (baja, proceso — la pregunta de gobernanza #11 de §6 sigue `(pendiente)`, veinte
pasadas consecutivas), ninguno de severidad alta que atender como P-XX urgente antes de esta
tarea. `roadmap/FEEDBACK.md` sin ninguna entrada `nuevo`; `mcp__github__list_issues`/
`list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero issues y cero PR abiertos. §1 (fuente
autoritativa) ya no tiene ninguna R-XX/T-XX `PENDIENTE` (R-22 es la última, `COMPLETADA`): cola
vacía, sin tarea de código que ejecutar. Verificación propia completa: `mypy`/`ruff` en verde sin
hallazgos (70 archivos), 637 tests (`pytest`) en verde, dieciocho etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en §3 (bloqueos) ni §5
(P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`). Nota sin acción, mismo patrón que
motivó `#24`: `ROADMAP_PRODUCTO.md` seguirá describiendo R-22 como "EN CURSO"/`PENDIENTE` en su
prosa de "Cola de producto" hasta el siguiente ciclo de Product Manager, que es quien archiva la
oleada — no se corrige desde este ciclo de Programador (la pregunta #11 de §6 sigue `(pendiente)`
de respuesta del dueño).

**Última actualización anterior (2026-10-05, ciclo de Programador): cuarta reconfirmación del día
tras R-22**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, cuarta reconfirmación del día tras
R-22, 2026-10-05):** sin incidencia. `git status` limpio antes de tocar nada; `git checkout
develop` dejó el contenedor en `HEAD` *detached*, sin rama asociada (resto de un contenedor
anterior, descartable: ya fusionado en `develop`); `git pull origin develop` resolvió en
fast-forward limpio hasta `309c945` (la tercera reconfirmación del día tras R-22), sin conflicto
ni rama divergida. `pip install -r requirements-dev.txt` limpio (mismas versiones pineadas:
`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador de esa sesión: cuarta reconfirmación del día tras R-22**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: único `ABIERTO`
sigue siendo `#24` (baja, proceso — la pregunta de gobernanza #11 de §6 sigue `(pendiente)`, veinte
pasadas consecutivas), ninguno de severidad alta que atender como P-XX urgente antes de esta
tarea. `roadmap/FEEDBACK.md` sin ninguna entrada `nuevo`; `mcp__github__list_issues`/
`list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero issues y cero PR abiertos. §1 (fuente
autoritativa) ya no tiene ninguna R-XX/T-XX `PENDIENTE` (R-22 es la última, `COMPLETADA`): cola
vacía, sin tarea de código que ejecutar. Verificación propia completa: `mypy`/`ruff` en verde sin
hallazgos (70 archivos), 637 tests (`pytest`) en verde, dieciocho etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en §3 (bloqueos) ni §5
(P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`). Nota sin acción, mismo patrón que
motivó `#24`: `ROADMAP_PRODUCTO.md` seguirá describiendo R-22 como "EN CURSO"/`PENDIENTE` en su
prosa de "Cola de producto" hasta el siguiente ciclo de Product Manager, que es quien archiva la
oleada — no se corrige desde este ciclo de Programador (la pregunta #11 de §6 sigue `(pendiente)`
de respuesta del dueño).

**Última actualización anterior (2026-10-05, ciclo de Programador): tercera reconfirmación del día
tras R-22**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, tercera reconfirmación del día tras
R-22, 2026-10-05):** sin incidencia. `git status` limpio antes de tocar nada; `git checkout
develop` avisó de 32 commits por delante de cualquier rama local, sin rama asociada (resto de un
contenedor anterior, descartable: ya fusionados en `develop`); `git pull origin develop` resolvió
en fast-forward limpio hasta `3069d13` (la segunda reconfirmación del día tras R-22), sin
conflicto ni rama divergida. `pip install -r requirements-dev.txt` limpio (mismas versiones
pineadas: `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador de esa sesión: tercera reconfirmación del día tras R-22**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: único `ABIERTO`
sigue siendo `#24` (baja, proceso — la pregunta de gobernanza #11 de §6 sigue `(pendiente)`,
diecinueve pasadas consecutivas), ninguno de severidad alta que atender como P-XX urgente antes de
esta tarea. `roadmap/FEEDBACK.md` sin ninguna entrada `nuevo`; `mcp__github__list_issues`/
`list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero issues y cero PR abiertos. §1 (fuente
autoritativa) ya no tiene ninguna R-XX/T-XX `PENDIENTE` (R-22 es la última, `COMPLETADA`): cola
vacía, sin tarea de código que ejecutar. Verificación propia completa: `mypy`/`ruff` en verde sin
hallazgos (70 archivos), 637 tests (`pytest`) en verde, dieciocho etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en §3 (bloqueos) ni §5
(P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`). Nota sin acción, mismo patrón que
motivó `#24`: `ROADMAP_PRODUCTO.md` seguirá describiendo R-22 como "EN CURSO"/`PENDIENTE` en su
prosa de "Cola de producto" hasta el siguiente ciclo de Product Manager, que es quien archiva la
oleada — no se corrige desde este ciclo de Programador (la pregunta #11 de §6 sigue `(pendiente)`
de respuesta del dueño).

**Última actualización anterior (2026-10-05, ciclo de Programador): segunda reconfirmación del día
tras R-22**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de esa sesión (ciclo de Programador, segunda reconfirmación del día tras
R-22, 2026-10-05):** sin incidencia. `git status` limpio antes de tocar nada; `git checkout
develop` avisó de 31 commits por delante de cualquier rama local, sin rama asociada (resto de un
contenedor anterior, descartable: ya fusionados en `develop`); `git pull origin develop` resolvió
en fast-forward limpio hasta `5f2575f` (la primera reconfirmación del día tras R-22), sin
conflicto ni rama divergida. `pip install -r requirements-dev.txt` limpio (mismas versiones
pineadas: `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador de esa sesión: segunda reconfirmación del día tras R-22**, sin novedad de
código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: único `ABIERTO`
sigue siendo `#24` (baja, proceso — la pregunta de gobernanza #11 de §6 sigue `(pendiente)`,
diecinueve pasadas consecutivas), ninguno de severidad alta que atender como P-XX urgente antes de
esta tarea. `roadmap/FEEDBACK.md` sin ninguna entrada `nuevo`; `mcp__github__list_issues`/
`list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero issues y cero PR abiertos. §1 (fuente
autoritativa) ya no tiene ninguna R-XX/T-XX `PENDIENTE` (R-22 es la última, `COMPLETADA`): cola
vacía, sin tarea de código que ejecutar. Verificación propia completa: `mypy`/`ruff` en verde sin
hallazgos (70 archivos), 637 tests (`pytest`) en verde, dieciocho etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Sin cambios en §3 (bloqueos) ni §5
(P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`). Nota sin acción, mismo patrón que
motivó `#24`: `ROADMAP_PRODUCTO.md` seguirá describiendo R-22 como "EN CURSO"/`PENDIENTE` en su
prosa de "Cola de producto" hasta el siguiente ciclo de Product Manager, que es quien archiva la
oleada — no se corrige desde este ciclo de Programador (la pregunta #11 de §6 sigue `(pendiente)`
de respuesta del dueño).

**Última actualización anterior (2026-10-05, ciclo de Programador): primera reconfirmación del día
tras R-22**, sin novedad de código (detalle en la nota de esa sesión, más abajo).

**Última actualización anterior (2026-10-05, ciclo de Programador): R-22 implementada y
`COMPLETADA`.** Oleada v10 (`capitulos-ffmpeg.txt`, formato `FFMETADATA1` nativo de ffmpeg)
cierra la única R-XX que quedaba en cola (detalle en la nota de esa sesión, más abajo).

**Nota de arranque de la sesión anterior (ciclo de Programador, 2026-10-05):** sin incidencia. `git
status` limpio antes de tocar nada; `git checkout develop` avisó de 29 commits por delante de
cualquier rama local, sin rama asociada (resto de un contenedor anterior, descartable: ya
fusionados en `develop`); `git pull origin develop` resolvió en fast-forward limpio hasta
`d926ede` (la auditoría 2026-10-05, "sin hallazgos nuevos"), sin conflicto ni rama divergida.
`pip install -r requirements-dev.txt` limpio (mismas versiones pineadas:
`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Ciclo de Programador (2026-10-05): R-22 implementada y `COMPLETADA`.** Revisión de entrada
(protocolo): registro de hallazgos de `auditoriacontinua.md` reconfirma un único `ABIERTO`, `#24`
(baja, proceso — la pregunta de gobernanza #11 de §6 sigue `(pendiente)`, decimonovena pasada
consecutiva), ninguno de severidad alta que atender como P-XX urgente antes de esta tarea. §1 (fuente
autoritativa) tenía a R-22 (Oleada v10) como la única R-XX `PENDIENTE`, ya especificada por completo
en `ROADMAP_PRODUCTO.md` §"Oleada v10" por el ciclo de PM del 2026-10-02: `capitulos-ffmpeg.txt`,
formato `FFMETADATA1` nativo de ffmpeg, reutilizando tal cual el emparejamiento título↔escena y los
tiempos real/estimado que `capitulos_youtube.calcular_capitulos` ya calcula para
`capitulos-youtube.txt` (R-07) — sin recalcular nada nuevo, solo exponerlos en un segundo formato.
Implementada siguiendo los diez requisitos de la ficha: `ResultadoCapitulos.duracion_total_segundos`
(campo aditivo), `formatear_capitulos_ffmpeg`/`validar_capitulos_ffmpeg` en `scripts/capitulos_youtube.py`,
generación como segunda mitad de la opción `CAPITULOS_YOUTUBE` del selector (no una séptima opción,
requisito 8) en `scripts/salidas.py::_generar_capitulos_youtube`, validada antes de escribir desde el
primer día (requisito 7, misma lección que el hallazgo `#27`/R-21). Detalle técnico completo en la
fila de §1 de este documento y en `DECISIONES_TECNICAS.md`/`HISTORIAL_SESIONES.md`. Verificación
pre-push completa: `mypy`/`ruff` en verde sin hallazgos (70 archivos), 637 tests (`pytest`, 619→637),
dieciocho etapas OK en `verificar_salidas.py --fixture` (dos nuevas: "Generación de capítulos de
ffmpeg (FFMETADATA1)" y "Validez de los capítulos de ffmpeg (FFMETADATA1)"). Las cuatro redes en
verde. `references/contrato-montaje.md`, `DEVELOPERS.md` y `SKILL.md` actualizados. Sin cambios en §3
(bloqueos) ni §5 (P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`). Nota sin acción, mismo
patrón que motivó `#24`: `ROADMAP_PRODUCTO.md` seguirá describiendo R-22 como "EN CURSO"/`PENDIENTE`
en su prosa de "Cola de producto" hasta el siguiente ciclo de Product Manager, que es quien archiva la
oleada — no se corrige desde este ciclo de Programador (la pregunta #11 de §6 sigue `(pendiente)` de
respuesta del dueño).

**Última actualización anterior (2026-10-04, ciclo de Product Manager): reconfirmación de cola, sin
R-XX nueva abierta.** R-22 (Oleada v10) seguía `PENDIENTE` de implementación por el Programador
(detalle en la nota de esa sesión, más abajo).

**Última actualización anterior (2026-10-03, ciclo de Product Manager): reconfirmación de cola, sin
R-XX nueva abierta** (detalle en la nota de arranque de esa sesión, más abajo).

**Última actualización anterior (2026-10-02, ciclo de Product Manager): archiva Fase transversal F-J
(R-21) y abre R-22 (Oleada v10)** (detalle en la nota de arranque de esa sesión, más abajo).

**Última actualización anterior (novena reconfirmación del día tras R-21, ciclo de Programador):**
**Ciclo de Programador: novena reconfirmación del día tras R-21**, sin novedad de código (detalle en
la nota de arranque de esa sesión, más abajo).

**Última actualización anterior (octava reconfirmación del día tras R-21):** **Ciclo de
Programador: octava reconfirmación del día tras R-21** (implementada y `COMPLETADA` en el ciclo
`1e8d514`, reconfirmada antes en `0f392b3`, `945155f`, `842c300`, `698fc05`, `787c4c4`, `cbf2e90` y
`e5125ee`), sin novedad de código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de
proceder: ningún `ABIERTO` de severidad alta (`#24` baja, proceso — la pregunta #11 de §6 sigue
`(pendiente)`; `#27`, media, cerrado en la práctica por la implementación de R-21 — reverificado de
nuevo en esta sesión leyendo directamente `scripts/salidas.py::_generar_concat_ffmpeg` (invoca
`validar_lista_concat_ffmpeg` antes de escribir a disco), `scripts/tomas.py::_sanear_archivo_video`
y `assets/reproductor/guion.js::sanearArchivoVideo` (ambos puntos de entrada de `archivo_video`
saneados): el código sigue intacto, pendiente solo de que la próxima pasada del auditor actualice su
propia fila del registro a `RESUELTO`, ninguno urgente por §0.3). `roadmap/FEEDBACK.md` sin ninguna
entrada `nuevo`; `mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/telePrompter`:
cero issues y cero PR abiertos. §1 ya no tiene ninguna R-XX/T-XX `PENDIENTE` (R-21 es la última,
`COMPLETADA`): cola vacía, sin tarea de código que ejecutar. Verificación propia completa:
`mypy`/`ruff` en verde sin hallazgos (70 archivos), 619 tests (`pytest`) en verde, dieciséis etapas OK
en `verificar_salidas.py --fixture`. Las cuatro redes en verde. Nota sin acción, mismo patrón que
motivó `#24`: `ROADMAP_PRODUCTO.md` sigue describiendo R-21 como la única `PENDIENTE` en su prosa de
"Cola de producto" pese a que este §1 ya la registra `COMPLETADA` — no se corrige desde aquí (la
pregunta #11 de §6 sigue `(pendiente)` de respuesta del dueño); se deja constancia para el próximo
ciclo de Product Manager, que es quien escribe ese documento.

**Última actualización anterior (séptima reconfirmación del día tras R-21):** **Ciclo de
Programador: séptima reconfirmación del día tras R-21** (implementada y `COMPLETADA` en el ciclo
`1e8d514`, reconfirmada antes en `0f392b3`, `945155f`, `842c300`, `698fc05`, `787c4c4` y `cbf2e90`),
sin novedad de código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder:
ningún `ABIERTO` de severidad alta (`#24` baja, proceso — la pregunta #11 de §6 sigue `(pendiente)`;
`#27`, media, cerrado en la práctica por la implementación de R-21 — reverificado de nuevo en esta
sesión leyendo directamente `scripts/salidas.py::_generar_concat_ffmpeg` (invoca
`validar_lista_concat_ffmpeg` antes de escribir a disco), `scripts/tomas.py::_sanear_archivo_video`
y `assets/reproductor/guion.js::sanearArchivoVideo` (ambos puntos de entrada de `archivo_video`
saneados): el código sigue intacto, pendiente solo de que la próxima pasada del auditor actualice su
propia fila del registro a `RESUELTO`, ninguno urgente por §0.3). `roadmap/FEEDBACK.md` sin ninguna
entrada `nuevo`; `mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/telePrompter`:
cero issues y cero PR abiertos. §1 ya no tiene ninguna R-XX/T-XX `PENDIENTE` (R-21 es la última,
`COMPLETADA`): cola vacía, sin tarea de código que ejecutar. Verificación propia completa:
`mypy`/`ruff` en verde sin hallazgos (70 archivos), 619 tests (`pytest`) en verde, dieciséis etapas OK
en `verificar_salidas.py --fixture`. Las cuatro redes en verde. Nota sin acción, mismo patrón que
motivó `#24`: `ROADMAP_PRODUCTO.md` sigue describiendo R-21 como la única `PENDIENTE` en su prosa de
"Cola de producto" pese a que este §1 ya la registra `COMPLETADA` — no se corrige desde aquí (la
pregunta #11 de §6 sigue `(pendiente)` de respuesta del dueño); se deja constancia para el próximo
ciclo de Product Manager, que es quien escribe ese documento.

**Última actualización anterior (sexta reconfirmación del día tras R-21):** **Ciclo de
Programador: sexta reconfirmación del día tras R-21** (implementada y `COMPLETADA` en el ciclo
`1e8d514`, reconfirmada antes en `0f392b3`, `945155f`, `842c300`, `698fc05` y `787c4c4`), sin
novedad de código. Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder:
ningún `ABIERTO` de severidad alta (`#24` baja, proceso — la pregunta #11 de §6 sigue `(pendiente)`;
`#27`, media, cerrado en la práctica por la implementación de R-21 (verificado de nuevo leyendo
`scripts/salidas.py`/`scripts/tomas.py`/`assets/reproductor/guion.js`: la fila del registro del
auditor seguía sin marcar `RESUELTO` pese a que el código ya invoca el validador y sanea
`archivo_video` en sus dos puntos de entrada — desfase de la propia pasada del auditor, no del
código, pendiente solo de que la próxima pasada lo reevalúe), ninguno urgente por §0.3).
`roadmap/FEEDBACK.md` sin ninguna entrada `nuevo`; `mcp__github__list_issues`/`list_pull_requests`
sobre `janosolerdiaz/telePrompter`: cero issues y cero PR abiertos. §1 ya no tiene ninguna R-XX/T-XX
`PENDIENTE` (R-21 es la última, `COMPLETADA`): cola vacía, sin tarea de código que ejecutar.
Verificación propia completa: `mypy`/`ruff` en verde sin hallazgos (70 archivos), 619 tests
(`pytest`) en verde, dieciséis etapas OK en `verificar_salidas.py --fixture`. Las cuatro redes en
verde. Nota sin acción, mismo patrón que motivó `#24`: `ROADMAP_PRODUCTO.md` sigue describiendo
R-21 como la única `PENDIENTE` en su prosa de "Cola de producto" pese a que este §1 ya la registra
`COMPLETADA` — no se corrige desde aquí (la pregunta #11 de §6 sigue `(pendiente)` de respuesta del
dueño); se deja constancia para el próximo ciclo de Product Manager, que es quien escribe ese
documento.

**Última actualización anterior (quinta reconfirmación del día tras R-21):** **Ciclo de
Programador: quinta reconfirmación del día tras R-21** (implementada y `COMPLETADA` en el ciclo
`1e8d514`, reconfirmada antes en `0f392b3`, `945155f`, `842c300` y `698fc05`), sin novedad de código.
Registro de hallazgos de `auditoriacontinua.md` revisado antes de proceder: ningún `ABIERTO` de
severidad alta (`#24` baja, proceso — la pregunta #11 de §6 sigue `(pendiente)`; `#27`, media,
cerrado en la práctica por la implementación de R-21, pendiente solo de que la próxima pasada del
auditor lo reevalúe y lo marque `RESUELTO`, ninguno urgente por §0.3 — la auditoría del 2026-10-02 ya
reconfirmó ambos sin cambios). `roadmap/FEEDBACK.md` sin ninguna entrada `nuevo`;
`mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero issues y
cero PR abiertos. §1 ya no tiene ninguna R-XX/T-XX `PENDIENTE` (R-21 es la última, `COMPLETADA`):
cola vacía, sin tarea de código que ejecutar. Verificación propia completa: `mypy`/`ruff` en verde sin
hallazgos (70 archivos), 619 tests (`pytest`) en verde, dieciséis etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Nota sin acción, mismo patrón que motivó
`#24`: `ROADMAP_PRODUCTO.md` sigue describiendo R-21 como la única `PENDIENTE` en su prosa de "Cola de
producto" pese a que este §1 ya la registra `COMPLETADA` — no se corrige desde aquí (la pregunta #11
de §6 sigue `(pendiente)` de respuesta del dueño); se deja constancia para el próximo ciclo de
Product Manager, que es quien escribe ese documento.

**Última actualización anterior (cuarta reconfirmación del día tras R-21):** **Ciclo de
Programador: cuarta reconfirmación del día tras R-21** (implementada y `COMPLETADA` en el ciclo
`1e8d514`, reconfirmada antes en `0f392b3`, `945155f` y `842c300`), sin novedad de código. Registro
de hallazgos de `auditoriacontinua.md` revisado antes de proceder: ningún `ABIERTO` de severidad alta
(`#24` baja, proceso — la pregunta #11 de §6 sigue `(pendiente)`; `#27`, media, cerrado en la
práctica por la implementación de R-21, pendiente solo de que la próxima pasada del auditor lo
reevalúe y lo marque `RESUELTO`, ninguno urgente por §0.3 — la auditoría del 2026-10-02 ya reconfirmó
ambos sin cambios). `roadmap/FEEDBACK.md` sin ninguna entrada `nuevo`;
`mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero issues y
cero PR abiertos. §1 ya no tiene ninguna R-XX/T-XX `PENDIENTE` (R-21 es la última, `COMPLETADA`):
cola vacía, sin tarea de código que ejecutar. Verificación propia completa: `mypy`/`ruff` en verde sin
hallazgos (70 archivos), 619 tests (`pytest`) en verde, dieciséis etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Nota sin acción, mismo patrón que motivó
`#24`: `ROADMAP_PRODUCTO.md` sigue describiendo R-21 como la única `PENDIENTE` en su prosa de "Cola de
producto" pese a que este §1 ya la registra `COMPLETADA` — no se corrige desde aquí (la pregunta #11
de §6 sigue `(pendiente)` de respuesta del dueño); se deja constancia para el próximo ciclo de
Product Manager, que es quien escribe ese documento.

**Última actualización anterior (tercera reconfirmación del día tras R-21):** **Ciclo de
Programador: tercera reconfirmación del día tras R-21** (implementada y `COMPLETADA` en el ciclo
`1e8d514`, reconfirmada antes en `0f392b3` y `945155f`), sin novedad de código. Registro de
hallazgos de `auditoriacontinua.md` revisado antes de proceder: ningún `ABIERTO` de severidad alta
(`#24` baja, proceso — la pregunta #11 de §6 sigue `(pendiente)`; `#27`, media, cerrado en la
práctica por la implementación de R-21, pendiente solo de que la próxima pasada del auditor lo
reevalúe y lo marque `RESUELTO`, ninguno urgente por §0.3 — la auditoría del 2026-10-02 ya reconfirmó
ambos sin cambios). `roadmap/FEEDBACK.md` sin ninguna entrada `nuevo`;
`mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero issues y
cero PR abiertos. §1 ya no tiene ninguna R-XX/T-XX `PENDIENTE` (R-21 es la última, `COMPLETADA`):
cola vacía, sin tarea de código que ejecutar. Verificación propia completa: `mypy`/`ruff` en verde sin
hallazgos (70 archivos), 619 tests (`pytest`) en verde, dieciséis etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Nota sin acción, mismo patrón que motivó
`#24`: `ROADMAP_PRODUCTO.md` sigue describiendo R-21 como la única `PENDIENTE` en su prosa de "Cola de
producto" pese a que este §1 ya la registra `COMPLETADA` — no se corrige desde aquí (la pregunta #11
de §6 sigue `(pendiente)` de respuesta del dueño); se deja constancia para el próximo ciclo de
Product Manager, que es quien escribe ese documento.

**Última actualización anterior (segunda reconfirmación del día tras R-21):** **Ciclo de
Programador: segunda reconfirmación del día tras R-21** (implementada y `COMPLETADA` en el ciclo
`1e8d514`, reconfirmada por primera vez ese mismo día en `0f392b3`), sin novedad de código. Registro
de hallazgos de `auditoriacontinua.md` revisado antes de proceder: ningún `ABIERTO` de severidad alta
(`#24` baja, proceso — la pregunta #11 de §6 sigue `(pendiente)`; `#27`, media, cerrado en la
práctica por la implementación de R-21, pendiente solo de que la próxima pasada del auditor lo
reevalúe y lo marque `RESUELTO`, ninguno urgente por §0.3 — la auditoría del 2026-10-02 ya reconfirmó
ambos sin cambios). `roadmap/FEEDBACK.md` sin ninguna entrada `nuevo`;
`mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero issues y
cero PR abiertos. §1 ya no tiene ninguna R-XX/T-XX `PENDIENTE` (R-21 es la última, `COMPLETADA`):
cola vacía, sin tarea de código que ejecutar. Verificación propia completa: `mypy`/`ruff` en verde sin
hallazgos (70 archivos), 619 tests (`pytest`) en verde, dieciséis etapas OK en
`verificar_salidas.py --fixture`. Las cuatro redes en verde. Nota sin acción, mismo patrón que motivó
`#24`: `ROADMAP_PRODUCTO.md` sigue describiendo R-21 como la única `PENDIENTE` en su prosa de "Cola de
producto" pese a que este §1 ya la registra `COMPLETADA` — no se corrige desde aquí (la pregunta #11
de §6 sigue `(pendiente)` de respuesta del dueño); se deja constancia para el próximo ciclo de
Product Manager, que es quien escribe ese documento.

**Última actualización anterior (R-21, implementada en el ciclo previo):** **Ciclo de Programador:
R-21 implementada y `COMPLETADA`** (Fase transversal F-J, cierra el hallazgo `#27` de
`auditoriacontinua.md`). `scripts/salidas.py::_generar_concat_ffmpeg`
invoca ahora `concat_ffmpeg.validar_lista_concat_ffmpeg` sobre el contenido antes de escribirlo —
hasta ahora solo lo ejercitaba `verificar_salidas.py --fixture`, nunca la ruta real de generación —
degradando a `SalidaOmitida` con el motivo exacto si falla, nunca una excepción sin capturar.
`scripts/tomas.py` gana `_sanear_archivo_video` (recorta espacios, normaliza a `""` si queda vacío o
trae `\n`/`\r`) aplicada al leer un parte de rodaje editado a mano; `assets/reproductor/guion.js` gana
la función gemela `sanearArchivoVideo(valor)` aplicada en los dos puntos donde el dueño teclea el
valor (grabación con `V`/`v` y edición desde el índice). 6 tests nuevos (613→619). Cuatro redes en
verde, incluidas las dieciséis etapas de `verificar_salidas.py --fixture`. `references/contrato-tomas.md`,
`contrato-montaje.md`, `DEVELOPERS.md` y `SKILL.md` actualizados. Decisión registrada en
`DECISIONES_TECNICAS.md`; detalle completo de este ciclo en `HISTORIAL_SESIONES.md`. §1 pasa `R-21` a
`COMPLETADA`. Sin hallazgo de severidad alta `ABIERTO` en `auditoriacontinua.md` que atender como
P-XX urgente antes de esta tarea (único hallazgo `ABIERTO` de severidad media, `#27`, es justamente el
que esta tarea cierra; `#24`, baja, sigue pendiente solo de la respuesta del dueño a la pregunta #11
de §6).

**Nota de arranque de esta sesión (ciclo de Product Manager, 2026-10-04):** sin incidencia. `git
status` limpio antes de tocar nada; `git checkout develop` avisó de 27 commits por detrás sin rama
asociada (reconfirmaciones y auditorías ya fusionadas en `develop`, descartable); `git pull origin
develop` resolvió en fast-forward limpio hasta `6689d90` (la auditoría 2026-10-04, "sin hallazgos
nuevos, sin cambios de código desde la pasada anterior"), sin conflicto ni rama divergida. `pip
install -r requirements-dev.txt` limpio.

**Ciclo de Product Manager (2026-10-04): reconfirmación de cola, sin R-XX nueva abierta.**
Revisión de entrada (protocolo): registro de hallazgos de `auditoriacontinua.md` reconfirma un único
`ABIERTO`, `#24` (baja, proceso — la pregunta de gobernanza #11 de §6 sigue `(pendiente)` de
respuesta del dueño, decimoctava pasada consecutiva esperándola según la propia auditoría de hoy;
no es una R-XX, ya enrutada) — confirmado contando la columna `Estado` de las 27 filas del registro,
no solo leyendo la narrativa. `roadmap/FEEDBACK.md`: sigue con la única fila de plantilla vacía,
ninguna entrada `nuevo` real — el bloqueo #7 de §3 (grabar un curso completo) sigue abierto, así que
no hay historia de rodaje real que incorporar. `mcp__github__list_issues`/`list_pull_requests` sobre
`janosolerdiaz/teleprompter`: cero issues y cero PR abiertos. §1 (fuente autoritativa): sin fila
nueva para R-22 — el ciclo de Programador que la implementa no ha corrido todavía desde que se abrió
(2026-10-02); confirmado con `git log` que `scripts/capitulos_youtube.py`, `scripts/salidas.py`,
`scripts/config.py` y `references/contrato-montaje.md` no se han tocado desde entonces, y con
`grep` que `FFMETADATA1`/`capitulos-ffmpeg`/`formatear_capitulos_ffmpeg` siguen sin aparecer en
ningún módulo de `scripts/`. R-22 sigue siendo la única R-XX `PENDIENTE` de todo el roadmap, ya
especificada por completo en "Oleada v10" de `ROADMAP_PRODUCTO.md`, sin ningún cambio necesario en
su ficha ni en la cabecera/"Cola de producto" del documento (ambas siguen describiendo R-22 con
exactitud). **No se abre ninguna R-XX nueva en este ciclo:** mismo razonamiento que el ciclo de PM
del 2026-10-03 (ver `DECISIONES_TECNICAS.md`) — abrir una R-23 especulativa mientras R-22 sigue sin
implementar rompería el patrón de no tener más de una R-XX pendiente de código a la vez, sin ninguna
evidencia real (auditoría, `FEEDBACK.md`, grieta de arquitectura nueva) que lo justifique. Decisión
registrada en `DECISIONES_TECNICAS.md`; detalle completo de este ciclo en `HISTORIAL_SESIONES.md`.
Sin cambios en §3, §5, §6 ni §7. Este ciclo es de PM, no de Programador: no se ejecuta la
verificación de las cuatro redes.

**Última actualización anterior (2026-10-03, ciclo de Product Manager): reconfirmación de cola, sin
R-XX nueva abierta** (detalle completo abajo).

**Nota de arranque de la sesión anterior (ciclo de Product Manager, 2026-10-03):** sin incidencia. `git
status` limpio antes de tocar nada; `git checkout develop` dejó el contenedor en `HEAD` *detached*
(commits de la auditoría del mismo día ya fusionados en `develop`, descartable); `git pull origin
develop` resolvió en fast-forward limpio hasta `113ae14` (la auditoría 2026-10-03, que cierra `#27`
y reconfirma `#24` por cuarta vez), sin conflicto ni rama divergida. `pip install -r
requirements-dev.txt` limpio.

**Ciclo de Product Manager (2026-10-03): reconfirmación de cola, sin R-XX nueva abierta.**
Revisión de entrada (protocolo): registro de hallazgos de `auditoriacontinua.md` reconfirma un único
`ABIERTO`, `#24` (baja, proceso — la pregunta de gobernanza #11 de §6 sigue `(pendiente)` de
respuesta del dueño, decimoséptima pasada consecutiva esperándola; no es una R-XX, ya enrutada); la
auditoría del mismo día (narrativa "sin hallazgos nuevos") no aporta ningún hallazgo de
producto/arquitectura que convertir. `roadmap/FEEDBACK.md`: sigue sin ninguna entrada `nuevo`
(plantilla vacía) — el bloqueo #7 de §3 (grabar un curso completo) sigue abierto, así que no hay
historia de rodaje real que incorporar. §1 (fuente autoritativa): sin fila nueva para R-22 — el
ciclo de Programador que la implementa aún no ha corrido desde que se abrió (2026-10-02); R-22
sigue siendo la única R-XX `PENDIENTE` de todo el roadmap, ya especificada por completo en
"Oleada v10" de `ROADMAP_PRODUCTO.md`, sin ningún cambio necesario en su ficha. Releídos de nuevo
`scripts/capitulos_youtube.py`, `scripts/salidas.py` y `references/contrato-montaje.md` buscando
otra grieta de arquitectura del mismo tipo que abrió R-12 a R-22 (observación directa del PM, no
del auditor): ninguna encontrada — ni `capitulos-ffmpeg.txt` ni `FFMETADATA1` aparecen todavía en
ningún módulo de `scripts/` ni en `references/`, consistente con que R-22 sigue sin implementar.
**No se abre ninguna R-XX nueva en este ciclo**: abrir una R-23 especulativa mientras R-22 — la
única candidata legítima de este propio criterio — sigue sin wiring real implementado contradiría
el principio ya establecido el 2026-09-17/22/23 (no apilar R-XX sin evidencia real solo para no
dejar el ciclo "vacío"); además rompería por primera vez el patrón histórico de abrir como mucho
una R-XX pendiente de código a la vez. Decisión registrada en `DECISIONES_TECNICAS.md`; detalle
completo de este ciclo en `HISTORIAL_SESIONES.md`. Sin cambios en §3, §5, §6 ni §7; ningún cambio
necesario en `ROADMAP_PRODUCTO.md` (su cabecera y "Cola de producto" ya describen R-22 con
exactitud, sin latencia que corregir esta vez). Este ciclo es de PM, no de Programador: no se
ejecuta la verificación de las cuatro redes.

**Última actualización anterior (2026-10-02, ciclo de Product Manager): archiva Fase transversal
F-J (R-21) y abre R-22 (Oleada v10)** (detalle completo abajo).

**Nota de arranque de la sesión anterior (ciclo de Product Manager, 2026-10-02):** sin incidencia.
`git status` limpio antes de tocar nada; `git checkout develop` dejó el contenedor en `HEAD`
*detached* sin rama asociada (commits de reconfirmaciones del Programador ya fusionados en
`develop`, descartable); `git pull origin develop` resolvió en fast-forward limpio hasta `c0cb579`
(novena reconfirmación del Programador del mismo día), sin conflicto ni rama divergida. `pip
install -r requirements-dev.txt` limpio.

**Ciclo de Product Manager (2026-10-02): archiva Fase transversal F-J (R-21) y abre R-22 (Oleada
v10).** §1 (fuente autoritativa) ya registraba R-21 `COMPLETADA` desde el ciclo de Programador de
esta misma fecha (`commit` del cierre del hallazgo `#27`, confirmado estable en nueve
reconfirmaciones posteriores sin cambio de código); `ROADMAP_PRODUCTO.md` seguía describiéndola como
"EN CURSO" (mismo patrón que el hallazgo `#24`) — movida a `ROADMAP_HISTORICO.md` con su spec
completa, cabecera y "Cola de producto" corregidas. Registro de hallazgos de `auditoriacontinua.md`:
un único `ABIERTO`, `#24` (baja, proceso, la pregunta de gobernanza #11 de §6 sigue `(pendiente)`,
ajena al contenido de este roadmap) — `#27` ya no aparece como pendiente de código, solo pendiente de
que la próxima pasada del auditor actualice su propia fila a `RESUELTO`. `roadmap/FEEDBACK.md` sigue
sin ninguna entrada `nuevo`: no hay historia de rodaje real que incorporar este ciclo (el bloqueo #7
de §3 — grabar un curso completo — sigue abierto). Sin ninguna de las dos fuentes habituales
(auditoría, feedback) aportando una R-XX nueva, se abre **R-22** por la tercera fuente ya
establecida por el propio rol de PM: **grieta de arquitectura verificada sobre código ya
construido**, mismo criterio que abrió R-12 a R-20. Releído línea a línea
`scripts/capitulos_youtube.py` (`calcular_capitulos`, `formatear_capitulos_youtube`,
`validar_capitulos_youtube`) y `scripts/salidas.py::_generar_capitulos_youtube` antes de especificar
la tarea, no solo `references/contrato-montaje.md` (mismo rigor que R-20 aplicó para no repetir el
error de `#26`): el emparejamiento título↔escena y el tiempo acumulado real/estimado de cada
capítulo ya están calculados y probados desde R-07, pero solo se exponen en el formato de texto para
la descripción de YouTube — nunca en el formato `FFMETADATA1` nativo de ffmpeg que la fase de
montaje (T-33, la siguiente de esta skill) necesita para incrustar capítulos de verdad en el
`.mp4` final. Spec completa (campo aditivo `duracion_total_segundos` en `ResultadoCapitulos`,
formateador y validador nuevos, validación-antes-de-escribir desde el primer día para no repetir la
lección de `#27`/R-21) en `ROADMAP_PRODUCTO.md` §Oleada v10. Decisiones registradas en
`DECISIONES_TECNICAS.md`; detalle completo de este ciclo en `HISTORIAL_SESIONES.md`. Sin cambios en
§3 (bloqueos) ni §5 (P-XX); §6 sin novedad (la pregunta #11 sigue `(pendiente)`). Este ciclo es de
PM, no de Programador: no se añade fila nueva a §1 para R-22 (la añade el Programador al
implementarla, mismo patrón que R-12 en adelante) ni se ejecuta la verificación de las cuatro redes.

**Nota de arranque de la sesión anterior (novena reconfirmación del día tras R-21, ciclo de
Programador):** sin incidencia. `git status` limpio antes de tocar nada; sesión iniciada con `HEAD`
*detached*, sin rama asociada (advertencia de 22 commits de reconfirmaciones previas sin rama
asociada, descartable: son commits ya fusionados en `develop`, no trabajo perdido); `git checkout
develop` y `git pull origin develop` resolvieron en fast-forward limpio hasta `f3a0a7d` (la octava
reconfirmación de hoy), sin rama divergida. `pip install -r requirements-dev.txt` limpio.

**Ciclo de Programador de esa sesión: novena reconfirmación del día tras R-21** (implementada y
`COMPLETADA` en el ciclo `1e8d514`, reconfirmada antes en `0f392b3`, `945155f`, `842c300`, `698fc05`,
`787c4c4`, `cbf2e90`, `e5125ee` y `f3a0a7d`), sin novedad de código. Registro de hallazgos de
`auditoriacontinua.md` revisado antes de proceder: ningún `ABIERTO` de severidad alta (`#24` baja,
proceso — la pregunta #11 de §6 sigue `(pendiente)`; `#27`, media, cerrado en la práctica por la
implementación de R-21 — reverificado de nuevo en esta sesión leyendo directamente
`scripts/salidas.py::_generar_concat_ffmpeg` (invoca `validar_lista_concat_ffmpeg` antes de escribir
a disco), `scripts/tomas.py::_sanear_archivo_video` y `assets/reproductor/guion.js::sanearArchivoVideo`
(ambos puntos de entrada de `archivo_video` saneados): el código sigue intacto, pendiente solo de que
la próxima pasada del auditor actualice su propia fila del registro a `RESUELTO`, ninguno urgente por
§0.3). `roadmap/FEEDBACK.md` sin ninguna entrada `nuevo`; `mcp__github__list_issues`/
`list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero issues y cero PR abiertos. §1 ya no
tiene ninguna R-XX/T-XX `PENDIENTE` (R-21 es la última, `COMPLETADA`): cola vacía, sin tarea de código
que ejecutar. Verificación propia completa: `mypy`/`ruff` en verde sin hallazgos (70 archivos), 619
tests (`pytest`) en verde, dieciséis etapas OK en `verificar_salidas.py --fixture`. Las cuatro redes
en verde. Nota sin acción, mismo patrón que motivó `#24`: `ROADMAP_PRODUCTO.md` sigue describiendo
R-21 como la única `PENDIENTE` en su prosa de "Cola de producto" pese a que este §1 ya la registra
`COMPLETADA` — no se corrige desde aquí (la pregunta #11 de §6 sigue `(pendiente)` de respuesta del
dueño); se deja constancia para el próximo ciclo de Product Manager, que es quien escribe ese
documento.

**Última actualización anterior (ciclo de Product Manager, 2026-10-01): archiva Oleada v9 (R-20) y
abre R-21** (Fase transversal F-J) desde el hallazgo `#27` de `auditoriacontinua.md` (detalle en la nota
de arranque de esa sesión, más abajo).

**Última actualización anterior (R-20, implementada en el ciclo previo):** `scripts/reproductor.py::_indicaciones_ancladas_por_indice` (R-12) se divide: el
algoritmo de anclaje (máximo bloque de respiración cuyo `linea_fin` precede a la indicación, o el
primero si no hay ninguno) se extrae a la función pública `anclar_indicaciones_a_bloques` (mismo
patrón que R-19 extrajo `tomas.toma_buena` de `duracion_toma_buena`), devolviendo la indicación
cruda por índice de bloque en vez del texto ya formateado; `_indicaciones_ancladas_por_indice` queda
como envoltorio de una línea que aplica el formato `Pantalla:`/`Nota:` — comportamiento del
reproductor intacto. `scripts/pptx.py` reutiliza esa función nueva: `Tarjeta` gana
`indicaciones_ancladas` (dataclass `IndicacionAnclada`: `texto`, `es_nota_interna`,
`instante_estimado_segundos`), mismo conjunto que `indicaciones_pantalla`/`notas_internas` sin
perder ni duplicar ninguna (invariante (a) extendido). El instante se calcula relativo al inicio de
la escena en `_indicaciones_ancladas_de_escena` y se convierte a absoluto del vídeo en
`_con_limites_absolutos` (R-16), sumando el mismo acumulado real-o-estimado que ya usa para
`inicio_segundos`/`fin_segundos` — sin ninguna fuente de tiempo nueva. Una escena sin ningún bloque
de locución (sin ejemplo en los guiones reales, pero contemplada por `validar_tarjetas`) ancla cada
indicación al inicio de la escena en vez de perderla. `--para-terceros` omite las notas internas
también aquí, con el mismo criterio que `notas_internas`. Cambio puramente aditivo: `version_contrato`
no sube, sin campo nuevo de `Configuracion` ni migración de `estado.json`. 7 tests nuevos (606→613),
incluido uno que compara el instante exacto de `tarjetas.json` contra el que calcula el reproductor
para la misma indicación del mismo guion (sin toma real de por medio, los dos acumulados coinciden
bit a bit — criterio de aceptación literal: "mismo bloque ancla, dos consumidores"). Cuatro redes en
verde, incluida la validación de `tarjetas.json` de `verificar_salidas.py --fixture` (la clave nueva
pasa por `validar_tarjetas` sin cambios propios en el validador, mismo rigor que el resto de listas
de indicaciones). `DEVELOPERS.md`, `SKILL.md` y `references/contrato-tarjetas.md`/
`contrato-montaje.md` actualizados. Decisiones registradas en `DECISIONES_TECNICAS.md`. Sin cambios
en §3 (bloqueos) ni §5 (P-XX); ningún hallazgo de `auditoriacontinua.md` es de severidad alta
(`#24` baja, `#27` media, ninguno urgente por §0.3); §1 pasa `R-20` a `COMPLETADA`.

**Nota de arranque de la sesión anterior (ciclo de Product Manager, 2026-10-01):** sin incidencia.
`git status` limpio antes de tocar nada; `git checkout develop` dejó el contenedor en `HEAD`
*detached* 11 commits por detrás de `origin/develop` (reconfirmaciones del Programador ya superadas);
`git pull origin develop` resolvió con fast-forward trivial (`51e38da..8e155bf`) sin conflicto ni
pérdida — ningún `git reset --hard` ni rama auxiliar necesarios. `pip install -r
requirements-dev.txt` limpio.

**Ciclo de Product Manager (2026-10-01): archiva Oleada v9 (R-20) y abre R-21 (Fase transversal
F-J).** §1 (fuente autoritativa) ya registraba R-20 `COMPLETADA` desde el 2026-09-30, tras nueve
reconfirmaciones del Programador sin cambio de código; `ROADMAP_PRODUCTO.md` seguía describiéndola
como "EN CURSO"/`PENDIENTE` (mismo patrón que el hallazgo `#24`) — movida a `ROADMAP_HISTORICO.md`
con su spec completa, cabecera y "Cola de producto" corregidas. Registro de hallazgos de
`auditoriacontinua.md`: dos `ABIERTO`, ninguno de severidad alta — `#24` (baja, proceso, la pregunta
de gobernanza #11 de §6 sigue `(pendiente)`, ajena al contenido de este roadmap) y `#27` (media,
2026-10-01, reproducido con código por el auditor: `scripts/salidas.py::_generar_concat_ffmpeg` no
invoca `concat_ffmpeg.validar_lista_concat_ffmpeg` antes de escribir a disco, y `archivo_video` no se
sanea en sus dos puntos de entrada). `#27` es el único hallazgo técnico de esta pasada: se convierte
en **R-21** (Fase transversal F-J, `origen: auditoría #27`), spec completa en `ROADMAP_PRODUCTO.md`
§Fase transversal F-J. `roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo`. Decisiones registradas
en `DECISIONES_TECNICAS.md`; detalle completo de este ciclo en `HISTORIAL_SESIONES.md` (sesión 58).
Sin cambios en §3 ni §5; §6 sin novedad (la pregunta #11 sigue `(pendiente)`). Este ciclo es de PM,
no de Programador: no se añade fila nueva a §1 para R-21 (la añade el Programador al implementarla,
mismo patrón que R-19/R-20) ni se ejecuta la verificación de las cuatro redes.

**Última actualización anterior (resumen; detalle completo en `HISTORIAL_SESIONES.md` y
`DECISIONES_TECNICAS.md`, no repetido aquí para no seguir engordando este documento):**
- 2026-10-02, ciclo de Programador: novena reconfirmación del día tras R-21, sin novedad de código.
  Ver el párrafo de "Última actualización anterior (novena reconfirmación...)" arriba para el
  detalle completo.
- 2026-10-02, ciclo de Programador: octava reconfirmación del día tras R-21, sin novedad de código.
  Ver el párrafo de "Última actualización anterior (octava reconfirmación...)" arriba para el
  detalle completo.
- 2026-10-02, ciclo de Programador: séptima reconfirmación del día tras R-21, sin novedad de código.
  Ver el párrafo de "Última actualización anterior (séptima reconfirmación...)" arriba para el
  detalle completo.
- 2026-10-02, ciclo de Programador: sexta reconfirmación del día tras R-21, sin novedad de código.
  Ver el párrafo de "Última actualización anterior (sexta reconfirmación...)" arriba para el
  detalle completo.
- 2026-10-02, ciclo de Programador: quinta reconfirmación del día tras R-21, sin novedad de código.
  Ver el párrafo de "Última actualización anterior (quinta reconfirmación...)" arriba para el
  detalle completo.
- 2026-10-02, ciclo de Programador: cuarta reconfirmación del día tras R-21, sin novedad de código.
  Ver el párrafo de "Última actualización anterior (cuarta reconfirmación...)" arriba para el
  detalle completo.
- 2026-10-02, ciclo de Programador: tercera reconfirmación del día tras R-21, sin novedad de código.
  Ver el párrafo de "Última actualización anterior (tercera reconfirmación...)" arriba para el
  detalle completo.
- 2026-10-02, ciclo de Programador: segunda reconfirmación del día tras R-21, sin novedad de código.
  Ver el párrafo de "Última actualización anterior (segunda reconfirmación...)" arriba para el
  detalle completo.
- 2026-10-02, ciclo de Programador: primera reconfirmación del día tras R-21, sin novedad de código.
- 2026-10-02, ciclo de Programador: R-21 implementada y `COMPLETADA` (Fase transversal F-J). Ver el
  párrafo de "Última actualización anterior (R-21...)" arriba para el detalle técnico completo.
- 2026-10-01, ciclo de Product Manager: archiva Oleada v9 (R-20) a `ROADMAP_HISTORICO.md` y abre
  R-21 (Fase transversal F-J) desde el hallazgo `#27` de `auditoriacontinua.md` (media, validación de
  `concat-ffmpeg.txt` nunca invocada en la ruta real de generación, `archivo_video` sin sanear).
  Detalle completo arriba (ver "Ciclo de Product Manager (2026-10-01)") y en `HISTORIAL_SESIONES.md`
  (sesión 58).
- 2026-10-01, ciclo de Programador: novena reconfirmación tras R-20, tras la octava de hoy
  (`ae3107a`), sin novedad de código. Verificación propia completa: `mypy`/`ruff` en verde sin
  hallazgos, 613 tests (`pytest`) en verde, dieciséis etapas OK en `verificar_salidas.py --fixture`.
  `auditoriacontinua.md` con dos `ABIERTO`, ninguno de severidad alta (`#24` baja, proceso; `#27`
  media, robustez de validación de `concat_ffmpeg.py`). `roadmap/FEEDBACK.md` sin ninguna entrada
  `nuevo`; cero issues y cero PR abiertos en GitHub. Nota sin acción, mismo patrón que motivó `#24`:
  la prosa de "Cola de producto" de `ROADMAP_PRODUCTO.md` seguía describiendo R-20 como
  "EN CURSO"/`PENDIENTE` pese a que este §1 ya la registraba `COMPLETADA` — corregido por el ciclo de
  PM siguiente (ver arriba).
- 2026-10-01, ciclo de Programador: octava reconfirmación tras R-20, sin novedad de código.
- 2026-10-01, ciclo de Programador: séptima reconfirmación tras R-20, sin novedad de código.
- 2026-10-01, ciclo de Programador: sexta reconfirmación tras R-20, sin novedad de código.
- 2026-10-01, ciclo de Programador: quinta reconfirmación tras R-20, sin novedad de código.
- 2026-10-01, ciclo de Programador: cuarta reconfirmación tras R-20, sin novedad de código.
- 2026-10-01, ciclo de Programador: tercera reconfirmación tras R-20, sin novedad de código.
- 2026-10-01, ciclo de Programador: segunda reconfirmación tras R-20, sin novedad de código.
- 2026-10-01, ciclo de Programador: primera reconfirmación tras R-20, sin novedad de código.
- 2026-10-01, ciclo de Programador: R-20 implementada y `COMPLETADA` (Oleada v9). Ver el párrafo de
  "Última actualización anterior (R-20...)" arriba para el detalle técnico completo.
- 2026-09-30, ciclo de Product Manager: archiva R-19/Oleada v8 a `ROADMAP_HISTORICO.md` y corrige la
  prosa de `ROADMAP_PRODUCTO.md` que seguía describiendo R-19 como `PENDIENTE` pese a que §1 ya la
  registraba `COMPLETADA` (mismo patrón de latencia que el hallazgo `#24`). Atiende el hallazgo `#26`
  de `auditoriacontinua.md` (media, gobernanza del propio PM): el ciclo del 2026-09-29 había
  presentado una frase fija del encargo de esta misma rutina como "instrucción directa del dueño",
  cuando `list_triggers` confirma que es texto sin cambios desde 2026-08-31 — R-19 no se revierte
  (diseño sólido y aditivo) pero `ROADMAP_PRODUCTO.md` corrige la premisa a la grieta de arquitectura
  ya razonada el 2026-09-21. Deja escrito en `DECISIONES_TECNICAS.md` el criterio para futuras
  aperturas: las tres fuentes ya establecidas (auditoría, `FEEDBACK.md`, grieta de arquitectura
  verificada) bastan por sí solas, sin apoyarse en el encargo estable de la rutina. **Abre R-20**
  (Oleada v9): `tarjetas.json` ganará `indicaciones_ancladas`, reutilizando el anclaje que
  `reproductor.py` (R-12) ya calcula para la cue en vivo — mismo patrón de apertura que R-12 a R-18
  (grieta de arquitectura verificada). Spec completa en `ROADMAP_PRODUCTO.md` §Oleada v9. Ciclo de PM:
  no se ejecuta la verificación de las cuatro redes.
- 2026-09-30, ciclo de Programador: R-19 implementada y COMPLETADA (Oleada v8). `archivo_video` por
  toma anotable con `V`/`v` durante la grabación o editable después desde el índice sin volver a
  grabar; `scripts/concat_ffmpeg.py` (módulo nuevo) genera `concat-ffmpeg.txt`, la lista de
  concatenación del demuxer `concat` de ffmpeg, sexta opción del selector de salidas (T-30). 23 tests
  nuevos (583→606). Cuatro redes en verde, incluidas dos etapas nuevas en `verificar_salidas.py
  --fixture` (dieciséis en total). Verificado también con Playwright/Chromium real. Detalle completo
  en `HISTORIAL_SESIONES.md`/`DECISIONES_TECNICAS.md`.
- 2026-09-30, décima sesión del día con el mismo patrón de arranque: contenedor en `HEAD` *detached*
  con la rama local divergida 50 commits sin ancestro común de `origin/develop`, resuelta con `git
  reset --hard origin/develop` sin riesgo de pérdida (commits locales descartados eran solo
  reconfirmaciones vacías ya superadas). Detalle completo en la entonces "nota de arranque de esta
  sesión", ahora superada por la de arriba.
- 2026-09-30, ciclo de Programador: novena reconfirmación tras R-19, tras la octava de hoy
  (`af4d09b`), sin novedad de código. Verificación propia completa: `mypy`/`ruff` en verde (70
  archivos, sin hallazgos), 606 tests (`pytest`) en verde, dieciséis etapas OK en
  `verificar_salidas.py --fixture`. `auditoriacontinua.md` mantiene los mismos dos `ABIERTO`,
  ninguno de severidad alta ni urgente por §0.3: `#24` (baja, proceso, esperando la respuesta del
  dueño a la pregunta #11 de §6) y `#26` (media, gobernanza de la apertura de R-19, ajena al
  código). `roadmap/FEEDBACK.md` sin ninguna entrada `nuevo`; `mcp__github__list_issues`/
  `list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero issues y cero PR abiertos. Nota sin
  acción, mismo patrón que motivó `#24`: la prosa de "Cola de producto" de `ROADMAP_PRODUCTO.md`
  sigue describiendo R-19 como `PENDIENTE` pese a que este §1 ya la registra `COMPLETADA` — no se
  corrige desde aquí (la pregunta #11 de §6, que decidiría si el Programador puede corregirla por
  su cuenta, sigue `(pendiente)` de respuesta del dueño). Divergencia de arranque repetida, misma
  magnitud que la sesión anterior (50 commits sin ancestro común a cada lado), resuelta con `git
  reset --hard origin/develop`; detalle en la nota de arranque de esta sesión, más arriba.
- 2026-09-30, ciclo de Programador: octava reconfirmación tras R-19, tras la séptima de hoy
  (`aec35da`), sin novedad de código. Verificación propia completa: `mypy`/`ruff` en verde (70
  archivos, sin hallazgos), 606 tests (`pytest`) en verde, dieciséis etapas OK en
  `verificar_salidas.py --fixture`. `auditoriacontinua.md` mantiene los mismos dos `ABIERTO`,
  ninguno de severidad alta ni urgente por §0.3: `#24` (baja, proceso, esperando la respuesta del
  dueño a la pregunta #11 de §6) y `#26` (media, gobernanza de la apertura de R-19, ajena al
  código). `roadmap/FEEDBACK.md` sin ninguna entrada `nuevo`; `mcp__github__list_issues`/
  `list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero issues y cero PR abiertos. Nota sin
  acción, mismo patrón que motivó `#24`: la prosa de "Cola de producto" de `ROADMAP_PRODUCTO.md`
  sigue describiendo R-19 como `PENDIENTE` pese a que este §1 ya la registra `COMPLETADA` — no se
  corrige desde aquí (la pregunta #11 de §6, que decidiría si el Programador puede corregirla por
  su cuenta, sigue `(pendiente)` de respuesta del dueño). Divergencia de arranque más marcada de lo
  habitual (50 commits sin ancestro común a cada lado), resuelta con `git reset --hard
  origin/develop`; detalle en la nota de arranque de esta sesión, más arriba.
- 2026-09-30, ciclo de Programador: séptima reconfirmación tras R-19, tras la sexta de hoy
  (`7f160cb`), sin novedad de código. Verificación propia completa: `mypy`/`ruff` en verde, 606 tests
  (`pytest`) en verde, dieciséis etapas OK en `verificar_salidas.py --fixture`. `auditoriacontinua.md`
  mantiene los mismos dos `ABIERTO`, ninguno de severidad alta ni urgente por §0.3: `#24` (baja,
  proceso, esperando la respuesta del dueño a la pregunta #11 de §6, sin pasada nueva desde la ya
  registrada) y `#26` (media, gobernanza de la apertura de R-19, ajena al código). `roadmap/FEEDBACK.md`
  sin ninguna entrada `nuevo`; `mcp__github__list_issues`/`list_pull_requests` sobre
  `janosolerdiaz/telePrompter`: cero issues y cero PR abiertos.
- 2026-09-30, ciclo de Programador: sexta reconfirmación tras R-19, tras la quinta de hoy
  (`431b304`), sin novedad de código. Verificación propia completa: `mypy`/`ruff` en verde, 606 tests
  (`pytest`) en verde, dieciséis etapas OK en `verificar_salidas.py --fixture`. `auditoriacontinua.md`
  mantiene los mismos dos `ABIERTO`, ninguno de severidad alta ni urgente por §0.3: `#24` (baja,
  proceso, esperando la respuesta del dueño a la pregunta #11 de §6, sin pasada nueva desde la ya
  registrada) y `#26` (media, gobernanza de la apertura de R-19, ajena al código). `roadmap/FEEDBACK.md`
  sin ninguna entrada `nuevo`; `mcp__github__list_issues`/`list_pull_requests` sobre
  `janosolerdiaz/telePrompter`: cero issues y cero PR abiertos.
- 2026-09-30, ciclo de Programador: quinta reconfirmación tras R-19, tras la cuarta de hoy
  (`1e3175a`), sin novedad de código. Verificación propia completa: `mypy`/`ruff` en verde, 606 tests
  (`pytest`) en verde, dieciséis etapas OK en `verificar_salidas.py --fixture`. `auditoriacontinua.md`
  mantiene los mismos dos `ABIERTO`, ninguno de severidad alta ni urgente por §0.3: `#24` (baja,
  proceso, esperando la respuesta del dueño a la pregunta #11 de §6, sin pasada nueva desde la ya
  registrada) y `#26` (media, gobernanza de la apertura de R-19, ajena al código). `roadmap/FEEDBACK.md`
  sin ninguna entrada `nuevo`; `mcp__github__list_issues`/`list_pull_requests` sobre
  `janosolerdiaz/telePrompter`: cero issues y cero PR abiertos.
- 2026-09-30, ciclo de Programador: cuarta reconfirmación tras R-19, tras la tercera de hoy
  (`9455322`), sin novedad de código. `auditoriacontinua.md` mantiene los mismos dos `ABIERTO`,
  ninguno de severidad alta ni urgente por §0.3: `#24` (baja, proceso, esperando la respuesta del
  dueño a la pregunta #11 de §6, sin pasada nueva desde la ya registrada) y `#26` (media, gobernanza
  de la apertura de R-19, ajena al código). `roadmap/FEEDBACK.md` sin ninguna entrada `nuevo`;
  `mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero issues y
  cero PR abiertos. Cuatro redes en verde (606 tests, dieciséis etapas OK en
  `verificar_salidas.py --fixture`).
- 2026-09-30, ciclo de Programador: tercera reconfirmación tras R-19, tras la segunda de hoy
  (`b2a6676`), sin novedad de código. `auditoriacontinua.md` mantiene los mismos dos `ABIERTO`,
  ninguno de severidad alta ni urgente por §0.3: `#24` (baja, proceso, esperando la respuesta del
  dueño a la pregunta #11 de §6, sin pasada nueva desde la ya registrada) y `#26` (media, gobernanza
  de la apertura de R-19, ajena al código). `roadmap/FEEDBACK.md` sin ninguna entrada `nuevo`;
  `mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero issues y
  cero PR abiertos. Cuatro redes en verde (606 tests, dieciséis etapas OK en
  `verificar_salidas.py --fixture`).
- 2026-09-30, ciclo de Programador: segunda reconfirmación tras R-19, tras la primera de hoy
  (`e684987`), sin novedad de código. `auditoriacontinua.md` mantiene dos `ABIERTO`, ninguno de
  severidad alta ni urgente por §0.3: `#24` (baja, proceso, catorce pasadas de auditoría esperando la
  respuesta del dueño a la pregunta #11 de §6, sin pasada nueva desde la del 2026-09-30 ya
  registrada) y `#26` (media, gobernanza de la apertura de R-19,
  ajena al código). `roadmap/FEEDBACK.md` sin ninguna entrada `nuevo`; `mcp__github__list_issues`/
  `list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero issues y cero PR abiertos. Cuatro
  redes en verde (606 tests, dieciséis etapas OK en `verificar_salidas.py --fixture`).
- 2026-09-30, ciclo de Programador: primera reconfirmación tras R-19 (implementada y COMPLETADA en
  el ciclo anterior, `5205549`), sin novedad de código. `auditoriacontinua.md` mantiene dos `ABIERTO`,
  ninguno de severidad alta ni urgente por §0.3: `#24` (baja, proceso, catorce pasadas de auditoría
  esperando la respuesta del dueño a la pregunta #11 de este §6) y `#26` (media, gobernanza de la
  apertura de R-19, ajena al código). Nota sin acción: la prosa de "Cola de producto" de
  `ROADMAP_PRODUCTO.md` sigue describiendo R-19 como `PENDIENTE` pese a que este §1 ya la registra
  `COMPLETADA` — mismo patrón que motivó `#24`; se deja constancia para el próximo ciclo de PM
  (quien escribe ese documento), sin corregirla desde aquí. `roadmap/FEEDBACK.md` sin ninguna entrada
  `nuevo`; `mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero
  issues y cero PR abiertos. Cuatro redes en verde (606 tests, dieciséis etapas OK en
  `verificar_salidas.py --fixture`).
- 2026-09-29, ciclo de Product Manager: se abre R-19 (Oleada v8), la primera R-XX nueva desde R-18
  (2026-09-17) tras quince ciclos de PM consecutivos reconfirmando la cola vacía. Spec completa en
  `ROADMAP_PRODUCTO.md` §Oleada v8. Corrige también el hallazgo `#25` de `auditoriacontinua.md`
  (baja, prosa) — cifra de "pasadas de auditoría... pregunta #11" de `quince` a **trece**. `#24`
  sigue `ABIERTO`, enrutado a la pregunta #11 de §6, *(pendiente)* de respuesta del dueño.
- 2026-09-29, ciclo de Programador: décima reconfirmación del día, tras la novena de hoy
  (`0d3fadd`), sin novedad de código. Verificación propia: clon *shallow* en *detached HEAD*
  resuelto (`git fetch --unshallow` + `git merge --ff-only origin/develop`, sin pérdida de trabajo
  local); cuatro redes en verde (583 tests, catorce etapas OK); `mcp__github__list_issues`/
  `list_pull_requests` sin issues ni PR abiertos.
- 2026-09-29, ciclo de Programador: novena reconfirmación del día, tras la octava de hoy
  (`09fd0e9`), sin novedad de código.
- 2026-09-29, ciclo de Programador: octava reconfirmación del día, tras la séptima de hoy
  (`3e272f6`), sin novedad de código.
- 2026-09-29, ciclo de Programador: séptima reconfirmación del día, tras la sexta de hoy
  (`f20002c`), sin novedad de código.
- 2026-09-29, ciclo de Programador: sexta reconfirmación del día, tras la quinta de hoy
  (`91cfc1d`), sin novedad de código.
- 2026-09-29, ciclo de Programador: quinta reconfirmación del día, tras la cuarta de hoy
  (`0ab65df`), sin novedad de código.
- 2026-09-29, ciclo de Programador: cuarta reconfirmación del día, tras la tercera de hoy
  (`c8c9be5`), sin novedad de código.
- 2026-09-29, ciclo de Programador: tercera reconfirmación del día, tras la segunda de hoy
  (`bf9c45e`), sin novedad de código.
- 2026-09-29, ciclo de Programador: segunda reconfirmación del día, tras la primera de hoy
  (`c59df89`), sin novedad de código.
- 2026-09-29, ciclo de Programador: primera reconfirmación del día, tras la decimosexta auditoría en
  profundidad (`d14776a`, un hallazgo nuevo de proceso, `#25`) y el decimoquinto ciclo de PM
  consecutivo sin apertura (`de45611`), sin novedad de código.
- 2026-09-28, ciclo de Product Manager: reconfirmación de cola vacía, sin R-XX nueva (decimoquinto
  ciclo de PM consecutivo sin apertura).
- 2026-09-28, ciclo de Programador: vigésima reconfirmación del día, tras la decimonovena de hoy
  (`92c7f46`), sin novedad de código.
- 2026-09-28, ciclo de Programador: decimonovena reconfirmación del día, tras la decimoctava de
  hoy (`3b1f3fe`), sin novedad de código.
- 2026-09-28, ciclo de Programador: decimoctava reconfirmación del día, tras la decimoséptima de
  hoy (`f774577`), sin novedad de código.
- 2026-09-28, ciclo de Programador: decimoséptima reconfirmación del día, tras la decimosexta de
  hoy (`7ac67d4`), sin novedad de código.
- 2026-09-28, ciclo de Programador: decimosexta reconfirmación del día, tras la decimoquinta de
  hoy (`41f719f`), sin novedad de código.
- 2026-09-28, ciclo de Programador: decimoquinta reconfirmación del día, tras la decimocuarta de
  hoy (`e881f58`), sin novedad de código.
- 2026-09-28, ciclo de Programador: decimocuarta reconfirmación del día, tras la decimotercera de
  hoy (`aa7a6f2`), sin novedad de código.
- 2026-09-28, ciclo de Programador: decimotercera reconfirmación del día, tras la duodécima de hoy
  (`c08cbcb`), sin novedad de código.
- 2026-09-28, ciclo de Programador: duodécima reconfirmación del día, tras la undécima de hoy
  (`8530ac2`), sin novedad de código.
- 2026-09-28, ciclo de Programador: undécima reconfirmación del día, tras la decimoquinta auditoría
  en profundidad (`f694a29`) y el decimocuarto ciclo de PM consecutivo sin apertura (`b4912c4`), sin
  novedad de código.
- 2026-09-27, ciclo de Product Manager: reconfirmación de cola vacía, sin R-XX nueva (decimocuarto
  ciclo de PM consecutivo sin apertura).
- 2026-09-27, ciclo de Auditoría: decimocuarta pasada consecutiva sin cambios de código, cero
  hallazgos nuevos. `#24` (baja, de proceso) reconfirmado `ABIERTO`, pendiente exclusivamente de la
  respuesta del dueño a la pregunta #11 de §6 (once pasadas consecutivas esperándola).
- 2026-09-26, ciclo de Product Manager: reconfirmación de cola vacía, sin R-XX nueva (decimotercer
  ciclo de PM consecutivo sin apertura).
- 2026-09-25, ciclo de Auditoría: decimotercera pasada consecutiva sin cambios de código, cero
  hallazgos nuevos. `#24` (baja, de proceso) reconfirmado `ABIERTO`, pendiente exclusivamente de la
  respuesta del dueño a la pregunta #11 de §6.
- 2026-09-25, ciclo de Product Manager: reconfirmación de cola vacía, sin R-XX nueva (duodécimo
  ciclo de PM consecutivo sin apertura).
- 2026-09-25, ciclo de Programador: décima reconfirmación del día, tras la novena de hoy
  (`4a1e7ab`), sin novedad de código.
- 2026-09-25, ciclo de Programador: novena reconfirmación del día, tras la octava de hoy
  (`630482d`), sin novedad de código.
- 2026-09-25, ciclo de Programador: octava reconfirmación del día, tras la séptima de hoy
  (`78075a2`), sin novedad de código.
- 2026-09-25, ciclo de Programador: séptima reconfirmación del día, tras la sexta de hoy
  (`ea04ef7`), sin novedad de código.
- 2026-09-25, ciclo de Programador: sexta reconfirmación del día, tras la quinta de hoy
  (`f91275a`), sin novedad de código.
- 2026-09-25, ciclo de Programador: quinta reconfirmación del día, tras la cuarta de hoy
  (`6a4dc53`), sin novedad de código.
- 2026-09-25, ciclo de Programador: cuarta reconfirmación del día, tras la tercera de hoy
  (`dc94f78`), sin novedad de código.
- 2026-09-25, ciclo de Programador: tercera reconfirmación del día, tras la segunda de hoy
  (`ef06378`), sin novedad de código.
- 2026-09-25, ciclo de Programador: segunda reconfirmación del día, tras la primera de hoy
  (`6e5c795`), sin novedad de código.
- 2026-09-25, ciclo de Programador: primera reconfirmación del día, tras la duodécima auditoría en
  profundidad (`312fe75`) y el undécimo ciclo de PM consecutivo sin apertura (`0af6e69`), sin
  novedad de código.
- 2026-09-25, ciclo de Auditoría: duodécima pasada consecutiva sin cambios de código, cero hallazgos
  nuevos. `#24` (baja, de proceso) reconfirmado `ABIERTO`, pendiente exclusivamente de la respuesta
  del dueño a la pregunta #11 de §6.
- 2026-09-24, ciclo de Product Manager: reconfirmación de cola vacía, sin R-XX nueva (undécimo ciclo
  de PM consecutivo sin apertura).
- 2026-09-24, ciclo de Programador: décima reconfirmación del día, tras la novena de hoy
  (`5d7168e`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-24, ciclo de Programador: novena reconfirmación del día, tras la octava de hoy
  (`d1c6751`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-24, ciclo de Programador: octava reconfirmación del día, tras la séptima de hoy
  (`1b60b67`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-24, ciclo de Programador: séptima reconfirmación del día, tras la sexta de hoy
  (`7f97666`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-24, ciclo de Programador: sexta reconfirmación del día, tras la quinta de hoy
  (`c3c8b93`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-24, ciclo de Programador: quinta reconfirmación del día, tras la cuarta de hoy
  (`5e16a5a`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-24, ciclo de Programador: cuarta reconfirmación del día, tras la tercera de hoy
  (`71bec46`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-24, ciclo de Programador: tercera reconfirmación del día, tras la segunda de hoy
  (`33c773d`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-24, ciclo de Programador: segunda reconfirmación del día, tras la primera de hoy
  (`7be1648`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-24, ciclo de Programador: primera reconfirmación del día, tras la undécima auditoría en
  profundidad (`6341558`) y el décimo ciclo de PM consecutivo sin apertura (`5f7b071`), sin novedad
  de código. Cuatro redes en verde (583 tests).
- 2026-09-23, ciclo de Product Manager: reconfirmación de cola vacía, sin R-XX nueva (décimo ciclo
  de PM consecutivo sin apertura).
- 2026-09-23, ciclo de Programador: décima reconfirmación del día, tras la novena de hoy
  (`b9858fb`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-23, ciclo de Programador: novena reconfirmación del día, tras la octava de hoy
  (`979e821`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-23, ciclo de Programador: octava reconfirmación del día, tras la séptima de hoy
  (`c2cf6bb`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-23, ciclo de Programador: séptima reconfirmación del día, tras la sexta de hoy
  (`df16dd8`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-23, ciclo de Programador: sexta reconfirmación del día, tras la quinta de hoy
  (`9e9e7fa`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-23, ciclo de Programador: quinta reconfirmación del día, tras la cuarta de hoy
  (`6d2ff43`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-23, ciclo de Programador: cuarta reconfirmación del día, tras la tercera de hoy
  (`20a7f21`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-23, ciclo de Programador: tercera reconfirmación del día, tras la segunda de hoy
  (`f408b3d`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-23, ciclo de Programador: segunda reconfirmación del día, tras la primera de hoy
  (`a5a45b1`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-23, ciclo de Programador: primera reconfirmación del día, tras la auditoría en
  profundidad de hoy (`3a58f1c`, décima pasada consecutiva sin cambios de código) y el noveno
  ciclo de PM consecutivo sin apertura (`3ed68e4`), sin novedad de código. Cuatro redes en verde
  (583 tests).
- 2026-09-22, ciclo de Product Manager: reconfirmación de cola vacía, sin R-XX nueva (noveno ciclo
  de PM consecutivo sin apertura). Verificación propia por `grep` del hilo
  `tomas_por_escena`/`EstadoProyecto.tomas` en los seis módulos que R-18 conecta, sin grieta nueva.
- 2026-09-22, ciclo de Programador: décima reconfirmación del día, tras la novena de esta mañana
  (`5e52707`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-22, ciclo de Programador: novena reconfirmación del día, tras la octava de esta mañana
  (`a4936ea`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-22, ciclo de Programador: octava reconfirmación del día, tras la séptima de esta mañana
  (`aa9aa23`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-22, ciclo de Programador: séptima reconfirmación del día, tras la sexta de esta mañana
  (`5f94051`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-22, ciclo de Programador: sexta reconfirmación del día, tras la quinta de esta mañana
  (`c231141`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-22, ciclo de Programador: quinta reconfirmación del día, tras la cuarta de esta mañana
  (`e5c77f5`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-22, ciclo de Programador: cuarta reconfirmación del día, tras la tercera de esta mañana
  (`9c8bfb0`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-22, ciclo de Programador: tercera reconfirmación del día, tras la segunda de esta mañana
  (`7b34ee8`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-22, ciclo de Programador: segunda reconfirmación del día, tras la primera de esta mañana
  (`8aa846b`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-22, ciclo de Programador: primera reconfirmación del día, tras la novena auditoría en
  profundidad (`f1d1728`) y el noveno ciclo de PM consecutivo sin apertura (`2e214d1`), sin novedad
  de código. Cuatro redes en verde (583 tests).
- 2026-09-21, ciclo de Product Manager: reconfirmación de cola vacía, sin R-XX nueva (octavo ciclo
  de PM consecutivo sin apertura). Candidata futura (toma↔archivo de vídeo + concatenación ffmpeg)
  registrada en `ROADMAP_PRODUCTO.md`/`DECISIONES_TECNICAS.md`, no abierta como R-XX.
- 2026-09-21, ciclo de Programador: décima reconfirmación del día, tras la novena de esta mañana
  (`f247522`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-21, ciclo de Programador: novena reconfirmación del día, tras la octava de esta mañana
  (`1665900`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-21, ciclo de Programador: octava reconfirmación del día, tras la séptima de esta mañana
  (`aa74cd2`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-21, ciclo de Programador: séptima reconfirmación del día, tras la sexta de esta mañana
  (`3d3ec38`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-21, ciclo de Programador: sexta reconfirmación del día, tras la quinta de esta mañana
  (`3284211`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-21, ciclo de Programador: quinta reconfirmación del día, tras la cuarta de esta mañana
  (`570fd81`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-21, ciclo de Programador: cuarta reconfirmación del día, tras la tercera de esta mañana
  (`410d657`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-21, ciclo de Programador: tercera reconfirmación del día, tras la segunda de esta mañana
  (`bb6779d`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-21, ciclo de Programador: segunda reconfirmación del día, tras la de esta mañana
  (`abd4129`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-21, ciclo de Programador: primera reconfirmación tras el fin de semana, sin novedad de
  código (solo ciclos de PM el 2026-09-19 y el 2026-09-20, sin cron de Programador en
  sábado/domingo). Cuatro redes en verde (583 tests).
- 2026-09-20, ciclo de Product Manager: reconfirmación de cola vacía, sin R-XX nueva (séptimo ciclo
  de PM consecutivo sin apertura).
- 2026-09-19, ciclo de Product Manager: reconfirmación de cola vacía, sin R-XX nueva.
- 2026-09-18, ciclo de Product Manager: reconfirmación de cola vacía, sin R-XX nueva.
- 2026-09-18, ciclo de Programador: décima reconfirmación tras el archivado de R-18 (PM) y la
  auditoría en profundidad, sin novedad de código. Cuatro redes en verde (583 tests). Único
  `ABIERTO` de `auditoriacontinua.md`: `#24` (baja, de proceso).
- 2026-09-18, ciclo de Programador: novena reconfirmación tras R-18 y la auditoría en profundidad,
  sin novedad de código. Cuatro redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`:
  `#24` (baja, de proceso).
- 2026-09-18, ciclo de Programador: octava reconfirmación tras R-18 y la auditoría en profundidad,
  sin novedad de código. Cuatro redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`:
  `#24` (baja, de proceso).
- 2026-09-18, ciclo de Programador: séptima reconfirmación tras R-18 y la auditoría en profundidad,
  sin novedad de código. Cuatro redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`:
  `#24` (baja, de proceso).
- 2026-09-18, ciclo de Programador: sexta reconfirmación tras R-18 y la auditoría en profundidad,
  sin novedad de código. Cuatro redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`:
  `#24` (baja, de proceso).
- 2026-09-18, ciclo de Programador: quinta reconfirmación tras R-18 y la auditoría en profundidad,
  sin novedad de código. Cuatro redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`:
  `#24` (baja, de proceso).
- 2026-09-18, ciclo de Programador: cuarta reconfirmación tras R-18 y la auditoría en profundidad,
  sin novedad de código. Cuatro redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`:
  `#24` (baja, de proceso).
- 2026-09-18, ciclo de Programador: tercera reconfirmación tras R-18 y la auditoría en profundidad,
  sin novedad de código. Cuatro redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`:
  `#24` (baja, de proceso).
- 2026-09-18, ciclo de Programador: segunda reconfirmación tras R-18 y la auditoría en profundidad,
  sin novedad de código. Cuatro redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`:
  `#24` (baja, de proceso).
- 2026-09-18, ciclo de Programador: primera reconfirmación tras R-18 y la auditoría en profundidad,
  sin novedad de código. Cuatro redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`:
  `#24` (baja, de proceso).
- 2026-09-18, ciclo de Auditoría: revisión en profundidad de R-18 ya implementada (integración de
  tomas reales en el selector T-30); cero hallazgos nuevos. Único `ABIERTO`: `#24` (baja, de
  proceso), reconfirmado sin que el patrón que lo motivó se repita una tercera vez.
- 2026-09-17, ciclo de Product Manager: archiva la Oleada v7 (R-18) a `ROADMAP_HISTORICO.md` y
  corrige la prosa de "Cola de producto" de `ROADMAP_PRODUCTO.md`. Cola de producto queda vacía.
- 2026-09-17, ciclo de Programador: novena reconfirmación tras R-18, sin novedad de código. Cuatro
  redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`: `#24` (baja, de proceso).
- 2026-09-17, ciclo de Programador: octava reconfirmación tras R-18, sin novedad de código. Cuatro
  redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`: `#24` (baja, de proceso).
- 2026-09-17, ciclo de Programador: séptima reconfirmación tras R-18, sin novedad de código. Cuatro
  redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`: `#24` (baja, de proceso).
- 2026-09-17, ciclo de Programador: sexta reconfirmación tras R-18, sin novedad de código. Cuatro
  redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`: `#24` (baja, de proceso).
- 2026-09-17, ciclo de Programador: quinta reconfirmación tras R-18, sin novedad de código. Cuatro
  redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`: `#24` (baja, de proceso).
- 2026-09-17, ciclo de Programador: cuarta reconfirmación tras R-18, sin novedad de código. Cuatro
  redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`: `#24` (baja, de proceso).
- 2026-09-17, ciclo de Programador: tercera reconfirmación tras R-18, sin novedad de código. Cuatro
  redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`: `#24` (baja, de proceso).
- 2026-09-17, ciclo de Programador: segunda reconfirmación tras R-18, sin novedad de código. Cuatro
  redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`: `#24` (baja, de proceso).
- 2026-09-17, ciclo de Programador: primera reconfirmación tras R-18, sin novedad de código. Cuatro
  redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`: `#24` (baja, de proceso).
- 2026-09-17, ciclo de Programador: R-18 implementada y COMPLETADA. `scripts/salidas.py` (T-30) gana
  `tomas_por_escena` opcional en `generar_salidas_seleccionadas`: con al menos una toma `buena`,
  `SRT` genera también `guion-alineado.srt` (R-05) y `PPTX` pasa las tomas a `exportar_pptx` para
  duración real y límites absolutos reales (R-13/R-16); `TipoSalida` gana `CAPITULOS_YOUTUBE`
  (quinta opción, R-07). Sin toma registrada, comportamiento idéntico a antes de R-18 (regresión
  byte a byte verificada). 8 tests nuevos (575→583). Cuatro redes en verde. `DEVELOPERS.md` y
  `SKILL.md` actualizados. Auditoría reconfirma `#24` (baja, de proceso) como único `ABIERTO`.
- 2026-09-16, ciclo de Product Manager: abre R-18 (oleada v7 nueva), origen en una grieta de
  arquitectura verificada por el PM releyendo `scripts/salidas.py` junto con los contratos de
  montaje: las salidas basadas en tomas reales (R-05/R-07/R-13/R-16) estaban completas y probadas
  pero nunca llegaban al selector real de T-30. Auditoría del mismo día cierra `#19` y abre `#24`
  (enrutado a la pregunta #11 de §6).
- 2026-09-16, ciclo de Programador: decimonovena reconfirmación tras R-17, sin novedad de código.
  Cuatro redes en verde (575 tests). Auditoría del mismo día cierra `#19` y abre `#24`.
- 2026-09-16, ciclo de Programador: decimoctava reconfirmación tras R-17, sin novedad de código.
- 2026-09-16, ciclo de Programador: decimoséptima reconfirmación tras R-17, sin novedad de código.
- 2026-09-16, ciclo de Programador: decimosexta reconfirmación tras R-17, sin novedad de código.
- 2026-09-16, ciclo de Programador: decimoquinta reconfirmación tras R-17, sin novedad de código.
- 2026-09-16, ciclo de Programador: decimocuarta reconfirmación tras R-17, sin novedad de código.
- 2026-09-16, ciclo de Programador: decimotercera reconfirmación tras R-17, sin novedad de código.
- 2026-09-16, ciclo de Programador: duodécima reconfirmación tras R-17, sin novedad de código.
- 2026-09-16, ciclo de Programador: undécima reconfirmación tras R-17, sin novedad de código.
- 2026-09-16, ciclo de Programador: décima reconfirmación tras R-17, sin novedad de código.
- 2026-09-16, ciclo de Auditoría: cierra `#19` (R-17 verificada en profundidad), abre `#24` (patrón
  recurrente de latencia PM/roadmap, confirmado).
- 2026-09-15, ciclo de Product Manager: prosa de "Cola de producto" corregida (R-17 ya `COMPLETADA`,
  no pendiente) y Fase transversal F-I archivada.
- 2026-09-15, ciclo de Programador: novena reconfirmación tras R-17, sin novedad. Cuatro redes en
  verde (575 tests). Sin trabajo de código pendiente.
- 2026-09-15, ciclo de Programador: octava reconfirmación tras R-17, sin novedad. Cuatro redes en
  verde (575 tests). Sin trabajo de código pendiente.
- 2026-09-15, ciclo de Programador: séptima reconfirmación tras R-17, sin novedad. Cuatro redes en
  verde (575 tests). Sin trabajo de código pendiente. Nota de arranque: clon local en *detached
  HEAD* con rama rezagada, resuelto con `git reset --hard origin/develop` (sin pérdida de historia
  real, verificado con `merge-base --is-ancestor`).
- 2026-09-15, ciclo de Programador: sexta reconfirmación tras R-17, sin novedad. Cuatro redes en
  verde (575 tests). Sin trabajo de código pendiente.
- 2026-09-15, ciclo de Programador: quinta reconfirmación tras R-17, sin novedad. Cuatro redes en
  verde (575 tests). Sin trabajo de código pendiente.
- 2026-09-15, ciclo de Programador: cuarta reconfirmación tras R-17, sin novedad. Cuatro redes en
  verde (575 tests). Sin trabajo de código pendiente.
- 2026-09-15, ciclo de Programador: tercera reconfirmación tras R-17, sin novedad. Cuatro redes en
  verde (575 tests). Sin trabajo de código pendiente.
- 2026-09-15, ciclo de Programador: segunda reconfirmación tras R-17, sin novedad. Cuatro redes en
  verde (575 tests). Sin trabajo de código pendiente.
- 2026-09-15, ciclo de Programador: primera reconfirmación tras R-17, sin novedad. Cuatro redes en
  verde (575 tests). Sin trabajo de código pendiente.
- 2026-09-15, ciclo de Programador: R-17 implementada y COMPLETADA. Investigado el hallazgo #19
  (`_incidencias_anclas_desajustadas` compara solo cardinalidad de anclas, no identidad exacta):
  bajo operación normal la identidad es inyectiva por construcción; el único camino para que la
  comparación no dispare exige corromper `estado.validacion["particiones_pospuestas"]` a mano entre
  pasadas (misma precondición de P-04), y se verificó con test nuevo que incluso ahí el invariante
  (a) de §0.2 sigue intacto (efecto cosmético único). 1 test nuevo (574→575). Cuatro redes en verde.
- 2026-09-14, ciclo de Product Manager: `ROADMAP_PRODUCTO.md` §"Cola de producto" corregida (ya no
  repite la prosa desactualizada del 2026-09-13); R-15 y R-16 confirmadas `COMPLETADA`, Fase F-H y
  Oleada v6 archivadas en `ROADMAP_HISTORICO.md`. Abre **R-17** (fase F-I nueva) a partir del
  hallazgo `#19` (diez pasadas de reconfirmación del auditor sin que nadie lo convirtiera en tarea).
- 2026-09-14, ciclo de Programador: octava reconfirmación del día, sin novedad tras R-16. Cuatro
  redes en verde (574 tests). Sin trabajo de código pendiente.
- 2026-09-14, ciclo de Programador: séptima reconfirmación del día, sin novedad tras R-16. Cuatro
  redes en verde (574 tests). Sin trabajo de código pendiente.
- 2026-09-14, ciclo de Programador: sexta reconfirmación del día, sin novedad tras R-16. Cuatro
  redes en verde (574 tests). Sin trabajo de código pendiente.
- 2026-09-14, ciclo de Programador: quinta reconfirmación del día, sin novedad tras R-16. Cuatro
  redes en verde (574 tests). Sin trabajo de código pendiente.
- 2026-09-14, ciclo de Programador: cuarta reconfirmación del día, sin novedad tras R-16. Cuatro
  redes en verde (574 tests). Sin trabajo de código pendiente.
- 2026-09-14, ciclo de Programador: tercera reconfirmación del día, sin novedad tras R-16. Cuatro
  redes en verde (574 tests). Sin trabajo de código pendiente.
- 2026-09-14, ciclo de Programador: segunda reconfirmación del día, sin novedad tras R-16. Cuatro
  redes en verde (574 tests). Sin trabajo de código pendiente.
- 2026-09-14, ciclo de Programador: primera reconfirmación del día, sin novedad tras R-16. Cuatro
  redes en verde (574 tests). Sin trabajo de código pendiente.
- 2026-09-14, ciclo de Programador: R-16 implementada y COMPLETADA.
`Tarjeta` (`scripts/pptx.py`) gana `inicio_segundos`/`fin_segundos` por escena, calculados una sola
vez (`_con_limites_absolutos`) acumulando en el orden de las escenas con la misma regla real-vs-
estimada que ya elige `duracion_real_segundos` (R-13); `references/contrato-tarjetas.md` documenta
las dos claves nuevas (aditivo, `version_contrato` no sube) y `references/contrato-montaje.md` deja
de pedirle a la cadena de montaje que sume las duraciones a mano — ahora lee los dos campos
directamente, con la fórmula de acumulación como transparencia, no como instrucción. 5 tests nuevos
(569→574): 2 unitarios en `test_pptx.py` (sin toma buena acumula la estimada sin huecos; con toma
buena usa la real) y 3 de integración en `test_integracion_montaje.py` (primera escena empieza en
`0` y no hay hueco/solape entre escenas sobre los tres guiones reales; el `fin_segundos` de la
última escena coincide con el fin de `guion.srt` sin parte de rodaje y con el de
`guion-alineado.srt` con parte de rodaje mezclando real/estimado). Cuatro redes en verde (`mypy`
limpio 68 archivos, `ruff` limpio, 574 tests, `verificar_salidas.py --fixture` catorce etapas en
OK; `.pptx`/`.pdf` reales LATENTES como siempre en este contenedor de nube). `DEVELOPERS.md` y
`SKILL.md` actualizados con la nueva sección/mención. Con R-16 completada, la cola de
`ROADMAP_PRODUCTO.md` vuelve a quedar vacía — la siguiente sesión de Programador no tiene tarea de
código pendiente salvo que el PM abra una nueva o el auditor escale un hallazgo. Sin cambios en
bloqueos ni preguntas abiertas; ninguna desviación respecto a la especificación de R-16.
- 2026-09-14, ciclo de Programador: R-15 implementada y COMPLETADA. `DEVELOPERS.md` gana un bloque
  de cita bajo "Verificación manual" advirtiendo explícitamente contra invocar `ruff`/`mypy`/
  `pytest` pelados en un contenedor de nube (un segundo juego preinstalado más nuevo que el
  pineado, por delante en el `PATH`, con señal distinta y falsos `import-not-found` de `mypy`);
  `SKILL.md` gana la misma advertencia en una frase con remisión. Tarea puramente documental: cero
  cambio en `scripts/`, `tests/` ni `assets/`. Cuatro redes en verde (569 tests).
- 2026-09-13, ciclo de Product Manager: abre R-16 (oleada v6 nueva), origen en una inconsistencia de
  arquitectura del contrato de montaje verificada por el PM (no un hallazgo del auditor):
  `references/contrato-montaje.md` obligaba a la cadena de montaje a reimplementar a mano la
  fórmula de acumulación de duraciones; R-16 añade `inicio_segundos`/`fin_segundos` ya resueltos a
  `tarjetas.json` (mismo patrón que R-13). Solo especificación, no se programa desde ese ciclo.
- 2026-09-12, ciclo de Product Manager: abre R-15 (fase transversal F-H nueva), origen `auditoría
  #22` (media) — un segundo juego de `ruff`/`mypy`/`pytest` preinstalado en el contenedor de nube da
  señal distinta y engañosa a quien lo invoque pelado; R-15 es puramente documental. `#19`
  reconfirmado sin cambios.
- 2026-09-11, ciclo de Product Manager: archiva la Oleada v5 (R-13) y la Fase transversal F-G
  (R-14) — ambas ya `COMPLETADA` por el Programador el mismo día — a `ROADMAP_HISTORICO.md`. Cola de
  `ROADMAP_PRODUCTO.md` quedó vacía en ese ciclo (20/21 hallazgos `RESUELTO`, `roadmap/FEEDBACK.md`
  sin entradas `nuevo`).
- 2026-09-11, ciclo de Programador: octava reconfirmación del día, sin novedad. Cuatro redes en
  verde (569 tests). Sin trabajo de código pendiente tras R-14.
- 2026-09-11, ciclo de Programador: séptima reconfirmación del día, sin novedad. Cuatro redes en
  verde (569 tests). Sin trabajo de código pendiente tras R-14.
- 2026-09-11, ciclo de Programador: sexta reconfirmación del día, sin novedad. Cuatro redes en
  verde (569 tests). Sin trabajo de código pendiente tras R-14.
- 2026-09-11, ciclo de Programador: quinta reconfirmación del día, sin novedad. Cuatro redes en
  verde (569 tests). Sin trabajo de código pendiente tras R-14.
- 2026-09-11, ciclo de Programador: cuarta reconfirmación del día, sin novedad. Cuatro redes en
  verde (569 tests). Sin trabajo de código pendiente tras R-14.
- 2026-09-11, ciclo de Programador: tercera reconfirmación del día, sin novedad. Cuatro redes en
  verde (569 tests). Sin trabajo de código pendiente tras R-14.
- 2026-09-11, ciclo de Programador: segunda reconfirmación del día, sin novedad. Cuatro redes en
  verde (569 tests). Sin trabajo de código pendiente tras R-14.
- 2026-09-11, ciclo de Programador: primera reconfirmación del día, sin novedad. Cuatro redes en
  verde (569 tests). Sin trabajo de código pendiente tras R-14.
- 2026-09-11, ciclo de Programador: R-14 implementada y COMPLETADA. `scripts/clasificador.py`
  extrae el separador `---` de fin de escena a su propio bloque `no_locucion` en vez de dejarlo
  pegado al `contenido` de la última indicación de la escena. 5 tests nuevos (564→569). Cuatro redes
  en verde. Era la última R-XX de la cola.
- 2026-09-11, ciclo de Programador: R-13 implementada y COMPLETADA. `scripts/pptx.py` incorpora
  `duracion_real_segundos` por escena en `tarjetas.json` y `mezcla_duracion_real_y_estimada` de
  cabecera, coherente con `guion-alineado.srt`. 7 tests nuevos (557→564). Cuatro redes en verde.
- 2026-09-10, ciclo de Product Manager: archiva la oleada v4 entera (R-12, ya COMPLETADA) a
  `ROADMAP_HISTORICO.md` y abre **R-13** y **R-14** (fase transversal F-G), ambas sobre huecos ya
  verificados en el código. Reconfirmado: `auditoriacontinua.md` sin ningún hallazgo `ABIERTO` de
  severidad alta.
- 2026-09-10, ciclo de Programador (décimo del día): sin tarea de código pendiente ni novedad que
  reportar. §1 sin ninguna T-XX/R-XX PENDIENTE tras R-12 (ya COMPLETADA); solo T-24b BLOQUEADA por
  hardware del dueño. Cuatro redes en verde (`mypy` limpio, `ruff` limpio, 557 tests, `verificar_
  salidas.py --fixture` catorce etapas OK; `.pptx`/`.pdf` LATENTES como siempre en este contenedor).
- 2026-09-10, sexto ciclo: bloqueo #8 corregido de `ABIERTO` a `RESUELTO` en §3. `list_triggers`
  trae `git_repository.url` y el prompt completo de cada rutina — datos que ninguna reconfirmación
  anterior había leído. El trío "sin sufijo" (`Auditor`/`Product manager`/`Programador`) apunta a
  `https://github.com/JanoSolerDiaz/centro-estudios-sw` (proyecto `GestorAcademia` del dueño, no
  teleprompter) y sus cron no coinciden con los de `-teleprompter`. Ninguna rutina de *este*
  proyecto está duplicada. `auditoriacontinua.md` #19 (baja) y #20 (media) reconfirmados sin
  cambios; #20 queda desactualizado por esta corrección pero es de escritura exclusiva del Auditor.

---

> ## ⚑ PARA EL DUEÑO — empieza por aquí
> Lo único que el proyecto necesita de ti está en dos sitios de este documento:
> - **§3 Bloqueos** = tu lista de tareas. **El #8 (rutinas "duplicadas") era una falsa alarma: corregido hoy (2026-09-10).** Ninguna sesión anterior había comparado el repositorio real de cada rutina, solo el nombre; el trío sin sufijo (`Auditor`/`Product manager`/`Programador`) resulta pertenecer a otro proyecto tuyo (`centro-estudios-sw`/GestorAcademia), no a teleprompter — su prompt lo dice explícitamente. Las tres rutinas de *este* proyecto (`auditor-teleprompter`, `product-manager-teleprompter`, `programador-teleprompter`) están cada una sola, sin solape: no hay coste doble que resolver aquí. Si quieres, revisa por tu cuenta si el trío de `centro-estudios-sw` tiene un problema similar, pero eso es asunto de ese otro repositorio. Los tres bloqueos que quedan siguen **sin urgencia** (aportar el paquete de `480-branded-pptx` cuando lo tengas, probar el clicker Bluetooth real contra el mapa de teclas ya implementado en T-24 cuando lo consigas, y grabar un curso completo con la skill instalada, que es lo que arrancaría el primer feedback real de rodaje) — **ninguno frena el desarrollo**. La instalación de la skill (T-32) ya la hiciste y quedó resuelta.
> - **§6 Preguntas abiertas** = tus decisiones. **Una pendiente: la #11** (2026-09-16, sin urgencia)
>   — si el ciclo de reconfirmación del Programador puede corregir por sí solo la prosa de "Cola de
>   producto" cuando solo refleja un estado que §1 ya registra como `COMPLETADA`. Las otras diez ya
>   están resueltas.
>
> Para control (no exige acción): `DECISIONES_TECNICAS.md` (qué decidió el agente y por qué — sustituye a leer código), `auditoriacontinua.md` (hallazgos abiertos), y aquí §7 (desviaciones) y §5 (P-XX; veta escribiendo `REVERTIR`).

---

## 1. ESTADO GLOBAL DE TAREAS  *(fuente autoritativa de estado y orden de "siguiente tarea")*

| ID | Tarea | Estado | Última sesión | Notas |
|----|-------|--------|---------------|-------|
| T-00 | Verificación inicial | **COMPLETADA** | 2026-08-31 | Esqueleto, 4 redes en verde. El repo ya existía: `git init` no fue necesario |
| T-01 | Linting y formato | **COMPLETADA** | 2026-09-01 | `ruff`/`mypy` estrictos (ya en verde desde T-00) + hook de pre-commit versionado (`scripts/instalar_hooks.py`) que bloquea el commit en rojo |
| T-02 | Logger centralizado | **COMPLETADA** | 2026-09-01 | `scripts/logger.py` (stdlib `logging`), separado de `presentacion.py`; log en la carpeta de salida del guion, `--verbose` cableado en `verificar_salidas.py` |
| T-03 | Suite de tests mínima | **COMPLETADA** | 2026-09-01 | Infraestructura + tests reales de convención contra `fixtures/reales/`; lógica aún no implementada (T-08 a T-13, T-27) cubierta con 8 `skip` con contrato explícito en `tests/test_logica_pendiente.py` |
| T-04 | CI (local + workflow inactivo) | **COMPLETADA** | 2026-09-01 | `scripts/ci.py` (único punto con las cuatro verificaciones); hook delega en él; `.github/workflows/ci.yml` con `workflow_dispatch` únicamente, inactivo |
| T-05 | Monitorización de errores (local) | **COMPLETADA** | 2026-09-01 | `scripts/monitorizacion.py`: `ejecutar_con_diagnostico` (captura + volcado + mensaje accionable) y `ResumenEjecucion` (recuento final). Infraestructura lista; T-07+ la usan desde su punto de entrada |
| T-06 | Robustez de entrada | **COMPLETADA** | 2026-09-01 | `scripts/entrada.py`: valida ruta/tamaño/codificación/estructura mínima, deriva la carpeta de salida de forma segura y acota el tiempo de proceso. `EntradaError` única para todos los fallos |
| T-07 | Estado del proyecto de guión (`estado.json`) | **COMPLETADA** | 2026-09-01 | `scripts/estado.py` + `scripts/migraciones/001_estado_inicial.py`. Escritura atómica, hash de guión, aviso de recalculo |
| T-08 | Parser Markdown y separador de escenas | **COMPLETADA** | 2026-09-01 | `scripts/parser.py`. 7/8/8 escenas exactas en los tres guiones reales, cero preguntas; conflicto de senales y ambiguedad de nivel resueltos con `DeteccionEscenasAmbiguaError` |
| T-09 | Clasificador locución / no locución | **COMPLETADA** | 2026-09-01 | `scripts/clasificador.py`. Ruta rápida por rótulo + cita de bloque; texto suelto en `**LOCUCIÓN**` → `revisar`; inferencia de respaldo ≥95% de precisión sin rótulos; cobertura total verificada por reconstrucción |
| T-10 | Convención de marcado propuesta | **COMPLETADA** | 2026-09-01 | `scripts/convencion.py`. Documenta la convención contractual (`generar_convencion_guiones`/`guardar_convencion_guiones`), señala desviaciones sin bloquear (`detectar_desviaciones`) y deja el mecanismo de consistencia/propuesta (`medir_consistencia_senales`/`proponer_convenciones`) para señales de inferencia futuras |
| T-11 | Troceo en bloques de respiración | **COMPLETADA** | 2026-09-01 | `scripts/troceo.py`. Corta por prioridad (fuerte→débil→nexos→sintagma), protege cifras/fechas/siglas, funde tramos cortos repartiendo si supera el máximo. 100% en rango sobre los tres guiones reales |
| T-12 | Motor de tiempos (ppm deducido del guión) | **COMPLETADA** | 2026-09-01 | `scripts/tiempos.py`. `calcular_tiempos` unica fuente de tiempos; ppm deducido 140-167 en los tres guiones reales (dentro de banda), respaldo 120 ppm documentado, contraste por escena y total |
| T-13 | Normalización a forma dicha | **COMPLETADA** | 2026-09-01 | `scripts/normalizacion.py`. Cardinales/ordinales/porcentajes/monedas/unidades/rangos/fracciones/símbolos/siglas/conjunciones, con diccionario del dueño (`diccionario-locucion.json`) por delante de toda regla automática |
| T-14 | Detector de problemas de locución | **COMPLETADA** | 2026-09-01 | `scripts/deteccion.py`. Cinco familias sobre `BloqueRespiracion` (T-11): frase sin punto de respiración, cacofonías/rima, trabalenguas, anglicismos, estructuras difíciles. Solo la primera admite partición (afecta al troceo); el resto solo avisa |
| T-15 | Reescrituras marcadas y reversibles | **COMPLETADA** | 2026-09-01 | `scripts/reescrituras.py`. Une T-13/T-14 en `Reescritura` (id estable), formato marcado con decisión de una palabra, persistencia append-only en `estado.reescrituras`, aplicación sobre texto y materialización de particiones aceptadas, deshacer global |
| T-16 | `guion-escenas.md` de una sola pasada | **COMPLETADA** | 2026-09-01 | `scripts/documento_revision.py`: compone parseo+tiempos+detección+reescrituras (T-08 a T-15) en un `.md` de revisión con bloques anclados, indicaciones al pie y marca de estado `PENDIENTE`/`VALIDADO` |
| T-17 | Revalidación (respeta ediciones) | **COMPLETADA** | 2026-09-01 | `scripts/revalidacion.py`: relee `guion-escenas.md`, funde con `estado.reescrituras` y materializa/superpone edición manual antes de recalcular tiempos con `tiempos.calcular_tiempos_desde_marcados` (T-12, extraída) |
| T-18 | Reproductor: esqueleto autocontenido | **COMPLETADA** | 2026-09-01 | `scripts/reproductor.py` + `assets/reproductor/`. Datos como JSON en `<script>`, volcados con `textContent`; validador de auto-contención activado de verdad en `verificar_salidas.py --fixture` |
| T-19 | Índice de escenas y pantalla completa | **COMPLETADA** | 2026-09-02 | `assets/reproductor/guion.js` + `estilo.css` reescritos: vista de índice (título, duración, estado pendiente/grabada/revisada) y vista de reproductor, alternadas sin recargar. Fila de escena = único `<button>` navegable con flechas/Tab/Enter/clic |
| T-20 | Motor de avance híbrido | **COMPLETADA** | 2026-09-02 | `assets/reproductor/guion.js`: cadena de `setTimeout` por bloque (duración = `fin_segundos - inicio_segundos` de T-12, escalada por velocidad); pausa/reanudación exacta, avance manual sin salir del automático, velocidad recordada por escena. `Configuracion` gana `paso_velocidad`/`velocidad_minima`/`velocidad_maxima`, viajan al JSON incrustado |
| T-21 | Resaltado, tipografía y tema | **COMPLETADA** | 2026-09-02 | `assets/reproductor/guion.js` + `estilo.css`: atenuación del contexto por distancia (gradiente configurable, opacidad calculada bloque a bloque), contraste AAA del bloque activo verificado por test, tamaño de texto en vivo (`[`/`]`, global, no por escena), margen seguro y cursor oculto en pantalla completa tras inactividad |
| T-22 | Autoscroll con bloque centrado | **COMPLETADA** | 2026-09-02 | `assets/reproductor/guion.js`: `centrarBloqueActivo` mueve `window.scrollY` con interpolacion propia (`requestAnimationFrame`, cancelable) para mantener el bloque activo centrado; corrige de paso un bug real de T-19 (foco diferido que deshacia el centrado) con `focus({preventScroll:true})` |
| T-23 | Ayudas de grabación | **COMPLETADA** | 2026-09-02 | `assets/reproductor/guion.js`: cuenta atrás 3-2-1 desactivable, cronómetro de la toma (deriva estructuralmente nula), barra de progreso por bloques (100% exacto en el último), indicadores ocultables con `H` |
| T-24 | Atajos y clicker Bluetooth | **COMPLETADA** | 2026-09-02 | Mapa completo configurable (`mapa_teclas_reproductor`), antirrebote y ayuda `?`. La verificación del clicker físico **no forma parte de esta tarea**: sale a T-24b por decisión del dueño (§6.9) y sigue en el bloqueo #5 de §3 |
| T-24b | Calibración del clicker Bluetooth real | **BLOQUEADA** — el dueño no dispone de clicker (2026-09-02) | — | Spec: T-24 requisito 2, mitad de verificación física. **El programador no la toca.** Cuando el dueño avise, se resuelve cambiando `Configuracion.mapa_teclas_reproductor`, sin tocar `guion.js`. Ver bloqueo §3.5 |
| T-25 | Modo espejo | **COMPLETADA** | 2026-09-02 | Volteo horizontal (`transform: scaleX(-1)`) de `.escena`, activable con `M`/`m` y con un boton en la cabecera; `Configuracion.espejo_incluye_indicadores` decide si tambien voltea los indicadores. Persistencia minima adelantada de T-26 solo para este ajuste (`claveAlmacenamiento`/`leerPreferencia`/`guardarPreferencia`), que T-26 reutilizara para el resto de preferencias |
| T-26 | Persistencia local de preferencias | **COMPLETADA** | 2026-09-02 | `localStorage` (clave por guion, `try/catch`) para tamaño de texto, velocidad por escena (clave por numero de escena), última escena vista (por `inicio_segundos`, no por índice) e indicadores. Botón "Continuar" en el índice (no auto-lanzamiento: `requestFullscreen` exige gesto de usuario) y "Restablecer preferencias" en la ayuda |
| T-27 | Exportador `.srt` borrador | **COMPLETADA** | 2026-09-02 | `scripts/srt.py`: un subtítulo por bloque de respiración (agrupable si es muy corto, sin cruzar fin de escena), texto locutado final (reescrituras aceptadas incluidas), partición limpia cuando no cabe en el límite de líneas/caracteres, validado con las mismas reglas que ffmpeg |
| T-28 | Exportador `.pdf` con marca 480 | **COMPLETADA** | 2026-09-02 | `scripts/pdf.py`: HTML de impresion (una escena por pagina + portada) con la identidad 480, logotipo incrustado con ratio medido del PNG, conversion con Chrome/Edge headless si esta disponible (nunca falla si no lo esta), modo `--para-terceros` via `incluir_notas_internas` |
| T-29 | Adaptador `.pptx` (`480-branded-pptx`) | **COMPLETADA** | 2026-09-02 | `scripts/pptx.py`: `tarjetas.json` + `brief-pptx.md`; la delegación la hace Claude, no el código. Con la skill de marca ausente (esta máquina) ambos se generan igual y la salida `.pptx` queda latente, tal como preveía su requisito 4 |
| T-30 | Selector de salidas por validación | **COMPLETADA** | 2026-09-02 | `scripts/salidas.py`: pregunta de opción múltiple como datos (`construir_pregunta_salidas`, la formula Claude, no un `input()`), sugerencia desde `estado.salidas_generadas` (sin migración), generación independiente por salida con `try`/`except`, `ResumenSalidas` con generadas/omitidas/latentes |
| T-31 | `SKILL.md` y configuración completa | **COMPLETADA** | 2026-09-02 | Tabla completa de los 81 campos de `Configuracion` en `SKILL.md`, verificada por `tests/test_skill_md.py` (compara claves en las dos direcciones); precedencia documentada; tres referencias nuevas en `references/` (convención de guion, formato de `guion-escenas.md`, mapa de teclas) |
| T-32 | Instalación de la skill y guión de ejemplo | **COMPLETADA** | 2026-09-03 | Desbloqueada: el dueño ejecutó `python scripts/instalar_skill.py` en su máquina (`~/.claude/skills/teleprompter/`) y el health check desde la copia instalada dio **11/11 etapas OK**. Bloqueo #6 de §3 RESUELTO. **Ojo:** la copia instalada quedó hecha ANTES de traer P-03/R-01 del remoto, así que hay que reinstalar para que incorpore ambos |
| T-33 | Encaje con la cadena de montaje | **COMPLETADA** | 2026-09-02 | `references/contrato-montaje.md`: contrato `.srt` + `tarjetas.json`, estructura de carpetas y formula para derivar el rango de tiempo de cada escena; numeracion de escena duplicada/no creciente ahora señalada como desviacion (`convencion.py`); `tests/test_integracion_montaje.py` valida ambas salidas juntas sobre los tres guiones reales |
| R-01 | Persistencia verificada + plan B | **COMPLETADA** | 2026-09-03 | Comprobación real (`try`+relectura al cargar, mas verificacion con Playwright/Chromium real: mismo perfil persiste, perfil nuevo no); aviso honesto si falla; exportar/importar preferencias como `.json` (lee de memoria, no de `localStorage`). Oleada v2 · `origen: auditoría #5` |
| R-02 | Registro de tomas por escena | **COMPLETADA** | 2026-09-03 | Índice = parte de rodaje real: tomas/duración real/toma buena por escena, nota rápida sin salir de grabación, exportación a `.json` fusionada en `estado.json` (migración 002). Oleada v2 · parte de rodaje |
| R-03 | Marcar tropiezos durante la toma | **COMPLETADA** | 2026-09-03 | Tecla `T` marca/desmarca el bloque en pantalla (`alternarTropiezoBloqueActual`); exportación `.json` fusionada por `scripts/feedback.py` en `FEEDBACK.md` (carpeta de salida del guion, no `roadmap/FEEDBACK.md`); destacado en la siguiente revisión por texto exacto. Sin migración, tal como pedía la ficha |
| R-04 | Recalibrar el ritmo con tiempos reales | **COMPLETADA** | 2026-09-03 | `scripts/calibracion.py`: contraste estimada/objetivo/real por escena (real = toma buena de R-02), tipo posicional (apertura/desarrollo/cierre), ppm calibrado propuesto con evidencia de ≥2 guiones (nunca aplicado solo), informe por tipo de escena. Sin migración |
| R-05 | `.srt` alineado con la toma buena | **COMPLETADA** | 2026-09-03 | `scripts/srt_alineado.py`: reescala cada escena a la duración real de su toma buena (mismo factor a palabras y pausa), conserva estimada la escena sin toma buena; `.srt` estimado y alineado en archivos independientes; misma validación estricta de T-27. Sin migración |
| R-06 | Coherencia de nombres y `assets/` | **COMPLETADA** | 2026-09-03 | Sufijo `-tarjetas` → `-teleprompter` (`config.NOMBRE_SUFIJO_CARPETA_SALIDA`); migración automática de carpetas heredadas en `entrada._migrar_carpeta_salida_heredada` (fuera de `scripts/migraciones/`, ver `DECISIONES_TECNICAS.md`); logotipos movidos a `assets/marca/`. Sin migración de `estado.json` |
| R-07 | Capítulos de YouTube con marcas de tiempo reales | **COMPLETADA** | 2026-09-03 | `scripts/capitulos_youtube.py`: empareja títulos de `Capítulos` (T-08) con escenas por orden, tiempo real de la toma buena (R-02) o estimado de T-12 con aviso explícito si se mezclan, formato exacto de YouTube (marca mínima 10 s). Sin migración |
| R-08 | Deuda técnica menor (colores de estado, `PROYECTO.md`, versión de Python) | **COMPLETADA** | 2026-09-03 | `color_estado_grabada_reproductor`/`color_estado_revisada_reproductor` en `Configuracion`; `PROYECTO.md` coincide con §0.2 (ritmo deducido, 120 ppm solo respaldo); `pyproject.toml` mantiene 3.12 como objetivo declarado, `ci.avisar_si_version_python_diverge` avisa (no bloquea) del desajuste con el intérprete real. Fase F-D · `origen: auditoría #10, #11, #12` |
| R-09 | Endurecer el validador de auto-contención | **COMPLETADA** | 2026-09-03 | Seis patrones nuevos en `PATRONES_RECURSO_EXTERNO` (`<object>`, `<embed src>`, `<base href>`, `WebSocket`, `EventSource`/`sendBeacon`, `url(...)` de CSS fuera de `@import`), excepción `data:` donde aplica; lista completa documentada en `references/validador-autocontencion.md`. Fase F-D · `origen: auditoría #13` |
| R-10 | Robustez multiplataforma detectada al correr en Windows por primera vez | **COMPLETADA** | 2026-09-04 | `entrada.leer_guion` normaliza `\r\n`/`\r` a `\n` tras decodificar (hallazgo real); `test_nombre_guion_seguro_nunca_vacio` diagnosticado sin cambio de código (`PureWindowsPath`/`PurePosixPath` parten `"....md"` igual); `test_instalar_hook_...` pasa a `skipif` no-POSIX; los doce `write_text` de `scripts/` fijan `newline="\n"` (requisito 4, hallazgo real de la comprobación). Fase F-E · `origen: hallazgo de sesión (no de auditoría)` |
| R-11 | Robustez de datos derivados del rodaje (toma buena ambigua, capítulos sobrantes, cobertura cruzada) | **COMPLETADA** | 2026-09-04 | `tomas.duracion_toma_buena` rechaza con `RegistroTomasError` más de una toma `buena` por escena (#16); `capitulos_youtube.calcular_capitulos` expone `titulos_sobrantes` cuando hay más títulos que escenas (#17); nuevo test de coherencia cruzada `.srt` alineado/capítulos de YouTube en `tests/test_integracion_montaje.py` (#18). Fase F-F · `origen: auditoría #16, #17, #18` |
| R-12 | Cue discreta de indicaciones EN PANTALLA/NOTA en el reproductor | **COMPLETADA** | 2026-09-10 | `reproductor._indicaciones_ancladas_por_indice` ancla cada indicación al ÚLTIMO bloque de respiración que la precede (sin bloque precedente, al primero — requisito 4), reutilizando tal cual la clasificación de T-09 y el filtro pantalla/nota de T-28/T-29 (`pdf.indicaciones_no_recitables`/`es_nota_interna`). `guion.js`/`estilo.css`: cue subordinada (`.cue-indicacion`, visible solo bajo `.bloque--activo`), plegada con el resto de indicadores en `H` (T-23), sin atajo nuevo. Prefijos `Pantalla:`/`Nota:` configurables. 7 tests nuevos (550→557); verificado también visualmente con Playwright/Chromium real. Oleada v4 · `origen: observación de arquitectura del PM (2026-09-08)` |
| R-13 | Duración real por escena en `tarjetas.json`, coherente con `guion-alineado.srt` | **COMPLETADA** | 2026-09-11 | `scripts/pptx.py`: `Tarjeta.duracion_real_segundos` (`None` si la escena no tiene toma buena, `tomas.duracion_toma_buena` reutilizada tal cual) y `ResultadoTarjetas.mezcla_duracion_real_y_estimada` (booleano de cabecera, `true` solo si el conjunto mezcla ambos casos); `duracion_estimada_segundos` intacta (requisito 2). `generar_tarjetas`/`exportar_pptx` ganan `tomas_por_escena` opcional (mismo patrón que `srt_alineado.py`/`capitulos_youtube.py`, no integrado en el selector automático de T-30); sin él, comportamiento idéntico a antes de R-13. `references/contrato-tarjetas.md` y `contrato-montaje.md` actualizados con la fórmula de rango correcta. 7 tests nuevos (557→564), incluido el cruce con `guion-alineado.srt` en `test_integracion_montaje.py`. Oleada v5 · `origen: observación de arquitectura del PM (2026-09-10)` |
| R-14 | El separador de escena no debe colarse en el texto de una indicación | **COMPLETADA** | 2026-09-11 | `scripts/clasificador.py`: `_separar_marcador_fin_escena` extrae el `---` de fin de escena (con las líneas en blanco que lo acompañan) en su propio bloque `no_locucion` (`senal="separador_escena"`) antes de clasificar rótulos/inferencia, en vez de dejarlo pegado al `contenido` de la última indicación. Nueva señal añadida a los tres sitios que la necesitan para no colarse como una "indicación" propia ni proponerse como convención: `pdf._SENALES_ESTRUCTURALES`, `documento_revision._SENALES_ESTRUCTURALES` y `convencion._SENALES_CONTRACTUALES`. `references/convencion-guion.md` documenta ahora el separador (requisito 1). Fixture golden `fixtures/guion-ejemplo-esperado.md` regenerado a mano (cambio esperado y verificado línea a línea). 5 tests nuevos (564→569). Verificado sobre los tres guiones reales: cero indicación termina en `---` en `guion-escenas.md`, `tarjetas.json` ni la cue del reproductor; reconstrucción íntegra (invariante (a)) intacta. Fase F-G · `origen: observación de arquitectura de R-12 (2026-09-10)` |
| R-15 | Advertir explícitamente contra el binario "pelado" de `ruff`/`mypy`/`pytest` en un contenedor de nube | **COMPLETADA** | 2026-09-14 | Tarea puramente documental: nota visible en `DEVELOPERS.md` (bloque de cita bajo "Verificación manual") y frase con remisión en la sección "Verificacion" de `SKILL.md`, explicando que la única verificación válida es `python scripts/ci.py` / `python -m <herramienta>`, nunca el binario pelado. Cero cambio en `scripts/`, `tests/` o `assets/`; cuatro redes en verde (569 tests). `origen: auditoría #22` — queda para la siguiente pasada del auditor cerrar `#22` a `RESUELTO` |
| R-16 | Límites absolutos de escena (`inicio_segundos`/`fin_segundos`) en `tarjetas.json` | **COMPLETADA** | 2026-09-14 | `Tarjeta` (`scripts/pptx.py`) gana los dos campos, calculados una sola vez (`_con_limites_absolutos`) con la misma regla real/estimada de R-13, acumulando en el orden de las escenas; `contrato-tarjetas.md` documenta las dos claves y `contrato-montaje.md` deja de pedirle a la cadena de montaje que sume las duraciones a mano — ahora las lee directamente. Cambio aditivo, `version_contrato` no sube, sin migración de `estado.json` ni campo nuevo de `Configuracion`. 5 tests nuevos (569→574): 2 unitarios (`test_pptx.py`) y 3 de integración (`test_integracion_montaje.py`, incluida la coherencia con `guion.srt`/`guion-alineado.srt`). Cuatro redes en verde. `origen: observación de arquitectura del PM (2026-09-13)` |
| R-17 | Endurecer o cerrar formalmente la asimetría teórica de `_incidencias_anclas_desajustadas` (`scripts/revalidacion.py`) | **COMPLETADA** | 2026-09-15 | Spec completa en `ROADMAP_PRODUCTO.md` §Fase F-I. `origen: auditoría #19` (abierto 2026-09-04, reconfirmado sin cambios en diez pasadas sucesivas del auditor). Investigada y cerrada por la vía del requisito 3 (con matiz): bajo operación normal la identidad es inyectiva por construcción (`pospuestas_previas` siempre coincide con lo que la pasada anterior persistió); el único escenario que rompe la comparación por cardinalidad exige corromper `estado.validacion["particiones_pospuestas"]` a mano (misma precondición ya conocida de P-04), y se verificó con test nuevo que incluso ahí el invariante (a) — nada se pierde ni se duplica — sigue intacto, con un único efecto cosmético (número de bloque erróneo en la incidencia de conflicto, escena correcta). 1 test nuevo (574→575) en `tests/test_revalidacion.py`. Cuatro redes en verde. Detalle completo en `DECISIONES_TECNICAS.md` |
| R-18 | Integrar en el selector de salidas (T-30, `scripts/salidas.py`) las salidas que dependen de tomas reales: `guion-alineado.srt` (R-05), `capitulos-youtube.txt` (R-07, hoy ni siquiera seleccionable) y los campos reales de `tarjetas.json` (R-13/R-16) | **COMPLETADA** | 2026-09-17 | `scripts/salidas.py`: `generar_salidas_seleccionadas` gana `tomas_por_escena` opcional (`EstadoProyecto.tomas` tal cual); con al menos una toma `buena`, `SRT` genera también `guion-alineado.srt` (R-05) bajo el mismo `TipoSalida.SRT`, y `PPTX` pasa las tomas a `exportar_pptx` para duración real/límites absolutos (R-13/R-16). `TipoSalida` gana `CAPITULOS_YOUTUBE` (quinta opción), generado con `capitulos_youtube.generar_capitulos_youtube`; sin sección `Capítulos`, queda `SalidaOmitida` con el motivo exacto, nunca fallo ni latente. `verificar_salidas.py::verificar_generacion` distingue ahora un fallo real (prefijo `"fallo al generar:"`) de esa omisión esperada. Sin tomas, comportamiento idéntico al de antes de R-18 (test de regresión byte a byte sobre los tres guiones reales). 8 tests nuevos (575→583). Cuatro redes en verde. Detalle completo en `DEVELOPERS.md` y `DECISIONES_TECNICAS.md` |
| R-19 | Enlazar la toma buena de cada escena con su archivo de vídeo real (campo opcional tecleado en el reproductor) y generar `concat-ffmpeg.txt`, la lista de concatenación lista para `ffmpeg -f concat` | **COMPLETADA** | 2026-09-30 | `Toma.archivo_video` (opcional, `""` por defecto) anotable con `V`/`v` durante la grabación o editable después desde el índice sin volver a grabar; `references/contrato-tomas.md` sube a versión 2 (aditivo, sin migración). `scripts/concat_ffmpeg.py` nuevo: reutiliza `tomas.toma_buena` (extraída de `duracion_toma_buena`, misma regla de exclusividad de R-11/#16) para generar `file '<archivo_video>'` o `# ESCENA N: <motivo>` por escena, en su orden real. `TipoSalida.CONCAT_FFMPEG` (sexta opción de T-30): omitida sin ningún parte de rodaje, nunca falla por escenas pendientes de anotar. 23 tests nuevos (583→606). Cuatro redes en verde, incluidas dos etapas nuevas en `verificar_salidas.py --fixture` (dieciséis en total). Verificado además con Playwright/Chromium real: anotar durante la grabación, editar desde el índice sin regrabar, exportar el parte de rodaje y generar `concat-ffmpeg.txt` con una ruta con comilla simple correctamente escapada. `DEVELOPERS.md`, `SKILL.md` y las referencias de `contrato-tomas.md`/`contrato-montaje.md`/`mapa-teclas.md` actualizados. Oleada v8, archivada en `ROADMAP_HISTORICO.md` en el ciclo de PM del 2026-09-30, junto con la nota de gobernanza sobre cómo se justificó su apertura (`auditoriacontinua.md` #26) |
| R-20 | Anclar cada indicación `EN PANTALLA`/`NOTA` de `tarjetas.json` a un instante estimado dentro de la escena (`indicaciones_ancladas`, campo aditivo), reutilizando el anclaje que R-12 ya calcula para la cue en vivo del reproductor | **COMPLETADA** | 2026-10-01 | `reproductor.py::_indicaciones_ancladas_por_indice` (R-12) se divide: el anclaje se extrae a la función pública `anclar_indicaciones_a_bloques` (mismo patrón que `tomas.toma_buena` en R-19), reutilizada tal cual por `pptx.py`. `Tarjeta` gana `indicaciones_ancladas` (dataclass `IndicacionAnclada`: `texto`/`es_nota_interna`/`instante_estimado_segundos`), mismo conjunto que `indicaciones_pantalla`+`notas_internas`, calculado relativo a la escena y convertido a absoluto en `_con_limites_absolutos` (R-16, mismo acumulado que `inicio_segundos`/`fin_segundos`). Escena sin bloques de locución (sin ejemplo real, contemplada por `validar_tarjetas`): ancla al inicio de la escena. `--para-terceros` omite notas internas también aquí. Cambio aditivo, `version_contrato` no sube, sin migración. 7 tests nuevos (606→613), incluido uno que compara el instante exacto contra la cue del reproductor para el mismo guion (sin toma real: acumulados idénticos bit a bit). Cuatro redes en verde. `references/contrato-tarjetas.md`/`contrato-montaje.md`, `DEVELOPERS.md` y `SKILL.md` actualizados |
| R-21 | Validar `concat-ffmpeg.txt` en la ruta real de generación (`scripts/salidas.py`) invocando el validador propio del demuxer `concat` de ffmpeg antes de escribirlo, y sanear `archivo_video` en el origen (recorte de espacios, rechazo de salto de línea) | **COMPLETADA** | 2026-10-02 | `scripts/salidas.py::_generar_concat_ffmpeg` llama a `concat_ffmpeg.validar_lista_concat_ffmpeg` sobre el contenido ya generado antes de `guardar_lista_concat_ffmpeg`; un contenido inválido degrada a `SalidaOmitida` con el motivo exacto (mismo patrón `try`/`except` que ya protege a las demás salidas), nunca una excepción sin capturar ni un archivo corrupto en disco. `scripts/tomas.py` gana `_sanear_archivo_video` (recorta espacios, normaliza a `""` si queda vacío o trae `\n`/`\r`), aplicada en `_toma_desde_dict` al leer un parte de rodaje editado a mano; `assets/reproductor/guion.js` gana la función gemela `sanearArchivoVideo(valor)`, aplicada en los dos puntos donde el dueño teclea el valor (`pedirArchivoVideoToma` durante la grabación y el botón de edición desde el índice). `references/contrato-tomas.md` y `contrato-montaje.md` documentan la regla de saneamiento y la validación antes de escritura. Fuera de alcance, explícito: no se extiende la misma validación-antes-de-escribir a `srt.py`/`capitulos_youtube.py` (misma deuda preexistente, sin las consecuencias reales que le da a `archivo_video` ser texto libre). 6 tests nuevos (613→619): 4 en `test_tomas.py` (recorte, solo espacios, salto de línea, retorno de carro), 1 en `test_salidas.py` (contenido inválido forzado por monkeypatch degrada a omitida sin escribir), 1 nuevo más la actualización de uno existente en `test_reproductor.py` (los dos puntos de entrada saneados en el HTML generado). Cuatro redes en verde, incluidas las dieciséis etapas de `verificar_salidas.py --fixture`. Fase transversal F-J, cierra el hallazgo `#27` de `auditoriacontinua.md`. `DEVELOPERS.md` y `SKILL.md` actualizados |
| R-22 | Capítulos reales incrustables en el vídeo final: `capitulos-ffmpeg.txt`, formato `FFMETADATA1` nativo de ffmpeg, reutilizando tal cual el emparejamiento título↔escena y los tiempos real/estimado que `capitulos_youtube.calcular_capitulos` ya calcula para `capitulos-youtube.txt` (R-07) | **COMPLETADA** | 2026-10-05 | `ResultadoCapitulos` gana el campo aditivo `duracion_total_segundos` (el cursor final que el bucle de `calcular_capitulos` ya acumulaba y hasta ahora descartaba, `0.0` en los tres casos de `motivo_sin_generar`). `scripts/capitulos_youtube.py` gana `formatear_capitulos_ffmpeg` (hermana de `formatear_capitulos_youtube`: primera línea `;FFMETADATA1`, un bloque `[CHAPTER]` por capítulo con `TIMEBASE=1/1000`/`START`/`END` en milisegundos truncados hacia abajo y `title=<título>` escapado según el propio formato — `\`, `=`, `;`, `#` y salto de línea con `\` por delante, mismo patrón que `concat_ffmpeg._escapar_ruta_ffmpeg` de R-19; `END` de un capítulo es el `START` del siguiente, el del último es `duracion_total_segundos` convertido a ms; nota de transparencia real/estimado como comentario `;` cuando aplica), deliberadamente SIN la marca mínima de YouTube (requisito 4: cada escena emparejada es su propio capítulo, un archivo de metadatos incrustado no compite por espacio de lectura) y `validar_capitulos_ffmpeg` (exige `;FFMETADATA1`, `START`/`END` enteros no negativos, `START` estrictamente creciente, sin solapes). `scripts/salidas.py::_generar_capitulos_youtube` genera `capitulos-ffmpeg.txt` como segunda mitad de la misma opción `CAPITULOS_YOUTUBE` (no una séptima, mismo patrón que `guion.srt`/`guion-alineado.srt` bajo `SRT`, R-18), validándolo antes de escribir desde el primer día (lección del hallazgo `#27`/R-21): un contenido inválido degrada solo esa mitad a `SalidaOmitida`, sin impedir que `capitulos-youtube.txt` se mantenga. `config.NOMBRE_ARCHIVO_CAPITULOS_FFMPEG = "capitulos-ffmpeg.txt"` (constante de módulo, no campo de `Configuracion`). 18 tests nuevos (619→637): `tests/test_capitulos_youtube.py` (formato exacto, contigüidad `END`=`START` siguiente, sin filtrado por marca mínima a diferencia de YouTube, escapado de caracteres especiales, nota de transparencia, criterio de aceptación sobre los tres guiones reales, validador independiente, guardado) y `tests/test_salidas.py` (contenido coincide con la llamada directa; contenido inválido forzado por monkeypatch degrada solo esa mitad sin afectar a `capitulos-youtube.txt`). Cuatro redes en verde, `verificar_salidas.py --fixture` gana dos etapas nuevas (dieciocho en total). `references/contrato-montaje.md`, `DEVELOPERS.md` y `SKILL.md` actualizados. Oleada v10, `origen: observación de arquitectura del PM (2026-10-02)` |
| R-23 | Desviaciones de convención visibles donde de verdad hacen falta: `scripts/convencion.py::detectar_desviaciones` (T-10/T-33) calcula correctamente escena sin rótulo, rótulo desconocido, sección auxiliar no reconocida y número de escena duplicado/no creciente, pero no se llama desde `documento_revision.py` (`guion-escenas.md`) ni `pptx.py` (`tarjetas.json`) — solo desde sus propios tests, pese a que `contrato-montaje.md` afirma lo contrario citando esa función | **COMPLETADA** | 2026-10-06 | `documento_revision.generar_documento_revision` llama una vez a `detectar_desviaciones` (misma `clasificacion` ya calculada) y reparte cada desviación por rango de línea: al pie de la escena que corresponda (`### Desviaciones de la convención`, separada de las indicaciones no recitables) o, si no cae en ninguna escena (p. ej. sección auxiliar no reconocida), en una sección propia tras el resumen global (`## Desviaciones de la convención (fuera de escena)`); cabecera gana el recuento "Desviaciones de la convención: N" (siempre presente, `N=0` no añade ninguna sección nueva). `pptx.py::ResultadoTarjetas` gana el campo aditivo `metadatos.desviaciones_convencion` (mismo `resultado`/`clasificacion` reutilizado, sin segunda implementación), vacío con `--para-terceros` igual que `notas_internas`. Cero cambio en `convencion.detectar_desviaciones` en sí (requisito 6). `references/contrato-tarjetas.md` y `contrato-montaje.md:68-73` actualizados — este último deja de afirmar en abstracto que la numeración "ya NO se da por supuesta en silencio" y dice exactamente dónde mirar. 9 tests nuevos (637→646): `tests/test_documento_revision.py` (localización correcta, sección fuera de escena, recuento de cabecera, `N=0` sin sección nueva), `tests/test_pptx.py` (lista vacía, misma descripción que `detectar_desviaciones`, exclusión `--para-terceros`, serialización) y `tests/test_integracion_montaje.py` (mismo texto en `guion-escenas.md` y `tarjetas.json` a la vez — el hallazgo que motivó la tarea). Fixture dorada `guion-ejemplo-esperado.md` regenerada (único cambio: la línea de cabecera en 0, ninguna sección nueva, confirma que los tres guiones reales no tienen desviaciones). Cuatro redes en verde; `verificar_salidas.py --fixture` sigue en dieciocho etapas (ninguna salida nueva). `DEVELOPERS.md` y `SKILL.md` actualizados. Oleada v11, `origen: observación de arquitectura del PM (2026-10-05)` |
| R-24 | Diagnóstico real de un fallo al generar una salida: `scripts/salidas.py::generar_salidas_seleccionadas` (T-30/R-18) captura hoy cualquier excepción con un `except` ad hoc que muestra al dueño el `repr` crudo de Python y no vuelca ningún diagnóstico, en vez de usar la infraestructura de logger/diagnóstico de T-02/T-05 que se construyó el primer día del proyecto anticipando exactamente este consumidor | **COMPLETADA** | 2026-10-07 | `scripts/monitorizacion.py::volcar_diagnostico` (antes `_volcar_diagnostico`) promovida a pública; `generar_salidas_seleccionadas` la reutiliza junto con `logger.obtener_logger` dentro del `except` ya existente (sin cablear `ejecutar_con_diagnostico`, que aborta el proceso), volcando `diagnostico-<timestamp>.log` y registrando en el logger antes de construir la `SalidaOmitida` con un motivo en español que cita la ruta del diagnóstico. 3 tests nuevos (646→649). Cuatro redes en verde |
| R-25 | Entregar `convencion-guiones.md` de verdad al dueño: conectar `scripts/convencion.py::generar_convencion_guiones`/`guardar_convencion_guiones` (T-10) — sin ningún consumidor fuera de sus propios tests — al selector real de salidas (T-30) | **COMPLETADA** | 2026-10-08 | `scripts/salidas.py` gana `TipoSalida.CONVENCION_GUIONES` (séptima opción, mismo patrón que `CAPITULOS_YOUTUBE`/R-18 y `CONCAT_FFMPEG`/R-19) y `_generar_convencion_guiones`, que reutiliza tal cual `convencion.guardar_convencion_guiones` (cero cambio en `convencion.py`). A diferencia de las demás salidas, no depende del parseo ni de la clasificación del guion de entrada, solo de `Configuracion`: se ofrece siempre en `construir_pregunta_salidas`, nunca omitida por falta de datos del guion o de parte de rodaje; el único fallo posible es de escritura a disco, cubierto por el mismo patrón `try`/`except`/diagnóstico de R-24. 3 tests nuevos (649→652), dos tests existentes actualizados al nuevo recuento de salidas siempre generadas. `references/contrato-montaje.md`, `SKILL.md` y `DEVELOPERS.md` actualizados. Cuatro redes en verde, dieciocho etapas de `verificar_salidas.py --fixture` sin cambio |
| R-26 | El diccionario del dueño (`diccionario-locucion.json`, T-13 requisito 3, "manda siempre") no tiene ningún llamador real fuera de sus propios tests, ni `cargar_diccionario_locucion` ni los cuatro puntos reales donde se aplicaría (`normalizar_guion`, `recopilar_propuestas`, `generar_documento_revision`, `revalidar_guion`): la garantía contractual del propio `SKILL.md` no se cumple hoy en el flujo real salvo que la sesión recuerde cargarlo a mano, sin ningún aviso si no lo hace | **COMPLETADA** | 2026-10-09 | `generar_documento_revision`/`revalidar_guion` ganan `carpeta_salida` opcional: `revalidar_guion` carga el diccionario por su cuenta (si no hay uno explícito); `generar_documento_revision` cuenta las entradas realmente aplicadas en la cabecera y avisa si el archivo tiene entradas sin aplicar. Mismo recuento expuesto en `tarjetas.json.metadatos.entradas_diccionario_aplicadas`. `SKILL.md` documenta el paso explícito con el fragmento de código exacto |
| R-27 | El aviso de guion modificado (`avisar_si_guion_modificado`, T-07) no tiene ningún llamador real ni mención en `SKILL.md`, y aunque se wireara tal cual, `estado.guion.hash_sha256`/`tamano_bytes` nunca se actualizan tras `estado_inicial`, así que el aviso se repetiría para siempre en vez de aparecer una sola vez | **COMPLETADA** | 2026-10-12 | `scripts/estado.py` gana `actualizar_info_guion(estado, ruta_guion)` (refresca `hash_sha256`/`tamano_bytes` al contenido actual, mutando `estado` en el sitio, llamada justo antes de `guardar_estado`). `documento_revision.generar_documento_revision` gana `guion_modificado: bool = False`: con `True`, la cabecera del resumen global añade la línea de aviso visible (mismo criterio de transparencia que ppm/T-12, diccionario/R-26, desviaciones/R-23). `SKILL.md` documenta el paso explícito con el fragmento de código exacto (tras cargar `estado.json` y antes de re-parsear/regenerar, `avisar_si_guion_modificado` → `generar_documento_revision(..., guion_modificado=...)`; `actualizar_info_guion` justo antes de `guardar_estado`), mismo patrón que R-26. Sin migración (solo refresca valores ya existentes de `InfoGuion`); `revalidar_guion` intacto, sin releer el guion de origen. 4 tests nuevos (665→669): 2 en `tests/test_estado.py` (refresco exacto al hash/tamaño actuales; cierra el bucle — tras actualizar, `avisar_si_guion_modificado` vuelve a `False` sin que el guion cambie de nuevo) y 2 en `tests/test_documento_revision.py` (línea de aviso con `True`; ninguna línea nueva con `False`, el valor por defecto). Cuatro redes en verde. `DEVELOPERS.md` actualizado con sección propia. Oleada v15, `origen: observación de arquitectura del PM (2026-10-09)` |
| R-28 | Tres validadores de contrato ya construidos (`pptx.validar_tarjetas`, `srt.validar_srt`, `capitulos_youtube.validar_capitulos_youtube`) nunca se invocan en la ruta real de generación de `scripts/salidas.py`/`pptx.exportar_pptx`, solo desde `verificar_salidas.py --fixture` — mismo patrón de grieta ya cerrado por R-21 (`concat-ffmpeg.txt`) y R-22 (`capitulos-ffmpeg.txt`), sin corregir aquí para sus tres gemelos (`tarjetas.json`, `guion.srt`/`guion-alineado.srt`, `capitulos-youtube.txt`) | **COMPLETADA** | 2026-10-13 | `pptx.py::exportar_pptx` valida con `validar_tarjetas` antes de `guardar_tarjetas_json` (lanza `TarjetasInvalidasError`, capturada por el `try`/`except` genérico de R-24); `salidas.py::_generar_srt`/`_generar_capitulos_youtube` validan cada mitad por separado con `validar_srt`/`validar_capitulos_youtube`, degradando a `SalidaOmitida` a mano (mismo patrón que `_generar_concat_ffmpeg`/R-21) sin impedir que la mitad sana se genere. Cero cambio en las reglas de los tres validadores ni en `concat_ffmpeg.py`/`validar_capitulos_ffmpeg` (ya conectados). 4 tests nuevos (669→673). Cuatro redes en verde, dieciocho etapas de `verificar_salidas.py --fixture` sin cambio. `DEVELOPERS.md` y `DECISIONES_TECNICAS.md` actualizados |
| R-29 | `revalidacion.py::_particion_aceptada_de`/`_materializar_marcados` reimplementan en privado, con las mismas cuatro condiciones a mano, el emparejamiento bloque↔reescritura que `reescrituras.py::aplicar_particion_aceptada`/`aplicar_particiones_aceptadas` ya construyó, probó y documentó explícitamente como la pieza a reutilizar por T-17 — nunca llamadas desde la ruta real, en el área exacta de dos incidencias de severidad alta ya cerradas (P-02, P-04) | **COMPLETADA** | 2026-10-14 | Investigado (requisito 1): dos tests nuevos confirman que ambas rutas ya coincidían bloque a bloque (tres guiones reales, sin ninguna partición propuesta hoy; y `_GUION`/`_GUION_ESCENA_DOS_PARTICIONES`, con particiones de verdad) — sin divergencia real (requisito 3 no aplica). Unificado (requisito 2): `_particion_aceptada_de` ahora delega en `aplicar_particion_aceptada` (lista de un bloque, longitud del resultado decide si coincidió); la salvaguarda P-02/P-04 (hallazgo #9) sigue intacta como guardia de entrada, sin tocar la función pública. 2 tests nuevos (673→675). Cuatro redes en verde. Detalle completo en `DECISIONES_TECNICAS.md` |

**Estados:** PENDIENTE · EN CURSO · COMPLETADA · DESPLEGADA EN PRODUCCIÓN · BLOQUEADA — <motivo> · DESCARTADA — <motivo>

*(La spec de cada tarea: T-XX en el cuerpo de `HOJA_DE_RUTA.md`; R-XX en `ROADMAP_PRODUCTO.md`. Este §1 NO repite la spec, solo el estado.)*

---

## 3. BLOQUEOS — ACCIONES PENDIENTES DEL DUEÑO

> El código se entrega igualmente; estas acciones activan funcionalidad latente.

| # | Acción | Tarea | Instrucciones exactas | Estado |
|---|--------|-------|-----------------------|--------|
| 1 | Instalar el plugin `skill-creator` (andamio de la skill) | T-00 | — | **RESUELTO 2026-08-31** — instalado (`skill-creator@claude-plugins-official`, ámbito usuario). |
| 2 | Aportar el **paquete** de `480-branded-pptx` | T-29 | El `SKILL.md` y el `brand-guide.md` ya están transcritos en `references/marca-480.md` (2026-08-31): bastan para el contrato, el brief y el estilo del PDF. Falta la skill instalada en `~/.claude/skills/480-branded-pptx/` con sus assets, y la skill `pptx` de la que depende. Hasta entonces la salida `.pptx` queda latente. **2026-09-02: el dueño confirma que aún no lo tiene y decide NO bloquear T-29** (§6.10) — se implementa entera por su requisito 4 y la salida queda latente, como ya preveía su criterio de aceptación. Este bloqueo no frena ninguna tarea. | ABIERTO — sin urgencia |
| 3 | Aportar 2–3 guiones de producción reales (`.md`) | T-09, T-10 | — | **RESUELTO 2026-08-31** — 3 guiones en `fixtures/reales/` (`guion-08-busqueda-investigacion`, `guion-09-proyectos`, `guion-artefactos-lienzo`). T-08 a T-12 recalibradas contra ellos en la hoja de ruta v1.1. |
| 4 | Conseguir los archivos de logotipo `480_*.png` | T-28 | — | **RESUELTO 2026-08-31** — las cuatro variantes en `assets/`, PNG RGBA con transparencia. **Ojo:** miden 1993×805 (ratio 2,4758), no el 1.7766 que dice la guía de marca; el ratio se mide del archivo. Ver `references/marca-480.md`. |
| 5 | Probar los atajos con el clicker Bluetooth real | T-24b | **2026-09-02: el dueño no dispone de clicker; queda en espera indefinida** (§6.9), y **T-24b está BLOQUEADA — el programador no debe intentarla**. El mapa completo ya está implementado (T-24, 2026-09-02): `Espacio`, `PageUp`/`PageDown`, flechas, `+`/`-`, `[`/`]`, `R`, `H`, `Esc` y `?`. Cuando el dueño consiga un mando: abrir el reproductor generado, pulsar cada botón y decir qué tecla envía cada uno — si no coincide con el mapa vigente (visible con `?` dentro del reproductor), el agente lo ajusta en `Configuracion.mapa_teclas_reproductor`, sin tocar `guion.js`. | ABIERTO — en espera indefinida |
| 6 | Instalar de verdad la skill (T-32) en tu propio Claude Code | T-32 | **2026-09-02: una sesión de nube no alcanza tu `~/.claude/skills/`** (nota de entorno, protocolo v1.3), así que ni la instalación ni el health check posterior pueden ejecutarse ni confirmarse desde aquí — todo lo demás de T-32 (`scripts/instalar_skill.py`, `fixtures/guion-ejemplo.md` y su versión esperada, la documentación de arquitectura en `DEVELOPERS.md`) ya está entregado y probado (contra una copia sincronizada de prueba, nunca contra tu ruta real). Ejecuta `python scripts/instalar_skill.py` (o pásale `--destino` si quieres otra ruta) y luego `python ~/.claude/skills/teleprompter/scripts/verificar_salidas.py --fixture`: si todas las etapas salen `OK`, T-32 puede marcarse COMPLETADA de verdad. Si algo falla, copia aquí la salida completa. | **RESUELTO 2026-09-03** — el dueño instaló la skill en `C:\Users\JanoSolerDíaz\.claude\skills\teleprompter` y el health check desde esa copia salió con las **11 etapas en OK**. Efecto colateral valioso: en su máquina **el `.pdf` real sí se genera** (tiene Chrome/Edge), no queda latente como en las sesiones de nube — es la primera vez que una verificación completa produce el PDF de verdad. La única salida que sigue latente es el `.pptx`, por el bloqueo #2. |
| 7 | Grabar un vídeo de curso completo con el teleprompter instalado, usando el ciclo entero (validación → grabación con tomas y tropiezos → revalidación → salidas) | Oleada v1 (criterio de salida) y v2 (evidencia real para R-04) | Todo el código de v1 a F-D está entregado, verificado y —desde T-32— instalado y probado en tu máquina real, `.pdf` real incluido. Falta el propio rodaje: sin él, el modo de operación sigue en AUTONOMÍA TOTAL (no conmuta a PRODUCCIÓN, §0.1) y `FEEDBACK.md` y la calibración de ppm de R-04 siguen sin ninguna entrada real. Cuando grabes, usa las ayudas ya entregadas: `G` marca la toma buena y `T` el tropiezo (R-02/R-03), así la primera grabación ya alimenta el ciclo de mejora en vez de perderse. | ABIERTO — sin urgencia, no bloquea ninguna tarea de código |
| 8 | ~~Revisar y desactivar/borrar las rutinas programadas duplicadas de este proyecto~~ — **diagnóstico corregido, no hace falta acción sobre teleprompter** | Infraestructura, no código | Hallazgo original de 2026-09-04 (duodécimo ciclo del día): `list_triggers` devuelve seis rutinas con nombre parecido — `Auditor`/`auditor-teleprompter`, `Product manager`/`product-manager-teleprompter`, `Programador`/`programador-teleprompter` — y se asumió que el trío sin sufijo (creado 2026-08-25, `trig_019V5UKE8jKMvA2LCneiTtTD`/`trig_01Gou6bJDBVucaAkfXYaynAz`/`trig_01RkE491KgehtmqBcoFUFFKz`) era un resto de prueba duplicando las rutinas `-teleprompter`, con coste doble de cómputo. **Corregido el 2026-09-10 (sexto ciclo de Programador):** `list_triggers` también trae `git_repository.url` y el prompt completo de cada rutina, campos que ninguna de las ~15 reconfirmaciones anteriores había leído. Los tres apuntan a `https://github.com/JanoSolerDiaz/centro-estudios-sw` (no a `telePrompter`) y su prompt lo confirma («...para **GestorAcademia**», no teleprompter) — son las rutinas de OTRO proyecto del dueño, con nombres aún sin el sufijo de producto que sí llevan las de este repo. Sus cron tampoco eran realmente coincidentes (`Programador` sin sufijo: `0 6,8,10,12,14 * * 1-5`, cinco disparos fijos, frente a `programador-teleprompter`: `0 6-15 * * 1-5`, diez disparos horarios — la lectura de 2026-09-04 los llamó "solapados" sin comparar el detalle). Las tres rutinas de *este* proyecto están cada una sola, sin duplicado ni solape. **Ninguna acción pendiente del dueño sobre las rutinas de teleprompter** — si quiere, puede revisar por separado si `centro-estudios-sw` tiene su propio problema de nomenclatura o rutinas duplicadas, pero es asunto de ese otro repositorio, fuera del alcance de este documento. **Nota histórica (2026-09-09):** el auditor había registrado por separado (`auditoriacontinua.md` #21, severidad alta) lo que parecía una reescritura del historial de `develop`; el programador lo investigó y confirmó que es un falso positivo del `git clone --depth` de cada contenedor efímero, sin relación con este bloqueo — se deja constancia aquí para que quede todo en un solo sitio. | **RESUELTO 2026-09-10** — diagnóstico corregido; no hay duplicado real para teleprompter |

---

## 4. INCIDENTES DE DEPLOY

> Cada vez que una instalación de la skill rompa el health check: qué pasó, qué commit lo causó, cómo se revirtió, qué se aprendió.

| Fecha | Commit causante | Síntoma | Resolución | Lección |
|-------|-----------------|---------|------------|---------|
| —     | Sin incidentes  | —       | —          | —       |

---

## 5. TAREAS AUTOPROPUESTAS (P-XX)

> Registrar aquí cada P-XX ANTES de implementarla (§0.3). El dueño veta con DESCARTAR o REVERTIR en la última columna.

| ID | Descripción | Motivo / valor esperado (incl. `origen: auditoría #N` si aplica) | Estado | Veto del dueño |
|----|-------------|-------------------------------------------------------------------|--------|----------------|
| P-01 | Acotar `.gitignore`: dejar de ignorar `assets/` y `fixtures/` completos | `origen: auditoría #2` (severidad alta). Con las reglas anteriores quedaban fuera del repo los logotipos de marca, los tres guiones de calibración y —en cuanto existan— las plantillas del reproductor y el fixture del health check, con lo que la CI de T-04 no podría reproducir la verificación. Sustituidas por reglas finas que siguen excluyendo lo generado. | **COMPLETADA** 2026-08-31 |  |
| P-02 | Corregir en `revalidacion.py` la pérdida silenciosa de una edición manual cuando coincide, en la misma revalidación, con la aceptación de una partición de respiración sobre el mismo bloque | `origen: auditoría #9` (severidad alta). Rompía el invariante (c) («la edición manual manda») en ese cruce concreto, sin aviso ni test que lo detectara — el dueño podía perder una corrección de texto sin saberlo. Atendida como urgente antes de T-23, según §0.1/§0.3. | **COMPLETADA** 2026-09-02 |  |
| P-03 | Corregir en `revalidacion.py` la duplicación de contenido en una revalidación posterior a un conflicto edición/partición ya pospuesto (P-02), cuando el dueño no vuelve a tocar el documento | `origen: auditoría #14` (severidad alta). El límite que P-02 había dejado documentado como "un fragmento de texto sin editar" resultó ser, verificado con reproducción de código, una duplicación real de contenido en `guion-escenas.md` sin ningún aviso — rompía el invariante (c) por desajuste de esquema de identidad entre pasadas. Atendida como urgente antes de R-01, según §0.1/§0.3. | **COMPLETADA** 2026-09-03 |  |
| P-04 | Endurecer el cierre de `#14`: lectura tolerante de la disposición persistida, persistir solo las particiones realmente pospuestas, incidencia cuando las anclas del documento no son las previstas, y corregir el mensaje del conflicto edición/partición | `origen: auditoría #14` (ya cerrado por P-03, que es correcto). Tres grietas alrededor: (1) `estado.validacion` no se valida al cargar, así que basura en `particiones_pospuestas` tiraba la revalidación entera en vez de degradar; (2) se persistía el conjunto sin filtrar de bloques editados, no el de particiones pospuestas, dejando en `estado.json` índices que nunca tuvieron nada que posponer; (3) **un `estado.json` anterior a P-03, justo en mitad de un conflicto, reproduce el #14 tal cual y en silencio** — sin la clave persistida, la reconstrucción vuelve a ser optimista. Además el aviso del conflicto invitaba a «revalidar sin tocar ese bloque» para materializar la partición, que es justo lo que no funciona: lo hace retirar la edición, como demuestra el test que dejó P-03. | **COMPLETADA** 2026-09-03 |  |
| P-05 | `instalar_skill.py` deja de guardar la copia de seguridad DENTRO de `~/.claude/skills/`; pasa a `~/.claude/teleprompter-copias-de-seguridad/` | **Detectado en vivo en la máquina del dueño** al reinstalar la skill en esta misma sesión: Claude Code registra como skill toda subcarpeta de `~/.claude/skills/` que tenga un `SKILL.md`, así que `teleprompter.bak-<marca>` apareció en la lista de skills disponibles **como una segunda `teleprompter`, con nombre y descripción idénticos**, compitiendo con la real en la selección. Cada reinstalación añadía una. No es cosmético: degrada la funcionalidad principal de la skill justo cuando el dueño va a usarla. La copia de la instalación de hoy se movió a mano fuera de `skills/`; el arreglo evita que vuelva a pasar. | **COMPLETADA** 2026-09-03 |  |
| P-06 | Extender la nota de `DEVELOPERS.md`/`SKILL.md` que ya cubre el binario "pelado" de `ruff`/`mypy`/`pytest` (R-15, `origen: auditoría #22`) para que también cubra la **instalación** (`pip install -r requirements-dev.txt` sin `python3 -m`), no solo la invocación | `origen: auditoría #28` (baja, infraestructura). Formalizado tras diez sesiones consecutivas resolviendo el mismo síntoma sin que quedara documentado: el `pip` pelado de los contenedores de nube de este proyecto instala contra Python 3.13 en vez del 3.11.x real, dejando las tres redes de tipos/estilo/tests en rojo con `No module named mypy/ruff/pytest` hasta reinstalar con `python3 -m pip install -r requirements-dev.txt`. Cola de tareas vacía tras R-24 (§1), hallazgo de severidad baja con recomendación de cierre ya escrita por el propio auditor: aprovechado como P-XX de esta sesión en vez de esperar a que el PM lo convierta en R-XX. Alcance puramente documental, sin tocar `scripts/`, `tests/` ni `assets/`. | **COMPLETADA** 2026-10-07 |  |

---

## 6. PREGUNTAS ABIERTAS PARA EL DUEÑO

> Decisiones que los agentes no pueden tomar. El dueño responde en la última columna.

| # | Pregunta | Tarea | Respuesta |
|---|----------|-------|-----------|
| 1 | ¿Confirmas 120 ppm como ritmo base, o prefieres el ppm implícito que se deduce de las duraciones objetivo de tus propios encabezados (T-12 lo calcula)? | T-12 | **ppm implícito de cada guión** (2026-08-31). Se deduce como valor único por guión, no por escena, para no anular el aviso de desviación. Respaldo 120 ppm si el guión no trae duraciones objetivo o el valor cae fuera de 90–180. → §0.2 y T-12. |
| 2 | ¿Qué nivel de encabezado usas hoy como escena en tus guiones (`#`, `##` o `###`), o prefieres que se detecte cada vez? | T-08 | *Respondida por evidencia (2026-08-31):* nivel `##` con patrón `BLOQUE N — <título> (m:ss – m:ss)`. Confirma solo si algún guión tuyo se sale de este patrón. |
| 3 | Tus guiones ya usan una convención estable (`**LOCUCIÓN**` en cita de bloque, `**EN PANTALLA**`, `**NOTA**`). ¿La fijamos como contractual, de modo que la skill deje de inferir y avise cuando un guión se salga de ella? | T-10 | **Contractual, con aviso** (2026-08-31). Los rótulos mandan; una escena sin rótulo se procesa infiriendo y se señala como desviación, nunca se convierte en error. → §0.2, T-09 y T-10. |
| 4 | Alcance de las reescrituras: ¿solo normalización a forma dicha y respiración, o también estilo (anglicismos, estructuras difíciles)? | T-15 | **Solo forma dicha y respiración** (2026-08-31). Cacofonías, trabalenguas, anglicismos y estructuras difíciles se avisan pero no se reescriben. Ampliar el alcance es decisión del dueño, no una P-XX. → §0.2, T-14 y T-15. |
| 5 | ¿El `.pdf` debe llevar la marca 480 en versión oscura (pantalla) o clara (impresión en papel)? | T-28 | **Clara, fondo blanco** (2026-08-31), alineado con la guía de `480-branded-pptx`. Uso: documento de repaso y, llegado el caso, entregable a terceros → una escena por página, locución como prosa legible y bandera `--para-terceros` que omite notas internas. → T-28 y T-29. |
| 6 | La guía de marca dice **Poppins** («familia oficial») y el `SKILL.md` de `480-branded-pptx` dice **Figtree** («familia obligatoria»). ¿Cuál manda? | T-28, T-29 | **Poppins** (2026-08-31): manda la guía de marca. El PDF sale en Poppins y el brief de T-29 se la pide también a la skill de marca, para que los dos documentos coincidan. Clave `tipografia_marca`. |
| 7 | **La rama de trabajo del protocolo no existe.** El repo está en `develop`, con `master` y remoto `origin` en GitHub; el protocolo decía `main`. | §0.1 · `origen: auditoría #1` | **`develop`** (2026-08-31). Los agentes commitean en `develop`; **`master` es del dueño**, que hace el merge manualmente. Protocolo actualizado (hoja de ruta v1.2, §0.1 y §0.2) y prompts de los tres agentes corregidos. |
| 8 | **Poppins no está instalada en esta máquina** (Figtree sí, Montserrat no). ¿Instalas Poppins, o cambiamos a Figtree? | T-28, T-29 · `origen: auditoría #3` | **Poppins instalada** (2026-08-31). Verificado: 5 archivos — Bold, SemiBold, Medium, Regular y Light —, que cubren toda la escala tipográfica de la guía de marca. La decisión se mantiene y ahora sí es efectiva. |
| 9 | **T-24 depende del clicker Bluetooth, que el dueño no tiene.** ¿Se bloquea la tarea entera (y con ella T-25 y T-26, que dependen de ella en cascada) o se parte? | T-24, T-25, T-26 | **Partirla** (2026-09-02). El clicker se identifica como un teclado corriente, así que el mapa completo, el antirrebote y la ayuda `?` son implementables y testeables sin hardware; lo único que exige el mando físico es saber qué botón manda qué tecla. **T-24 se implementa con alcance reducido** (requisitos 1, 3, 4 y la mitad software del 2) y **la calibración sale a T-24b, BLOQUEADA hasta nuevo aviso del dueño**. FASE B4 continúa: T-25 y T-26 no se bloquean. **Nota del mismo día:** la sesión de nube de T-24 corrió en paralelo sin conocer esta decisión y entregó exactamente ese alcance, así que T-24 quedó COMPLETADA y la decisión no revierte nada — solo formaliza T-24b. → §1, §3.5 y §7. |
| 10 | **El paquete de `480-branded-pptx` sigue sin estar disponible.** ¿Se bloquea T-29 (y con ella T-30, T-31, T-32 y T-33 en cascada)? | T-29, T-30 | **No se bloquea** (2026-09-02). T-29 ya está especificada para funcionar con la skill de marca ausente: su requisito 4 y su criterio de aceptación exigen que se generen `tarjetas.json` y el brief, que la salida se marque latente y que no falle. Se implementa entera; **solo la generación real del `.pptx` queda latente** hasta que el dueño aporte el paquete (bloqueo §3.2). → §1, §3.2 y §7. |
| 11 | El auditor (`auditoriacontinua.md` #24, 2026-09-16) señala que la prosa de "Cola de producto" de `ROADMAP_PRODUCTO.md` lleva reconfirmaciones enteras desactualizada tras completarse una R-XX, y sugiere que el propio ciclo de reconfirmación del Programador quede autorizado a corregirla por sí solo cuando se limite a reflejar un estado que este §1 ya registra como `COMPLETADA` (sin ninguna decisión de producto nueva de por medio), en vez de esperar al siguiente ciclo de PM completo. Es un cambio de quién escribe en qué documento (§0.4 de `HOJA_DE_RUTA.md`), protocolo que solo cambia el dueño — el PM no puede concedérselo por su cuenta. ¿Autorizas esa excepción puntual (solo prosa de estado ya reflejado en §1, nunca una decisión de producto), o prefieres que la prosa siga esperando al siguiente ciclo de PM? | §0.4, `ROADMAP_PRODUCTO.md` | *(pendiente)* |
| 12 | El auditor (`auditoriacontinua.md` #30, 2026-10-10) señala que la rutina programada "Programador" dispara en cron horario durante toda la jornada (nueve disparos, `07:15` a `15:15`) y repite el protocolo completo de verificación (clon, `pip install`, las cuatro redes: `mypy`/`ruff`/`pytest`/`verificar_salidas.py --fixture`) en cada reconfirmación aunque §1 esté vacío de tareas `PENDIENTE`, con un coste de cómputo que se acumula mientras el ritmo de apertura de R-XX (aprox. una por jornada) sea mucho más lento que el cron horario. Propone dos remedios alternativos, ninguno ejecutable por el propio Programador ni por el PM sin autorización: (a) espaciar el cron de la rutina "Programador" a un ritmo más cercano al de apertura real de trabajo (cambio de configuración de la rutina, fuera del repositorio); o (b) añadir al protocolo (`HOJA_DE_RUTA.md` §0.1, que solo cambia el dueño) una comprobación barata de "cola vacía" — leer solo §1 de `SEGUIMIENTO.md` — que permita terminar la sesión sin ejecutar `scripts/ci.py`/`verificar_salidas.py --fixture` cuando no hay ninguna R-XX/T-XX `PENDIENTE` ni hallazgo de severidad alta que atender. ¿Cuál de las dos prefieres, alguna combinación de ambas, o ninguna (aceptar el coste actual como el precio de la cadencia horaria)? | §0.1, cadencia de la rutina "Programador" | *(pendiente)* |

---

## 7. DESVIACIONES RESPECTO A LA HOJA DE RUTA ORIGINAL

> Resumen consolidado para comparar contra `HOJA_DE_RUTA.md` de un vistazo.

| Fecha | Tarea | Desviación | Motivo |
|-------|-------|-----------|--------|
| 2026-08-31 | T-00 | Se trabajó y se commiteó en `develop`, no en `main` como fijaba §0.1 | **Desviación cerrada el mismo día:** el dueño resolvió §6.7 confirmando `develop` como rama de trabajo y `master` como suya para el merge manual. El protocolo se actualizó (hoja de ruta v1.2) y a partir de ahí `develop` deja de ser una desviación: es la norma. |
| 2026-08-31 | T-00 | No se ejecutó `git init` | Ya estaba hecho. El resto de la tarea se cumplió íntegro. |
| 2026-09-02 | T-24 | La tarea se parte en dos: **T-24** (mapa de teclado, antirrebote, ayuda `?`) y **T-24b** (calibración del clicker físico, BLOQUEADA). La hoja de ruta la define como una sola tarea | **Decisión del dueño** (§6.9): no dispone de clicker. Bloquear T-24 entera habría bloqueado en cascada T-25 y T-26 y parado toda FASE B4, cuando la mitad software es implementable y testeable sin hardware. `HOJA_DE_RUTA.md` no se modifica (es inmutable): la spec de T-24b es el requisito 2 de T-24 en su mitad de verificación física. La sesión de nube de T-24, en paralelo y sin conocer la decisión, entregó ese mismo alcance por su cuenta: T-24 queda COMPLETADA y la desviación se reduce a la existencia de T-24b. |
| 2026-09-02 | T-29 | Ninguna desviación de la spec; se deja constancia de que **NO se bloquea** pese a seguir sin el paquete de marca | **Decisión del dueño** (§6.10). Se registra aquí porque la nota «Bloqueo humano» de T-29 en la hoja de ruta podía leerse como motivo para marcarla BLOQUEADA, cuando su propio requisito 4 y su criterio de aceptación exigen justo lo contrario: entregar el código completo con la salida latente. |
| 2026-08-31 | T-00 | No se hizo push al remoto | El protocolo §0.1 contemplaba push porque en un proyecto web equivale a desplegar. Aquí el despliegue es la instalación local de la skill (T-32) y publicar en GitHub es una acción hacia fuera. **Incorporado a la norma en v1.2:** no se hace push sin autorización explícita del dueño. Deja de ser desviación. |
