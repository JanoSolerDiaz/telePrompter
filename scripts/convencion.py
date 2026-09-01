"""Deteccion de convencion de marcado y propuesta de convencion explicita (T-10).

La convencion (rotulo `**LOCUCIÓN**` con cuerpo en cita de bloque frente a
`**EN PANTALLA**`/`**NOTA**`, encabezado `## BLOQUE N — <titulo> (m:ss-m:ss)`)
ya es contractual, con aviso, por decision del dueno (§6 pregunta 3 de
SEGUIMIENTO, promovida a §0.2 de HOJA_DE_RUTA): los rotulos mandan siempre y una
escena sin rotulo se procesa igual, por inferencia, senalada como desviacion.
Esta tarea no descubre esa convencion (T-08/T-09 ya la implementan) ni decide si
adoptarla (el dueno ya lo hizo): la documenta para el guionista
(`generar_convencion_guiones`/`guardar_convencion_guiones`), cierra sus huecos
declarando explicitamente que categorias de seccion auxiliar y de desviacion
existen (`detectar_desviaciones`), y deja el mecanismo general para medir
consistencia de una senal y proponer promoverla a contractual
(`medir_consistencia_senales`/`proponer_convenciones`) para cuando aparezca una
senal de inferencia nueva y estable en guiones futuros -- en los tres guiones
reales de calibracion no hace falta: ya se clasifican enteros por la ruta rapida
de rotulo, sin apoyarse en ninguna senal de inferencia de contenido.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from clasificador import TIPO_LOCUCION, TIPO_REVISAR, ResultadoClasificacion
from config import Configuracion
from parser import MOTIVO_SECCION_NO_RECONOCIDA, ResultadoParseo

NOMBRE_ARCHIVO_CONVENCION = "convencion-guiones.md"
# Mismo caracter y misma razon que `parser._GUION_LARGO` (T-08): los rangos
# horarios de los guiones reales usan el guion largo Unicode U+2013, no el corto
# del teclado. Se referencia por escape para no disparar la regla RUF001 de ruff
# (caracter "ambiguo" por su parecido visual con el guion corto).
_GUION_LARGO = "\u2013"

# Senales que ya forman parte de la convencion contractual (T-08/T-09, §0.2): no
# tiene sentido "proponer" adoptarlas, ya estan adoptadas. Incluye tambien las
# senales estructurales sin contenido recitable propio (linea en blanco, seccion
# de rotulo vacia): promoverlas a convencion explicita no aporta nada al
# guionista.
_SENALES_CONTRACTUALES = frozenset(
    {
        "rotulo",
        "cita_bloque",
        "rotulo_no_locucion",
        "encabezado",
        "seccion_auxiliar",
        "preambulo",
        "blank",
        "seccion_vacia",
    }
)

_PATRON_ROTULO_LINEA = re.compile(r"^\*\*[^*]+\*\*$")


@dataclass
class ConsistenciaSenal:
    """Cuantas veces aparece una senal de clasificacion y que tan consistente es.

    Requisito 1 de T-10: medida sobre uno o varios guiones ya clasificados por
    T-09 (`medir_consistencia_senales` acepta una lista para poder agregar el
    guion actual con el historico de guiones ya procesados, sin que este modulo
    tenga que inventar su propio almacen de historico: quien llama decide que
    resultados anteriores pasar)."""

    senal: str
    tipo_dominante: str
    apariciones: int
    apariciones_tipo_dominante: int
    ejemplo: str

    @property
    def consistencia(self) -> float:
        return self.apariciones_tipo_dominante / self.apariciones if self.apariciones else 0.0

    @property
    def es_consistente(self) -> bool:
        return self.apariciones > 0 and self.consistencia == 1.0


@dataclass
class PropuestaConvencion:
    """Propuesta de adoptar una senal de inferencia como convencion explicita
    (requisito 2 de T-10): ejemplo de antes/despues y el ahorro que supondria."""

    senal: str
    tipo: str
    apariciones: int
    ejemplo_antes: str
    ejemplo_despues: str
    ahorro: str


@dataclass
class Desviacion:
    """Un guion concreto que se sale de la convencion vigente (requisito 5).

    Nunca bloquea el proceso: la escena o seccion se sigue procesando por
    inferencia. Solo informa, para que el guionista pueda cerrar el hueco en el
    guion de origen si quiere pasar a la ruta rapida."""

    tipo: str
    descripcion: str
    linea: int


def medir_consistencia_senales(
    resultados: list[ResultadoClasificacion],
) -> list[ConsistenciaSenal]:
    """Consistencia de cada senal de clasificacion vista en `resultados`.

    Una senal es consistente cuando siempre decide el mismo tipo
    (locucion/no_locucion/revisar) alli donde aparece. Agrega tantos resultados
    como se le pasen: el guion actual solo, o el actual mas el historico de
    guiones ya procesados en sesiones anteriores."""
    conteo: dict[str, dict[str, int]] = {}
    ejemplos: dict[str, str] = {}
    for resultado in resultados:
        for bloque in resultado.bloques:
            por_tipo = conteo.setdefault(bloque.senal, {})
            por_tipo[bloque.tipo] = por_tipo.get(bloque.tipo, 0) + 1
            ejemplos.setdefault(bloque.senal, bloque.contenido.strip())

    consistencias = []
    for senal, por_tipo in conteo.items():
        tipo_dominante = max(por_tipo, key=lambda tipo: por_tipo[tipo])
        apariciones = sum(por_tipo.values())
        consistencias.append(
            ConsistenciaSenal(
                senal=senal,
                tipo_dominante=tipo_dominante,
                apariciones=apariciones,
                apariciones_tipo_dominante=por_tipo[tipo_dominante],
                ejemplo=ejemplos[senal],
            )
        )
    return sorted(consistencias, key=lambda consistencia: consistencia.senal)


def proponer_convenciones(
    consistencias: list[ConsistenciaSenal], configuracion: Configuracion | None = None
) -> list[PropuestaConvencion]:
    """Propone adoptar como convencion explicita cada senal de inferencia que
    cubre de forma 100% consistente contenido recitable o no recitable
    (requisito 2). Ignora las senales ya contractuales y las que solo producen
    `revisar` (no cubren nada con claridad, no hay nada que proponer)."""
    configuracion = configuracion or Configuracion()
    propuestas = []
    for consistencia in consistencias:
        if consistencia.senal in _SENALES_CONTRACTUALES:
            continue
        if consistencia.tipo_dominante == TIPO_REVISAR:
            continue
        if not consistencia.es_consistente:
            continue

        if consistencia.tipo_dominante == TIPO_LOCUCION:
            rotulo = configuracion.rotulo_locucion
            despues = f"{rotulo}\n> {consistencia.ejemplo}"
        else:
            rotulo = configuracion.rotulos_no_locucion[0]
            despues = f"{rotulo}\n{consistencia.ejemplo}"

        propuestas.append(
            PropuestaConvencion(
                senal=consistencia.senal,
                tipo=consistencia.tipo_dominante,
                apariciones=consistencia.apariciones,
                ejemplo_antes=consistencia.ejemplo,
                ejemplo_despues=despues,
                ahorro=(
                    f"{consistencia.apariciones} bloque(s) detectados hoy por inferencia "
                    f"('{consistencia.senal}') dejarian de depender de ella y de quedar "
                    "expuestos a un cambio de redaccion que la despiste, si se marcan con "
                    f"{rotulo} en el guion de origen."
                ),
            )
        )
    return propuestas


def _escena_tiene_rotulo_locucion(
    escena_linea_inicio: int,
    escena_linea_fin: int,
    clasificacion: ResultadoClasificacion,
    configuracion: Configuracion,
) -> bool:
    return any(
        bloque.senal == "rotulo"
        and bloque.contenido.strip() == configuracion.rotulo_locucion
        and escena_linea_inicio <= bloque.linea_inicio <= escena_linea_fin
        for bloque in clasificacion.bloques
    )


_MOTIVO_NIVEL_DISTINTO_PREFIJO = "encabezado de nivel"


def _es_subtitulo_reconocido(auxiliar_linea_inicio: int, resultado: ResultadoParseo) -> bool:
    """El subtitulo entrecomillado justo tras el titulo del guion (evidencia de
    T-08: "el subtitulo entrecomillado tras el # inicial") es una categoria de
    seccion auxiliar conocida y esperada, aunque no este en la lista negra
    literal de `configuracion.secciones_auxiliares` (esa lista es de titulos
    fijos; el titulo del subtitulo varia con cada video, asi que se reconoce por
    posicion: es el primer encabezado **del nivel separador** de todo el guion --
    no el `#` del titulo, que es de otro nivel y ya aparece aparte, con su propio
    motivo, entre las secciones auxiliares)."""
    lineas_nivel_separador = [
        seccion.linea_inicio
        for seccion in resultado.secciones_auxiliares
        if not seccion.motivo.startswith(_MOTIVO_NIVEL_DISTINTO_PREFIJO)
    ] + [escena.linea_inicio for escena in resultado.escenas]
    if not lineas_nivel_separador or auxiliar_linea_inicio != min(lineas_nivel_separador):
        return False
    auxiliar = next(
        s for s in resultado.secciones_auxiliares if s.linea_inicio == auxiliar_linea_inicio
    )
    titulo = auxiliar.titulo.strip()
    return titulo.startswith('"') and titulo.endswith('"') and len(titulo) > 1


def detectar_desviaciones(
    resultado: ResultadoParseo,
    clasificacion: ResultadoClasificacion,
    configuracion: Configuracion | None = None,
) -> list[Desviacion]:
    """Desviaciones respecto a la convencion vigente (requisito 5): escena sin
    rotulo de locucion, rotulo desconocido y seccion auxiliar no reconocida.
    Nunca bloquea el proceso -- solo se informa, la escena/seccion ya se ha
    procesado igualmente por inferencia (T-08/T-09)."""
    configuracion = configuracion or Configuracion()
    desviaciones: list[Desviacion] = []

    for escena in resultado.escenas:
        if not _escena_tiene_rotulo_locucion(
            escena.linea_inicio, escena.linea_fin, clasificacion, configuracion
        ):
            desviaciones.append(
                Desviacion(
                    tipo="escena_sin_rotulo_locucion",
                    descripcion=(
                        f"Escena {escena.numero} ('{escena.titulo}') no usa el rotulo "
                        f"{configuracion.rotulo_locucion!r}: se ha procesado por inferencia, "
                        "sin bloquear el proceso."
                    ),
                    linea=escena.linea_inicio,
                )
            )

        for indice, linea in enumerate(escena.contenido.split("\n")):
            texto = linea.strip()
            if not _PATRON_ROTULO_LINEA.match(texto):
                continue
            if texto in (configuracion.rotulo_locucion, *configuracion.rotulos_no_locucion):
                continue
            desviaciones.append(
                Desviacion(
                    tipo="rotulo_desconocido",
                    descripcion=(
                        f"Escena {escena.numero}: {texto!r} tiene forma de rotulo de seccion "
                        "pero no es ninguno de los reconocidos "
                        f"({configuracion.rotulo_locucion!r}, "
                        f"{', '.join(map(repr, configuracion.rotulos_no_locucion))})."
                    ),
                    linea=escena.linea_inicio + indice,
                )
            )

    for auxiliar in resultado.secciones_auxiliares:
        if auxiliar.motivo != MOTIVO_SECCION_NO_RECONOCIDA:
            continue
        if _es_subtitulo_reconocido(auxiliar.linea_inicio, resultado):
            continue
        desviaciones.append(
            Desviacion(
                tipo="seccion_auxiliar_no_reconocida",
                descripcion=(
                    f"Seccion '{auxiliar.titulo}' no es una escena ni esta en la lista de "
                    "secciones auxiliares reconocidas "
                    f"({', '.join(configuracion.secciones_auxiliares)})."
                ),
                linea=auxiliar.linea_inicio,
            )
        )

    return sorted(desviaciones, key=lambda desviacion: desviacion.linea)


def generar_convencion_guiones(configuracion: Configuracion | None = None) -> str:
    """Documento de una pagina, listo para pegar en la plantilla de guiones del
    dueno (requisito 4): patron de encabezado de escena, rotulo de locucion con
    cuerpo en cita de bloque, rotulos de no locucion, secciones auxiliares
    reconocidas y metadatos de cabecera. Generado a partir de `Configuracion`
    para que un cambio de convencion en `config.py` se refleje aqui solo, sin
    mantener un segundo texto a mano ("sin numeros magicos", §0.2)."""
    configuracion = configuracion or Configuracion()
    rotulos_no_locucion = "\n\n".join(
        f"    {rotulo}\n    Prosa normal, sin cita de bloque: no se recita."
        for rotulo in configuracion.rotulos_no_locucion
    )
    secciones_auxiliares = "\n".join(f"- {titulo}" for titulo in configuracion.secciones_auxiliares)
    return f"""# Convención de guiones — teleprompter

