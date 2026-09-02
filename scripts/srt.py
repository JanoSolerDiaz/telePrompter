"""Exportador de subtitulos `.srt` borrador (tarea T-27).

Arranca los subtitulos en la fase de montaje sin partir de cero: un subtitulo por
bloque de respiracion (T-11) con los tiempos ya calculados por el motor de tiempos
(T-12), sobre el TEXTO LOCUTADO FINAL -- el que trae `ResultadoTiempos` tras una
revalidacion (T-17), con las reescrituras aceptadas ya materializadas -- no el
original del guion (requisito 4). Este modulo no calcula ningun tiempo por su
cuenta: consume `tiempos.BloqueConTiempo` tal cual, la unica fuente de tiempos del
proyecto (T-12, requisito 4).

Agrupacion (requisito 1): un bloque cuya duracion total (palabras + pausa) no llega
a `Configuracion.srt_duracion_minima_segundos` se funde con el siguiente bloque de la
misma escena, para que no parpadee un subtitulo en pantalla menos de un instante.
Nunca cruza un fin de escena (`tiempos.PAUSA_FIN_ESCENA`): dos escenas nunca
comparten subtitulo.

Particion limpia (requisito 3): si el texto de un grupo no cabe en
`Configuracion.srt_lineas_max_por_subtitulo` lineas de
`Configuracion.srt_caracteres_por_linea_max` caracteres cada una, se reparte en
varios subtitulos consecutivos -- nunca se trunca ni se descarta texto (invariante
(a), §0.2) -- con el tiempo del grupo repartido en proporcion a las palabras de cada
reparto, envolviendo siempre por palabra completa.

Formato (requisito 2): `.srt` estandar (indice, marca de tiempo
`HH:MM:SS,mmm --> HH:MM:SS,mmm`, texto, linea en blanco), UTF-8, con opcion de
anteponer BOM (`Configuracion.srt_con_bom`) para editores de Windows que lo
prefieran. `validar_srt` aplica las mismas reglas que un lector estricto tipo
ffmpeg (requisito 5): indice secuencial, marca de tiempo valida, inicio anterior al
fin, sin solapes ni tiempos decrecientes entre subtitulos consecutivos.
"""

from __future__ import annotations

import re
import textwrap
from dataclasses import dataclass
from pathlib import Path

from config import NOMBRE_ARCHIVO_SRT, Configuracion
from tiempos import PAUSA_FIN_ESCENA, BloqueConTiempo, ResultadoTiempos


@dataclass(frozen=True)
class EntradaSrt:
    """Un subtitulo ya formado: indice 1-based, intervalo de tiempo y texto (una
    o mas lineas, segun `Configuracion.srt_lineas_max_por_subtitulo`)."""

    indice: int
    inicio_segundos: float
    fin_segundos: float
    lineas: tuple[str, ...]


def formatear_marca_tiempo(segundos: float) -> str:
    """`segundos` -> `HH:MM:SS,mmm`, la marca de tiempo estandar de un `.srt`."""
    total_ms = round(max(segundos, 0.0) * 1000)
    horas, resto_ms = divmod(total_ms, 3_600_000)
    minutos, resto_ms = divmod(resto_ms, 60_000)
    segundos_enteros, milisegundos = divmod(resto_ms, 1000)
    return f"{horas:02d}:{minutos:02d}:{segundos_enteros:02d},{milisegundos:03d}"


def _agrupar_bloques_cortos(
    bloques: list[BloqueConTiempo], configuracion: Configuracion
) -> list[list[BloqueConTiempo]]:
    """Funde bloques consecutivos de una misma escena cuya duracion acumulada
    (palabras + pausa, `fin_segundos - inicio_segundos` del grupo) no llega al
    minimo configurado (requisito 1), sin cruzar nunca un fin de escena. Con
    `srt_duracion_minima_segundos=0` ningun grupo queda nunca por debajo del
    minimo, asi que cada bloque cierra su propio grupo de inmediato -- agrupar
    queda desactivado sin necesitar un interruptor aparte."""
    grupos: list[list[BloqueConTiempo]] = []
    grupo_actual: list[BloqueConTiempo] = []
    for bloque_con_tiempo in bloques:
        grupo_actual.append(bloque_con_tiempo)
        duracion_grupo = grupo_actual[-1].fin_segundos - grupo_actual[0].inicio_segundos
        fin_de_escena = bloque_con_tiempo.tipo_pausa == PAUSA_FIN_ESCENA
        if fin_de_escena or duracion_grupo >= configuracion.srt_duracion_minima_segundos:
            grupos.append(grupo_actual)
            grupo_actual = []
    if grupo_actual:  # cola sin cerrar (guion sin ningun bloque marcado fin_de_escena)
        grupos.append(grupo_actual)
    return grupos


