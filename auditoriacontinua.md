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
| #24 | 2026-09-16 | Proceso / coherencia roadmap-código | baja | ABIERTO | Patrón recurrente de latencia entre "tarea completada en código" y "prosa de `ROADMAP_PRODUCTO.md` actualizada para reflejarlo": ocurrió antes de la corrección del ciclo de PM del 2026-09-14 (ocho reconfirmaciones sucesivas del Programador señalando la prosa desactualizada de "Cola de producto" sin que nadie la corrigiera) y ha vuelto a ocurrir de forma prácticamente idéntica con R-17 — completada en código el 2026-09-15 a las 06:18 (`b9b6bcb`), pero `ROADMAP_PRODUCTO.md` siguió listándola como pendiente durante **nueve reconfirmaciones sucesivas del Programador** (07:10 a 15:08, mismo día) hasta que un ciclo de PM la corrigió a las 19:12 (`892e80f`). Es la segunda vez que se repite el mismo patrón pese a que la auditoría del 2026-09-15 dejó constancia expresa de "vigilar si el patrón se repite" — ya no es un hecho aislado. **No hay ningún riesgo real de trazabilidad**: `SEGUIMIENTO.md` §1 (la fuente autoritativa de estado, según su propio encabezado) reflejó `R-17 COMPLETADA` con la fecha correcta desde el primer ciclo de PM que la tocó, y ninguna decisión se tomó apoyándose en la prosa desactualizada de `ROADMAP_PRODUCTO.md` — es un documento narrativo secundario, no la fuente de verdad. El coste real es atención de sesión futura (nueve reconfirmaciones del Programador dedicando parte de su informe a señalar, sin corregir, algo que no es su documento). Se registra como hallazgo trazable, no como nota de vigilancia suelta, precisamente porque la vigilancia sin tarea ya falló una vez (es el mismo defecto de proceso que motivó abrir R-17 a partir de `#19`: un hallazgo señalado repetidamente sin enrutarse a acción). Sugerencia para el PM, no prescriptiva: que el propio ciclo de reconfirmación del Programador esté autorizado a corregir por sí solo la prosa de "Cola de producto" cuando se limite a reflejar un estado que `SEGUIMIENTO.md` §1 ya registra como `COMPLETADA` (sin decisión de producto nueva que tomar), en vez de esperar a que un ciclo de PM completo la alcance. **Reconfirmado en la pasada 2026-09-17: sigue ABIERTO, correctamente.** El PM no se lo concedió por su cuenta (leído su razonamiento del 2026-09-16 en `DECISIONES_TECNICAS.md`: cambiar quién escribe en qué documento es protocolo de §0.4, que solo cambia el dueño) y lo enruta como pregunta nueva #11 de `SEGUIMIENTO.md` §6, todavía `(pendiente)` de respuesta del dueño. Es la gestión correcta del hallazgo — no un hallazgo de código que este auditor deba resolver — así que se mantiene `ABIERTO` hasta que el dueño responda la #11. **Reconfirmado de nuevo en la pasada 2026-09-18, tras completarse R-18: la pregunta #11 sigue `(pendiente)` en `SEGUIMIENTO.md` §6 y esta vez la prosa de "Cola de producto" SÍ se actualizó en el mismo ciclo de PM que archivó R-18 (`DECISIONES_TECNICAS.md`, 2026-09-17), sin ninguna reconfirmación de más señalándolo — el patrón que motivó el hallazgo no se ha repetido una tercera vez. Sigue `ABIERTO` porque la pregunta de gobernanza en sí no tiene respuesta, no porque haya vuelto a fallar.** **Reconfirmado en la pasada 2026-09-19: cero commits de código desde la auditoría anterior (`8437367`), solo un ciclo de PM (`bdce88a`) que reconfirma la cola de producto vacía sin abrir ninguna R-XX y sin ningún cambio de prosa que corregir esta vez (no hay ninguna R-XX que archivar desde el 2026-09-17). La pregunta #11 de `SEGUIMIENTO.md` §6 sigue `(pendiente)` de respuesta del dueño, sin ningún nuevo ciclo de reconfirmación del Programador dedicando informe a señalarla sin corregirla. Sigue `ABIERTO` exclusivamente a la espera de esa respuesta.** **Reconfirmado en la pasada 2026-09-20: un único commit desde la auditoría anterior (`7a42b2f`), otro ciclo de PM reconfirmando la cola vacía sin código ni R-XX ni prosa que corregir. La pregunta #11 sigue `(pendiente)` en `SEGUIMIENTO.md` §6. Sigue `ABIERTO` exclusivamente por eso.** **Reconfirmado en la pasada 2026-09-21: un único commit desde la auditoría anterior (`b577c21`, séptimo ciclo consecutivo de PM, `c3bc66d`), otra reconfirmación de cola vacía sin código, sin R-XX y sin prosa que corregir. La pregunta #11 sigue `(pendiente)` en `SEGUIMIENTO.md` §6 — ya son cinco pasadas de auditoría (2026-09-17 a 2026-09-21) esperando exclusivamente esa respuesta. Sigue `ABIERTO` por lo mismo.** **Reconfirmado en la pasada 2026-09-22: once commits desde la auditoría anterior (`e7858c5`) — un noveno ciclo consecutivo de PM (`2e214d1`) y diez reconfirmaciones sucesivas del Programador, todos sin tocar `scripts/`, `tests/` ni ningún otro archivo fuera de `roadmap/`. El único contenido no repetitivo es una nota del PM en `DECISIONES_TECNICAS.md`/`ROADMAP_PRODUCTO.md` (2026-09-21) registrando, sin abrir R-XX, la idea de asociar cada toma buena con su archivo de vídeo real para una futura lista de concatenación de ffmpeg — aparcada explícitamente hasta que se resuelva el bloqueo #7, no una prosa desactualizada del patrón que motivó este hallazgo. La pregunta #11 sigue `(pendiente)` en `SEGUIMIENTO.md` §6 — ya son seis pasadas de auditoría consecutivas (2026-09-17 a 2026-09-22) esperando exclusivamente esa respuesta. Sigue `ABIERTO` por lo mismo.** **Reconfirmado en la pasada 2026-09-23: once commits desde la auditoría anterior (`f1d1728`) — un noveno ciclo consecutivo de PM (`3ed68e4`) y diez reconfirmaciones sucesivas del Programador, todos sin tocar `scripts/`, `tests/`, `assets/` ni ningún otro archivo fuera de `roadmap/` (`git diff --stat f1d1728..HEAD` limitado a `DECISIONES_TECNICAS.md`, `HISTORIAL_SESIONES.md`, `ROADMAP_PRODUCTO.md` y `SEGUIMIENTO.md`). El único contenido no repetitivo es la verificación propia del ciclo de PM del 2026-09-22 (`grep` del hilo `tomas_por_escena`/`EstadoProyecto.tomas` en los seis módulos que R-18 conecta, sin grieta nueva), reproducida de forma independiente en esta pasada con el mismo resultado. La pregunta #11 sigue `(pendiente)` en `SEGUIMIENTO.md` §6 — ya son siete pasadas de auditoría consecutivas (2026-09-17 a 2026-09-23) esperando exclusivamente esa respuesta. Sigue `ABIERTO` por lo mismo.** **Reconfirmado en la pasada 2026-09-24: once commits desde la auditoría anterior (`3a58f1c`) — un décimo ciclo consecutivo de PM (`5f7b071`) reconfirmando cola vacía sin código ni R-XX nueva, y diez reconfirmaciones sucesivas del Programador, todos limitados a `roadmap/` (`git diff --stat 3a58f1c..HEAD` sin tocar `scripts/`, `tests/`, `assets/` ni ningún otro archivo fuera de `roadmap/`). La pregunta #11 sigue `(pendiente)` en `SEGUIMIENTO.md` §6 — ya son ocho pasadas de auditoría consecutivas (2026-09-17 a 2026-09-24) esperando exclusivamente esa respuesta. Sigue `ABIERTO` por lo mismo.** | `roadmap/ROADMAP_PRODUCTO.md` · patrón ya señalado como "a vigilar" en la auditoría 2026-09-15, confirmado recurrente el 2026-09-16, enrutado a `SEGUIMIENTO.md` §6 #11 el mismo día |
| #20 | 2026-09-05 | Infraestructura / proceso (fuera del código) | media | **RESUELTO** | Diagnóstico original: seis rutinas programadas en vez de tres, en dos tríos con cron idéntico o solapado (`Auditor`/`auditor-teleprompter`, `Product manager`/`product-manager-teleprompter`, `Programador`/`programador-teleprompter`), asumido como coste doble de cómputo sobre la cuenta del dueño. **Corregido el 2026-09-10 por el programador** (sexto ciclo, `DECISIONES_TECNICAS.md`): el trío sin sufijo apunta a otro repositorio del dueño (`centro-estudios-sw`/GestorAcademia), no a este proyecto. **Cerrado en esta pasada con verificación independiente propia, no por transcribir la corrección ajena:** llamada directa a `list_triggers` en esta sesión (2026-09-11) leyendo `session_request.config.sources[].git_repository.url` de las seis rutinas — el campo completo, no solo `name`/`cron_expression` como comprobaban las ~15 reconfirmaciones previas a la corrección: `auditor-teleprompter`/`product-manager-teleprompter`/`programador-teleprompter` → `https://github.com/JanoSolerDiaz/telePrompter` (este repositorio); `Auditor`/`Product manager`/`Programador` (sin sufijo) → `https://github.com/JanoSolerDiaz/centro-estudios-sw` (otro proyecto del dueño). Confirmado: ninguna rutina de *este* proyecto está duplicada, una sola por rol, sin solape de cron. | `SEGUIMIENTO.md` §3 bloqueo #8 · verificado de forma independiente por esta auditoría (2026-09-11) leyendo `git_repository.url` de `list_triggers` |
| #14 | 2026-09-03 | Invariantes / revalidación | **alta** | **RESUELTO** | **Reproducido de forma independiente en esta auditoría** (no solo verificado a mano, como constaba en `DECISIONES_TECNICAS.md` al cerrar P-02): el límite que P-02 dejó explícitamente sin cerrar es más grave de lo que su propia nota describe. Escenario: en una revalidación coinciden una edición manual y la aceptación de una partición sobre el mismo bloque de origen (conflicto correctamente pospuesto por P-02/#9); en la revalidación INMEDIATAMENTE POSTERIOR, sin que el dueño toque nada más, el emparejamiento ancla→identidad no solo atribuye mal el contenido: **duplica el bloque siguiente de la misma escena.** Con un guion de prueba de dos bloques en la escena 1 (edición manual + partición aceptada sobre el bloque 0, bloque 1 intacto), la segunda revalidación produce 3 bloques en la escena donde debería haber 2, con el texto del bloque 1 repetido dos veces (una de ellas bajo la identidad equivocada, la mitad `'b'` de la partición del bloque 0) y la partición aceptada por el dueño sin materializarse nunca en dos mitades reales. Es contenido duplicado y mal atribuido en `guion-escenas.md`, generado en silencio, sin incidencia que lo señale ni test que lo cubra — exactamente el tipo de fallo que el invariante (c) existe para prevenir. Reproducción paso a paso en la narrativa de esta pasada, más abajo. **Cerrado por P-03** (2026-09-03): `revalidacion.py` ahora persiste entre pasadas qué particiones quedaron pospuestas (`estado.validacion["particiones_pospuestas"]`), así que la pasada siguiente interpreta las anclas del documento con el MISMO esquema de identidad con el que se escribió, en vez de asumir que toda partición aceptada ya está materializada. Efecto: mientras la edición manual siga en el documento, la partición se queda pospuesta sin duplicar ni mal atribuir nada; solo se materializa cuando el dueño deja de tocar el bloque. Dos tests de regresión nuevos en `tests/test_revalidacion.py` reproducen exactamente el escenario de este hallazgo (falla sin el fix) y confirman que la materialización posterior sigue funcionando cuando el conflicto se resuelve. | `revalidacion.py` · invariante (c) · límite conocido de P-02 |
| #21 | 2026-09-09 | Infraestructura / trazabilidad (git) | **alta** | **RESUELTO** | Diagnóstico original (2026-09-09): el historial de `origin/develop` parecía reescrito, colapsando T-00→P-05 en un commit raíz distinto en cada pasada, con commits "citados como vigentes" que `git merge-base --is-ancestor` daba por no-antepasados. **Era un falso positivo del clon superficial (`git clone --depth`) de cada contenedor efímero, no una reescritura real.** El programador ya lo investigó y corrigió el mismo día (`DECISIONES_TECNICAS.md`, primer ciclo 2026-09-09) con `git fetch --unshallow`; **esta auditoría lo reproduce de forma independiente en esta pasada (2026-09-10), no se limita a leer la corrección:** este clon también llegó superficial (`git rev-parse --is-shallow-repository` → `true`); `git fetch --unshallow origin` (operación de solo lectura) trajo el historial completo — **114 commits**, raíz real `f78a92c` ("initial commit") → `e8b9663` (T-00) → …; `git merge-base --is-ancestor 1a40c84 develop` **y** `... 576f6d9 develop` devuelven ambos **"IS ancestor"** tras el `unshallow`, confirmando que ninguno de los dos commits que auditorías previas creyeron "perdidos" lo estaba de verdad. Se corrige aquí a `RESUELTO` (no solo en `DECISIONES_TECNICAS.md`, que el auditor no puede dar por bueno sin repetir la comprobación): el contenido y la trazabilidad commit-a-commit del proyecto están intactos; la causa raíz observable (clon superficial con frontera variable) no es una acción de código y no requiere P-XX. | `origen: corrección del programador 2026-09-09` · reproducido de forma independiente por esta auditoría (2026-09-10) con `git fetch --unshallow` + `git merge-base --is-ancestor` |
| #22 | 2026-09-12 | Infraestructura / entorno de verificación | media | **RESUELTO** | Este contenedor trae, además del `mypy`/`ruff`/`pytest` que instala `pip install -r requirements-dev.txt` (versiones exactas pineadas: `mypy==1.18.2`, `ruff==0.14.0`, `pytest==8.4.2`, resueltos en `/usr/local/lib/python3.11/dist-packages`, el mismo Python que usa el proyecto), un **segundo juego de los mismos tres binarios preinstalado en `/root/.local/bin`** (`mypy 1.19.1`, `ruff 0.15.8`, `pytest 9.0.2`), con `/root/.local/bin` por delante en el `PATH`. Las cuatro verificaciones del protocolo son inmunes porque `scripts/ci.py` invoca siempre `sys.executable -m <herramienta>` (nunca el nombre pelado) y el hook de pre-commit llama a `python scripts/ci.py` — confirmado leyendo el código, no solo probando. El riesgo es para un humano o una sesión que teclee el comando pelado (`ruff check .`, `mypy scripts tests`, `pytest`) directamente en la terminal, tal como queda escrito literalmente en varias entradas de `HISTORIAL_SESIONES.md`: verificado en esta pasada que el binario pelado da una señal **distinta y engañosa** de la que da la versión pineada — `ruff check .` pelado marca `UP042` en `scripts/salidas.py:48` (`class TipoSalida(str, Enum)`, sugiere heredar de `enum.StrEnum`) que `python -m ruff check .`/`scripts/ci.py` NO marca; `mypy scripts tests` pelado no es solo más estricto, está **roto de verdad para este proyecto**: al vivir en un entorno de Python aislado que no ve `dist-packages`, no encuentra el paquete `pytest` y devuelve **34 errores falsos en 22 archivos** (`import-not-found` de `pytest`, más los `Untyped decorator` en cascada que provoca cada decorador de pytest sin tipos resueltos) donde `python -m mypy scripts/ tests/` (el que de verdad ejecuta el hook) da limpio. Es exactamente el tipo de señal que podría hacer perder tiempo a una sesión futura investigando "34 errores de tipos" que no existen en la verificación real del proyecto. No es un hallazgo de código: ninguna verificación real del protocolo lo sufre, y el origen (qué preinstala este contenedor de nube y en qué orden de `PATH`) no es una decisión de este repositorio. Se registra para que una futura pasada no lo redescubra desde cero y para valorar si conviene una nota explícita en `DEVELOPERS.md`/`SKILL.md` ("verificar siempre con `python scripts/ci.py`, nunca con el binario pelado en un contenedor de nube") que corte de raíz la confusión. **Cerrado por R-15** (2026-09-14, commit `3af47cb`), reverificado de forma independiente en esta pasada (2026-09-15): `grep -in pelado DEVELOPERS.md SKILL.md` localiza la advertencia en ambos sitios exactamente como pedía la ficha — bloque de cita en `DEVELOPERS.md` bajo "Verificación manual" ("Nunca el binario 'pelado' (`ruff`, `mypy`, `pytest` sin `python -m` por delante)") y frase con remisión en `SKILL.md`; tarea puramente documental, sin ninguna línea tocada en `scripts/ci.py` ni en ningún otro módulo (confirmado con `git show --stat 3af47cb`). | Entorno de contenedor de nube · verificado en esta pasada (2026-09-12) comparando `which`/`--version` de `ruff`/`mypy`/`pytest` pelados contra `python3 -m <herramienta> --version` y ejecutando ambos sobre el mismo código → **R-15** · cierre verificado de forma independiente por esta auditoría (2026-09-15) |
| #23 | 2026-09-15 | Proceso auditor / precisión del propio registro | baja | **RESUELTO** | Al reverificar la protección `.bak` del invariante (d) de forma directa (no repitiendo la lista de auditorías anteriores), `grep -rln "copia_seguridad\s*=" scripts/*.py` solo encuentra **cuatro** sitios reales: `documento_revision.py`, `entrada.py`, `feedback.py`, `instalar_skill.py`. Las narrativas del 2026-09-13 y 2026-09-14 (y probablemente alguna anterior) venían repitiendo "cinco puntos... (`convencion.py`, `documento_revision.py`, `entrada.py`, `feedback.py`, `instalar_skill.py`)". `convencion.py` no aplica ni ha aplicado nunca la copia `.bak`: su única función de escritura, `guardar_convencion_guiones`, lo documenta explícitamente en su propio docstring como excepción deliberada y correcta — `convencion-guiones.md` es un documento generado "para pegar en su plantilla", no un archivo del dueño que se vuelva a leer como entrada (a diferencia de `guion-escenas.md`), así que el invariante (d) no le aplica. No es un defecto de código ni una regresión de seguridad: el invariante (d) sigue cubierto al 100 % en los cuatro sitios reales que sí escriben archivos del dueño o de instalación. Es una inexactitud que se coló en el propio relato del auditor y se repitió sin recontar en al menos dos pasadas sucesivas — exactamente el tipo de "hallazgo sobre el propio proceso" que esta auditoría existe para atrapar. **Cerrado en esta misma pasada:** la cifra y la lista quedan corregidas aquí; no requiere ninguna acción de PM ni de programador porque el código nunca estuvo mal — solo la prosa de auditorías anteriores. | Precisión interna de `auditoriacontinua.md` · verificado en esta pasada (2026-09-15) con `grep -rln "copia_seguridad\s*=" scripts/*.py` |

---

## NARRATIVA POR AUDITORÍA

> Cada pasada: fecha, hallazgos y conclusiones. Append, la más reciente arriba. Prestar
> atención especial a la coherencia entre lo decidido (`DECISIONES_TECNICAS.md` y §0.2 de la
> hoja de ruta) y lo realmente implementado, y a las desviaciones (§7 de SEGUIMIENTO).

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
