# DEVELOPERS — teleprompter

> Notas para quien clone este repositorio y quiera trabajar en el código. No sustituye a
> `roadmap/SEGUIMIENTO.md` (el hub del proyecto): esto es solo lo mecánico de arrancar.

## Puesta en marcha

1. Requiere Python 3.12+.
2. Instala las herramientas de desarrollo (mypy, ruff, pytest). **Son solo de desarrollo**:
   la skill se ejecuta sin ellas, únicamente con la biblioteca estándar de Python 3.
   ```
   pip install -r requirements-dev.txt
   ```
3. Instala el hook de pre-commit (§0.1). No está en `.git/hooks/` tras clonar porque esa
   carpeta no se versiona; hay que instalarlo una vez por clon:
   ```
   python scripts/instalar_hooks.py
   ```
   A partir de ahí, cada `git commit` ejecuta la verificación completa (mypy, ruff, pytest,
   `verificar_salidas.py --fixture`) y aborta el commit si algo falla. Para saltarlo
   puntualmente: `git commit --no-verify` (bajo tu responsabilidad).

## CI local (T-04)

`scripts/ci.py` es el único sitio donde viven las cuatro verificaciones del protocolo
(antes duplicadas entre el hook y esta guía). El hook de pre-commit lo invoca; para
lanzarlas sueltas, sin pasar por un commit:
```
python scripts/ci.py
```
Ejecuta las cuatro etapas en orden y hasta el final aunque alguna falle, para que el
resumen final diga de una vez qué está roto y qué no; agrega el resultado en un único
código de salida (0 si las cuatro pasan, 1 si alguna falla).

No hay CI remota propia: el repositorio no tiene integración con un servicio externo.
Existe un workflow de GitHub Actions equivalente en `.github/workflows/ci.yml`
(`workflow_dispatch`, sin disparo automático en `push`/`pull_request`) preparado para el
día que el dueño decida activarlo sobre `origin/develop`; hasta entonces solo se lanza a
mano desde la pestaña "Actions" de GitHub.

## Verificación manual

Los mismos cuatro pasos que ejecuta `scripts/ci.py` (y, a través de él, el hook), por si
hace falta lanzarlos sueltos uno a uno:

```
python -m mypy scripts/ tests/
python -m ruff check scripts/ tests/
python -m pytest -q
python scripts/verificar_salidas.py --fixture
```

## Salida al usuario y diagnóstico (T-02)

Dos módulos, dos audiencias, ninguna se mezcla con la otra:

- `scripts/presentacion.py` — lo único autorizado a hablarle al dueño (mensajes en
  español sobre el resultado de la ejecución). `print()` fuera de este módulo está
  prohibido por lint (`ruff` regla `T20`).
- `scripts/logger.py` — diagnóstico técnico. `configurar_logger(carpeta_salida,
  verbose=...)` escribe siempre `<carpeta_salida>/teleprompter.log` en nivel DEBUG;
  `--verbose` solo decide si además se ve por stderr mientras el proceso corre. El
  archivo vive dentro de la carpeta de salida del guion (regla de aislamiento, §0.2),
  nunca fuera.

## Monitorización de errores (T-05)

`scripts/monitorizacion.py` es la red de seguridad ante fallos que el resto del
protocolo no cubre (no hay Sentry ni servicio externo: la regla de cero red aplica
también aquí). Dos piezas:

- `ejecutar_con_diagnostico(funcion, carpeta_salida)` — envuelve el punto de entrada
  real de la CLI. Si `funcion` lanza una excepción no controlada: vuelca tipo, mensaje
  y traceback a `<carpeta_salida>/diagnostico-<timestamp>.log` (nunca variables
  locales, para no arrastrar el contenido íntegro del guion al archivo), dejar
  constancia en el logger de T-02 y muestra al dueño un mensaje accionable genérico en
  español por `presentacion.py` — la traza técnica nunca llega a la consola del dueño.
  Devuelve un código de salida distinto de 0.
- `ResumenEjecucion` — dataclass con el recuento final que debe mostrarse al terminar
  sin errores: escenas procesadas, bloques, avisos, reescrituras y salidas generadas.

Como con el logger de T-02, todavía no hay un `main()` real que envolver (llega con
T-07 en adelante): esta tarea deja la mecánica lista y probada para que cada punto de
entrada futuro la use en vez de inventar su propio manejo de errores.

## Robustez de entrada (T-06)

`scripts/entrada.py` blinda la única puerta de entrada real (el `.md` del guion)
antes de que nada lo procese, delante del parser (`scripts/parser.py`, T-08):

- `validar_ruta_guion(ruta)` — existe, no es una carpeta, tamaño ≤
  `TAMANO_GUION_MAX_BYTES` (`config.py`). Devuelve la ruta resuelta.
