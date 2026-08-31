# HOJA DE RUTA — teleprompter — Desarrollo automatizado con Claude Code

> DOCUMENTO INMUTABLE. Este archivo NO se modifica nunca. Es la referencia original para
> trazabilidad. El cuerpo (tareas T-XX) es inmutable y el protocolo solo lo cambia el dueño.
> Todo progreso, decisión, hallazgo, desviación o tarea nueva se registra en los documentos
> vivos de `roadmap/` (ver §0.4).
>
> Versión: 1.1 — 2026-08-31 (corrección de inicialización antes de la primera sesión: renombrado
> del proyecto a `teleprompter`, `skill-creator` ya instalado y calibración de T-08 a T-12 contra
> los tres guiones reales aportados en `fixtures/reales/`; guía de marca y logotipos 480 recogidos
> en `references/marca-480.md` y `assets/`, con Poppins fijada y el ratio del logotipo corregido.
> A partir de aquí, inmutable.)
> Proyecto: teleprompter — instalación local en `~/.claude/skills/teleprompter/`
> Repo: <pendiente> (git local, sin remoto)
> Modo de operación: AUTONOMÍA TOTAL (ver §0.1).

---

## 0. PROTOCOLO DE EJECUCIÓN (leer en cada sesión)

1. Lee este documento y `roadmap/SEGUIMIENTO.md` (el hub). El estado y el orden de "siguiente tarea" son los de §1 de SEGUIMIENTO (fuente autoritativa).
2. **Antes de elegir tarea**, revisa el registro de hallazgos de `auditoriacontinua.md`: si hay algún hallazgo ABIERTO de severidad alta (seguridad, bug en producción, rotura de UX), atiéndelo como P-XX urgente (§0.3) antes de la cola.
3. Identifica la siguiente tarea pendiente y consulta su especificación **donde vive**: si es T-XX, en el cuerpo de este documento; si es R-XX, en `roadmap/ROADMAP_PRODUCTO.md`.
4. Ejecuta las tareas EN ORDEN. No saltes a una posterior si la anterior no está COMPLETADA o BLOQUEADA en §1.
5. Si una tarea está BLOQUEADA, pasa a la siguiente y deja constancia (motivo + acción exacta que necesita el dueño) en §3 de SEGUIMIENTO.
6. Al terminar, actualiza los registros como indica §0.4 y commitea junto con el código.
7. NUNCA modifiques este archivo (`HOJA_DE_RUTA.md`).

### 0.1 Modo de operación

**MODO ACTUAL: AUTONOMÍA TOTAL.**

**AUTONOMÍA TOTAL** (vigente antes del primer curso grabado con la skill — prima la agilidad):
- Trabaja directamente en `main` y haz commit. El "despliegue" de este proyecto es la **instalación local de la skill**: sincronizar el paquete a `C:\Users\JanoSolerDíaz\.claude\skills\teleprompter\`. Es intencionado y está permitido.
- "Migraciones" = cambios del esquema de `estado.json` (el estado del proyecto de guión). Guarda SIEMPRE el archivo de migración (`scripts/migraciones/NNN_<nombre>.py`, idempotente) ANTES de ejecutarla y ejecuta exactamente ese archivo. Toda migración debe poder aplicarse sobre proyectos de guión ya existentes sin perder validaciones ni ediciones del dueño.
- Único requisito antes de cada commit/instalación: la verificación local completa debe pasar:
  ```
  python -m mypy scripts/ tests/                 # 1. tipos
  python -m ruff check scripts/ tests/           # 2. estilo
  python -m pytest -q                            # 3. tests
  python scripts/verificar_salidas.py --fixture  # 4. "build": e2e sobre el guión de ejemplo + auto-contención del HTML
  ```
  Es la red que sustituye a la revisión humana. Si algo falla, NO instales ni commitees: arregla o revierte.
- Verificación post-instalación (health check): tras cada sincronización, ejecuta `python scripts/verificar_salidas.py --fixture` **desde la copia instalada** y comprueba que termina en `OK` con código de salida 0 — genera las salidas sobre `fixtures/guion-ejemplo.md`, el `.html` no referencia ningún recurso externo y el `.srt` valida. Si falla, revierte el commit y restaura la versión anterior de la skill inmediatamente. Registra el incidente en §4 de SEGUIMIENTO.
- Decisiones autónomas: tómalas sin esperar aprobación, pero REGISTRA cada una en `roadmap/DECISIONES_TECNICAS.md`. El dueño no revisa el código: revisa ese registro.

> MODO PRODUCCIÓN (futuro, NO vigente): cuando el dueño lo indique (criterio de conmutación: **primer curso grabado en real usando la skill**), el protocolo cambia a ramas + Pull Request + merge manual por el dueño, y las migraciones de `estado.json` solo se preparan, nunca se autoejecutan sobre proyectos de guión reales. Hasta ese aviso, aplica el modo actual.

### 0.2 Reglas arquitectónicas innegociables (aplican en cualquier modo)

> Aquí viven las decisiones que son **norma permanente**, no solo historia. Cuando una decisión técnica deba regir para siempre ("usamos X, no reintroducir Y"), se promueve aquí desde `DECISIONES_TECNICAS.md`, porque esta sección se lee en cada sesión.

- INVARIANTES DE DATOS:
  - **(a) Cobertura total del guión** — todo bloque del `.md` de origen queda clasificado (locución o no locución) con su motivo visible. Prohibido descartar texto en silencio; un test de reconstrucción lo verifica.
  - **(b) Original siempre recuperable** — toda reescritura de locutabilidad conserva el texto original junto a la propuesta; el registro de reescrituras es append-only.
  - **(c) La edición manual manda** — al revalidar, el texto editado a mano por el dueño en `guion-escenas.md` es autoritativo y jamás se sobrescribe; solo se recalculan los derivados (troceo, tiempos, avisos).
  - **(d) Sin borrado destructivo** — nunca se sobrescribe ni se borra un archivo del dueño sin copia previa `.bak` con marca de tiempo.

  Jamás generar código que los viole ni desactivar la restricción "temporalmente".
- Aislamiento: **por proyecto de guión**. Toda escritura ocurre dentro de la carpeta de salida derivada del guión de origen (`<carpeta-del-guion>/<nombre-guion>-tarjetas/`); nunca fuera de ella. **Cero red en tiempo de ejecución**: la skill no hace ninguna petición, no envía telemetría y funciona íntegramente offline.
- Validación de entradas en toda función pública y en todo punto de entrada de la CLI: ruta inexistente, `.md` vacío, codificación no UTF-8, guión sin encabezados, escena sin locución, tamaño desmesurado. Errores accionables en español, nunca trazas crudas.
- Logger centralizado — nunca dejar `print()` de depuración en el código; la salida al usuario pasa por el módulo de presentación y los diagnósticos por el logger.
- Secretos: no commitear jamás claves ni ficheros de entorno. No imprimir secretos en logs ni en ningún documento. No rotar ni modificar claves existentes sin instrucción del dueño.
- Commits atómicos por tarea con prefijo del ID (p. ej. `T-03: <descripción>`).
- Textos de UI y mensajes en español. Todo el proyecto (documentación, código de cara al usuario, salidas) en español.
- PROHIBIDO degradar seguridad por agilidad (escribir fuera de la carpeta de salida, sobrescribir sin `.bak`, silenciar validaciones, ejecutar contenido del guión de entrada).
- **Salida autocontenida (regla dura):** el reproductor generado es UN ÚNICO archivo `.html` sin dependencias ni CDN. Prohibido que la salida contenga `http://`, `https://`, `//cdn`, `src=` externo, `@import`, `<link rel="stylesheet">` remoto, fuentes remotas o cualquier `fetch`/`XMLHttpRequest`. Un test automático lo comprueba y su fallo bloquea el commit.
- **Runtime sin dependencias:** la skill se ejecuta solo con la biblioteca estándar de Python 3. `mypy`, `ruff` y `pytest` son dependencias **exclusivamente de desarrollo** y nunca pueden ser necesarias para ejecutar la skill en la máquina del dueño.
- **Sin números mágicos:** todo valor por defecto (ppm, tamaño de bloque de respiración, márgenes, tamaños de fuente, umbrales de aviso) vive en un único módulo de configuración, es sobreescribible por el dueño y está documentado en `SKILL.md`.
- **Codificación explícita:** toda lectura y escritura declara `encoding="utf-8"` (entorno Windows, con acentos y eñes en las propias rutas de trabajo).
- **El reproductor prioriza legibilidad sobre branding:** neutro y oscuro, sin identidad corporativa. La marca 480 / Cuatroochenta solo aparece en las salidas `.pptx` y `.pdf`.
- **Convención de guión contractual, con aviso** (decisión del dueño, 2026-08-31): los rótulos mandan siempre — `**LOCUCIÓN**` con el cuerpo en cita de bloque frente a `**EN PANTALLA**` y `**NOTA**`, y escenas `## BLOQUE N — <título> (m:ss – m:ss)`. Una escena sin rótulo **no es un error**: se procesa infiriendo y se señala como desviación de la convención. Nunca al revés: la inferencia jamás sobrescribe lo que dice un rótulo.
- **Alcance de las reescrituras** (decisión del dueño, 2026-08-31): la skill solo propone reescritura para **normalización a forma dicha** y para **puntos de respiración**. Cacofonías, trabalenguas, anglicismos y estructuras difíciles se **avisan pero no se reescriben**. Ampliar este alcance es decisión del dueño, no una P-XX.
- **Ritmo base derivado del propio guión** (decisión del dueño, 2026-08-31): el ppm de referencia se deduce de las duraciones objetivo del guión; 120 ppm es solo el respaldo. Ver T-12.

