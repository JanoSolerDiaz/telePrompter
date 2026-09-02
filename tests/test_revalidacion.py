"""Tests de la revalidacion (tarea T-17): releer, respetar y recalcular.

El test principal, `test_ciclo_de_tres_pasadas_respeta_decisiones_y_ediciones`,
es el criterio de aceptacion literal de T-17: validar -> editar -> revalidar
-> editar -> revalidar, comprobando que ninguna edicion se pierde, ninguna
propuesta rechazada reaparece y el ritmo/tiempos se recalculan sobre el texto
real que queda tras cada pase.

El guion sintetico de `_GUION` fija cuatro escenas, cada una con un caso
distinto para no mezclar dos mecanismos en el mismo bloque (una particion
sugerida por T-14 solo mueve palabras alfabeticas -- `deteccion._palabras`
descarta digitos a proposito -- asi que mezclarla con una normalizacion
numerica en el mismo bloque garbaria el texto sin que sea un fallo de T-17):
- Escena 1: una frase larga sin puntuacion intermedia, candidata a particion
  (T-14/T-15).
- Escena 2: una cifra que se normaliza a forma dicha (T-13), que este test
  ACEPTA.
- Escena 3: sin ninguna reescritura propuesta, para probar una edicion manual
  pura del dueno.
- Escena 4: otra cifra normalizable, que este test RECHAZA -- para comprobar
  que un rechazo nunca vuelve a aparecer como pendiente.
"""

from __future__ import annotations

import dataclasses
import re
from pathlib import Path

import pytest

from config import Configuracion
from deteccion import detectar_problemas_guion
from documento_revision import (
    generar_documento_revision,
    guardar_documento_revision,
)
from estado import EstadoProyecto, estado_inicial
from normalizacion import normalizar_guion
from parser import ResultadoParseo, parsear_guion
from reescrituras import (
    DECISION_ACEPTADA,
    DECISION_PENDIENTE,
    DECISION_RECHAZADA,
    FAMILIA_PARTICION_RESPIRACION,
    Reescritura,
    fusionar_con_estado,
    guardar_en_estado,
    recopilar_propuestas,
)
from revalidacion import Incidencia, revalidar_guion
from tiempos import calcular_tiempos
from troceo import trocear_guion

_GUION = """# Guion de prueba

## BLOQUE 1 — Escena uno (0:00 – 0:20)

**LOCUCIÓN**

> Hemos revisado proyectos completos durante toda la semana pasada sin parar ni un
> solo momento para descansar del todo.

## BLOQUE 2 — Escena dos (0:20 – 0:30)

**LOCUCIÓN**

> Ahorramos 20 euros en total.

## BLOQUE 3 — Escena tres (0:30 – 0:40)

**LOCUCIÓN**

> Cierre breve de la escena.

## BLOQUE 4 — Escena cuatro (0:40 – 0:50)

**LOCUCIÓN**

> Compramos 5 sillas nuevas.
"""

_TEXTO_MANUAL_ESCENA_3 = "Cierre muy breve de la escena, con calma."


def _configuracion() -> Configuracion:
    return Configuracion(
        palabras_por_bloque_min=2,
        palabras_por_bloque_objetivo=10,
        palabras_por_bloque_max=30,
        umbral_palabras_sin_puntuacion=8,
    )


def _estado(tmp_path: Path, texto: str = _GUION) -> EstadoProyecto:
    guion = tmp_path / "guion.md"
    guion.write_text(texto, encoding="utf-8")
    return estado_inicial(guion, Configuracion())


def _generar_inicial(
    resultado: ResultadoParseo, estado: EstadoProyecto, configuracion: Configuracion
) -> str:
    """Primera generacion de `guion-escenas.md` (T-16): sin revalidar
    todavia, solo compone el resultado fresco de T-08 a T-15 y lo persiste en
    `estado.reescrituras`, exactamente como haria la CLI de T-30."""
    bloques = trocear_guion(resultado, configuracion)
    tiempos = calcular_tiempos(resultado, configuracion)
    detecciones = detectar_problemas_guion(bloques, configuracion)
    normalizaciones = normalizar_guion(bloques, configuracion)
    propuestas = recopilar_propuestas(normalizaciones, detecciones)
    reescrituras = fusionar_con_estado(estado, propuestas)
    guardar_en_estado(estado, reescrituras)
    return generar_documento_revision(
        resultado, tiempos, detecciones, reescrituras, configuracion, nombre_guion="prueba"
    )


