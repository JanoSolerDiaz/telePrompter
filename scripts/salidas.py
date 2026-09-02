"""Selector de salidas por validacion (tarea T-30).

Ata en una sola canalizacion los cuatro generadores ya completos --
`reproductor.py` (T-18), `srt.py` (T-27), `pdf.py` (T-28) y `pptx.py`
(T-29) -- sin duplicar ni una linea de lo que cada uno ya hace:

1. `construir_pregunta_salidas` arma la pregunta de opcion multiple
   (requisito 1) con la ultima seleccion registrada en
   `estado.salidas_generadas` como sugerencia (requisito 2), nunca como
   decision silenciosa. Quien pregunta de verdad al dueno es Claude, no
   este modulo: mismo patron que `parser.DeteccionEscenasAmbiguaError`
   (T-08), que deja la ambiguedad como datos estructurados para que la
   sesion formule la pregunta y la respuesta vuelva ya decidida.
2. `generar_salidas_seleccionadas` genera cada tipo seleccionado de forma
   independiente (requisito 3): la excepcion de una salida nunca impide
   las demas, y queda reflejada como salida omitida con su motivo. Una
   salida que ya el propio modulo (T-28/T-29) marca como latente por una
   dependencia externa ausente se refleja igual, sin fusionarla con un
   fallo real.
3. `ResumenSalidas` es el resumen final (requisito 4): ruta y tamano de
   cada archivo generado, mas las omitidas (no seleccionadas o fallidas)
   y las latentes (seleccionadas, con lo generable ya en disco, pero con
   una parte pendiente de instalar algo) con su motivo.
4. `registrar_generacion` anexa el resultado a `estado.salidas_generadas`
   (contenedor generico ya reservado desde T-07, sin migracion nueva:
   T-30 no la requiere) para que la proxima pregunta sugiera la misma
   seleccion.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from config import Configuracion
from estado import EstadoProyecto, marca_de_tiempo
from parser import ResultadoParseo
from pdf import exportar_pdf
from pptx import exportar_pptx
from presentacion import Nivel, mostrar, titulo
from reproductor import generar_reproductor_html, guardar_reproductor
from srt import exportar_srt, guardar_srt
from tiempos import ResultadoTiempos


class TipoSalida(str, Enum):
    """Las cuatro salidas de la skill (requisito 1), en el orden en que se
    ofrecen siempre en la pregunta y en el resumen."""

    HTML = "html"
    PPTX = "pptx"
    PDF = "pdf"
    SRT = "srt"


DESCRIPCION_SALIDA: dict[TipoSalida, str] = {
    TipoSalida.HTML: "Reproductor .html (principal, para grabar)",
    TipoSalida.PPTX: "Presentación .pptx con marca 480",
    TipoSalida.PDF: "Documento .pdf con marca 480",
    TipoSalida.SRT: "Subtítulos .srt borrador",
}

TODAS_LAS_SALIDAS: tuple[TipoSalida, ...] = (
    TipoSalida.HTML,
    TipoSalida.PPTX,
    TipoSalida.PDF,
    TipoSalida.SRT,
)


@dataclass(frozen=True)
class OpcionSalida:
    """Una fila de la pregunta de opcion multiple: la salida, su
    descripcion legible y si viene marcada como sugerencia."""

    tipo: TipoSalida
    descripcion: str
    sugerida: bool


@dataclass(frozen=True)
class PreguntaSeleccionSalidas:
    """La pregunta que Claude formula al dueno en cada validacion
    (requisito 1). `opciones` trae siempre las cuatro salidas; la
    seleccion final la decide el dueno, nunca este modulo."""

    opciones: tuple[OpcionSalida, ...]

    @property
    def sugerencia(self) -> tuple[TipoSalida, ...]:
        return tuple(opcion.tipo for opcion in self.opciones if opcion.sugerida)


def _ultima_seleccion(estado: EstadoProyecto) -> tuple[TipoSalida, ...] | None:
    """La seleccion de la ultima entrada de `estado.salidas_generadas`, o
    `None` si no hay ninguna generacion previa registrada (requisito 2:
    la sugerencia nunca sustituye a preguntar, solo la precompleta)."""
    for entrada in reversed(estado.salidas_generadas):
        crudos = entrada.get("seleccion")
        if crudos is None:
            continue
        return tuple(TipoSalida(valor) for valor in crudos)
    return None


def construir_pregunta_salidas(estado: EstadoProyecto) -> PreguntaSeleccionSalidas:
    """Construye la pregunta de opcion multiple (requisito 1) con la
    ultima seleccion marcada como sugerencia (requisito 2); a falta de
    historico, sugiere las cuatro salidas."""
    sugerencia = _ultima_seleccion(estado)
    sugeridas = sugerencia if sugerencia is not None else TODAS_LAS_SALIDAS
    return PreguntaSeleccionSalidas(
        opciones=tuple(
            OpcionSalida(tipo, DESCRIPCION_SALIDA[tipo], tipo in sugeridas)
            for tipo in TODAS_LAS_SALIDAS
        )
    )


@dataclass(frozen=True)
class SeleccionSalidas:
    """La respuesta del dueno a `PreguntaSeleccionSalidas`: que salidas
    generar en esta pasada. Vacia es valida (el dueno puede no querer
    ninguna); este modulo nunca la completa por su cuenta."""

    tipos: tuple[TipoSalida, ...]


@dataclass(frozen=True)
class ArchivoGenerado:
    """Un archivo real ya escrito en disco (requisito 4: ruta y tamano)."""

    tipo: TipoSalida
    ruta: Path
    tamano_bytes: int


@dataclass(frozen=True)
class SalidaOmitida:
    """Una salida sin archivo: no se selecciono, o la generacion fallo."""

    tipo: TipoSalida
    motivo: str


@dataclass(frozen=True)
class SalidaLatente:
    """Una salida seleccionada cuya parte generable ya existe en disco,
    pero cuyo artefacto final depende de algo ausente en esta maquina
    (Chrome/Edge para el `.pdf` real, T-28; la skill de marca para el
    `.pptx` real, T-29). Nunca se confunde con un fallo: el motivo es
    siempre la falta de una dependencia externa, no un error del codigo."""

    tipo: TipoSalida
    motivo: str


@dataclass(frozen=True)
class ResumenSalidas:
    """Resultado final de una pasada de generacion (requisito 4)."""

    generadas: tuple[ArchivoGenerado, ...]
    omitidas: tuple[SalidaOmitida, ...]
    latentes: tuple[SalidaLatente, ...]

    def como_dict(self) -> dict[str, Any]:
        """Forma serializable para anexar a `estado.salidas_generadas`."""
        return {
            "generadas": [
                {"tipo": a.tipo.value, "ruta": str(a.ruta), "tamano_bytes": a.tamano_bytes}
                for a in self.generadas
            ],
            "omitidas": [{"tipo": o.tipo.value, "motivo": o.motivo} for o in self.omitidas],
            "latentes": [
                {"tipo": latente.tipo.value, "motivo": latente.motivo} for latente in self.latentes
            ],
        }

    def mostrar_resumen(self) -> None:
        """Muestra el resumen final al dueño por `presentacion.py` (requisito
        4): ruta y tamaño de cada archivo generado, y el motivo de cada
        salida omitida o latente."""
        titulo("Resumen de salidas")
        for archivo in self.generadas:
            mostrar(
                f"{archivo.tipo.value}: {archivo.ruta} ({archivo.tamano_bytes} bytes)", Nivel.OK
            )
        for latente in self.latentes:
            mostrar(f"{latente.tipo.value}: LATENTE — {latente.motivo}", Nivel.AVISO)
        for omitida in self.omitidas:
            mostrar(f"{omitida.tipo.value}: omitida — {omitida.motivo}", Nivel.INFO)


def _generar_html(
    resultado: ResultadoParseo,
    resultado_tiempos: ResultadoTiempos,
    carpeta_salida: Path,
    nombre_guion: str,
    configuracion: Configuracion,
) -> list[ArchivoGenerado]:
    pagina = generar_reproductor_html(resultado, resultado_tiempos, nombre_guion, configuracion)
    ruta = guardar_reproductor(pagina, carpeta_salida)
    return [ArchivoGenerado(TipoSalida.HTML, ruta, ruta.stat().st_size)]


def _generar_srt(
    resultado: ResultadoParseo,
    resultado_tiempos: ResultadoTiempos,
    carpeta_salida: Path,
    nombre_guion: str,
    configuracion: Configuracion,
) -> list[ArchivoGenerado]:
    del resultado, nombre_guion  # el .srt no necesita ni el parseo ni el nombre
    contenido = exportar_srt(resultado_tiempos, configuracion)
    ruta = guardar_srt(contenido, carpeta_salida, configuracion)
    return [ArchivoGenerado(TipoSalida.SRT, ruta, ruta.stat().st_size)]


def _generar_pdf(
    resultado: ResultadoParseo,
    resultado_tiempos: ResultadoTiempos,
    carpeta_salida: Path,
    nombre_guion: str,
    configuracion: Configuracion,
) -> tuple[list[ArchivoGenerado], list[SalidaLatente]]:
    resultado_pdf = exportar_pdf(
        resultado, resultado_tiempos, carpeta_salida, nombre_guion, configuracion
    )
    generadas = [
        ArchivoGenerado(
            TipoSalida.PDF, resultado_pdf.ruta_html, resultado_pdf.ruta_html.stat().st_size
        )
    ]
    if resultado_pdf.ruta_pdf is not None:
        generadas.append(
            ArchivoGenerado(
                TipoSalida.PDF, resultado_pdf.ruta_pdf, resultado_pdf.ruta_pdf.stat().st_size
            )
        )
        return generadas, []
    return generadas, [SalidaLatente(TipoSalida.PDF, resultado_pdf.mensaje)]


def _generar_pptx(
    resultado: ResultadoParseo,
    resultado_tiempos: ResultadoTiempos,
    carpeta_salida: Path,
    nombre_guion: str,
    configuracion: Configuracion,
) -> tuple[list[ArchivoGenerado], list[SalidaLatente]]:
    resultado_pptx = exportar_pptx(
        resultado, resultado_tiempos, carpeta_salida, nombre_guion, configuracion
    )
    generadas = [
        ArchivoGenerado(
            TipoSalida.PPTX,
            resultado_pptx.ruta_tarjetas_json,
            resultado_pptx.ruta_tarjetas_json.stat().st_size,
        ),
        ArchivoGenerado(
            TipoSalida.PPTX, resultado_pptx.ruta_brief, resultado_pptx.ruta_brief.stat().st_size
        ),
    ]
    if resultado_pptx.skill_disponible:
        return generadas, []
    return generadas, [SalidaLatente(TipoSalida.PPTX, resultado_pptx.mensaje)]


def generar_salidas_seleccionadas(
    seleccion: SeleccionSalidas,
    resultado: ResultadoParseo,
    resultado_tiempos: ResultadoTiempos,
    carpeta_salida: Path,
    nombre_guion: str = "guion",
    configuracion: Configuracion | None = None,
) -> ResumenSalidas:
    """Genera cada salida seleccionada de forma independiente (requisito
    3): la excepcion de una nunca impide las demas -- se captura y se
    convierte en una `SalidaOmitida` con el motivo del fallo, en vez de
    propagarse y tumbar la pasada entera. Las no seleccionadas quedan
    omitidas con un motivo neutro."""
    configuracion = configuracion or Configuracion()
    generadas: list[ArchivoGenerado] = []
    omitidas: list[SalidaOmitida] = []
    latentes: list[SalidaLatente] = []

    for tipo in TODAS_LAS_SALIDAS:
        if tipo not in seleccion.tipos:
            omitidas.append(SalidaOmitida(tipo, "no seleccionada por el dueño en esta pasada."))
            continue
        try:
            if tipo is TipoSalida.HTML:
                generadas.extend(
                    _generar_html(
                        resultado, resultado_tiempos, carpeta_salida, nombre_guion, configuracion
                    )
                )
            elif tipo is TipoSalida.SRT:
                generadas.extend(
                    _generar_srt(
                        resultado, resultado_tiempos, carpeta_salida, nombre_guion, configuracion
                    )
                )
            elif tipo is TipoSalida.PDF:
                nuevas, nuevas_latentes = _generar_pdf(
                    resultado, resultado_tiempos, carpeta_salida, nombre_guion, configuracion
                )
                generadas.extend(nuevas)
                latentes.extend(nuevas_latentes)
            elif tipo is TipoSalida.PPTX:
                nuevas, nuevas_latentes = _generar_pptx(
                    resultado, resultado_tiempos, carpeta_salida, nombre_guion, configuracion
                )
                generadas.extend(nuevas)
                latentes.extend(nuevas_latentes)
        except Exception as excepcion:  # una salida rota no tumba la pasada
            omitidas.append(SalidaOmitida(tipo, f"fallo al generar: {excepcion}"))

    return ResumenSalidas(tuple(generadas), tuple(omitidas), tuple(latentes))


def registrar_generacion(
    estado: EstadoProyecto, seleccion: SeleccionSalidas, resumen: ResumenSalidas
) -> None:
    """Anexa esta pasada a `estado.salidas_generadas` (append-only, mismo
    contenedor generico reservado desde T-07): la proxima
    `construir_pregunta_salidas` la lee para sugerir la misma seleccion
    (requisito 2). Quien llama sigue siendo responsable de `guardar_estado`
    despues -- este modulo no decide cuando persistir."""
    entrada: dict[str, Any] = {
        "marca_de_tiempo": marca_de_tiempo(),
        "seleccion": [tipo.value for tipo in seleccion.tipos],
    }
    entrada.update(resumen.como_dict())
    estado.salidas_generadas.append(entrada)
