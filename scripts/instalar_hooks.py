"""Instala los git hooks versionados del proyecto (T-01).

Los hooks reales viven en `.git/hooks/`, que no esta bajo control de version: cada clon
del repositorio -incluidas las sesiones de nube efimeras- necesita instalarlos de nuevo.
Las plantillas viven en `scripts/hooks/` (si versionadas) y este script las copia al
sitio donde git las ejecuta, dandoles permiso de ejecucion.
"""

from __future__ import annotations

import argparse
import shutil
import stat
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from presentacion import Nivel, mostrar

RAIZ = Path(__file__).resolve().parent.parent
PLANTILLAS = RAIZ / "scripts" / "hooks"


def ruta_hooks_git(raiz_repo: Path) -> Path:
    """Resuelve el `.git/hooks` real, incluso si `.git` es un fichero (worktree)."""
    git_dir = raiz_repo / ".git"
    if git_dir.is_file():
        contenido = git_dir.read_text(encoding="utf-8").strip()
        prefijo = "gitdir:"
        if not contenido.startswith(prefijo):
            mensaje = f"Formato de '.git' no reconocido: {contenido!r}"
            raise ValueError(mensaje)
        git_dir = Path(contenido[len(prefijo) :].strip())
    return git_dir / "hooks"


def instalar_hook(nombre: str, raiz_repo: Path = RAIZ) -> Path:
    """Copia `scripts/hooks/<nombre>` a `.git/hooks/<nombre>` y lo hace ejecutable."""
    origen = PLANTILLAS / nombre
    if not origen.exists():
        mensaje = f"No existe la plantilla de hook: {origen}"
        raise FileNotFoundError(mensaje)
    destino_dir = ruta_hooks_git(raiz_repo)
    destino_dir.mkdir(parents=True, exist_ok=True)
    destino = destino_dir / nombre
    shutil.copyfile(origen, destino)
    permisos_actuales = destino.stat().st_mode
    destino.chmod(permisos_actuales | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return destino


def main() -> int:
    analizador = argparse.ArgumentParser(
        description="Instala los git hooks versionados del proyecto (T-01).",
    )
    analizador.add_argument(
        "--repo",
        type=Path,
        default=RAIZ,
        help="Raiz del repositorio donde instalar (por defecto, este repositorio).",
    )
    argumentos = analizador.parse_args()

    try:
        destino = instalar_hook("pre-commit", argumentos.repo)
    except (FileNotFoundError, ValueError) as excepcion:
        mostrar(f"No se pudo instalar el hook: {excepcion}", Nivel.ERROR)
        return 1

    mostrar(f"Hook de pre-commit instalado en {destino}", Nivel.OK)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
