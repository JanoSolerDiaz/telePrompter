"""Tests del documento de revision de una sola pasada (tarea T-16).

`test_documento_cubre_todas_las_escenas_y_bloques_en_guiones_reales` es el
criterio de aceptacion literal de T-16 sobre los tres guiones reales (mismo
tratamiento que T-08 a T-15): cobertura total de escenas y bloques de
respiracion, sin perder ninguno.
"""

from __future__ import annotations

import re
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
from normalizacion import FAMILIA_DICCIONARIO, normalizar_bloque
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
    texto: str,
    configuracion: Configuracion | None = None,
    diccionario: dict[str, str] | None = None,
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
    normalizaciones = [normalizar_bloque(b, configuracion, diccionario) for b in bloques]
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


def test_pie_de_escena_ninguna_indicacion_termina_en_separador_de_escena(
    texto_guiones_reales: dict[str, str],
) -> None:
    """R-14: el separador `---` de fin de escena no debe colarse pegado al
    extracto de una indicacion no-locucion del pie de escena, verificado sobre
    los tres guiones reales (criterio de aceptacion de R-14)."""
    patron_extracto = re.compile(r'\*\*\[[A-Z_]+\]\*\* \([^)]+\): "(?P<extracto>[^"]*)"')
    for nombre, texto in texto_guiones_reales.items():
        resultado, tiempos, detecciones, reescrituras = _pipeline(texto)
        documento = generar_documento_revision(resultado, tiempos, detecciones, reescrituras)
        for coincidencia in patron_extracto.finditer(documento):
            extracto = coincidencia.group("extracto")
            assert not extracto.rstrip().endswith("---"), (
                f"{nombre}: indicacion con separador de escena colado: {extracto!r}"
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


# --- Desviaciones de la convencion (R-23) --------------------------------------------

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


def test_desviaciones_se_listan_al_pie_de_la_escena_que_corresponda() -> None:
    """R-23, requisito 1: una desviacion localizada dentro del rango de una
    escena aparece en SU seccion, con su propio encabezado separado de las
    indicaciones no recitables, nunca en la escena equivocada."""
    resultado, tiempos, detecciones, reescrituras = _pipeline(_GUION_CON_DESVIACIONES)
    documento = generar_documento_revision(resultado, tiempos, detecciones, reescrituras)

    inicio_bloque_0 = documento.index("## BLOQUE 0 — Arranque")
    inicio_bloque_1 = documento.index("## BLOQUE 1 — Sin rotulo")
    seccion_bloque_0 = documento[inicio_bloque_0:inicio_bloque_1]
    seccion_bloque_1 = documento[inicio_bloque_1:]

    assert "### Desviaciones de la convención" in seccion_bloque_0
    assert "[rotulo_desconocido]" in seccion_bloque_0
    assert "ALGO RARO" in seccion_bloque_0
    assert "[escena_sin_rotulo_locucion]" not in seccion_bloque_0

    assert "### Desviaciones de la convención" in seccion_bloque_1
    assert "[escena_sin_rotulo_locucion]" in seccion_bloque_1
    assert "[rotulo_desconocido]" not in seccion_bloque_1


def test_desviaciones_sin_escena_van_en_su_propia_seccion_antes_del_cuerpo() -> None:
    """R-23, requisito 1: una desviacion que no cae en ninguna escena (p. ej.
    una seccion auxiliar no reconocida) va en una seccion propia tras el
    resumen global, nunca al pie de ninguna escena."""
    resultado, tiempos, detecciones, reescrituras = _pipeline(_GUION_CON_DESVIACIONES)
    documento = generar_documento_revision(resultado, tiempos, detecciones, reescrituras)

    inicio_seccion = documento.index("## Desviaciones de la convención (fuera de escena)")
    inicio_bloque_0 = documento.index("## BLOQUE 0 — Arranque")
    assert inicio_seccion < inicio_bloque_0
    assert "[seccion_auxiliar_no_reconocida]" in documento[inicio_seccion:inicio_bloque_0]
    assert "Seccion rara sin marcar" in documento[inicio_seccion:inicio_bloque_0]


def test_resumen_global_cuenta_las_desviaciones_de_la_convencion() -> None:
    resultado, tiempos, detecciones, reescrituras = _pipeline(_GUION_CON_DESVIACIONES)
    documento = generar_documento_revision(resultado, tiempos, detecciones, reescrituras)
    assert "**Desviaciones de la convención:** 3" in documento


def test_sin_desviaciones_no_anade_ninguna_seccion_nueva() -> None:
    """Requisito 2 de R-23: `N = 0` no añade ninguna sección nueva al
    documento -- ni al pie de ninguna escena ni fuera de ellas -- solo el
    recuento de cabecera en 0, mismo criterio que ya sigue el resto del
    documento con avisos y reescrituras vacios."""
    resultado, tiempos, detecciones, reescrituras = _pipeline(_GUION_DOS_ESCENAS)
    documento = generar_documento_revision(resultado, tiempos, detecciones, reescrituras)
    assert "**Desviaciones de la convención:** 0" in documento
    assert "### Desviaciones de la convención" not in documento
    assert "## Desviaciones de la convención (fuera de escena)" not in documento


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


# --- Diccionario del dueño aplicado, visible en la cabecera (R-26) ------------------

_GUION_CON_SIGLA = """# Guion de prueba

## BLOQUE 0 — Arranque (0:00 – 0:10)

**LOCUCIÓN**

> La IA ayuda a escribir guiones.
"""


def test_cabecera_cuenta_cero_entradas_de_diccionario_sin_diccionario() -> None:
    resultado, tiempos, detecciones, reescrituras = _pipeline(_GUION_CON_SIGLA)
    documento = generar_documento_revision(resultado, tiempos, detecciones, reescrituras)
    assert "**Diccionario del dueño aplicado:** 0 entradas" in documento


def test_cabecera_cuenta_entradas_de_diccionario_efectivamente_aplicadas() -> None:
    resultado, tiempos, detecciones, reescrituras = _pipeline(
        _GUION_CON_SIGLA, diccionario={"IA": "inteligencia artificial"}
    )
    assert sum(1 for r in reescrituras if r.familia == FAMILIA_DICCIONARIO) == 1
    documento = generar_documento_revision(resultado, tiempos, detecciones, reescrituras)
    assert "**Diccionario del dueño aplicado:** 1 entradas" in documento


def test_sin_carpeta_salida_nunca_hay_aviso_aunque_cero_entradas_aplicadas() -> None:
    """Comportamiento por defecto (sin `carpeta_salida`): solo se cuenta lo
    que ya traen las `reescrituras`, nunca se toca disco ni se avisa de nada
    -- regresion explicita de compatibilidad con las llamadas anteriores a
    R-26, que no conocian este parametro."""
    resultado, tiempos, detecciones, reescrituras = _pipeline(_GUION_CON_SIGLA)
    documento = generar_documento_revision(resultado, tiempos, detecciones, reescrituras)
    assert "diccionario-locucion.json" not in documento


def test_carpeta_salida_con_diccionario_no_aplicado_muestra_aviso_explicito(
    tmp_path: Path,
) -> None:
    """R-26, objetivo literal: si `diccionario-locucion.json` existe con
    entradas pero `reescrituras` no trae ninguna de esa familia (la grieta
    que motivo la tarea -- quien genero el documento olvido cargarlo antes
    de normalizar), `generar_documento_revision` lo advierte en la cabecera
    en vez de quedarse en silencio con el recuento en cero."""
    (tmp_path / "diccionario-locucion.json").write_text(
        '{"IA": "inteligencia artificial"}', encoding="utf-8"
    )
    # Reescrituras calculadas SIN el diccionario -- el escenario del hallazgo.
    resultado, tiempos, detecciones, reescrituras = _pipeline(_GUION_CON_SIGLA)
    documento = generar_documento_revision(
        resultado, tiempos, detecciones, reescrituras, carpeta_salida=tmp_path
    )
    assert "**Diccionario del dueño aplicado:** 0 entradas" in documento
    assert "⚠ diccionario-locucion.json tiene 1 entrada(s)" in documento


def test_carpeta_salida_con_diccionario_aplicado_no_muestra_aviso(tmp_path: Path) -> None:
    """Integracion real (a diferencia de los tests de T-13, que construyen el
    diccionario a mano en memoria): el archivo se escribe en disco, se carga
    con `cargar_diccionario_locucion` (no a mano) y se propaga a
    `normalizar_bloque` antes de generar -- el camino correcto, sin aviso."""
    from normalizacion import cargar_diccionario_locucion

    (tmp_path / "diccionario-locucion.json").write_text(
        '{"IA": "inteligencia artificial"}', encoding="utf-8"
    )
    diccionario = cargar_diccionario_locucion(tmp_path)
    resultado, tiempos, detecciones, reescrituras = _pipeline(
        _GUION_CON_SIGLA, diccionario=diccionario
    )
    documento = generar_documento_revision(
        resultado, tiempos, detecciones, reescrituras, carpeta_salida=tmp_path
    )
    assert "**Diccionario del dueño aplicado:** 1 entradas" in documento
    assert "diccionario-locucion.json" not in documento
