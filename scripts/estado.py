"""Estado persistente del proyecto de guion (`estado.json`, tarea T-07).

Da al proceso memoria entre sesiones: a partir de T-08, cada etapa lee y escribe
este archivo en vez de recalcular todo desde cero cada vez que se relanza sobre el
mismo guion. Esta tarea fija el contrato de datos (las dataclasses de mas abajo) y
la mecanica de persistencia (escritura atomica + migraciones); las escenas, las
reescrituras y las validaciones quedan vacias hasta que T-08 y siguientes las
rellenen -- mismo tratamiento que T-02/T-04/T-05: infraestructura sin productor de
datos todavia.

Este modulo no valida la ruta del guion ni deriva la carpeta de salida: eso es
trabajo de `entrada.py` (T-06). Quien llame a `estado_inicial`/`guardar_estado` debe
haber pasado ya por `entrada.validar_ruta_guion` y `entrada.carpeta_salida_para`.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from config import NOMBRE_ARCHIVO_ESTADO, VERSION_ESQUEMA_ESTADO, Configuracion
from migraciones import aplicar_migraciones
from presentacion import Nivel, mostrar


class EstadoError(Exception):
    """Estado invalido, ilegible o con estructura incompleta.

    El mensaje del propio error ya es el texto accionable en espanol: quien la
    capture solo tiene que mostrarlo, nunca su traza (mismo contrato que
    `entrada.EntradaError`).
    """


def marca_de_tiempo() -> str:
    """Marca de tiempo ISO-8601 en UTC. Publica desde T-30, que la reutiliza
    para fechar cada entrada de `EstadoProyecto.salidas_generadas` con el
    mismo formato que `creado_en`/`actualizado_en`, en vez de duplicar la
    misma linea (mismo patron que `tiempos.PAUSA_FIN_ESCENA` en T-27)."""
    return datetime.now(UTC).isoformat()


def calcular_hash_guion(ruta_guion: Path) -> str:
    """Hash sha256 del contenido del guion, para detectar cambios entre sesiones."""
    return hashlib.sha256(ruta_guion.read_bytes()).hexdigest()


@dataclass
class InfoGuion:
    """Identidad del guion de origen sobre el que se construyo este estado."""

    ruta: str
    hash_sha256: str
    tamano_bytes: int


@dataclass
class SeparadorEscena:
    """Nivel de encabezado y patron elegidos como separador de escena (T-08).

    `None` en ambos campos mientras T-08 no se haya ejecutado todavia sobre este
    guion, o mientras la eleccion siga pendiente de confirmar por el dueno ante un
    caso ambiguo (T-08, requisito 6).
    """

    nivel: str | None = None
    patron: str | None = None


@dataclass
class EstadoProyecto:
    """Estado persistente completo de un proyecto de guion.

    `escenas`, `reescrituras`, `validacion` y `salidas_generadas` son listas/dicts
    de `dict[str, Any]` a proposito: su forma interna la fijan T-08 a T-27 segun
    avancen; este esquema solo garantiza que el contenedor existe, se conserva
    integro entre sesiones y no se pierde al migrar.
    """

    version_esquema: int
    guion: InfoGuion
    configuracion_efectiva: dict[str, Any]
    separador_escena: SeparadorEscena
    escenas: list[dict[str, Any]] = field(default_factory=list)
    reescrituras: list[dict[str, Any]] = field(default_factory=list)
    validacion: dict[str, Any] = field(default_factory=dict)
    salidas_generadas: list[dict[str, Any]] = field(default_factory=list)
    creado_en: str = field(default_factory=marca_de_tiempo)
    actualizado_en: str = field(default_factory=marca_de_tiempo)

    def a_dict(self) -> dict[str, Any]:
        return asdict(self)

    @staticmethod
    def desde_dict(datos: dict[str, Any]) -> EstadoProyecto:
        """Reconstruye el estado a partir del dict ya migrado a la version actual."""
        return EstadoProyecto(
            version_esquema=datos["version_esquema"],
            guion=InfoGuion(**datos["guion"]),
            configuracion_efectiva=datos["configuracion_efectiva"],
            separador_escena=SeparadorEscena(**datos["separador_escena"]),
            escenas=datos["escenas"],
            reescrituras=datos["reescrituras"],
            validacion=datos["validacion"],
            salidas_generadas=datos["salidas_generadas"],
            creado_en=datos["creado_en"],
            actualizado_en=datos["actualizado_en"],
        )


def estado_inicial(ruta_guion: Path, configuracion: Configuracion) -> EstadoProyecto:
    """Construye el estado de partida para un guion que aun no tiene `estado.json`."""
    ahora = marca_de_tiempo()
    return EstadoProyecto(
        version_esquema=VERSION_ESQUEMA_ESTADO,
        guion=InfoGuion(
            ruta=str(ruta_guion),
            hash_sha256=calcular_hash_guion(ruta_guion),
            tamano_bytes=ruta_guion.stat().st_size,
        ),
        configuracion_efectiva=asdict(configuracion),
        separador_escena=SeparadorEscena(),
        creado_en=ahora,
        actualizado_en=ahora,
    )


def ruta_estado(carpeta_salida: Path) -> Path:
    """Ruta del `estado.json` de un proyecto de guion, dentro de su carpeta de salida."""
    return carpeta_salida / NOMBRE_ARCHIVO_ESTADO


def guardar_estado(estado: EstadoProyecto, carpeta_salida: Path) -> Path:
    """Escribe `estado.json` de forma atomica (fichero temporal + reemplazo).

    Un corte a mitad de escritura nunca deja un `estado.json` a medio escribir:
    `os.replace` es atomico dentro del mismo sistema de ficheros (POSIX y Windows
    ambos lo garantizan), y el temporal vive en la misma carpeta que el destino para
    asegurar que ambos estan en el mismo sistema de ficheros. Si algo falla antes del
    reemplazo, el `estado.json` anterior queda intacto y el temporal se limpia.
    """
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    estado.actualizado_en = marca_de_tiempo()
    destino = ruta_estado(carpeta_salida)
    temporal = destino.with_name(destino.name + ".tmp")
    try:
        temporal.write_text(
            json.dumps(estado.a_dict(), ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        temporal.replace(destino)
    except OSError:
        temporal.unlink(missing_ok=True)
        raise
    return destino


def cargar_estado(carpeta_salida: Path) -> EstadoProyecto:
    """Lee `estado.json`, aplicando migraciones si viene de un esquema anterior."""
    ruta = ruta_estado(carpeta_salida)
    if not ruta.exists():
        raise EstadoError(f"No existe estado.json en la carpeta de salida: {ruta}")

    try:
        datos = json.loads(ruta.read_text(encoding="utf-8"))
    except json.JSONDecodeError as excepcion:
        raise EstadoError(
            f"El estado.json esta corrupto y no se puede leer: {ruta}. Detalle: {excepcion}"
        ) from excepcion

    datos_migrados = aplicar_migraciones(datos)
    try:
        return EstadoProyecto.desde_dict(datos_migrados)
    except (KeyError, TypeError) as excepcion:
        raise EstadoError(
            f"El estado.json tiene una estructura incompleta o invalida: {ruta}. "
            f"Detalle: {excepcion}"
        ) from excepcion


def guion_modificado(estado: EstadoProyecto, ruta_guion: Path) -> bool:
    """True si el guion de origen ha cambiado desde la ultima pasada (por hash)."""
    return calcular_hash_guion(ruta_guion) != estado.guion.hash_sha256


def avisar_si_guion_modificado(estado: EstadoProyecto, ruta_guion: Path) -> bool:
    """Comprueba si el guion cambio y, si es asi, avisa que se recalculara.

    Todavia no hay recalculo incremental (llega con T-08 en adelante): el aviso deja
    claro que la proxima pasada reconstruye escenas, clasificacion y tiempos desde
    cero para este guion, en vez de fallar en silencio con datos desactualizados.
    Devuelve True si el guion cambio.
    """
    if not guion_modificado(estado, ruta_guion):
        return False
    mostrar(
        f"El guion ha cambiado desde la ultima pasada ({ruta_guion}). "
        "Se recalcularan escenas, clasificacion y tiempos en la proxima pasada.",
        Nivel.AVISO,
    )
    return True
