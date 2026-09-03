"""Feedback de grabacion: bloques marcados como tropiezo (tarea R-03).

Objetivo (`ROADMAP_PRODUCTO.md` R-03): capturar en caliente donde se traba el
locutor, para que ese conocimiento no se pierda entre la grabacion y la
siguiente revision. El reproductor (`assets/reproductor/guion.js`) deja marcar
el bloque EN PANTALLA con una tecla, sin interrumpir la toma (requisito 1);
cuando el dueno pulsa "Exportar tropiezos" vuelca el registro completo, tal
como esta en memoria, a un archivo `.json` independiente -- el propio
navegador `file://` no puede escribir en la carpeta de salida del guion (cero
red en tiempo de ejecucion, §0.2), mismo puente que ya usa el parte de rodaje
de R-02 (`scripts/tomas.py`).

Este modulo es el lado Python de ese volcado. A diferencia de `tomas.py`, que
fusiona en `estado.json`, R-03 esta marcada explicitamente "Migracion: No" en
`ROADMAP_PRODUCTO.md": no anade ningun contenedor nuevo al esquema de estado.
En su lugar, `FEEDBACK.md` -- un archivo nuevo dentro de la CARPETA DE SALIDA
del guion, no `roadmap/FEEDBACK.md` -- es en si mismo el registro persistente
(requisito 2): `registrar_tropiezos_en_feedback` le anade filas nuevas en
estado `nuevo`, y `tropiezos_marcados_por_escena` lo relee para que
`documento_revision.generar_documento_revision` destaque esos bloques en la
siguiente revision (requisito 3). No hace falta una copia en `estado.json`
para eso: el propio `FEEDBACK.md` ya sobrevive entre sesiones igual que
`guion-escenas.md`.

**Aviso de nombre:** `roadmap/FEEDBACK.md` (la bandeja de historias de usuario
del propio proyecto teleprompter, gestionada por el ciclo de Product Manager)
y el `FEEDBACK.md` que genera este modulo (uno por cada guion procesado, con
los tropiezos marcados durante SU grabacion) comparten nombre de archivo por
coincidencia de vocabulario, no de proposito ni de ubicacion: uno vive en el
repositorio de la skill: el otro, en la carpeta de salida de cada guion.

La skill no invoca esto sola: es Claude quien llama a
`cargar_registro_tropiezos`/`registrar_tropiezos_en_feedback` cuando el dueno
entrega el archivo exportado tras una sesion de rodaje, y
`tropiezos_marcados_por_escena` antes de la siguiente llamada a
`documento_revision.generar_documento_revision` (mismo patron que
`scripts/tomas.py` para el parte de rodaje).

Contrato completo del archivo exportado y de `FEEDBACK.md`: `references/contrato-tropiezos.md`.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from config import NOMBRE_ARCHIVO_FEEDBACK

ESTADO_NUEVO = "nuevo"

_ENCABEZADO_FEEDBACK = """\
# FEEDBACK — {guion}

> Bloques de locución marcados como tropiezo durante la grabación (R-03):
> «Escena»/«Bloque» identifican el mismo bloque de respiración numerado en
> `guion-escenas.md`; el texto es el que estaba en pantalla en el momento de
> marcarlo. Mientras una fila siga en estado `nuevo`, la siguiente revisión
> la destaca en `guion-escenas.md` para reescribirla a mano o con propuesta
> de la skill. Cambia la palabra `nuevo` por cualquier otra (p. ej.
> `resuelto`) para dejar de verla destacada sin tener que reescribir el
> texto.