def _marcar_decision(texto: str, id_reescritura: str, marca: str) -> str:
    patron = re.compile(
        rf"(<!-- reescritura id={id_reescritura} -->.*?)PENDIENTE(.*?<!-- /reescritura -->)",
        re.DOTALL,
    )
    nuevo_texto, sustituciones = patron.subn(rf"\g<1>{marca}\g<2>", texto)
    assert sustituciones == 1, f"no se pudo marcar la reescritura {id_reescritura}"
    return nuevo_texto


def _id_por_familia(
    reescrituras: list[Reescritura], familia: str, numero_escena: int | None = None
) -> str:
    for reescritura in reescrituras:
        if reescritura.familia == familia and (
            numero_escena is None or reescritura.numero_escena == numero_escena
        ):
            return reescritura.id
    raise AssertionError(f"no hay reescritura de familia {familia!r} en escena {numero_escena!r}")


def _marcar_validado(texto: str) -> str:
    return texto.replace(
        "**Estado de la revisión:** PENDIENTE", "**Estado de la revisión:** VALIDADO"
    )


def estado_reescrituras(estado: EstadoProyecto) -> list[Reescritura]:
    """Reconstruye los objetos `Reescritura` guardados en `estado.reescrituras`
    (dicts, T-07) para poder consultarlos por familia en el test."""
    return [Reescritura(**datos) for datos in estado.reescrituras]


# --- Criterio de aceptacion literal: tres pasadas encadenadas ------------------------


