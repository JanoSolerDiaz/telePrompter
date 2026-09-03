"""Tests del documento de revision de una sola pasada (tarea T-16).

`test_documento_cubre_todas_las_escenas_y_bloques_en_guiones_reales` es el
criterio de aceptacion literal de T-16 sobre los tres guiones reales (mismo
tratamiento que T-08 a T-15): cobertura total de escenas y bloques de
respiracion, sin perder ninguno.
"""

from __future__ import annotations

from pathlib import Path

from config import Configuracion
from deteccion import detectar_problemas_bloque
from documento_revision import (
    MARCA_ESTADO_PENDIENTE,
    MARCA_ESTADO_VALIDADO,
    extraer_estado_revision,
    extraer_texto_bloques,
    formatear_bloque_respiracion,
    formatear_indicaciones,
    generar_documento_revision,
    guardar_documento_revision,
)
from normalizacion import normalizar_bloque
from parser import ResultadoParseo, parsear_guion
from reescrituras import Reescritura, recopilar_propuestas
from tiempos import BloqueConTiempo, ResultadoTiempos, calcular_tiempos
from troceo import BloqueRespiracion, trocear_guion

_GUION_DOS_ESCENAS = """# Guion de prueba

## BLOQUE 0 — Arranque (0:00 – 0:10)

**LOCUCIÓN**

> Esta es la primera frase del bloque. Y esta la segunda, ya con más ritmo.

**EN PANTALLA**

Título del vídeo en pantalla.

## BLOQUE 1 — Cierre (0:10 – 0:20)

**LOCUCIÓN**

> Segunda escena, con su propia frase de cierre para la locución.

Un aparte sin cita de bloque, que debería marcarse revisar.
"""


def _pipeline(
    texto: str, configuracion: Configuracion | None = None
) -> tuple[ResultadoParseo, ResultadoTiempos, list, list[Reescritura]]:  # type: ignore[type-arg]
    """Misma canalizacion que ya usa `test_reescrituras.py` para sus tests
    sobre guiones reales: parsear -> trocear -> tiempos/deteccion/normalizacion
    -> reescrituras. `generar_documento_revision` no vuelve a hacer nada de
    esto por su cuenta, solo compone el resultado."""
    configuracion = configuracion or Configuracion()
    resultado = parsear_guion(texto, configuracion=configuracion)
    bloques = trocear_guion(resultado, configuracion)
    tiempos = calcular_tiempos(resultado, configuracion)
    detecciones = [detectar_problemas_bloque(b, configuracion) for b in bloques]
    normalizaciones = [normalizar_bloque(b, configuracion) for b in bloques]
    reescrituras = recopilar_propuestas(normalizaciones, detecciones)
    return resultado, tiempos, detecciones, reescrituras


# --- Criterio de aceptacion sobre los tres guiones reales --------------------------


def test_documento_cubre_todas_las_escenas_y_bloques_en_guiones_reales(
    texto_guiones_reales: dict[str, str],
) -> None:
    for nombre, texto in texto_guiones_reales.items():
        configuracion = Configuracion()
        resultado, tiempos, detecciones, reescrituras = _pipeline(texto, configuracion)
        documento = generar_documento_revision(
            resultado, tiempos, detecciones, reescrituras, configuracion, nombre_guion=nombre
        )

        for escena in resultado.escenas:
            assert f"## BLOQUE {escena.numero} — {escena.titulo}" in documento, (
                f"{nombre}: falta la escena {escena.numero} en el documento de revision"
            )

        extraidos = extraer_texto_bloques(documento)
        assert len(extraidos) == len(tiempos.bloques), (
            f"{nombre}: el documento no cubre el 100% de los bloques de respiracion "
            f"({len(extraidos)} de {len(tiempos.bloques)})"
        )


def test_documento_abre_legible_como_texto_plano(texto_guiones_reales: dict[str, str]) -> None:
    """El documento es una cadena de texto normal, sin nada que exija un
    visor especial (requisito: "se abre legible en un editor de texto plano")."""
    for texto in texto_guiones_reales.values():
        resultado, tiempos, detecciones, reescrituras = _pipeline(texto)
        documento = generar_documento_revision(resultado, tiempos, detecciones, reescrituras)
        assert isinstance(documento, str)
        assert documento.strip()
        assert "\x00" not in documento


# --- Resumen global (requisito 5) ---------------------------------------------------


