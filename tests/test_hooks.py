"""Tests del hook de pre-commit y su instalador (T-01)."""

from __future__ import annotations

import stat
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from instalar_hooks import instalar_hook

RAIZ = Path(__file__).resolve().parent.parent
PLANTILLA_PRE_COMMIT = RAIZ / "scripts" / "hooks" / "pre-commit"


def test_plantilla_pre_commit_ejecuta_la_verificacion_completa() -> None:
    contenido = PLANTILLA_PRE_COMMIT.read_text(encoding="utf-8")
    for comando in ("mypy", "ruff check", "pytest", "verificar_salidas.py"):
        assert comando in contenido, f"el hook no ejecuta: {comando}"


def test_plantilla_pre_commit_aborta_ante_cualquier_fallo() -> None:
    contenido = PLANTILLA_PRE_COMMIT.read_text(encoding="utf-8")
    assert contenido.count("exit 1") >= 4


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