### 0.3 Tareas autopropuestas (P-XX) — régimen de autonomía

Claude Code puede proponer y ejecutar mejoras de alcance nuevo sin esperar aprobación:

**Procedimiento:**
1. Asigna un ID con prefijo `P-` (P-01, P-02...). La numeración nunca se reutiliza.
2. ANTES de implementarla, regístrala en §5 de SEGUIMIENTO (descripción, motivo/origen, valor esperado, alcance). Garantiza trazabilidad aunque la sesión se corte.
3. Impleméntala con el mismo rigor que una T-XX: criterios de aceptación por escrito, tests si toca lógica de negocio, verificación pre-commit completa y health check post-instalación.
4. Refleja su estado en §1 de SEGUIMIENTO.

**Priorización:**
- Las T-XX/R-XX son la columna vertebral: por defecto, las P-XX se ejecutan cuando la tarea en curso está terminada o bloqueada.
- **Excepción (urgente):** pérdida de texto del guión, corrupción del estado, rotura del reproductor o de la auto-contención del HTML —propias o procedentes de un hallazgo ABIERTO de severidad alta del auditor— se atienden de inmediato, con justificación en `DECISIONES_TECNICAS.md`.
- No acumular más de 3 P-XX entre dos tareas consecutivas de la columna vertebral.

**Límites (una P-XX NUNCA puede):**
- Cambiar la convención de marcado de guiones acordada con el dueño, ni la identidad visual 480 / Cuatroochenta (colores, logotipo, tipografías).
- Introducir dependencias externas, CDN o cualquier acceso de red en la skill o en sus salidas.
- Eliminar funcionalidad existente ni realizar operaciones destructivas sobre guiones, salidas o archivos del dueño.
- Publicar o distribuir la skill fuera del equipo, ni subirla a un repositorio remoto.
- Dar de alta servicios externos de pago ni gestionar credenciales.
- Modificar textos legales ni generar comunicaciones a terceros.
- Contradecir las reglas de §0.2 ni los requisitos de una tarea pendiente.

**Veto:** el dueño puede marcar cualquier P-XX como DESCARTADA o pedir su revert en §5. Si está marcada para revert, revertirla es lo primero de la siguiente sesión.

### 0.4 Registro repartido — qué documento se toca y cuándo

El registro está repartido en varios documentos dentro de `roadmap/`. **Un dato vive en un solo sitio**; `SEGUIMIENTO.md` es el índice.

| Documento | Contiene | Acceso del programador |
|-----------|----------|------------------------|
| `SEGUIMIENTO.md` | Hub: estado (§1), bloqueos (§3), incidentes (§4), P-XX (§5), preguntas (§6), desviaciones (§7) | Lee siempre; escribe estado y transversales |
| `ROADMAP_PRODUCTO.md` | Visión + oleadas/fases + spec de las R-XX | Lee la spec de la R-XX en curso (lo gestiona el PM) |
| `DECISIONES_TECNICAS.md` | Decisiones técnicas (append-only) | **Consulta** antes de una decisión no trivial en el área que toca; **añade** las nuevas |
| `HISTORIAL_SESIONES.md` | Bitácora de sesiones (append-only) | Añade su sesión al terminar |
| `FEEDBACK.md` | Historias de usuario (lo gestiona el PM) | — |
| `auditoriacontinua.md` (raíz) | Hallazgos del auditor | **Lee** el registro de hallazgos al empezar |

**Al terminar cada sesión (definición de hecho):**
1. Actualiza el **estado** de la tarea en §1 de SEGUIMIENTO (y «última actualización» de la cabecera).
2. Añade las **decisiones** relevantes a `DECISIONES_TECNICAS.md` (append-only). Si alguna es norma permanente, promuévela también a §0.2.
3. Añade la **sesión** a `HISTORIAL_SESIONES.md` (append-only, la más reciente arriba), **referenciando** las filas de decisión añadidas y los cambios de estado (consistencia cruzada).
4. Actualiza `DEVELOPERS.md` si la tarea cambió algo que un desarrollador deba saber.
5. Si abriste una pregunta de negocio, déjala en §6; si te desviaste del plan, regístralo en §7.

---

## FASE A — VERIFICACIÓN Y BASE DE CALIDAD

> Obligatoria y primero: monta la red de seguridad que sustituye a la revisión humana. No empezar producto sin ella.

### T-00 — Verificación inicial del estado
**Prioridad:** ALTA · **Migración:** No
Inicializa el repositorio (`git init`, rama `main`, `.gitignore`) y el esqueleto del paquete: `SKILL.md` (borrador), `scripts/`, `tests/`, `fixtures/`, `assets/`, `references/`, `requirements-dev.txt`, `pyproject.toml`. Confirma que Python 3.14 responde y que el esqueleto se ejecuta sin error. **Usa el plugin `skill-creator` como andamio** (instalado el 2026-08-31): `skill-creator@claude-plugins-official`. Conserva los tres guiones reales que ya están en `fixtures/reales/` — son la referencia de calibración de T-08 a T-12 y no se tocan.
**Aceptación:** los cuatro comandos de verificación se ejecutan (aunque aún sin tests reales) y T-00 queda COMPLETADA en §1 con constancia del estado de partida.

### T-01 — Linting y formato
**Prioridad:** ALTA · **Migración:** No
Configurar `ruff` (lint + formato) con reglas estrictas en `pyproject.toml`, más `mypy` en modo estricto para `scripts/`. Hook de pre-commit que ejecute la verificación completa.
**Aceptación:** `ruff check` y `mypy` con 0 errores; hook funcional que impide commitear con la verificación en rojo.