def test_resumen_global_incluye_los_campos_del_requisito_5() -> None:
    resultado, tiempos, detecciones, reescrituras = _pipeline(_GUION_DOS_ESCENAS)
    documento = generar_documento_revision(resultado, tiempos, detecciones, reescrituras)

    assert "## Resumen global" in documento
    assert f"**Escenas:** {len(resultado.escenas)}" in documento
    assert f"**Ritmo aplicado:** {tiempos.ritmo.ppm_aplicado} ppm" in documento
    assert tiempos.ritmo.motivo in documento
    total_avisos = sum(len(d.avisos) for d in detecciones)
    assert f"**Avisos de locutabilidad:** {total_avisos}" in documento
    assert "**Reescrituras:**" in documento


def test_cabecera_de_escena_incluye_duracion_palabras_y_bloques() -> None:
    resultado, tiempos, detecciones, reescrituras = _pipeline(_GUION_DOS_ESCENAS)
    documento = generar_documento_revision(resultado, tiempos, detecciones, reescrituras)

    assert "**Duración estimada:**" in documento
    assert "**Palabras:**" in documento
    assert "**Bloques de respiración:**" in documento


# --- Bloques de respiracion numerados (requisito 2) ---------------------------------


def test_bloques_de_respiracion_numerados_desde_uno_por_escena() -> None:
    resultado, tiempos, detecciones, reescrituras = _pipeline(_GUION_DOS_ESCENAS)
    documento = generar_documento_revision(resultado, tiempos, detecciones, reescrituras)

    for numero_escena in (0, 1):
        bloques_escena = [b for b in tiempos.bloques if b.bloque.numero_escena == numero_escena]
        for indice in range(1, len(bloques_escena) + 1):
            assert f"<!-- bloque escena={numero_escena} indice={indice} -->" in documento
            assert f"**Bloque {indice}**" in documento


def test_bloques_sin_locucion_en_la_escena_lo_dice_explicito() -> None:
    guion = """# Guion

## BLOQUE 0 — Solo pantalla (0:00 – 0:05)

**EN PANTALLA**

Nada que decir en esta escena.
"""
    resultado, tiempos, detecciones, reescrituras = _pipeline(guion)
    documento = generar_documento_revision(resultado, tiempos, detecciones, reescrituras)
    assert "*(sin locución en esta escena)*" in documento


# --- Reescrituras marcadas y avisos localizados (requisito 3) -----------------------


def test_reescritura_de_normalizacion_aparece_junto_a_su_bloque() -> None:
    guion = """# Guion

## BLOQUE 0 — Cifras (0:00 – 0:10)

**LOCUCIÓN**

> Tardarás solo 2 minutos en configurarlo.
"""
    resultado, tiempos, detecciones, reescrituras = _pipeline(guion)
    assert reescrituras, "el bloque sintetico deberia disparar al menos una normalizacion"

    documento = generar_documento_revision(resultado, tiempos, detecciones, reescrituras)
    for reescritura in reescrituras:
        assert f"<!-- reescritura id={reescritura.id} -->" in documento
        assert reescritura.propuesta in documento
        assert "**Decisión:** PENDIENTE" in documento


def test_aviso_no_particionable_se_muestra_sin_generar_reescritura() -> None:
    guion = """# Guion

## BLOQUE 0 — Cacofonia (0:00 – 0:10)

**LOCUCIÓN**

> Qué es el registro horario obligatorio para todos.
"""
    resultado, tiempos, detecciones, reescrituras = _pipeline(guion)
    total_avisos = sum(len(d.avisos) for d in detecciones)
    assert total_avisos > 0

    documento = generar_documento_revision(resultado, tiempos, detecciones, reescrituras)
    assert "> ⚠ **Aviso (cacofonia)" in documento
    assert not any(r.familia == "particion_respiracion" for r in reescrituras)


