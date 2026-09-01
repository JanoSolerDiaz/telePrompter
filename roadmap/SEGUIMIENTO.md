# SEGUIMIENTO — teleprompter — Hub / panel de control

> Hub del registro repartido (ver §0.4 de `HOJA_DE_RUTA.md`). Aquí viven el estado y lo
> transversal; el detalle vive en los documentos vivos de `roadmap/`.
> El dueño no revisa el código: revisa este documento.
>
> **Documentos hermanos:** las **decisiones técnicas** están en `DECISIONES_TECNICAS.md`
> (antiguo §2) y la **bitácora de sesiones** en `HISTORIAL_SESIONES.md` (antiguo §8). Las
> secciones no se renumeran para no romper referencias.

**Hoja de ruta de referencia:** `HOJA_DE_RUTA.md` v1.1 (2026-08-31)
**Modo de operación:** AUTONOMÍA TOTAL
**Última actualización:** 2026-09-01 — T-03 (suite de tests mínima) COMPLETADA por una sesión de nube. Su criterio de aceptación cita lógica (parser, clasificador, troceador, motor de tiempos, normalizador, `.srt`) que todavía no existe — esas tareas van después en §1 y solo dependen de T-01 —, así que el hueco se trató como una etapa "NO APLICABLE" expresada en tests: `tests/test_logica_pendiente.py` reúne 8 tests con `@pytest.mark.skip(reason="T-XX: …")` (uno por capacidad pendiente más las invariantes (a) y (c) de §0.2), cada uno con el contrato exacto que deberá cumplir cuando su tarea aterrice. Lo que sí existe hoy —el contrato de convención de `config.py` (`PATRON_ENCABEZADO_ESCENA`, `ROTULO_LOCUCION`, `ROTULOS_NO_LOCUCION`)— se cubre con 5 tests reales en `tests/test_convencion_guiones_reales.py` contra los tres guiones de `fixtures/reales/`, apoyados en `tests/conftest.py` (fixtures `guiones_reales`/`texto_guiones_reales`, reutilizables por T-08 y siguientes). Detalle en `DECISIONES_TECNICAS.md`. Suite: 29 pasan + 8 skipped (antes 24 pasan). Las cuatro verificaciones en verde. Sin hallazgos ABIERTOS de severidad alta en `auditoriacontinua.md`. Siguiente tarea: T-04 (CI local + workflow inactivo).

---

> ## ⚑ PARA EL DUEÑO — empieza por aquí
> Lo único que el proyecto necesita de ti está en dos sitios de este documento:
> - **§3 Bloqueos** = tu lista de tareas. Quedan **dos**: instalar el paquete de `480-branded-pptx` (solo afecta a la salida `.pptx`) y probar el clicker cuando haya reproductor (T-24). La funcionalidad asociada queda *latente* hasta que las resuelvas.
> - **§6 Preguntas abiertas** = tus decisiones. **Ninguna pendiente**: las ocho están resueltas.
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
| T-04 | CI (local + workflow inactivo) | PENDIENTE | — | — |
| T-05 | Monitorización de errores (local) | PENDIENTE | — | Sin servicio externo: regla de cero red |
| T-06 | Robustez de entrada | PENDIENTE | — | Equivalente al rate limiting |
| T-07 | Estado del proyecto de guión (`estado.json`) | PENDIENTE | — | Migración `001_estado_inicial` |
| T-08 | Parser Markdown y separador de escenas | PENDIENTE | — | Escenas = `## BLOQUE N — … (m:ss – m:ss)`; hay `##` que no son escena |
| T-09 | Clasificador locución / no locución | PENDIENTE | — | Ruta rápida por `**LOCUCIÓN**` / `**EN PANTALLA**`; inferencia de respaldo |
| T-10 | Convención de marcado propuesta | PENDIENTE | — | Formaliza la convención ya existente; genera `convencion-guiones.md` |
| T-11 | Troceo en bloques de respiración | PENDIENTE | — | 6–12 palabras configurable |
| T-12 | Motor de tiempos (ppm deducido del guión) | PENDIENTE | — | Respaldo 120 ppm; contraste estimado vs. duración objetivo |
| T-13 | Normalización a forma dicha | PENDIENTE | — | Con diccionario del dueño |
| T-14 | Detector de problemas de locución | PENDIENTE | — | Avisa, no modifica |
| T-15 | Reescrituras marcadas y reversibles | PENDIENTE | — | Alcance acotado: forma dicha y respiración |
| T-16 | `guion-escenas.md` de una sola pasada | PENDIENTE | — | Documento de revisión |
| T-17 | Revalidación (respeta ediciones) | PENDIENTE | — | Ciclo iterable |
| T-18 | Reproductor: esqueleto autocontenido | PENDIENTE | — | Validador de auto-contención |
| T-19 | Índice de escenas y pantalla completa | PENDIENTE | — | — |
| T-20 | Motor de avance híbrido | PENDIENTE | — | Auto + manual sin salir de modo |
| T-21 | Resaltado, tipografía y tema | PENDIENTE | — | Legibilidad sobre branding |
| T-22 | Autoscroll con bloque centrado | PENDIENTE | — | — |
| T-23 | Ayudas de grabación | PENDIENTE | — | Cuenta atrás, cronómetro, progreso |
| T-24 | Atajos y clicker Bluetooth | PENDIENTE | — | — |
| T-25 | Modo espejo | PENDIENTE | — | — |
| T-26 | Persistencia local de preferencias | PENDIENTE | — | localStorage con try/catch |
| T-27 | Exportador `.srt` borrador | PENDIENTE | — | Consumible por ffmpeg |
| T-28 | Exportador `.pdf` con marca 480 | PENDIENTE | — | Repaso / entregable; blanco, Poppins, logotipo con ratio medido del PNG |
| T-29 | Adaptador `.pptx` (`480-branded-pptx`) | PENDIENTE | — | `tarjetas.json` + brief; la delegación la hace Claude, no el código |
| T-30 | Selector de salidas por validación | PENDIENTE | — | Pregunta cada vez |
| T-31 | `SKILL.md` y configuración completa | PENDIENTE | — | Todo default documentado |
| T-32 | Instalación de la skill y guión de ejemplo | PENDIENTE | — | Es el "deploy" |
| T-33 | Encaje con la cadena de montaje | PENDIENTE | — | Contrato `.srt` + `tarjetas.json` |
| R-01 | Persistencia verificada + plan B | PENDIENTE | — | Oleada v2 · `origen: auditoría #5` |
| R-02 | Registro de tomas por escena | PENDIENTE | — | Oleada v2 · parte de rodaje |
| R-03 | Marcar tropiezos durante la toma | PENDIENTE | — | Oleada v2 · alimenta `FEEDBACK.md` |
| R-04 | Recalibrar el ritmo con tiempos reales | PENDIENTE | — | Oleada v2 · cierra el bucle de T-12 |
| R-05 | `.srt` alineado con la toma buena | PENDIENTE | — | Oleada v3 · continuidad con el montaje |
| R-06 | Coherencia de nombres y `assets/` | PENDIENTE | — | Fase F-D · `origen: auditoría #6` |