| Fecha | Escena | Bloque | Texto exacto | Estado |
|-------|--------|--------|---------------|--------|
"""

_PATRON_FILA = re.compile(
    r"^\|\s*(?P<fecha>[^|]*)\|\s*(?P<escena>\d+)\s*\|\s*(?P<bloque>\d+)\s*\|"
    r"\s*(?P<texto>.*?)\s*\|\s*(?P<estado>[^|]*)\|\s*$"
)


class RegistroFeedbackError(Exception):
    """Registro de tropiezos ilegible, de otro guion o con estructura invalida.

    El mensaje del propio error ya es el texto accionable en espanol (mismo
    contrato que `entrada.EntradaError`/`estado.EstadoError`/`tomas.RegistroTomasError`).
    """


@dataclass(frozen=True)
class TropiezoBloque:
    """Un bloque de respiracion marcado como problematico durante la grabacion."""

    indice_bloque: int
    texto: str


@dataclass(frozen=True)
class EscenaTropiezos:
    """Todos los tropiezos marcados de una escena en una sesion de rodaje."""

    numero_escena: int
    titulo: str
    tropiezos: tuple[TropiezoBloque, ...]


@dataclass(frozen=True)
class RegistroTropiezos:
    """El archivo `.json` completo que exporta el boton "Exportar tropiezos"."""

    guion: str
    escenas: tuple[EscenaTropiezos, ...]


def _requerido(bruto: dict[str, Any], clave: str, contexto: str) -> Any:
    if clave not in bruto:
        raise RegistroFeedbackError(f"{contexto}: falta la clave obligatoria '{clave}'.")
    return bruto[clave]


def _tropiezo_desde_dict(bruto: Any, contexto: str) -> TropiezoBloque:
    if not isinstance(bruto, dict):
        raise RegistroFeedbackError(
            f"{contexto}: cada tropiezo debe ser un objeto, no {type(bruto).__name__}."
        )
    try:
        indice = int(_requerido(bruto, "indice_bloque", contexto))
    except (TypeError, ValueError) as excepcion:
        raise RegistroFeedbackError(
            f"{contexto}: 'indice_bloque' debe ser numerico ({excepcion})."
        ) from excepcion
    if indice < 0:
        raise RegistroFeedbackError(
            f"{contexto}: el indice de bloque no puede ser negativo ({indice})."
        )
    texto = _requerido(bruto, "texto", contexto)
    if not isinstance(texto, str) or not texto.strip():
        raise RegistroFeedbackError(f"{contexto}: 'texto' debe ser texto no vacio.")
    if "\n" in texto or "|" in texto:
        raise RegistroFeedbackError(
            f"{contexto}: 'texto' no puede contener saltos de línea ni '|' "
            "(rompería la tabla de FEEDBACK.md)."
        )
    return TropiezoBloque(indice_bloque=indice, texto=texto)


def _escena_desde_dict(bruto: Any, indice: int) -> EscenaTropiezos:
    contexto_escena = f"Escena en la posicion {indice} del registro de tropiezos"
    if not isinstance(bruto, dict):
        raise RegistroFeedbackError(
            f"{contexto_escena}: debe ser un objeto, no {type(bruto).__name__}."
        )
    try:
        numero = int(_requerido(bruto, "numero", contexto_escena))
    except (TypeError, ValueError) as excepcion:
        raise RegistroFeedbackError(
            f"{contexto_escena}: 'numero' debe ser numerico ({excepcion})."
        ) from excepcion
    titulo = bruto.get("titulo", "")
    if not isinstance(titulo, str):
        raise RegistroFeedbackError(f"Escena {numero}: el titulo debe ser texto.")
    tropiezos_bruto = bruto.get("tropiezos", [])
    if not isinstance(tropiezos_bruto, list):
        raise RegistroFeedbackError(f"Escena {numero}: 'tropiezos' debe ser una lista.")
    tropiezos = tuple(
        _tropiezo_desde_dict(tropiezo, f"Escena {numero}, tropiezo en la posicion {i}")
        for i, tropiezo in enumerate(tropiezos_bruto)
    )
    return EscenaTropiezos(numero_escena=numero, titulo=titulo, tropiezos=tropiezos)


def cargar_registro_tropiezos(ruta: Path, nombre_guion: str) -> RegistroTropiezos:
    """Lee y valida el `.json` exportado por "Exportar tropiezos".

    `nombre_guion` es el mismo identificador con el que se genero el reproductor
    (`generar_reproductor_html(..., nombre_guion=...)`, tambien `datos.guion` en
    `guion.js`): un archivo de otro guion se rechaza en vez de fusionarse por
    error, mismo criterio que `tomas.cargar_parte_de_rodaje`.
    """
    if not ruta.exists():
        raise RegistroFeedbackError(f"No existe el archivo de tropiezos: {ruta}")
    try:
        bruto = json.loads(ruta.read_text(encoding="utf-8"))
    except json.JSONDecodeError as excepcion:
        raise RegistroFeedbackError(
            f"El archivo de tropiezos no es JSON valido: {ruta}. Detalle: {excepcion}"
        ) from excepcion
    if not isinstance(bruto, dict):
        raise RegistroFeedbackError(f"El archivo de tropiezos debe contener un objeto: {ruta}")

    guion_archivo = bruto.get("guion")
    if guion_archivo != nombre_guion:
        raise RegistroFeedbackError(
            f'El registro de tropiezos es de otro guion ("{guion_archivo}"), '
            f'no de "{nombre_guion}".'
        )
    escenas_bruto = bruto.get("escenas", [])
    if not isinstance(escenas_bruto, list):
        raise RegistroFeedbackError(f"'escenas' debe ser una lista en {ruta}.")

    escenas = tuple(
        _escena_desde_dict(escena, indice) for indice, escena in enumerate(escenas_bruto)
    )
    return RegistroTropiezos(guion=guion_archivo, escenas=escenas)


def _fila_feedback(fecha: str, numero_escena: int, tropiezo: TropiezoBloque) -> str:
    return (
        f"| {fecha} | {numero_escena} | {tropiezo.indice_bloque} | "
        f"{tropiezo.texto} | {ESTADO_NUEVO} |"
    )


def registrar_tropiezos_en_feedback(
    carpeta_salida: Path,
    registro: RegistroTropiezos,
    fecha: str | None = None,
) -> int:
    """Anade a `FEEDBACK.md` (carpeta de salida del guion) una fila `nuevo`
    por cada tropiezo del `registro` que todavia no este en el archivo
    (requisito 2). Crea el archivo con su cabecera si no existia. Si ya
    existia, se copia antes a `<nombre>.bak-<marca>` -- mismo tratamiento que
    `documento_revision.guardar_documento_revision` (invariante (d) de §0.2:
    sin sobrescritura destructiva de un archivo que el dueno puede haber
    editado a mano, p. ej. cambiando `nuevo` por `resuelto`).

    Nunca borra ni reescribe una fila existente: solo anade filas nuevas al
    final. Devuelve cuantas filas nuevas se anadieron (0 si el registro no
    trae ningun tropiezo que no estuviera ya)."""
    fecha = fecha or datetime.now(UTC).date().isoformat()
    ruta = carpeta_salida / NOMBRE_ARCHIVO_FEEDBACK

    if ruta.exists():
        texto_existente = ruta.read_text(encoding="utf-8")
    else:
        texto_existente = _ENCABEZADO_FEEDBACK.format(guion=registro.guion)

    existentes = {
        (fila.numero_escena, fila.indice_bloque, fila.texto)
        for fila in _filas_existentes(texto_existente)
    }

    filas_nuevas = []
    for escena in registro.escenas:
        for tropiezo in escena.tropiezos:
            clave = (escena.numero_escena, tropiezo.indice_bloque, tropiezo.texto)
            if clave in existentes:
                continue
            existentes.add(clave)
            filas_nuevas.append(_fila_feedback(fecha, escena.numero_escena, tropiezo))

    if not filas_nuevas:
        return 0

    if ruta.exists():
        marca = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        copia_seguridad = ruta.with_name(f"{ruta.name}.bak-{marca}")
        copia_seguridad.write_bytes(ruta.read_bytes())

    separador = "" if texto_existente.endswith("\n") else "\n"
    texto_final = texto_existente + separador + "\n".join(filas_nuevas) + "\n"
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    ruta.write_text(texto_final, encoding="utf-8")
    return len(filas_nuevas)


@dataclass(frozen=True)
class _FilaFeedback:
    numero_escena: int
    indice_bloque: int
    texto: str
    estado: str


def _filas_existentes(texto: str) -> list[_FilaFeedback]:
    filas = []
    for linea in texto.splitlines():
        coincidencia = _PATRON_FILA.match(linea.strip())
        if coincidencia is None:
            continue
        # La propia fila de cabecera de la tabla ("Fecha | Escena | Bloque |
        # ...") tambien casaria el patron generico salvo que 'Escena'/'Bloque'
        # no son numericos -- `\d+` ya la descarta sin necesitar un caso especial.
        filas.append(
            _FilaFeedback(
                numero_escena=int(coincidencia.group("escena")),
                indice_bloque=int(coincidencia.group("bloque")),
                texto=coincidencia.group("texto"),
                estado=coincidencia.group("estado").strip(),
            )
        )
    return filas


def tropiezos_marcados_por_escena(carpeta_salida: Path) -> dict[int, frozenset[str]]:
    """Lee `FEEDBACK.md` (si existe) y devuelve, por numero de escena, el
    conjunto de textos de bloque todavia en estado `nuevo` (requisito 3): la
    entrada que usa `documento_revision.generar_documento_revision` para
    destacar esos bloques en la siguiente revision. Una fila cuyo estado ya no
    es `nuevo` -- el dueno la cambio a mano -- deja de destacarse aunque el
    texto del bloque no haya cambiado."""
    ruta = carpeta_salida / NOMBRE_ARCHIVO_FEEDBACK
    if not ruta.exists():
        return {}
    resultado: dict[int, set[str]] = {}
    for fila in _filas_existentes(ruta.read_text(encoding="utf-8")):
        if fila.estado.lower() != ESTADO_NUEVO:
            continue
        resultado.setdefault(fila.numero_escena, set()).add(fila.texto)
    return {escena: frozenset(textos) for escena, textos in resultado.items()}
