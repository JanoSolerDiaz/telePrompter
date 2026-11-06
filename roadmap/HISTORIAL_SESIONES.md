# HISTORIAL DE SESIONES — teleprompter

> Bitácora **append-only** de sesiones (antiguo §8 de SEGUIMIENTO). La más reciente arriba.
> Cada entrada referencia las filas de decisión añadidas en `DECISIONES_TECNICAS.md` y los
> cambios de estado en §1 de `SEGUIMIENTO.md` (consistencia cruzada).
>
> **Rotación:** mantener en línea las ~15 sesiones más recientes; archivar el resto por mes en
> `roadmap/HISTORIAL_SESIONES/AAAA-MM.md` y dejar aquí, al inicio, un índice de los meses archivados.

## Meses archivados
- `2026-08` (agosto de 2026): 1 sesión — `roadmap/HISTORIAL_SESIONES/2026-08.md`
- `2026-09` (septiembre de 2026): 266 sesiones — `roadmap/HISTORIAL_SESIONES/2026-09.md`
- `2026-10` (octubre de 2026): 251 sesiones — `roadmap/HISTORIAL_SESIONES/2026-10.md`
- `2026-11` (noviembre de 2026): 29 sesiones — `roadmap/HISTORIAL_SESIONES/2026-11.md`

---

## Plantilla por sesión (copiar y rellenar, la más reciente arriba)

```
### Sesión YYYY-MM-DD HH:MM
**Tarea(s):** T-XX / R-XX / P-XX
**Estado resultante:** EN CURSO / COMPLETADA / DESPLEGADA EN PRODUCCIÓN / BLOQUEADA
**Commits a develop:** <hashes y mensajes>
**Migraciones ejecutadas:** <archivo y resultado, o "ninguna">
**Archivos creados/modificados:** <lista>
**Verificaciones pre-push:** tipos ✅/❌ · lint ✅/❌ · tests ✅/❌ · build ✅/❌
**Health check post-deploy:** ✅/❌ (python scripts/verificar_salidas.py --fixture desde la copia instalada)
**Decisiones tomadas:** <referencia a las filas añadidas en DECISIONES_TECNICAS.md>
**Hallazgos del auditor atendidos:** <#N resueltos, o "ninguno">
**Hallazgos:** <bugs, deuda técnica o riesgos descubiertos>
**Tareas autopropuestas (P-XX):** <registradas/ejecutadas, con referencia a §5, o "ninguna">
**Próximo paso:** <qué debe hacer la siguiente sesión — incluye reverts pendientes>
```

---

### Sesión 2026-11-06 (345) — Ciclo de Programador: implementa R-47 (aviso de guion completo en el índice)

**Arranque.** Sesión en la nube (clon efímero, rutina "programador-teleprompter"). `git checkout
develop && git pull origin develop` reportó de nuevo "leaving 50 commits behind" y "divergent
branches" por el límite de profundidad superficial ya documentado (`#21` de `auditoriacontinua.md`,
`RESUELTO`), sin ninguna reescritura real de `develop`. Árbol de trabajo confirmado limpio (`git
status`) antes de actuar; resuelto con `git reset --hard origin/develop`. `pip install -r
requirements-dev.txt` (bare `pip`) instaló de nuevo contra Python 3.13 en vez del 3.11.18 real (mismo
síntoma de `#22`/`#28`/P-06); corregido con `python3 -m pip install -r requirements-dev.txt`.

**Registro de hallazgos y bloqueos revisado antes de elegir tarea.** §1 de `SEGUIMIENTO.md`: las 34
T-XX (`T-24b` `BLOQUEADA`, ajena al programador) y R-01 a R-46 `COMPLETADA`; R-47 (Oleada v35) única
fila `PENDIENTE`, abierta por el PM en la sesión anterior (344), ficha completa en
`ROADMAP_PRODUCTO.md`. `auditoriacontinua.md` revisado completo: ningún hallazgo `ABIERTO` de
severidad alta (`#42`/`#44` ya `RESUELTO`, reverificados de forma independiente por el propio auditor
en su pasada del 2026-11-06); `#45` (baja, nuevo: prosa obsoleta del sufijo de carpeta en
`HOJA_DE_RUTA.md` §0.2) y `#43` (baja) son deuda documental/técnica pura, candidatas a una futura P-XX,
no urgentes. `#24`/`#30` siguen `ABIERTO` a la espera del dueño; `#36` `ASUMIDO`. Ninguna urgencia:
se implementa R-47 siguiendo la cola normal.

**R-47 implementada.** `assets/reproductor/guion.js::renderizarIndice` gana la rama `else if
(pendientes === 0 && grabadas === 0)` del mismo `if` que ya decide el botón "Grabar siguiente
pendiente" (R-40), insertando `<p id="aviso-guion-completo">` con el texto fijo exacto de la ficha
cuando todas las escenas tienen ya una toma buena. CSS nuevo en `estilo.css`
(`.aviso-guion-completo`) reutiliza el borde y color de acento de `.btn-continuar` sin ser
interactivo. Sin campo nuevo en el JSON embebido, sin cambio en `scripts/reproductor.py` ni en
ningún otro módulo de `scripts/`. 7 tests nuevos en `tests/test_reproductor.py` (798→805).
Verificado también visualmente con Playwright/Chromium real sobre una fixture de dos escenas,
cubriendo el criterio de aceptación completo: pendiente → botón de R-40 sin aviso; grabada sin
buena (con o sin otra escena pendiente) → sin aviso, sin botón si ya no queda ninguna pendiente;
las dos con toma buena → aparece el aviso con el texto exacto, botón ausente, resumen de progreso
(R-39) y aviso de ritmo (R-45) intactos. Detalle completo de las decisiones de implementación en
`DECISIONES_TECNICAS.md`.

**Tarea(s):** R-47 (Oleada v35)
**Estado resultante:** COMPLETADA
**Commits a develop:** (pendiente de commitear al cierre de esta sesión)
**Migraciones ejecutadas:** ninguna
**Archivos creados/modificados:** `assets/reproductor/guion.js`, `assets/reproductor/estilo.css`,
`tests/test_reproductor.py`, `roadmap/SEGUIMIENTO.md`, `roadmap/DECISIONES_TECNICAS.md`,
`roadmap/HISTORIAL_SESIONES.md`
**Verificaciones pre-push:** tipos ✅ (mypy, 72 archivos) · lint ✅ (ruff check) · tests ✅ (805/805,
798 previos + 7 nuevos) · build ✅ (`verificar_salidas.py --fixture`, diecinueve etapas en `OK`),
todo ejecutado sobre el intérprete real (3.11.18)
**Health check post-deploy:** no aplica (sesión de nube, sin instalación local de la skill)
**Decisiones tomadas:** `DECISIONES_TECNICAS.md`, tres filas "R-47 (implementación)", 2026-11-06.
**Hallazgos del auditor atendidos:** ninguno nuevo cerrado en esta sesión (sin hallazgo urgente que
atender); `#42`/`#44` ya `RESUELTO` por P-13/P-14 en sesiones anteriores.
**Hallazgos:** ninguno nuevo.
**Tareas autopropuestas (P-XX):** ninguna (cola normal, sin urgencia).
**Próximo paso:** el siguiente ciclo de Product Manager debe archivar la Oleada v35 (R-47) en
`ROADMAP_HISTORICO.md` y abrir la siguiente, releyendo `auditoriacontinua.md` completo y
`roadmap/FEEDBACK.md` antes de decidir.

---

### Sesión 2026-11-05 (344) — Ciclo de Product Manager: archiva Oleada v34 (R-46) y abre R-47 (Oleada v35)

**Tarea(s):** PM — gestión de roadmap (ninguna T-XX/R-XX implementada, no toca `scripts/`/`tests/`/`assets/`)
**Estado resultante:** COMPLETADA (gestión de roadmap)
**Commits a develop:** (pendiente de commitear al cierre de esta sesión)
**Migraciones ejecutadas:** ninguna
**Archivos creados/modificados:** `roadmap/ROADMAP_PRODUCTO.md`, `roadmap/ROADMAP_HISTORICO.md`,
`roadmap/SEGUIMIENTO.md`, `roadmap/DECISIONES_TECNICAS.md`, `roadmap/HISTORIAL_SESIONES.md`
**Verificaciones pre-push:** tipos — (sin cambio de código) · lint — (sin cambio de código) · tests —
(sin cambio de código, 798/798 ya en verde desde la sesión anterior) · build — (sin cambio de código)
**Health check post-deploy:** no aplica (sesión de nube, sin instalación local; ninguna salida tocada)
**Decisiones tomadas:** `DECISIONES_TECNICAS.md`, fila "PM (archiva Oleada v34, abre R-47 como Oleada
v35)", 2026-11-05.
**Hallazgos del auditor atendidos:** ninguno nuevo cerrado por el PM; `#42` y `#44` ya resueltos en
código por P-13/P-14 (Programador, misma jornada), pendientes solo de reverificación del auditor;
`#43` (baja, deuda técnica del validador de auto-contención) dejado explícitamente como candidato a
una futura P-XX del Programador, no convertido en R-XX (no es producto/arquitectura); `#24`/`#30`
siguen `ABIERTO`, de gobernanza pura, a la espera de la respuesta del dueño a `#11`/`#12` de §6.
**Hallazgos:** ninguno nuevo. `roadmap/FEEDBACK.md` revisado completo: sigue con su única fila de
plantilla vacía, sin ninguna entrada `nuevo` que incorporar al roadmap — el bloqueo #7 de §3 (grabar
un curso completo) sigue abierto, ahora 63 días desde que T-32 lo dejó listo para grabar.
**Tareas autopropuestas (P-XX):** ninguna registrada por el PM en esta sesión (el PM no implementa).
**Próximo paso:** la siguiente sesión de Programador debe implementar R-47 (Oleada v35, ficha completa
en `ROADMAP_PRODUCTO.md`): avisar en el índice del reproductor, cuando todas las escenas tengan ya una
toma marcada como buena, de que el guion está listo para generar las salidas de montaje (T-30). Sin
migración, sin campo nuevo en el JSON embebido, cambio enteramente en
`assets/reproductor/guion.js`/`estilo.css`. Tras implementarla, el siguiente ciclo de PM debe archivar
la Oleada v35 en `ROADMAP_HISTORICO.md` y abrir la siguiente. Releer `auditoriacontinua.md` completo
(hasta su pasada vigente) y `roadmap/FEEDBACK.md` antes de decidir cualquier R-XX nueva.

---

### Sesión 2026-11-05 (343) — Ciclo de Programador: P-14, rotación mensual de `HISTORIAL_SESIONES.md`

