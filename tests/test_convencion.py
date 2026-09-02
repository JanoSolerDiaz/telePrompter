"""Tests de deteccion de convencion y propuesta de convencion explicita (T-10)."""

from __future__ import annotations

from pathlib import Path

from clasificador import (
    TIPO_LOCUCION,
    TIPO_NO_LOCUCION,
    TIPO_REVISAR,
    BloqueClasificado,
    ResultadoClasificacion,
    clasificar_guion,
)
from config import Configuracion
from convencion import (
    NOMBRE_ARCHIVO_CONVENCION,
    detectar_desviaciones,
    generar_convencion_guiones,
    guardar_convencion_guiones,
    medir_consistencia_senales,
    proponer_convenciones,
)
from parser import parsear_guion

# --- Criterio de aceptacion sobre los tres guiones reales -------------------------


def test_guiones_reales_se_clasifican_por_convencion_sin_desviaciones(
    texto_guiones_reales: dict[str, str],
) -> None:
    """Los tres guiones reales usan la convencion completa: cero desviaciones y
    ninguna senal de inferencia de contenido consistente que proponer (ya estan
    en la ruta rapida contractual, no hay nada nuevo que promover)."""
    for nombre, texto in texto_guiones_reales.items():
        resultado = parsear_guion(texto)
        clasificacion = clasificar_guion(resultado)

        desviaciones = detectar_desviaciones(resultado, clasificacion)
        assert desviaciones == [], f"{nombre}: desviaciones inesperadas {desviaciones}"

        consistencias = medir_consistencia_senales([clasificacion])
        propuestas = proponer_convenciones(consistencias)
        assert propuestas == [], f"{nombre}: propuestas inesperadas {propuestas}"


def test_convencion_guiones_describe_los_rotulos_reales(
    texto_guiones_reales: dict[str, str],
) -> None:
    """El documento generado (requisito 4) nombra literalmente los rotulos y el
    patron de encabezado que los tres guiones reales usan de verdad."""
    documento = generar_convencion_guiones()
    for texto in texto_guiones_reales.values():
        assert "**LOCUCIÓN**" in texto
        assert "**EN PANTALLA**" in documento
    assert "**LOCUCIÓN**" in documento
    assert "**NOTA**" in documento
    assert "BLOQUE N" in documento
    assert "Capítulos" in documento
    assert "Preparación antes de grabar" in documento
    assert "Notas de producción" in documento


def test_guardar_convencion_guiones_escribe_el_archivo(tmp_path: Path) -> None:
    destino = guardar_convencion_guiones(tmp_path)
    assert destino == tmp_path / NOMBRE_ARCHIVO_CONVENCION
    assert destino.read_text(encoding="utf-8") == generar_convencion_guiones()


# --- Requisito 5: desviaciones, sin bloquear el proceso ----------------------------

_GUION_CON_DESVIACIONES = """# Guion de prueba

## BLOQUE 0 — Arranque (0:00 - 0:10)

**LOCUCIÓN**
> Primera frase citada.

**ALGO RARO**
Un rotulo que no existe en la convencion.

**EN PANTALLA**
Descripcion de plano.

---

## BLOQUE 1 — Sin rotulo (0:10 - 0:20)

Esto es locucion sin marcar con ningun rotulo, solo texto suelto.

---

## Seccion rara sin marcar

Esta seccion no esta en la lista negra ni tiene el rotulo de locucion.
"""


def test_escena_sin_rotulo_se_procesa_y_se_senala_como_desviacion() -> None:
    """Criterio de aceptacion de T-10: un guion con una escena sin rotulo se
    procesa igualmente (no lanza, no pierde contenido) y aparece senalada."""
    resultado = parsear_guion(_GUION_CON_DESVIACIONES)
    clasificacion = clasificar_guion(resultado)

    # se sigue procesando: la escena sin rotulo tiene su locucion inferida
    escena_sin_rotulo = next(e for e in resultado.escenas if e.numero == 1)
    bloques_escena = [
        b
        for b in clasificacion.bloques
        if escena_sin_rotulo.linea_inicio <= b.linea_inicio <= escena_sin_rotulo.linea_fin
    ]
    assert any(b.tipo in (TIPO_LOCUCION, TIPO_REVISAR) for b in bloques_escena)

    desviaciones = detectar_desviaciones(resultado, clasificacion)
    tipos = {d.tipo for d in desviaciones}
    assert "escena_sin_rotulo_locucion" in tipos
    assert "rotulo_desconocido" in tipos
    assert "seccion_auxiliar_no_reconocida" in tipos

    sin_rotulo = next(d for d in desviaciones if d.tipo == "escena_sin_rotulo_locucion")
    assert "BLOQUE 1" in sin_rotulo.descripcion or "1" in sin_rotulo.descripcion

    desconocido = next(d for d in desviaciones if d.tipo == "rotulo_desconocido")
    assert "ALGO RARO" in desconocido.descripcion

    auxiliar = next(d for d in desviaciones if d.tipo == "seccion_auxiliar_no_reconocida")
    assert "Seccion rara sin marcar" in auxiliar.descripcion


