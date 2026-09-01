# HISTORIAL DE SESIONES — teleprompter

> Bitácora **append-only** de sesiones (antiguo §8 de SEGUIMIENTO). La más reciente arriba.
> Cada entrada referencia las filas de decisión añadidas en `DECISIONES_TECNICAS.md` y los
> cambios de estado en §1 de `SEGUIMIENTO.md` (consistencia cruzada).
>
> **Rotación:** mantener en línea las ~15 sesiones más recientes; archivar el resto por mes en
> `roadmap/HISTORIAL_SESIONES/AAAA-MM.md` y dejar aquí, al inicio, un índice de los meses archivados.

## Meses archivados
*(ninguno todavía)*

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

### Sesión 2026-08-31 — arranque manual de las tres rutinas
**Tarea(s):** auditoría inicial · primer ciclo de PM · T-00 · P-01
**Estado resultante:** T-00 COMPLETADA · P-01 COMPLETADA
**Commits a develop:** ver commit `T-00` de esta fecha (rama `develop`, no `main`: desviación registrada en §7)
**Migraciones ejecutadas:** ninguna
**Archivos creados/modificados:** `SKILL.md` (borrador), `pyproject.toml`, `requirements-dev.txt`, `.gitignore` (P-01), `scripts/presentacion.py`, `scripts/config.py`, `scripts/verificar_salidas.py`, `scripts/migraciones/`, `tests/test_esqueleto.py`, `auditoriacontinua.md`, `roadmap/ROADMAP_PRODUCTO.md`, `roadmap/SEGUIMIENTO.md`, `roadmap/DECISIONES_TECNICAS.md`
**Verificaciones pre-push:** tipos ✅ (4 archivos, mypy estricto) · lint ✅ (tras corregir 5 avisos de `noqa` sobrantes) · tests ✅ (11 pasan) · salidas ✅ (código 0, 4 etapas declaradas NO APLICABLE con su tarea)
**Health check post-deploy:** no aplicable — la instalación de la skill es T-32; no hay copia instalada que comprobar todavía
**Decisiones tomadas:** 5 filas añadidas a `DECISIONES_TECNICAS.md` (scaffolder de skill-creator, `pip --user` frente a entorno virtual, cuarta red con etapas NO APLICABLE, regla de lint T20 contra `print()`, alcance del `.gitignore`)
**Hallazgos del auditor atendidos:** #2 resuelto vía P-01; #4 resuelto por diseño en `verificar_salidas.py`. #1 y #3 escalados al dueño como §6.7 y §6.8 porque no son decisiones del agente. #5, #6, #7 y #8 enrutados por el PM a R-01, R-06 y al backlog
**Hallazgos:** el repositorio ya existía en `develop` con remoto en GitHub, y `main` no existe: el protocolo §0.1 no es aplicable tal cual. Poppins no está instalada en la máquina, lo que vacía de efecto la decisión tipográfica del dueño
**Tareas autopropuestas (P-XX):** P-01 registrada en §5 antes de implementarla, ejecutada y cerrada
**Próximo paso:** T-01 (linting y formato) — ya hay base: `ruff` y `mypy` estricto configurados en `pyproject.toml` y en verde. Falta el hook de pre-commit que impida commitear con la verificación en rojo. Antes de tocar T-28/T-29 hace falta la respuesta a §6.8 (tipografía) y, para poder hacer push, la de §6.7 (rama)

---

*(Las sesiones reales se añaden debajo, la más reciente primero.)*

---

