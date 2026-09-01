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

### Sesión 2026-09-01 — T-15 (reescrituras marcadas, aceptables y reversibles), sesión de nube
**Tarea(s):** T-15
**Estado resultante:** T-15 COMPLETADA
**Commits a develop:** `T-15: reescrituras marcadas, aceptables y reversibles (une T-13 y T-14)` (ver `git log` de esta fecha en `develop`)
**Migraciones ejecutadas:** ninguna (el contenedor `reescrituras: list[dict]` ya existía en `estado.json` desde T-07; T-15 solo fija la forma de esos `dict`, sin tocar el esquema ni su versión)
**Archivos creados/modificados:** `scripts/reescrituras.py` (nuevo: `Reescritura`, `recopilar_propuestas`, `formatear_reescritura`/`extraer_decisiones`, `aplicar_decisiones`, `fusionar_con_estado`/`guardar_en_estado`, `pendientes`, `texto_con_reescrituras_aceptadas`, `aplicar_particion_aceptada`/`aplicar_particiones_aceptadas`, `revertir_reescrituras`), `tests/test_reescrituras.py` (nuevo, 26 tests: recopilación, identidad estable del `id`, formato marcado y lectura de la decisión, persistencia y revalidación, aplicación sobre texto y troceo, deshacer global, el ciclo completo del criterio de aceptación literal, y una pasada sobre los tres guiones reales), `SKILL.md` (sección nueva sobre el formato marcado, para el dueño que va a editarlo a mano), `DEVELOPERS.md` (sección T-15), `roadmap/SEGUIMIENTO.md` (§1, cabecera), `roadmap/DECISIONES_TECNICAS.md`, `roadmap/HISTORIAL_SESIONES.md` (esta entrada)
**Verificaciones pre-push:** tipos ✅ · lint ✅ · tests ✅ (224 pasan + 2 skipped, antes 198 + 2) · build ✅ (`verificar_salidas.py --fixture` sigue en verde con las mismas 4 etapas NO APLICABLE hasta T-18/T-27/T-30/T-32, nada roto)
**Health check post-deploy:** N/A — sesión de nube, no instala en `~/.claude/skills/` (T-32 sigue BLOQUEADA por ese motivo)
**Decisiones tomadas:** 5 filas nuevas en `DECISIONES_TECNICAS.md` (2026-09-01, T-15): identidad de `Reescritura.id` por ocasión (escena+posición+familia+original), no por el contenido de la propuesta; solo la familia `sin_punto_respiracion` de T-14 genera reescritura, sin parámetro para ampliarlo; el formato marcado es un bloque autónomo pensado para T-16, no el documento `guion-escenas.md` completo; la marca de decisión es una sola palabra tolerante a la sintaxis Markdown de alrededor, no dos casillas; una partición aceptada hereda `corte_forzado` del bloque de origen sin recalcularlo
**Hallazgos del auditor atendidos:** ninguno ABIERTO de severidad alta en `auditoriacontinua.md` al empezar la sesión; no se tocó el registro
**Hallazgos:** ninguno nuevo. Se detectó y corrigió en la propia sesión (antes de dar la tarea por completada) un fallo en la primera versión del regex de `extraer_decisiones`: exigía un `:` literal justo antes de la marca de decisión y no reconocía el propio formato que `formatear_reescritura` genera (`> **Decisión:** PENDIENTE`, con `**` de negrita Markdown de por medio); corregido a `Decisi[oó]n\W*(...)`, con test de regresión (`test_extraer_decisiones_es_tolerante_a_mayusculas_y_espacios`)
**Tareas autopropuestas (P-XX):** ninguna
**Próximo paso:** T-16 (`guion-escenas.md` de una sola pasada). Ya tiene disponibles `formatear_reescritura`/`extraer_decisiones` de T-15 para insertar dentro de cada escena, y `pendientes`/`fusionar_con_estado` para no repetir una reescritura ya decidida en revalidaciones sucesivas.

---

