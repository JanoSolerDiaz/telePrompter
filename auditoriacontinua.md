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
| #5 | 2026-08-31 | Producto | media | ABIERTO | T-26 asume que `localStorage` persiste al abrir el reproductor desde `file://`. No está verificado en el navegador de grabación; el `try/catch` evita el error pero no salva la promesa de «retomar entre sesiones». | T-26 |
| #6 | 2026-08-31 | Coherencia | baja | ABIERTO | Nomenclatura arrastrada del nombre anterior: la carpeta de salida es `<nombre-guion>-tarjetas/` con el proyecto ya llamado `teleprompter`. Además `assets/` mezcla dos cosas distintas (logotipos de marca y, en el futuro, plantillas del reproductor). | T-07, T-18, T-28 |
| #7 | 2026-08-31 | Trazabilidad | baja | **RESUELTO** | Los tres logs estaban vacíos con el proyecto ya commiteado. **Cerrado:** la sesión de T-00 dejó 7 decisiones en `DECISIONES_TECNICAS.md`, su entrada en `HISTORIAL_SESIONES.md` y tres desviaciones en §7 (dos ya cerradas al resolverse §6.7). El cambio a v1.2 sí está registrado en los tres sitios. | §0.4 |
| #8 | 2026-08-31 | Documentación | baja | **RESUELTO** | `DEVELOPERS.md` se referencia en §0.4 y en T-32 pero todavía no existía. **Cerrado por acumulación:** existe ya con 934 líneas y una sección por cada tarea completada (T-00 a T-21), mantenida sesión a sesión como parte del cierre de cada una — cumple de sobra lo que T-32 le exige, con antelación sobre esa tarea. | T-32 |
| #9 | 2026-09-02 | Invariantes / revalidación | **alta** | **RESUELTO** | Si en una misma revalidación coincidían una edición manual del dueño y la aceptación de una partición de respiración sobre ese mismo bloque, la identidad usada para localizar la edición no se traducía a las identidades resultantes de la partición y la edición se perdía en silencio. **Cerrado por P-02** (2026-09-02): `revalidacion.py` pospone la partición ese mismo pase cuando hay conflicto y deja una incidencia explícita; test de regresión (`test_edicion_manual_y_particion_aceptada_misma_pasada_no_pierde_edicion`) reproduce exactamente este escenario. Verificado de nuevo en esta pasada (2026-09-03): sigue en verde. El propio cierre documentó un límite distinto, no cubierto por esta corrección → **#14**. | `revalidacion.py` · invariante (c) |
| #10 | 2026-09-02 | Configuración / calidad | baja | ABIERTO | Dos colores de estado del índice del reproductor (`.escena-estado--grabada` `#4ade80`, `.escena-estado--revisada` `#60a5fa`, de T-19) están escritos a mano en `estilo.css` en vez de vivir en `Configuracion` — la misma deuda de «sin números mágicos» que T-21 cerró para el color de acento del reproductor sin tocar estos dos. | T-19, T-21 · §0.2 |
| #11 | 2026-09-02 | Documentación / coherencia | baja | ABIERTO | `PROYECTO.md` (documento estable, «cambia poco») sigue describiendo en su glosario el ritmo como «por defecto 120, propio de locución didáctica y pausada» — la decisión anterior a T-12, ya sustituida en §0.2: el ritmo base es el deducido del propio guión, con 120 ppm solo de respaldo. | PROYECTO.md · T-12 |
| #12 | 2026-09-02 | Infraestructura | baja | ABIERTO | `pyproject.toml` exige Python ≥3.12 (`requires-python`, `target-version = "py312"`), pero el intérprete real de las sesiones de nube es 3.11.15. Ya mitigado evitando deliberadamente sintaxis exclusiva de 3.12 (decisión de T-06), pero el desajuste de fondo sigue sin corregirse ni vigilarse fuera de una nota suelta en `DECISIONES_TECNICAS.md`. | pyproject.toml · DECISIONES_TECNICAS (T-06) |
| #13 | 2026-09-02 | Robustez del validador | baja | ABIERTO | El validador de auto-contención (`verificar_salidas.py`) cubre `http(s)://`, `//cdn`, `<link>` remoto, `@import`, `fetch`/`XMLHttpRequest` y `src=` externo, pero no contempla `<object>`/`<embed src>`/`<base href>`/`WebSocket`/`EventSource`/`sendBeacon` ni `url(...)` de CSS fuera de `@import`. Hoy ninguna plantilla los usa; la regla dura solo se sostiene mientras nadie los introduzca sin ampliar el validador. Ya recogido en `R-09` (PENDIENTE), sin cambios en esta pasada. | `verificar_salidas.py` · regla «salida autocontenida» · R-09 |
| #14 | 2026-09-03 | Invariantes / revalidación | **alta** | ABIERTO | **Reproducido de forma independiente en esta auditoría** (no solo verificado a mano, como constaba en `DECISIONES_TECNICAS.md` al cerrar P-02): el límite que P-02 dejó explícitamente sin cerrar es más grave de lo que su propia nota describe. Escenario: en una revalidación coinciden una edición manual y la aceptación de una partición sobre el mismo bloque de origen (conflicto correctamente pospuesto por P-02/#9); en la revalidación INMEDIATAMENTE POSTERIOR, sin que el dueño toque nada más, el emparejamiento ancla→identidad no solo atribuye mal el contenido: **duplica el bloque siguiente de la misma escena.** Con un guion de prueba de dos bloques en la escena 1 (edición manual + partición aceptada sobre el bloque 0, bloque 1 intacto), la segunda revalidación produce 3 bloques en la escena donde debería haber 2, con el texto del bloque 1 repetido dos veces (una de ellas bajo la identidad equivocada, la mitad `'b'` de la partición del bloque 0) y la partición aceptada por el dueño sin materializarse nunca en dos mitades reales. Es contenido duplicado y mal atribuido en `guion-escenas.md`, generado en silencio, sin incidencia que lo señale ni test que lo cubra — exactamente el tipo de fallo que el invariante (c) existe para prevenir. Reproducción paso a paso en la narrativa de esta pasada, más abajo. | `revalidacion.py` · invariante (c) · límite conocido de P-02 |

---

## NARRATIVA POR AUDITORÍA

> Cada pasada: fecha, hallazgos y conclusiones. Append, la más reciente arriba. Prestar
> atención especial a la coherencia entre lo decidido (`DECISIONES_TECNICAS.md` y §0.2 de la
> hoja de ruta) y lo realmente implementado, y a las desviaciones (§7 de SEGUIMIENTO).

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
