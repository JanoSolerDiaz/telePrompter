"""Tests de los comandos de montaje encadenados (tarea R-30).

Mismo patron que `tests/test_concat_ffmpeg.py`/`tests/test_capitulos_youtube.py`:
guiones sinteticos minimos con control total sobre el numero de escenas, mas un
mapa `{numero_escena: dict_de_escena}` de tomas buenas (mismo contenedor que
`EstadoProyecto.tomas`, R-02).
"""

from __future__ import annotations

from pathlib import Path

from comandos_montaje import (
    calcular_comandos_montaje,
    formatear_comandos_montaje,
    generar_comandos_montaje,
    guardar_comandos_montaje,
)
from config import NOMBRE_ARCHIVO_COMANDOS_MONTAJE, Configuracion
from parser import ResultadoParseo, parsear_guion
from tiempos import ResultadoTiempos, calcular_tiempos

_GUION_DOS_ESCENAS = """# Guion de prueba

## BLOQUE 0 — Arranque (0:00 – 0:10)

**LOCUCIÓN**

> Esta es la primera frase del bloque. Y esta la segunda, ya con más ritmo.

## BLOQUE 1 — Cierre (0:10 – 0:20)

**LOCUCIÓN**

> Segunda escena, con su propia frase de cierre para la locución.
"""

_GUION_DOS_ESCENAS_CON_CAPITULOS = """# Guion de prueba

## Capítulos (para la descripción del vídeo)

| Marca | Capítulo |
|---|---|
| 0:00 | Primero |
| 0:00 | Segundo |
""" + _GUION_DOS_ESCENAS.split("\n", 1)[1]

# Toma `buena` con `archivo_video` anotado para la escena 0 -- lo minimo que
# necesita el paso 1 (concatenacion) para tener una linea `file` real.
_TOMAS_ESCENA_0_BUENA_CON_ARCHIVO = {
    "0": {
        "titulo": "Arranque",
        "tomas": [
            {
                "numero": 1,
                "duracion_segundos": 4.0,
                "nota": "",
                "buena": True,
                "archivo_video": "CLIP0001.MP4",
            }
        ],
    },
}

# Toma registrada pero NUNCA marcada `buena`: hay parte de rodaje (la escena 0
# aparece en el dict), pero ninguna evidencia real -- ni concatenable ni
# alineable, para distinguir ese caso de "sin ningun parte de rodaje".
_TOMAS_ESCENA_0_SIN_BUENA = {
    "0": {
        "titulo": "Arranque",
        "tomas": [{"numero": 1, "duracion_segundos": 4.0, "nota": "", "buena": False}],
    },
}


def _pipeline(
    texto: str, configuracion: Configuracion | None = None
) -> tuple[ResultadoParseo, ResultadoTiempos]:
    configuracion = configuracion or Configuracion()
    resultado = parsear_guion(texto, configuracion=configuracion)
    tiempos = calcular_tiempos(resultado, configuracion)
    return resultado, tiempos


# --- Requisito 4 (sin rodaje, no hay nada real que montar todavia) ------------------


def test_sin_ningun_parte_de_rodaje_no_genera_nada() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS_CON_CAPITULOS)
    calculo = calcular_comandos_montaje(resultado, tiempos, "prueba", {})
    assert calculo.pasos == ()
    assert calculo.motivo_sin_generar is not None
    assert formatear_comandos_montaje(calculo, "prueba") is None

    contenido, calculo_directo = generar_comandos_montaje(resultado, tiempos, "prueba", {})
    assert contenido is None
    assert calculo_directo.motivo_sin_generar == calculo.motivo_sin_generar


def test_con_tomas_registradas_pero_sin_ninguna_buena_si_concatena() -> None:
    """Con al menos un parte de rodaje registrado (aunque ninguna toma este
    marcada `buena`), `concat-ffmpeg.txt` SI se genera (todo comentarios) --
    el mismo criterio decide que los comandos de montaje tambien se generen,
    nunca se omiten por falta de evidencia real, solo por falta de rodaje."""
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS, Configuracion())
    calculo = calcular_comandos_montaje(resultado, tiempos, "prueba", _TOMAS_ESCENA_0_SIN_BUENA)
    assert calculo.motivo_sin_generar is None
    assert len(calculo.pasos) >= 1


