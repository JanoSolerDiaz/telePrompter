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
**Última actualización:** 2026-10-02 — **Ciclo de Programador: R-21 implementada y `COMPLETADA`**
(Fase transversal F-J, cierra el hallazgo `#27` de `auditoriacontinua.md`). `scripts/salidas.py::_generar_concat_ffmpeg`
invoca ahora `concat_ffmpeg.validar_lista_concat_ffmpeg` sobre el contenido antes de escribirlo —
hasta ahora solo lo ejercitaba `verificar_salidas.py --fixture`, nunca la ruta real de generación —
degradando a `SalidaOmitida` con el motivo exacto si falla, nunca una excepción sin capturar.
`scripts/tomas.py` gana `_sanear_archivo_video` (recorta espacios, normaliza a `""` si queda vacío o
trae `\n`/`\r`) aplicada al leer un parte de rodaje editado a mano; `assets/reproductor/guion.js` gana
la función gemela `sanearArchivoVideo(valor)` aplicada en los dos puntos donde el dueño teclea el
valor (grabación con `V`/`v` y edición desde el índice). 6 tests nuevos (613→619). Cuatro redes en
verde, incluidas las dieciséis etapas de `verificar_salidas.py --fixture`. `references/contrato-tomas.md`,
`contrato-montaje.md`, `DEVELOPERS.md` y `SKILL.md` actualizados. Decisión registrada en
`DECISIONES_TECNICAS.md`; detalle completo de este ciclo en `HISTORIAL_SESIONES.md`. §1 pasa `R-21` a
`COMPLETADA`. Sin hallazgo de severidad alta `ABIERTO` en `auditoriacontinua.md` que atender como
P-XX urgente antes de esta tarea (único hallazgo `ABIERTO` de severidad media, `#27`, es justamente el
que esta tarea cierra; `#24`, baja, sigue pendiente solo de la respuesta del dueño a la pregunta #11
de §6).