> Generado automáticamente (T-10). Pégalo en tu plantilla de guiones para que la
> skill use siempre la ruta rápida (por rótulo), dejando la inferencia como red
> de seguridad para lo que se te olvide marcar.

## Encabezado de escena

Cada escena empieza con un encabezado `##` con este patrón:

    ## BLOQUE N — <título> (m:ss {_GUION_LARGO} m:ss)

Ejemplo: `## BLOQUE 3 — Las tres comprobaciones (1:05 {_GUION_LARGO} 1:55)`

## Locución

El texto que se recita va bajo el rótulo `{configuracion.rotulo_locucion}`, en
cita de bloque (una línea que empieza por `> ` por cada línea de locución):

    {configuracion.rotulo_locucion}
    > Texto que se recita, línea a línea, en cita de bloque.

Cualquier texto suelto de esa misma escena que quede fuera de la cita de bloque
(una acotación de ritmo, un ejemplo sin comillar…) se marca `revisar`: nunca se
recita ni se descarta en silencio.

## Indicaciones no recitables

{rotulos_no_locucion}

## Secciones auxiliares reconocidas

Estos encabezados `##`, si aparecen, se tratan como material auxiliar del
guión (no como escena ni como locución):

{secciones_auxiliares}
- El subtítulo entrecomillado justo después del título del guión (`# Título` +
  `## "Subtítulo entre comillas"`), si lo usas como página de portada.