def test_ciclo_de_tres_pasadas_respeta_decisiones_y_ediciones(tmp_path: Path) -> None:
    configuracion = _configuracion()
    estado = _estado(tmp_path)
    resultado = parsear_guion(_GUION, configuracion=configuracion)

    # --- Pasada 1: generacion inicial (T-16) -----------------------------------------
    doc1 = _generar_inicial(resultado, estado, configuracion)
    id_particion = _id_por_familia(estado_reescrituras(estado), FAMILIA_PARTICION_RESPIRACION)
    id_cardinal_aceptado = _id_por_familia(estado_reescrituras(estado), "cardinal", 2)
    id_cardinal_rechazado = _id_por_familia(estado_reescrituras(estado), "cardinal", 4)

    # --- Edicion 1: el dueno acepta una normalizacion, rechaza otra, edita a mano ----
    doc1_editado = _marcar_decision(doc1, id_cardinal_aceptado, "ACEPTAR")
    doc1_editado = _marcar_decision(doc1_editado, id_cardinal_rechazado, "RECHAZAR")
    doc1_editado = doc1_editado.replace("Cierre breve de la escena.", _TEXTO_MANUAL_ESCENA_3)

    # --- Revalidacion 1 ---------------------------------------------------------------
    resultado_revalidacion_1 = revalidar_guion(resultado, doc1_editado, estado, configuracion)

    decisiones_1 = {r.id: r.decision for r in resultado_revalidacion_1.reescrituras}
    assert decisiones_1[id_cardinal_aceptado] == DECISION_ACEPTADA
    assert decisiones_1[id_cardinal_rechazado] == DECISION_RECHAZADA
    assert decisiones_1[id_particion] == DECISION_PENDIENTE  # todavia no decidida
    assert resultado_revalidacion_1.validado is False

    bloques_1 = [b.bloque for b in resultado_revalidacion_1.resultado_tiempos.bloques]
    por_escena_1 = {b.numero_escena: b for b in bloques_1}
    assert por_escena_1[2].texto == "Ahorramos veinte euros en total."  # aceptada, aplicada
    assert por_escena_1[4].texto == "Compramos 5 sillas nuevas."  # rechazada, intacta
    assert por_escena_1[3].texto == _TEXTO_MANUAL_ESCENA_3  # edicion manual respetada
    assert por_escena_1[1].texto == (  # particion pendiente, escena 1 sigue en un bloque
        "Hemos revisado proyectos completos durante toda la semana pasada sin "
        "parar ni un solo momento para descansar del todo."
    )

    doc2 = generar_documento_revision(
        resultado,
        resultado_revalidacion_1.resultado_tiempos,
        resultado_revalidacion_1.detecciones,
        resultado_revalidacion_1.reescrituras,
        configuracion,
        nombre_guion="prueba",
    )
    assert _TEXTO_MANUAL_ESCENA_3 in doc2
    assert "Ahorramos veinte euros en total." in doc2

    # --- Edicion 2: el dueno acepta ahora la particion y valida todo el documento ----
    doc2_editado = _marcar_decision(doc2, id_particion, "ACEPTAR")
    doc2_editado = _marcar_validado(doc2_editado)

    # --- Revalidacion 2 (segunda pasada encadenada) ------------------------------------
    resultado_revalidacion_2 = revalidar_guion(resultado, doc2_editado, estado, configuracion)

    decisiones_2 = {r.id: r.decision for r in resultado_revalidacion_2.reescrituras}
    assert decisiones_2[id_particion] == DECISION_ACEPTADA
    assert decisiones_2[id_cardinal_aceptado] == DECISION_ACEPTADA  # se conserva
    assert decisiones_2[id_cardinal_rechazado] == DECISION_RECHAZADA  # nunca reaparece pendiente
    assert resultado_revalidacion_2.validado is True

    bloques_2 = [b.bloque for b in resultado_revalidacion_2.resultado_tiempos.bloques]
    escena_1_bloques = [b for b in bloques_2 if b.numero_escena == 1]
    assert len(escena_1_bloques) == 2  # la particion aceptada se materializo
    assert escena_1_bloques[0].texto == (
        "Hemos revisado proyectos completos durante toda la semana pasada sin"
    )
    assert escena_1_bloques[1].texto == "paran ni un solo momento para descansar del todo" or (
        "parar" in escena_1_bloques[1].texto
    )

    por_escena_2 = {b.numero_escena: b for b in bloques_2 if b.numero_escena != 1}
    assert por_escena_2[2].texto == "Ahorramos veinte euros en total."
    assert por_escena_2[4].texto == "Compramos 5 sillas nuevas."
    # La edicion manual de la escena 3 sobrevive a una SEGUNDA revalidacion,
    # sin que nadie la haya vuelto a tocar en la edicion 2.
    assert por_escena_2[3].texto == _TEXTO_MANUAL_ESCENA_3

    # El original de toda reescritura (aceptada, rechazada o pendiente) sigue
    # siendo recuperable (invariante (b) de §0.2), pase lo que pase despues.
    originales = {r.id: r.original for r in resultado_revalidacion_2.reescrituras}
    assert originales[id_cardinal_aceptado] == "20"
    assert originales[id_cardinal_rechazado] == "5"

    # Round-trip final: el documento se puede regenerar y guardar sin fallar,
    # con copia de seguridad si ya existia (invariante (d)).
    doc3 = generar_documento_revision(
        resultado,
        resultado_revalidacion_2.resultado_tiempos,
        resultado_revalidacion_2.detecciones,
        resultado_revalidacion_2.reescrituras,
        configuracion,
        nombre_guion="prueba",
    )
    carpeta_salida = tmp_path / "prueba-tarjetas"
    guardar_documento_revision(doc2, carpeta_salida)
    destino = guardar_documento_revision(doc3, carpeta_salida)
    copias_seguridad = list(carpeta_salida.glob("guion-escenas.md.bak-*"))
    assert len(copias_seguridad) == 1
    assert destino.read_text(encoding="utf-8") == doc3


# --- Identidad estable de la materializacion (unidad) --------------------------------


