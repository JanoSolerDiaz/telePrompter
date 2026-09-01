"""Tests de las reescrituras marcadas, aceptables y reversibles (tarea T-15).

Cubre el ciclo completo que pide el criterio de aceptacion literal: proponer,
aceptar una, rechazar otra, revalidar y comprobar que las decisiones se
respetan y el original sigue disponible; ademas de cada requisito por
separado (formato marcado, persistencia en `estado.json`, aplicacion sobre el
texto y el troceo, deshacer global).
"""

from __future__ import annotations

from pathlib import Path

from config import Configuracion
from deteccion import detectar_problemas_bloque
from estado import EstadoProyecto, estado_inicial
from normalizacion import normalizar_bloque
from parser import parsear_guion
from reescrituras import (
    DECISION_ACEPTADA,
    DECISION_PENDIENTE,
    DECISION_RECHAZADA,
    FAMILIA_PARTICION_RESPIRACION,
    aplicar_decisiones,
    aplicar_particion_aceptada,
    aplicar_particiones_aceptadas,
    extraer_decisiones,
    formatear_reescritura,
    fusionar_con_estado,
    guardar_en_estado,
    pendientes,
    recopilar_propuestas,
    revertir_reescrituras,
    texto_con_reescrituras_aceptadas,
)
from troceo import BloqueRespiracion, trocear_guion


def _bloque(texto: str, numero_escena: int = 1) -> BloqueRespiracion:
    return BloqueRespiracion(
        texto=texto,
        numero_escena=numero_escena,
        linea_inicio=1,
        linea_fin=1,
        num_palabras=len(texto.split()),
        corte_forzado=False,
    )


# --- recopilar_propuestas: une T-13 (normalizacion) y T-14 (particion) --------------


def test_recopilar_propuestas_incluye_normalizaciones() -> None:
    bloque = _bloque("En 2026 grabamos.")
    resultado_normalizacion = normalizar_bloque(bloque)
    propuestas = recopilar_propuestas([resultado_normalizacion])
    assert len(propuestas) == 1
    propuesta = propuestas[0]
    assert propuesta.original == "2026"
    assert propuesta.propuesta == "dos mil veintiséis"
    assert propuesta.decision == DECISION_PENDIENTE


def test_recopilar_propuestas_incluye_particion_sin_punto_respiracion() -> None:
    texto = " ".join(["palabra"] * 20)  # sin puntuacion, largo, sin digitos (_palabras los ignora)
    bloque = _bloque(texto)
    resultado_deteccion = detectar_problemas_bloque(bloque)
    propuestas = recopilar_propuestas([], [resultado_deteccion])
    assert len(propuestas) == 1
    propuesta = propuestas[0]
    assert propuesta.familia == FAMILIA_PARTICION_RESPIRACION
    assert propuesta.original == texto
    mitad_a, _, mitad_b = propuesta.propuesta.partition("\n\n")
    assert mitad_a and mitad_b
    assert f"{mitad_a} {mitad_b}" == texto


def test_recopilar_propuestas_ignora_avisos_que_no_admiten_particion() -> None:
    # "de" encadenado dispara cacofonia, no una particion (alcance de T-15: solo
    # forma dicha y respiracion, §0.2).
    bloque = _bloque("El libro de la mesa de la sala de estar de la casa.")
    resultado_deteccion = detectar_problemas_bloque(bloque)
    assert resultado_deteccion.avisos  # hay avisos de cacofonia
    propuestas = recopilar_propuestas([], [resultado_deteccion])
    assert propuestas == []


def test_recopilar_propuestas_sin_resultados_deteccion_no_falla() -> None:
    bloque = _bloque("Texto sin nada que normalizar.")
    resultado_normalizacion = normalizar_bloque(bloque)
    assert recopilar_propuestas([resultado_normalizacion]) == []


# --- Identidad estable (requisito 4) -------------------------------------------------