## Metadatos de cabecera

Antes de la primera escena, toda línea `**Clave:** valor` se recoge como
metadato del guión (duración objetivo, formato, promesa del vídeo…). No hay una
lista cerrada de claves: usa el nombre que prefieras, siempre en negrita y
seguido de `:` y el valor en la misma línea.

## Si te sales de la convención

Una escena sin `{configuracion.rotulo_locucion}`, un rótulo que no sea ninguno
de los de arriba, o una sección auxiliar con un título nuevo no bloquean el
proceso: la skill lo procesa igual por inferencia y te lo señala como
desviación en el informe, para que decidas si lo corriges en el guión o lo
dejas así.
"""


def guardar_convencion_guiones(
    carpeta_salida: Path, configuracion: Configuracion | None = None
) -> Path:
    """Escribe `convencion-guiones.md` en la carpeta de salida del guion.

    Documento generado, no editado a mano por el dueno (es "para pegar en su
    plantilla", no un archivo que se vuelva a leer como entrada): no aplica la
    regla de copia `.bak` de invariante (d), reservada a archivos del dueno como
    `guion-escenas.md` (T-17)."""
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    destino = carpeta_salida / NOMBRE_ARCHIVO_CONVENCION
    destino.write_text(generar_convencion_guiones(configuracion), encoding="utf-8")
    return destino