- `leer_guion(ruta)` — lee validando la ruta, decodifica UTF-8 (con o sin BOM, vía
  `utf-8-sig`) y rechaza cualquier otra codificación o un contenido vacío/solo
  blancos, con un error accionable en vez de un `UnicodeDecodeError` crudo.
- `verificar_estructura_minima(texto)` — cuenta encabezados Markdown de **cualquier
  nivel** (no el patrón estricto de escena de `PATRON_ENCABEZADO_ESCENA`, a
  propósito: una entrada hostil podría evitarlo) y rechaza 0 encabezados o más de
  `ESCENAS_MAX`. No decide qué encabezado es escena — eso sigue siendo trabajo de
  T-08.
- `nombre_guion_seguro(ruta)` / `carpeta_salida_para(ruta)` — derivan
  `<carpeta-del-guion>/<nombre-guion>-tarjetas/` saneando el nombre (unicode NFC,
  sin separadores de ruta ni secuencias de puntos) y comprobando con
  `Path.relative_to` que el resultado nunca cae fuera de la carpeta del guion
  (regla de aislamiento, §0.2).
- `ejecutar_con_limite_de_tiempo(funcion, segundos=...)` — tope de tiempo con
  `ThreadPoolExecutor` en vez de `signal.alarm` (no existe en Windows, la máquina
  del dueño). Si se agota el tiempo, el proceso principal recupera el control de
  inmediato; el hilo huérfano no se puede matar desde Python.

Todos los fallos usan una única excepción, `EntradaError`, con el mensaje ya
accionable en español: el futuro `main()` (T-07 en adelante) solo tiene que
capturarla y mostrarla por `presentacion.py`, igual que hace ya
`ejecutar_con_diagnostico` (T-05) con cualquier otra excepción no controlada.

**Nota de entorno:** el `python` real de este contenedor es 3.11.15 pese a que
`pyproject.toml` fija `requires-python = ">=3.12"` (`python3.12` existe aparte, sin
usarse). Por eso `entrada.py` evita la sintaxis de generics de PEP 695
(`def f[T](...)`, que `ast.parse` de 3.11 ni siquiera analiza) y usa
`typing.TypeVar` clásico. Ver `DECISIONES_TECNICAS.md`, T-06.

## Estado del proyecto de guion (T-07)

`scripts/estado.py` da al proceso memoria entre sesiones: `estado.json`, dentro de la
carpeta de salida derivada del guion (`<carpeta-del-guion>/<nombre-guion>-tarjetas/`,
que deriva `entrada.carpeta_salida_para`). Piezas:

- `EstadoProyecto` (dataclass) — el contrato de datos: versión de esquema, `InfoGuion`
  (ruta, hash sha256, tamaño), configuración efectiva, `SeparadorEscena` (nivel/patrón
  elegidos por T-08, `None` hasta entonces), y los contenedores que T-08 en adelante
  rellenan (`escenas`, `reescrituras`, `validacion`, `salidas_generadas`), vacíos por
  ahora — mismo tratamiento que T-02/T-04/T-05: infraestructura sin productor de datos
  todavía.
- `estado_inicial(ruta_guion, configuracion)` — estado de partida para un guion sin
  `estado.json` previo.
- `guardar_estado(estado, carpeta_salida)` — escritura **atómica**: escribe a
  `estado.json.tmp` en la misma carpeta y hace `Path.replace()` (atómico en POSIX y
  Windows) sobre `estado.json`; si algo falla antes del reemplazo, el `estado.json`
  anterior queda intacto y el temporal se limpia. Así un proceso interrumpido a mitad
  de escritura y relanzado nunca encuentra un archivo a medias.
- `cargar_estado(carpeta_salida)` — lee `estado.json`, aplica las migraciones
  pendientes (ver abajo) y reconstruye `EstadoProyecto`. Cualquier fallo (archivo
  ausente, JSON corrupto, estructura incompleta) levanta `EstadoError` con mensaje ya
  accionable en español, mismo contrato que `EntradaError` (T-06).
- `guion_modificado(estado, ruta_guion)` / `avisar_si_guion_modificado(...)` — compara
  el hash guardado contra el hash actual del guion; si difiere, avisa por
  `presentacion.py` que la próxima pasada recalculará escenas, clasificación y tiempos
  (todavía no hay recálculo incremental).

**Migraciones (`scripts/migraciones/`).** Cada archivo `NNN_<nombre>.py` define
`VERSION_DESTINO: int` y `aplicar(datos: dict) -> dict`, debe ser idempotente y debe
**preservar** cualquier clave ya presente en `datos` (invariante (c) de §0.2: la
edición del dueño manda), completando solo lo que falte con valores por defecto.
`aplicar_migraciones` (en `migraciones/__init__.py`) descubre los archivos por el
prefijo numérico, los ordena y aplica en cadena los que falten según
`version_esquema` (0 si no existe). El prefijo numérico no es un identificador Python
válido, así que se cargan con `importlib.import_module` en vez de `import` (mismo
mecanismo que usa Django); `N999` de ruff está ignorado para esa carpeta a propósito
(ver `pyproject.toml`). La migración `001_estado_inicial.py` es la que establece el
esquema versión 1 por primera vez.