def test_id_distingue_dos_ocurrencias_del_mismo_original_en_el_mismo_bloque() -> None:
    bloque = _bloque("En 2026 y en 2026 grabamos.")
    resultado = normalizar_bloque(bloque)
    ids = {propuesta.id for propuesta in recopilar_propuestas([resultado])}
    assert len(ids) == 2  # misma familia y original, distinta posicion -> id distinto


def test_id_es_estable_entre_pasadas_con_el_mismo_bloque() -> None:
    bloque = _bloque("En 2026 grabamos.")
    primera = recopilar_propuestas([normalizar_bloque(bloque)])
    segunda = recopilar_propuestas([normalizar_bloque(bloque)])
    assert primera[0].id == segunda[0].id


# --- Formato marcado y lectura de la decision (requisitos 1 y 2) --------------------


def test_formatear_reescritura_muestra_original_propuesta_y_motivo() -> None:
    bloque = _bloque("En 2026 grabamos.")
    propuesta = recopilar_propuestas([normalizar_bloque(bloque)])[0]
    texto = formatear_reescritura(propuesta)
    assert "2026" in texto
    assert "dos mil veintiséis" in texto
    assert propuesta.motivo in texto
    assert "PENDIENTE" in texto


def test_extraer_decisiones_lee_aceptar_y_rechazar() -> None:
    bloque = _bloque("En 2026 grabamos con 15%.")
    propuestas = recopilar_propuestas([normalizar_bloque(bloque)])
    texto_documento = "\n\n".join(formatear_reescritura(p) for p in propuestas)
    # El dueno edita a mano: acepta la primera, rechaza la segunda.
    editado = texto_documento.replace("PENDIENTE", "ACEPTAR", 1)
    editado = editado.replace("PENDIENTE", "RECHAZAR", 1)
    decisiones = extraer_decisiones(editado)
    assert decisiones[propuestas[0].id] == DECISION_ACEPTADA
    assert decisiones[propuestas[1].id] == DECISION_RECHAZADA


def test_extraer_decisiones_es_tolerante_a_mayusculas_y_espacios() -> None:
    bloque = _bloque("En 2026 grabamos.")
    propuesta = recopilar_propuestas([normalizar_bloque(bloque)])[0]
    texto = formatear_reescritura(propuesta).replace(
        "> **Decisión:** PENDIENTE", "> **decision**:    aceptar  "
    )
    assert extraer_decisiones(texto)[propuesta.id] == DECISION_ACEPTADA


def test_extraer_decisiones_bloque_sin_marca_reconocible_se_ignora() -> None:
    texto = "<!-- reescritura id=abc123 -->\nsin marca de decision\n<!-- /reescritura -->"
    assert extraer_decisiones(texto) == {}


def test_aplicar_decisiones_conserva_las_no_mencionadas() -> None:
    bloque = _bloque("En 2026 grabamos con 15%.")
    propuestas = recopilar_propuestas([normalizar_bloque(bloque)])
    decisiones = {propuestas[0].id: DECISION_ACEPTADA}
    resultado = aplicar_decisiones(propuestas, decisiones)
    assert resultado[0].decision == DECISION_ACEPTADA
    assert resultado[1].decision == DECISION_PENDIENTE  # no mencionada, sin cambios


def test_formatear_y_extraer_es_reversible_para_una_reescritura_ya_decidida() -> None:
    bloque = _bloque("En 2026 grabamos.")
    propuesta = recopilar_propuestas([normalizar_bloque(bloque)])[0]
    aceptada = aplicar_decisiones([propuesta], {propuesta.id: DECISION_ACEPTADA})[0]
    texto = formatear_reescritura(aceptada)
    assert "ACEPTAR" in texto
    assert extraer_decisiones(texto)[aceptada.id] == DECISION_ACEPTADA


# --- Persistencia y revalidacion (requisitos 3 y 4) ----------------------------------


def _estado(tmp_path: Path) -> EstadoProyecto:
    guion = tmp_path / "guion.md"
    guion.write_text("# Titulo\n", encoding="utf-8")
    return estado_inicial(guion, Configuracion())