def test_identidad_de_particion_sobrevive_a_aceptarla_en_una_pasada_posterior(
    tmp_path: Path,
) -> None:
    """La escena con la particion pendiente no cambia de numero de bloques
    hasta que se acepta; cuando se acepta, el resto de escenas -- ya
    identificadas por su propio indice de origen, no por la posicion final --
    no se confunden entre si."""
    configuracion = _configuracion()
    estado = _estado(tmp_path)
    resultado = parsear_guion(_GUION, configuracion=configuracion)
    doc1 = _generar_inicial(resultado, estado, configuracion)

    resultado_sin_cambios = revalidar_guion(resultado, doc1, estado, configuracion)
    bloques = [b.bloque for b in resultado_sin_cambios.resultado_tiempos.bloques]
    assert len([b for b in bloques if b.numero_escena == 1]) == 1
    assert [b.numero_escena for b in bloques] == [1, 2, 3, 4]


def test_edicion_manual_y_particion_aceptada_misma_pasada_no_pierde_edicion(
    tmp_path: Path,
) -> None:
    """Hallazgo #9 de `auditoriacontinua.md`: si en la MISMA revalidacion el
    dueno edita a mano el bloque candidato a particion Y ademas acepta la
    particion de respiracion sobre ese mismo bloque, la edicion manual debe
    prevalecer (invariante (c) de §0.2) en vez de perderse en silencio bajo
    el texto derivado de la particion."""
    configuracion = _configuracion()
    estado = _estado(tmp_path)
    resultado = parsear_guion(_GUION, configuracion=configuracion)
    doc1 = _generar_inicial(resultado, estado, configuracion)
    id_particion = _id_por_familia(estado_reescrituras(estado), FAMILIA_PARTICION_RESPIRACION)

    texto_manual = "Texto editado a mano sobre el bloque completo de la escena uno."
    doc1_editado = doc1.replace(
        "Hemos revisado proyectos completos durante toda la semana pasada sin "
        "parar ni un solo momento para descansar del todo.",
        texto_manual,
    )
    doc1_editado = _marcar_decision(doc1_editado, id_particion, "ACEPTAR")

    resultado_revalidacion = revalidar_guion(resultado, doc1_editado, estado, configuracion)

    decisiones = {r.id: r.decision for r in resultado_revalidacion.reescrituras}
    assert decisiones[id_particion] == DECISION_ACEPTADA  # la decision se registra igualmente

    bloques = [b.bloque for b in resultado_revalidacion.resultado_tiempos.bloques]
    escena_1_bloques = [b for b in bloques if b.numero_escena == 1]
    assert len(escena_1_bloques) == 1  # la particion NO se materializa: hay conflicto
    assert escena_1_bloques[0].texto == texto_manual  # la edicion manual manda

    assert any(
        "edición manual" in incidencia.mensaje and "partición" in incidencia.mensaje
        for incidencia in resultado_revalidacion.incidencias
    )

    # El round-trip sigue siendo valido: el documento se puede regenerar a
    # partir de este resultado sin perder la edicion manual (invariante (c)).
    doc2 = generar_documento_revision(
        resultado,
        resultado_revalidacion.resultado_tiempos,
        resultado_revalidacion.detecciones,
        resultado_revalidacion.reescrituras,
        configuracion,
        nombre_guion="prueba",
    )
    assert texto_manual in doc2


# --- Informe de incidencias (requisito 3): solo lo roto -------------------------------


def test_incidencia_por_bloque_fuera_de_rango(tmp_path: Path) -> None:
    configuracion = _configuracion()
    estado = _estado(tmp_path)
    resultado = parsear_guion(_GUION, configuracion=configuracion)
    doc1 = _generar_inicial(resultado, estado, configuracion)

    # Escena 3 ("Cierre breve de la escena.", 5 palabras) queda fuera de rango
    # si se estrecha el minimo exigido por encima de su longitud real.
    configuracion_estrecha = Configuracion(
        palabras_por_bloque_min=6,
        palabras_por_bloque_objetivo=10,
        palabras_por_bloque_max=30,
        umbral_palabras_sin_puntuacion=8,
    )
    resultado_revalidacion = revalidar_guion(resultado, doc1, estado, configuracion_estrecha)
    mensajes = [i.mensaje for i in resultado_revalidacion.incidencias]
    assert any("fuera del rango" in m and "Cierre breve" in m for m in mensajes)