def test_aviso_sin_punto_respiracion_no_se_repite_junto_a_su_reescritura() -> None:
    """Requisito 3: no mostrar dos veces el mismo problema. La familia
    `sin_punto_respiracion` con particion sugerida ya se muestra como
    reescritura marcada (T-15); el aviso plano de esa misma familia no debe
    duplicarse junto a ella. El troceo (T-11) nunca deja pasar un bloque tan
    largo en operacion normal (tope `palabras_por_bloque_max`), asi que --
    igual que hacen los propios tests de T-14 -- se construye el
    `BloqueRespiracion` a mano en vez de esperar a que el troceo lo produzca."""
    palabras = " ".join(f"palabra{n}" for n in range(20))
    bloque = BloqueRespiracion(
        texto=palabras,
        numero_escena=0,
        linea_inicio=5,
        linea_fin=5,
        num_palabras=20,
        corte_forzado=True,
    )
    deteccion = detectar_problemas_bloque(bloque)
    assert any(aviso.familia == "sin_punto_respiracion" for aviso in deteccion.avisos)

    reescrituras = recopilar_propuestas([], [deteccion])
    assert reescrituras, "deberia generar la reescritura de particion (T-15)"

    bloque_con_tiempo = BloqueConTiempo(
        bloque=bloque,
        inicio_segundos=0.0,
        duracion_palabras_segundos=8.0,
        tipo_pausa="ninguna",
        pausa_segundos=0.0,
    )
    texto = formatear_bloque_respiracion(0, 1, bloque_con_tiempo, reescrituras, [deteccion])
    assert f"<!-- reescritura id={reescrituras[0].id} -->" in texto
    assert "Aviso (sin_punto_respiracion)" not in texto


# --- Tropiezos marcados en grabacion (R-03, requisito 3) -----------------------------


def test_bloque_marcado_como_tropiezo_se_destaca() -> None:
    resultado, tiempos, detecciones, reescrituras = _pipeline(_GUION_DOS_ESCENAS)
    texto_bloque_0 = next(
        b.bloque.texto for b in tiempos.bloques if b.bloque.numero_escena == 0
    )
    tropiezos_por_escena = {0: frozenset({texto_bloque_0})}

    documento = generar_documento_revision(
        resultado,
        tiempos,
        detecciones,
        reescrituras,
        tropiezos_por_escena=tropiezos_por_escena,
    )

    assert "🎬 **Tropiezo marcado en grabación:**" in documento


def test_sin_tropiezos_por_escena_no_destaca_nada() -> None:
    """Comportamiento por defecto (parametro opcional): identico al de antes
    de R-03, sin ninguna linea nueva en el documento."""
    resultado, tiempos, detecciones, reescrituras = _pipeline(_GUION_DOS_ESCENAS)
    documento = generar_documento_revision(resultado, tiempos, detecciones, reescrituras)
    assert "Tropiezo marcado en grabación" not in documento


def test_tropiezo_de_otra_escena_no_destaca_bloques_de_esta() -> None:
    resultado, tiempos, detecciones, reescrituras = _pipeline(_GUION_DOS_ESCENAS)
    texto_bloque_0 = next(
        b.bloque.texto for b in tiempos.bloques if b.bloque.numero_escena == 0
    )
    # Mismo texto, pero asociado a una escena que no lo contiene: no debe
    # destacar nada -- el emparejamiento es (escena, texto), no solo texto.
    tropiezos_por_escena = {99: frozenset({texto_bloque_0})}

    documento = generar_documento_revision(
        resultado,
        tiempos,
        detecciones,
        reescrituras,
        tropiezos_por_escena=tropiezos_por_escena,
    )

    assert "Tropiezo marcado en grabación" not in documento


def test_tropiezo_con_texto_que_ya_no_coincide_no_destaca_nada() -> None:
    """El emparejamiento es por texto EXACTO (`references/contrato-tropiezos.md`):
    si el bloque se reescribio entre la grabacion y esta revision, el aviso
    desaparece solo -- no queda una marca obsoleta sobre texto que ya no
    existe."""
    resultado, tiempos, detecciones, reescrituras = _pipeline(_GUION_DOS_ESCENAS)
    tropiezos_por_escena = {0: frozenset({"Este texto ya no esta en ningun bloque."})}

    documento = generar_documento_revision(
        resultado,
        tiempos,
        detecciones,
        reescrituras,
        tropiezos_por_escena=tropiezos_por_escena,
    )

    assert "Tropiezo marcado en grabación" not in documento


# --- Indicaciones no recitables al pie de escena (requisito 4) ----------------------


def test_pie_de_escena_incluye_indicacion_no_locucion_con_motivo() -> None:
    resultado, tiempos, detecciones, reescrituras = _pipeline(_GUION_DOS_ESCENAS)
    documento = generar_documento_revision(resultado, tiempos, detecciones, reescrituras)
    assert "**[NO_LOCUCION]**" in documento
    assert "Título del vídeo en pantalla" in documento
    assert "rotulo" in documento.lower()