def test_fusionar_con_estado_anade_propuestas_nuevas_como_pendientes(tmp_path: Path) -> None:
    estado = _estado(tmp_path)
    bloque = _bloque("En 2026 grabamos.")
    propuestas = recopilar_propuestas([normalizar_bloque(bloque)])
    fusionadas = fusionar_con_estado(estado, propuestas)
    assert len(fusionadas) == 1
    assert fusionadas[0].decision == DECISION_PENDIENTE


def test_fusionar_con_estado_conserva_decision_ya_tomada(tmp_path: Path) -> None:
    estado = _estado(tmp_path)
    bloque = _bloque("En 2026 grabamos.")
    propuesta = recopilar_propuestas([normalizar_bloque(bloque)])[0]
    decidida = aplicar_decisiones([propuesta], {propuesta.id: DECISION_ACEPTADA})
    guardar_en_estado(estado, decidida)

    # Revalidacion: la misma propuesta vuelve a generarse identica.
    propuesta_recalculada = recopilar_propuestas([normalizar_bloque(bloque)])
    fusionadas = fusionar_con_estado(estado, propuesta_recalculada)
    assert len(fusionadas) == 1
    assert fusionadas[0].decision == DECISION_ACEPTADA  # no se propone de nuevo como pendiente


def test_fusionar_con_estado_no_pierde_reescrituras_que_dejan_de_generarse(
    tmp_path: Path,
) -> None:
    estado = _estado(tmp_path)
    bloque = _bloque("En 2026 grabamos.")
    propuesta = recopilar_propuestas([normalizar_bloque(bloque)])[0]
    decidida = aplicar_decisiones([propuesta], {propuesta.id: DECISION_RECHAZADA})
    guardar_en_estado(estado, decidida)

    # El guion cambio: esta pasada ya no genera ninguna propuesta.
    fusionadas = fusionar_con_estado(estado, [])
    assert len(fusionadas) == 1
    assert fusionadas[0].original == "2026"
    assert fusionadas[0].decision == DECISION_RECHAZADA


def test_pendientes_filtra_las_ya_decididas() -> None:
    bloque = _bloque("En 2026 grabamos con 15%.")
    propuestas = recopilar_propuestas([normalizar_bloque(bloque)])
    decididas = aplicar_decisiones(propuestas, {propuestas[0].id: DECISION_ACEPTADA})
    assert pendientes(decididas) == [decididas[1]]


# --- Aplicacion sobre el texto (requisito 1 de T-15, invariante (b)) ----------------


def test_texto_con_reescrituras_aceptadas_solo_aplica_las_aceptadas() -> None:
    bloque = _bloque("En 2026 grabamos con 15%.")
    propuestas = recopilar_propuestas([normalizar_bloque(bloque)])
    decididas = aplicar_decisiones(
        propuestas, {propuestas[0].id: DECISION_ACEPTADA, propuestas[1].id: DECISION_RECHAZADA}
    )
    resultado = texto_con_reescrituras_aceptadas(bloque, decididas)
    assert "dos mil veintiséis" in resultado  # aceptada: se aplica
    assert "15%" in resultado  # rechazada: el original se conserva


def test_texto_con_reescrituras_pendientes_no_aplica_nada() -> None:
    bloque = _bloque("En 2026 grabamos.")
    propuestas = recopilar_propuestas([normalizar_bloque(bloque)])
    resultado = texto_con_reescrituras_aceptadas(bloque, propuestas)
    assert resultado == bloque.texto


# --- Materializar una particion aceptada (T-14 requisito 6, alcance de T-15) --------


