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
| #15 | 2026-09-04 | Robustez / multiplataforma | media | ABIERTO | `entrada.leer_guion` decodifica el guion con `read_bytes()` + `decode("utf-8-sig")`, sin normalizar `\r\n`/`\r` a `\n` — a diferencia de otras rutas de lectura del propio proyecto (p. ej. `Path.read_text()` en `verificar_salidas.py`), que sí aplican la traducción universal de saltos de línea de Python. Un guion escrito y guardado en Windows (el sistema real del dueño) llega con `\r` incrustado a todo el pipeline de parseo/troceo/revalidación. Verificado en el código actual: el `\r` no se elimina en ningún punto de `entrada.py`. Riesgo real: dos textos idénticos salvo el fin de línea podrían no reconocerse como iguales exactamente donde el invariante (c) depende de esa comparación. Detectado por el propio equipo en sesión local sobre Windows (no por este auditor) y ya registrado como `R-10` con requisito 1 explícito y test propuesto; sin código de corrección todavía tras varias sesiones intermedias (R-01 a R-09) que no tocaron `entrada.py`. | `entrada.leer_guion` · R-10 (PENDIENTE) |
| #16 | 2026-09-04 | Robustez / datos (rodaje real) | media | ABIERTO | `tomas.duracion_toma_buena` no valida que como mucho una toma esté marcada `buena` por escena — esa exclusividad solo la garantiza el lado JS (`finalizarTomaActual` desmarca las demás antes de añadir la nueva). Si el `.json` exportado llega con dos tomas `buena: true` para la misma escena (edición manual del archivo, fusión de dos exportaciones, un futuro bug de `guion.js`), la función Python elige la primera en silencio, sin ninguna señal de ambigüedad. Reproducido en esta auditoría: `tomas=[{numero:1, duracion:10.0, buena:True}, {numero:2, duracion:999.0, buena:True}]` → `duracion_toma_buena(...) == 10.0` sin aviso. Es el punto único de fallo del que dependen a la vez R-04 (calibración de ppm), R-05 (`.srt` alineado) y R-07 (capítulos de YouTube): un dato de "toma buena" corrupto o ambiguo se propagaría en silencio a las tres salidas. Sin test que cubra este caso en `tests/test_tomas.py`. | `scripts/tomas.py` · R-02, hereda en R-04/R-05/R-07 |
| #17 | 2026-09-04 | Cobertura / salida derivada | baja | ABIERTO | `capitulos_youtube.calcular_capitulos` empareja títulos de la sección «Capítulos» con escenas posicionalmente "hasta la más corta" (decisión documentada en el propio docstring). Cuando hay **más títulos de capítulo que escenas**, los títulos sobrantes se descartan de `capitulos-youtube.txt` sin ningún aviso ni `motivo_sin_generar` — a diferencia del caso simétrico (menos títulos que escenas), que sí está cubierto por un test. Reproducido: guion con 1 escena y una tabla de 3 capítulos → el archivo derivado solo trae el primero, los otros dos desaparecen sin rastro (el texto original de la sección auxiliar del guion sigue íntegro, así que no es pérdida de la fuente, solo de la salida derivada que se pega en la descripción de YouTube). | `scripts/capitulos_youtube.py` · R-07 |
| #18 | 2026-09-04 | Calidad / cobertura de tests | baja | ABIERTO | No existe ningún test de integración cruzada entre `guion-alineado.srt` (R-05) y `capitulos-youtube.txt` (R-07) que confirme que, alimentados con el mismo `ResultadoTiempos`+`tomas_por_escena`, producen marcas de tiempo mutuamente coherentes — ambos comparten la misma función `tomas.duracion_toma_buena`, así que la coherencia es "por construcción" hoy, no verificada por regresión. Es exactamente el tipo de brecha que `tests/test_integracion_montaje.py` (T-33) se creó para cerrar entre `.srt` y `tarjetas.json`, sin extenderse todavía a estas dos salidas más recientes. No es un bug hoy: es riesgo de deriva silenciosa si una de las dos cambia de fórmula por separado en el futuro. | `tests/test_integracion_montaje.py` · R-05, R-07 |
| #19 | 2026-09-04 | Invariantes / revalidación (residual de #14) | baja | ABIERTO | El endurecimiento de P-04 (`_incidencias_anclas_desajustadas`) compara, por escena, solo el **conjunto/cantidad** de índices de ancla esperados contra los reales — no su contenido ni orden. Si dos conflictos coincidieran en número exacto de anclas pero en una disposición distinta, el aviso de incidencia no se dispararía. No se ha encontrado un escenario real del código actual que lo produzca (las claves de identidad `(escena, índice_original, mitad)` son deterministas dado el mismo guion + estado), por lo que es una asimetría teórica entre "detecta desajuste de cantidad" y "detecta desajuste de contenido", no un fallo reproducido. Se dejó constancia para que no se pierda de cara a una futura revisión de `revalidacion.py`. Reevaluado en esta pasada (2026-09-05): sin cambios en `revalidacion.py` desde la última auditoría, sigue exactamente en el mismo estado teórico. | `scripts/revalidacion.py` · límite residual de P-04 |
| #20 | 2026-09-05 | Infraestructura / proceso (fuera del código) | media | ASUMIDO | Confirmado de forma independiente en esta pasada (no solo leído en `SEGUIMIENTO.md` §3 bloqueo #8): el proyecto tiene seis rutinas programadas en vez de tres, en dos tríos con cron idéntico o solapado (`Auditor`/`auditor-teleprompter`, `Product manager`/`product-manager-teleprompter`, `Programador`/`programador-teleprompter`), el trío sin sufijo creado 2026-08-25, antes del primer commit (2026-08-31). Efecto observado en esta misma sesión: el clon de `develop` llegó DETACHED y con 4 commits sin ancestro común con `origin/develop` (52 de diferencia), exactamente el síntoma que trece sesiones consecutivas llevan documentando sin explicación de fondo hasta que el PM lo conectó con esta causa el 2026-09-04. No es una decisión que un auditor de código deba tomar (afecta a la cuenta del dueño, no al repositorio) ni ejecutable desde esta sesión: se registra como riesgo asumido y ya notificado, no como hallazgo nuevo — el PM ya lo documentó con el detalle completo (IDs, cron, fechas) y ya lo notificó al dueño por separado. Se deja constancia aquí únicamente para que la auditoría, como supervisor externo, conste de que verificó el bloqueo por su cuenta y coincide en el diagnóstico, y para vigilar que no quede olvidado si sigue sin resolverse varias pasadas más. | `SEGUIMIENTO.md` §3 bloqueo #8 · acción del dueño, no de código |
| #14 | 2026-09-03 | Invariantes / revalidación | **alta** | **RESUELTO** | **Reproducido de forma independiente en esta auditoría** (no solo verificado a mano, como constaba en `DECISIONES_TECNICAS.md` al cerrar P-02): el límite que P-02 dejó explícitamente sin cerrar es más grave de lo que su propia nota describe. Escenario: en una revalidación coinciden una edición manual y la aceptación de una partición sobre el mismo bloque de origen (conflicto correctamente pospuesto por P-02/#9); en la revalidación INMEDIATAMENTE POSTERIOR, sin que el dueño toque nada más, el emparejamiento ancla→identidad no solo atribuye mal el contenido: **duplica el bloque siguiente de la misma escena.** Con un guion de prueba de dos bloques en la escena 1 (edición manual + partición aceptada sobre el bloque 0, bloque 1 intacto), la segunda revalidación produce 3 bloques en la escena donde debería haber 2, con el texto del bloque 1 repetido dos veces (una de ellas bajo la identidad equivocada, la mitad `'b'` de la partición del bloque 0) y la partición aceptada por el dueño sin materializarse nunca en dos mitades reales. Es contenido duplicado y mal atribuido en `guion-escenas.md`, generado en silencio, sin incidencia que lo señale ni test que lo cubra — exactamente el tipo de fallo que el invariante (c) existe para prevenir. Reproducción paso a paso en la narrativa de esta pasada, más abajo. **Cerrado por P-03** (2026-09-03): `revalidacion.py` ahora persiste entre pasadas qué particiones quedaron pospuestas (`estado.validacion["particiones_pospuestas"]`), así que la pasada siguiente interpreta las anclas del documento con el MISMO esquema de identidad con el que se escribió, en vez de asumir que toda partición aceptada ya está materializada. Efecto: mientras la edición manual siga en el documento, la partición se queda pospuesta sin duplicar ni mal atribuir nada; solo se materializa cuando el dueño deja de tocar el bloque. Dos tests de regresión nuevos en `tests/test_revalidacion.py` reproducen exactamente el escenario de este hallazgo (falla sin el fix) y confirman que la materialización posterior sigue funcionando cuando el conflicto se resuelve. | `revalidacion.py` · invariante (c) · límite conocido de P-02 |

---

## NARRATIVA POR AUDITORÍA

> Cada pasada: fecha, hallazgos y conclusiones. Append, la más reciente arriba. Prestar
> atención especial a la coherencia entre lo decidido (`DECISIONES_TECNICAS.md` y §0.2 de la
> hoja de ruta) y lo realmente implementado, y a las desviaciones (§7 de SEGUIMIENTO).

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