## Parser de escenas (T-08)

`scripts/parser.py` convierte el `.md` en escenas: `parsear_guion(texto)` es el punto
de entrada. Piezas:

- `dividir_en_bloques(texto)` — trocea el `.md` en un `Bloque` por encabezado (de
  cualquier nivel), más el preámbulo si lo hay, con la línea de inicio/fin sobre el
  texto original (trazabilidad). Ignora `#` dentro de vallas de código (` ``` `/`~~~`).
  Concatenar el `contenido` de todos los bloques, en orden, reconstruye el `.md` línea
  a línea sin pérdida.
- `elegir_separador(texto, configuracion)` — decide el nivel/patrón de escena
  (`estado.SeparadorEscena`). El nivel se deriva de los `#` iniciales de
  `PATRON_ENCABEZADO_ESCENA` (`config.py`), no está fijado a mano.
- `parsear_guion(texto, *, configuracion=None, separador=None)` — si `separador` ya
  trae `nivel`/`patrón` (una decisión persistida de una sesión anterior en
  `estado.json`, T-07), se usa tal cual sin volver a preguntar el nivel. Los
  conflictos de clasificación de un encabezado concreto **sí** se revisan siempre,
  persistido o no, porque dependen de `configuracion.secciones_auxiliares`, que puede
  cambiar entre pasadas sin que cambie el separador.
- `extraer_metadatos(texto)` — pares `**Clave:** valor` de la cabecera (duración
  objetivo, formato, promesa/idea única…), sin esquema fijo de claves: los tres
  guiones reales no usan las mismas.

**Clasificación de un encabezado del nivel elegido** (ni todo `##` es escena — ver el
docstring del módulo para el detalle completo):
1. Casa con el patrón → escena.
2. Si no: título en `secciones_auxiliares` (lista negra) y cuerpo con
   `**LOCUCIÓN**` **a la vez** → conflicto real, se levanta
   `DeteccionEscenasAmbiguaError` con las alternativas y sus consecuencias (nº de
   escenas, duración media) en vez de decidir en silencio (requisito 6 de T-08).
   Solo lista negra → auxiliar. Solo `**LOCUCIÓN**` → escena (señal secundaria).
   Ninguna de las dos → auxiliar (caso por defecto, mayoritario en los tres guiones
   reales: el subtítulo entrecomillado, por ejemplo).
3. Ningún encabezado del nivel esperado casa con el patrón → también
   `DeteccionEscenasAmbiguaError`, con una alternativa por nivel candidato (`#`, `##`,
   `###`).

Sin CLI todavía que capture la excepción y le pregunte de verdad al dueño (llega con
T-16/T-17): hoy la persistencia de la respuesta se demuestra en
`tests/test_parser.py::test_conflicto_de_senales_se_resuelve_ajustando_la_lista_negra`.

## Suite de tests (T-03)

`tests/conftest.py` expone `guiones_reales` y `texto_guiones_reales`: acceso de una sola
vez a los tres guiones de calibración de `fixtures/reales/`. Úsalas en vez de rutas
sueltas si tu test necesita texto de guion real.

`tests/test_logica_pendiente.py` reúne, con `@pytest.mark.skip(reason=...)`, los tests
de la lógica de producto que T-03 debía cubrir pero que todavía no existe (clasificador,
troceador, motor de tiempos, normalizador, exportador `.srt`, y las dos invariantes de
cobertura total e idempotencia de §0.2; el parser de T-08 ya no está aquí, ver
`tests/test_parser.py`). Cada `skip` nombra la tarea que lo desbloquea y describe, en el
docstring, lo que el test debe comprobar. Al implementar esa tarea: quita el `skip` y
escribe el test descrito como parte de su propio criterio de aceptación — no lo dejes
como nota aparte.

## Estructura

- `scripts/` — código de la skill (biblioteca estándar únicamente).
- `scripts/hooks/` — plantillas de git hooks versionadas; instálalas con `instalar_hooks.py`.
- `scripts/migraciones/` — migraciones idempotentes del esquema de `estado.json`.
- `tests/` — suite de pytest.
- `fixtures/` — guiones de calibración y de ejemplo para las verificaciones.
- `assets/` — logotipos de marca 480 y, más adelante, plantillas del reproductor.
- `references/` — documentación de referencia (marca 480, contratos de datos).
- `roadmap/` — el registro de gobierno del proyecto: `SEGUIMIENTO.md` es el hub.

## Convenciones de rama

Se trabaja siempre en `develop`. `master` es del dueño del proyecto: nunca se commitea,
mergea ni empuja ahí. Ver `roadmap/HOJA_DE_RUTA.md` §0.1 para el protocolo completo.