### T-02 — Logger centralizado
**Prioridad:** MEDIA · **Migración:** No · **Depende de:** T-01
Módulo único de salida: `logger` para diagnósticos (con `--verbose`) y capa de presentación para los mensajes en español al dueño. Sustituir todo `print()` suelto.
**Aceptación:** 0 `print()` fuera del módulo de presentación (verificado por regla de lint); el log de ejecución se escribe en la carpeta de salida del guión.

### T-03 — Suite de tests mínima  ← la tarea MÁS importante en modo autonomía total
**Prioridad:** ALTA · **Migración:** No · **Depende de:** T-01
Configurar `pytest` y cubrir la lógica crítica con fixtures reales: parseo de encabezados, clasificación locución/no locución, troceo en bloques de respiración, cálculo de tiempos, normalización a forma dicha, generación de `.srt` y auto-contención del `.html`. Incluir un **test de cobertura total del guión** (invariante (a)) y un **test de idempotencia de la revalidación** (invariante (c)).
**Aceptación:** suite en verde; a partir de aquí los tests son obligatorios antes de cada commit.

### T-04 — Integración continua (CI)
**Prioridad:** ALTA · **Migración:** No · **Depende de:** T-01, T-03
Como no hay repositorio remoto, la CI es **local y obligatoria**: `scripts/ci.py` ejecuta las cuatro verificaciones en orden, con salida resumida y código de salida agregado, invocado por el hook de pre-commit. Dejar preparado un workflow de GitHub Actions equivalente, inactivo, para el día que haya remoto.
**Aceptación:** `python scripts/ci.py` en verde sobre el último commit; el hook falla si alguna verificación falla.

### T-05 — Monitorización de errores
**Prioridad:** ALTA · **Migración:** No · **Depende de:** T-02
No hay servicio externo (regla §0.2: cero red). La monitorización es **local**: captura de excepciones no controladas con mensaje accionable en español, volcado del diagnóstico completo a `<salida>/diagnostico-<timestamp>.log`, y resumen final de la ejecución (escenas procesadas, bloques, avisos, reescrituras, salidas generadas). El diagnóstico no incluye el contenido íntegro del guión, solo referencias de posición.
**Aceptación:** un fallo provocado en un test produce mensaje accionable + archivo de diagnóstico, y el proceso termina con código de salida distinto de 0.

### T-06 — Robustez de entrada (equivalente al rate limiting)
**Prioridad:** ALTA · **Migración:** No · **Depende de:** T-03
No hay endpoints; el equivalente es blindar la entrada: límites configurables de tamaño de guión y número de escenas, guardas ante `.md` malformado, sin encabezados, con encabezados inconsistentes, con codificación no UTF-8 o con BOM, rutas con acentos y espacios (Windows), y tiempo máximo de proceso. Ninguna entrada puede provocar bucle infinito, consumo desbocado ni escritura fuera de la carpeta de salida.
**Aceptación:** batería de tests de entradas hostiles en verde; todas degradan con error accionable, ninguna rompe ni escribe fuera.

---

## FASE B — PRODUCTO (derivada de los requisitos)

> Orden por valor incremental: primero el análisis del guión (sin él no hay nada), luego la
> locutabilidad, luego el ciclo de validación cómodo, luego el reproductor (la salida principal),
> después las salidas secundarias y por último el empaquetado como skill.

### FASE B1 — Núcleo de análisis del guión

### T-07 — Estado del proyecto de guión (`estado.json`)
**Prioridad:** ALTA · **Migración:** Sí (`001_estado_inicial`) · **Depende de:** T-06

**Objetivo:** dar al proceso una memoria persistente para retomar el trabajo en otra sesión sin perder validaciones ni ajustes, y fijar el contrato de datos del que dependen las demás tareas.

**Requisitos:**
1. Carpeta de salida derivada del guión: `<carpeta-del-guion>/<nombre-guion>-tarjetas/`. Nombres de archivo derivados del nombre del guión.
2. `estado.json` con: versión de esquema, ruta y hash del guión de origen, configuración efectiva, nivel de encabezado elegido como separador, escenas (id, título, bloques, clasificación, motivos), reescrituras (original + propuesta + aceptada/rechazada), estado de validación por escena, salidas generadas y marcas de tiempo.
3. Escritura atómica (fichero temporal + reemplazo) para que un corte no corrompa el estado.
4. Mecanismo de migraciones idempotentes en `scripts/migraciones/NNN_<nombre>.py`, con la versión de esquema dentro del propio `estado.json`.
5. Detección de guión modificado desde la última pasada (por hash) y aviso explícito de qué se recalculará.

**Criterio de aceptación:** proceso interrumpido a mitad y relanzado que reanuda sin pérdida; test que aplica la migración 001 sobre un `estado.json` de versión anterior sin perder validaciones ni ediciones.

### T-08 — Parser de Markdown y detección del separador de escenas
**Prioridad:** ALTA · **Migración:** No · **Depende de:** T-07

**Objetivo:** convertir el `.md` en una estructura de escenas fiable, decidiendo qué nivel de encabezado actúa como separador.

> **Evidencia de los guiones reales (`fixtures/reales/`, tres guiones):** el nivel separador es
> `##`, pero **no todos los `##` son escena**. Las escenas siguen el patrón
> `## BLOQUE N — <título> (m:ss – m:ss)`, y conviven con secciones `##` que NO son escena:
> el subtítulo entrecomillado tras el `#`, `## Capítulos (para la descripción del vídeo)`,
> `## Preparación antes de grabar` y `## Notas de producción`. Antes del primer `##` hay
> metadatos en negrita (`**Duración objetivo:**`, `**Formato:**`, `**Promesa del vídeo:**`).

**Requisitos:**
1. Parseo del `.md` conservando la posición original (línea de inicio y fin) de cada bloque, para trazabilidad.
2. Analizar la distribución de `#`, `##`, `###`: número de encabezados por nivel, volumen de texto bajo cada uno, regularidad.
3. **Distinguir escena de sección auxiliar dentro del mismo nivel.** Señal primaria: patrón de escena configurable, por defecto un encabezado que empieza por un marcador de bloque (`BLOQUE N`) y/o incluye un rango de timestamps `(m:ss – m:ss)`. Señal secundaria: la sección contiene un marcador de locución (T-09). Señal terciaria: lista negra configurable de títulos auxiliares (`Capítulos`, `Preparación antes de grabar`, `Notas de producción`).
4. Las secciones auxiliares no se descartan: se conservan como material no recitable del guión y aparecen en el informe (invariante (a)), diferenciadas de las indicaciones internas de escena.
5. Elegir automáticamente el nivel y el patrón cuando la señal es clara (criterio documentado y configurable).
6. **Si hay ambigüedad, proponer la elección al dueño con las alternativas y sus consecuencias (nº de escenas y duración media resultantes) y esperar confirmación antes de seguir.** La decisión se guarda en `estado.json` y no se vuelve a preguntar salvo que cambie el guión.
7. Extraer los metadatos de cabecera (duración objetivo, formato, promesa) y conservarlos para el informe y el contraste de tiempos (T-12).
8. Soportar preámbulo antes del primer encabezado (escena 0 o ignorado, según configuración documentada).

**Criterio de aceptación:** sobre los tres guiones reales, la skill detecta exactamente los bloques `BLOQUE 0…N` como escenas (7, 8 y 8 escenas respectivamente: `guion-08` 7, `guion-09` 8, `guion-artefactos-lienzo` 8) y ninguna sección auxiliar entra como escena; con una fixture ambigua pregunta en vez de decidir, y la respuesta queda persistida.

### T-09 — Clasificador locución / no locución
**Prioridad:** ALTA · **Migración:** No · **Depende de:** T-08

**Objetivo:** separar dentro de cada escena el texto que se recita del que no (indicaciones de pantalla, B-roll, notas de producción, timestamps).

