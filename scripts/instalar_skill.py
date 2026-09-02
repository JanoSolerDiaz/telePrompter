"""Instalacion/actualizacion de la skill en ~/.claude/skills/teleprompter/ (T-32).

El "deploy" de este proyecto (§0.1): no hay servidor que reiniciar, hay una carpeta
de skill que sincronizar. Copia el paquete distribuible -- lo que la skill necesita
para funcionar, mas su documentacion de cara al dueno -- a la carpeta de destino,
haciendo antes copia de seguridad de cualquier version anterior en vez de
sobrescribirla in situ (invariante (d) de §0.2, sin borrado destructivo, mismo
patron que `documento_revision.guardar_documento_revision`).

Nota de entorno (v1.3): una sesion de nube no alcanza `~/.claude/skills/` del
dueno, asi que este script existe, se prueba contra un destino cualquiera (ver
`tests/test_instalar_skill.py`) y queda a la espera de que una sesion local o el
propio dueno lo ejecuten de verdad con el destino real -- ejecutarlo aqui contra
esa ruta no seria una instalacion real, solo la apariencia de una.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import RUTA_INSTALACION_SKILL
from presentacion import Nivel, mostrar

RAIZ = Path(__file__).resolve().parent.parent

# Que compone el paquete distribuible: exactamente lo que hace falta para que la
# skill funcione en ejecucion (biblioteca estandar, cero red) mas la
# documentacion pensada para el dueno (`SKILL.md`) y de referencia
# (`references/`). Fuera queda todo lo de desarrollo/gobierno del propio
# repositorio -- `tests/`, `roadmap/`, `.github/`, `DEVELOPERS.md` -- que no
# tiene sentido en una copia instalada y nunca lo ejecuta un dueno.
ENTRADAS_PAQUETE: tuple[str, ...] = (
    "SKILL.md",
    "scripts",
    "assets",
    "references",
    "fixtures/guion-ejemplo.md",
)


class InstalacionError(Exception):
    """Origen incompleto o destino invalido. Mensaje ya accionable en espanol."""


@dataclass
class ResultadoInstalacion:
    """Resultado de `sincronizar_skill`: donde quedo el paquete y, si existia
    una version anterior, donde quedo su copia de seguridad."""

    destino: Path
    copia_seguridad: Path | None


def _copiar_entrada(origen: Path, destino: Path) -> None:
    if origen.is_dir():
        shutil.copytree(origen, destino)
    else:
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(origen, destino)


def sincronizar_skill(destino: Path, raiz_origen: Path = RAIZ) -> ResultadoInstalacion:
    """Copia el paquete actual de `raiz_origen` a `destino`.

    Si `destino` ya existe (una instalacion previa), se renombra primero a
    `<nombre>.bak-<marca_de_tiempo>` en la misma carpeta padre -- nunca se
    sobrescribe in situ ni se borra -- y la copia nueva se escribe desde cero.
    """
    faltantes = [e for e in ENTRADAS_PAQUETE if not (raiz_origen / e).exists()]
    if faltantes:
        mensaje = (
            "Faltan en el origen, no se puede empaquetar la skill: " + ", ".join(faltantes)
        )
        raise InstalacionError(mensaje)

    copia_seguridad: Path | None = None
    if destino.exists():
        marca = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        copia_seguridad = destino.with_name(f"{destino.name}.bak-{marca}")
        destino.rename(copia_seguridad)

    destino.mkdir(parents=True)
    for entrada in ENTRADAS_PAQUETE:
        _copiar_entrada(raiz_origen / entrada, destino / entrada)

    return ResultadoInstalacion(destino=destino, copia_seguridad=copia_seguridad)


def main() -> int:
    analizador = argparse.ArgumentParser(
        description="Instala o actualiza la skill teleprompter en ~/.claude/skills/ (T-32).",
    )
    analizador.add_argument(
        "--destino",
        type=Path,
        default=Path(RUTA_INSTALACION_SKILL).expanduser(),
        help="Carpeta de instalacion (por defecto, ~/.claude/skills/teleprompter).",
    )
    argumentos = analizador.parse_args()

    try:
        resultado = sincronizar_skill(argumentos.destino)
    except InstalacionError as excepcion:
        mostrar(f"No se pudo instalar la skill: {excepcion}", Nivel.ERROR)
        return 1

    if resultado.copia_seguridad is not None:
        mostrar(f"Version anterior conservada en {resultado.copia_seguridad}", Nivel.AVISO)
    mostrar(f"Skill instalada en {resultado.destino}", Nivel.OK)
    mostrar(
        "Health check: "
        f"python {resultado.destino / 'scripts' / 'verificar_salidas.py'} --fixture",
        Nivel.INFO,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