_GUION_CON_NUMERO_ESCENA_DUPLICADO = """# Guion de prueba

## BLOQUE 0 — Arranque (0:00 - 0:10)

**LOCUCIÓN**
> Primera frase citada.

---

## BLOQUE 0 — Numero repetido (0:10 - 0:20)

**LOCUCIÓN**
> Segunda frase citada.
"""

_GUION_CON_NUMERO_ESCENA_NO_CRECIENTE = """# Guion de prueba

## BLOQUE 0 — Arranque (0:00 - 0:10)

**LOCUCIÓN**
> Primera frase citada.

---

## BLOQUE 2 — Intermedio (0:10 - 0:20)

**LOCUCIÓN**
> Segunda frase citada.

---

## BLOQUE 1 — Numero no creciente (0:20 - 0:30)

**LOCUCIÓN**
> Tercera frase citada.
"""


def test_numero_de_escena_repetido_se_procesa_y_se_senala() -> None:
    """Requisito 2 de T-33: un numero de escena duplicado no bloquea el proceso
    (las dos escenas se siguen procesando) pero queda senalado, porque rompe el
    emparejamiento sin ambiguedad de tomas con escenas que exige la cadena de
    montaje (`references/contrato-montaje.md`)."""
    resultado = parsear_guion(_GUION_CON_NUMERO_ESCENA_DUPLICADO)
    clasificacion = clasificar_guion(resultado)
    assert len(resultado.escenas) == 2

    desviaciones = detectar_desviaciones(resultado, clasificacion)
    tipos = [d.tipo for d in desviaciones]
    assert tipos.count("numero_escena_duplicado") == 1
    assert "numero_escena_no_creciente" not in tipos

    duplicado = next(d for d in desviaciones if d.tipo == "numero_escena_duplicado")
    assert "Numero repetido" in duplicado.descripcion


def test_numero_de_escena_no_creciente_se_procesa_y_se_senala() -> None:
    """Un numero de escena menor o igual que el de la escena anterior, sin ser
    un duplicado exacto, tambien rompe el orden predecible y se senala aparte."""
    resultado = parsear_guion(_GUION_CON_NUMERO_ESCENA_NO_CRECIENTE)
    clasificacion = clasificar_guion(resultado)
    assert len(resultado.escenas) == 3

    desviaciones = detectar_desviaciones(resultado, clasificacion)
    tipos = [d.tipo for d in desviaciones]
    assert tipos.count("numero_escena_no_creciente") == 1
    assert "numero_escena_duplicado" not in tipos

    no_creciente = next(d for d in desviaciones if d.tipo == "numero_escena_no_creciente")
    assert "Numero no creciente" in no_creciente.descripcion


def test_subtitulo_entrecomillado_no_es_una_desviacion() -> None:
    """El subtitulo tras el titulo del guion (evidencia de T-08) es una
    categoria de seccion auxiliar reconocida, no una desviacion cada vez."""
    texto = (
        "# Titulo del guion\n\n"
        '## "Subtitulo entre comillas"\n\n'
        "Contenido de portada.\n\n"
        "---\n\n"
        "## BLOQUE 0 — Arranque (0:00 - 0:10)\n\n"
        "**LOCUCIÓN**\n"
        "> Frase citada.\n"
    )
    resultado = parsear_guion(texto)
    clasificacion = clasificar_guion(resultado)
    desviaciones = detectar_desviaciones(resultado, clasificacion)
    assert desviaciones == []


# --- Requisitos 1 y 2: consistencia y propuesta de convencion explicita -----------