> **Evidencia de los guiones reales:** existe ya una convención de facto, consistente en los tres
> guiones. Dentro de cada escena, el texto recitable va bajo un rótulo `**LOCUCIÓN**` y **en cita
> de bloque** (`> `); lo no recitable va bajo `**EN PANTALLA**` (23 apariciones) y `**NOTA**`.
> Recuento: `**LOCUCIÓN**` y `**EN PANTALLA**` aparecen 7/7, 8/8 y 8/8 veces —exactamente una vez
> por escena—, lo que la convierte en la señal primaria y deja la inferencia como red de
> seguridad, no como mecanismo principal.

**Requisitos:**
1. **Señal primaria (ruta rápida): rótulo de sección dentro de la escena.** Rótulos de locución y de no locución configurables; por defecto `**LOCUCIÓN**` (con el cuerpo en cita de bloque) frente a `**EN PANTALLA**` y `**NOTA**`. Cuando el rótulo está presente, manda sobre cualquier heurística.
2. **Señales de respaldo (inferencia)** para guiones sin rótulos o con rótulos parciales, cada una con su motivo legible: timestamps (`00:12`, `[0:45-1:10]`), corchetes y paréntesis de acotación, líneas en MAYÚSCULAS, cursiva o negrita de línea completa, viñetas de checklist, prefijos tipo `PANTALLA:`, `B-ROLL:`, `NOTA:`, `IMAGEN:`, `TÍTULO:`, bloques de código, tablas, enlaces sueltos, encabezados internos.
3. Si una escena tiene rótulo de locución pero además texto suelto fuera de la cita de bloque, ese texto se marca `revisar`: es el caso ambiguo más probable en estos guiones.
4. Cada bloque queda etiquetado como `locución` o `no-locución` **con el motivo y la señal que lo decidió**, y con su rango de líneas en el guión original.
5. Umbral de confianza: los bloques dudosos se marcan `revisar` y aparecen destacados en el `.md` anotado; nunca se silencian.
6. **Cobertura total obligatoria** (invariante (a)): la unión de bloques clasificados reconstruye el guión de origen sin pérdida; test de reconstrucción.
7. Resumen por escena de cuánto texto se excluyó y por qué.

**Criterio de aceptación:** sobre los tres guiones reales, clasificación **100 % correcta por la ruta rápida** (ningún texto de `**LOCUCIÓN**` perdido, ninguna línea de `**EN PANTALLA**` o `**NOTA**` colada como locución) y 0 bloques sin clasificar; con los mismos guiones despojados de rótulos, la inferencia alcanza ≥95 % de precisión en bloques de locución; el test de reconstrucción pasa en ambos casos.

### T-10 — Detección de convención de marcado y propuesta de convención explícita
**Prioridad:** MEDIA · **Migración:** No · **Depende de:** T-09

**Objetivo:** formalizar la convención que el dueño ya usa, para que la skill no tenga que inferir nada en los guiones futuros y el guionista sepa exactamente qué escribir.

> **Evidencia:** la convención ya existe de facto y es estable (ver T-08 y T-09). Esta tarea la
> **documenta y la vuelve contractual**, más que descubrirla. El valor añadido está en cerrar sus
> huecos: qué hacer con las secciones auxiliares, con el texto suelto fuera de la cita de bloque
> y con las escenas sin rótulo.

**Requisitos:**
1. Medir la consistencia de cada señal detectada en T-09 a lo largo del guión y del histórico de guiones procesados.
2. Cuando una señal cubre de forma consistente el contenido recitable o el no recitable, **proponer al dueño adoptarla como convención explícita**, con ejemplo de antes/después y el ahorro que supone.
3. Si el dueño acepta, guardar la convención en la configuración del usuario y **usar la ruta rápida** en guiones futuros, dejando la inferencia como red de seguridad.
4. Generar en la carpeta de salida una `convencion-guiones.md` de una página, lista para pegar en la plantilla de guiones del dueño, que recoja al menos: patrón de encabezado de escena (`## BLOQUE N — <título> (m:ss – m:ss)`), rótulo `**LOCUCIÓN**` con cuerpo en cita de bloque, rótulos `**EN PANTALLA**` y `**NOTA**`, títulos de secciones auxiliares reconocidas y metadatos de cabecera.
5. Informar de cada desviación del guión respecto a la convención vigente (escena sin rótulo de locución, rótulo desconocido, sección auxiliar no reconocida), sin bloquear el proceso.

**Criterio de aceptación:** los tres guiones reales se clasifican por convención sin recurrir a la inferencia y `convencion-guiones.md` los describe con exactitud; un guión con una escena sin rótulo se procesa igualmente y aparece señalado como desviación.

### T-11 — Troceo en bloques de respiración
**Prioridad:** ALTA · **Migración:** No · **Depende de:** T-09

**Objetivo:** producir la unidad de resaltado de todas las salidas: bloques de 6–12 palabras que se puedan decir de una respiración.

**Requisitos:**
1. Cortar por prioridad: puntuación fuerte (`.`, `?`, `!`, `;`, `:`) → puntuación débil (`,`, guiones, paréntesis) → conjunciones y nexos (`y`, `o`, `pero`, `que`, `porque`, `aunque`, `mientras`) → límites de sintagma (antes de preposición o determinante).
2. Rango 6–12 palabras **configurable** (mínimo, máximo y objetivo). Nunca cortar dentro de una cifra, una fecha, una sigla o una expresión normalizada por T-13.
3. Los bloques por debajo del mínimo se fusionan con el vecino más afín; los que superan el máximo se subdividen por el mejor punto disponible, registrando que fue un corte forzado.
4. Cada bloque conserva su texto exacto y su referencia a la escena y a la posición en el guión original.
5. Determinista: la misma entrada produce siempre el mismo troceo.

**Criterio de aceptación:** sobre las fixtures, ≥90 % de los bloques dentro del rango configurado, 0 cortes dentro de cifras o siglas, y troceo idéntico en dos ejecuciones consecutivas.

### T-12 — Motor de tiempos (ritmo deducido del guión, respaldo 120 ppm)
**Prioridad:** ALTA · **Migración:** No · **Depende de:** T-11

**Objetivo:** estimar duraciones creíbles para el reproductor, el `.srt` y la planificación del rodaje.

**Requisitos:**
1. **Ritmo base = ppm implícito del guión.** Se deduce del total de palabras de locución frente a la suma de las duraciones objetivo de los encabezados, como **valor único para todo el guión** (nunca por escena: un ppm por escena haría que la estimación cuadrase siempre con el objetivo y anularía el aviso del requisito 6, que es justo lo útil). **Respaldo: 120 ppm** si el guión no trae duraciones objetivo, si son incompletas, o si el ppm deducido cae fuera de una banda de plausibilidad configurable (por defecto 90–180 ppm); en ese caso se avisa de por qué se ha descartado. Todo configurable global, por guión y por escena.
2. Duración por bloque a partir del número de palabras, más pausas configurables según la puntuación final del bloque (coma < punto < fin de párrafo < fin de escena).
3. Agregados: duración por escena y total del vídeo, con el desglose visible.
4. Todos los tiempos derivan de una única función; ninguna salida recalcula por su cuenta.
5. Los tiempos se recalculan íntegramente al revalidar, sin arrastrar valores obsoletos.
6. **Contraste con la duración objetivo del guión** (los encabezados reales ya la traen: `(0:15 – 0:45)`, más el metadato `**Duración objetivo:**` de cabecera). Comparar estimación contra objetivo por escena y en total, y avisar cuando la desviación supere un umbral configurable, indicando cuántas palabras sobran o faltan para encajar. Es el aviso más útil antes de grabar.
7. **Transparencia del ritmo aplicado:** el informe y la cabecera del `guion-escenas.md` dicen siempre qué ppm se ha usado, de dónde sale (deducido del guión o respaldo de 120) y cuál sería el otro valor, para poder forzarlo a mano en una línea.
8. **Calibración opcional con toma real:** permitir fijar un ppm medido cronometrando una escena grabada, que tiene prioridad sobre el deducido. Queda guardado como preferencia del dueño.

