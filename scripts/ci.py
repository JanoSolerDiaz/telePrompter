"""CI local del protocolo (T-04): un unico punto de entrada para las cuatro
verificaciones de HOJA_DE_RUTA.md §0.1 (tipos, estilo, tests, extremo a extremo).

Antes cada comando vivia duplicado en `scripts/hooks/pre-commit` y en `DEVELOPERS.md`.
Desde T-04 el hook delega aqui (`python scripts/ci.py`) en vez de repetir los cuatro
comandos, para que solo exista un sitio que decidir que se ejecuta y en que orden.

No hay repositorio remoto propio que ofrezca CI (GitHub Actions u otro): por eso esta
verificacion es local y su ejecucion es obligatoria antes de cada commit (via el hook).
Existe ademas un workflow de GitHub Actions equivalente en `.github/workflows/ci.yml`,
preparado pero inactivo (solo se dispara a mano), para el dia que el dueño decida
activarlo sobre `origin/develop`.

Ejecuta las cuatro etapas en orden y SIEMPRE hasta el final -incluso si una falla-, para
que el resumen final diga de una vez que esta roto y que no, en vez de abortar en la
primera y obligar a repetir para ver la siguiente. Agrega el resultado en un unico
codigo de salida: 0 si las cuatro pasan, 1 si alguna falla.

Uso: `python scripts/ci.py`
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from presentacion import Nivel, mostrar, titulo

RAIZ = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Etapa:
    """Una de las cuatro verificaciones del protocolo."""

    nombre: str
    comando: tuple[str, ...]


ETAPAS: tuple[Etapa, ...] = (
    Etapa("Tipos (mypy)", (sys.executable, "-m", "mypy", "scripts/", "tests/")),
    Etapa("Estilo (ruff check)", (sys.executable, "-m", "ruff", "check", "scripts/", "tests/")),
    Etapa("Tests (pytest)", (sys.executable, "-m", "pytest", "-q")),
    Etapa(
        "Extremo a extremo (verificar_salidas.py --fixture)",
        (sys.executable, str(RAIZ / "scripts" / "verificar_salidas.py"), "--fixture"),
    ),
)


def ejecutar_etapa(etapa: Etapa) -> bool:
    """Ejecuta una etapa mostrando su salida en directo. Devuelve True si paso."""
    titulo(etapa.nombre)
    resultado = subprocess.run(etapa.comando, cwd=RAIZ, check=False)
    return resultado.returncode == 0


def codigo_salida_agregado(resultados: list[bool]) -> int:
    """Agrega los resultados de las etapas en un unico codigo de salida de proceso."""
    return 0 if all(resultados) else 1


def main() -> int:
    titulo("CI local (T-04) — HOJA_DE_RUTA.md §0.1")
    resultados = [(etapa.nombre, ejecutar_etapa(etapa)) for etapa in ETAPAS]

    titulo("Resumen")
    for nombre, ok in resultados:
        mostrar(nombre, Nivel.OK if ok else Nivel.ERROR)

    fallidas = [nombre for nombre, ok in resultados if not ok]
    if fallidas:
        mostrar(f"CI en ROJO: {len(fallidas)} etapa(s) fallidas. No commitear.", Nivel.ERROR)
    else:
        mostrar("CI en VERDE: las cuatro verificaciones pasan.", Nivel.OK)

    return codigo_salida_agregado([ok for _, ok in resultados])


if __name__ == "__main__":
    raise SystemExit(main())