**Estados:** PENDIENTE · EN CURSO · COMPLETADA · DESPLEGADA EN PRODUCCIÓN · BLOQUEADA — <motivo> · DESCARTADA — <motivo>

*(La spec de cada tarea: T-XX en el cuerpo de `HOJA_DE_RUTA.md`; R-XX en `ROADMAP_PRODUCTO.md`. Este §1 NO repite la spec, solo el estado.)*

---

## 3. BLOQUEOS — ACCIONES PENDIENTES DEL DUEÑO

> El código se entrega igualmente; estas acciones activan funcionalidad latente.

| # | Acción | Tarea | Instrucciones exactas | Estado |
|---|--------|-------|-----------------------|--------|
| 1 | Instalar el plugin `skill-creator` (andamio de la skill) | T-00 | — | **RESUELTO 2026-08-31** — instalado (`skill-creator@claude-plugins-official`, ámbito usuario). |
| 2 | Aportar el **paquete** de `480-branded-pptx` | T-29 | El `SKILL.md` y el `brand-guide.md` ya están transcritos en `references/marca-480.md` (2026-08-31): bastan para el contrato, el brief y el estilo del PDF. Falta la skill instalada en `~/.claude/skills/480-branded-pptx/` con sus assets, y la skill `pptx` de la que depende. Hasta entonces la salida `.pptx` queda latente. | ABIERTO |
| 3 | Aportar 2–3 guiones de producción reales (`.md`) | T-09, T-10 | — | **RESUELTO 2026-08-31** — 3 guiones en `fixtures/reales/` (`guion-08-busqueda-investigacion`, `guion-09-proyectos`, `guion-artefactos-lienzo`). T-08 a T-12 recalibradas contra ellos en la hoja de ruta v1.1. |
| 4 | Conseguir los archivos de logotipo `480_*.png` | T-28 | — | **RESUELTO 2026-08-31** — las cuatro variantes en `assets/`, PNG RGBA con transparencia. **Ojo:** miden 1993×805 (ratio 2,4758), no el 1.7766 que dice la guía de marca; el ratio se mide del archivo. Ver `references/marca-480.md`. |
| 5 | Probar los atajos con el clicker Bluetooth real | T-24 | Abrir el reproductor generado, pulsar cada botón del mando y decir qué tecla envía cada uno. El agente ajusta el mapa. | ABIERTO |

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
---

## 7. DESVIACIONES RESPECTO A LA HOJA DE RUTA ORIGINAL

> Resumen consolidado para comparar contra `HOJA_DE_RUTA.md` de un vistazo.

| Fecha | Tarea | Desviación | Motivo |
|-------|-------|-----------|--------|
| 2026-08-31 | T-00 | Se trabajó y se commiteó en `develop`, no en `main` como fijaba §0.1 | **Desviación cerrada el mismo día:** el dueño resolvió §6.7 confirmando `develop` como rama de trabajo y `master` como suya para el merge manual. El protocolo se actualizó (hoja de ruta v1.2) y a partir de ahí `develop` deja de ser una desviación: es la norma. |
| 2026-08-31 | T-00 | No se ejecutó `git init` | Ya estaba hecho. El resto de la tarea se cumplió íntegro. |
| 2026-08-31 | T-00 | No se hizo push al remoto | El protocolo §0.1 contemplaba push porque en un proyecto web equivale a desplegar. Aquí el despliegue es la instalación local de la skill (T-32) y publicar en GitHub es una acción hacia fuera. **Incorporado a la norma en v1.2:** no se hace push sin autorización explícita del dueño. Deja de ser desviación. |