**Criterio de aceptación:** test que comprueba que un texto de 120 palabras sin puntuación fuerte estima 60 s ± la tolerancia documentada con el ritmo de respaldo; suma de bloques = duración de escena = total, sin descuadres de redondeo; sobre los tres guiones reales se deduce un ppm dentro de la banda de plausibilidad, se aplica como base y se emite el contraste estimado/objetivo por escena; un guión sin duraciones objetivo cae a 120 ppm avisando del motivo.

### FASE B2 — Pasada de locutabilidad

### T-13 — Normalización a forma dicha
**Prioridad:** ALTA · **Migración:** No · **Depende de:** T-11

**Objetivo:** que el texto de la tarjeta sea exactamente lo que hay que decir, sin traducir mentalmente al leer.

**Requisitos:**
1. Cifras (cardinales y ordinales), años, fechas, horas, unidades, porcentajes, monedas, rangos, símbolos (`%`, `€`, `>`, `+`, `/`) y siglas (deletreadas o leídas según diccionario: `API`, `IA`, `PDF`, `URL`).
2. Reglas del español: concordancia de género y número, apócope (`un` / `uno`), `y`/`e`, `o`/`u`.
3. Diccionario de excepciones editable por el dueño (`diccionario-locucion.json` en la configuración) con prioridad sobre las reglas automáticas.
4. Toda normalización es una **reescritura marcada** (T-15): original recuperable y propuesta visible.
5. Documentar en `SKILL.md` cada familia de reglas y su valor por defecto.

**Criterio de aceptación:** batería de casos en español (`2026` → «dos mil veintiséis», `15 %` → «quince por ciento», `1.500 €` → «mil quinientos euros», `1ª` → «primera») en verde, y una entrada del diccionario del dueño sobrescribe la regla automática.

### T-14 — Detector de problemas de lectura en voz alta
**Prioridad:** MEDIA · **Migración:** No · **Depende de:** T-11

**Objetivo:** avisar de lo que va a costar decir antes de estar delante de la cámara.

**Requisitos:**
1. Frases sin punto de respiración (longitud por encima de un umbral configurable sin puntuación intermedia).
2. Cacofonías y repeticiones fónicas próximas (sílabas repetidas, rima involuntaria, `de` encadenados).
3. Trabalenguas: acumulación de consonantes difíciles o secuencias de palabras largas seguidas.
4. Anglicismos y extranjerismos, con sugerencia de equivalente en español o de pronunciación.
5. Estructuras difíciles: incisos anidados, subordinadas encadenadas, doble negación, voz pasiva larga.
6. Cada aviso indica escena, bloque, severidad y recomendación, y se vuelca al `.md` anotado. **Estos avisos nunca generan reescritura** (§0.2, alcance decidido por el dueño): se quedan en aviso para que decidas a mano. La única excepción es la frase sin punto de respiración, que sí puede proponer partición porque afecta al troceo.

**Criterio de aceptación:** cada familia de problemas tiene al menos un test que la detecta y un contraejemplo que no dispara falso positivo; los avisos aparecen localizados en el `.md` anotado.

### T-15 — Reescrituras marcadas, aceptables y reversibles
**Prioridad:** ALTA · **Migración:** No · **Depende de:** T-13, T-14

**Objetivo:** permitir que la skill mejore el texto sin quitarle nunca el control al dueño, dentro del alcance acotado en §0.2: solo forma dicha y respiración.

**Requisitos:**
1. Formato único de reescritura en el `.md` anotado: original y propuesta visibles a la vez, con marca inequívoca y motivo (normalización, respiración, cacofonía, anglicismo…).
2. Aceptación o rechazo **individual** por reescritura, editando el propio archivo con una marca simple, sin sintaxis frágil.
3. Registro append-only en `estado.json`: ninguna reescritura se pierde aunque se rechace; el original siempre es recuperable (invariante (b)).
4. Al revalidar, las reescrituras ya decididas no se vuelven a proponer; solo se proponen las nuevas.
5. Deshacer global: revertir todas las reescrituras de una escena o del guión completo.

**Criterio de aceptación:** ciclo completo en test — proponer, aceptar una, rechazar otra, revalidar y comprobar que las decisiones se respetan y el original sigue disponible.

### FASE B3 — Ciclo de validación

### T-16 — `guion-escenas.md`: el documento de revisión de una sola pasada
**Prioridad:** ALTA · **Migración:** No · **Depende de:** T-12, T-15

**Objetivo:** que el dueño revise TODO el guión de una sentada en su editor, sin ping-pong en el chat.

**Requisitos:**
1. Un único archivo con **todas** las escenas, en orden: título, duración estimada, número de palabras y número de bloques.
2. Dentro de cada escena, los bloques de respiración numerados y separados visualmente, tal y como se resaltarán.
3. Reescrituras marcadas en su formato (T-15) y avisos de locutabilidad (T-14) localizados.
4. **Al pie de cada escena**, las indicaciones no recitables detectadas, con la decisión tomada y el motivo (T-09), incluidos los bloques `revisar`.
5. Cabecera con el resumen global: total de escenas, palabras, duración estimada, avisos y reescrituras pendientes de decidir, ritmo aplicado.
6. Instrucciones breves al inicio: cómo editar, cómo aceptar o rechazar una reescritura, cómo forzar la clasificación de un bloque y cómo decir «validado».
7. Editable a mano sin romper el formato: las marcas deben tolerar espacios, tildes y reordenaciones.

**Criterio de aceptación:** el archivo generado sobre la fixture contiene el 100 % de escenas y bloques, se abre legible en un editor de texto plano y una edición manual arbitraria sigue siendo reprocesable por T-17.

### T-17 — Revalidación: releer, respetar y recalcular
**Prioridad:** ALTA · **Migración:** No · **Depende de:** T-16

**Objetivo:** cerrar el ciclo iterable —validar, pedir cambios, revalidar— sin perder nunca los ajustes anteriores.

**Requisitos:**
1. Al decir «validado», la skill **relee el archivo del disco** y toma su texto como autoritativo (invariante (c)).
2. Recalcula troceo y tiempos sobre el texto editado; nunca reescribe el texto del dueño ni reintroduce propuestas rechazadas.
3. Informe de revalidación **solo con lo roto o inconsistente**: bloques fuera de rango, escenas sin locución, marcas de reescritura ambiguas, indicaciones que parecen haber quedado dentro de la locución, escenas cuya duración se ha disparado. Nada de repetir lo que ya está bien.
4. Ciclo iterable: cada revalidación conserva las decisiones previas y se registra con marca de tiempo en `estado.json`.
5. Copia `.bak` con marca de tiempo del `guion-escenas.md` antes de regenerarlo (invariante (d)).

**Criterio de aceptación:** test de tres ciclos encadenados (validar → editar → revalidar → editar → revalidar) que comprueba que ninguna edición se pierde, ninguna propuesta rechazada reaparece y el informe solo lista incidencias reales.

### FASE B4 — Reproductor web (salida principal)

### T-18 — Esqueleto del reproductor autocontenido
**Prioridad:** ALTA · **Migración:** No · **Depende de:** T-17

**Objetivo:** el artefacto principal: un `.html` que funciona con doble clic, offline, en cualquier máquina.