**Nota de arranque de esta sesión:** sin incidencia. `git status` limpio antes de tocar nada;
`git checkout develop && git pull origin develop` resolvió en fast-forward limpio hasta `4890134`
(trece commits), sin `HEAD` *detached* ni rama divergida esta vez. `pip install -r
requirements-dev.txt` limpio. Registro de hallazgos de `auditoriacontinua.md`: dos `ABIERTO`, ninguno
de severidad alta — `#24` (baja, proceso, pregunta de gobernanza #11 de §6 sigue `(pendiente)`) y
`#27` (media, exactamente el hallazgo que esta tarea atiende). Siguiente tarea según §1: `R-21`
(única R-XX `PENDIENTE` tras R-20, abierta por el ciclo de PM anterior, spec completa en
`ROADMAP_PRODUCTO.md` §Fase transversal F-J).

**Última actualización anterior (ciclo de Product Manager, 2026-10-01): archiva Oleada v9 (R-20) y
abre R-21** (Fase transversal F-J) desde el hallazgo `#27` de `auditoriacontinua.md` (detalle en la nota
de arranque de esa sesión, más abajo).

**Última actualización anterior (R-20, implementada en el ciclo previo):** `scripts/reproductor.py::_indicaciones_ancladas_por_indice` (R-12) se divide: el
algoritmo de anclaje (máximo bloque de respiración cuyo `linea_fin` precede a la indicación, o el
primero si no hay ninguno) se extrae a la función pública `anclar_indicaciones_a_bloques` (mismo
patrón que R-19 extrajo `tomas.toma_buena` de `duracion_toma_buena`), devolviendo la indicación
cruda por índice de bloque en vez del texto ya formateado; `_indicaciones_ancladas_por_indice` queda
como envoltorio de una línea que aplica el formato `Pantalla:`/`Nota:` — comportamiento del
reproductor intacto. `scripts/pptx.py` reutiliza esa función nueva: `Tarjeta` gana
`indicaciones_ancladas` (dataclass `IndicacionAnclada`: `texto`, `es_nota_interna`,
`instante_estimado_segundos`), mismo conjunto que `indicaciones_pantalla`/`notas_internas` sin
perder ni duplicar ninguna (invariante (a) extendido). El instante se calcula relativo al inicio de
la escena en `_indicaciones_ancladas_de_escena` y se convierte a absoluto del vídeo en
`_con_limites_absolutos` (R-16), sumando el mismo acumulado real-o-estimado que ya usa para
`inicio_segundos`/`fin_segundos` — sin ninguna fuente de tiempo nueva. Una escena sin ningún bloque
de locución (sin ejemplo en los guiones reales, pero contemplada por `validar_tarjetas`) ancla cada
indicación al inicio de la escena en vez de perderla. `--para-terceros` omite las notas internas
también aquí, con el mismo criterio que `notas_internas`. Cambio puramente aditivo: `version_contrato`
no sube, sin campo nuevo de `Configuracion` ni migración de `estado.json`. 7 tests nuevos (606→613),
incluido uno que compara el instante exacto de `tarjetas.json` contra el que calcula el reproductor
para la misma indicación del mismo guion (sin toma real de por medio, los dos acumulados coinciden
bit a bit — criterio de aceptación literal: "mismo bloque ancla, dos consumidores"). Cuatro redes en
verde, incluida la validación de `tarjetas.json` de `verificar_salidas.py --fixture` (la clave nueva
pasa por `validar_tarjetas` sin cambios propios en el validador, mismo rigor que el resto de listas
de indicaciones). `DEVELOPERS.md`, `SKILL.md` y `references/contrato-tarjetas.md`/
`contrato-montaje.md` actualizados. Decisiones registradas en `DECISIONES_TECNICAS.md`. Sin cambios
en §3 (bloqueos) ni §5 (P-XX); ningún hallazgo de `auditoriacontinua.md` es de severidad alta
(`#24` baja, `#27` media, ninguno urgente por §0.3); §1 pasa `R-20` a `COMPLETADA`.

**Nota de arranque de la sesión anterior (ciclo de Product Manager, 2026-10-01):** sin incidencia.
`git status` limpio antes de tocar nada; `git checkout develop` dejó el contenedor en `HEAD`
*detached* 11 commits por detrás de `origin/develop` (reconfirmaciones del Programador ya superadas);
`git pull origin develop` resolvió con fast-forward trivial (`51e38da..8e155bf`) sin conflicto ni
pérdida — ningún `git reset --hard` ni rama auxiliar necesarios. `pip install -r
requirements-dev.txt` limpio.

**Ciclo de Product Manager (2026-10-01): archiva Oleada v9 (R-20) y abre R-21 (Fase transversal
F-J).** §1 (fuente autoritativa) ya registraba R-20 `COMPLETADA` desde el 2026-09-30, tras nueve
reconfirmaciones del Programador sin cambio de código; `ROADMAP_PRODUCTO.md` seguía describiéndola
como "EN CURSO"/`PENDIENTE` (mismo patrón que el hallazgo `#24`) — movida a `ROADMAP_HISTORICO.md`
con su spec completa, cabecera y "Cola de producto" corregidas. Registro de hallazgos de
`auditoriacontinua.md`: dos `ABIERTO`, ninguno de severidad alta — `#24` (baja, proceso, la pregunta
de gobernanza #11 de §6 sigue `(pendiente)`, ajena al contenido de este roadmap) y `#27` (media,
2026-10-01, reproducido con código por el auditor: `scripts/salidas.py::_generar_concat_ffmpeg` no
invoca `concat_ffmpeg.validar_lista_concat_ffmpeg` antes de escribir a disco, y `archivo_video` no se
sanea en sus dos puntos de entrada). `#27` es el único hallazgo técnico de esta pasada: se convierte
en **R-21** (Fase transversal F-J, `origen: auditoría #27`), spec completa en `ROADMAP_PRODUCTO.md`
§Fase transversal F-J. `roadmap/FEEDBACK.md` sigue sin ninguna entrada `nuevo`. Decisiones registradas
en `DECISIONES_TECNICAS.md`; detalle completo de este ciclo en `HISTORIAL_SESIONES.md` (sesión 58).
Sin cambios en §3 ni §5; §6 sin novedad (la pregunta #11 sigue `(pendiente)`). Este ciclo es de PM,
no de Programador: no se añade fila nueva a §1 para R-21 (la añade el Programador al implementarla,
mismo patrón que R-19/R-20) ni se ejecuta la verificación de las cuatro redes.

**Última actualización anterior (resumen; detalle completo en `HISTORIAL_SESIONES.md` y
`DECISIONES_TECNICAS.md`, no repetido aquí para no seguir engordando este documento):**
- 2026-10-01, ciclo de Product Manager: archiva Oleada v9 (R-20) a `ROADMAP_HISTORICO.md` y abre
  R-21 (Fase transversal F-J) desde el hallazgo `#27` de `auditoriacontinua.md` (media, validación de
  `concat-ffmpeg.txt` nunca invocada en la ruta real de generación, `archivo_video` sin sanear).
  Detalle completo arriba (ver "Ciclo de Product Manager (2026-10-01)") y en `HISTORIAL_SESIONES.md`
  (sesión 58).
- 2026-10-01, ciclo de Programador: novena reconfirmación tras R-20, tras la octava de hoy
  (`ae3107a`), sin novedad de código. Verificación propia completa: `mypy`/`ruff` en verde sin
  hallazgos, 613 tests (`pytest`) en verde, dieciséis etapas OK en `verificar_salidas.py --fixture`.
  `auditoriacontinua.md` con dos `ABIERTO`, ninguno de severidad alta (`#24` baja, proceso; `#27`
  media, robustez de validación de `concat_ffmpeg.py`). `roadmap/FEEDBACK.md` sin ninguna entrada
  `nuevo`; cero issues y cero PR abiertos en GitHub. Nota sin acción, mismo patrón que motivó `#24`:
  la prosa de "Cola de producto" de `ROADMAP_PRODUCTO.md` seguía describiendo R-20 como
  "EN CURSO"/`PENDIENTE` pese a que este §1 ya la registraba `COMPLETADA` — corregido por el ciclo de
  PM siguiente (ver arriba).
- 2026-10-01, ciclo de Programador: octava reconfirmación tras R-20, sin novedad de código.
- 2026-10-01, ciclo de Programador: séptima reconfirmación tras R-20, sin novedad de código.
- 2026-10-01, ciclo de Programador: sexta reconfirmación tras R-20, sin novedad de código.
- 2026-10-01, ciclo de Programador: quinta reconfirmación tras R-20, sin novedad de código.
- 2026-10-01, ciclo de Programador: cuarta reconfirmación tras R-20, sin novedad de código.
- 2026-10-01, ciclo de Programador: tercera reconfirmación tras R-20, sin novedad de código.
- 2026-10-01, ciclo de Programador: segunda reconfirmación tras R-20, sin novedad de código.
- 2026-10-01, ciclo de Programador: primera reconfirmación tras R-20, sin novedad de código.
- 2026-10-01, ciclo de Programador: R-20 implementada y `COMPLETADA` (Oleada v9). Ver el párrafo de
  "Última actualización anterior (R-20...)" arriba para el detalle técnico completo.
- 2026-09-30, ciclo de Product Manager: archiva R-19/Oleada v8 a `ROADMAP_HISTORICO.md` y corrige la
  prosa de `ROADMAP_PRODUCTO.md` que seguía describiendo R-19 como `PENDIENTE` pese a que §1 ya la
  registraba `COMPLETADA` (mismo patrón de latencia que el hallazgo `#24`). Atiende el hallazgo `#26`
  de `auditoriacontinua.md` (media, gobernanza del propio PM): el ciclo del 2026-09-29 había
  presentado una frase fija del encargo de esta misma rutina como "instrucción directa del dueño",
  cuando `list_triggers` confirma que es texto sin cambios desde 2026-08-31 — R-19 no se revierte
  (diseño sólido y aditivo) pero `ROADMAP_PRODUCTO.md` corrige la premisa a la grieta de arquitectura
  ya razonada el 2026-09-21. Deja escrito en `DECISIONES_TECNICAS.md` el criterio para futuras
  aperturas: las tres fuentes ya establecidas (auditoría, `FEEDBACK.md`, grieta de arquitectura
  verificada) bastan por sí solas, sin apoyarse en el encargo estable de la rutina. **Abre R-20**
  (Oleada v9): `tarjetas.json` ganará `indicaciones_ancladas`, reutilizando el anclaje que
  `reproductor.py` (R-12) ya calcula para la cue en vivo — mismo patrón de apertura que R-12 a R-18
  (grieta de arquitectura verificada). Spec completa en `ROADMAP_PRODUCTO.md` §Oleada v9. Ciclo de PM:
  no se ejecuta la verificación de las cuatro redes.
- 2026-09-30, ciclo de Programador: R-19 implementada y COMPLETADA (Oleada v8). `archivo_video` por
  toma anotable con `V`/`v` durante la grabación o editable después desde el índice sin volver a
  grabar; `scripts/concat_ffmpeg.py` (módulo nuevo) genera `concat-ffmpeg.txt`, la lista de
  concatenación del demuxer `concat` de ffmpeg, sexta opción del selector de salidas (T-30). 23 tests
  nuevos (583→606). Cuatro redes en verde, incluidas dos etapas nuevas en `verificar_salidas.py
  --fixture` (dieciséis en total). Verificado también con Playwright/Chromium real. Detalle completo
  en `HISTORIAL_SESIONES.md`/`DECISIONES_TECNICAS.md`.
- 2026-09-30, décima sesión del día con el mismo patrón de arranque: contenedor en `HEAD` *detached*
  con la rama local divergida 50 commits sin ancestro común de `origin/develop`, resuelta con `git
  reset --hard origin/develop` sin riesgo de pérdida (commits locales descartados eran solo
  reconfirmaciones vacías ya superadas). Detalle completo en la entonces "nota de arranque de esta
  sesión", ahora superada por la de arriba.
- 2026-09-30, ciclo de Programador: novena reconfirmación tras R-19, tras la octava de hoy
  (`af4d09b`), sin novedad de código. Verificación propia completa: `mypy`/`ruff` en verde (70
  archivos, sin hallazgos), 606 tests (`pytest`) en verde, dieciséis etapas OK en
  `verificar_salidas.py --fixture`. `auditoriacontinua.md` mantiene los mismos dos `ABIERTO`,
  ninguno de severidad alta ni urgente por §0.3: `#24` (baja, proceso, esperando la respuesta del
  dueño a la pregunta #11 de §6) y `#26` (media, gobernanza de la apertura de R-19, ajena al
  código). `roadmap/FEEDBACK.md` sin ninguna entrada `nuevo`; `mcp__github__list_issues`/
  `list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero issues y cero PR abiertos. Nota sin
  acción, mismo patrón que motivó `#24`: la prosa de "Cola de producto" de `ROADMAP_PRODUCTO.md`
  sigue describiendo R-19 como `PENDIENTE` pese a que este §1 ya la registra `COMPLETADA` — no se
  corrige desde aquí (la pregunta #11 de §6, que decidiría si el Programador puede corregirla por
  su cuenta, sigue `(pendiente)` de respuesta del dueño). Divergencia de arranque repetida, misma
  magnitud que la sesión anterior (50 commits sin ancestro común a cada lado), resuelta con `git
  reset --hard origin/develop`; detalle en la nota de arranque de esta sesión, más arriba.
- 2026-09-30, ciclo de Programador: octava reconfirmación tras R-19, tras la séptima de hoy
  (`aec35da`), sin novedad de código. Verificación propia completa: `mypy`/`ruff` en verde (70
  archivos, sin hallazgos), 606 tests (`pytest`) en verde, dieciséis etapas OK en
  `verificar_salidas.py --fixture`. `auditoriacontinua.md` mantiene los mismos dos `ABIERTO`,
  ninguno de severidad alta ni urgente por §0.3: `#24` (baja, proceso, esperando la respuesta del
  dueño a la pregunta #11 de §6) y `#26` (media, gobernanza de la apertura de R-19, ajena al
  código). `roadmap/FEEDBACK.md` sin ninguna entrada `nuevo`; `mcp__github__list_issues`/
  `list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero issues y cero PR abiertos. Nota sin
  acción, mismo patrón que motivó `#24`: la prosa de "Cola de producto" de `ROADMAP_PRODUCTO.md`
  sigue describiendo R-19 como `PENDIENTE` pese a que este §1 ya la registra `COMPLETADA` — no se
  corrige desde aquí (la pregunta #11 de §6, que decidiría si el Programador puede corregirla por
  su cuenta, sigue `(pendiente)` de respuesta del dueño). Divergencia de arranque más marcada de lo
  habitual (50 commits sin ancestro común a cada lado), resuelta con `git reset --hard
  origin/develop`; detalle en la nota de arranque de esta sesión, más arriba.
- 2026-09-30, ciclo de Programador: séptima reconfirmación tras R-19, tras la sexta de hoy
  (`7f160cb`), sin novedad de código. Verificación propia completa: `mypy`/`ruff` en verde, 606 tests
  (`pytest`) en verde, dieciséis etapas OK en `verificar_salidas.py --fixture`. `auditoriacontinua.md`
  mantiene los mismos dos `ABIERTO`, ninguno de severidad alta ni urgente por §0.3: `#24` (baja,
  proceso, esperando la respuesta del dueño a la pregunta #11 de §6, sin pasada nueva desde la ya
  registrada) y `#26` (media, gobernanza de la apertura de R-19, ajena al código). `roadmap/FEEDBACK.md`
  sin ninguna entrada `nuevo`; `mcp__github__list_issues`/`list_pull_requests` sobre
  `janosolerdiaz/telePrompter`: cero issues y cero PR abiertos.
- 2026-09-30, ciclo de Programador: sexta reconfirmación tras R-19, tras la quinta de hoy
  (`431b304`), sin novedad de código. Verificación propia completa: `mypy`/`ruff` en verde, 606 tests
  (`pytest`) en verde, dieciséis etapas OK en `verificar_salidas.py --fixture`. `auditoriacontinua.md`
  mantiene los mismos dos `ABIERTO`, ninguno de severidad alta ni urgente por §0.3: `#24` (baja,
  proceso, esperando la respuesta del dueño a la pregunta #11 de §6, sin pasada nueva desde la ya
  registrada) y `#26` (media, gobernanza de la apertura de R-19, ajena al código). `roadmap/FEEDBACK.md`
  sin ninguna entrada `nuevo`; `mcp__github__list_issues`/`list_pull_requests` sobre
  `janosolerdiaz/telePrompter`: cero issues y cero PR abiertos.
- 2026-09-30, ciclo de Programador: quinta reconfirmación tras R-19, tras la cuarta de hoy
  (`1e3175a`), sin novedad de código. Verificación propia completa: `mypy`/`ruff` en verde, 606 tests
  (`pytest`) en verde, dieciséis etapas OK en `verificar_salidas.py --fixture`. `auditoriacontinua.md`
  mantiene los mismos dos `ABIERTO`, ninguno de severidad alta ni urgente por §0.3: `#24` (baja,
  proceso, esperando la respuesta del dueño a la pregunta #11 de §6, sin pasada nueva desde la ya
  registrada) y `#26` (media, gobernanza de la apertura de R-19, ajena al código). `roadmap/FEEDBACK.md`
  sin ninguna entrada `nuevo`; `mcp__github__list_issues`/`list_pull_requests` sobre
  `janosolerdiaz/telePrompter`: cero issues y cero PR abiertos.
- 2026-09-30, ciclo de Programador: cuarta reconfirmación tras R-19, tras la tercera de hoy
  (`9455322`), sin novedad de código. `auditoriacontinua.md` mantiene los mismos dos `ABIERTO`,
  ninguno de severidad alta ni urgente por §0.3: `#24` (baja, proceso, esperando la respuesta del
  dueño a la pregunta #11 de §6, sin pasada nueva desde la ya registrada) y `#26` (media, gobernanza
  de la apertura de R-19, ajena al código). `roadmap/FEEDBACK.md` sin ninguna entrada `nuevo`;
  `mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero issues y
  cero PR abiertos. Cuatro redes en verde (606 tests, dieciséis etapas OK en
  `verificar_salidas.py --fixture`).
- 2026-09-30, ciclo de Programador: tercera reconfirmación tras R-19, tras la segunda de hoy
  (`b2a6676`), sin novedad de código. `auditoriacontinua.md` mantiene los mismos dos `ABIERTO`,
  ninguno de severidad alta ni urgente por §0.3: `#24` (baja, proceso, esperando la respuesta del
  dueño a la pregunta #11 de §6, sin pasada nueva desde la ya registrada) y `#26` (media, gobernanza
  de la apertura de R-19, ajena al código). `roadmap/FEEDBACK.md` sin ninguna entrada `nuevo`;
  `mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero issues y
  cero PR abiertos. Cuatro redes en verde (606 tests, dieciséis etapas OK en
  `verificar_salidas.py --fixture`).
- 2026-09-30, ciclo de Programador: segunda reconfirmación tras R-19, tras la primera de hoy
  (`e684987`), sin novedad de código. `auditoriacontinua.md` mantiene dos `ABIERTO`, ninguno de
  severidad alta ni urgente por §0.3: `#24` (baja, proceso, catorce pasadas de auditoría esperando la
  respuesta del dueño a la pregunta #11 de §6, sin pasada nueva desde la del 2026-09-30 ya
  registrada) y `#26` (media, gobernanza de la apertura de R-19,
  ajena al código). `roadmap/FEEDBACK.md` sin ninguna entrada `nuevo`; `mcp__github__list_issues`/
  `list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero issues y cero PR abiertos. Cuatro
  redes en verde (606 tests, dieciséis etapas OK en `verificar_salidas.py --fixture`).
- 2026-09-30, ciclo de Programador: primera reconfirmación tras R-19 (implementada y COMPLETADA en
  el ciclo anterior, `5205549`), sin novedad de código. `auditoriacontinua.md` mantiene dos `ABIERTO`,
  ninguno de severidad alta ni urgente por §0.3: `#24` (baja, proceso, catorce pasadas de auditoría
  esperando la respuesta del dueño a la pregunta #11 de este §6) y `#26` (media, gobernanza de la
  apertura de R-19, ajena al código). Nota sin acción: la prosa de "Cola de producto" de
  `ROADMAP_PRODUCTO.md` sigue describiendo R-19 como `PENDIENTE` pese a que este §1 ya la registra
  `COMPLETADA` — mismo patrón que motivó `#24`; se deja constancia para el próximo ciclo de PM
  (quien escribe ese documento), sin corregirla desde aquí. `roadmap/FEEDBACK.md` sin ninguna entrada
  `nuevo`; `mcp__github__list_issues`/`list_pull_requests` sobre `janosolerdiaz/telePrompter`: cero
  issues y cero PR abiertos. Cuatro redes en verde (606 tests, dieciséis etapas OK en
  `verificar_salidas.py --fixture`).
- 2026-09-29, ciclo de Product Manager: se abre R-19 (Oleada v8), la primera R-XX nueva desde R-18
  (2026-09-17) tras quince ciclos de PM consecutivos reconfirmando la cola vacía. Spec completa en
  `ROADMAP_PRODUCTO.md` §Oleada v8. Corrige también el hallazgo `#25` de `auditoriacontinua.md`
  (baja, prosa) — cifra de "pasadas de auditoría... pregunta #11" de `quince` a **trece**. `#24`
  sigue `ABIERTO`, enrutado a la pregunta #11 de §6, *(pendiente)* de respuesta del dueño.
- 2026-09-29, ciclo de Programador: décima reconfirmación del día, tras la novena de hoy
  (`0d3fadd`), sin novedad de código. Verificación propia: clon *shallow* en *detached HEAD*
  resuelto (`git fetch --unshallow` + `git merge --ff-only origin/develop`, sin pérdida de trabajo
  local); cuatro redes en verde (583 tests, catorce etapas OK); `mcp__github__list_issues`/
  `list_pull_requests` sin issues ni PR abiertos.
- 2026-09-29, ciclo de Programador: novena reconfirmación del día, tras la octava de hoy
  (`09fd0e9`), sin novedad de código.
- 2026-09-29, ciclo de Programador: octava reconfirmación del día, tras la séptima de hoy
  (`3e272f6`), sin novedad de código.
