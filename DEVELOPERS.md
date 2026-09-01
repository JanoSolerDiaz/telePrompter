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

## Suite de tests (T-03)

`tests/conftest.py` expone `guiones_reales` y `texto_guiones_reales`: acceso de una sola
vez a los tres guiones de calibración de `fixtures/reales/`. Úsalas en vez de rutas
sueltas si tu test necesita texto de guion real.

`tests/test_logica_pendiente.py` reúne, con `@pytest.mark.skip(reason=...)`, los tests
de la lógica de producto que T-03 debía cubrir pero que todavía no existe (parser,
clasificador, troceador, motor de tiempos, normalizador, exportador `.srt`, y las dos
invariantes de cobertura total e idempotencia de §0.2). Cada `skip` nombra la tarea que
lo desbloquea y describe, en el docstring, lo que el test debe comprobar. Al implementar
esa tarea: quita el `skip` y escribe el test descrito como parte de su propio criterio de
aceptación — no lo dejes como nota aparte.

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