def test_particion_aceptada_sustituye_el_bloque_por_dos() -> None:
    texto = " ".join(["palabra"] * 20)
    bloque = _bloque(texto)
    propuesta = recopilar_propuestas([], [detectar_problemas_bloque(bloque)])[0]
    aceptada = aplicar_decisiones([propuesta], {propuesta.id: DECISION_ACEPTADA})[0]

    resultado = aplicar_particion_aceptada([bloque], aceptada)

    assert len(resultado) == 2
    assert resultado[0].numero_escena == bloque.numero_escena
    assert resultado[0].linea_inicio == bloque.linea_inicio
    mitad_a, mitad_b = aceptada.propuesta.split("\n\n")
    assert resultado[0].texto == mitad_a
    assert resultado[1].texto == mitad_b
    assert f"{resultado[0].texto} {resultado[1].texto}" == texto


def test_particion_rechazada_no_se_materializa() -> None:
    texto = " ".join(["palabra"] * 20)
    bloque = _bloque(texto)
    propuesta = recopilar_propuestas([], [detectar_problemas_bloque(bloque)])[0]
    rechazada = aplicar_decisiones([propuesta], {propuesta.id: DECISION_RECHAZADA})[0]

    resultado = aplicar_particion_aceptada([bloque], rechazada)

    assert resultado == [bloque]


def test_particion_pendiente_no_se_materializa() -> None:
    texto = " ".join(["palabra"] * 20)
    bloque = _bloque(texto)
    propuesta = recopilar_propuestas([], [detectar_problemas_bloque(bloque)])[0]

    assert aplicar_particion_aceptada([bloque], propuesta) == [bloque]


def test_aplicar_particiones_aceptadas_deja_intactos_los_demas_bloques() -> None:
    texto_largo = " ".join(["palabra"] * 20)
    bloque_largo = _bloque(texto_largo, numero_escena=1)
    bloque_normal = _bloque("Un bloque normal y corto.", numero_escena=2)
    propuesta = recopilar_propuestas([], [detectar_problemas_bloque(bloque_largo)])[0]
    aceptada = aplicar_decisiones([propuesta], {propuesta.id: DECISION_ACEPTADA})[0]

    resultado = aplicar_particiones_aceptadas([bloque_largo, bloque_normal], [aceptada])

    assert len(resultado) == 3
    assert resultado[-1] is bloque_normal


# --- Deshacer global (requisito 5) ---------------------------------------------------


def test_revertir_reescrituras_de_una_escena_no_afecta_a_otras() -> None:
    bloque_1 = _bloque("En 2026 grabamos.", numero_escena=1)
    bloque_2 = _bloque("En 2027 grabamos.", numero_escena=2)
    propuestas = recopilar_propuestas(
        [normalizar_bloque(bloque_1), normalizar_bloque(bloque_2)]
    )
    aceptadas = aplicar_decisiones(
        propuestas, {p.id: DECISION_ACEPTADA for p in propuestas}
    )

    resultado = revertir_reescrituras(aceptadas, numero_escena=1)

    por_escena = {r.numero_escena: r.decision for r in resultado}
    assert por_escena[1] == DECISION_RECHAZADA
    assert por_escena[2] == DECISION_ACEPTADA
    # El original nunca desaparece, aunque se revierta (invariante (b)).
    assert {r.original for r in resultado} == {"2026", "2027"}


def test_revertir_reescrituras_global_afecta_a_todo_el_guion() -> None:
    bloque_1 = _bloque("En 2026 grabamos.", numero_escena=1)
    bloque_2 = _bloque("En 2027 grabamos.", numero_escena=2)
    propuestas = recopilar_propuestas(
        [normalizar_bloque(bloque_1), normalizar_bloque(bloque_2)]
    )
    aceptadas = aplicar_decisiones(propuestas, {p.id: DECISION_ACEPTADA for p in propuestas})

    resultado = revertir_reescrituras(aceptadas)

    assert all(r.decision == DECISION_RECHAZADA for r in resultado)


# --- Ciclo completo (criterio de aceptacion literal de T-15) ------------------------