- 2026-09-29, ciclo de Programador: séptima reconfirmación del día, tras la sexta de hoy
  (`f20002c`), sin novedad de código.
- 2026-09-29, ciclo de Programador: sexta reconfirmación del día, tras la quinta de hoy
  (`91cfc1d`), sin novedad de código.
- 2026-09-29, ciclo de Programador: quinta reconfirmación del día, tras la cuarta de hoy
  (`0ab65df`), sin novedad de código.
- 2026-09-29, ciclo de Programador: cuarta reconfirmación del día, tras la tercera de hoy
  (`c8c9be5`), sin novedad de código.
- 2026-09-29, ciclo de Programador: tercera reconfirmación del día, tras la segunda de hoy
  (`bf9c45e`), sin novedad de código.
- 2026-09-29, ciclo de Programador: segunda reconfirmación del día, tras la primera de hoy
  (`c59df89`), sin novedad de código.
- 2026-09-29, ciclo de Programador: primera reconfirmación del día, tras la decimosexta auditoría en
  profundidad (`d14776a`, un hallazgo nuevo de proceso, `#25`) y el decimoquinto ciclo de PM
  consecutivo sin apertura (`de45611`), sin novedad de código.
- 2026-09-28, ciclo de Product Manager: reconfirmación de cola vacía, sin R-XX nueva (decimoquinto
  ciclo de PM consecutivo sin apertura).
- 2026-09-28, ciclo de Programador: vigésima reconfirmación del día, tras la decimonovena de hoy
  (`92c7f46`), sin novedad de código.
- 2026-09-28, ciclo de Programador: decimonovena reconfirmación del día, tras la decimoctava de
  hoy (`3b1f3fe`), sin novedad de código.
- 2026-09-28, ciclo de Programador: decimoctava reconfirmación del día, tras la decimoséptima de
  hoy (`f774577`), sin novedad de código.
- 2026-09-28, ciclo de Programador: decimoséptima reconfirmación del día, tras la decimosexta de
  hoy (`7ac67d4`), sin novedad de código.
- 2026-09-28, ciclo de Programador: decimosexta reconfirmación del día, tras la decimoquinta de
  hoy (`41f719f`), sin novedad de código.
- 2026-09-28, ciclo de Programador: decimoquinta reconfirmación del día, tras la decimocuarta de
  hoy (`e881f58`), sin novedad de código.
- 2026-09-28, ciclo de Programador: decimocuarta reconfirmación del día, tras la decimotercera de
  hoy (`aa7a6f2`), sin novedad de código.
- 2026-09-28, ciclo de Programador: decimotercera reconfirmación del día, tras la duodécima de hoy
  (`c08cbcb`), sin novedad de código.
- 2026-09-28, ciclo de Programador: duodécima reconfirmación del día, tras la undécima de hoy
  (`8530ac2`), sin novedad de código.
- 2026-09-28, ciclo de Programador: undécima reconfirmación del día, tras la decimoquinta auditoría
  en profundidad (`f694a29`) y el decimocuarto ciclo de PM consecutivo sin apertura (`b4912c4`), sin
  novedad de código.
- 2026-09-27, ciclo de Product Manager: reconfirmación de cola vacía, sin R-XX nueva (decimocuarto
  ciclo de PM consecutivo sin apertura).
- 2026-09-27, ciclo de Auditoría: decimocuarta pasada consecutiva sin cambios de código, cero
  hallazgos nuevos. `#24` (baja, de proceso) reconfirmado `ABIERTO`, pendiente exclusivamente de la
  respuesta del dueño a la pregunta #11 de §6 (once pasadas consecutivas esperándola).
- 2026-09-26, ciclo de Product Manager: reconfirmación de cola vacía, sin R-XX nueva (decimotercer
  ciclo de PM consecutivo sin apertura).
- 2026-09-25, ciclo de Auditoría: decimotercera pasada consecutiva sin cambios de código, cero
  hallazgos nuevos. `#24` (baja, de proceso) reconfirmado `ABIERTO`, pendiente exclusivamente de la
  respuesta del dueño a la pregunta #11 de §6.
- 2026-09-25, ciclo de Product Manager: reconfirmación de cola vacía, sin R-XX nueva (duodécimo
  ciclo de PM consecutivo sin apertura).
- 2026-09-25, ciclo de Programador: décima reconfirmación del día, tras la novena de hoy
  (`4a1e7ab`), sin novedad de código.
- 2026-09-25, ciclo de Programador: novena reconfirmación del día, tras la octava de hoy
  (`630482d`), sin novedad de código.
- 2026-09-25, ciclo de Programador: octava reconfirmación del día, tras la séptima de hoy
  (`78075a2`), sin novedad de código.
- 2026-09-25, ciclo de Programador: séptima reconfirmación del día, tras la sexta de hoy
  (`ea04ef7`), sin novedad de código.
- 2026-09-25, ciclo de Programador: sexta reconfirmación del día, tras la quinta de hoy
  (`f91275a`), sin novedad de código.
- 2026-09-25, ciclo de Programador: quinta reconfirmación del día, tras la cuarta de hoy
  (`6a4dc53`), sin novedad de código.
- 2026-09-25, ciclo de Programador: cuarta reconfirmación del día, tras la tercera de hoy
  (`dc94f78`), sin novedad de código.
- 2026-09-25, ciclo de Programador: tercera reconfirmación del día, tras la segunda de hoy
  (`ef06378`), sin novedad de código.
- 2026-09-25, ciclo de Programador: segunda reconfirmación del día, tras la primera de hoy
  (`6e5c795`), sin novedad de código.
- 2026-09-25, ciclo de Programador: primera reconfirmación del día, tras la duodécima auditoría en
  profundidad (`312fe75`) y el undécimo ciclo de PM consecutivo sin apertura (`0af6e69`), sin
  novedad de código.
- 2026-09-25, ciclo de Auditoría: duodécima pasada consecutiva sin cambios de código, cero hallazgos
  nuevos. `#24` (baja, de proceso) reconfirmado `ABIERTO`, pendiente exclusivamente de la respuesta
  del dueño a la pregunta #11 de §6.
- 2026-09-24, ciclo de Product Manager: reconfirmación de cola vacía, sin R-XX nueva (undécimo ciclo
  de PM consecutivo sin apertura).
