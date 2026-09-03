# Contrato de tropiezos marcados en grabación (R-03)

> Genera el archivo `.json` el reproductor (`assets/reproductor/guion.js`,
> `construirRegistroTropiezos`/`exportarRegistroTropiezos`), disparado por el
> botón "Exportar tropiezos" del índice. Lo valida y lo vuelca a `FEEDBACK.md`
> (dentro de la carpeta de salida del guion) `scripts/feedback.py`
> (`cargar_registro_tropiezos`/`registrar_tropiezos_en_feedback`). Es
> **estable e independiente de quien lo lea**: el dueño abriéndolo a mano, o
> `scripts/documento_revision.py` destacando los bloques en la siguiente
> revisión (`tropiezos_marcados_por_escena`), pueden confiar en esta forma
> exacta.
>
> `version` sube solo si el JSON cambia de forma incompatible con este
> documento; nunca decrece (mismo criterio que `version` de
> `references/contrato-tomas.md`). Versión actual: **1**.

## Aviso de nombre: dos `FEEDBACK.md` distintos

`roadmap/FEEDBACK.md` es la bandeja de historias de usuario del propio
proyecto teleprompter, gestionada por el ciclo de Product Manager (ver
`roadmap/HOJA_DE_RUTA.md` §0.4) — vive en el repositorio de la skill, no en
la carpeta de salida de ningún guion, y el programador no escribe ahí
directamente.

El `FEEDBACK.md` de este contrato es **otro archivo**: uno por cada guion
procesado, dentro de SU carpeta de salida (`NOMBRE_ARCHIVO_FEEDBACK` en
`config.py`), con los bloques que el dueño marcó como tropiezo mientras
grababa ESE guion. Comparten nombre de archivo por coincidencia de
vocabulario del roadmap, no propósito ni ubicación.

## Por qué existe un archivo suelto además de `estado.json`

El reproductor es un único `.html` sin dependencias, ejecutado desde
`file://`, con cero red en tiempo de ejecución (§0.2): no puede escribir
directamente en la carpeta de salida del guion. El marcado de tropiezos vive
primero en `localStorage` del navegador (persistente entre sesiones, mismo
mecanismo que T-26/R-01/R-02) y se vuelca a un `.json` independiente cuando
el dueño pulsa "Exportar tropiezos" — el archivo es el puente entre el
navegador de grabación y el resto del pipeline, que sí corre en la máquina
del dueño con acceso a disco.

A diferencia de R-02 (que fusiona el parte de rodaje en `estado.json`), R-03
está marcada explícitamente **"Migración: No"** en `ROADMAP_PRODUCTO.md`: no
añade ningún contenedor nuevo al esquema de estado. `FEEDBACK.md` (carpeta de
salida) es en sí mismo el registro persistente — no hace falta una segunda
copia en `estado.json` para que sobreviva entre sesiones, igual que
`guion-escenas.md` no necesita una copia ahí.

## Forma completa del `.json` exportado

```jsonc
{
  "version": 1,
  "guion": "guion-08-busqueda-investigacion",
  "generado": "2026-09-03T10:00:00.000Z",
  "escenas": [
    {
      "numero": 3,
      "titulo": "Búsqueda avanzada",
      "tropiezos": [
        { "indice_bloque": 0, "texto": "Texto exacto del bloque marcado." },
        { "indice_bloque": 2, "texto": "Otro bloque marcado en la misma escena." }
      ]
    }
  ]
}
```

Solo se incluyen escenas con al menos un bloque marcado (una escena sin
tropiezos no aparece en el archivo).

## Claves de cabecera

| Clave | Tipo | Significado |
|-------|------|-------------|
| `guion` | `string` | Mismo identificador que `nombre_guion` en `generar_reproductor_html(...)` (`datos.guion` en `guion.js`). `cargar_registro_tropiezos` rechaza un archivo de otro guion. |
| `generado` | `string` | Marca de tiempo ISO-8601 de la exportación (informativa; no se valida). |
| `escenas` | `array` | Ver abajo. |

## Claves de cada elemento de `escenas`

| Clave | Tipo | Significado |
|-------|------|-------------|
| `numero` | `int` | Número de escena (`## BLOQUE N — …`), NO su índice. |
| `titulo` | `string` | Título de la escena en el momento de exportar. |
| `tropiezos` | `array` | Ver abajo. Nunca vacío en este archivo (una escena sin tropiezos simplemente no aparece). |