# --- Requisito 1 (cadena de 1 a 3 comandos, salida de cada paso = entrada del
# siguiente) ---------------------------------------------------------------------


def test_guion_completo_genera_tres_pasos_encadenados_con_capitulos() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS_CON_CAPITULOS)
    calculo = calcular_comandos_montaje(
        resultado, tiempos, "prueba", _TOMAS_ESCENA_0_BUENA_CON_ARCHIVO
    )
    assert calculo.motivo_sin_generar is None
    assert len(calculo.pasos) == 3
    assert calculo.incluye_capitulos is True

    concatenado, subtitulado, final = calculo.pasos

    # Paso 1: concatenar -- entrada real concat-ffmpeg.txt, salida nombrada.
    assert "concat-ffmpeg.txt" in concatenado.comando
    assert concatenado.comando.endswith("prueba-concatenado.mp4")

    # Paso 2: subtitulos -- entrada es la SALIDA del paso 1 (encadenado real),
    # usa guion-alineado.srt porque la escena 0 si tiene toma buena.
    assert "prueba-concatenado.mp4" in subtitulado.comando
    assert "guion-alineado.srt" in subtitulado.comando
    assert subtitulado.comando.endswith("prueba-con-subtitulos.mp4")
    assert subtitulado.comentario_alternativo is not None
    assert "subtitles=" in subtitulado.comentario_alternativo

    # Paso 3: capitulos -- entrada es la SALIDA del paso 2.
    assert "prueba-con-subtitulos.mp4" in final.comando
    assert "capitulos-ffmpeg.txt" in final.comando
    assert final.comando.endswith("prueba-final.mp4")


def test_sin_seccion_capitulos_solo_dos_pasos_y_lo_dice_explicito() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)  # sin seccion Capítulos
    calculo = calcular_comandos_montaje(
        resultado, tiempos, "prueba", _TOMAS_ESCENA_0_BUENA_CON_ARCHIVO
    )
    assert len(calculo.pasos) == 2
    assert calculo.incluye_capitulos is False

    contenido = formatear_comandos_montaje(calculo, "prueba")
    assert contenido is not None
    assert "capitulos-ffmpeg.txt" not in contenido
    assert "no trae sección «Capítulos»" in contenido


def test_sin_toma_alineada_usa_el_srt_estimado() -> None:
    """Sin ninguna escena con toma buena (aunque haya parte de rodaje), el
    paso de subtitulos cae a `guion.srt`, nunca a `guion-alineado.srt`."""
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS_CON_CAPITULOS)
    calculo = calcular_comandos_montaje(resultado, tiempos, "prueba", _TOMAS_ESCENA_0_SIN_BUENA)
    _, subtitulado, _ = calculo.pasos
    assert "guion.srt" in subtitulado.comando
    assert "guion-alineado.srt" not in subtitulado.comando


# --- Requisito 2 (documento, nombres reales, nota de escenas pendientes) -----------


def test_formato_no_trae_ninguna_ruta_de_ejemplo() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS_CON_CAPITULOS)
    calculo = calcular_comandos_montaje(
        resultado, tiempos, "prueba", _TOMAS_ESCENA_0_BUENA_CON_ARCHIVO
    )
    contenido = formatear_comandos_montaje(calculo, "prueba")
    assert contenido is not None
    assert "video.mp4" not in contenido
    assert "video-final.mp4" not in contenido
    for nombre_real in (
        "concat-ffmpeg.txt",
        "guion-alineado.srt",
        "capitulos-ffmpeg.txt",
        "prueba-concatenado.mp4",
        "prueba-con-subtitulos.mp4",
        "prueba-final.mp4",
    ):
        assert nombre_real in contenido