**Arranque.** Sesión en la nube (clon efímero, rutina "programador-teleprompter"). Mismo patrón que
las ocho reconfirmaciones anteriores de hoy: contenedor arrancado con `HEAD` desprendido sobre
`e3d0e71` (punta congelada del clon superficial `--depth 50` del 2026-10-30), mientras
`origin/develop` ya estaba en `c71b1fe` (sesión 342, hoy). `git checkout develop && git pull origin
develop` repitió "leaving 50 commits behind" y "divergent branches" por el mismo límite de
profundidad superficial ya documentado (`git merge-base` entre ambas puntas de 50 commits, vacío);
árbol de trabajo confirmado limpio (`git status`) antes de actuar, resuelto con `git reset --hard
origin/develop`. `pip install -r requirements-dev.txt` (bare `pip`) instaló de nuevo contra Python
3.13 en vez del 3.11.18 real (mismo síntoma de `#22`/`#28`/P-06); corregido con `python3 -m pip
install -r requirements-dev.txt`.

**Registro de hallazgos y bloqueos revisado antes de elegir tarea.** §1 de `SEGUIMIENTO.md`
confirmada de punta a punta: las 34 T-XX (`T-24b` `BLOQUEADA`, ajena al programador) y las 46 R-XX
están `COMPLETADA`; ninguna fila `PENDIENTE` ni `BLOQUEADA` ejecutable, el PM todavía no ha abierto
ninguna oleada tras R-46. `auditoriacontinua.md` completo: `#42` (alta) sigue `ABIERTO` solo a la
espera de que la próxima pasada del auditor reverifique el cierre ya hecho por P-13, sin exigir
ninguna acción nueva del Programador. De los hallazgos de severidad baja de la pasada del
2026-11-05, `#44` (`HISTORIAL_SESIONES.md` sin ninguna rotación pese a que su propia cabecera fija
la regla desde el origen — 553 sesiones/18 836 líneas en el momento de la auditoría, 562 en el
momento de esta sesión) es exactamente el mismo patrón que `#39` (resuelto por P-10) y `#40`
(resuelto por P-12): candidata directa a P-XX de esta sesión, sin esperar al PM. `#43` sigue
`ABIERTO`, baja, sin acción urgente; `#24`/`#30` siguen a la espera de la respuesta del dueño a
`#11`/`#12` de §6 (sin respuesta nueva: sesión automatizada, sin entrada de usuario en vivo); `#36`
sigue `ASUMIDO`; `#40` sigue pendiente solo de reverificación del auditor.

**P-14 registrada e implementada (§5).** Rotación de `roadmap/HISTORIAL_SESIONES.md` por mes, misma
regla que la propia cabecera del documento fija desde el origen. Las 547 sesiones más antiguas (todas
salvo las 15 más recientes) se mueven a cuatro archivos nuevos: `roadmap/HISTORIAL_SESIONES/2026-08.md`
(1 sesión), `2026-09.md` (266), `2026-10.md` (251) y `2026-11.md` (29), cada uno con cabecera propia
(alcance, recuento, fecha y motivo de archivado, puntero de vuelta). La "Plantilla por sesión" (sin
fecha propia, intercalada por accidente entre sesiones de septiembre desde 2026-09-29) se reubica al
principio del documento vigente, junto al índice de "Meses archivados" (antes `*(ninguno todavía)*`).
Verificado con un script de comparación propio antes de cerrar: los 562 bloques de sesión más el de
la plantilla aparecen exactamente una vez entre el documento vigente y los cuatro archivos, byte a
byte idénticos al original — cero pérdida, cero alteración de contenido. Un primer borrador de las
cabeceras de los archivos se escribió sin tildes por descuido propio; corregido en la misma sesión
antes de cerrar (regla dura §0.2, "todo en español"), re-verificado tras la corrección. Cero cambio
en `scripts/`, `tests/` ni `assets/`: ningún código depende de este documento. Detalle completo de las
decisiones en `DECISIONES_TECNICAS.md`.

**Verificación completa.** Las cuatro redes ejecutadas de forma independiente sobre el intérprete real
(3.11.18): `mypy .` limpio (72 archivos); `ruff check .` sin avisos; `pytest` **798/798 tests** en
verde (misma cifra que la sesión anterior, sin test nuevo ni roto, como corresponde a una tarea
puramente documental); `verificar_salidas.py --fixture` con las diecinueve etapas en `OK`.