def test_pie_de_escena_incluye_bloques_revisar() -> None:
    resultado, tiempos, detecciones, reescrituras = _pipeline(_GUION_DOS_ESCENAS)
    documento = generar_documento_revision(resultado, tiempos, detecciones, reescrituras)
    assert "**[REVISAR]**" in documento
    assert "Un aparte sin cita de bloque" in documento


def test_formatear_indicaciones_sin_bloques_dice_ninguna() -> None:
    assert formatear_indicaciones([]) == "*(ninguna)*"


def test_formatear_indicaciones_trunca_extractos_largos() -> None:
    from clasificador import TIPO_NO_LOCUCION, BloqueClasificado

    bloque = BloqueClasificado(
        tipo=TIPO_NO_LOCUCION,
        contenido="palabra " * 60,
        linea_inicio=10,
        linea_fin=10,
        motivo="prueba de truncado",
        senal="prefijo",
    )
    configuracion = Configuracion(longitud_extracto_indicacion_max=20)
    texto = formatear_indicaciones([bloque], configuracion)
    inicio_extracto = texto.index('"') + 1
    fin_extracto = texto.index('"', inicio_extracto)
    assert len(texto[inicio_extracto:fin_extracto]) <= 20


# --- Editable a mano sin romper el formato (requisito 7) ----------------------------


def test_extraer_texto_bloques_recupera_edicion_manual(tmp_path: Path) -> None:
    resultado, tiempos, detecciones, reescrituras = _pipeline(_GUION_DOS_ESCENAS)
    documento = generar_documento_revision(resultado, tiempos, detecciones, reescrituras)

    original = "Esta es la primera frase del bloque."
    editado = documento.replace(original, "ESTA es la primera frase, corregida a mano.")
    assert editado != documento

    textos = extraer_texto_bloques(editado)
    assert textos[(0, 1)] == "ESTA es la primera frase, corregida a mano."


def test_extraer_texto_bloques_no_incluye_reescrituras_ni_avisos() -> None:
    guion = """# Guion

## BLOQUE 0 — Cifras (0:00 – 0:10)

**LOCUCIÓN**

> Tardarás solo 2 minutos en configurarlo.
"""
    resultado, tiempos, detecciones, reescrituras = _pipeline(guion)
    documento = generar_documento_revision(resultado, tiempos, detecciones, reescrituras)
    textos = extraer_texto_bloques(documento)
    assert textos[(0, 1)] == "Tardarás solo 2 minutos en configurarlo."
    assert "reescritura" not in textos[(0, 1)]
    assert "Decisión" not in textos[(0, 1)]


def test_extraer_estado_revision_por_defecto_pendiente() -> None:
    resultado, tiempos, detecciones, reescrituras = _pipeline(_GUION_DOS_ESCENAS)
    documento = generar_documento_revision(resultado, tiempos, detecciones, reescrituras)
    assert extraer_estado_revision(documento) == MARCA_ESTADO_PENDIENTE
    assert extraer_estado_revision("texto sin ninguna marca") == MARCA_ESTADO_PENDIENTE


def test_extraer_estado_revision_detecta_validado_tolerante_a_formato() -> None:
    variantes = [
        "> **Estado de la revisión:** VALIDADO",
        "Estado de la revision:   validado",
        "**Estado de la revisión**: VALIDADO",
    ]
    for variante in variantes:
        assert extraer_estado_revision(variante) == MARCA_ESTADO_VALIDADO


# --- Persistencia sin borrado destructivo (invariante (d) de §0.2) -----------------


def test_guardar_documento_revision_escribe_el_archivo(tmp_path: Path) -> None:
    destino = guardar_documento_revision("contenido de prueba", tmp_path)
    assert destino.name == "guion-escenas.md"
    assert destino.read_text(encoding="utf-8") == "contenido de prueba"


def test_guardar_documento_revision_hace_copia_de_seguridad_si_ya_existia(
    tmp_path: Path,
) -> None:
    guardar_documento_revision("version original", tmp_path)
    guardar_documento_revision("version nueva", tmp_path)

    destino = tmp_path / "guion-escenas.md"
    assert destino.read_text(encoding="utf-8") == "version nueva"

    copias = list(tmp_path.glob("guion-escenas.md.bak-*"))
    assert len(copias) == 1
    assert copias[0].read_text(encoding="utf-8") == "version original"