def test_nota_de_escenas_pendientes_cuando_las_hay() -> None:
    """La escena 1 nunca tiene parte de rodaje en estos fixtures: debe quedar
    anotada como pendiente (requisito 2) en la nota final."""
    resultado, tiempos = _pipeline(
        _GUION_DOS_ESCENAS_CON_CAPITULOS, Configuracion()
    )
    calculo = calcular_comandos_montaje(
        resultado, tiempos, "prueba", _TOMAS_ESCENA_0_BUENA_CON_ARCHIVO
    )
    assert len(calculo.escenas_pendientes) == 1
    assert calculo.escenas_pendientes[0].numero_escena == 1
    assert calculo.escenas_pendientes[0].motivo == "sin_toma_buena"

    contenido = formatear_comandos_montaje(calculo, "prueba")
    assert contenido is not None
    assert "Escena 1: sin_toma_buena" in contenido


def test_sin_escenas_pendientes_no_hay_nota() -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS_CON_CAPITULOS)
    tomas_completas = {
        **_TOMAS_ESCENA_0_BUENA_CON_ARCHIVO,
        "1": {
            "titulo": "Cierre",
            "tomas": [
                {
                    "numero": 1,
                    "duracion_segundos": 4.0,
                    "nota": "",
                    "buena": True,
                    "archivo_video": "CLIP0002.MP4",
                }
            ],
        },
    }
    calculo = calcular_comandos_montaje(resultado, tiempos, "prueba", tomas_completas)
    assert calculo.escenas_pendientes == ()
    contenido = formatear_comandos_montaje(calculo, "prueba")
    assert contenido is not None
    assert "todavía sin toma buena" not in contenido


# --- Sufijos configurables (regla "todo default configurable", §0.2) --------------


def test_sufijos_de_archivo_intermedio_son_configurables() -> None:
    configuracion = Configuracion(
        comandos_montaje_sufijo_concatenado="-paso1.mp4",
        comandos_montaje_sufijo_con_subtitulos="-paso2.mp4",
        comandos_montaje_sufijo_final="-paso3.mp4",
    )
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS_CON_CAPITULOS, configuracion)
    calculo = calcular_comandos_montaje(
        resultado,
        tiempos,
        "prueba",
        _TOMAS_ESCENA_0_BUENA_CON_ARCHIVO,
        configuracion,
    )
    concatenado, subtitulado, final = calculo.pasos
    assert concatenado.comando.endswith("prueba-paso1.mp4")
    assert "prueba-paso1.mp4" in subtitulado.comando
    assert subtitulado.comando.endswith("prueba-paso2.mp4")
    assert "prueba-paso2.mp4" in final.comando
    assert final.comando.endswith("prueba-paso3.mp4")


# --- guardar_comandos_montaje -------------------------------------------------------


def test_guardar_comandos_montaje_escribe_el_archivo(tmp_path: Path) -> None:
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS_CON_CAPITULOS)
    contenido, calculo = generar_comandos_montaje(
        resultado, tiempos, "prueba", _TOMAS_ESCENA_0_BUENA_CON_ARCHIVO
    )
    assert contenido is not None
    assert calculo.motivo_sin_generar is None
    ruta = guardar_comandos_montaje(contenido, tmp_path)
    assert ruta == tmp_path / NOMBRE_ARCHIVO_COMANDOS_MONTAJE
    assert ruta.read_text(encoding="utf-8") == contenido


# --- R-31: avisar de archivos referenciados que todavia no existen en disco --------


def test_sin_carpeta_salida_no_comprueba_nada_comportamiento_identico_a_antes_de_r31() -> None:
    """Requisito 4/compatibilidad: sin pasar `carpeta_salida` (valor por
    defecto `None`), ningun archivo se marca como faltante -- mismo
    comportamiento exacto que antes de R-31."""
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS_CON_CAPITULOS)
    calculo = calcular_comandos_montaje(
        resultado, tiempos, "prueba", _TOMAS_ESCENA_0_BUENA_CON_ARCHIVO
    )
    assert calculo.archivos_referenciados_faltantes == ()
    contenido = formatear_comandos_montaje(calculo, "prueba")
    assert contenido is not None
    assert "todavía no existen en esta carpeta de salida" not in contenido