**Requisitos:**
1. Generador que embebe datos (escenas, bloques, tiempos), CSS y JS en **un único archivo**, a partir de plantillas en `assets/`, sin dependencias ni CDN.
2. HTML/CSS/JS vanilla. Fuentes del sistema con pila de respaldo; nada remoto.
3. Escapado seguro del contenido del guión al inyectarlo (nada de romper el HTML con comillas, `<`, `&` o acentos).
4. **Validador de auto-contención** ejecutado en la verificación: detecta `http://`, `https://`, `//cdn`, `src=` externo, `@import`, `<link>` remoto y `fetch`, y falla el commit.
5. El archivo abre correctamente con doble clic desde `file://` sin errores de consola.

**Criterio de aceptación:** `verificar_salidas.py --fixture` genera el HTML, el validador de auto-contención pasa y el archivo se abre sin errores de consola desde `file://`.

### T-19 — Índice de escenas y entrada a pantalla completa
**Prioridad:** ALTA · **Migración:** No · **Depende de:** T-18

**Objetivo:** elegir qué escena se graba y arrancar en un gesto.

**Requisitos:**
1. Índice con título de escena, duración estimada y estado (pendiente / grabada / revisada), navegable con teclado (flechas, `Tab`, `Enter`) y con clic.
2. Botón de play por escena que **entra en pantalla completa** (Fullscreen API) directamente en esa escena.
3. Contador de escena visible (`4/12`) y foco visible en todo elemento navegable.
4. Volver al índice desde el reproductor sin recargar la página.

**Criterio de aceptación:** recorrido completo solo con teclado —llegar a la escena 4, arrancar en pantalla completa y volver al índice— sin usar el ratón.

### T-20 — Motor de avance híbrido
**Prioridad:** ALTA · **Migración:** No · **Depende de:** T-19

**Objetivo:** que el ritmo acompañe al locutor en vez de imponerse.

**Requisitos:**
1. Avance automático: cada bloque se resalta durante su duración estimada (T-12).
2. Velocidad ajustable **en vivo** con `+` / `-` (paso y límites configurados y documentados), aplicándose desde el bloque siguiente sin cortes.
3. Avance manual bloque a bloque en cualquier momento, **sin salir del modo automático ni reiniciar**: al avanzar a mano, el reloj del bloque se reinicia y el automático continúa desde ahí.
4. Pausa / reanudar, reiniciar escena, bloque anterior y siguiente, escena anterior y siguiente.
5. La velocidad ajustada se recuerda **por escena** (T-26).

**Criterio de aceptación:** con la escena en marcha, `+` acelera, avanzar a mano no detiene el automático y `Espacio` pausa y reanuda exactamente donde estaba.

### T-21 — Resaltado, tipografía y tema de grabación
**Prioridad:** ALTA · **Migración:** No · **Depende de:** T-20

**Objetivo:** legibilidad a distancia de cámara por encima de cualquier otra consideración.

**Requisitos:**
1. Resaltado por bloque de respiración: bloque activo destacado; contexto anterior y posterior visible pero atenuado, con gradiente de atenuación configurable.
2. Texto grande por defecto (tamaño base configurable y documentado) con control **en vivo** de tamaño.
3. Tema oscuro de alto contraste; contraste AAA para el bloque activo.
4. Márgenes seguros configurables; cursor oculto en pantalla completa tras un tiempo de inactividad; cero elementos que distraigan.
5. Sin identidad corporativa: neutro y oscuro.

**Criterio de aceptación:** revisión visual sobre la fixture a pantalla completa: el bloque activo se lee a distancia, el contexto se distingue sin competir y no hay elementos superfluos.

### T-22 — Autoscroll que mantiene el bloque activo centrado
**Prioridad:** ALTA · **Migración:** No · **Depende de:** T-21

**Objetivo:** que el bloque que toca decir esté siempre visible, sin saltos que despisten.

**Requisitos:**
1. Si el texto de la escena no cabe en pantalla, desplazamiento vertical automático que mantiene el bloque activo visible, idealmente **centrado en vertical**.
2. Desplazamiento suave, sin saltos bruscos, con duración configurable; sin rebotes al avanzar rápido a mano.
3. Si el texto cabe entero, no se desplaza nada.
4. Correcto tras cambiar el tamaño de texto, al activar el modo espejo y al redimensionar la ventana.

**Criterio de aceptación:** con una escena larga y varios cambios de tamaño de fuente, el bloque activo permanece siempre dentro del tercio central de la pantalla y no se producen saltos visibles.

### T-23 — Ayudas de grabación
**Prioridad:** MEDIA · **Migración:** No · **Depende de:** T-20

**Objetivo:** poder grabar sin ayudante ni cronómetro externo.

**Requisitos:**
1. Cuenta atrás 3-2-1 antes de arrancar (duración configurable, desactivable).
2. Cronómetro de la toma (tiempo real transcurrido) frente a la duración estimada de la escena.
3. Contador de escena (`4/12`) y barra de progreso de la escena por bloques.
4. Todos los indicadores discretos, en márgenes seguros, ocultables con una tecla.

**Criterio de aceptación:** al pulsar play arranca la cuenta atrás, el cronómetro coincide con el tiempo real (deriva < 1 % en una toma de 3 minutos) y la barra llega al 100 % justo con el último bloque.

### T-24 — Atajos de teclado y compatibilidad con clicker Bluetooth
**Prioridad:** ALTA · **Migración:** No · **Depende de:** T-23

**Objetivo:** manejar el teleprompter desde el mando de presentaciones, a distancia de cámara.

**Requisitos:**
1. Mapa completo: `Espacio` (pausa/reanudar o avanzar, según configuración), `→` / `PageDown` (bloque siguiente), `←` / `PageUp` (bloque anterior), `↑` / `↓` (escena anterior / siguiente), `+` / `-` (velocidad), teclas de tamaño de texto, `R` (reiniciar escena), `M` (espejo), `H` (ocultar indicadores), `Esc` (salir de pantalla completa).
2. **Compatibilidad con clicker Bluetooth**, que se identifica como teclado: aceptar `PageUp`/`PageDown`, flechas y `Espacio`; tolerar pulsaciones repetidas rápidas (antirrebote configurable) y evitar el desplazamiento nativo de la página.
3. Mapa de teclas configurable en la generación y visible en una ayuda dentro del reproductor (tecla `?`).
4. Ningún atajo depende de combinaciones que un clicker no puede enviar.

**Criterio de aceptación:** la escena se puede recorrer entera usando solo `Espacio`, `PageUp` y `PageDown`; la ayuda `?` lista el mapa vigente.

### T-25 — Modo espejo
**Prioridad:** MEDIA · **Migración:** No · **Depende de:** T-24

**Objetivo:** usar el reproductor con cristal de teleprompter.

**Requisitos:**
1. Volteo horizontal del texto, activable con tecla y desde los controles, sin afectar a la orientación de los indicadores si así se configura.
2. Compatible con autoscroll, resaltado y cambio de tamaño.
3. Estado recordado entre sesiones (T-26).

**Criterio de aceptación:** con el modo espejo activo, el texto se lee correctamente reflejado, el autoscroll sigue centrando el bloque activo y el ajuste persiste tras recargar.

### T-26 — Persistencia local de preferencias
**Prioridad:** MEDIA · **Migración:** No · **Depende de:** T-25

**Objetivo:** retomar la grabación entre sesiones sin reconfigurar nada.

**Requisitos:**
1. `localStorage` para: tamaño de texto, velocidad **ajustada por escena**, última escena vista, modo espejo y visibilidad de indicadores.
2. Clave de almacenamiento derivada del guión, para que dos guiones no se pisen las preferencias.
3. Toda lectura y escritura protegida con `try/catch`: si el almacenamiento no está disponible (`file://` restringido, navegación privada), el reproductor funciona igual con los valores por defecto.
4. Restablecer preferencias desde la ayuda del reproductor.
5. Un HTML regenerado sobre el mismo guión conserva las preferencias; si el troceo cambió, la velocidad por escena se conserva y la posición se reajusta al bloque más cercano.