def test_ciclo_completo_proponer_aceptar_rechazar_revalidar(tmp_path: Path) -> None:
    """Proponer, aceptar una, rechazar otra, revalidar y comprobar que las
    decisiones se respetan y el original sigue disponible -- exactamente el
    criterio de aceptacion de T-15."""
    estado = _estado(tmp_path)
    bloque = _bloque("En 2026 grabamos con 15%.")

    # 1. Proponer.
    propuestas = recopilar_propuestas([normalizar_bloque(bloque)])
    assert len(propuestas) == 2
    fusionadas = fusionar_con_estado(estado, propuestas)
    guardar_en_estado(estado, fusionadas)

    # 2. El dueno edita el documento marcado: acepta una, rechaza la otra.
    documento = "\n\n".join(formatear_reescritura(r) for r in pendientes(fusionadas))
    editado = documento.replace("PENDIENTE", "ACEPTAR", 1).replace("PENDIENTE", "RECHAZAR", 1)
    decisiones = extraer_decisiones(editado)
    decididas = aplicar_decisiones(fusionadas, decisiones)
    guardar_en_estado(estado, decididas)

    aceptada = next(r for r in decididas if r.decision == DECISION_ACEPTADA)
    rechazada = next(r for r in decididas if r.decision == DECISION_RECHAZADA)
    assert {aceptada.familia, rechazada.familia} == {"cardinal", "porcentaje"}

    # 3. Revalidar: la misma pasada de T-13 sobre el mismo bloque no vuelve a
    # proponer nada nuevo, y las decisiones ya tomadas se respetan.
    propuestas_revalidadas = recopilar_propuestas([normalizar_bloque(bloque)])
    fusionadas_revalidadas = fusionar_con_estado(estado, propuestas_revalidadas)
    assert len(fusionadas_revalidadas) == 2
    assert pendientes(fusionadas_revalidadas) == []  # nada nuevo que proponer
    por_id = {r.id: r for r in fusionadas_revalidadas}
    assert por_id[aceptada.id].decision == DECISION_ACEPTADA
    assert por_id[rechazada.id].decision == DECISION_RECHAZADA

    # 4. El original sigue disponible para ambas, se hayan aceptado o no.
    assert por_id[aceptada.id].original in ("2026", "15%")
    assert por_id[rechazada.id].original in ("2026", "15%")
    texto_final = texto_con_reescrituras_aceptadas(bloque, fusionadas_revalidadas)
    if aceptada.familia == "cardinal":
        assert "dos mil veintiséis" in texto_final
        assert "15%" in texto_final
    else:
        assert "15 %" not in texto_final or "por ciento" in texto_final
        assert "2026" in texto_final


# --- Cobertura sobre los guiones reales (mismo patron que T-13/T-14) ----------------


def test_pipeline_completo_sobre_guiones_reales_no_pierde_originales(
    texto_guiones_reales: dict[str, str],
) -> None:
    configuracion = Configuracion()
    for texto in texto_guiones_reales.values():
        resultado_parseo = parsear_guion(texto)
        bloques = trocear_guion(resultado_parseo, configuracion)
        resultados_normalizacion = [normalizar_bloque(b, configuracion) for b in bloques]
        resultados_deteccion = [detectar_problemas_bloque(b, configuracion) for b in bloques]

        propuestas = recopilar_propuestas(resultados_normalizacion, resultados_deteccion)
        decididas = aplicar_decisiones(
            propuestas, {p.id: DECISION_ACEPTADA for p in propuestas}
        )
        rechazadas = revertir_reescrituras(decididas)

        # Con todo rechazado, el texto de cada bloque debe seguir siendo el original.
        for bloque in bloques:
            reescrituras_bloque = [
                r
                for r in rechazadas
                if r.numero_escena == bloque.numero_escena
                and r.linea_inicio == bloque.linea_inicio
                and r.linea_fin == bloque.linea_fin
            ]
            assert texto_con_reescrituras_aceptadas(bloque, reescrituras_bloque) == bloque.texto

        # El formato marcado no revienta con texto real (requisito 1).
        for propuesta in propuestas:
            texto_marcado = formatear_reescritura(propuesta)
            assert extraer_decisiones(texto_marcado)[propuesta.id] == DECISION_PENDIENTE