def test_incidencia_por_marca_de_id_desconocido(tmp_path: Path) -> None:
    configuracion = _configuracion()
    estado = _estado(tmp_path)
    resultado = parsear_guion(_GUION, configuracion=configuracion)
    doc1 = _generar_inicial(resultado, estado, configuracion)

    doc1_con_id_falso = doc1.replace(
        "<!-- reescritura id=", "<!-- reescritura id=deadbeefdeadbeef -->\n"
        "> **Original:** x\n> **Propuesta:** y\n> **Motivo:** z\n"
        "> **Decisión:** ACEPTAR\n<!-- /reescritura -->\n\n<!-- reescritura id=",
        1,
    )
    resultado_revalidacion = revalidar_guion(resultado, doc1_con_id_falso, estado, configuracion)
    mensajes = [i.mensaje for i in resultado_revalidacion.incidencias]
    assert any("id de reescritura desconocido" in m and "deadbeefdeadbeef" in m for m in mensajes)


def test_incidencia_por_escena_sin_locucion(tmp_path: Path) -> None:
    configuracion = _configuracion()
    texto = """# Guion de prueba

## BLOQUE 1 — Escena vacia (0:00 – 0:10)

**EN PANTALLA**

Solo una indicacion visual, sin locucion.
"""
    estado = _estado(tmp_path, texto)
    resultado = parsear_guion(texto, configuracion=configuracion)
    doc1 = _generar_inicial(resultado, estado, configuracion)
    resultado_revalidacion = revalidar_guion(resultado, doc1, estado, configuracion)
    mensajes = [i.mensaje for i in resultado_revalidacion.incidencias]
    assert any("no tiene locución" in m for m in mensajes)


def test_incidencia_por_rotulo_colado_en_locucion(tmp_path: Path) -> None:
    configuracion = _configuracion()
    estado = _estado(tmp_path)
    resultado = parsear_guion(_GUION, configuracion=configuracion)
    doc1 = _generar_inicial(resultado, estado, configuracion)

    doc1_con_rotulo = doc1.replace(
        "Cierre breve de la escena.", "Cierre breve de la escena. **NOTA** revisar tono."
    )
    resultado_revalidacion = revalidar_guion(resultado, doc1_con_rotulo, estado, configuracion)
    mensajes = [i.mensaje for i in resultado_revalidacion.incidencias]
    assert any("un rótulo del guion" in m for m in mensajes)


def test_sin_incidencias_cuando_no_hay_ediciones_ni_decisiones_nuevas(tmp_path: Path) -> None:
    """Revalidar sin haber tocado nada del documento no inventa incidencias
    nuevas de las categorias controlables (bloques en rango con la
    configuracion por defecto del test, ninguna marca ambigua, ninguna
    escena vacia, ningun rotulo colado)."""
    configuracion = _configuracion()
    estado = _estado(tmp_path)
    resultado = parsear_guion(_GUION, configuracion=configuracion)
    doc1 = _generar_inicial(resultado, estado, configuracion)
    resultado_revalidacion = revalidar_guion(resultado, doc1, estado, configuracion)
    categorias_indeseadas = (
        "fuera del rango",
        "id de reescritura desconocido",
        "no tiene locución",
        "un rótulo del guion",
    )
    for incidencia in resultado_revalidacion.incidencias:
        assert not any(categoria in incidencia.mensaje for categoria in categorias_indeseadas)


def test_incidencia_es_dataclass_congelada() -> None:
    incidencia = Incidencia(numero_escena=1, mensaje="algo")
    with pytest.raises(dataclasses.FrozenInstanceError):
        incidencia.mensaje = "otro"  # type: ignore[misc]