def test_con_carpeta_salida_vacia_avisa_de_los_tres_archivos_faltantes(tmp_path: Path) -> None:
    """Escenario del criterio de aceptacion de R-31: carpeta de salida vacia
    (solo se selecciono `COMANDOS_MONTAJE`) -- los tres archivos referenciados
    (concat, srt, capitulos) faltan, cada uno con la opcion exacta del
    selector que hay que marcar."""
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS_CON_CAPITULOS)
    calculo = calcular_comandos_montaje(
        resultado,
        tiempos,
        "prueba",
        _TOMAS_ESCENA_0_BUENA_CON_ARCHIVO,
        carpeta_salida=tmp_path,
    )
    faltantes = {
        f.nombre_archivo: f.descripcion_opcion for f in calculo.archivos_referenciados_faltantes
    }
    assert faltantes == {
        "concat-ffmpeg.txt": "Lista de concatenación de ffmpeg (.txt)",
        "guion-alineado.srt": "Subtítulos .srt borrador",
        "capitulos-ffmpeg.txt": "Capítulos de YouTube con marcas de tiempo (.txt)",
    }

    contenido = formatear_comandos_montaje(calculo, "prueba")
    assert contenido is not None
    assert "todavía no existen en esta carpeta de salida" in contenido
    for nombre_archivo, descripcion in faltantes.items():
        assert f"`{nombre_archivo}`: selecciona «{descripcion}»" in contenido


def test_sin_seccion_capitulos_no_avisa_del_archivo_de_capitulos(tmp_path: Path) -> None:
    """Sin seccion `Capítulos` en el guion, el tercer paso no se incluye --
    tampoco debe avisar de `capitulos-ffmpeg.txt`, que nunca se referencia."""
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS)  # sin seccion Capítulos
    calculo = calcular_comandos_montaje(
        resultado,
        tiempos,
        "prueba",
        _TOMAS_ESCENA_0_BUENA_CON_ARCHIVO,
        carpeta_salida=tmp_path,
    )
    nombres_faltantes = {f.nombre_archivo for f in calculo.archivos_referenciados_faltantes}
    assert nombres_faltantes == {"concat-ffmpeg.txt", "guion-alineado.srt"}


def test_con_los_tres_archivos_ya_en_disco_no_avisa_de_nada(tmp_path: Path) -> None:
    """Requisito 4: con los tres archivos referenciados ya en `carpeta_salida`
    (de una pasada anterior, por ejemplo), ningun archivo se marca como
    faltante y el documento no gana ninguna linea nueva -- sin falso
    positivo."""
    for nombre in ("concat-ffmpeg.txt", "guion-alineado.srt", "capitulos-ffmpeg.txt"):
        (tmp_path / nombre).write_text("contenido de prueba", encoding="utf-8")

    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS_CON_CAPITULOS)
    calculo = calcular_comandos_montaje(
        resultado,
        tiempos,
        "prueba",
        _TOMAS_ESCENA_0_BUENA_CON_ARCHIVO,
        carpeta_salida=tmp_path,
    )
    assert calculo.archivos_referenciados_faltantes == ()
    contenido = formatear_comandos_montaje(calculo, "prueba")
    assert contenido is not None
    assert "todavía no existen en esta carpeta de salida" not in contenido


def test_sin_toma_alineada_el_archivo_faltante_es_el_srt_estimado(tmp_path: Path) -> None:
    """Sin ninguna escena con toma buena, el paso de subtitulos referencia
    `guion.srt` (no `guion-alineado.srt`, ver
    `test_sin_toma_alineada_usa_el_srt_estimado`) -- el aviso de archivo
    faltante debe seguir exactamente esa misma decision, nunca duplicar ni
    inventar un nombre distinto."""
    resultado, tiempos = _pipeline(_GUION_DOS_ESCENAS_CON_CAPITULOS)
    calculo = calcular_comandos_montaje(
        resultado,
        tiempos,
        "prueba",
        _TOMAS_ESCENA_0_SIN_BUENA,
        carpeta_salida=tmp_path,
    )
    nombres_faltantes = {f.nombre_archivo for f in calculo.archivos_referenciados_faltantes}
    assert "guion.srt" in nombres_faltantes
    assert "guion-alineado.srt" not in nombres_faltantes