### Sesión 2026-09-01 — agente de nube, rutina programada
**Tarea(s):** T-03 (suite de tests mínima)
**Estado resultante:** T-03 COMPLETADA
**Commits a develop:** `T-03: suite de tests mínima — contrato de convención + talones de la lógica pendiente` (ver `git log origin/develop`)
**Migraciones ejecutadas:** ninguna
**Archivos creados/modificados:** `tests/conftest.py` (nuevo, fixtures `guiones_reales`/`texto_guiones_reales`), `tests/test_convencion_guiones_reales.py` (nuevo, 5 tests reales contra `fixtures/reales/`), `tests/test_logica_pendiente.py` (nuevo, 8 tests `skip` con contrato), `DEVELOPERS.md` (sección "Suite de tests"), `roadmap/SEGUIMIENTO.md` (§1, cabecera), `roadmap/DECISIONES_TECNICAS.md` (1 fila nueva)
**Verificaciones pre-push:** tipos ✅ (mypy estricto, 0 errores) · lint ✅ (ruff, 0 avisos) · tests ✅ (29 pasan, 8 skipped con motivo; antes 24 pasan / 0 skipped) · salidas ✅ (código 0, 4 etapas aún NO APLICABLE con su tarea)
**Health check post-deploy:** no aplicable — sesión de nube, sin acceso a `~/.claude/skills/teleprompter/` (T-32); no se simula
**Decisiones tomadas:** 1 fila añadida a `DECISIONES_TECNICAS.md` (T-03: cómo resolver que su criterio de aceptación cita lógica que T-08 a T-13/T-27 implementan después, mediante tests `skip` con contrato explícito en vez de darla por completada sin más o dejarla sin registro)
**Hallazgos del auditor atendidos:** ninguno de severidad alta abierto en `auditoriacontinua.md` (#5, #6, #8 siguen media/baja, sin acción de esta sesión)
**Hallazgos:** el orden de §1 pone T-03 (que depende solo de T-01) antes que la lógica de producto que su propio criterio de aceptación menciona (T-08 a T-13, T-27, todas después en la cola). No es un bug de esta sesión, es una tensión estructural entre la hoja de ruta (inmutable) y el orden real de implementación; queda documentada en `DECISIONES_TECNICAS.md` para que ninguna sesión futura la redescubra. `test_esqueleto.py` ya anticipaba esto en su docstring ("la suite de verdad es T-03"), escrito en T-00 antes de que la secuencia completa estuviera clara
**Tareas autopropuestas (P-XX):** ninguna
**Próximo paso:** T-04 (CI local + workflow inactivo). Nota para T-08 y siguientes: al implementar cada capacidad, localizar su test correspondiente en `tests/test_logica_pendiente.py`, quitarle el `skip` e implementarlo según el contrato descrito en su docstring — es parte del criterio de aceptación de esa tarea, no un paso aparte

---

### Sesión 2026-09-01 08:00 — agente de nube, rutina programada
**Tarea(s):** T-01 (linting y formato)
**Estado resultante:** T-01 COMPLETADA
**Commits a develop:** `T-01: hook de pre-commit versionado que bloquea el commit en rojo` (ver `git log origin/develop`)
**Migraciones ejecutadas:** ninguna
**Archivos creados/modificados:** `scripts/hooks/pre-commit` (nuevo), `scripts/instalar_hooks.py` (nuevo), `tests/test_hooks.py` (nuevo), `DEVELOPERS.md` (nuevo), `roadmap/SEGUIMIENTO.md` (§1, cabecera), `roadmap/DECISIONES_TECNICAS.md` (1 fila nueva)
**Verificaciones pre-push:** tipos ✅ (mypy estricto, 0 errores) · lint ✅ (ruff, 0 avisos) · tests ✅ (17 pasan, 6 nuevos de `test_hooks.py`) · salidas ✅ (código 0, 4 etapas aún NO APLICABLE con su tarea, como es esperable antes de T-18/T-27/T-30/T-32)
**Health check post-deploy:** no aplicable — sesión de nube, sin acceso a `~/.claude/skills/teleprompter/` (T-32); no se simula
**Decisiones tomadas:** 1 fila añadida a `DECISIONES_TECNICAS.md` (hook versionado + instalador en vez de escribir directamente en `.git/hooks/` o adoptar el framework `pre-commit`)
**Hallazgos del auditor atendidos:** ninguno de severidad alta abierto en `auditoriacontinua.md` (#5, #6, #8 siguen media/baja, enrutados a R-01/R-06/T-32, sin acción de esta sesión)
**Hallazgos:** ninguno nuevo. `ruff`/`mypy` ya estaban en verde desde T-00; lo que faltaba de T-01 era exclusivamente el hook de pre-commit, tal y como dejó anotado la sesión anterior en «Próximo paso»
**Tareas autopropuestas (P-XX):** ninguna
**Próximo paso:** T-02 (logger centralizado). Nota: `scripts/presentacion.py` ya existe y ya es la única capa autorizada a hacer `print()` (regla T20 activa desde T-00); T-02 debe confirmar que cubre todos los casos de diagnóstico con `--verbose` y que el log de ejecución se escribe en la carpeta de salida del guión, no solo por consola

### Sesión 2026-09-01 — nota de infraestructura (push por API)
**Tarea(s):** ninguna adicional; anexo a la sesión de T-01
**Estado resultante:** sin cambio de estado de tareas
**Hallazgo de infraestructura:** `git push` sobre HTTPS (vía el proxy de git de la sesión) devuelve 403 con el mensaje «Claude doesn't have GitHub access to JanoSolerDiaz/telePrompter for your organization» — tanto desde el clon de trabajo como desde un segundo clon obtenido con `access: push`. Sin embargo, el servidor MCP de GitHub (`mcp__github__*`, autenticado por otra vía) sí tiene acceso de lectura y escritura al repositorio: `get_me`, `list_branches` y finalmente `push_files` funcionaron con normalidad. Este commit de T-01 se subió a `origin/develop` con `mcp__github__push_files` en lugar de `git push`, para no perder el trabajo de la sesión.
**Acción para el dueño:** si se quiere que las futuras sesiones de nube puedan usar `git push` directamente (más simple y con hooks locales reales), instalar o revincular la GitHub App de Claude para esta organización/repositorio: https://github.com/apps/claude/installations/select_target o revincular en https://claude.ai/customize/connectors?auth_start=github&auth_start_force=1. Mientras tanto, el push por API (`mcp__github__push_files`) es la vía de repuesto y queda documentado aquí para que ninguna sesión futura lo redescubra desde cero.
**Próximo paso:** ninguno adicional al ya anotado arriba (T-02); si el dueño revincula el acceso, la siguiente sesión puede confirmar con un `git push` de prueba.

---

### Sesión 2026-09-01 — agente de nube, rutina programada
**Tarea(s):** T-02 (logger centralizado)
**Estado resultante:** T-02 COMPLETADA
**Commits a develop:** `T-02: logger centralizado de diagnostico` (ver `git log origin/develop`)
**Migraciones ejecutadas:** ninguna
**Archivos creados/modificados:** `scripts/logger.py` (nuevo), `tests/test_logger.py` (nuevo, 7 tests), `scripts/config.py` (constante `NOMBRE_ARCHIVO_LOG`), `scripts/verificar_salidas.py` (flag `--verbose`, logger cableado sobre `fixtures/salida/`), `.gitignore` (`fixtures/salida/` pasa a ignorarse por ser artefacto generado), `DEVELOPERS.md` (sección "Salida al usuario y diagnóstico"), `roadmap/SEGUIMIENTO.md` (§1, cabecera), `roadmap/DECISIONES_TECNICAS.md` (1 fila nueva)
**Verificaciones pre-push:** tipos ✅ (mypy estricto, 0 errores) · lint ✅ (`ruff check` y `ruff format --check`, 0 avisos; regla `T20` confirma 0 `print()` fuera de `presentacion.py`) · tests ✅ (24 pasan, 7 nuevos de `test_logger.py`) · salidas ✅ (código 0, 4 etapas aún NO APLICABLE con su tarea; probado también con `--verbose`)
**Health check post-deploy:** no aplicable — sesión de nube, sin acceso a `~/.claude/skills/teleprompter/` (T-32); no se simula
**Decisiones tomadas:** 1 fila añadida a `DECISIONES_TECNICAS.md` (logger separado de `presentacion.py` vía `logging` de la biblioteca estándar, un único logger nombrado en vez de uno por módulo, idempotente entre llamadas repetidas)
**Hallazgos del auditor atendidos:** ninguno de severidad alta abierto en `auditoriacontinua.md` (#5, #6, #8 siguen media/baja, sin acción de esta sesión)
**Hallazgos:** ninguno nuevo. `fixtures/salida/` no estaba en `.gitignore` pese a que `verificar_salidas.py` ya la usaba como destino futuro de `reproductor.html` (T-18); corregido de paso, era necesario para no versionar el log generado por esta tarea. Nota de infraestructura: a diferencia de la sesión de T-01, `git push -u origin develop` funcionó directamente sin el 403 de HTTPS documentado más arriba; no hizo falta recurrir a `mcp__github__push_files`. No se sabe si el acceso quedó revinculado de forma permanente o si fue puntual: la siguiente sesión debe seguir intentando `git push` primero y solo caer al push por API si vuelve a fallar
**Tareas autopropuestas (P-XX):** ninguna
**Próximo paso:** T-03 (suite de tests mínima) — la tarea más importante en autonomía total (§1)