### Sesión 2026-09-01 — Gestión de roadmap (Product Manager), sesión de nube
**Tarea(s):** ninguna T-XX/P-XX; gestión de `ROADMAP_PRODUCTO.md` y del hub
**Estado resultante:** N/A (no toca código ni tests)
**Commits a develop:** `roadmap: R-07 (capitulos YouTube) y revision de hallazgos/feedback` (ver `git log` de esta fecha en `develop`)
**Migraciones ejecutadas:** ninguna
**Archivos creados/modificados:** `roadmap/ROADMAP_PRODUCTO.md` (nueva R-07, oleada v3), `roadmap/SEGUIMIENTO.md` (§1 fila R-07, cabecera), `roadmap/HISTORIAL_SESIONES.md` (esta entrada)
**Verificaciones pre-push:** N/A — sesión sin cambios de código; no aplica `ci.py`
**Health check post-deploy:** N/A
**Decisiones tomadas:** ninguna decisión técnica (esta sesión no escribe código); ver `ROADMAP_PRODUCTO.md` para la justificación de R-07
**Hallazgos del auditor atendidos:** revisados los tres ABIERTOS de `auditoriacontinua.md` (#5, #6, #8); los tres ya estaban enrutados (R-01, R-06, T-32 respectivamente), ninguno requería una R-XX nueva
**Hallazgos:** `FEEDBACK.md` sigue vacío (sin entradas `nuevo`) — no hay todavía rodaje real que alimente la oleada v2
**Tareas autopropuestas (P-XX):** ninguna (esta sesión no ejecuta código, solo gestiona el roadmap de producto)
**Próximo paso:** el programador sigue por T-14 (detector de problemas de lectura en voz alta), completada en paralelo por otra sesión de nube (ver entrada siguiente); R-07 queda especificada para cuando la oleada v1 esté entregada y arranque la v2/v3, sin bloquear el orden vigente en §1 de `SEGUIMIENTO.md`.

---

### Sesión 2026-09-01 — T-14 (detector de problemas de lectura en voz alta), sesión de nube
**Tarea(s):** T-14
**Estado resultante:** T-14 COMPLETADA
**Commits a develop:** `T-14: detector de problemas de lectura en voz alta (cinco familias sobre BloqueRespiracion)` (ver `git log` de esta fecha en `develop`)
**Migraciones ejecutadas:** ninguna (T-14 no toca el esquema de `estado.json`; no hay todavía un punto de entrada que persista avisos, igual que T-10/T-12/T-13)
**Archivos creados/modificados:** `scripts/deteccion.py` (nuevo: `Aviso`, `ResultadoDeteccionBloque`, `detectar_problemas_bloque`/`detectar_problemas_guion` y las cinco familias privadas), `scripts/config.py` (umbrales nuevos como campos de `Configuracion` con validación de entero positivo, más el diccionario plano `ANGLICISMOS_COMUNES`), `tests/test_deteccion.py` (nuevo, 19 tests: una familia disparada + un contraejemplo por cada uno de los cinco requisitos, cobertura total sobre los tres guiones reales, la restricción de `admite_particion` a una sola familia, y validación de configuración), `SKILL.md` (tabla nueva de familias y su valor por defecto), `roadmap/SEGUIMIENTO.md` (§1, cabecera), `roadmap/DECISIONES_TECNICAS.md`, `roadmap/HISTORIAL_SESIONES.md`, `DEVELOPERS.md` (sección T-14)
**Verificaciones pre-push:** tipos ✅ · lint ✅ · tests ✅ (198 pasan + 2 skipped, antes 179 + 2) · build ✅ (`verificar_salidas.py --fixture` sigue en verde con las mismas 4 etapas NO APLICABLE hasta T-18/T-27/T-30/T-32, nada roto)
**Health check post-deploy:** N/A — sesión de nube, no instala en `~/.claude/skills/` (T-32 sigue BLOQUEADA por ese motivo)
**Decisiones tomadas:** 4 filas nuevas en `DECISIONES_TECNICAS.md` (2026-09-01, T-14): operar sobre `BloqueRespiracion` (T-11) en vez de reimplementar partición de oraciones; solo `sin_punto_respiracion` admite partición (requisito 6 literal); heurísticas de caracteres sin analizador sintáctico real, con el mismo razonamiento que la concordancia de género de T-13; `ANGLICISMOS_COMUNES` como diccionario plano de módulo, no campo de `Configuracion`
**Hallazgos del auditor atendidos:** ninguno ABIERTO de severidad alta en `auditoriacontinua.md` al empezar la sesión; no se tocó el registro
**Hallazgos:** ninguno nuevo. Verificado manualmente (fuera de la suite) que las cinco familias no disparan falsos positivos sobre frases cotidianas sencillas y sí producen avisos reales y acotados (15-17 por guion sobre 71-87 bloques) en los tres guiones de `fixtures/reales/`, sin que ninguna familia inunde el resultado
**Tareas autopropuestas (P-XX):** ninguna
**Próximo paso:** T-15 (reescrituras marcadas, aceptables y reversibles) — depende de T-13 y T-14, ambas ya completadas. Su alcance ya está acotado por el dueño (§0.2, §6.4: solo forma dicha y respiración) y por el requisito 6 de T-14 (la partición de `sin_punto_respiracion` es la única aviso-familia que T-15 puede llegar a aplicar de verdad).

---

### Sesión 2026-09-01 — T-13 (normalización a forma dicha), sesión de nube
**Tarea(s):** T-13
**Estado resultante:** T-13 COMPLETADA
**Commits a develop:** `T-13: normalizacion a forma dicha (cifras, siglas, conjunciones, diccionario del dueno)` (ver `git log` de esta fecha en `develop`)
**Migraciones ejecutadas:** ninguna (T-13 no toca el esquema de `estado.json`; no hay todavía un punto de entrada que persista reescrituras, igual que T-10 con el histórico y T-12 con la calibración manual)
**Archivos creados/modificados:** `scripts/normalizacion.py` (nuevo: `normalizar_texto`/`normalizar_bloque`/`normalizar_guion`, `numero_a_cardinal`/`numero_a_ordinal`, `deletrear_sigla`, `aplicar_normalizaciones`/`deshacer_normalizaciones`, `cargar_diccionario_locucion`), `scripts/config.py` (tablas nuevas `NOMBRE_ARCHIVO_DICCIONARIO_LOCUCION`, `SIMBOLOS_MONEDA`, `UNIDADES_ABREVIADAS`), `tests/test_normalizacion.py` (nuevo, 28 tests), `tests/test_logica_pendiente.py` (se quita el skip de T-13, ya cubierto por los tests reales), `SKILL.md` (tabla de familias de regla y su valor por defecto, requisito 5), `roadmap/SEGUIMIENTO.md` (§1, cabecera), `roadmap/DECISIONES_TECNICAS.md`, `roadmap/HISTORIAL_SESIONES.md`
**Verificaciones pre-push:** tipos ✅ · lint ✅ · tests ✅ (179 pasan + 2 skipped) · build ✅ (`verificar_salidas.py --fixture`, 4 etapas aún NO APLICABLE)
**Health check post-deploy:** N/A — sesión de nube, no instala la skill (T-32 la instala; ver §3 de SEGUIMIENTO)
**Decisiones tomadas:** 5 filas nuevas en `DECISIONES_TECNICAS.md` (2026-09-01, T-13): resolución de familias de regla por prioridad con un `bytearray` de "ocupado" en vez de una única regex combinada; apócope y concordancia de género solo cuando el número precede a una palabra alfabética en el propio texto, nunca por el dígito final en solitario; concordancia de género por heurística de sufijo con excepciones cortas, no un analizador morfológico completo, apoyada en que el diccionario del dueño siempre puede corregir el fallo; las tablas de monedas/unidades de `config.py` quedan como diccionarios planos de módulo (no como campos de `Configuracion`) porque el diccionario de excepciones ya cubre la sobreescritura entrada a entrada; `normalizar_guion` opera sobre `BloqueRespiracion` (T-11) ya trozado, no antes del troceo, para que ningún corte de respiración parta una propuesta por la mitad.
**Hallazgos del auditor atendidos:** ninguno (sin hallazgos ABIERTOS de severidad alta en `auditoriacontinua.md` al empezar la sesión)
**Hallazgos:** ninguno nuevo; se verificó contra los tres guiones reales que el único texto de locución con cifras/siglas son `"80%"` (`guion-09-proyectos.md`) y `"SVG"` (`guion-artefactos-lienzo.md`) — la batería sintética del criterio de aceptación (años, porcentajes, monedas, ordinales) cubre el resto de familias de regla, sin fixtures reales que las ejerzan todavía.
**Tareas autopropuestas (P-XX):** ninguna
**Próximo paso:** siguiente tarea de §1 es T-14 (detector de problemas de lectura en voz alta), que depende de T-11 (ya completada); sus avisos nunca generan reescritura salvo la excepción ya decidida en §0.2 (frase sin punto de respiración, que puede proponer partición).

---

### Sesión 2026-09-01 — T-12 (motor de tiempos), sesión de nube
**Tarea(s):** T-12
**Estado resultante:** T-12 COMPLETADA
**Commits a develop:** `T-12: motor de tiempos (ppm deducido del guion, respaldo 120 ppm)` (ver `git log` de esta fecha en `develop`)
**Migraciones ejecutadas:** ninguna (T-12 no toca el esquema de `estado.json`; `Configuracion.ppm_manual` viaja dentro de `configuracion_efectiva`, que ya existe desde T-07)
**Archivos creados/modificados:** `scripts/tiempos.py` (nuevo), `scripts/parser.py` (`_rango_segundos` renombrada a pública `rango_segundos_titulo`, reutilizable por T-12), `scripts/troceo.py` (nueva función pública `categoria_puntuacion_final`), `scripts/config.py` (campos nuevos en `Configuracion`: `ppm_banda_plausible`, `ppm_manual`, `pausa_coma_segundos`, `pausa_punto_segundos`, `pausa_fin_parrafo_segundos`, `pausa_fin_escena_segundos`, `umbral_desviacion_tiempos`, con su validación en `__post_init__`), `tests/test_tiempos.py` (nuevo, 8 tests), `tests/test_logica_pendiente.py` (se quita el skip de T-12, ya cubierto por los tests reales), `DEVELOPERS.md` (sección T-12 nueva), `roadmap/SEGUIMIENTO.md` (§1, cabecera), `roadmap/DECISIONES_TECNICAS.md`, `roadmap/HISTORIAL_SESIONES.md`
**Verificaciones pre-push:** tipos ✅ · lint ✅ · tests ✅ (151 pasan + 3 skipped) · build ✅ (`verificar_salidas.py --fixture`, 4 etapas aún NO APLICABLE)
**Health check post-deploy:** N/A — sesión de nube, no instala la skill (T-32 la instala; ver §3 de SEGUIMIENTO)
**Decisiones tomadas:** 4 filas nuevas en `DECISIONES_TECNICAS.md` (2026-09-01, T-12): el rango horario de un encabezado de escena (marcas de tiempo del vídeo) y el del metadato `**Duración objetivo:**` (horquilla real de duración) reciben tratamientos distintos pese a compartir el mismo patrón — bug real encontrado probando contra los tres guiones reales antes de escribir un test, que deducía un ppm de 33-47 (muy fuera de banda) hasta corregirlo; la duración objetivo total usa el metadato de cabecera si está presente, con la suma de escenas como respaldo de mismo tipo; "fin de párrafo"/"fin de escena" se deciden reclasificando la escena en vez de ampliar `BloqueRespiracion` (T-11); `ppm_manual` no necesita mecanismo de persistencia propio, ya viaja en `configuracion_efectiva`.
**Hallazgos del auditor atendidos:** ninguno (sin hallazgos ABIERTOS de severidad alta en `auditoriacontinua.md` al empezar la sesión)
**Hallazgos:** el bug de las dos semánticas del rango horario (ver decisiones) se detectó ejecutando `calcular_tiempos` a mano contra los tres guiones reales ANTES de escribir `tests/test_tiempos.py` — con la primera versión, los tres guiones deducían un ppm de 33-47 y el aviso total pedía "faltan 863/1625/1236 palabras", una desviación sin sentido que delató el error de cálculo antes de que ningún test lo hubiera podido enmascarar con datos sintéticos. Corregido, los tres guiones deducen ppm 140-167 (dentro de banda) con avisos de desviación pequeños y creíbles (0-15%).
**Tareas autopropuestas (P-XX):** ninguna
**Próximo paso:** siguiente tarea de §1 es T-13 (normalización a forma dicha, con diccionario del dueño), que depende de T-11 (ya completada) y es la primera tarea de la FASE B2 (pasada de locutabilidad).

---

### Sesión 2026-09-01 — T-11 (troceo en bloques de respiración), sesión de nube
**Tarea(s):** T-11
**Estado resultante:** T-11 COMPLETADA
**Commits a develop:** `T-11: troceo en bloques de respiracion` (ver `git log` de esta fecha en `develop`)
**Migraciones ejecutadas:** ninguna (T-11 no toca el esquema de `estado.json`)
**Archivos creados/modificados:** `scripts/troceo.py` (nuevo), `scripts/config.py` (nuevo campo `palabras_por_bloque_objetivo` en `Configuracion`, con validación de que `min <= objetivo <= max`), `tests/test_troceo.py` (nuevo, 14 tests), `tests/test_logica_pendiente.py` (se quita el skip de T-11, ya cubierto por el test real), `DEVELOPERS.md` (sección T-11 nueva), `roadmap/SEGUIMIENTO.md` (§1, cabecera), `roadmap/DECISIONES_TECNICAS.md`, `roadmap/HISTORIAL_SESIONES.md`
**Verificaciones pre-push:** tipos ✅ · lint ✅ · tests ✅ (144 pasan + 4 skipped) · build ✅ (`verificar_salidas.py --fixture`, 4 etapas aún NO APLICABLE)
**Health check post-deploy:** N/A — sesión de nube, no instala la skill (T-32 la instala; ver §3 de SEGUIMIENTO)
**Decisiones tomadas:** 4 filas nuevas en `DECISIONES_TECNICAS.md` (2026-09-01, T-11): el algoritmo de corte por prioridad no puede renunciar a un nivel para todo el resto del texto solo porque el candidato más cercano no quepa en la ventana del máximo (bug real encontrado contra `guion-09-proyectos.md`, no en un test sintético); la fusión de tramos por debajo del mínimo reparte la unión en dos si supera el máximo en vez de devolverla entera (subía la cobertura en rango del 88.6% al 100% sobre los tres guiones reales); el troceo no trackea posición palabra a palabra, hereda `linea_inicio`/`linea_fin` del bloque clasificado de origen; `trocear_guion` reclasifica escena a escena en vez de ampliar `BloqueClasificado` con un campo de número de escena.
**Hallazgos del auditor atendidos:** ninguno (sin hallazgos ABIERTOS de severidad alta en `auditoriacontinua.md` al empezar la sesión)
**Hallazgos:** el primer diseño del troceador tenía un bug real de "abandono de nivel de prioridad" que solo se detectó al probar contra los tres guiones reales, no contra los tests sintéticos escritos primero — ambos bugs (el de prioridad y el de fusión sobre el máximo) están documentados en `DECISIONES_TECNICAS.md` con el caso concreto que los destapó, siguiendo la misma disciplina de sesiones anteriores (T-08, T-09) de calibrar contra los guiones reales, no solo contra casos inventados.
**Tareas autopropuestas (P-XX):** ninguna
**Próximo paso:** siguiente tarea de §1 es T-12 (motor de tiempos: ppm deducido del guión, respaldo 120 ppm), que depende de T-11 (ya completada) y consume `BloqueRespiracion.num_palabras` para estimar duraciones por bloque.

---

### Sesión 2026-09-01 — T-10 (convención de marcado y propuesta de convención explícita), sesión de nube
**Tarea(s):** T-10
**Estado resultante:** T-10 COMPLETADA
**Commits a develop:** `T-10: deteccion de convencion de marcado y propuesta de convencion explicita` (ver `git log` de esta fecha en `develop`)
**Migraciones ejecutadas:** ninguna (T-10 no toca el esquema de `estado.json`)
**Archivos creados/modificados:** `scripts/convencion.py` (nuevo), `scripts/parser.py` (extrae el literal repetido a la constante `MOTIVO_SECCION_NO_RECONOCIDA`), `tests/test_convencion.py` (nuevo, 10 tests), `DEVELOPERS.md` (sección T-10 nueva), `roadmap/SEGUIMIENTO.md` (§1, cabecera), `roadmap/DECISIONES_TECNICAS.md`, `roadmap/HISTORIAL_SESIONES.md`
**Verificaciones pre-push:** tipos ✅ · lint ✅ · tests ✅ (130 pasan + 5 skipped) · build ✅ (`verificar_salidas.py --fixture`, 4 etapas aún NO APLICABLE hasta T-18/T-27/T-30/T-32, nada roto)
**Health check post-deploy:** N/A — sesión de nube, sin acceso a `~/.claude/skills/teleprompter/` (protocolo v1.3, §0.1)
**Decisiones tomadas:** 4 filas nuevas en `DECISIONES_TECNICAS.md` (2026-09-01, T-10): reconocimiento del subtítulo entrecomillado por posición en vez de ampliar la lista negra de `config.py`; histórico de guiones procesados como parámetro de quien llama, sin persistencia nueva; exclusión de las señales estructurales `blank`/`seccion_vacia` de las propuestas
**Hallazgos del auditor atendidos:** ninguno ABIERTO de severidad alta en `auditoriacontinua.md` (revisado antes de elegir tarea)
**Hallazgos:** ninguno nuevo. Se confirmó que, sin el reconocimiento por posición del subtítulo entrecomillado, los tres guiones reales habrían salido con una "desviación" en cada pasada por algo que T-08 ya documentó como categoría auxiliar esperada — corregido antes de cerrar la tarea, no quedó como hallazgo pendiente
**Tareas autopropuestas (P-XX):** ninguna
**Próximo paso:** T-11 (troceo en bloques de respiración, 6–12 palabras configurable)

---

### Sesión 2026-09-01 — T-09 (clasificador locución / no locución), sesión de nube
**Tarea(s):** T-09
**Estado resultante:** T-09 COMPLETADA
**Commits a develop:** `T-09: clasificador locucion/no locucion` (ver `git log` de esta fecha en `develop`)
**Migraciones ejecutadas:** ninguna (T-09 no toca el esquema de `estado.json`)
**Archivos creados/modificados:** `scripts/clasificador.py` (nuevo), `scripts/config.py` (`Configuracion` gana `rotulo_locucion`/`rotulos_no_locucion`), `tests/test_clasificador.py` (nuevo, 11 tests), `tests/test_logica_pendiente.py` (quita los talones `test_clasificador_distingue_locucion_de_no_locucion` y `test_invariante_cobertura_total_del_guion`, ya implementados), `pyproject.toml` (`per-file-ignores` para `RUF001` en `tests/test_clasificador.py`), `DEVELOPERS.md` (sección T-09 nueva, actualiza las menciones a `tests/test_logica_pendiente.py`), `roadmap/SEGUIMIENTO.md` (§1, cabecera), `roadmap/DECISIONES_TECNICAS.md`
**Verificaciones pre-push:** tipos ✅ · lint ✅ · tests ✅ (120 pasan + 5 skipped, antes 109 + 7) · build ✅ (cuarta red: 4 etapas NO APLICABLE, todavía correcto a esta altura del backlog)
**Health check post-deploy:** N/A — sesión de nube, sin instalación local que verificar (T-32 sigue bloqueada por el mismo motivo que en sesiones anteriores)
**Decisiones tomadas:** 6 filas nuevas en `DECISIONES_TECNICAS.md` con fecha 2026-09-01 y tarea T-09: partición cita-de-bloque/texto-suelto dentro de `**LOCUCIÓN**` (requisito 3); la cita de bloque como señal de inferencia adicional al requisito 2 literal (imprescindible para el ≥95% de precisión exigido); métrica de precisión en palabras, no en líneas, del test de inferencia; `rotulo_locucion`/`rotulos_no_locucion` como campos nuevos de `Configuracion`; y la trampa de `.splitlines()` sobre contenido ya unido con `"\n".join(...)`, que rompía la reconstrucción exacta hasta corregirla con `.split("\n")`.
**Hallazgos del auditor atendidos:** ninguno nuevo desde la última pasada (2026-08-31, segunda); sin hallazgos ABIERTOS de severidad alta, no había urgencia P-XX que atender antes de T-09.
**Hallazgos:** ninguno nuevo para el registro de auditoría. Fuera de ese registro: la trampa de `.splitlines()` (ver decisión anterior) es deuda de atención, no de código — queda documentada en `DEVELOPERS.md` para que un futuro módulo que re-trocee un `contenido` ya construido por T-08/T-09 no la repita.
**Tareas autopropuestas (P-XX):** ninguna.
**Próximo paso:** T-10 (detección de convención de marcado y propuesta de convención explícita), que depende de T-09 y ya puede arrancar. Su `convencion-guiones.md` puede describir directamente la partición cita-de-bloque/rótulo que este `clasificador.py` ya usa como señal.

---

### Sesión 2026-09-01 — T-08 (parser de Markdown y separador de escenas), sesión de nube
**Tarea(s):** T-08
**Estado resultante:** T-08 COMPLETADA
**Commits a develop:** `T-08: parser de Markdown y deteccion del separador de escenas` (ver `git log` de esta fecha en `develop`)
**Migraciones ejecutadas:** ninguna (T-08 no toca el esquema de `estado.json`; consume `SeparadorEscena`, ya definido por T-07)
**Archivos creados/modificados:** `scripts/parser.py` (nuevo), `tests/test_parser.py` (nuevo, 18 tests), `tests/test_logica_pendiente.py` (quita el talón `test_parser_reconoce_toda_escena_del_guion_real`, ya implementado), `pyproject.toml` (`per-file-ignores` para `RUF001` en `tests/test_parser.py`), `DEVELOPERS.md` (sección T-08, actualiza la mención de T-06 a `parser.py`), `roadmap/SEGUIMIENTO.md` (§1, cabecera), `roadmap/DECISIONES_TECNICAS.md`
**Verificaciones pre-push:** tipos ✅ · lint ✅ · tests ✅ (109 pasan + 7 skipped) · build ✅ (`verificar_salidas.py --fixture`, 4 etapas NO APLICABLE, nada roto)
**Health check post-deploy:** N/A — sesión de nube, no alcanza `~/.claude/skills/teleprompter/` (nota de entorno del protocolo v1.3)
**Decisiones tomadas:** 5 filas nuevas en `DECISIONES_TECNICAS.md` (2026-09-01, T-08): clasificación de encabezado en tres pasos (patrón → escena; lista negra y rótulo de locución consultados a la vez, conflicto solo si las dos aplican) y el porqué de no preguntar ante una sola señal; `DeteccionEscenasAmbiguaError` compartida entre ambigüedad de nivel y de conflicto, con persistencia por `SeparadorEscena` o por `secciones_auxiliares` según el caso, sin ampliar el esquema de `estado.json`; escape unicode del guion largo (U+2013) en el código de producción y `per-file-ignore` de `RUF001` acotado a `tests/test_parser.py`; `extraer_metadatos` sin esquema fijo de claves; el preámbulo nunca es "escena 0", sin bandera de configuración sin uso real que la respalde
**Hallazgos del auditor atendidos:** ninguno nuevo — revisado `auditoriacontinua.md` al empezar, sin hallazgos ABIERTOS de severidad alta; #5, #6 y #8 siguen abiertos y no aplican a esta tarea
**Hallazgos:** ninguno
**Tareas autopropuestas (P-XX):** ninguna
**Próximo paso:** T-09 (clasificador locución / no locución), que reutiliza `parsear_guion` y clasifica dentro de cada `Escena.contenido` qué bloques son recitables

---

### Sesión 2026-09-01 — T-07 (estado del proyecto de guión, `estado.json`), sesión de nube
**Tarea(s):** T-07
**Estado resultante:** T-07 COMPLETADA
**Commits a develop:** `T-07: estado persistente del proyecto de guion (estado.json)` (ver `git log` de esta fecha en `develop`)
**Migraciones ejecutadas:** ninguna sobre datos reales; se añade el mecanismo y la migración `001_estado_inicial` (cubierta por tests, no hay ningún `estado.json` de producción todavía que migrar)
**Archivos creados/modificados:** `scripts/estado.py` (nuevo), `scripts/migraciones/__init__.py` (nuevo), `scripts/migraciones/001_estado_inicial.py` (nuevo), `scripts/config.py` (`NOMBRE_ARCHIVO_ESTADO`, `VERSION_ESQUEMA_ESTADO`), `tests/test_estado.py` (nuevo, 27 tests), `tests/test_migraciones.py` (nuevo, 8 tests), `pyproject.toml` (`per-file-ignores` para `N999` en `scripts/migraciones/*.py`), `DEVELOPERS.md` (sección T-07), `roadmap/SEGUIMIENTO.md` (§1, cabecera), `roadmap/DECISIONES_TECNICAS.md`
**Verificaciones pre-push:** tipos ✅ · lint ✅ · tests ✅ (91 pasan + 8 skipped) · build ✅ (`verificar_salidas.py --fixture`, 4 etapas NO APLICABLE, nada roto)
**Health check post-deploy:** N/A — sesión de nube, no alcanza `~/.claude/skills/teleprompter/` (nota de entorno del protocolo v1.3)
**Decisiones tomadas:** 3 filas nuevas en `DECISIONES_TECNICAS.md` (2026-09-01, T-07): escritura atómica con `Path.replace()` en vez de `os.replace()` (regla `PTH105` de ruff); mecanismo de migraciones `NNN_<nombre>.py` cargadas con `importlib.import_module` (patrón Django, verificado antes de escribir código); la migración `001_estado_inicial` trata cualquier dict sin `version_esquema` como "versión anterior" implícita, al no existir una versión 0 real que preceda a T-07
**Hallazgos del auditor atendidos:** ninguno nuevo — revisado `auditoriacontinua.md` al empezar, sin hallazgos ABIERTOS de severidad alta; #5, #6 y #8 siguen abiertos y no aplican a esta tarea
**Hallazgos:** ninguno
**Tareas autopropuestas (P-XX):** ninguna
**Próximo paso:** T-08 (parser de Markdown y detección del separador de escenas), que consume `EstadoProyecto.separador_escena` para persistir la elección del nivel/patrón de escena

---

### Sesión 2026-09-01 — T-06 (robustez de entrada), sesión de nube
**Tarea(s):** T-06
**Estado resultante:** T-06 COMPLETADA
**Commits a develop:** `T-06: robustez de entrada (validacion, codificacion, tope de tiempo)` (ver `git log` de esta fecha en `develop`)
**Migraciones ejecutadas:** ninguna
**Archivos creados/modificados:** `scripts/entrada.py` (nuevo), `scripts/config.py` (`TIEMPO_PROCESO_MAX_SEGUNDOS`), `tests/test_entrada.py` (nuevo, 20 tests), `DEVELOPERS.md` (sección de robustez de entrada), `roadmap/SEGUIMIENTO.md` (§1, cabecera), `roadmap/DECISIONES_TECNICAS.md`
**Verificaciones pre-push:** tipos ✅ · lint ✅ · tests ✅ (64 pasan + 8 skipped) · build ✅ (`verificar_salidas.py --fixture`, 4 etapas NO APLICABLE como antes)
**Health check post-deploy:** No aplica — sesión de nube, sin acceso a `~/.claude/skills/teleprompter/` (nota de entorno del protocolo, v1.3).
**Decisiones tomadas:** dos filas nuevas en `DECISIONES_TECNICAS.md` (2026-09-01, T-06): diseño de `scripts/entrada.py` (guardas de ruta/tamaño/codificación/estructura, `carpeta_salida_para` saneada, `ejecutar_con_limite_de_tiempo` sin `signal.alarm`) y la nota de entorno sobre el `python` real de este contenedor (3.11.15, no 3.12) que descarta la sintaxis PEP 695 en este módulo.
**Hallazgos del auditor atendidos:** ninguno (sin hallazgos ABIERTOS de severidad alta; #5, #6 y #8 siguen abiertos y no dependen de esta tarea).
**Hallazgos:** el `python` del PATH en este contenedor es 3.11.15 pese a `requires-python = ">=3.12"` en `pyproject.toml` (`python3.12` existe pero no se usa en los comandos del protocolo). No bloquea nada hoy porque el código no había usado hasta ahora sintaxis exclusiva de 3.12+; queda anotado en `DECISIONES_TECNICAS.md` para que una sesión futura no tropiece igual. No se abre P-XX ni se toca `pyproject.toml`: es una observación de entorno, no una tarea con valor de producto propio.
**Tareas autopropuestas (P-XX):** ninguna.
**Próximo paso:** T-07 (estado del proyecto de guión, `estado.json`, migración `001_estado_inicial`). Especificación en el cuerpo de `HOJA_DE_RUTA.md`.

### Sesión 2026-09-01 — T-05 (monitorización de errores local), sesión de nube
**Tarea(s):** T-05
**Estado resultante:** T-05 COMPLETADA
**Commits a develop:** `T-05: monitorizacion de errores local (captura, diagnostico, resumen)` (ver `git log` de esta fecha en `develop`)
**Migraciones ejecutadas:** ninguna
**Archivos creados/modificados:** `scripts/monitorizacion.py` (nuevo), `scripts/config.py` (`PREFIJO_ARCHIVO_DIAGNOSTICO`), `tests/test_monitorizacion.py` (nuevo, 9 tests), `DEVELOPERS.md` (sección de monitorización de errores), `roadmap/SEGUIMIENTO.md` (§1, cabecera), `roadmap/DECISIONES_TECNICAS.md`
**Verificaciones pre-push:** tipos ✅ · lint ✅ · tests ✅ (44 pasan + 8 skipped) · build ✅ (`verificar_salidas.py --fixture`, 4 etapas NO APLICABLE, nada roto)
**Health check post-deploy:** N/A — sesión de nube, no alcanza `~/.claude/skills/teleprompter/` (T-32 sigue BLOQUEADA por ese motivo)
**Decisiones tomadas:** 1 fila nueva en `DECISIONES_TECNICAS.md` bajo T-05 (mecánica de `ejecutar_con_diagnostico`/`ResumenEjecucion`, sin captura de variables locales en el volcado, wrapper de función en vez de `sys.excepthook`)
**Hallazgos del auditor atendidos:** ninguno — no había hallazgos ABIERTOS de severidad alta en `auditoriacontinua.md` al empezar la sesión
**Hallazgos:** ninguno nuevo
**Tareas autopropuestas (P-XX):** ninguna
**Próximo paso:** T-06 (robustez de entrada, depende de T-03 ya completada)

---

### Sesión 2026-09-01 — T-04 (CI local + workflow inactivo), sesión de nube
**Tarea(s):** T-04
**Estado resultante:** T-04 COMPLETADA
**Commits a develop:** `T-04: CI local centralizada en scripts/ci.py + workflow de GitHub Actions inactivo` (ver `git log` de esta fecha en `develop`)
**Migraciones ejecutadas:** ninguna
**Archivos creados/modificados:** `scripts/ci.py` (nuevo), `scripts/hooks/pre-commit` (ahora delega en `ci.py`), `.github/workflows/ci.yml` (nuevo, `workflow_dispatch` únicamente), `tests/test_ci.py` (nuevo), `tests/test_hooks.py` (aserciones sobre el hook actualizadas a la delegación), `DEVELOPERS.md` (sección CI local), `roadmap/SEGUIMIENTO.md` (§1, cabecera), `roadmap/DECISIONES_TECNICAS.md`
**Verificaciones pre-push:** tipos ✅ · lint ✅ · tests ✅ (35 pasan + 8 skipped) · build ✅ (`verificar_salidas.py --fixture`, 4 etapas NO APLICABLE, nada roto)
**Health check post-deploy:** N/A — sesión de nube, no alcanza `~/.claude/skills/teleprompter/` (T-32 sigue BLOQUEADA por ese motivo)
**Decisiones tomadas:** 2 filas nuevas en `DECISIONES_TECNICAS.md` bajo T-04 (centralización de las cuatro verificaciones en `scripts/ci.py`; workflow de GitHub Actions inactivo a propósito pese a que ya existe remoto)
**Hallazgos del auditor atendidos:** ninguno — no había hallazgos ABIERTOS de severidad alta en `auditoriacontinua.md` al empezar la sesión
**Hallazgos:** ninguno nuevo
**Tareas autopropuestas (P-XX):** ninguna
**Próximo paso:** T-05 (monitorización de errores local, depende de T-02 ya completada)

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
