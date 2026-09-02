# Convención de marcado del guion de entrada (T-08 a T-10)

> Contractual, con aviso (decisión del dueño, 2026-08-31, §0.2 de `HOJA_DE_RUTA.md`):
> los rótulos de abajo **mandan siempre**. Cuando un guion se sale de ellos, la skill
> **infiere y avisa** de la desviación — nunca falla ni pregunta por eso. Solo pregunta
> cuando dos señales de inferencia se contradicen de verdad (ver «Conflictos» más abajo).

## Escena

```
## BLOQUE N — <título> (m:ss – m:ss)
```

- `PATRON_ENCABEZADO_ESCENA` (`scripts/config.py`): nivel de encabezado (`##`) y patrón
  exactos. El guion largo (`–`, U+2013) es el que usan los guiones reales del dueño, no
  un guion corto ASCII.
- El rango horario entre paréntesis es la **duración objetivo** de la escena; opcional.
- Si ningún encabezado del nivel esperado casa con el patrón, la skill pregunta por el
  nivel/patrón real en vez de adivinar (`DeteccionEscenasAmbiguaError`).
- El **preámbulo** (texto antes del primer encabezado de cualquier nivel) nunca se trata
  como escena 0: se conserva íntegro pero no entra en el recuento de escenas.

## Texto a recitar

```
**LOCUCIÓN**
> Primer párrafo que se lee tal cual.
> Segundo párrafo.
```

- El rótulo `**LOCUCIÓN**` (`Configuracion.rotulo_locucion`) marca la sección.
- El cuerpo va en **cita de bloque** (`> `): es la mitad de la señal contractual, no un
  detalle tipográfico. Texto suelto (sin `> `) dentro de una sección `**LOCUCIÓN**` se
  clasifica `revisar`, nunca se recita a ciegas — cubre acotaciones de ritmo entre
  comillas y ejemplos de código que no son locución real.

## No recitable

```
**EN PANTALLA**
Texto descriptivo de lo que aparece en pantalla, sin cita de bloque.

**NOTA**
Recordatorio interno de producción.
```

- `Configuracion.rotulos_no_locucion` (`**EN PANTALLA**`, `**NOTA**` por defecto).
- `**NOTA**` es lo único que `--para-terceros` omite (ver T-28/T-29); `**EN PANTALLA**`
  y cualquier indicación ambigua sin rótulo claro se mantienen siempre.

## Secciones auxiliares (no son escena)

`Configuracion.secciones_auxiliares`: lista de títulos fijos que nunca se procesan como
escena aunque casen con el nivel de encabezado esperado (`Capítulos`,
`Preparación antes de grabar`, `Notas de producción` por defecto). El subtítulo
entrecomillado justo tras el título del guion (`# Título` + `## "Subtítulo"`) se
reconoce como auxiliar **por posición** (primer encabezado del nivel separador, con
comillas), sin necesidad de añadirlo a esta lista.

## Metadatos de cabecera

Cualquier par `**Clave:** valor` en el preámbulo se extrae tal cual (sin esquema fijo:
distintos guiones usan claves distintas, p. ej. «Idea única del vídeo» frente a
«Promesa del vídeo»). El motor de tiempos (T-12) busca `Duración objetivo` por nombre.

## Conflictos (cuándo sí se pregunta)

Un encabezado dispara `DeteccionEscenasAmbiguaError` solo cuando **dos señales se
contradicen a la vez**: aparece en la lista negra de `secciones_auxiliares` **y** trae
el rótulo `**LOCUCIÓN**` en el cuerpo. Con una sola señal (solo lista negra, o solo
rótulo) la skill decide sin preguntar — auxiliar en el primer caso, escena en el
segundo — y solo avisa de la desviación si corresponde.

## Diccionario del dueño

`diccionario-locucion.json`, dentro de la carpeta de salida del guion
(`Configuracion.NOMBRE_ARCHIVO_DICCIONARIO_LOCUCION`), tiene prioridad sobre cualquier
regla automática de normalización a forma dicha (T-13). Ausente por defecto.

## Ver también

- `references/formato-guion-escenas.md` — el documento de revisión que genera la skill
  a partir de esta convención.
- `DEVELOPERS.md`, secciones T-08 a T-10 — implementación y casos límite verificados
  contra los tres guiones reales de calibración.
