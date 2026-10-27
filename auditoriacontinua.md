# AUDITORÍA CONTINUA — teleprompter

> Documento del agente Auditor (supervisor externo). Es el **único** archivo que el auditor
> modifica. Dos partes: un registro de hallazgos rastreable (arriba) y la narrativa por
> auditoría (debajo, la más reciente primero).
>
> Para que ningún hallazgo quede en saco roto: el **PM** convierte los hallazgos `ABIERTO` en
> tareas (R-XX o backlog) con `origen: auditoría #N`; los de **severidad alta** (seguridad,
> bug en producción, rotura de UX) los atiende el **programador** como P-XX urgente. En cada
> pasada, el auditor reevalúa los `ABIERTO` contra el código y los cierra o escala.

## REGISTRO DE HALLAZGOS

> Severidad: alta / media / baja. Estado: ABIERTO / RESUELTO / ASUMIDO (riesgo aceptado por el dueño). Numeración nunca reutilizada.

| #ID | Fecha | Área | Severidad | Estado | Resumen | Tarea / origen |
|-----|-------|------|-----------|--------|---------|----------------|
| #1 | 2026-08-31 | Proceso / git | alta | **RESUELTO** | El protocolo fijaba `main`, rama inexistente en el repo real. **Cerrado el mismo día:** el dueño confirmó `develop` como rama de trabajo y `master` como suya para el merge manual; hoja de ruta v1.2 (§0.1 y §0.2) y los tres prompts de agente actualizados. Verificado: ya no queda ninguna referencia a `main` en el protocolo ni en los prompts. | §0.1 · §6.7 |
| #2 | 2026-08-31 | Infraestructura | alta | **RESUELTO** | `.gitignore` excluye `assets/` y `fixtures/` completos. Quedan fuera del control de versiones los logotipos 480, los tres guiones de calibración y —en cuanto existan— las plantillas del reproductor (T-18) y el `guion-ejemplo.md` del health check (T-32). **Cerrado por P-01:** `.gitignore` acotado a artefactos generados; `assets/` y `fixtures/` versionados y presentes en el commit `e8b9663`. | P-01 · T-04 |
| #3 | 2026-08-31 | Producto / marca | alta | **RESUELTO** | Poppins no estaba instalada, lo que vaciaba de efecto la decisión tipográfica. **Cerrado:** el dueño la instaló el mismo día. Reverificado: 5 archivos (Bold, SemiBold, Medium, Regular, Light), cobertura completa de la escala de la guía de marca. | T-28 · §6.8 |
| #4 | 2026-08-31 | Calidad | media | **RESUELTO** | La 4ª verificación (`verificar_salidas.py --fixture`) es obligatoria desde T-00, pero su fixture no existe hasta T-32 y el generador HTML no existe hasta T-18: la red de seguridad quedaba incompleta durante casi todo el backlog. **Cerrado en T-00:** `verificar_salidas.py` declara cada etapa NO APLICABLE nombrando la tarea que la implementará, y se activará sola según avance el backlog. | T-00 |
| #5 | 2026-08-31 | Producto | media | **RESUELTO** | T-26 asumía que `localStorage` persiste al abrir el reproductor desde `file://`, sin verificación real ni plan B si fallaba. **Cerrado por R-01** (2026-09-03), reverificado de forma independiente en esta pasada (2026-09-04) leyendo `guion.js`: `comprobarAlmacenamientoDisponible()` (líneas ~68-79) detecta con certeza si `localStorage` no funciona y muestra un aviso visible en el índice; "Exportar/Importar preferencias" (~1288-1410) lee siempre de las variables en memoria (nunca de `localStorage` en el momento del clic) y descarga un `.json` vía Blob, con `window.prompt()` como segundo nivel de resguardo si la descarga fallara. Verificado además con Playwright/Chromium real (persiste entre cierres del mismo perfil, vacío en un perfil nuevo). Es un plan B real en código, no solo documentado. | R-01 |
| #6 | 2026-08-31 | Coherencia | baja | **RESUELTO** | Nomenclatura arrastrada del nombre anterior: la carpeta de salida era `<nombre-guion>-tarjetas/` con el proyecto ya llamado `teleprompter`, y `assets/` mezclaba logotipos de marca con plantillas del reproductor. **Cerrado por R-06** (2026-09-03), reverificado en esta pasada: `config.NOMBRE_SUFIJO_CARPETA_SALIDA = "-teleprompter"`, con migración automática de carpetas heredadas (`entrada._migrar_carpeta_salida_heredada`, copia `.bak` antes de renombrar, 7 tests en `test_entrada.py`) y `assets/` separado en `assets/marca/`, `assets/reproductor/`, `assets/pdf/`, cada una referenciada por separado en el código real (`config.py`, `reproductor.py`). | R-06 |
| #7 | 2026-08-31 | Trazabilidad | baja | **RESUELTO** | Los tres logs estaban vacíos con el proyecto ya commiteado. **Cerrado:** la sesión de T-00 dejó 7 decisiones en `DECISIONES_TECNICAS.md`, su entrada en `HISTORIAL_SESIONES.md` y tres desviaciones en §7 (dos ya cerradas al resolverse §6.7). El cambio a v1.2 sí está registrado en los tres sitios. | §0.4 |
| #8 | 2026-08-31 | Documentación | baja | **RESUELTO** | `DEVELOPERS.md` se referencia en §0.4 y en T-32 pero todavía no existía. **Cerrado por acumulación:** existe ya con 934 líneas y una sección por cada tarea completada (T-00 a T-21), mantenida sesión a sesión como parte del cierre de cada una — cumple de sobra lo que T-32 le exige, con antelación sobre esa tarea. | T-32 |
| #9 | 2026-09-02 | Invariantes / revalidación | **alta** | **RESUELTO** | Si en una misma revalidación coincidían una edición manual del dueño y la aceptación de una partición de respiración sobre ese mismo bloque, la identidad usada para localizar la edición no se traducía a las identidades resultantes de la partición y la edición se perdía en silencio. **Cerrado por P-02** (2026-09-02): `revalidacion.py` pospone la partición ese mismo pase cuando hay conflicto y deja una incidencia explícita; test de regresión (`test_edicion_manual_y_particion_aceptada_misma_pasada_no_pierde_edicion`) reproduce exactamente este escenario. Verificado de nuevo en esta pasada (2026-09-03): sigue en verde. El propio cierre documentó un límite distinto, no cubierto por esta corrección → **#14**. | `revalidacion.py` · invariante (c) |
| #10 | 2026-09-02 | Configuración / calidad | baja | **RESUELTO** | Dos colores de estado del índice del reproductor (`.escena-estado--grabada` `#4ade80`, `.escena-estado--revisada` `#60a5fa`, de T-19) estaban escritos a mano en `estilo.css` en vez de vivir en `Configuracion`. **Cerrado por R-08** (2026-09-03), reverificado en esta pasada: `COLOR_ESTADO_GRABADA_REPRODUCTOR`/`COLOR_ESTADO_REVISADA_REPRODUCTOR` en `config.py`, inyectados por `reproductor.py` como variables CSS (`--color-estado-grabada`/`--color-estado-revisada`); cero hex literal en `estilo.css`. | R-08 |
| #11 | 2026-09-02 | Documentación / coherencia | baja | **RESUELTO** | `PROYECTO.md` seguía describiendo el ritmo como «por defecto 120, propio de locución didáctica y pausada» — la decisión anterior a T-12. **Cerrado por R-08** (2026-09-03), reverificado en esta pasada: `PROYECTO.md:45` dice ahora «El ritmo base se deduce de las duraciones objetivo del propio guión; 120 ppm es solo el respaldo», palabra por palabra con §0.2. | R-08 |
| #12 | 2026-09-02 | Infraestructura | baja | **RESUELTO** | `pyproject.toml` exige Python ≥3.12, pero el intérprete real de las sesiones de nube es 3.11.15, sin corrección ni vigilancia más allá de una nota suelta. **Cerrado por R-08** (2026-09-03) por la vía de mitigación explícita en vez de bajar la versión declarada (decisión razonada en `DECISIONES_TECNICAS.md`): `scripts/ci.py` gana `avisar_si_version_python_diverge`, que lee el mínimo real de `pyproject.toml` con `tomllib` y avisa (sin bloquear) si el intérprete no lo alcanza, llamada desde `ci.main()`; 4 tests dedicados en `test_ci.py`. Reverificado en esta pasada: sigue vigente y en verde. | R-08 |
| #13 | 2026-09-02 | Robustez del validador | baja | **RESUELTO** | El validador de auto-contención cubría `http(s)://`/`@import`/`fetch`/`src=` externo, pero no `<object>`/`<embed src>`/`<base href>`/`WebSocket`/`EventSource`/`sendBeacon` ni `url(...)` de CSS. **Cerrado por R-09** (2026-09-03), reverificado en esta pasada: los seis patrones nuevos están en `PATRONES_RECURSO_EXTERNO` (`verificar_salidas.py`), con excepción `data:` donde corresponde (`<embed>`, `url()`) y 14 tests parametrizados en `test_esqueleto.py` (uno por patrón, más los de la excepción `data:`). Documentado en `references/validador-autocontencion.md`, incluida una tabla explícita de huecos deliberadamente fuera de alcance. Nota menor sin severidad propia: `<object data="data:...">` se sigue marcando como hallazgo aunque esté embebido en base64 (a diferencia de `<embed>`/`src=`) — verificado que es una política deliberada y documentada, no una inconsistencia. | R-09 |
| #15 | 2026-09-04 | Robustez / multiplataforma | media | **RESUELTO** | `entrada.leer_guion` decodificaba el guion con `read_bytes()` + `decode("utf-8-sig")` sin normalizar `\r\n`/`\r` a `\n`, a diferencia de otras rutas de lectura del propio proyecto que sí aplican la traducción universal de saltos de línea de Python. **Cerrado por R-10** (2026-09-04), verificado de nuevo en esta pasada leyendo el código: `entrada.py:118` aplica `texto.replace("\r\n", "\n").replace("\r", "\n")` justo después de `decode("utf-8-sig")`, con el motivo documentado en el propio docstring de `leer_guion`. La auditoría del 2026-09-05 ya había verificado el cierre en su narrativa pero dejó esta fila del registro sin actualizar a RESUELTO — corregido en esta pasada. | R-10 |
| #16 | 2026-09-04 | Robustez / datos (rodaje real) | media | **RESUELTO** | `tomas.duracion_toma_buena` no validaba que como mucho una toma estuviera marcada `buena` por escena; con dos tomas `buena: true` para la misma escena elegía la primera en silencio. **Cerrado por R-11** (2026-09-04), verificado de nuevo en esta pasada: `duracion_toma_buena` (`scripts/tomas.py:186-215`) ahora levanta `RegistroTomasError` citando los números de toma en conflicto cuando `len(buenas) > 1`, en vez de elegir. Misma nota que `#15`: la fila seguía ABIERTO en el registro pese a que la narrativa del 2026-09-05 ya daba el hallazgo por cerrado; corregido aquí. | R-11 |
| #17 | 2026-09-04 | Cobertura / salida derivada | baja | **RESUELTO** | `capitulos_youtube.calcular_capitulos` descartaba en silencio los títulos de capítulo sobrantes cuando había más filas en la sección «Capítulos» que escenas en el guion. **Cerrado por R-11** (2026-09-04), verificado de nuevo en esta pasada: `ResultadoCapitulos.titulos_sobrantes` (`scripts/capitulos_youtube.py`) expone los títulos que no llegaron a emparejarse por exceso, con el propio docstring citando este hallazgo por número. Fila corregida de ABIERTO a RESUELTO en esta pasada, igual que `#15`/`#16`. | R-11 |
| #18 | 2026-09-04 | Calidad / cobertura de tests | baja | **RESUELTO** | No existía test de integración cruzada entre `guion-alineado.srt` (R-05) y `capitulos-youtube.txt` (R-07) que confirmara marcas de tiempo mutuamente coherentes. **Cerrado por R-11** (2026-09-04), verificado de nuevo en esta pasada: `tests/test_integracion_montaje.py::test_srt_alineado_y_capitulos_youtube_son_coherentes_entre_si` reproduce exactamente ese cruce con un guion sintético de capítulos + tomas. Fila corregida de ABIERTO a RESUELTO en esta pasada. | R-11 |
| #19 | 2026-09-04 | Invariantes / revalidación (residual de #14) | baja | **RESUELTO** | El endurecimiento de P-04 (`_incidencias_anclas_desajustadas`) compara, por escena, solo el **conjunto/cantidad** de índices de ancla esperados contra los reales — no su contenido ni orden. Diez pasadas sucesivas de reconfirmación (2026-09-04 a 2026-09-14) sin escenario reproducido; el PM enrutó el hallazgo a **R-17** (fase F-I, commit `9c90b8e`, 2026-09-14) con instrucción de investigar primero antes de tocar `revalidacion.py`. **Cerrado por R-17** (`b9b6bcb`, 2026-09-15), verificado en esta pasada leyendo el diff completo y el test nuevo: la asimetría teórica **sí es real** (se construyó un caso concreto: dos disposiciones de `particiones_pospuestas` del mismo tamaño con miembro distinto — `{1}` en vez de `{0}` — coinciden en cardinalidad sin disparar el aviso), pero solo es alcanzable corrompiendo `estado.validacion["particiones_pospuestas"]` a mano entre pasadas — misma precondición ya conocida de P-04 — porque bajo operación normal esa disposición siempre coincide con la que la pasada anterior persistió (identidad inyectiva por construcción). Verificado además, no solo asumido, que incluso en el escenario corrompido el invariante (a) (nada se pierde ni se duplica) sigue intacto: interpretación y reconstrucción usan la misma disposición de forma autoconsistente y el documento se reconstruye completo; el único efecto observable es que la incidencia de conflicto P-04 puede citar el número de bloque equivocado dentro de la escena correcta (defecto cosmético del mensaje, no de contenido). No se endurece la comparación por decisión razonada (no hay señal independiente para detectar la corrupción sin desconfiar del dato que P-04 ya decidió no validar más allá del tipo). Test de regresión `test_disposicion_pospuesta_corrompida_con_mismo_tamano_no_pierde_ni_duplica_contenido` (`tests/test_revalidacion.py`) reproduce el caso construido y confirma ambas partes de la conclusión. 574→575 tests. | `scripts/revalidacion.py` · límite residual de P-04 · cerrado por **R-17** (F-I), commit `b9b6bcb`, 2026-09-15 |
| #24 | 2026-09-16 | Proceso / coherencia roadmap-código | baja | ABIERTO | Patrón recurrente, sin ningún riesgo real en ninguna repetición: la prosa de "Cola de producto" de `ROADMAP_PRODUCTO.md` queda desactualizada durante las reconfirmaciones horarias del Programador tras completarse cada R-XX, hasta que el ciclo de PM que archiva la oleada la corrige en el mismo commit — nunca más de una jornada, y `SEGUIMIENTO.md` §1 (fuente autoritativa) siempre correcto. El PM no puede resolverlo por su cuenta (cambiar quién escribe en qué documento es protocolo de §0.4, solo lo cambia el dueño); enrutado como pregunta de gobernanza `#11` de `SEGUIMIENTO.md` §6, **pendiente desde 2026-09-16**. **Repetido ya catorce veces** (R-17, R-19, R-22 a R-31 sin excepción salvo R-20, que el propio PM corrigió en el mismo commit de apertura), siempre autocorregido el mismo día de archivo. **Decimocuarta repetición, con R-31** (esta pasada, 2026-10-17): verificado con `git log --oneline 3cb5075..08a59de -- roadmap/ROADMAP_PRODUCTO.md` — el único commit que toca el archivo es `08a59de` (el propio archivo de PM); ninguna de las nueve reconfirmaciones horarias del Programador lo corrige. Historial completo de repeticiones anteriores recuperable con `git log -p -- auditoriacontinua.md`. Sigue `ABIERTO` únicamente a la espera de la respuesta del dueño a `#11`. **Reconfirmado sin desfase activo en esta pasada (2026-10-19):** el ciclo de PM del 2026-10-18 (`4cc381b`) volvió a reescribir la prosa de cabecera de `ROADMAP_PRODUCTO.md` en el mismo commit en que tomó su decisión (corrección de `#32` + especificación de R-33), sin que medie ninguna reconfirmación horaria del Programador de por medio — mismo patrón de autocorrección que el hallazgo describe, no una repetición nueva. **Sin desfase activo tampoco en esta pasada (2026-10-20):** `git log --oneline b4c597e..HEAD -- roadmap/ROADMAP_PRODUCTO.md` trae solo dos commits, `ef8727c` (R-33, que en el mismo commit archiva R-32 y abre R-33 — nunca deja una referencia obsoleta a mitad camino) y `93c7dc3` (PM, que archiva R-33 y abre R-34); ninguna de las ocho reconfirmaciones horarias de Programador intercaladas (ver repetición nueva de `#30` en esta misma pasada) tocó el archivo, y no hizo falta porque no había ninguna prosa que quedara desactualizada en esos huecos — el hallazgo solo se manifiesta cuando una R-XX se completa sin archivarse en el mismo commit, y esta vez no fue el caso. **Decimoquinta repetición, esta vez CON desfase real, con R-34 (esta pasada, 2026-10-21):** a diferencia de las dos pasadas anteriores, sí se repite el patrón completo. R-34 quedó `COMPLETADA` en §1 de `SEGUIMIENTO.md` a las 06:21 del 2026-10-20 (`91b4c66`); `ROADMAP_PRODUCTO.md` siguió diciendo «Oleada v22 (R-34) abierta, sin implementar» durante las nueve reconfirmaciones horarias de Programador siguientes (07:08 a 15:09) — verificado con `git log --oneline 91b4c66..12a1be7 -- roadmap/ROADMAP_PRODUCTO.md`, que no devuelve ningún commit salvo el propio `12a1be7` final — hasta que el ciclo de PM de las 19:19 (`12a1be7`) archivó la Oleada v22 y corrigió la prosa en el mismo commit en que abrió R-35. Trece horas de desfase (06:21 a 19:19), exactamente el patrón que describe el hallazgo: nunca lo corrige una reconfirmación de Programador, solo el ciclo de PM que archiva. **Decimosexta repetición, con R-35 (esta pasada, 2026-10-22):** mismo patrón otra vez. R-35 quedó `COMPLETADA` a las 06:21 del 2026-10-21 (`a7736a5`); `ROADMAP_PRODUCTO.md` siguió diciendo «Oleada v23 (R-35) abierta, sin implementar» durante las nueve reconfirmaciones horarias de Programador siguientes (P-07 a las 07:13 más ocho reconfirmaciones, 08:10 a 15:10) — verificado con `git log --oneline a7736a5..18f0ee2 -- roadmap/ROADMAP_PRODUCTO.md`, que no devuelve ningún commit salvo el propio `18f0ee2` final del ciclo de PM — hasta que ese ciclo (19:15) archivó la Oleada v23 y corrigió la prosa en el mismo commit en que abrió R-36. Casi trece horas de desfase (06:21 a 19:15), tercera vez consecutiva que se repite con desfase real tras dos pasadas sin él. Sigue `ABIERTO` solo a la espera de la respuesta del dueño a `#11`: verificado con `list_triggers` en esta misma pasada que el prompt de la rutina "Product manager" no ha cambiado desde su creación (2026-08-31), así que no hay ninguna autorización nueva que aplicar. **Decimoséptima repetición, con R-36 (esta pasada, 2026-10-23):** mismo patrón otra vez, verificado leyendo `ROADMAP_PRODUCTO.md` en el commit `8d96052` (reconfirmación de mediodía): seguía diciendo «Oleada v24 (R-36) abierta, sin implementar» aunque R-36 ya estaba `COMPLETADA` desde las 06:24 (`5b8492e`); `git log --oneline 5b8492e..e6b1e9b -- roadmap/ROADMAP_PRODUCTO.md` solo devuelve el propio commit final del ciclo de PM (`e6b1e9b`, 19:18), que archiva la Oleada v24 y corrige la prosa en el mismo commit en que abre R-37 — las nueve reconfirmaciones horarias intermedias no la tocan. Casi trece horas de desfase (06:24 a 19:18), cuarta vez consecutiva con desfase real. Sigue `ABIERTO` solo a la espera de la respuesta del dueño a `#11`: verificado de nuevo con `list_triggers` en esta pasada que el prompt de "product-manager-teleprompter" sigue sin cambios desde su creación (2026-08-31). **Decimoctava repetición, con R-37 (esta pasada, 2026-10-24):** mismo patrón otra vez, verificado con `git log --format="%h %ad %s" --date=format:'%H:%M' 9004c0c..c4b4b90 -- roadmap/ROADMAP_PRODUCTO.md`, que solo devuelve el commit final del ciclo de PM (`c4b4b90`, 19:18) — ninguna de las nueve reconfirmaciones horarias intermedias (07:11 a 15:10) toca el archivo, pese a que R-37 ya estaba `COMPLETADA` desde las 06:15. Casi trece horas de desfase (06:15 a 19:18), quinta vez consecutiva con desfase real. Sigue `ABIERTO` solo a la espera de la respuesta del dueño a `#11`: verificado de nuevo con `list_triggers` que el prompt de "product-manager-teleprompter" sigue sin cambios desde su creación (2026-08-31). **Sin ocasión de repetirse en esta pasada (2026-10-25, domingo):** el cron de "programador-teleprompter" (`0 6-15 * * 1-5`) no dispara en fin de semana y el ciclo de PM del 2026-10-24 (`48d206a`, 19:13) fue una reconfirmación de cola sin archivar oleada (R-38 sigue `PENDIENTE`, verificado con `git log --oneline c4b4b90..HEAD -- scripts/ tests/ assets/ fixtures/`, vacío) — sin ninguna R-XX completada ni ninguna reconfirmación horaria de por medio, no hay prosa de `ROADMAP_PRODUCTO.md` que pueda quedar desactualizada en este intervalo; `ROADMAP_PRODUCTO.md` sigue describiendo el estado real sin desfase. Sigue `ABIERTO` únicamente a la espera de la respuesta del dueño a `#11`, ahora 39 días (desde 2026-09-16) sin respuesta. **Sin ocasión de repetirse tampoco en esta pasada (2026-10-26) [según la auditoría de esa fecha, antes del disparo diario]:** a la hora de esta auditoría (03:03 UTC) el cron de «programador-teleprompter» (`0 6-15 * * 1-5`) todavía no había disparado hoy (`next_run_at` 06:04 UTC, confirmado con `list_triggers`), y `git log --oneline 59ad5bf..HEAD -- roadmap/ROADMAP_PRODUCTO.md` no trae ningún commit — sin ninguna reconfirmación horaria ni ninguna R-XX completada en el intervalo, no hay prosa que pueda quedar desactualizada. Sigue `ABIERTO` únicamente a la espera de la respuesta del dueño a `#11`, ahora 40 días (desde 2026-09-16) sin respuesta. **Decimonovena repetición, con R-38 (esta pasada, 2026-10-27):** R-38 quedó `COMPLETADA` a las 06:23 del 2026-10-26 (`fcb783b`); `ROADMAP_PRODUCTO.md` siguió describiendo la Oleada v26 (R-38) como «abierta, sin implementar» durante las ocho reconfirmaciones horarias de Programador y el ciclo de P-08 que siguieron (07:15 a 15:17), hasta que el ciclo de PM de esa misma tarde la archivó y abrió R-39 (`6b9ba62`, 19:18) — verificado con `git log --oneline fcb783b..6b9ba62 -- roadmap/ROADMAP_PRODUCTO.md`, que solo devuelve ese commit final. Casi trece horas de desfase (06:23 a 19:18), mismo patrón exacto que las dieciocho repeticiones anteriores, autocorregido el mismo día sin pasar a la jornada siguiente. Sigue `ABIERTO` únicamente a la espera de la respuesta del dueño a `#11`: verificado de nuevo con `list_triggers` que el prompt de "product-manager-teleprompter" sigue sin cambios desde su creación (2026-08-31), ahora 41 días (desde 2026-09-16) sin respuesta. | `roadmap/ROADMAP_PRODUCTO.md` · enrutado a `SEGUIMIENTO.md` §6 #11 el 2026-09-16 · decimocuarta repetición (R-31) reconfirmada el 2026-10-17 · sin desfase activo en 2026-10-19 y 2026-10-20 · decimoquinta repetición CON desfase (R-34, trece horas) el 2026-10-21 · decimosexta repetición CON desfase (R-35, casi trece horas) el 2026-10-22 · decimoséptima repetición CON desfase (R-36, casi trece horas) el 2026-10-23 · decimoctava repetición CON desfase (R-37, casi trece horas) reconfirmada el 2026-10-24 · sin ocasión de repetirse el 2026-10-25 (domingo, sin ciclo de Programador; PM sin archivar oleada) · decimonovena repetición CON desfase (R-38, casi trece horas) el 2026-10-26, detectada en la auditoría del 2026-10-27, 41 días de espera de `#11`, historial completo en `git log -p -- auditoriacontinua.md` |
| #28 | 2026-10-07 | Infraestructura / entorno de verificación (instalación, no invocación) | baja | **RESUELTO** | Variante de `#22`/R-15 no cubierta por su cierre: desde la sesión de implementación de R-23 (2026-10-05/06) y en las diez sesiones siguientes sin excepción (nueve reconfirmaciones del Programador más esta propia auditoría), el `pip` pelado de este contenedor (`/usr/bin/pip`) resuelve `pip install -r requirements-dev.txt` contra **Python 3.13**, no contra el **3.11.17/3.11.15** real que usa `scripts/ci.py` vía `sys.executable` — reproducido de forma independiente en esta misma pasada: tras el `pip install` liso del preámbulo, `python3 scripts/ci.py` daba **las tres redes de tipos/estilo/tests en ROJO** con `No module named mypy`/`ruff`/`pytest` (fallo total, no solo una señal distinta como en `#22`), hasta reinstalar con `python3 -m pip install -r requirements-dev.txt`, tras lo cual las cuatro redes dieron `OK`. La auditoría del 2026-10-06 ya detectó exactamente este síntoma y decidió, de forma razonable en ese momento, no abrir hallazgo nuevo y solo "dejar constancia" en su narrativa por tratarse de un posible detalle puntual de esa sesión — pero se ha repetido de forma idéntica en las diez sesiones siguientes sin ninguna excepción, y la nota de R-15 en `DEVELOPERS.md`/`SKILL.md` sigue cubriendo solo el binario pelado en la **invocación** (`ruff`/`mypy`/`pytest` sin `python -m`), nunca la **instalación** (`pip install` sin `python3 -m pip install`), así que cada sesión sigue perdiendo el mismo minuto redescubriendo y aplicando el mismo rodeo sin que quede nunca documentado. Cero riesgo de producto (ninguna sesión ha llegado a dar una verificación en verde por error) y cero coste más allá de la repetición — mismo perfil que `#24`. **Cerrado por P-06** (2026-10-07, commit `0a8e90e`), verificado de forma independiente en esta pasada (2026-10-08) con `grep -n pelado DEVELOPERS.md SKILL.md`: el bloque de cita de ambos archivos que ya cubría el binario pelado de `ruff`/`mypy`/`pytest` (R-15/`#22`) gana ahora el párrafo gemelo para la instalación, citando `python3 -m pip install -r requirements-dev.txt` como forma correcta y `origen: auditoría #28` explícito. Reproducción propia de esta pasada: `pip install -r requirements-dev.txt` pelado volvió a instalar contra Python 3.13 (síntoma intacto, el contenedor no cambia), pero la documentación ya lo cubre y lo advierte exactamente como pedía el cierre. | `origen: narrativa de auditoría 2026-10-06 ("se deja constancia"), formalizado como hallazgo por la auditoría 2026-10-07 tras diez repeticiones idénticas sin cierre documental · cerrado por P-06 (`0a8e90e`, 2026-10-07) · verificado de forma independiente por esta auditoría (2026-10-08)` |
| #25 | 2026-09-29 | Proceso / precisión de la prosa de estado (roadmap) | baja | **RESUELTO** | El ciclo de PM del 2026-09-28 (`de45611`) actualizó a la vez `SEGUIMIENTO.md` §1 y `ROADMAP_PRODUCTO.md` (cabecera y "Cola de producto") cambiando el recuento de "pasadas de auditoría consecutivas esperando la respuesta del dueño a la pregunta #11" de **doce** (correcto ese mismo día: la auditoría 2026-09-28, que corrió antes que el ciclo de PM, ya lo había escrito bien — `2026-09-17 a 2026-09-28` = 12 días) a **quince**, saltándose `trece`/`catorce`. Verificado con `git log -p -- roadmap/SEGUIMIENTO.md` (pickaxe sobre la frase completa) que la progresión real de la cifra en los commits que la tocan fue `once` (2026-09-27) → `doce` (2026-09-28, commit de la auditoría) → `quince` (2026-09-28, commit del ciclo de PM posterior, mismo día): un salto de +3 en una sola jornada, sin que hayan transcurrido tres pasadas reales. Causa más probable, no confirmable sin preguntar al propio ciclo que lo escribió: confusión con el ordinal, no relacionado, de "pasada de auditoría consecutiva sin cambios de código" (que sí llegó a **decimoquinta** ese mismo día, pero cuenta desde una fecha de arranque distinta — 2026-09-14, tres días antes de que existiera la pregunta #11 — de donde sale el desfase estable de 3 que todas las pasadas anteriores habían mantenido sin romper: once/decimocuarta el 27, doce/decimoquinta el 28). **No afecta a ningún invariante ni a ninguna decisión real**: la respuesta a la pregunta #11 sigue `(pendiente)` con cualquiera de las dos cifras, y `SEGUIMIENTO.md` §1 sigue siendo la fuente autoritativa correcta en todo lo demás — es un error de aritmética en la prosa, no de contenido de decisión ni de estado de tareas. **Cerrado por el propio ciclo de PM del 2026-09-29** (`ac851d3`), reverificado de forma independiente en esta pasada (2026-09-30) leyendo el diff `d14776a..ac851d3`: la cifra pasa a **trece** (`2026-09-17 a 2026-09-29`, el recuento correcto a esa fecha) tanto en `SEGUIMIENTO.md` §1 como en `ROADMAP_PRODUCTO.md` (cabecera y "Cola de producto"), exactamente como pedía esta fila. | `roadmap/SEGUIMIENTO.md` §1 · `roadmap/ROADMAP_PRODUCTO.md` cabecera y "Cola de producto" · detectado por la auditoría 2026-09-29 con `git log -p` sobre la frase y recuento manual de días · cerrado por el ciclo de PM del 2026-09-29 (`ac851d3`) |
| #20 | 2026-09-05 | Infraestructura / proceso (fuera del código) | media | **RESUELTO** | Diagnóstico original: seis rutinas programadas en vez de tres, en dos tríos con cron idéntico o solapado (`Auditor`/`auditor-teleprompter`, `Product manager`/`product-manager-teleprompter`, `Programador`/`programador-teleprompter`), asumido como coste doble de cómputo sobre la cuenta del dueño. **Corregido el 2026-09-10 por el programador** (sexto ciclo, `DECISIONES_TECNICAS.md`): el trío sin sufijo apunta a otro repositorio del dueño (`centro-estudios-sw`/GestorAcademia), no a este proyecto. **Cerrado en esta pasada con verificación independiente propia, no por transcribir la corrección ajena:** llamada directa a `list_triggers` en esta sesión (2026-09-11) leyendo `session_request.config.sources[].git_repository.url` de las seis rutinas — el campo completo, no solo `name`/`cron_expression` como comprobaban las ~15 reconfirmaciones previas a la corrección: `auditor-teleprompter`/`product-manager-teleprompter`/`programador-teleprompter` → `https://github.com/JanoSolerDiaz/telePrompter` (este repositorio); `Auditor`/`Product manager`/`Programador` (sin sufijo) → `https://github.com/JanoSolerDiaz/centro-estudios-sw` (otro proyecto del dueño). Confirmado: ninguna rutina de *este* proyecto está duplicada, una sola por rol, sin solape de cron. | `SEGUIMIENTO.md` §3 bloqueo #8 · verificado de forma independiente por esta auditoría (2026-09-11) leyendo `git_repository.url` de `list_triggers` |
| #14 | 2026-09-03 | Invariantes / revalidación | **alta** | **RESUELTO** | **Reproducido de forma independiente en esta auditoría** (no solo verificado a mano, como constaba en `DECISIONES_TECNICAS.md` al cerrar P-02): el límite que P-02 dejó explícitamente sin cerrar es más grave de lo que su propia nota describe. Escenario: en una revalidación coinciden una edición manual y la aceptación de una partición sobre el mismo bloque de origen (conflicto correctamente pospuesto por P-02/#9); en la revalidación INMEDIATAMENTE POSTERIOR, sin que el dueño toque nada más, el emparejamiento ancla→identidad no solo atribuye mal el contenido: **duplica el bloque siguiente de la misma escena.** Con un guion de prueba de dos bloques en la escena 1 (edición manual + partición aceptada sobre el bloque 0, bloque 1 intacto), la segunda revalidación produce 3 bloques en la escena donde debería haber 2, con el texto del bloque 1 repetido dos veces (una de ellas bajo la identidad equivocada, la mitad `'b'` de la partición del bloque 0) y la partición aceptada por el dueño sin materializarse nunca en dos mitades reales. Es contenido duplicado y mal atribuido en `guion-escenas.md`, generado en silencio, sin incidencia que lo señale ni test que lo cubra — exactamente el tipo de fallo que el invariante (c) existe para prevenir. Reproducción paso a paso en la narrativa de esta pasada, más abajo. **Cerrado por P-03** (2026-09-03): `revalidacion.py` ahora persiste entre pasadas qué particiones quedaron pospuestas (`estado.validacion["particiones_pospuestas"]`), así que la pasada siguiente interpreta las anclas del documento con el MISMO esquema de identidad con el que se escribió, en vez de asumir que toda partición aceptada ya está materializada. Efecto: mientras la edición manual siga en el documento, la partición se queda pospuesta sin duplicar ni mal atribuir nada; solo se materializa cuando el dueño deja de tocar el bloque. Dos tests de regresión nuevos en `tests/test_revalidacion.py` reproducen exactamente el escenario de este hallazgo (falla sin el fix) y confirman que la materialización posterior sigue funcionando cuando el conflicto se resuelve. | `revalidacion.py` · invariante (c) · límite conocido de P-02 |
| #21 | 2026-09-09 | Infraestructura / trazabilidad (git) | **alta** | **RESUELTO** | Diagnóstico original (2026-09-09): el historial de `origin/develop` parecía reescrito, colapsando T-00→P-05 en un commit raíz distinto en cada pasada, con commits "citados como vigentes" que `git merge-base --is-ancestor` daba por no-antepasados. **Era un falso positivo del clon superficial (`git clone --depth`) de cada contenedor efímero, no una reescritura real.** El programador ya lo investigó y corrigió el mismo día (`DECISIONES_TECNICAS.md`, primer ciclo 2026-09-09) con `git fetch --unshallow`; **esta auditoría lo reproduce de forma independiente en esta pasada (2026-09-10), no se limita a leer la corrección:** este clon también llegó superficial (`git rev-parse --is-shallow-repository` → `true`); `git fetch --unshallow origin` (operación de solo lectura) trajo el historial completo — **114 commits**, raíz real `f78a92c` ("initial commit") → `e8b9663` (T-00) → …; `git merge-base --is-ancestor 1a40c84 develop` **y** `... 576f6d9 develop` devuelven ambos **"IS ancestor"** tras el `unshallow`, confirmando que ninguno de los dos commits que auditorías previas creyeron "perdidos" lo estaba de verdad. Se corrige aquí a `RESUELTO` (no solo en `DECISIONES_TECNICAS.md`, que el auditor no puede dar por bueno sin repetir la comprobación): el contenido y la trazabilidad commit-a-commit del proyecto están intactos; la causa raíz observable (clon superficial con frontera variable) no es una acción de código y no requiere P-XX. | `origen: corrección del programador 2026-09-09` · reproducido de forma independiente por esta auditoría (2026-09-10) con `git fetch --unshallow` + `git merge-base --is-ancestor` |
| #22 | 2026-09-12 | Infraestructura / entorno de verificación | media | **RESUELTO** | Este contenedor trae, además del `mypy`/`ruff`/`pytest` que instala `pip install -r requirements-dev.txt` (versiones exactas pineadas: `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`, resueltos en `/usr/local/lib/python3.11/dist-packages`, el mismo Python que usa el proyecto), un **segundo juego de los mismos tres binarios preinstalado en `/root/.local/bin`** (`mypy 1.19.1`, `ruff 0.15.8`, `pytest 9.0.2`), con `/root/.local/bin` por delante en el `PATH`. Las cuatro verificaciones del protocolo son inmunes porque `scripts/ci.py` invoca siempre `sys.executable -m <herramienta>` (nunca el nombre pelado) y el hook de pre-commit llama a `python scripts/ci.py` — confirmado leyendo el código, no solo probando. El riesgo es para un humano o una sesión que teclee el comando pelado (`ruff check .`, `mypy scripts tests`, `pytest`) directamente en la terminal, tal como queda escrito literalmente en varias entradas de `HISTORIAL_SESIONES.md`: verificado en esta pasada que el binario pelado da una señal **distinta y engañosa** de la que da la versión pineada — `ruff check .` pelado marca `UP042` en `scripts/salidas.py:48` (`class TipoSalida(str, Enum)`, sugiere heredar de `enum.StrEnum`) que `python -m ruff check .`/`scripts/ci.py` NO marca; `mypy scripts tests` pelado no es solo más estricto, está **roto de verdad para este proyecto**: al vivir en un entorno de Python aislado que no ve `dist-packages`, no encuentra el paquete `pytest` y devuelve **34 errores falsos en 22 archivos** (`import-not-found` de `pytest`, más los `Untyped decorator` en cascada que provoca cada decorador de pytest sin tipos resueltos) donde `python -m mypy scripts/ tests/` (el que de verdad ejecuta el hook) da limpio. Es exactamente el tipo de señal que podría hacer perder tiempo a una sesión futura investigando "34 errores de tipos" que no existen en la verificación real del proyecto. No es un hallazgo de código: ninguna verificación real del protocolo lo sufre, y el origen (qué preinstala este contenedor de nube y en qué orden de `PATH`) no es una decisión de este repositorio. Se registra para que una futura pasada no lo redescubra desde cero y para valorar si conviene una nota explícita en `DEVELOPERS.md`/`SKILL.md` ("verificar siempre con `python scripts/ci.py`, nunca con el binario pelado en un contenedor de nube") que corte de raíz la confusión. **Cerrado por R-15** (2026-09-14, commit `3af47cb`), reverificado de forma independiente en esta pasada (2026-09-15): `grep -in pelado DEVELOPERS.md SKILL.md` localiza la advertencia en ambos sitios exactamente como pedía la ficha — bloque de cita en `DEVELOPERS.md` bajo "Verificación manual" ("Nunca el binario 'pelado' (`ruff`, `mypy`, `pytest` sin `python -m` por delante)") y frase con remisión en `SKILL.md`; tarea puramente documental, sin ninguna línea tocada en `scripts/ci.py` ni en ningún otro módulo (confirmado con `git show --stat 3af47cb`). | Entorno de contenedor de nube · verificado en esta pasada (2026-09-12) comparando `which`/`--version` de `ruff`/`mypy`/`pytest` pelados contra `python3 -m <herramienta> --version` y ejecutando ambos sobre el mismo código → **R-15** · cierre verificado de forma independiente por esta auditoría (2026-09-15) |
| #23 | 2026-09-15 | Proceso auditor / precisión del propio registro | baja | **RESUELTO** | Al reverificar la protección `.bak` del invariante (d) de forma directa (no repitiendo la lista de auditorías anteriores), `grep -rln "copia_seguridad\s*=" scripts/*.py` solo encuentra **cuatro** sitios reales: `documento_revision.py`, `entrada.py`, `feedback.py`, `instalar_skill.py`. Las narrativas del 2026-09-13 y 2026-09-14 (y probablemente alguna anterior) venían repitiendo "cinco puntos... (`convencion.py`, `documento_revision.py`, `entrada.py`, `feedback.py`, `instalar_skill.py`)". `convencion.py` no aplica ni ha aplicado nunca la copia `.bak`: su única función de escritura, `guardar_convencion_guiones`, lo documenta explícitamente en su propio docstring como excepción deliberada y correcta — `convencion-guiones.md` es un documento generado "para pegar en su plantilla", no un archivo del dueño que se vuelva a leer como entrada (a diferencia de `guion-escenas.md`), así que el invariante (d) no le aplica. No es un defecto de código ni una regresión de seguridad: el invariante (d) sigue cubierto al 100 % en los cuatro sitios reales que sí escriben archivos del dueño o de instalación. Es una inexactitud que se coló en el propio relato del auditor y se repitió sin recontar en al menos dos pasadas sucesivas — exactamente el tipo de "hallazgo sobre el propio proceso" que esta auditoría existe para atrapar. **Cerrado en esta misma pasada:** la cifra y la lista quedan corregidas aquí; no requiere ninguna acción de PM ni de programador porque el código nunca estuvo mal — solo la prosa de auditorías anteriores. | Precisión interna de `auditoriacontinua.md` · verificado en esta pasada (2026-09-15) con `grep -rln "copia_seguridad\s*=" scripts/*.py` |
| #26 | 2026-09-30 | Proceso / gobernanza del Product Manager | media | **RESUELTO** | El ciclo de PM del 2026-09-29 (`ac851d3`) había abierto R-19 presentando una frase fija del prompt de la rutina (sin cambios desde 2026-08-31, verificado con `list_triggers`) como "instrucción de este ciclo" — una premisa inexacta, aunque el diseño de R-19 en sí fuera sólido. **Cerrado por el propio PM en el ciclo del 2026-09-30** (`51e38da`, `DECISIONES_TECNICAS.md` líneas "PM (respuesta al hallazgo `#26`)" y "PM (criterio de apertura de R-XX, aclaración)"): no revierte R-19 (correcto: el auditor ya había certificado que el diseño no viola ningún invariante), corrige la premisa en `ROADMAP_PRODUCTO.md`/`ROADMAP_HISTORICO.md` apoyando R-19 en la grieta de arquitectura verificada el 2026-09-21 (la fuente legítima real), y deja escrita una norma explícita para el futuro: el encargo estable de la rutina de PM nunca cuenta como una "cuarta fuente" nueva, solo las tres ya establecidas (auditoría / `FEEDBACK.md` / grieta de arquitectura verificada). **Verificado de forma independiente en esta pasada (2026-10-01)** leyendo el texto completo de ambas entradas y la cabecera vigente de `ROADMAP_PRODUCTO.md`: la corrección es honesta y completa, exactamente lo que pedía la fila — no una mención de pasada. | `roadmap/DECISIONES_TECNICAS.md` (entradas 2026-09-30) · `roadmap/ROADMAP_PRODUCTO.md` (cabecera) · cerrado por el PM (`51e38da`), verificado de forma independiente por esta auditoría (2026-10-01) |
| #27 | 2026-10-01 | Robustez / validación de salida (R-19, concat-ffmpeg) | media | **RESUELTO** | `scripts/concat_ffmpeg.py` exponía un validador propio del formato del demuxer `concat` de ffmpeg que la ruta real de generación nunca invocaba, y `archivo_video` no se recortaba ni rechazaba saltos de línea en sus dos puntos de entrada — detalle completo de los dos huecos reproducidos en la entrada original de este registro (recuperable con `git log -p -- auditoriacontinua.md`). **Cerrado por R-21** (commit `1e8d514`, 2026-10-02), verificado en esta pasada leyendo el diff completo, no solo la ficha de `SEGUIMIENTO.md`: `scripts/salidas.py::_generar_concat_ffmpeg` llama ahora a `validar_lista_concat_ffmpeg` sobre el contenido antes de `guardar_lista_concat_ffmpeg`, degradando a `SalidaOmitida` con el motivo exacto si falla (cubierto por `test_concat_ffmpeg_con_contenido_invalido_degrada_a_omitida_en_vez_de_escribir`, que fuerza el fallo por monkeypatch y confirma que nunca llega a escribirse a disco); `scripts/tomas.py` gana `_sanear_archivo_video` (recorta espacios, normaliza a `""` si queda vacío o trae `\n`/`\r`), aplicada en `_toma_desde_dict`; `assets/reproductor/guion.js` gana la función gemela `sanearArchivoVideo`, aplicada en los dos puntos donde el dueño teclea el valor (verificado leyendo ambos puntos de entrada línea a línea, no solo el nombre de la función). Las dos decisiones de diseño (saneamiento duplicado en los dos lenguajes en vez de confiar en uno solo; valor inválido normalizado a "sin anotar" en vez de error fatal) están razonadas en `DECISIONES_TECNICAS.md` y son coherentes con el resto del proyecto (mismo criterio que R-10 ya aplicó para `\r\n` en `entrada.py`). 6 tests nuevos (613→619), los cuatro redes en verde. | `scripts/concat_ffmpeg.py` · `scripts/salidas.py` · `scripts/tomas.py` · `assets/reproductor/guion.js` · cerrado por **R-21** (commit `1e8d514`, 2026-10-02), verificado de forma independiente por esta auditoría (2026-10-03) leyendo el diff completo |
| #29 | 2026-10-08 | Proceso / gobernanza del Product Manager (§1 de SEGUIMIENTO.md como fuente autoritativa) | baja | **RESUELTO** | El ciclo de PM que archivó la Oleada v12 y abrió R-25 (commit `2628739`, 2026-10-07) rompió, por primera vez desde que existe el patrón, la práctica hasta ahora constante de añadir una fila `PENDIENTE` a §1 de `SEGUIMIENTO.md` en el mismo commit que abre cada R-XX nueva — verificado comparando los diffs de apertura de R-23/R-24 (que sí añadían su fila) contra el de R-25, que no lo hacía. Riesgo mitigado en la práctica desde el principio (cabecera de `SEGUIMIENTO.md` e `HISTORIAL_SESIONES.md` sí narraban la apertura), pero la fila formal de §1 faltaba. Recomendación de cierre de esta misma fila (pasada 2026-10-08): añadir `R-25 | ... | PENDIENTE | ...` a §1 en el próximo ciclo que lo tocara. **Cerrado por el propio ciclo de PM del 2026-10-08** (commit `7e803f2`, el mismo que archivó R-25 y abrió R-26): verificado en esta pasada (2026-10-09) con `grep -n "^| R-2[4-6]" roadmap/SEGUIMIENTO.md` sobre el `HEAD` actual (`7e803f2`) — §1 trae ahora `R-25 | ... | COMPLETADA | 2026-10-08 | ...` **y** `R-26 | ... | PENDIENTE | 2026-10-08 | ...`, ambas con fila propia, sin ningún hueco. El propio commit de apertura de R-26 ya reconocía y cerraba la causa raíz en su prosa ("§1 tenía a R-25 como COMPLETADA desde el mismo commit... sin el patrón de latencia que motivó #24 esta vez"). No vuelve a repetirse: dos aperturas de R-XX seguidas (R-25 then R-26) con exactamente un ciclo de retraso en la primera y ninguno en la segunda. | `roadmap/SEGUIMIENTO.md` §1 · cerrado por el ciclo de PM del 2026-10-08 (`7e803f2`) · verificado de forma independiente por esta auditoría (2026-10-09) |
| #31 | 2026-10-15 | Proceso / trazabilidad de decisiones (`DECISIONES_TECNICAS.md`) | baja | **RESUELTO** | Primera ruptura de un patrón constante desde R-21: las nueve aperturas de R-XX anteriores (R-21 a R-29) tenían cada una su fila `PM (apertura de R-XX)` en `DECISIONES_TECNICAS.md`; la apertura de R-30 (commit `87fc45e`, 2026-10-14) no la tenía, y la narrativa de esa sesión justificaba la omisión con una premisa de "convención" verificablemente falsa (detalle completo en `git log -p -- auditoriacontinua.md`). **Cerrado por el propio ciclo de PM del 2026-10-15** (commit `96ea17a`, el mismo que archiva la Oleada v18 y abre R-31), verificado en esta pasada (2026-10-16) leyendo el diff completo: añade dos filas nuevas a `DECISIONES_TECNICAS.md` — `PM (corrección del hallazgo #31: fila de apertura de R-30 faltante)`, que documenta con fecha real de la corrección la decisión de apertura de R-30 que debió registrarse el 2026-10-14, citando explícitamente por qué se añade ahora y no se deja ausente (evitar que una futura sesión cite la omisión como precedente válido); y `PM (apertura de R-31)`, que **no repite** la premisa de "convención" — exactamente la condición de cierre que pedía esta fila. Cierre completo, no una mención de pasada. | `roadmap/DECISIONES_TECNICAS.md` · cerrado por el ciclo de PM del 2026-10-15 (`96ea17a`) · verificado de forma independiente por esta auditoría (2026-10-16) |
| #30 | 2026-10-10 | Proceso / coste de cómputo (cadencia de la rutina Programador) | media | ABIERTO | La rutina programada "Programador" dispara con cron horario durante toda la jornada. Cuando la R-XX del día se implementa temprano, las **nueve** reconfirmaciones horarias siguientes no tienen ninguna tarea que ejecutar (§1 de `SEGUIMIENTO.md` vacío hasta el siguiente ciclo de PM) y aun así cada una repite el protocolo completo de entrada: `git pull`, `pip install`, y las cuatro redes enteras, solo para commitear "sin novedad de código". No es un síntoma oculto: el propio ciclo de Programador lo señaló antes de que esta auditoría lo registrara. Riesgo de producto: ninguno (verificación siempre en verde). Coste real: cada reconfirmación ociosa paga el precio íntegro de una sesión de nube completa por un commit que no cambia una sola línea de `scripts/`, `tests/` ni `assets/`. **Enrutado por el PM el 2026-10-10** (commit `845e2d9`) como pregunta de gobernanza `#12` de `SEGUIMIENTO.md` §6, **pendiente**, con dos remedios propuestos (espaciar el cron, o añadir una comprobación barata de "cola vacía") que ninguno de los dos aplicable sin autorización del dueño. **Materializado de forma idéntica en cada oleada desde R-27** (R-27 a R-30, detalle día a día recuperable con `git log -p -- auditoriacontinua.md`) **y de nuevo con R-31** (R-31 completada a las 06:25 del 2026-10-16, `3cb5075`; nueve reconfirmaciones horarias siguientes, `07:16` a `15:17`, `0d01fcc`…`7fcbaab`, sin cambio de código). **Sin nueva repetición que registrar en esta pasada (2026-10-18):** desde la apertura de R-32 (`08a59de`, 2026-10-16 19:21) no ha corrido ningún ciclo de Programador todavía, solo auditoría y PM, así que el patrón no tiene ocasión de repetirse hasta que lo haga. El hallazgo sigue `ABIERTO` porque ninguno de los dos remedios se ha aplicado todavía y la pregunta `#12` sigue `(pendiente)`. **Sin nueva repetición que registrar tampoco en esta pasada (2026-10-19):** `git log` desde la apertura de R-32 (`08a59de`, 2026-10-16) solo trae el ciclo de auditoría anterior (`7430595`) y el de PM (`4cc381b`) — sigue sin correr ningún ciclo de "Programador", así que la circunstancia que dispara el patrón (reconfirmaciones horarias ociosas) no se ha vuelto a dar. **Repetido de nuevo, dos veces en el mismo día, con R-32 y R-33 (esta pasada, 2026-10-20):** verificado con `git log --oneline b4c597e..HEAD`, que trae **ocho** commits de "Ciclo de Programador" sin ningún cambio de código, confirmado con `git show --stat` uno a uno — primera tanda, tres reconfirmaciones (`8199be5` 07:12, `1279660` 08:10, `5309a73` 09:08) entre que R-32 se completó (`aa3e86c`, 06:19) y R-33 se implementó (`ef8727c`, 10:27), con §1 vacío de tareas `PENDIENTE` porque R-33 estaba especificada pero aún sin abrir formalmente; segunda tanda, cinco reconfirmaciones más (`11c1497` 11:09, `51053c9` 12:11, `f74df19` 13:16, `dabdf26` 14:09, `b99c4df` 15:13) entre que R-33 se completó (misma sesión de `ef8727c`) y el ciclo de PM archivó la oleada y abrió R-34 (`93c7dc3`, 19:18). Mismo patrón exacto que las repeticiones anteriores: cada una paga el protocolo completo (clon/`pull`, reinstalación de dependencias, las cuatro redes enteras) para terminar en "sin novedad de código". Sigue `ABIERTO`: ninguno de los dos remedios propuestos en la pregunta `#12` se ha aplicado y la pregunta sigue `(pendiente)` de respuesta del dueño. **Repetido de nuevo con R-34 (esta pasada, 2026-10-21):** verificado con `git log --format="%h %ad %s" --date=format:'%H:%M' 91b4c66..12a1be7`, que trae **nueve** commits de "Ciclo de Programador" (`4402ff7` 07:08, `ae66718` 08:08, `eba10bf` 09:09, `70d3791` 10:09, `b8087cf` 11:08, `3881014` 12:10, `2214e0b` 13:11, `e98084d` 14:13, `e72ae37` 15:09) entre que R-34 se completó (`91b4c66`, 06:21) y el ciclo de PM archivó la oleada y abrió R-35 (`12a1be7`, 19:19), confirmado con `git show --stat` uno a uno que ninguno toca `scripts/`, `tests/`, `assets/` ni `fixtures/` — solo `roadmap/`. Mismo patrón exacto: cada una paga el protocolo completo (clon/`pull`, reinstalación de dependencias, las cuatro redes enteras) para terminar en "sin novedad de código". Sigue `ABIERTO`: pregunta `#12` sigue `(pendiente)` de respuesta del dueño. **Repetido de nuevo tras R-35 (esta pasada, 2026-10-22):** verificado con `git log --format="%h %ad %s" --date=format:'%H:%M' a7736a5..18f0ee2`, que trae **ocho** commits de "Ciclo de Programador... sin novedad de código" (`286d0ed` 08:10, `ed53c99` 09:09, `a145894` 10:09, `6181364` 11:12, `e6708c1` 12:13, `48f42c4` 13:12, `2234a53` 14:11, `8cf594c` 15:10), todos posteriores a que P-07 (`2c24017`, 07:13) cerrara el hallazgo `#33` esa misma mañana — ninguno de los ocho toca `scripts/`, `tests/`, `assets/` ni `fixtures/`, confirmado con `git show --stat` uno a uno. Sigue `ABIERTO`: verificado con `list_triggers` en esta pasada que la rutina "programador-teleprompter" conserva el mismo cron horario (`0 6-15 * * 1-5`) desde su creación (2026-08-31/2026-09-02) — ninguno de los dos remedios de la pregunta `#12` se ha aplicado todavía. **Repetido de nuevo tras R-36 (esta pasada, 2026-10-23):** verificado con `git log --oneline 5b8492e..e6b1e9b`, que trae **nueve** commits de "Ciclo de Programador... sin novedad de código" (`ec04a8f` 07:14, `d20b81c` 08:08, `914afe7` 09:09, `4c69282` 10:10, `407a6ef` 11:13, `8d96052` 12:09, `2cb7309` 13:15, `63b0413` 14:15, `abe8a3b` 15:13), confirmado con `git show --stat` uno a uno que ninguno toca `scripts/`, `tests/`, `assets/` ni `fixtures/` — solo `roadmap/`. Mismo patrón exacto: cada una paga el protocolo completo (clon/`pull`, reinstalación de dependencias, las cuatro redes enteras) para terminar en "sin novedad de código". Sigue `ABIERTO`: verificado de nuevo con `list_triggers` en esta pasada que el cron de "programador-teleprompter" no ha cambiado; pregunta `#12` sigue `(pendiente)` de respuesta del dueño. **Repetido de nuevo tras R-37 (esta pasada, 2026-10-24):** verificado con `git log --format="%h %ad %s" --date=format:'%H:%M' 9004c0c..c4b4b90`, que trae **nueve** commits de "Ciclo de Programador... sin novedad de código" (`ce8bcc9` 07:11, `df4d693` 08:09, `d4a3aae` 09:09, `97d7ab4` 10:09, `453681b` 11:11, `a26d0fc` 12:15, `5da46a6` 13:09, `f964d76` 14:09, `8d4b31e` 15:10), confirmado con `git show --stat` uno a uno que ninguno toca `scripts/`, `tests/`, `assets/` ni `fixtures/` — solo `roadmap/`. Mismo patrón exacto: cada una paga el protocolo completo (clon/`pull`, reinstalación de dependencias, las cuatro redes enteras) para terminar en "sin novedad de código". Sigue `ABIERTO`: verificado de nuevo con `list_triggers` en esta pasada que el cron de "programador-teleprompter" (`0 6-15 * * 1-5`) no ha cambiado desde su creación (2026-09-02); pregunta `#12` sigue `(pendiente)` de respuesta del dueño. **Sin repetición nueva que registrar en esta pasada (2026-10-25, domingo):** el cron de "programador-teleprompter" (`0 6-15 * * 1-5`) no dispara en fin de semana (confirmado con `list_triggers`: `last_fired_at` 2026-10-23T15:07, `next_run_at` 2026-10-26T06:04) — sin ninguna reconfirmación horaria en este intervalo, el coste que describe este hallazgo no se ha vuelto a pagar. Sigue `ABIERTO`: ninguno de los dos remedios de la pregunta `#12` se ha aplicado y sigue `(pendiente)`, ahora 15 días (desde 2026-10-10) sin respuesta. **Sin repetición nueva que registrar tampoco en esta pasada (2026-10-26) [según la auditoría de esa fecha, antes del disparo diario]:** a la hora de esta auditoría (03:03 UTC) el cron de "programador-teleprompter" todavía no había disparado hoy (`next_run_at` 06:04 UTC, confirmado con `list_triggers`) — sin ninguna reconfirmación horaria en el intervalo, el coste que describe este hallazgo no se ha vuelto a pagar. Sigue `ABIERTO`, ahora 16 días (desde 2026-10-10) sin respuesta. **Repetido de nuevo tras R-38/P-08 (esta pasada, 2026-10-27):** verificado con `git log --format="%h %ad %s" --date=format:'%H:%M' fcb783b..6b9ba62`, que trae **ocho** commits de "Ciclo de Programador... sin novedad de código" (`52df16a` 07:15, `e547462` 08:09, `690ad25` 09:09, `54acb79` 10:10, `bd5747a` 12:14, `3bfbea0` 13:11, `d0069b6` 14:19, `1bd0150` 15:17) intercalados con un noveno ciclo que sí produjo código real (`ae030e5` 11:13, P-08, cierre del hallazgo `#34`) — confirmado con `git show --stat` uno a uno que los ocho "sin novedad" no tocan `scripts/`, `tests/`, `assets/` ni `fixtures/`, solo `roadmap/`. Mismo patrón exacto: cada reconfirmación ociosa paga el protocolo completo (clon/`pull`, reinstalación de dependencias, las cuatro redes enteras) para terminar sin cambiar una línea de código. Sigue `ABIERTO`: verificado de nuevo con `list_triggers` en esta pasada que el cron de "programador-teleprompter" (`0 6-15 * * 1-5`) no ha cambiado desde su creación (2026-09-02); pregunta `#12` sigue `(pendiente)`, ahora 17 días (desde 2026-10-10) sin respuesta. | `roadmap/SEGUIMIENTO.md` (notas de reconfirmación del Programador) · enrutado como pregunta `#12` de `SEGUIMIENTO.md` §6 por el PM el 2026-10-10 (commit `845e2d9`) · repetido dos veces el 2026-10-20 (R-32/R-33), de nuevo con R-34 el 2026-10-21, con R-35 el 2026-10-22, con R-36 el 2026-10-23, con R-37 el 2026-10-24 y con R-38/P-08 el 2026-10-26 (detectado en la auditoría del 2026-10-27) · sin ocasión de repetirse el 2026-10-25 (domingo, cron sin disparos), 17 días de espera de `#12` |
| #32 | 2026-10-18 | Proceso / gobernanza del Product Manager (§0.4 cierre de sesión) | baja | **RESUELTO** | El ciclo de PM del 2026-10-17 19:11 (commit `1b8fae3`) tocó `DECISIONES_TECNICAS.md`, `ROADMAP_PRODUCTO.md` e `HISTORIAL_SESIONES.md`, pero no `roadmap/SEGUIMIENTO.md` — confirmado con `git show --stat 1b8fae3`, que no lista el archivo. Incumple la regla de cierre de sesión §0.4.1 de `HOJA_DE_RUTA.md` ("Actualiza el estado de la tarea en §1 de SEGUIMIENTO... y «última actualización» de la cabecera"), aplicable a toda sesión que termina. Efecto observable: la cabecera de `SEGUIMIENTO.md` sigue fechada "2026-10-16" y `grep -n "2026-10-17" roadmap/SEGUIMIENTO.md` no encuentra ninguna coincidencia, pese a que el propio documento se autodescribe como el único "hub" que el dueño revisa ("El dueño no revisa el código: revisa este documento"). No se pierde información (recuperable en `HISTORIAL_SESIONES.md`/`git log`) ni se infringe ningún invariante de producto; es un hallazgo de proceso puro, mismo perfil que `#29`/`#31`, normalmente autocorregido por el propio PM en su ciclo siguiente. **Cerrado por el propio ciclo de PM del 2026-10-18** (commit `4cc381b`), verificado de forma independiente por esta auditoría (2026-10-19) leyendo el diff completo: `SEGUIMIENTO.md` gana "Última actualización: 2026-10-18" en cabecera y el bloque completo "Ciclo de Product Manager (2026-10-18)" documentando la corrección con fecha real, exactamente el patrón de cierre ya usado en `#29`/`#31` — no una mención de pasada. | `roadmap/SEGUIMIENTO.md` §0.4.1 · commit `1b8fae3` (2026-10-17) · detectado de forma independiente por la auditoría del 2026-10-18 · cerrado por el ciclo de PM del 2026-10-18 (`4cc381b`), verificado de forma independiente por esta auditoría (2026-10-19) |
| #33 | 2026-10-21 | Documentación / coherencia (SKILL.md vs. funcionalidad real) | baja | **RESUELTO** | R-34 (`91b4c66`, 2026-10-20) añade la columna «Instante» a `FEEDBACK.md` y sube el contrato de tropiezos a la versión 2, pero la sección `## Marcar tropiezos durante la toma (R-03)` de `SKILL.md` no se tocó: su tabla de columnas seguía mostrando solo 5 columnas, sin mención a «Instante» ni a R-34. **Cerrado por P-07** (commit `2c24017`, 2026-10-21), verificado de forma independiente en esta pasada (2026-10-22) leyendo el archivo: `SKILL.md` gana el párrafo "Desde R-34, cada tropiezo marcado durante la grabación guarda además, de forma opcional, el instante exacto..." inmediatamente tras el párrafo de emparejamiento por texto exacto, y la tabla de columnas pasa a `Fecha/Escena/Bloque/Texto exacto/Instante/Estado` (6 columnas) citando explícitamente "(R-34)" — exactamente el párrafo que pedía esta fila, con el mismo patrón ya usado para `archivo_video` (R-19/R-21) en la sección inmediatamente anterior. | `SKILL.md` líneas 233-246 · R-34 (`91b4c66`, 2026-10-20) · cerrado por **P-07** (`2c24017`, 2026-10-21), verificado de forma independiente por esta auditoría (2026-10-22) |
| #34 | 2026-10-26 | Documentación interna / coherencia de código | baja | **RESUELTO** | Al revisar en profundidad el invariante (c) (ediciones manuales mandan al revalidar) leyendo `scripts/revalidacion.py` completo, el docstring del módulo (línea ~34) sigue citando una función `_edicion_manual_de` que ya no existe con ese nombre: la detección de ediciones manuales vive hoy inline dentro de `revalidar_guion` (confirmado leyendo el módulo entero, no solo el docstring). No es un defecto funcional — el invariante (c) sigue íntegro y se reverificó en esta misma pasada con evidencia línea a línea (detección por diff de anclas en `ediciones_manuales`, materialización `texto_manual if texto_manual is not None else _texto_derivado(...)`, y el caso límite de P-02/P-03 con partición pospuesta sigue tratado correctamente) — es solo un comentario interno desactualizado tras un refactor anterior, con riesgo real de que una futura sesión busque esa función por nombre, no la encuentre y pierda tiempo o, peor, asuma que la lógica descrita ya no existe en absoluto. Severidad baja, cero riesgo de producto; pendiente de que una sesión de código actualice el docstring para describir la lógica real (o de extraer esa lógica a una función con el nombre que el docstring ya cita). **Cerrado por P-08** (commit `ae030e5`, 2026-10-26), verificado de forma independiente en esta pasada (2026-10-27) leyendo el diff completo: el párrafo pasa a describir "el bucle de deteccion de `revalidar_guion` (comparando, ancla a ancla, el texto que de verdad trae `guion-escenas.md` contra el que el sistema habria derivado)" — ya no cita ningún nombre de función inexistente — sin extraer ninguna función nueva ni tocar comportamiento (740 tests en verde, mismo recuento citado por el commit). Cierre exacto del remedio que pedía esta fila. | detectado por esta auditoría (2026-10-26) leyendo `scripts/revalidacion.py` completo durante la reverificación línea a línea del invariante (c) · cerrado por **P-08** (`ae030e5`, 2026-10-26), verificado de forma independiente por esta auditoría (2026-10-27) |

---

## NARRATIVA POR AUDITORÍA

> Cada pasada: fecha, hallazgos y conclusiones. Append, la más reciente arriba. Prestar
> atención especial a la coherencia entre lo decidido (`DECISIONES_TECNICAS.md` y §0.2 de la
> hoja de ruta) y lo realmente implementado, y a las desviaciones (§7 de SEGUIMIENTO).

### Auditoría 2026-10-27 — `#34` cerrado (P-08, verificado); R-38 (único código nuevo desde la auditoría anterior) revisado línea a línea sin hallazgos; cuatro redes en verde, 740/740 tests; `#24`/`#30` repiten su patrón crónico de proceso por decimonovena/novena vez (41/17 días sin respuesta del dueño a `#11`/`#12`); sin desviaciones nuevas en §7 de `SEGUIMIENTO.md`; R-39 (Oleada v27) abierta y coherente con las reglas de producto

Preámbulo de protocolo: `git checkout develop && git pull origin develop` sin incidencias, árbol de trabajo limpio antes y después, ya en `develop` al arrancar. `pip install -r requirements-dev.txt` pelado reprodujo una vez más el síntoma ya cerrado de `#22`/`#28`/P-06 (instala contra un intérprete distinto del real: `pip`/`ruff`/`mypy` pelados resuelven a binarios de `/root/.local/bin` instalados para Python 3.13, no al intérprete 3.11 de `sys.executable`); corregido reinstalando con `python3 -m pip install -r requirements-dev.txt` y verificando después con `python3 -m pytest`/`python3 -m mypy`/`ruff check` (vía `scripts/ci.py`, que sí invoca la versión correcta). Mismo perfil de siempre, no es hallazgo nuevo — confirmado además en esta pasada que `ruff` pelado (`/root/.local/bin/ruff`, v0.16.9) marca el aviso cosmético `UP042` (`TipoSalida(str, Enum)` → sugiere `enum.StrEnum`) que `python3 -m ruff` (v0.14.0, la versión fijada en `requirements-dev.txt`) no marca — artefacto de versión de binario, no una regresión del proyecto.

**Único código nuevo desde la auditoría anterior: R-38, revisado línea a línea, sin hallazgos.** `git log --oneline 572ea01..6b9ba62` trae un commit de tarea (`fcb783b`, R-38: «Puntos a revisar antes de concatenar» en `comandos-montaje.md`), uno de corrección de hallazgo (`ae030e5`, P-08, ver `#34` abajo), ocho reconfirmaciones ociosas del Programador y el cierre de ciclo del PM (`6b9ba62`). De R-38 se leyó el diff completo de `scripts/comandos_montaje.py`, `scripts/feedback.py`, `scripts/salidas.py` y `tests/test_comandos_montaje.py`/`tests/test_salidas.py`, no solo el mensaje de commit:
- **Reutiliza la regla de exclusividad sin reimplementarla.** `_puntos_a_revisar` (nuevo, `comandos_montaje.py`) llama a `tomas.toma_buena` -- la misma función que ya usa `feedback._es_toma_buena` -- para obtener la toma marcada buena de cada escena, y compara `tropiezo.numero_toma` contra ese número; nunca repite la lógica de "como mucho una toma buena por escena" que `toma_buena` ya centraliza. `feedback._formatear_instante` se promueve a pública (`formatear_instante`) para que `comandos_montaje.py` reutilice el mismo formato `mm:ss`, mismo patrón ya usado por R-24 con `volcar_diagnostico`.
- **Backward-compatible de verdad, no solo de palabra.** `registro_tropiezos: RegistroTropiezos | None = None` es el último parámetro, en las cuatro firmas que lo propagan (`calcular_comandos_montaje` → `generar_comandos_montaje` → `salidas._generar_comandos_montaje` → `generar_salidas_seleccionadas`); con el valor por defecto, `_puntos_a_revisar` devuelve `()` de inmediato y `formatear_comandos_montaje` no añade la sección nueva — verificado que el test `test_sin_registro_tropiezos_documento_identico_byte_a_byte_a_antes_de_r38` existe y pasa.
- **El requisito 4 (ignorar tropiezos sin `numero_toma`/`instante_toma_segundos`) está en el código, no solo en el docstring**: el filtro de `_puntos_a_revisar` descarta explícitamente ambos casos `None` antes de comparar, con test dedicado (`test_tropiezo_sin_numero_toma_o_instante_se_ignora_sin_avisar`).
- **Alcance de la escena respetado**: el cruce se hace dentro del bucle `for escena in registro_tropiezos.escenas`, con `toma_buena` resuelta para esa misma escena — un tropiezo de una escena no puede aparecer bajo el número de toma buena de otra.
- **Alcanzable de verdad, no solo testeado**: `SKILL.md` (líneas ~653-658) documenta explícitamente que desde R-38 hay que pasar el registro de tropiezos exportado al generar `comandos-montaje.md` para obtener la sección nueva — no es un parámetro que solo exista para los tests o para `verificar_salidas.py --fixture` (su único llamador real además de los tests), sino una instrucción operativa para la sesión que ejecuta la skill en un rodaje real.
- **Sin número mágico nuevo y sin tocar `config.py`**: no introduce ningún umbral; reutiliza formato y comparación ya existentes.

Conclusión: R-38 es un cierre de hueco limpio, consistente con el patrón ya usado por R-30/R-31/R-37, sin regresión de comportamiento por defecto y con los seis invariantes del encargo intactos (no toca el reproductor, no añade dependencias, no escribe fuera de la carpeta de salida, todo en español, documentado en `SKILL.md`).

**`#34` cerrado, verificado de forma independiente.** `ae030e5` (P-08, 2026-10-26) sustituye en el docstring de `revalidacion.py` la referencia a la inexistente `_edicion_manual_de` por una descripción real ("el bucle de deteccion de `revalidar_guion` ... comparando, ancla a ancla, el texto que de verdad trae `guion-escenas.md` contra el que el sistema habria derivado"), sin extraer ninguna función nueva ni cambiar comportamiento. Exactamente el remedio que pedía la fila; marcado `RESUELTO` en el registro.

**Las cuatro redes, de punta a punta.** `python3 scripts/ci.py` sobre el `HEAD` actual (`6b9ba62`): mypy limpio (72 archivos), `ruff check` (vía `python -m`) sin avisos, **740/740 tests en verde** (coherente con las 8 pruebas nuevas de R-38 citadas en su commit, 732→740), `verificar_salidas.py --fixture` con las 19 etapas en `OK`, incluida la auto-contención de `reproductor.html` y de `guion-impresion.html` verificadas explícitamente. Reproducido también por separado con `python3 -m pytest` (740 passed) y `python3 -m mypy` ("Success: no issues found in 72 source files"). Latencias esperadas sin cambios: `.pptx` real latente por falta de la skill `480-branded-pptx`, `.pdf` real latente por falta de Chrome/Edge headless en esta máquina.

**Invariantes: sin re-revisión exhaustiva línea a línea esta pasada (ya hecha el 2026-10-26 sobre el mismo código), pero con el único cambio real desde entonces (R-38) auditado en detalle arriba** y encontrado conforme a los seis. No hay motivo para sospechar regresión en el resto del código, que no se tocó (`git diff --stat 572ea01..6b9ba62 -- scripts tests` solo trae `comandos_montaje.py`, `feedback.py`, `revalidacion.py`, `salidas.py` y sus tests — exactamente R-38 y P-08, nada más).

**Coherencia roadmap/código y gobernanza (§0.2, DECISIONES_TECNICAS.md, §7 de SEGUIMIENTO.md).** La apertura de R-39 (Oleada v27, `6b9ba62`) decide conscientemente no seguir encadenando solo cierres de huecos internos entre salidas de montaje (patrón de las últimas doce oleadas) y elige en su lugar una mejora directa del reproductor (progreso de grabación visible en el índice) explícitamente orientada a la primera sesión de grabación real — decisión razonada y registrada en `DECISIONES_TECNICAS.md` con las tres alternativas consideradas, coherente con el principio de producto "utilidad real para un formador que graba" y con el reconocimiento explícito, en la propia nota de producto, de que las últimas 38 R-XX nacen todas de auditoría/observación del PM y ninguna de rodaje real (bloqueo `#7` de §3, sin resolver desde 2026-09-03). Es una autocorrección de rumbo sana, no un hallazgo. §7 de `SEGUIMIENTO.md` (desviaciones respecto a la hoja de ruta original) sigue con sus seis entradas históricas, todas cerradas desde 2026-09-02; ningún cambio de esta pasada introduce una desviación nueva. `FEEDBACK.md` sigue sin ninguna entrada `nuevo`.

**`#24`/`#30`, patrón crónico de proceso puro, sin riesgo de producto, pendientes de respuesta del dueño.** Ambos se repitieron de nuevo el 2026-10-26: `#24` (prosa de `ROADMAP_PRODUCTO.md` desactualizada mientras R-38 esperaba su archivo por el PM, ~13h de desfase, decimonovena repetición, 41 días de espera de `#11`) y `#30` (ocho reconfirmaciones horarias del Programador sin ningún cambio de código tras completarse R-38, 17 días de espera de `#12`) — detalle completo con commits citados en sus filas del registro. Ninguno de los dos convertible en tarea sin que el dueño responda; ninguno representa degradación de producto.

**Entorno/infraestructura de verificación — sin hallazgo nuevo.** El desajuste de intérprete al instalar dependencias (`#22`/`#28`, ya `RESUELTO`) se reprodujo de nuevo en este clon efímero, con el mismo remedio ya documentado (`python3 -m pip install` en vez del `pip` pelado); no se trata como repetición de hallazgo porque el propio registro ya documenta que es inherente a cómo arranca cada contenedor nuevo, no algo que el código del proyecto pueda corregir.

### Auditoría 2026-10-26 — un hallazgo nuevo de severidad baja (`#34`, docstring desactualizado en `revalidacion.py`, cero riesgo funcional, invariante (c) reverificado íntegro); sin ningún cambio de código desde la auditoría anterior (un solo commit de PM, reconfirmación de cola sin archivar oleada); R-38 (Oleada v26) sigue correctamente `PENDIENTE`; cuatro redes en verde, 732/732 tests; los seis invariantes reverificados con evidencia línea a línea en el código (no solo repitiendo cierres anteriores) y los seis mantienen su veredicto; `#24`/`#30` sin ocasión de repetirse en este intervalo (el cron de "programador-teleprompter" aún no había disparado hoy a la hora de esta auditoría), ambos siguen `ABIERTO` pendientes de respuesta del dueño, ahora 40 días (`#11`) y 16 días (`#12`) sin respuesta

Preámbulo de protocolo: clon llegó con `HEAD` desconectado de cualquier rama (`detached HEAD`) tras el checkout automático; `git checkout develop && git pull origin develop` lo resolvió con un fast-forward limpio de un solo commit, árbol de trabajo limpio antes y después. `pip install -r requirements-dev.txt` pelado reprodujo una vez más el síntoma ya cerrado de `#22`/`#28`/P-06 (instala mypy/ruff/pytest contra Python 3.13, no contra el intérprete 3.11 real de `sys.executable`); no fue necesario corregirlo con `python3 -m pip install` porque en este contenedor concreto el binario pelado de `pytest`/`ruff`/`mypy` resultó ser justo el que se acababa de instalar (`/root/.local/bin` por delante en `PATH`, mismo perfil que documenta `#22`) — verificado explícitamente con `pytest -q`, `ruff check .` y `mypy scripts` antes de dar nada por bueno, sin asumir que "clon limpio" implique "entorno correcto". Mismo perfil de siempre, no es hallazgo nuevo.

**Sin cambio de código que revisar.** `git log --oneline 59ad5bf..HEAD` trae un único commit nuevo desde la auditoría anterior: `7f8ac8d` (PM, 2026-10-25 19:11), reconfirmación de cola que no abre ninguna R-39 especulativa mientras R-38 siga sin código — mismo criterio ya aplicado en los ciclos "sin apertura" anteriores. `roadmap/SEGUIMIENTO.md` §1 confirma: ninguna fila `PENDIENTE` salvo R-38 (abierta el 2026-10-23, sin tocar desde entonces). Verificado con `list_triggers` que, a la hora de esta auditoría (03:03 UTC), el cron de "programador-teleprompter" (`0 6-15 * * 1-5`, hoy lunes) todavía no había disparado (`next_run_at` 06:04 UTC) — la cola de hoy sigue intacta, sin ninguna reconfirmación horaria que pueda dejar nada desactualizado.

**Las cuatro redes, de punta a punta.** `python3 scripts/ci.py` completo sobre el `HEAD` actual (`7f8ac8d`): mypy limpio, ruff sin avisos, **732/732 tests en verde** (mismo recuento que el cierre de R-37/R-38 sin código nuevo, coherencia esperada), `verificar_salidas.py --fixture` con todas las etapas en `OK`, incluida la auto-contención de `reproductor.html` y de `guion-impresion.html`. Reproducido también por separado con `pytest -q` (732 passed, visibles como líneas de puntos) y `mypy scripts` ("Success: no issues found in 35 source files" — cifra de archivos de `scripts/` en solitario, sin `tests/`, coherente con conteos anteriores que sí incluían `tests/`). `ruff check .` pelado (sin `python -m`) marca el único aviso cosmético ya conocido, `UP042` en `salidas.py` (`TipoSalida(str, Enum)` → sugiere `enum.StrEnum`), que `scripts/ci.py`/`python -m ruff` no marca — mismo artefacto de versión de binario ya documentado en `#22`, no una regresión.

**Invariantes reverificados con evidencia línea a línea en el código, no solo repitiendo cierres de pasadas anteriores.** Esta pasada dedicó una revisión específica, archivo por archivo, a los seis invariantes del encargo:
- **Cobertura total del guión — sostenido.** `clasificador.py` (`_dividir_en_parrafos`, `_agrupar_cita_suelto`) recorre toda la escena sin saltos; cualquier párrafo sin señal reconocida cae en `TIPO_REVISAR` ("sin_senal") en vez de descartarse, y `reconstruir()` se compara contra el texto original en `test_clasificador.py`/`test_parser.py`. `parser.py` conserva `secciones_auxiliares` y `preambulo` en vez de tirar encabezados no reconocidos. Ningún `continue`/excepción silenciosa en la ruta de cobertura.
- **Original recuperable y ediciones manuales respetadas — sostenido.** `Reescritura` conserva siempre `original` y `propuesta`; `revertir_reescrituras` solo cambia `decision`, nunca toca `original`. En `revalidacion.py`, la edición manual se detecta por diff de anclas (`ediciones_manuales`) y gana siempre en la materialización (`texto_manual if texto_manual is not None else _texto_derivado(...)`); el caso límite de P-02/P-03 (partición aceptada en conflicto con una edición manual sobre el mismo bloque) sigue pospuesto en vez de perder o duplicar contenido. Único matiz, no funcional: ver `#34` más abajo.
- **Reproductor HTML autocontenido — sostenido.** `verificar_salidas.py::verificar_autocontencion` sigue activo y no es código muerto: lo invoca `scripts/ci.py` (cuarta red) y lo asertan directamente `tests/test_reproductor.py`. `reproductor.py` no contiene ninguna URL ni referencia a CDN.
- **Runtime solo biblioteca estándar — sostenido.** Barrido de imports (AST) sobre los 35 módulos de `scripts/*.py`: cero import de terceros; los únicos nombres que no son de la biblioteca estándar resuelven a otros módulos locales del propio proyecto (p. ej. `from tomas import ...`). `requirements-dev.txt` no se filtra a ningún script de runtime.
- **Defaults configurables, sin números mágicos — sostenido.** `config.py` sigue siendo la única fuente de constantes de comportamiento, y `test_skill_md.py` lo autoimpone: compara cada campo de `Configuracion` contra las claves citadas en la tabla de SKILL.md y falla ante cualquier divergencia en cualquier dirección — test en verde en esta misma pasada. Revisión puntual de `tiempos.py`/`calibracion.py`/`deteccion.py`: sin umbral numérico suelto fuera de `config.py`.
- **Nada fuera de la carpeta de salida, nada sin `.bak` — sostenido.** Los 17 puntos de escritura de `scripts/*.py` derivan su ruta de `carpeta_salida` con constantes `NOMBRE_ARCHIVO_*` fijas, sin nombre controlado por el usuario. La copia `.bak` sigue acotada, por diseño explícito y documentado en el propio código (`convencion.py`), a los archivos del dueño que se vuelven a leer como entrada (`guion-escenas.md`, carpeta del guion, `FEEDBACK.md`, carpeta de instalación de la skill) — exactamente los cuatro sitios reales de siempre (`documento_revision.py`, `entrada.py`, `feedback.py`, `instalar_skill.py`), nunca las salidas puramente generadas. El propio texto de §0.2 de `HOJA_DE_RUTA.md` ("archivo del dueño") ya acota el invariante a ese alcance, así que no es una laguna: la regla y el código coinciden.

**Hallazgo nuevo: `#34`, docstring desactualizado en `revalidacion.py`.** Al leer el módulo completo para reverificar el invariante (c), el docstring de cabecera (línea ~34) sigue citando una función `_edicion_manual_de` que ya no existe con ese nombre — la lógica que describe vive hoy inline dentro de `revalidar_guion`. No es un defecto de comportamiento: el invariante (c) está íntegro y se acaba de reverificar con evidencia de código, no de narrativa. Es, igual que `#23` en su día, un hallazgo sobre la precisión de la propia documentación interna, no sobre el producto — pero a diferencia de `#23` (que vivía en la prosa de este mismo documento), este vive en un comentario de código real, con riesgo concreto de desorientar a una futura sesión de desarrollo que busque esa función por nombre. Severidad baja, `ABIERTO`, a la espera de que una sesión de código actualice el comentario.

**Coherencia roadmap/código.** `roadmap/SEGUIMIENTO.md` §3 (bloqueos), §4 (incidentes de deploy) y §7 (desviaciones) releídos enteros: sin filas nuevas desde la auditoría anterior. §6 (preguntas abiertas): doce preguntas, diez respondidas; solo `#11`/`#12` siguen `(pendiente)`. Verificado con `list_triggers` que ni el cron ni el prompt de "auditor-teleprompter" (`0 3 * * *`), "product-manager-teleprompter" (`0 19 * * *`) ni "programador-teleprompter" (`0 6-15 * * 1-5`) han cambiado desde su creación — ninguna autorización nueva que aplicar a `#11`/`#12`; las tres rutinas sin sufijo ("Auditor"/"Product manager"/"Programador") siguen apuntando a `centro-estudios-sw`/GestorAcademia, no a este repositorio — `#20` sigue cerrado sin ambigüedad. GitHub (`janosolerdiaz/teleprompter`): 0 issues y 0 PRs abiertos.

**`#24` y `#30`: sin ocasión de repetirse en esta pasada.** Hoy es lunes y el cron de "programador-teleprompter" sí dispara en días laborables, pero a la hora de esta auditoría (03:03 UTC) todavía no lo había hecho (`next_run_at` 06:04 UTC) — sin ninguna reconfirmación horaria todavía, no hay ventana en la que `ROADMAP_PRODUCTO.md` pueda desactualizarse (`#24`) ni ninguna reconfirmación ociosa que contar (`#30`). Ambos siguen `ABIERTO` únicamente a la espera de la respuesta del dueño: la espera lleva ya 40 días (`#11`, desde 2026-09-16) y 16 días (`#12`, desde 2026-10-10) sin que esta auditoría tenga ninguna acción propia que tomar más allá de seguir reconfirmando.

**Conclusión.** Quincuagésima séptima auditoría del proyecto. El proyecto sigue en un estado sano: cero cambio de código en este intervalo, las cuatro redes en verde de punta a punta, y los seis invariantes de producto reverificados esta vez con una pasada deliberadamente más profunda —evidencia de código línea a línea en vez de repetir la conclusión de auditorías previas— sin encontrar ninguna violación ni debilitamiento real. Esa misma profundidad es la que saca a la luz el único hallazgo nuevo de la pasada (`#34`): un detalle interno, de severidad baja y cero riesgo de producto, exactamente el tipo de cosa que una auditoría que solo revalidara cierres anteriores sin releer el código fuente se dejaría pasar indefinidamente. El patrón de gobernanza a vigilar sigue siendo el mismo de siempre (`#24`/`#30`), sin ningún efecto sobre la calidad ni la seguridad del producto entregado, y esta pasada tampoco ha tenido ocasión de manifestarse por no haber corrido aún ningún ciclo de Programador.

---

### Auditoría 2026-10-25 — sin hallazgos nuevos; sin ningún cambio de código desde la auditoría anterior (domingo, el cron de "programador-teleprompter" no dispara en fin de semana; el ciclo de PM del 2026-10-24 fue una reconfirmación de cola sin archivar oleada); R-38 (Oleada v26) sigue correctamente `PENDIENTE`; cuatro redes en verde, 732/732 tests; auto-contención y los seis invariantes reverificados sin desviación; `#24`/`#30` sin ocasión de repetirse en este intervalo (sin ciclo de Programador que pueda dejar `ROADMAP_PRODUCTO.md` desactualizado), ambos siguen `ABIERTO` pendientes de respuesta del dueño, ahora 39 días (`#11`) y 15 días (`#12`) sin respuesta

Preámbulo de protocolo: clon llegó con `HEAD` sobre `develop` ya al día con `origin/develop` tras `git checkout develop && git pull origin develop` (fast-forward limpio, cinco commits, árbol de trabajo limpio antes y después). `pip install -r requirements-dev.txt` pelado volvió a reproducir el síntoma ya cerrado de `#22`/`#28`/P-06 (instala contra Python 3.13, no contra el `/usr/local/bin/python3` 3.11.17 real que usa `sys.executable`); `python3 -m pip install -r requirements-dev.txt` lo corrigió tal como documentan `DEVELOPERS.md`/`SKILL.md` — mismo perfil de siempre, no es hallazgo nuevo.

**Nota metodológica de esta pasada: reproducción fiel, y descartada, de un falso positivo ya cerrado (`#21`/bloqueo §3 #8, 2026-09-09).** Al revisar `git log --oneline -- roadmap/HOJA_DE_RUTA.md` para comprobar que el documento sigue inmutable, el resultado apuntaba a un único commit `81ad243` fechado 2026-10-20, **sin padre** (`git show --format="%P" -s` en blanco) y con TODO el árbol del repositorio listado como `new file` en su diff — aparentando que el historial real de `develop` solo arranca el 2026-10-20 y que las casi dos meses de T-00 a R-33 documentados en este mismo archivo (con sus commits citados uno a uno) no existirían como commits reales. Antes de escalarlo como hallazgo de integridad de severidad alta, se verificó la causa: `git rev-parse --is-shallow-repository` confirmó que el clon de este contenedor es **superficial** (`.git/shallow` listaba exactamente esos dos commits límite); `git fetch --unshallow origin` trajo el historial completo (526 commits, no 50), tras lo cual `81ad243` deja de ser root y aparecen de nuevo como objetos reales `e8b9663` (T-00) y commits anteriores hasta `f47be6b` ("initial commit"). Es exactamente el mismo artefacto de `git clone --depth` que el programador ya diagnosticó y cerró el 2026-09-09 (nota de bloqueo §3 #8) — reproducido de forma independiente por esta auditoría con una herramienta de verificación distinta (`--is-shallow-repository`/`--unshallow` en vez de comparar `git_repository.url`), por si alguna sesión futura lo encuentra y duda de nuevo: el historial de `develop` es real e íntegro, el clon de cada contenedor efímero simplemente llega truncado por profundidad hasta que se le pide expresamente lo contrario. No se abre hallazgo nuevo; se deja esta nota para que quede documentado el método de descarte, no solo la conclusión.

**Sin cambio de código que revisar.** `git log --oneline c4b4b90..HEAD -- scripts/ tests/ assets/ fixtures/` vacío: el único commit nuevo desde la auditoría anterior es la propia reconfirmación de cola del PM (`48d206a`, 2026-10-24 19:13), que no toca código ni specs — confirma por su propio mensaje que R-38 "sigue pendiente" y que no abre ninguna R-39 especulativa mientras R-38 no tenga código, mismo criterio ya aplicado en ciclos "sin apertura" anteriores (2026-10-04, 10-10, 10-11, 10-17). `roadmap/SEGUIMIENTO.md` §1 confirma: ninguna fila `PENDIENTE` salvo R-38, sin cambio en su ficha.

**Las cuatro redes, de punta a punta.** `python3 scripts/ci.py` completo sobre el `HEAD` actual (`48d206a`): mypy limpio (72 archivos), ruff sin avisos, **732/732 tests en verde** (mismo recuento que citaba el cierre de R-37, coherente con que no ha corrido código nuevo), `verificar_salidas.py --fixture` con las 19 etapas en `OK`, incluida la auto-contención de `reproductor.html` y de `guion-impresion.html` verificadas explícitamente. Reproducido también por separado con `python3 -m pytest tests/` (732 passed) y `python3 -m mypy scripts/ tests/` ("Success: no issues found in 72 source files"). Latencias esperadas sin cambios: `.pptx` real latente por falta de la skill `480-branded-pptx`, `.pdf` real latente por falta de Chrome/Edge headless en esta máquina.

**Invariantes reverificados directamente contra el código, no solo contra la narrativa de cierres anteriores.** Auto-contención: `grep -rnE "http[s]?://|@import|fetch\(|WebSocket|EventSource|sendBeacon" assets/reproductor/ assets/pdf/` sin resultados — cero recurso externo colado en las plantillas fuente, coherente con que el `verificar_salidas.py --fixture` de esta misma pasada confirmó lo mismo sobre la salida generada. Runtime solo con biblioteca estándar: `requirements-dev.txt` sigue limitado a `mypy`/`ruff`/`pytest`, los tres con su comentario explícito de "solo desarrollo"; ningún `import` nuevo que los traiga a `scripts/` (sin cambio de código desde R-37, nada que revisar aquí de nuevo). Defaults configurables: sin código nuevo, sin número mágico nuevo que comprobar.

**Coherencia roadmap/código.** `roadmap/SEGUIMIENTO.md` §3 (bloqueos), §4 (incidentes de deploy) y §7 (desviaciones) releídos enteros: sin filas nuevas desde la auditoría anterior, mismas ocho/cero/cinco entradas históricas de siempre. §6 (preguntas abiertas) releído entero: doce preguntas, diez respondidas y registradas con su decisión exacta, solo `#11`/`#12` siguen `(pendiente)`. Verificado con `list_triggers` (no solo con el texto de SEGUIMIENTO.md) que ni el cron ni el prompt de "product-manager-teleprompter" (`0 19 * * *`, dispara también fines de semana) ni de "programador-teleprompter" (`0 6-15 * * 1-5`, solo días laborables) han cambiado desde su creación — ninguna autorización nueva que aplicar a `#11`/`#12`; reconfirmado también, leyendo el prompt completo de las tres rutinas sin sufijo ("Auditor"/"Product manager"/"Programador"), que siguen apuntando a `centro-estudios-sw`/GestorAcademia, no a este repositorio — `#20` sigue cerrado sin ambigüedad. GitHub: 0 issues y 0 PRs abiertos/cerrados en `janosolerdiaz/teleprompter`, verificado con la API.

**`#24` y `#30`: sin ocasión de repetirse en esta pasada.** Ninguno de los dos hallazgos tiene un escenario nuevo que reconfirmar hoy, por razones distintas a las de las pasadas "sin desfase activo" anteriores (2026-10-19/20): hoy es domingo, así que el cron de "programador-teleprompter" (`0 6-15 * * 1-5`) no dispara ninguna reconfirmación horaria —no hay ninguna que pueda quedar ociosa (`#30`) ni ninguna ventana en la que `ROADMAP_PRODUCTO.md` pueda desactualizarse tras completarse una R-XX (`#24`), porque además R-38 sigue sin completarse. Ambos siguen `ABIERTO` únicamente a la espera de la respuesta del dueño: verificado de nuevo con `list_triggers` que ni el cron ni el prompt de ninguna de las dos rutinas han cambiado, así que no hay autorización nueva que aplicar — se deja constancia aquí, como en cada pasada, de que la espera lleva ya 39 días (`#11`, desde 2026-09-16) y 15 días (`#12`, desde 2026-10-10) sin que esta auditoría tenga ninguna acción propia que tomar al respecto más allá de seguir reconfirmando.

**Conclusión.** Quincuagésima sexta auditoría del proyecto (recuento de cabeceras `### Auditoría` de este mismo documento); sin ningún hallazgo nuevo de severidad media o alta desde la apertura de `#30` el 2026-10-10 (quince días, seis auditorías consecutivas sin novedad). El proyecto sigue en un estado sano: cero cambio de código en este intervalo y, aun así, las cuatro redes verificadas de punta a punta siguen en verde, los invariantes (auto-contención, biblioteca estándar en runtime, configuración centralizada) intactos y reverificados de forma independiente, y la coherencia roadmap/código completa. El único patrón a vigilar sigue siendo puramente de gobernanza (`#24`/`#30`), sin ningún efecto sobre la calidad ni la seguridad del producto entregado — y esta pasada, al no haber corrido ningún ciclo de Programador, ni siquiera ha tenido ocasión de manifestarse.

---

### Auditoría 2026-10-24 — sin hallazgos nuevos; R-37 (Oleada v25, cruce automático de «Toma» con la toma buena del parte de rodaje en `FEEDBACK.md`) completada y revisada línea a línea, buena calidad y coherente con los invariantes; R-38 (Oleada v26, avisar en `comandos-montaje.md` de los tropiezos caídos dentro de la toma buena) abierta con spec completa y bien fundamentada, correctamente `PENDIENTE` sin código; `#24` repetido por decimoctava vez CON desfase real (~13 h); `#30` repetido de nuevo (nueve reconfirmaciones ociosas del Programador tras R-37); ambos siguen `ABIERTO` pendientes de respuesta del dueño, ahora 38 días (`#11`) y 14 días (`#12`) sin respuesta

Preámbulo de protocolo: clon llegó con `HEAD` *detached* sobre `develop`, tres commits por detrás de `origin/develop`; `git checkout develop && git pull origin develop` lo resolvió sin conflicto (fast-forward limpio, árbol de trabajo limpio). `pip install -r requirements-dev.txt` pelado volvió a reproducir el síntoma de `#22`/`#28`/P-06 (instala con el intérprete equivocado, no con el `/usr/local/bin/python3` 3.11.17 real); `python3 -m pip install -r requirements-dev.txt` lo corrigió tal como documentan `DEVELOPERS.md`/`SKILL.md` — mismo perfil ya cerrado, no es hallazgo nuevo.

**Revisión de código: R-37 (`9004c0c`, implementada 2026-10-23 06:15).** Diff completo leído línea a línea, no solo el resumen de `SEGUIMIENTO.md`. `scripts/feedback.py::registrar_tropiezos_en_feedback` gana el parámetro opcional `tomas_por_escena` (mismo contenedor que `EstadoProyecto.tomas`, valor por defecto `None` que no rompe ninguna llamada existente — verificado que es verdad: `grep` confirma que `registrar_tropiezos_en_feedback` no se invoca todavía desde ningún otro script de `scripts/`, solo desde los tests y desde el propio flujo que sigue Claude al describirlo en `SKILL.md` §"Volcado a FEEDBACK.md", coherente con la arquitectura de esta skill — los scripts son funciones de librería que invoca el agente siguiendo el protocolo, no un único binario orquestador). La función nueva `_es_toma_buena` reutiliza tal cual `tomas.toma_buena` (R-02/R-11) sin envolver en `try`/`except`: si el parte de rodaje trae dos tomas `buena` en la misma escena, `RegistroTomasError` se propaga sin interceptar. Punto que esta auditoría verificó con especial atención, por ser una decisión que podría parecer, a primera vista, que endurece de más una columna meramente informativa: la razón que da `DECISIONES_TECNICAS.md` (coherencia con el único otro punto de la base de código que ya reutiliza `toma_buena`, `concat_ffmpeg.py` de R-19, y el principio de §0.2 de nunca enmascarar una corrupción de estado real) es sólida y se sostiene al leer el código — un dato corrupto en el parte de rodaje no debe convertirse en una columna vacía que parecería simplemente "sin dato todavía". El tercer grupo opcional de `_PATRON_FILA` (regex) se verificó con el mismo razonamiento ya validado en R-34/R-36: ninguno de los tres grupos capturados (`toma`, `toma_buena`, `instante`) se usa en `_filas_existentes` (solo decide cuántas columnas de relleno saltar antes de `estado`), así que el backtracking estándar de `re` basta para distinguir sin ambigüedad las cuatro anchuras de fila válidas (5 a 8 columnas) — confirmado además con el test nuevo `test_registrar_tropiezos_no_recalcula_una_fila_de_antes_de_r37`, que fija el requisito 7 de la spec (no recalcular filas ya escritas por una ejecución anterior). 5 tests nuevos (727→732), más el ajuste de 4 existentes al nuevo literal de fila. `references/contrato-tropiezos.md` correctamente NO sube de versión (sigue en 3: el cruce vive enteramente en Python al formatear la fila, nada cambia en el `.json` exportado ni en `guion.js`). `SKILL.md`/`DEVELOPERS.md` actualizados en el mismo commit (a diferencia de `#33`, que fue precisamente `SKILL.md` quedándose atrás tras R-34).

**Revisión de gobernanza: archivo de Oleada v25 y apertura de R-38 (PM, `c4b4b90`, 2026-10-23 19:18).** Diff completo de `DECISIONES_TECNICAS.md`/`SEGUIMIENTO.md`/`ROADMAP_HISTORICO.md`/`ROADMAP_PRODUCTO.md` leído entero. Sin ninguna de las grietas de proceso que motivaron `#29`/`#31`/`#32`: fila `R-37 | ... | COMPLETADA | 2026-10-23` ya estaba en §1 desde el ciclo de Programador (no es el PM quien la completa, solo la archiva); spec de R-38 completa en `ROADMAP_PRODUCTO.md` (Oleada v26: `calcular_comandos_montaje` gana `registro_tropiezos` opcional, nueva sección "Puntos a revisar antes de concatenar" solo si algún tropiezo cae en la toma buena, reutilizando la misma comparación que `feedback._es_toma_buena` — explícitamente fuera de alcance generar o ejecutar ningún comando de recorte real, mismo límite ya fijado por R-30/R-31); verificado con `grep -n "registro_tropiezos\|Puntos a revisar" scripts/comandos_montaje.py` que no hay código adelantado: R-38 sigue siendo pura especificación. `ROADMAP_PRODUCTO.md` actualizado en el mismo commit que archiva (prosa de "Oleada v25" y "Cola de producto" coherente con §1, sin el desfase que describe `#24`... salvo por las nueve reconfirmaciones intermedias, ver más abajo).

**Verificación de las cuatro redes, de punta a punta, no solo leída de la narrativa.** `python3 -m mypy scripts/ tests/`: limpio, 72 archivos. `python3 -m ruff check scripts/ tests/`: todo correcto. `python3 -m pytest`: **732/732 tests en verde**. `python3 scripts/verificar_salidas.py --fixture`: las 19 etapas en `OK`, incluida la auto-contención de `reproductor.html` y de `guion-impresion.html` (ambas verificadas explícitamente, no solo inferidas del resumen) — coincide exactamente con la cifra que cita el commit de R-37. Latencias esperadas y ya conocidas (sin cambios): `.pptx` real latente por falta de la skill `480-branded-pptx` en esta máquina, `.pdf` real latente por falta de Chrome/Edge headless.

**Coherencia roadmap/código.** `roadmap/SEGUIMIENTO.md` §3 (bloqueos) y §7 (desviaciones) releídos enteros: sin filas nuevas desde la auditoría anterior. §6 (preguntas abiertas) releído entero: doce preguntas, diez respondidas y registradas con su decisión exacta, solo `#11`/`#12` siguen `(pendiente)`; verificado con `list_triggers` que ni el cron ni el prompt de "product-manager-teleprompter" (`0 19 * * *`) ni de "programador-teleprompter" (`0 6-15 * * 1-5`) han cambiado desde su creación (2026-08-31/2026-09-02) — ninguna autorización nueva que aplicar a `#11`/`#12`. Reglas innegociables de §0.2 de `HOJA_DE_RUTA.md` contrastadas una por una contra el código de R-37: cero número mágico nuevo sin configurar, cero dependencia de runtime nueva, cero red, español en toda la documentación y mensajes nuevos, commit con prefijo correcto (`R-37: ...`), push a `develop` únicamente. Verificado también con `grep` que `assets/reproductor/` y `assets/pdf/` siguen sin ninguna referencia a `http(s)://`, `@import`, `fetch(`, `WebSocket` ni similares — auto-contención intacta (cambio de R-37 es puramente Python/Markdown, no toca ningún asset). GitHub: 0 issues y 0 PRs abiertos/cerrados en `janosolerdiaz/teleprompter`, verificado con la API.

**`#24` (baja, roadmap desactualizado durante reconfirmaciones) y `#30` (media, cadencia del Programador).** Ambos reconfirmados `ABIERTO` con el mismo patrón exacto de siempre, verificado de nuevo con `git log`/`git show --stat` commit a commit y no solo leyendo la narrativa de sesiones anteriores — detalle completo en el registro de hallazgos. R-37 quedó `COMPLETADA` a las 06:15 del 2026-10-23; `ROADMAP_PRODUCTO.md` siguió sin corregirse durante las nueve reconfirmaciones horarias de Programador siguientes (07:11 a 15:10, ninguna toca `scripts/`, `tests/`, `assets/` ni `fixtures/`) hasta que el ciclo de PM de las 19:18 (`c4b4b90`) archivó la Oleada v25 y corrigió la prosa en el mismo commit en que abrió R-38 — decimoctava repetición de `#24`, con casi trece horas de desfase (quinta vez consecutiva con desfase real), y nueva repetición de `#30` con el mismo coste de cómputo de siempre. Ninguno de los dos remedios de `#12` se ha aplicado y la autorización de `#11` sigue sin llegar — se deja constancia aquí, como en cada pasada, de que la espera de respuesta del dueño lleva ya 38 días (`#11`, desde 2026-09-16) y 14 días (`#12`, desde 2026-10-10) sin que esta auditoría tenga ninguna acción propia que tomar al respecto más allá de seguir reconfirmando.

**Conclusión.** Quincuagésima quinta auditoría del proyecto (recuento de cabeceras `### Auditoría` de este mismo documento); sin ningún hallazgo nuevo de severidad media o alta desde la apertura de `#30` el 2026-10-10. El proyecto sigue en un estado sano: arquitectura coherente con sus propias decisiones documentadas, calidad de código alta y consistente oleada tras oleada (razonamiento explícito de alternativas descartadas, tests de regresión dirigidos al propio riesgo que cada cambio introduce, documentación de cara al dueño actualizada en el mismo commit), invariantes de datos intactos y verificados de forma independiente, y ningún recurso externo colado en el reproductor generado. El único patrón a vigilar sigue siendo puramente de gobernanza (`#24`/`#30`), sin ningún efecto sobre la calidad ni la seguridad del producto entregado.

---

### Auditoría 2026-10-23 — sin hallazgos nuevos; R-36 (Oleada v24, vincular tropiezo con número de toma) completada y revisada línea a línea, buena calidad y coherente con los invariantes; R-37 (Oleada v25, cruce automático de «Toma» con la toma buena) abierta con spec completa y bien fundamentada, correctamente `PENDIENTE` sin código; `#24` repetido por decimoséptima vez CON desfase real (~13 h); `#30` repetido de nuevo (nueve reconfirmaciones ociosas del Programador tras R-36); ambos siguen `ABIERTO` pendientes de respuesta del dueño, ahora 37 días (`#11`) y 13 días (`#12`) sin respuesta

Preámbulo de protocolo: clon llegó con `HEAD` *detached* sobre `develop`, veinticinco commits por detrás de `origin/develop`; `git checkout develop && git pull` lo resolvió sin conflicto. `pip install -r requirements-dev.txt` pelado reprodujo una vez más el síntoma de `#28`/P-06 (instala contra Python 3.13, no contra el 3.11.17 real de `sys.executable`); `python3 -m pip install -r requirements-dev.txt` lo corrigió como documenta `DEVELOPERS.md`/`SKILL.md` — mismo perfil ya cerrado, no es hallazgo nuevo.

**Revisión de código: R-36 (`5b8492e`, implementada 2026-10-22 06:24).** Diff completo leído línea a línea, no solo el resumen de `SEGUIMIENTO.md`. Añade `numero_toma` (opcional, entero ≥ 1) a cada tropiezo marcado durante la grabación, calculado en `guion.js::alternarTropiezoBloqueActual` con el mismo cálculo que ya usa el indicador de cabecera (`tomasEscena[escena].length + 1`), guardado solo al marcar (no al desmarcar, mismo criterio que R-34). Lado Python (`scripts/feedback.py`): `TropiezoBloque.numero_toma` opcional con la misma validación que `instante_toma_segundos`; columna nueva «Toma» en `FEEDBACK.md`; `_PATRON_FILA` gana un segundo grupo opcional en la propia expresión regular. Punto que esta auditoría verificó con especial atención, porque es exactamente el tipo de ambigüedad de parseo que podría violar el invariante (a)/(d) en silencio: con dos grupos opcionales delante de `estado`, una fila de 6 columnas (versión 2 del contrato, con «Instante» pero sin «Toma») podría, en teoría, hacer que el valor caiga en el grupo `toma` en vez de en `instante` sin que el regex lo distinga — confirmado leyendo el resto del módulo que **ninguno de los dos valores capturados se usa en `_filas_existentes`** (solo escena/bloque/texto/estado deciden deduplicado y destacado), así que la ambigüedad de a qué grupo cae el valor es inocua por construcción, no por descuido: el propio commit lo razona explícitamente en `DECISIONES_TECNICAS.md` y lo prueba con un test dedicado (`test_registrar_tropiezos_sobre_un_feedback_de_la_version_2_no_duplica_filas`) que no existía hasta ahora. `references/contrato-tropiezos.md` sube a versión 3 documentando el campo y su límite («solo es de fiar cuando «Toma» coincide con la toma buena del parte de rodaje»); `SKILL.md` y `DEVELOPERS.md` actualizados en el mismo commit (a diferencia de `#33`, que fue precisamente SKILL.md quedándose atrás tras R-34). 8 tests nuevos (719→727). Verificado con `grep` que `assets/reproductor/` y `assets/pdf/` siguen sin ninguna referencia a `http(s)://`, `@import`, `fetch(`, `WebSocket` ni similares — auto-contención intacta.

**Revisión de gobernanza: archivo de Oleada v24 y apertura de R-37 (PM, `e6b1e9b`, 2026-10-22 19:18).** Diff completo de `DECISIONES_TECNICAS.md`/`SEGUIMIENTO.md` leído entero, no solo la cabecera. Sin ninguna de las grietas de proceso que motivaron `#29`/`#31`/`#32`: fila `R-37 | ... | PENDIENTE | 2026-10-22 | ...` añadida a §1 en el mismo commit que abre la tarea, entrada `PM (apertura de R-37)` en `DECISIONES_TECNICAS.md` con las tres alternativas consideradas y motivo de descarte de cada una, spec completa de R-37 en `ROADMAP_PRODUCTO.md` (7 requisitos, migración explícitamente "No", dependencias citadas con su estado `COMPLETADA`, criterio de aceptación concreto con cifras de ejemplo). R-37 reutiliza `scripts/tomas.toma_buena` (ya construida por R-02/R-11) en vez de reimplementar la regla de "como mucho una toma buena por escena" — coherente con el principio de no duplicar lógica ya existente que otras oleadas (R-19/R-20/R-21) ya siguieron.

**Verificación de las cuatro redes, de punta a punta, no solo leída de la narrativa.** `python3 scripts/ci.py` completo sobre el `HEAD` actual: mypy limpio (72 archivos), ruff limpio, **727/727 tests en verde**, `verificar_salidas.py --fixture` con las 19 etapas en `OK` (incluida la auto-contención del reproductor y del HTML de impresión). Reproducido también por separado con `python3 -m pytest tests/` (727 passed). Coincide exactamente con la cifra que cita el commit de R-36.

**Coherencia roadmap/código.** `roadmap/SEGUIMIENTO.md` §3 (bloqueos) y §7 (desviaciones) releídos enteros: sin filas nuevas desde la auditoría anterior, siguen con las mismas ocho (§3) y cinco (§7) entradas históricas de siempre, ya cerradas o en espera indefinida del dueño (clicker Bluetooth, paquete `480-branded-pptx`, rodaje real de un curso completo). §6 (preguntas abiertas) releído entero: doce preguntas, diez respondidas y registradas con su decisión exacta, solo `#11`/`#12` siguen `(pendiente)`. Reglas innegociables de §0.2 de `HOJA_DE_RUTA.md` contrastadas una por una contra el código de R-36/R-37: ningún número mágico nuevo sin configurar (el mínimo `numero_toma >= 1` es una restricción estructural del dominio, no un valor por defecto sobreescribible, mismo criterio ya aplicado a `instante_toma_segundos >= 0`), cero dependencias de runtime nuevas, cero red, español en toda la documentación y mensajes nuevos, commits con prefijo correcto. `roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía — el bloqueo `#7` (grabar un curso real) sigue siendo la única fricción real capaz de motivar producto nuevo por esa vía; todo lo demás de esta oleada nació de una grieta de arquitectura verificada, no de feedback.

**`#24` (baja, roadmap desactualizado durante reconfirmaciones) y `#30` (media, cadencia del Programador).** Ambos reconfirmados `ABIERTO` con el mismo patrón exacto de siempre, verificado de nuevo con `git log`/`git show --stat` commit a commit y no solo leyendo la narrativa de sesiones anteriores — detalle completo en el registro de hallazgos. Ninguno de los dos remedios de `#12` se ha aplicado y la autorización de `#11` sigue sin llegar; verificado con `list_triggers` que ni el prompt de "product-manager-teleprompter" ni el cron de "programador-teleprompter" han cambiado desde su creación. Es la decimoséptima y novena repetición respectivamente, sin que ninguna de las dos represente nunca un riesgo real de producto (ambas puramente de proceso/coste, nunca de corrección ni de seguridad) — se deja constancia aquí, como en cada pasada, de que la espera de respuesta del dueño lleva ya 37 días (`#11`, desde 2026-09-16) y 13 días (`#12`, desde 2026-10-10) sin que esta auditoría tenga ninguna acción propia que tomar al respecto más allá de seguir reconfirmando.

**Conclusión.** Quincuagésima cuarta auditoría del proyecto (recuento de cabeceras `### Auditoría` de este mismo documento); sin ningún hallazgo nuevo de severidad media o alta desde la apertura de `#30` el 2026-10-10. El proyecto sigue en un estado sano: arquitectura coherente con sus propias decisiones documentadas, calidad de código alta y consistente oleada tras oleada (razonamiento explícito de alternativas descartadas, tests de regresión dirigidos al propio riesgo que cada cambio introduce, documentación de cara al dueño actualizada en el mismo commit), invariantes de datos intactos y verificados de forma independiente, y ningún recurso externo colado en el reproductor generado. El único patrón a vigilar sigue siendo puramente de gobernanza (`#24`/`#30`), sin ningún efecto sobre la calidad ni la seguridad del producto entregado.

### Auditoría 2026-10-22 — sin hallazgos nuevos; cierra `#33` (P-07 ya documentó «Instante» en SKILL.md); R-35 (Oleada v23, relocalizar tropiezos por texto) completada y verificada, buena calidad y coherente con los invariantes; R-36 (Oleada v24) abierta con grieta de arquitectura verificada; `#24` repetido por decimosexta vez CON desfase real (~13 h); `#30` repetido de nuevo (ocho reconfirmaciones ociosas del Programador tras R-35); ambos siguen `ABIERTO` pendientes de respuesta del dueño

**Nota de arranque.** El contenedor arrancó con `HEAD` *detached* 13 commits por detrás de
`develop`; `git checkout develop && git pull origin develop` lo puso al día con `origin/develop`
(`18f0ee2`) por fast-forward, sin ningún cambio local que perder. Árbol de trabajo limpio antes y
después.

**Reinstalación de dependencias.** Igual que documentan `#22`/`#28`: el `pip install -r
requirements-dev.txt` pelado del preámbulo resolvió contra Python 3.13 (síntoma intacto, el
contenedor no cambia), confirmado reproduciendo el fallo (`pip show mypy` vacío tras el primer
intento); `python3 -m pip install -r requirements-dev.txt` instaló correctamente
`mypy==1.18.2`/`ruff==0.14.0`/`pytest==8.4.2` contra el intérprete real (Python 3.11.17). Sin
incidencia nueva — la documentación de `#28` sigue cubriendo exactamente este rodeo.

**Las cuatro redes, en verde.** `python3 scripts/ci.py` completo: mypy limpio sobre 72 archivos,
`ruff check .` sin avisos, **719/719 tests** en pytest, y `verificar_salidas.py --fixture` con las
19 etapas en `OK` sobre `fixtures/guion-ejemplo.md` — incluida la auto-contención del reproductor y
del HTML de impresión, ambas explícitamente `OK`. El aviso de desajuste de versión de Python
(`#12`/R-08) sigue imprimiéndose como aviso no bloqueante, tal como diseñado.

**Cierro `#33`.** P-07 (commit `2c24017`, 2026-10-21 07:13) documentó la columna «Instante» en
`SKILL.md`: leído el archivo completo en esta pasada, la sección "Marcar tropiezos durante la toma
(R-03)" trae ahora el párrafo "Desde R-34, cada tropiezo marcado durante la grabación guarda
además..." y la tabla de columnas pasa a `Fecha/Escena/Bloque/Texto exacto/Instante/Estado`,
citando "(R-34)" explícitamente — cierre completo, mismo patrón que ya usó R-07 para
`titulo_seccion_capitulos` y R-19/R-21 para `archivo_video`.

**R-35 (Oleada v23), revisada línea a línea.** El hallazgo de arquitectura que la abrió (`guion.js`
guardaba tropiezos por `indice_bloque` crudo de `localStorage`, sin revalidar si el troceo de la
escena había cambiado desde que se marcaron) es real y el arreglo lo cierra con el mismo criterio
ya establecido por `scripts/feedback.py` para el mismo problema del lado Python: casar por texto
exacto, nunca por índice. Verificado leyendo el diff completo de `assets/reproductor/guion.js`
(no solo el resumen del commit): `cargarTropiezosGuardados(escena, indice)` comprueba primero el
camino feliz (`escena.bloques[indice_bloque].texto === texto`, sin tocar nada si coincide), y solo
si no coincide busca el mismo texto exacto entre todos los bloques de la escena, relocalizando con
coincidencia única y descartando con cero o más de una — exactamente la contraparte en JavaScript
del contrato que `references/contrato-tropiezos.md` ya documentaba para Python. La corrección
(reubicación o descarte) se fija de inmediato en `localStorage`, pero **solo para las escenas que
de verdad cambiaron** (`_indicesConCorreccionDeTropiezos`, poblado durante el propio `.map` que
construye `tropiezosEscena`): no reescribe las claves de escenas sin ningún tropiezo o ya
correctas, coherente con el criterio de "no tocar lo que no hace falta" que ya aplican R-21/R-24.
Punto más fino, y bien resuelto: el propio objeto `normalizado` solo copiaba antes `indice_bloque`
y `texto` del valor crudo; sin copiar también `instante_toma_segundos` (R-34) antes de decidir si
se conserva/relocaliza/descarta, el requisito 3 de esta misma tarea ("guardar de inmediato la
corrección") habría fijado esa pérdida para siempre en el primer guardado — el propio commit lo
documenta como detectado durante la implementación, no después, y el test
`test_guion_js_conserva_instante_toma_segundos_al_relocalizar` lo cubre. `cargarTomasGuardadas`
queda intacto (confirmado: cero referencias a `indice_bloque` en su cuerpo), tal como exige el
requisito 5 de la ficha. 6 tests nuevos (713→719), todos aserciones estructurales sobre el texto
fuente generado — mismo patrón de testing ya usado en todo `test_reproductor.py` desde T-18 (sin
motor de JavaScript como dependencia de desarrollo, por decisión reiterada y documentada en
`DECISIONES_TECNICAS.md`: Playwright se usa a mano, sesión a sesión, nunca como dependencia del
proyecto), no una regresión de cobertura de esta tarea.

**R-36 (Oleada v24), apertura verificada.** El PM abre R-36 tras detectar que `tropiezosEscena`
es una lista plana por escena que se acumula a través de TODAS las tomas grabadas, sin distinguir
cuál pertenece a la toma `buena` que de verdad llega al montaje — confirmado leyendo `guion.js`:
ni `finalizarTomaActual` ni el manejador de `G` reinician o particionan `tropiezosEscena[escena]`
por número de toma. Es una grieta de arquitectura real, del mismo tipo y mismo criterio de apertura
ya usado desde R-12 (verificada sobre código construido, no especulativa), y la especificación en
`ROADMAP_PRODUCTO.md` queda acotada (columna «Toma» en `FEEDBACK.md`, versión 3 del contrato, sin
cruce automático contra el registro de tomas). `SEGUIMIENTO.md` §1 gana su fila `PENDIENTE` en el
mismo commit, sin el hueco que motivó `#29`.

**`#24` y `#30`, reconfirmados con el mismo patrón exacto que las pasadas anteriores.** Verificado
con `git log` acotado a los rangos exactos (detalle completo en las filas del registro, no
repetido aquí): la prosa de "Cola de producto" de `ROADMAP_PRODUCTO.md` quedó obsoleta durante
las nueve reconfirmaciones horarias de Programador que siguieron a la finalización de R-35
(06:21), corregida solo cuando el ciclo de PM archivó la oleada a las 19:15 (~13 h de desfase,
decimosexta repetición de `#24`) — y ocho de esas nueve reconfirmaciones no tuvieron ninguna tarea
`PENDIENTE` que ejecutar, pagando igualmente el protocolo completo para terminar en "sin novedad de
código" (repetición de `#30`). Verificado con `list_triggers` en esta misma sesión, no solo
asumido: las tres rutinas de este proyecto (`auditor-teleprompter` diario a las 03:00,
`product-manager-teleprompter` diario a las 19:00, `programador-teleprompter` horario `6-15`
L-V) conservan exactamente el mismo cron y el mismo texto de prompt desde su creación
(2026-08-31/2026-09-02) — no hay ninguna respuesta del dueño a las preguntas `#11`/`#12` de §6 que
aplicar todavía, así que ambos hallazgos permanecen `ABIERTO` por el motivo correcto: nada que un
agente pueda resolver por su cuenta, no un descuido de proceso.

**Coherencia documental y de gobernanza.** `DECISIONES_TECNICAS.md` registra la apertura de R-36
con sus alternativas descartadas, sin la premisa de "convención" que motivó `#31`. `§7` de
`SEGUIMIENTO.md` (desviaciones) sin entradas nuevas desde la última pasada — las cinco existentes
siguen siendo las mismas, todas cerradas o absorbidas en la norma. `§6` (preguntas al dueño) sin
cambios más allá de las reconfirmaciones de `#11`/`#12` ya descritas. No se encontró ninguna otra
grieta entre `DECISIONES_TECNICAS.md`/§0.2 de `HOJA_DE_RUTA.md` y el código real en los módulos
tocados por R-33/R-34/R-35 (`reproductor.py`, `feedback.py`, `guion.js`): los tres añaden su campo
de configuración nuevo donde corresponde (`Configuracion.titulo_seccion_preparacion`, documentado
en `SKILL.md`), sin número mágico suelto.

**Conclusión general.** Trigésima sexta oleada de trabajo real (R-00 a R-36 contando T-00 a T-33),
mismo nivel de rigor que el resto del historial: código, tests y documentación avanzan juntos,
sin ninguna grieta nueva entre lo decidido y lo implementado, y el único hallazgo nuevo cerrado
esta pasada (`#33`) lo cerró el propio equipo el mismo día en que se detectó. Los dos hallazgos que
siguen `ABIERTO` (`#24`, `#30`) son exactamente lo que llevan siendo desde que se abrieron: coste de
proceso sin ningún riesgo de producto, correctamente enrutados como preguntas de gobernanza que
solo el dueño puede resolver, reconfirmados con evidencia fresca en cada pasada en vez de darse por
buenos sin mirar.

### Auditoría 2026-10-21 — un hallazgo nuevo de baja severidad (`#33`, `SKILL.md` sin actualizar tras R-34); R-34 (Oleada v22, instante del tropiezo) completada y verificada línea a línea, buena calidad y coherente con los invariantes; R-35 (Oleada v23) especificada y correctamente `PENDIENTE` sin código, premisa del bug verificada contra el código real; `#24` repetido por decimoquinta vez, esta vez CON desfase real (trece horas); `#30` repetido de nuevo (nueve reconfirmaciones ociosas del Programador tras R-34); ambos siguen `ABIERTO` pendientes de respuesta del dueño

**Nota de arranque.** El contenedor arrancó con `HEAD` *detached* sobre `develop` desactualizado
un commit (`e72ae37`); `git checkout develop && git pull origin develop` lo puso al día con
`origin/develop` (`12a1be7`) por fast-forward, sin ningún cambio local que perder. Árbol de
trabajo limpio antes y después.

**Reinstalación de dependencias.** Igual que documentan `#22`/`#28`, `python3 -m pip install -r
requirements-dev.txt` instaló `mypy==1.18.2`/`ruff==0.14.0`/`pytest==8.4.2` contra el intérprete
real (Python 3.11.17). Sin incidencia nueva.

**Verificación propia completa.** `python3 scripts/ci.py` da las cuatro redes en verde: `mypy`
sin hallazgos (72 archivos), `ruff` sin hallazgos, **713 tests** (↑ desde 704 en la auditoría
anterior, coherente con los 9 tests nuevos de R-34) y las diecinueve etapas de
`verificar_salidas.py --fixture` en `OK`, incluida la auto-contención de `reproductor.html` y
`guion-impresion.html`. Aviso textual ya conocido y aceptado (desajuste Python 3.11 real vs.
`>=3.12` declarado en `pyproject.toml`, T-06). `.pptx` y `.pdf` quedan `SalidaLatente` como es
esperado (skill de marca y Chrome/Edge ausentes en este contenedor); `concat_ffmpeg`/
`comandos_montaje` se omiten por falta de parte de rodaje — sin novedad.

**Incidencia de esta sesión, resuelta en el momento: clon superficial.** Al reconstruir el
historial de `scripts/reescrituras.py`/`scripts/revalidacion.py` para verificar el invariante (b),
`git log` señalaba como último commit real uno de reconfirmación "sin novedad de código"
(`20b3005`, 2026-10-15) con un diff de "archivo nuevo" de cientos de líneas — exactamente el
síntoma que `#21` (RESUELTO, 2026-09-09) ya documentó y explicó: clon superficial (`git clone
--depth`) con `20b3005` como límite del historial descargado, no una reescritura real.
Reproducido y resuelto de la misma forma que entonces, no solo dado por bueno: `git rev-parse
--is-shallow-repository` confirmó `true`; `git fetch --unshallow origin` (operación de solo
lectura) trajo el historial completo (488 commits); repetida la consulta tras el `unshallow`,
el último commit real que toca esos dos archivos es `5fa5ac8` (R-29, 2026-10-14), coherente con
que R-34 no los toca. No es un hallazgo nuevo — es la reaparición ya prevista y cerrada de `#21`,
dejada aquí constando por transparencia del proceso de esta pasada, no porque requiera ninguna
acción.

**Un commit de código desde la auditoría anterior, revisado línea a línea, no solo por su
mensaje.**

- **R-34 (`91b4c66`) — captura el instante real del tropiezo dentro de la toma en curso.**
  `assets/reproductor/guion.js`: el cálculo de tiempo transcurrido de la toma, antes repetido en
  `actualizarCronometro` y `finalizarTomaActual`, se extrae a una única función compartida
  `tomaTranscurridoMs()` (requisito 1: "promover la función que ya existe, no duplicarla", mismo
  criterio que R-19/R-20) — verificado leyendo las tres funciones que la reutilizan, ninguna
  repite el cálculo por su cuenta. `alternarTropiezoBloqueActual` la reutiliza para guardar
  `instante_toma_segundos` solo en la rama que AÑADE el tropiezo (`posicion === -1`), nunca en la
  que lo quita (`lista.splice`) — confirmado leyendo ambas ramas, requisito 2 cumplido por
  construcción, no por comentario. `scripts/feedback.py`: `TropiezoBloque.instante_toma_segundos`
  opcional (`float | None`), validado numérico y ≥0 en `_tropiezo_desde_dict`; columna nueva
  «Instante» en `FEEDBACK.md`, formateada `mm:ss` con minutos a dos dígitos (`_formatear_instante`,
  deliberadamente distinta de `capitulos_youtube._formatear_mm_ss`, que resuelve un problema
  distinto — razonado en `DECISIONES_TECNICAS.md`). **Punto más delicado del cambio, verificado a
  mano con `re.match` suelto además de confiar en los tests:** `_PATRON_FILA` hace opcional el
  tramo `instante \|` completo (grupo + su separador) en la propia expresión regular, apoyándose en
  el backtracking estándar de `re` — una fila de 5 columnas (versión 1 del contrato, escrita antes
  de R-34) se sigue reconociendo exactamente igual que una de 6, sin perder en silencio el estado
  `nuevo`/`resuelto` de ninguna fila ya marcada por el dueño. Probado con las dos formas a mano:
  ambas encajan sin ambigüedad. `references/contrato-tropiezos.md` sube a versión 2 (cambio
  aditivo, documentado como tal) y fija el límite honesto del requisito 3: el instante no se
  re-ancla si la escena se regraba desde cero. 9 tests nuevos verificados por nombre y contenido
  (5 en `test_feedback.py`, 4 en `test_reproductor.py`): cubren carga/validación del campo,
  formateo `mm:ss`, retrocompatibilidad de la fila de 5 columnas, reutilización de la función
  compartida, captura solo al marcar (nunca al desmarcar) y la subida de `version` a 2. Sin
  objeción.

**Los seis invariantes, revisados directamente contra el código actual.** (a) cobertura total
intacta (`test_deteccion.py::test_cobertura_total_guiones_reales` en verde); (b) original
recuperable + edición manual intacto: `reescrituras.py`/`revalidacion.py` sin tocar desde R-29
(`5fa5ac8`, 2026-10-14), confirmado tras resolver la incidencia de clon superficial descrita
arriba; (c) auto-contención: `grep` propio sobre `assets/reproductor/*` (incluido el código nuevo
de R-34) sin ninguna URL, CDN ni `fetch` externo, y la cuarta red de `verificar_salidas.py` certifica
lo mismo de forma automática; (d) runtime solo stdlib: barrido de imports de los 33 módulos de
`scripts/*.py` con un script propio (AST, no solo `grep`, distinguiendo módulos locales de
paquetes de terceros) — cero paquete de terceros, `pyproject.toml` sigue con `dependencies = []`;
(e) configuración: R-34 no añade ningún campo a `Configuracion` ni ningún número mágico de negocio
(el formato `mm:ss` es una convención de presentación, no un umbral configurable) —
`tests/test_skill_md.py` sigue en verde, aunque ver `#33` más abajo sobre la documentación de la
*funcionalidad*, no de la configuración; (f) contención + `.bak`: `grep -rln
"copia_seguridad\s*=" scripts/*.py` sigue devolviendo exactamente los mismos cuatro sitios
(`documento_revision.py`, `entrada.py`, `feedback.py`, `instalar_skill.py`), sin regresión.
**Los seis invariantes se cumplen.**

**Hallazgo nuevo: `#33`, `SKILL.md` sin actualizar tras R-34 (baja).** Detalle completo en el
registro de hallazgos. En síntesis: la sección de `SKILL.md` que describe "Marcar tropiezos
durante la toma" para el dueño sigue mostrando la tabla de `FEEDBACK.md` de 5 columnas, sin
ninguna mención a la columna «Instante» ni a R-34, mientras que `references/contrato-tropiezos.md`,
`DEVELOPERS.md` y `DECISIONES_TECNICAS.md` sí documentan el cambio con detalle ejemplar — y la
sección inmediatamente anterior del mismo archivo (tomas, R-02) sí ganó su párrafo "Desde R-19..."
cuando le pasó lo mismo con `archivo_video`. No infringe ningún invariante automatizado (no es un
campo de `Configuracion`) ni pone en riesgo ningún dato; es una inconsistencia de documentación de
cara al dueño, fácil de cerrar con un párrafo análogo al de R-19/R-21.

**`#24` reconfirmado: decimoquinta repetición, esta vez CON desfase real.** A diferencia de las
dos pasadas anteriores (R-32/R-33, archivadas en el mismo commit que abría la siguiente R-XX, sin
hueco), esta vez sí hay un desfase real de trece horas: R-34 quedó `COMPLETADA` en §1 a las 06:21
(`91b4c66`) y `ROADMAP_PRODUCTO.md` siguió diciendo "sin implementar" hasta que el PM archivó a
las 19:19 (`12a1be7`). Detalle completo con hashes en el registro de hallazgos. Sigue `ABIERTO`
solo porque la pregunta `#11` de §6 sigue `(pendiente)`.

**`#30` reconfirmado: repetido de nuevo con R-34.** Nueve reconfirmaciones horarias de Programador
(`4402ff7` a `e72ae37`, 07:08 a 15:09) entre que R-34 se completó y el PM archivó, ninguna con
cambio de código, confirmado commit a commit con `git show --stat`. Mismo patrón exacto de coste
de cómputo ya descrito por el hallazgo. Sigue `ABIERTO`: pregunta `#12` de §6 sigue `(pendiente)`.

**Coherencia roadmap↔código y §7.** La apertura de R-35 (`12a1be7`, solo ciclo de PM) se
contrastó contra el código real, no solo contra su propia prosa: el commit afirma que el
indicador "⚠ Tropiezo" del reproductor "compara `indice_bloque` de forma literal al releer
`localStorage`" en vez de casar por texto exacto como exige `references/contrato-tropiezos.md` del
lado Python — verificado con `grep -n "indice_bloque" assets/reproductor/guion.js`: las líneas
1152 y 1177 en efecto comparan `tropiezo.indice_bloque === bloqueActual` de forma literal. Premisa
correcta, R-35 bien fundamentada. La decisión técnica única de R-34 (regex retrocompatible,
`_formatear_instante` propio) contrastada contra las reglas innegociables de `HOJA_DE_RUTA.md`
§0.2: auto-contención, runtime stdlib, sin números mágicos sueltos, codificación UTF-8 explícita y
logger centralizado — ninguna regla violada. `SEGUIMIENTO.md` §7 sin ninguna desviación activa
nueva: las siete filas existentes siguen siendo todas de 2026-08-31/09-02, cerradas o incorporadas
a la norma permanente. §3 (bloqueos) y §5 (P-XX) sin cambios.

**Verificación GitHub y `FEEDBACK.md`.** `list_issues`/`list_pull_requests` sobre
`janosolerdiaz/teleprompter` devuelven cero issues y cero PR abiertos/cerrados. `roadmap/FEEDBACK.md`
sigue con su única fila de plantilla vacía, sin ninguna entrada `nuevo`.

---

### Auditoría 2026-10-20 — sin hallazgos nuevos; R-32 (Oleada v20, exportador `.pdf`) y R-33 (Oleada v21, checklist de preparación) completadas y verificadas línea a línea, ambas de buena calidad y coherentes con los invariantes; R-34 (Oleada v22) especificada y correctamente `PENDIENTE` sin código; `#24` reconfirmado sin desfase activo; `#30` repetido dos veces en el mismo día (ocho reconfirmaciones ociosas del Programador en torno a R-32/R-33), sigue `ABIERTO` pendiente de respuesta del dueño

**Nota de arranque.** A diferencia de las últimas pasadas, esta vez sin incidencia: el contenedor ya
arrancó sobre `develop` y `git status`/`git pull origin develop` confirmaron que el clon local
estaba al día con `origin/develop` sin ninguna divergencia que requiriera `reset --hard`. Árbol de
trabajo limpio antes y después.

**Reinstalación de dependencias.** Igual que documentan `#22`/`#28`, el `pip` pelado de este
contenedor resuelve contra un intérprete distinto del real; `python3 -m pip install -r
requirements-dev.txt` instaló `mypy==1.18.2`/`ruff==0.14.0`/`pytest==8.4.2` contra el intérprete real
(Python 3.11.17). Sin incidencia nueva.

**Verificación propia completa.** `python3 scripts/ci.py` da las cuatro redes en verde: `mypy` sin
hallazgos, `ruff` sin hallazgos, **704 tests** (↑ desde 696 en la auditoría anterior, coherente con
los 3 tests nuevos de R-32 y los 5 de R-33) y las diecinueve etapas de `verificar_salidas.py
--fixture` en `OK`, incluida la auto-contención de `reproductor.html` y `guion-impresion.html`. Aviso
textual ya conocido y aceptado (desajuste Python 3.11 real vs. `>=3.12` declarado en
`pyproject.toml`, T-06). `.pptx` y `.pdf` quedan `SalidaLatente` como es esperado (skill de marca y
Chrome/Edge ausentes en este contenedor); `concat_ffmpeg`/`comandos_montaje` se omiten por falta de
parte de rodaje — sin novedad.

**Tres commits de código desde la auditoría anterior, los tres revisados línea a línea, no solo por
su mensaje.**

- **R-32 (`aa3e86c`) — exportador `.pdf`, distingue Chrome ausente de Chrome detectado pero fallido.**
  `ResultadoPdf` gana `chrome_detectado: bool`; `_generar_pdf` pasa de dos a tres desenlaces (éxito /
  `SalidaLatente` sin Chrome / `SalidaOmitida` con diagnóstico real si Chrome está pero la conversión
  revienta), reutilizando tal cual `volcar_diagnostico`/`ruta_diagnostico`/`obtener_logger` de R-24 —
  mismo criterio de diagnóstico que el resto de salidas desde esa tarea. `convertir_html_a_pdf` sigue
  sin lanzar nunca (T-28 intacto). El patrón `raise RuntimeError(...)` capturado de inmediato dentro
  de `_generar_pdf` para obtener un `__traceback__` real está explícitamente razonado en
  `DECISIONES_TECNICAS.md` (alternativa descartada: construir la excepción sin lanzarla, que dejaría
  `volcar_diagnostico` sin traza útil) — no es un descuido, es la opción correcta dado que
  `traceback.format_exception` necesita un `__traceback__` real. 3 tests nuevos verificados a mano:
  cubren tanto el camino nuevo (Chrome detectado + conversión fallida → diagnóstico en disco, motivo
  correcto, nunca latente) como el de regresión explícito (sin Chrome, comportamiento idéntico al de
  antes de R-32). Sin objeción.
- **R-33 (`ef8727c`) — checklist de "Preparación antes de grabar" reabrible en el reproductor.**
  `reproductor.py::_buscar_seccion_preparacion` localiza la sección por prefijo (mismo patrón que
  `capitulos_youtube._buscar_seccion_capitulos` de R-07, verificado leyendo ambas funciones una junto
  a la otra) y su contenido íntegro —nunca fabricado— viaja al payload como `preparacion_antes_grabar`
  (`None` si el guión no trae la sección). La garantía de "nunca se abre durante una cuenta atrás o el
  registro de una toma" queda satisfecha **por construcción**, no por una comprobación de estado: el
  panel y su manejador de teclado (`manejarTeclaIndice`) solo existen dentro del índice de escenas
  (`renderizarIndice`), nunca en `renderizarReproductor`, donde viven esas dos situaciones — decisión
  razonada explícitamente en `DECISIONES_TECNICAS.md` frente a la alternativa descartada de una
  comprobación de estado en la vista de reproducción. `Configuracion.titulo_seccion_preparacion` es un
  campo propio en vez de indexar `SECCIONES_AUXILIARES[1]`, mismo criterio ya usado por R-07 para
  `titulo_seccion_capitulos` y correctamente documentado en `SKILL.md` (tabla de secciones auxiliares
  y de campos de `Configuracion`, confirmado con `grep`). La tecla nueva `P`/`p` está en
  `MAPA_TECLAS_REPRODUCTOR` y en `references/mapa-teclas.md`. Verificado también que la apertura
  automática no rompe el invariante de que `renderizarIndice();` es la última sentencia del script
  (test ya existente que lo protege, mencionado en `DECISIONES_TECNICAS.md` como motivo de descartar
  el primer borrador de la implementación). Visualmente verificado con Playwright según el propio
  commit. Sin objeción.
- **R-34 (`93c7dc3`, solo ciclo de PM) — Oleada v22 especificada, correctamente sin implementar.**
  Verificado con `grep -rn "instante_toma_segundos" scripts/feedback.py assets/reproductor/guion.js
  references/contrato-tropiezos.md`: cero coincidencias, confirmando que §1 (`PENDIENTE`) y el código
  están sincronizados. La ficha en `ROADMAP_PRODUCTO.md` (Oleada v22) sigue el mismo formato que
  cualquier R-XX archivada, con un requisito 3 ("límite documentado, no resuelto con heurística") que
  anticipa honestamente la limitación del dato cuando se regraba una escena desde cero, y un "fuera de
  alcance" explícito (nada de comandos `ffmpeg` automáticos todavía, nada en `estado.json`, ninguna
  tecla nueva). `DECISIONES_TECNICAS.md` razona por qué esta vez el PM abre pero no implementa en la
  misma sesión (a diferencia de R-33): R-34 toca el cronómetro de `guion.js` que ya está en producción
  y exige redactar con cuidado `references/contrato-tropiezos.md` antes de tocar código. Sin objeción.

**Los seis invariantes, revisados directamente contra el código actual** (no solo frente al estado de
la auditoría anterior, por si R-32/R-33 hubieran introducido alguna grieta): (a) cobertura total
intacta (`test_deteccion.py::test_cobertura_total_guiones_reales` en verde); (b) original recuperable
+ edición manual intacto (`reescrituras.py`/`revalidacion.py` sin tocar desde la auditoría anterior,
confirmado con `git log`); (c) auto-contención: `grep` propio sobre `assets/reproductor/*` (incluido
el código nuevo de R-33) sin ninguna URL, CDN ni `fetch` externo; (d) runtime solo stdlib: barrido de
imports de los 35 módulos de `scripts/*.py` con un script propio (AST, no solo `grep`) — cero paquete
de terceros, `pyproject.toml` sigue con `dependencies = []`; (e) configuración: `titulo_seccion_preparacion`
(el único campo nuevo desde la auditoría anterior) está documentado en `SKILL.md`, confirmado con
`grep`, y `tests/test_skill_md.py` sigue en verde; (f) contención + `.bak`: `grep -rln
"copia_seguridad\s*=" scripts/*.py` sigue devolviendo exactamente los mismos cuatro sitios, sin
regresión. **Los seis invariantes se cumplen.**

**`#24` reconfirmado: sin desfase activo.** `git log --oneline b4c597e..HEAD -- roadmap/ROADMAP_PRODUCTO.md`
trae solo `ef8727c` (que archiva R-32 y abre R-33 en el mismo commit) y `93c7dc3` (que archiva R-33 y
abre R-34 en el mismo commit) — nunca queda una referencia obsoleta a mitad camino, así que ninguna de
las ocho reconfirmaciones horarias de Programador intercaladas tuvo nada que corregir. Sigue `ABIERTO`
solo porque la pregunta `#11` de §6 sigue `(pendiente)`.

**`#30` repetido de nuevo, dos veces en el mismo día.** Detalle completo con hashes y horas en el
registro de hallazgos. Ocho reconfirmaciones horarias de Programador (`8199be5`, `1279660`, `5309a73`,
`11c1497`, `51053c9`, `f74df19`, `dabdf26`, `b99c4df`) sin ningún cambio de código, confirmado commit a
commit con `git show --stat`, repartidas en dos tandas alrededor de R-32/R-33. Mismo patrón exacto de
coste de cómputo ya descrito por el hallazgo. Sigue `ABIERTO`: pregunta `#12` de §6 sigue `(pendiente)`.

**Coherencia roadmap↔código y §7.** Las tres decisiones técnicas nuevas (R-32, R-33, apertura de R-34)
contrastadas contra las reglas innegociables de `HOJA_DE_RUTA.md` §0.2: auto-contención, runtime
stdlib, sin números mágicos sueltos, codificación UTF-8 explícita y logger centralizado — ninguna regla
violada, confirmado leyendo el diff completo de cada commit, no solo su mensaje. `SEGUIMIENTO.md` §7
sin ninguna desviación activa nueva: las siete filas existentes siguen siendo todas de 2026-08-31/09-02,
cerradas o incorporadas a la norma permanente. §3 (bloqueos) y §5 (P-XX) sin cambios.

**Verificación GitHub y `FEEDBACK.md`.** `list_issues`/`list_pull_requests` sobre
`janosolerdiaz/teleprompter` devuelven cero issues y cero PR abiertos. `roadmap/FEEDBACK.md` sigue con
su única fila de plantilla vacía, sin ninguna entrada `nuevo`.

---

### Auditoría 2026-10-19 — sin hallazgos nuevos; cierra `#32` (el ciclo de PM del 2026-10-18 corrigió la cabecera de `SEGUIMIENTO.md`); R-32 (Oleada v20) sigue `PENDIENTE` sin ningún commit de código; R-33 (Oleada v21) especificada pero correctamente sin abrir en §1; `#24`/`#30` reconfirmados `ABIERTO`, ambos pendientes solo de respuesta del dueño

**Nota de arranque.** El contenedor arrancó con `HEAD` *detached* sobre un commit antiguo de
`develop` (`b62c0af`). `git checkout develop` encontró el clon local "diverged" frente a
`origin/develop` (50 commits distintos a cada lado — la rama remota se ha reescrito en algún punto
anterior del historial del proyecto, mismo síntoma ya normalizado por auditorías previas; el árbol
de trabajo estaba limpio, sin ningún cambio ni stash pendiente). Resuelto con `git reset --hard
origin/develop`, sin pérdida de trabajo real: no había ningún commit local propio de esta sesión.
`git status` limpio antes y después.

**Reinstalación de dependencias.** El `pip` pelado de este contenedor vuelve a resolver, igual que
documentan `#22`/`#28`, contra un intérprete distinto del real; `python3 -m pip install -r
requirements-dev.txt` (forma correcta ya documentada en `DEVELOPERS.md`/`SKILL.md`) instaló
`mypy==1.18.2`/`ruff==0.14.0`/`pytest==8.4.2` contra el intérprete real del proyecto (Python
3.11.17). Sin incidencia nueva.

**Verificación propia completa.** `python3 scripts/ci.py` da las cuatro redes en verde: `mypy` sin
hallazgos (72 archivos), `ruff` sin hallazgos, **696 tests** (sin cambio desde la auditoría
anterior — coincide con que el único commit desde entonces es de documentación, sin tocar
`scripts/`, `tests/` ni `assets/`) y las diecinueve etapas de `verificar_salidas.py --fixture` en
`OK`, incluida la auto-contención de `reproductor.html` y `guion-impresion.html`. Aviso textual ya
conocido y aceptado desde T-06 (desajuste Python 3.11 real vs. `>=3.12` declarado en
`pyproject.toml`), sin bloquear nada. `.pptx` y `.pdf` quedan `SalidaLatente` como es esperado
(skill de marca y Chrome/Edge ausentes en este contenedor); `concat_ffmpeg`/`comandos_montaje` se
omiten por falta de parte de rodaje — sin novedad frente a pasadas anteriores.

**Los seis invariantes, revisados directamente contra el código.** Sin ningún commit de código
desde la auditoría anterior, se repite la verificación punto por punto en vez de darla por buena:
(a) cobertura total intacta (`test_deteccion.py::test_cobertura_total_guiones_reales` sigue en
verde); (b) original recuperable + ediciones manuales intacto (`reescrituras.py`/`revalidacion.py`
sin cambios); (c) auto-contención: `grep` propio sobre `assets/reproductor/*` sin ninguna URL, CDN
ni `fetch` externo, y los 13 patrones de `PATRONES_RECURSO_EXTERNO` (`scripts/verificar_salidas.py`)
intactos línea a línea; (d) runtime solo stdlib: repetido el barrido de `import`/`from` de los 35
módulos de `scripts/*.py`, cero paquete de terceros, `pyproject.toml` sigue con `dependencies = []`
citando la regla §0.2; (e) configuración: `tests/test_skill_md.py` (4 passed) confirma de nuevo que
cada campo de `Configuracion` está documentado en `SKILL.md`; único número suelto en
`reproductor.py` sigue siendo la fórmula WCAG de luminancia, no un umbral de negocio; (f) contención
+ `.bak`: `grep -rln "copia_seguridad\s*=" scripts/*.py` sigue devolviendo exactamente los mismos
cuatro sitios (`documento_revision.py`, `entrada.py`, `feedback.py`, `instalar_skill.py`), sin
regresión del hallazgo `#23`. **Los seis invariantes se cumplen.**

**Único commit desde la auditoría anterior: un ciclo de PM, de documentación pura.**
`git log 7430595..HEAD` trae un solo commit, `4cc381b` ("PM: corrige hallazgo #32..."), que no toca
`scripts/`, `tests/`, `assets/`, `fixtures/` ni `references/` — confirmado con `git show --stat`:
solo `roadmap/DECISIONES_TECNICAS.md`, `roadmap/HISTORIAL_SESIONES.md`, `roadmap/ROADMAP_PRODUCTO.md`
y `roadmap/SEGUIMIENTO.md`.

**Hallazgo `#32` cerrado, verificado de forma independiente, no solo transcrito.** Leído el diff
completo de `4cc381b` sobre `roadmap/SEGUIMIENTO.md`: la cabecera pasa de "Última actualización:
2026-10-16" a "2026-10-18", con un bloque nuevo "Ciclo de Product Manager (2026-10-18)" que
documenta, con fecha real, que el ciclo anterior (`1b8fae3`, 2026-10-17) dejó este mismo documento
sin tocar — exactamente el defecto que describía esta fila, corregido con el mismo patrón ya usado
para cerrar `#29`/`#31` (reconocer la omisión con fecha real de la corrección, no fingir que nunca
pasó). `grep -n "2026-10-18" roadmap/SEGUIMIENTO.md` ya encuentra coincidencias. Se marca
`RESUELTO` en el registro.

**R-32 (Oleada v20, exportador `.pdf`) sigue `PENDIENTE`.** `git log -- scripts/pdf.py
scripts/salidas.py` desde `08a59de` (su apertura, 2026-10-16) sigue sin traer ningún commit nuevo:
cero código tocado en tres días. Correctamente no se ha abierto ninguna R-33 en §1 todavía (regla de
"nunca más de una R-XX pendiente de código a la vez").

**R-33 (Oleada v21) especificada por el PM — revisada de forma independiente, no solo transcrita.**
El ciclo de PM del 2026-10-18 especifica íntegra, pero sin abrir en §1, una nueva R-XX: mostrar la
sección auxiliar "Preparación antes de grabar" del guión como panel reabrible en el reproductor, hoy
reconocida solo para excluirla de la clasificación de escena y de las desviaciones de convención,
sin llegar nunca a ninguna salida real. Comprobada la premisa con grep propio, no solo citada: `grep
-rn "SeccionAuxiliar" scripts/*.py` confirma que la única sección auxiliar con consumidor real es
"Capítulos" (`capitulos_youtube.py::_seccion_capitulos`, por coincidencia de `titulo`); `grep -rn
"Preparaci\|preparacion_antes\|notas_produc" scripts/*.py assets/reproductor/*.js` no encuentra
ningún consumidor de "Preparación antes de grabar" ni de "Notas de producción" fuera de las menciones
de `config.py`/`parser.py` que solo sirven para no clasificarlas mal — la grieta descrita es real, no
hipotética. La decisión de **no abrirla todavía en §1** (queda lista para el ciclo que archive R-32,
o antes si el dueño prefiere adelantarla en paralelo) es coherente con el criterio ya consolidado
desde R-19 y está documentada con las alternativas descartadas en `DECISIONES_TECNICAS.md`. La ficha
en sí sigue el mismo formato que cualquier R-XX ya archivada (Migración/Depende de/Origen/Objetivo/
Requisitos/Criterio de aceptación), con alcance acotado explícito (no toca `tarjetas.json`, `.pdf`
ni la convención de marcado) y una regla dura de auto-contención repetida en su propio criterio de
aceptación. Sin ninguna objeción de esta auditoría.

**`#24` reconfirmado: sin desfase activo.** El mismo commit `4cc381b` que corrige `#32` reescribe
también la cabecera de `ROADMAP_PRODUCTO.md` con la decisión del día, sin que haya mediado ninguna
reconfirmación horaria del Programador entre medias — el mecanismo de autocorrección sigue
funcionando como siempre. Sigue `ABIERTO` solo porque la pregunta `#11` de `SEGUIMIENTO.md` §6 sigue
`(pendiente)` de respuesta del dueño.

**`#30` sin nueva repetición: sigue sin correr ningún ciclo de "Programador" desde la apertura de
R-32.** `git log` entre `08a59de` (2026-10-16) y `HEAD` solo trae auditoría y PM, en dos pasadas
sucesivas (2026-10-18 y esta). El hallazgo sigue `ABIERTO` (pregunta `#12` de §6 sigue `(pendiente)`
y el cron no se ha espaciado), sin que la circunstancia que dispara el patrón (reconfirmaciones
horarias ociosas) se haya vuelto a dar.

**Coherencia roadmap↔código y §7.** Revisada la única decisión técnica nueva (PM, 2026-10-18) contra
las reglas innegociables de `HOJA_DE_RUTA.md` §0.2: no implica ningún cambio de código, así que
ninguna regla aplica todavía (se verificará en R-33 cuando se implemente). `SEGUIMIENTO.md` §7 sin
ninguna desviación activa nueva: las siete filas existentes siguen siendo todas de 2026-08-31/09-02,
cerradas o incorporadas a la norma permanente. §3 (bloqueos) y §5 (P-XX) sin cambios.

**Verificación GitHub y `FEEDBACK.md`.** `list_issues`/`list_pull_requests` sobre
`JanoSolerDiaz/telePrompter` devuelven cero issues y cero PR abiertos. `roadmap/FEEDBACK.md` sigue
con su única fila de plantilla vacía, sin ninguna entrada `nuevo`.

---

### Auditoría 2026-10-18 — un hallazgo nuevo (`#32`, proceso/PM, baja): el ciclo de PM del 2026-10-17 (19:11, commit `1b8fae3`) no tocó `SEGUIMIENTO.md`, incumpliendo su propia regla de cierre de sesión (§0.4.1); R-32 (Oleada v20, exportador `.pdf`) sigue `PENDIENTE` sin ningún commit de código desde su apertura; `#24` reconfirmado sin desfase activo ahora mismo; `#30` sin ciclos de Programador que reconfirmar desde la apertura de R-32

**Nota de arranque.** El contenedor arrancó, igual que en pasadas anteriores, con `HEAD` *detached*
sobre un commit antiguo de `develop` (`b62c0af`). `git checkout develop` seguido de `git pull
origin develop` resolvió por **fast-forward limpio** hasta `1b8fae3` (49 commits), sin ninguna
divergencia que requiriera `git fetch --deepen`/`--unshallow` ni `reset --hard`. `git status`
limpio antes y después.

**Reinstalación de dependencias.** El `pip` pelado de este contenedor vuelve a resolver, igual que
advierten `#22`/`#28`, contra un intérprete distinto del real; `python3 -m pip install -r
requirements-dev.txt` (forma correcta ya documentada en `DEVELOPERS.md`/`SKILL.md`) instaló
`mypy==1.18.2`/`ruff==0.14.0`/`pytest==8.4.2` contra el intérprete real del proyecto (Python
3.11.17). Sin incidencia nueva: la nota de `#28`/P-06 sigue cubriendo exactamente este síntoma.

**Verificación propia completa.** `python3 scripts/ci.py` da las cuatro redes en verde: `mypy` sin
hallazgos (72 archivos), `ruff` sin hallazgos, **696 tests** (sin cambio desde la auditoría
anterior — coincide con que no ha corrido ningún ciclo de Programador ni de código desde R-31) y
las diecinueve etapas de `verificar_salidas.py --fixture` en `OK`, incluida la auto-contención de
`reproductor.html` y `guion-impresion.html` (ambos explícitamente confirmados "autocontenido" por
el propio validador). Aviso textual ya conocido y aceptado desde T-06 (desajuste Python 3.11 real
vs. `>=3.12` declarado en `pyproject.toml`), sin bloquear nada. Dos salidas quedan `SalidaLatente`
como es esperado (`.pptx` real por falta de la skill `480-branded-pptx` instalada en este
contenedor, `.pdf` por falta de Chrome/Edge) y dos etapas se omiten por falta de parte de rodaje —
mismo comportamiento que pasadas anteriores, sin novedad.

**Los seis invariantes, revisados directamente contra el código (no contra documentación vieja).**
(a) Cobertura total: `parser.py`/`clasificador.py` clasifican cada bloque sin ningún descarte
silencioso; test dedicado `test_deteccion.py::test_cobertura_total_guiones_reales` compara
`len(resultados) == len(bloques)` sobre guiones reales. (b) Original recuperable + ediciones
manuales: `reescrituras.py` conserva siempre `original` junto a `propuesta`
(`fusionar_con_estado`/`revertir_reescrituras` nunca lo borran); `revalidacion.py` relee
`guion-escenas.md` del disco y trata cualquier discrepancia frente al texto esperado como edición
manual autoritativa que nunca se sobrescribe, incluido el conflicto edición-manual-vs-partición ya
resuelto por P-02/P-03 (`#9`/`#14`). (c) Auto-contención: `assets/reproductor/*` sin ninguna URL,
CDN ni `fetch` externo (grep limpio); `verificar_salidas.py::verificar_autocontencion` cubre 13
patrones y corre tanto en `tests/test_reproductor.py` como en la cuarta red de `ci.py` — matiz ya
conocido y aceptado por diseño: la verificación es de tests/CI, no un chequeo bloqueante inline
dentro de `generar_reproductor_html`, porque la garantía real viene de que las plantillas nunca
referencian nada externo. (d) Runtime solo stdlib: ningún import de terceros en `scripts/*.py`;
`pyproject.toml` declara `dependencies = []` citando la regla §0.2 en el propio comentario. (e)
Configuración: `config.py` (~124 constantes) alimenta `Configuracion`, y
`test_skill_md.py::test_toda_clave_de_configuracion_esta_documentada_en_skill_md` (4 passed)
confirma mecánicamente que cada campo está en `SKILL.md`; los números "mágicos" que sí aparecen
sueltos en `reproductor.py` son la fórmula fija WCAG de luminancia relativa (255, 12.92, 2.4,
0.2126…), no un umbral de negocio. (f) Contención + `.bak`: `entrada.py::carpeta_salida_para`
valida con `.resolve().relative_to(...)` que toda escritura caiga dentro de la carpeta del guion;
los cuatro sitios que sobrescriben contenido único del dueño o de instalación
(`documento_revision.py`, `entrada.py`, `feedback.py`, `instalar_skill.py`) siguen aplicando la
copia `.bak`; las salidas puramente derivadas (reproductor, `.srt`, `.pdf`, `.pptx`, capítulos,
comandos de montaje, convención) no la llevan por política ya documentada y consistente (no son
contenido único ni se releen como entrada) — mismo criterio que ya cubría `convencion.py`, ahora
confirmado extendido sin excepción al resto de generadores. **Los seis invariantes se cumplen.**

**Coherencia roadmap↔código.** Revisadas las últimas decisiones técnicas (R-27 a R-32) contra las
reglas innegociables de `HOJA_DE_RUTA.md` §0.2: ninguna las incumple (cero red, cero dependencia
nueva, español, `encoding="utf-8"`, sin números mágicos, logger centralizado — R-32 existe
precisamente para reforzar esta última). `SEGUIMIENTO.md` §7 sin ninguna desviación activa nueva:
las siete filas existentes siguen siendo todas de 2026-08-31/09-02, cerradas o incorporadas a la
norma permanente.

**R-32 (Oleada v20, exportador `.pdf`) sigue `PENDIENTE`.** `git log -- scripts/pdf.py
scripts/salidas.py` desde `08a59de` (su apertura, 2026-10-16) no trae ningún commit nuevo: cero
código tocado. Correctamente no se ha abierto ninguna R-33 (regla de "nunca más de una R-XX
pendiente de código a la vez", explícita en el propio commit `1b8fae3`). Tampoco ha corrido ningún
ciclo de "Programador" desde la apertura de R-32 — solo el de auditoría (`7490d1b`) y el de PM
(`1b8fae3`), ambos el mismo día 2026-10-17.

**`#24` reconfirmado: sin desfase activo ahora mismo.** El propio ciclo de PM (`1b8fae3`) reescribió
la prosa de cabecera de `ROADMAP_PRODUCTO.md` ("Última actualización: 2026-10-17… R-32 sigue
PENDIENTE") al cerrar su ciclo, exactamente el patrón de autocorrección que el hallazgo describe.
Sigue `ABIERTO` en el registro porque la pregunta de gobernanza `#11` de `SEGUIMIENTO.md` §6 sigue
`(pendiente)` de respuesta del dueño y el mecanismo de fondo no ha cambiado — no porque haya
desfase hoy.

**`#30` sin poder reconfirmarse esta vez: no ha corrido ningún ciclo de Programador desde la
apertura de R-32.** El patrón de nueve reconfirmaciones horarias "sin novedad de código" se repitió
sin excepción en las cuatro oleadas anteriores (R-27 a R-30/R-31), pero desde que se abrió R-32
(2026-10-16 19:21) solo han corrido la auditoría y el PM — ninguna reconfirmación del Programador
todavía. El hallazgo sigue `ABIERTO` (la pregunta `#12` de §6 sigue `(pendiente)` y el cron no se ha
espaciado), pero esta pasada no puede añadir una repetición nueva del patrón porque no se ha dado
la circunstancia que lo dispara.

**Hallazgo nuevo `#32` (proceso / gobernanza del PM, baja): el ciclo de PM del 2026-10-17 (19:11,
commit `1b8fae3`) no actualizó `SEGUIMIENTO.md`.** Verificado de forma directa, no solo citado:
`git show --stat 1b8fae3` lista `DECISIONES_TECNICAS.md`, `HISTORIAL_SESIONES.md` y
`ROADMAP_PRODUCTO.md` como únicos archivos tocados — `roadmap/SEGUIMIENTO.md` no aparece. Efecto
observable: su cabecera sigue fechada "**Última actualización:** 2026-10-16" y `grep -n
"2026-10-17" roadmap/SEGUIMIENTO.md` no encuentra ninguna coincidencia en todo el archivo, pese a
que el propio ciclo de PM sí tomó una decisión real ese día (confirmar que R-32 sigue sin código,
decidir no abrir R-33, y corregir la prosa de `ROADMAP_PRODUCTO.md` para cerrar `#24`). Esto
incumple literalmente la regla de cierre de sesión §0.4.1 de `HOJA_DE_RUTA.md` ("Actualiza el
**estado** de la tarea en §1 de SEGUIMIENTO (y «última actualización» de la cabecera)"), que se
aplica a *cualquier* sesión que termine, no solo a las que cambian el estado de una tarea. El
riesgo real es de experiencia de uso más que de producto: `SEGUIMIENTO.md` se autodescribe como
"Hub / panel de control" y dice explícitamente "El dueño no revisa el código: revisa este
documento" — un dueño que solo abra `SEGUIMIENTO.md` hoy no vería ningún rastro de que hubo un
ciclo de PM la noche del 17, ni de la corrección de `#24`; tendría que ir a `HISTORIAL_SESIONES.md`
o al propio `git log` para enterarse, rompiendo la promesa de "un solo documento que consultar". No
se pierde ninguna información (recuperable en `HISTORIAL_SESIONES.md`/`git log`) ni se infringe
ningún invariante de producto — mismo perfil exacto que `#29` (fila de §1 faltante) y `#31` (fila
de `DECISIONES_TECNICAS.md` faltante), ambos puro proceso, autocorregidos por el propio PM en su
siguiente ciclo. Queda `ABIERTO`: es posterior al commit de la auditoría anterior (`7490d1b`), así
que ningún auditor lo había revisado hasta ahora, y ningún ciclo posterior lo ha corregido todavía.

**Verificación GitHub y `FEEDBACK.md`.** `list_issues`/`list_pull_requests` sobre
`JanoSolerDiaz/telePrompter` devuelven cero issues y cero PR abiertos. `roadmap/FEEDBACK.md` sigue
con su única fila de plantilla vacía, sin ninguna entrada `nuevo`.

---

### Auditoría 2026-10-17 — sin hallazgos nuevos; R-31 (Oleada v19) revisado de forma independiente y correcto; R-32 (Oleada v20) abierto por el PM el 2026-10-16, grieta de arquitectura en el exportador `.pdf` verificada de forma independiente y bien fundamentada, aún `PENDIENTE` de implementación; `#24` reconfirmado `ABIERTO` (decimocuarta repetición, con R-31); `#30` reconfirmado `ABIERTO`, coste vuelto a materializarse con las nueve reconfirmaciones ociosas del Programador tras R-31

**Nota de arranque.** El contenedor arrancó con `HEAD` *detached* sobre un commit antiguo de
`develop` (`b62c0af`, el mismo punto de partida que las dos pasadas anteriores). `git checkout
develop` seguido de `git pull origin develop` resolvió por **fast-forward limpio** hasta `08a59de`
(47 commits), sin ninguna divergencia que requiriera `git fetch --deepen`/`--unshallow` ni `reset
--hard`. `git status` limpio antes y después.

**Reinstalación de dependencias.** El `pip` pelado de este contenedor resuelve, igual que advierten
`#22`/`#28`, contra un intérprete distinto del real; `python3 -m pip install -r
requirements-dev.txt` (forma correcta ya documentada en `DEVELOPERS.md`/`SKILL.md`) instaló
`mypy==1.18.2`/`ruff==0.14.0`/`pytest==8.4.2` contra el intérprete real del proyecto (Python
3.11.17). Sin incidencia: la nota de `#28`/P-06 sigue cubriendo exactamente este síntoma.

**Verificación propia completa.** `python3 scripts/ci.py` da las cuatro redes en verde: `mypy` sin
hallazgos (72 archivos), `ruff` sin hallazgos, **696 tests** (`pytest`, 690→696 desde la auditoría
anterior, coincide con el commit de R-31) y las diecinueve etapas de `verificar_salidas.py
--fixture` en `OK`, incluida la auto-contención de `reproductor.html`/`guion-impresion.html`
(invariante de "un único `.html` sin dependencias, CDN ni acceso de red", patrones de
`PATRONES_RECURSO_EXTERNO` sin cambio desde R-09). Reverificado de forma puntual: los cuatro sitios
que aplican la copia `.bak` antes de sobrescribir (`documento_revision.py`, `entrada.py`,
`feedback.py`, `instalar_skill.py`, invariante (d)) siguen siendo exactamente esos cuatro;
`comandos_montaje.py` (R-30/R-31) sigue sin aplicarla — correcto, mismo trato que
`concat-ffmpeg.txt`/`capitulos-ffmpeg.txt`, documentos generados que el dueño no edita ni se
vuelven a leer como entrada; `roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin
ninguna entrada `nuevo`; `mcp__github__list_issues`/`list_pull_requests` sobre
`JanoSolerDiaz/telePrompter` devuelven cero issues y cero PR abiertos. `git diff --stat
96ea17a..08a59de -- scripts/ tests/ assets/ fixtures/ references/ pyproject.toml SKILL.md` confirma
que el único cambio de código desde la auditoría anterior es el commit de R-31 (`3cb5075`) —
ningún valor por defecto nuevo que verificar contra `SKILL.md`, ningún magic number introducido,
ningún riesgo nuevo para el validador de auto-contención.

**R-31 revisado de forma independiente, no solo transcrito del commit.** Leído el diff completo de
`3cb5075`: `calcular_comandos_montaje` gana `carpeta_salida: Path | None = None` que solo comprueba
EXISTENCIA en disco de `concat-ffmpeg.txt`, el `.srt` elegido (misma decisión real/alineado del
paso 2, reutilizada tal cual — no reimplementada) y, solo si el tercer paso está incluido,
`capitulos-ffmpeg.txt`; nunca relee contenido (eso ya lo hacen los validadores propios de R-21/R-28
en su propia ruta de generación). Confirmado leyendo `scripts/salidas.py::TODAS_LAS_SALIDAS`
(línea a línea, no solo el resumen del commit) que `COMANDOS_MONTAJE` es la octava y última opción
del selector, así que si el dueño selecciona también `CONCAT_FFMPEG`/`SRT`/`CAPITULOS_YOUTUBE` en
la misma pasada (`scripts/salidas.py:575`, bucle secuencial sobre `TODAS_LAS_SALIDAS`, cada
`_generar_*` escribe a disco de forma síncrona antes de la siguiente iteración), esos archivos ya
están en disco cuando le toca el turno — la premisa central del diseño es real, no asumida. Las
tres constantes de texto (`DESCRIPCION_OPCION_CONCAT_FFMPEG`/`_SRT`/`_CAPITULOS_YOUTUBE`) se
centralizan en `config.py` para que `comandos_montaje.py` y `salidas.py::DESCRIPCION_SALIDA` las
compartan sin crear un ciclo de imports (`salidas.py` ya importa de `comandos_montaje.py` desde
R-30, nunca al revés) — decisión razonada y correcta en `DECISIONES_TECNICAS.md`. Los 6 tests
nuevos cubren exactamente el criterio de aceptación: sin `carpeta_salida` no cambia nada
(compatibilidad hacia atrás), carpeta vacía avisa de los tres, sin sección `Capítulos` no avisa del
archivo de capítulos que nunca se referencia, con los tres ya en disco no avisa de nada (sin falso
positivo) y sin toma alineada el archivo que falta es el `.srt` estimado, no el alineado — más el
test de `test_salidas.py` que confirma que seleccionar las cuatro opciones a la vez no deja ninguna
nota de archivo faltante. `DEVELOPERS.md`/`contrato-montaje.md`/`SEGUIMIENTO.md`
`§1`/`DECISIONES_TECNICAS.md` actualizados de forma coherente entre sí. Implementación correcta,
mínima, sin ninguna objeción de esta auditoría.

**R-32 (apertura) revisado — grieta de arquitectura verificada de forma independiente, no solo
transcrita.** `git show 08a59de --stat` confirma que la apertura deja su fila en
`DECISIONES_TECNICAS.md` (patrón de `#31`, sin repetir ninguna premisa falsa). Comprobado con
`grep`/lectura directa, sin confiar en la cita del PM: `scripts/pdf.py` no importa `logger` ni
`monitorizacion` en ningún punto (confirmado, cero coincidencias); `convertir_html_a_pdf`
(`scripts/pdf.py:377-410`) nunca lanza una excepción y devuelve `(False, mensaje)` tanto si
Chrome/Edge no se encuentra (`OSError`/`TimeoutExpired` al intentar ejecutarlo) como si se
encuentra pero la conversión falla de verdad (código de salida distinto de cero, o el `.pdf` no
aparece en disco); `_generar_pdf` (`scripts/salidas.py:370-392`) clasifica ambos desenlaces por
igual como `SalidaLatente` en cuanto `resultado_pdf.ruta_pdf is None`, sin distinguir el motivo. El
propio docstring de `SalidaLatente` (línea 258-263) dice literalmente "el motivo es siempre la
falta de una dependencia externa, no un error del código" — una conversión que revienta con Chrome
sí detectado es exactamente lo contrario, y no deja ningún rastro en `teleprompter.log` ni
`diagnostico-<timestamp>.log` pese a que la infraestructura de R-24 ya existe para ese caso. La
grieta es real, no hipotética. La decisión de diseño elegida (opción c: `ResultadoPdf` gana
`chrome_detectado: bool`, y es `_generar_pdf` —no `pdf.py`— quien decide con ese dato si degrada a
`SalidaOmitida` con diagnóstico volcado o mantiene `SalidaLatente`) preserva intacto el contrato ya
documentado de T-28 ("`convertir_html_a_pdf` nunca lanza excepción") sin tocar `pdf.py` ni su
contrato, y reutiliza tal cual el patrón de diagnóstico de R-24 en la capa que ya lo alberga
(`salidas.py`) — razonada y coherente, sin objeción. Aún `PENDIENTE` de implementación.

**Coherencia roadmap↔código.** `ROADMAP_PRODUCTO.md` ("Oleada v20 — EN CURSO", R-32) y
`SEGUIMIENTO.md` §1 (`R-32 PENDIENTE`, única fila sin completar; `R-31 COMPLETADA`) coinciden
palabra por palabra en objetivo y estado. `§7` de `SEGUIMIENTO.md` sin ninguna desviación nueva
(las cinco filas existentes, todas de 2026-08-31/09-02, siguen siendo las únicas). `§6` sin
novedad: las preguntas `#11`/`#12` siguen `(pendiente)`. `§5` (P-XX) sin fila nueva.

**`#24` reconfirmado `ABIERTO`, decimocuarta repetición del patrón, con R-31.** La pregunta `#11`
sigue `(pendiente)`. Verificado con `git log --oneline 3cb5075..08a59de --
roadmap/ROADMAP_PRODUCTO.md`: el único commit que toca el archivo en todo el ciclo de R-31 es
`08a59de`, el propio archivo de PM — ninguna de las nueve reconfirmaciones horarias del Programador
(`0d01fcc` a `7fcbaab`, 2026-10-16) lo corrige. Fila del registro recondensada de nuevo en esta
pasada para mantenerla legible.

**`#30` reconfirmado `ABIERTO`, coste vuelto a materializarse con R-31.** La pregunta `#12` sigue
`(pendiente)`. Mismos `timestamp` reales de los commits que ya cita el registro: R-31 completada a
las 06:25 del 2026-10-16 (`3cb5075`); nueve reconfirmaciones horarias siguientes, `07:16` a `15:17`
(`0d01fcc`…`7fcbaab`), cada una repitiendo clon + `pip install` + las cuatro redes sin ningún
cambio de código que reportar; archivo de PM a las 19:21 (`08a59de`). Mismo patrón exacto que las
cuatro oleadas anteriores (R-27 a R-30). Fila del registro recondensada de nuevo en esta pasada
para mantenerla legible.

---

### Auditoría 2026-10-16 — sin hallazgos nuevos; `#31` cerrado por el propio PM (fila de apertura de R-30 añadida a `DECISIONES_TECNICAS.md`, sin repetir la premisa de "convención"); R-30 (Oleada v18, `comandos-montaje.md`) revisado de forma independiente y correcto; R-31 (Oleada v19) abierto por el PM el 2026-10-15, aún `PENDIENTE` de implementación; `#24` reconfirmado `ABIERTO` (decimotercera repetición, con R-30); `#30` reconfirmado `ABIERTO`, coste vuelto a materializarse con las nueve reconfirmaciones ociosas del Programador tras R-30

**Nota de arranque.** El contenedor arrancó con `HEAD` *detached* sobre un commit antiguo de
`develop` (`b62c0af`). `git checkout develop` seguido de `git pull origin develop` resolvió por
**fast-forward limpio** hasta `96ea17a` (35 commits), sin ninguna divergencia que requiriera
`git fetch --deepen`/`--unshallow` ni `reset --hard`. `git status` limpio antes y después.

**Reinstalación de dependencias.** El `pip` pelado de este contenedor resuelve, igual que
advierten `#22`/`#28`, contra un intérprete distinto del real; `python3 -m pip install -r
requirements-dev.txt` (forma correcta ya documentada en `DEVELOPERS.md`/`SKILL.md`) instaló
`mypy==1.18.2`/`ruff==0.14.0`/`pytest==8.4.2` contra el intérprete real del proyecto (Python
3.11.17). Sin incidencia: la nota de `#28`/P-06 sigue cubriendo exactamente este síntoma.

**Verificación propia completa.** `python3 scripts/ci.py` da las cuatro redes en verde: `mypy`
sin hallazgos (72 archivos), `ruff` sin hallazgos, **690 tests** (`pytest`, sin cambio desde
R-30) y las diecinueve etapas de `verificar_salidas.py --fixture` en `OK`, incluida la nueva
etapa de R-30 ("Generación de los comandos de montaje") y la auto-contención de
`reproductor.html`/`guion-impresion.html` (invariante de "un único `.html` sin dependencias, CDN
ni acceso de red" verificado con el validador real, patrones de `PATRONES_RECURSO_EXTERNO` sin
cambio desde R-09). Reverificado de forma puntual: los cuatro sitios que aplican la copia `.bak`
antes de sobrescribir (`documento_revision.py`, `entrada.py`, `feedback.py`,
`instalar_skill.py`, invariante (d)) siguen siendo exactamente esos cuatro;
`guardar_comandos_montaje` (nuevo en R-30) no aplica `.bak` — correcto, mismo trato que
`concat-ffmpeg.txt`/`capitulos-ffmpeg.txt`: es un documento generado por la skill, no un archivo
que el dueño edite y se vuelva a leer como entrada; `roadmap/FEEDBACK.md` sigue con su única fila
de plantilla vacía, sin ninguna entrada `nuevo`; `mcp__github__list_issues`/`list_pull_requests`
sobre `JanoSolerDiaz/telePrompter` devuelven cero issues y cero PR abiertos. `git diff --stat
87fc45e..96ea17a -- scripts/ tests/ assets/ fixtures/ references/ pyproject.toml SKILL.md`
confirma que el único cambio de código desde la auditoría anterior es el commit de R-30
(`2312795`) — ningún valor por defecto nuevo que verificar contra `SKILL.md`, ningún magic
number introducido, ningún riesgo nuevo para el validador de auto-contención.

**R-30 revisado de forma independiente, no solo transcrito del commit.** Leído el módulo completo
`scripts/comandos_montaje.py`: `calcular_comandos_montaje` reutiliza tal cual
`concat_ffmpeg.calcular_lista_concat_ffmpeg` (R-19), `srt_alineado.generar_srt_alineado` (R-05) y
`capitulos_youtube.generar_capitulos_youtube`/`formatear_capitulos_ffmpeg` (R-07/R-22) — nunca
relee del disco lo que otras salidas ya hayan escrito (confirmado: ninguna llamada a `Path.read*`
en el módulo), exactamente la decisión de diseño que motivó la apertura de R-31 más abajo. El
paso 1 (concatenación) decide si hay algo real que montar, reutilizando el propio
`motivo_sin_generar` de `concat_ffmpeg` en vez de una condición propia (decisión razonada en
`DECISIONES_TECNICAS.md`, verificada coherente: así `concat-ffmpeg.txt` y `comandos-montaje.md`
aparecen o desaparecen siempre juntos). Los tres sufijos de vídeo intermedios
(`comandos_montaje_sufijo_concatenado`/`_con_subtitulos`/`_final`) son campos de `Configuracion`
overridables, correctamente distinguidos de `NOMBRE_ARCHIVO_COMANDOS_MONTAJE` (no overridable,
mismo trato que el resto de `NOMBRE_ARCHIVO_*`) — ninguno es un número mágico suelto en el
código. `verificar_salidas.py` gana la etapa de "Generación" (no de "Validez", decisión razonada:
no hay contrato con una herramienta externa como ffmpeg que un validador propio pudiera
comprobar, mismo criterio que `CONVENCION_GUIONES`/R-25). Los 15 tests nuevos cubren el caso de
los tres pasos completos, la detención en subtítulos sin sección `Capítulos`, la ausencia total
sin parte de rodaje y la independencia de selección (el test que motiva la apertura de R-31).
Implementación correcta, mínima, coherente con la decisión razonada y sin ninguna objeción de
esta auditoría.

**`#31` cerrado — verificado, no solo transcrito.** Leído el diff completo de `96ea17a`: añade la
fila `PM (corrección del hallazgo #31...)` documentando con la fecha real de hoy la decisión de
apertura de R-30 que debió registrarse el 2026-10-14, razonando explícitamente por qué se añade
ahora en vez de dejarse ausente (evitar que una futura sesión cite la omisión como precedente
válido — el riesgo exacto que señalaba esta fila); y la fila `PM (apertura de R-31)`, que no
repite la premisa de "convención". Cierre completo. Fila del registro actualizada a `RESUELTO`
arriba.

**R-31 (apertura) revisado.** La spec (`ROADMAP_PRODUCTO.md`, Oleada v19: avisar en
`comandos-montaje.md` cuando el documento referencia un archivo —`concat-ffmpeg.txt`, el `.srt`
elegido, `capitulos-ffmpeg.txt`— que no existe todavía en la carpeta de salida real) está bien
fundamentada: cita una grieta verificada con un test ya existente de R-30
(`test_comandos_montaje_es_independiente_de_que_tambien_se_seleccione_concat_ffmpeg`), no
hipotética. La decisión de diseño elegida (comprobar en disco tras calcular los pasos y añadir
una nota visible por cada archivo ausente, sin bloquear ni forzar selección conjunta) preserva la
generación independiente de T-30 requisito 3, el pilar del selector desde su apertura. Sin
objeción. Aún `PENDIENTE` de implementación.

**Coherencia roadmap↔código.** `ROADMAP_PRODUCTO.md` ("Oleada v19 — EN CURSO", R-31) y
`SEGUIMIENTO.md` §1 (`R-31 PENDIENTE`, única fila sin completar; `R-30 COMPLETADA`) coinciden
palabra por palabra en objetivo y estado. `§7` de `SEGUIMIENTO.md` sin ninguna desviación nueva
(las cinco filas existentes, todas de 2026-08-31/09-02, siguen siendo las únicas). `§6` sin
novedad: las preguntas `#11`/`#12` siguen `(pendiente)`. `§5` (P-XX) sin fila nueva.

**`#24` reconfirmado `ABIERTO`, decimotercera repetición del patrón, con R-30.** La pregunta
`#11` sigue `(pendiente)`. Verificado con `git log --oneline 2312795..96ea17a --
roadmap/ROADMAP_PRODUCTO.md`: el único commit que toca el archivo en todo el ciclo de R-30 es
`96ea17a`, el propio archivo de PM — ninguna de las nueve reconfirmaciones horarias del
Programador (`20b3005` a `3f4894d`, 2026-10-15) lo corrige. Fila del registro recondensada de
nuevo en esta pasada (cuarta vez) para mantenerla legible.

**`#30` reconfirmado `ABIERTO`, coste vuelto a materializarse con R-30.** La pregunta `#12` sigue
`(pendiente)`. Mismos `timestamp` reales de los commits que ya cita el registro: R-30 completada
a las 06:29 del 2026-10-15 (`2312795`); nueve reconfirmaciones horarias siguientes, `07:15` a
`15:14` (`20b3005`…`3f4894d`), cada una repitiendo clon + `pip install` + las cuatro redes sin
ningún cambio de código que reportar; archivo de PM a las 19:17 (`96ea17a`). Mismo patrón exacto
que las tres oleadas anteriores (R-27, R-28, R-29). Fila del registro recondensada de nuevo en
esta pasada (quinta vez) para mantenerla legible.

---

### Auditoría 2026-10-15 — un hallazgo nuevo de proceso (`#31`, baja: apertura de R-30 sin fila en `DECISIONES_TECNICAS.md`, premisa de "convención" inexacta en `HISTORIAL_SESIONES.md`); R-29 (completado el 2026-10-14) revisado de forma independiente y correcto; R-30 (Oleada v18) abierto por el PM el 2026-10-14, aún `PENDIENTE` de implementación; `#24` reconfirmado `ABIERTO` (duodécima repetición, con R-29); `#30` reconfirmado `ABIERTO`, coste vuelto a materializarse con las nueve reconfirmaciones ociosas del Programador tras R-29

**Nota de arranque.** El contenedor arrancó con `HEAD` *detached* sobre un commit antiguo de
`develop` (`b62c0af`, el mismo punto de partida que la pasada anterior). `git checkout develop`
seguido de `git pull origin develop` resolvió por **fast-forward limpio** hasta `87fc45e` (23
commits), sin ninguna divergencia que requiriera `git fetch --deepen`/`--unshallow` ni `reset
--hard`. `git status` limpio antes y después.

**Reinstalación de dependencias.** El `pip` pelado de este contenedor resuelve, igual que
advierten `#22`/`#28`, contra un intérprete distinto del real (`pip --version` → Python 3.13);
`python3 -m pip install -r requirements-dev.txt` (forma correcta ya documentada en
`DEVELOPERS.md`/`SKILL.md`) instaló `mypy==1.18.2`/`ruff==0.14.0`/`pytest==8.4.2` contra el
intérprete real del proyecto (Python 3.11.17). Sin incidencia: la nota de `#28`/P-06 sigue
cubriendo exactamente este síntoma.

**Verificación propia completa.** `python3 scripts/ci.py` da las cuatro redes en verde: `mypy`
sin hallazgos (70 archivos), `ruff` sin hallazgos, **675 tests** (`pytest`, sin cambio desde
R-29) y las dieciocho etapas de `verificar_salidas.py --fixture` en `OK`, incluida la
auto-contención de `reproductor.html` y de `guion-impresion.html` (invariante de "un único
`.html` sin dependencias, CDN ni acceso de red" verificado con el validador real). Reverificado
de forma puntual: los cuatro sitios que aplican la copia `.bak` antes de sobrescribir
(`documento_revision.py`, `entrada.py`, `feedback.py`, `instalar_skill.py`, invariante (d))
siguen siendo exactamente esos cuatro; `roadmap/FEEDBACK.md` sigue con su única fila de
plantilla vacía, sin ninguna entrada `nuevo`; `mcp__github__list_issues`/`list_pull_requests`
sobre `JanoSolerDiaz/telePrompter` devuelven cero issues y cero PR abiertos. `git diff --stat
8fc4106..87fc45e -- scripts/ tests/ assets/ fixtures/ references/ pyproject.toml SKILL.md`
confirma que el único cambio de código desde la auditoría anterior es el commit de R-29
(`5fa5ac8`: `scripts/revalidacion.py` + `tests/test_revalidacion.py`) — ningún valor por defecto
nuevo que verificar contra `SKILL.md`, ningún magic number introducido, ningún riesgo nuevo para
el validador de auto-contención.

**R-29 revisado de forma independiente, no solo transcrito del commit.** Leído el diff completo
de `5fa5ac8`: `revalidacion._particion_aceptada_de` dejaba de reimplementar a mano las cuatro
condiciones de emparejamiento (`familia`/`decision`/`numero_escena`/`linea_inicio`/`linea_fin`/
igualdad de texto) y pasa a invocar `reescrituras.aplicar_particion_aceptada` sobre una lista de
un único bloque, leyendo la longitud del resultado (1 = no coincidió, 2 = las dos mitades) —
exactamente el refactor que especificaba la apertura de R-29 (`DECISIONES_TECNICAS.md`,
2026-10-13). La salvaguarda `indices_con_edicion_previa_a_particion`
(hallazgo `#9`/P-02/P-04) no se tocó: sigue decidiendo ANTES de llamar a `_particion_aceptada_de`
si procede buscar partición para ese bloque, confirmado leyendo `_materializar_marcados`/
`_indices_con_particion_pospuesta` línea a línea, no solo el resumen del commit. Los dos tests
nuevos (`test_materializacion_revalidacion_coincide_con_aplicar_particiones_*`) comparan bloque a
bloque la materialización de `revalidacion.py` contra una llamada directa a
`aplicar_particiones_aceptadas`, sobre los tres guiones reales (ninguno propone particiones hoy,
T-11 ya trocea sin dejar frases candidatas) y sobre dos guiones sintéticos con particiones de
verdad (`_GUION`, `_GUION_ESCENA_DOS_PARTICIONES`, dos particiones en la misma escena) — cubren
el caso que la ficha de apertura pedía investigar, sin dejar sin ejercitar la coincidencia real.
`SEPARADOR_MITADES`/`FAMILIA_PARTICION_RESPIRACION`/`DECISION_ACEPTADA` dejan de importarse en
`revalidacion.py` por no usarse ya ahí, confirmado con `grep -n` sobre el archivo. Los 20 tests
ya existentes de `test_revalidacion.py`, incluidos los dos que fijan el hallazgo `#9`
(`test_edicion_manual_y_particion_aceptada_misma_pasada_no_pierde_edicion`,
`test_revalidacion_posterior_al_conflicto_no_duplica_bloques`), siguen pasando sin ningún cambio
de comportamiento. Implementación correcta, mínima, coherente con la decisión razonada de
`DECISIONES_TECNICAS.md` (entrada 2026-10-14) y sin ninguna objeción de esta auditoría.

**R-30 (apertura) revisado — y un hallazgo nuevo de proceso, `#31`.** La spec de R-30
(`ROADMAP_PRODUCTO.md`, Oleada v18: `comandos-montaje.md`, encadenar concat→subtítulos→capítulos
con nombres de archivo reales) está bien acotada y razonada — alcance explícito de "documento,
no script ejecutado por la skill" (coherente con §0.2: cero red, runtime solo biblioteca
estándar), decisiones de diseño ya cerradas (subtítulos como pista blanda por defecto, cada paso
opcional sin romper el encadenado) y criterio de aceptación verificable. Sin objeción al
contenido de la spec en sí. Lo que sí es nuevo: `git show 87fc45e --stat` confirma que el commit
que la abre **no toca `roadmap/DECISIONES_TECNICAS.md`** — la primera vez desde R-21 que una
apertura de R-XX no deja fila propia ahí (`grep -n "apertura de R-" roadmap/DECISIONES_TECNICAS.md`
localiza las nueve anteriores, R-21 a R-29, sin hueco). La narrativa de la propia sesión
(`HISTORIAL_SESIONES.md`, sesión 161) lo explica con una frase que no resiste el contraste con el
propio registro: *"sin decisiones técnicas nuevas... ya documentada en `ROADMAP_PRODUCTO.md` como
es convención"* — la convención real, observable en las nueve aperturas anteriores sin ninguna
excepción, es la contraria. Registrado como hallazgo `#31` (baja, detalle completo en el
registro de arriba); mismo patrón de fondo que `#26` (ya cerrado), una afirmación de
"convención"/"instrucción" que no se sostiene al comprobarla, esta vez sin corregir todavía.

**Coherencia roadmap↔código.** `ROADMAP_PRODUCTO.md` ("Oleada v18 — EN CURSO", R-30) y
`SEGUIMIENTO.md` §1 (`R-30 PENDIENTE`, única fila sin completar; `R-29 COMPLETADA`) coinciden
palabra por palabra en objetivo y estado. `§7` de `SEGUIMIENTO.md` sin ninguna desviación nueva
(las cinco filas existentes, todas de 2026-08-31/09-02, siguen siendo las únicas). `§6` sin
novedad: las preguntas `#11`/`#12` siguen `(pendiente)`. `§5` (P-XX) sin fila nueva.

**`#24` reconfirmado `ABIERTO`, duodécima repetición del patrón, con R-29.** La pregunta `#11`
sigue `(pendiente)`. Verificado con `git log --oneline de1ec03..87fc45e -- roadmap/ROADMAP_PRODUCTO.md`:
el único commit que toca el archivo en todo el ciclo de R-29 es `87fc45e`, el propio archivo de
PM — ninguna de las nueve reconfirmaciones horarias del Programador (`c425efe` a `9edb4d3`,
2026-10-14) lo corrige, así que `ROADMAP_PRODUCTO.md` mantuvo "Oleada v17 — EN CURSO"/R-29
`PENDIENTE` pese a que el código ya estaba completo desde las 06:20, hasta que el ciclo de PM de
la tarde lo corrigió en el mismo commit que archivó la oleada — duodécima repetición, siempre
autocorregida el mismo día. Fila del registro recondensada de nuevo en esta pasada (cuarta vez)
para mantenerla legible.

**`#30` reconfirmado `ABIERTO`, coste vuelto a materializarse con R-29.** La pregunta `#12` sigue
`(pendiente)`. Mismos `timestamp` reales de los commits que ya cita el registro: R-29 completada
a las 06:20 del 2026-10-14 (`5fa5ac8`); nueve reconfirmaciones horarias siguientes, `07:15` a
`15:15` (`c425efe`…`9edb4d3`), cada una repitiendo clon + `pip install` + las cuatro redes sin
ningún cambio de código que reportar; archivo de PM a las 19:16 (`87fc45e`). Mismo patrón exacto
que R-27/R-28, sin materializar coste nuevo de arquitectura, solo de cómputo — reconfirma que
ninguno de los dos remedios propuestos se ha aplicado todavía.

### Auditoría 2026-10-14 — cero hallazgos nuevos; único cambio de código desde la pasada anterior es R-28 (completado el 2026-10-13, revisado de forma independiente y correcto); R-29 (Oleada v17) abierto por el PM el 2026-10-13, verificado de forma independiente y aún `PENDIENTE` de implementación; `#24` reconfirmado `ABIERTO` (undécima repetición del patrón, con R-28); `#30` reconfirmado `ABIERTO`, coste vuelto a materializarse con las nueve reconfirmaciones ociosas del Programador tras R-28

**Nota de arranque.** El contenedor arrancó con `HEAD` *detached*. `git checkout develop` dejó la
rama local apuntando a un commit antiguo (`b62c0af`, el cierre de la auditoría anterior, once
commits por detrás de `origin/develop`); a diferencia de varias pasadas recientes, `git pull origin
develop` resolvió esta vez con un **fast-forward limpio** hasta `de1ec03`, sin ninguna divergencia
que requiriera `git reset --hard` — no se reproduce en esta sesión el artefacto de clon superficial
que sí afectó a las dos auditorías anteriores (documentado en su día como hallazgo `#21`, descartado).
`git status` limpio antes y después.

**Reinstalación de dependencias.** `pip install -r requirements-dev.txt` (sin `python3 -m` por
delante) instaló correctamente `mypy==1.18.2`/`ruff==0.14.0`/`pytest==8.4.2` contra el intérprete real
del proyecto (`/usr/local/lib/python3.13/dist-packages`) — no se reprodujo esta vez el síntoma de
`#28`/P-06 (el contenedor de esta sesión resuelve `pip` correctamente sin el rodeo). Sí se confirma
una variante ya conocida de `#22`/R-15: el `PATH` antepone un segundo juego de los mismos binarios
(`/root/.local/bin`, instalado vía `uv tool`, `pytest 9.1.1`) al que instala `pip`; invocar `pytest`
a secas corre esa versión en vez de la pineada. Sin impacto real — `scripts/ci.py` invoca siempre
`sys.executable -m <herramienta>`, nunca el binario pelado, y la suite completa (673 tests) pasa igual
de verde con cualquiera de los dos binarios — así que no se registra como hallazgo nuevo: es la misma
causa raíz que `#22`/R-15 ya documenta y cierra (la nota de `DEVELOPERS.md`/`SKILL.md` ya advierte de
usar siempre `python scripts/ci.py`, no el binario suelto), solo con una variante de gestor de paquetes
(`uv` en vez de otro `pip`) que no cambia la recomendación ni el riesgo.

**Verificación propia completa, no solo lectura de la narrativa ajena.** `python scripts/ci.py` da las
cuatro redes en verde: `mypy` sin hallazgos (34 archivos), `ruff` sin hallazgos, **673 tests** (`pytest`,
sin cambio desde el commit de R-28, coincide con el recuento que cita su propio mensaje) y las
dieciocho etapas de `verificar_salidas.py --fixture` en `OK`, incluida la auto-contención de
`reproductor.html` y de `guion-impresion.html` (`verificar_autocontencion`, invariante de "un único
`.html` sin dependencias, CDN ni acceso de red" verificado con el validador real, no solo asumido).
Reverificados también, de forma puntual e independiente: los cuatro sitios que aplican la copia `.bak`
antes de sobrescribir (`documento_revision.py`, `entrada.py`, `feedback.py`, `instalar_skill.py`,
invariante (d)) siguen siendo exactamente esos cuatro (`grep -rln "copia_seguridad\s*=" scripts/*.py`);
`.gitignore` sigue versionando `assets/`/`fixtures/` completos (P-01) y solo ignorando lo generado;
`roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin ninguna entrada `nuevo`.
`git diff --stat b62c0af..de1ec03 -- scripts/ tests/ assets/ fixtures/ references/ pyproject.toml
SKILL.md` confirma que el único cambio de código desde la auditoría anterior es el commit de R-28
(`b990a1c`): ni `scripts/config.py` ni `assets/reproductor/` se tocaron, así que no hay ningún valor
por defecto nuevo que verificar contra `SKILL.md` ni ningún riesgo nuevo para el validador de
auto-contención.

**R-28 revisado de forma independiente, no solo transcrito del commit.** Leído el diff completo de
`b990a1c`: `pptx.py` gana `TarjetasInvalidasError` y `exportar_pptx` llama a `validar_tarjetas` sobre
los datos ya construidos antes de `guardar_tarjetas_json`, lanzando la excepción (capturada por el
`try`/`except` genérico de `salidas.py` ya existente desde R-24) sin escribir ni `tarjetas.json` ni el
brief si el contenido es inválido. `salidas.py::_generar_srt` pasa a devolver `(generadas, omitidas)` y
valida `guion.srt`/`guion-alineado.srt` por separado con `validar_srt`, degradando solo la mitad
inválida a `SalidaOmitida` sin impedir que la otra se genere — verificado leyendo el `for`/`if` completo,
no solo la firma de la función. `_generar_capitulos_youtube` gana la misma validación para
`capitulos-youtube.txt` con `validar_capitulos_youtube`, junto a la de `capitulos-ffmpeg.txt` que ya
existía desde R-22. El llamador en `generar_salidas_seleccionadas` se actualiza para desempaquetar la
nueva tupla de `_generar_srt` sin perder ninguna rama existente (confirmado leyendo las líneas
modificadas, no solo el resumen del diff). 4 tests nuevos (669→673) cubren los tres casos nuevos; cero
cambio en las reglas de los propios validadores ni en `concat_ffmpeg.py`/`validar_capitulos_ffmpeg`
(ya conectados desde R-21/R-22). Sin ningún magic number nuevo introducido; `DEVELOPERS.md` gana
sección propia (confirmado con `git show --stat`). Implementación correcta, coherente con el patrón ya
sentado por R-21/R-22 y sin ninguna objeción de esta auditoría.

**R-29 verificado de forma independiente, no solo leído de `DECISIONES_TECNICAS.md`.** La apertura
afirma que `revalidacion.py::_particion_aceptada_de`/`_materializar_marcados` reimplementan en privado
el mismo emparejamiento bloque↔reescritura que `reescrituras.py::aplicar_particion_aceptada`/
`aplicar_particiones_aceptadas` ya exponen en público. Confirmado leyendo ambos pares de funciones
línea a línea: `reescrituras.py:322-355` compara `reescritura.familia`/`decision`/`numero_escena`/
`linea_inicio`/`linea_fin`/igualdad de texto para decidir si un bloque coincide con la partición
aceptada y lo sustituye por sus dos mitades; `revalidacion.py:190-243` repite exactamente las mismas
cuatro condiciones de emparejamiento a mano, con su propio bucle, para el mismo propósito — sin llamar
nunca a las funciones públicas. `grep -rn "aplicar_particion" scripts/ tests/` confirma que
`aplicar_particion_aceptada`/`aplicar_particiones_aceptadas` no tienen ningún llamador real fuera de
`tests/test_reescrituras.py`: la grieta de arquitectura es real, no una lectura superficial del
docstring de intención (`reescrituras.py:61-63`, citado por la ficha) que el código no respaldara. La
spec de `ROADMAP_PRODUCTO.md` (Oleada v17) pide investigar primero la equivalencia completa —incluida
la salvaguarda `indices_con_edicion_previa_a_particion` del hallazgo `#9`/P-02/P-04, que hoy solo vive
en `revalidacion.py` y que la función pública no contempla— antes de unificar o corregir, en vez de
prescribir directamente la refactorización; criterio razonado y prudente dado que el área ya causó dos
incidencias de severidad alta en este mismo proyecto. Apertura legítima y bien fundamentada, aún
`PENDIENTE`, sin ningún ciclo de Programador que la haya tocado todavía.

**Coherencia roadmap↔código.** `ROADMAP_PRODUCTO.md` ("Oleada v17 — EN CURSO", R-29) y
`SEGUIMIENTO.md` §1 (`R-29 PENDIENTE`, única fila sin completar; `R-28 COMPLETADA`) coinciden palabra
por palabra en objetivo y estado. `DECISIONES_TECNICAS.md` sigue append-only; sus entradas de R-28
(convención de propagación del fallo: excepción para `tarjetas.json`, `SalidaOmitida` a mano para
`.srt`/capítulos, razonada por dónde vive ya cada validación) y de apertura de R-29 están razonadas y
no contradicen ninguna decisión vigente de §0.2. `§7` de `SEGUIMIENTO.md` sin ninguna desviación
nueva (las cinco filas existentes, todas de 2026-08-31/09-02, siguen siendo las únicas). `§6` sin
novedad: las preguntas `#11`/`#12` siguen `(pendiente)`.

**`#24` reconfirmado `ABIERTO`, undécima repetición del patrón, con R-28.** La pregunta `#11` de
`SEGUIMIENTO.md` §6 sigue `(pendiente)`. Verificado con `git log --oneline -- roadmap/ROADMAP_PRODUCTO.md`:
entre la apertura de R-28 (`93839f7`) y su archivo (`de1ec03`) el archivo no lo toca ningún otro commit
— en particular, ninguna de las nueve reconfirmaciones horarias del Programador (`8279e8a` a `371e523`,
2026-10-13) lo corrige, así que `ROADMAP_PRODUCTO.md` mantuvo "Oleada v16 — EN CURSO"/R-28 `PENDIENTE`
pese a que el código ya estaba completo desde las 06:21, hasta que el ciclo de PM de la tarde lo
corrigió en el mismo commit que archivó la oleada — undécima repetición, siempre autocorregida el
mismo día. Fila del registro recondensada de nuevo en esta pasada (tercera vez) para mantenerla legible.

**`#30` reconfirmado `ABIERTO`, coste vuelto a materializarse con R-28.** Mismo escenario exacto que
motivó el hallazgo: R-28 se completó a las 06:21 del 2026-10-13 y las nueve reconfirmaciones horarias
siguientes (`07:17` a `15:15`, verificado con los `timestamp` reales de los commits) repitieron el
protocolo completo de verificación sin ningún cambio de código que reportar, hasta el ciclo de PM de
la tarde (`de1ec03`, 19:18). Sigue `ABIERTO` porque ninguno de los dos remedios propuestos (espaciar el
cron, o añadir una comprobación de "cola vacía" al protocolo) se ha aplicado todavía — ambas decisiones
reservadas al dueño. Fila recondensada en esta pasada para legibilidad tras cuatro repeticiones de
historial día a día.

**Conclusión de esta pasada.** Cero hallazgos `ABIERTO` nuevos. El único cambio de código desde la
pasada anterior (R-28) se revisó de forma independiente y es correcto, sin violar ningún invariante de
§0.2 y sin introducir ningún magic number. R-29 es una apertura legítima y bien fundamentada del PM,
verificada de forma independiente por esta auditoría, aún sin implementar — y de un tipo distinto a
las diez aperturas anteriores (no una pieza huérfana, sino una pieza pública construida para
reutilizarse que la ruta real ignora, en el área exacta de dos incidencias de severidad alta ya
cerradas). Los dos únicos `ABIERTO` del registro (`#24`, `#30`) siguen siendo de proceso/gobernanza
puro, ambos ya enrutados como pregunta formal en `SEGUIMIENTO.md` §6 (`#11`, `#12`) a falta solo de la
respuesta del dueño, sin ningún coste de producto ni riesgo de código. Cuatro redes en verde, 673
tests, las cuatro invariantes de datos (a)-(d) más los invariantes de aislamiento/auto-contención/
runtime de §0.2 vigentes sin regresión, roadmap y seguimiento coherentes entre sí y con el código. Sin
ninguna acción propia sobre `scripts/`, `tests/`, `assets/` ni ningún documento salvo este.

---

### Auditoría 2026-10-13 — cero hallazgos nuevos; único cambio de código desde la pasada anterior es R-27 (completado el 2026-10-12, revisado de forma independiente y correcto); R-28 (Oleada v16) abierto por el PM el 2026-10-12, verificado de forma independiente y aún `PENDIENTE` de implementación; `#24` reconfirmado `ABIERTO` (veintisiete pasadas, décima repetición del patrón, fila recondensada por segunda vez); `#30` reconfirmado `ABIERTO`, coste vuelto a materializarse con las nueve reconfirmaciones ociosas del Programador tras R-27

**Nota de arranque.** El contenedor arrancó con `HEAD` *detached*. `git checkout develop` dejó la
rama local en `cc0ac86` (residuo de un contenedor anterior, cincuenta commits por detrás); `git pull
origin develop` encontró divergencia real entre ese ref y `origin/develop` (traído ya en `93839f7`),
sin ancestro común visible bajo el clon superficial por defecto (`git rev-parse
--is-shallow-repository` → `true`) — mismo artefacto del `git clone --depth` de cada contenedor
efímero ya diagnosticado en profundidad por el hallazgo `#21` y repetido por todas las auditorías
recientes. `git status` estaba limpio (nada propio que perder), así que se resolvió con `git reset
--hard origin/develop`, confirmando una vez más que `origin/develop` es la fuente autoritativa. Quedó
en `93839f7` (ciclo de PM del 2026-10-12: archiva Oleada v15/R-27 y abre R-28).

**Reinstalación de dependencias.** `pip install -r requirements-dev.txt` pelado del preámbulo
reprodujo una vez más, intacto, el síntoma de `#28`/P-06 (instala `mypy`/`ruff`/`pytest` contra el
intérprete equivocado del contenedor), corregido reinstalando con `python3 -m pip install -r
requirements-dev.txt` tal como documentan ya `DEVELOPERS.md`/`SKILL.md`. No se registra como hallazgo
nuevo — misma causa raíz que `#28`/P-06 ya cierra, repetida porque el contenedor no cambia entre
sesiones.

**Verificación propia completa, no solo lectura de la narrativa ajena.** Tras la reinstalación
correcta, `python scripts/ci.py` da las cuatro redes en verde: `mypy`/`ruff` sin hallazgos, **669
tests** (`pytest`, +4 desde la auditoría anterior, coincide con el recuento que cita el commit de
R-27) y las dieciocho etapas de `verificar_salidas.py --fixture` en `OK`, incluida la
auto-contención de `reproductor.html` y de `guion-impresion.html`. Reverificados también, de forma
puntual e independiente: los cuatro sitios que aplican la copia `.bak` antes de sobrescribir
(`documento_revision.py`, `entrada.py`, `feedback.py`, `instalar_skill.py`, invariante (d)) siguen
siendo exactamente esos cuatro; `.github/workflows/ci.yml` sigue con `workflow_dispatch` como único
disparador, inactivo a propósito (T-04); el aviso de versión de Python (`avisar_si_version_python_diverge`,
R-08/`#12`) sigue llamado desde `ci.main()`. `git diff --stat 9506ef5..93839f7 --
scripts/ tests/ assets/ fixtures/ references/ pyproject.toml SKILL.md` confirma que el único cambio
de código desde la auditoría anterior es el commit de R-27 (`9324938`): ningún archivo de
`scripts/config.py` ni de `assets/reproductor/` se tocó, así que no hay ningún valor por defecto
nuevo que verificar contra `SKILL.md` ni ningún riesgo nuevo para el validador de auto-contención.

**R-27 revisado de forma independiente, no solo transcrito del commit.** Leído el diff completo de
`9324938`: `scripts/estado.py::actualizar_info_guion` refresca `hash_sha256`/`tamano_bytes` mutando
`estado` en el sitio (mismo tratamiento que `guardar_estado`, razonado en `DECISIONES_TECNICAS.md`);
`documento_revision.generar_documento_revision` gana `guion_modificado: bool = False`, que añade el
aviso visible en la cabecera del resumen global solo con `True`. Al buscar los llamadores reales con
`grep -rn` en `scripts/*.py` no aparece ninguno fuera de `estado.py`/`documento_revision.py` mismos —
**no es una grieta igual a la que motivó R-26/R-27/R-28**, porque este proyecto es una *skill* sin
script orquestador único en `scripts/` (no existe ningún `main.py` que encadene parseo → tiempos →
documento → estado): la "ruta real" de invocación es la secuencia que `SKILL.md` documenta para que
la sesión que ejecuta la skill la seguida paso a paso. Verificado leyendo `SKILL.md:116-125`: el
fragmento de código documenta exactamente `avisar_si_guion_modificado` → `generar_documento_revision(...,
guion_modificado=...)` → `actualizar_info_guion` → `guardar_estado`, en ese orden — el mismo patrón ya
usado por R-26 para el diccionario del dueño. El bucle queda cerrado de verdad, no solo documentado:
4 tests nuevos (`test_estado.py`, `test_documento_revision.py`) cubren el refresco del hash y que el
aviso no vuelve a repetirse tras `actualizar_info_guion`. Sin ningún magic number nuevo introducido.

**R-28 verificado de forma independiente, no solo leído de `DECISIONES_TECNICAS.md`.** Reproducido el
`grep -rn` que cita el PM sobre `pptx.validar_tarjetas`, `srt.validar_srt` y
`capitulos_youtube.validar_capitulos_youtube`: los tres solo tienen llamadores en sus propios tests y
en `verificar_salidas.py --fixture` (líneas 410/631/645/660). Confirmado leyendo `scripts/salidas.py`
línea a línea que `_generar_srt` (295-317), `_generar_pptx` (345-368) y la mitad "YouTube" de
`_generar_capitulos_youtube` (371-411, a diferencia de su mitad "ffmpeg" que sí valida desde R-22)
escriben a disco sin pasar por el validador correspondiente — exactamente la misma forma de grieta que
R-21 y R-22 ya cerraron para sus gemelos (`concat-ffmpeg.txt`, `capitulos-ffmpeg.txt`), con cita de
línea verificada de forma propia, no solo tomada del commit del PM. `DECISIONES_TECNICAS.md` registra
además, de forma verificable, los candidatos descartados por el agente Explore que localizó la grieta
(`verificar_autocontencion`, `calibracion.calcular_calibracion`, `convencion.medir_consistencia_senales`/
`proponer_convenciones`) con motivo propio para cada descarte. Spec completa en `ROADMAP_PRODUCTO.md`
(Oleada v16); aún `PENDIENTE`, sin ningún ciclo de Programador que la haya tocado todavía — apertura
legítima y bien fundamentada, sin ninguna objeción de esta auditoría.

**Coherencia roadmap↔código.** `ROADMAP_PRODUCTO.md` ("Oleada v16 — EN CURSO", R-28) y
`SEGUIMIENTO.md` §1 (`R-28 PENDIENTE`, única fila sin completar) coinciden palabra por palabra en
objetivo y estado. `DECISIONES_TECNICAS.md` sigue append-only; sus entradas de R-27 (mutación en el
sitio, posición del aviso) y de apertura de R-28 están razonadas y no contradicen ninguna decisión
vigente de §0.2. `DEVELOPERS.md` gana sección propia para R-27 (confirmado con `git show --stat`).
`§7` de `SEGUIMIENTO.md` sin ninguna desviación nueva. `roadmap/FEEDBACK.md` sigue con su única fila
de plantilla vacía, sin ninguna entrada `nuevo`.

**`#24` reconfirmado `ABIERTO`, veintisiete pasadas, décima repetición del patrón.** La pregunta `#11`
de `SEGUIMIENTO.md` §6 sigue `(pendiente)`. Verificado leyendo los commits de las nueve
reconfirmaciones horarias del Programador tras R-27 (`789a343` a `842255a`, 2026-10-12): las nueve
mantienen `ROADMAP_PRODUCTO.md` en "Oleada v15 — EN CURSO" pese a que el código de R-27 ya estaba
completo desde las 06:19, corregido recién por el PM en el mismo commit (`75b318b`) que archivó la
oleada por la tarde — décima repetición del patrón, siempre autocorregido el mismo día. Fila del
registro recondensada en esta pasada (ya lo había sido el 2026-10-01) para mantenerla legible tras
nueve repeticiones más de historial día a día.

**`#30` reconfirmado `ABIERTO`, coste vuelto a materializarse.** Mismo escenario exacto que motivó el
hallazgo: R-27 se completó a las 06:19 del 2026-10-12 y las nueve reconfirmaciones horarias
siguientes (07:15 a 15:15) repitieron el protocolo completo de verificación sin ningún cambio de
código que reportar, hasta el ciclo de PM de la tarde. Sigue `ABIERTO` porque ninguno de los dos
remedios propuestos (espaciar el cron, o añadir una comprobación de "cola vacía" al protocolo) se ha
aplicado todavía — ambas decisiones reservadas al dueño.

**Conclusión de esta pasada.** Cero hallazgos `ABIERTO` nuevos. El único cambio de código desde la
pasada anterior (R-27) se revisó de forma independiente y es correcto, sin violar ningún invariante
de §0.2 y sin introducir ningún magic number. R-28 es una apertura legítima y bien fundamentada del
PM, verificada de forma independiente por esta auditoría, aún sin implementar. Los dos únicos
`ABIERTO` del registro (`#24`, `#30`) siguen siendo de proceso/gobernanza puro, ambos ya enrutados
como pregunta formal en `SEGUIMIENTO.md` §6 (`#11`, `#12`) a falta solo de la respuesta del dueño, sin
ningún coste de producto ni riesgo de código. Cuatro redes en verde, 669 tests, las seis invariantes
de §0.2 vigentes sin regresión, roadmap y seguimiento coherentes entre sí y con el código. Sin ninguna
acción propia sobre `scripts/`, `tests/`, `assets/` ni ningún documento salvo este.

---

### Auditoría 2026-10-12 — cero hallazgos nuevos; cero cambios de código desde la pasada anterior (único ciclo intermedio es de PM, sin tocar `scripts/`/`tests/`/`assets/`, cayó en fin de semana sin disparo de la rutina «Programador»); `#24` reconfirmado `ABIERTO` (veintiséis pasadas, patrón sin ocasión de repetirse ni romperse); `#30` reconfirmado `ABIERTO`, sin coste nuevo desde el enrutado; R-27 sigue `PENDIENTE` sin ningún ciclo de Programador que la haya tocado

**Nota de arranque.** El contenedor arrancó con `HEAD` *detached*; la rama local `develop` cacheada
(`cc0ac86`, residuo de un contenedor anterior) quedó muy por detrás de `origin/develop`, que el
`fetch` trajo ya en `9506ef5` — mismo síntoma estructural ya descrito por las dos auditorías previas
(artefacto del `git clone`/`fetch` de cada contenedor efímero frente a un `origin/develop` que ha
seguido avanzando, no una reescritura real de historia; investigado en profundidad en su día como
hallazgo `#21`, descartado). `git checkout develop` dejó la rama local en `cc0ac86`; `git pull origin
develop` encontró divergencia real entre ese ref local y el remoto recién traído (50/50 commits a
cada lado, sin ancestro común reciente) y pidió resolución manual. Resuelto con `git status` limpio
(nada propio que perder) seguido de `git reset --hard origin/develop`, confirmando una vez más que
`origin/develop` es la
fuente autoritativa. Quedó en `9506ef5` (ciclo de PM del 2026-10-11, sin apertura de R-XX).

**Reinstalación de dependencias.** `pip install -r requirements-dev.txt` pelado del preámbulo
reprodujo una vez más, intacto, el síntoma de `#28`/P-06: instaló `mypy`/`ruff`/`pytest` contra el
intérprete equivocado del contenedor (confirmado por el `ModuleNotFoundError` de las tres
herramientas al primer `python scripts/ci.py`), corregido reinstalando con `python3 -m pip install
-r requirements-dev.txt` tal como documentan ya `DEVELOPERS.md`/`SKILL.md`. No se registra como
hallazgo nuevo — es exactamente la causa raíz que `#28`/P-06 ya cierra y documenta, repetida porque
el contenedor no cambia entre sesiones, no porque la documentación esté incompleta.

**Verificación propia completa, no solo lectura de la narrativa ajena:** tras la reinstalación
correcta, `python scripts/ci.py` da las cuatro redes en verde: `mypy`/`ruff` sin hallazgos, **665
tests** (`pytest`, sin cambio desde la auditoría anterior) y las dieciocho etapas de
`verificar_salidas.py --fixture` en `OK`, incluida la auto-contención del reproductor
(`reproductor.html`) y del HTML de impresión (`guion-impresion.html`) — el invariante de "un único
`.html` sin dependencias, CDN ni acceso de red" sigue verificado con el validador real, no solo
asumido. Reverificados también, de forma puntual e independiente: los cuatro sitios que aplican la
copia `.bak` antes de sobrescribir (`documento_revision.py`, `entrada.py`, `feedback.py`,
`instalar_skill.py`, invariante (d)) siguen siendo exactamente esos cuatro, sin ninguno nuevo ni
ninguno perdido (`grep -rln "copia_seguridad\s*=" scripts/*.py`); el flujo de GitHub Actions
(`.github/workflows/ci.yml`) sigue con `workflow_dispatch` como único disparador, inactivo a
propósito (T-04).

**Cero cambios de código desde la pasada anterior.** `git diff --stat 48ae5f1..9506ef5 --
scripts/ tests/ assets/ fixtures/ references/ pyproject.toml SKILL.md` no devuelve nada: el único
commit entre la auditoría del 2026-10-11 y esta pasada es un ciclo de PM (`9506ef5`), que solo toca
`roadmap/SEGUIMIENTO.md` y `roadmap/HISTORIAL_SESIONES.md` para dejar constancia de un reescaneo
propio (de solo lectura) de funciones públicas huérfanas que reconfirma a R-27 como la grieta
correcta, sin abrir ninguna R-XX nueva. Consecuencia directa: las seis invariantes de §0.2 no han
tenido ocasión de romperse, y `HOJA_DE_RUTA.md` sigue sin tocarse desde `791ec07` (2026-10-06,
R-23), coherente con su condición de documento inmutable. `DECISIONES_TECNICAS.md` tampoco cambió en
este ciclo (es un ciclo de PM sin decisión de producto/arquitectura nueva que registrar, confirmado
en el propio diff de `9506ef5`).

**`#24` reconfirmado `ABIERTO`, veintiséis pasadas consecutivas.** La pregunta `#11` de
`SEGUIMIENTO.md` §6 sigue `(pendiente)`. Sin ningún commit de Programador desde la pasada anterior
(el único ciclo intermedio es de PM, sin apertura de R-XX, y cae en fin de semana — la rutina
«Programador» solo dispara de lunes a viernes, §3 bloqueo #8), el patrón de prosa desactualizada no
tuvo ocasión de repetirse ni de romperse esta vez — verificado que `ROADMAP_PRODUCTO.md` sigue en
"Oleada v15 — EN CURSO"/R-27 `PENDIENTE`, coherente con `SEGUIMIENTO.md` §1. Detalle completo en el
registro de arriba.

**`#30` reconfirmado `ABIERTO`, sin coste nuevo.** Mismo razonamiento que `#24`: sin ningún disparo
de la rutina «Programador» desde el enrutado de la pregunta `#12` (fin de semana), no hay ninguna
reconfirmación horaria ociosa nueva que sumar al conteo que motivó el hallazgo. Sigue `ABIERTO`
porque ninguno de los dos remedios propuestos (espaciar el cron, o añadir una comprobación de "cola
vacía" al protocolo) se ha aplicado todavía — ambas decisiones reservadas al dueño.

**Coherencia roadmap↔código.** `ROADMAP_PRODUCTO.md` ("Oleada v15 — EN CURSO", R-27) y
`SEGUIMIENTO.md` §1 (`R-27 PENDIENTE`, única fila sin completar) coinciden palabra por palabra en
objetivo y estado. `DECISIONES_TECNICAS.md` sigue append-only (sin cambios en este ciclo); su
historial no contradice ninguna decisión vigente de §0.2. `DEVELOPERS.md` sigue describiendo la
estructura real del repositorio (sin cambios desde la pasada anterior). `§7` de `SEGUIMIENTO.md` sin
ninguna desviación nueva. `roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin
ninguna entrada `nuevo`.

**Conclusión de esta pasada.** Cero hallazgos `ABIERTO` nuevos. Los dos únicos `ABIERTO` del registro
(`#24`, `#30`) son de proceso/gobernanza puro, ambos ya enrutados como pregunta formal en
`SEGUIMIENTO.md` §6 (`#11`, `#12`) a falta solo de la respuesta del dueño, sin ningún coste de
producto ni riesgo de código. Cuatro redes en verde, las seis invariantes de §0.2 vigentes sin
regresión (por ausencia total de cambio de código, no solo por verificación repetida), roadmap y
seguimiento coherentes entre sí y con el código. Sin ninguna acción propia sobre `scripts/`, `tests/`,
`assets/` ni ningún documento salvo este.

---

### Auditoría 2026-10-11 — cero hallazgos nuevos; cero cambios de código desde la pasada anterior (único ciclo intermedio es de PM, sin tocar `scripts/`/`tests/`/`assets/`); `#24` reconfirmado `ABIERTO` (veinticinco pasadas, patrón sin ocasión de repetirse ni romperse); `#30` reconfirmado `ABIERTO`, ahora formalmente enrutado como pregunta `#12` de `SEGUIMIENTO.md` §6; R-27 sigue `PENDIENTE` sin ningún ciclo de Programador que la haya tocado

**Nota de arranque.** El contenedor arrancó con `HEAD` *detached*, 50 commits por detrás de
`origin/develop` (residuo de un contenedor anterior, mismo síntoma ya descrito por auditorías
previas). `git checkout develop` dejó la rama local atrás; `git pull origin develop` encontró el
historial de `origin` reescrito respecto al ref local cacheado (actualización forzada
`cc0ac86...845e2d9`, 50/50 commits a cada lado) y pidió resolución manual. Resuelto con `git status`
limpio (nada propio que perder) seguido de `git reset --hard origin/develop`, confirmando que
`origin/develop` es la fuente autoritativa — sin indicio de pérdida de trabajo, solo de una
reescritura de historia aguas arriba que esta auditoría no investiga más (no es su alcance). Quedó en
`845e2d9` (ciclo de PM del 2026-10-10 que enruta `#30` como pregunta `#12`).

`pip install -r requirements-dev.txt` pelado del preámbulo reprodujo una vez más el síntoma intacto
de `#28`/P-06: instaló contra **Python 3.13** (`ruff` resuelto en **0.16.8**, no en el `0.14.0`
pineado) en vez del intérprete real **3.11.17**, y con él `mypy`/`ruff` en rojo por `ModuleNotFoundError`
hasta reinstalar con `python3 -m pip install -r requirements-dev.txt`. Detalle nuevo frente a lo ya
documentado: el ruff "pelado" no solo corre contra el intérprete equivocado, también resuelve una
**versión distinta a la pineada** (0.16.8 frente a 0.14.0), con una regla nueva en esa versión
(`UP042`, sugiere `enum.StrEnum` en vez de `class TipoSalida(str, Enum)` de `scripts/salidas.py:125`)
que no existe en 0.14.0 y que por tanto nunca se dispara con la instalación correcta — reproducido y
confirmado: `python3 -m ruff check scripts/ tests/` (intérprete e instalación correctos) da
`All checks passed!`, cero hallazgos. **No se registra como hallazgo nuevo**: es el mismo síntoma de
raíz que `#28`/P-06 ya cierra y documenta (`SKILL.md` líneas 614-622, "nunca el binario pelado... tampoco
el `pip` pelado al instalar"), con un síntoma secundario (versión de paquete distinta, no solo
intérprete distinto) que es consecuencia directa de la misma causa ya cubierta, no una grieta nueva —
anotado aquí para que una pasada futura no lo redescubra desde cero.

**Verificación propia completa, no solo lectura de la narrativa ajena:** `python scripts/ci.py`
(con la instalación correcta): `mypy`/`ruff` en verde sin hallazgos (70 archivos), **665 tests**
(`pytest`, sin cambio desde R-26) en verde, dieciocho etapas `OK` en `verificar_salidas.py --fixture`
(incluida la auto-contención del reproductor y del HTML de impresión). Las cuatro redes en verde.

**Cero cambios de código desde la pasada anterior.** `git diff --stat fd34455..845e2d9 -- scripts/
tests/ assets/ fixtures/` no devuelve nada: el único commit entre la auditoría del 2026-10-10 y esta
pasada es el ciclo de PM (`845e2d9`), que solo toca `roadmap/DECISIONES_TECNICAS.md`,
`roadmap/HISTORIAL_SESIONES.md` y `roadmap/SEGUIMIENTO.md`. Consecuencia directa: las seis invariantes
de §0.2, verificadas de forma exhaustiva y con AST propio en la pasada del 2026-10-10, siguen
vigentes sin necesidad de repetir ese barrido completo — no hay una sola línea de `scripts/`, `tests/`
ni `assets/` que pudiera haberlas roto. Confirmado igualmente que `HOJA_DE_RUTA.md` sigue sin tocarse
desde `791ec07` (2026-10-06, R-23), coherente con su condición de documento inmutable (§7 de
`SEGUIMIENTO.md`).

**`#24` reconfirmado `ABIERTO`, veinticinco pasadas consecutivas.** La pregunta `#11` de
`SEGUIMIENTO.md` §6 sigue `(pendiente)`. Sin ningún commit de Programador desde la pasada anterior
(el único ciclo intermedio es de PM, sin apertura de R-XX), el patrón de prosa desactualizada no tuvo
ocasión de repetirse ni de romperse esta vez — verificado que `ROADMAP_PRODUCTO.md` sigue en
"Oleada v15 — EN CURSO"/R-27 `PENDIENTE`, coherente con `SEGUIMIENTO.md` §1. Detalle completo en el
registro de arriba.

**`#30` reconfirmado `ABIERTO`, ahora formalmente enrutado.** El ciclo de PM del 2026-10-10
(`845e2d9`) incorporó el hallazgo de la pasada anterior como pregunta de gobernanza `#12` de
`SEGUIMIENTO.md` §6, con el razonamiento completo en `DECISIONES_TECNICAS.md` (verificado leyendo el
diff íntegro, no solo la ficha de `SEGUIMIENTO.md`): ninguno de los dos remedios que proponía el
propio hallazgo —espaciar el cron, o añadir una comprobación de "cola vacía" al protocolo— es
ejecutable por el PM o el Programador sin decisión del dueño, mismo tratamiento que ya recibió `#24`.
El hallazgo sigue `ABIERTO` porque el coste de fondo (reconfirmaciones horarias que repiten las cuatro
redes sin tarea pendiente) no se ha corregido todavía, solo se ha formalizado la pregunta. Nota de
esta misma pasada, sin coste propio: entre el enrutado (2026-10-10 19:12) y esta auditoría
(2026-10-11 03:07) no se ha disparado ninguna reconfirmación horaria del Programador —coherente con
el patrón ya observado de que el cron corre durante la jornada (~07:15 a ~15:15) y no de madrugada—,
así que esta pasada no suma ninguna sesión ociosa nueva al conteo que motivó el hallazgo.

**Coherencia roadmap↔código.** `ROADMAP_PRODUCTO.md` ("Oleada v15 — EN CURSO", R-27) y
`SEGUIMIENTO.md` §1 (`R-27 PENDIENTE`, única fila sin completar) coinciden palabra por palabra en
objetivo y estado. `DECISIONES_TECNICAS.md` sigue append-only (`git diff fd34455..845e2d9 --
roadmap/DECISIONES_TECNICAS.md` solo añade una línea, no quita ninguna); su entrada de esta pasada de
PM (enrutado de `#30`) es coherente con lo implementado: no hay ninguna decisión que debiera subir a
§0.2 y no lo haya hecho. `DEVELOPERS.md` sigue describiendo la estructura real del repositorio (sin
cambios desde la pasada anterior). `§7` de `SEGUIMIENTO.md` sin ninguna desviación nueva.
`roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin ninguna entrada `nuevo`.

**Conclusión de esta pasada.** Cero hallazgos `ABIERTO` nuevos. Los dos únicos `ABIERTO` del registro
(`#24`, `#30`) son de proceso/gobernanza puro, ambos ya enrutados como pregunta formal en
`SEGUIMIENTO.md` §6 (`#11`, `#12`) a falta solo de la respuesta del dueño, sin ningún coste de
producto ni riesgo de código. Cuatro redes en verde, las seis invariantes de §0.2 vigentes sin
regresión (por ausencia total de cambio de código, no solo por verificación repetida), roadmap y
seguimiento coherentes entre sí y con el código. Sin ninguna acción propia sobre `scripts/`, `tests/`,
`assets/` ni ningún documento salvo este.

---

### Auditoría 2026-10-10 — un hallazgo nuevo (`#30`, media, cadencia de la rutina Programador frente al ritmo real de trabajo pendiente); R-26 implementada y verificada con código; R-27 abierta sin implementar, premisa de arquitectura confirmada de forma independiente; `#24` reconfirmado `ABIERTO` (veinticuatro pasadas, octava y novena repetición del patrón, con R-25 y R-26, ambas autocorregidas el mismo día de archivo)

**Nota de arranque.** `git checkout develop && git pull origin develop` trajo el repositorio hasta
`4cfa236` en fast-forward limpio (49 commits por detrás del `HEAD` que tenía este clon antes del
`checkout` — resto de un contenedor anterior, todos ya fusionados en `develop`, nada perdido).
`python3 -m pip install -r requirements-dev.txt` instaló sin incidencia contra el intérprete correcto
(Python 3.11.17); el `pip` pelado del preámbulo sí reinstaló contra Python 3.13 como de costumbre
(síntoma intacto de `#28`/P-06, ya cubierto por la documentación, no reabierto).

**Verificación propia completa, no solo lectura de la narrativa ajena:** `python scripts/ci.py`:
`mypy`/`ruff` en verde sin hallazgos (70 archivos), **665 tests** (`pytest`, sin cambio desde R-26) en
verde, dieciocho etapas `OK` en `verificar_salidas.py --fixture` (incluida la auto-contención del
reproductor y del HTML de impresión). Las cuatro redes en verde.

**Las seis invariantes de §0.2, reverificadas contra el código vigente, no solo contra la narrativa
de pasadas anteriores** (encargado a una verificación independiente dedicada, con AST propio sobre
los 25 módulos de `scripts/*.py` en vez de repetir un `grep` ya hecho):
- **(a) Cobertura total** — PASS. `clasificador.py`/`troceo.py` releídos enteros: todo bloque se
  reparte en `BloqueClasificado` (locución/no locución/`TIPO_REVISAR` de respaldo, nunca descartado),
  `reconstruir()` es el invariante de ida y vuelta documentado; el único `continue` de `troceo.py`
  (línea 430, salta bloques no-locución para la fragmentación en bloques de respiración) no pierde
  esos bloques del resultado global porque `clasificar_escena` ya los conserva por separado para
  `guion-escenas.md`/`tarjetas.json`.
- **(b) Original recuperable / edición manual manda** — PASS. Los tests de regresión de `#9`/`#14`/
  `#19` (`test_edicion_manual_y_particion_aceptada_misma_pasada_no_pierde_edicion`,
  `test_disposicion_pospuesta_corrompida_con_mismo_tamano_no_pierde_ni_duplica_contenido`) siguen en
  el suite y en verde; `revalidar_guion` (línea 433 de `revalidacion.py`) solo gana parámetros nuevos
  de R-26 (`diccionario`/`carpeta_salida`) delante de la tubería de marcado/fusión ya existente, sin
  tocar la lógica de identidad de anclas que protege este invariante.
- **(c) Reproductor autocontenido** — PASS. `PATRONES_RECURSO_EXTERNO` de `scripts/verificar_salidas.py`
  sigue cubriendo los trece patrones fijados por `#13`/R-09; `assets/reproductor/` no tiene ningún
  commit desde `cc0ac86` (anterior a esta pasada), y un barrido propio de `guion.js`/`plantilla.html`
  no encuentra ningún `fetch`, `import()`, `importScripts`, `ServiceWorker`, `Worker`,
  `BroadcastChannel`, `postMessage` ni `<link rel="preload">` que abriera un vector nuevo no cubierto.
- **(d) Runtime solo biblioteca estándar** — PASS. AST de los 25 módulos de `scripts/*.py`: el único
  import no stdlib resuelto es `from migraciones import ...` (`scripts/estado.py:26`), paquete propio
  del proyecto (`scripts/migraciones/`), no de terceros. `pyproject.toml` sigue con `dependencies = []`
  explícito.
- **(e) Sin números mágicos** — PASS, con una nota sin severidad propia. Todos los valores de
  configuración muestreados (`palabras_por_bloque_min/max`, `ppm_respaldo`, `pausa_coma_segundos`,
  `umbral_desviacion_tiempos`, `calibracion_guiones_minimos/palabras_minimas`) viven en
  `Configuracion` y están documentados por su nombre en la tabla de defectos de `SKILL.md`. Única
  excepción localizada: `scripts/reproductor.py:67-86` (`_luminancia_relativa`/`contraste_relativo`)
  tiene inline las constantes de la fórmula WCAG de luminancia relativa (`0.2126`, `0.7152`, `0.0722`,
  `12.92`, `0.03928`, `0.055`, `2.4`) y el umbral AAA `7.0` (citado en el docstring, afirmado solo en
  `tests/test_reproductor.py:304`, no en ninguna puerta de `scripts/ci.py`). **No se registra como
  hallazgo**: son constantes de un estándar externo fijo (W3C WCAG), no un valor de producto que el
  dueño pudiera querer ajustar — mismo tipo de exención, razonada aquí por primera vez de forma
  explícita, que ya aplicó `#13` a `<object data="data:...">`. Queda anotado para que una pasada futura
  no lo redescubra desde cero.
- **(f) Sin borrado destructivo / aislamiento por carpeta de salida** — PASS. `grep -rln
  "copia_seguridad\s*=" scripts/*.py` sigue devolviendo exactamente los cuatro sitios de `#23`
  (`documento_revision.py`, `entrada.py`, `feedback.py`, `instalar_skill.py`), los cuatro con copia
  `.bak`/`.bak-<marca>` antes de sobrescribir. Revisados también, uno a uno, el resto de
  `write_text`/`write_bytes` de `scripts/*.py` (capítulos, concat, convención, estado, monitorización,
  pdf, pptx, reproductor, srt): todos escriben dentro de `carpeta_salida / NOMBRE_ARCHIVO_*`. El único
  punto que escribe fuera de la carpeta de salida del guión es `instalar_skill.py`, que instala el
  propio paquete de la skill (no una salida del guión) — fuera de alcance de este invariante por
  naturaleza, y aun así con copia de respaldo previa.

**R-26 verificada con código, no solo con la ficha de `SEGUIMIENTO.md`.** Leído el diff completo de
`cdafa5b` (13 tests nuevos, 652→665): `revalidar_guion` (`revalidacion.py:433-458`) gana
`diccionario`/`carpeta_salida` opcionales — el explícito gana siempre sobre el cargado desde disco,
verificado con `test_revalidar_guion_diccionario_explicito_gana_sobre_carpeta_salida`;
`generar_documento_revision` (`documento_revision.py`) cuenta las `Reescritura` de
`familia == FAMILIA_DICCIONARIO` ya presentes (no relee el archivo para el recuento normal, solo para
el aviso de inconsistencia cuando hay entradas en disco y cero aplicadas — decisión razonada en
`DECISIONES_TECNICAS.md`, verificada leyendo el código, no solo la justificación escrita); el mismo
recuento llega tal cual a `tarjetas.json.metadatos.entradas_diccionario_aplicadas` vía
`pptx.generar_tarjetas`/`exportar_pptx`. Confirmado también el límite conocido y documentado: el
selector automático de `salidas.py` (T-30) no construye `reescrituras` por su cuenta, así que
`tarjetas.json` generado por esa vía sigue mostrando `entradas_diccionario_aplicadas: 0` salvo que
quien orquesta la skill lo pase explícitamente — mismo patrón ya aceptado para `tomas_por_escena`/R-13
y `--para-terceros`, no una omisión nueva. `SKILL.md` (líneas 53-68) documenta el paso obligatorio con
el fragmento de código exacto. Cierra de verdad la grieta de arquitectura que motivó la tarea: el
diccionario del dueño ahora tiene un camino real de carga en el flujo documentado, con aviso explícito
si se olvida.

**R-27 (Oleada v15) verificada de forma independiente, no solo leída.** Mismo criterio de apertura que
R-12 a R-26: `grep -rn "guion_modificado" scripts/*.py` solo encuentra la propia definición de
`avisar_si_guion_modificado`/`guion_modificado` (`estado.py:192-205`) y su llamada interna entre sí,
ningún llamador real; `grep -n "guion_modificado" SKILL.md` no da ningún resultado — ni siquiera está
como paso de la receta documentada. Segundo defecto confirmado leyendo `estado.py`: `InfoGuion` solo
se construye de nuevo (con hash/tamaño frescos) en `estado_inicial` (línea 126); la otra aparición
(`desde_dict`, línea 108) reconstruye desde lo ya guardado, no lo actualiza — así que un wiring
ingenuo repetiría el aviso para siempre tras el primer cambio real del guion, en vez de una sola vez.
Spec completa y acotada en `ROADMAP_PRODUCTO.md` (Oleada v15), con la candidata alternativa
(`ejecutar_con_limite_de_tiempo`, T-06) correctamente descartada por menor severidad (defensa en
profundidad sin incidente en §4, frente a una señal de transparencia que el dueño notaría
directamente) — razonamiento coherente con el propio principio de producto nº 1
("nada se descarta en silencio").

**Hallazgo nuevo `#30` (media, proceso/coste de cómputo).** La rutina "Programador" dispara con cron
horario durante toda la jornada; en cuanto la R-XX del día se implementa temprano (`cdafa5b`, 06:26 el
2026-10-09), las nueve reconfirmaciones horarias siguientes (07:15 a 15:15, verificado con los
`timestamp` reales de los commits) no tienen ninguna tarea pendiente y aun así repiten el protocolo
completo — `git pull`, `pip install`, las cuatro redes enteras — solo para commitear "sin novedad de
código". Mismo patrón confirmado tras R-25 el día anterior (nueve reconfirmaciones más). No es un
síntoma oculto: el propio ciclo de Programador lo señaló explícitamente dos veces seguidas en sus
propias notas de `SEGUIMIENTO.md` ("la cadencia de disparo de esta rutina programada frente al ritmo
real de trabajo pendiente sigue mereciendo una revisión del dueño"), sin que ninguna pasada de
auditoría lo hubiera convertido todavía en hallazgo registrado ni en pregunta formal de §6. Detalle y
recomendación completos en el registro de arriba. Severidad `media` (no por riesgo de producto —
ninguno: la verificación siempre da en verde y no hay escritura fuera de protocolo — sino por el coste
real y acumulado de sesiones de nube completas gastadas en commits que no cambian una sola línea).

**Coherencia roadmap↔código.** `ROADMAP_PRODUCTO.md` ("Se abre R-27", Oleada v15) y `SEGUIMIENTO.md`
§1 (`R-27 PENDIENTE`, única fila sin completar) coinciden palabra por palabra en objetivo y estado.
`DECISIONES_TECNICAS.md` sigue append-only; sus entradas de R-26 (dos decisiones de diseño razonadas:
contar la familia en vez de releer el archivo, pasar el entero ya calculado a `pptx.py` en vez de que
recalculara) y la de apertura de R-27 (con el barrido completo de los cinco candidatos huérfanos y por
qué se descartaron cuatro) son coherentes con lo implementado, sin ninguna que debiera subir a §0.2 y
no lo haya hecho. `DEVELOPERS.md` sigue describiendo la estructura real del repositorio. `§7` de
`SEGUIMIENTO.md` sin ninguna desviación nueva desde la última pasada. `roadmap/FEEDBACK.md` sigue con
su única fila de plantilla vacía — el bloqueo #7 de §3 (grabar un curso completo) sigue sin resolverse,
sin acción posible desde una sesión de nube.

**Conclusión de esta pasada.** Cero hallazgos `ABIERTO` nuevos de código o arquitectura; el único
hallazgo nuevo (`#30`) es de proceso/coste, sin riesgo de producto, con una recomendación concreta para
el dueño. `#24` sigue siendo el único `ABIERTO` de proceso puro, ahora en su vigésimo cuarta pasada
consecutiva esperando la misma respuesta de gobernanza. Cuatro redes en verde, las seis invariantes de
§0.2 reverificadas sin regresión, roadmap y seguimiento coherentes entre sí y con el código, y una
R-XX nueva (R-27) bien razonada y correctamente acotada, lista para su implementación. Sin ninguna
acción propia sobre `scripts/`, `tests/`, `assets/` ni ningún documento salvo este.

---

### Auditoría 2026-10-09 — cero hallazgos nuevos; `#29` cerrado `RESUELTO` (verificado: §1 ya trae fila propia para R-25 y R-26); R-25 implementada y verificada con código (séptima auditoría de este año que puede marcar tanto el código como el seguimiento en verde el mismo día); R-26 abierta sin implementar, premisa técnica verificada de forma independiente; `#24` reconfirmado `ABIERTO` (veintitrés pasadas, sin repetición del patrón esta vez)

**Nota de arranque.** `git checkout develop && git pull origin develop` trajo el repositorio hasta
`7e803f2` en fast-forward limpio (37 commits por detrás del `HEAD` que tenía este clon antes del
`checkout`, todos ya fusionados en `develop` — nada perdido, solo un *detached HEAD* residual de un
contenedor anterior). `python3 -m pip install -r requirements-dev.txt` instaló sin incidencia contra
el intérprete correcto (Python 3.11.17, mismo síntoma de `#28`/P-06 no reproducido esta vez).

**Verificación propia completa, no solo lectura de la narrativa ajena:**
- `python scripts/ci.py`: `mypy`/`ruff` en verde sin hallazgos (70 archivos), 652 tests (`pytest`,
  sin cambio desde R-25) en verde, dieciocho etapas `OK` en `verificar_salidas.py --fixture`
  (incluida la auto-contención del reproductor y del HTML de impresión). Las cuatro redes en verde,
  tal y como narran las nueve reconfirmaciones del Programador del 2026-10-08 — reproducido aquí de
  forma independiente, no solo transcrito.
- **Invariante «runtime solo biblioteca estándar» reverificada con script propio** (no repetición de
  un `grep` anterior): recorrido AST de los 25 módulos de `scripts/*.py` que separa imports de
  biblioteca estándar de imports de módulos propios del proyecto — cero import de tercero. Confirma
  de nuevo que `mypy`/`ruff`/`pytest` (los únicos paquetes de `requirements-dev.txt`) siguen fuera
  del runtime real.
- **Invariante «sin borrado destructivo» (d)** reverificada: `grep -rln "copia_seguridad\s*=" scripts/*.py`
  sigue devolviendo exactamente los cuatro sitios que `#23` dejó documentados
  (`documento_revision.py`, `entrada.py`, `feedback.py`, `instalar_skill.py`); `convencion.py` sigue
  sin aplicar `.bak` por el mismo motivo ya razonado (genera un documento para pegar en plantilla, no
  un archivo del dueño que se relea como entrada) — sin regresión.
- **Validador de auto-contención**: `PATRONES_RECURSO_EXTERNO` en `scripts/verificar_salidas.py`
  sigue con los trece patrones fijados por `#13`/R-09 (URLs, CDN, `@import`, `fetch`,
  `XMLHttpRequest`, `src=` externo, `<object>`, `<embed src>`, `<base href>`, `WebSocket`,
  `EventSource`/`sendBeacon`, `url(...)` de CSS), sin ningún hueco nuevo detectado en el código
  tocado desde la última pasada (ninguno: no hubo commit de Programador entre el 2026-10-08 y hoy).

**`#29` cerrado `RESUELTO` (verificado, no solo transcrito).** La fila de este registro recomendaba
añadir `R-25` a §1 de `SEGUIMIENTO.md` en el próximo ciclo que lo tocara. El propio commit de PM que
archivó la Oleada v13 y abrió R-26 (`7e803f2`, 2026-10-08) lo hizo en el mismo movimiento: `grep -n
"^| R-2[4-6]" roadmap/SEGUIMIENTO.md` sobre el `HEAD` actual trae tres filas, `R-24 COMPLETADA`,
`R-25 COMPLETADA` y `R-26 PENDIENTE`, cada una con su fecha. Sin hueco. Detalle de la corrección en
el registro de arriba.

**R-26 (Oleada v14) verificada de forma independiente, no solo leída.** El PM abrió R-26 (sin
intervención del auditor: es una grieta de arquitectura que el propio PM detectó leyendo código línea
a línea, mismo criterio que abrió R-12 a R-25) sobre la afirmación de que `diccionario-locucion.json`
(T-13, "el diccionario del dueño manda siempre") no tiene ningún camino real de carga en producción.
Reproducido en esta pasada con los mismos `grep` que cita la ficha, más una comprobación que la ficha
no hace explícita: `scripts/revalidacion.py::revalidar_guion` (línea 437) **sí** expone un parámetro
`diccionario: dict[str, str] | None = None` y lo propaga a `normalizar_guion` (línea 458) — la
tubería interna entre funciones ya existe y es correcta; la grieta real está exactamente donde dice
la ficha: no hay ningún llamador, dentro o fuera de los tests, que construya ese diccionario
invocando `cargar_diccionario_locucion(carpeta_salida)` y se lo pase a `revalidar_guion` o a
`generar_documento_revision` sobre un guion real — confirmado también que `SKILL.md` documenta la
prioridad del diccionario (línea 38, "el diccionario del dueño manda siempre sobre cualquiera de
ellas") pero no instruye en ningún punto a la sesión que orquesta la skill a cargarlo antes de
generar o revalidar, así que el hueco no es solo de `scripts/`: es también de instrucción, en un
proyecto donde la "tubería" real es la propia sesión de Claude siguiendo `SKILL.md`, no un `main()`
único — exactamente lo que el requisito 3 de la spec de R-26 pide corregir. Premisa técnica
confirmada con exactitud; spec bien acotada (fuera de alcance explícito: no cambia el formato del
diccionario, no añade campos a `estado.json`, no construye un `main()` de CLI nuevo). No se abre
hallazgo nuevo en este registro porque no es un descubrimiento del auditor: ya está correctamente
enrutado como R-26 con spec completa en `ROADMAP_PRODUCTO.md`, a la espera del siguiente ciclo de
Programador.

**Coherencia roadmap↔código.** `ROADMAP_PRODUCTO.md` ("Oleada v14 — EN CURSO") y `SEGUIMIENTO.md` §1
(`R-26 PENDIENTE`) coinciden palabra por palabra en objetivo y estado: no hay prosa desactualizada
que corregir esta vez (motivo exacto por el que `#24` no repite el patrón en esta pasada — ver
registro de arriba). `DECISIONES_TECNICAS.md` sigue append-only y sus últimas entradas (R-25/R-19)
sustentan decisiones ya promovidas o correctamente acotadas a su propia ficha, sin ninguna que
debiera subir a §0.2 y no lo haya hecho. `DEVELOPERS.md` sigue describiendo la estructura real del
repositorio (confirmado contra `assets/`, `references/`, `scripts/`, `tests/` tal y como existen hoy)
y `roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin ninguna entrada `nuevo` que
el PM deba incorporar — el bloqueo #7 de §3 (grabar un curso completo) sigue sin resolverse, sin
acción posible desde una sesión de nube.

**Las cuatro invariantes de datos (a)-(d) de §0.2, muestreadas contra el código vigente, sin
regresión:** (a) cobertura total — sin cambio en `clasificador.py`/`troceo.py` desde R-25, suite de
reconstrucción sigue en verde; (b) original recuperable — registro append-only de reescrituras sin
tocar; (c) edición manual manda — el endurecimiento de P-02/P-03/P-04 (`#9`/`#14`/`#19`) sigue en
`revalidacion.py` sin ningún commit que lo toque desde su último cierre; (d) sin borrado
destructivo — cuatro sitios `.bak`, verificado arriba. Ninguna de las cuatro está en riesgo por R-26:
su propia spec las declara explícitamente fuera de alcance (requisito 5).

**Conclusión de esta pasada.** Proyecto en el estado más saludable observado hasta ahora: cero
hallazgos `ABIERTO` de código — el único `ABIERTO` que queda (`#24`) es puramente de proceso, sin
coste de producto, y va por 23 pasadas esperando una única respuesta de gobernanza del dueño —,
cuatro redes en verde, roadmap y seguimiento coherentes entre sí y con el código, y una R-XX nueva
(R-26) bien razonada y correctamente acotada, lista para su implementación. Sin ninguna acción propia
sobre `scripts/`, `tests/`, `assets/` ni ningún documento salvo este.

---

### Auditoría 2026-10-08 — un hallazgo nuevo (`#29`, baja, primera apertura de R-XX sin fila de seguimiento en §1); `#28` cerrado (P-06, verificado); R-24 implementada y verificada con código; R-25 abierta sin implementar; `#24` reconfirmado `ABIERTO` (veintidós pasadas, séptima repetición del patrón, con R-24, autocorregida el mismo día)

**Nota de arranque.** Contenedor arrancado ya en `develop`, sin *detached HEAD*; `git pull origin
develop` resolvió en fast-forward limpio hasta `738eea9` (doce commits desde la última auditoría,
`98a684b`), sin conflicto. `pip install -r requirements-dev.txt` pelado (primer paso del preámbulo)
volvió a instalar contra **Python 3.13** en vez del **3.11.x** real — mismo síntoma de siempre, ya
cubierto por la documentación desde `P-06` (ver más abajo); resuelto con `python3 -m pip install -r
requirements-dev.txt`.

**Alcance desde la última auditoría (`98a684b`) — doce commits, dos de código/documentación real.**
`git log 98a684b..738eea9` muestra: la implementación real de R-24 (`03c7aa1`, diagnóstico real de
un fallo al generar una salida), el cierre documental de `#28` por `P-06` (`0a8e90e`), nueve
reconfirmaciones sucesivas del Programador el mismo día y el ciclo de PM que archivó la Oleada v12 y
abrió R-25 (`2628739`, `738eea9`).

**R-24 revisada línea a línea contra su propia spec** (ya revisada por esta auditoría en la pasada
anterior). `scripts/monitorizacion.py::_volcar_diagnostico` se promueve a pública
(`volcar_diagnostico`) exactamente como anunciaba la ficha; `scripts/salidas.py::
generar_salidas_seleccionadas` la reutiliza junto con `logger.obtener_logger` dentro del `except`
ya existente, sin envolver con `ejecutar_con_diagnostico` (razonado en `DECISIONES_TECNICAS.md`:
esa función aborta el proceso, justo lo contrario del requisito 3 de T-30). Confirmado con
`grep -n "ruta_diagnostico\|carpeta_salida" scripts/monitorizacion.py` que la ruta del diagnóstico
sigue construyéndose siempre dentro de `carpeta_salida` — invariante "nada se escribe fuera de la
carpeta de salida" intacto también para este archivo nuevo. El `motivo` de la `SalidaOmitida` deja
de mostrar `str(excepcion)` crudo y pasa a citar la ruta del `.log`; el test que documentaba el
contrato antiguo se actualizó en el mismo commit en vez de quedar en rojo o duplicado (decisión
razonada en `DECISIONES_TECNICAS.md`, sin nada que objetar). Sin hallazgo de código.

**`#28` cerrado, verificado de forma independiente, no solo transcrito de `SEGUIMIENTO.md`.**
`grep -n pelado DEVELOPERS.md SKILL.md` confirma el párrafo nuevo en ambos archivos, junto al que ya
cubría el binario pelado de R-15: recomienda `python3 -m pip install -r requirements-dev.txt` y cita
`origen: auditoría #28`. Reproducido en esta misma pasada (ver nota de arranque) que el síntoma del
contenedor sigue existiendo tal cual — el cierre es documental, no corrige el contenedor, que no es
responsabilidad de este repositorio — exactamente lo que pedía la recomendación de cierre que la
propia auditoría anterior había dejado escrita. Fila `#28` pasa a `RESUELTO` en el registro.

**Hallazgo nuevo `#29` (proceso/gobernanza, baja): la apertura de R-25 no añadió su fila a §1 de
`SEGUIMIENTO.md`.** Detectado comparando sistemáticamente los diffs de apertura de las tres últimas
R-XX, no dando por sentado que el patrón se repite: `git show cc0ac86 -- roadmap/SEGUIMIENTO.md` y
`git show 98a684b -- roadmap/SEGUIMIENTO.md` confirman que abrir R-23 y R-24 añadió, en el mismo
commit, una fila `PENDIENTE` a la tabla de §1; `git show 2628739 -- roadmap/SEGUIMIENTO.md` no toca
esa tabla en absoluto para R-25, y `grep -n "^| R-25" roadmap/SEGUIMIENTO.md` sobre el `HEAD` actual
no da ningún resultado — la última fila de §1 sigue siendo la de R-24, `COMPLETADA`. §1 se declara a
sí mismo "fuente autoritativa de estado... no duplicar" en otro documento: con R-25 ausente de esa
tabla, el propio documento incumple su regla de fuente única por primera vez desde que el patrón de
apertura existe. Riesgo real acotado: la cabecera de "Última actualización" de `SEGUIMIENTO.md` y la
sesión 104 de `HISTORIAL_SESIONES.md` sí narran la apertura con detalle, y las sesiones de
Programador de este proyecto vienen revisando tanto §1 como la prosa de `ROADMAP_PRODUCTO.md` antes
de concluir "cola vacía" (verificado leyendo las nueve reconfirmaciones del 2026-10-07, todas citan
la spec de R-24/R-25 correctamente) — pero nada garantiza que ese hábito se mantenga si una sesión
futura se ciñe estrictamente al contrato documentado ("§1 es la fuente, no busques en otro sitio").
Severidad baja (sin coste real todavía, cero impacto de producto) con recomendación de cierre
igual de concreta que `#28`: añadir la fila que falta, mismo patrón que R-23/R-24. No se corrige
aquí (el auditor no modifica `SEGUIMIENTO.md`).

**Cuatro redes de verificación, todas en verde, ejecutadas directamente por este auditor:** `python3
-m ruff check .` → "All checks passed!"; `python3 -m mypy scripts/ tests/` → "Success: no issues
found in 70 source files"; `python3 -m pytest` → **649 passed**, cifra idéntica a la que
`SEGUIMIENTO.md` §1 registra para R-24 (P-06 no añade tests, correcto: cambio puramente documental);
`python3 scripts/ci.py` → CI en VERDE de punta a punta, incluidas las **dieciocho** etapas de
`verificar_salidas.py --fixture` (sin cambio de número: ni R-24 ni P-06 añaden salida nueva). `.pptx`/
`.pdf` reales siguen LATENTES en este contenedor (sin la skill de marca, sin Chrome/Edge) —
degradación esperada, sin cambios. `git status` limpio tras la verificación.

**Invariantes de §0.2 reverificados con código:** protección `.bak` sin cambios, reconfirmada con
`grep -rln "copia_seguridad\s*=" scripts/*.py` → los mismos cuatro sitios de siempre
(`documento_revision.py`, `entrada.py`, `feedback.py`, `instalar_skill.py`); nada se escribe fuera de
la carpeta de salida (confirmado también para el nuevo `diagnostico-<timestamp>.log` de R-24, ver
arriba); runtime solo biblioteca estándar sin cambios; cobertura total del guión intacta (R-24/P-06
no tocan `clasificador.py` ni `parser.py`); auto-contención del reproductor y del HTML de impresión
reverificada por `verificar_salidas.py --fixture` (`OK` en ambas etapas). R-25 todavía sin código
(confirmado con `grep -rn "CONVENCION_GUIONES" scripts/salidas.py` → sin resultado): nada que auditar
más allá de su spec.

**Spec de R-25 revisada antes de que el Programador la implemente.** Grieta de arquitectura real,
verificada con `grep -rn "generar_convencion_guiones\|guardar_convencion_guiones" scripts/*.py
SKILL.md` → sin resultado fuera de `scripts/convencion.py` y sus tests, igual que documenta la
ficha. Las dos alternativas descartadas (`calibracion.calcular_calibracion`, `reescrituras.
revertir_reescrituras`) están razonadas con el mismo rigor que las elegidas en oleadas anteriores,
sin indicio de sobrediseño ni de construir por adelantado algo que el bloqueo #7 (cero curso grabado
todavía) no justifica. Requisitos acotados (séptima opción aditiva del enum, cero segunda
implementación de la lógica de T-10, fuera de alcance explícito) y criterio de aceptación con
regresión de las seis salidas existentes. Nada que objetar.

**Coherencia roadmap↔código.** §1 de `SEGUIMIENTO.md` coincide con el código real en el único punto
que cambió desde la última pasada: R-24 `COMPLETADA` (verificado arriba). R-25 es la única ausencia
real de esta pasada (`#29`, ver arriba). §3 (bloqueos) sin cambios. §5 gana P-06, `COMPLETADA`,
consistente con el commit `0a8e90e`. §6 sin novedad (pregunta `#11` sigue `(pendiente)`). §7
(desviaciones) sin entrada nueva: ni R-24 ni R-25 se han apartado de ninguna spec.

**Conclusión.** Proyecto en el mismo estado sólido que las auditorías anteriores: cuatro redes en
verde, invariantes intactos, R-24 implementada con tests que cubren exactamente el contrato que la
motivó, R-25 especificada con el mismo rigor. Dos movimientos en el registro de hallazgos: `#28` se
cierra (documentación aplicada y verificada), `#29` se abre (un hueco de proceso real, aunque de bajo
riesgo, en la propia disciplina de seguimiento que hasta ahora no había fallado nunca) — balance neto
sin hallazgos nuevos de severidad relevante.

---

### Auditoría 2026-10-07 — un hallazgo nuevo (`#28`, baja, formalización de un síntoma ya visto diez veces sin cerrar); R-23 implementada y verificada con código; R-24 abierta sin implementar; `#24` reconfirmado `ABIERTO` (veintiuna pasadas, sexta repetición del patrón, con R-23, autocorregida el mismo día)

**Nota de arranque.** Contenedor arrancado con `HEAD` *detached* en `98a684b` (no en `develop`);
`git checkout develop && git pull origin develop` resolvió en fast-forward limpio
(`cc0ac86..98a684b`, doce commits) sin conflicto ni pérdida — nada que perder: el *detached HEAD* ya
apuntaba al mismo commit que `origin/develop` trae de más. `pip install -r requirements-dev.txt`
pelado (primer paso del preámbulo, tal cual lo pide el protocolo) instaló de nuevo contra **Python
3.13** en vez del **3.11.15** real del proyecto — reproducido y confirmado en código, no solo
anotado: `python3 scripts/ci.py` dio las tres redes de tipos/estilo/tests en **ROJO** con `No module
named mypy`/`ruff`/`pytest` hasta reinstalar con `python3 -m pip install -r requirements-dev.txt`.
Van ya once sesiones consecutivas (la de implementación de R-23 más las nueve reconfirmaciones del
Programador más esta auditoría) con el mismo síntoma idéntico y el mismo rodeo, sin que la nota de
R-15 en `DEVELOPERS.md`/`SKILL.md` lo cubra todavía — se formaliza como hallazgo nuevo, `#28` (ver
registro), en vez de dejarlo otra vez como nota suelta en esta narrativa.

**Alcance desde la última auditoría (`cc0ac86`) — doce commits, uno de código real.** `git log
cc0ac86..98a684b` muestra: la implementación real de R-23 (`791ec07`, desviaciones de convención
cableadas en `guion-escenas.md`/`tarjetas.json`), nueve reconfirmaciones sucesivas del Programador el
mismo día ("sin novedad de código") y el ciclo de PM que archivó la Oleada v11 y abrió R-24
(`98a684b`). Confirmado con `git show --stat 791ec07` que el cambio toca exactamente lo que anuncia:
`scripts/documento_revision.py`, `scripts/pptx.py`, sus tests (`test_documento_revision.py`,
`test_pptx.py`, `test_integracion_montaje.py`), la fixture dorada y la documentación
(`references/contrato-tarjetas.md`, `contrato-montaje.md`, `formato-guion-escenas.md`,
`DEVELOPERS.md`, `SKILL.md`, roadmap) — cero archivo fuera de ese conjunto, cero cambio en
`scripts/convencion.py` (requisito 6 de la ficha, verificado con `git show --stat` sin ese archivo en
la lista).

**Revisión completa del diff de R-23, línea a línea, no solo de su resumen.** `documento_revision.py`
gana `_desviaciones_de_escena`/`_desviaciones_sin_escena` (localización por rango de línea, mismo
patrón que `_indicaciones_no_recitables` ya usaba) y `formatear_desviaciones`; la cabecera global
siempre muestra el recuento (`N=0` incluido) pero ninguna sección vacía se añade ni al pie de escena
ni fuera de ella — verificado con los dos tests dedicados exactamente a ese contraste
(`test_sin_desviaciones_no_anade_ninguna_seccion_nueva`). `pptx.py::ResultadoTarjetas` gana
`desviaciones_convencion` a nivel de metadatos (no por `Tarjeta`), razonado en
`DECISIONES_TECNICAS.md` porque una desviación de numeración implica a dos escenas a la vez o a
ninguna — coherente con la forma real del dato que devuelve `detectar_desviaciones` (lista plana con
número de línea). Vacía con `--para-terceros`, calculada ya vacía en `generar_tarjetas` (no filtrada
al serializar), mismo criterio que `notas_internas` ya aplicaba — confirmado leyendo las dos rutas de
código, no solo el test. Verificación cruzada propia (no solo la del test de integración que ya trae
el commit): generé `guion-escenas.md` y `tarjetas.json` sobre los tres guiones reales de
`fixtures/reales/` y comprobé que los tres tienen `Desviaciones de la convención: 0` y
`"desviaciones_convencion": []` — coherente con que esos guiones ya numeran sus escenas sin huecos ni
repeticiones (lo que la propia fixture dorada regenerada también confirma). Conclusión: implementación
sólida, sin ningún hallazgo de código.

**Grieta de arquitectura de R-24 (manejo de errores ad hoc en `salidas.py` en vez del
logger/diagnóstico de T-02/T-05), spec revisada antes de que el Programador la implemente.** Leída la
ficha completa en `ROADMAP_PRODUCTO.md` §Oleada v12 y el código real que motiva la apertura:
`scripts/salidas.py` línea ~499 captura `Exception` y construye `SalidaOmitida(tipo, f"fallo al
generar: {excepcion}")` sin volcar ningún diagnóstico ni pasar por `logger.obtener_logger` —
confirmado con `grep -n "fallo al generar" scripts/salidas.py`. La spec decide explícitamente NO
envolver con `ejecutar_con_diagnostico` (pensada para abortar un proceso con código de salida) sino
reutilizar solo `volcar_diagnostico` (promovida a pública) y `obtener_logger` dentro del `except` ya
existente, preservando el requisito 3 de T-30 ("una salida rota nunca impide las demás") — razonamiento
coherente con §0.2 y sin ningún indicio de sobrediseño. El archivo de diagnóstico se escribe dentro de
`<carpeta_salida>/`, respetando el invariante de no escribir nada fuera de ella. Nada que objetar: R-24
no está implementada todavía (confirmado con `grep -rn "volcar_diagnostico\|diagnostico-" scripts/salidas.py`
→ sin resultado), así que no hay código que auditar más allá de la spec.

**Cuatro redes de verificación, todas en verde, ejecutadas directamente por este auditor (no
transcritas de ninguna ficha), tras corregir el entorno de `pip` descrito arriba:** `python3 -m ruff
check .` → "All checks passed!"; `python3 -m mypy scripts/ tests/` → "Success: no issues found in 70
source files"; `python3 -m pytest` → **646 passed** (637→646, los 9 tests nuevos de R-23), cifra
idéntica a la que `SEGUIMIENTO.md` §1 registra para R-23; `python3 scripts/ci.py` → CI en VERDE de
punta a punta, incluidas las **dieciocho** etapas de `verificar_salidas.py --fixture` (sin cambio de
número: R-23 no añade salida nueva, solo enriquece dos ya existentes). `.pptx`/`.pdf` reales siguen
LATENTES en este contenedor (sin la skill de marca, sin Chrome/Edge) — degradación esperada y
documentada, sin cambios. `git status` limpio tras la verificación: ningún archivo generado por
`verificar_salidas.py --fixture` quedó fuera de la carpeta de salida ignorada por git.

**Invariantes de §0.2 reverificados con código, no solo con la ficha de la tarea que los
introdujo:** cobertura total del guión intacta (R-23 es puro enriquecimiento de dos documentos ya
existentes, no toca `clasificador.py` ni `parser.py`); protección `.bak` sin cambios desde `#23`,
reconfirmada con `grep -rln "copia_seguridad\s*=" scripts/*.py` → los mismos cuatro sitios
(`documento_revision.py`, `entrada.py`, `feedback.py`, `instalar_skill.py`); auto-contención del
reproductor y del HTML de impresión reverificada por `verificar_salidas.py --fixture` (`OK` en ambas
etapas) y con `grep -rnE` propio sobre `assets/reproductor/` y `assets/pdf/` en busca de
`https?://`/`//cdn`/`@import`/`<object`/`<embed`/`<base href`/`WebSocket`/`EventSource`/`sendBeacon`/
`url\(` → ningún resultado; runtime solo biblioteca estándar (`pyproject.toml` sin `dependencies`,
`requirements-dev.txt` marcado explícitamente como solo-desarrollo); `SKILL.md` sigue documentando
los 81 campos de `Configuracion` (`tests/test_skill_md.py` en verde, comparación en las dos
direcciones); nada se escribe fuera de la carpeta de salida del guion (confirmado también para el
nuevo `diagnostico-<timestamp>.log` que especifica R-24, todavía sin implementar).

**Coherencia roadmap↔código.** §1 de `SEGUIMIENTO.md` (fuente autoritativa) coincide con el código
real en los dos puntos que cambiaron desde la última pasada: R-23 `COMPLETADA` (código presente,
verificado arriba) y R-24 `PENDIENTE` (spec presente, código ausente, verificado arriba). §3
(bloqueos) sin cambios — bloqueo #2 (`480-branded-pptx`), #5 (clicker) y #7 (grabar un curso
completo) siguen abiertos sin urgencia, tal como ya constaba. §5 (P-XX) sin entradas nuevas desde
P-05. §7 (desviaciones) sin entrada nueva: R-23/R-24 no se han apartado de ninguna spec.
`roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía — el bloqueo #7 sigue siendo la
única razón.

**Conclusión.** Proyecto en el mismo estado sólido que las auditorías anteriores: cuatro redes en
verde, invariantes intactos, R-23 implementada con tests que reproducen exactamente el hallazgo de
arquitectura que la motivó, R-24 especificada con el mismo rigor y sin sobrediseño. Único hallazgo
nuevo de esta pasada (`#28`) es de documentación de entorno, severidad baja, sin ningún coste de
producto — mismo perfil que `#24`, con el que comparte también la recomendación: una línea de
documentación cerraría ambos para siempre en vez de seguir reconfirmándolos pasada tras pasada.

---

### Auditoría 2026-10-06 — sin hallazgos nuevos; R-22 implementada y verificada con código; R-23 abierta sin implementar; `#24` reconfirmado `ABIERTO` (veinte pasadas, quinta repetición del patrón, con R-22, autocorregida el mismo día)

**Nota de arranque.** Contenedor arrancado ya en `develop` (sin *detached HEAD*), `git status`
limpio desde el inicio; `git pull origin develop` → "Already up to date" en `cc0ac86`, sin
necesidad de `stash` ni de resolver divergencia. Clon superficial (`git rev-parse
--is-shallow-repository` → `true`, 50 commits visibles) — mismo síntoma benigno ya cerrado de forma
independiente por `#21` (2026-09-10); no se repite `git fetch --unshallow` esta pasada por no haber
ninguna sospecha de historial reescrito (el `pull` no tuvo nada que resolver). `pip install -r
requirements-dev.txt` con el `pip`/`python3` por defecto de este contenedor instaló las herramientas
contra **Python 3.13** (`pip --version` resuelve a `/usr/bin/pip` con `(python 3.13)`), no contra el
**3.11.17** real del proyecto (`/usr/local/bin/python3`) — detalle de entorno nuevo en esta sesión,
no visto en pasadas anteriores: `python3 -m ruff`/`mypy`/`pytest` fallaban con `No module named
<herramienta>` hasta reinstalar explícitamente con `python3 -m pip install -r
requirements-dev.txt`, que sí resuelve al intérprete 3.11 correcto. No es un hallazgo de código —ya
existe un hallazgo histórico equivalente (`#22`, RESUELTO por R-15) sobre el riesgo de invocar
herramientas sin pasar por el intérprete correcto en un contenedor de nube con más de un Python
instalado— y `scripts/ci.py` sigue siendo inmune porque usa siempre `sys.executable -m <herramienta>`
(confirmado de nuevo en esta pasada). Se deja constancia para que una pasada futura no pierda tiempo
si un `pip install` liso vuelve a instalar contra el intérprete equivocado: usar `python3 -m pip
install` directamente, nunca el `pip` pelado.

**Alcance desde la última auditoría (`d926ede`) — nueve commits, uno de código real.** `git log
d926ede..cc0ac86` muestra: la novena reconfirmación del día de Programador tras R-22 (de las nueve,
ocho eran "sin novedad de código"), la propia implementación de R-22 (`979a620`,
`capitulos-ffmpeg.txt` en formato `FFMETADATA1`) y el ciclo de PM que la archivó y abrió R-23
(`cc0ac86`). Confirmado con `git show --stat 979a620` que el cambio de código toca exactamente lo que
anuncia su mensaje: `scripts/capitulos_youtube.py`, `scripts/config.py`, `scripts/salidas.py`,
`scripts/verificar_salidas.py`, sus tests (`test_capitulos_youtube.py`, `test_salidas.py`) y la
documentación (`references/contrato-montaje.md`, `DEVELOPERS.md`, `SKILL.md`, roadmap) — cero
archivo fuera de ese conjunto.

**Revisión completa del diff de R-22, línea a línea, no solo de su resumen.** `ResultadoCapitulos`
gana el campo aditivo `duracion_total_segundos` (el cursor final que el bucle de `calcular_capitulos`
ya acumulaba); `formatear_capitulos_ffmpeg`/`validar_capitulos_ffmpeg` son hermanas deliberadas de las
de R-07/R-19, mismo patrón de escapado FFMETADATA1 (`\`, `=`, `;`, `#`, salto de línea) que el que
`concat_ffmpeg._escapar_ruta_ffmpeg` ya usa para la ruta de vídeo. `scripts/salidas.py` valida el
contenido con `validar_capitulos_ffmpeg` ANTES de escribir, desde el primer commit de la tarea —
aplicando ya la lección de `#27`/R-21 en vez de repetir el hueco y cerrarlo después, confirmado
leyendo `DECISIONES_TECNICAS.md` (entrada "R-22 (alcance)") donde el propio ciclo razona
explícitamente por qué no repite ese error a sabiendas. Se exploró a fondo un posible hueco teórico
no cubierto por los 18 tests nuevos: `validar_capitulos_ffmpeg` nunca comprueba que `END` sea mayor
que su propio `START` dentro del mismo capítulo (solo que `START` crezca y que no se solape con el
`END` anterior) — reproducible solo si una escena tuviera duración estimada `0.0`
(`tiempos.calcular_tiempos_desde_marcados` no impide una escena sin ningún bloque de locución).
Verificado con los cuatro guiones reales (`fixtures/reales/` + `fixtures/guion-ejemplo.md`) que
**ninguna escena de ninguno de los dos tiene duración `0.0`** — no es un escenario alcanzable hoy, y
si llegara a serlo el propio validador lo degradaría a `SalidaOmitida` con motivo explícito (nunca
corrompería el archivo en silencio), el mismo comportamiento defensivo que ya protege a
`concat-ffmpeg.txt`. No se registra como hallazgo nuevo por el mismo criterio que cerró `#19`: una
asimetría teórica sin ruta de alcance real y con degradación segura ya verificada no es un riesgo de
producto. Conclusión: implementación sólida, sin ningún hallazgo de código.

**Grieta de arquitectura de R-23 (`detectar_desviaciones` nunca llamada desde la generación real),
verificada de forma independiente, no solo leída en `SEGUIMIENTO.md`.** `grep -rn
"detectar_desviaciones" scripts/*.py tests/*.py` confirma exactamente lo que dice la ficha de la
tarea: la función solo aparece en `scripts/convencion.py` (donde se define) y en
`tests/test_convencion.py`/`tests/test_integracion_montaje.py` — cero resultado en
`scripts/documento_revision.py` ni `scripts/pptx.py`, los dos consumidores reales que el dueño y la
cadena de montaje usan. `references/contrato-montaje.md:68-73` sigue afirmando hoy, sin matiz, que la
numeración de escena "ya NO se da por supuesta en silencio" citando esa función por nombre — una
garantía que ningún archivo generado real respalda todavía. El PM ya lo deja dicho con la misma
franqueza en `SEGUIMIENTO.md`/`ROADMAP_PRODUCTO.md`/`DECISIONES_TECNICAS.md`, así que no se abre un
hallazgo nuevo en este registro (R-23 ya es el origen correcto, `PENDIENTE`, con spec completa y
razonada en `ROADMAP_PRODUCTO.md` §Oleada v11): el papel de esta pasada es solo corroborar con su
propia verificación independiente que la premisa de R-23 es exacta antes de que el Programador la
implemente, no inventar una segunda entrada para el mismo hecho.

**Cuatro redes de verificación, todas en verde, ejecutadas directamente por este auditor (no
transcritas de ninguna ficha):** `python3 -m ruff check .` → "All checks passed!"; `python3 -m mypy
scripts/ tests/` → "Success: no issues found in 70 source files"; `python3 -m pytest` → **637
passed** (619→637, los 18 tests nuevos de R-22), cifra idéntica a la que `SEGUIMIENTO.md` §1 registra
para R-22; `python3 scripts/ci.py` → CI en VERDE de punta a punta, incluidas las **dieciocho** etapas
de `verificar_salidas.py --fixture` (dieciséis→dieciocho, las dos nuevas de "capítulos de ffmpeg
(FFMETADATA1)"), `capitulos-ffmpeg.txt` generado y validado sobre `guion-ejemplo.md` con `END` del
último capítulo igual a `duracion_total_segundos`. `.pptx`/`.pdf` reales siguen LATENTES en este
contenedor (sin la skill de marca, sin Chrome/Edge) — degradación esperada y documentada, sin
cambios.

**Invariantes de §0.2 reverificados con código, no solo con la ficha de la tarea que los
introdujo:** auto-contención del reproductor (`grep -rnE` sobre `assets/reproductor/` y
`assets/pdf/` en busca de `https?://`, `//cdn`, `@import`, `<object`, `<embed`, `<base href`,
`WebSocket`, `EventSource`, `sendBeacon` → ningún resultado); runtime solo biblioteca estándar
(`pyproject.toml:6`, `dependencies = []`); protección `.bak` sin cambios desde que `#23` la acotó a
los cuatro sitios reales (`documento_revision.py`, `entrada.py`, `feedback.py`, `instalar_skill.py`,
reconfirmado con `grep -rln "copia_seguridad\s*=" scripts/*.py`); `capitulos-ffmpeg.txt` es una
salida derivada regenerable sin intervención manual (como el resto de `.txt`/`.srt` generados), no un
archivo del dueño, así que correctamente no lleva copia `.bak` — mismo criterio que `#23` ya dejó
establecido; aviso no bloqueante de versión de Python (`ci.avisar_si_version_python_diverge`, R-08)
sigue disparando correctamente contra el intérprete real de esta sesión (3.11.17 < 3.12 declarado);
cero `print()` de depuración fuera de `presentacion.py`/`logger.py`; nombre de archivo nuevo
(`NOMBRE_ARCHIVO_CAPITULOS_FFMPEG`) es una constante de módulo, igual que el resto de
`NOMBRE_ARCHIVO_*` (nunca un campo de `Configuracion`, por no ser un valor que el dueño deba poder
cambiar) — ningún número mágico suelto. Ningún hallazgo nuevo de robustez.

**Coherencia roadmap ↔ código.** `SEGUIMIENTO.md` §1: R-22 `COMPLETADA` (2026-10-05), R-23
`PENDIENTE` como única R-XX en cola — coincide con el código (`FFMETADATA1` presente,
`detectar_desviaciones` todavía sin cablear). `ROADMAP_PRODUCTO.md` "Cola de producto" ya corregida
por el propio PM en `cc0ac86` (ver `#24` arriba): describe R-23 como único pendiente, Oleada v10
movida íntegra a `ROADMAP_HISTORICO.md`. §7 (desviaciones) sin filas nuevas desde 2026-09-02;
`roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin ninguna entrada `nuevo`;
`mcp__github__list_issues`/`list_pull_requests` sobre `JanoSolerDiaz/telePrompter`: cero issues y
cero PR abiertos, igual que en todas las pasadas anteriores. Entrada de `DECISIONES_TECNICAS.md` para
R-22 (seis decisiones razonadas: dónde ancla el archivo en el selector, por qué una función hermana
propia en vez de compartir el cálculo de la nota de transparencia, por qué dos etapas de
`verificar_salidas.py` separadas) y para R-23 (origen, alcance en `tarjetas.json.metadatos`) leídas
íntegras: mismo rigor razonado que R-08 a R-21, sin ninguna premisa sin verificar en código (la
propia entrada de apertura de R-23 cita el `grep` exacto usado, evitando el error que `#26` señaló en
su día).

**`#24` reconfirmado `ABIERTO` (fila actualizada arriba):** la pregunta de gobernanza `#11` de
`SEGUIMIENTO.md` §6 sigue `(pendiente)` de respuesta del dueño — veinte pasadas de auditoría
consecutivas (2026-09-17 a 2026-10-06). Esta vez el patrón de prosa desactualizada **sí** se repitió
(quinta vez, con R-22: nueve reconfirmaciones del Programador el mismo día que la implementó dejaron
`ROADMAP_PRODUCTO.md` en "EN CURSO"/`PENDIENTE`), pero el propio PM volvió a autocorregirse en el
mismo commit que archivó la oleada (`cc0ac86`) — ninguna R-XX ha quedado desactualizada en la prosa
más de una jornada en ninguna de las cinco repeticiones del patrón hasta ahora.

**Conclusión de esta pasada.** Ningún hallazgo nuevo. R-22 está completa, verificada con código
línea a línea (no solo con la ficha) y sin ninguna grieta de robustez explotable hoy; R-23 queda bien
especificada y su premisa de arquitectura, verificada de forma independiente. Las cuatro redes de
verificación están en verde con las cifras que el roadmap anuncia (637 tests, dieciocho etapas de
`verificar_salidas.py --fixture`), los invariantes de §0.2 siguen intactos y verificados con código,
y el único hallazgo abierto (`#24`, severidad baja) sigue dependiendo exclusivamente de una decisión
de gobernanza del dueño, sin ningún riesgo de producto o de código detrás. No se detecta ninguna
desviación entre lo decidido en `DECISIONES_TECNICAS.md`/§0.2 y lo realmente implementado.

---

### Auditoría 2026-10-05 — sin hallazgos nuevos; sin cambios de código desde la pasada anterior; R-22 sigue sin implementar; `#24` reconfirmado `ABIERTO` (diecinueve pasadas consecutivas)

**Nota de arranque.** Contenedor arrancado con `HEAD` desprendido (28 commits por delante de
cualquier rama local, resto de un contenedor anterior); `git checkout develop && git pull origin
develop` en fast-forward limpio hasta `b60294f`, árbol de trabajo limpio desde el inicio, sin
necesidad de `stash` ni de resolver divergencia. Clon superficial (`git rev-parse
--is-shallow-repository` → `true`) — mismo síntoma benigno ya cerrado de forma independiente por
`#21` (2026-09-10); no se repite `git fetch --unshallow` esta pasada por no haber ninguna sospecha
nueva de historial reescrito (el `pull` fue un fast-forward limpio, sin divergencia). `pip install -r
requirements-dev.txt` limpio (mismas versiones pineadas: `mypy==1.18.2`, `ruff==0.14.0`,
`pytest==8.4.2`).

**Alcance desde la última auditoría (`6689d90`) — un commit, ninguno de código.** `git log
6689d90..b60294f` muestra un único ciclo de PM (`b60294f`, "reconfirmación de cola, sin R-XX nueva
abierta"). Confirmado con `git diff --stat 6689d90..b60294f` que los únicos archivos tocados son
`roadmap/DECISIONES_TECNICAS.md`, `roadmap/HISTORIAL_SESIONES.md` y `roadmap/SEGUIMIENTO.md` — cero
líneas de `scripts/`, `tests/`, `assets/` ni `references/`. La entrada de `DECISIONES_TECNICAS.md`
("2026-10-04 · PM (ciclo sin apertura)") razona por qué no se abre una R-23 especulativa, confirmando
con `git log`/`grep` que ni `capitulos_youtube.py`/`salidas.py`/`config.py`/`contrato-montaje.md` se
tocaron desde la apertura de R-22 (2026-10-02) ni `FFMETADATA1`/`capitulos-ffmpeg`/
`formatear_capitulos_ffmpeg` aparecen todavía en `scripts/` — mismo método disciplinado que los
ciclos anteriores, verificado leyendo la entrada completa, no solo el titular.

**Cuatro redes de verificación, todas en verde, ejecutadas directamente por este auditor (no
transcritas de ninguna ficha):** `python3 -m ruff check .` → "All checks passed!"; `python3 -m mypy
scripts/ tests/` → "Success: no issues found in 70 source files", cifra idéntica a la de pasadas
anteriores; `python3 -m pytest` → **619 passed**, cifra idéntica a la que `SEGUIMIENTO.md` §1 registra
desde R-21; `python3 scripts/ci.py` → CI en VERDE de punta a punta, incluido `verificar_salidas.py
--fixture` con sus dieciséis etapas en `OK` (`concat-ffmpeg.txt` entre ellas, generación y validez).
`.pptx`/`.pdf` reales siguen LATENTES en este contenedor (sin la skill de marca, sin Chrome/Edge) —
degradación esperada y documentada, sin cambios.

**Invariantes de §0.2 reverificados con código, no solo con la ficha de la tarea que los
introdujo:** auto-contención del reproductor (`grep -rnE` sobre `assets/reproductor/` y
`assets/pdf/` en busca de `https?://`, `//cdn`, `@import`, `<object`, `<embed`, `<base href`,
`WebSocket`, `EventSource`, `sendBeacon` → ningún resultado); runtime solo biblioteca estándar
(`pyproject.toml:6`, `dependencies = []`); protección `.bak` sin cambios desde que `#23` la acotó a
los cuatro sitios reales (`documento_revision.py`, `entrada.py`, `feedback.py`, `instalar_skill.py`,
reconfirmado con `grep -rln "copia_seguridad\s*=" scripts/*.py`); aviso no bloqueante de versión de
Python (`ci.avisar_si_version_python_diverge`, R-08) sigue disparando correctamente contra el
intérprete real de esta sesión (3.11.15 < 3.12 declarado); cero `print()` de depuración fuera de
`presentacion.py`/`logger.py` (`grep -rn "print(" scripts/*.py scripts/migraciones/*.py`). Ningún
hallazgo nuevo de robustez ni de números mágicos.

**Coherencia roadmap ↔ código, sin el patrón de `#24` esta vez (nada que corregir: no hubo ningún
ciclo de Programador reconfirmando una R-XX ya completada en medio).** `ROADMAP_PRODUCTO.md` "Cola de
producto" (sin cambios desde `9ea18f6`/`2988d11`) sigue describiendo **R-22** como la única R-XX
`PENDIENTE` — verificado contra `SEGUIMIENTO.md` §1 (R-21 `COMPLETADA`, sin fila para R-22 todavía,
consistente con que el Programador aún no la ha implementado) y contra `scripts/capitulos_youtube.py`/
`scripts/salidas.py` (sin ninguna función `FFMETADATA1`/`capitulos-ffmpeg.txt` todavía): coincide
exactamente, cero código adelantado a la spec ni spec desfasada del código. §7 (desviaciones) sin
filas nuevas desde 2026-09-02; `roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin
ninguna entrada `nuevo`; `mcp__github__list_issues`/`list_pull_requests` sobre
`JanoSolerDiaz/teleprompter`: cero issues y cero PR abiertos, igual que en todas las pasadas
anteriores.

**`#24` reconfirmado `ABIERTO` (fila actualizada arriba):** la pregunta de gobernanza `#11` de
`SEGUIMIENTO.md` §6 sigue `(pendiente)` de respuesta del dueño — diecinueve pasadas de auditoría
consecutivas (2026-09-17 a 2026-10-05) sin que haya costado nada más allá de la propia repetición.
Sin código nuevo que revisar esta pasada, el patrón que motivó el hallazgo (prosa de "Cola de
producto" desactualizada tras completarse una R-XX) no tuvo ocasión ni de repetirse ni de romperse:
el único ciclo intermedio fue de PM, que escribe ese documento directamente.

**Conclusión de esta pasada.** Ningún hallazgo nuevo, ningún hallazgo cerrado. El proyecto no tuvo
ningún cambio de código desde la auditoría anterior (solo un ciclo de PM que reconfirma la cola sin
abrir trabajo nuevo, razonado con disciplina en `DECISIONES_TECNICAS.md`); las cuatro redes de
verificación siguen en verde con cifras idénticas a las ya documentadas, los invariantes de §0.2
siguen intactos y verificados con código (no solo con la ficha de la tarea que los introdujo), y el
único hallazgo abierto (`#24`, severidad baja) sigue dependiendo exclusivamente de una decisión de
gobernanza del dueño, sin ningún riesgo de producto o de código detrás. No se detecta ninguna
desviación entre lo decidido en `DECISIONES_TECNICAS.md`/§0.2 y lo realmente implementado.

---

### Auditoría 2026-10-04 — sin hallazgos nuevos; sin cambios de código desde la pasada anterior; R-22 sigue sin implementar; `#24` reconfirmado `ABIERTO` (dieciocho pasadas consecutivas)

**Nota de arranque.** Contenedor arrancado con `HEAD` desprendido (26 commits por delante de
cualquier rama local, resto de un contenedor anterior); `git checkout develop && git pull origin
develop` en fast-forward limpio hasta `4b56e1a`, árbol de trabajo limpio desde el inicio. Clon
superficial (`git rev-parse --is-shallow-repository` → `true`) — mismo síntoma benigno ya cerrado de
forma independiente por `#21` (2026-09-10); no se repite `git fetch --unshallow` esta pasada por no
haber ninguna sospecha nueva de historial reescrito que lo justifique (el `pull` fue un fast-forward
limpio, sin divergencia). `pip install -r requirements-dev.txt` limpio (mismas versiones pineadas:
`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Alcance desde la última auditoría (`113ae14`) — dos commits, ninguno de código.** `git log
113ae14..4b56e1a` muestra únicamente el propio commit de la auditoría anterior y un ciclo de PM
(`4b56e1a`, "reconfirmación de cola, sin R-XX nueva abierta"). Confirmado con `git diff --stat
113ae14..4b56e1a` que los únicos archivos tocados son `auditoriacontinua.md`,
`roadmap/DECISIONES_TECNICAS.md`, `roadmap/HISTORIAL_SESIONES.md` y `roadmap/SEGUIMIENTO.md` — cero
líneas de `scripts/`, `tests/`, `assets/` ni `references/`. El ciclo de PM razona en
`DECISIONES_TECNICAS.md` (entrada "2026-10-03 · PM (ciclo sin apertura)") por qué no abre una R-23
especulativa en vez de mantener solo R-22 en cola, releyendo `capitulos_youtube.py`/`salidas.py`/
`contrato-montaje.md` en busca de otra grieta de arquitectura antes de concluir que no hay ninguna —
mismo método disciplinado que las aperturas R-12 a R-22, verificado leyendo la entrada completa, no
solo el titular.

**Cuatro redes de verificación, todas en verde, ejecutadas directamente por este auditor (no
transcritas de ninguna ficha):** `python3 -m mypy scripts/ tests/` (invocación exacta de
`scripts/ci.py`) → "Success: no issues found in 70 source files", cifra idéntica a la de pasadas
anteriores; `python3 -m ruff check .` → "All checks passed!"; `python3 -m pytest` → **619 passed**, cifra idéntica
a la que `SEGUIMIENTO.md` §1 registra desde R-21; `python3 scripts/ci.py` → CI en VERDE de punta a
punta, incluido `verificar_salidas.py --fixture` con sus dieciséis etapas en `OK` (`concat-ffmpeg.txt`
entre ellas, generación y validez). `.pptx`/`.pdf` reales siguen LATENTES en este contenedor (sin la
skill de marca, sin Chrome/Edge) — degradación esperada y documentada, sin cambios.

**Comprobación independiente del hallazgo ya cerrado `#22` (binario "pelado" de `ruff`/`mypy`/
`pytest`), reproducida de nuevo en esta pasada:** este contenedor también trae un segundo juego de
binarios en `/root/.local/bin` por delante en el `PATH` (`ruff 0.15.20` frente al `ruff==0.14.0`
pineado). `ruff check .` (binario pelado) marca `UP042` en `scripts/salidas.py:83`
(`class TipoSalida(str, Enum)`, sugiere `enum.StrEnum`) que `python3 -m ruff check .` (la invocación
real del proyecto) NO marca — exactamente la señal falsa y engañosa que `#22`/R-15 ya documentaron y
advirtieron en `DEVELOPERS.md`/`SKILL.md`. No es un hallazgo nuevo: se confirma aquí que la mitigación
documental sigue vigente y que esta pasada usó siempre `python3 -m <herramienta>`, nunca el binario
pelado, para no caer en la misma confusión.

**Invariantes de §0.2 reverificados con código, no solo con la ficha de la tarea que los
introdujo:** auto-contención del reproductor (`grep -rnE` sobre `assets/reproductor/` y
`assets/pdf/` en busca de `https?://`, `//cdn`, `@import`, `<object`, `<embed`, `<base href`,
`WebSocket`, `EventSource`, `sendBeacon` → ningún resultado); runtime solo biblioteca estándar
(`pyproject.toml:6`, `dependencies = []`); protección `.bak` sin cambios desde que `#23` la acotó a
los cuatro sitios reales (`documento_revision.py`, `entrada.py`, `feedback.py`, `instalar_skill.py`,
reconfirmado con `grep -rln "copia_seguridad\s*=" scripts/*.py`); aviso no bloqueante de versión de
Python (`ci.avisar_si_version_python_diverge`, R-08) sigue disparando correctamente contra el
intérprete real de esta sesión (3.11.15 < 3.12 declarado); cero `print()` de depuración fuera de
`presentacion.py`/`logger.py` (`grep -rn "print(" scripts/*.py scripts/migraciones/*.py`); los tres
sitios con `write_text`/`open` sin `encoding=` explícito en la misma línea resultaron, al leer el
contexto completo, falsos positivos del propio grep (dos llamadas multilínea con `encoding="utf-8"`
en la línea siguiente, en `estado.py` y `monitorizacion.py`; la tercera, en `pdf.py`, es una lectura
en modo binario `"rb"` que no admite ni necesita `encoding`, para leer la cabecera de un PNG). Ningún
hallazgo nuevo de robustez o de números mágicos.

**Coherencia roadmap ↔ código, sin el patrón de `#24` esta vez (nada que corregir: no hubo ningún
ciclo de Programador reconfirmando una R-XX ya completada en medio).** `ROADMAP_PRODUCTO.md` "Cola de
producto" (sin cambios desde `9ea18f6`/`2988d11`) sigue describiendo **R-22** como la única R-XX
`PENDIENTE` — verificado letra por letra contra `SEGUIMIENTO.md` §1 (R-21 `COMPLETADA`, sin fila para
R-22 todavía, consistente con que el Programador aún no la ha implementado) y contra `scripts/
capitulos_youtube.py`/`scripts/salidas.py` (sin ninguna función `FFMETADATA1`/`capitulos-ffmpeg.txt`
todavía, confirmado con `grep -n "ffmpeg\|FFMETADATA"`): coincide exactamente, cero código
adelantado a la spec ni spec desfasada del código. §7 (desviaciones) sin filas nuevas desde
2026-09-02; `roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía, sin ninguna entrada
`nuevo`; `mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero
issues y cero PR abiertos, igual que en todas las pasadas anteriores.

**`#24` reconfirmado `ABIERTO` (fila actualizada arriba):** la pregunta de gobernanza `#11` de
`SEGUIMIENTO.md` §6 sigue `(pendiente)` de respuesta del dueño — dieciocho pasadas de auditoría
consecutivas (2026-09-17 a 2026-10-04) sin que haya costado nada más allá de la propia repetición.
Sin código nuevo que revisar esta pasada, el patrón que motivó el hallazgo (prosa de "Cola de
producto" desactualizada tras completarse una R-XX) no tuvo ocasión ni de repetirse ni de romperse:
el único ciclo intermedio fue de PM, que escribe ese documento directamente.

**Conclusión de esta pasada.** Ningún hallazgo nuevo, ningún hallazgo cerrado. El proyecto no tuvo
ningún cambio de código desde la auditoría anterior (solo un ciclo de PM que reconfirma la cola sin
abrir trabajo nuevo, razonado con disciplina en `DECISIONES_TECNICAS.md`); las cuatro redes de
verificación siguen en verde con cifras idénticas a las ya documentadas, los seis invariantes de
§0.2 siguen intactos y verificados con código (no solo con la ficha de la tarea que los introdujo), y
el único hallazgo abierto (`#24`, severidad baja) sigue dependiendo exclusivamente de una decisión de
gobernanza del dueño, sin ningún riesgo de producto o de código detrás. No se detecta ninguna
desviación entre lo decidido en `DECISIONES_TECNICAS.md`/§0.2 y lo realmente implementado.

---

### Auditoría 2026-10-03 — sin hallazgos nuevos; R-21 implementada y verificada, cierra `#27`; R-22 abierta y aún sin implementar; `#24` reconfirmado `ABIERTO` (cuarta repetición del patrón, con R-21)

**Nota de arranque.** Contenedor arrancado con `HEAD` desprendido (24 commits por delante de
cualquier rama local, resto de un contenedor anterior); `git checkout develop && git pull origin
develop` en fast-forward limpio hasta `2988d11`, árbol de trabajo limpio desde el inicio, sin
necesidad de `stash` ni de resolver divergencia. No se repite `git fetch --unshallow` esta pasada:
mismo síntoma benigno de clon superficial ya cerrado de forma independiente por `#21` (2026-09-10),
sin ninguna sospecha nueva de historial reescrito que lo justifique. `pip install -r
requirements-dev.txt` limpio (mismas versiones pineadas: `mypy==1.18.2`, `ruff==0.14.0`,
`pytest==8.4.2`).

**Alcance desde la última auditoría (`4890134`) — once commits: R-21 implementada y archivada, R-22
abierta (sin implementar).** `git log 51e38da..2988d11` (rango que arranca justo después del commit
de la auditoría anterior) muestra: `1e8d514` (ciclo de Programador, implementa R-21 completa),
nueve reconfirmaciones sucesivas del mismo día sin tocar código, y `2988d11` (ciclo de PM, archiva
R-21 en `ROADMAP_HISTORICO.md` y abre R-22). Confirmado con `git diff --stat
1e8d514..c0cb579 -- scripts/ tests/ assets/ references/ SKILL.md DEVELOPERS.md` (salida vacía): las
nueve reconfirmaciones no tocaron ni una línea de código, test, asset ni documentación de contrato
— exactamente lo que sus propios mensajes de commit afirman.

**Cuatro redes de verificación, todas en verde, ejecutadas directamente por este auditor (no
transcritas de ninguna ficha):** `python3 -m ruff check .` → "All checks passed!"; `python3 -m mypy
scripts/ tests/` → "Success: no issues found in 70 source files"; `python3 -m pytest` → **619
passed**, cifra que coincide exactamente con la que `SEGUIMIENTO.md` §1 registra para R-21
(613→619); `python3 scripts/ci.py` → CI en VERDE, incluido `verificar_salidas.py --fixture` con las
**dieciséis etapas en OK** (`concat-ffmpeg.txt` entre ellas, generación y validez). `.pptx`/`.pdf`
reales siguen LATENTES en este contenedor (sin la skill de marca, sin Chrome/Edge) — degradación
esperada y documentada, sin cambios.

**R-21 (validar `concat-ffmpeg.txt` en la ruta real de generación y sanear `archivo_video` en el
origen), verificada de forma independiente leyendo el diff completo de `1e8d514`, no solo la ficha
de `SEGUIMIENTO.md` o el mensaje del commit.** `scripts/salidas.py::_generar_concat_ffmpeg` invoca
ahora `concat_ffmpeg.validar_lista_concat_ffmpeg` sobre el contenido ya generado, justo antes de
`guardar_lista_concat_ffmpeg`, degradando a `SalidaOmitida` con el motivo exacto si falla — mismo
patrón `try`/`except` que ya protege a las demás cinco salidas, sin excepción sin capturar ni
archivo corrupto en disco. `scripts/tomas.py` gana `_sanear_archivo_video` (recorta espacios;
normaliza a `""` si queda vacío tras el recorte o contiene `\n`/`\r`), aplicada en
`_toma_desde_dict` al leer un parte de rodaje editado a mano; `assets/reproductor/guion.js` gana la
función gemela `sanearArchivoVideo`, aplicada en los dos puntos donde el dueño teclea el valor
(`pedirArchivoVideoToma` durante la grabación, y el botón de edición desde el índice) — verificado
leyendo ambos puntos de entrada línea a línea, no solo el nombre de la función. Las tres decisiones
de diseño registradas en `DECISIONES_TECNICAS.md` (validar en `salidas.py`, no en `concat_ffmpeg.py`;
sanear en los dos lenguajes por separado, no solo en `guion.js`; normalizar a `""` en vez de
rechazar con error fatal) son coherentes entre sí, con el invariante de que ningún dato del dueño se
pierde por un despiste de tecleo, y con el precedente ya sentado por R-10 (recorte de `\r\n` en
`entrada.py`, aplicado en la lectura, no solo en la escritura). Seis tests nuevos verificados uno a
uno (`test_archivo_video_se_recorta_de_espacios`,
`test_archivo_video_de_solo_espacios_se_normaliza_a_vacio`,
`test_archivo_video_con_salto_de_linea_se_normaliza_a_vacio`,
`test_archivo_video_con_retorno_de_carro_se_normaliza_a_vacio` en `test_tomas.py`;
`test_concat_ffmpeg_con_contenido_invalido_degrada_a_omitida_en_vez_de_escribir` en
`test_salidas.py`, que fuerza el fallo por monkeypatch —el saneamiento en origen ya impide
alcanzarlo en uso normal— y confirma que el archivo nunca llega a escribirse a disco;
`test_guion_js_sanea_el_archivo_video_en_los_dos_puntos_de_entrada` en `test_reproductor.py`): los
seis reproducen exactamente los dos huecos que `#27` documentó, sin dejar ningún caso límite de la
ficha original sin cubrir. `#27` se cierra `RESUELTO` en el registro de arriba.

**Invariantes de §0.2 reverificados con código, no solo con la ficha de la tarea que los
introdujo:** auto-contención del reproductor (`grep -rnE` sobre `assets/reproductor/` y
`assets/pdf/` en busca de `https?://`, `cdn.`, `@import`, `<object`, `<embed`, `<base href`,
`WebSocket`, `EventSource`, `sendBeacon` → ningún resultado); runtime solo biblioteca estándar
(`pyproject.toml:6`, `dependencies = []`); protección `.bak` sin cambios desde que `#23` la acotó a
los cuatro sitios reales (`documento_revision.py`, `entrada.py`, `feedback.py`,
`instalar_skill.py`, reconfirmado con `grep -rln "copia_seguridad\s*=" scripts/*.py`) — correcto
que R-21 no añada un quinto sitio: `concat-ffmpeg.txt` sigue siendo una salida derivada y
regenerable, nunca un archivo de entrada del dueño. Ningún número mágico nuevo: el saneamiento de
`archivo_video` es lógica (recortar, rechazar salto de línea), no un umbral configurable que debiera
vivir en `Configuracion`/`SKILL.md`.

**R-22 (Oleada v10, `capitulos-ffmpeg.txt` en formato `FFMETADATA1` de ffmpeg), spec revisada,
coherente y sin implementar todavía.** Leída la ficha completa de `ROADMAP_PRODUCTO.md` y la
justificación en `DECISIONES_TECNICAS.md`: se abre por grieta de arquitectura verificada
(`capitulos_youtube.py::calcular_capitulos` ya empareja título↔escena y calcula el tiempo acumulado
real/estimado de cada capítulo desde R-07, pero solo lo expone en el formato de descripción de
YouTube, nunca en el formato nativo de capítulos de ffmpeg que la fase de montaje, T-33, podría usar
para incrustarlos de verdad en el vídeo final) — mismo patrón de bajo riesgo que abrió R-12 a R-20,
verificado leyendo `calcular_capitulos`/`formatear_capitulos_youtube` línea a línea antes de
especificar la tarea, no solo citando el contrato. La propia spec aprende la lección de `#27`/R-21
desde el primer requisito: exige que `capitulos-ffmpeg.txt` valide su contenido antes de escribirse
a disco desde el primer commit, en vez de repetir el hueco y cerrarlo después — decisión razonada
explícitamente en `DECISIONES_TECNICAS.md` citando el propio precedente. `git diff --stat
1e8d514..2988d11 -- scripts/ tests/` confirma que el ciclo de PM no tocó ningún archivo de código:
R-22 es solo especificación, consistente con que `SEGUIMIENTO.md` §1 no trae fila nueva para ella.

**Coherencia roadmap ↔ código, con el patrón de `#24` repitiéndose una cuarta vez.**
`ROADMAP_PRODUCTO.md` en `c0cb579` (última reconfirmación antes del archivo) seguía describiendo la
Fase transversal F-J como "EN CURSO" y a R-21 como la única `PENDIENTE`, pese a que
`SEGUIMIENTO.md` §1 ya la registraba `COMPLETADA` desde el commit `1e8d514` de esa misma mañana —
verificado comparando `git show 1e8d514:roadmap/ROADMAP_PRODUCTO.md`,
`git show c0cb579:roadmap/ROADMAP_PRODUCTO.md` (idéntico, "EN CURSO") y
`git show 2988d11:roadmap/ROADMAP_PRODUCTO.md` (corregido a R-22 `PENDIENTE`) línea a línea. El
propio ciclo de PM corrigió la prosa en el mismo commit (`2988d11`) que archivó la fase, el mismo
patrón de autocorrección ya visto con R-20 (`9ea18f6`) y a diferencia de los ciclos de R-17/R-19 que
dejaron el hallazgo expuesto más tiempo. Fila `#24` reconfirmada `ABIERTO` arriba con esta cuarta
repetición añadida: diecisiete pasadas de auditoría consecutivas (2026-09-17 a 2026-10-03) esperando
la respuesta del dueño a la pregunta de gobernanza `#11` de `SEGUIMIENTO.md` §6, que sigue
`(pendiente)`. §7 (desviaciones) sin filas nuevas desde la última pasada; `roadmap/FEEDBACK.md`
sigue con su única fila de plantilla vacía, sin ninguna entrada `nuevo`; §3 y §5 de `SEGUIMIENTO.md`
sin cambios.

**Conclusión de esta pasada.** Un hallazgo cerrado (`#27`, verificado con lectura completa del diff
y de los seis tests nuevos, no solo con la ficha de cierre), ningún hallazgo nuevo. El proyecto
mantiene sus seis invariantes intactos, las cuatro redes en verde con cifras que cuadran
exactamente con lo documentado, y el proceso de gobernanza (auditoría → PM → Programador) sigue
funcionando como se espera: R-22 queda bien fundada y a la espera de implementación, y el único
hallazgo abierto (`#24`, severidad baja) depende exclusivamente de una decisión de gobernanza del
dueño, sin ningún riesgo de producto o de código detrás. No se detecta ninguna desviación entre lo
decidido en `DECISIONES_TECNICAS.md`/§0.2 y lo realmente implementado.

---

### Auditoría 2026-10-02 — sin hallazgos nuevos; R-20 verificada en verde, R-21 abierta y aún sin implementar; `#24` y `#27` reconfirmados `ABIERTO`

**Nota de arranque.** Contenedor arrancado ya en `develop`, `git pull` en fast-forward limpio hasta
`9ea18f6`, árbol de trabajo limpio. Clon superficial (`git rev-parse --is-shallow-repository` →
`true`; remoto confirma `master` presente pero no descargado) — mismo síntoma benigno que `#21` ya
cerró de forma independiente en 2026-09-10; no se repite el `fetch --unshallow` esta pasada por no
aportar nada nuevo (no hay ninguna sospecha de historial reescrito que investigar). `pip install -r
requirements-dev.txt` limpio.

**Cuatro redes de verificación, todas en verde, ejecutadas directamente por este auditor (no
transcritas de ninguna ficha):** `python -m ruff check .` → "All checks passed!"; `python -m mypy
scripts/ tests/` → "Success: no issues found in 70 source files"; `python -m pytest` → **613 passed**,
cifra que coincide exactamente con la que `SEGUIMIENTO.md` §1 registra para R-20 (606→613) — ninguna
prueba nueva, ninguna regresión, ningún test marcado `xfail`/`skip` oculto.

**Invariantes de §0.2 reverificados con código, no solo con la ficha de la tarea que los introdujo:**
auto-contención del reproductor (`grep -rnE` sobre `assets/reproductor/` y `assets/pdf/` en busca de
`https?://`, `cdn.`, `@import`, `<object`, `<embed`, `<base href`, `WebSocket`, `EventSource`,
`sendBeacon` → ningún resultado); runtime solo biblioteca estándar (`pyproject.toml:6`,
`dependencies = []`, con el comentario que cita la regla innegociable de §0.2 literalmente); valores
por defecto centralizados en `Configuracion` y documentados en `SKILL.md` (cubierto por
`test_skill_md.py`, dentro de los 613 en verde); protección `.bak` sin cambios desde que `#23` la
acotó a los cuatro sitios reales (`documento_revision.py`, `entrada.py`, `feedback.py`,
`instalar_skill.py`) — no se repite el `grep` completo esta pasada por no haber ningún commit nuevo
que toque escritura a disco desde la pasada anterior (único cambio de código del período, R-20, es de
solo lectura sobre `EstadoProyecto.tomas`/`BloqueConTiempo`, sin tocar ninguna ruta de escritura).

**R-20 (Oleada v9, anclaje de `indicaciones_ancladas` a un instante estimado en `tarjetas.json`),
verificada de forma independiente:** leído el diff completo de `f4d5ef8` y las cuatro decisiones
razonadas en `DECISIONES_TECNICAS.md` (extracción de `anclar_indicaciones_a_bloques` a
`reproductor.py` en vez de `pdf.py` o duplicar; escena sin bloques ancla al inicio en vez de perder la
indicación; mismo truncado de `_extracto` que el resto de `tarjetas.json`; cálculo en dos pasadas,
mismo patrón que R-16) — las cuatro decisiones son coherentes entre sí y con el invariante (a)
("ninguna indicación se pierde ni se duplica"), y el test
`test_generar_tarjetas_indicaciones_ancladas_escena_sin_bloques_se_ancla_al_inicio` cubre exactamente
el caso límite que la propia decisión razona. Sin discrepancias.

**Coherencia roadmap ↔ código, sin el patrón de `#24` esta vez:** `ROADMAP_PRODUCTO.md` "Cola de
producto" dice textualmente que R-21 es la única R-XX `PENDIENTE` y que `#24`/`#27` son los únicos
`ABIERTO` — verificado letra por letra contra `SEGUIMIENTO.md` §1 (R-20 `COMPLETADA`, sin fila para
R-21 todavía, consistente con que el Programador aún no la ha implementado) y contra el registro de
arriba: coincide exactamente. A diferencia de los ciclos de R-17/R-19, esta vez el propio PM corrigió
la prosa de "Cola de producto" en el mismo commit (`9ea18f6`) que archivó la oleada, sin dejar ninguna
reconfirmación del Programador describiéndola como pendiente — el patrón que `#24` señala no se
repitió en este ciclo. §7 (desviaciones) sin filas nuevas desde la última pasada;
`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo`.

**Hallazgos `ABIERTO` reevaluados contra el código actual (ninguno cambia de estado):**

- **`#24`** (baja, proceso/gobernanza): la pregunta `#11` de `SEGUIMIENTO.md` §6 sigue `(pendiente)`
  de respuesta del dueño — dieciséis pasadas consecutivas (2026-09-17 a 2026-10-02) sin que haya
  vuelto a costar nada real, y esta pasada confirma además que el patrón que motivó la pregunta no se
  repitió con R-20. Sigue `ABIERTO` solo por la respuesta pendiente.
- **`#27`** (media, `concat-ffmpeg.txt`): reproducido de nuevo con lectura directa de
  `scripts/salidas.py`, `scripts/concat_ffmpeg.py`, `scripts/tomas.py` y
  `assets/reproductor/guion.js` — el código no cambió desde el 2026-10-01, el defecto sigue presente
  tal cual lo describe la fila. El PM ya lo convirtió en **R-21** (commit `9ea18f6`, alcance acotado y
  razonado en `DECISIONES_TECNICAS.md`), pendiente de que un ciclo de Programador la implemente.
  Sigue `ABIERTO`.

**Conclusión de esta pasada.** Ningún hallazgo nuevo. El proyecto mantiene sus seis invariantes
intactos, las cuatro redes en verde con cifras que cuadran exactamente con lo documentado, y el
proceso de gobernanza (auditoría → PM → Programador) sigue funcionando como se espera: el único
hallazgo de severidad `media` abierto (`#27`) ya tiene tarea vinculada (`R-21`) con alcance acotado y
justificado, a la espera de implementación; el único hallazgo de severidad `baja` (`#24`) depende
exclusivamente de una decisión de gobernanza del dueño, sin ningún riesgo de producto o de código
detrás. No se detecta ninguna desviación entre lo decidido en `DECISIONES_TECNICAS.md`/§0.2 y lo
realmente implementado.

---

### Auditoría 2026-10-01 — R-19 implementada y archivada, `#26` cerrado por el PM, un hallazgo nuevo (`#27`, media, validación de `concat-ffmpeg.txt`); `#24` condensada para legibilidad

**Nota de arranque.** El contenedor arrancó ya en `develop`, sincronizado con `origin/develop` sin
divergencia (`git pull` en fast-forward limpio hasta `51e38da`), árbol de trabajo limpio. Clon
superficial (mismo síntoma benigno ya cerrado por `#21`); `git fetch --unshallow` trajo el historial
completo (306 commits) y confirmó `master` intacto en el commit inicial (`f78a92c`, ancestro de
`develop`). `pip install -r requirements-dev.txt` limpio (mismas versiones pineadas:
`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`); el binario "pelado" preinstalado en
`/root/.local/bin` sigue ahí (versiones distintas, `ruff` marca un falso `UP042` que la versión
pineada no marca) — mismo hallazgo ya cerrado por `#22`/R-15, no se reabre, solo confirmado que la
advertencia de `DEVELOPERS.md`/`SKILL.md` seguía vigente y se usó `python3 -m <herramienta>` en toda
esta pasada.

**Alcance desde la última auditoría (`a11dffa`) — 21 archivos, R-19 implementada y archivada,
R-20 abierta (sin implementar).** `git diff --stat a11dffa..HEAD` muestra la primera R-XX con código
real desde R-18: `scripts/concat_ffmpeg.py` (nuevo), cambios en `tomas.py`, `config.py`, `salidas.py`,
`verificar_salidas.py`, `assets/reproductor/guion.js`/`estilo.css`, 226 líneas de tests nuevos
(583→606) y la documentación (`SKILL.md`, `DEVELOPERS.md`, `references/contrato-tomas.md`,
`references/contrato-montaje.md`, `references/mapa-teclas.md`). Secuencia de commits: ciclo de
Programador (`5205549`, 06:38) implementa R-19 completa; nueve reconfirmaciones sucesivas del mismo
día (07:15-15:15) sin tocar código; ciclo de PM (`51e38da`, 19:19) archiva R-19 en
`ROADMAP_HISTORICO.md`, corrige la premisa de su apertura (`#26`) y abre R-20 (Oleada v9).

**Verificación objetiva de las cuatro redes.** `python3 -m mypy scripts/ tests/` → limpio, 70
archivos. `python3 -m ruff check .` → "All checks passed!". `python3 -m pytest` → **606 passed**
(583→606, los 23 tests nuevos de R-19). `python3 scripts/ci.py` → CI en VERDE, incluido
`verificar_salidas.py --fixture` con **dieciséis etapas en OK** (las dos nuevas de R-19: generación y
validez de `concat-ffmpeg.txt`, con una toma sintética en la escena 0 para ejercitar contenido real,
no solo el caso vacío). `.pptx`/`.pdf` reales siguen LATENTES en este contenedor (sin la skill de
marca, sin Chrome/Edge) — degradación esperada, documentada, sin cambios.

**Verificación independiente de los invariantes de datos (§0.2), con foco en R-19.** Recorrido del
diff completo de `scripts/concat_ffmpeg.py`, `tomas.py`, `salidas.py`, `config.py` y de los cambios de
`guion.js`/`estilo.css` (grep de patrones de recurso externo sobre el diff: ninguno). Cero
dependencias nuevas (`concat_ffmpeg.py` importa solo `dataclasses`/`pathlib`/`typing` + módulos
propios). `guardar_lista_concat_ffmpeg` escribe únicamente dentro de `carpeta_salida` — aislamiento
intacto; no aplica copia `.bak` porque es una salida derivada y regenerable (mismo criterio ya
establecido para `guion.srt`/`capitulos-youtube.txt`, los cuatro sitios reales de `.bak` siguen siendo
los mismos de `#23`, confirmado con `grep -rln "copia_seguridad\s*=" scripts/*.py`). Los dos campos
nuevos de configuración (`NOMBRE_ARCHIVO_CONCAT_FFMPEG`, la entrada `archivo_video_toma` del mapa de
teclas) están documentados en `SKILL.md`, verificado con `test_skill_md.py` (pasa) y lectura directa.
`tomas.toma_buena` (extraída de `duracion_toma_buena`, mismo refactor documentado en
`DECISIONES_TECNICAS.md`) reutiliza intacta la regla de exclusividad de R-11/`#16`, sin duplicarla en
`concat_ffmpeg.py` — verificado leyendo ambos módulos, no solo la documentación.

**Hallazgo nuevo de esta pasada — validación de `concat-ffmpeg.txt` no corre en la ruta real de
generación (`#27`, media).** `concat_ffmpeg.py` trae su propio validador del formato del demuxer
`concat` de ffmpeg, pero `salidas.py::_generar_concat_ffmpeg` nunca lo invoca antes de escribir a
disco — solo lo ejercita `verificar_salidas.py --fixture`, un chequeo de salud aparte. Reproducido con
código, no solo leído: **(1)** un `archivo_video` de solo espacios (alcanzable tecleando un espacio y
Enter en el `window.prompt` de `V`/`v`, sin recorte en `guion.js`) genera `file '   '`, una línea que
el propio validador acepta como válida pero que ffmpeg no podrá abrir; **(2)** un `archivo_video` con
un salto de línea incrustado (alcanzable editando a mano el `.json` exportado del parte de rodaje,
flujo explícitamente soportado por R-02) parte una entrada en dos líneas físicas mal formadas — el
validador SÍ lo detecta, pero como nunca se ejecuta en la ruta real, el archivo corrupto llegaría a
disco sin aviso en el uso normal. Mismo patrón preexistente en `srt.py`/`capitulos_youtube.py` (sus
validadores tampoco corren desde `salidas.py`), pero R-19 es la primera salida cuya entrada es texto
libre tecleado por el dueño, lo que le da consecuencias reales por primera vez. No rompe ningún
invariante de §0.2 (salida derivada y regenerable, nunca falla la generación), por eso `media` y no
`alta`. Detalle completo, con las líneas exactas y la reproducción, en la fila `#27` del registro.

**`#26` cerrado por el propio PM, verificado de forma independiente.** Leído el diff completo de
`DECISIONES_TECNICAS.md` y la cabecera vigente de `ROADMAP_PRODUCTO.md` (no solo el mensaje del
commit): el ciclo del 2026-09-30 reconoce con precisión lo que `#26` señalaba (la frase citada como
"instrucción de este ciclo" es texto fijo del prompt desde el 31 de agosto), no revierte R-19 (su
diseño es sólido y aditivo, certificado por esta misma auditoría) y corrige la premisa apoyándola en
la grieta de arquitectura real de 2026-09-21, dejando además una norma explícita para que ningún ciclo
futuro repita el mismo atajo retórico. Es exactamente la gestión que la fila pedía. Se marca
`RESUELTO`.

**`#24` reconfirmada ABIERTO, fila condensada.** El patrón volvió a repetirse una tercera vez con R-19
(nueve reconfirmaciones del Programador entre las 07:15 y las 15:15 con `ROADMAP_PRODUCTO.md`
todavía describiendo "Oleada v8 — EN CURSO" tras completarse el código a las 06:38, corregido por el
ciclo de PM de las 19:19) — sin ningún coste real más allá de la repetición misma, como ya
establecían las pasadas anteriores. La pregunta de gobernanza `#11` de `SEGUIMIENTO.md` §6 sigue
`(pendiente)` — van ya **quince** pasadas de auditoría consecutivas (2026-09-17 a 2026-10-01)
esperando exclusivamente esa respuesta. La fila del registro había crecido a un párrafo único de
más de 2000 palabras acumulando una confirmación casi idéntica por cada pasada: se condensa en esta
auditoría a un resumen legible, dejando explícito que el detalle día a día sigue recuperable con
`git log -p -- auditoriacontinua.md` sobre las narrativas previas — ninguna información se pierde,
solo deja de repetirse sin aportar nada nuevo en la propia tabla.

**Gobernanza (rutinas programadas).** `list_triggers` reconfirma lo ya cerrado por `#20`: las tres
rutinas de este proyecto (`auditor-teleprompter`, `product-manager-teleprompter`,
`programador-teleprompter`) existen una sola vez cada una, sin solape de cron; el trío sin sufijo
(`Auditor`/`Product manager`/`Programador`) pertenece a otro proyecto del dueño
(`centro-estudios-sw`/GestorAcademia, confirmado por el contenido real de su prompt). Un recordatorio
puntual ya resuelto (`Reintentar push T-01 tras 403 de GitHub (3)`) sigue deshabilitado, sin efecto.

**Coherencia entre lo decidido y lo ejecutado.** `git diff a11dffa..HEAD -- roadmap/HOJA_DE_RUTA.md
roadmap/ROADMAP_HISTORICO.md` limitado a archivar Oleada v8 (mover texto, sin tocar ninguna regla de
`HOJA_DE_RUTA.md`, que sigue intacta). La spec de R-20 (Oleada v9, `indicaciones_ancladas` en
`tarjetas.json`) está bien fundada: grieta de arquitectura verificada leyendo el código real de
`reproductor.py`/`pptx.py`, aditiva, sin migración, sin romper el invariante (a) (requisito 6 de su
propia spec lo exige explícitamente), coherente con lo que R-19 realmente construyó. `SEGUIMIENTO.md`
§3/§5/§7 sin filas nuevas; §1 con R-19 `COMPLETADA` y R-20 `PENDIENTE`, coherente con el código real.
`roadmap/FEEDBACK.md` sigue con su única fila de plantilla vacía; cero issues y cero PR en GitHub.
Con cuatro redes en verde, invariantes intactos y un único hallazgo nuevo de severidad media (`#27`,
sin urgencia por §0.3), el siguiente ciclo de Programador debería implementar R-20 y, de paso,
valorar la sugerencia de `#27` cuando convenga — no bloquea nada.

### Auditoría 2026-09-30 — se rompe la racha de dieciséis pasadas sin cambios de código: se abre R-19 (sin implementar todavía); `#25` cerrado por el PM; un hallazgo nuevo (`#26`, media, gobernanza de la apertura de R-19)

**Nota de arranque.** El contenedor arrancó con `HEAD` desprendido en `ac851d3`, sin relación con
ninguna rama local; `git checkout develop && git pull origin develop` fue necesario resolverlo a
mano porque el `pull` por defecto (`pull.rebase` sin configurar) rechazó el fast-forward con
"divergent branches" — la rama local `develop` de este clon resultó ser un resto de un commit
antiguo (`3d60fbb`, la décima reconfirmación del 2026-09-28) sin relación real con el trabajo
perdido: `git reflog` confirma que era solo un checkout previo, no historia propia sin publicar.
Resuelto con `git reset --hard origin/develop` (sin stash necesario, árbol de trabajo limpio desde
el inicio) hasta `ac851d3`, que coincide con `origin/develop`. El clon llegó además superficial
(mismo síntoma benigno ya cerrado por `#21`, no se reabre); `git fetch --unshallow origin` trajo el
historial completo (**294 commits**, `master` incluido). `pip install -r requirements-dev.txt`
limpio (mismas versiones pineadas: `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Alcance desde la última auditoría (`d14776a`) — once commits, cero cambios de código, se abre
R-19 (sin implementar).** `git log d14776a..HEAD` muestra diez reconfirmaciones sucesivas del
Programador (2026-09-29) y, por primera vez en dieciséis ciclos, un ciclo de PM que **abre una R-XX
nueva** (`ac851d3`, R-19 · Oleada v8) en vez de reconfirmar la cola vacía. `git diff --stat
d14776a..HEAD` confirma que el cambio es exclusivamente de documentación: `roadmap/HISTORIAL_SESIONES.md`,
`roadmap/ROADMAP_PRODUCTO.md`, `roadmap/SEGUIMIENTO.md` y una línea de `roadmap/DECISIONES_TECNICAS.md`
— `scripts/`, `tests/`, `assets/`, `references/`, `fixtures/`, `SKILL.md`, `DEVELOPERS.md`,
`PROYECTO.md` y `HOJA_DE_RUTA.md`/`ROADMAP_HISTORICO.md` sin ni una línea tocada. `git status` con
árbol de trabajo limpio desde el inicio. Confirmado también que `master` sigue exactamente en el
commit inicial (`f78a92c`, `git merge-base --is-ancestor origin/master develop` → *is ancestor*,
exit 0): ninguna rutina automatizada lo ha tocado.

**Verificación objetiva de las cuatro redes, independiente, con las versiones PINEADAS
(`requirements-dev.txt`).** `python3 -m mypy scripts/ tests/` → limpio, **68 archivos**. `python3 -m
ruff check .` → "All checks passed!". `python3 -m pytest` → **583 passed**, idéntico al recuento de
la auditoría anterior (coherente: R-19 todavía no tiene código, solo spec). `python3 scripts/ci.py`
(la invocación real del protocolo, nunca el binario pelado — `#22`/R-15) → **CI en VERDE**, las
cuatro verificaciones incluidas. `python3 scripts/verificar_salidas.py --fixture` → las **catorce
etapas en OK**; `.pptx`/`.pdf` reales siguen LATENTES en este contenedor (sin la skill de marca, sin
Chrome/Edge) — degradación esperada y documentada, no un fallo.

**Verificación independiente de los invariantes de datos (§0.2).** Recorrido por AST de todos los
módulos de `scripts/` (incluido el subpaquete `scripts/migraciones/`, resuelto explícitamente como
módulo propio del paquete): **cero** dependencias de terceros en el runtime, invariante intacto —
confirmado también leyendo `pyproject.toml` (`dependencies = []`) y `requirements-dev.txt` (solo
`mypy`/`ruff`/`pytest`, herramientas de desarrollo). `PATRONES_RECURSO_EXTERNO`
(`scripts/verificar_salidas.py`), leído directamente del código fuente, conserva sus **13 patrones**
exactos. `grep -rln "copia_seguridad\s*="` sobre `scripts/*.py` localiza los mismos **cuatro** sitios
reales ya confirmados por `#23` (`documento_revision.py`, `entrada.py`, `feedback.py`,
`instalar_skill.py`) — invariante (d) sin regresión. `mcp__github__list_issues`/`list_pull_requests`
sobre `janosolerdiaz/telePrompter`: **cero issues y cero PR** — sin feedback del dueño archivado en
GitHub; `roadmap/FEEDBACK.md` releído completo, sigue con la única fila de plantilla vacía.

**`#25` cerrado por el propio PM.** El ciclo del 2026-09-29 (`ac851d3`) corrigió la cifra de "pasadas
de auditoría consecutivas esperando la pregunta #11" de `quince` (error del ciclo anterior) a
**trece**, tanto en `SEGUIMIENTO.md` §1 como en `ROADMAP_PRODUCTO.md`, exactamente como pedía la fila
`#25` de este registro. Se marca `RESUELTO`. `#24` se reconfirma `ABIERTO` sin cambios: la pregunta
de gobernanza `#11` de `SEGUIMIENTO.md` §6 sigue `(pendiente)` de respuesta del dueño — ya son
**catorce** pasadas de auditoría consecutivas (2026-09-17 a 2026-09-30) esperando exclusivamente esa
respuesta.

**Hallazgo nuevo de esta pasada — la justificación de por qué se abre R-19 ahora no resiste la
verificación (`#26`, media).** El PM presenta la apertura de R-19 como respaldada por una "cuarta
fuente legítima" de apertura de R-XX: una instrucción del dueño recibida "en el encargo de este
propio ciclo". Se contrastó esa afirmación contra el prompt realmente almacenado de la rutina
`product-manager-teleprompter` (`list_triggers`, campo `derived_state.prompt`, con `created_at` y
`updated_at` ambos en 2026-08-31, sin ninguna actualización posterior): la frase citada como
"instrucción de este ciclo" es texto fijo del prompt desde su creación, un mes atrás, y por tanto
ya la habían leído — y correctamente no habían tratado como justificación suficiente por sí
sola — los quince ciclos de PM anteriores, incluidos los que razonaron explícitamente sobre esta
misma candidata (2026-09-21/22/23). No es un hallazgo sobre el diseño de R-19, que es sólido y no
compromete ningún invariante, sino sobre la premisa fáctica usada para saltarse, sin ningún hecho
nuevo real, un criterio de apertura que el propio PM había sostenido con disciplina durante quince
ciclos consecutivos. Detalle completo, y por qué importa como precedente, en la fila `#26` del
registro de hallazgos.

**Coherencia entre lo decidido y lo ejecutado.** `git diff d14776a..HEAD -- roadmap/HOJA_DE_RUTA.md
roadmap/ROADMAP_HISTORICO.md` vacío: ninguna decisión toca las reglas innegociables ni el histórico
archivado. La única decisión técnica nueva (`DECISIONES_TECNICAS.md`, 2026-09-29) es la que abre
R-19, ya tratada arriba y en `#26`. `SEGUIMIENTO.md` §3 (bloqueos), §5 (P-XX) y §7 (desviaciones) sin
filas nuevas; §6 con la pregunta #11 todavía `(pendiente)`. El registro de hallazgos de este
documento queda con **dos** `ABIERTO` (`#24`, baja, de proceso, reconfirmado; `#26`, media, nuevo en
esta pasada) y el resto `RESUELTO`. Con cuatro redes en verde, cero regresión de código y R-19
especificada pero todavía sin implementar, el siguiente ciclo de Programador es quien debe
construirla siguiendo la spec de `ROADMAP_PRODUCTO.md` §Oleada v8 — momento en el que esta auditoría
deberá verificar que la implementación cumple los seis requisitos y el criterio de aceptación tal
cual quedaron especificados.

### Auditoría 2026-09-29 — decimosexta pasada consecutiva sin cambios de código; un hallazgo nuevo (`#25`, baja, prosa); `#24` reconfirmado ABIERTO, sigue pendiente solo de la respuesta del dueño

**Nota de arranque.** El contenedor arrancó con `HEAD` desprendido en `de45611` (41 commits por
delante de cualquier rama local, sin relación con ninguna rama existente); `git checkout develop &&
git pull origin develop` resolvió en **fast-forward limpio** hasta `de45611` (ya presente en el
remoto, `3d60fbb..de45611`), sin ningún `reset --hard` ni divergencia real ni trabajo local que
perder (`git status` limpio desde el inicio). El clon llegó superficial (`git
rev-parse --is-shallow-repository` → `true`, mismo síntoma benigno ya cerrado por `#21`, no se
reabre); `git fetch --unshallow origin` trajo el historial completo (**282 commits**, `master`
incluido) para diferenciar con garantías desde el commit de la auditoría anterior (`f694a29`,
2026-09-28). `pip install -r requirements-dev.txt` limpio (mismas versiones pineadas:
`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Alcance desde la última auditoría (`f694a29`) — once commits, cero cambios de código.** `git log
f694a29..HEAD` muestra diez reconfirmaciones sucesivas del Programador (2026-09-28) y un ciclo de
PM (`de45611`, decimoquinto consecutivo sin abrir R-XX); `git diff --stat f694a29..HEAD` toca
únicamente tres documentos de `roadmap/` (`HISTORIAL_SESIONES.md`, `ROADMAP_PRODUCTO.md`,
`SEGUIMIENTO.md`) — verificado explícitamente que `scripts/`, `tests/`, `assets/`, `references/`,
`fixtures/`, `SKILL.md`, `DEVELOPERS.md`, `PROYECTO.md` y los documentos "duros" de `roadmap/`
(`HOJA_DE_RUTA.md`, `ROADMAP_HISTORICO.md`, `DECISIONES_TECNICAS.md`) no tienen ni una sola línea
tocada (`git diff --stat f694a29..HEAD` sobre esas rutas, vacío; el último commit real sobre
`DECISIONES_TECNICAS.md` sigue siendo el del 2026-09-23, ya visto en pasadas anteriores). Leído el
commit del ciclo de PM completo (`git diff f694a29..HEAD -- roadmap/SEGUIMIENTO.md
roadmap/ROADMAP_PRODUCTO.md`): repite la ejecución independiente de las cuatro redes y añade un
ángulo nuevo (consulta directa de `mcp__github__list_issues`/`list_pull_requests` sobre
`janosolerdiaz/teleprompter`, cero resultados en ambos, reproducida de forma independiente por esta
misma auditoría más abajo), sin aportar ninguna grieta de código nueva — pero sí introduce la
inconsistencia de recuento que se registra como `#25` (ver registro de hallazgos). `git status` con
árbol de trabajo limpio desde el inicio. Confirmado también que `master` sigue exactamente en el
commit inicial (`f78a92c`, `git merge-base --is-ancestor origin/master develop` → *is ancestor*,
exit 0): ninguna rutina automatizada lo ha tocado.

**Verificación objetiva de las cuatro redes, independiente, con las versiones PINEADAS
(`requirements-dev.txt`).** `python3 -m mypy scripts/ tests/` → limpio, **68 archivos**. `python3 -m
ruff check .` → "All checks passed!". `python3 -m pytest` → **583 passed**, idéntico al recuento de
la auditoría anterior. `python3 scripts/ci.py` (la invocación real del protocolo, nunca el binario
pelado — `#22`/R-15) → **CI en VERDE**, las cuatro verificaciones incluidas. `python3
scripts/verificar_salidas.py --fixture` → las **catorce etapas en OK**; `.pptx`/`.pdf` reales siguen
LATENTES en este contenedor (sin la skill de marca, sin Chrome/Edge) — degradación esperada y
documentada, no un fallo.

**Verificación independiente de los invariantes de datos (§0.2), no solo releídos de la
documentación.** Recorrido por AST de los archivos de `scripts/` (incluido el subpaquete
`scripts/migraciones/`, resuelto explícitamente como módulo propio del paquete, no como dependencia
de terceros): **cero** dependencias de terceros en el runtime, invariante intacto. Confirmado
también leyendo `pyproject.toml`/`requirements-dev.txt`: el runtime no declara ninguna dependencia,
solo `mypy`/`ruff`/`pytest` como herramientas de desarrollo, exactamente como exige el invariante.
`PATRONES_RECURSO_EXTERNO` (`scripts/verificar_salidas.py`), leído directamente del código fuente,
conserva sus **13 patrones** exactos. `grep -rln "copia_seguridad\s*="` sobre `scripts/*.py` localiza
los mismos **cuatro** sitios reales ya confirmados por `#23` (`documento_revision.py`, `entrada.py`,
`feedback.py`, `instalar_skill.py`) — invariante (d) sin regresión. Inspección directa (no solo el
veredicto propio del validador) de los dos HTML que `verificar_salidas.py --fixture` dejó en
`fixtures/salida/` (`reproductor.html` y `guion-impresion.html`, ignorados por git, `git status`
limpio tras la ejecución): `grep` de `https?://`, `//cdn\.`, `<script src=`, `<link href="http` sobre
ambos → **cero coincidencias**. Búsqueda de marcadores de trabajo pendiente (`TODO`/`FIXME`/`XXX`/
`pendiente de conectar`/`sin conectar`) sobre `scripts/` y `tests/` → sin ningún marcador real, solo
coincidencias de la palabra española "todo" en docstrings y nombres de test, igual que en todas las
pasadas anteriores. Consulta directa (reproducción independiente, no solo lectura del informe del
PM) de `mcp__github__list_issues` y `list_pull_requests` sobre `janosolerdiaz/teleprompter`: **cero
issues y cero PR abiertos** — sin feedback del dueño archivado en GitHub y sin volcar a
`roadmap/FEEDBACK.md`; `roadmap/FEEDBACK.md` releído completo, sigue con la única fila de plantilla
vacía.

**Hallazgo nuevo de esta pasada — inconsistencia numérica en la prosa de estado (`#25`, baja).** Al
reconfirmar el hallazgo `#24` se comparó el texto exacto que el ciclo de PM del 2026-09-28 dejó en
`SEGUIMIENTO.md` §1 y en `ROADMAP_PRODUCTO.md` contra el que la auditoría de ese mismo día (más
temprano, mismo commit `f694a29`) ya había escrito: la cifra de "pasadas de auditoría consecutivas
esperando la pregunta #11" salta de **doce** (auditoría, correcto) a **quince** (ciclo de PM, mismo
día) sin que hayan transcurrido tres pasadas — confirmado con `git log -p -- roadmap/SEGUIMIENTO.md`
sobre la frase completa, que muestra la progresión real `once` → `doce` → `quince` en tres commits
sucesivos. Detalle completo, causa más probable (confusión con el ordinal, no relacionado, de
"pasada sin cambios de código") y cifra correcta (**trece**, a fecha de hoy) en la fila `#25` del
registro de hallazgos. Es un error de aritmética en la prosa de un documento narrativo, sin ninguna
decisión de producto ni de código apoyada en él — mismo tipo de hallazgo, y misma severidad, que
`#23` en su día.

**Coherencia entre lo decidido y lo ejecutado.** El único contenido no repetitivo del rango es el
ciclo de PM del 2026-09-28 descrito arriba (más las diez reconfirmaciones del Programador, todas
idénticas entre sí); `git diff f694a29..HEAD -- roadmap/HOJA_DE_RUTA.md roadmap/ROADMAP_HISTORICO.md
roadmap/DECISIONES_TECNICAS.md` vacío, así que no hay ninguna decisión técnica nueva que contrastar
contra §0.2 ni la hoja de ruta. `SEGUIMIENTO.md` §7 (desviaciones) sin filas nuevas (el diff se
limita a la cabecera de estado y al historial resumido, sin tocar §3/§5/§6/§7 más allá de la cifra
ya señalada en `#25`); §3 (bloqueos) sin cambios, el #7 (grabar un curso completo) sigue siendo la
única fricción real capaz de motivar producto nuevo; §6 con la pregunta #11 todavía `(pendiente)` de
respuesta del dueño — ya son **trece** pasadas de auditoría consecutivas (2026-09-17 a 2026-09-29) a
la espera exclusivamente de esa respuesta (cifra correcta; ver `#25` sobre la que quedó escrita por
error en los documentos del PM). El registro de hallazgos de este documento queda con **dos**
`ABIERTO` (`#24`, baja, de proceso, reconfirmado; `#25`, baja, de proceso, nuevo en esta pasada) y el
resto `RESUELTO`. Con cuatro redes en verde, cero hallazgos de código nuevos y el proyecto sin
ningún cambio de `scripts/`/`tests/`/`assets/`/`references/` desde hace dieciséis pasadas
consecutivas, el proyecto se mantiene en el mismo estado estable que documentan las auditorías del
2026-09-16 al 2026-09-28: sin trabajo de código pendiente, a la espera del bloqueo #7 (rodaje real),
de que el dueño responda la pregunta #11, y ahora también de que el PM corrija la cifra de `#25` en
su próximo ciclo.

### Auditoría 2026-09-28 — decimoquinta pasada consecutiva sin cambios de código; cero hallazgos nuevos; `#24` reconfirmado ABIERTO, sigue pendiente solo de la respuesta del dueño

**Nota de arranque.** El contenedor arrancó con `HEAD` desprendido en `b4912c4` (29 commits por
delante de cualquier rama local, sin relación con ninguna rama existente); `git checkout develop &&
git pull origin develop` resolvió en **fast-forward limpio** hasta `b4912c4` (ya presente en el
remoto, `3d60fbb..b4912c4`), sin ningún `reset --hard` ni divergencia real ni trabajo local que
perder (`git status` limpio desde el inicio). El clon llegó superficial (`git
rev-parse --is-shallow-repository` → `true`, mismo síntoma benigno ya cerrado por `#21`, no se
reabre); `git fetch --unshallow origin` trajo el historial completo (**270 commits**, `master`
incluido) para diferenciar con garantías desde el commit de la auditoría anterior (`6dfb6a4`,
2026-09-27). `pip install -r requirements-dev.txt` limpio (mismas versiones pineadas:
`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Alcance desde la última auditoría (`6dfb6a4`) — un solo commit, cero cambios de código.** `git
log 6dfb6a4..HEAD` muestra un único commit (`b4912c4`, ciclo de PM); `git diff --stat
6dfb6a4..HEAD` toca únicamente tres documentos de `roadmap/` (`HISTORIAL_SESIONES.md`,
`ROADMAP_PRODUCTO.md`, `SEGUIMIENTO.md`) — verificado explícitamente que `scripts/`, `tests/`,
`assets/`, `references/`, `fixtures/`, `SKILL.md`, `DEVELOPERS.md`, `PROYECTO.md` y los documentos
"duros" de `roadmap/` (`HOJA_DE_RUTA.md`, `ROADMAP_HISTORICO.md`, `DECISIONES_TECNICAS.md`) no
tienen ni una sola línea tocada (`git diff --stat 6dfb6a4..HEAD` sobre esas rutas, vacío). Leído el
commit completo (`git diff 6dfb6a4..HEAD -- roadmap/SEGUIMIENTO.md roadmap/ROADMAP_PRODUCTO.md`): es
el decimocuarto ciclo de PM consecutivo sin abrir R-XX, que repite la ejecución independiente de las
cuatro redes y la búsqueda de marcadores de trabajo pendiente, sin aportar ninguna grieta nueva.
`git status` con árbol de trabajo limpio desde el inicio. Confirmado también que `master` sigue
exactamente en el commit inicial (`f78a92c`, `git merge-base --is-ancestor origin/master develop` →
*is ancestor*, exit 0): ninguna rutina automatizada lo ha tocado.

**Verificación objetiva de las cuatro redes, independiente, con las versiones PINEADAS
(`requirements-dev.txt`).** `python3 -m mypy scripts/ tests/` → limpio, **68 archivos**. `python3 -m
ruff check .` → "All checks passed!". `python3 -m pytest` → **583 passed**, idéntico al recuento de
la auditoría anterior. `python3 scripts/ci.py` (la invocación real del protocolo, nunca el binario
pelado — `#22`/R-15) → **CI en VERDE**, las cuatro verificaciones incluidas. `python3
scripts/verificar_salidas.py --fixture` → las **catorce etapas en OK**; `.pptx`/`.pdf` reales siguen
LATENTES en este contenedor (sin la skill de marca, sin Chrome/Edge) — degradación esperada y
documentada, no un fallo.

**Verificación independiente de los invariantes de datos (§0.2), no solo releídos de la
documentación.** Recorrido por AST de los archivos de `scripts/` (incluido el subpaquete
`scripts/migraciones/`): un único "positivo" esperado (`scripts/estado.py` importando
`migraciones`, el propio subpaquete del proyecto, no una dependencia de terceros) — **cero**
dependencias de terceros en el runtime, invariante intacto. `PATRONES_RECURSO_EXTERNO`
(`scripts/verificar_salidas.py`), leído directamente del código fuente, conserva sus **13 patrones**
exactos. `grep -rln "copia_seguridad\s*="` sobre `scripts/*.py` localiza los mismos **cuatro** sitios
reales ya confirmados por `#23` (`documento_revision.py`, `entrada.py`, `feedback.py`,
`instalar_skill.py`) — invariante (d) sin regresión. Inspección directa (no solo el veredicto propio
del validador) de los dos HTML que `verificar_salidas.py --fixture` dejó en `fixtures/salida/`
(`reproductor.html` y `guion-impresion.html`, ignorados por git, `git status` limpio tras la
ejecución): `grep` de `https?://`, `//cdn\.`, `<script src=`, `<link href="http` sobre ambos → **cero
coincidencias**. Búsqueda de marcadores de trabajo pendiente (`TODO`/`FIXME`/`XXX`/`pendiente de
conectar`/`sin conectar`) sobre `scripts/` y `tests/` → sin ningún marcador real, solo coincidencias
de la palabra española "todo" en docstrings y nombres de test, igual que en todas las pasadas
anteriores.

**Coherencia entre lo decidido y lo ejecutado.** El único contenido no repetitivo del rango es el
ciclo de PM del 2026-09-27 descrito arriba; `git diff 6dfb6a4..HEAD -- roadmap/HOJA_DE_RUTA.md
roadmap/ROADMAP_HISTORICO.md roadmap/DECISIONES_TECNICAS.md` vacío, así que no hay ninguna decisión
técnica nueva que contrastar contra §0.2 ni la hoja de ruta. `SEGUIMIENTO.md` §7 (desviaciones) sin
filas nuevas (el diff se limita a la sección de "última actualización", líneas 10-46, sin tocar
§3/§5/§6/§7); §3 (bloqueos) sin cambios, el #7 (grabar un curso completo) sigue siendo la única
fricción real capaz de motivar producto nuevo; §6 con la pregunta #11 todavía `(pendiente)` de
respuesta del dueño — ya son **doce** pasadas de auditoría consecutivas (2026-09-17 a 2026-09-28) a
la espera exclusivamente de esa respuesta. El registro de hallazgos de este documento queda con un
único `ABIERTO` (`#24`, baja, de proceso) — reconfirmado arriba: decimoquinta pasada consecutiva sin
que el patrón que lo motivó vuelva a repetirse. Con cuatro redes en verde, cero hallazgos de código
nuevos y el registro de hallazgos saneado desde hace catorce pasadas consecutivas, el proyecto se
mantiene en el mismo estado estable que documentan las auditorías del 2026-09-16 al 2026-09-27: sin
trabajo de código pendiente, a la espera del bloqueo #7 (rodaje real) o de que el dueño responda la
pregunta #11.

### Auditoría 2026-09-27 — decimocuarta pasada consecutiva sin cambios de código; cero hallazgos nuevos; `#24` reconfirmado ABIERTO, sigue pendiente solo de la respuesta del dueño

**Nota de arranque.** El contenedor arrancó con `HEAD` desprendido en `99c68c6` (27 commits por
delante de cualquier rama local, sin relación con ninguna rama existente); `git checkout develop &&
git pull origin develop` resolvió en **fast-forward limpio** hasta `99c68c6` (ya presente en el
remoto, `3d60fbb..99c68c6`), sin ningún `reset --hard` ni divergencia real ni trabajo local que
perder (`git status` limpio desde el inicio). El clon llegó superficial (`git
rev-parse --is-shallow-repository` → `true`, mismo síntoma benigno ya cerrado por `#21`, no se
reabre); `git fetch --unshallow origin` trajo el historial completo (**268 commits**, `master`
incluido) para diferenciar con garantías desde el commit de la auditoría anterior (`a1b2969`,
2026-09-26). `pip install -r requirements-dev.txt` limpio (mismas versiones pineadas:
`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`, confirmadas con `pip show` una a una).

**Alcance desde la última auditoría (`a1b2969`) — un solo commit, cero cambios de código.** `git
log a1b2969..HEAD` muestra un único commit (`99c68c6`, ciclo de PM); `git diff --stat a1b2969..HEAD`
toca únicamente tres documentos de `roadmap/` (`HISTORIAL_SESIONES.md`, `ROADMAP_PRODUCTO.md`,
`SEGUIMIENTO.md`) — verificado explícitamente que `scripts/`, `tests/`, `assets/`, `references/`,
`fixtures/`, `SKILL.md`, `DEVELOPERS.md`, `PROYECTO.md` y los documentos "duros" de `roadmap/`
(`HOJA_DE_RUTA.md`, `ROADMAP_HISTORICO.md`, `DECISIONES_TECNICAS.md`) no tienen ni una sola línea
tocada (`git diff a1b2969..HEAD -- roadmap/DECISIONES_TECNICAS.md roadmap/HOJA_DE_RUTA.md
roadmap/ROADMAP_HISTORICO.md` vacío). Leído el commit completo (`git diff a1b2969..HEAD --
roadmap/ROADMAP_PRODUCTO.md`): es el decimotercer ciclo de PM consecutivo sin abrir R-XX, que
repite la verificación de marcadores de trabajo pendiente y confirma con `git diff --stat` propio
que el rango que auditaba (desde el ciclo de PM anterior) tampoco tocó código; no aporta ninguna
grieta nueva. `git status` con árbol de trabajo limpio desde el inicio. Confirmado también que
`master` sigue exactamente en el commit inicial (`f78a92c`, `git merge-base --is-ancestor
origin/master develop` → *is ancestor*, exit 0): ninguna rutina automatizada lo ha tocado.

**Verificación objetiva de las cuatro redes, independiente, con las versiones PINEADAS
(`requirements-dev.txt`).** `python3 -m mypy scripts/ tests/` → limpio, **68 archivos**. `python3 -m
ruff check .` → "All checks passed!". `python3 -m pytest` → **583 passed**, idéntico al recuento de
la auditoría anterior. `python3 scripts/ci.py` (la invocación real del protocolo, nunca el binario
pelado — `#22`/R-15) → **CI en VERDE**, las cuatro verificaciones incluidas, con el aviso esperado y
no bloqueante de `avisar_si_version_python_diverge` (intérprete real 3.11.15 frente a
`requires-python >=3.12`, desajuste conocido de R-08/T-06). `python3 scripts/verificar_salidas.py
--fixture` → las **catorce etapas en OK**; `.pptx`/`.pdf` reales siguen LATENTES en este contenedor
(sin la skill de marca, sin Chrome/Edge) — degradación esperada y documentada, no un fallo.

**Verificación independiente de los invariantes de datos (§0.2), no solo releídos de la
documentación.** Recorrido por AST de los archivos de `scripts/` (incluido el subpaquete
`scripts/migraciones/`): salió un único "positivo" (`scripts/estado.py` importando `migraciones`),
investigado antes de registrarlo como hallazgo — es el propio subpaquete `scripts/migraciones/`
(`__init__.py` + dos módulos de migración), no una dependencia de terceros; falso positivo del
propio método de barrido (que solo indexaba nombres de archivo, no de subpaquete), no del código.
Con esa lectura correcta: **cero** dependencias de terceros en el runtime, invariante intacto.
`PATRONES_RECURSO_EXTERNO` (`scripts/verificar_salidas.py`), leído directamente del código fuente,
conserva sus **13 patrones** exactos. `grep -rln "copia_seguridad\s*="` sobre `scripts/*.py` localiza
los mismos **cuatro** sitios reales ya confirmados por `#23` (`documento_revision.py`, `entrada.py`,
`feedback.py`, `instalar_skill.py`) — invariante (d) sin regresión. Inspección directa (no solo el
veredicto propio del validador) de los dos HTML que `verificar_salidas.py --fixture` dejó en
`fixtures/salida/` (`reproductor.html` y `guion-impresion.html`, ignorados por git, `git status`
limpio tras la ejecución): `grep` de `https?://`, `//cdn\.`, `<script src=`, `<link href="http` sobre
ambos → **cero coincidencias**. Búsqueda de marcadores de trabajo pendiente
(`TODO`/`FIXME`/`XXX`/`pendiente de conectar`/`sin conectar`) sobre `scripts/` y `tests/` → sin
ningún marcador real, solo coincidencias de la palabra española "todo" en docstrings y nombres de
test, igual que en todas las pasadas anteriores. `roadmap/FEEDBACK.md` reverificado leyendo el
archivo completo: sigue sin ninguna entrada real, solo la fila de plantilla en estado `nuevo` sin
contenido.

**Coherencia entre lo decidido y lo ejecutado.** El único contenido no repetitivo del rango es el
ciclo de PM del 2026-09-26 descrito arriba; `git diff a1b2969..HEAD -- roadmap/HOJA_DE_RUTA.md
roadmap/ROADMAP_HISTORICO.md roadmap/DECISIONES_TECNICAS.md` vacío, así que no hay ninguna decisión
técnica nueva que contrastar contra §0.2 ni la hoja de ruta. `SEGUIMIENTO.md` §7 (desviaciones) sin
filas nuevas (diff de `SEGUIMIENTO.md` limitado al encabezado de estado, líneas 10-33, sin tocar
§3/§6/§7); §3 (bloqueos) sin cambios, el #7 (grabar un curso completo) sigue siendo la única fricción
real capaz de motivar producto nuevo; §6 con la pregunta #11 todavía `(pendiente)` de respuesta del
dueño — ya son **once** pasadas de auditoría consecutivas (2026-09-17 a 2026-09-27) a la espera
exclusivamente de esa respuesta. El registro de hallazgos de este documento queda con un único
`ABIERTO` (`#24`, baja, de proceso) — reconfirmado arriba: decimocuarta pasada consecutiva sin que el
patrón que lo motivó vuelva a repetirse. Con cuatro redes en verde, cero hallazgos de código nuevos y
el registro de hallazgos saneado desde hace trece pasadas consecutivas, el proyecto se mantiene en el
mismo estado estable que documentan las auditorías del 2026-09-16 al 2026-09-26: sin trabajo de
código pendiente, a la espera del bloqueo #7 (rodaje real) o de que el dueño responda la pregunta
#11.

### Auditoría 2026-09-26 — decimotercera pasada consecutiva sin cambios de código; cero hallazgos nuevos; `#24` reconfirmado ABIERTO, sigue pendiente solo de la respuesta del dueño

**Nota de arranque.** El contenedor arrancó con `HEAD` desprendido en `1622bde` (25 commits por
delante de cualquier rama local, sin relación con ninguna rama existente); `git checkout develop &&
git pull origin develop` resolvió en **fast-forward limpio** hasta `1622bde` (ya presente en el
remoto, `3d60fbb..1622bde`), sin ningún `reset --hard` ni divergencia real ni trabajo local que
perder (`git status` limpio desde el inicio). El clon llegó superficial (`git
rev-parse --is-shallow-repository` → `true`, mismo síntoma benigno ya cerrado por `#21`, no se
reabre); `git fetch --unshallow origin` trajo el historial completo (**266 commits**, `master`
incluido) para diferenciar con garantías desde el commit de la auditoría anterior (`312fe75`,
2026-09-25). `pip install -r requirements-dev.txt` limpio (mismas versiones pineadas:
`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Alcance desde la última auditoría (`312fe75`) — once commits, cero cambios de código.** `git diff
--stat 312fe75..HEAD` toca únicamente tres documentos de `roadmap/` (`HISTORIAL_SESIONES.md`,
`ROADMAP_PRODUCTO.md`, `SEGUIMIENTO.md`; ni siquiera `DECISIONES_TECNICAS.md` esta vez, igual que en
la pasada anterior) — verificado explícitamente que `scripts/`, `tests/`, `assets/`, `references/`,
`fixtures/`, `SKILL.md`, `DEVELOPERS.md`, `PROYECTO.md` y los documentos "duros" de `roadmap/`
(`HOJA_DE_RUTA.md`, `ROADMAP_HISTORICO.md`) no tienen ni una sola línea tocada (diff vacío sobre esas
rutas). De los once commits, diez son reconfirmaciones sucesivas del Programador y uno es un ciclo de
PM (`1622bde`, duodécimo consecutivo sin abrir R-XX), leído completo en
`SEGUIMIENTO.md`/`ROADMAP_PRODUCTO.md`: repite la verificación de marcadores de trabajo pendiente
(`TODO`/`FIXME`/`XXX`/`pendiente de conectar`/`sin conectar`) y el contraste
`SKILL.md`/`Configuracion`/`references/contrato-*.md` que ya cubrió el ciclo anterior, sin ninguna
grieta nueva; no abre ninguna R-XX. `git status` con árbol de trabajo limpio desde el inicio.
Confirmado también que `master` sigue exactamente en el commit inicial (`f78a92c`, `git merge-base
--is-ancestor origin/master develop` → *is ancestor*, exit 0): ninguna rutina automatizada lo ha
tocado.

**Verificación objetiva de las cuatro redes, independiente, con las versiones PINEADAS
(`requirements-dev.txt`).** `python3 -m mypy scripts/ tests/` → limpio, **68 archivos**. `python3 -m
ruff check .` → "All checks passed!". `python3 -m pytest` → **583 passed**, idéntico al recuento de
la auditoría anterior. `python3 scripts/ci.py` (la invocación real del protocolo, nunca el binario
pelado — `#22`/R-15) → **CI en VERDE**, las cuatro verificaciones incluidas, con el aviso esperado y
no bloqueante de `avisar_si_version_python_diverge` (intérprete real 3.11.15 frente a
`requires-python >=3.12`, desajuste conocido de R-08/T-06). `python3 scripts/verificar_salidas.py
--fixture` → las **catorce etapas en OK**; `.pptx`/`.pdf` reales siguen LATENTES en este contenedor
(sin la skill de marca, sin Chrome/Edge) — degradación esperada y documentada, no un fallo.

**Verificación independiente de los invariantes de datos (§0.2), no solo releídos de la
documentación.** Recorrido por AST de los archivos de `scripts/` (incluido el subpaquete
`scripts/migraciones/`), esta vez resolviendo explícitamente contra la lista real de módulos propios
del paquete (no solo contra `sys.stdlib_module_names`, para no repetir el falso positivo que
señalarían los `import config`/`import parser`/etc. entre módulos hermanos sin `__init__.py`):
**cero** dependencias de terceros en el runtime, invariante intacto. `PATRONES_RECURSO_EXTERNO`
(`scripts/verificar_salidas.py`), leído directamente del código fuente, conserva sus **13 patrones**
exactos. `grep -rln "copia_seguridad\s*="` sobre `scripts/*.py` localiza los mismos **cuatro** sitios
reales ya confirmados por `#23` (`documento_revision.py`, `entrada.py`, `feedback.py`,
`instalar_skill.py`) — invariante (d) sin regresión. Inspección directa (no solo el veredicto propio
del validador) de los dos HTML que `verificar_salidas.py --fixture` dejó en `fixtures/salida/`
(`reproductor.html` y `guion-impresion.html`, ignorados por git, `git status` limpio tras la
ejecución): `grep` de `https?://`, `//cdn\.`, `<script src=`, `<link href="http` sobre ambos →
**cero coincidencias** en los dos archivos. `roadmap/FEEDBACK.md` reverificado leyendo el archivo
completo: sigue sin ninguna entrada real, solo la fila de plantilla en estado `nuevo` sin contenido.

**Coherencia entre lo decidido y lo ejecutado.** El único contenido no repetitivo del rango es el
ciclo de PM del 2026-09-25 descrito arriba; `git diff 312fe75..HEAD -- roadmap/HOJA_DE_RUTA.md
roadmap/ROADMAP_HISTORICO.md roadmap/DECISIONES_TECNICAS.md` vacío, así que no hay ninguna decisión
técnica nueva que contrastar contra §0.2 ni la hoja de ruta. `SEGUIMIENTO.md` §7 (desviaciones) sin
filas nuevas; §3 (bloqueos) sin cambios, el #7 (grabar un curso completo) sigue siendo la única
fricción real capaz de motivar producto nuevo; §6 con la pregunta #11 todavía `(pendiente)` de
respuesta del dueño — ya son **diez** pasadas de auditoría consecutivas (2026-09-17 a 2026-09-26) a
la espera exclusivamente de esa respuesta. El registro de hallazgos de este documento queda con un
único `ABIERTO` (`#24`, baja, de proceso) — reconfirmado arriba: decimotercera pasada consecutiva sin
que el patrón que lo motivó vuelva a repetirse. Con cuatro redes en verde, cero hallazgos de código
nuevos y el registro de hallazgos saneado desde hace doce pasadas consecutivas, el proyecto se
mantiene en el mismo estado estable que documentan las auditorías del 2026-09-16 al 2026-09-25: sin
trabajo de código pendiente, a la espera del bloqueo #7 (rodaje real) o de que el dueño responda la
pregunta #11.

### Auditoría 2026-09-25 — duodécima pasada consecutiva sin cambios de código; cero hallazgos nuevos; `#24` reconfirmado ABIERTO, sigue pendiente solo de la respuesta del dueño

**Nota de arranque.** El contenedor arrancó con `develop` ya en `HEAD` (`0af6e69`), sin necesidad de
ningún `fast-forward` ni `reset` (`git checkout develop` bastó, `git pull origin develop` confirmó
"up to date") y sin ningún trabajo local que perder (`git status` limpio desde el inicio). El clon
llegó superficial (`git rev-parse --is-shallow-repository` → `true`, mismo síntoma benigno ya
cerrado por `#21`, no se reabre); `git fetch --unshallow origin` trajo el historial completo (**254
commits**, `master` incluido) para diferenciar con garantías desde el commit de la auditoría
anterior (`6341558`, 2026-09-24). `pip install -r requirements-dev.txt` limpio (mismas versiones
pineadas: `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Alcance desde la última auditoría (`6341558`) — once commits, cero cambios de código.** `git diff
--stat 6341558..HEAD` toca únicamente tres documentos de `roadmap/` (`HISTORIAL_SESIONES.md`,
`ROADMAP_PRODUCTO.md`, `SEGUIMIENTO.md`; ni siquiera `DECISIONES_TECNICAS.md` esta vez, a diferencia
de casi todos los ciclos anteriores) — verificado explícitamente que `scripts/`, `tests/`, `assets/`,
`references/`, `fixtures/`, `SKILL.md`, `DEVELOPERS.md`, `PROYECTO.md` y los documentos "duros" de
`roadmap/` (`HOJA_DE_RUTA.md`, `ROADMAP_HISTORICO.md`) no tienen ni una sola línea tocada (diff vacío
sobre esas rutas). De los once commits, diez son reconfirmaciones sucesivas del Programador y uno es
un ciclo de PM (`0af6e69`, undécimo consecutivo sin abrir R-XX), leído completo en
`SEGUIMIENTO.md`/`ROADMAP_PRODUCTO.md`: verificación propia del ciclo con `git diff --stat
5f7b071..HEAD` (commit del ciclo de PM anterior) y una repetición de la búsqueda de marcadores de
trabajo pendiente (`TODO`/`FIXME`/`XXX`/`pendiente de conectar`/`sin conectar`), sin ninguna grieta
nueva; no abre ninguna R-XX. `git status` con árbol de trabajo limpio desde el inicio. Confirmado
también que `master` sigue exactamente en el commit inicial (`f78a92c`, `git merge-base
--is-ancestor origin/master develop` → *is ancestor*, exit 0): ninguna rutina automatizada lo ha
tocado.

**Verificación objetiva de las cuatro redes, independiente, con las versiones PINEADAS
(`requirements-dev.txt`).** `python3 -m mypy scripts/ tests/` → limpio, **68 archivos**. `python3 -m
ruff check .` → "All checks passed!". `python3 -m pytest` → **583 passed**, idéntico al recuento de
la auditoría anterior. `python3 scripts/ci.py` (la invocación real del protocolo, nunca el binario
pelado — `#22`/R-15) → **CI en VERDE**, las cuatro verificaciones incluidas, con el aviso esperado y
no bloqueante de `avisar_si_version_python_diverge` (intérprete real 3.11 frente a `requires-python
>=3.12`, desajuste conocido de R-08/T-06). `python3 scripts/verificar_salidas.py --fixture` → las
**catorce etapas en OK**; `.pptx`/`.pdf` reales siguen LATENTES en este contenedor (sin la skill de
marca, sin Chrome/Edge) — degradación esperada y documentada, no un fallo.

**Verificación independiente de los invariantes de datos (§0.2), no solo releídos de la
documentación.** Recorrido por AST de los 33 archivos de `scripts/` (incluido el subpaquete
`scripts/migraciones/`) confirmando que toda importación de nivel superior resuelve a la biblioteca
estándar de Python o a un módulo propio del paquete — cero dependencias de terceros en el runtime,
invariante intacto. `PATRONES_RECURSO_EXTERNO` (`scripts/verificar_salidas.py`), leído directamente
del código fuente, conserva sus **13 patrones** exactos. `grep -rln "copia_seguridad\s*="` sobre
`scripts/*.py` localiza los mismos **cuatro** sitios reales ya confirmados por `#23`
(`documento_revision.py`, `entrada.py`, `feedback.py`, `instalar_skill.py`) — invariante (d) sin
regresión. Inspección directa (no solo el veredicto propio del validador) del `reproductor.html` que
`verificar_salidas.py --fixture` dejó en `fixtures/salida/` (ignorado por git, `git status` limpio
tras la ejecución): `grep` de `https?://`, `//cdn\.`, `<script src=`, `<link href="http` → **cero
coincidencias**. **Verificación adicional propia de esta pasada, sobre el invariante "ningún número
mágico suelto en el código" (§0.2) que ninguna narrativa reciente había abordado de forma directa:**
en vez de fiarse de que ninguna auditoría anterior lo señalara, se enumeraron por regex las **115**
constantes en mayúsculas de `scripts/config.py` y se cruzaron contra `SKILL.md` de forma ingenua
(coincidencia de texto literal) — dio **110** "no encontradas", una señal que a primera vista
parecería un hallazgo grave. Investigado antes de registrarlo: es un falso positivo del propio
método de verificación, no del código. El docstring del archivo (`scripts/config.py:1-8`) documenta
que la garantía real la exige un test dedicado de T-31 (`tests/test_skill_md.py`, 4 tests, releído y
reejecutado en esta pasada: **4 passed**) que compara los *campos del dataclass* `Configuracion`
(nombres en minúscula, p. ej. `ppm_respaldo`) contra las claves documentadas en `SKILL.md` — no las
constantes en mayúsculas de nivel de módulo que solo son el valor por defecto de esos campos (p. ej.
`PPM_RESPALDO` alimenta `ppm_respaldo: int = PPM_RESPALDO`, confirmado leyendo
`scripts/config.py:473`). Mi cruce ingenio comparaba el nombre equivocado. Con el mecanismo correcto
identificado y su test en verde, el invariante queda verificado sin necesidad de repetir a mano la
comparación que el propio test ya hace mejor — se deja constancia aquí para que una pasada futura no
repita el mismo cruce ingenuo desde cero. `roadmap/FEEDBACK.md` reverificado leyendo el archivo
completo: sigue sin ninguna entrada real, solo la fila de plantilla en estado `nuevo` sin contenido.

**Coherencia entre lo decidido y lo ejecutado.** El único contenido no repetitivo del rango es el
ciclo de PM del 2026-09-24 descrito arriba; `git diff 6341558..HEAD -- roadmap/HOJA_DE_RUTA.md
roadmap/ROADMAP_HISTORICO.md` vacío, y ninguna fila nueva de `DECISIONES_TECNICAS.md` (no se tocó en
este rango) que pudiera contradecir §0.2 ni la hoja de ruta. `SEGUIMIENTO.md` §7 (desviaciones) sin
filas nuevas; §3 (bloqueos) sin cambios, el #7 (grabar un curso completo) sigue siendo la única
fricción real capaz de motivar producto nuevo; §6 con la pregunta #11 todavía `(pendiente)` de
respuesta del dueño — ya son **nueve** pasadas de auditoría consecutivas (2026-09-17 a 2026-09-25) a
la espera exclusivamente de esa respuesta. El registro de hallazgos de este documento queda con un
único `ABIERTO` (`#24`, baja, de proceso) — reconfirmado arriba: duodécima pasada consecutiva sin que
el patrón que lo motivó vuelva a repetirse. Con cuatro redes en verde, cero hallazgos de código
nuevos y el registro de hallazgos saneado desde hace once pasadas consecutivas, el proyecto se
mantiene en el mismo estado estable que documentan las auditorías del 2026-09-16 al 2026-09-24: sin
trabajo de código pendiente, a la espera del bloqueo #7 (rodaje real) o de que el dueño responda la
pregunta #11.

### Auditoría 2026-09-24 — undécima pasada consecutiva sin cambios de código; cero hallazgos nuevos; `#24` reconfirmado ABIERTO, sigue pendiente solo de la respuesta del dueño

**Nota de arranque.** El contenedor arrancó con `develop` en estado detached (`HEAD` en `5f7b071`,
sin rama local) y clon inicial sin `master` (`git fetch --unshallow origin` trajo `master` como
"nueva rama" — mismo síntoma benigno ya cerrado por `#21`, no se reabre). `git checkout develop &&
git pull origin develop` resolvió en **fast-forward limpio** de `3d60fbb` a `5f7b071` (un solo
commit, ya presente en el remoto), sin ningún `reset --hard` ni divergencia real ni trabajo local
que perder (`git status` limpio desde el inicio). `git fetch --unshallow origin` trajo el historial
completo (**242 commits**, `master` incluido) para diferenciar con garantías desde el commit de la
auditoría anterior (`3a58f1c`, 2026-09-23). `pip install -r requirements-dev.txt` limpio (mismas
versiones pineadas: `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Alcance desde la última auditoría (`3a58f1c`) — once commits, cero cambios de código.** `git diff
--stat 3a58f1c..HEAD` toca únicamente cuatro documentos de `roadmap/` (`DECISIONES_TECNICAS.md`,
`HISTORIAL_SESIONES.md`, `ROADMAP_PRODUCTO.md`, `SEGUIMIENTO.md`) — verificado explícitamente que
`scripts/`, `tests/`, `assets/`, `references/`, `fixtures/`, `SKILL.md`, `DEVELOPERS.md`,
`PROYECTO.md` y los documentos "duros" de `roadmap/` (`HOJA_DE_RUTA.md`, `ROADMAP_HISTORICO.md`) no
tienen ni una sola línea tocada (diff vacío sobre esas rutas). De los once commits, diez son
reconfirmaciones sucesivas del Programador y uno es un ciclo de PM (`5f7b071`, décimo consecutivo
sin abrir R-XX), leído completo en `DECISIONES_TECNICAS.md`: en vez de repetir la búsqueda de
marcadores de trabajo pendiente del ciclo anterior, reconfirma sin cambios la candidata toma↔archivo
de vídeo real para la lista de concatenación de ffmpeg (aparcada desde el 2026-09-21 hasta que el
bloqueo #7 aporte evidencia real de rodaje) y no abre ninguna R-XX nueva. `git status` con árbol de
trabajo limpio desde el inicio. Confirmado también que `master` sigue exactamente en el commit
inicial (`f78a92c`, `git merge-base --is-ancestor origin/master develop` → *is ancestor*, exit 0):
ninguna rutina automatizada lo ha tocado.

**Verificación objetiva de las cuatro redes, independiente, con las versiones PINEADAS
(`requirements-dev.txt`).** `python3 -m mypy scripts/ tests/` → limpio, **68 archivos**. `python3 -m
ruff check .` → "All checks passed!". `python3 -m pytest` → **583 passed**, idéntico al recuento de
la auditoría anterior. `python3 scripts/ci.py` (la invocación real del protocolo, nunca el binario
pelado — `#22`/R-15) → **CI en VERDE**, las cuatro verificaciones incluidas, con el aviso esperado y
no bloqueante de `avisar_si_version_python_diverge` (intérprete real 3.11 frente a `requires-python
>=3.12`, desajuste conocido de R-08/T-06). `python3 scripts/verificar_salidas.py --fixture` → las
**catorce etapas en OK**; `.pptx`/`.pdf` reales siguen LATENTES en este contenedor (sin la skill de
marca, sin Chrome/Edge) — degradación esperada y documentada, no un fallo.

**Verificación independiente de los invariantes de datos (§0.2), no solo releídos de la
documentación.** Recorrido por AST de los 33 archivos de `scripts/` (incluido el subpaquete
`scripts/migraciones/`) confirmando que toda importación de nivel superior resuelve a la biblioteca
estándar de Python o a un módulo propio del paquete — cero dependencias de terceros en el runtime,
invariante intacto. `PATRONES_RECURSO_EXTERNO` (`scripts/verificar_salidas.py`), leído directamente
del código fuente, conserva sus **13 patrones** exactos. `grep -rln "copia_seguridad\s*="` sobre
`scripts/*.py` localiza los mismos **cuatro** sitios reales ya confirmados por `#23`
(`documento_revision.py`, `entrada.py`, `feedback.py`, `instalar_skill.py`) — invariante (d) sin
regresión. **Verificación adicional propia de esta pasada, no repetida de auditorías anteriores:**
en vez de confiar solo en el veredicto propio de `verificar_salidas.py --fixture` sobre el
autocontenimiento, se inspeccionó directamente el `reproductor.html` que la propia ejecución del
fixture dejó en `fixtures/salida/` (94.436 bytes, correctamente ignorado por git — `git status`
limpio tras la ejecución): `grep` directo de `https?://`, `//cdn\.`, `<script src=`, `<link
href="http` sobre el archivo → **cero coincidencias**, confirmando el autocontenimiento del HTML
generado de forma independiente al validador que lo produce, no solo repitiendo su propio veredicto.
`roadmap/FEEDBACK.md` reverificado leyendo el archivo completo: sigue sin ninguna entrada real, solo
la fila de plantilla en estado `nuevo` sin contenido.

**Coherencia entre lo decidido y lo ejecutado.** El único contenido no repetitivo del rango es el
ciclo de PM del 2026-09-23 descrito arriba; `git diff 3a58f1c..HEAD -- roadmap/HOJA_DE_RUTA.md
roadmap/ROADMAP_HISTORICO.md` vacío, y la única fila nueva de `DECISIONES_TECNICAS.md` no introduce
ninguna decisión técnica que contradiga §0.2 ni la hoja de ruta. `SEGUIMIENTO.md` §7 (desviaciones)
sin filas nuevas; §3 (bloqueos) sin cambios, el #7 (grabar un curso completo) sigue siendo la única
fricción real capaz de motivar producto nuevo; §6 con la pregunta #11 todavía `(pendiente)` de
respuesta del dueño — ya son **ocho** pasadas de auditoría consecutivas (2026-09-17 a 2026-09-24) a
la espera exclusivamente de esa respuesta. El registro de hallazgos de este documento queda con un
único `ABIERTO` (`#24`, baja, de proceso) — reconfirmado arriba: undécima pasada consecutiva sin que
el patrón que lo motivó vuelva a repetirse. Con cuatro redes en verde, cero hallazgos de código
nuevos y el registro de hallazgos saneado desde hace diez pasadas consecutivas, el proyecto se
mantiene en el mismo estado estable que documentan las auditorías del 2026-09-16 al 2026-09-23: sin
trabajo de código pendiente, a la espera del bloqueo #7 (rodaje real) o de que el dueño responda la
pregunta #11.

### Auditoría 2026-09-23 — décima pasada consecutiva sin cambios de código; cero hallazgos nuevos; `#24` reconfirmado ABIERTO, sigue pendiente solo de la respuesta del dueño

**Nota de arranque.** El contenedor arrancó con `develop` en estado detached (`HEAD` en `3ed68e4`,
sin rama local) y un clon superficial (`git rev-parse --is-shallow-repository` → `true`, mismo
síntoma benigno ya cerrado por `#21`, no se reabre). `git checkout develop && git pull origin
develop` resolvió en **fast-forward limpio** de `e182237` a `3ed68e4` (un solo commit, ya presente
en el remoto), sin ningún `reset --hard` ni divergencia real ni trabajo local que perder (`git
status` limpio desde el inicio). `git fetch --unshallow origin` trajo el historial completo (**230
commits**, `master` incluido) para diferenciar con garantías desde el commit de la auditoría
anterior (`f1d1728`, 2026-09-22). `pip install -r requirements-dev.txt` limpio (mismas versiones
pineadas: `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Alcance desde la última auditoría (`f1d1728`) — once commits, cero cambios de código.** `git diff
--stat f1d1728..HEAD` toca únicamente cuatro documentos de `roadmap/` (`DECISIONES_TECNICAS.md`,
`HISTORIAL_SESIONES.md`, `ROADMAP_PRODUCTO.md`, `SEGUIMIENTO.md`) — verificado explícitamente que
`scripts/`, `tests/`, `assets/`, `references/`, `fixtures/`, `SKILL.md`, `DEVELOPERS.md`,
`PROYECTO.md` y los documentos "duros" de `roadmap/` (`HOJA_DE_RUTA.md`, `ROADMAP_HISTORICO.md`) no
tienen ni una sola línea tocada (diff vacío sobre esas rutas). De los once commits, diez son
reconfirmaciones sucesivas del Programador y uno es un ciclo de PM (`3ed68e4`, noveno consecutivo
sin abrir R-XX), leído completo en `DECISIONES_TECNICAS.md` y `ROADMAP_PRODUCTO.md`: en vez de
releer otra vez los mismos contratos que cubrieron los dos ciclos de PM anteriores
(`contrato-montaje.md`, `contrato-tomas.md`, `tomas.py`), verifica con `grep` el hilo completo de
`tomas_por_escena`/`EstadoProyecto.tomas` a través de los seis módulos que R-18 debía conectar
(`calibracion.py`, `capitulos_youtube.py`, `pptx.py`, `salidas.py`, `srt_alineado.py`, `tomas.py`).
**Reproducido de forma independiente en esta pasada, no solo leído:** `grep -ln
"tomas_por_escena\|estado\.tomas\|EstadoProyecto" scripts/calibracion.py
scripts/capitulos_youtube.py scripts/pptx.py scripts/salidas.py scripts/srt_alineado.py
scripts/tomas.py` confirma la presencia del hilo en los seis archivos citados, sin ningún módulo
huérfano — la afirmación del PM se sostiene. `git status` con árbol de trabajo limpio desde el
inicio. Confirmado también que `master` sigue exactamente en el commit inicial (`f78a92c`, `git
merge-base --is-ancestor origin/master develop` → *is ancestor*, exit 0): ninguna rutina
automatizada lo ha tocado.

**Verificación objetiva de las cuatro redes, independiente, con las versiones PINEADAS
(`requirements-dev.txt`).** `python3 -m mypy scripts/ tests/` → limpio, **68 archivos**. `python3 -m
ruff check .` → "All checks passed!". `python3 -m pytest` → **583 passed**, idéntico al recuento de
la auditoría anterior. `python3 scripts/ci.py` (la invocación real del protocolo) → **CI en
VERDE**, las cuatro verificaciones incluidas, con el aviso esperado y no bloqueante de
`avisar_si_version_python_diverge` (intérprete real 3.11 frente a `requires-python >=3.12`,
desajuste conocido de R-08/T-06). `python3 scripts/verificar_salidas.py --fixture` → las **catorce
etapas en OK**; `.pptx`/`.pdf` reales siguen LATENTES en este contenedor (sin la skill de marca, sin
Chrome/Edge) — degradación esperada y documentada, no un fallo.

**Verificación independiente de los invariantes de datos (§0.2), no solo releídos de la
documentación.** Recorrido por AST de los 33 archivos de `scripts/` (incluido el subpaquete
`scripts/migraciones/`) confirmando que toda importación de nivel superior resuelve a la biblioteca
estándar de Python o a un módulo propio del paquete — cero dependencias de terceros en el runtime,
invariante intacto. `PATRONES_RECURSO_EXTERNO` (`scripts/verificar_salidas.py`), leído directamente
del código fuente, conserva sus **13 patrones** exactos (última entrada, `url(...)` de CSS con
excepción `data:`, de R-09). `grep -rln "copia_seguridad\s*="` sobre `scripts/*.py` localiza los
mismos **cuatro** sitios reales ya confirmados por `#23` (`documento_revision.py`, `entrada.py`,
`feedback.py`, `instalar_skill.py`) — invariante (d) sin regresión. `roadmap/FEEDBACK.md`
reverificado leyendo el archivo completo: sigue sin ninguna entrada real, solo la fila de plantilla
en estado `nuevo` sin contenido.

**Coherencia entre lo decidido y lo ejecutado.** El único contenido no repetitivo del rango es la
verificación del PM del 2026-09-22 descrita arriba, ya reproducida de forma independiente; no
introduce ninguna decisión técnica que contradiga §0.2 ni la hoja de ruta. `SEGUIMIENTO.md` §7
(desviaciones) sin filas nuevas; §3 (bloqueos) sin cambios, el #7 (grabar un curso completo) sigue
siendo la única fricción real capaz de motivar producto nuevo; §6 con la pregunta #11 todavía
`(pendiente)` de respuesta del dueño — ya son **siete** pasadas de auditoría consecutivas
(2026-09-17 a 2026-09-23) a la espera exclusivamente de esa respuesta. El registro de hallazgos de
este documento queda con un único `ABIERTO` (`#24`, baja, de proceso) — reconfirmado arriba: décima
pasada consecutiva sin que el patrón que lo motivó vuelva a repetirse. Con cuatro redes en verde,
cero hallazgos de código nuevos y el registro de hallazgos saneado desde hace nueve pasadas
consecutivas, el proyecto se mantiene en el mismo estado estable que documentan las auditorías del
2026-09-16 al 2026-09-22: sin trabajo de código pendiente, a la espera del bloqueo #7 (rodaje real)
o de que el dueño responda la pregunta #11.

### Auditoría 2026-09-22 — novena pasada consecutiva sin cambios de código; cero hallazgos nuevos; `#24` reconfirmado ABIERTO, sigue pendiente solo de la respuesta del dueño

**Nota de arranque.** El contenedor arrancó con `develop` en un estado local (`1e9855f`, historial de
50 commits) sin ancestro común con `origin/develop` (`git merge-base` sin resultado): la misma
divergencia de historial ya diagnosticada y cerrada en `SEGUIMIENTO.md` §3 bloqueo #8 (2026-09-10)
como artefacto benigno del clon superficial por contenedor efímero, no una reescritura real de
`develop` — no se reabre `#21`. Resuelto con `git reset --hard origin/develop` (sin trabajo local
que perder: árbol de trabajo limpio, ninguna diferencia de contenido real entre ambas puntas más
allá de los hashes) y `git fetch --unshallow origin` para poder diferenciar con garantías desde el
commit de la auditoría anterior. `pip install -r requirements-dev.txt` limpio (mismas versiones
pineadas: `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Alcance desde la última auditoría (`e7858c5`, 2026-09-21) — once commits, cero cambios de
código.** `git diff --stat e7858c5..HEAD` toca únicamente cuatro documentos de `roadmap/`
(`DECISIONES_TECNICAS.md`, `HISTORIAL_SESIONES.md`, `ROADMAP_PRODUCTO.md`, `SEGUIMIENTO.md`; 450
inserciones, 42 eliminaciones) — verificado explícitamente que `scripts/`, `tests/`, `assets/`,
`references/`, `fixtures/`, `SKILL.md`, `DEVELOPERS.md`, `PROYECTO.md` y los documentos "duros" de
`roadmap/` (`HOJA_DE_RUTA.md`, `ROADMAP_HISTORICO.md`) no tienen ni una sola línea tocada. De los
once commits, diez son reconfirmaciones sucesivas del Programador y uno es un ciclo de PM
(`2e214d1`, noveno consecutivo sin abrir R-XX), leído completo en `roadmap/HISTORIAL_SESIONES.md`:
reconfirma la cola de producto vacía con el mismo criterio ya razonado en los ocho ciclos
anteriores, y dedica su revisión de arquitectura propia a `references/contrato-montaje.md`,
`references/contrato-tomas.md` y `scripts/tomas.py` sin encontrar ninguna grieta nueva del tipo que
motivó R-12 a R-18. `git status` con árbol de trabajo limpio desde el inicio. Confirmado que
`master` sigue exactamente en el commit inicial (`f78a92c`, `git merge-base --is-ancestor
origin/master develop` → *is ancestor*, exit 0): ninguna rutina automatizada lo ha tocado.

**Verificación objetiva de las cuatro redes, independiente, con las versiones PINEADAS
(`requirements-dev.txt`).** `python3 -m mypy scripts/ tests/` → limpio, **68 archivos**. `python3 -m
ruff check .` → "All checks passed!". `python3 -m pytest` → **583 passed**, idéntico al recuento de
la auditoría anterior. `python3 scripts/ci.py` (la invocación real del protocolo) → **CI en
VERDE**, las cuatro verificaciones incluidas, con el aviso esperado y no bloqueante de
`avisar_si_version_python_diverge` (intérprete real 3.11 frente a `requires-python >=3.12`,
desajuste conocido de R-08/T-06). `python3 scripts/verificar_salidas.py --fixture` → las **catorce
etapas en OK**; `.pptx`/`.pdf` reales siguen LATENTES en este contenedor (sin la skill de marca, sin
Chrome/Edge) — degradación esperada y documentada, no un fallo.

**Verificación independiente de los invariantes de datos (§0.2), no solo releídos de la
documentación.** Recorrido por AST de todos los archivos de `scripts/` (incluido el subpaquete
`scripts/migraciones/`) confirmando que toda importación de nivel superior resuelve a la biblioteca
estándar de Python o a un módulo propio del paquete — cero dependencias de terceros en el runtime,
invariante intacto. `PATRONES_RECURSO_EXTERNO` (`scripts/verificar_salidas.py`), leído directamente
del código fuente, conserva sus **13 patrones** exactos. `grep -rln "copia_seguridad\s*="` sobre
`scripts/*.py` localiza los mismos **cuatro** sitios reales ya confirmados por `#23`
(`documento_revision.py`, `entrada.py`, `feedback.py`, `instalar_skill.py`) — invariante (d) sin
regresión. Revisión puntual de codificación explícita (`open(...)` sin `encoding=`): el único caso
sin ella es `pdf.py::dimensiones_png`, que abre en modo binario (`"rb"`) para leer la cabecera
`IHDR` de un PNG — no aplica, no es texto. Ningún `print()` de depuración fuera de
`presentacion.py` (la única mención en `logger.py` es la propia frase del docstring que prohíbe la
práctica, no una llamada real). `roadmap/FEEDBACK.md` reverificado: sigue sin ninguna entrada real,
solo la fila de plantilla.

**Coherencia entre lo decidido y lo ejecutado.** El único contenido no repetitivo del rango es la
nota de PM del 2026-09-21 en `DECISIONES_TECNICAS.md` (con eco en `ROADMAP_PRODUCTO.md`)
registrando, sin abrir R-XX, la idea de asociar cada toma buena con su archivo de vídeo real para
una futura lista de concatenación de ffmpeg de montaje — razonada y aparcada explícitamente hasta
que se resuelva el bloqueo #7 (grabar un curso completo), no una decisión técnica que contradiga
§0.2 ni la hoja de ruta. `SEGUIMIENTO.md` §7 (desviaciones) sin filas nuevas; §3 (bloqueos) sin
cambios, el #7 sigue siendo la única fricción real capaz de motivar producto nuevo; §6 con la
pregunta #11 todavía `(pendiente)` de respuesta del dueño — ya son **seis** pasadas de auditoría
consecutivas (2026-09-17 a 2026-09-22) a la espera exclusivamente de esa respuesta. El registro de
hallazgos de este documento queda con un único `ABIERTO` (`#24`, baja, de proceso) — reconfirmado
arriba: novena pasada consecutiva sin que el patrón que lo motivó vuelva a repetirse. Con cuatro
redes en verde, cero hallazgos de código nuevos y el registro de hallazgos saneado desde hace ocho
pasadas consecutivas, el proyecto se mantiene en el mismo estado estable que documentan las
auditorías del 2026-09-16 al 2026-09-21: sin trabajo de código pendiente, a la espera del bloqueo
#7 (rodaje real) o de que el dueño responda la pregunta #11.

### Auditoría 2026-09-21 — octava pasada consecutiva sin cambios de código; cero hallazgos nuevos; `#24` reconfirmado ABIERTO, sigue pendiente solo de la respuesta del dueño

**Nota de arranque.** Clon superficial al arrancar (`git rev-parse --is-shallow-repository` →
`true`, síntoma benigno ya cerrado por `#21`, no se reabre). `git checkout develop && git pull
origin develop` resolvió en **fast-forward limpio** (`1e9855f..c3bc66d`), sin ningún `reset --hard`
ni divergencia real. `git fetch --unshallow origin` trajo el historial completo (**206 commits**,
`master` incluido) para diferenciar con garantías desde el commit de la auditoría anterior
(`b577c21`, 2026-09-20). `pip install -r requirements-dev.txt` limpio (mismas versiones pineadas:
`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Alcance desde la última auditoría (`b577c21`) — un único commit, cero cambios de código.** `git
diff --stat b577c21..HEAD` toca únicamente tres documentos de `roadmap/` (`HISTORIAL_SESIONES.md`,
`ROADMAP_PRODUCTO.md`, `SEGUIMIENTO.md`; 79 inserciones, 51 eliminaciones) — verificado
explícitamente que `scripts/`, `tests/`, `assets/`, `references/`, `fixtures/`, `SKILL.md`,
`DEVELOPERS.md`, `PROYECTO.md` y los tres documentos "duros" de `roadmap/`
(`DECISIONES_TECNICAS.md`, `HOJA_DE_RUTA.md`, `ROADMAP_HISTORICO.md`) no tienen ni una sola línea
tocada (diff vacío sobre esas rutas). El único commit del rango (`c3bc66d`) es el séptimo ciclo de
PM consecutivo, leído completo en `roadmap/HISTORIAL_SESIONES.md`: reconfirma la cola de producto
vacía con el mismo criterio ya razonado en los seis ciclos anteriores (no abrir una R-XX
especulativa sin hallazgo de auditoría, entrada de `FEEDBACK.md` ni grieta de arquitectura
verificada), hace un inventario propio de los 28 módulos de `scripts/` contra `SKILL.md` y revisa
de nuevo la regla de aislamiento "por proyecto de guion" (§0.2) frente al objetivo de curso completo
sin encontrar ninguna grieta verificable. `git status` con árbol de trabajo limpio desde el inicio.
Confirmado también que `master` sigue exactamente en el commit inicial (`f78a92c`, `git merge-base
--is-ancestor origin/master develop` → `IS ancestor`, exit 0): ninguna rutina automatizada lo ha
tocado.

**Verificación objetiva de las cuatro redes, independiente, con las versiones PINEADAS
(`requirements-dev.txt`).** `python3 -m mypy scripts/ tests/` → limpio, **68 archivos**. `python3
-m ruff check .` → "All checks passed!". `python3 -m pytest` → **583 passed**, idéntico al recuento
de la auditoría anterior — coherente con que ningún test cambió. `python3 scripts/ci.py` (la única
invocación real del protocolo, nunca el binario pelado — `#22`/R-15) → **CI en VERDE**, las cuatro
verificaciones incluidas. `python3 scripts/verificar_salidas.py --fixture` → las **catorce etapas
en OK**; `.pptx`/`.pdf` reales siguen LATENTES en este contenedor (sin la skill de marca, sin
Chrome/Edge) — degradación esperada y documentada, no un fallo.

**Verificación independiente de los invariantes de datos (§0.2), no solo releídos de la
documentación.** Recorrido por AST de los 33 archivos de `scripts/` (incluido el subpaquete
`scripts/migraciones/`) confirmando que toda importación de nivel superior resuelve a la biblioteca
estándar de Python (incluidos `__future__` y `stat`, los dos que un primer barrido con una lista
blanca incompleta señaló como "sospechosos" antes de confirmarlos manualmente como stdlib) o a un
módulo propio del paquete — cero dependencias de terceros en el runtime, invariante intacto.
`PATRONES_RECURSO_EXTERNO` (`scripts/verificar_salidas.py`), leído directamente del código fuente,
conserva sus **13 patrones** exactos. `grep -rln "copia_seguridad\s*="` sobre `scripts/*.py` localiza
exactamente los mismos **cuatro** sitios reales confirmados por `#23` (`documento_revision.py`,
`entrada.py`, `feedback.py`, `instalar_skill.py`) — invariante (d) sin regresión. `roadmap/
FEEDBACK.md` reverificado: sigue sin ninguna entrada real, solo la fila de plantilla.

**Coherencia entre lo decidido y lo ejecutado.** El único commit del rango es documental y ya
descrito arriba; `git diff b577c21..HEAD -- roadmap/DECISIONES_TECNICAS.md roadmap/HOJA_DE_RUTA.md
roadmap/ROADMAP_HISTORICO.md` vacío, así que no hay ninguna decisión técnica nueva que contrastar
contra el código. `SEGUIMIENTO.md` §7 (desviaciones) sin filas nuevas; §3 (bloqueos) sin cambios, el
#7 (grabar un curso completo) sigue siendo la única fricción real capaz de motivar producto nuevo;
§6 con la pregunta #11 todavía `(pendiente)` de respuesta del dueño — ya son cinco pasadas de
auditoría consecutivas (2026-09-17 a 2026-09-21) a la espera exclusivamente de esa respuesta. El
registro de hallazgos de este documento queda con un único `ABIERTO` (`#24`, baja, de proceso) —
reconfirmado arriba: octava pasada consecutiva sin que el patrón que lo motivó vuelva a repetirse.
Con cuatro redes en verde, cero hallazgos de código nuevos y el registro de hallazgos saneado desde
hace siete pasadas consecutivas, el proyecto se mantiene en el mismo estado estable que documentan
las auditorías del 2026-09-16 al 2026-09-20: sin trabajo de código pendiente, a la espera del
bloqueo #7 (rodaje real) o de que el dueño responda la pregunta #11.

### Auditoría 2026-09-20 — séptima pasada consecutiva sin cambios de código; cero hallazgos nuevos; `#24` reconfirmado ABIERTO, sigue pendiente solo de la respuesta del dueño

**Nota de arranque.** Clon superficial al arrancar (`git rev-parse --is-shallow-repository` →
`true`, síntoma benigno ya cerrado por `#21`, no se reabre). `git checkout develop && git pull
origin develop` resolvió en **fast-forward limpio** (`1e9855f..7a42b2f`), sin ningún `reset --hard`
ni divergencia real. `git fetch --unshallow origin` trajo el historial completo (**204 commits**,
`master` incluido) para diferenciar con garantías desde el commit de la auditoría anterior
(`a3e8acc`, 2026-09-19). `pip install -r requirements-dev.txt` limpio (mismas versiones pineadas:
`mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`).

**Alcance desde la última auditoría (`a3e8acc`) — un único commit, cero cambios de código.** `git
diff --stat a3e8acc..HEAD` toca únicamente tres documentos de `roadmap/` (`HISTORIAL_SESIONES.md`,
`ROADMAP_PRODUCTO.md`, `SEGUIMIENTO.md`; 71 inserciones, 26 eliminaciones) — verificado
explícitamente que `scripts/`, `tests/`, `assets/`, `references/`, `SKILL.md`, `DEVELOPERS.md` y
`PROYECTO.md` no tienen ni una sola línea tocada (diff vacío sobre esas rutas). El único commit del
rango (`7a42b2f`) es un ciclo de PM que reconfirma la cola de producto vacía (sexto ciclo
consecutivo sin abrir ninguna R-XX), leído completo en `roadmap/DECISIONES_TECNICAS.md`: releyó el
registro de hallazgos íntegro, hizo un barrido propio de `TODO`/`FIXME`/`pendiente`/`futuro`/`no
implementado` sobre `scripts/`, `references/`, `SKILL.md` y `DEVELOPERS.md` sin resultado
accionable, y revisó de nuevo `salidas.py`/`calibracion.py`/`tomas.py` en busca de una grieta de
arquitectura sin encontrar ninguna nueva — mismo criterio ya razonado en los cinco ciclos de PM
anteriores. `git status` con árbol de trabajo limpio desde el inicio. Confirmado también que
`master` sigue exactamente en el commit inicial (`f78a92c`, `git merge-base --is-ancestor
origin/master develop` → `IS ancestor`): ninguna rutina automatizada lo ha tocado.

**Verificación objetiva de las cuatro redes, independiente, con las versiones PINEADAS
(`requirements-dev.txt`).** `python3 -m mypy scripts/ tests/` → limpio, **68 archivos**. `python3
-m ruff check .` → "All checks passed!". `python3 -m pytest` → **583 passed**, idéntico al recuento
de la auditoría anterior — coherente con que ningún test cambió. `python3 scripts/ci.py` (la única
invocación real del protocolo, nunca el binario pelado — `#22`/R-15) → **CI en VERDE**, las cuatro
verificaciones incluidas. `python3 scripts/verificar_salidas.py --fixture` → las **catorce etapas
en OK**; `.pptx`/`.pdf` reales siguen LATENTES en este contenedor (sin la skill de marca, sin
Chrome/Edge) — degradación esperada y documentada, no un fallo.

**Verificación independiente de los invariantes de datos (§0.2), no solo releídos de la
documentación, esta vez con un ángulo distinto al de las últimas pasadas.** Recorrido por AST (no a
mano) de los 33 archivos de `scripts/` confirmando que toda importación de nivel superior resuelve
a la biblioteca estándar o a un módulo propio del paquete (el único "hallazgo" del barrido,
`scripts/estado.py` importando `migraciones`, es el subpaquete propio `scripts/migraciones/`, no
una dependencia externa) — invariante de runtime-solo-stdlib intacto. `PATRONES_RECURSO_EXTERNO`
(`scripts/verificar_salidas.py`) conserva sus **13 patrones** exactos, leídos directamente del
código fuente. `grep -rln "copia_seguridad\s*="` sobre `scripts/*.py` localiza exactamente los
mismos **cuatro** sitios reales confirmados por `#23` (`documento_revision.py`, `entrada.py`,
`feedback.py`, `instalar_skill.py`) — invariante (d) sin regresión. Barrido específico de esta
pasada sobre el invariante "ningún número mágico suelto": grep de literales numéricos habituales
(`60`, `100`, `120`, `255`, `1000`, `1024`, `3600`, `24`) en `scripts/*.py` fuera de `config.py` —
todos los que aparecen son constantes matemáticas/de formato universales (segundos por minuto/hora,
milisegundos por segundo, bytes por KB, máximo de un canal RGB, offset y firma del encabezado PNG en
`pptx.py`) y no valores de negocio configurables; el respaldo real de negocio (120 ppm) sigue
viviendo en `config.py` como ya verificaron `#10`/`#11`/R-08, solo citado en comentarios/docstrings
de otros módulos. No es una regresión del invariante, es la categoría de constante que el invariante
nunca pretendió capturar. `tests/test_skill_md.py` (compara las claves de `Configuracion` contra la
tabla de `SKILL.md` en ambas direcciones) sigue en verde. `roadmap/FEEDBACK.md` reverificado: sigue
sin ninguna entrada real, solo la fila de plantilla.

**Coherencia entre lo decidido y lo ejecutado.** El único commit del rango es documental y ya
descrito arriba; no introduce ninguna decisión técnica nueva en `DECISIONES_TECNICAS.md` que
contrastar contra el código (confirmado con `git diff a3e8acc..HEAD -- roadmap/
DECISIONES_TECNICAS.md roadmap/HOJA_DE_RUTA.md roadmap/ROADMAP_HISTORICO.md`, los tres vacíos).
`SEGUIMIENTO.md` §7 (desviaciones) sin filas nuevas; §3 (bloqueos) sin cambios, el #7 (grabar un
curso completo) sigue siendo la única fricción real capaz de motivar producto nuevo; §6 con la
pregunta #11 todavía `(pendiente)` de respuesta del dueño. El registro de hallazgos de este
documento queda con un único `ABIERTO` (`#24`, baja, de proceso) — reconfirmado arriba: séptima
pasada consecutiva (incluidas dos auditorías en profundidad y cinco reconfirmaciones de PM/
Programador) sin que el patrón que lo motivó vuelva a repetirse; sigue abierto únicamente a la
espera de la respuesta del dueño a la pregunta de gobernanza. Con cuatro redes en verde, cero
hallazgos de código nuevos y el registro de hallazgos saneado desde hace seis pasadas consecutivas,
el proyecto se mantiene en el mismo estado estable que documentan las auditorías del 2026-09-16 al
2026-09-19: sin trabajo de código pendiente, a la espera del bloqueo #7 (rodaje real) o de que el
dueño responda la pregunta #11.

### Auditoría 2026-09-19 — cero cambios de código desde la pasada anterior; cero hallazgos nuevos; `#24` reconfirmado ABIERTO, sigue pendiente solo de la respuesta del dueño

**Nota de arranque.** Clon superficial al arrancar (`git rev-parse --is-shallow-repository` →
`true`, síntoma benigno ya cerrado por `#21`, no se reabre). `git checkout develop && git pull
origin develop` resolvió en **fast-forward limpio** (`1e9855f..bdce88a`) sin ningún `reset --hard`
ni divergencia real. `git fetch --unshallow origin` trajo el historial completo (202 commits,
`master` incluido) para diferenciar con garantías desde el commit de la auditoría anterior
(`8437367`, 2026-09-18).

**Alcance desde la última auditoría (`8437367`) — cero cambios de código, otra vez.** `git diff
--stat 8437367..HEAD` toca únicamente tres documentos de `roadmap/` (`HISTORIAL_SESIONES.md`,
`ROADMAP_PRODUCTO.md`, `SEGUIMIENTO.md`; 396 inserciones, 41 eliminaciones) — verificado
explícitamente que `scripts/`, `tests/`, `assets/`, `references/`, `SKILL.md`, `DEVELOPERS.md` y
`PROYECTO.md` no tienen ni una sola línea tocada (`git diff --stat 8437367..HEAD -- scripts/ tests/
assets/ references/ SKILL.md DEVELOPERS.md PROYECTO.md` vacío). Los once commits del rango son diez
reconfirmaciones sucesivas del Programador sin ningún cambio de código (primera a décima tras R-18 y
la auditoría en profundidad del 2026-09-18) y un único ciclo de PM (`bdce88a`) que reconfirma la cola
de producto vacía sin abrir ninguna R-XX. `git status` con árbol de trabajo limpio desde el inicio.
Confirmado también que `master` sigue exactamente en el commit inicial (`f78a92c`, `git
merge-base --is-ancestor origin/master develop` → `IS ancestor`): ninguna rutina automatizada lo ha
tocado, como exige el protocolo.

**Verificación objetiva de las cuatro redes, independiente, con las versiones PINEADAS
(`requirements-dev.txt`).** `pip install -r requirements-dev.txt` limpio. `python3 -m mypy scripts/
tests/` → limpio, **68 archivos**. `python3 -m ruff check .` → "All checks passed!". `python3 -m
pytest` → **583 passed**, idéntico al recuento de la auditoría anterior — coherente con que ningún
test cambió. `python3 scripts/ci.py` (la única invocación real del protocolo, nunca el binario
pelado — `#22`/R-15) → **CI en VERDE**, las cuatro verificaciones incluidas. `python3
scripts/verificar_salidas.py --fixture` → las **catorce etapas en OK**; `.pptx`/`.pdf` reales siguen
LATENTES en este contenedor (sin la skill de marca, sin Chrome/Edge) — degradación esperada y
documentada, no un fallo.

**Verificación independiente de los invariantes de datos (§0.2), no solo releídos de la
documentación.** Comprobado por AST (no a mano ni por cuenta visual) que ningún módulo de
`scripts/` importa un paquete de terceros: recorridos los 33 archivos con `ast.parse`, todas las
importaciones de nivel superior resuelven a la biblioteca estándar de Python o a otro módulo propio
del paquete — cero dependencias de runtime, invariante intacto. `PATRONES_RECURSO_EXTERNO`
(`scripts/verificar_salidas.py`), leído directamente del código fuente, conserva sus **13 patrones**
exactos. `grep -rln "copia_seguridad\s*="` sobre `scripts/*.py` localiza exactamente los mismos
**cuatro** sitios reales confirmados por `#23` (`documento_revision.py`, `entrada.py`,
`feedback.py`, `instalar_skill.py`) — invariante (d) sin regresión. `tests/test_skill_md.py` (que
compara las claves de `Configuracion` contra la tabla de `SKILL.md` en ambas direcciones) sigue en
verde, sin ninguna clave nueva sin documentar. `roadmap/FEEDBACK.md` reverificado (`grep -n nuevo`):
sigue sin ninguna entrada real, solo la fila de plantilla.

**Coherencia entre lo decidido y lo ejecutado.** El único commit de código-adyacente del rango es el
ciclo de PM `bdce88a`, leído completo en `DECISIONES_TECNICAS.md`: reconfirma con el mismo criterio
ya razonado en los ciclos del 2026-09-11, 2026-09-15 y 2026-09-17 que abrir una R-XX especulativa sin
hallazgo de auditoría, entrada de `FEEDBACK.md` o grieta de arquitectura verificada iría contra el
principio de no diseñar sobre hipótesis sin evidencia real de rodaje, y revisa de nuevo
`scripts/salidas.py`, `scripts/calibracion.py` y `scripts/tomas.py` en busca de una grieta del mismo
tipo que motivó R-12 a R-18 sin encontrar ninguna — coincide con lo que esta auditoría también
verificó de forma independiente (ninguna de las tres decisiones registradas contradice el código
real, ninguna quedó como intención sin ejecutar). `SEGUIMIENTO.md` §7 (desviaciones) sin filas
nuevas desde la pasada anterior; §3 (bloqueos) sin cambios, el #7 (grabar un curso completo) sigue
siendo la única fricción real capaz de motivar producto nuevo. El registro de hallazgos queda con un
único `ABIERTO` (`#24`, baja, de proceso) — reconfirmado arriba: esta vez no hubo ninguna R-XX que
archivar ni prosa de "Cola de producto" que corregir, así que no hay nada nuevo que decir sobre el
patrón de latencia en sí; sigue abierto únicamente porque la pregunta de gobernanza #11 de
`SEGUIMIENTO.md` §6 continúa sin respuesta del dueño. Con cuatro redes en verde, cero hallazgos de
código nuevos y el registro de hallazgos saneado desde hace cinco pasadas consecutivas, el proyecto
se mantiene en el mismo estado estable que documentan las auditorías del 2026-09-16 al 2026-09-18:
sin trabajo de código pendiente, a la espera del bloqueo #7 (rodaje real) o de que el dueño responda
la pregunta #11.

### Auditoría 2026-09-18 — revisión en profundidad de R-18 ya implementada (integración de tomas reales en el selector T-30); cero hallazgos nuevos; `#24` reconfirmado ABIERTO sin haber vuelto a repetirse el patrón que lo motivó

**Nota de arranque.** Clon superficial al arrancar (`git rev-parse --is-shallow-repository` →
`true`, síntoma benigno ya cerrado por `#21`, no se reabre). `git checkout develop && git pull
origin develop` resolvió en **fast-forward limpio** (`1e9855f..a59d75c`), sin ningún `reset --hard`
ni divergencia real. `git fetch --unshallow origin` trajo el historial completo para diferenciar
con garantías desde el commit de la auditoría anterior (`056c797`, 2026-09-17).

**Alcance desde la última auditoría (`056c797`).** `git diff --stat 056c797..HEAD` toca
`scripts/salidas.py` (102 líneas), `scripts/verificar_salidas.py` (36 líneas) y
`tests/test_salidas.py` (259 líneas) como único cambio de código real, más `DEVELOPERS.md` y
`SKILL.md` (documentación) y cuatro documentos de `roadmap/`; `scripts/`, `tests/`, `assets/` y
`references/` sin tocar fuera de esos tres archivos (`git diff --stat 056c797..HEAD -- assets/
references/` vacío). Los once commits del rango son la implementación de **R-18** (`f14bf07`),
nueve reconfirmaciones sucesivas del Programador sin cambio de código, y un ciclo de PM
(`a59d75c`) que archiva la Oleada v7 y corrige la prosa de "Cola de producto". `git status` con
árbol de trabajo limpio desde el inicio.

**Verificación objetiva de las cuatro redes, independiente, con las versiones PINEADAS
(`requirements-dev.txt`).** `pip install -r requirements-dev.txt` limpio. `python3 -m mypy
scripts/ tests/` → limpio, **68 archivos**. `python3 -m ruff check .` → "All checks passed!".
**Nota reproducida de nuevo, no solo citada: el binario "pelado" (`which ruff` → `/root/.local/
bin/ruff 0.15.8`, por delante en el `PATH`) marca `UP042` en `scripts/salidas.py:62`
(`class TipoSalida(str, Enum)`) que `python3 -m ruff` (pineado, `0.14.0`) NO marca — exactamente el
mismo síntoma que documenta el hallazgo `#22` (cerrado por R-15), reconfirmado aquí de primera mano
en el código ya modificado por R-18, no una regresión.** `python3 -m pytest` → **583 passed**,
coincide con el recuento que cita el propio commit de R-18 (575→583). `python3
scripts/ci.py` (la única invocación real del protocolo) → **CI en VERDE**, las cuatro
verificaciones incluidas. `python3 scripts/verificar_salidas.py --fixture` → las **catorce etapas
en OK**, incluidas las dos nuevas de R-18 ("Generación/Validez del .srt alineado" y "Generación/
Validez de capítulos de YouTube"); `.pptx`/`.pdf` reales siguen LATENTES en este contenedor (sin la
skill de marca, sin Chrome/Edge) — degradación esperada, no un fallo.

**Verificación independiente de los invariantes de datos (§0.2), no solo releídos de la
documentación.** `grep -rln "copia_seguridad\s*=" scripts/*.py` → exactamente los mismos
**cuatro** sitios que `#23` (`documento_revision.py`, `entrada.py`, `feedback.py`,
`instalar_skill.py`); las dos salidas nuevas de R-18 (`guion-alineado.srt`, `capitulos-
youtube.txt`) son artefactos generados de nuevo en cada pasada, no archivos del dueño que se
relean como entrada, así que el invariante (d) no les aplica — mismo razonamiento ya asentado para
`convencion-guiones.md`. `PATRONES_RECURSO_EXTERNO` (`scripts/verificar_salidas.py`), leído por
código (no contado a mano), sigue en **13** patrones intactos. `grep -rEn "^import |^from "
scripts/*.py` sobre los 33 módulos de `scripts/`: ninguna importación de un paquete de terceros —
solo biblioteca estándar (`re`, `json`, `pathlib`, `dataclasses`, `enum`, `typing`, `datetime`,
`hashlib`, `shutil`, `subprocess`, `tomllib`, `base64`, `html`, `struct`, `unicodedata`,
`concurrent.futures`, `logging`…) — invariante de runtime sin dependencias intacto. `guardar_
capitulos_youtube`/`guardar_srt_alineado` (los dos escritores nuevos que ejercita R-18 por primera
vez desde el selector real) declaran `encoding="utf-8"` y `newline="\n"` explícitos, igual que el
resto de escritores del proyecto. Tests de reconstrucción del invariante (a) localizados en
`test_clasificador.py`, `test_normalizacion.py`, `test_revalidacion.py` y `test_troceo.py`, sin
cambios desde la pasada anterior.

**Revisión en profundidad de R-18 (`scripts/salidas.py`, `scripts/verificar_salidas.py`,
`tests/test_salidas.py`) — la spec que la auditoría del 2026-09-17 dejó pendiente de revisar en
cuanto se implementara.** Leído el diff completo de `f14bf07`, no solo el mensaje del commit,
contra los seis requisitos de la ficha archivada en `ROADMAP_HISTORICO.md`:
- **Requisito de no regresión (comportamiento idéntico sin tomas):** `tests/
  test_salidas.py::test_regresion_guiones_reales_sin_tomas_identica_a_antes_de_r18` compara, sobre
  los tres guiones reales de `fixtures/reales/`, la salida completa de `generar_salidas_
  seleccionadas` con y sin el parámetro `tomas_por_escena` (ausente por defecto,
  `tomas_por_escena or {}` en la línea 348) — confirmado leyendo el test, no asumido por el nombre.
- **`.srt` alineado condicionado a evidencia real, no a la mera presencia del parámetro:**
  `_generar_srt` (línea ~229) llama SIEMPRE a `generar_srt_alineado` cuando `tomas_por_escena` no
  está vacío, pero solo añade `guion-alineado.srt` a `generadas` si `alineacion.escenas_alineadas`
  es no vacío — la decisión razonada en `DECISIONES_TECNICAS.md` (2026-09-17, primera fila de R-18)
  de preguntarle al resultado de la reescala en vez de inspeccionar el diccionario crudo a mano se
  verifica cierta en el código, no solo en la prosa. `test_srt_con_tomas_sin_ninguna_buena_no_
  genera_el_alineado` reproduce exactamente el caso límite (tomas registradas, ninguna `buena`) y
  confirma que no aparece un segundo archivo redundante.
- **`CAPITULOS_YOUTUBE` nunca fallo silencioso, nunca `SalidaLatente` indebida:** `_generar_
  capitulos_youtube` devuelve `SalidaOmitida` con el motivo exacto (`calculo.motivo_sin_generar`)
  cuando `generar_capitulos_youtube` devuelve `contenido=None` — nunca propaga una excepción ni la
  marca latente. `verificar_salidas.py::verificar_generacion` distingue esa omisión esperada de un
  fallo real mirando el prefijo literal `"fallo al generar:"` (el único que antepone el `except`
  genérico de `generar_salidas_seleccionadas`), tal como razona la segunda decisión de R-18 en
  `DECISIONES_TECNICAS.md` — verificado leyendo `verificar_generacion` línea a línea, no solo la
  cita del commit. `test_capitulos_youtube_sin_seccion_queda_omitida_nunca_latente_ni_fallo` cubre
  exactamente esta distinción.
- **Generación independiente (requisito 3 heredado de T-30) conservada con la quinta opción:** el
  `try`/`except` por tipo de salida dentro del bucle de `generar_salidas_seleccionadas` envuelve
  también la rama nueva de `CAPITULOS_YOUTUBE`, sin ningún camino que pueda tumbar las demás
  salidas seleccionadas.
- **Sin campo nuevo de `Configuracion` ni migración de `estado.json`:** confirmado con `git diff
  056c797..HEAD -- scripts/config.py scripts/migraciones/` vacío — coherente con que `estado.tomas`
  ya existía desde R-02 y el cambio es aditivo puro sobre datos ya persistidos.
- **Brief/contrato de `tarjetas.json` sin romper compatibilidad:** `_generar_pptx` pasa `tomas_por_
  escena` a `exportar_pptx` (ya lo aceptaba desde R-13/R-16); `test_pptx_con_tomas_incluye_
  duracion_real` confirma que las claves aditivas siguen apareciendo igual desde el selector real,
  no solo desde la llamada directa que ya probaba R-13.

Los seis requisitos de la ficha están satisfechos y verificados en código, no solo en la narrativa
del commit. Sin hallazgo.

**Coherencia entre lo decidido y lo ejecutado.** Las tres decisiones de R-18 registradas en
`DECISIONES_TECNICAS.md` el 2026-09-17 (la regla de "preguntarle al resultado, no al diccionario
crudo" para el `.srt` alineado; el prefijo `"fallo al generar:"` para distinguir omisión esperada
de fallo real; y el cierre de ciclo del PM sin abrir ninguna R-XX especulativa) se contrastaron
contra el código real en el punto anterior y coinciden palabra por palabra con lo implementado —
ninguna quedó como intención sin ejecutar. `SEGUIMIENTO.md` §7 (desviaciones) sin filas nuevas desde
la pasada anterior. §3 (bloqueos) sin cambios: el #7 (grabar un curso completo) sigue siendo, como
ya señalaba la propia ficha de R-18, la fricción real de rodaje que más valor aportaría, y ninguno
de los tres bloqueos abiertos frena el desarrollo. `roadmap/FEEDBACK.md` reverificado
(`grep -n nuevo`): sigue sin ninguna entrada real, solo la fila de plantilla. El registro de
hallazgos queda con un único `ABIERTO` (`#24`, baja, de proceso) — reconfirmado arriba con una nota
nueva: esta vez la prosa de "Cola de producto" se corrigió en el mismo ciclo de PM que archivó
R-18, sin que se acumulara ninguna reconfirmación de más señalándola, así que el patrón que motivó
el hallazgo no se ha repetido una tercera vez — sigue `ABIERTO` únicamente porque la pregunta de
gobernanza #11 de `SEGUIMIENTO.md` §6 sigue sin respuesta del dueño, no porque haya vuelto a
fallar. Recomendación para la próxima auditoría: sin ninguna R-XX pendiente ni hallazgo de código
abierto, lo único que puede generar trabajo nuevo de producto es el bloqueo #7 (rodaje real) o una
respuesta del dueño a la pregunta #11 — hasta entonces, cada pasada sin cambios de código es una
reconfirmación más de un proyecto en estado saneado, no una omisión de la auditoría.

### Auditoría 2026-09-17 — sin cambios de código desde la pasada anterior; revisión de la apertura de R-18 (spec, todavía sin implementar) y reconfirmación de `#24` (correctamente enrutado a `SEGUIMIENTO.md` §6 #11, pendiente del dueño)

**Nota de arranque.** Clon superficial de nuevo al arrancar (`git rev-parse --is-shallow-repository`
→ `true`, síntoma benigno ya cerrado por `#21`, no se reabre). `git checkout develop && git pull
origin develop` resolvió en **fast-forward limpio** (`1e9855f..e3ce15d`, sin ningún `reset --hard`
ni divergencia real). `git fetch --unshallow origin` trajo el historial completo (178 commits) para
poder diferenciar con garantías desde el commit de la auditoría anterior.

**Alcance desde la última auditoría (`610f396`) — cero cambios de código.** `git diff --stat
610f396..HEAD` toca únicamente cuatro documentos de `roadmap/` (`DECISIONES_TECNICAS.md`,
`HISTORIAL_SESIONES.md`, `ROADMAP_PRODUCTO.md`, `SEGUIMIENTO.md`; 540 inserciones, 0 en cualquier
otro sitio) — verificado explícitamente que `scripts/`, `tests/`, `assets/` y `references/` no
tienen ni una sola línea tocada (`git diff --stat 610f396..HEAD -- DEVELOPERS.md SKILL.md
PROYECTO.md references/` vacío). Los diez commits del rango son nueve reconfirmaciones sucesivas
del Programador sin novedad de código (décima a decimonovena tras R-17, 06:08 a 15:08 del
2026-09-16) y un ciclo de PM (`e3ce15d`, 19:15) que abre **R-18** (oleada v7) y enruta `#24` a
pregunta abierta. `git status` con árbol de trabajo limpio desde el inicio.

**Verificación objetiva de las cuatro redes, independiente, con las versiones PINEADAS
(`requirements-dev.txt`).** `pip install -r requirements-dev.txt` limpio. `python3 -m mypy` →
limpio, 68 archivos. `python3 -m ruff check .` → "All checks passed!". `python3 -m pytest` → **575
passed**, exactamente el mismo recuento que la pasada anterior — coherente con que ningún test
cambió. `python3 scripts/verificar_salidas.py --fixture` → las catorce etapas en **OK**;
`.pptx`/`.pdf` reales siguen LATENTES en este contenedor (sin la skill de marca, sin Chrome/Edge) —
degradación esperada y documentada, no un fallo. Reverificado con `grep` que
`PATRONES_RECURSO_EXTERNO` (`scripts/verificar_salidas.py`) conserva sus **13 patrones** intactos
(invariante del reproductor autocontenido) y que la copia `.bak` antes de sobrescribir sigue
presente en exactamente los mismos **cuatro** sitios reales confirmados por `#23`
(`documento_revision.py`, `entrada.py`, `feedback.py`, `instalar_skill.py`) — invariantes (d)/(f)
sin regresión. `HOJA_DE_RUTA.md` sin ningún commit nuevo desde T-17 (documento del dueño, intocado).

**Revisión de la apertura de R-18 (`ROADMAP_PRODUCTO.md` §Oleada v7) — todavía sin código,
verificación de que la grieta de arquitectura que motiva la tarea es real, no solo asumida sobre la
palabra del PM.** Leído `scripts/salidas.py` directamente: `TipoSalida` (líneas 48-69) solo declara
`HTML`/`PPTX`/`PDF`/`SRT`, sin ninguna opción `CAPITULOS_YOUTUBE`; `_generar_pptx` (línea 253) llama
a `exportar_pptx(resultado, resultado_tiempos, carpeta_salida, nombre_guion, configuracion)` — cinco
posicionales, sin `tomas_por_escena` — que en `pptx.py` (línea 229) cae por defecto a `{}` cuando no
se pasa; `generar_salidas_seleccionadas` no lee `estado.tomas` en ningún punto del módulo (`grep -n
"estado.tomas\|tomas_por_escena" scripts/salidas.py` no encuentra nada). `SKILL.md` (sección
"Selector de salidas por validación (T-30)", línea ~297) documenta literalmente "las cuatro
salidas", confirmando que la grieta llega incluso al propio contrato con el dueño, no es solo un
detalle interno. La grieta es real, verificada leyendo el código en vivo, no solo citada de
`DECISIONES_TECNICAS.md`. Revisada también la solidez de la spec en sí (nada que implementar
todavía, `R-18` en `PENDIENTE`): los seis requisitos son coherentes con las decisiones ya asentadas
del proyecto — aditivo puro (comportamiento actual intacto sin tomas registradas, requisitos 2 y 3
lo dicen explícitamente), reutiliza el patrón ya existente de varios `ArchivoGenerado` bajo un mismo
`TipoSalida` (citando `_generar_pdf`/`_generar_pptx` como precedente real, no uno inventado), sin
campo nuevo de `Configuracion` ni migración de `estado.json` (coherente con que son datos derivados
de `estado.tomas`, ya persistido desde R-02), y el requisito 4 deja explícito que la ausencia de
capítulos o de una sola marca por encima del umbral configurado cae a `SalidaOmitida` con motivo,
nunca a fallo silencioso ni a `SalidaLatente` indebido — coherente con el invariante de cobertura
total y con el criterio ya usado en R-07. Sin hallazgo: la apertura es sólida y no hay código que
auditar todavía.

**Reconfirmación de `#24`.** Revisado el razonamiento del ciclo de PM del 2026-09-16 en
`DECISIONES_TECNICAS.md`: en vez de conceder la excepción de gobernanza que el propio hallazgo
sugería (autorizar al Programador a corregir por su cuenta la prosa de "Cola de producto" cuando
solo refleja un estado que `SEGUIMIENTO.md` §1 ya marca `COMPLETADA`), el PM la deja como pregunta
nueva #11 en §6, razonando correctamente que cambiar el reparto de acceso de §0.4 de
`HOJA_DE_RUTA.md` es protocolo que solo cambia el dueño. Es la respuesta correcta al hallazgo, no
una forma de aparcarlo: se confirma `#24` sigue `ABIERTO` en el registro (fila actualizada arriba
con la cita a la pregunta #11) a la espera de que el dueño responda — no hay nada más que este
auditor pueda verificar en código sobre un hallazgo de proceso ya enrutado correctamente.

**Coherencia entre lo decidido y lo ejecutado.** `SEGUIMIENTO.md` §7 confirmado bit a bit idéntico
al de la pasada anterior (`git diff 610f396..HEAD -- roadmap/SEGUIMIENTO.md` solo toca cabecera,
§1 (nueva fila R-18) y §6 (nueva pregunta #11)): sin desviaciones nuevas. §3 (bloqueos) sin cambios;
el bloqueo #7 (grabar un curso completo) sigue abierto y sigue siendo, como ya señalaba la spec de
R-18, la fricción real de rodaje que más valor aportaría. `roadmap/FEEDBACK.md` sigue sin ninguna
entrada `nuevo`. El registro de hallazgos queda con un único `ABIERTO` (`#24`, baja, de proceso,
correctamente enrutado y a la espera del dueño) — mismo nivel de saneamiento que la pasada anterior,
sin ninguna grieta nueva de código, invariante o robustez encontrada en esta pasada. Recomendación
para la próxima auditoría: en cuanto el Programador entregue R-18, revisar con detalle el diff de
`scripts/salidas.py` contra los seis requisitos de la spec — en particular que la ruta sin capítulos
o sin marca por encima del umbral caiga de verdad a `SalidaOmitida` (nunca a `SalidaLatente` ni a
excepción no capturada) y que los tres guiones reales de `fixtures/reales/` sin tomas registradas
produzcan una salida bit a bit idéntica a la de antes de R-18, tal como exige su propio criterio de
aceptación.

### Auditoría 2026-09-16 — cierra `#19` (R-17 verificada en profundidad), hallazgo nuevo `#24` (patrón recurrente de latencia PM/roadmap, ya señalado como "a vigilar" el 2026-09-15 y ahora confirmado)

**Nota de arranque.** Clon superficial de nuevo (`git rev-parse --is-shallow-repository` → `true`,
síntoma benigno ya cerrado por `#21`, no se reabre). `git checkout develop && git pull origin
develop` resolvió en **fast-forward limpio** (`1e9855f..892e80f`, 3 commits) sin ningún `reset
--hard` ni divergencia real, a diferencia de la pasada anterior.

**Alcance desde la última auditoría (`1ff2dc3`).** `git log 1ff2dc3..HEAD` muestra 11 commits: la
implementación de **R-17** (`b9b6bcb`), nueve reconfirmaciones sucesivas del Programador sin
ningún cambio de código, y un ciclo de PM (`892e80f`) que corrige la prosa de "Cola de producto" y
archiva la Fase F-I. `git diff --stat 1ff2dc3..HEAD` confirma que el único módulo de `scripts/`
tocado es `revalidacion.py` (23 líneas), con su test correspondiente en `tests/test_revalidacion.py`
(114 líneas) — cero cambios en cualquier otro script, en `assets/reproductor/` ni en el validador
de auto-contención.

**Verificación objetiva de las cuatro redes, independiente, con las versiones PINEADAS
(`requirements-dev.txt`).** `pip install -r requirements-dev.txt` limpio. `python3 -m mypy` →
limpio, 68 archivos. `python3 -m ruff check .` → "All checks passed!". `python3 -m pytest` → **575
passed**, exacto con el recuento que cita el propio commit de R-17 (574→575). `python3
scripts/verificar_salidas.py --fixture` → las catorce etapas en **OK**; `.pptx`/`.pdf` reales
siguen LATENTES en este contenedor (sin la skill de marca, sin Chrome/Edge) — degradación esperada
y documentada, no un fallo. Verificado por AST (no por cuenta visual) que
`PATRONES_RECURSO_EXTERNO` (`scripts/verificar_salidas.py`) conserva sus **13 patrones** intactos
(invariante del reproductor autocontenido) y, con `grep`, que la copia `.bak` antes de sobrescribir
sigue presente en los mismos **cuatro** sitios reales confirmados por `#23`
(`documento_revision.py`, `entrada.py`, `feedback.py`, `instalar_skill.py`) — invariantes (d)/(f)
sin regresión.

**Revisión en profundidad de R-17 (`scripts/revalidacion.py`) — cierra `#19`.** Leído el diff
completo de `b9b6bcb`, el test nuevo y la fila correspondiente de `DECISIONES_TECNICAS.md`, no solo
el mensaje del commit. Es un cierre de investigación genuino, no una racionalización: el test
`test_disposicion_pospuesta_corrompida_con_mismo_tamano_no_pierde_ni_duplica_contenido` construye
un escenario real (dos bloques largos sin puntuación en la misma escena, ambos candidatos a
partición) donde la asimetría teórica del `#19` **sí se materializa** — `{1}` corrompido a mano en
vez de `{0}` real produce el mismo conjunto de índices por escena y la incidencia de cardinalidad
no dispara — antes de concluir que es inofensiva para el invariante (a). La cadena de razonamiento
resiste una lectura adversarial: `pospuestas_previas` solo puede provenir de
`_particiones_pospuestas_previas`, que lee literalmente lo que `_guardar_particiones_pospuestas`
persistió en la pasada anterior — no hay ningún otro productor de ese valor en el módulo, así que
"corromper `estado.json` a mano entre pasadas" no es una hipérbole retórica sino la única vía
posible, y coincide exactamente con la precondición ya aceptada de P-04. La prueba de que el
invariante (a) no se rompe tampoco se da por sentada: el test compara los textos reconstruidos de
las dos revalidaciones (`textos_2 == textos_1`) y confirma que la edición manual del dueño sigue
presente, no solo que no salta ninguna excepción. Decisión de no endurecer la comparación,
razonada en `DECISIONES_TECNICAS.md` con las dos alternativas descartadas explícitamente: correcta
y proporcionada — no hay una tercera fuente de verdad contra la que contrastar la disposición
persistida sin caer en circularidad. Se cierra `#19` a `RESUELTO`.

**Hallazgo nuevo `#24` (baja, ABIERTO): patrón recurrente de latencia entre "completado en
código" y "prosa de roadmap actualizada".** La propia narrativa de la auditoría del 2026-09-15
dejó constancia de un ciclo de PM que corrigió la prosa de "Cola de producto" tras **ocho**
reconfirmaciones sucesivas del Programador señalándola sin corregirla, calificándolo como "algo a
vigilar si el patrón se repite". Revisando las marcas de tiempo de los commits de esta pasada
(`git log --format="%h %ad %s" --date=format:"%Y-%m-%d %H:%M"`), el patrón se ha repetido de forma
casi idéntica: R-17 quedó completada en código el 2026-09-15 a las 06:18 (`b9b6bcb`), pero
`ROADMAP_PRODUCTO.md` siguió listándola como pendiente durante **nueve** reconfirmaciones
sucesivas del Programador (07:10 a 15:08, mismo día) hasta que un ciclo de PM la corrigió a las
19:12 (`892e80f`) — trece horas de prosa desactualizada, no un día suelto. No hay ningún riesgo de
trazabilidad real: `SEGUIMIENTO.md` §1, la fuente autoritativa según su propio encabezado, marcó
`R-17 COMPLETADA` con fecha correcta desde el primer ciclo que la tocó, y ninguna decisión se apoyó
en la prosa desactualizada del documento secundario. El coste es atención de sesión: nueve
reconfirmaciones dedicando parte de su informe a señalar, sin poder corregir, un documento que no
es el suyo. Se registra como hallazgo trazable (no como nota de vigilancia suelta) precisamente
porque la vigilancia sin tarea ya falló una vez — es el mismo defecto de proceso, a escala menor,
que motivó abrir R-17 a partir de `#19` (diez reconfirmaciones sin enrutar). Sugerencia no
prescriptiva para el PM: autorizar al propio ciclo de reconfirmación del Programador a corregir por
sí solo la prosa de "Cola de producto" cuando se limite a reflejar un estado que `SEGUIMIENTO.md`
§1 ya registra como `COMPLETADA` (sin ninguna decisión de producto nueva de por medio), en vez de
esperar al siguiente ciclo de PM completo.

**Coherencia entre lo decidido y lo ejecutado.** `HOJA_DE_RUTA.md` sigue sin ninguna modificación
de contenido desde T-17 (documento inmutable, respetado; su único commit reciente, `7be48f5`,
reproduce el mismo patrón benigno de reintroducción de árbol completo en clon superficial ya
diagnosticado por `#21`, no una edición real). `SEGUIMIENTO.md` §7 confirmado bit a bit idéntico al
de la pasada anterior (`git diff 1ff2dc3..HEAD -- roadmap/SEGUIMIENTO.md` solo toca la cabecera y
§1, fila de R-17): sin desviaciones nuevas. §3 (bloqueos) y §6 (preguntas al dueño) sin cambios;
el bloqueo #7 — grabar un curso completo — sigue sin resolverse, y sigue siendo la fricción real de
rodaje que más haría avanzar el roadmap más allá de deuda técnica interna. `roadmap/FEEDBACK.md`
sigue sin ninguna entrada `nuevo`. El ciclo de PM del 2026-09-15 es internamente coherente en los
cinco documentos que toca, revisó explícitamente `contrato-montaje.md`/`contrato-tarjetas.md` en
busca de otra grieta de arquitectura y no abrió ninguna R-XX especulativa sin evidencia real de
rodaje — decisión correcta y ya razonada en el propio documento. Con `#19` cerrado y `#24` abierto,
el registro de hallazgos queda con un único `ABIERTO` (`#24`, baja, puramente de proceso) — mismo
nivel de saneamiento que la pasada anterior, sin ninguna grieta nueva de código, invariante o
robustez encontrada en esta pasada.

### Auditoría 2026-09-15 — revisión en profundidad de R-15/R-16 ya implementadas y de la apertura de R-17; cierra `#22`, reconfirma `#19` (ahora enrutado a R-17), hallazgo nuevo `#23` (inexactitud menor en la propia narrativa del auditor, autocorregida)

**Nota de arranque — esta vez el síntoma no fue el clon superficial (`#21`, cerrado), sino un
`develop` local realmente divergente.** `git checkout develop` dejó el repositorio con `HEAD`
*detached* 50 commits por detrás; `git pull origin develop` reportó **divergencia real** (50
commits solo locales, 50 solo en `origin/develop`, con aviso explícito de `git`: `develop ->
origin/develop (forced update)`). A diferencia de `#21` (falso positivo de frontera de clon
superficial), aquí `origin/develop` sí llevaba un historial distinto por delante (hasta
`9c90b8e`, la apertura de R-17). Con el árbol de trabajo limpio (`git status` sin cambios
pendientes) y sin ninguna razón para preservar 50 commits locales obsoletos que ya no
corresponden a la punta real del proyecto, se resolvió con `git reset --hard origin/develop` —
la única vía coherente con "esto es un clon efímero; lo que no esté en `origin/develop` no ha
ocurrido" (instrucción de esta misma rutina). No se detectó ninguna pérdida de trabajo real: el
árbol resultante es exactamente `origin/develop`, la fuente autoritativa.

**Alcance — dos R-XX completadas y una tercera abierta desde la última auditoría.** `git diff
--stat d0abe29 HEAD` (`d0abe29` es el commit de la auditoría del 2026-09-14) muestra cambios en
`scripts/pptx.py`, dos archivos de test y seis documentos de `roadmap/`/`references/`, cero
cambios en cualquier otro módulo de `scripts/`. Tres hitos desde la pasada anterior: **R-15**
(`3af47cb`, advertencia contra el binario "pelado", origen `#22`), **R-16** (`e2812e5`, límites
absolutos `inicio_segundos`/`fin_segundos` en `tarjetas.json`) y un ciclo de PM (`9c90b8e`) que
archiva ambas a histórico y abre **R-17** (fase F-I, origen `#19`) — todavía sin código, pura
especificación.

**Verificación objetiva de las cuatro redes, independiente, con las versiones PINEADAS
(`requirements-dev.txt`).** `pip install -r requirements-dev.txt` limpio. `python3 -m mypy` (usa
`files` de `pyproject.toml`) → limpio, 68 archivos. `python3 -m ruff check .` → "All checks
passed!". `python3 -m pytest` → **574 passed** (569→574, coherente con los 5 tests nuevos que
declara el propio commit de R-16). `python3 scripts/verificar_salidas.py --fixture` → las
catorce etapas en **OK**; `.pptx`/`.pdf` reales siguen LATENTES en este contenedor (sin la skill
de marca, sin Chrome/Edge) — degradación esperada y documentada, no un fallo. Verificado también
que `PATRONES_RECURSO_EXTERNO` (`scripts/verificar_salidas.py`) conserva sus **13 patrones**
intactos (invariante del reproductor autocontenido) y que ningún commit desde la pasada anterior
tocó `scripts/reproductor.py`, `assets/reproductor/` ni el validador de auto-contención — cero
riesgo de regresión ahí, confirmado por el propio `git diff --stat` de arriba, no solo asumido.

**Revisión en profundidad de R-16 (`scripts/pptx.py`), con atención a los invariantes (e)/(f) y a
"sin números mágicos".** Leído el diff completo de `e2812e5`: `_con_limites_absolutos` es una
segunda pasada `O(n)` sobre la tupla ya construida de `Tarjeta` (razonada así explícitamente en
`DECISIONES_TECNICAS.md` para no acoplar `_tarjeta_de_escena`, que hoy es pura, a un acumulador
mutable), reutiliza `dataclasses.replace` (patrón ya usado en `revalidacion.py`) y lee
`duracion_real_segundos`/`duracion_estimada_segundos` directamente de cada `Tarjeta` sin
reimplementar la regla real-vs-estimada de R-13 — una sola fuente de verdad, como exige el
criterio ya aplicado en R-13/R-14. Verificado el caso límite que el propio código sugiere: como
`duracion_estimada_segundos: float` (no opcional) y solo `duracion_real_segundos` puede ser
`None`, el `if/else` de la función nunca puede quedarse sin valor que acumular — no hay ningún
camino a una `TypeError` en tiempo de ejecución con datos reales. `references/contrato-tarjetas.md`
documenta las dos claves nuevas sin subir `version_contrato` (cambio aditivo, mismo criterio que
R-13) y `references/contrato-montaje.md` ya no le pide a un consumidor externo reproducir a mano
la fórmula de acumulación — la cierra exactamente como prometía la ficha de R-16. Los cinco tests
nuevos (`test_pptx.py`, `test_integracion_montaje.py`) no son triviales: cubren el caso sin toma
buena, el caso mixto real/estimado, ausencia de huecos/solapes sobre los **tres guiones reales**
de `fixtures/reales/` (no solo sintéticos) y la coincidencia exacta de `fin_segundos` de la
última escena contra el fin del `.srt` correspondiente (estimado y alineado). Ningún campo nuevo
de `Configuracion`, coherente con que son datos derivados, no un ajuste del dueño. Sin hallazgo.

**Revisión de R-15 (documental) — cierra `#22`.** `grep -in pelado DEVELOPERS.md SKILL.md`
localiza la advertencia en los dos sitios exactos que pedía la ficha (bloque de cita en
`DEVELOPERS.md` bajo "Verificación manual", frase con remisión en `SKILL.md`); `git show --stat
3af47cb` confirma cero líneas tocadas en `scripts/ci.py` ni en ningún otro módulo — tarea
puramente documental, tal como su propio commit declara. Detalle verificado en el registro de
hallazgos, fila `#22`.

**Revisión de la apertura de R-17 (todavía sin implementar, solo spec) — `#19` reconfirmado,
ahora con tarea trazable.** Leída la ficha completa en `ROADMAP_PRODUCTO.md` y la entrada
correspondiente de `DECISIONES_TECNICAS.md`. Es una apertura prudente y bien acotada: en vez de
mandar "endurecer la comparación" a ciegas (descartado explícitamente como alternativa, por
razón correcta: `revalidacion.py` es la zona más sensible del proyecto, origen de `#9`/`#14`,
ambos severidad alta en su día), la ficha exige **investigar primero** si el escenario teórico es
alcanzable y bifurca el criterio de aceptación según lo que se encuentre — endurecer con test de
regresión si es real, o dejar una prueba explícita en código de que es inalcanzable si no lo es.
Confirmado que no se ha adelantado nada a medias: `git diff --stat 9c90b8e HEAD -- scripts/`
(vacío, sin commits posteriores de código) y lectura directa de `scripts/revalidacion.py`
confirman que `_incidencias_anclas_desajustadas`/`_particiones_pospuestas_previas` siguen
exactamente como los dejó P-04. Se mantiene `#19` en `ABIERTO`, baja, sin escalar — ya no es un
hallazgo sin ruta: tiene R-17 asignada desde el 2026-09-14, con instrucción de que su cierre en
código autorice a esta auditoría a pasarlo a `RESUELTO` sin más reconfirmaciones idénticas.

**Hallazgo nuevo `#23` (baja, RESUELTO en la misma pasada): inexactitud menor y autocorregida en
la propia narrativa del auditor.** Al reverificar la protección `.bak` del invariante (d) contando
directamente con `grep` en vez de repetir la lista de pasadas anteriores, aparecen solo **cuatro**
sitios reales (`documento_revision.py`, `entrada.py`, `feedback.py`, `instalar_skill.py`), no
cinco: las narrativas del 2026-09-13 y 2026-09-14 venían incluyendo `convencion.py` en esa lista,
pero su única función de escritura (`guardar_convencion_guiones`) documenta en su propio docstring
por qué NO aplica `.bak` — genera un documento derivado ("para pegar en su plantilla"), no un
archivo del dueño que se vuelva a leer como entrada. El invariante (d) sigue cubierto al 100 % en
los cuatro sitios reales; el código nunca estuvo mal, solo la cuenta que venía repitiéndose en el
relato del auditor sin recontarse. Detalle completo en el registro de hallazgos, fila `#23`. Es
exactamente el tipo de deriva que una auditoría continua debe cazar en sí misma, no solo en el
producto.

**Coherencia entre lo decidido y lo ejecutado.** `HOJA_DE_RUTA.md` sigue sin ninguna modificación
de contenido posterior a T-17 (documento inmutable, respetado). El ciclo de PM del 2026-09-14
(`9c90b8e`) es internamente coherente en los cinco documentos que toca y corrige, sin dejarla
pasar una sexta vez, la prosa desactualizada de "Cola de producto" que ocho reconfirmaciones
sucesivas del Programador venían señalando sin que nadie la arreglara — una latencia de proceso
real (más de una semana de un documento vivo con prosa obsoleta pese al mandato de mantenerlo al
día) que se resolvió por sí sola dentro del propio ciclo de gestión y no deja ninguna desviación
abierta que registrar en este momento; se deja constancia aquí, no como hallazgo nuevo (no hay
ningún rastro de la inconsistencia que corregir ya en el código en vivo), sino como algo a vigilar
si el patrón se repite. `SEGUIMIENTO.md` §7 no tiene ninguna desviación nueva que registrar; §3
(bloqueos, incluido el #7 — grabar un curso completo, sigue sin resolverse) y §6 (preguntas al
dueño) sin cambios. `roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo`. Con `#22` cerrado y
`#19` ahora enrutado a R-17, el registro de hallazgos queda con un único `ABIERTO` (`#19`,
baja) — el estado más saneado desde que empezó esta auditoría continua.

### Auditoría 2026-09-14 — pasada de reconfirmación sin cambios de código (R-16 abierta el día anterior, todavía sin implementar; R-15 sigue igual); ningún hallazgo nuevo

**Nota de arranque.** Clon con `develop` en `HEAD` *detached* en 45 commits; `git checkout develop
&& git pull origin develop` resolvió en **fast-forward limpio** (`467833f..ad41bc1`) sin ningún
`reset --hard` ni historial huérfano. El clon **sí llegó superficial** (`git rev-parse
--is-shallow-repository` → `true`), el mismo síntoma benigno ya diagnosticado y cerrado por `#21`:
no se reabre, solo se deja constancia porque reaparece en cada contenedor nuevo. Confirmado además,
al revisar `HOJA_DE_RUTA.md`, que su único commit posterior a T-17 en este clon (`f9cf521`,
2026-09-08) es exactamente el patrón `new file mode` ya diagnosticado por `#21` (reintroducción del
árbol completo por un commit de reconfirmación en un clon superficial), no una modificación de
contenido: el documento sigue inmutable.

**Alcance — cero cambio de código desde la pasada anterior.** `git diff --stat e21a662 HEAD` (e21a662
es el commit de la propia auditoría del 2026-09-13) da como único cambio 4 archivos de `roadmap/`
(`DECISIONES_TECNICAS.md`, `HISTORIAL_SESIONES.md`, `ROADMAP_PRODUCTO.md`, `SEGUIMIENTO.md`), cero
líneas en `scripts/`, `tests/`, `assets/` ni `references/`. El único commit posterior (`ad41bc1`, PM)
abre **R-16** (oleada v6: `inicio_segundos`/`fin_segundos` por escena en `tarjetas.json`), sin tocar
código. No hay, por tanto, código nuevo que auditar en profundidad esta vez; esta pasada es una
reconfirmación objetiva de las cuatro redes más una revisión de coherencia de la nueva spec R-16 y de
si algo se ha movido en los hallazgos `ABIERTO`.

**Verificación objetiva de las cuatro redes, independiente, con las versiones PINEADAS
(`requirements-dev.txt`).** `pip install -r requirements-dev.txt` limpio. `python3 -m mypy scripts
tests` → limpio, 68 archivos. `python3 -m ruff check scripts/ tests/` (el comando exacto de
`scripts/ci.py`) → limpio. `python3 -m pytest` → **569 passed**, igual que las dos pasadas anteriores
(coherente con que no hay código nuevo). `python3 scripts/verificar_salidas.py --fixture` → las
catorce etapas en **OK**; `.pptx`/`.pdf` reales siguen LATENTES en este contenedor (sin la skill de
marca, sin Chrome/Edge) — degradación esperada y documentada, no un fallo. Verificado además, contando
la tupla por AST en vez de fiarme de una cuenta visual, que `scripts/verificar_salidas.py`
(`PATRONES_RECURSO_EXTERNO`) conserva sus **13 patrones** intactos (invariante del reproductor
autocontenido, R-09) y que la copia `.bak-<marca>` antes de sobrescribir sigue presente en los cinco
puntos que tocan archivos del dueño o de instalación (`convencion.py`, `documento_revision.py`,
`entrada.py`, `feedback.py`, `instalar_skill.py`) — invariante (d)/(f) sin regresión.

**`#22` reevaluado: sigue ABIERTO, correctamente — R-15 sigue sin implementar.** Confirmado que
`DEVELOPERS.md` y `SKILL.md` siguen sin ninguna mención a "pelado" (`grep -n pelado` no encuentra nada
en ninguno de los dos). Reproducido de nuevo, sin depender de la nota de pasadas anteriores: el binario
pelado sigue en `/root/.local/bin` (`ruff 0.15.8`, `mypy 1.19.1`, `pytest 9.0.2`), por delante en el
`PATH`, distinto de las versiones pineadas que resuelve `python3 -m <herramienta>` (`ruff 0.14.0`,
`mypy 1.18.2`). `SEGUIMIENTO.md` §1 sigue con `R-15 | ... | PENDIENTE`, coherente con
`ROADMAP_PRODUCTO.md`. Se mantiene `#22` en `ABIERTO`, media, sin escalar.

**`#19` reevaluado, sin cambios.** `git diff --stat e21a662 HEAD -- scripts/revalidacion.py` da vacío:
`_particiones_pospuestas_previas` e `_incidencias_anclas_desajustadas` siguen presentes y sin
modificar. El límite teórico (comparación de anclas por conjunto/cantidad, no por contenido/orden)
sigue exacto y sin escenario reproducido. Se mantiene `ABIERTO`, baja, sin escalar.

**Revisión de coherencia de la spec R-16 (todavía sin implementar, solo documento).** Leída la ficha
completa en `ROADMAP_PRODUCTO.md` y la fila correspondiente de `DECISIONES_TECNICAS.md`. La
justificación de apertura es sólida: `references/contrato-montaje.md` (T-33) hoy exige a un
consumidor externo reimplementar a mano la misma fórmula de acumulación real/estimada que R-13 ya
resuelve una sola vez y con tests — cerrar esa grieta antes de que exista una skill de montaje real
que la sufra con datos de producción es coherente con el criterio ya aplicado a R-08/R-09/R-11/R-14
(deuda técnica agrupada, tratada en cuanto se identifica en vez de esperar a que duela). Los cuatro
requisitos y el criterio de aceptación son concretos y verificables (límites sin huecos ni solapes,
reutilizar la lógica de T-12/R-13 sin una segunda implementación, cambio aditivo sin subir
`version_contrato`, sin campo nuevo de `Configuracion` por no ser un valor ajustable por el dueño) —
respetan los invariantes (e) y (f) de §0.2 tal y como están redactados, sin necesidad de código
todavía para confirmarlo. No se ha adelantado ningún cambio a medias: `grep -n
"inicio_segundos\|fin_segundos" scripts/pptx.py` no devuelve nada, confirmando que la tarea sigue
siendo pura especificación, sin implementación parcial que revisar.

**Coherencia entre lo decidido y lo ejecutado.** `HOJA_DE_RUTA.md` sigue sin ninguna modificación de
contenido posterior a T-17 (documento inmutable, respetado; ver nota de arranque sobre el falso
positivo de `f9cf521`). El ciclo de PM del 2026-09-13 que abre R-16 es internamente coherente en los
cuatro documentos que toca (`ROADMAP_PRODUCTO.md`, `SEGUIMIENTO.md` §1 y su cabecera,
`DECISIONES_TECNICAS.md`, `HISTORIAL_SESIONES.md`) y no reabre ni contradice ningún hallazgo cerrado:
el propio commit deja constancia de que `#22` ya está enrutado a R-15 (pendiente de implementar) y
`#19` reconfirmado sin cambios. `SEGUIMIENTO.md` §7 no tiene ninguna desviación nueva que registrar
(idéntica a la pasada anterior); §3 (bloqueos) y §6 (preguntas al dueño) sin cambios.
`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo`. Ningún hallazgo nuevo en esta pasada: la
revisión de invariantes (auto-contención, `.bak`, cobertura total del guion, biblioteca estándar en
runtime) no encontró ninguna grieta que las 23 pasadas anteriores no hubieran ya cubierto, y no había
código nuevo que pudiera introducir una.

### Auditoría 2026-09-13 — pasada de reconfirmación sin cambios de código (R-15 abierta el día anterior, todavía sin implementar); ningún hallazgo nuevo

**Nota de arranque.** Clon con `develop` en `HEAD` *detached* en 43 commits; `git checkout develop
&& git pull origin develop` resolvió en **fast-forward limpio** (`467833f..64f40c6`) sin ningún
`reset --hard` ni historial huérfano. El clon **sí llegó superficial** (`git rev-parse
--is-shallow-repository` → `true`), el mismo síntoma benigno ya diagnosticado y cerrado por `#21`:
no se reabre, solo se deja constancia porque reaparece en cada contenedor nuevo.

**Alcance — cero cambio de código desde la pasada anterior.** `git diff --stat 7116c23 HEAD --
scripts/ tests/` (7116c23 es el commit de la propia auditoría del 2026-09-12) da **vacío**: el
único commit posterior (`64f40c6`, PM) toca solo `roadmap/DECISIONES_TECNICAS.md`,
`roadmap/HISTORIAL_SESIONES.md`, `roadmap/ROADMAP_PRODUCTO.md` y `roadmap/SEGUIMIENTO.md` — abre
**R-15** (fase transversal F-H) con origen en el hallazgo `#22` de la pasada anterior. No hay,
por tanto, código nuevo que auditar en profundidad esta vez; esta pasada es una reconfirmación
objetiva de las cuatro redes más una revisión de si R-15 ya se implementó (no) y de si algo se
ha movido en los hallazgos `ABIERTO`.

**Verificación objetiva de las cuatro redes, independiente, con las versiones PINEADAS
(`requirements-dev.txt`).** `pip install -r requirements-dev.txt` limpio. `python3 -m mypy scripts
tests` → limpio, 68 archivos. `python3 -m ruff check scripts/ tests/` (el comando exacto de
`scripts/ci.py`) → limpio. `python3 -m pytest` → **569 passed**, igual que la pasada anterior
(coherente con que no hay código nuevo). `python3 scripts/verificar_salidas.py --fixture` → las
catorce etapas en **OK**; `.pptx`/`.pdf` reales siguen LATENTES en este contenedor (sin la skill de
marca, sin Chrome/Edge) — degradación esperada y documentada, no un fallo. Verificado además que
`scripts/verificar_salidas.py:94-114` (`PATRONES_RECURSO_EXTERNO`) conserva sus 14 patrones intactos
(invariante del reproductor autocontenido, R-09) y que la copia `.bak-<marca>` antes de sobrescribir
sigue presente en los cinco puntos que tocan archivos del dueño o de instalación
(`convencion.py`, `documento_revision.py`, `entrada.py`, `feedback.py`, `instalar_skill.py`) —
invariante (d) sin regresión.

**`#22` reevaluado: sigue ABIERTO, correctamente — R-15 fue abierta pero no implementada.**
Confirmado que `DEVELOPERS.md` y `SKILL.md` siguen sin ninguna mención a `python scripts/ci.py`
como única fuente de verdad frente al binario pelado (`grep -rn pelado` solo encuentra el propio
`auditoriacontinua.md` y los cuatro documentos de `roadmap/`, ninguno de los dos sitios que R-15
debe tocar). Reproducido de nuevo, sin depender de la nota de la pasada anterior: el binario pelado
sigue en `/root/.local/bin` (`ruff 0.15.8`, `mypy 1.19.1`, `pytest 9.0.2`), por delante en el
`PATH`, de las versiones pineadas que sí resuelve `python3 -m <herramienta>` (`ruff 0.14.0`, `mypy
1.18.2`). `SEGUIMIENTO.md` §1 sí registra ya `R-15 | ... | PENDIENTE | 2026-09-12 (abierta por PM)`,
coherente con `ROADMAP_PRODUCTO.md` (Fase F-H, spec completa con 4 requisitos y criterio de
aceptación) y con `DECISIONES_TECNICAS.md` (entrada del PM justificando por qué se abre como R-XX
en vez de quedar como observación suelta o P-XX directa del programador). No hay indicio de que el
programador la haya tocado ya (sin commit posterior a `64f40c6`): se mantiene `#22` en `ABIERTO`,
media, sin escalar — es exactamente el estado esperado a la espera de que se programe R-15.

**`#19` reevaluado, sin cambios.** `scripts/revalidacion.py` es bit a bit idéntico al de la última
pasada (confirmado por el `git diff` vacío de arriba): `_particiones_pospuestas_previas` e
`_incidencias_anclas_desajustadas` siguen presentes y sin modificar. El límite teórico (comparación
de anclas por conjunto/cantidad, no por contenido/orden) sigue exacto y sin escenario reproducido.
Se mantiene `ABIERTO`, baja, sin escalar.

**Coherencia entre lo decidido y lo ejecutado.** `HOJA_DE_RUTA.md` sigue sin ninguna modificación
posterior a T-17 (documento inmutable, respetado). El ciclo de PM del 2026-09-12 que abre R-15 es
internamente coherente en los cuatro documentos que toca (`ROADMAP_PRODUCTO.md`,
`SEGUIMIENTO.md` §1 y su cabecera, `DECISIONES_TECNICAS.md`, `HISTORIAL_SESIONES.md`) y su
justificación (agrupar deuda técnica menor bajo una fase transversal, mismo criterio que F-D/F-F/
F-G) es razonable y proporcionada al tamaño real de la tarea (una nota documental, sin tocar
`scripts/`). `SEGUIMIENTO.md` §7 no tiene ninguna desviación nueva que registrar; §3 (bloqueos) y
§6 (preguntas al dueño) sin cambios desde la pasada anterior. `roadmap/FEEDBACK.md` sigue sin
ninguna entrada `nuevo`. Ningún hallazgo nuevo en esta pasada: la revisión de invariantes
(auto-contención, `.bak`, cobertura total del guion, biblioteca estándar en runtime) no encontró
ninguna grieta que las 22 pasadas anteriores no hubieran ya cubierto, y no había código nuevo que
pudiera introducir una.

### Auditoría 2026-09-12 — primera pasada con R-13/R-14 ya implementadas (la del 2026-09-11 las auditó como `PENDIENTE`); hallazgo nuevo `#22` (binarios `ruff`/`mypy` preinstalados en el contenedor dan señal distinta y engañosa frente a los pineados); `#19` reconfirmado sin cambios

**Nota de arranque.** Clon con `develop` en `HEAD` *detached*; `git checkout develop && git pull
origin develop` resolvió en **fast-forward limpio** (`467833f..2219b6c`, 41 commits) sin ningún
`reset --hard` ni historial huérfano. El clon **sí llegó superficial** (`git rev-parse
--is-shallow-repository` → `true`), el mismo síntoma benigno ya diagnosticado por `#21`
(`RESUELTO`): no se reabre, solo se deja constancia porque reaparece.

**Alcance — primera pasada con R-13 y R-14 ya como código real, no como spec.** La auditoría
anterior (2026-09-11, commit `7c0c647`) verificó R-12 en profundidad y dejó R-13/R-14
`PENDIENTE`, confirmando explícitamente que ninguna se había adelantado a medias. Desde entonces,
el mismo día 2026-09-11, el programador implementó **ambas** (`7f3f9ee` R-13, `df92f6c` R-14) y el
PM archivó la oleada v5 y la fase F-G a histórico (`2219b6c`), dejando la cola de
`ROADMAP_PRODUCTO.md` vacía. `git diff --stat 7c0c647 HEAD -- scripts/ tests/ SKILL.md
PROYECTO.md DEVELOPERS.md references/ assets/ fixtures/ roadmap/` confirma 21 archivos, 959
inserciones/195 borrados — nada fuera de ese diff. Esta es, por tanto, la primera pasada con
código de producto real de R-13/R-14 que revisar en profundidad.

**Verificación objetiva de las cuatro redes, independiente, con las versiones PINEADAS
(`requirements-dev.txt`).** `pip install -r requirements-dev.txt` limpio. `python3 -m mypy
scripts tests` → limpio, 68 archivos. `python3 -m ruff check scripts/ tests/` (el comando exacto
de `scripts/ci.py`) → limpio. `python3 -m pytest` → **569 passed**, exacto con el recuento que
cita `SEGUIMIENTO.md` tras R-13+R-14 (557→564→569). `python3 scripts/verificar_salidas.py
--fixture` → **las catorce etapas en OK**; `.pptx`/`.pdf` reales siguen LATENTES en este
contenedor (sin la skill de marca, sin Chrome/Edge) — degradación esperada y documentada, no un
fallo.

**Revisión en profundidad de R-14 (`scripts/clasificador.py`), con atención específica al
invariante (b).** Al ver que `_separar_marcador_fin_escena` añade un bloque nuevo (`no_locucion`,
`senal="separador_escena"`) al final de los bloques de cada escena, la primera pregunta que se
verificó de propio motu (no solo se dio por buena la nota de `DECISIONES_TECNICAS.md`) fue si
esto podía desplazar la identidad `(numero_escena, indice_original, mitad)` que usa
`revalidacion.py` para anclar ediciones manuales — el mismo tipo de fallo que costó `#9`/`#14` en
su día. Verificado leyendo el código, no asumido: tanto `tiempos.bloques_respiracion_marcados`
(`scripts/tiempos.py:160-163`) como `troceo.trocear_guion` (`scripts/troceo.py:429-431`) —- los
dos únicos puntos que alimentan la identidad de revalidación — filtran explícitamente `if
bloque.tipo == TIPO_LOCUCION` / `if bloque.tipo != TIPO_LOCUCION: continue` **antes** de enumerar
índices; el nuevo bloque `separador_escena` es `TIPO_NO_LOCUCION`, así que nunca entra en esa
enumeración y no puede desplazar ningún índice de un bloque de locución existente. Confirmado
también que el ancla `<!-- bloque escena=N indice=K -->` de `guion-escenas.md`
(`documento_revision.py`) numera solo esos mismos bloques de respiración (T-11), no las
indicaciones no-locución, que se listan al pie de la escena sin ancla individual — dos esquemas
de numeración distintos que no interfieren entre sí. Confirmado además que los tres sitios que
`R-14` tenía que tocar para no colar `separador_escena` como indicación real están los tres
actualizados (`pdf._SENALES_ESTRUCTURALES`, `documento_revision._SENALES_ESTRUCTURALES`,
`convencion._SENALES_CONTRACTUALES`), con test de regresión explícito de "no se inventa un bloque
separador si no hay `---`". Conclusión: R-14 no representa ningún riesgo para el invariante (b),
y la propia lógica de partición (`_separar_marcador_fin_escena`, que solo mira la última línea no
en blanco del cuerpo antes de decidir) es correcta y determinista.

**Revisión de R-13 (`scripts/pptx.py`), atención a si `tomas_por_escena` llega a usarse con datos
reales.** Verificado que `salidas.py` (T-30, el selector automático) no llama en ningún punto a
`generar_srt_alineado`/`calcular_capitulos`/`exportar_pptx` con `tomas_por_escena` real — ninguno
de los tres consumidores de "duración real" (R-05, R-07, R-13) está cableado al selector
automático, algo que R-13 documenta él mismo y que resulta ser **simétrico** con R-05/R-07, no
una laguna nueva de R-13: los tres son, por diseño, salidas de la fase de montaje que se generan
aparte (documentado en `SKILL.md` §"cadena de montaje", invocadas directamente cuando existe
parte de rodaje), no parte de la tanda inicial de T-30. No es un hallazgo. El resto de R-13 es
correcto: `duracion_real_segundos` se descarta a `None` si es `<= 0` (dato degenerado, no un cero
real), `duracion_estimada_segundos` queda intacta, y el test de integración
(`test_integracion_montaje.py`) reconstruye los límites de `guion-alineado.srt` sumando
`duracion_real_segundos`/`duracion_estimada_segundos` de `tarjetas.json` y los compara exactos.

**Hallazgo nuevo `#22` (media, ABIERTO): binarios `ruff`/`mypy`/`pytest` preinstalados en el
contenedor, distintos de los pineados, en el `PATH` por delante.** Detectado al ejecutar `ruff
check .` (sin `python3 -m`) para una comprobación exploratoria y obtener un `UP042` en
`scripts/salidas.py:48` que `python3 -m ruff check .` no da; investigado hasta la causa (`which
ruff` → `/root/.local/bin/ruff`, versión **0.15.8**, frente a `python3 -m ruff --version` →
**0.14.0**, la pineada). Mismo patrón en `mypy`: el binario pelado (`/root/.local/bin/mypy`,
**1.19.1**) vive en un entorno de Python que no ve el `pytest` recién instalado en
`dist-packages`, y da **34 errores falsos** (`import-not-found` de `pytest` en la mayoría de los archivos de
test, más los `Untyped decorator` en cascada) que `python3 -m mypy scripts/ tests/` no reproduce.
Verificado que las cuatro verificaciones reales del protocolo son inmunes: `scripts/ci.py`
invoca siempre `sys.executable -m <herramienta>` (nunca el nombre pelado, leído directamente en
las cuatro `Etapa(...)` de `ETAPAS`) y el hook de pre-commit (`scripts/hooks/pre-commit`) llama a
`python scripts/ci.py`, no a los binarios sueltos — así que ningún commit real ni ninguna de las
`~30` reconfirmaciones diarias registradas en `HISTORIAL_SESIONES.md` (que sí citan `python -m
mypy`/`ruff check .` de forma inconsistente en su texto) corrió jamás contra el juego
desactualizado. El riesgo es puramente para un humano o una sesión que teclee el comando pelado a
mano esperando el mismo resultado que `ci.py`. Se registra como hallazgo de infraestructura, no de
código: no requiere ninguna P-XX de `scripts/`, pero sí vale la pena que el PM valore una nota
explícita en `DEVELOPERS.md` ("verificar siempre con `python scripts/ci.py`, nunca con el binario
pelado") para que ninguna sesión futura pierda tiempo interpretando esos 34 errores de `mypy`
pelado como una regresión real.

**`#19` reevaluado, sin cambios.** `grep` sobre `scripts/revalidacion.py` confirma
`_particiones_pospuestas_previas` (línea 110) y `_incidencias_anclas_desajustadas` (línea 300)
presentes y sin modificar desde la última pasada. El límite teórico (comparación de anclas por
conjunto/cantidad, no por contenido/orden) sigue exacto y sin escenario reproducido. Se mantiene
`ABIERTO`, baja, sin escalar.

**Coherencia entre lo decidido y lo ejecutado.** `HOJA_DE_RUTA.md` sigue sin ninguna modificación
posterior a T-17 (documento inmutable, respetado). `ROADMAP_HISTORICO.md`/`ROADMAP_PRODUCTO.md`/
`SEGUIMIENTO.md`/`DECISIONES_TECNICAS.md` cuentan la misma historia sin contradicciones: R-13/R-14
`COMPLETADA` y archivadas, cola de `ROADMAP_PRODUCTO.md` vacía, ninguna T-XX/R-XX pendiente salvo
T-24b (BLOQUEADA, hardware del dueño). La decisión de no extraer una función compartida para
"real si hay toma buena, estimada si no" (`DECISIONES_TECNICAS.md`, 2026-09-11) es razonable y
está bien fundamentada: los tres módulos que repiten el patrón (`srt_alineado.py`,
`capitulos_youtube.py`, `pptx.py`) ya tienen su propia suite verde y tocar los dos primeros solo
para ahorrar tres líneas no compensa el riesgo. `roadmap/FEEDBACK.md` sigue sin ninguna entrada
`nuevo`. Sin desviaciones nuevas que añadir a §7 de `SEGUIMIENTO.md`.

**Invariantes de datos, verificados contra el código actual.**
- **(a) cobertura total:** sostenida; R-14 la refuerza en vez de arriesgarla — el separador de fin
  de escena sigue contabilizado, solo cambia de bloque, con test de reconstrucción íntegra
  (`reconstruir(bloques) == "\n".join(...)`) en ambos tests nuevos.
- **(b) original recuperable / ediciones manuales respetadas:** sostenida, verificado en detalle
  arriba que R-14 no puede desplazar la identidad `(escena, índice_original, mitad)` porque los
  dos consumidores de esa identidad filtran a `TIPO_LOCUCION` antes de enumerar.
- **(c) reproductor autocontenido, sin red:** reverificado por la cuarta red sobre el fixture
  (`auto-contención: OK`); R-13/R-14 no tocan `reproductor.py`/`guion.js`/`estilo.css` en este
  ciclo (confirmado por el `git diff --stat` de arriba, ningún archivo de `assets/reproductor/`
  ni `scripts/reproductor.py` en la lista).
- **(d) runtime solo biblioteca estándar:** `pyproject.toml` sigue con `dependencies = []`;
  `mypy`/`ruff`/`pytest` solo en `requirements-dev.txt`, con versiones exactas pineadas — ver
  `#22` arriba sobre por qué esas versiones exactas importan y qué pasa si no se respetan.
- **(e) sin número mágico suelto / defaults en `SKILL.md`:** R-13/R-14 no añaden ningún campo de
  configuración nuevo (`mezcla_duracion_real_y_estimada` es un booleano derivado, no una entrada
  de `Configuracion`); nada que documentar en `SKILL.md` que no esté ya.
- **(f) nada se escribe fuera de la carpeta de salida / copia `.bak`:** sostenida, sin cambios en
  el área.

**Conclusión general.** R-13 y R-14 están bien implementadas, verificadas de forma independiente
contra el riesgo más probable de cada una (desplazamiento de identidad de revalidación para R-14,
cableado real de `tomas_por_escena` para R-13) y ninguna de las dos preocupaciones se materializó.
Las cuatro redes siguen en verde con las versiones pineadas (569 tests). Se abre `#22` (media,
infraestructura de entorno, no de código): el contenedor de nube trae un segundo juego de
`ruff`/`mypy`/`pytest` más nuevo que el pineado, delante en el `PATH`, que da señales distintas y
en el caso de `mypy` activamente engañosas (34 errores falsos) si alguien lo invoca sin `python3
-m`; el protocolo real (`scripts/ci.py`, el hook) es inmune, verificado leyendo el código. `#19`
sigue como límite teórico sin escenario reproducido. No queda ningún hallazgo `ABIERTO` de código
sin enrutar (solo `#19` y el nuevo `#22`, ambos de bajo riesgo real); nada exige tratamiento
urgente en esta pasada.

### Auditoría 2026-09-11 — primera pasada con código real que auditar desde R-11 (R-12 implementada y revisada en profundidad); `#20` cerrado con verificación independiente propia (el trío "duplicado" era de otro proyecto del dueño); `#19` reconfirmado sin cambios

**Nota de arranque.** El clon efímero de esta sesión llegó con `develop` en HEAD *attached* y
`git checkout develop && git pull origin develop` resolvió en un **fast-forward limpio**
(`467833f..19ff44c`, 29 commits) sin ningún `reset --hard` ni historial huérfano que realinear.
El propio clon **sí llegó superficial** (`git rev-parse --is-shallow-repository` → `true`), el mismo
síntoma benigno que `#21` (cerrado 2026-09-10) ya diagnosticó como un falso positivo del
`git clone --depth` de cada contenedor efímero: no se reabre como hallazgo, solo se deja constancia
porque reaparece en esta sesión (ver más abajo cómo afectó, y cómo se verificó sin necesidad de
`--unshallow`, la reevaluación de `#19`).

**Alcance — primera pasada con código nuevo desde R-11 (2026-09-04).** La auditoría anterior
(2026-09-10, commit `7d1559e`) cerró con R-12 todavía `PENDIENTE` ("no hay código que auditar
todavía", literalmente, en su propia narrativa). Desde entonces: `279edc3` implementa R-12 por
completo (`scripts/reproductor.py`, `scripts/config.py`, `assets/reproductor/guion.js`/`estilo.css`,
`tests/test_reproductor.py`, `SKILL.md`, `DEVELOPERS.md`), diez ciclos de reconfirmación de
Programador sin cambio de código, uno de ellos (`14773ee`, sexto del día) corrigiendo el diagnóstico
del bloqueo #8, y `19ff44c` (PM) archiva la oleada v4 a histórico y abre R-13/R-14. `git diff --stat
7d1559e HEAD -- scripts/ tests/ SKILL.md PROYECTO.md DEVELOPERS.md references/ assets/` confirma
exactamente esos 7 archivos tocados, 321 líneas — nada más. Esta es, por tanto, la primera pasada
desde R-11 con código de producto real que revisar en profundidad, no solo reconfirmar.

**Verificación objetiva de las cuatro redes, independiente.** `pip install -r requirements-dev.txt`
limpio. `python -m mypy scripts/ tests/` → **limpio sobre 68 archivos**. `python -m ruff check
scripts/ tests/` → **limpio**. `python -m pytest` → **557 passed en 3.7s** (550→557, los 7 tests
nuevos de R-12). `python scripts/verificar_salidas.py --fixture` → **las catorce etapas en OK**;
`.pptx`/`.pdf` reales siguen LATENTES en este contenedor (sin la skill de marca, sin Chrome/Edge) —
degradación esperada y documentada, no un fallo.

**Revisión en profundidad de R-12 (`scripts/reproductor.py`), no solo lectura del diff.** Leído el
código completo de `_indicaciones_ancladas_por_indice`/`_formatear_indicacion_reproductor` y su
integración en `_construir_datos`, más `guion.js`/`estilo.css`. Reutiliza tal cual la clasificación de
T-09 (`clasificador.clasificar_guion`) y el filtro pantalla/nota ya público de T-28
(`pdf.indicaciones_no_recitables`/`es_nota_interna`), sin duplicar heurística — coherente con lo que
`DEVELOPERS.md` documenta. El anclaje (mayor índice de bloque cuyo `linea_fin` cae antes de la
indicación, o el primero si no hay ninguno) es correcto y determinista; `guion.js` usa
`item.textContent = bloque.texto` seguido de `appendChild` de un `<p class="cue-indicacion">` con
`textContent` propio — nunca `innerHTML`, consistente con la nota de seguridad del propio módulo
(cero vía de inyección de marcado). Los siete tests nuevos cubren el caso principal (ancla al último
bloque), el prefijo distinto para `NOTA`, el caso sin bloque precedente (ancla al primero), la
cobertura total contra los tres guiones reales, la visibilidad condicionada por `.bloque--activo` y
el plegado con `H`, y la configurabilidad de los prefijos — batería sólida, no cosmética.

**Verificado también en vivo, no solo por los tests unitarios (Playwright/Chromium real, ejecutado
en esta sesión).** Generado `reproductor.html` sobre `fixtures/reales/guion-artefactos-lienzo.md`
(la escena con `EN PANTALLA`+`NOTA` seguidas que cita `DEVELOPERS.md`) y recorridas las ocho escenas
con un navegador real: **cero errores de consola** en las ocho; la escena 2 (`El requisito que nadie
te cuenta`) muestra correctamente las dos cues (`Pantalla:`/`Nota:`) ancladas al bloque activo
correcto. Confirmado además, en el propio texto capturado del DOM, que **`#R-14` (la fuga del
separador `---` de fin de escena en el texto de la indicación) reproduce tal cual en las ocho
escenas del fixture real** — no solo en la escena que motivó su apertura —, verificación
independiente de que la ficha de R-14 describe el problema con exactitud y sigue sin corregir
(`clasificador.py` no toca la cadena `---` en ningún punto: confirmado también por `grep`). No se
abre un hallazgo nuevo por esto: R-14 ya lo cubre, `PENDIENTE`, con spec ya escrita y verificada
contra el código actual.

**Observación menor, sin severidad propia (spot-check, no un defecto accionable).** Si una escena no
tiene NINGÚN bloque de respiración (`bloques_escena` vacío -- posible en la convención si una escena
carece por completo de `**LOCUCIÓN**`, escenario que `revalidacion._incidencias_escenas_sin_locucion`
ya detecta y avisa en T-17), `_indicaciones_ancladas_por_indice` devuelve un diccionario vacío y esa
escena pierde toda cue en el reproductor. No se registra como hallazgo porque, en ese mismo escenario
degenerado, la escena ya no tiene ningún `<li class="bloque">` que renderizar en el reproductor (todo
`escena.bloques` sale vacío): no hay ancla posible para la indicación con o sin este código, es una
limitación estructural preexistente de una escena sin locución en un reproductor pensado para
recitar, no una regresión de R-12, y el propio caso ya se avisa aguas arriba (T-17) antes de llegar
a generarse. Se deja constancia para que una futura revisión de R-14/R-13 no lo redescubra de cero.

**R-13 y R-14 verificadas contra el código actual (ambas `PENDIENTE`, no implementadas
todavía).** `grep -n "duracion_toma_buena\|duracion_real_segundos" scripts/pptx.py` no devuelve nada:
`tarjetas.json` en efecto sigue exponiendo solo la duración estimada, confirmando que la premisa de
R-13 (único consumidor de `tomas.duracion_toma_buena` que no la usa) sigue siendo exacta y la tarea
no se ha adelantado a medias. R-14 verificada en vivo, arriba. Ninguna contradice §0.2 ni los
principios de producto; ambas están correctamente enrutadas en §1 de `SEGUIMIENTO.md` como
`PENDIENTE`, con spec completa en `ROADMAP_PRODUCTO.md`.

**`#19` reevaluado, sin cambios.** El hash que `git log -1 -- scripts/revalidacion.py` devuelve en
este clon (`f3a954b`, 2026-09-06) no coincide con el citado por auditorías anteriores (`1a40c84`,
2026-09-03) — el mismo síntoma de colapso de historial en clones superficiales que ya cerró `#21`:
confirmado leyendo el contenido, no solo el hash, que `_particiones_pospuestas_previas` (línea 110) y
`_incidencias_anclas_desajustadas` (línea 300) siguen presentes y sin cambios; `f3a954b` resulta ser
un commit de PM que reintroduce el árbol completo del repositorio como "archivo nuevo" (síntoma ya
diagnosticado, no una reescritura real del contenido). El límite teórico de `#19` (comparación de
anclas por conjunto/cantidad, no por contenido/orden) sigue exacto y sin escenario reproducido. Se
mantiene `ABIERTO`, baja, sin escalar.

**`#20` cerrado a `RESUELTO`, con verificación independiente propia.** Ver el registro de arriba:
llamada directa a `list_triggers` en esta sesión leyendo el campo completo
`session_request.config.sources[].git_repository.url` de las seis rutinas (no solo `name`/
`cron_expression`, que es todo lo que comprobaban las ~15 reconfirmaciones anteriores a la corrección
del programador) — confirma de forma independiente, no por transcribir `DECISIONES_TECNICAS.md`, que
el trío sin sufijo pertenece a `centro-estudios-sw` (otro proyecto del dueño) y el trío `-teleprompter`
a este repositorio, sin duplicado ni solape real para teleprompter. Coincide exactamente con la
corrección que el programador registró el 2026-09-10 (sexto ciclo); esta pasada la reproduce con su
propia llamada a la herramienta, no se limita a darla por buena.

**Coherencia entre lo decidido y lo ejecutado.** `HOJA_DE_RUTA.md` sigue sin ninguna modificación
posterior a T-17 (documento inmutable, respetado). `ROADMAP_HISTORICO.md`/`ROADMAP_PRODUCTO.md`/
`SEGUIMIENTO.md`/`DECISIONES_TECNICAS.md` cuentan la misma historia sin contradicciones: R-12
`COMPLETADA` y archivada, R-13/R-14 `PENDIENTE` con spec completa, bloqueo #8 `RESUELTO` (diagnóstico
corregido), ninguna T-XX/R-XX pendiente salvo T-24b (BLOQUEADA, hardware del dueño). `SEGUIMIENTO.md`
señalaba explícitamente que la fila `#20` de este documento "queda desactualizada por esta corrección
pero es de escritura exclusiva del Auditor" — exactamente la corrección que esta pasada aplica.
`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (bloqueo #7 sin resolver). Sin desviaciones
nuevas que añadir a §7 de `SEGUIMIENTO.md`.

**Invariantes de datos, verificados contra el código actual (revisión dirigida, con código nuevo
real que auditar por primera vez desde R-11).**
- **(a) cobertura total:** sostenida; R-12 la extiende sin arriesgarla — test dedicado
  (`test_indicaciones_no_recitables_no_se_pierden_en_los_guiones_reales`) compara el total de
  indicaciones ancladas en el reproductor contra el total que clasifica T-09 sobre los tres guiones
  reales, y sale exacto. El caso degenerado de escena sin locución (arriba) es una limitación
  estructural preexistente, no una pérdida silenciosa de R-12.
- **(b) original recuperable / ediciones manuales respetadas:** sostenida, `revalidacion.py` intacto
  en contenido desde P-04/P-03 (confirmado por contenido, no por hash — ver `#19`).
- **(c) reproductor autocontenido, sin red:** reverificado por la cuarta red sobre el fixture real y
  por `PATRONES_RECURSO_EXTERNO` (trece patrones intactos); R-12 no añade ningún recurso, icono ni
  fuente nueva — solo texto plano vía `textContent`.
- **(d) runtime solo biblioteca estándar:** `pyproject.toml` sigue con `dependencies = []`;
  `mypy`/`ruff`/`pytest` solo en `requirements-dev.txt`.
- **(e) sin número mágico suelto / defaults en `SKILL.md`:** los dos campos nuevos de R-12
  (`prefijo_indicacion_pantalla_reproductor`/`prefijo_indicacion_nota_reproductor`) están documentados
  en `SKILL.md` (confirmado por `grep`, dos tablas). El `font-size: 0.5em` de `.cue-indicacion` en
  `estilo.css` NO es un número mágico nuevo: sigue el mismo patrón ya establecido y auditado (`#10`,
  cerrado) de que los ratios tipográficos relativos de elementos secundarios se fijan en CSS (0.55em,
  0.6em, 0.7em, 0.75em, 0.85em ya existentes en el mismo archivo) mientras que los COLORES sí viajan
  por `Configuracion`/variables CSS — la cue usa `var(--color-texto-secundario)`, no un color nuevo.
- **(f) nada se escribe fuera de la carpeta de salida / copia `.bak`:** sostenida, sin cambios en el
  área.

**Conclusión general.** Primera pasada desde R-11 con trabajo de código real que auditar en
profundidad, no solo reconfirmar: R-12 está bien implementada, reutiliza la clasificación existente
sin duplicar lógica, tiene batería de tests sólida y se verificó en vivo con Playwright/Chromium real
sin errores de consola — incluida la confirmación independiente de que el hallazgo cosmético que
motivó R-14 (la fuga del separador `---`) reproduce exactamente como su ficha describe, en las ocho
escenas del fixture real, no solo en la que se citó al abrirla. Las cuatro redes siguen en verde
(557 tests, no 550: primer cambio de recuento desde R-11). Se cierra `#20` a `RESUELTO` con
verificación propia e independiente (no por transcribir la corrección del programador), completando
la corrección que `SEGUIMIENTO.md` había señalado como pendiente de aplicar en este documento. `#19`
sigue como límite teórico sin escenario reproducido, reconfirmado pese al mismo síntoma de colapso de
historial en clon superficial que ya cerró `#21` (no reabierto: contenido verificado directamente).
R-13 y R-14 están bien especificadas, verificadas contra el código actual y no contradicen ningún
invariante ni principio vigente. No queda ningún hallazgo `ABIERTO` de código sin enrutar; nada exige
tratamiento urgente en esta pasada.

### Auditoría 2026-09-10 — sexta reconfirmación consecutiva sin cambios de código; `#21` cerrado con verificación independiente propia (falso positivo de clon superficial), `#20` reconfirmado por acceso directo a `list_triggers`

**Nota de arranque.** El clon efímero de esta sesión llegó con `develop` en HEAD *attached* y
`git checkout develop && git pull origin develop` resolvió en un **fast-forward limpio**
(`467833f..d620270`, 17 commits) sin ningún `reset --hard` ni historial huérfano que realinear —
tercera vez consecutiva (tras 2026-09-08 y 2026-09-09) sin el síntoma *detached* que documentaron
quince sesiones anteriores. El propio clon, sin embargo, **sí llegó superficial**
(`git rev-parse --is-shallow-repository` → `true`), lo cual es precisamente el dato que esta pasada
usa para cerrar `#21` de forma independiente (ver más abajo), no para reabrir la nota de arranque
como hallazgo nuevo.

**Alcance.** `git diff --stat 8d3516e HEAD` (mi propio commit de la pasada anterior, 2026-09-09,
contra el `HEAD` actual) confirma que los **17 commits nuevos tocan exclusivamente
`roadmap/`**: diez ciclos de reconfirmación de Programador el 2026-09-09 (todas sin cambio de
código, documentando `#21` como investigado y las cuatro redes en verde), uno de ellos corrigiendo
`#21` en `DECISIONES_TECNICAS.md`, y un ciclo de PM que abre **R-12** (oleada v4, `PENDIENTE`,
todavía sin implementar). **Cero cambios en `scripts/`, `tests/`, `SKILL.md`, `PROYECTO.md`,
`DEVELOPERS.md` o `references/`** desde la pasada anterior — confirmado con
`git diff --stat 8d3516e HEAD -- scripts/ tests/ SKILL.md PROYECTO.md DEVELOPERS.md references/`,
que no devuelve ninguna línea. Sexta pasada consecutiva sin código nuevo que auditar en el árbol de
fuentes desde la última con trabajo real (R-11, 2026-09-04); el foco es, como en las cinco
anteriores, reverificar de forma independiente las cuatro redes y cerrar o escalar los hallazgos
`ABIERTO` contra evidencia propia, no contra la narrativa de otro rol.

**Verificación objetiva de las cuatro redes, repetida de forma independiente.** `pip install -r
requirements-dev.txt` limpio. `python -m mypy scripts/ tests/` → **limpio sobre 68 archivos**.
`python -m ruff check scripts/ tests/` → **limpio**. `python -m pytest` → **550 passed en 2.83s**,
mismo recuento que las seis pasadas anteriores (sin código nuevo, no se esperaba otro número).
`python scripts/verificar_salidas.py --fixture` → las **catorce etapas en OK**; `.pptx`/`.pdf`
reales siguen LATENTES en este contenedor por las mismas razones ya documentadas (sin la skill de
marca `480-branded-pptx`, sin Chrome/Edge instalado) — degradación esperada y documentada, no un
fallo.

**`#21` cerrado a `RESUELTO`, con verificación independiente propia, no por transcribir la
corrección del programador.** El programador ya había investigado `#21` el 2026-09-09 y concluido,
en `DECISIONES_TECNICAS.md`, que era un falso positivo del clon superficial de cada contenedor
efímero — pero esa corrección vive en un documento que el auditor no escribe, y la instrucción de
esta auditoría es reevaluar cada `ABIERTO` contra el código, no dar por buena la palabra de otro rol.
Repetí la comprobación por mi cuenta en esta misma sesión: `git rev-parse
--is-shallow-repository` → `true` (mi propio clon también llegó superficial, con 50 commits locales
visibles antes de la operación); `git fetch --unshallow origin` (operación de solo lectura, no
destructiva) trajo el historial completo, **114 commits**, con raíz real `f78a92c` ("initial
commit") → `e8b9663` (T-00) → …, **no** `576f6d9` ni ningún otro commit intermedio citado por pasadas
anteriores como "raíz". Tras el `unshallow`, `git merge-base --is-ancestor 1a40c84 develop` **y**
`git merge-base --is-ancestor 576f6d9 develop` devuelven ambos **"IS ancestor"**: ninguno de los dos
commits que auditorías anteriores creyeron perdidos o huérfanos lo estaba — eran alcanzables desde
`develop` en todo momento, solo invisibles para un clon superficial que no había traído esa parte del
grafo. Se corrige el registro de arriba de `ABIERTO` a `RESUELTO` con esta evidencia propia. Lección
para las próximas pasadas (y para mí mismo si repito el error): antes de diagnosticar una reescritura
de historial a partir de `git log --oneline --reverse | head -1` o de `git merge-base
--is-ancestor`, comprobar primero `git rev-parse --is-shallow-repository` — es la comprobación más
barata y habría evitado que `#21` llegara a abrirse con severidad alta el 2026-09-09.

**`#19` reevaluado, sin cambios.** `git log -1 -- scripts/revalidacion.py` sigue devolviendo
`1a40c84` (P-04, 2026-09-03): el archivo no se ha tocado desde entonces (confirmado también
leyendo el contenido: `_particiones_pospuestas_previas`/`_incidencias_anclas_desajustadas` siguen en
`scripts/revalidacion.py`, líneas 110 y 300). El límite teórico (comparación por conjunto/cantidad
de anclas, no por contenido/orden) sigue exacto y sin escenario reproducido. Se mantiene `ABIERTO`,
sin escalar.

**`#20` reevaluado con `list_triggers` en directo (no solo releyendo `SEGUIMIENTO.md`).** Llamada
propia a `list_triggers` en esta pasada: siguen existiendo exactamente las mismas **seis** rutinas de
teleprompter, todas `enabled: true`, mismos `id`/`cron_expression`/`created_at` que documentan las
pasadas anteriores — `auditor-teleprompter` (`trig_01PUyc5iBFvJwY2Eu2iga9Ai`, `0 3 * * *`,
2026-08-31) junto a `Auditor` (`trig_019V5UKE8jKMvA2LCneiTtTD`, mismo cron, 2026-08-25);
`product-manager-teleprompter` (`trig_01UeizxJHtmf1U8stMcdnAfy`, `0 19 * * *`, 2026-08-31) junto a
`Product manager` (`trig_01Gou6bJDBVucaAkfXYaynAz`, mismo cron, 2026-08-25);
`programador-teleprompter` (`trig_01FWDZPhNLTjaxS5zabErJbT`, `0 6-15 * * 1-5`, 2026-08-31) junto a
`Programador` (`trig_01RkE491KgehtmqBcoFUFFKz`, `0 6,8,10,12,14 * * 1-5`, solapado, 2026-08-25). Sin
cambios desde la notificación del 2026-09-04. Se mantiene `#20` como `ASUMIDO`, sin escalar ni
renotificar: sigue siendo una acción sobre la cuenta del dueño, ya notificada, sin novedad que
justifique repetir el aviso. **Efecto colateral ya visible, sin severidad propia nueva:** el volumen
de ciclos de reconfirmación duplicados ha hecho crecer `DECISIONES_TECNICAS.md` a 265 KB y
`HISTORIAL_SESIONES.md` a 298 KB — la mayoría de ese volumen son entradas casi idénticas de
"reconfirmación N del día". No degrada ningún invariante ni la funcionalidad, pero empieza a costar
legibilidad al propio proceso de auditoría (hay que paginar los documentos para encontrar la última
entrada real); es el mismo coste de `#20` haciéndose visible en un sitio nuevo, no un hallazgo
independiente.

**R-12 revisada (nueva, `PENDIENTE`, todavía sin implementar — no hay código que auditar
todavía).** La ficha (`ROADMAP_PRODUCTO.md`) especifica una cue discreta para las indicaciones `**EN
PANTALLA**`/`**NOTA**` en el reproductor, ancladas al bloque de respiración que las precede,
reutilizando `linea_inicio`/`linea_fin` ya calculados por T-09/T-11 sin clasificación nueva. La
ficha es coherente con los principios de producto ya vigentes: fija como requisito no negociable
que la cue nunca compita en tamaño/contraste con el bloque activo (principio #5), que se pliegue en
el mecanismo de ocultar indicadores ya entregado por T-23 (sin atajo nuevo) y que ninguna indicación
se pierda si no hay bloque de locución posterior en la escena (extiende el invariante (a) de forma
explícita y razonada, no lo relaja). No encuentro ninguna contradicción entre esta ficha y §0.2 ni
con el resto del roadmap; queda pendiente de auditar en código cuando se implemente.

**Coherencia entre lo decidido y lo ejecutado.** Sin desviaciones nuevas que añadir a §7 de
`SEGUIMIENTO.md` (las cinco filas existentes describen exactamente lo mismo). `HOJA_DE_RUTA.md`
sigue con su último commit real en `74cd27f` (T-17), sin ninguna modificación posterior — la regla
de inmutabilidad se sigue respetando, y §0.2 (invariantes (a)-(d), aislamiento por proyecto, cero
red, runtime sin dependencias, sin números mágicos) sigue coincidiendo palabra por palabra con el
código verificado en esta pasada. `ROADMAP_PRODUCTO.md` y `SEGUIMIENTO.md` §1 coinciden: única
tarea `PENDIENTE` es R-12 (recién abierta), T-24b sigue `BLOQUEADA` por hardware del dueño.
`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo` (bloqueo #7 — grabar un curso completo — sin
resolver).

**Invariantes de datos, verificados de nuevo contra el código (spot-check dirigido, no
re-auditoría completa, al no haber cambios de código desde la pasada anterior).**
- **(a) cobertura total:** sostenida, sin cambios en el área desde R-11; R-12 la extiende (sin
  implementar todavía) en vez de arriesgarla.
- **(b) original recuperable / ediciones manuales respetadas:** sostenida, `revalidacion.py` intacto
  en contenido desde P-04/P-03.
- **(c) reproductor autocontenido, sin red:** reverificado por la cuarta red sobre el fixture real y
  por spot-check directo de `PATRONES_RECURSO_EXTERNO` (trece patrones, líneas 94-114 de
  `scripts/verificar_salidas.py`) — `reproductor.html` y `guion-impresion.html` autocontenidos,
  catorce etapas en OK.
- **(d) runtime solo biblioteca estándar:** `pyproject.toml` sigue con `dependencies = []`;
  `mypy`/`ruff`/`pytest` solo en `requirements-dev.txt`.
- **(e) sin número mágico suelto / defaults en `SKILL.md`:** sin cambios en `config.py` desde la
  última verificación exhaustiva; `test_skill_md.py` (parte de los 550) sigue verificando la
  correspondencia bidireccional.
- **(f) nada se escribe fuera de la carpeta de salida / copia `.bak`:** sostenida, sin cambios en el
  área.

**Conclusión general.** Sexta pasada consecutiva sin trabajo de código que auditar: el contenido del
proyecto permanece exactamente donde lo dejó la pasada del 2026-09-09, con las cuatro redes en verde
y ningún invariante degradado. A diferencia de las cinco pasadas anteriores, esta sí cierra un
hallazgo de severidad alta con verificación propia: `#21` pasa a `RESUELTO`, reproducido de forma
independiente (no transcrito de `DECISIONES_TECNICAS.md`) con `git fetch --unshallow` y
`git merge-base --is-ancestor` sobre mi propio clon. `#19` sigue siendo un límite teórico sin
escenario reproducido; `#20` sigue `ASUMIDO`, reconfirmado por acceso directo a `list_triggers`, con
el coste acumulado ahora también visible en el tamaño de los documentos vivos del proyecto. R-12
(nueva, `PENDIENTE`) está bien especificada y no contradice ningún principio ni invariante vigente.
No queda ningún hallazgo `ABIERTO` de código sin enrutar; nada exige tratamiento urgente en esta
pasada.

### Auditoría 2026-09-09 — quinta reconfirmación consecutiva sin cambios de código; hallazgo nuevo de fondo: el historial de `develop` está reescrito desde hace días sin que ninguna pasada lo detectara (#21)

**Nota de arranque.** El clon efímero de esta sesión volvió a partir con `develop` local en HEAD
*detached* (mismo síntoma que quince y más sesiones anteriores documentaron, ligado al bloqueo #8),
pero esta vez `git checkout develop && git pull origin develop` resolvió en un **fast-forward
limpio** (`467833f..95f029e`, dos commits) sin necesitar `git reset --hard` ni realinear ningún
historial huérfano — igual que la pasada anterior (2026-09-08), aunque con el detalle de que esta
sesión sí vio el HEAD *detached* inicial y aquella no lo mencionó. No se trata como hallazgo nuevo
por sí solo: es el mismo síntoma de siempre, con un desenlace benigno.

**Alcance.** `git diff --stat 95f029e HEAD` (mi propio HEAD tras el pull) confirma cero commits
nuevos desde la pasada anterior: el `HEAD` de `origin/develop` sigue siendo exactamente `95f029e`,
el mismo commit de PM que auditó la pasada del 2026-09-08. Quinta pasada consecutiva sin código
nuevo que revisar en `scripts/`/`tests/` desde la última con trabajo real (2026-09-05); el foco,
como en las cuatro anteriores, es reverificar las cuatro redes de forma independiente y comprobar
que el propio registro de hallazgos sigue siendo coherente y verificable — y es precisamente en esa
segunda comprobación donde apareció el único hallazgo real de esta pasada.

**Verificación objetiva de las cuatro redes, repetida de forma independiente.** `pip install -r
requirements-dev.txt` limpio. `python -m mypy scripts/ tests/` → **limpio sobre 68 archivos**.
`python -m ruff check scripts/ tests/` → **limpio**. `python -m pytest -q` → **550 passed**, mismo
recuento que las cuatro pasadas anteriores (sin código nuevo, no se esperaba otro número). `python
scripts/verificar_salidas.py --fixture` → las **catorce etapas en OK**; `.pptx`/`.pdf` reales siguen
LATENTES en este contenedor por las mismas razones ya documentadas (sin la skill de marca
`480-branded-pptx`, sin Chrome/Edge instalado) — degradación esperada y documentada, no un fallo.

**Registro de hallazgos, reevaluado fila por fila.** Sin discrepancias en las filas existentes: las
`RESUELTO` siguen citando evidencia de archivo:línea verificable (confirmé de nuevo, por spot-check
directo, que `_particiones_pospuestas_previas`/`_incidencias_anclas_desajustadas` siguen en
`scripts/revalidacion.py`, líneas 110 y 300). `#19` sigue `ABIERTO` sin cambios: `revalidacion.py`
no se ha tocado en contenido desde P-04 (verificado leyendo el archivo, no solo el hash — ver más
abajo por qué el hash por sí solo ya no basta como prueba). `#20` sigue `ASUMIDO`, reverificado con
acceso directo a `list_triggers`.

**`#20` reevaluado con verificación directa de `list_triggers`, con un matiz nuevo sin severidad
propia.** Confirmado por esta sesión: siguen existiendo exactamente las mismas **seis** rutinas de
teleprompter, las seis `enabled: true`, mismos `id`/`cron_expression`/`created_at` ya documentados
en pasadas anteriores — `auditor-teleprompter`/`Auditor` (`0 3 * * *`), `product-manager-teleprompter`/
`Product manager` (`0 19 * * *`), `programador-teleprompter`/`Programador` (crons solapados). La
consulta devolvió además un séptimo disparador, `trig_01U8Lzv82wbkP7kSxYcwANCq`
("Reintentar push T-01 tras 403 de GitHub (3)", creado 2026-08-31, **`enabled: false`**, un
disparo único con `next_run_at` ya vencido desde 2026-09-01): es un resto inerte de un mecanismo de
reintento de una sesión muy temprana, deshabilitado y caducado, no una séptima rutina activa —
mencionado aquí solo para que quede constancia de que se revisó, no porque cambie el diagnóstico de
`#20`. Sin cambios respecto a lo ya registrado el 2026-09-04: se mantiene `#20` `ASUMIDO`, sin
escalar ni renotificar por sí solo.

**Hallazgo nuevo — `#21`, severidad alta, `ABIERTO`: el historial de `develop` lleva reescrito desde
hace días y ninguna de las últimas cinco pasadas lo detectó.** Al comprobar `#19` no me limité a
repetir "`revalidacion.py` no se ha tocado desde P-04, commit `1a40c84`" como hacían las pasadas del
2026-09-05 al 2026-09-08: intenté reproducir esa misma comprobación con `git log -1 --format=%H --
scripts/revalidacion.py` y el resultado fue `576f6d9`, no `1a40c84`. Antes de asumir que el archivo
había cambiado, comprobé el contenido (sin diferencias: el arreglo de P-04 sigue íntegro) y después
el propio commit: `git cat-file -t 1a40c84` confirma que el objeto **existe** en la base de datos de
este clon, pero `git merge-base --is-ancestor 1a40c84 HEAD` confirma que **ya no es antepasado de
`HEAD`** — es un commit huérfano, alcanzable solo porque quedó suelto en el almacén de objetos, no
porque forme parte de la rama. Tirando del hilo: `git log --oneline --reverse | head -1` muestra que
el **primer commit de todo `develop`** es hoy `576f6d9` ("P-05: la copia de seguridad de
`instalar_skill.py` sale de `~/.claude/skills/`", 2026-09-03) — es decir, **todo el tramo T-00 a P-05
completo (decenas de commits atómicos, entre ellos los que cerraron `#9` y `#14`) está colapsado en
un único commit raíz.** Los hashes que las auditorías del 2026-09-04 al 2026-09-08 citaron como
evidencia para `HOJA_DE_RUTA.md` (`7176b46`, `8971150`) ni siquiera existen ya como objetos
(`git cat-file -t` responde "Not a valid object name" para ambos). El commit `82e3ef4` (la propia
auditoría del 2026-09-07) **sí** sigue siendo antepasado de `HEAD`, así que el colapso afecta solo al
tramo anterior a P-05, no al trabajo de las pasadas más recientes.

Contenido verificado de nuevo, independiente del hash: `HOJA_DE_RUTA.md` termina en T-33, versión
1.3, sin ninguna línea añadida (leído íntegro en esta pasada); `revalidacion.py` conserva el arreglo
de P-04 y los cinco tests de regresión de `#9`/`#14` en `tests/test_revalidacion.py` (incluido
`test_edicion_manual_y_particion_aceptada_misma_pasada_no_pierde_edicion`) siguen presentes y en
verde, confirmado por el recuento de 550 tests pasando. **No hay ninguna pérdida de contenido ni de
funcionalidad** — el invariante (c) sigue intacto y probado. Lo que se ha perdido es la
**trazabilidad commit-a-commit** que §0.2 exige literalmente ("commits atómicos por tarea con
prefijo del ID") para toda la primera fase del proyecto, y la propia cadena de citas de hash de este
documento de auditoría, que cinco pasadas consecutivas dieron por buena sin que nadie comparara el
hash citado hoy contra el citado ayer. Es la misma causa raíz que el bloqueo #8 (rutinas duplicadas
compitiendo por escribir en `origin/develop`, con el push de una sesión pisando o reescribiendo el de
otra) pero una consecuencia distinta y más seria que el coste de cómputo doble ya aceptado como
`#20`: no es dinero perdido, es historia perdida, y no es reversible desde ninguna sesión de código
ni de auditoría. Se registra como `#21`, `ABIERTO` (no `ASUMIDO` como `#20`, porque es información que
el dueño no ha visto todavía) — la acción que necesita, igual que `#20`, es de infraestructura sobre
su cuenta (detener la duplicidad de rutinas que compiten por el mismo `push`), no de código.

**Coherencia entre lo decidido y lo ejecutado.** Sin desviaciones nuevas que añadir a §7 de
`SEGUIMIENTO.md`. `ROADMAP_PRODUCTO.md` y `SEGUIMIENTO.md` §1 coinciden: cola de R-XX vacía, ninguna
T-XX/R-XX `PENDIENTE` salvo T-24b `BLOQUEADA` por hardware del dueño. `roadmap/FEEDBACK.md` sigue sin
ninguna entrada `nuevo` (solo la fila de plantilla vacía). Todo coincide entre documentos y con el
código — el hallazgo de esta pasada es sobre el *historial* del repositorio, no sobre su estado
actual, que sigue siendo internamente coherente.

**Invariantes de datos, verificados de nuevo contra el código (spot-check, no re-auditoría completa,
al no haber cambios de código desde la pasada anterior).**
- **(a) cobertura total:** sostenida, sin cambios en el área desde R-11.
- **(b) original recuperable / ediciones manuales respetadas:** sostenida, `revalidacion.py` intacto
  en contenido desde P-04/P-03 (confirmado leyendo el archivo, no solo citando un hash de commit).
- **(c) reproductor autocontenido, sin red:** reverificado por la cuarta red sobre el fixture real —
  `reproductor.html` y `guion-impresion.html` autocontenidos, catorce etapas en OK.
- **(d) runtime solo biblioteca estándar:** `pyproject.toml` sigue con `dependencies = []`;
  `mypy`/`ruff`/`pytest` solo en `requirements-dev.txt`.
- **(e) sin número mágico suelto / defaults en `SKILL.md`:** sin cambios en `config.py` desde la
  última verificación exhaustiva; no se repite la revisión completa por no haber código nuevo.
- **(f) nada se escribe fuera de la carpeta de salida / copia `.bak`:** sostenida, sin cambios en el
  área.

**Conclusión general.** Quinta pasada consecutiva sin trabajo de código que auditar: el contenido del
proyecto permanece exactamente donde lo dejó la pasada del 2026-09-08, con las cuatro redes en verde
y ningún invariante de producto degradado. Pero esta pasada encontró algo que las cuatro anteriores
no vieron por confiar en la cita de un hash sin volver a comprobarlo contra el día anterior: el
historial de `develop` para todo el tramo T-00–P-05 está colapsado en un único commit, con al menos
tres hashes citados como evidencia en auditorías recientes (`7176b46`, `8971150`, `1a40c84`) ya
inexistentes o inalcanzables desde `HEAD`. Registrado como `#21`, severidad alta, `ABIERTO` — el
contenido y la funcionalidad no están en riesgo (verificado de nuevo, independientemente del hash),
pero la trazabilidad commit-a-commit que el proyecto exige como norma permanente sí se ha perdido, de
forma irreversible, para esa primera fase. `#19` sigue siendo un límite teórico sin escenario
reproducido; `#20` sigue `ASUMIDO`, con el mismo diagnóstico de siempre y un matiz inerte sin
severidad propia (un disparador único, deshabilitado y caducado). Nada de esto exige una P-XX de
código — ambos hallazgos de infraestructura (#20 y #21) son, de nuevo, acción del dueño sobre su
cuenta, no de ninguna sesión de código.

### Auditoría 2026-09-08 — cuarta reconfirmación consecutiva sin cambios de código, clon sincronizado sin desajuste por primera vez en semanas

**Nota de arranque — cambio de síntoma, sin severidad propia.** A diferencia de las últimas
veintitantas sesiones documentadas, `git checkout develop && git pull origin develop` en esta
sesión resolvió en un **fast-forward limpio** (`7cc283b..518fe5a`, dos commits nuevos) sin ningún
HEAD *detached* ni historial huérfano que realinear. No hay forma de confirmar desde esta sesión
si el bloqueo #8 (rutinas duplicadas) se ha resuelto de fondo o si esta vez simplemente no coincidió
la carrera entre clones efímeros — `list_triggers`, más abajo, sigue mostrando las mismas seis
rutinas activas — pero se deja constancia del cambio porque es la primera sesión en mucho tiempo que
no necesita `git reset --hard`.

**Alcance.** Desde la pasada anterior (2026-09-07, commit `82e3ef4`) `git diff --stat 82e3ef4 HEAD`
confirma que los dos únicos commits nuevos tocan exclusivamente `roadmap/DECISIONES_TECNICAS.md`,
`roadmap/HISTORIAL_SESIONES.md`, `roadmap/ROADMAP_PRODUCTO.md` y `roadmap/SEGUIMIENTO.md` (ciclos de
reconfirmación de Programador y PM del 2026-09-07, seis y uno respectivamente): cero cambios en
`scripts/`, `tests/`, `SKILL.md`, `PROYECTO.md`, `DEVELOPERS.md` o `references/`. Cuarta pasada de
auditoría sin código nuevo que revisar desde la última con trabajo real (2026-09-05); el foco es,
igual que las tres anteriores, reverificar de forma independiente las cuatro redes y la coherencia
del propio registro.

**Verificación objetiva de las cuatro redes, repetida de forma independiente.** `pip install -r
requirements-dev.txt` limpio. `python -m mypy scripts/ tests/` → **limpio sobre 68 archivos**.
`python -m ruff check scripts/ tests/` → **limpio**. `python -m pytest` → **550 passed en 2.88s**,
mismo recuento que las tres pasadas anteriores. `python scripts/verificar_salidas.py --fixture` →
las **catorce etapas en OK**; `.pptx`/`.pdf` reales siguen LATENTES en este contenedor por las
mismas razones ya documentadas (sin la skill de marca `480-branded-pptx`, sin Chrome/Edge instalado)
— degradación esperada y documentada, no un fallo.

**Registro de hallazgos, reevaluado fila por fila.** Sin discrepancias: las filas `RESUELTO` siguen
citando evidencia de archivo:línea verificable, `#19` sigue `ABIERTO` y `#20` sigue `ASUMIDO` con el
resumen que ya tenían. No hace falta ninguna corrección de mantenimiento en esta pasada.

**`#19` reevaluado, sin cambios.** `git log -1 -- scripts/revalidacion.py` sigue devolviendo
`1a40c84` (2026-09-03, el commit de P-04): el archivo no se ha tocado desde entonces, así que el
límite teórico (comparación por conjunto/cantidad de anclas, no por contenido/orden) sigue exacto y
sin escenario reproducido. Se mantiene `ABIERTO`, sin escalar.

**`#20` reevaluado con verificación directa nueva de `list_triggers`.** Confirmado por esta sesión:
siguen existiendo exactamente las mismas **seis** rutinas para este proyecto, las seis con
`enabled: true` y los mismos `cron_expression`/`created_at` ya documentados —
`auditor-teleprompter` (`trig_01PUyc5iBFvJwY2Eu2iga9Ai`, `0 3 * * *`, creada 2026-08-31) junto a
`Auditor` (`trig_019V5UKE8jKMvA2LCneiTtTD`, mismo cron, creada 2026-08-25); `product-manager-teleprompter`
(`trig_01UeizxJHtmf1U8stMcdnAfy`, `0 19 * * *`, 2026-08-31) junto a `Product manager`
(`trig_01Gou6bJDBVucaAkfXYaynAz`, mismo cron, 2026-08-25); `programador-teleprompter`
(`trig_01FWDZPhNLTjaxS5zabErJbT`, `0 6-15 * * 1-5`, 2026-08-31) junto a `Programador`
(`trig_01RkE491KgehtmqBcoFUFFKz`, `0 6,8,10,12,14 * * 1-5`, solapado, 2026-08-25). Sin cambios
respecto a lo ya registrado. Se mantiene `#20` como `ASUMIDO`, sin escalar ni renotificar (sin
novedad desde la notificación del 2026-09-04): el fast-forward limpio de esta sesión (ver nota de
arranque) no basta por sí solo para dar el bloqueo por resuelto mientras las seis rutinas sigan
activas.

**Coherencia entre lo decidido y lo ejecutado.** Sin desviaciones nuevas que añadir a §7 de
`SEGUIMIENTO.md` (las cinco filas existentes siguen describiendo exactamente lo mismo).
`HOJA_DE_RUTA.md` permanece con un único commit en toda su historia (`7176b46`, T-28, 2026-09-02) y
sin ninguna modificación posterior — la regla de inmutabilidad se sigue respetando. (Nota aparte,
sin severidad propia: ese mismo commit introduce de una sola vez 77 archivos y ~18.700 líneas —
prácticamente todo el repositorio hasta T-28 —, consistente con lo que `HISTORIAL_SESIONES.md` ya
documenta como una reescritura y `force-push` del historial remoto por una sesión anterior; no es un
hallazgo nuevo, solo una confirmación directa de algo ya registrado.) `ROADMAP_PRODUCTO.md` confirma
la cola de R-XX vacía y remite a §1 de `SEGUIMIENTO.md`, que a su vez no tiene ninguna T-XX/R-XX
`PENDIENTE` salvo T-24b `BLOQUEADA` (clicker físico, decisión del dueño). `roadmap/FEEDBACK.md` sigue
sin ninguna entrada `nuevo`. Todo coincide entre documentos y con el código.

**Invariantes de datos, verificados de nuevo contra el código (spot-check, no re-auditoría completa,
al no haber cambios de código desde la pasada anterior).**
- **(a) cobertura total:** sostenida, sin cambios en el área desde R-11.
- **(b) original recuperable / ediciones manuales respetadas:** sostenida, `revalidacion.py` intacto
  desde P-04/P-03.
- **(c) reproductor autocontenido, sin red:** reverificado por la cuarta red sobre el fixture real —
  `reproductor.html` y `guion-impresion.html` autocontenidos, catorce etapas en OK.
- **(d) runtime solo biblioteca estándar:** `pyproject.toml` sigue con `dependencies = []`;
  `mypy`/`ruff`/`pytest` solo en `requirements-dev.txt`.
- **(e) sin número mágico suelto / defaults en `SKILL.md`:** sin cambios en `config.py` desde la
  última verificación exhaustiva; no se repite la revisión completa por no haber código nuevo.
- **(f) nada se escribe fuera de la carpeta de salida / copia `.bak`:** sostenida, sin cambios en el
  área.

**Conclusión general.** Cuarta pasada consecutiva sin trabajo de código que auditar: el proyecto
permanece exactamente donde lo dejó la pasada del 2026-09-07, con las cuatro redes en verde, el
registro de hallazgos coherente consigo mismo y ningún invariante degradado. `#19` sigue siendo un
límite teórico sin escenario reproducido; `#20` sigue `ASUMIDO`, a la espera de que el dueño decida
qué trío de rutinas conservar — reverificado de nuevo por acceso directo, sin cambios desde el
2026-09-04, pese a que el propio clon de esta sesión sincronizó sin incidencia por primera vez en
mucho tiempo. Nada exige tratamiento urgente en esta pasada.

### Auditoría 2026-09-07 — tercera reconfirmación consecutiva sin cambios de código, registro sin desajustes

**Nota de arranque, sin severidad propia — mismo síntoma que ya lleva dieciséis sesiones
documentado.** El clon efímero de esta sesión partía otra vez con `develop` local en HEAD
*detached*, apuntando a un historial de 4 commits (`f78a92c`…`74cd27f`) sin ancestro común con
`origin/develop` (52 commits de diferencia — `git merge-base --is-ancestor` lo confirma: ninguno de
los dos historiales es antepasado del otro). Realineado con `git reset --hard origin/develop`
(árbol de trabajo limpio antes de la operación, nada local que perder). Mismo diagnóstico que el
resto de sesiones: consecuencia del bloqueo #8 (rutinas duplicadas), reverificado más abajo.

**Alcance.** Desde la pasada anterior (2026-09-06, commit `2bf65bd`) no ha habido ninguna sesión de
código: `git log f3a954b..HEAD` da cero commits nuevos — el propio HEAD de `origin/develop` es
todavía `f3a954b`, un ciclo de PM que solo reconfirmó el bloqueo #8 sin tocar `scripts/` ni `tests/`.
Tercera pasada consecutiva (2026-09-05 fue la última con trabajo de código real) sin nada nuevo que
auditar en el árbol de fuentes; el foco de esta pasada es, por tanto, reverificar de forma
independiente que nada se ha degradado en silencio y comprobar que el propio registro de hallazgos
sigue coherente con su narrativa (el único tipo de desajuste que esta auditoría ha encontrado en las
últimas pasadas).

**Verificación objetiva de las cuatro redes, repetida de forma independiente.** `pip install -r
requirements-dev.txt` limpio. `python -m mypy scripts/ tests/` → **limpio sobre 68 archivos**.
`python -m ruff check scripts/ tests/` → **limpio**. `python -m pytest` → **550 passed en 2.43s**,
idéntico recuento a las dos pasadas anteriores (sin código nuevo, no se esperaba otro número).
`python scripts/verificar_salidas.py --fixture` → las **catorce etapas en OK**; `.pptx`/`.pdf` reales
siguen LATENTES en este contenedor por las mismas razones ya documentadas (sin la skill de marca
`480-branded-pptx`, sin Chrome/Edge instalado) — degradación esperada y documentada, no un fallo.

**Registro de hallazgos, reevaluado fila por fila.** A diferencia de la pasada del 2026-09-06 (que
encontró cuatro filas `#15`-`#18` desfasadas respecto a su propia narrativa), esta vez la tabla ya
está coherente: las cuatro figuran `RESUELTO` con la evidencia de archivo:línea correcta. No hace
falta ninguna corrección de mantenimiento en esta pasada.

**`#19` reevaluado, sin cambios.** `git log -1 -- scripts/revalidacion.py` sigue devolviendo
`1a40c84` (2026-09-03, el commit de P-04): el archivo no se ha tocado desde entonces, así que el
límite teórico (comparación por conjunto/cantidad de anclas, no por contenido/orden) sigue exacto y
sin escenario reproducido. Se mantiene `ABIERTO`, sin escalar.

**`#20` reevaluado con verificación directa nueva de `list_triggers` (no solo releyendo
`SEGUIMIENTO.md`).** Confirmado por esta sesión: siguen existiendo exactamente las mismas **seis**
rutinas para este proyecto, las seis con `enabled: true` y los mismos `cron_expression` ya
documentados — `Auditor` (`trig_019V5UKE8jKMvA2LCneiTtTD`, `0 3 * * *`) junto a
`auditor-teleprompter` (`trig_01PUyc5iBFvJwY2Eu2iga9Ai`, mismo cron); `Product manager`
(`trig_01Gou6bJDBVucaAkfXYaynAz`, `0 19 * * *`) junto a `product-manager-teleprompter`
(`trig_01UeizxJHtmf1U8stMcdnAfy`, mismo cron); `Programador` (`trig_01RkE491KgehtmqBcoFUFFKz`,
`0 6,8,10,12,14 * * 1-5`) junto a `programador-teleprompter` (`trig_01FWDZPhNLTjaxS5zabErJbT`,
`0 6-15 * * 1-5`, solapado). Sin cambios de `updated_at` respecto a lo ya registrado el 2026-09-06.
Sigue siendo el síntoma más probable detrás del clon `detached` que abre esta misma narrativa y las
quince anteriores. Se mantiene `#20` como `ASUMIDO`, sin escalar ni renotificar (sin novedad desde
la notificación del 2026-09-04): repetir la misma información sin cambio sería ruido, no señal.

**Coherencia entre lo decidido y lo ejecutado.** Sin desviaciones nuevas que añadir a §7 de
`SEGUIMIENTO.md` (las cinco filas existentes siguen describiendo exactamente lo mismo).
`HOJA_DE_RUTA.md` sigue en v1.3, sin ninguna modificación desde T-17 (`git log` confirma que su
último commit real es `8971150`, T-19) — la regla de inmutabilidad se sigue respetando.
`ROADMAP_PRODUCTO.md` confirma la cola de R-XX vacía y remite a §1 de `SEGUIMIENTO.md`, que a su vez
no tiene ninguna T-XX/R-XX `PENDIENTE` salvo T-24b `BLOQUEADA` (clicker físico, decisión del dueño).
`roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo`. Todo coincide entre documentos y con el
código.

**Invariantes de datos, verificados de nuevo contra el código (spot-check, no re-auditoría completa,
al no haber cambios de código desde la pasada anterior).**
- **(a) cobertura total:** sostenida, sin cambios en el área desde R-11.
- **(b) original recuperable / ediciones manuales respetadas:** sostenida, `revalidacion.py` intacto
  desde P-04/P-03.
- **(c) reproductor autocontenido, sin red:** reverificado leyendo `PATRONES_RECURSO_EXTERNO` en
  `scripts/verificar_salidas.py` — los trece patrones de R-09 siguen activos y la cuarta red confirma
  `reproductor.html` y `guion-impresion.html` autocontenidos sobre el fixture real.
- **(d) runtime solo biblioteca estándar:** `pyproject.toml` sigue con `dependencies = []`;
  `mypy`/`ruff`/`pytest` solo en `requirements-dev.txt`.
- **(e) sin número mágico suelto / defaults en `SKILL.md`:** sin cambios en `config.py` desde la
  última verificación exhaustiva; no se repite la revisión completa por no haber código nuevo.
- **(f) nada se escribe fuera de la carpeta de salida / copia `.bak`:** sostenida, sin cambios en el
  área.

**Conclusión general.** Tercera pasada consecutiva sin trabajo de código que auditar: el proyecto
permanece exactamente donde lo dejó la pasada del 2026-09-06, con las cuatro redes en verde, el
registro de hallazgos ya coherente consigo mismo (sin el desajuste de mantenimiento que sí hubo que
corregir la pasada anterior) y ningún invariante degradado. `#19` sigue siendo un límite teórico sin
escenario reproducido; `#20` sigue `ASUMIDO`, a la espera de que el dueño decida qué trío de rutinas
conservar — verificado de nuevo por acceso directo, sin cambios desde el 2026-09-04. Nada exige
tratamiento urgente en esta pasada.

### Auditoría 2026-09-06 — reconfirmación sin cambios de código, corrección de un desajuste en el propio registro de hallazgos

**Nota de arranque, sin severidad propia.** El clon efímero de esta sesión partía otra vez con
`develop` local en HEAD *detached*, apuntando al mismo historial huérfano de 4 commits sin ancestro
común con `origin/develop` (52 commits de diferencia) — decimoquinta vez consecutiva con el mismo
síntoma, ya diagnosticado por el PM el 2026-09-04 como bloqueo #8 (rutinas programadas duplicadas).
Realineado con `git reset --hard origin/develop` (árbol de trabajo limpio, nada local que perder).

**Alcance.** Desde la pasada anterior (2026-09-05) no ha habido ninguna sesión de código: el único
commit en `develop` es un ciclo de PM (2026-09-05) que reconfirma la cola de producto vacía y el
bloqueo #8 sin novedad, sin tocar `scripts/` ni `tests/`. Esta pasada es por tanto una
reconfirmación: repite las cuatro redes de forma independiente, revisa la coherencia
decisión-ejecución y —a diferencia de una simple relectura— audita también el propio documento de
auditoría, que es donde apareció el único hallazgo real de esta pasada.

**Verificación objetiva de las cuatro redes, repetida de forma independiente.** `pip install -r
requirements-dev.txt` limpio. `python -m mypy scripts/ tests/` → limpio sobre 68 archivos. `python -m
ruff check scripts/ tests/` → limpio. `python -m pytest` → **550 passed**, idéntico al recuento de la
pasada anterior (sin código nuevo, no se esperaba otro número). `python scripts/verificar_salidas.py
--fixture` → las catorce etapas en `OK`, mismo resultado que las dos pasadas previas; `.pptx`/`.pdf`
reales siguen LATENTES en este contenedor por las mismas razones de siempre (sin la skill de marca,
sin Chrome/Edge), degradación documentada y no fallo.

**Hallazgo nuevo — desajuste dentro del propio registro de hallazgos, corregido en esta pasada, sin
número propio por ser un error de mantenimiento del documento y no del proyecto auditado.** La
narrativa de la auditoría 2026-09-05 afirma explícitamente, con evidencia de código, que R-10 y R-11
cierran `#15` a `#18` ("cerrando `#15` de verdad", "cerrando... `#16`", etc.) y los tres documentos
vivos del PM (`DECISIONES_TECNICAS.md`, `ROADMAP_PRODUCTO.md`, `SEGUIMIENTO.md`, todos con fecha
2026-09-05) dan por hecho ese cierre. Pero la fila de la tabla de las cuatro entradas `#15`-`#18`
seguía literalmente con `Estado = ABIERTO` y la redacción PREVIA al arreglo (la descripción del
hallazgo, no su cierre) — un desajuste entre lo que la pasada anterior concluyó y lo que dejó escrito
en el propio registro rastreable, que es exactamente el tipo de deriva silenciosa que este documento
existe para vigilar en el proyecto, y que en esta ocasión apareció en sí mismo. Verifiqué las cuatro
correcciones contra el código real antes de tocar la tabla, no me fié de la narrativa previa: `#15`
(`entrada.py:118`, normalización CRLF confirmada), `#16` (`tomas.py:186-215`,
`RegistroTomasError` confirmado), `#17` (`ResultadoCapitulos.titulos_sobrantes` confirmado en
`capitulos_youtube.py`) y `#18` (`test_srt_alineado_y_capitulos_youtube_son_coherentes_entre_si`
confirmado en `tests/test_integracion_montaje.py`). Las cuatro filas se corrigen a `RESUELTO` en el
registro de arriba, con la evidencia de archivo:línea que faltaba. No abro un `#ID` nuevo porque no
es un hallazgo sobre el código del proyecto: es una corrección de mantenimiento sobre este mismo
documento, y la propia instrucción del encargo pide reevaluar los `ABIERTO` contra el código en cada
pasada, no limitarse a repetir el estado de la tabla.

**`#19` reevaluado, sin cambios.** `scripts/revalidacion.py` no se ha tocado desde P-04 (2026-09-03,
último commit sobre ese archivo); sigue siendo el mismo límite teórico sin escenario reproducido.

**`#20` reevaluado.** Bloqueo #8 (rutinas duplicadas) sigue `ABIERTO` en `SEGUIMIENTO.md` §3, sin
cambios desde su notificación al dueño el 2026-09-04 — el propio síntoma de esta sesión (clon
detached, historial huérfano) es la decimoquinta repetición consecutiva. Se mantiene como `#20`,
`ASUMIDO`, sin escalar: sigue siendo una acción operativa sobre la cuenta del dueño, ya notificada,
fuera del alcance de cualquier sesión de código o de auditoría.

**Coherencia entre lo decidido y lo ejecutado.** Sin desviaciones nuevas que añadir a §7 de
`SEGUIMIENTO.md`. `HOJA_DE_RUTA.md` sigue en v1.3 sin ninguna modificación desde T-17 — la regla de
inmutabilidad se sigue respetando. `ROADMAP_PRODUCTO.md` y `SEGUIMIENTO.md` §1 coinciden entre sí y
con el código: cola de R-XX vacía, T-24b sigue BLOQUEADA a la espera del clicker real, ninguna otra
tarea PENDIENTE.

**Invariantes de datos, verificados de nuevo contra el código (spot-check, no re-auditoría completa,
al no haber cambios de código desde la pasada anterior).**
- **(a) cobertura total:** sostenida; `#17` sigue exponiendo `titulos_sobrantes` en vez de descartar
  en silencio.
- **(b) original recuperable:** sostenida, sin cambios en el área.
- **(c) la edición manual manda:** sostenida; `revalidacion.py` intacto desde P-04, `#15` (CRLF)
  sigue cerrado de verdad.
- **(d) sin borrado destructivo:** sostenida, sin cambios en el área.

**Salida autocontenida y cero red.** Reverificado leyendo `PATRONES_RECURSO_EXTERNO` en
`scripts/verificar_salidas.py`: los trece patrones de R-09 siguen activos (http(s), CDN, hoja de
estilos enlazada, `@import`, `fetch`, `XMLHttpRequest`, `src=` externo, `<object>`, `<embed src>`
externo, `<base href>`, `WebSocket`, `EventSource`/`sendBeacon`, `url(...)` externo), con la excepción
`data:` donde corresponde. Runtime sigue sin dependencias fuera de la biblioteca estándar
(`dependencies = []` en `pyproject.toml`).

**Conclusión general.** Segunda pasada consecutiva sin trabajo de código que auditar: el proyecto
permanece exactamente donde lo dejó la pasada anterior, con las cuatro redes en verde y ningún
invariante degradado. El único hallazgo real de esta sesión no fue en el código del proyecto sino en
el propio documento de auditoría — la tabla de hallazgos se había quedado un paso por detrás de su
propia narrativa, dejando cuatro filas `ABIERTO` que la pasada anterior ya había cerrado con evidencia
de código. Corregido en esta misma pasada. No queda ningún hallazgo `ABIERTO` de código sin enrutar
(`#19` sigue siendo un límite teórico sin escenario reproducido, ya razonado por qué no merece R-XX
propia); `#20` sigue `ASUMIDO`, a la espera de que el dueño decida qué trío de rutinas conservar. Nada
exige tratamiento urgente en esta pasada.

### Auditoría 2026-09-05 — cierre de F-E/F-F (R-10, R-11), cola de producto vacía, confirmación del bloqueo de infraestructura #8

**Nota de arranque, sin severidad propia — mismo síntoma que ya lleva trece sesiones documentado.**
El clon efímero de esta sesión partía otra vez con `develop` local en HEAD *detached*, apuntando al
mismo historial huérfano de 4 commits (esqueleto muy temprano) sin ancestro común con
`origin/develop` (52 commits de diferencia). Realineado con `git reset --hard origin/develop`
(árbol de trabajo limpio antes de la operación, nada local que perder). No lo trato como hallazgo
nuevo: el equipo ya lo diagnosticó el 2026-09-04 y lo conectó con una causa plausible (bloqueo #8,
rutinas duplicadas) — ver más abajo, donde confirmo esa lectura de forma independiente.

**Alcance.** Desde la pasada anterior (2026-09-04, que auditó la oleada R completa y abrió `#15`
a `#19`) el equipo ha completado **R-10** (robustez multiplataforma en Windows: CRLF, `write_text`
con `newline="\n"`, skip del test del bit de ejecución en no-POSIX) y **R-11** (robustez de datos
derivados del rodaje: toma buena ambigua, títulos de capítulo sobrantes, test de coherencia cruzada
`.srt` alineado/capítulos de YouTube), cerrando `#15` a `#18`. Un ciclo de PM archivó ambas fases
(F-E, F-F) a `ROADMAP_HISTORICO.md` y confirmó, en varios ciclos sucesivos sin sesión de código, que
la cola de producto sigue vacía — hasta que el último de esos ciclos encontró y documentó el
bloqueo #8 (rutinas programadas duplicadas). Esta pasada verifica ese tramo completo de forma
independiente, código y no solo narrativa, y presta atención especial a si el hallazgo de
infraestructura del último ciclo de PM merece una lectura distinta desde fuera del proyecto.

**Verificación objetiva de las cuatro redes, repetida de forma independiente.** `pip install -r
requirements-dev.txt` limpio. `python -m mypy scripts/ tests/` limpio. `python -m ruff check
scripts/ tests/` limpio. `python -m pytest` → **550 passed**, coincide con el recuento que narra
`DECISIONES_TECNICAS.md`/`SEGUIMIENTO.md` (antes 541, +9 de R-10/R-11). `python
scripts/verificar_salidas.py --fixture` → las catorce etapas en `OK`, mismo resultado que la pasada
anterior; `.pptx`/`.pdf` reales siguen LATENTES en este contenedor por las mismas razones de
siempre (sin la skill de marca, sin Chrome/Edge), degradación documentada y no fallo.

**R-10 y R-11 verificadas leyendo el código real, no los mensajes de commit.** `entrada.leer_guion`
normaliza `\r\n`/`\r` a `\n` justo después de `decode("utf-8-sig")` (`scripts/entrada.py`), cerrando
`#15` de verdad — comprobado también que los otros once `Path.write_text(...)` de `scripts/` fijan
`newline="\n"` explícito (los dos que mi primer grep de una sola línea no encontró, en `estado.py` y
`monitorizacion.py`, sí lo tienen: el parámetro cae en su propia línea dentro de una llamada
multilínea, falso negativo de mi propio grep, no del código) y que el test de guarda léxico
(`test_ninguna_salida_generada_reintroduce_saltos_de_linea_de_plataforma`) los cubre a los catorce.
`tomas.duracion_toma_buena` ahora levanta `RegistroTomasError` con más de una toma `buena` por
escena en vez de elegir la primera en silencio (`#16`), con el número de escena en el mensaje;
`capitulos_youtube.calcular_capitulos` expone `titulos_sobrantes` cuando sobran títulos de capítulo
(`#17`); `tests/test_integracion_montaje.py` gana el test de coherencia cruzada `.srt` alineado /
capítulos de YouTube (`#18`). Las tres decisiones de diseño están razonadas en
`DECISIONES_TECNICAS.md` (2026-09-04) y coinciden exactamente con el código: la validación de
exclusividad vive en el punto de LECTURA (`duracion_toma_buena`, compartida por R-04/R-05/R-07), no
en el de carga, precisamente para cubrir también la edición manual de `estado.json` y no solo el
`.json` exportado — el mismo criterio que ya se aplicó en `#9`/`#14` de no conformarse con blindar
la vía "normal". Ningún número mágico nuevo, ninguna dependencia añadida, `SKILL.md` y
`references/contrato-tomas.md` actualizados en la misma sesión que el código, no después.

**`#19` reevaluado, sin cambios.** `revalidacion.py` no se ha tocado desde la auditoría anterior:
sigue siendo el mismo límite teórico sin escenario reproducido, correctamente sin R-XX propia por
las mismas razones ya registradas por el PM (2026-09-04).

**El hallazgo de infraestructura (bloqueo #8), confirmado de forma independiente.** No es un
hallazgo de este auditor — lo detectó y documentó el propio PM el 2026-09-04, con el detalle exacto
(seis `trig_...`, cron de cada uno, fechas de creación) en `SEGUIMIENTO.md` §3 y
`DECISIONES_TECNICAS.md` — pero como esta pasada es la primera desde entonces, verifiqué la lectura
en vez de darla por buena sin más: la nota de arranque de esta misma sesión (`develop` local
detached, sin ancestro común con `origin/develop`) es exactamente el síntoma que el PM lleva trece
sesiones registrando y que conectó con el bloqueo #8 como causa plausible. No tengo acceso a
`list_triggers` desde este rol para confirmar el número exacto de rutinas por mi cuenta, así que no
puedo verificar el hecho en sí, solo su síntoma observable — coincide con lo narrado. Registrado como
**`#20`, severidad media, estado ASUMIDO**: es una acción operativa sobre la cuenta del dueño, ya
notificada y fuera del alcance de cualquier sesión de código o de auditoría, no un hallazgo que deba
convertirse en tarea. Lo dejo con severidad propia (no simplemente "ver bloqueo #8") porque el coste
acumulado es real (cómputo doble desde hace más de una semana, riesgo de condición de carrera entre
clones efímeros escribiendo casi a la vez sobre `origin/develop`) y porque el propio registro de
hallazgos es el sitio donde este documento vigila que nada se pierda por estar "fuera del código".

**Coherencia entre lo decidido y lo ejecutado.** Sin desviaciones nuevas que añadir a §7 de
`SEGUIMIENTO.md`. `HOJA_DE_RUTA.md` sigue en v1.3, sin ninguna modificación desde la pasada anterior
— la regla de inmutabilidad se sigue respetando. `ROADMAP_PRODUCTO.md` y `SEGUIMIENTO.md` §1
coinciden: cola de R-XX vacía, las dos fases F-E/F-F archivadas en `ROADMAP_HISTORICO.md` con su
spec completa. `roadmap/FEEDBACK.md` sigue con cero entradas `nuevo`, coherente con que el bloqueo
#7 (grabar un curso real) sigue sin resolverse.

**Invariantes de datos, verificados de nuevo contra el código.**
- **(a) cobertura total:** sostenida; `#17` (títulos de capítulo sobrantes) ya no descarta sin
  rastro, ahora expone `titulos_sobrantes`.
- **(b) original recuperable:** sostenida, sin cambios en el área en esta pasada.
- **(c) la edición manual manda:** sostenida — R-10/R-11 no tocan `revalidacion.py` ni el mecanismo
  de identidad ancla/partición. El riesgo real que quedaba sobre este invariante (`#15`, CRLF) está
  cerrado de verdad.
- **(d) sin borrado destructivo:** sostenida, sin cambios en el área.

**Salida autocontenida y cero red.** Reverificado con el patrón completo de
`PATRONES_RECURSO_EXTERNO` (los seis de R-09 más los originales) y una búsqueda propia en
`guion.js` de `fetch`/`XMLHttpRequest`/`WebSocket`/`EventSource`/`sendBeacon`: sin coincidencias.
Runtime sigue sin dependencias fuera de la biblioteca estándar (`dependencies = []` en
`pyproject.toml`).

**Conclusión general.** El proyecto cerró F-E y F-F sin introducir deuda nueva de las categorías que
esta auditoría vigila: R-10 y R-11 son cierres reales, no maquillados, verificados línea a línea
contra `#15`-`#18`, y no tocan ninguno de los invariantes centrales que motivaron `#9`/`#14`. La
única nota que merece seguimiento no es de código: es el bloqueo #8 (rutinas duplicadas), que esta
pasada confirma de forma independiente por su síntoma observable y tiene coste acumulado real
aunque esté fuera del alcance de cualquier sesión de código o de auditoría — quedará como `#20`
hasta que el dueño decida qué trío conservar. Nada exige tratamiento urgente de código en esta
pasada; el backlog de producto sigue legítimamente vacío a la espera del primer rodaje real
(bloqueo #7) o de una nueva pasada de esta misma auditoría.

### Auditoría 2026-09-04 — oleada R completa (R-01 a R-09) + endurecimiento de #14 (P-04/P-05), primera pasada tras el rodaje real

**Nota de arranque, sin severidad propia.** El clon efímero de esta sesión partía con `develop`
local desalineado del remoto: apuntaba a un historial huérfano de 4 commits (esqueleto muy
temprano), sin ancestro común con `origin/develop` (53 commits) — una sesión anterior ya había
detectado y corregido exactamente este mismo desajuste (`SEGUIMIENTO.md`, sesión de R-09) sin que
volviera a ocurrir por causa del propio proyecto; es un artefacto del entorno de sesión, no del
código. Realineado con `git reset --hard origin/develop` (árbol de trabajo limpio antes de la
operación, nada local que perder). Se deja constancia por si se repite: si vuelve a pasar en
sesiones sucesivas, merece investigarse como incidencia de infraestructura, no seguir
resolviéndose en silencio cada vez.

**Alcance.** Desde la pasada anterior (2026-09-03, que auditó T-22 a T-33 y abrió `#14`) el equipo
ha completado **toda la oleada R** (R-01 a R-09, oleadas v2/v3 y fase transversal F-D, las nueve
`COMPLETADA`), cerrado y endurecido `#14` (P-03 y P-04), corregido un bug real de instalación
detectado en la máquina del dueño (P-05), completado por fin T-32 con instalación real y health
check en Windows (11/11 OK), y registrado `R-10` (PENDIENTE) a partir de hallazgos de esa sesión
real. Un ciclo de PM (2026-09-03) archivó las oleadas ya entregadas a `ROADMAP_HISTORICO.md`. Esta
pasada audita todo ese tramo: no relee lo que el equipo narra, lo verifica de forma independiente
—código, tests propios y ejecución real de las cuatro redes— y busca específicamente lo que el
propio equipo, por estar dentro del proyecto, podría no haber visto.

**Verificación objetiva de las cuatro redes, repetida de forma independiente.** `pip install -r
requirements-dev.txt` (limpio, confirma una vez más que el runtime no las necesita). `python -m
mypy scripts/ tests/` → limpio sobre 68 archivos. `python -m ruff check scripts/ tests/` → limpio.
`python -m pytest` → **541 passed**, coincide exacto con lo que narra `SEGUIMIENTO.md` (antes 402).
`python scripts/verificar_salidas.py --fixture` → las **catorce** etapas en `OK` (antes diez):
`.srt` alineado y capítulos de YouTube nuevos desde R-05/R-07, ambos cayendo honestamente a la
estimación de T-12 porque `fixtures/guion-ejemplo.md` nunca se grabó de verdad — degradación
documentada, no fallo. `.pptx`/`.pdf` reales siguen LATENTES en este contenedor por las mismas
razones de siempre (sin la skill de marca, sin Chrome/Edge). Ninguna etapa NO APLICABLE.

**Cierre verificado de los seis hallazgos `ABIERTO` heredados (#5, #6, #10, #11, #12, #13).**
Encargué una verificación independiente completa, leyendo el código real y no los mensajes de
commit: las seis R-XX que el equipo dice haberlos cerrado (R-01, R-06, R-08 ×3, R-09) los cierran
de verdad, con evidencia de archivo:línea para cada uno (detalle en la tabla de arriba). Ninguno
quedó a medias ni maquillado. Dos matices que el propio equipo no señaló, ninguno grave: (1) el
validador de auto-contención (#13/R-09) marca `<object data="data:...">` como hallazgo aunque esté
embebido en base64, a diferencia de `<embed>`/`src=` — verificado que es una política **deliberada
y documentada** en `references/validador-autocontencion.md`, no una inconsistencia; (2) el propio
endurecimiento de P-04 sobre `#14` (`_incidencias_anclas_desajustadas`) compara solo la
**cantidad** de anclas por escena, no su disposición — asimetría teórica sin escenario real que la
dispare hoy, registrada como **#19** para que no se pierda de cara a una futura revisión de
`revalidacion.py`.

**`#14` reverificado, sigue cerrado, y su endurecimiento (P-04) resiste el mismo tipo de ataque.**
Además de los dos tests de regresión de P-03, confirmé que `_particiones_pospuestas_previas` hace
lectura tolerante de verdad: basura en `estado.validacion["particiones_pospuestas"]` (no-dict,
claves no convertibles, valores `None`) no aborta la revalidación, degrada a `{}` y sigue —
exactamente lo que P-04 prometía y que un `estado.json` corrupto o anterior a P-03 necesita para no
reproducir `#14` en silencio. La "incidencia de anclas" nueva es defensa en profundidad real, no
cosmética: se dispara cuando el documento en disco no trae las anclas que la reconstrucción
esperaba (p. ej. ese mismo `estado.json` antiguo). Mensaje de conflicto corregido: ya no promete
que "revalidar sin tocar el bloque" materializa la partición, afirmación que P-03 había dejado sin
corregir y que era literalmente falsa.

**Hallazgos nuevos en la oleada R (rodaje real), ninguno urgente pero todos reales.** Encargué una
revisión dedicada de R-02 a R-07 (tomas, tropiezos, calibración, `.srt` alineado, capítulos de
YouTube) contra los cuatro invariantes y contra el patrón de "cobertura fina sospechosa" que
produjo `#9`/`#14` en `revalidacion.py` — ningún módulo nuevo se acerca a esa proporción
(líneas/test entre ~12 y ~29, frente a las ~35-46 de `revalidacion.py` cuando apareció el bug).
Aun así, aparecieron tres huecos reales, todos de severidad baja o media, ninguno con incidente
observado en material real:
- **#16 (media):** `tomas.duracion_toma_buena` no detecta que dos tomas lleguen marcadas `buena`
  para la misma escena en el `.json` — elige la primera en silencio. La exclusividad solo la
  garantiza el lado JS (`finalizarTomaActual`), nunca la función Python que R-04, R-05 **y** R-07
  comparten como única fuente de "duración real". Es el tipo de punto único de fallo silencioso
  que el propio proyecto ya sabe identificar y cerrar (mismo espíritu que `#9`/`#14`, aunque de
  impacto menor: un dato de rodaje mal atribuido en una salida derivada, no pérdida del guion de
  origen). Reproducido con datos sintéticos en esta auditoría.
- **#17 (baja):** `capitulos_youtube.calcular_capitulos` descarta en silencio los títulos de
  capítulo sobrantes cuando hay más filas en la sección «Capítulos» que escenas en el guion — el
  caso simétrico (menos títulos que escenas) sí está cubierto por un test, este no.
- **#18 (baja):** sin test de integración cruzada entre `.srt` alineado y capítulos de YouTube pese
  a compartir literalmente la misma fuente de duración real — el mismo tipo de brecha que
  `tests/test_integracion_montaje.py` (T-33) cerró una vez para `.srt`/`tarjetas.json`, sin
  extenderse todavía a estas dos salidas más recientes de R-05/R-07.

Lo positivo de esta oleada, verificado y no solo leído: el diseño de identidad de "tropiezo" por
**texto exacto** (nunca por índice) en vez de reabrir el problema de `revalidacion.py` es una
decisión defensiva correcta y explícitamente razonada así en `references/contrato-tropiezos.md`;
`calibracion.py` no toca `tiempos.calcular_tiempos`, que sigue siendo la única fuente de tiempos;
y `.srt` alineado/capítulos de YouTube comparten la misma función de duración real en vez de
reimplementarla cada uno, coherencia por construcción (aunque sin test que la confirme, `#18`).

**Hallazgo nuevo fuera de la oleada R — #15 (media): CRLF sin normalizar en `entrada.leer_guion`,
ya detectado por el propio equipo, todavía sin corregir tras nueve sesiones.** Verificado en el
código actual: `leer_guion` decodifica con `read_bytes()` + `decode("utf-8-sig")`, sin normalizar
`\r\n`/`\r`, mientras otras rutas de lectura del propio proyecto (`Path.read_text()`, usado en
`verificar_salidas.py` y otros módulos) sí aplican la traducción universal de saltos de línea de
Python — una asimetría real entre rutas de lectura del mismo proyecto. No es un hallazgo mío: lo
detectó el propio equipo en la primera sesión que corrió de verdad en el Windows del dueño (sesión
"T-32 desbloqueada + P-04"), lo dejó explícitamente como "propuesta y no ejecutada", y el PM lo
recuperó a tiempo como `R-10` antes de que se perdiera del todo (ocho sesiones lo habían dejado
pasar). Lo señalo aquí porque el riesgo que describe es exactamente del tipo que este documento
existe para vigilar —una comparación de texto que falla en silencio justo donde el invariante (c)
depende de que dos textos idénticos se reconozcan como idénticos— y porque ya es la tarea
`PENDIENTE` con más antigüedad sin tocar del backlog. Confirmado que `R-10` la especifica con el
rigor habitual (test con bytes `\r\n` explícitos, no dependiente de la plataforma que ejecuta el
test), así que no hace falta una P-XX adicional: solo que se ejecute pronto.

**Coherencia entre lo decidido y lo ejecutado, muestreada contra `DECISIONES_TECNICAS.md`.**
Contrasté la decisión de R-06 de sacar la migración de carpetas heredadas de `scripts/migraciones/`
(paquete reservado al esquema de `estado.json`, no a rutas del sistema de ficheros) pese a que la
ficha de `ROADMAP_PRODUCTO.md` sugería ese nombre — la desviación está documentada donde debe y es
técnicamente correcta: meter un archivo con el patrón de nombre de migración sin esa forma habría
roto `migraciones._migraciones_disponibles()`. Contrasté también el autoajuste del propio R-09
(corrección de un falso positivo real del patrón `url(...)` contra `URL.createObjectURL` del
reproductor, detectado por el test de guiones reales y corregido en la misma sesión antes de dar la
tarea por buena) — el tipo de autocorrección que demuestra que las cuatro redes se usan de verdad,
no se leen por encima. Sin desviaciones nuevas que añadir a §7 de `SEGUIMIENTO.md` más allá de las
ya registradas.

**Invariantes de datos, verificados de nuevo contra el código, no solo releídos.**
- **(a) cobertura total:** sostenida en el núcleo del pipeline; dos huecos menores y nuevos en
  salidas derivadas de la oleada R (`#16`, `#17`), ninguno toca el guion de origen ni descarta
  locución — el texto de origen sigue íntegro en ambos casos, solo una salida derivada pierde un
  dato sin avisar.
- **(b) original recuperable:** sostenida — `FEEDBACK.md` (R-03) es append-only de verdad, nunca
  reescribe una fila existente.
- **(c) la edición manual manda:** sostenida en el código de esta oleada — tomas y tropiezos viven
  fuera de `guion-escenas.md` (en `estado.json` y `FEEDBACK.md` respectivamente) y ninguno toca el
  mecanismo de identidad ancla/partición donde vivieron `#9`/`#14`. El riesgo real que queda sobre
  este invariante es `#15` (CRLF), no código nuevo de esta pasada.
- **(d) sin borrado destructivo:** sostenida — `feedback.registrar_tropiezos_en_feedback` hace
  copia `.bak-<marca>` antes de reescribir un `FEEDBACK.md` existente; `srt_alineado.py`/
  `capitulos_youtube.py` no necesitan `.bak` por ser derivados puramente regenerables, sin estado
  del dueño que perder — correcto y documentado como tal en el propio criterio de aceptación de
  R-07.

**Salida autocontenida y cero red.** Sostenidas: `guion.js` sigue sin `fetch`/`WebSocket`/
`XMLHttpRequest`; la exportación de tomas/tropiezos/preferencias usa `Blob`+`URL.createObjectURL`,
sin red. El validador se endureció de verdad en R-09 (seis patrones nuevos, 14 tests) y el fixture
pasa con las plantillas reales.

**Conclusión general.** Nueve sesiones de código después de la auditoría anterior, el proyecto
sigue sin introducir deuda nueva de las categorías graves que este documento vigila: los seis
hallazgos heredados están genuinamente cerrados, no solo declarados, y el hallazgo más grave del
histórico (`#14`) no solo sigue resuelto sino que su endurecimiento (P-04) resiste un ataque de
lectura tolerante que el propio equipo se propuso a sí mismo verificar. La oleada R añade
funcionalidad de rodaje real completa y bien aislada de los invariantes centrales, con solo deuda
menor propia (`#16`, `#17`, `#18`) del mismo tamaño y tipo que el proyecto ya sabe reconocer y
cerrar sin ayuda — ninguna exige tratamiento urgente. La única nota que merece más atención de la
que está recibiendo es `#15`/`R-10`: no es un hallazgo nuevo ni oculto, el propio equipo lo vio y
lo documentó con precisión, pero ha esperado nueve sesiones en la cola mientras se priorizaba
funcionalidad nueva sobre una corrección de robustez ya diagnosticada — y es precisamente el tipo
de deuda que, a diferencia de `#16`/`#17`/`#18`, ya se sabe que afecta a la máquina real del dueño,
no a un escenario hipotético. Recomiendo que sea la primera tarea de la próxima sesión de código,
antes de abrir ninguna R-XX nueva.

### Auditoría 2026-09-03 — backlog T-XX cerrado (T-22 a T-33), primera pasada tras el ciclo de PM

**Alcance.** Desde la pasada anterior (2026-09-02, T-00 a T-21) el equipo ha completado **todo el
backlog de tareas conocido**: T-22 a T-26 (reproductor: autoscroll, ayudas de grabación, atajos y
clicker, espejo, persistencia), T-27 a T-30 (salidas secundarias: `.srt`, `.pdf`, `.pptx`, selector
unificado), T-31 (`SKILL.md` y configuración completa) y T-33 (encaje con la cadena de montaje).
T-32 (instalación real) queda BLOQUEADA solo en su último tramo, que exige la máquina del dueño —
correctamente marcada así, no simulada. Además hubo un ciclo de **Product Manager** (sin código)
que revisó `auditoriacontinua.md` y creó `R-08`/`R-09` para los hallazgos #10-#13. Esta pasada
audita ese tramo completo: no solo relee lo que el equipo dice haber hecho, también lo verifica de
forma independiente y reproduce en código el límite que P-02 había dejado documentado como
pendiente.

**Verificación objetiva de las cuatro redes, repetida de forma independiente.** `python -m mypy
scripts/ tests/` → limpio sobre 57 archivos. `python -m ruff check scripts/ tests/` → limpio.
`python -m pytest` → **402 passed**, coincide exacto con lo que narra SEGUIMIENTO (402, antes 399).
`python scripts/verificar_salidas.py --fixture` → las diez etapas en `OK`, incluidas las seis que
ya no son NO APLICABLE desde T-27 a T-30 (`.srt`, HTML de impresión, `tarjetas.json`/brief, cada una
con su auto-contención o validez donde aplica); `.pptx` y `.pdf` reales quedan LATENTES por falta de
la skill de marca y de Chrome/Edge en esta máquina, exactamente como predicen sus propios requisitos
— no es un fallo, es la degradación documentada. No queda ninguna etapa NO APLICABLE: el hallazgo
#4 de la primera auditoría (31-08) está completamente cerrado, no solo parcialmente.

**Hallazgo nuevo — #14, severidad alta: el límite de P-02 es peor de lo que su propia nota dice.**
Al cerrar P-02 (2026-09-02), el equipo dejó escrito en `DECISIONES_TECNICAS.md` un "límite conocido,
no cerrado por esta P-XX", **verificado a mano**: en una revalidación posterior sin nuevo toque del
dueño, la mitad `'a'` de una partición podía quedarse con el texto editado completo y la mitad `'b'`
con "un fragmento del texto de ORIGEN sin editar". Esta pasada no se conformó con leer esa nota:
construí una reproducción de código independiente (guion sintético de dos bloques en la escena 1,
edición manual + partición aceptada sobre el bloque 0, bloque 1 intacto) y encadené dos
revalidaciones reales sobre `revalidacion.revalidar_guion`. El resultado es más grave que la nota:
la escena pasa de 2 a **3 bloques**, con el texto del bloque 1 **duplicado** (aparece intacto bajo
su propia identidad y una segunda vez, mal atribuido, como la mitad `'b'` de la partición del bloque
0) y la partición que el dueño aceptó **nunca llega a materializarse en dos mitades reales** — ni
en esta pasada ni en ninguna posterior, porque el mismo emparejamiento erróneo se repite indefinidamente
mientras el dueño no vuelva a tocar ese ancla a mano. Es exactamente el tipo de corrupción silenciosa
que el invariante (c) existe para impedir: el dueño abriría `guion-escenas.md` y vería un bloque de
más con texto repetido, sin ninguna incidencia que se lo señale — a diferencia de #9/P-02, aquí no
hay ni siquiera un aviso. Severidad alta por ser el mismo invariante central, no por la frecuencia
(el disparador requiere el mismo cruce estrecho que #9, más una segunda revalidación sin editar el
ancla en medio). Recomiendo tratarlo como P-XX urgente, igual que #9: la solución probablemente
pase por materializar la partición en la MISMA pasada donde deja de haber conflicto en vez de
esperar a que el emparejamiento por ancla la reconstruya sola, que es donde se cuela el error.

**El resto de hallazgos ABIERTO, reevaluados contra el código de esta pasada, sin cambios.** #5
(persistencia en `file://`, T-26) y #6 (nomenclatura de `assets/`/carpeta de salida) siguen
esperando a R-01 y R-06 (oleada v2, ninguna de las dos tocada todavía). #10 (colores de estado sin
migrar a `Configuracion`), #11 (`PROYECTO.md` con el ritmo antiguo) y #12 (desajuste de versión de
Python) verificados de nuevo uno a uno contra el código real: los tres literalmente intactos —
`estilo.css:139/143` sigue con los dos colores en literal, `PROYECTO.md:45` sigue diciendo «por
defecto 120», `pyproject.toml` sigue en `>=3.12`/`py312` con el intérprete real en 3.11.15 — ahora
correctamente agrupados en `R-08` (PENDIENTE) por el PM, coherente con el propio hallazgo. #13
(huecos del validador de auto-contención) también intacto, sin ningún patrón nuevo cubierto en
`verificar_salidas.py`, y correctamente en `R-09` (PENDIENTE). Ninguno de los cinco ha crecido ni se
ha visto agravado por el trabajo de T-22 a T-33: el equipo no ha tocado ninguna de esas áreas
todavía, como corresponde mientras R-08/R-09 sigan sin empezar.

**Coherencia entre lo decidido y lo ejecutado (T-22 a T-33 contra `DECISIONES_TECNICAS.md`).**
Contrasté una muestra amplia de decisiones —el mecanismo de scroll manual de T-22 en vez de
`scrollIntoView` nativo, el reparto de responsabilidades T-28/T-29 (el PDF y el `.pptx` reutilizan
`dimensiones_png`/`es_nota_interna`/`indicaciones_no_recitables` en vez de duplicar el criterio de
qué es nota interna), el uso de tuplas en vez de `dict` para `mapa_teclas_reproductor` (T-24) para
no romper la inmutabilidad del `Configuracion` congelado, y la detección de `--no-sandbox` para
Chrome solo cuando `os.geteuid() == 0` (T-28)— contra el código real: las cinco coinciden
exactamente. Ninguna reescribe la historia ni maquilla un resultado distinto al narrado.

**Invariantes de datos, verificados de nuevo contra el código, no solo releídos.**
- **(a) cobertura total:** sostenida, y ahora también verificada de extremo a extremo entre
  salidas: `tests/test_integracion_montaje.py` (T-33) confirma que `.srt` y `tarjetas.json`
  numeran las escenas de forma idéntica entre sí y contra el guion de origen, cerrando el hueco de
  que cada salida solo se validaba contra sí misma.
- **(b) original recuperable:** sostenida, sin cambios en esta pasada.
- **(d) sin borrado destructivo:** sostenida, y extendida correctamente a la nueva superficie de
  escritura fuera de la carpeta de salida del guion: `instalar_skill.sincronizar_skill` renombra
  cualquier instalación previa a `<nombre>.bak-<marca>` antes de escribir la nueva, mismo patrón
  que `documento_revision.guardar_documento_revision` usa para `guion-escenas.md`. Revisé también
  que ninguna de las nuevas funciones de escritura (`pdf.py`, `pptx.py`, `srt.py`, `convencion.py`)
  decide su propio `destino`: todas lo reciben del llamador, que sigue derivándolo de
  `entrada.carpeta_salida_para` — el único punto que verifica contención de ruta. Aislamiento
  intacto.
- **(c) la edición manual manda:** parcialmente sostenida — ver #14 arriba, el hallazgo central de
  esta pasada.

**Salida autocontenida y cero red.** Sostenidas en las diez etapas de `verificar_salidas.py
--fixture`: el HTML de impresión del PDF incrusta el logotipo como `data:image/png;base64,...`
(nunca una ruta relativa, que el propio validador rechazaría) y ninguna de las nuevas plantillas
introduce `http(s)://`/CDN/`fetch`. Cero `print()` fuera de `presentacion.py`, cero `console.log`
en `guion.js`, cero `TODO`/`FIXME` sueltos en todo `scripts/` (barrido completo, no solo del código
tocado esta sesión).

**Conclusión general.** El proyecto cerró la totalidad de su backlog de tareas conocido en esta
franja sin introducir ninguna deuda nueva de las categorías que esta auditoría vigila —números
mágicos, escritura fuera de la carpeta de salida, autocontención, documentación desincronizada—: los
cinco hallazgos menores que quedaban abiertos siguen exactamente donde estaban, ahora con oleada
asignada (R-08, R-09) en vez de sueltos. La única grieta real es #14, y es una grieta seria: nace de
la propia honestidad del equipo (P-02 documentó el límite en vez de ocultarlo) pero esta pasada
confirma que el límite es más profundo que "un fragmento de texto sin editar" — es duplicación de
contenido en el documento que el dueño revisa, sin aviso. Recomiendo que sea la primera P-XX urgente
de la próxima sesión de código, antes de empezar R-01, exactamente el mismo tratamiento que recibió
#9.

### Auditoría 2026-09-02 — primera revisión de código real (T-00 a T-21)

**Alcance.** Desde la última pasada (31-08, antes de que existiera código) el equipo ha completado
T-00 a T-21: todo el núcleo de análisis del guion (parser, clasificador, convención, troceo,
tiempos, normalización, detección, reescrituras), el ciclo de validación completo (documento de
revisión + revalidación) y las primeras cuatro tareas del reproductor (esqueleto, índice, avance
híbrido, resaltado/tema). Esta pasada audita ese código real —arquitectura, invariantes, robustez—,
no solo el andamiaje documental de la pasada anterior.

**Verificación objetiva de las cuatro redes.** Ejecuté `python scripts/ci.py` de forma
independiente, sin fiarme del resumen de SEGUIMIENTO: `mypy` limpio sobre 44 archivos, `ruff`
limpio, `pytest` en **288 passed, 1 skipped** (recontado a mano, coincide exacto con lo que narra
SEGUIMIENTO), y `verificar_salidas.py --fixture` en verde con las tres etapas aún NO APLICABLE
correctamente justificadas. Los 21 commits de tareas son atómicos, con prefijo `T-XX:`, uno por
tarea, ninguno en `master`. El relato de SEGUIMIENTO.md se corresponde con el estado real del
repositorio, no es una narrativa optimista.

**Invariantes de datos (a)-(d) — el núcleo del producto, verificado contra el código, no contra
la documentación.**
- **(a) cobertura total:** sostenida — test de reconstrucción real contra los tres guiones de
  calibración (`tests/test_clasificador.py`), sin huecos.
- **(b) original recuperable:** sostenida — el registro de reescrituras es append-only de verdad;
  un rechazo nunca toca `original`.
- **(d) sin borrado destructivo:** sostenida — `.bak-<marca_de_tiempo>` antes de cada sobrescritura
  de `guion-escenas.md`, probado en el ciclo de tres revalidaciones encadenadas.
- **(c) edición manual manda:** sostenida en el ciclo normal (tres pasadas encadenadas sin perder
  ninguna edición), pero **aparece un hueco real** en el cruce menos frecuente entre una edición
  manual y una partición de respiración aceptada sobre el mismo bloque, dentro de la misma
  revalidación: la identidad que localiza la edición del dueño no sobrevive a la materialización de
  la partición, y la edición se descarta en silencio en favor del texto derivado, sin aviso ni test
  que lo detecte. Es exactamente el tipo de fallo que este invariante existe para prevenir —el
  dueño perdería una corrección de texto sin saberlo—, aunque el disparador es estrecho y ningún
  guion real lo ha provocado todavía. → **#9**, severidad alta por tratarse del invariante que es
  la razón de ser del ciclo de validación, no por su frecuencia observada.

**Autocontención y cero red.** Sostenidas sin excepción: cero `urllib`/`requests`/`socket` en
`scripts/`, cero CDN/`@import`/`src=` externo en las plantillas del reproductor,
`dependencies = []` en `pyproject.toml`. El validador de auto-contención es real y forma parte de
la CI, no decorativo. Su cobertura de patrones tiene margen de mejora (no contempla
`<object>`/`<base href>`/`WebSocket`) que hoy no importa porque nada los usa, pero conviene
cerrarlo antes de que T-22 a T-26 —que van a seguir tocando `guion.js`— lo hagan sin querer.
→ **#13**.

**Sin números mágicos.** Sostenida en general: `config.py` es de verdad el único sitio con valores
por defecto, y T-19/T-20/T-21 han ido cerrando sus propios huecos sesión a sesión (el color de
acento del reproductor pasó de literal a `Configuracion` en la propia T-21, según consta en
`DECISIONES_TECNICAS.md`). Encontré dos colores de estado del índice (`grabada`/`revisada`) que
quedaron fuera de ese barrido — deuda menor, del mismo tipo que el propio proyecto ya sabe
identificar y cerrar. → **#10**.

**`SKILL.md` sigue siendo un borrador, como declara su propia cabecera.** Cerca de la mitad de los
campos de `Configuracion` (pausas por puntuación, umbrales de detección, límites de velocidad,
calibración manual de ppm) no están todavía en su tabla de valores por defecto. **No es un hallazgo
nuevo:** es exactamente el hueco que T-31 existe para cerrar, y `SKILL.md` lo declara honestamente
desde su primera línea («BORRADOR (T-00)»). Se deja constancia aquí solo para confirmar que la
brecha tiene el tamaño esperado a esta altura del backlog y no ha crecido de forma descontrolada.

**Coherencia documental.** Contrasté varias decisiones citadas en `DECISIONES_TECNICAS.md` (T-06,
T-12, T-14, T-18, T-20) contra el código real: las cinco coinciden exactamente, sin ninguna
narrativa que se aparte de lo implementado. El único documento que se ha quedado atrás es
`PROYECTO.md`, que se declara a sí mismo «cambia poco» pero no siguió a T-12 cuando el ritmo dejó
de ser «120 ppm por defecto» para pasar a «deducido del guion, 120 de respaldo» — inconsistencia de
redacción, no de comportamiento (el código y `SKILL.md` sí están al día). → **#11**. También
localicé que `pyproject.toml` pide Python ≥3.12 mientras el intérprete real de las sesiones de nube
es 3.11.15; ya está mitigado (T-06 evitó a propósito sintaxis exclusiva de 3.12) pero el desajuste
de fondo sigue sin corregirse. → **#12**.

**Arquitectura y calidad de código.** El pipeline está bien factorizado y cada módulo respeta su
frontera: `tiempos.calcular_tiempos` sigue siendo la única fuente de tiempos (T-12), nadie
recalcula por su cuenta; `config.py` centraliza de verdad los valores por defecto sin lógica de
negocio dispersa. El punto más cargado es `revalidacion.py`: una función de 371 líneas que
reconcilia identidades de bloque entre pasadas, con solo 8 tests frente a los 25-28 de módulos de
complejidad comparable (`normalizacion.py`, `reproductor.py`) — la cobertura más fina de todo el
pipeline es, no por casualidad, donde apareció el hallazgo #9. Manejo de errores consistente
(una excepción por módulo con mensaje ya accionable en español); no hay `TODO`/`FIXME` sueltos ni
`print()` fuera de `presentacion.py`. `entrada.py` está genuinamente blindado contra entradas
hostiles (codificación no UTF-8, guiones vacíos o desmesurados, rutas con traversal, tiempo de
proceso acotado sin `SIGALRM` por portabilidad a Windows).

**Cierro #8.** `DEVELOPERS.md` existe, con 934 líneas y una sección por cada tarea completada
(arquitectura, decisiones de diseño, cómo tocar cada módulo) — cumple de sobra lo que T-32 le pedía,
con antelación sobre esa tarea porque cada sesión ya lo actualiza al cerrar.

**Lo que sigue abierto y por qué no preocupa todavía.** #5 (persistencia en `file://`) y #6
(nomenclatura de `assets/`/carpeta de salida) siguen sin poder verificarse hasta T-26 y
T-32/R-06 respectivamente; ambos ya están enrutados a R-01 y R-06. Nada de severidad alta salvo
el nuevo #9, que sí debería tratarse como P-XX urgente antes de seguir con T-22 en adelante, por
tocar directamente el invariante que el propio encargo de esta auditoría señala como razón de ser
del proyecto.

**Conclusión general.** El proyecto mantiene, veintiuna tareas después, el mismo nivel de rigor que
impresionó en la auditoría de arranque: cada decisión no trivial está registrada con sus
alternativas descartadas y por qué, los cuatro invariantes de datos son el criterio real de diseño
—no una frase de la hoja de ruta—, y las cuatro redes de verificación son ciertas, no teatro. La
única grieta real que esta pasada encontró (#9) es precisamente el tipo de caso límite —dos
decisiones del dueño coincidiendo sobre el mismo bloque en la misma sesión— que es más difícil de
ver desde dentro del propio proyecto que desde la distancia de un auditor externo. El resto son
deudas menores, ya del tamaño y tipo que el propio equipo sabe reconocer y cerrar sin ayuda.

### Auditoría 2026-08-31 (segunda pasada) — reevaluación tras la sesión de T-00

Pasada corta de reevaluación, como manda el procedimiento: contrastar los hallazgos `ABIERTO`
contra el estado real y cerrar los que ya no existen. **Cinco de los ocho quedan RESUELTOS el
mismo día, incluidos los tres de severidad alta.**

- **#1 y #3 los cerró el dueño**, que era lo correcto: ninguno era decisión del agente. La rama
  pasa a `develop` con `master` reservada para su merge manual, y Poppins está instalada con los
  cinco pesos que la escala de marca necesita. Ambas resoluciones están donde deben —protocolo y
  `DECISIONES_TECNICAS.md`—, no solo en una conversación.
- **#2 y #4 los cerró el programador** en la misma sesión: `.gitignore` acotado vía P-01 y la
  cuarta red convertida en algo que dice la verdad en vez de pasar en vacío.
- **#7 se cierra por acumulación:** los tres logs han dejado de estar vacíos.

**Lo que sigue abierto y por qué no preocupa todavía.** #5 (persistencia en `file://`) y #6
(nomenclatura y separación de `assets/`) están enrutados a R-01 y R-06 y no pueden verificarse
hasta que exista reproductor. #8 (`DEVELOPERS.md`) es entregable de T-32.

**Observación de proceso, sin severidad.** La hoja de ruta, declarada inmutable, se ha modificado
tres veces (v1.0 → v1.2). Las tres son legítimas —dos correcciones de inicialización previas a la
primera sesión y un cambio de protocolo del dueño, que es el único autorizado— y las tres están
justificadas en su cabecera. Pero el margen se ha agotado: con T-00 ya commiteada, cualquier
cambio posterior de ese documento debería considerarse una anomalía y no una corrección. Se
vigilará en la próxima pasada.

### Auditoría 2026-08-31 — estado de partida (antes de la primera sesión del programador)

**Alcance.** No hay código todavía: el proyecto está en fase de arranque, con los documentos de
gobierno, tres guiones reales de calibración y los cuatro logotipos de marca. Por tanto esta
pasada audita **el propio andamiaje**: coherencia entre documentos, viabilidad del protocolo
contra la máquina real y suposiciones que el backlog da por buenas sin haberlas comprobado.

**Conclusión general.** El conjunto documental es sólido y poco frecuente en su nivel de
concreción: los invariantes están enunciados en términos verificables por test (cobertura total
del guión, original recuperable, edición manual autoritativa, salida autocontenida) y el backlog
está calibrado contra guiones reales, no contra suposiciones. Lo que falla no es el diseño, sino
**tres choques entre lo escrito y la máquina donde va a ejecutarse**, los tres detectados
midiendo, no leyendo.

**Lo que se ha verificado en esta pasada (no es opinión):**

- `git rev-parse --show-toplevel` → el repositorio **ya existe** y su raíz es el propio proyecto;
  `git branch -a` → `develop` (actual), `master`, `origin/develop`, `origin/master`. **No hay
  `main`.** El protocolo lo nombra siete veces. → **#1**
- `git check-ignore -v` → `assets/480_Gris.png` y `fixtures/reales/guion-09-proyectos.md` están
  ignorados por las dos únicas reglas del `.gitignore`. El commit inicial contiene 11 archivos,
  todos documentación. → **#2**
- Recuento de archivos de fuente en `C:\Windows\Fonts` y en las fuentes de usuario: **Poppins 0,
  Montserrat 0, Figtree 16, Calibri 6**. La decisión de marca del dueño no es aplicable tal cual
  en esta máquina. → **#3**
- `python -m mypy|ruff|pytest` → los tres ausentes. No es un hallazgo: es exactamente el trabajo
  de T-01 y T-03, y confirma que la red de seguridad aún no existe.
- Chrome y Edge presentes en sus rutas estándar: la vía de T-28 para el PDF es viable.

**Sobre #3, que es el más incómodo.** La decisión «Poppins» se tomó ayer con la información
disponible —la guía de marca dice que es la familia oficial— y es defendible. Pero en esta
máquina produce el peor de los resultados posibles: PDF en Calibri y PPTX en Figtree, dos
documentos con la misma marca y tipografías distintas, que es justo lo que la decisión pretendía
evitar. Las salidas son tres: instalar Poppins (y garantizar que esté allí donde se abra el
documento), aceptar Figtree —que ya está instalada y es lo que la skill de marca usa por
defecto—, o incrustar la fuente, que **choca con la regla de cero red y de no distribuir
binarios de fuentes sin licencia comprobada**. No es una decisión del agente.

**Coherencia entre lo decidido y lo escrito.** Buena. Las tres decisiones permanentes del dueño
(convención contractual con aviso, alcance de reescrituras, ritmo deducido del guión) están
promovidas a §0.2, que es donde el método manda que vivan, y cada tarea afectada las referencia
en lugar de duplicarlas. El único punto flojo es de registro, no de fondo: la hoja de ruta se
modificó dos veces antes de la primera sesión sin dejar rastro en los logs (**#7**). Es
legítimo —el dueño gobierna el documento y la propia cabecera lo explica— pero conviene fijar el
precedente ahora: a partir de la primera sesión del programador, ese documento no se toca.

**Riesgo estructural a vigilar (#4).** La verificación de cuatro redes es el corazón del modo
autonomía total, y la cuarta no puede pasar hasta T-32. Si nadie lo resuelve, el agente hará una
de dos cosas malas: saltársela sistemáticamente —y perder el hábito— o dar por buena una
comprobación vacía. La salida limpia es que T-00 cree el talón y que este vaya creciendo con cada
tarea que añada una salida, de modo que la cuarta red diga siempre algo verdadero.

**Lo que no es un hallazgo pero conviene tener presente.** La salida `.pptx` depende de dos
skills que no están instaladas (`480-branded-pptx` y la `pptx` de la que depende). Ya está
registrado como bloqueo #2 en §3 de SEGUIMIENTO, con la funcionalidad correctamente aislada: el
resto del producto no se ve afectado. Es el tratamiento correcto y no requiere acción del auditor.
