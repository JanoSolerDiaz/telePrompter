"""Tests de la instalacion/actualizacion de la skill (tarea T-32).

Una sesion de nube no alcanza el `~/.claude/skills/` real del dueno (nota de
entorno del protocolo v1.3), asi que estos tests nunca instalan ahi: sincronizan
contra un `tmp_path` cualquiera. Eso no es simular la instalacion -- es probar
el mecanismo (que copia lo que debe, que hace copia de seguridad en vez de
sobrescribir, que la copia resultante es ejecutable por si sola) sin fingir que
ha ocurrido un despliegue real en la maquina del dueno.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from instalar_skill import RAIZ, InstalacionError, sincronizar_skill


def test_sincronizar_skill_copia_todas_las_entradas_del_paquete(tmp_path: Path) -> None:
    destino = tmp_path / "teleprompter"
    resultado = sincronizar_skill(destino)

    assert resultado.destino == destino
    assert resultado.copia_seguridad is None
    assert (destino / "SKILL.md").is_file()
    assert (destino / "scripts" / "verificar_salidas.py").is_file()
    assert (destino / "assets").is_dir()
    assert (destino / "references").is_dir()
    assert (destino / "fixtures" / "guion-ejemplo.md").is_file()
    # Lo que NO forma parte del paquete distribuible se queda fuera.
    assert not (destino / "tests").exists()
    assert not (destino / "roadmap").exists()
    assert not (destino / "fixtures" / "reales").exists()


def test_sincronizar_skill_hace_copia_de_seguridad_en_vez_de_sobrescribir(
    tmp_path: Path,
) -> None:
    destino = tmp_path / "teleprompter"
    sincronizar_skill(destino)
    marca_version_anterior = destino / "marca-de-version-anterior.txt"
    marca_version_anterior.write_text("version vieja", encoding="utf-8")

    resultado = sincronizar_skill(destino)

    assert resultado.copia_seguridad is not None
    assert resultado.copia_seguridad.name.startswith("teleprompter.bak-")
    # P-05: la copia NUNCA queda dentro de la carpeta de skills, o Claude Code
    # la registra como una skill duplicada que compite con la real.
    assert resultado.copia_seguridad.parent != destino.parent
    assert not any(
        hermana.name.startswith("teleprompter.bak-") for hermana in destino.parent.iterdir()
    )
    # La version anterior completa (con el archivo marcador) sigue intacta.
    assert (resultado.copia_seguridad / "marca-de-version-anterior.txt").read_text(
        encoding="utf-8"
    ) == "version vieja"
    # La nueva instalacion es un paquete fresco, sin el marcador de la anterior.
    assert not (destino / "marca-de-version-anterior.txt").exists()
    assert (destino / "SKILL.md").is_file()


def test_copia_de_seguridad_no_queda_dentro_de_la_carpeta_de_skills(tmp_path: Path) -> None:
    """P-05, el caso real: con el destino dentro de una carpeta `skills/`
    (`~/.claude/skills/teleprompter`), la copia de seguridad debe salir de ahi.

    Claude Code registra como skill toda subcarpeta de `skills/` que tenga un
    `SKILL.md`: dejar la copia dentro daba de alta una skill duplicada, con el
    mismo nombre y la misma descripcion que la real. Ocurrio de verdad en la
    maquina del dueno al reinstalar."""
    skills = tmp_path / ".claude" / "skills"
    destino = skills / "teleprompter"
    sincronizar_skill(destino)

    resultado = sincronizar_skill(destino)

    assert resultado.copia_seguridad is not None
    assert skills not in resultado.copia_seguridad.parents
    # En `skills/` solo queda la skill de verdad, ni un SKILL.md de mas.
    assert [entrada.name for entrada in skills.iterdir()] == ["teleprompter"]
    assert (
        resultado.copia_seguridad.parent
        == tmp_path / ".claude" / "teleprompter-copias-de-seguridad"
    )
    assert (resultado.copia_seguridad / "SKILL.md").is_file()


def test_sincronizar_skill_falla_si_falta_algo_del_paquete_en_el_origen(
    tmp_path: Path,
) -> None:
    origen_incompleto = tmp_path / "origen"
    origen_incompleto.mkdir()
    (origen_incompleto / "SKILL.md").write_text("---\n", encoding="utf-8")

    with pytest.raises(InstalacionError):
        sincronizar_skill(tmp_path / "destino", raiz_origen=origen_incompleto)


def test_health_check_funciona_ejecutado_desde_la_copia_instalada(tmp_path: Path) -> None:
    """Requisito 3 de T-32: `verificar_salidas.py --fixture` debe funcionar
    ejecutado desde la copia instalada, no solo desde el repositorio. Se
    prueba de verdad, como subproceso aislado, contra una copia sincronizada
    en `tmp_path` -- sin tocar el `~/.claude/skills/` real del dueno."""
    destino = tmp_path / "teleprompter"
    resultado = sincronizar_skill(destino)

    proceso = subprocess.run(
        [sys.executable, str(resultado.destino / "scripts" / "verificar_salidas.py"), "--fixture"],
        cwd=resultado.destino,
        capture_output=True,
        text=True,
        check=False,
    )

    assert proceso.returncode == 0, (
        f"health check fallido desde la copia instalada:\n{proceso.stdout}\n{proceso.stderr}"
    )


def test_paquete_declarado_existe_realmente_en_el_repositorio() -> None:
    """Si alguien anade una entrada a `ENTRADAS_PAQUETE` sin que exista
    todavia en el repositorio, este test lo detecta antes que un dueno
    instalando la skill."""
    from instalar_skill import ENTRADAS_PAQUETE

    for entrada in ENTRADAS_PAQUETE:
        assert (RAIZ / entrada).exists(), f"falta en el repositorio: {entrada}"