def _envolver_texto(texto: str, caracteres_por_linea_max: int) -> list[str]:
    """Envuelve `texto` en lineas de como maximo `caracteres_por_linea_max`
    caracteres, siempre por palabra completa: nunca corta una palabra a la
    mitad, aunque eso deje alguna linea por encima del limite en el caso
    extremo de una palabra mas larga que el propio limite."""
    return (
        textwrap.wrap(
            texto,
            width=caracteres_por_linea_max,
            break_long_words=False,
            break_on_hyphens=False,
        )
        or [""]
    )


def _paginar(lineas: list[str], lineas_max: int) -> list[list[str]]:
    """Reparte `lineas` en paginas de como maximo `lineas_max` lineas cada una,
    en orden: la primera pagina se lee antes que la segunda, etc."""
    return [lineas[indice : indice + lineas_max] for indice in range(0, len(lineas), lineas_max)]


def _entradas_de_grupo(
    grupo: list[BloqueConTiempo], indice_inicial: int, configuracion: Configuracion
) -> list[EntradaSrt]:
    """Convierte un grupo de bloques ya fundidos (T-11 los da en 6-12 palabras;
    la agrupacion de arriba puede fundir varios) en una o mas `EntradaSrt`: una
    sola si el texto cabe en el limite de lineas/caracteres configurado, varias
    -- "particion limpia" -- si no cabe (requisito 3). Nunca trunca ni descarta
    una palabra (invariante (a), §0.2): todo lo que dice el grupo aparece en
    alguna de las entradas resultantes. El tiempo del grupo se reparte entre
    las paginas en proporcion a sus palabras; la ultima pagina siempre cierra
    exactamente en `fin_segundos` del grupo, sin deriva de coma flotante."""
    texto = " ".join(bloque_con_tiempo.bloque.texto for bloque_con_tiempo in grupo)
    lineas = _envolver_texto(texto, configuracion.srt_caracteres_por_linea_max)
    paginas = _paginar(lineas, configuracion.srt_lineas_max_por_subtitulo)

    inicio_grupo = grupo[0].inicio_segundos
    fin_grupo = grupo[-1].fin_segundos
    duracion_total = fin_grupo - inicio_grupo
    palabras_por_pagina = [sum(len(linea.split()) for linea in pagina) for pagina in paginas]
    palabras_totales = sum(palabras_por_pagina) or 1

    entradas: list[EntradaSrt] = []
    cursor_segundos = inicio_grupo
    for indice_pagina, (pagina, palabras_pagina) in enumerate(
        zip(paginas, palabras_por_pagina, strict=True)
    ):
        es_ultima_pagina = indice_pagina == len(paginas) - 1
        fin_pagina = (
            fin_grupo
            if es_ultima_pagina
            else cursor_segundos + duracion_total * (palabras_pagina / palabras_totales)
        )
        entradas.append(
            EntradaSrt(
                indice=indice_inicial + indice_pagina,
                inicio_segundos=cursor_segundos,
                fin_segundos=fin_pagina,
                lineas=tuple(pagina),
            )
        )
        cursor_segundos = fin_pagina
    return entradas


def generar_entradas_srt(
    resultado_tiempos: ResultadoTiempos, configuracion: Configuracion | None = None
) -> list[EntradaSrt]:
    """Construye la lista completa de subtitulos a partir de tiempos ya
    calculados (T-12): agrupa (requisito 1), envuelve y reparte en paginas
    (requisito 3), y numera las entradas resultantes en orden. Pasa
    `resultado_tiempos` de la ultima revalidacion (T-17) para que el texto sea
    el locutado final con las reescrituras aceptadas ya materializadas
    (requisito 4) -- esta funcion no distingue el origen, solo consume
    `bloque.texto` tal cual le llega."""
    configuracion = configuracion or Configuracion()
    entradas: list[EntradaSrt] = []
    for grupo in _agrupar_bloques_cortos(resultado_tiempos.bloques, configuracion):
        entradas.extend(_entradas_de_grupo(grupo, len(entradas) + 1, configuracion))
    return entradas


def formatear_srt(entradas: list[EntradaSrt]) -> str:
    """Serializa las entradas ya construidas al formato `.srt` estandar
    (requisito 2): indice, marca de tiempo, texto, linea en blanco."""
    bloques_texto = [
        "\n".join(
            (
                str(entrada.indice),
                f"{formatear_marca_tiempo(entrada.inicio_segundos)} --> "
                f"{formatear_marca_tiempo(entrada.fin_segundos)}",
                *entrada.lineas,
            )
        )
        for entrada in entradas
    ]
    return "\n\n".join(bloques_texto) + ("\n" if bloques_texto else "")