**Criterio de aceptación:** cerrar el navegador y reabrir el archivo restaura tamaño, velocidad de la escena y última escena vista; con `localStorage` bloqueado, el reproductor arranca sin errores.

### FASE B5 — Salidas secundarias y selector

### T-27 — Exportador `.srt` borrador
**Prioridad:** ALTA · **Migración:** No · **Depende de:** T-12

**Objetivo:** arrancar los subtítulos en la fase de montaje sin partir de cero.

**Requisitos:**
1. Un subtítulo por bloque de respiración (agrupable por configuración si el bloque es muy corto), con tiempos acumulados de T-12.
2. Formato `.srt` estándar: índice, `HH:MM:SS,mmm --> HH:MM:SS,mmm`, texto, línea en blanco; sin solapes ni tiempos decrecientes; UTF-8 (con opción de BOM documentada).
3. Longitud máxima de línea y de subtítulo configurables, con partición limpia.
4. El texto es el **texto locutado final** (con las reescrituras aceptadas), no el original del guión.
5. **Consumible por ffmpeg**: validado con un test que lo parsea con las mismas reglas y comprueba monotonía y formato.

**Criterio de aceptación:** el `.srt` de la fixture pasa el validador estricto, no tiene solapes y sus tiempos suman la duración estimada del vídeo.

### T-28 — Exportador `.pdf` con identidad 480
**Prioridad:** MEDIA · **Migración:** No · **Depende de:** T-16

**Objetivo:** documento de repaso antes de grabar y, llegado el caso, **entregable presentable a terceros** con el guión de locución, con la identidad visual de la casa.

