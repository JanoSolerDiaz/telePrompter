"""Tests del hook de pre-commit y su instalador (T-01, delega en `scripts/ci.py` desde T-04)."""

from __future__ import annotations

import os
import stat
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from instalar_hooks import instalar_hook

RAIZ = Path(__file__).resolve().parent.parent
PLANTILLA_PRE_COMMIT = RAIZ / "scripts" / "hooks" / "pre-commit"


def test_plantilla_pre_commit_delega_en_ci_py() -> None:
    contenido = PLANTILLA_PRE_COMMIT.read_text(encoding="utf-8")
    assert "scripts/ci.py" in contenido


def _preparar_hook_con_ci_falso(tmp_path: Path, codigo_salida: int) -> Path:
    """Copia la plantilla del hook a un repo temporal con un `scripts/ci.py` de mentira."""
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "ci.py").write_text(
        f"import sys\nsys.exit({codigo_salida})\n", encoding="utf-8"
    )
    hook = tmp_path / "pre-commit"
    hook.write_text(PLANTILLA_PRE_COMMIT.read_text(encoding="utf-8"), encoding="utf-8")
    hook.chmod(hook.stat().st_mode | stat.S_IXUSR)
    return hook


def test_hook_aborta_si_ci_falla(tmp_path: Path) -> None:
    hook = _preparar_hook_con_ci_falso(tmp_path, codigo_salida=1)
    resultado = subprocess.run(["sh", str(hook)], cwd=tmp_path, capture_output=True, check=False)
    assert resultado.returncode == 1


def test_hook_permite_commit_si_ci_pasa(tmp_path: Path) -> None:
    hook = _preparar_hook_con_ci_falso(tmp_path, codigo_salida=0)
    resultado = subprocess.run(["sh", str(hook)], cwd=tmp_path, capture_output=True, check=False)
    assert resultado.returncode == 0


@pytest.mark.skipif(
    os.name != "posix",
    reason=(
        "El bit de ejecucion S_IXUSR es un concepto POSIX sin equivalente en Windows "
        "(R-10): instalar el hook sigue copiando el archivo con normalidad ahi, solo "
        "esta comprobacion puntual del permiso deja de aplicar."
    ),
)
def test_instalar_hook_copia_y_da_permiso_de_ejecucion(tmp_path: Path) -> None:
    (tmp_path / ".git").mkdir()

    destino = instalar_hook("pre-commit", raiz_repo=tmp_path)

    assert destino == tmp_path / ".git" / "hooks" / "pre-commit"
    assert destino.read_text(encoding="utf-8") == PLANTILLA_PRE_COMMIT.read_text(encoding="utf-8")
    assert destino.stat().st_mode & stat.S_IXUSR


def test_instalar_hook_resuelve_gitdir_de_worktree(tmp_path: Path) -> None:
    git_real = tmp_path / "real" / ".git" / "worktrees" / "rama"
    git_real.mkdir(parents=True)
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    (worktree / ".git").write_text(f"gitdir: {git_real}\n", encoding="utf-8")

    destino = instalar_hook("pre-commit", raiz_repo=worktree)

    assert destino == git_real / "hooks" / "pre-commit"
    assert destino.exists()


def test_instalar_hook_falla_si_falta_la_plantilla(tmp_path: Path) -> None:
    (tmp_path / ".git").mkdir()
    with pytest.raises(FileNotFoundError):
        instalar_hook("hook-inexistente", raiz_repo=tmp_path)


def test_instalar_hook_falla_si_gitdir_no_reconocido(tmp_path: Path) -> None:
    (tmp_path / ".git").write_text("no es un gitdir valido\n", encoding="utf-8")
    with pytest.raises(ValueError, match="no reconocido"):
        instalar_hook("pre-commit", raiz_repo=tmp_path)
