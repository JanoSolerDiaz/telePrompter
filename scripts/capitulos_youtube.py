"""Capitulos de YouTube con marcas de tiempo reales (tarea R-07).

T-08 ya detecta y conserva integra la seccion auxiliar `## Capitulos (para la
descripcion del video)` de los guiones reales, pero hasta ahora ese contenido no
salia de ahi: el formador tenia que volver a cronometrar el video ya montado a
mano para pegar los capitulos en la descripcion de YouTube. Con R-02 (registro de
tomas) existe ya el dato que hace falta -- cuanto duro de verdad cada escena buena
-- asi que este modulo une dos datos que el producto ya tiene, sin calcular
tiempos ni reimplementar reglas de guion por su cuenta: parte del
`ResultadoParseo` de T-08 (para leer los titulos de capitulo) y del
`ResultadoTiempos` ya calculado por T-12 (para la duracion estimada de cada
escena, en el mismo orden en que aparecen en el guion), y reutiliza
`tomas.duracion_toma_buena` (R-02/R-04/R-05) para la duracion real.

Requisito 1 (emparejar capitulos y escenas por orden): `_titulos_capitulos` lee
las filas de la tabla Markdown de la seccion auxiliar cuyo titulo empieza por
`Configuracion.titulo_seccion_capitulos` ("Capitulos" por defecto, el mismo
prefijo que ya reconoce `parser._en_lista_negra`) y devuelve los titulos de su
columna "Capitulo", en el orden en que aparecen las filas. `calcular_capitulos`
empareja esa lista, POSICIONALMENTE, con las escenas del guion en el mismo orden
en que aparecen (`resultado_tiempos.escenas`, que conserva el orden de
`parser.py`) -- nunca por texto ni por numero de escena, tal como pide el
requisito ("en el mismo orden en que aparecen ambos"). Si las dos listas no
tienen la misma longitud, se empareja hasta la mas corta: no es un error, los
tres guiones reales que traen la seccion ya cuadran 1:1, pero nada obliga a que
siga siendo asi.

Requisito 2 (tiempo real cuando hay evidencia, estimado si no, nunca mezclado en
silencio): para cada escena, en orden, se usa la duracion REAL de su toma buena
(`tomas.duracion_toma_buena`) si existe; si no, su duracion ESTIMADA de T-12
(`TiempoEscena.duracion_estimada_segundos`) -- el cursor de tiempo se acumula de
forma continua escena a escena, igual que `tiempos.py` y `srt_alineado.py`, asi
que las marcas siguen siendo una unica linea de tiempo sin huecos. Que una escena
concreta se apoye en tiempo real o estimado queda registrado en
`ResultadoCapitulos.escenas_sin_toma_buena` (mismo nombre de campo que
`ResultadoAlineacion` de R-05, mismo criterio); en cuanto CUALQUIERA de las
escenas que aportan una marca reportada depende de la estimacion,
`formatear_capitulos_youtube` antepone una nota explicita como primera linea del
archivo (criterio de aceptacion literal: "sin tomas registradas... la primera
linea del archivo lo advierte") -- nunca dos fuentes de tiempo sin decir cual es
cual.

Requisito 3 (formato exacto de YouTube): `formatear_capitulos_youtube` antepone
siempre "0:00" a la primera marca (la primera escena arranca en el cursor 0.0 por
construccion) y omite -- sin perder el capitulo en ningun otro sitio, solo no
aparece como marca propia en este archivo derivado -- cualquier marca posterior a
menos de `Configuracion.capitulos_youtube_marca_minima_segundos` (10 s por
defecto, el minimo de la propia plataforma) de la ultima marca que si se
conservo.

Requisito 4 (sin seccion Capitulos, no se genera nada en silencio):
`calcular_capitulos` devuelve `capitulos=()` con `motivo_sin_generar` explicito
cuando el guion no trae la seccion, o cuando la trae pero no se pudo leer ningun
titulo de su tabla; `formatear_capitulos_youtube` devuelve `None` en ese caso y
`guardar_capitulos_youtube` no debe llamarse.

R-11 (hallazgo #17): cuando sobran TITULOS de capitulo (mas titulos que
escenas -- el caso simetrico al de arriba, que ya emparejaba "hasta el mas
corto" sin avisar de los titulos que se quedaban fuera) los titulos
descartados quedan ahora en `ResultadoCapitulos.titulos_sobrantes`, en vez de
desaparecer sin rastro: la seccion auxiliar del guion sigue integra (no es
perdida de la fuente), pero quien orquesta la generacion puede avisar al
dueno de que un titulo de capitulo no llego a `capitulos-youtube.txt`.

Requisito 5 (regenerable sin intervencion manual): este modulo no persiste nada
por si mismo -- es una funcion pura del `ResultadoParseo`/`ResultadoTiempos` y de
`EstadoProyecto.tomas` que se le pasen, igual que `srt_alineado.py`. La skill no
lo invoca sola: es Claude quien lo llama de nuevo cada vez que revalida el guion
o el dueno cierra una tanda de tomas nueva, mismo patron que el `.srt` alineado
(R-05).
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from config import NOMBRE_ARCHIVO_CAPITULOS_YOUTUBE, Configuracion
from parser import ResultadoParseo, SeccionAuxiliar
from tiempos import ResultadoTiempos
from tomas import duracion_toma_buena

_PATRON_FILA_TABLA = re.compile(r"^\|(.+)\|\s*$")
_PATRON_SEPARADOR_CELDA = re.compile(r"^:?-{1,}:?$")
_PATRON_LINEA_MARCA = re.compile(r"^(\d+):(\d{2})[ \t]+(.+)$")
_PREFIJO_NOTA = "Nota: "


def _normalizar(texto: str) -> str:
    """Minusculas y sin tildes, para comparar la cabecera "Capitulo" de la
    tabla sin depender de como el guion la haya acentuado."""
    descompuesto = unicodedata.normalize("NFKD", texto.strip().lower())
    return "".join(caracter for caracter in descompuesto if not unicodedata.combining(caracter))


def _filas_tabla(contenido: str) -> list[list[str]]:
    """Filas de la primera tabla Markdown (`| celda | celda |`) de `contenido`,
    sin la fila separadora (`|---|---|`). Cada fila es la lista de sus celdas,
    ya sin espacios sobrantes."""
    filas: list[list[str]] = []
    for linea in contenido.splitlines():
        coincidencia = _PATRON_FILA_TABLA.match(linea.strip())
        if not coincidencia:
            continue
        celdas = [celda.strip() for celda in coincidencia.group(1).split("|")]
        if all(_PATRON_SEPARADOR_CELDA.match(celda) for celda in celdas):
            continue
        filas.append(celdas)
    return filas


def _titulos_capitulos(seccion: SeccionAuxiliar) -> list[str]:
    """Titulos de la columna "Capitulo" de la tabla de la seccion, en orden.

    Busca la columna por su cabecera (insensible a mayusculas/tildes) para no
    depender de que "Capitulo" sea siempre la ultima columna; si no encuentra una
    cabecera reconocible, usa la ultima columna como respaldo -- el formato que
    traen los guiones reales que tienen la seccion (`Marca | Capitulo`)."""
    filas = _filas_tabla(seccion.contenido)
    if not filas:
        return []
    cabecera, filas_datos = filas[0], filas[1:]
    indice = next(
        (i for i, celda in enumerate(cabecera) if _normalizar(celda) == "capitulo"),
        len(cabecera) - 1,
    )
    return [
        fila[indice].strip()
        for fila in filas_datos
        if indice < len(fila) and fila[indice].strip()
    ]


def _seccion_capitulos(
    resultado_parseo: ResultadoParseo, configuracion: Configuracion
) -> SeccionAuxiliar | None:
    objetivo = configuracion.titulo_seccion_capitulos.strip()
    return next(
        (
            seccion
            for seccion in resultado_parseo.secciones_auxiliares
            if seccion.titulo.strip().startswith(objetivo)
        ),
        None,
    )


@dataclass(frozen=True)
class CapituloYoutube:
    """Un capitulo ya emparejado con su escena y su marca de tiempo (sin
    filtrar todavia por la marca minima entre capitulos, requisito 3)."""

    numero_escena: int
    titulo: str
    inicio_segundos: float


@dataclass(frozen=True)
class ResultadoCapitulos:
    """Salida de `calcular_capitulos`.

    `capitulos` vacio junto con `motivo_sin_generar` (no `None`) es la senal de
    "no generar el archivo" (requisito 4): guion sin seccion de capitulos,
    seccion sin ninguna fila legible, o ningun titulo emparejable con una
    escena. `escenas_sin_toma_buena` son, entre las escenas que si aportan una
    marca reportada, las que no tenian toma buena y cayeron a la duracion
    estimada de T-12 (requisito 2, mismo nombre de campo que
    `srt_alineado.ResultadoAlineacion`); vacio significa que todas las marcas
    reportadas son tiempo real. `titulos_sobrantes` son los titulos de la
    tabla de capitulos que no llegaron a emparejarse con ninguna escena por
    haber MAS titulos que escenas (requisito 2 de R-11, hallazgo #17); vacio
    en el caso normal (mismo numero de titulos que escenas, o menos).
    """

    capitulos: tuple[CapituloYoutube, ...]
    escenas_sin_toma_buena: tuple[int, ...]
    titulos_sobrantes: tuple[str, ...]
    motivo_sin_generar: str | None


def calcular_capitulos(
    resultado_parseo: ResultadoParseo,
    resultado_tiempos: ResultadoTiempos,
    tomas_por_escena: dict[str, Any] | None = None,
    configuracion: Configuracion | None = None,
) -> ResultadoCapitulos:
    """Empareja titulos de capitulo con escenas (requisito 1) y calcula el
    tiempo acumulado de inicio de cada una (requisito 2), sin filtrar todavia
    por la marca minima entre capitulos consecutivos (eso lo hace
    `formatear_capitulos_youtube`, requisito 3)."""
    configuracion = configuracion or Configuracion()
    tomas_por_escena = tomas_por_escena or {}

    seccion = _seccion_capitulos(resultado_parseo, configuracion)
    if seccion is None:
        return ResultadoCapitulos(
            capitulos=(),
            escenas_sin_toma_buena=(),
            titulos_sobrantes=(),
            motivo_sin_generar=(
                f"el guion no trae ninguna seccion '{configuracion.titulo_seccion_capitulos}'."
            ),
        )
    titulos = _titulos_capitulos(seccion)
    if not titulos:
        return ResultadoCapitulos(
            capitulos=(),
            escenas_sin_toma_buena=(),
            titulos_sobrantes=(),
            motivo_sin_generar=(
                f"la seccion '{seccion.titulo}' no trae ninguna fila de tabla legible."
            ),
        )

    numero_capitulos = min(len(titulos), len(resultado_tiempos.escenas))
    capitulos: list[CapituloYoutube] = []
    escenas_sin_toma_buena: list[int] = []
    cursor_segundos = 0.0
    for indice, tiempo_escena in enumerate(resultado_tiempos.escenas):
        if indice >= numero_capitulos:
            break
        duracion_real = duracion_toma_buena(
            tomas_por_escena.get(str(tiempo_escena.numero)), tiempo_escena.numero
        )
        if duracion_real is not None and duracion_real > 0:
            duracion = duracion_real
        else:
            duracion = tiempo_escena.duracion_estimada_segundos
            escenas_sin_toma_buena.append(tiempo_escena.numero)
        capitulos.append(
            CapituloYoutube(
                numero_escena=tiempo_escena.numero,
                titulo=titulos[indice],
                inicio_segundos=cursor_segundos,
            )
        )
        cursor_segundos += duracion

    if not capitulos:
        return ResultadoCapitulos(
            capitulos=(),
            escenas_sin_toma_buena=(),
            titulos_sobrantes=tuple(titulos),
            motivo_sin_generar="el guion no tiene ninguna escena con la que emparejar un capitulo.",
        )
    return ResultadoCapitulos(
        capitulos=tuple(capitulos),
        escenas_sin_toma_buena=tuple(escenas_sin_toma_buena),
        titulos_sobrantes=tuple(titulos[numero_capitulos:]),
        motivo_sin_generar=None,
    )


def _formatear_mm_ss(segundos: float) -> str:
    """`M:SS`, redondeando siempre hacia abajo: una marca nunca puede caer
    despues del instante real en el que empieza la escena que anuncia."""
    total_segundos = int(segundos)
    minutos, segs = divmod(total_segundos, 60)
    return f"{minutos}:{segs:02d}"


def formatear_capitulos_youtube(
    resultado: ResultadoCapitulos, configuracion: Configuracion | None = None
) -> str | None:
    """Texto final de `capitulos-youtube.txt`. `None` si `resultado` no trae
    ningun capitulo (requisito 4: nada que generar).

    Requisito 3: primera marca "0:00", una linea "M:SS Titulo" por capitulo en
    orden creciente, nunca dos marcas a menos de
    `capitulos_youtube_marca_minima_segundos` entre si -- la marca demasiado
    cercana a la anterior se omite (el capitulo sigue integro en el guion, solo
    no aparece como marca propia en este archivo derivado). El filtrado se hace
    sobre los tiempos en coma flotante sin redondear todavia: si la diferencia
    real ya es >= el minimo, la diferencia entre los "M:SS" redondeados hacia
    abajo tambien lo es (redondear hacia abajo nunca puede acercar dos marcas
    mas de lo que ya estaban).

    Requisito 2: si alguna de las marcas conservadas depende de una duracion
    estimada en vez de la toma buena real, la primera linea del archivo lo
    advierte explicitamente en vez de mezclarlo en silencio.
    """
    configuracion = configuracion or Configuracion()
    if not resultado.capitulos:
        return None

    conservados: list[CapituloYoutube] = [resultado.capitulos[0]]
    for capitulo in resultado.capitulos[1:]:
        anterior = conservados[-1]
        if (
            capitulo.inicio_segundos - anterior.inicio_segundos
            < configuracion.capitulos_youtube_marca_minima_segundos
        ):
            continue
        conservados.append(capitulo)

    lineas = [f"{_formatear_mm_ss(c.inicio_segundos)} {c.titulo}" for c in conservados]

    numeros_reportados = {c.numero_escena for c in conservados}
    estimadas_reportadas = sorted(
        n for n in resultado.escenas_sin_toma_buena if n in numeros_reportados
    )
    if estimadas_reportadas:
        if len(estimadas_reportadas) == len(conservados):
            nota = (
                f"{_PREFIJO_NOTA}tiempos ESTIMADOS (T-12): todavia no hay ninguna toma buena "
                "registrada (R-02)."
            )
        else:
            lista = ", ".join(str(n) for n in estimadas_reportadas)
            nota = (
                f"{_PREFIJO_NOTA}tiempos ESTIMADOS (T-12) en la(s) escena(s) {lista} -- sin "
                "toma buena registrada todavia (R-02); el resto de marcas usa la duracion real "
                "de su toma buena."
            )
        lineas.insert(0, nota)

    return "\n".join(lineas) + "\n"


def validar_capitulos_youtube(
    contenido: str, configuracion: Configuracion | None = None
) -> list[str]:
    """Mismas reglas que exige YouTube para reconocer capitulos en la
    descripcion de un video (requisito 3): la primera marca es "0:00", las
    marcas van en orden estrictamente creciente y ninguna esta a menos de
    `capitulos_youtube_marca_minima_segundos` de la anterior. Ignora la linea de
    nota (`Nota: ...`) que antepone `formatear_capitulos_youtube` cuando hay
    tiempos estimados: esa linea no es una marca."""
    configuracion = configuracion or Configuracion()
    lineas_marca = [
        linea
        for linea in contenido.splitlines()
        if linea.strip() and not linea.startswith(_PREFIJO_NOTA)
    ]
    if not lineas_marca:
        return ["el archivo no tiene ninguna marca de capitulo."]

    problemas: list[str] = []
    segundos_anterior: int | None = None
    for indice, linea in enumerate(lineas_marca):
        coincidencia = _PATRON_LINEA_MARCA.match(linea)
        if not coincidencia:
            problemas.append(f"linea {indice + 1} no tiene el formato 'M:SS Titulo': {linea!r}")
            continue
        minutos, segs, titulo = coincidencia.groups()
        segundos = int(minutos) * 60 + int(segs)
        if not titulo.strip():
            problemas.append(f"linea {indice + 1} no trae titulo de capitulo.")
        if indice == 0 and segundos != 0:
            problemas.append(f"la primera marca debe ser '0:00', no '{minutos}:{segs}'.")
        if segundos_anterior is not None:
            if segundos <= segundos_anterior:
                problemas.append(
                    f"linea {indice + 1}: la marca {minutos}:{segs} no es mayor que la anterior."
                )
            elif (
                segundos - segundos_anterior
                < configuracion.capitulos_youtube_marca_minima_segundos
            ):
                problemas.append(
                    f"linea {indice + 1}: solo {segundos - segundos_anterior}s desde la marca "
                    f"anterior (minimo {configuracion.capitulos_youtube_marca_minima_segundos}s)."
                )
        segundos_anterior = segundos
    return problemas


def generar_capitulos_youtube(
    resultado_parseo: ResultadoParseo,
    resultado_tiempos: ResultadoTiempos,
    tomas_por_escena: dict[str, Any] | None = None,
    configuracion: Configuracion | None = None,
) -> tuple[str | None, ResultadoCapitulos]:
    """Punto de entrada de R-07: empareja, calcula tiempos y formatea en un
    solo paso (requisito 5: regenerable sin intervencion manual). La skill no
    la invoca sola: es Claude quien reune el `ResultadoParseo` y el
    `ResultadoTiempos` (idealmente los de una revalidacion, para que los
    titulos y tiempos sean los vigentes) y `EstadoProyecto.tomas` ya fusionado
    por R-02, y llama a esta funcion dentro de la sesion tras revalidar el
    guion o cerrar una tanda de tomas nueva -- mismo patron que
    `srt_alineado.generar_srt_alineado` (R-05). `contenido` es `None` cuando no
    hay nada que generar (requisito 4): no llamar a `guardar_capitulos_youtube`
    en ese caso."""
    configuracion = configuracion or Configuracion()
    resultado = calcular_capitulos(
        resultado_parseo, resultado_tiempos, tomas_por_escena, configuracion
    )
    contenido = formatear_capitulos_youtube(resultado, configuracion)
    return contenido, resultado


def guardar_capitulos_youtube(contenido: str, carpeta_salida: Path) -> Path:
    """Escribe `capitulos-youtube.txt` en la carpeta de salida del guion.
    Nunca fuera de `carpeta_salida` (regla de aislamiento, §0.2). No llamar con
    `contenido=None` (requisito 4): quien orquesta decide no escribir nada."""
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    destino = carpeta_salida / NOMBRE_ARCHIVO_CAPITULOS_YOUTUBE
    destino.write_text(contenido, encoding="utf-8", newline="\n")
    return destino