def _bloque(tipo: str, senal: str, contenido: str) -> BloqueClasificado:
    return BloqueClasificado(
        tipo=tipo, contenido=contenido, linea_inicio=1, linea_fin=1, motivo=senal, senal=senal
    )


def test_senal_de_inferencia_consistente_genera_propuesta() -> None:
    """Requisito 2: una senal de inferencia que siempre acierta el mismo tipo
    (aqui: 'timestamp' -> no_locucion, tres veces sin excepcion) se propone
    como convencion explicita, con ejemplo antes/despues y ahorro."""
    resultado = ResultadoClasificacion(
        bloques=[
            _bloque(TIPO_NO_LOCUCION, "timestamp", "00:12 corte a plano general"),
            _bloque(TIPO_NO_LOCUCION, "timestamp", "00:20 corte a detalle"),
            _bloque(TIPO_NO_LOCUCION, "timestamp", "00:45 corte a logo"),
        ],
        resumenes=[],
    )
    consistencias = medir_consistencia_senales([resultado])
    consistencia_timestamp = next(c for c in consistencias if c.senal == "timestamp")
    assert consistencia_timestamp.es_consistente
    assert consistencia_timestamp.apariciones == 3

    propuestas = proponer_convenciones(consistencias)
    assert len(propuestas) == 1
    propuesta = propuestas[0]
    assert propuesta.senal == "timestamp"
    assert propuesta.tipo == TIPO_NO_LOCUCION
    assert "00:12 corte a plano general" in propuesta.ejemplo_antes
    assert Configuracion().rotulos_no_locucion[0] in propuesta.ejemplo_despues
    assert "3" in propuesta.ahorro


def test_senal_inconsistente_no_genera_propuesta() -> None:
    """Una senal que a veces acierta locucion y a veces no_locucion no es lo
    bastante fiable como para proponerla: no hay 'ejemplo antes/despues' honesto."""
    resultado = ResultadoClasificacion(
        bloques=[
            _bloque(TIPO_NO_LOCUCION, "mayusculas", "TITULO EN PANTALLA"),
            _bloque(TIPO_LOCUCION, "mayusculas", "SI ESTO TAMBIEN SE DICE ASI"),
        ],
        resumenes=[],
    )
    consistencias = medir_consistencia_senales([resultado])
    propuestas = proponer_convenciones(consistencias)
    assert propuestas == []


def test_senales_ya_contractuales_no_se_proponen_de_nuevo() -> None:
    """rotulo/cita_bloque ya son la convencion vigente (decision del dueno):
    proponerlas de nuevo no aportaria nada."""
    resultado = ResultadoClasificacion(
        bloques=[
            _bloque(TIPO_LOCUCION, "cita_bloque", "> Frase citada."),
            _bloque(TIPO_NO_LOCUCION, "rotulo", "**LOCUCIÓN**"),
        ],
        resumenes=[],
    )
    consistencias = medir_consistencia_senales([resultado])
    assert proponer_convenciones(consistencias) == []


def test_senal_solo_revisar_no_se_propone() -> None:
    resultado = ResultadoClasificacion(
        bloques=[
            _bloque(TIPO_REVISAR, "sin_senal", "algo ambiguo"),
            _bloque(TIPO_REVISAR, "sin_senal", "otra cosa ambigua"),
        ],
        resumenes=[],
    )
    consistencias = medir_consistencia_senales([resultado])
    assert proponer_convenciones(consistencias) == []


def test_medir_consistencia_agrega_varios_resultados() -> None:
    """Requisito 1: la funcion agrega tantos resultados como se le pasen, para
    poder sumar el guion actual con el historico de guiones ya procesados."""
    resultado_a = ResultadoClasificacion(
        bloques=[_bloque(TIPO_NO_LOCUCION, "timestamp", "00:05 corte")], resumenes=[]
    )
    resultado_b = ResultadoClasificacion(
        bloques=[_bloque(TIPO_NO_LOCUCION, "timestamp", "00:10 corte")], resumenes=[]
    )
    consistencias = medir_consistencia_senales([resultado_a, resultado_b])
    consistencia_timestamp = next(c for c in consistencias if c.senal == "timestamp")
    assert consistencia_timestamp.apariciones == 2
    assert consistencia_timestamp.es_consistente
