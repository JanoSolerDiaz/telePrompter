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

### Sesión 2026-09-02 — T-25 (modo espejo), sesión de nube
**Tarea(s):** T-25
**Estado resultante:** T-25 **COMPLETADA**
**Commits a develop:** `T-25: modo espejo` (ver `git log` de esta fecha en `develop`)
**Migraciones ejecutadas:** ninguna
**Archivos creados/modificados:** `scripts/config.py` (nueva acción `espejo` en `MAPA_TECLAS_REPRODUCTOR`, `ESPEJO_INCLUYE_INDICADORES`/`Configuracion.espejo_incluye_indicadores`), `scripts/reproductor.py` (`espejo_incluye_indicadores` al JSON incrustado), `assets/reproductor/guion.js` (persistencia local mínima — `claveAlmacenamiento`/`leerPreferencia`/`guardarPreferencia` — y el propio modo espejo — `aplicarClaseEspejo`/`actualizarBotonEspejo`/`alternarEspejo`, botón `#btn-espejo` agrupado en `.reproductor-controles`, `case "espejo"` en `manejarTeclaReproductor`), `assets/reproductor/estilo.css` (`.reproductor-controles`, `.btn-espejo[aria-pressed="true"]`, `#vista-reproductor.espejo-texto .escena`, `#vista-reproductor.espejo-completo`), `tests/test_reproductor.py` (5 tests nuevos), `tests/test_esqueleto.py` (1 test nuevo), `DEVELOPERS.md` (sección T-25), `roadmap/SEGUIMIENTO.md` (cabecera, §1 fila T-25), `roadmap/DECISIONES_TECNICAS.md` (2 filas nuevas), `roadmap/HISTORIAL_SESIONES.md` (esta entrada)
**Verificaciones pre-push:** tipos ✅ · lint ✅ · tests ✅ (316 passed, 1 skipped; antes 310+1) · build ✅ (`verificar_salidas.py --fixture`, 3 etapas NO APLICABLE justificadas + reproductor y auto-contención OK)
**Health check post-deploy:** No aplica — sesión de nube, sin instalación local de la skill (T-32 sigue pendiente y fuera del alcance de una sesión de nube)
**Decisiones tomadas:** 2 filas nuevas en `DECISIONES_TECNICAS.md` (2026-09-02, T-25): (1) el volteo horizontal es `transform: scaleX(-1)` sobre `.escena` por defecto, con una segunda clase (`espejo-completo`) configurable para voltear también los indicadores; (2) persistencia local mínima adelantada de T-26, limitada al ajuste de espejo (`claveAlmacenamiento`/`leerPreferencia`/`guardarPreferencia`, clave ya derivada del guion), porque el propio criterio de aceptación de T-25 exige que el ajuste persista tras recargar y nada bloquea implementarlo ya — a diferencia del estado de escena de T-19, que si se dejó deliberadamente en memoria por no exigirlo su propio criterio
**Hallazgos del auditor atendidos:** ninguno nuevo; sin hallazgos ABIERTOS de severidad alta al empezar (el #9 ya está corregido en código por P-02, pendiente solo de que el auditor lo reevalúe y lo cierre en su propio documento — no es trabajo de esta sesión)
**Hallazgos:** ninguno nuevo. El hallazgo #5 de `auditoriacontinua.md` (localStorage no verificado contra `file://`) pasa a aplicar también al ajuste de espejo, no solo a lo que traerá T-26 — mismo mecanismo, mismo límite conocido, sin ampliar su alcance
**Tareas autopropuestas (P-XX):** ninguna
**Próximo paso:** T-26 (persistencia local de preferencias), décima de FASE B4. Ya puede reutilizar directamente `claveAlmacenamiento`/`leerPreferencia`/`guardarPreferencia` de `guion.js` (T-25) para el resto de preferencias (tamaño de texto, velocidad por escena, última escena vista, indicadores) en vez de diseñar el mecanismo desde cero — solo falta decidir la clave de cada preferencia y leerla/guardarla en los puntos ya identificados (`ajustarTamanoTexto`, `ajustarVelocidad`, `volverAlIndice`/`reproducirEscena`, `alternarIndicadores`)

### Sesión 2026-09-02 — Decisiones del dueño sobre T-24 y T-29, sesión local (sin código)
**Tarea(s):** T-24, T-24b (nueva), T-29 — ninguna implementada; solo se fija su alcance
**Estado resultante:** T-24 **COMPLETADA** por la sesión de nube que corrió en paralelo (ver la entrada siguiente), con exactamente el alcance aquí decidido · T-24b BLOQUEADA · T-29 PENDIENTE, confirmada como NO bloqueada
**Commits a develop:** `affeb6f decisiones del dueno: T-24 se parte (T-24b bloqueada) y T-29 no se bloquea`, más el merge con `46e8d15` (T-24), que se cruzó en el remoto mientras se redactaba esta decisión
**Migraciones ejecutadas:** ninguna
**Archivos creados/modificados:** `roadmap/SEGUIMIENTO.md` (cabecera, bloque «PARA EL DUEÑO», §1 filas T-24/T-24b/T-29, §3 bloqueos 2 y 5, §6 preguntas 9 y 10, §7 dos desviaciones; de paso se recompone la tabla de §6 como un solo bloque contiguo, que venía partida por líneas en blanco y desordenaba las filas 7 y 8), `roadmap/HISTORIAL_SESIONES.md` (esta entrada)
**Verificaciones pre-push:** no aplica — no se ha tocado ni una línea de código ni de test
**Health check post-deploy:** no aplica
**Decisiones tomadas:** son decisiones **del dueño**, no del agente, así que van a §6 de `SEGUIMIENTO.md` (preguntas 9 y 10) y no a `DECISIONES_TECNICAS.md`. (1) **T-24 se parte:** el dueño no dispone de clicker Bluetooth; el mando se identifica como un teclado corriente, de modo que el mapa completo, el antirrebote y la ayuda `?` son implementables y testeables sin hardware y solo la calibración «qué botón manda qué tecla» lo exige. T-24 conserva los requisitos 1, 3, 4 y la mitad software del 2; la verificación física sale a **T-24b, BLOQUEADA hasta nuevo aviso**. Se evita bloquear en cascada T-25 y T-26 y parar toda FASE B4. (2) **T-29 no se bloquea** pese a seguir sin el paquete de `480-branded-pptx`: su propio requisito 4 y su criterio de aceptación ya exigen entregar `tarjetas.json` y el brief con la skill de marca ausente, dejando latente solo la generación real del `.pptx`. Se evita bloquear en cascada T-30, T-31, T-32 y T-33.
**Hallazgos del auditor atendidos:** ninguno
**Cruce con la sesión de nube de T-24:** esta decisión se tomó sin saber que una sesión de nube estaba implementando T-24 a la vez. **No hubo trabajo perdido ni contradicción:** esa sesión entregó justo el alcance decidido aquí (mapa de teclado, antirrebote, ayuda `?`) y dejó el mando físico en el bloqueo #5, sin intentar verificarlo. El merge conserva T-24 COMPLETADA y añade T-24b BLOQUEADA como tarea aparte.
**Hallazgos:** la nota «**Bloqueo humano**» del cuerpo de T-29 en `HOJA_DE_RUTA.md` se contradice en apariencia con el requisito 4 y el criterio de aceptación de esa misma tarea; podía inducir a una sesión futura a marcarla BLOQUEADA por error. Aclarado en §1, §3.2 y §7 de `SEGUIMIENTO.md` (la hoja de ruta es inmutable y no se toca).
**Tareas autopropuestas (P-XX):** ninguna
**Próximo paso:** **T-25 (modo espejo)**, octava de FASE B4 — T-24 ya está COMPLETADA. **No intentar T-24b** ni verificar ningún mando físico hasta que el dueño avise.

---

### Sesión 2026-09-02 — T-24 (atajos de teclado y clicker Bluetooth), sesión de nube
**Tarea(s):** T-24
**Estado resultante:** T-24 COMPLETADA. Bloqueo #5 de §3 sigue ABIERTO (falta la verificación del dueño con el clicker físico contra el mapa ya implementado).
**Commits a develop:** `T-24: atajos de teclado y clicker bluetooth` (ver `git log` de esta fecha en `develop`)
**Migraciones ejecutadas:** ninguna (T-24 no toca el esquema de `estado.json`)
**Archivos creados/modificados:** `scripts/config.py` (cablea `ANTIRREBOTE_CLICKER_MS`, ya reservada desde T-20 sin usar, a `Configuracion`; añade `ESPACIO_AVANZA_BLOQUE` y `MAPA_TECLAS_REPRODUCTOR` —tupla de pares `(accion, teclas)`, no `dict`, para conservar la inmutabilidad del dataclass congelado— con sus campos y validación en `__post_init__`: antirrebote no negativo, mapa no vacío, ninguna acción sin tecla), `scripts/reproductor.py` (`_construir_datos` añade las tres claves nuevas al JSON incrustado, convirtiendo la tupla de pares a `dict()` en el borde de serialización), `assets/reproductor/guion.js` (`manejarTeclaReproductor` reescrito: ya no compara literales de tecla, resuelve `evento.key` contra `teclaAAccion` —construida desde `datos.mapa_teclas`— y despacha sobre el nombre de la ACCIÓN; funciones nuevas `pulsacionPermitida` —antirrebote por acción—, `construirListaAyudaTeclado`, `alternarAyuda`, `etiquetaTecla`; nuevo caso `salir_pantalla_completa` que llama a `salirPantallaCompleta()` ya existente desde T-19; nuevo overlay de ayuda en `renderizarReproductor`), `assets/reproductor/estilo.css` (`.ayuda-teclado`, `.ayuda-teclado-panel`, `.ayuda-teclado-lista` y derivados), `tests/test_reproductor.py` (6 tests nuevos), `tests/test_esqueleto.py` (4 tests nuevos), `SKILL.md` (sección T-24), `DEVELOPERS.md` (sección T-24), `roadmap/SEGUIMIENTO.md` (§1, §3, cabecera, callout del dueño), `roadmap/DECISIONES_TECNICAS.md` (6 filas nuevas), `roadmap/HISTORIAL_SESIONES.md` (esta entrada)
**Verificaciones pre-push:** tipos ✅ (mypy estricto, 0 errores) · lint ✅ (ruff, 0 avisos) · tests ✅ (310 pasan + 1 skipped, antes 300 + 1) · salidas ✅ (`verificar_salidas.py --fixture`, código 0; 3 etapas siguen NO APLICABLE por su tarea correspondiente)
**Health check post-deploy:** no aplicable — sesión de nube, sin acceso a `~/.claude/skills/teleprompter/` (T-32); no se simula. En su lugar, criterio de aceptación literal de T-24 verificado con Playwright headless (paquete `playwright` de Python instalado solo para esta comprobación manual, Chromium ya preinstalado en el contenedor vía `/opt/pw-browsers`; ninguno de los dos es dependencia del proyecto) sobre `fixtures/salida/reproductor.html` (guion real de 7 escenas): la primera escena (4 bloques) se recorrió entera usando solo `Espacio` (pausa/reanuda), `PageDown` (llegó hasta el bloque 4 de 4) y `PageUp` (retrocedió uno) — exactamente el criterio de aceptación; con dos `PageUp` pegados sin esperar entre ellos, solo se retrocedió un bloque en vez de dos, confirmando el antirrebote (120 ms por defecto); `?` abrió un panel con las trece acciones del mapa por defecto, con texto legible ("Espacio", "Re Pág", "Av Pág", "Esc" comprobados literalmente) y una segunda pulsación lo cerró; `Escape` salió de pantalla completa (concedida en Chromium headless) sin ocultar el reproductor. Aparte, sobre un reproductor generado con `espacio_avanza_bloque=True`, `Espacio` avanzó el bloque activo en vez de pausar (indicador "estado-pausa" vacío tras la pulsación) — confirma la rama alternativa del requisito 1. Sin errores de consola en ningún paso.
**Decisiones tomadas:** 6 filas añadidas a `DECISIONES_TECNICAS.md`: (1) el mapa de teclas pasa de literales en el `switch` a una tupla de pares configurable, resuelta via `teclaAAccion`; (2) `Espacio` pausa/reanuda o avanza según `espacio_avanza_bloque`, decisión del dueño porque el navegador no distingue qué botón físico del clicker envió la tecla; (3) el antirrebote es por acción, no global, para no descartar por error dos teclas distintas pulsadas rápido; (4) `preventDefault()` se aplica antes del antirrebote, para evitar el scroll nativo incluso en una pulsación descartada; (5) `Esc` llama explícitamente a `salirPantallaCompleta()` para que el atajo quede documentado en el mapa y en la ayuda, aunque el navegador ya lo intercepte por su cuenta; (6) la ayuda `?` se construye leyendo `datos.mapa_teclas` en tiempo de ejecución, nunca una lista escrita a mano, para que nunca se desincronice del mapa real
**Hallazgos del auditor atendidos:** ninguno de severidad alta abierto en `auditoriacontinua.md` al empezar
**Hallazgos:** ninguno nuevo
**Tareas autopropuestas (P-XX):** ninguna
**Próximo paso:** T-25 (modo espejo), octava de FASE B4 — depende de T-24 (ya completada). El bloqueo #5 de §3 de SEGUIMIENTO sigue ABIERTO: cuando el dueño prueba el clicker físico, si alguna tecla no coincide con el mapa vigente (visible con `?` dentro del reproductor), basta con ajustar `Configuracion.mapa_teclas_reproductor` — no hace falta tocar `guion.js`.

---

### Sesión 2026-09-02 — T-23 (ayudas de grabación), sesión de nube
**Tarea(s):** T-23
**Estado resultante:** T-23 COMPLETADA
**Commits a develop:** `T-23: ayudas de grabacion` (ver `git log` de esta fecha en `develop`)
**Migraciones ejecutadas:** ninguna (T-23 no toca el esquema de `estado.json`)
**Archivos creados/modificados:** `scripts/config.py` (constante `CUENTA_ATRAS_ACTIVADA` y campos `cuenta_atras_segundos`/`cuenta_atras_activada` en `Configuracion`, con validación de entero positivo en `__post_init__`; `CUENTA_ATRAS_SEGUNDOS` ya existía sin uso desde antes de T-18 y queda wireada aquí por primera vez), `scripts/reproductor.py` (`_construir_datos` añade las dos claves nuevas al JSON incrustado), `assets/reproductor/guion.js` (funciones nuevas `iniciarCuentaAtras`/`detenerCuentaAtras`, `actualizarCronometro`/`iniciarCronometro`/`detenerCronometro`, `actualizarBarraProgreso`, `alternarIndicadores`; `reproducirEscena` envuelve `iniciarMotor` en la cuenta atrás; `iniciarMotor`/`detenerMotor` arrancan/paran cronómetro y barra; `togglePausa` congela/reanuda el cronómetro; `marcarBloqueActivo` actualiza la barra; tecla `H`/`h` en `manejarTeclaReproductor`; nuevos elementos en `renderizarReproductor`), `assets/reproductor/estilo.css` (`.cronometro-toma`, `.barra-progreso-contenedor`/`.barra-progreso-relleno`, `.cuenta-atras`, regla de ocultación `#vista-reproductor.indicadores-ocultos ...`), `tests/test_reproductor.py` (6 tests nuevos), `tests/test_esqueleto.py` (1 test nuevo), `DEVELOPERS.md` (sección T-23), `roadmap/SEGUIMIENTO.md` (§1, cabecera), `roadmap/DECISIONES_TECNICAS.md` (4 filas nuevas), `roadmap/HISTORIAL_SESIONES.md` (esta entrada)
**Verificaciones pre-push:** tipos ✅ (mypy estricto, 0 errores) · lint ✅ (ruff, 0 avisos) · tests ✅ (300 pasan + 1 skipped, antes 294 + 1) · salidas ✅ (`verificar_salidas.py --fixture`, código 0; 3 etapas siguen NO APLICABLE por su tarea correspondiente)
**Health check post-deploy:** no aplicable — sesión de nube, sin acceso a `~/.claude/skills/teleprompter/` (T-32); no se simula. En su lugar, criterio de aceptación literal de T-23 verificado con Playwright headless (paquete `playwright` de Python instalado solo para esta comprobación manual, Chromium ya preinstalado en el contenedor vía `/opt/pw-browsers`; ninguno de los dos es dependencia del proyecto) sobre `fixtures/salida/reproductor.html` (guion real de 7 escenas): al pulsar play aparece "3" en el overlay de cuenta atrás y el motor no arranca (`.bloque--activo` con recuento 0) hasta que termina 3 segundos después; con `cuenta_atras_activada=False` el motor arranca al instante sin overlay visible; el cronómetro mostró "0:02 / 0:16" tras 2 s reales y quedó congelado en dos lecturas idénticas separadas por 1.5 s de pausa; la barra de progreso pasó de 25% (bloque 1 de 4) a 100% exacto al llegar al último bloque avanzando con `ArrowRight`; `H` ocultó la cabecera y la barra, una segunda pulsación las devolvió — sin errores de consola en ningún paso.
**Decisiones tomadas:** 4 filas añadidas a `DECISIONES_TECNICAS.md`: (1) la cuenta atrás envuelve `iniciarMotor` (callback) en vez de vivir dentro de él; (2) el cronómetro recalcula siempre desde marcas de reloj absolutas (`Date.now()`) para que la deriva sea estructuralmente nula, no una acumulación por intervalo; (3) la barra de progreso se calcula por recuento de bloques, no por tiempo, para llegar al 100% exactamente con el último bloque tal como exige el criterio de aceptación; (4) los indicadores se ocultan con un único interruptor de clase CSS que sobrevive a un cambio de escena, en vez de alternar cada elemento por separado desde JS
**Hallazgos del auditor atendidos:** ninguno de severidad alta abierto en `auditoriacontinua.md` al empezar (el único, #9, ya lo cerró P-02 en la sesión anterior)
**Hallazgos:** ninguno nuevo
**Tareas autopropuestas (P-XX):** ninguna
**Próximo paso:** T-24 (atajos de teclado y compatibilidad con clicker Bluetooth), séptima de FASE B4 — depende de T-23 (ya completada). Nota para quien la retome: el bloqueo #5 de §3 de SEGUIMIENTO ("Probar los atajos con el clicker Bluetooth real") sigue ABIERTO — una sesión de nube puede implementar el mapa completo de teclas (`manejarTeclaReproductor` ya tiene la estructura `switch` lista para ampliar) y la ayuda `?`, pero la verificación con el clicker físico solo puede hacerla el dueño; documentar esa parte como pendiente en vez de simularla.

---

### Sesión 2026-09-02 — P-02 (hallazgo #9, urgente antes de T-23), sesión de nube
**Tarea(s):** P-02 (origen: auditoría #9, severidad alta)
**Estado resultante:** P-02 COMPLETADA. T-23 sigue PENDIENTE — esta sesión se dedicó íntegra al hallazgo urgente, según manda §0.1/§0.3 ("antes de elegir tarea, revisa el registro de hallazgos... si hay algún hallazgo ABIERTO de severidad alta, atiéndelo como P-XX urgente antes de la cola").
**Commits a develop:** `P-02: corrige perdida silenciosa de edicion manual al coincidir con particion aceptada (hallazgo #9)` (ver `git log` de esta fecha en `develop`)
**Migraciones ejecutadas:** ninguna (no toca el esquema de `estado.json`)
**Archivos creados/modificados:** `scripts/revalidacion.py` (`_materializar_marcados` gana el parámetro `indices_con_edicion_previa_a_particion` y no aplica la partición sobre esos índices; función nueva `_incidencias_conflicto_edicion_particion`; `revalidar_guion` calcula el conjunto de conflicto por escena a partir de `ediciones_manuales` y lo pasa a ambos), `tests/test_revalidacion.py` (test nuevo `test_edicion_manual_y_particion_aceptada_misma_pasada_no_pierde_edicion`), `roadmap/SEGUIMIENTO.md` (§1 cabecera, §5 fila P-02), `roadmap/DECISIONES_TECNICAS.md` (1 fila nueva), `roadmap/HISTORIAL_SESIONES.md` (esta entrada)
**Verificaciones pre-push:** tipos ✅ (mypy estricto, 0 errores) · lint ✅ (ruff, 0 avisos) · tests ✅ (294 pasan + 1 skipped, antes 293 + 1) · salidas ✅ (`verificar_salidas.py --fixture`, código 0; 3 etapas siguen NO APLICABLE por su tarea correspondiente)
**Health check post-deploy:** no aplicable — sesión de nube, sin acceso a `~/.claude/skills/teleprompter/` (T-32); no se simula.
**Decisiones tomadas:** 1 fila añadida a `DECISIONES_TECNICAS.md`: posponer la materialización de la partición (sin revertir su decisión de aceptación ni tocar el texto editado) y avisar con una incidencia explícita, descartando sobrescribir la edición (violaría el invariante), revertir la decisión del dueño en su nombre, o volver a trocear el texto editado automáticamente.
**Hallazgos del auditor atendidos:** #9 (severidad alta) — corregido y verificado con test de reproducción exacta del escenario descrito por el auditor.
**Hallazgos:** al verificar la corrección a mano se encontró un límite conocido, no cerrado por esta P-XX y registrado en `DECISIONES_TECNICAS.md`: en una revalidación POSTERIOR sin que el dueño vuelva a tocar el bloque, el emparejamiento ancla→identidad puede atribuir el texto editado íntegro a la mitad `'a'` de la partición y dejar en la mitad `'b'` un fragmento del texto de ORIGEN sin editar — no hay pérdida de texto, pero sí contenido incorrecto visible. Queda para que la próxima auditoría lo registre como hallazgo propio (candidato a #14) en vez de ampliar el alcance de esta corrección urgente.
**Tareas autopropuestas (P-XX):** P-02 registrada y ejecutada (ver §5 de SEGUIMIENTO).
**Próximo paso:** T-23 (ayudas de grabación), sexta de FASE B4 — no se tocó en esta sesión. Quien la retome puede seguir la nota de la sesión de T-22: `elementosBloque[bloqueActual]` y `escenaActual`/`bloqueActual` ya identifican el bloque activo, y `inicio_segundos`/`fin_segundos` ya están disponibles para el cronómetro/contador de progreso.

---

### Sesión 2026-09-02 — T-22 (autoscroll con bloque centrado), sesión de nube
**Tarea(s):** T-22
**Estado resultante:** T-22 COMPLETADA
**Commits a develop:** `T-22: autoscroll con bloque centrado` (ver `git log` de esta fecha en `develop`)
**Migraciones ejecutadas:** ninguna (T-22 no toca el esquema de `estado.json`)
**Archivos creados/modificados:** `scripts/config.py` (constante `DURACION_AUTOSCROLL_MS` y campo `duracion_autoscroll_ms` en `Configuracion`, con validación de entero positivo en `__post_init__`), `scripts/reproductor.py` (`_construir_datos` añade la clave `duracion_autoscroll_ms` al JSON incrustado), `assets/reproductor/guion.js` (funciones nuevas `centrarBloqueActivo`/`detenerAnimacionScroll`/`alturaViewport`/`scrollMaximo`/`suavizarProgreso`; llamadas añadidas en `avanzarAutomatico`, `irABloque`, `iniciarMotor` y `ajustarTamanoTexto`; listener nuevo de `resize`; corrección en `solicitarPantallaCompleta` — `focus({preventScroll: true})` en sus dos llamadas, arreglando un bug real de interacción con T-19 detectado en esta misma sesión), `tests/test_reproductor.py` (3 tests nuevos), `tests/test_esqueleto.py` (2 tests nuevos), `SKILL.md` (sección T-22), `DEVELOPERS.md` (sección T-22), `roadmap/SEGUIMIENTO.md` (§1, cabecera — con una nota de corrección sobre el alcance real de FASE B4), `roadmap/DECISIONES_TECNICAS.md` (4 filas nuevas), `roadmap/HISTORIAL_SESIONES.md` (esta entrada)
**Verificaciones pre-push:** tipos ✅ (mypy estricto, 0 errores) · lint ✅ (ruff, 0 avisos) · tests ✅ (293 pasan + 1 skipped, antes 288 + 1) · salidas ✅ (`verificar_salidas.py --fixture`, código 0, "Generación del reproductor" y "Auto-contención" en OK; 3 etapas siguen NO APLICABLE por su tarea correspondiente)
**Health check post-deploy:** no aplicable — sesión de nube, sin acceso a `~/.claude/skills/teleprompter/` (T-32); no se simula. En su lugar, criterio de aceptación literal de T-22 verificado con Playwright headless (Chromium ya preinstalado en el contenedor vía `/opt/pw-browsers/chromium`; el paquete Node `playwright` ya estaba disponible globalmente en el entorno — no se instaló ni se desinstaló nada para esta comprobación, ninguno de los dos es dependencia del proyecto) sobre el fixture real generado por la 4ª red (guion de 7 escenas, 4-21 bloques): con un viewport donde la escena más corta (4 bloques) cabe entera, `scrollY` permanece en `0` tras entrar en ella; en la escena de 21 bloques, el bloque activo permaneció dentro del tercio central de la pantalla en las 20 transiciones manuales por `ArrowRight`, tras dos aumentos y varias reducciones del tamaño de texto (`[`/`]`), tras cinco avances manuales seguidos sin esperar a que terminara la animación anterior (sin rebote: terminó exactamente centrado) y tras redimensionar la ventana de 500 a 700 px de alto — sin errores de consola en ningún paso
**Decisiones tomadas:** 4 filas añadidas a `DECISIONES_TECNICAS.md`: (1) interpolación propia con `requestAnimationFrame`, cancelable, en vez de `scrollIntoView({behavior:'smooth'})`, para que un avance rápido a mano no rebote; (2) el requisito "si cabe entero no se desplaza" no lleva rama explícita, sale del propio cálculo acotado; (3) `centrarBloqueActivo` recibe un booleano explícito de quien llama en vez de inferir cuándo animar; (4) el bug real de esta sesión — el foco diferido de `solicitarPantallaCompleta` (T-19) deshacía el centrado — corregido con `focus({preventScroll: true})`, sin tocar el recorrido de teclado de T-19
**Hallazgos del auditor atendidos:** ninguno de severidad alta abierto en `auditoriacontinua.md` (#5, #6, #8 siguen media/baja, sin acción de esta sesión)
**Hallazgos:** un bug real propio de esta sesión, encontrado y corregido antes del commit (ver arriba: foco diferido de T-19 deshaciendo el autoscroll de T-22 cuando el navegador concede pantalla completa); también se detectó y corrigió una imprecisión en la nota de la sesión anterior (T-21 llamaba a T-22 "quinta y última de FASE B4", pero la hoja de ruta extiende esa fase hasta T-26) — corregida en la cabecera de `SEGUIMIENTO.md` para que no se repita
**Tareas autopropuestas (P-XX):** ninguna
**Próximo paso:** T-23 (ayudas de grabación), sexta de FASE B4 — depende de T-20 (ya completada). Nota para quien la retome: `elementosBloque[bloqueActual]` y `escenaActual`/`bloqueActual` ya identifican el bloque activo con precisión; el cronómetro/contador de progreso de T-23 puede apoyarse en `bloques.length`/`bloqueActual` y en las marcas de tiempo ya presentes (`inicio_segundos`/`fin_segundos`) sin inventar un nuevo mecanismo de seguimiento.

---

### Sesión 2026-09-02 — T-21 (resaltado, tipografía y tema de grabación), sesión de nube
**Tarea(s):** T-21
**Estado resultante:** T-21 COMPLETADA
**Commits a develop:** `T-21: resaltado, tipografia y tema de grabacion` (ver `git log` de esta fecha en `develop`)
**Migraciones ejecutadas:** ninguna (T-21 no toca el esquema de `estado.json`)
**Archivos creados/modificados:** `scripts/config.py` (constantes y campos nuevos en `Configuracion`: `atenuacion_niveles`, `atenuacion_minima`, `paso_tamano_texto_px`, `tamano_texto_minimo_px`/`maximo_px`, `color_acento_reproductor`, `margen_seguro_px`, `tiempo_inactividad_cursor_ms`, con validación en `__post_init__`), `scripts/reproductor.py` (`_construir_datos` añade las siete claves nuevas al JSON incrustado; `generar_reproductor_html` sustituye `__COLOR_ACENTO__`/`__MARGEN_SEGURO_PX__`; función nueva `contraste_relativo`/`_luminancia_relativa`, fórmula WCAG), `assets/reproductor/guion.js` (`opacidadPorDistancia`/`marcarBloqueActivo` con atenuación por distancia, `ajustarTamanoTexto`/`actualizarIndicadorTamano` con teclas `[`/`]`, ocultación de cursor tras inactividad en pantalla completa), `assets/reproductor/estilo.css` (`--color-acento`, `--margen-seguro`, `.cursor-oculto`, `.tamano-texto`, transición de opacidad en `.bloque`), `tests/test_reproductor.py` (7 tests nuevos), `tests/test_esqueleto.py` (6 tests nuevos de validación de `Configuracion`), `SKILL.md` (sección T-21), `DEVELOPERS.md` (sección T-21), `roadmap/SEGUIMIENTO.md` (§1, cabecera), `roadmap/DECISIONES_TECNICAS.md` (5 filas nuevas), `roadmap/HISTORIAL_SESIONES.md` (esta entrada)
**Verificaciones pre-push:** tipos ✅ (mypy estricto, 0 errores) · lint ✅ (ruff, 0 avisos) · tests ✅ (288 pasan + 1 skipped, antes 281 + 1) · salidas ✅ (`verificar_salidas.py --fixture`, código 0, "Generación del reproductor" y "Auto-contención" en OK; 3 etapas siguen NO APLICABLE por su tarea correspondiente)
**Health check post-deploy:** no aplicable — sesión de nube, sin acceso a `~/.claude/skills/teleprompter/` (T-32); no se simula. En su lugar, criterio de aceptación literal de T-21 verificado con Playwright headless (paquete instalado solo para esta comprobación manual, desinstalado al terminar; Chromium ya preinstalado en el contenedor, ninguno de los dos es dependencia del proyecto) sobre el fixture real generado por la 4ª red: con el bloque activo en el índice 2, los bloques 0/1/3 mostraron opacidad computada 0.5/0.75/0.75 — exactamente los valores que predicen los niveles de atenuación por defecto (`0.75, 0.5, 0.35`) según su distancia real al activo; dos pulsaciones de `]` subieron el tamaño de texto de 48 a 56 px, reflejado tanto en `--tamano-base` como en el indicador visible; tras 3.3 s de inactividad del ratón en pantalla completa el contenedor ganó la clase `cursor-oculto`, y un movimiento posterior del ratón la quitó de inmediato — sin errores de consola en ningún paso
**Decisiones tomadas:** 5 filas añadidas a `DECISIONES_TECNICAS.md`: (1) atenuación de contexto calculada en JS como opacidad por distancia en vez de clases CSS fijas, porque el número de niveles es configurable; (2) contraste AAA verificado por una función y un test propios (fórmula WCAG), no solo a ojo; (3) tamaño de texto en vivo como preferencia global, no por escena, a diferencia de la velocidad de T-20; (4) cursor oculto solo con pantalla completa activa, comprobado en el momento de disparar el temporizador; (5) color de acento (`#f5c542`) centralizado en `Configuracion`, cerrando una excepción a "sin números mágicos" que arrastraban T-19/T-20
**Hallazgos del auditor atendidos:** ninguno de severidad alta abierto en `auditoriacontinua.md` (#5, #6, #8 siguen media/baja, sin acción de esta sesión)
**Hallazgos:** ninguno nuevo
**Tareas autopropuestas (P-XX):** ninguna
**Próximo paso:** T-22 (autoscroll con bloque centrado), quinta y última de FASE B4 — depende de T-21. Nota para quien la retome: `marcarBloqueActivo(indice)` en `guion.js` ya recorre `elementosBloque` en cada cambio de bloque para fijar la opacidad de contexto; T-22 puede reutilizar ese mismo recorrido (o el propio `indice`) para centrar el elemento activo con `scrollIntoView`/cálculo manual, sin duplicar el índice del bloque activo en una variable aparte.

---

### Sesión 2026-09-02 — T-20 (motor de avance híbrido), sesión de nube
**Tarea(s):** T-20
**Estado resultante:** T-20 COMPLETADA
**Commits a develop:** `T-20: motor de avance hibrido` (ver `git log` de esta fecha en `develop`)
**Migraciones ejecutadas:** ninguna (T-20 no toca el esquema de `estado.json`)
**Archivos creados/modificados:** `scripts/config.py` (`VELOCIDAD_MINIMA`/`VELOCIDAD_MAXIMA` nuevas, campos `paso_velocidad`/`velocidad_minima`/`velocidad_maxima` en `Configuracion` con validación), `scripts/reproductor.py` (`_construir_datos` recibe `configuracion` y añade los tres campos de velocidad al JSON incrustado), `assets/reproductor/guion.js` (motor de avance híbrido completo: temporizador encadenado por bloque, velocidad por escena, pausa/reanudación exacta, avance/escena manual, teclado del reproductor), `assets/reproductor/estilo.css` (indicadores de velocidad/pausa, `.bloque--activo`), `tests/test_reproductor.py` (6 tests nuevos), `tests/test_esqueleto.py` (3 tests nuevos de validación de `Configuracion`), `DEVELOPERS.md` (sección T-20), `roadmap/SEGUIMIENTO.md` (§1, cabecera), `roadmap/DECISIONES_TECNICAS.md` (4 filas nuevas), `roadmap/HISTORIAL_SESIONES.md` (esta entrada)
**Verificaciones pre-push:** tipos ✅ (mypy estricto, 0 errores) · lint ✅ (ruff, 0 avisos) · tests ✅ (281 pasan + 1 skipped, antes 272 + 1) · salidas ✅ (`verificar_salidas.py --fixture`, código 0, "Generación del reproductor" y "Auto-contención" en OK; 3 etapas siguen NO APLICABLE por su tarea correspondiente)
**Health check post-deploy:** no aplicable — sesión de nube, sin acceso a `~/.claude/skills/teleprompter/` (T-32); no se simula. En su lugar, criterio de aceptación literal de T-20 verificado con Playwright headless (paquete instalado solo para esta comprobación manual, Chromium ya preinstalado en el contenedor, ninguno de los dos es dependencia del proyecto) sobre el fixture real generado por la 4ª red (guion de 7 escenas/71 bloques): cadena de avances automáticos con tiempos reales medidos contra la duración real de cada bloque; avance manual (`ArrowRight`) que mueve el bloque activo sin detener el automático, que sigue encadenando después; `+`/`-` que cambian el indicador de velocidad y aceleran medible los avances por segundo siguientes sin alterar el bloque en curso; `Espacio` que pausa (congela el bloque activo durante varios segundos de espera) y reanuda exactamente donde estaba (mismo bloque, mismo resto de tiempo), incluso con varios ciclos de pausa/reanudación seguidos; `R` que reinicia la escena al primer bloque; `↑`/`↓` que cambian de escena sin volver a pedir pantalla completa y recuerdan la velocidad ajustada al volver a una escena ya visitada (mientras que una escena nueva arranca en 1.0×); vuelta al índice con la escena marcada "Grabada" — sin errores de consola en ningún paso
**Decisiones tomadas:** 4 filas añadidas a `DECISIONES_TECNICAS.md`: (1) temporizador encadenado por bloque en vez de un reloj global con offsets absolutos; (2) pausa como "milisegundos restantes desde la última marca" en vez de un instante absoluto de fin previsto; (3) límites/paso de velocidad viajan en el JSON incrustado, no como constantes escritas a mano en `guion.js`; (4) resaltado del bloque activo deliberadamente mínimo, dejando el tratamiento completo (atenuación, contraste AAA) para T-21
**Hallazgos del auditor atendidos:** ninguno de severidad alta abierto en `auditoriacontinua.md` (#5, #6, #8 siguen media/baja, sin acción de esta sesión)
**Hallazgos:** ninguno nuevo. Se verificó explícitamente con Playwright, antes de dar la tarea por buena, un caso que parecía un bug (una escena de calibración de solo 4 bloques se quedaba "congelada" en el último bloque tras pausar/reanudar) y resultó ser el comportamiento correcto: en el último bloque de una escena no hay nada más que encadenar, así que el motor se detiene ahí a propósito hasta que el dueño vuelva al índice o cambie de escena a mano
**Tareas autopropuestas (P-XX):** ninguna
**Próximo paso:** T-21 (resaltado, tipografía y tema de grabación) — depende de T-20. Nota para quien la retome: `.bloque--activo` en `estilo.css` ya marca el bloque en curso con un tratamiento mínimo (fondo y borde); T-21 debe sustituirlo por el resaltado real (contexto anterior/posterior atenuado con gradiente configurable, contraste AAA) sin romper las clases/ids que ya lee `guion.js` (`elementosBloque`, `marcarBloqueActivo`)

---

### Sesión 2026-09-02 — T-19 (índice de escenas y entrada a pantalla completa), sesión de nube
**Tarea(s):** T-19
**Estado resultante:** T-19 COMPLETADA
**Commits a develop:** `T-19: indice de escenas y entrada a pantalla completa` (ver `git log` de esta fecha en `develop`)
**Migraciones ejecutadas:** ninguna (T-19 no toca el esquema de `estado.json`)
**Archivos creados/modificados:** `assets/reproductor/guion.js` (reescrito: vista de índice y vista de reproductor alternadas dentro de `#app`, navegación por teclado, `requestFullscreen`/`exitFullscreen`, estado por escena en memoria), `assets/reproductor/estilo.css` (estilos nuevos: filas del índice, insignias de estado, foco visible, cabecera del reproductor y botón volver), `tests/test_reproductor.py` (5 tests nuevos, estáticos sobre el HTML/JS generado), `roadmap/SEGUIMIENTO.md` (§1, cabecera), `roadmap/DECISIONES_TECNICAS.md` (3 filas nuevas), `roadmap/HISTORIAL_SESIONES.md` (esta entrada)
**Verificaciones pre-push:** tipos ✅ (mypy estricto, 0 errores) · lint ✅ (ruff, 0 avisos) · tests ✅ (272 pasan + 1 skipped, antes 262 + 1) · salidas ✅ (`verificar_salidas.py --fixture`, código 0, "Generación del reproductor" y "Auto-contención" en OK; 3 etapas siguen NO APLICABLE por su tarea correspondiente)
**Health check post-deploy:** no aplicable — sesión de nube, sin acceso a `~/.claude/skills/teleprompter/` (T-32); no se simula. En su lugar, criterio de aceptación literal de T-19 verificado con Playwright headless (paquete instalado solo para esta comprobación manual, Chromium ya preinstalado en el contenedor, ninguno de los dos es dependencia del proyecto) sobre el fixture real generado por la 4ª red: recorrido completo solo con teclado — `Tab` a la primera fila, tres `ArrowDown` hasta la escena 4, `Enter` arranca en pantalla completa con contador "4/N", `Enter` sobre "Volver al índice" regresa sin recargar (misma URL) con el foco de vuelta en la fila 4 — sin usar el ratón y sin errores de consola
**Decisiones tomadas:** 3 filas añadidas a `DECISIONES_TECNICAS.md`: (1) estado por escena solo en memoria de la pestaña, no persistido (transitorio hasta R-02/T-26); (2) cada fila del índice es un único `<button>` que hace de fila navegable y de botón de play a la vez; (3) refocar el botón "Volver al índice" dentro del `.then()` de `requestFullscreen()`, porque Chromium vacía el foco al completar la transición a pantalla completa
**Hallazgos del auditor atendidos:** ninguno de severidad alta abierto en `auditoriacontinua.md` (#5, #6, #8 siguen media/baja, sin acción de esta sesión)
**Hallazgos:** uno propio, corregido en la misma sesión antes del push: el `.focus()` síncrono sobre "Volver al índice" se perdía al completar la transición a pantalla completa (Chromium resetea el foco de la página), lo que habría dejado el recorrido de teclado sin foco visible justo tras arrancar la escena. Detectado con la verificación manual de Playwright, no con la suite de `pytest` (el proyecto no ejecuta JS en sus tests, solo verifica el HTML/JS generado como texto)
**Tareas autopropuestas (P-XX):** ninguna
**Próximo paso:** T-20 (motor de avance híbrido) — depende de T-19. Nota para quien la retome: el estado por escena vive en `estadosEscena` dentro de `guion.js` (in-memory); T-20 no necesita tocarlo, pero T-26 sí deberá decidir cómo persistirlo (o sustituirlo) junto con la velocidad por escena

---

### Sesión 2026-09-01 — T-18 (esqueleto del reproductor autocontenido), sesión de nube
**Tarea(s):** T-18
**Estado resultante:** T-18 COMPLETADA
**Commits a develop:** `T-18: esqueleto del reproductor autocontenido` (ver `git log` de esta fecha en `develop`)
**Migraciones ejecutadas:** ninguna (T-18 no toca el esquema de `estado.json`)
**Archivos creados/modificados:** `scripts/reproductor.py` (nuevo: `generar_reproductor_html`, `guardar_reproductor`, `_construir_datos`, `_json_seguro_para_script`), `assets/reproductor/plantilla.html`, `assets/reproductor/estilo.css`, `assets/reproductor/guion.js` (nuevos: las tres plantillas del requisito 1), `scripts/config.py` (nuevos campos de `Configuracion`: `tamano_texto_base_px`, `color_fondo_reproductor`, `color_texto_reproductor`, `color_texto_secundario_reproductor`, `pila_tipografica_reproductor`, más las constantes de módulo correspondientes y `NOMBRE_ARCHIVO_REPRODUCTOR`), `scripts/verificar_salidas.py` (nueva etapa `generar_reproductor_fixture`, que activa "Generación del reproductor" y "Auto-contención del reproductor" generando de verdad sobre el primer guion de `fixtures/reales/`, a falta de `fixtures/guion-ejemplo.md` de T-32), `tests/test_reproductor.py` (nuevo, 10 tests: cobertura total de escenas/bloques y auto-contención sobre los tres guiones reales, escapado seguro contra un guion hostil con `</script>`/`<b>`/`&`/comillas, escapado del título, conservación de tildes, aplicación de la configuración de estilo, ningún marcador de plantilla sin sustituir, guardado en la carpeta de salida, escena sin locución), `pyproject.toml` (per-file-ignore `RUF001` para el nuevo test que usa el guion largo real), `DEVELOPERS.md` (sección T-18), `SKILL.md` (sección T-18 con la tabla de valores por defecto del reproductor), `roadmap/SEGUIMIENTO.md` (§1, cabecera), `roadmap/DECISIONES_TECNICAS.md`, `roadmap/HISTORIAL_SESIONES.md` (esta entrada)
**Verificaciones pre-push:** tipos ✅ · lint ✅ · tests ✅ (262 pasan + 1 skipped, antes 252 + 1) · build ✅ (`verificar_salidas.py --fixture`: "Generación del reproductor" y "Auto-contención del reproductor" pasan a OK generando sobre `guion-08-busqueda-investigacion.md`; "Guion de ejemplo" y "Generación de salidas" siguen NO APLICABLE, correctamente, hasta T-32 y T-30)
**Health check post-deploy:** N/A — sesión de nube, no instala en `~/.claude/skills/` (T-32 sigue BLOQUEADA por ese motivo). Verificación manual adicional (no automatizada, no es dependencia del proyecto): el `.html` generado se abrió con Chromium headless vía Playwright (instalado solo para esta comprobación) desde `file://`, sin mensajes de consola ni errores de página, y un guion hostil con `</script><script>alert(1)</script>` y `<img onerror=...>` se renderizó como texto literal sin diálogos — confirma el requisito 5 y el escapado seguro del requisito 3.
**Decisiones tomadas:** 5 filas nuevas en `DECISIONES_TECNICAS.md` (2026-09-01, T-18): datos del guion viajan como JSON en un `<script type="application/json">` leído con `JSON.parse` y volcado con `textContent` (nunca `innerHTML` ni interpolación directa en el marcado); `_json_seguro_para_script` escapa `<`, `>` y `&` con su escape Unicode tras `json.dumps(ensure_ascii=False)`, no `ensure_ascii=True`; HTML/CSS/JS como archivos de plantilla en `assets/reproductor/` unidos por sustitución de marcadores, no f-strings; `verificar_salidas.py --fixture` genera sobre el primer guion de `fixtures/reales/` en vez de esperar a T-30/T-32, como ya anticipó la decisión de T-00 sobre la cuarta red
**Hallazgos del auditor atendidos:** ninguno ABIERTO de severidad alta en `auditoriacontinua.md` al empezar la sesión; no se tocó el registro (los tres ABIERTO existentes — #5, #6, #8 — siguen enrutados a R-01/R-06/T-32, ninguno afectado por T-18)
**Hallazgos:** ninguno nuevo. Alcance deliberadamente mínimo, documentado en `DEVELOPERS.md`: el reproductor de este esqueleto lista escenas y bloques en orden, sin índice navegable, pantalla completa, resaltado ni autoscroll — eso es T-19 a T-22, no una omisión de T-18.
**Tareas autopropuestas (P-XX):** ninguna
**Próximo paso:** T-19 (índice de escenas y entrada a pantalla completa), siguiente tarea de FASE B4. Puede construirse sobre `reproductor.generar_reproductor_html`/`guardar_reproductor` tal cual: añadirá su propia plantilla de índice y su propio JS de navegación sin tocar `_construir_datos` (las escenas y bloques que ya expone cubren lo que T-19 necesita).

---

### Sesión 2026-09-01 — T-17 (revalidación: releer, respetar y recalcular), sesión de nube
**Tarea(s):** T-17
**Estado resultante:** T-17 COMPLETADA
**Commits a develop:** `T-17: revalidacion, releer, respetar y recalcular` (ver `git log` de esta fecha en `develop`)
**Migraciones ejecutadas:** ninguna (`estado.validacion` es el contenedor genérico ya reservado desde T-07; T-17 solo fija la forma de su contenido, sin tocar el esquema ni su versión)
**Archivos creados/modificados:** `scripts/revalidacion.py` (nuevo: `revalidar_guion`, `ResultadoRevalidacion`, `Incidencia`, materialización de particiones con identidad estable `_materializar_marcados`, detectores de incidencia por categoría), `scripts/tiempos.py` (refactor sin cambio de comportamiento: `_bloques_respiracion_marcados` → pública `bloques_respiracion_marcados`; `calcular_tiempos` se divide y delega en el nuevo `calcular_tiempos_desde_marcados`), `scripts/reescrituras.py` (`_SEPARADOR_MITADES` → pública `SEPARADOR_MITADES`, mismo valor), `tests/test_revalidacion.py` (nuevo, 8 tests: el ciclo de tres pasadas encadenadas del criterio de aceptación literal —validar → editar → revalidar → editar → revalidar—, identidad estable de una partición aceptada en una pasada posterior, y un test por categoría del informe de incidencias), `tests/test_logica_pendiente.py` (se quita el `@pytest.mark.skip` de `test_invariante_idempotencia_de_la_revalidacion` y se implementa de verdad, tal como pedía su propio motivo desde T-03), `pyproject.toml` (per-file-ignore `RUF001` para los dos tests nuevos que usan el guion largo real de los rangos horarios), `roadmap/SEGUIMIENTO.md` (§1, cabecera, corrige de paso la referencia obsoleta a la hoja de ruta v1.1), `roadmap/DECISIONES_TECNICAS.md`, `roadmap/HISTORIAL_SESIONES.md` (esta entrada)
**Verificaciones pre-push:** tipos ✅ · lint ✅ · tests ✅ (252 pasan + 1 skipped, antes 243 + 2) · build ✅ (`verificar_salidas.py --fixture` sigue en verde con las mismas etapas NO APLICABLE hasta T-18/T-27/T-30/T-32, nada roto)
**Health check post-deploy:** N/A — sesión de nube, no instala en `~/.claude/skills/` (T-32 sigue BLOQUEADA por ese motivo)
**Decisiones tomadas:** 7 filas nuevas en `DECISIONES_TECNICAS.md` (2026-09-01, T-17): división de `calcular_tiempos` en bloques marcados + núcleo parametrizable; `SEPARADOR_MITADES` pública; identidad de bloque entre pasadas por `(escena, índice de origen, mitad)` en vez de por número de ancla o por rango de líneas; una edición manual se detecta comparando contra el texto que el sistema derivaría, sin registro explícito aparte; límite de alcance aceptado (no resuelto) cuando una normalización y una partición aceptadas coinciden en el mismo bloque de origen; `estado.validacion` guarda historial con marca de tiempo por revalidación, no solo la última; `revalidar_guion` se queda como función pura sobre datos en memoria, sin orquestar disco por su cuenta
**Hallazgos del auditor atendidos:** ninguno ABIERTO de severidad alta en `auditoriacontinua.md` al empezar la sesión; no se tocó el registro
**Hallazgos:** ninguno nuevo. Límite de alcance documentado (no un bug): una normalización (T-13) aceptada sobre un bloque que ADEMÁS tiene una partición (T-14/T-15) aceptada no se materializa en ninguna de las dos mitades — la decisión queda intacta en `estado.json` (invariante (b)), solo no se aplica visualmente en ese cruce concreto; ver la fila correspondiente en `DECISIONES_TECNICAS.md`
**Tareas autopropuestas (P-XX):** ninguna
**Próximo paso:** T-18 (esqueleto del reproductor autocontenido), primera tarea de FASE B4. No depende de ninguna pieza nueva de T-17 en particular, pero si una futura T-30 (CLI) quiere ofrecer "revalidar" como comando, ya tiene `revalidacion.revalidar_guion` como función pura lista para envolver (lee `resultado`/`texto_documento`/`estado`, no toca disco por su cuenta).

---

### Sesión 2026-09-01 — T-16 (`guion-escenas.md`, documento de revisión de una sola pasada), sesión de nube
**Tarea(s):** T-16
**Estado resultante:** T-16 COMPLETADA
**Commits a develop:** `T-16: guion-escenas.md, el documento de revision de una sola pasada` (ver `git log` de esta fecha en `develop`)
**Migraciones ejecutadas:** ninguna (no toca `estado.json`; el documento se escribe aparte, en `guion-escenas.md`)
**Archivos creados/modificados:** `scripts/documento_revision.py` (nuevo: `generar_documento_revision`, `formatear_escena`/`formatear_bloque_respiracion`/`formatear_indicaciones`/`formatear_aviso`, `extraer_texto_bloques`, `extraer_estado_revision`, `guardar_documento_revision`), `scripts/config.py` (`NOMBRE_ARCHIVO_GUION_ESCENAS`, `LONGITUD_EXTRACTO_INDICACION_MAX` y su campo en `Configuracion` con validación), `pyproject.toml` (per-file-ignore `RUF001` para el nuevo test, que usa el guion largo real de los rangos horarios como literal), `tests/test_documento_revision.py` (nuevo, 19 tests: cobertura total de escenas y bloques sobre los tres guiones reales, resumen global, numeración de bloques, reescrituras y avisos localizados sin duplicarse, indicaciones no recitables al pie con `revisar` incluido, tolerancia de `extraer_texto_bloques` a la edición manual, marca de estado `PENDIENTE`/`VALIDADO`, copia de seguridad al regenerar), `DEVELOPERS.md` (sección T-16), `roadmap/SEGUIMIENTO.md` (§1, cabecera), `roadmap/DECISIONES_TECNICAS.md`, `roadmap/HISTORIAL_SESIONES.md` (esta entrada)
**Verificaciones pre-push:** tipos ✅ · lint ✅ · tests ✅ (243 pasan + 2 skipped, antes 224 + 2) · build ✅ (`verificar_salidas.py --fixture` sigue en verde con las mismas etapas NO APLICABLE hasta T-18/T-27/T-30/T-32, nada roto)
**Health check post-deploy:** N/A — sesión de nube, no instala en `~/.claude/skills/` (T-32 sigue BLOQUEADA por ese motivo)
**Decisiones tomadas:** 5 filas nuevas en `DECISIONES_TECNICAS.md` (2026-09-01, T-16): cada escena se reorganiza en "Locución" + "Indicaciones no recitables" en vez de reproducir literalmente los rótulos del guion de origen; cada bloque de respiración se ancla con `<!-- bloque escena=N indice=K -->` (índice propio, porque varios bloques pueden compartir rango de líneas de origen); un aviso `sin_punto_respiracion` con partición sugerida no se repite junto a su reescritura de partición; el título del documento lo decide quien llama a `generar_documento_revision`, no se infiere del guion; `guardar_documento_revision` copia a `.bak-<marca_de_tiempo>` pero no usa escritura atómica de fichero temporal, a diferencia de `estado.json`
**Hallazgos del auditor atendidos:** ninguno ABIERTO de severidad alta en `auditoriacontinua.md` al empezar la sesión; no se tocó el registro
**Hallazgos:** ninguno. Se corrigió en la propia sesión (antes de dar la tarea por completada) un fallo en la primera versión de `extraer_texto_bloques`: el ancla `\A` de la cabecera `**Bloque N** (...)` no toleraba los saltos de línea que preceden a esa cabecera dentro del propio ancla `<!-- bloque ... -->`, así que la cabecera quedaba sin recortar; corregido a `\A\s*\*\*Bloque...`, verificado con `test_extraer_texto_bloques_recupera_edicion_manual` y a mano contra los tres guiones reales antes de escribir la suite
**Tareas autopropuestas (P-XX):** ninguna
**Próximo paso:** T-17 (revalidación: releer, respetar y recalcular). Ya tiene disponibles `extraer_texto_bloques` y `extraer_estado_revision` de T-16 para releer `guion-escenas.md` como autoritativo (invariante (c)), y `pendientes`/`fusionar_con_estado` de T-15 para no repetir una reescritura ya decidida.

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