- 2026-09-24, ciclo de Programador: décima reconfirmación del día, tras la novena de hoy
  (`5d7168e`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-24, ciclo de Programador: novena reconfirmación del día, tras la octava de hoy
  (`d1c6751`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-24, ciclo de Programador: octava reconfirmación del día, tras la séptima de hoy
  (`1b60b67`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-24, ciclo de Programador: séptima reconfirmación del día, tras la sexta de hoy
  (`7f97666`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-24, ciclo de Programador: sexta reconfirmación del día, tras la quinta de hoy
  (`c3c8b93`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-24, ciclo de Programador: quinta reconfirmación del día, tras la cuarta de hoy
  (`5e16a5a`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-24, ciclo de Programador: cuarta reconfirmación del día, tras la tercera de hoy
  (`71bec46`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-24, ciclo de Programador: tercera reconfirmación del día, tras la segunda de hoy
  (`33c773d`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-24, ciclo de Programador: segunda reconfirmación del día, tras la primera de hoy
  (`7be1648`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-24, ciclo de Programador: primera reconfirmación del día, tras la undécima auditoría en
  profundidad (`6341558`) y el décimo ciclo de PM consecutivo sin apertura (`5f7b071`), sin novedad
  de código. Cuatro redes en verde (583 tests).
- 2026-09-23, ciclo de Product Manager: reconfirmación de cola vacía, sin R-XX nueva (décimo ciclo
  de PM consecutivo sin apertura).
- 2026-09-23, ciclo de Programador: décima reconfirmación del día, tras la novena de hoy
  (`b9858fb`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-23, ciclo de Programador: novena reconfirmación del día, tras la octava de hoy
  (`979e821`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-23, ciclo de Programador: octava reconfirmación del día, tras la séptima de hoy
  (`c2cf6bb`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-23, ciclo de Programador: séptima reconfirmación del día, tras la sexta de hoy
  (`df16dd8`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-23, ciclo de Programador: sexta reconfirmación del día, tras la quinta de hoy
  (`9e9e7fa`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-23, ciclo de Programador: quinta reconfirmación del día, tras la cuarta de hoy
  (`6d2ff43`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-23, ciclo de Programador: cuarta reconfirmación del día, tras la tercera de hoy
  (`20a7f21`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-23, ciclo de Programador: tercera reconfirmación del día, tras la segunda de hoy
  (`f408b3d`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-23, ciclo de Programador: segunda reconfirmación del día, tras la primera de hoy
  (`a5a45b1`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-23, ciclo de Programador: primera reconfirmación del día, tras la auditoría en
  profundidad de hoy (`3a58f1c`, décima pasada consecutiva sin cambios de código) y el noveno
  ciclo de PM consecutivo sin apertura (`3ed68e4`), sin novedad de código. Cuatro redes en verde
  (583 tests).
- 2026-09-22, ciclo de Product Manager: reconfirmación de cola vacía, sin R-XX nueva (noveno ciclo
  de PM consecutivo sin apertura). Verificación propia por `grep` del hilo
  `tomas_por_escena`/`EstadoProyecto.tomas` en los seis módulos que R-18 conecta, sin grieta nueva.
- 2026-09-22, ciclo de Programador: décima reconfirmación del día, tras la novena de esta mañana
  (`5e52707`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-22, ciclo de Programador: novena reconfirmación del día, tras la octava de esta mañana
  (`a4936ea`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-22, ciclo de Programador: octava reconfirmación del día, tras la séptima de esta mañana
  (`aa9aa23`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-22, ciclo de Programador: séptima reconfirmación del día, tras la sexta de esta mañana
  (`5f94051`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-22, ciclo de Programador: sexta reconfirmación del día, tras la quinta de esta mañana
  (`c231141`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-22, ciclo de Programador: quinta reconfirmación del día, tras la cuarta de esta mañana
  (`e5c77f5`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-22, ciclo de Programador: cuarta reconfirmación del día, tras la tercera de esta mañana
  (`9c8bfb0`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-22, ciclo de Programador: tercera reconfirmación del día, tras la segunda de esta mañana
  (`7b34ee8`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-22, ciclo de Programador: segunda reconfirmación del día, tras la primera de esta mañana
  (`8aa846b`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-22, ciclo de Programador: primera reconfirmación del día, tras la novena auditoría en
  profundidad (`f1d1728`) y el noveno ciclo de PM consecutivo sin apertura (`2e214d1`), sin novedad
  de código. Cuatro redes en verde (583 tests).
- 2026-09-21, ciclo de Product Manager: reconfirmación de cola vacía, sin R-XX nueva (octavo ciclo
  de PM consecutivo sin apertura). Candidata futura (toma↔archivo de vídeo + concatenación ffmpeg)
  registrada en `ROADMAP_PRODUCTO.md`/`DECISIONES_TECNICAS.md`, no abierta como R-XX.
- 2026-09-21, ciclo de Programador: décima reconfirmación del día, tras la novena de esta mañana
  (`f247522`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-21, ciclo de Programador: novena reconfirmación del día, tras la octava de esta mañana
  (`1665900`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-21, ciclo de Programador: octava reconfirmación del día, tras la séptima de esta mañana
  (`aa74cd2`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-21, ciclo de Programador: séptima reconfirmación del día, tras la sexta de esta mañana
  (`3d3ec38`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-21, ciclo de Programador: sexta reconfirmación del día, tras la quinta de esta mañana
  (`3284211`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-21, ciclo de Programador: quinta reconfirmación del día, tras la cuarta de esta mañana
  (`570fd81`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-21, ciclo de Programador: cuarta reconfirmación del día, tras la tercera de esta mañana
  (`410d657`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-21, ciclo de Programador: tercera reconfirmación del día, tras la segunda de esta mañana
  (`bb6779d`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-21, ciclo de Programador: segunda reconfirmación del día, tras la de esta mañana
  (`abd4129`), sin novedad de código. Cuatro redes en verde (583 tests).
- 2026-09-21, ciclo de Programador: primera reconfirmación tras el fin de semana, sin novedad de
  código (solo ciclos de PM el 2026-09-19 y el 2026-09-20, sin cron de Programador en
  sábado/domingo). Cuatro redes en verde (583 tests).
- 2026-09-20, ciclo de Product Manager: reconfirmación de cola vacía, sin R-XX nueva (séptimo ciclo
  de PM consecutivo sin apertura).
- 2026-09-19, ciclo de Product Manager: reconfirmación de cola vacía, sin R-XX nueva.
- 2026-09-18, ciclo de Product Manager: reconfirmación de cola vacía, sin R-XX nueva.
- 2026-09-18, ciclo de Programador: décima reconfirmación tras el archivado de R-18 (PM) y la
  auditoría en profundidad, sin novedad de código. Cuatro redes en verde (583 tests). Único
  `ABIERTO` de `auditoriacontinua.md`: `#24` (baja, de proceso).
- 2026-09-18, ciclo de Programador: novena reconfirmación tras R-18 y la auditoría en profundidad,
  sin novedad de código. Cuatro redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`:
  `#24` (baja, de proceso).
- 2026-09-18, ciclo de Programador: octava reconfirmación tras R-18 y la auditoría en profundidad,
  sin novedad de código. Cuatro redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`:
  `#24` (baja, de proceso).
- 2026-09-18, ciclo de Programador: séptima reconfirmación tras R-18 y la auditoría en profundidad,
  sin novedad de código. Cuatro redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`:
  `#24` (baja, de proceso).
- 2026-09-18, ciclo de Programador: sexta reconfirmación tras R-18 y la auditoría en profundidad,
  sin novedad de código. Cuatro redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`:
  `#24` (baja, de proceso).
- 2026-09-18, ciclo de Programador: quinta reconfirmación tras R-18 y la auditoría en profundidad,
  sin novedad de código. Cuatro redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`:
  `#24` (baja, de proceso).
- 2026-09-18, ciclo de Programador: cuarta reconfirmación tras R-18 y la auditoría en profundidad,
  sin novedad de código. Cuatro redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`:
  `#24` (baja, de proceso).
- 2026-09-18, ciclo de Programador: tercera reconfirmación tras R-18 y la auditoría en profundidad,
  sin novedad de código. Cuatro redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`:
  `#24` (baja, de proceso).
- 2026-09-18, ciclo de Programador: segunda reconfirmación tras R-18 y la auditoría en profundidad,
  sin novedad de código. Cuatro redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`:
  `#24` (baja, de proceso).
- 2026-09-18, ciclo de Programador: primera reconfirmación tras R-18 y la auditoría en profundidad,
  sin novedad de código. Cuatro redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`:
  `#24` (baja, de proceso).
- 2026-09-18, ciclo de Auditoría: revisión en profundidad de R-18 ya implementada (integración de
  tomas reales en el selector T-30); cero hallazgos nuevos. Único `ABIERTO`: `#24` (baja, de
  proceso), reconfirmado sin que el patrón que lo motivó se repita una tercera vez.
- 2026-09-17, ciclo de Product Manager: archiva la Oleada v7 (R-18) a `ROADMAP_HISTORICO.md` y
  corrige la prosa de "Cola de producto" de `ROADMAP_PRODUCTO.md`. Cola de producto queda vacía.
- 2026-09-17, ciclo de Programador: novena reconfirmación tras R-18, sin novedad de código. Cuatro
  redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`: `#24` (baja, de proceso).
- 2026-09-17, ciclo de Programador: octava reconfirmación tras R-18, sin novedad de código. Cuatro
  redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`: `#24` (baja, de proceso).
- 2026-09-17, ciclo de Programador: séptima reconfirmación tras R-18, sin novedad de código. Cuatro
  redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`: `#24` (baja, de proceso).
- 2026-09-17, ciclo de Programador: sexta reconfirmación tras R-18, sin novedad de código. Cuatro
  redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`: `#24` (baja, de proceso).
- 2026-09-17, ciclo de Programador: quinta reconfirmación tras R-18, sin novedad de código. Cuatro
  redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`: `#24` (baja, de proceso).
- 2026-09-17, ciclo de Programador: cuarta reconfirmación tras R-18, sin novedad de código. Cuatro
  redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`: `#24` (baja, de proceso).
- 2026-09-17, ciclo de Programador: tercera reconfirmación tras R-18, sin novedad de código. Cuatro
  redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`: `#24` (baja, de proceso).
- 2026-09-17, ciclo de Programador: segunda reconfirmación tras R-18, sin novedad de código. Cuatro
  redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`: `#24` (baja, de proceso).
- 2026-09-17, ciclo de Programador: primera reconfirmación tras R-18, sin novedad de código. Cuatro
  redes en verde (583 tests). Único `ABIERTO` de `auditoriacontinua.md`: `#24` (baja, de proceso).
- 2026-09-17, ciclo de Programador: R-18 implementada y COMPLETADA. `scripts/salidas.py` (T-30) gana
  `tomas_por_escena` opcional en `generar_salidas_seleccionadas`: con al menos una toma `buena`,
  `SRT` genera también `guion-alineado.srt` (R-05) y `PPTX` pasa las tomas a `exportar_pptx` para
  duración real y límites absolutos reales (R-13/R-16); `TipoSalida` gana `CAPITULOS_YOUTUBE`
  (quinta opción, R-07). Sin toma registrada, comportamiento idéntico a antes de R-18 (regresión
  byte a byte verificada). 8 tests nuevos (575→583). Cuatro redes en verde. `DEVELOPERS.md` y
  `SKILL.md` actualizados. Auditoría reconfirma `#24` (baja, de proceso) como único `ABIERTO`.
- 2026-09-16, ciclo de Product Manager: abre R-18 (oleada v7 nueva), origen en una grieta de
  arquitectura verificada por el PM releyendo `scripts/salidas.py` junto con los contratos de
  montaje: las salidas basadas en tomas reales (R-05/R-07/R-13/R-16) estaban completas y probadas
  pero nunca llegaban al selector real de T-30. Auditoría del mismo día cierra `#19` y abre `#24`
  (enrutado a la pregunta #11 de §6).
- 2026-09-16, ciclo de Programador: decimonovena reconfirmación tras R-17, sin novedad de código.
  Cuatro redes en verde (575 tests). Auditoría del mismo día cierra `#19` y abre `#24`.
- 2026-09-16, ciclo de Programador: decimoctava reconfirmación tras R-17, sin novedad de código.
- 2026-09-16, ciclo de Programador: decimoséptima reconfirmación tras R-17, sin novedad de código.
- 2026-09-16, ciclo de Programador: decimosexta reconfirmación tras R-17, sin novedad de código.
- 2026-09-16, ciclo de Programador: decimoquinta reconfirmación tras R-17, sin novedad de código.
- 2026-09-16, ciclo de Programador: decimocuarta reconfirmación tras R-17, sin novedad de código.
- 2026-09-16, ciclo de Programador: decimotercera reconfirmación tras R-17, sin novedad de código.
- 2026-09-16, ciclo de Programador: duodécima reconfirmación tras R-17, sin novedad de código.
- 2026-09-16, ciclo de Programador: undécima reconfirmación tras R-17, sin novedad de código.
- 2026-09-16, ciclo de Programador: décima reconfirmación tras R-17, sin novedad de código.
- 2026-09-16, ciclo de Auditoría: cierra `#19` (R-17 verificada en profundidad), abre `#24` (patrón
  recurrente de latencia PM/roadmap, confirmado).
- 2026-09-15, ciclo de Product Manager: prosa de "Cola de producto" corregida (R-17 ya `COMPLETADA`,
  no pendiente) y Fase transversal F-I archivada.
- 2026-09-15, ciclo de Programador: novena reconfirmación tras R-17, sin novedad. Cuatro redes en
  verde (575 tests). Sin trabajo de código pendiente.
- 2026-09-15, ciclo de Programador: octava reconfirmación tras R-17, sin novedad. Cuatro redes en
  verde (575 tests). Sin trabajo de código pendiente.
- 2026-09-15, ciclo de Programador: séptima reconfirmación tras R-17, sin novedad. Cuatro redes en
  verde (575 tests). Sin trabajo de código pendiente. Nota de arranque: clon local en *detached
  HEAD* con rama rezagada, resuelto con `git reset --hard origin/develop` (sin pérdida de historia
  real, verificado con `merge-base --is-ancestor`).
- 2026-09-15, ciclo de Programador: sexta reconfirmación tras R-17, sin novedad. Cuatro redes en
  verde (575 tests). Sin trabajo de código pendiente.
- 2026-09-15, ciclo de Programador: quinta reconfirmación tras R-17, sin novedad. Cuatro redes en
  verde (575 tests). Sin trabajo de código pendiente.
- 2026-09-15, ciclo de Programador: cuarta reconfirmación tras R-17, sin novedad. Cuatro redes en
  verde (575 tests). Sin trabajo de código pendiente.
- 2026-09-15, ciclo de Programador: tercera reconfirmación tras R-17, sin novedad. Cuatro redes en
  verde (575 tests). Sin trabajo de código pendiente.
- 2026-09-15, ciclo de Programador: segunda reconfirmación tras R-17, sin novedad. Cuatro redes en
  verde (575 tests). Sin trabajo de código pendiente.
- 2026-09-15, ciclo de Programador: primera reconfirmación tras R-17, sin novedad. Cuatro redes en
  verde (575 tests). Sin trabajo de código pendiente.
- 2026-09-15, ciclo de Programador: R-17 implementada y COMPLETADA. Investigado el hallazgo #19
  (`_incidencias_anclas_desajustadas` compara solo cardinalidad de anclas, no identidad exacta):
  bajo operación normal la identidad es inyectiva por construcción; el único camino para que la
  comparación no dispare exige corromper `estado.validacion["particiones_pospuestas"]` a mano entre
  pasadas (misma precondición de P-04), y se verificó con test nuevo que incluso ahí el invariante
  (a) de §0.2 sigue intacto (efecto cosmético único). 1 test nuevo (574→575). Cuatro redes en verde.
- 2026-09-14, ciclo de Product Manager: `ROADMAP_PRODUCTO.md` §"Cola de producto" corregida (ya no
  repite la prosa desactualizada del 2026-09-13); R-15 y R-16 confirmadas `COMPLETADA`, Fase F-H y
  Oleada v6 archivadas en `ROADMAP_HISTORICO.md`. Abre **R-17** (fase F-I nueva) a partir del
  hallazgo `#19` (diez pasadas de reconfirmación del auditor sin que nadie lo convirtiera en tarea).
- 2026-09-14, ciclo de Programador: octava reconfirmación del día, sin novedad tras R-16. Cuatro
  redes en verde (574 tests). Sin trabajo de código pendiente.
- 2026-09-14, ciclo de Programador: séptima reconfirmación del día, sin novedad tras R-16. Cuatro
  redes en verde (574 tests). Sin trabajo de código pendiente.
- 2026-09-14, ciclo de Programador: sexta reconfirmación del día, sin novedad tras R-16. Cuatro
  redes en verde (574 tests). Sin trabajo de código pendiente.
- 2026-09-14, ciclo de Programador: quinta reconfirmación del día, sin novedad tras R-16. Cuatro
  redes en verde (574 tests). Sin trabajo de código pendiente.
- 2026-09-14, ciclo de Programador: cuarta reconfirmación del día, sin novedad tras R-16. Cuatro
  redes en verde (574 tests). Sin trabajo de código pendiente.
- 2026-09-14, ciclo de Programador: tercera reconfirmación del día, sin novedad tras R-16. Cuatro
  redes en verde (574 tests). Sin trabajo de código pendiente.
- 2026-09-14, ciclo de Programador: segunda reconfirmación del día, sin novedad tras R-16. Cuatro
  redes en verde (574 tests). Sin trabajo de código pendiente.
- 2026-09-14, ciclo de Programador: primera reconfirmación del día, sin novedad tras R-16. Cuatro
  redes en verde (574 tests). Sin trabajo de código pendiente.
- 2026-09-14, ciclo de Programador: R-16 implementada y COMPLETADA.
`Tarjeta` (`scripts/pptx.py`) gana `inicio_segundos`/`fin_segundos` por escena, calculados una sola
vez (`_con_limites_absolutos`) acumulando en el orden de las escenas con la misma regla real-vs-
estimada que ya elige `duracion_real_segundos` (R-13); `references/contrato-tarjetas.md` documenta
las dos claves nuevas (aditivo, `version_contrato` no sube) y `references/contrato-montaje.md` deja
de pedirle a la cadena de montaje que sume las duraciones a mano — ahora lee los dos campos
directamente, con la fórmula de acumulación como transparencia, no como instrucción. 5 tests nuevos
(569→574): 2 unitarios en `test_pptx.py` (sin toma buena acumula la estimada sin huecos; con toma
buena usa la real) y 3 de integración en `test_integracion_montaje.py` (primera escena empieza en
`0` y no hay hueco/solape entre escenas sobre los tres guiones reales; el `fin_segundos` de la
última escena coincide con el fin de `guion.srt` sin parte de rodaje y con el de
`guion-alineado.srt` con parte de rodaje mezclando real/estimado). Cuatro redes en verde (`mypy`
limpio 68 archivos, `ruff` limpio, 574 tests, `verificar_salidas.py --fixture` catorce etapas en
OK; `.pptx`/`.pdf` reales LATENTES como siempre en este contenedor de nube). `DEVELOPERS.md` y
`SKILL.md` actualizados con la nueva sección/mención. Con R-16 completada, la cola de
`ROADMAP_PRODUCTO.md` vuelve a quedar vacía — la siguiente sesión de Programador no tiene tarea de
código pendiente salvo que el PM abra una nueva o el auditor escale un hallazgo. Sin cambios en
bloqueos ni preguntas abiertas; ninguna desviación respecto a la especificación de R-16.
- 2026-09-14, ciclo de Programador: R-15 implementada y COMPLETADA. `DEVELOPERS.md` gana un bloque
  de cita bajo "Verificación manual" advirtiendo explícitamente contra invocar `ruff`/`mypy`/
  `pytest` pelados en un contenedor de nube (un segundo juego preinstalado más nuevo que el
  pineado, por delante en el `PATH`, con señal distinta y falsos `import-not-found` de `mypy`);
  `SKILL.md` gana la misma advertencia en una frase con remisión. Tarea puramente documental: cero
  cambio en `scripts/`, `tests/` ni `assets/`. Cuatro redes en verde (569 tests).
- 2026-09-13, ciclo de Product Manager: abre R-16 (oleada v6 nueva), origen en una inconsistencia de
  arquitectura del contrato de montaje verificada por el PM (no un hallazgo del auditor):
  `references/contrato-montaje.md` obligaba a la cadena de montaje a reimplementar a mano la
  fórmula de acumulación de duraciones; R-16 añade `inicio_segundos`/`fin_segundos` ya resueltos a
  `tarjetas.json` (mismo patrón que R-13). Solo especificación, no se programa desde ese ciclo.
- 2026-09-12, ciclo de Product Manager: abre R-15 (fase transversal F-H nueva), origen `auditoría
  #22` (media) — un segundo juego de `ruff`/`mypy`/`pytest` preinstalado en el contenedor de nube da
  señal distinta y engañosa a quien lo invoque pelado; R-15 es puramente documental. `#19`
  reconfirmado sin cambios.
- 2026-09-11, ciclo de Product Manager: archiva la Oleada v5 (R-13) y la Fase transversal F-G
  (R-14) — ambas ya `COMPLETADA` por el Programador el mismo día — a `ROADMAP_HISTORICO.md`. Cola de
  `ROADMAP_PRODUCTO.md` quedó vacía en ese ciclo (20/21 hallazgos `RESUELTO`, `roadmap/FEEDBACK.md`
  sin entradas `nuevo`).
- 2026-09-11, ciclo de Programador: octava reconfirmación del día, sin novedad. Cuatro redes en
  verde (569 tests). Sin trabajo de código pendiente tras R-14.
- 2026-09-11, ciclo de Programador: séptima reconfirmación del día, sin novedad. Cuatro redes en
  verde (569 tests). Sin trabajo de código pendiente tras R-14.
- 2026-09-11, ciclo de Programador: sexta reconfirmación del día, sin novedad. Cuatro redes en
  verde (569 tests). Sin trabajo de código pendiente tras R-14.
- 2026-09-11, ciclo de Programador: quinta reconfirmación del día, sin novedad. Cuatro redes en
  verde (569 tests). Sin trabajo de código pendiente tras R-14.
- 2026-09-11, ciclo de Programador: cuarta reconfirmación del día, sin novedad. Cuatro redes en
  verde (569 tests). Sin trabajo de código pendiente tras R-14.
- 2026-09-11, ciclo de Programador: tercera reconfirmación del día, sin novedad. Cuatro redes en
  verde (569 tests). Sin trabajo de código pendiente tras R-14.
- 2026-09-11, ciclo de Programador: segunda reconfirmación del día, sin novedad. Cuatro redes en
  verde (569 tests). Sin trabajo de código pendiente tras R-14.
- 2026-09-11, ciclo de Programador: primera reconfirmación del día, sin novedad. Cuatro redes en
  verde (569 tests). Sin trabajo de código pendiente tras R-14.
- 2026-09-11, ciclo de Programador: R-14 implementada y COMPLETADA. `scripts/clasificador.py`
  extrae el separador `---` de fin de escena a su propio bloque `no_locucion` en vez de dejarlo
  pegado al `contenido` de la última indicación de la escena. 5 tests nuevos (564→569). Cuatro redes
  en verde. Era la última R-XX de la cola.
- 2026-09-11, ciclo de Programador: R-13 implementada y COMPLETADA. `scripts/pptx.py` incorpora
  `duracion_real_segundos` por escena en `tarjetas.json` y `mezcla_duracion_real_y_estimada` de
  cabecera, coherente con `guion-alineado.srt`. 7 tests nuevos (557→564). Cuatro redes en verde.
- 2026-09-10, ciclo de Product Manager: archiva la oleada v4 entera (R-12, ya COMPLETADA) a
  `ROADMAP_HISTORICO.md` y abre **R-13** y **R-14** (fase transversal F-G), ambas sobre huecos ya
  verificados en el código. Reconfirmado: `auditoriacontinua.md` sin ningún hallazgo `ABIERTO` de
  severidad alta.
- 2026-09-10, ciclo de Programador (décimo del día): sin tarea de código pendiente ni novedad que
  reportar. §1 sin ninguna T-XX/R-XX PENDIENTE tras R-12 (ya COMPLETADA); solo T-24b BLOQUEADA por
  hardware del dueño. Cuatro redes en verde (`mypy` limpio, `ruff` limpio, 557 tests, `verificar_
  salidas.py --fixture` catorce etapas OK; `.pptx`/`.pdf` LATENTES como siempre en este contenedor).
- 2026-09-10, sexto ciclo: bloqueo #8 corregido de `ABIERTO` a `RESUELTO` en §3. `list_triggers`
  trae `git_repository.url` y el prompt completo de cada rutina — datos que ninguna reconfirmación
  anterior había leído. El trío "sin sufijo" (`Auditor`/`Product manager`/`Programador`) apunta a
  `https://github.com/JanoSolerDiaz/centro-estudios-sw` (proyecto `GestorAcademia` del dueño, no
  teleprompter) y sus cron no coinciden con los de `-teleprompter`. Ninguna rutina de *este*
  proyecto está duplicada. `auditoriacontinua.md` #19 (baja) y #20 (media) reconfirmados sin
  cambios; #20 queda desactualizado por esta corrección pero es de escritura exclusiva del Auditor.

---

> ## ⚑ PARA EL DUEÑO — empieza por aquí
> Lo único que el proyecto necesita de ti está en dos sitios de este documento:
> - **§3 Bloqueos** = tu lista de tareas. **El #8 (rutinas "duplicadas") era una falsa alarma: corregido hoy (2026-09-10).** Ninguna sesión anterior había comparado el repositorio real de cada rutina, solo el nombre; el trío sin sufijo (`Auditor`/`Product manager`/`Programador`) resulta pertenecer a otro proyecto tuyo (`centro-estudios-sw`/GestorAcademia), no a teleprompter — su prompt lo dice explícitamente. Las tres rutinas de *este* proyecto (`auditor-teleprompter`, `product-manager-teleprompter`, `programador-teleprompter`) están cada una sola, sin solape: no hay coste doble que resolver aquí. Si quieres, revisa por tu cuenta si el trío de `centro-estudios-sw` tiene un problema similar, pero eso es asunto de ese otro repositorio. Los tres bloqueos que quedan siguen **sin urgencia** (aportar el paquete de `480-branded-pptx` cuando lo tengas, probar el clicker Bluetooth real contra el mapa de teclas ya implementado en T-24 cuando lo consigas, y grabar un curso completo con la skill instalada, que es lo que arrancaría el primer feedback real de rodaje) — **ninguno frena el desarrollo**. La instalación de la skill (T-32) ya la hiciste y quedó resuelta.
> - **§6 Preguntas abiertas** = tus decisiones. **Una pendiente: la #11** (2026-09-16, sin urgencia)
>   — si el ciclo de reconfirmación del Programador puede corregir por sí solo la prosa de "Cola de
>   producto" cuando solo refleja un estado que §1 ya registra como `COMPLETADA`. Las otras diez ya
>   están resueltas.
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
| T-22 | Autoscroll con bloque centrado | **COMPLETADA** | 2026-09-02 | `assets/reproductor/guion.js`: `centrarBloqueActivo` mueve `window.scrollY` con interpolacion propia (`requestAnimationFrame`, cancelable) para mantener el bloque activo centrado; corrige de paso un bug real de T-19 (foco diferido que deshacia el centrado) con `focus({preventScroll:true})` |
| T-23 | Ayudas de grabación | **COMPLETADA** | 2026-09-02 | `assets/reproductor/guion.js`: cuenta atrás 3-2-1 desactivable, cronómetro de la toma (deriva estructuralmente nula), barra de progreso por bloques (100% exacto en el último), indicadores ocultables con `H` |
| T-24 | Atajos y clicker Bluetooth | **COMPLETADA** | 2026-09-02 | Mapa completo configurable (`mapa_teclas_reproductor`), antirrebote y ayuda `?`. La verificación del clicker físico **no forma parte de esta tarea**: sale a T-24b por decisión del dueño (§6.9) y sigue en el bloqueo #5 de §3 |
| T-24b | Calibración del clicker Bluetooth real | **BLOQUEADA** — el dueño no dispone de clicker (2026-09-02) | — | Spec: T-24 requisito 2, mitad de verificación física. **El programador no la toca.** Cuando el dueño avise, se resuelve cambiando `Configuracion.mapa_teclas_reproductor`, sin tocar `guion.js`. Ver bloqueo §3.5 |
| T-25 | Modo espejo | **COMPLETADA** | 2026-09-02 | Volteo horizontal (`transform: scaleX(-1)`) de `.escena`, activable con `M`/`m` y con un boton en la cabecera; `Configuracion.espejo_incluye_indicadores` decide si tambien voltea los indicadores. Persistencia minima adelantada de T-26 solo para este ajuste (`claveAlmacenamiento`/`leerPreferencia`/`guardarPreferencia`), que T-26 reutilizara para el resto de preferencias |
| T-26 | Persistencia local de preferencias | **COMPLETADA** | 2026-09-02 | `localStorage` (clave por guion, `try/catch`) para tamaño de texto, velocidad por escena (clave por numero de escena), última escena vista (por `inicio_segundos`, no por índice) e indicadores. Botón "Continuar" en el índice (no auto-lanzamiento: `requestFullscreen` exige gesto de usuario) y "Restablecer preferencias" en la ayuda |
| T-27 | Exportador `.srt` borrador | **COMPLETADA** | 2026-09-02 | `scripts/srt.py`: un subtítulo por bloque de respiración (agrupable si es muy corto, sin cruzar fin de escena), texto locutado final (reescrituras aceptadas incluidas), partición limpia cuando no cabe en el límite de líneas/caracteres, validado con las mismas reglas que ffmpeg |
| T-28 | Exportador `.pdf` con marca 480 | **COMPLETADA** | 2026-09-02 | `scripts/pdf.py`: HTML de impresion (una escena por pagina + portada) con la identidad 480, logotipo incrustado con ratio medido del PNG, conversion con Chrome/Edge headless si esta disponible (nunca falla si no lo esta), modo `--para-terceros` via `incluir_notas_internas` |
| T-29 | Adaptador `.pptx` (`480-branded-pptx`) | **COMPLETADA** | 2026-09-02 | `scripts/pptx.py`: `tarjetas.json` + `brief-pptx.md`; la delegación la hace Claude, no el código. Con la skill de marca ausente (esta máquina) ambos se generan igual y la salida `.pptx` queda latente, tal como preveía su requisito 4 |
| T-30 | Selector de salidas por validación | **COMPLETADA** | 2026-09-02 | `scripts/salidas.py`: pregunta de opción múltiple como datos (`construir_pregunta_salidas`, la formula Claude, no un `input()`), sugerencia desde `estado.salidas_generadas` (sin migración), generación independiente por salida con `try`/`except`, `ResumenSalidas` con generadas/omitidas/latentes |
| T-31 | `SKILL.md` y configuración completa | **COMPLETADA** | 2026-09-02 | Tabla completa de los 81 campos de `Configuracion` en `SKILL.md`, verificada por `tests/test_skill_md.py` (compara claves en las dos direcciones); precedencia documentada; tres referencias nuevas en `references/` (convención de guion, formato de `guion-escenas.md`, mapa de teclas) |
| T-32 | Instalación de la skill y guión de ejemplo | **COMPLETADA** | 2026-09-03 | Desbloqueada: el dueño ejecutó `python scripts/instalar_skill.py` en su máquina (`~/.claude/skills/teleprompter/`) y el health check desde la copia instalada dio **11/11 etapas OK**. Bloqueo #6 de §3 RESUELTO. **Ojo:** la copia instalada quedó hecha ANTES de traer P-03/R-01 del remoto, así que hay que reinstalar para que incorpore ambos |
| T-33 | Encaje con la cadena de montaje | **COMPLETADA** | 2026-09-02 | `references/contrato-montaje.md`: contrato `.srt` + `tarjetas.json`, estructura de carpetas y formula para derivar el rango de tiempo de cada escena; numeracion de escena duplicada/no creciente ahora señalada como desviacion (`convencion.py`); `tests/test_integracion_montaje.py` valida ambas salidas juntas sobre los tres guiones reales |
| R-01 | Persistencia verificada + plan B | **COMPLETADA** | 2026-09-03 | Comprobación real (`try`+relectura al cargar, mas verificacion con Playwright/Chromium real: mismo perfil persiste, perfil nuevo no); aviso honesto si falla; exportar/importar preferencias como `.json` (lee de memoria, no de `localStorage`). Oleada v2 · `origen: auditoría #5` |
| R-02 | Registro de tomas por escena | **COMPLETADA** | 2026-09-03 | Índice = parte de rodaje real: tomas/duración real/toma buena por escena, nota rápida sin salir de grabación, exportación a `.json` fusionada en `estado.json` (migración 002). Oleada v2 · parte de rodaje |
| R-03 | Marcar tropiezos durante la toma | **COMPLETADA** | 2026-09-03 | Tecla `T` marca/desmarca el bloque en pantalla (`alternarTropiezoBloqueActual`); exportación `.json` fusionada por `scripts/feedback.py` en `FEEDBACK.md` (carpeta de salida del guion, no `roadmap/FEEDBACK.md`); destacado en la siguiente revisión por texto exacto. Sin migración, tal como pedía la ficha |
| R-04 | Recalibrar el ritmo con tiempos reales | **COMPLETADA** | 2026-09-03 | `scripts/calibracion.py`: contraste estimada/objetivo/real por escena (real = toma buena de R-02), tipo posicional (apertura/desarrollo/cierre), ppm calibrado propuesto con evidencia de ≥2 guiones (nunca aplicado solo), informe por tipo de escena. Sin migración |
| R-05 | `.srt` alineado con la toma buena | **COMPLETADA** | 2026-09-03 | `scripts/srt_alineado.py`: reescala cada escena a la duración real de su toma buena (mismo factor a palabras y pausa), conserva estimada la escena sin toma buena; `.srt` estimado y alineado en archivos independientes; misma validación estricta de T-27. Sin migración |
| R-06 | Coherencia de nombres y `assets/` | **COMPLETADA** | 2026-09-03 | Sufijo `-tarjetas` → `-teleprompter` (`config.NOMBRE_SUFIJO_CARPETA_SALIDA`); migración automática de carpetas heredadas en `entrada._migrar_carpeta_salida_heredada` (fuera de `scripts/migraciones/`, ver `DECISIONES_TECNICAS.md`); logotipos movidos a `assets/marca/`. Sin migración de `estado.json` |
| R-07 | Capítulos de YouTube con marcas de tiempo reales | **COMPLETADA** | 2026-09-03 | `scripts/capitulos_youtube.py`: empareja títulos de `Capítulos` (T-08) con escenas por orden, tiempo real de la toma buena (R-02) o estimado de T-12 con aviso explícito si se mezclan, formato exacto de YouTube (marca mínima 10 s). Sin migración |
| R-08 | Deuda técnica menor (colores de estado, `PROYECTO.md`, versión de Python) | **COMPLETADA** | 2026-09-03 | `color_estado_grabada_reproductor`/`color_estado_revisada_reproductor` en `Configuracion`; `PROYECTO.md` coincide con §0.2 (ritmo deducido, 120 ppm solo respaldo); `pyproject.toml` mantiene 3.12 como objetivo declarado, `ci.avisar_si_version_python_diverge` avisa (no bloquea) del desajuste con el intérprete real. Fase F-D · `origen: auditoría #10, #11, #12` |
| R-09 | Endurecer el validador de auto-contención | **COMPLETADA** | 2026-09-03 | Seis patrones nuevos en `PATRONES_RECURSO_EXTERNO` (`<object>`, `<embed src>`, `<base href>`, `WebSocket`, `EventSource`/`sendBeacon`, `url(...)` de CSS fuera de `@import`), excepción `data:` donde aplica; lista completa documentada en `references/validador-autocontencion.md`. Fase F-D · `origen: auditoría #13` |
| R-10 | Robustez multiplataforma detectada al correr en Windows por primera vez | **COMPLETADA** | 2026-09-04 | `entrada.leer_guion` normaliza `\r\n`/`\r` a `\n` tras decodificar (hallazgo real); `test_nombre_guion_seguro_nunca_vacio` diagnosticado sin cambio de código (`PureWindowsPath`/`PurePosixPath` parten `"....md"` igual); `test_instalar_hook_...` pasa a `skipif` no-POSIX; los doce `write_text` de `scripts/` fijan `newline="\n"` (requisito 4, hallazgo real de la comprobación). Fase F-E · `origen: hallazgo de sesión (no de auditoría)` |
| R-11 | Robustez de datos derivados del rodaje (toma buena ambigua, capítulos sobrantes, cobertura cruzada) | **COMPLETADA** | 2026-09-04 | `tomas.duracion_toma_buena` rechaza con `RegistroTomasError` más de una toma `buena` por escena (#16); `capitulos_youtube.calcular_capitulos` expone `titulos_sobrantes` cuando hay más títulos que escenas (#17); nuevo test de coherencia cruzada `.srt` alineado/capítulos de YouTube en `tests/test_integracion_montaje.py` (#18). Fase F-F · `origen: auditoría #16, #17, #18` |
| R-12 | Cue discreta de indicaciones EN PANTALLA/NOTA en el reproductor | **COMPLETADA** | 2026-09-10 | `reproductor._indicaciones_ancladas_por_indice` ancla cada indicación al ÚLTIMO bloque de respiración que la precede (sin bloque precedente, al primero — requisito 4), reutilizando tal cual la clasificación de T-09 y el filtro pantalla/nota de T-28/T-29 (`pdf.indicaciones_no_recitables`/`es_nota_interna`). `guion.js`/`estilo.css`: cue subordinada (`.cue-indicacion`, visible solo bajo `.bloque--activo`), plegada con el resto de indicadores en `H` (T-23), sin atajo nuevo. Prefijos `Pantalla:`/`Nota:` configurables. 7 tests nuevos (550→557); verificado también visualmente con Playwright/Chromium real. Oleada v4 · `origen: observación de arquitectura del PM (2026-09-08)` |
| R-13 | Duración real por escena en `tarjetas.json`, coherente con `guion-alineado.srt` | **COMPLETADA** | 2026-09-11 | `scripts/pptx.py`: `Tarjeta.duracion_real_segundos` (`None` si la escena no tiene toma buena, `tomas.duracion_toma_buena` reutilizada tal cual) y `ResultadoTarjetas.mezcla_duracion_real_y_estimada` (booleano de cabecera, `true` solo si el conjunto mezcla ambos casos); `duracion_estimada_segundos` intacta (requisito 2). `generar_tarjetas`/`exportar_pptx` ganan `tomas_por_escena` opcional (mismo patrón que `srt_alineado.py`/`capitulos_youtube.py`, no integrado en el selector automático de T-30); sin él, comportamiento idéntico a antes de R-13. `references/contrato-tarjetas.md` y `contrato-montaje.md` actualizados con la fórmula de rango correcta. 7 tests nuevos (557→564), incluido el cruce con `guion-alineado.srt` en `test_integracion_montaje.py`. Oleada v5 · `origen: observación de arquitectura del PM (2026-09-10)` |
| R-14 | El separador de escena no debe colarse en el texto de una indicación | **COMPLETADA** | 2026-09-11 | `scripts/clasificador.py`: `_separar_marcador_fin_escena` extrae el `---` de fin de escena (con las líneas en blanco que lo acompañan) en su propio bloque `no_locucion` (`senal="separador_escena"`) antes de clasificar rótulos/inferencia, en vez de dejarlo pegado al `contenido` de la última indicación. Nueva señal añadida a los tres sitios que la necesitan para no colarse como una "indicación" propia ni proponerse como convención: `pdf._SENALES_ESTRUCTURALES`, `documento_revision._SENALES_ESTRUCTURALES` y `convencion._SENALES_CONTRACTUALES`. `references/convencion-guion.md` documenta ahora el separador (requisito 1). Fixture golden `fixtures/guion-ejemplo-esperado.md` regenerado a mano (cambio esperado y verificado línea a línea). 5 tests nuevos (564→569). Verificado sobre los tres guiones reales: cero indicación termina en `---` en `guion-escenas.md`, `tarjetas.json` ni la cue del reproductor; reconstrucción íntegra (invariante (a)) intacta. Fase F-G · `origen: observación de arquitectura de R-12 (2026-09-10)` |
| R-15 | Advertir explícitamente contra el binario "pelado" de `ruff`/`mypy`/`pytest` en un contenedor de nube | **COMPLETADA** | 2026-09-14 | Tarea puramente documental: nota visible en `DEVELOPERS.md` (bloque de cita bajo "Verificación manual") y frase con remisión en la sección "Verificacion" de `SKILL.md`, explicando que la única verificación válida es `python scripts/ci.py` / `python -m <herramienta>`, nunca el binario pelado. Cero cambio en `scripts/`, `tests/` o `assets/`; cuatro redes en verde (569 tests). `origen: auditoría #22` — queda para la siguiente pasada del auditor cerrar `#22` a `RESUELTO` |
| R-16 | Límites absolutos de escena (`inicio_segundos`/`fin_segundos`) en `tarjetas.json` | **COMPLETADA** | 2026-09-14 | `Tarjeta` (`scripts/pptx.py`) gana los dos campos, calculados una sola vez (`_con_limites_absolutos`) con la misma regla real/estimada de R-13, acumulando en el orden de las escenas; `contrato-tarjetas.md` documenta las dos claves y `contrato-montaje.md` deja de pedirle a la cadena de montaje que sume las duraciones a mano — ahora las lee directamente. Cambio aditivo, `version_contrato` no sube, sin migración de `estado.json` ni campo nuevo de `Configuracion`. 5 tests nuevos (569→574): 2 unitarios (`test_pptx.py`) y 3 de integración (`test_integracion_montaje.py`, incluida la coherencia con `guion.srt`/`guion-alineado.srt`). Cuatro redes en verde. `origen: observación de arquitectura del PM (2026-09-13)` |
| R-17 | Endurecer o cerrar formalmente la asimetría teórica de `_incidencias_anclas_desajustadas` (`scripts/revalidacion.py`) | **COMPLETADA** | 2026-09-15 | Spec completa en `ROADMAP_PRODUCTO.md` §Fase F-I. `origen: auditoría #19` (abierto 2026-09-04, reconfirmado sin cambios en diez pasadas sucesivas del auditor). Investigada y cerrada por la vía del requisito 3 (con matiz): bajo operación normal la identidad es inyectiva por construcción (`pospuestas_previas` siempre coincide con lo que la pasada anterior persistió); el único escenario que rompe la comparación por cardinalidad exige corromper `estado.validacion["particiones_pospuestas"]` a mano (misma precondición ya conocida de P-04), y se verificó con test nuevo que incluso ahí el invariante (a) — nada se pierde ni se duplica — sigue intacto, con un único efecto cosmético (número de bloque erróneo en la incidencia de conflicto, escena correcta). 1 test nuevo (574→575) en `tests/test_revalidacion.py`. Cuatro redes en verde. Detalle completo en `DECISIONES_TECNICAS.md` |
| R-18 | Integrar en el selector de salidas (T-30, `scripts/salidas.py`) las salidas que dependen de tomas reales: `guion-alineado.srt` (R-05), `capitulos-youtube.txt` (R-07, hoy ni siquiera seleccionable) y los campos reales de `tarjetas.json` (R-13/R-16) | **COMPLETADA** | 2026-09-17 | `scripts/salidas.py`: `generar_salidas_seleccionadas` gana `tomas_por_escena` opcional (`EstadoProyecto.tomas` tal cual); con al menos una toma `buena`, `SRT` genera también `guion-alineado.srt` (R-05) bajo el mismo `TipoSalida.SRT`, y `PPTX` pasa las tomas a `exportar_pptx` para duración real/límites absolutos (R-13/R-16). `TipoSalida` gana `CAPITULOS_YOUTUBE` (quinta opción), generado con `capitulos_youtube.generar_capitulos_youtube`; sin sección `Capítulos`, queda `SalidaOmitida` con el motivo exacto, nunca fallo ni latente. `verificar_salidas.py::verificar_generacion` distingue ahora un fallo real (prefijo `"fallo al generar:"`) de esa omisión esperada. Sin tomas, comportamiento idéntico al de antes de R-18 (test de regresión byte a byte sobre los tres guiones reales). 8 tests nuevos (575→583). Cuatro redes en verde. Detalle completo en `DEVELOPERS.md` y `DECISIONES_TECNICAS.md` |
| R-19 | Enlazar la toma buena de cada escena con su archivo de vídeo real (campo opcional tecleado en el reproductor) y generar `concat-ffmpeg.txt`, la lista de concatenación lista para `ffmpeg -f concat` | **COMPLETADA** | 2026-09-30 | `Toma.archivo_video` (opcional, `""` por defecto) anotable con `V`/`v` durante la grabación o editable después desde el índice sin volver a grabar; `references/contrato-tomas.md` sube a versión 2 (aditivo, sin migración). `scripts/concat_ffmpeg.py` nuevo: reutiliza `tomas.toma_buena` (extraída de `duracion_toma_buena`, misma regla de exclusividad de R-11/#16) para generar `file '<archivo_video>'` o `# ESCENA N: <motivo>` por escena, en su orden real. `TipoSalida.CONCAT_FFMPEG` (sexta opción de T-30): omitida sin ningún parte de rodaje, nunca falla por escenas pendientes de anotar. 23 tests nuevos (583→606). Cuatro redes en verde, incluidas dos etapas nuevas en `verificar_salidas.py --fixture` (dieciséis en total). Verificado además con Playwright/Chromium real: anotar durante la grabación, editar desde el índice sin regrabar, exportar el parte de rodaje y generar `concat-ffmpeg.txt` con una ruta con comilla simple correctamente escapada. `DEVELOPERS.md`, `SKILL.md` y las referencias de `contrato-tomas.md`/`contrato-montaje.md`/`mapa-teclas.md` actualizados. Oleada v8, archivada en `ROADMAP_HISTORICO.md` en el ciclo de PM del 2026-09-30, junto con la nota de gobernanza sobre cómo se justificó su apertura (`auditoriacontinua.md` #26) |
| R-20 | Anclar cada indicación `EN PANTALLA`/`NOTA` de `tarjetas.json` a un instante estimado dentro de la escena (`indicaciones_ancladas`, campo aditivo), reutilizando el anclaje que R-12 ya calcula para la cue en vivo del reproductor | **COMPLETADA** | 2026-10-01 | `reproductor.py::_indicaciones_ancladas_por_indice` (R-12) se divide: el anclaje se extrae a la función pública `anclar_indicaciones_a_bloques` (mismo patrón que `tomas.toma_buena` en R-19), reutilizada tal cual por `pptx.py`. `Tarjeta` gana `indicaciones_ancladas` (dataclass `IndicacionAnclada`: `texto`/`es_nota_interna`/`instante_estimado_segundos`), mismo conjunto que `indicaciones_pantalla`+`notas_internas`, calculado relativo a la escena y convertido a absoluto en `_con_limites_absolutos` (R-16, mismo acumulado que `inicio_segundos`/`fin_segundos`). Escena sin bloques de locución (sin ejemplo real, contemplada por `validar_tarjetas`): ancla al inicio de la escena. `--para-terceros` omite notas internas también aquí. Cambio aditivo, `version_contrato` no sube, sin migración. 7 tests nuevos (606→613), incluido uno que compara el instante exacto contra la cue del reproductor para el mismo guion (sin toma real: acumulados idénticos bit a bit). Cuatro redes en verde. `references/contrato-tarjetas.md`/`contrato-montaje.md`, `DEVELOPERS.md` y `SKILL.md` actualizados |
| R-21 | Validar `concat-ffmpeg.txt` en la ruta real de generación (`scripts/salidas.py`) invocando el validador propio del demuxer `concat` de ffmpeg antes de escribirlo, y sanear `archivo_video` en el origen (recorte de espacios, rechazo de salto de línea) | **COMPLETADA** | 2026-10-02 | `scripts/salidas.py::_generar_concat_ffmpeg` llama a `concat_ffmpeg.validar_lista_concat_ffmpeg` sobre el contenido ya generado antes de `guardar_lista_concat_ffmpeg`; un contenido inválido degrada a `SalidaOmitida` con el motivo exacto (mismo patrón `try`/`except` que ya protege a las demás salidas), nunca una excepción sin capturar ni un archivo corrupto en disco. `scripts/tomas.py` gana `_sanear_archivo_video` (recorta espacios, normaliza a `""` si queda vacío o trae `\n`/`\r`), aplicada en `_toma_desde_dict` al leer un parte de rodaje editado a mano; `assets/reproductor/guion.js` gana la función gemela `sanearArchivoVideo(valor)`, aplicada en los dos puntos donde el dueño teclea el valor (`pedirArchivoVideoToma` durante la grabación y el botón de edición desde el índice). `references/contrato-tomas.md` y `contrato-montaje.md` documentan la regla de saneamiento y la validación antes de escritura. Fuera de alcance, explícito: no se extiende la misma validación-antes-de-escribir a `srt.py`/`capitulos_youtube.py` (misma deuda preexistente, sin las consecuencias reales que le da a `archivo_video` ser texto libre). 6 tests nuevos (613→619): 4 en `test_tomas.py` (recorte, solo espacios, salto de línea, retorno de carro), 1 en `test_salidas.py` (contenido inválido forzado por monkeypatch degrada a omitida sin escribir), 1 nuevo más la actualización de uno existente en `test_reproductor.py` (los dos puntos de entrada saneados en el HTML generado). Cuatro redes en verde, incluidas las dieciséis etapas de `verificar_salidas.py --fixture`. Fase transversal F-J, cierra el hallazgo `#27` de `auditoriacontinua.md`. `DEVELOPERS.md` y `SKILL.md` actualizados |

**Estados:** PENDIENTE · EN CURSO · COMPLETADA · DESPLEGADA EN PRODUCCIÓN · BLOQUEADA — <motivo> · DESCARTADA — <motivo>

*(La spec de cada tarea: T-XX en el cuerpo de `HOJA_DE_RUTA.md`; R-XX en `ROADMAP_PRODUCTO.md`. Este §1 NO repite la spec, solo el estado.)*

---

## 3. BLOQUEOS — ACCIONES PENDIENTES DEL DUEÑO

> El código se entrega igualmente; estas acciones activan funcionalidad latente.

| # | Acción | Tarea | Instrucciones exactas | Estado |
|---|--------|-------|-----------------------|--------|
| 1 | Instalar el plugin `skill-creator` (andamio de la skill) | T-00 | — | **RESUELTO 2026-08-31** — instalado (`skill-creator@claude-plugins-official`, ámbito usuario). |
| 2 | Aportar el **paquete** de `480-branded-pptx` | T-29 | El `SKILL.md` y el `brand-guide.md` ya están transcritos en `references/marca-480.md` (2026-08-31): bastan para el contrato, el brief y el estilo del PDF. Falta la skill instalada en `~/.claude/skills/480-branded-pptx/` con sus assets, y la skill `pptx` de la que depende. Hasta entonces la salida `.pptx` queda latente. **2026-09-02: el dueño confirma que aún no lo tiene y decide NO bloquear T-29** (§6.10) — se implementa entera por su requisito 4 y la salida queda latente, como ya preveía su criterio de aceptación. Este bloqueo no frena ninguna tarea. | ABIERTO — sin urgencia |
| 3 | Aportar 2–3 guiones de producción reales (`.md`) | T-09, T-10 | — | **RESUELTO 2026-08-31** — 3 guiones en `fixtures/reales/` (`guion-08-busqueda-investigacion`, `guion-09-proyectos`, `guion-artefactos-lienzo`). T-08 a T-12 recalibradas contra ellos en la hoja de ruta v1.1. |
| 4 | Conseguir los archivos de logotipo `480_*.png` | T-28 | — | **RESUELTO 2026-08-31** — las cuatro variantes en `assets/`, PNG RGBA con transparencia. **Ojo:** miden 1993×805 (ratio 2,4758), no el 1.7766 que dice la guía de marca; el ratio se mide del archivo. Ver `references/marca-480.md`. |
| 5 | Probar los atajos con el clicker Bluetooth real | T-24b | **2026-09-02: el dueño no dispone de clicker; queda en espera indefinida** (§6.9), y **T-24b está BLOQUEADA — el programador no debe intentarla**. El mapa completo ya está implementado (T-24, 2026-09-02): `Espacio`, `PageUp`/`PageDown`, flechas, `+`/`-`, `[`/`]`, `R`, `H`, `Esc` y `?`. Cuando el dueño consiga un mando: abrir el reproductor generado, pulsar cada botón y decir qué tecla envía cada uno — si no coincide con el mapa vigente (visible con `?` dentro del reproductor), el agente lo ajusta en `Configuracion.mapa_teclas_reproductor`, sin tocar `guion.js`. | ABIERTO — en espera indefinida |
| 6 | Instalar de verdad la skill (T-32) en tu propio Claude Code | T-32 | **2026-09-02: una sesión de nube no alcanza tu `~/.claude/skills/`** (nota de entorno, protocolo v1.3), así que ni la instalación ni el health check posterior pueden ejecutarse ni confirmarse desde aquí — todo lo demás de T-32 (`scripts/instalar_skill.py`, `fixtures/guion-ejemplo.md` y su versión esperada, la documentación de arquitectura en `DEVELOPERS.md`) ya está entregado y probado (contra una copia sincronizada de prueba, nunca contra tu ruta real). Ejecuta `python scripts/instalar_skill.py` (o pásale `--destino` si quieres otra ruta) y luego `python ~/.claude/skills/teleprompter/scripts/verificar_salidas.py --fixture`: si todas las etapas salen `OK`, T-32 puede marcarse COMPLETADA de verdad. Si algo falla, copia aquí la salida completa. | **RESUELTO 2026-09-03** — el dueño instaló la skill en `C:\Users\JanoSolerDíaz\.claude\skills\teleprompter` y el health check desde esa copia salió con las **11 etapas en OK**. Efecto colateral valioso: en su máquina **el `.pdf` real sí se genera** (tiene Chrome/Edge), no queda latente como en las sesiones de nube — es la primera vez que una verificación completa produce el PDF de verdad. La única salida que sigue latente es el `.pptx`, por el bloqueo #2. |
| 7 | Grabar un vídeo de curso completo con el teleprompter instalado, usando el ciclo entero (validación → grabación con tomas y tropiezos → revalidación → salidas) | Oleada v1 (criterio de salida) y v2 (evidencia real para R-04) | Todo el código de v1 a F-D está entregado, verificado y —desde T-32— instalado y probado en tu máquina real, `.pdf` real incluido. Falta el propio rodaje: sin él, el modo de operación sigue en AUTONOMÍA TOTAL (no conmuta a PRODUCCIÓN, §0.1) y `FEEDBACK.md` y la calibración de ppm de R-04 siguen sin ninguna entrada real. Cuando grabes, usa las ayudas ya entregadas: `G` marca la toma buena y `T` el tropiezo (R-02/R-03), así la primera grabación ya alimenta el ciclo de mejora en vez de perderse. | ABIERTO — sin urgencia, no bloquea ninguna tarea de código |
| 8 | ~~Revisar y desactivar/borrar las rutinas programadas duplicadas de este proyecto~~ — **diagnóstico corregido, no hace falta acción sobre teleprompter** | Infraestructura, no código | Hallazgo original de 2026-09-04 (duodécimo ciclo del día): `list_triggers` devuelve seis rutinas con nombre parecido — `Auditor`/`auditor-teleprompter`, `Product manager`/`product-manager-teleprompter`, `Programador`/`programador-teleprompter` — y se asumió que el trío sin sufijo (creado 2026-08-25, `trig_019V5UKE8jKMvA2LCneiTtTD`/`trig_01Gou6bJDBVucaAkfXYaynAz`/`trig_01RkE491KgehtmqBcoFUFFKz`) era un resto de prueba duplicando las rutinas `-teleprompter`, con coste doble de cómputo. **Corregido el 2026-09-10 (sexto ciclo de Programador):** `list_triggers` también trae `git_repository.url` y el prompt completo de cada rutina, campos que ninguna de las ~15 reconfirmaciones anteriores había leído. Los tres apuntan a `https://github.com/JanoSolerDiaz/centro-estudios-sw` (no a `telePrompter`) y su prompt lo confirma («...para **GestorAcademia**», no teleprompter) — son las rutinas de OTRO proyecto del dueño, con nombres aún sin el sufijo de producto que sí llevan las de este repo. Sus cron tampoco eran realmente coincidentes (`Programador` sin sufijo: `0 6,8,10,12,14 * * 1-5`, cinco disparos fijos, frente a `programador-teleprompter`: `0 6-15 * * 1-5`, diez disparos horarios — la lectura de 2026-09-04 los llamó "solapados" sin comparar el detalle). Las tres rutinas de *este* proyecto están cada una sola, sin duplicado ni solape. **Ninguna acción pendiente del dueño sobre las rutinas de teleprompter** — si quiere, puede revisar por separado si `centro-estudios-sw` tiene su propio problema de nomenclatura o rutinas duplicadas, pero es asunto de ese otro repositorio, fuera del alcance de este documento. **Nota histórica (2026-09-09):** el auditor había registrado por separado (`auditoriacontinua.md` #21, severidad alta) lo que parecía una reescritura del historial de `develop`; el programador lo investigó y confirmó que es un falso positivo del `git clone --depth` de cada contenedor efímero, sin relación con este bloqueo — se deja constancia aquí para que quede todo en un solo sitio. | **RESUELTO 2026-09-10** — diagnóstico corregido; no hay duplicado real para teleprompter |

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
| P-02 | Corregir en `revalidacion.py` la pérdida silenciosa de una edición manual cuando coincide, en la misma revalidación, con la aceptación de una partición de respiración sobre el mismo bloque | `origen: auditoría #9` (severidad alta). Rompía el invariante (c) («la edición manual manda») en ese cruce concreto, sin aviso ni test que lo detectara — el dueño podía perder una corrección de texto sin saberlo. Atendida como urgente antes de T-23, según §0.1/§0.3. | **COMPLETADA** 2026-09-02 |  |
| P-03 | Corregir en `revalidacion.py` la duplicación de contenido en una revalidación posterior a un conflicto edición/partición ya pospuesto (P-02), cuando el dueño no vuelve a tocar el documento | `origen: auditoría #14` (severidad alta). El límite que P-02 había dejado documentado como "un fragmento de texto sin editar" resultó ser, verificado con reproducción de código, una duplicación real de contenido en `guion-escenas.md` sin ningún aviso — rompía el invariante (c) por desajuste de esquema de identidad entre pasadas. Atendida como urgente antes de R-01, según §0.1/§0.3. | **COMPLETADA** 2026-09-03 |  |
| P-04 | Endurecer el cierre de `#14`: lectura tolerante de la disposición persistida, persistir solo las particiones realmente pospuestas, incidencia cuando las anclas del documento no son las previstas, y corregir el mensaje del conflicto edición/partición | `origen: auditoría #14` (ya cerrado por P-03, que es correcto). Tres grietas alrededor: (1) `estado.validacion` no se valida al cargar, así que basura en `particiones_pospuestas` tiraba la revalidación entera en vez de degradar; (2) se persistía el conjunto sin filtrar de bloques editados, no el de particiones pospuestas, dejando en `estado.json` índices que nunca tuvieron nada que posponer; (3) **un `estado.json` anterior a P-03, justo en mitad de un conflicto, reproduce el #14 tal cual y en silencio** — sin la clave persistida, la reconstrucción vuelve a ser optimista. Además el aviso del conflicto invitaba a «revalidar sin tocar ese bloque» para materializar la partición, que es justo lo que no funciona: lo hace retirar la edición, como demuestra el test que dejó P-03. | **COMPLETADA** 2026-09-03 |  |
| P-05 | `instalar_skill.py` deja de guardar la copia de seguridad DENTRO de `~/.claude/skills/`; pasa a `~/.claude/teleprompter-copias-de-seguridad/` | **Detectado en vivo en la máquina del dueño** al reinstalar la skill en esta misma sesión: Claude Code registra como skill toda subcarpeta de `~/.claude/skills/` que tenga un `SKILL.md`, así que `teleprompter.bak-<marca>` apareció en la lista de skills disponibles **como una segunda `teleprompter`, con nombre y descripción idénticos**, compitiendo con la real en la selección. Cada reinstalación añadía una. No es cosmético: degrada la funcionalidad principal de la skill justo cuando el dueño va a usarla. La copia de la instalación de hoy se movió a mano fuera de `skills/`; el arreglo evita que vuelva a pasar. | **COMPLETADA** 2026-09-03 |  |

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
| 9 | **T-24 depende del clicker Bluetooth, que el dueño no tiene.** ¿Se bloquea la tarea entera (y con ella T-25 y T-26, que dependen de ella en cascada) o se parte? | T-24, T-25, T-26 | **Partirla** (2026-09-02). El clicker se identifica como un teclado corriente, así que el mapa completo, el antirrebote y la ayuda `?` son implementables y testeables sin hardware; lo único que exige el mando físico es saber qué botón manda qué tecla. **T-24 se implementa con alcance reducido** (requisitos 1, 3, 4 y la mitad software del 2) y **la calibración sale a T-24b, BLOQUEADA hasta nuevo aviso del dueño**. FASE B4 continúa: T-25 y T-26 no se bloquean. **Nota del mismo día:** la sesión de nube de T-24 corrió en paralelo sin conocer esta decisión y entregó exactamente ese alcance, así que T-24 quedó COMPLETADA y la decisión no revierte nada — solo formaliza T-24b. → §1, §3.5 y §7. |
| 10 | **El paquete de `480-branded-pptx` sigue sin estar disponible.** ¿Se bloquea T-29 (y con ella T-30, T-31, T-32 y T-33 en cascada)? | T-29, T-30 | **No se bloquea** (2026-09-02). T-29 ya está especificada para funcionar con la skill de marca ausente: su requisito 4 y su criterio de aceptación exigen que se generen `tarjetas.json` y el brief, que la salida se marque latente y que no falle. Se implementa entera; **solo la generación real del `.pptx` queda latente** hasta que el dueño aporte el paquete (bloqueo §3.2). → §1, §3.2 y §7. |
| 11 | El auditor (`auditoriacontinua.md` #24, 2026-09-16) señala que la prosa de "Cola de producto" de `ROADMAP_PRODUCTO.md` lleva reconfirmaciones enteras desactualizada tras completarse una R-XX, y sugiere que el propio ciclo de reconfirmación del Programador quede autorizado a corregirla por sí solo cuando se limite a reflejar un estado que este §1 ya registra como `COMPLETADA` (sin ninguna decisión de producto nueva de por medio), en vez de esperar al siguiente ciclo de PM completo. Es un cambio de quién escribe en qué documento (§0.4 de `HOJA_DE_RUTA.md`), protocolo que solo cambia el dueño — el PM no puede concedérselo por su cuenta. ¿Autorizas esa excepción puntual (solo prosa de estado ya reflejado en §1, nunca una decisión de producto), o prefieres que la prosa siga esperando al siguiente ciclo de PM? | §0.4, `ROADMAP_PRODUCTO.md` | *(pendiente)* |

---

## 7. DESVIACIONES RESPECTO A LA HOJA DE RUTA ORIGINAL

> Resumen consolidado para comparar contra `HOJA_DE_RUTA.md` de un vistazo.

| Fecha | Tarea | Desviación | Motivo |
|-------|-------|-----------|--------|
| 2026-08-31 | T-00 | Se trabajó y se commiteó en `develop`, no en `main` como fijaba §0.1 | **Desviación cerrada el mismo día:** el dueño resolvió §6.7 confirmando `develop` como rama de trabajo y `master` como suya para el merge manual. El protocolo se actualizó (hoja de ruta v1.2) y a partir de ahí `develop` deja de ser una desviación: es la norma. |
| 2026-08-31 | T-00 | No se ejecutó `git init` | Ya estaba hecho. El resto de la tarea se cumplió íntegro. |
| 2026-09-02 | T-24 | La tarea se parte en dos: **T-24** (mapa de teclado, antirrebote, ayuda `?`) y **T-24b** (calibración del clicker físico, BLOQUEADA). La hoja de ruta la define como una sola tarea | **Decisión del dueño** (§6.9): no dispone de clicker. Bloquear T-24 entera habría bloqueado en cascada T-25 y T-26 y parado toda FASE B4, cuando la mitad software es implementable y testeable sin hardware. `HOJA_DE_RUTA.md` no se modifica (es inmutable): la spec de T-24b es el requisito 2 de T-24 en su mitad de verificación física. La sesión de nube de T-24, en paralelo y sin conocer la decisión, entregó ese mismo alcance por su cuenta: T-24 queda COMPLETADA y la desviación se reduce a la existencia de T-24b. |
| 2026-09-02 | T-29 | Ninguna desviación de la spec; se deja constancia de que **NO se bloquea** pese a seguir sin el paquete de marca | **Decisión del dueño** (§6.10). Se registra aquí porque la nota «Bloqueo humano» de T-29 en la hoja de ruta podía leerse como motivo para marcarla BLOQUEADA, cuando su propio requisito 4 y su criterio de aceptación exigen justo lo contrario: entregar el código completo con la salida latente. |
| 2026-08-31 | T-00 | No se hizo push al remoto | El protocolo §0.1 contemplaba push porque en un proyecto web equivale a desplegar. Aquí el despliegue es la instalación local de la skill (T-32) y publicar en GitHub es una acción hacia fuera. **Incorporado a la norma en v1.2:** no se hace push sin autorización explícita del dueño. Deja de ser desviación. |