## Claves de cada elemento de `tropiezos`

| Clave | Tipo | Significado |
|-------|------|-------------|
| `indice_bloque` | `int` (≥ 0) | Índice del bloque de respiración dentro de `datos.escenas[i].bloques` en el reproductor que lo generó — el mismo orden que consume `documento_revision._bloques_de_escena`. Es una pista secundaria (ver más abajo): el emparejamiento real con `guion-escenas.md` se hace por `texto`. |
| `texto` | `string` (no vacío, sin `\|` ni saltos de línea) | El texto EXACTO del bloque en el momento de marcarlo (requisito 2 literal, "texto exacto"). Es el criterio de verdad: `documento_revision.py` destaca un bloque cuando su texto coincide con este, no cuando su índice coincide. |

## Por qué se casa por texto, no por índice

El índice de un bloque dentro de una escena puede desplazarse entre la
grabación y la siguiente revisión: una partición de respiración aceptada
(T-15) desplaza los índices de los bloques posteriores de la misma escena
(mismo fenómeno que ya documenta `revalidacion.py` para la identidad estable
`(numero_escena, indice_original, mitad)`). El texto de un bloque de
respiración, en cambio, no cambia salvo que alguien lo reescriba a
propósito — y si se reescribió, el tropiezo marcado sobre el texto viejo ya
no tiene sentido destacarlo, así que dejar de encontrar coincidencia es el
comportamiento correcto, no un fallo. `indice_bloque` se conserva en el
archivo solo como referencia legible para el dueño (para ubicar el bloque a
ojo en el `.json`), nunca como clave de emparejamiento.

## `FEEDBACK.md` (carpeta de salida): la misma información, en una tabla legible

`scripts/feedback.registrar_tropiezos_en_feedback` vuelca cada tropiezo del
`.json` exportado a una fila nueva de `FEEDBACK.md`, en estado `nuevo`:

```markdown
# FEEDBACK — guion-08-busqueda-investigacion

> Bloques de locución marcados como tropiezo durante la grabación (R-03): ...

| Fecha | Escena | Bloque | Texto exacto | Estado |
|-------|--------|--------|---------------|--------|
| 2026-09-03 | 3 | 0 | Texto exacto del bloque marcado. | nuevo |
| 2026-09-03 | 3 | 2 | Otro bloque marcado en la misma escena. | nuevo |
```

**Nunca borra ni reescribe una fila existente**: solo añade filas nuevas al
final, y solo las que no estuvieran ya (misma escena, mismo `indice_bloque`,
mismo texto) — exportar el mismo registro dos veces no duplica filas. Si el
archivo ya existía, se copia antes a `<nombre>.bak-<marca>` (invariante (d)
de §0.2), igual que `documento_revision.guardar_documento_revision` con
`guion-escenas.md`.

**Ciclo de vida de una fila** (mismo patrón "una palabra que el dueño
sobrescribe" que usan T-15/T-16 para las decisiones de reescritura): mientras
el `Estado` de una fila siga siendo `nuevo`, `tropiezos_marcados_por_escena`
la incluye y `documento_revision.generar_documento_revision` destaca el
bloque correspondiente en `guion-escenas.md`. El dueño puede cambiar la
palabra `nuevo` por cualquier otra (`resuelto`, `descartado`...) para dejar
de verlo destacado sin tener que tocar el texto del bloque — útil cuando el
problema no era el texto, sino la propia lectura del locutor esa toma.

## Invariantes que `cargar_registro_tropiezos` comprueba

1. El archivo existe, es JSON válido y su raíz es un objeto.
2. `guion` coincide exactamente con el guion sobre el que se está trabajando.
3. Cada escena tiene `numero` numérico; `tropiezos`, si aparece, es una lista.
4. Cada tropiezo tiene `indice_bloque` entero no negativo y `texto` una
   cadena no vacía, sin `\n` ni `|` (romperían la fila de la tabla de
   `FEEDBACK.md`).

Sin `jsonschema` ni ninguna biblioteca externa (§0.2): comprobación a mano,
mismo patrón que `tomas.cargar_parte_de_rodaje` (R-02). Cualquier archivo que
no cumpla esto se rechaza con `RegistroFeedbackError` y un mensaje ya
accionable en español — nunca se fusiona a medias.