**Cambios de estado (§1 de `SEGUIMIENTO.md`).** §5 gana la fila `P-14`, `COMPLETADA`. Sin cambio en
ninguna T-XX/R-XX (R-46 permanece `COMPLETADA`). Cabecera de `SEGUIMIENTO.md` actualizada ("Última
actualización") respetando la norma de P-10.

**Próximo paso.** Ninguna tarea de código pendiente. La siguiente sesión debe releer §1 de
`SEGUIMIENTO.md` y `auditoriacontinua.md` completo antes de decidir; si sigue sin T-XX/R-XX
`PENDIENTE` y sin hallazgo `ABIERTO` de severidad alta, repetir la reconfirmación habitual. Las
preguntas `#11`/`#12` de §6 siguen esperando respuesta del dueño; ningún agente puede resolverlas por
su cuenta.

---

### Sesión 2026-11-05 (342) — Ciclo de Programador: octava reconfirmación del día tras R-46, sin novedad de código

**Arranque.** Sesión en la nube (clon efímero, rutina "programador-teleprompter"). Mismo patrón que
la sesión 341 (hace unas horas) y que la nota histórica del 2026-09-09 (bloqueo #8 de
`SEGUIMIENTO.md` §3, hallazgo `#21` `RESUELTO` de `auditoriacontinua.md`): contenedor arrancado con
`HEAD` desprendido sobre `e3d0e71` (punta congelada del clon superficial `--depth 50` del 2026-10-30),
mientras `origin/develop` ya estaba en `0aab830` (sesión 341, hoy). `git checkout develop && git pull
origin develop` reportó de nuevo "leaving 50 commits behind" y "divergent branches" por el límite de
profundidad superficial (`git merge-base` entre ambas puntas de 50 commits vacío, sin antecesor común
dentro de la ventana), no por ninguna reescritura real de `develop` (sin `--force` en el tráfico real,
solo `fast-forward` de sesiones anteriores). Árbol de trabajo confirmado limpio (`git status`) antes
de actuar; resuelto con `git reset --hard origin/develop`, trivialmente seguro al no haber nada propio
que descartar.

Igual que las sesiones anteriores de hoy, `pip install -r requirements-dev.txt` (bare `pip`) instaló
`mypy`/`ruff`/`pytest` contra un intérprete distinto al que resuelve `python3` en este contenedor
(`pip --version` confirma Python 3.13 frente al 3.11.18 real; mismo síntoma de siempre, `#22`/`#28`/
P-06); corregido invocando `python3 -m pip install -r requirements-dev.txt`, tras lo cual las cuatro
redes se ejecutaron con las versiones correctas.

**Registro de hallazgos y bloqueos revisado antes de elegir tarea.** `auditoriacontinua.md` completo:
sin ninguna pasada de auditoría nueva desde `be05fc4` (2026-11-05, ya conocida por las sesiones
anteriores). `#42` (alta) sigue `ABIERTO` en el registro solo a la espera de que la próxima pasada del
auditor reverifique el cierre ya hecho por **P-13** (sesión 333, `68cf14d`) — reverificado de nuevo en
esta sesión leyendo `SKILL.md` directamente: la sección "Punto de entrada" sigue presente, con
`entrada.leer_guion`/`entrada.carpeta_salida_para` como primer paso del flujo; no exige una P-XX
nueva, es terreno exclusivo del auditor. `#43`/`#44` (baja) sin acción urgente, no convertibles en
tarea del Programador por su cuenta. `#30` (alta, de proceso/cómputo, no de las categorías que exigen
P-XX urgente) y `#24` (baja) siguen `ABIERTO`, ambos a la espera de la respuesta del dueño a `#11`/
`#12` de §6 (sin respuesta nueva: no hay entrada de usuario en vivo en esta sesión automatizada);
`#36` sigue `ASUMIDO`; `#40` `RESUELTO` (P-12), pendiente solo de reverificación del auditor.

**Ninguna tarea elegida.** §1 confirmada de punta a punta: las 34 T-XX (`T-24b` `BLOQUEADA`, ajena al
programador) y las 46 R-XX (hasta R-46) están `COMPLETADA`; §5 completa, P-01 a P-13. Ninguna fila
`PENDIENTE` ni `BLOQUEADA` ejecutable. El PM todavía no ha abierto ninguna oleada tras R-46.

**Verificación completa, sin cambios de código.** Las cuatro redes ejecutadas de forma independiente
sobre el intérprete real (3.11.18): `mypy .` limpio (72 archivos); `ruff check .` sin avisos; `pytest`
**798/798 tests** en verde (misma cifra que la sesión anterior, sin test nuevo ni roto);
`verificar_salidas.py --fixture` con las diecinueve etapas en `OK`, incluida la salida latente
esperada en este contenedor (`.pptx` sin la skill `480-branded-pptx` instalada) y las omisiones
esperadas sin parte de rodaje real. `git status` tras la verificación, limpio salvo los dos documentos
de registro que esta propia sesión actualiza.

**Cambios de estado (§1 de `SEGUIMIENTO.md`).** Ninguno: R-46 y P-13 permanecen `COMPLETADA`. Sin
decisiones nuevas en `DECISIONES_TECNICAS.md` (el incidente del clon superficial no es una decisión
técnica nueva, es la repetición exacta de un patrón ya documentado el 2026-09-09 y reconfirmado la
sesión anterior el 2026-11-05). Sin novedad en §3 (bloqueos), §6 (preguntas, `#11`/`#12` siguen
`(pendiente)`) ni §7 (desviaciones). Cabecera de `SEGUIMIENTO.md` actualizada ("Última actualización")
respetando la norma de P-10: solo el estado vigente, sin acumular la narrativa de esta sesión, que
vive aquí.

**Nota de cierre.** Octava reconfirmación de hoy de la rutina "programador-teleprompter" tras
P-13/R-46, sin ningún código que tocar: el patrón que motivó la escalada de `#30` a severidad alta
(cron horario repitiendo las cuatro redes con la cola vacía) sigue vigente mientras el dueño no
responda `#11`/`#12` de §6. Ninguna acción unilateral tomada sobre la cadencia de la rutina ni sobre
el protocolo: ambas son decisiones del dueño, no del Programador.

---

### Sesión 2026-11-05 (341) — Ciclo de Programador: séptima reconfirmación del día tras R-46, sin novedad de código

**Arranque.** Sesión en la nube (clon efímero, rutina "programador-teleprompter"). Contenedor
arrancado con `HEAD` desprendido sobre `e3d0e71` (punta de un clon superficial `--depth 50`
congelado desde el 2026-10-30, seis jornadas atrás), mientras `origin/develop` ya estaba en
`b9855a0` (sesión 340, hoy). `git checkout develop && git pull origin develop` no resolvió solo:
al traer el fetch, el límite de profundidad superficial hizo que el historial local de 50 commits y
el de origin de 50 commits no compartieran ningún antecesor común (`git merge-base` vacío pese a
tratarse de la misma rama), y git pidió reconciliar manualmente ramas "divergentes". Diagnosticado
como el mismo falso positivo de `git clone --depth` que ya documentó el programador el 2026-09-09
(nota histórica del bloqueo #8 de `SEGUIMIENTO.md` §3), no una reescritura real de `develop` (que
sigue intacta: `origin/develop` nunca se tocó con `--force`, el tráfico es solo `fast-forward` de
sesiones anteriores). Árbol de trabajo confirmado limpio (`git status`) antes de actuar, sin ningún
cambio local que perder; resuelto con `git reset --hard origin/develop`, trivialmente seguro al no
haber nada propio que descartar.

Igual que las seis sesiones anteriores de hoy, `pip install -r requirements-dev.txt` (bare `pip`)
instaló `mypy`/`ruff`/`pytest` contra un intérprete distinto al que resuelve `python3` en este
contenedor (`pip --version` confirma Python 3.13 frente al 3.11.18 real; mismo síntoma de siempre,
`#22`/`#28`/P-06); corregido invocando `python3 -m pip install -r requirements-dev.txt`, tras lo
cual las cuatro redes dieron `OK` con las versiones correctas.

**Registro de hallazgos y bloqueos revisado antes de elegir tarea.** `auditoriacontinua.md` completo:
sin ninguna pasada de auditoría nueva desde `be05fc4` (2026-11-05, ya conocida por las sesiones
anteriores). `#42` (alta) sigue `ABIERTO` en el registro solo a la espera de que la próxima pasada
del auditor reverifique el cierre ya hecho por **P-13** (sesión 333, `68cf14d`) — reverificado de
nuevo en esta sesión leyendo `SKILL.md` directamente: la sección "Punto de entrada" sigue presente,
con `entrada.leer_guion`/`entrada.carpeta_salida_para` como primer paso del flujo; no exige una P-XX
nueva, es terreno exclusivo del auditor. `#43`/`#44` (baja) sin acción urgente, no convertibles en
tarea del Programador por su cuenta. `#30` (alta, pero de proceso/cómputo, no de las categorías que
exigen P-XX urgente) y `#24` (baja) siguen `ABIERTO`, ambos a la espera de la respuesta del dueño a
`#11`/`#12` de §6 (sin respuesta nueva: no hay entrada de usuario en vivo en esta sesión
automatizada); `#36` sigue `ASUMIDO`; `#40` `RESUELTO` (P-12), pendiente solo de reverificación del
auditor. `ROADMAP_PRODUCTO.md` releído: su "Cola de producto" sigue describiendo R-46 como recién
abierta "sin implementarla" (prosa del ciclo de PM del 2026-11-04), desajustada contra §1 de
`SEGUIMIENTO.md` (R-46 ya `COMPLETADA`) — exactamente el patrón que describe `#24`, cuyo remedio
(autorizar al Programador a corregir esa prosa por su cuenta) sigue pendiente de la respuesta del
dueño a la pregunta `#11`; no se toca sin esa autorización.

**Ninguna tarea elegida.** §1 confirmada de punta a punta: las 34 T-XX (`T-24b` `BLOQUEADA`, ajena al
programador) y las 46 R-XX (hasta R-46) están `COMPLETADA`; §5 completa, P-01 a P-13. Ninguna fila
`PENDIENTE` ni `BLOQUEADA` ejecutable. El PM todavía no ha abierto ninguna oleada tras R-46.

**Verificación completa, sin cambios de código.** Las cuatro redes ejecutadas de forma independiente
sobre el intérprete real (3.11.18): `mypy .` limpio (72 archivos); `ruff check .` sin avisos;
`pytest` **798/798 tests** en verde (misma cifra que la sesión anterior, sin test nuevo ni roto);
`verificar_salidas.py --fixture` con las diecinueve etapas en `OK`, incluida la salida latente
esperada en este contenedor (`.pptx` sin la skill `480-branded-pptx` instalada) y las omisiones
esperadas sin parte de rodaje real; el `.pdf` se generó de verdad con Chrome/Edge headless. `git
status` tras la verificación, limpio salvo los dos documentos de registro que esta propia sesión
actualiza.

**Cambios de estado (§1 de `SEGUIMIENTO.md`).** Ninguno: R-46 y P-13 permanecen `COMPLETADA`. Sin
decisiones nuevas en `DECISIONES_TECNICAS.md` (nada no trivial que decidir en una sesión sin código;
el incidente del clon superficial diverge no es una decisión técnica nueva, es la repetición exacta
de un patrón ya documentado el 2026-09-09). Sin novedad en §3 (bloqueos), §6 (preguntas, `#11`/`#12`
siguen `(pendiente)`) ni §7 (desviaciones). Cabecera de `SEGUIMIENTO.md` actualizada ("Última
actualización") respetando la norma de P-10: solo el estado vigente, sin acumular la narrativa de
esta sesión, que vive aquí.

**Nota de cierre.** Séptima reconfirmación de hoy de la rutina "programador-teleprompter" tras
P-13/R-46, sin ningún código que tocar: el patrón que motivó la escalada de `#30` a severidad alta
(cron horario repitiendo las cuatro redes con la cola vacía) sigue vigente mientras el dueño no
responda `#11`/`#12` de §6. Ninguna acción unilateral tomada sobre la cadencia de la rutina ni sobre
el protocolo: ambas son decisiones del dueño, no del Programador.

---

### Sesión 2026-11-05 (340) — Ciclo de Programador: sexta reconfirmación del día tras R-46, sin novedad de código

**Arranque.** Sesión en la nube (clon efímero, rutina "programador-teleprompter"). Contenedor
arrancado con `HEAD` desprendido, resto de un contenedor anterior; `git checkout develop && git pull
origin develop` trajo en fast-forward trivial los commits ya fusionados hasta `488841b` (sesión 339:
quinta reconfirmación de hoy), árbol de trabajo limpio antes y después. Igual que las cinco sesiones
anteriores de hoy, `pip install -r requirements-dev.txt` (bare `pip`) instaló `mypy`/`ruff`/`pytest`
contra un intérprete distinto al que resuelve `python3` en este contenedor (mismo síntoma de siempre,
`#22`/`#28`/P-06); corregido invocando `python3 -m pip install -r requirements-dev.txt` (reinstala
`mypy==1.18.2`/`ruff==0.14.0`/`pytest==8.4.2` fijados en el fichero), tras lo cual las cuatro redes
dieron `OK` con las versiones correctas.

**Registro de hallazgos y bloqueos revisado antes de elegir tarea.** `auditoriacontinua.md` completo:
sin ninguna pasada de auditoría nueva desde `be05fc4` (2026-11-05, ya conocida por la sesión anterior).
`#42` (alta) sigue `ABIERTO` en el registro solo a la espera de que la próxima pasada del auditor
reverifique el cierre ya hecho por **P-13** (sesión 333, `68cf14d`) — reverificado de nuevo en esta
sesión leyendo `SKILL.md` directamente: la sección "Punto de entrada" sigue presente, con
`entrada.leer_guion`/`entrada.carpeta_salida_para` como primer paso del flujo; no exige una P-XX
nueva, es terreno exclusivo del auditor. `#43`/`#44` (baja) sin acción urgente, no convertibles en
tarea del Programador por su cuenta. `#30` (alta, pero de proceso/cómputo, no de las categorías que
exigen P-XX urgente) y `#24` (baja) siguen `ABIERTO`, ambos a la espera de la respuesta del dueño a
`#11`/`#12` de §6 (sin respuesta nueva: no hay entrada de usuario en vivo en esta sesión
automatizada); `#36` sigue `ASUMIDO`; `#40` `RESUELTO` (P-12), pendiente solo de reverificación del
auditor.

**Ninguna tarea elegida.** §1 confirmada de punta a punta: las 34 T-XX (`T-24b` `BLOQUEADA`, ajena al
programador) y las 46 R-XX (hasta R-46) están `COMPLETADA`; §5 completa, P-01 a P-13. Ninguna fila
`PENDIENTE` ni `BLOQUEADA` ejecutable. El PM todavía no ha abierto ninguna oleada tras R-46;
`roadmap/ROADMAP_PRODUCTO.md` confirmado sin ningún hito pendiente fuera de lo ya reflejado en §1.

**Verificación completa, sin cambios de código.** Las cuatro redes ejecutadas de forma independiente
sobre el intérprete real (3.11.18): `mypy scripts/ tests/` limpio (72 archivos); `ruff check scripts/
tests/` sin avisos; `pytest` **798/798 tests** en verde (misma cifra que la sesión anterior, sin test
nuevo ni roto); `verificar_salidas.py --fixture` con las diecinueve etapas en `OK`, incluida la salida
latente esperada en este contenedor (`.pptx` sin la skill `480-branded-pptx` instalada) y las
omisiones esperadas sin parte de rodaje real; el `.pdf` se generó de verdad con Chrome/Edge headless.
`git status` tras la verificación, limpio salvo los dos documentos de registro que esta propia sesión
actualiza.

**Cambios de estado (§1 de `SEGUIMIENTO.md`).** Ninguno: R-46 y P-13 permanecen `COMPLETADA`. Sin
decisiones nuevas en `DECISIONES_TECNICAS.md` (nada no trivial que decidir en una sesión sin código).
Sin novedad en §3 (bloqueos), §6 (preguntas, `#11`/`#12` siguen `(pendiente)`) ni §7 (desviaciones).
Cabecera de `SEGUIMIENTO.md` actualizada ("Última actualización") respetando la norma de P-10: solo
el estado vigente, sin acumular la narrativa de esta sesión, que vive aquí.

**Nota de cierre.** Sexta reconfirmación de hoy de la rutina "programador-teleprompter" tras
P-13/R-46, sin ningún código que tocar: el patrón que motivó la escalada de `#30` a severidad alta
(cron horario repitiendo las cuatro redes con la cola vacía) sigue vigente mientras el dueño no
responda `#11`/`#12` de §6. Ninguna acción unilateral tomada sobre la cadencia de la rutina ni sobre
el protocolo: ambas son decisiones del dueño, no del Programador.

---

### Sesión 2026-11-05 (339) — Ciclo de Programador: quinta reconfirmación del día tras R-46, sin novedad de código

**Arranque.** Sesión en la nube (clon efímero, rutina "programador-teleprompter"). Contenedor
arrancado con `HEAD` desprendido (48 commits por delante de cualquier rama local, resto de un
contenedor anterior); `git checkout develop && git pull origin develop` trajo en fast-forward
trivial los commits ya fusionados hasta `fb19165` (sesión 338: cuarta reconfirmación de hoy), árbol
de trabajo limpio antes y después. Igual que las cuatro sesiones anteriores de hoy, `pip install -r
requirements-dev.txt` (bare `pip`) instaló `mypy`/`ruff`/`pytest` contra un intérprete distinto al
que resuelve `python3` en este contenedor (mismo síntoma de siempre, `#22`/`#28`/P-06); corregido
invocando `python3 -m pip install -r requirements-dev.txt` (reinstala `mypy==1.18.2`/`ruff==0.14.0`/
`pytest==8.4.2` fijados en el fichero), tras lo cual las cuatro redes dieron `OK` con las versiones
correctas.

**Registro de hallazgos y bloqueos revisado antes de elegir tarea.** `auditoriacontinua.md` completo
(filas de estado y narrativa de la pasada del 2026-11-05, `be05fc4`): ningún hallazgo nuevo desde la
sesión anterior. `#42` (alta) sigue `ABIERTO` en el registro solo a la espera de que la próxima
pasada del auditor reverifique el cierre ya hecho por **P-13** (sesión 333, `68cf14d`) —
reverificado de nuevo en esta sesión leyendo `SKILL.md` directamente: la sección "Punto de entrada"
sigue presente, con `entrada.leer_guion`/`entrada.carpeta_salida_para` como primer paso del flujo; no
exige una P-XX nueva, es terreno exclusivo del auditor. `#43`/`#44` (baja) sin acción urgente, no
convertibles en tarea del Programador por su cuenta (`#44` en particular es un hallazgo de archivado
documental sin invitación explícita a una P-XX, a diferencia de `#39`/`#40`). `#30` (alta, pero de
proceso/cómputo, no de las categorías que exigen P-XX urgente — pérdida de texto, corrupción de
estado, rotura del reproductor o de su auto-contención, seguridad) y `#24` (baja) siguen `ABIERTO`,
ambos a la espera de la respuesta del dueño a `#11`/`#12` de §6 (sin respuesta nueva: no hay entrada
de usuario en vivo en esta sesión automatizada); `#36` sigue `ASUMIDO`; `#40` `RESUELTO` (P-12),
pendiente solo de reverificación del auditor.

**Ninguna tarea elegida.** §1 confirmada de punta a punta: las 34 T-XX (`T-24b` `BLOQUEADA`, ajena al
programador) y las 46 R-XX (hasta R-46) están `COMPLETADA`; §5 completa, P-01 a P-13. Ninguna fila
`PENDIENTE` ni `BLOQUEADA` ejecutable. El PM todavía no ha abierto ninguna oleada tras R-46;
`roadmap/ROADMAP_PRODUCTO.md` confirmado sin ningún hito pendiente fuera de lo ya reflejado en §1.

**Verificación completa, sin cambios de código.** Las cuatro redes ejecutadas de forma independiente
sobre el intérprete real (3.11.18): `mypy scripts/ tests/` limpio (72 archivos); `ruff check scripts/
tests/` sin avisos; `pytest` **798/798 tests** en verde (misma cifra que la sesión anterior, sin test
nuevo ni roto); `verificar_salidas.py --fixture` con las diecinueve etapas en `OK`, incluida la salida
latente esperada en este contenedor (`.pptx` sin la skill `480-branded-pptx` instalada) y las
omisiones esperadas sin parte de rodaje real; el `.pdf` se generó de verdad con Chrome/Edge headless.
`git status` tras la verificación, limpio salvo los dos documentos de registro que esta propia sesión
actualiza.

**Cambios de estado (§1 de `SEGUIMIENTO.md`).** Ninguno: R-46 y P-13 permanecen `COMPLETADA`. Sin
decisiones nuevas en `DECISIONES_TECNICAS.md` (nada no trivial que decidir en una sesión sin código).
Sin novedad en §3 (bloqueos), §6 (preguntas, `#11`/`#12` siguen `(pendiente)`) ni §7 (desviaciones).
Cabecera de `SEGUIMIENTO.md` actualizada ("Última actualización") respetando la norma de P-10: solo
el estado vigente, sin acumular la narrativa de esta sesión, que vive aquí.

**Nota de cierre.** Quinta reconfirmación de hoy de la rutina "programador-teleprompter" tras
P-13/R-46, sin ningún código que tocar: el patrón que motivó la escalada de `#30` a severidad alta
(cron horario repitiendo las cuatro redes con la cola vacía) sigue vigente mientras el dueño no
responda `#11`/`#12` de §6. Ninguna acción unilateral tomada sobre la cadencia de la rutina ni sobre
el protocolo: ambas son decisiones del dueño, no del Programador.

---

### Sesión 2026-11-05 (338) — Ciclo de Programador: cuarta reconfirmación del día tras R-46, sin novedad de código

**Arranque.** Sesión en la nube (clon efímero, rutina "programador-teleprompter"). Contenedor
arrancado con `HEAD` desprendido (47 commits por delante de cualquier rama local, resto de un
contenedor anterior); `git checkout develop && git pull origin develop` trajo en fast-forward
trivial los commits ya fusionados hasta `0da1d67` (sesión 337: tercera reconfirmación de hoy), árbol
de trabajo limpio antes y después. Igual que las tres sesiones anteriores de hoy, `pip install -r
requirements-dev.txt` (bare `pip`, resuelto contra Python 3.13 vía `/usr/lib/python3/dist-packages`)
instaló `mypy`/`ruff`/`pytest` contra un intérprete distinto al que resuelve `python3` en este
contenedor (3.11.18) — mismo síntoma de siempre (`#22`/`#28`/P-06); corregido invocando `python3 -m
pip install -r requirements-dev.txt` (reinstala `mypy==1.18.2`/`ruff==0.14.0`/`pytest==8.4.2` fijados
en el fichero), tras lo cual las cuatro redes dieron `OK` con las versiones correctas.

**Registro de hallazgos y bloqueos revisado antes de elegir tarea.** `auditoriacontinua.md` completo
(filas de estado y narrativa de la pasada del 2026-11-05, `be05fc4`): ningún hallazgo nuevo desde la
sesión anterior. `#42` (alta) sigue `ABIERTO` solo a la espera de que la próxima pasada del auditor
reverifique el cierre ya hecho por **P-13** (sesión 333, `68cf14d`) — no exige una P-XX nueva, es
terreno exclusivo del auditor. `#43`/`#44` (baja) sin acción urgente, no convertibles en tarea del
Programador por su cuenta. `#30` (alta, pero de proceso/cómputo, no de las categorías que exigen P-XX
urgente — pérdida de texto, corrupción de estado, rotura del reproductor o de su auto-contención,
seguridad) y `#24` (baja) siguen `ABIERTO`, ambos a la espera de la respuesta del dueño a `#11`/`#12`
de §6; `#36` sigue `ASUMIDO`; `#40` `RESUELTO` (P-12), pendiente solo de reverificación del auditor.

**Ninguna tarea elegida.** §1 confirmada de punta a punta: las 34 T-XX (`T-24b` `BLOQUEADA`, ajena al
programador) y las 46 R-XX (hasta R-46) están `COMPLETADA`; §5 completa, P-01 a P-13. Ninguna fila
`PENDIENTE` ni `BLOQUEADA` ejecutable. El PM todavía no ha abierto ninguna oleada tras R-46;
`roadmap/ROADMAP_PRODUCTO.md` confirmado sin ningún hito pendiente fuera de lo ya reflejado en §1.

**Verificación completa, sin cambios de código.** Las cuatro redes ejecutadas de forma independiente
sobre el intérprete real (3.11.18): `mypy scripts/ tests/` limpio (72 archivos); `ruff check scripts/
tests/` sin avisos; `pytest` **798/798 tests** en verde (misma cifra que la sesión anterior, sin test
nuevo ni roto); `verificar_salidas.py --fixture` con las diecinueve etapas en `OK`, incluida la salida
latente esperada en este contenedor (`.pptx` sin la skill `480-branded-pptx` instalada) y las
omisiones esperadas sin parte de rodaje real; el `.pdf` se generó de verdad con Chrome/Edge headless.
`git status` tras la verificación, limpio salvo los dos documentos de registro que esta propia sesión
actualiza.

**Cambios de estado (§1 de `SEGUIMIENTO.md`).** Ninguno: R-46 y P-13 permanecen `COMPLETADA`. Sin
decisiones nuevas en `DECISIONES_TECNICAS.md` (nada no trivial que decidir en una sesión sin código).
Sin novedad en §3 (bloqueos), §6 (preguntas, `#11`/`#12` siguen `(pendiente)`) ni §7 (desviaciones).
Cabecera de `SEGUIMIENTO.md` actualizada ("Última actualización") respetando la norma de P-10: solo
el estado vigente, sin acumular la narrativa de esta sesión, que vive aquí.

**Nota de cierre.** Cuarta reconfirmación de hoy de la rutina "programador-teleprompter" tras
P-13/R-46, sin ningún código que tocar: el patrón que motivó la escalada de `#30` a severidad alta
(cron horario repitiendo las cuatro redes con la cola vacía) sigue vigente mientras el dueño no
responda `#11`/`#12` de §6. Ninguna acción unilateral tomada sobre la cadencia de la rutina ni sobre
el protocolo: ambas son decisiones del dueño, no del Programador.

---

### Sesión 2026-11-05 (337) — Ciclo de Programador: tercera reconfirmación del día tras R-46, sin novedad de código

**Arranque.** Sesión en la nube (clon efímero, rutina "programador-teleprompter"). Contenedor
arrancado con `HEAD` desprendido (46 commits por delante de cualquier rama local, resto de un
contenedor anterior); `git checkout develop && git pull origin develop` trajo en fast-forward
trivial los commits ya fusionados hasta `f56c466` (sesión 336: segunda reconfirmación de hoy), árbol
de trabajo limpio antes y después. Igual que las dos sesiones anteriores de hoy, `pip install -r
requirements-dev.txt` (bare `pip`) instaló `mypy 2.3.1`/`ruff 0.16.9`/`pytest` (vía `uv tool`) contra
un intérprete distinto al que resuelve `python3` en este contenedor (mismo síntoma de siempre,
`#22`/`#28`/P-06: `mypy`/`ruff` del `PATH` dieron `No module named pytest`/una regla `UP042` nueva
ajena a la versión fijada); corregido invocando `python3 -m pip install -r requirements-dev.txt`
(reinstala `mypy==1.18.2`/`ruff==0.14.0`/`pytest==8.4.2` fijados en el fichero), tras lo cual las
cuatro redes dieron `OK` con las versiones correctas.

**Registro de hallazgos y bloqueos revisado antes de elegir tarea.** `auditoriacontinua.md` completo
(filas de estado y narrativa de la pasada del 2026-11-05, `be05fc4`): ningún hallazgo nuevo desde la
sesión anterior. `#42` (alta) sigue `ABIERTO` solo a la espera de que la próxima pasada del auditor
reverifique el cierre ya hecho por **P-13** (sesión 333, `68cf14d`) — no exige una P-XX nueva, es
terreno exclusivo del auditor. `#43`/`#44` (baja) sin acción urgente, no convertibles en tarea del
Programador por su cuenta. `#30` (alta, pero de proceso/cómputo, no de las categorías que exigen P-XX
urgente — pérdida de texto, corrupción de estado, rotura del reproductor o de su auto-contención,
seguridad) y `#24` (baja) siguen `ABIERTO`, ambos a la espera de la respuesta del dueño a `#11`/`#12`
de §6; `#36` sigue `ASUMIDO`; `#40` `RESUELTO` (P-12), pendiente solo de reverificación del auditor.

**Ninguna tarea elegida.** §1 confirmada de punta a punta: las 34 T-XX (`T-24b` `BLOQUEADA`, ajena al
programador) y las 46 R-XX (hasta R-46) están `COMPLETADA`; §5 completa, P-01 a P-13. Ninguna fila
`PENDIENTE` ni `BLOQUEADA` ejecutable. El PM todavía no ha abierto ninguna oleada tras R-46;
`roadmap/ROADMAP_PRODUCTO.md` confirmado sin ningún hito pendiente fuera de lo ya reflejado en §1.

**Verificación completa, sin cambios de código.** Las cuatro redes ejecutadas de forma independiente
sobre el intérprete real (3.11.18): `mypy scripts/ tests/` limpio (72 archivos); `ruff check scripts/
tests/` sin avisos; `pytest` **798/798 tests** en verde (misma cifra que la sesión anterior, sin test
nuevo ni roto); `verificar_salidas.py --fixture` con las diecinueve etapas en `OK`, incluida la salida
latente esperada en este contenedor (`.pptx` sin la skill `480-branded-pptx` instalada) y las
omisiones esperadas sin parte de rodaje real; el `.pdf` se generó de verdad con Chrome/Edge headless.
`git status` tras la verificación, limpio salvo los dos documentos de registro que esta propia sesión
actualiza.

**Cambios de estado (§1 de `SEGUIMIENTO.md`).** Ninguno: R-46 y P-13 permanecen `COMPLETADA`. Sin
decisiones nuevas en `DECISIONES_TECNICAS.md` (nada no trivial que decidir en una sesión sin código).
Sin novedad en §3 (bloqueos), §6 (preguntas, `#11`/`#12` siguen `(pendiente)`) ni §7 (desviaciones).
Cabecera de `SEGUIMIENTO.md` actualizada ("Última actualización") respetando la norma de P-10: solo
el estado vigente, sin acumular la narrativa de esta sesión, que vive aquí.

**Nota de cierre.** Tercera reconfirmación de hoy de la rutina "programador-teleprompter" tras
P-13/R-46, sin ningún código que tocar: el patrón que motivó la escalada de `#30` a severidad alta
(cron horario repitiendo las cuatro redes con la cola vacía) sigue vigente mientras el dueño no
responda `#11`/`#12` de §6. Ninguna acción unilateral tomada sobre la cadencia de la rutina ni sobre
el protocolo: ambas son decisiones del dueño, no del Programador.

---

### Sesión 2026-11-05 (336) — Ciclo de Programador: segunda reconfirmación del día tras R-46, sin novedad de código

**Arranque.** Sesión en la nube (clon efímero, rutina "programador-teleprompter"). `git checkout
develop && git pull origin develop` trajo en fast-forward trivial los commits ya fusionados hasta
`99e6489` (sesión 335: primera reconfirmación de hoy), árbol de trabajo limpio antes y después. Igual
que la sesión anterior, `pip install -r requirements-dev.txt` (bare `pip`) instaló `mypy`/`ruff`/
`pytest` contra un intérprete distinto al que resuelve `python3` en este contenedor (mismo síntoma de
siempre, `#22`/`#28`/P-06, reproducido de nuevo: `python3 scripts/ci.py` dio las tres redes de
tipos/estilo/tests en ROJO con `No module named mypy`/`ruff`/`pytest`); corregido invocando `python3
-m pip install -r requirements-dev.txt`, tras lo cual las cuatro redes dieron `OK`.

**Registro de hallazgos y bloqueos revisado antes de elegir tarea.** `auditoriacontinua.md` completo
(filas de estado y narrativa de la pasada del 2026-11-05, `be05fc4`): ningún hallazgo nuevo desde la
sesión anterior. `#42` (alta) sigue `ABIERTO` solo a la espera de que la próxima pasada del auditor
reverifique el cierre ya hecho por **P-13** (sesión 333, `68cf14d`) — no exige una P-XX nueva, es
terreno exclusivo del auditor. `#43`/`#44` (baja) sin acción urgente, no convertibles en tarea del
Programador por su cuenta. `#30` (alta, pero de proceso/cómputo, no de las categorías que exigen P-XX
urgente — pérdida de texto, corrupción de estado, rotura del reproductor o de su auto-contención,
seguridad) y `#24` (baja) siguen `ABIERTO`, ambos a la espera de la respuesta del dueño a `#11`/`#12`
de §6; `#36` sigue `ASUMIDO`; `#40` `RESUELTO` (P-12), pendiente solo de reverificación del auditor.

**Ninguna tarea elegida.** §1 confirmada de punta a punta: las 34 T-XX (`T-24b` `BLOQUEADA`, ajena al
programador) y las 46 R-XX (hasta R-46) están `COMPLETADA`; §5 completa, P-01 a P-13. Ninguna fila
`PENDIENTE` ni `BLOQUEADA` ejecutable. El PM todavía no ha abierto ninguna oleada tras R-46;
`roadmap/ROADMAP_PRODUCTO.md` confirmado sin ningún hito pendiente fuera de lo ya reflejado en §1.

**Verificación completa, sin cambios de código.** Las cuatro redes ejecutadas de forma independiente
sobre el intérprete real (3.11.18): `mypy scripts/ tests/` limpio (72 archivos); `ruff check scripts/
tests/` sin avisos; `pytest -v` **798/798 tests** en verde; `verificar_salidas.py --fixture` con las
diecinueve etapas en `OK`, incluida la salida latente esperada en este contenedor (`.pptx` sin la
skill `480-branded-pptx` instalada) y las omisiones esperadas sin parte de rodaje real; el `.pdf` se
generó de verdad con Chrome/Edge headless. `git status` tras la verificación, limpio salvo los dos
documentos de registro que esta propia sesión actualiza.

**Cambios de estado (§1 de `SEGUIMIENTO.md`).** Ninguno: R-46 y P-13 permanecen `COMPLETADA`. Sin
decisiones nuevas en `DECISIONES_TECNICAS.md` (nada no trivial que decidir en una sesión sin código).
Sin novedad en §3 (bloqueos), §6 (preguntas, `#11`/`#12` siguen `(pendiente)`) ni §7 (desviaciones).
Cabecera de `SEGUIMIENTO.md` actualizada ("Última actualización") respetando la norma de P-10: solo
el estado vigente, sin acumular la narrativa de esta sesión, que vive aquí.

**Nota de cierre.** Segunda reconfirmación de hoy de la rutina "programador-teleprompter" tras
P-13/R-46, sin ningún código que tocar: el patrón que motivó la escalada de `#30` a severidad alta
(cron horario repitiendo las cuatro redes con la cola vacía) sigue vigente mientras el dueño no
responda `#11`/`#12` de §6. Ninguna acción unilateral tomada sobre la cadencia de la rutina ni sobre
el protocolo: ambas son decisiones del dueño, no del Programador.

---

### Sesión 2026-11-05 (335) — Ciclo de Programador: primera reconfirmación del día tras R-46, sin novedad de código

**Arranque.** Sesión en la nube (clon efímero, rutina "programador-teleprompter"). `git checkout
develop && git pull origin develop` trajo en fast-forward trivial los commits ya fusionados hasta
`4cbc825` (sesión 334: P-13 y R-46), árbol de trabajo limpio antes y después. `pip install -r
requirements-dev.txt` (bare `pip`) dejó `mypy`/`ruff`/`pytest` instalados contra un intérprete
distinto al que resuelve `python3` en este contenedor (mismo síntoma de siempre, `#22`/`#28`/P-06);
corregido invocando `python3 -m pip install -r requirements-dev.txt`, verificado con `python3 -m
mypy --version`/`ruff --version`/`pytest --version` antes de continuar.

**Registro de hallazgos y bloqueos revisado antes de elegir tarea.** `auditoriacontinua.md` completo
(filas de estado y narrativa de la pasada del 2026-11-05, `be05fc4`): ningún hallazgo nuevo desde la
sesión anterior. `#42` (alta) sigue `ABIERTO` solo a la espera de que la próxima pasada del auditor
reverifique el cierre ya hecho por **P-13** en la sesión 333 (`68cf14d`, `SKILL.md` ya invoca
`entrada.py` al inicio del flujo) — no exige una P-XX nueva, es terreno exclusivo del auditor. `#43`/
`#44` (baja) sin acción urgente. `#24`/`#30` (gobernanza pura) siguen `ABIERTO` a la espera de la
respuesta del dueño a `#11`/`#12` de §6; `#36` sigue `ASUMIDO`.

**Ninguna tarea elegida.** §1 confirmada de punta a punta: las 34 T-XX (`T-24b` `BLOQUEADA`, ajena al
programador) y las 46 R-XX (hasta R-46) están `COMPLETADA`; §5 completa, P-01 a P-13. Ninguna fila
`PENDIENTE` ni `BLOQUEADA` ejecutable. El PM todavía no ha abierto ninguna oleada tras R-46.
`roadmap/ROADMAP_PRODUCTO.md` confirmado sin ningún hito pendiente fuera de lo ya reflejado en §1.

**Verificación completa, sin cambios de código.** Las cuatro redes ejecutadas de forma independiente
sobre el intérprete real (3.11.18): `mypy scripts/ tests/` limpio (72 archivos); `ruff check scripts/
tests/` sin avisos; `pytest` **798/798 tests** en verde (el recuento exacto solo se ve pasando `-v`/
sin duplicar `-q`, porque `addopts` ya fija `-q` en `pyproject.toml` y una segunda `-q` en línea de
comandos silencia también la línea de resumen — artefacto de invocación, no del proyecto);
`verificar_salidas.py --fixture` con las diecinueve etapas en `OK`, incluida la salida latente
esperada en este contenedor (`.pptx` sin la skill `480-branded-pptx` instalada) y las omisiones
esperadas sin parte de rodaje real; el `.pdf` se generó de verdad con Chrome/Edge headless. `git
status` tras la verificación, limpio salvo los dos documentos de registro que esta propia sesión
actualiza.

**Cambios de estado (§1 de `SEGUIMIENTO.md`).** Ninguno: R-46 y P-13 permanecen `COMPLETADA`. Sin
decisiones nuevas en `DECISIONES_TECNICAS.md` (nada no trivial que decidir en una sesión sin código).
Sin novedad en §3 (bloqueos), §6 (preguntas, `#11`/`#12` siguen `(pendiente)`) ni §7 (desviaciones).
Cabecera de `SEGUIMIENTO.md` actualizada ("Última actualización") respetando la norma de P-10: solo
el estado vigente, sin acumular la narrativa de esta sesión, que vive aquí.

**Nota de cierre.** Primera reconfirmación de hoy de la rutina "programador-teleprompter" tras
P-13/R-46, sin ningún código que tocar: el patrón que motivó la escalada de `#30` a severidad alta
(cron horario repitiendo las cuatro redes con la cola vacía) sigue vigente mientras el dueño no
responda `#11`/`#12` de §6. Ninguna acción unilateral tomada sobre la cadencia de la rutina ni sobre
el protocolo: ambas son decisiones del dueño, no del Programador.

---

### Sesión 2026-11-05 (334) — Ciclo de Programador: R-46 completada (anticipo de la indicación del bloque siguiente)

**Contexto.** Continuación de la misma sesión en la nube que acaba de cerrar **P-13** (hallazgo
urgente `#42`, ver entrada anterior). Con la urgencia resuelta, única R-XX `PENDIENTE` en §1 de
`SEGUIMIENTO.md`: R-46, spec completa leída en `roadmap/ROADMAP_PRODUCTO.md` (Oleada v34).
`DECISIONES_TECNICAS.md` consultado en el área que toca (reproductor/`guion.js`, filas de
R-39/R-42/R-43/R-44/R-45) antes de implementar, mismo patrón exacto.

**R-46 implementada.** `assets/reproductor/guion.js::renderizarReproductor`, en el mismo
`escena.bloques.forEach` donde ya se añade `.cue-indicacion` por indicación propia (R-12), añade
ahora al bloque anterior un `<p class="cue-proxima-indicacion">` por cada indicación de
`escena.bloques[indiceBloque + 1]` (si existe), con el texto `"Después: "` + el texto ya formateado,
en el mismo orden que la cue real los mostrará. Ámbito limitado a la escena actual sin ninguna guarda
extra: el índice `+ 1` es `undefined` justo en el último bloque. CSS nuevo en
`assets/reproductor/estilo.css`: `.cue-proxima-indicacion` reutiliza la visibilidad de
`.cue-indicacion` (oculta salvo bloque activo, plegable con `H`) con un peso visual más subordinado
(`font-size: 0.42em` + `opacity: 0.7`, frente al `0.5em` sin opacidad reducida de la cue real) —
decisión razonada en `DECISIONES_TECNICAS.md`. Sin campo nuevo en el JSON embebido, sin cambio en
`scripts/reproductor.py`/`pdf.py`/`pptx.py`/`documento_revision.py`, sin elemento interactivo ni
`localStorage` nuevo. 8 tests nuevos en `tests/test_reproductor.py` (790→798): fixture propia
(`_GUION_ANTICIPO_INDICACION`, tres bloques consecutivos con la indicación anclada solo al del medio)
verificada primero en sí misma y después contra `guion.js` generado (clase, prefijo, índice `+ 1`,
plegado con `H`, contrato embebido sin campo nuevo, sin control ni `localStorage` nuevo); un test más
reutiliza la fixture de R-12 (`Pantalla:`+`Nota:` en el mismo bloque) para el orden con varias
indicaciones. Cuatro redes en verde (`mypy`, `ruff`, 798 tests, `verificar_salidas.py --fixture` con
sus diecinueve etapas sin cambio de comportamiento visible). Verificado también visualmente con
Playwright/Chromium real (Node.js, preinstalado) sobre la fixture de tres bloques: con el primero
activo, su anticipo (`"Después: Pantalla: Diapositiva de apoyo."`) visible y la cue real oculta; al
avanzar al segundo (el que ancla la indicación), el anticipo del primero desaparece y la cue real
(sin el prefijo `"Después:"`) ocupa su lugar; en el tercero, ni cue ni anticipo — exactamente el
criterio de aceptación de la ficha.

**Decisiones añadidas a `DECISIONES_TECNICAS.md`.** Dos filas 2026-11-05/R-46: (1) mirar hacia
adelante dentro del mismo `forEach` ya existente (`escena.bloques[indiceBloque + 1]`) en vez de un
campo nuevo en el contrato embebido o un segundo recorrido; (2) diferenciar `.cue-proxima-indicacion`
de `.cue-indicacion` combinando tamaño de fuente y opacidad reducidos, en vez de solo uno de los dos.

**Cambios de estado en `SEGUIMIENTO.md` §1.** R-46: `PENDIENTE` → `COMPLETADA` (2026-11-05), fila con
el detalle completo de la entrega. Cabecera actualizada al estado vigente de hoy: ninguna R-XX/T-XX
de código `PENDIENTE` en §1; la siguiente oleada la abre el próximo ciclo de Product Manager. Sin
cambios en §3 (bloqueos), §5 (P-XX, ya cerrada en la entrada anterior) ni §6 (preguntas abiertas).

**`SKILL.md`/`DEVELOPERS.md` actualizados** con la sección "Anticipo de la indicación del bloque
siguiente (R-46)", mismo formato que las secciones de R-39/R-43/R-44/R-45 que la preceden.

**Cierre.** `git add` de los cuatro archivos de código/test tocados (`assets/reproductor/guion.js`,
`assets/reproductor/estilo.css`, `tests/test_reproductor.py`, `SKILL.md`) más `DEVELOPERS.md` y los
documentos de registro (`SEGUIMIENTO.md`, `DECISIONES_TECNICAS.md`, `HISTORIAL_SESIONES.md`); commit
único con prefijo `R-46:`; push a `origin/develop` (nunca a `master`).

---

### Sesión 2026-11-05 (333) — Ciclo de Programador: P-13 urgente, cierra el hueco de `entrada.py` sin invocar en `SKILL.md` (hallazgo `#42`)

**Arranque.** Sesión en la nube (clon efímero, rutina "programador-teleprompter"). `git checkout
develop && git pull origin develop` trajo ya fusionado el ciclo de Auditoría del 2026-11-05
(`be05fc4`: tres hallazgos nuevos `#42`/`#43`/`#44`, cierra `#40`) sobre el ciclo de PM del
2026-11-04 (archivo de Oleada v33/R-45 y apertura de R-46/Oleada v34, `eca9a21`), árbol de trabajo
limpio. `pip install -r requirements-dev.txt` dejó las herramientas en un intérprete distinto al que
resuelve `python`/`python3` en este contenedor (`No module named mypy` al invocar
`python -m mypy`); reinstalado con `python3 -m pip install -r requirements-dev.txt`, mismo tipo de
desajuste ya registrado para sesiones anteriores (`DECISIONES_TECNICAS.md`, T-06/R-45).

**Lectura previa (protocolo del rol Programador).** `HOJA_DE_RUTA.md` §0 (protocolo, solo lectura);
`roadmap/SEGUIMIENTO.md` completo (§1 estado, §3 bloqueos); `auditoriacontinua.md` — registro de
hallazgos completo y la narrativa más reciente — buscando cualquier `ABIERTO` de severidad alta:
**`#42` (2026-11-05, alta)** señala que `scripts/entrada.py` (T-06, `COMPLETADA`, 20+ tests) nunca se
invoca desde `SKILL.md` (`grep -c` confirmado en 0), así que una sesión que siga `SKILL.md` al pie de
la letra nunca pasa el guion de origen por la validación de tamaño/codificación/estructura ni por la
comprobación de contención de ruta de la carpeta de salida. `#43`/`#44` (mismo día, baja) no exigen
P-XX urgente. Atendido `#42` de inmediato como **P-13**, antes de la cola normal (§0.1/§0.3,
"pérdida de texto del guion, corrupción de estado, rotura del reproductor o de su auto-contención,
seguridad... procedentes de un hallazgo ABIERTO de severidad alta del auditor").

**P-13 implementada (urgente, `origen: auditoría #42`).** Nueva sección en `SKILL.md`, "Punto de
entrada: validar y leer el guion, siempre antes de nada (T-06)", insertada justo antes de "Reglas
que esta skill no rompe nunca" (el principio literal del documento): fragmento obligatorio
`entrada.leer_guion(ruta_guion)` / `entrada.carpeta_salida_para(ruta_guion)` como primer paso de
cualquier sesión, con el mismo patrón de "paso obligatorio" que ya usan R-26 (diccionario del dueño)
y R-27 (aviso de guion modificado). Deliberadamente fuera de alcance:
`entrada.ejecutar_con_limite_de_tiempo`, ya evaluado y descartado el 2026-10-09 (apertura de R-27)
por menor severidad y cero incidente real — no se reabre sin evidencia nueva (`DECISIONES_TECNICAS.md`
consultado antes de implementar, tal como exige el protocolo). Alcance puramente documental: cero
cambio en `scripts/`, `tests/` ni `assets/`. Cuatro redes en verde (`mypy`, `ruff`, 790 tests sin
cambio, `verificar_salidas.py --fixture` con sus diecinueve etapas intactas).

**Decisión añadida a `DECISIONES_TECNICAS.md`.** Una fila 2026-11-05/P-13: el remedio exacto que
propone la propia auditoría `#42` (añadir solo el fragmento de `validar_ruta_guion`/`leer_guion`/
`carpeta_salida_para`), frente a no tocar nada (descartado: es precisamente el defecto señalado) o
envolver además `ejecutar_con_limite_de_tiempo` (descartado por decisión previa de R-27, 2026-10-09,
sin evidencia nueva que la contradiga).

**Cambios de estado en `SEGUIMIENTO.md` §5.** Nueva fila **P-13** (urgente, `origen: auditoría #42`,
`COMPLETADA` 2026-11-05). Cabecera actualizada para reflejar el hallazgo `#42` atendido antes de la
cola normal, pendiente solo de reverificación del auditor. Sin cambios en §1 (ninguna T-XX/R-XX
afectada directamente), §3 (bloqueos) ni §6 (preguntas abiertas). Sigue R-46 `PENDIENTE` en §1 — se
retoma a continuación en la misma sesión (entrada siguiente).

**Cierre.** `git add` de `SKILL.md` más los documentos de registro (`SEGUIMIENTO.md`,
`DECISIONES_TECNICAS.md`, `HISTORIAL_SESIONES.md`); commit único con prefijo `P-13:`; push a
`origin/develop` (nunca a `master`). La sesión continúa a continuación con R-46 (única R-XX
`PENDIENTE` restante), ver entrada siguiente.

---

### Sesión 2026-11-04 (332) — Ciclo de Product Manager: archiva la Oleada v33 (R-45) y abre R-46 (Oleada v34)

**Arranque.** Sesión en la nube (clon efímero, rutina "product-manager-teleprompter"). `git checkout
develop && git pull origin develop` hizo fast-forward limpio hasta `4e3238d` (sesión 331), árbol de
trabajo limpio. `pip install -r requirements-dev.txt` (bare `pip`) instaló sin incidencia esta vez.

**Lectura previa.** `roadmap/SEGUIMIENTO.md` (§1, §3, §5, §6, §7), `roadmap/ROADMAP_PRODUCTO.md`,
`roadmap/FEEDBACK.md` y `auditoriacontinua.md` (registro de hallazgos completo vía `grep` de
`ABIERTO`/`ASUMIDO` y las narrativas de las auditorías más recientes, 2026-10-31 a 2026-11-04, dado
que el archivo supera el límite de lectura directa) revisados antes de actuar.

**Hallazgos de auditoría.** La pasada del auditor del 2026-11-04 (posterior a la última lectura de
`ROADMAP_PRODUCTO.md`, que seguía fechada 2026-11-03) cierra `#39` y `#41` (P-10 y P-11, reverificados
en código/documentación), aplica el remedio propuesto por el propio `#38` (condensar la narrativa
crónica de `#24`/`#30`, terreno exclusivo del auditor, ya cerrado) y pasa `#36` a `ASUMIDO` (riesgo
aceptado, sin acción pendiente). Solo quedan `ABIERTO`: `#24`/`#30` (gobernanza pura, pendientes de
la respuesta del dueño a `#11`/`#12` de §6) y `#40` (rotación de `DECISIONES_TECNICAS.md`), esta
última ya resuelta en código por **P-12** en la jornada del Programador de hoy, pendiente solo de que
la próxima pasada del auditor la reverifique y la cierre. Ninguno de los tres es de severidad alta en
las categorías que exigirían una P-XX urgente, y ninguno es convertible en una R-XX de producto.

**Feedback de rodaje.** `roadmap/FEEDBACK.md` sigue con su única fila, plantilla vacía, sin ninguna
entrada `nuevo`: no hay historia de rodaje real que incorporar. El bloqueo #7 de `SEGUIMIENTO.md` §3
(grabar un curso completo) sigue abierto, 62 días desde que T-32 lo dejó listo para grabar
(2026-09-03) — se deja constancia en la cabecera de `ROADMAP_PRODUCTO.md`, sin repetirlo como
pregunta nueva en §6 (es una acción del dueño, no una decisión).

**Archivado.** R-45 (Oleada v33) llevaba `COMPLETADA` en §1 desde el ciclo de Programador posterior a
P-12 de esta misma jornada (2026-11-04), reconfirmada en verde en varias pasadas sucesivas sin que
ningún ciclo de PM la archivara todavía. Movida íntegra (ficha + "Cómo se entregó", este último
construido a partir de la descripción ya verificada en §1) a `roadmap/ROADMAP_HISTORICO.md`, con su
propia sección "### Oleada v33 — entregada" en `ROADMAP_PRODUCTO.md` y el índice de fechas de archivo
al pie de `ROADMAP_HISTORICO.md` actualizado.

**Apertura de R-46 (Oleada v34).** Observación de arquitectura propia: `anclar_indicaciones_a_bloques`
(R-12/R-20) ancla cada indicación `EN PANTALLA`/`NOTA` al bloque de locución que la precede y la
muestra en cuanto ese bloque se vuelve activo, pero un formador en solitario rara vez puede ejecutar
esa indicación (cambiar de ventana, mostrar una diapositiva) de forma instantánea — hoy el aviso llega
justo cuando toca actuar, sin margen para prepararlo sin cortar la locución. R-46 reutiliza el mismo
array ya anclado para anticiparlo, de forma subordinada, en el bloque inmediatamente anterior, mismo
principio de "reutilizar un dato ya calculado" que R-39/R-42/R-44/R-45. Ficha completa (Migración/
Depende de/Origen/Objetivo/Requisitos/Criterio de aceptación) en `ROADMAP_PRODUCTO.md`, registrada
`PENDIENTE` en §1 de `SEGUIMIENTO.md`. Criterio de una sola R-XX de código pendiente a la vez
respetado: ninguna otra R-XX estaba `PENDIENTE` antes de abrir esta.

**Cambios de estado (§1 de `SEGUIMIENTO.md`).** R-46 añadida como `PENDIENTE`. Sin cambios en §3
(bloqueos), §6 (preguntas, `#11`/`#12` siguen `(pendiente)`) ni §7 (desviaciones). Cabecera de
`SEGUIMIENTO.md` actualizada respetando la norma de P-10 (solo estado vigente, narrativa de esta
sesión aquí). Ningún cambio de código: esta sesión es puramente de gestión de roadmap.

**Verificación.** Sin cambios en `scripts/`, `tests/` ni `assets/`: no se ejecutó `scripts/ci.py`
(nada que verificar en código). `git status` tras los cambios, limpio salvo los cuatro documentos de
roadmap que esta sesión actualiza (`SEGUIMIENTO.md`, `ROADMAP_PRODUCTO.md`, `ROADMAP_HISTORICO.md`,
`HISTORIAL_SESIONES.md`).

**Nota de cierre.** Primera sesión de PM desde la del 2026-11-03 (R-45/Oleada v33). Push a
`origin/develop` pendiente, único paso que falta para que la propuesta esté disponible para la
siguiente sesión de Programador.

---

### Sesión 2026-11-04 (331) — Ciclo de Programador: cuarta reconfirmación del día tras P-12, sin novedad de código

**Arranque.** Sesión en la nube (clon efímero, rutina "programador-teleprompter"). `git checkout
develop && git pull origin develop` encontró la rama desconectada de cualquier commit local
(mismo artefacto de arranque de contenedor ya documentado en sesiones anteriores, no divergencia
real): resuelto con el propio `checkout develop`, que hizo fast-forward limpio hasta el commit
`1a258fa` (sesión 330), árbol de trabajo limpio. `pip install -r requirements-dev.txt` (bare `pip`)
no dejó `mypy`/`ruff`/`pytest` importables por el `python` real (`/usr/local/bin/python` →
`python3.11`): el `pip` del `PATH` resuelve contra `python3.13`, un intérprete distinto, mismo
rodeo ya documentado por `#22`/`#28`/P-06 aunque con el emparejamiento de binarios invertido al de
sesiones previas. Corregido invocando `python -m pip install -r requirements-dev.txt` (instala
contra el mismo intérprete que luego ejecuta `scripts/ci.py`), verificado con `python -m mypy
--version`/`python -m ruff --version`/`python -m pytest --version` antes de continuar.

**Registro de hallazgos y bloqueos revisado antes de elegir tarea.** `auditoriacontinua.md`
revisado completo (`git log --oneline -- auditoriacontinua.md`): sin ninguna pasada nueva del
auditor desde la sesión anterior (la más reciente sigue siendo `f501cad`, que cerró `#39`/`#41`,
condensó `#24`/`#30` vía `#38` y pasó `#36` a `ASUMIDO`). Ningún hallazgo `ABIERTO` de severidad
alta en las categorías que exigen P-XX urgente (pérdida de texto del guion, corrupción de estado,
rotura del reproductor o de su auto-contención, seguridad). `#24`/`#30` (gobernanza pura, preguntas
`#11`/`#12` de §6 sin respuesta del dueño) siguen `ABIERTO`; `#40` (rotación de
`DECISIONES_TECNICAS.md`) resuelto en código por P-12, pendiente solo de que el auditor lo
reverifique y lo cierre (terreno exclusivo suyo); `#36` sigue `ASUMIDO`.

**Ninguna tarea elegida.** §1 confirmada de punta a punta: las 34 T-XX (`T-24b` `BLOQUEADA`, ajena
al programador) y las 45 R-XX (hasta R-45) están `COMPLETADA`; §5 también completa, P-01 a P-12.
Ninguna fila `PENDIENTE` ni `BLOQUEADA` ejecutable. El PM todavía no ha abierto ninguna oleada tras
R-45. `roadmap/ROADMAP_PRODUCTO.md` confirmado sin ningún hito pendiente fuera de lo ya reflejado
en §1.

**Verificación completa, sin cambios de código.** `python scripts/ci.py` tras instalar las
dependencias de desarrollo: `mypy` (72 archivos, sin problemas), `ruff check` (todo correcto),
`pytest` (790/790 tests, código de salida 0) y `verificar_salidas.py --fixture` (diecinueve etapas
`OK`, incluida la salida latente esperada en este contenedor — `.pptx` sin la skill
`480-branded-pptx` instalada — y las omisiones esperadas sin parte de rodaje real; el `.pdf` sí se
generó de verdad con Chrome/Edge headless). Cuatro redes en verde; `git status` tras la
verificación, limpio salvo los dos documentos de registro que esta propia sesión actualiza.

**Cambios de estado (§1 de `SEGUIMIENTO.md`).** Ninguno: R-45 y P-12 permanecen `COMPLETADA`. Sin
decisiones nuevas en `DECISIONES_TECNICAS.md`. Sin novedad en §3 (bloqueos), §6 (preguntas,
`#11`/`#12` siguen `(pendiente)`) ni §7 (desviaciones). Cabecera de `SEGUIMIENTO.md` actualizada
("Última actualización") respetando la norma de P-10: solo el estado vigente, sin acumular la
narrativa de esta sesión, que vive aquí.

**Nota de cierre.** Cuarta reconfirmación de hoy de la rutina "programador-teleprompter" tras
R-45/P-12, sin ningún código que tocar: el patrón que motivó la escalada de `#30` a severidad alta
(cron horario repitiendo las cuatro redes con la cola vacía) sigue vigente mientras el dueño no
responda `#11`/`#12` de §6. Ninguna acción unilateral tomada sobre la cadencia de la rutina ni sobre
el protocolo: ambas son decisiones del dueño, no del Programador.

---

### Sesión 2026-11-04 (330) — Ciclo de Programador: tercera reconfirmación del día tras P-12, sin novedad de código

**Arranque.** Sesión en la nube (clon efímero, rutina "programador-teleprompter"). `git checkout
develop && git pull origin develop` encontró la rama desconectada de cualquier commit local
(artefacto del arranque del contenedor, no divergencia real): resuelto con el propio `checkout
develop`, que hizo fast-forward limpio hasta el commit `9ae94d6` (sesión 329), árbol de trabajo
limpio. `python3.13 -m pip install -r requirements-dev.txt` instalado de forma explícita contra
ese intérprete (mismo rodeo ya documentado por `#22`/`#28`/P-06: `python3`/`pip` desnudos no
resuelven de forma consistente contra el mismo intérprete en este contenedor).

**Registro de hallazgos y bloqueos revisado antes de elegir tarea.** `auditoriacontinua.md`
revisado completo: sin ninguna pasada nueva del auditor desde la sesión anterior (la más reciente
sigue siendo la del 2026-11-04 que cerró `#39`/`#41` y condensó `#24`/`#30` vía `#38`, pasó `#36`
a `ASUMIDO` y reconfirmó `#40` `ABIERTO`). Ningún hallazgo `ABIERTO` de severidad alta en las
categorías que exigen P-XX urgente (pérdida de texto del guion, corrupción de estado, rotura del
reproductor o de su auto-contención, seguridad). `#24`/`#30` (gobernanza pura, preguntas `#11`/
`#12` de §6 sin respuesta del dueño) siguen `ABIERTO`; `#40` (rotación de `DECISIONES_TECNICAS.md`)
resuelto en código por P-12 de dos sesiones atrás, pendiente solo de que el auditor lo reverifique
y lo cierre (terreno exclusivo suyo); `#36` sigue `ASUMIDO`.

**Ninguna tarea elegida.** §1 confirmada de punta a punta: las 34 T-XX (`T-24b` `BLOQUEADA`, ajena
al programador) y las 45 R-XX (hasta R-45) están `COMPLETADA`; §5 también completa, P-01 a P-12.
Ninguna fila `PENDIENTE` ni `BLOQUEADA` ejecutable. El PM todavía no ha abierto ninguna oleada tras
R-45.

**Verificación completa, sin cambios de código.** `python3.13 -m mypy scripts/ tests/` (72
archivos, sin problemas), `python3.13 -m ruff check scripts/ tests/` (todo correcto), `python3.13
-m pytest` (790/790 tests, código de salida 0) y `python3.13 scripts/verificar_salidas.py
--fixture` (diecinueve etapas `OK`, incluida la salida latente esperada en este contenedor — `.pptx`
sin la skill `480-branded-pptx` instalada — y las omisiones esperadas sin parte de rodaje real; el
`.pdf` sí se generó de verdad). Cuatro redes en verde; `git status` tras la verificación, limpio
salvo los dos documentos de registro que esta propia sesión actualiza.

**Cambios de estado (§1 de `SEGUIMIENTO.md`).** Ninguno: R-45 y P-12 permanecen `COMPLETADA`. Sin
decisiones nuevas en `DECISIONES_TECNICAS.md`. Sin novedad en §3 (bloqueos), §6 (preguntas,
`#11`/`#12` siguen `(pendiente)`) ni §7 (desviaciones). Cabecera de `SEGUIMIENTO.md` actualizada
("Última actualización") respetando la norma de P-10: solo el estado vigente, sin acumular la
narrativa de esta sesión, que vive aquí.

**Nota de cierre.** Octavo disparo de hoy de la rutina "programador-teleprompter" (cinco
reconfirmaciones tras R-45 + P-12 + esta tercera tras P-12), sin ningún código que tocar: el patrón
que motivó la escalada de `#30` a severidad alta (cron horario repitiendo las cuatro redes con la
cola vacía) sigue vigente mientras el dueño no responda `#11`/`#12` de §6. Ninguna acción
unilateral tomada sobre la cadencia de la rutina ni sobre el protocolo: ambas son decisiones del
dueño, no del Programador.

---

### Sesión 2026-11-04 (329) — Ciclo de Programador: segunda reconfirmación del día tras P-12, sin novedad de código

**Arranque.** Sesión en la nube (clon efímero, rutina "programador-teleprompter"). `git checkout
develop && git pull origin develop` encontró el repo en estado "HEAD detached" (artefacto del
arranque del contenedor, no divergencia real): resuelto con el propio `checkout develop`, que dejó
la rama al día con la sesión anterior (commit `5e71fbe`, sesión 328), árbol de trabajo limpio.
Mismo rodeo ya documentado por `#22`/`#28`/P-06: `pip install -r requirements-dev.txt` desnudo
resuelve contra `python3.11` (`/usr/local/bin/python3` es symlink a `/usr/bin/python3.11`) mientras
`pip` apunta a `python3.13`; reinstalado con `python3.13 -m pip install -r requirements-dev.txt` y
verificado con ese mismo intérprete antes de dar nada por bueno.

**Registro de hallazgos y bloqueos revisado antes de elegir tarea.** `auditoriacontinua.md`
revisado completo (registro de hallazgos íntegro, filas `#1`–`#40`): ningún hallazgo `ABIERTO` de
severidad alta en las categorías que exigen P-XX urgente (pérdida de texto del guion, corrupción de
estado, rotura del reproductor o de su auto-contención, seguridad). `#24`/`#30` (gobernanza pura,
preguntas `#11`/`#12` de §6 sin respuesta del dueño) siguen `ABIERTO`, igual que `#40` (rotación de
`DECISIONES_TECNICAS.md`, resuelta en código por P-12 pero pendiente de reverificación del auditor,
terreno exclusivo suyo); `#36` sigue `ASUMIDO`. Sin pasada nueva del auditor desde la sesión
anterior.

**Ninguna tarea elegida.** §1 confirmada de punta a punta: las 34 T-XX (`T-24b` `BLOQUEADA`, ajena
al programador) y las 45 R-XX (hasta R-45) están `COMPLETADA`; §5 también completa, P-01 a P-12.
Ninguna fila `PENDIENTE` ni `BLOQUEADA` ejecutable. El PM todavía no ha abierto ninguna oleada tras
R-45.

**Verificación completa, sin cambios de código.** `python3.13 -m mypy scripts/ tests/` (72
archivos, sin problemas), `python3.13 -m ruff check scripts/ tests/` (todo correcto), `python3.13
-m pytest -q` (790/790 tests, código de salida 0) y `python3.13 scripts/verificar_salidas.py
--fixture` (diecinueve etapas `OK`, incluida la salida latente esperada en este contenedor — `.pptx`
sin la skill `480-branded-pptx` instalada — y las omisiones esperadas sin parte de rodaje real; el
`.pdf` sí se generó de verdad). Cuatro redes en verde; `git status` tras la verificación, limpio
salvo los dos documentos de registro que esta propia sesión actualiza.

**Cambios de estado (§1 de `SEGUIMIENTO.md`).** Ninguno: R-45 y P-12 permanecen `COMPLETADA`. Sin
decisiones nuevas en `DECISIONES_TECNICAS.md`. Sin novedad en §3 (bloqueos), §6 (preguntas,
`#11`/`#12` siguen `(pendiente)`) ni §7 (desviaciones). Cabecera de `SEGUIMIENTO.md` actualizada
("Última actualización") respetando la norma de P-10: solo el estado vigente, sin acumular la
narrativa de esta sesión, que vive aquí.

**Nota de cierre.** Séptimo disparo de hoy de la rutina "programador-teleprompter" (cuatro
reconfirmaciones tras R-45 + P-12 + esta segunda tras P-12), sin ningún código que tocar: el patrón
que motivó la escalada de `#30` a severidad alta (cron horario repitiendo las cuatro redes con la
cola vacía) sigue vigente mientras el dueño no responda `#11`/`#12` de §6. Ninguna acción
unilateral tomada sobre la cadencia de la rutina ni sobre el protocolo: ambas son decisiones del
dueño, no del Programador.

---

### Sesión 2026-11-04 (328) — Ciclo de Programador: primera reconfirmación del día tras P-12, sin novedad de código

**Arranque.** Sesión en la nube (clon efímero, rutina "programador-teleprompter"). `git checkout
develop && git pull origin develop` ya estaba al día con la sesión anterior (commit `ae521d0`,
P-12), árbol de trabajo limpio sin divergencia que resolver. Mismo rodeo ya documentado por
`#22`/`#28`/P-06: `pip install -r requirements-dev.txt` desnudo resuelve contra `python3.13`
mientras `python`/`python3` apuntan a `/usr/bin/python3.11`; reinstalado con `python3 -m pip
install -r requirements-dev.txt` antes de verificar nada.

**Registro de hallazgos y bloqueos revisado antes de elegir tarea.** `auditoriacontinua.md`
revisado completo: sin ninguna pasada nueva del auditor desde la sesión anterior (la más reciente
sigue siendo la del 2026-11-04 que cerró `#39`/`#41` y condensó `#24`/`#30`, cerrando `#38`).
Ningún hallazgo `ABIERTO` de severidad alta en las categorías que exigen P-XX urgente (pérdida de
texto del guion, corrupción de estado, rotura del reproductor o de su auto-contención, seguridad).
`#24`/`#30` (gobernanza pura, preguntas `#11`/`#12` de §6 sin respuesta del dueño) siguen `ABIERTO`;
`#40` (rotación de `DECISIONES_TECNICAS.md`) queda resuelto en código por P-12 de la sesión
anterior, pendiente solo de que el auditor lo reverifique y lo cierre (terreno exclusivo suyo);
`#36` sigue `ASUMIDO`.

**Ninguna tarea elegida.** §1 confirmada de punta a punta: las 34 T-XX (`T-24b` `BLOQUEADA`, ajena
al programador) y las 45 R-XX (hasta R-45) están `COMPLETADA`; §5 también completa, P-01 a P-12.
Ninguna fila `PENDIENTE` ni `BLOQUEADA` ejecutable. El PM todavía no ha abierto ninguna oleada tras
R-45 (`ROADMAP_PRODUCTO.md` sigue fechado 2026-11-03). Primer ciclo de pura reconfirmación del día
tras el cierre de P-12.

**Verificación completa, sin cambios de código.** `python3 scripts/ci.py`: `mypy` (72 archivos,
sin problemas), `ruff check` (todo correcto), `pytest` (790/790 tests) y
`verificar_salidas.py --fixture` (diecinueve etapas `OK`, incluida la salida latente esperada en
este contenedor — `.pptx` sin la skill `480-branded-pptx` instalada — y las omisiones esperadas sin
parte de rodaje real; el `.pdf` sí se generó de verdad, Chrome/Edge headless disponible en este
contenedor). Cuatro redes en verde; `git status` tras la verificación, limpio salvo los dos
documentos de registro que esta propia sesión actualiza.

**Cambios de estado (§1 de `SEGUIMIENTO.md`).** Ninguno: R-45 y P-12 permanecen `COMPLETADA`. Sin
decisiones nuevas en `DECISIONES_TECNICAS.md`. Sin novedad en §3 (bloqueos), §6 (preguntas,
`#11`/`#12` siguen `(pendiente)`) ni §7 (desviaciones). Cabecera de `SEGUIMIENTO.md` actualizada
("Última actualización") respetando la norma de P-10: solo el estado vigente, sin acumular la
narrativa de esta sesión, que vive aquí.

**Nota de cierre.** Sexto disparo de hoy de la rutina "programador-teleprompter" (cuatro
reconfirmaciones + P-12 + esta), sin ningún código que tocar tras R-45/P-12: el patrón que motivó
la escalada de `#30` a severidad alta (cron horario repitiendo las cuatro redes con la cola vacía)
sigue vigente mientras el dueño no responda `#11`/`#12` de §6. Ninguna acción unilateral tomada
sobre la cadencia de la rutina ni sobre el protocolo: ambas son decisiones del dueño, no del
Programador.

---

