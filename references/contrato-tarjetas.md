# Contrato `tarjetas.json` — intercambio con la generación del `.pptx` (T-29)

> Genera y valida este contrato `scripts/pptx.py` (`generar_tarjetas`,
> `tarjetas_a_diccionario`, `validar_tarjetas`). Es **estable e independiente del
> generador**: cualquier cosa que lea `tarjetas.json` — la skill `480-branded-pptx`
> delegada por Claude, un script del dueño, una versión futura de este adaptador —
> puede confiar en esta forma exacta sin conocer `scripts/pptx.py`.
>
> `version_contrato` sube solo si el JSON cambia de forma incompatible con este
> documento; nunca decrece (mismo criterio que `VERSION_ESQUEMA_ESTADO` de
> `estado.json`, T-07). Version actual: **1**.

## Forma completa

```jsonc
{
  "version_contrato": 1,
  "metadatos": {
    "titulo": "guion-08-busqueda-investigacion",
    "para_terceros": false,
    "numero_escenas": 7,
    "palabras_locucion_total": 412,
    "duracion_total_segundos": 187.4,
    "duracion_objetivo_total_segundos": [180, 210]   // o null si el guion no trae objetivo
  },
  "escenas": [
    {
      "numero": 0,
      "titulo": "Arranque",
      "duracion_estimada_segundos": 24.1,
      "duracion_objetivo_segundos": 25.0,             // o null
      "aviso_desviacion": null,                        // o el texto del aviso de T-12
      "bloques": [
        "Primer bloque de respiración.",
        "Segundo bloque de respiración."
      ],
      "texto_locucion": "Primer bloque de respiración. Segundo bloque de respiración.",
      "indicaciones_pantalla": ["Título del vídeo en pantalla."],
      "notas_internas": ["Recordatorio interno: no mencionar el precio antiguo."]
    }
  ]
}
```

## Claves de `metadatos` (cabecera, requisito 1 de T-29)

| Clave | Tipo | Significado |
|-------|------|-------------|
| `titulo` | `string` | Nombre del guion (mismo que usan el `.pdf`/`.srt`/reproductor). |
| `para_terceros` | `bool` | `true` si se generó con `--para-terceros` (`Configuracion.incluir_notas_internas=False`). |
| `numero_escenas` | `int` | Debe coincidir con `len(escenas)`; `validar_tarjetas` lo comprueba. |
| `palabras_locucion_total` | `int` | Suma de palabras de locución de todas las escenas. |
| `duracion_total_segundos` | `number` | Duración estimada total (T-12). |
| `duracion_objetivo_total_segundos` | `[number, number]` \| `null` | Horquilla objetivo del metadato de cabecera del guion, si lo trae. |

## Claves de cada elemento de `escenas` (requisito 1)

| Clave | Tipo | Significado |
|-------|------|-------------|
| `numero` | `int` | Número de escena (`## BLOQUE N — …`). |
| `titulo` | `string` | Título de la escena. |
| `duracion_estimada_segundos` | `number` | Duración estimada de la escena (T-12). |
| `duracion_objetivo_segundos` | `number` \| `null` | Duración objetivo de la escena, si el guion la trae en su encabezado. |
| `aviso_desviacion` | `string` \| `null` | Aviso de desviación de T-12 si la estimada se aleja de la objetivo; `null` si no hay. |
| `bloques` | `string[]` | Un elemento por bloque de respiración (T-11), texto **locutado final** (reescrituras aceptadas ya materializadas si viene de una revalidación, T-17). |
| `texto_locucion` | `string` | `bloques` unidos con un espacio — la prosa continua de la escena. |
| `indicaciones_pantalla` | `string[]` | Indicaciones no recitables que NO son nota interna de producción (mismo criterio que `pdf.es_nota_interna`, T-28): `**EN PANTALLA**` y cualquier indicación ambigua sin rótulo `NOTA` claro. |
| `notas_internas` | `string[]` | Indicaciones marcadas `**NOTA**`. **Vacía siempre** que `metadatos.para_terceros` sea `true` — la bandera `--para-terceros` las omite del propio contrato, no solo de la presentación (requisito 3 de T-29). |

## Invariantes que `validar_tarjetas` comprueba

1. Existen `version_contrato`, `metadatos` y `escenas`, con las claves de arriba y su tipo.
2. `metadatos.numero_escenas == len(escenas)`.
3. Ninguna escena queda totalmente vacía: al menos un bloque de locución o una
   indicación de pantalla (nunca una tarjeta sin nada que mostrar).

No depende de `jsonschema` ni de ninguna biblioteca externa (§0.2, sin dependencias de
terceros en el runtime): es una comprobación a mano, mismo patrón que `srt.validar_srt`
(T-27).

## Qué NO lleva este contrato

Igual que `pdf.py` (T-28), nunca lleva el aparato de reescrituras
(`original`/`propuesta`/`decisión`) — esa vista de edición vive solo en
`guion-escenas.md` (T-16). `bloques`/`texto_locucion` ya son el texto decidido.
