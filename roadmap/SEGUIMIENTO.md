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
**Última actualización:** 2026-09-02 — T-21 (resaltado, tipografía y tema de grabación) COMPLETADA por una sesión de nube. Sin código estructural nuevo en `reproductor.py` más allá de siete claves nuevas en el JSON incrustado (`atenuacion_niveles`, `atenuacion_minima`, `tamano_texto_base_px`, `paso_tamano_texto_px`, `tamano_texto_minimo_px`, `tamano_texto_maximo_px`, `tiempo_inactividad_cursor_ms`) y dos marcadores nuevos en la plantilla de `estilo.css` (`__COLOR_ACENTO__`, `__MARGEN_SEGURO_PX__`), mismo patrón que T-20 para los límites de velocidad. Todo el trabajo vive en `assets/reproductor/guion.js` y `estilo.css`. Requisito 1 (resaltado con contexto atenuado): `marcarBloqueActivo` calcula, para cada bloque que no es el activo, `opacidadPorDistancia(distancia)` y la aplica como `style.opacity`; la distancia indexa el gradiente configurable `atenuacion_niveles` (por defecto `0.75, 0.5, 0.35`), y más allá del último nivel se aplica el suelo `atenuacion_minima` (`0.2`) para que el contexto nunca desaparezca del todo. Requisito 2 (tamaño de texto en vivo): teclas `[`/`]` llaman a `ajustarTamanoTexto`, que mueve una única preferencia global (no por escena, a propósito — ver decisión en `DECISIONES_TECNICAS.md`) dentro de `[24, 96]` px con paso de 4 px, aplicada a la variable CSS `--tamano-base`. Requisito 3 (contraste AAA): `reproductor.contraste_relativo` implementa la fórmula WCAG de luminancia relativa; un test nuevo verifica que los colores por defecto (`#f5f5f5` sobre `#0b0b0d`) superan la razón 7:1 exigida (real: ~18.5:1) — verificable en cada `pytest`, no solo a ojo. Requisito 4 (márgenes seguros y cursor oculto): `#app` usa ahora `padding: var(--margen-seguro)` (64 px por defecto, antes fijo) y un listener de `mousemove`/`fullscreenchange` oculta el cursor (`.cursor-oculto`) tras 3000 ms de inactividad, solo mientras hay pantalla completa activa. De paso se cerró una excepción a "sin números mágicos" que arrastraban T-19/T-20: el color de acento (`#f5c542`, usado en foco visible/pausa/borde activo) pasa a `color_acento_reproductor` en `Configuracion`. Verificado a mano con Playwright headless sobre el fixture real (`fixtures/salida/reproductor.html`): con el bloque activo en el índice 2, los bloques 0/1/3 muestran opacidad 0.5/0.75/0.75 exactamente como predicen los niveles por defecto; el tamaño de texto sube de 48 a 56 px con dos pulsaciones de `]` y se refleja en el indicador; el cursor se oculta tras la inactividad configurada y reaparece al mover el ratón — sin errores de consola en ningún paso. Suite: 288 pasan + 1 skipped (antes 281 + 1; 13 tests nuevos: 9 en `tests/test_reproductor.py`, 4 en `tests/test_esqueleto.py` para la validación de la nueva configuración). Las cuatro verificaciones en verde. Sin hallazgos ABIERTOS de severidad alta en `auditoriacontinua.md`. Siguiente tarea: T-22 (autoscroll con bloque centrado), quinta y última de FASE B4.
>
> **Sesión anterior (2026-09-02) — T-20 (motor de avance híbrido) COMPLETADA por una sesión de nube.** Sin código estructural nuevo en `reproductor.py`: los bloques ya traían `inicio_segundos`/`fin_segundos` (T-12 vía T-18), cuya diferencia es exactamente la duración a resaltar; solo se añaden tres claves de configuración al JSON incrustado (`paso_velocidad`, `velocidad_minima`, `velocidad_maxima`, nuevas en `Configuracion`) para que `guion.js` no las lleve escritas a mano. Todo el motor vive en `assets/reproductor/guion.js`. Requisito 1 (avance automático): `iniciarTemporizadorBloque()` arma un `setTimeout` con la duración del bloque activo entre su velocidad vigente; al disparar, `avanzarAutomatico()` mueve el índice y encadena el siguiente — no hay un intervalo global, cada bloque programa su propio reloj. Requisito 2 (velocidad ajustable en vivo, sin cortes): `+`/`-` (y `=`) llaman a `ajustarVelocidad`, que solo actualiza `velocidadesEscena[escenaActual]` (redondeada al paso configurado) y el indicador visible, sin tocar el temporizador en curso — el cambio se aplica desde el bloque siguiente. Requisito 3 (avance manual sin salir de modo ni reiniciar): `bloqueSiguienteManual`/`bloqueAnteriorManual` mueven el índice y reinician el reloj del bloque de destino con su duración completa, continuando en automático si no estaba en pausa. Requisito 4 (pausa exacta, reiniciar escena, navegación entre bloques y escenas): `togglePausa()` guarda los milisegundos restantes medidos desde la última marca de tiempo y los reutiliza tal cual al reanudar — verificado con Playwright que pausar/reanudar reproduce exactamente donde se dejó, incluso con varios ciclos seguidos; `R` reinicia la escena, `↑`/`↓` cambian de escena sin volver a pedir pantalla completa (`solicitarPantallaCompleta` ahora comprueba `document.fullscreenElement` antes de pedirla de nuevo). Requisito 5 (velocidad recordada por escena): `velocidadesEscena`, un array en memoria de la pestaña paralelo a `estadosEscena` (T-19) — persistirlo entre sesiones sigue siendo T-26, no esta tarea. Teclado adelantado del mapa final de T-24 (`Espacio`, `+`/`-`, flechas/`PageUp`/`PageDown`, `R`) para no tener que reasignarlo después. Resaltado del bloque activo (`.bloque--activo`) deliberadamente mínimo: el tratamiento completo (contexto atenuado, contraste AAA) es T-21, la tarea siguiente, y no se adelanta aquí. Verificado a mano con Playwright headless sobre el fixture real (`fixtures/salida/reproductor.html`, guion de 7 escenas/71 bloques): cadena de avances automáticos con tiempos reales, avance manual que no detiene el automático, pausa/reanudación exacta contra las duraciones reales de los bloques, velocidad que acelera medible en los avances por segundo, velocidad recordada al volver a una escena tras visitar otra, y retorno al índice con la escena marcada "Grabada" — sin errores de consola en ningún paso. Suite: 281 pasan + 1 skipped (antes 272 + 1; 9 tests nuevos: 6 en `tests/test_reproductor.py`, 3 en `tests/test_esqueleto.py` para la validación de los nuevos límites de velocidad). Las cuatro verificaciones en verde. Sin hallazgos ABIERTOS de severidad alta en `auditoriacontinua.md`. Siguiente tarea: T-21 (resaltado, tipografía y tema de grabación), cuarta de FASE B4.
>
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
| R-07 | Capítulos de YouTube con marcas de tiempo reales | PENDIENTE | — | Oleada v3 · une T-08 (sección auxiliar `Capítulos`) con R-02 (tomas) |

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