def exportar_srt(
    resultado_tiempos: ResultadoTiempos, configuracion: Configuracion | None = None
) -> str:
    """Genera el contenido completo del `.srt` borrador: orquesta
    `generar_entradas_srt` + `formatear_srt`, el punto de entrada normal del
    modulo."""
    configuracion = configuracion or Configuracion()
    return formatear_srt(generar_entradas_srt(resultado_tiempos, configuracion))


def guardar_srt(
    contenido: str, carpeta_salida: Path, configuracion: Configuracion | None = None
) -> Path:
    """Escribe el `.srt` en la carpeta de salida del guion (regla de
    aislamiento, §0.2): nunca fuera de `carpeta_salida`."""
    configuracion = configuracion or Configuracion()
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    destino = carpeta_salida / NOMBRE_ARCHIVO_SRT
    codificacion = "utf-8-sig" if configuracion.srt_con_bom else "utf-8"
    destino.write_text(contenido, encoding=codificacion)
    return destino


_PATRON_MARCA_TIEMPO = re.compile(
    r"^(\d{2,}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2,}):(\d{2}):(\d{2}),(\d{3})\s*$"
)


def _segundos_de_grupos(horas: str, minutos: str, segundos: str, milisegundos: str) -> float:
    return int(horas) * 3600 + int(minutos) * 60 + int(segundos) + int(milisegundos) / 1000


def validar_srt(contenido: str, configuracion: Configuracion | None = None) -> list[str]:
    """Valida `contenido` con las mismas reglas que aplica un lector estricto de
    `.srt` como ffmpeg (requisito 5): un bloque es indice + marca de tiempo +
    una o mas lineas de texto, separado del siguiente por una linea en blanco;
    el indice es secuencial desde 1; la marca de tiempo respeta el formato
    exacto `HH:MM:SS,mmm --> HH:MM:SS,mmm` con el inicio estrictamente anterior
    al fin; ningun subtitulo empieza antes de que termine el anterior (ni
    solape ni retroceso); ninguna linea de texto supera
    `Configuracion.srt_caracteres_por_linea_max`. Lista vacia == valido."""
    configuracion = configuracion or Configuracion()
    problemas: list[str] = []
    bloques = [bloque for bloque in contenido.strip("\n").split("\n\n") if bloque.strip()]
    fin_anterior_segundos: float | None = None
    for numero_bloque, bloque in enumerate(bloques, start=1):
        lineas = bloque.split("\n")
        if len(lineas) < 3:
            problemas.append(
                f"Bloque {numero_bloque}: le faltan lineas (se esperan indice, marca de "
                "tiempo y al menos una linea de texto)."
            )
            continue
        indice_texto, marca_texto, *lineas_subtitulo = lineas
        if not indice_texto.strip().isdigit() or int(indice_texto) != numero_bloque:
            problemas.append(
                f"Bloque {numero_bloque}: el indice '{indice_texto}' no es secuencial desde 1."
            )
        coincidencia = _PATRON_MARCA_TIEMPO.match(marca_texto)
        if coincidencia is None:
            problemas.append(
                f"Bloque {numero_bloque}: marca de tiempo mal formada: '{marca_texto}'."
            )
            continue
        h1, m1, s1, ms1, h2, m2, s2, ms2 = coincidencia.groups()
        inicio_segundos = _segundos_de_grupos(h1, m1, s1, ms1)
        fin_segundos = _segundos_de_grupos(h2, m2, s2, ms2)
        if fin_segundos <= inicio_segundos:
            problemas.append(
                f"Bloque {numero_bloque}: el fin de la marca de tiempo no es posterior al "
                f"inicio ('{marca_texto}')."
            )
        if fin_anterior_segundos is not None and inicio_segundos < fin_anterior_segundos:
            problemas.append(
                f"Bloque {numero_bloque}: empieza antes de que termine el subtitulo anterior "
                "(solape o tiempo decreciente)."
            )
        fin_anterior_segundos = fin_segundos
        if not lineas_subtitulo:
            problemas.append(f"Bloque {numero_bloque}: no tiene ninguna linea de texto.")
        for linea in lineas_subtitulo:
            if len(linea) > configuracion.srt_caracteres_por_linea_max:
                problemas.append(
                    f"Bloque {numero_bloque}: una linea supera "
                    f"{configuracion.srt_caracteres_por_linea_max} caracteres "
                    f"({len(linea)}): '{linea}'."
                )
    return problemas