**Requisitos:**
1. Generar un HTML de impresión con `@page` y saltos por escena, siguiendo **`references/marca-480.md`** (paleta completa, escala tipográfica, interlineado 1,3–1,5, alineación siempre a la izquierda, márgenes ≥0,6", línea fina de acento verde bajo los títulos, fondos planos sin gradientes). Resumen: fondo blanco puro, texto `#333333`, secundario `#888888`, verde `#39FE90` primario, cian `#1CF9FC` secundario, rojo `#FF4950` solo alertas.
2. **Tipografía: Poppins** (decisión del dueño, 2026-08-31: manda la guía de marca sobre el `SKILL.md` de la skill de marca), con respaldo Montserrat → Calibri → sans del sistema, resuelta por nombre del sistema. Configurable en la clave `tipografia_marca`.
3. **Logotipo:** los cuatro archivos ya están en `assets/` del proyecto. Colocar la variante **Gris** (fondo claro). **La relación de aspecto se mide del propio PNG** leyendo su cabecera `IHDR` con la biblioteca estándar —`alto = ancho / (ancho_px/alto_px)`—; **está prohibido codificar la constante `668/376` de la guía**, que no corresponde a estos archivos (1993×805, ratio 2,4758) y los estiraría un 39 % en vertical. Respetar el mínimo de 20 mm en impresión y reservar en la maqueta el margen de seguridad, porque los PNG vienen recortados al contorno. Ruta de los assets configurable; si el archivo no está, el PDF sale sin logotipo y no falla. Detalle y tabla de alturas en `references/marca-480.md`.
4. Convertir a PDF con Chrome/Edge en modo headless (`--headless --print-to-pdf`), detectando el ejecutable en Windows; **si no se encuentra, dejar el HTML de impresión listo y decirlo con instrucciones para imprimir a PDF con Ctrl+P** (funcionalidad latente, no error).
5. **Una escena por página**, con título, duración objetivo y estimada, y el texto de locución **legible como prosa** —con los límites de bloque marcados de forma discreta, no troceado en lista—, más las indicaciones no recitables al pie. Es un documento para leer, no tarjetas para recitar: eso es el reproductor.
6. **Modo entregable a terceros** (`--para-terceros`, desactivado por defecto y documentado): omite las notas internas de producción y el aparato de reescrituras, y deja solo el texto de locución final y las indicaciones de pantalla. Sin él, el PDF es el documento de repaso completo.
7. Portada con título del vídeo, duración objetivo y total, número de escenas y palabras.
8. Sin dependencias de terceros en Python; las fuentes se resuelven por nombre del sistema, **ninguna descarga ni recurso remoto** (§0.2). Si Figtree no está instalada, el respaldo actúa sin romper la maqueta.

**Criterio de aceptación:** con Chrome disponible se genera el PDF, su número de páginas coincide con el número de escenas más la portada, y el validador de auto-contención pasa sobre el HTML de impresión; sin Chrome, la skill deja el HTML y un mensaje accionable, sin fallar; `--para-terceros` produce un PDF sin ninguna nota interna.

### T-29 — Adaptador `.pptx` (delegación en `480-branded-pptx`)
**Prioridad:** MEDIA · **Migración:** No · **Depende de:** T-16

**Objetivo:** entregar el guión de locución como presentación con la marca 480 **sin reinventar estilos**: documento de repaso y, llegado el caso, entregable a terceros.

> **Cómo funciona realmente la delegación** (verificado con el `SKILL.md` de `480-branded-pptx`,
> 2026-08-31): esa skill son **instrucciones para Claude**, no un ejecutable — genera el `.pptx`
> con Node y `pptxgenjs` apoyándose a su vez en la skill `pptx`, y exige QA visual. Por tanto
> nuestra skill **no puede invocarla como subproceso**. El reparto es: nosotros producimos
> `tarjetas.json` + un **brief de invocación**, y el `.pptx` lo genera Claude delegando en ella
> dentro de la misma sesión. Nosotros no escribimos ni una línea de estilo de marca.

**Requisitos:**
1. Definir el **contrato de intercambio** `tarjetas.json` (escenas, bloques, duraciones objetivo y estimada, títulos, indicaciones de pantalla, notas internas, metadatos de cabecera), documentado en `references/`, estable e independiente del generador.
2. Generar junto a él un **brief de invocación** en Markdown que le diga a Claude qué estructura de deck se espera, **respetando la estructura que esa skill ya impone** (portada DARK, índice si hay 4+ secciones, contenido LIGHT, separadores, cierre — ver `references/marca-480.md`). El brief debe además **corregir por escrito dos cosas del `SKILL.md` de esa skill**, porque su código las lleva fijas y con estos assets fallan: (a) usar **Poppins**, no Figtree; (b) usar la relación de aspecto **medida del PNG** (2,4758 con los archivos actuales) y las alturas que se derivan de ella, no la constante `668/376`, que deforma el logotipo un 39 %: **una diapositiva por escena** (agrupación configurable), texto de locución como prosa legible, duración objetivo y estimada, indicaciones de pantalla en la propia diapositiva y **texto completo de la escena en las notas del orador**. El brief no repite estilos de marca: para eso está la skill de marca.
3. Respetar el modo **entregable a terceros** de T-28: la misma bandera omite notas internas y aparato de reescrituras en el `tarjetas.json` exportado.
4. Detección de disponibilidad: si la skill de marca no está instalada, **no fallar** — dejar el `tarjetas.json` y el brief generados, marcar la salida como latente e indicar en §3 de SEGUIMIENTO qué falta.

**Bloqueo humano:** el **paquete** de `480-branded-pptx` no está en esta máquina. El dueño transcribió su `SKILL.md` y su `references/brand-guide.md` (2026-08-31, recogidos en `references/marca-480.md`), suficiente para fijar el contrato, el brief y el estilo del PDF. Faltan los `assets/480_*.png` (el dueño los está consiguiendo) y la skill `pptx` de la que depende. Mientras tanto el código se entrega completo y la salida `.pptx` queda latente; el resto de salidas no se ve afectado.

**Criterio de aceptación:** con la skill de marca ausente, `tarjetas.json` y el brief se generan y el mensaje explica exactamente qué falta; el contrato está documentado y testeado contra un esquema; el brief sobre un guión real describe tantas diapositivas de contenido como escenas.

### T-30 — Selector de salidas en cada validación
**Prioridad:** ALTA · **Migración:** No · **Depende de:** T-18, T-27, T-28, T-29

**Objetivo:** que cada validación pregunte qué se genera, sin asumir nada.

**Requisitos:**
1. Al validar, **preguntar cada vez** qué salidas se generan (HTML, PPTX, PDF, SRT), en una única pregunta de opción múltiple.
2. Recordar la última selección como **sugerencia** (no como decisión silenciosa) en `estado.json`.
3. Generación independiente: el fallo o la latencia de una salida no impide las demás.
4. Resumen final con la ruta de cada archivo generado, su tamaño y las salidas omitidas o latentes con su motivo.

**Criterio de aceptación:** dos validaciones seguidas preguntan las dos veces; con la salida `.pptx` latente, las otras tres se generan igualmente y el resumen lo refleja.

### FASE B6 — Empaquetado como skill e integración

### T-31 — `SKILL.md` y configuración completa
**Prioridad:** ALTA · **Migración:** No · **Depende de:** T-30

**Objetivo:** que la skill se active sola cuando toca y que todo valor por defecto sea visible y ajustable.

**Requisitos:**
1. `SKILL.md` con frontmatter (`name: teleprompter`, `description` con los disparadores en español: «tarjetas de locución», «teleprompter», «guión para grabar», «bloques de respiración»…) y el flujo de trabajo paso a paso.
2. **Tabla completa de valores por defecto y su configuración**: origen del ritmo (deducido del guión, respaldo 120 ppm, banda de plausibilidad 90–180), rango de bloque (6–12 palabras), pausas por puntuación, patrón de encabezado de escena y lista de secciones auxiliares, rótulos de la convención (`**LOCUCIÓN**`, `**EN PANTALLA**`, `**NOTA**`), alcance de las reescrituras, tamaño base y límites de texto, paso de velocidad, atenuación del contexto, márgenes seguros, cuenta atrás, antirrebote del clicker, límites de línea del `.srt`, agrupación de diapositivas bandera `--para-terceros`, `tipografia_marca` y ruta de los assets de logotipo.
3. Precedencia de configuración documentada: valores por defecto → configuración del usuario → configuración del proyecto de guión → argumentos de la invocación.
4. Documentación extensa en `references/` (contrato `tarjetas.json`, formato del `.md` anotado, convención de marcado, mapa de teclas), no en el `SKILL.md`.
5. Guía de uso en tres líneas al principio: guión → validación → salidas.

**Criterio de aceptación:** no queda ningún valor por defecto en el código que no esté en la tabla del `SKILL.md`; test que compara las claves del módulo de configuración con las documentadas y falla si divergen.

### T-32 — Instalación de la skill y guión de ejemplo
**Prioridad:** ALTA · **Migración:** No · **Depende de:** T-31

**Objetivo:** el "deploy" de este proyecto: dejar la skill instalada y verificable.

**Requisitos:**
1. Script de instalación/actualización que sincroniza el paquete a `~/.claude/skills/teleprompter/`, con copia de seguridad de la versión anterior.
2. `fixtures/guion-ejemplo.md`: guión realista de curso en español, con locución mezclada con indicaciones de pantalla, B-roll, notas y timestamps, y su versión esperada anotada.
3. `verificar_salidas.py --fixture` como health check ejecutable **desde la copia instalada**.
4. `DEVELOPERS.md` con la arquitectura, el mapa de módulos y cómo añadir una regla nueva (de clasificación, de normalización o de aviso).

**Criterio de aceptación:** tras instalar, el health check pasa desde la ruta instalada y genera las cuatro salidas (o tres más la latente) sobre el guión de ejemplo.

### T-33 — Encaje con la cadena de montaje de vídeo
**Prioridad:** MEDIA · **Migración:** No · **Depende de:** T-27, T-32

**Objetivo:** que esta skill sea el paso previo limpio de la skill de montaje con ffmpeg.

**Requisitos:**
1. Documentar el contrato de salida hacia la fase de montaje: `.srt` estándar + `tarjetas.json` + estructura de carpetas y nomenclatura de archivos.
2. Nombres y orden de escenas estables y predecibles, para casar tomas con escenas sin ambigüedad.
3. Test de integración que valida el `.srt` con las reglas que aplica ffmpeg y comprueba la estructura del `tarjetas.json` contra su esquema.
4. Sección en `SKILL.md` que explique dónde encaja en la cadena y qué espera la skill de montaje.

**Criterio de aceptación:** el `.srt` de la fixture se valida sin avisos y la documentación del encaje está en `SKILL.md` y en `references/`.

---

## ESTRUCTURA DE UNA TAREA (formato de toda T-XX)

```
### T-NN — <título>
**Prioridad:** ALTA | MEDIA | BAJA · **Migración:** Sí (`NNN_<nombre>`) | No · **Depende de:** <T-XX o —>

**Objetivo:** <qué problema resuelve y por qué importa>

**Requisitos:**
1. <paso concreto>

**Bloqueo humano (si lo hay):** <qué hace el dueño; el código se entrega igual, la funcionalidad queda latente>

**Criterio de aceptación:** <condición objetiva y verificable de "hecho">
```

---

## RESUMEN DE DEPENDENCIAS Y BLOQUEOS HUMANOS

| Tarea | Depende de | Bloqueo humano (no impide entregar el código) |
|-------|-----------|------------------------------------------------|
| T-00  | —         | — (resuelto: `skill-creator` instalado el 2026-08-31)          |
| T-01  | —         | —                                              |
| T-02  | T-01      | —                                              |
| T-03  | T-01      | —                                              |
| T-04  | T-01, T-03| —                                              |
| T-05  | T-02      | —                                              |
| T-06  | T-03      | —                                              |
| T-07  | T-06      | —                                              |
| T-08  | T-07      | — (resuelto por evidencia: escenas `## BLOQUE N — … (m:ss – m:ss)`) |
| T-09  | T-08      | — (resuelto: 3 guiones reales en `fixtures/reales/`)           |
| T-10  | T-09      | Aceptar la convención ya observada como contractual (§6)      |
| T-11  | T-09      | —                                              |
| T-12  | T-11      | Confirmar 120 ppm o adoptar el ppm implícito de los guiones (§6) |
| T-13  | T-11      | —                                              |
| T-14  | T-11      | —                                              |
| T-15  | T-13, T-14| —                                              |
| T-16  | T-12, T-15| —                                              |
| T-17  | T-16      | —                                              |
| T-18  | T-17      | —                                              |
| T-19  | T-18      | —                                              |
| T-20  | T-19      | —                                              |
| T-21  | T-20      | —                                              |
| T-22  | T-21      | —                                              |
| T-23  | T-20      | —                                              |
| T-24  | T-23      | Probar con el clicker Bluetooth real            |
| T-25  | T-24      | —                                              |
| T-26  | T-25      | —                                              |
| T-27  | T-12      | —                                              |
| T-28  | T-16      | Confirmar assets de marca 480 (logotipo y tipografía) |
| T-29  | T-16      | **Skill `480-branded-pptx` no instalada** — salida latente |
| T-30  | T-18, T-27, T-28, T-29 | —                                  |
| T-31  | T-30      | —                                              |
| T-32  | T-31      | —                                              |
| T-33  | T-27, T-32| —                                              |

---

*Fin de la hoja de ruta original v1.0 — no modificar este archivo.*
