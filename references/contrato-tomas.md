# Contrato del parte de rodaje — registro de tomas por escena (R-02)

> Genera este archivo el reproductor (`assets/reproductor/guion.js`,
> `construirParteDeRodaje`/`exportarParteDeRodaje`), disparado por el botón
> "Exportar parte de rodaje" del índice. Lo valida y lo fusiona en `estado.json`
> `scripts/tomas.py` (`cargar_parte_de_rodaje`/`registrar_tomas`). Es **estable e
> independiente de quien lo lea**: la fase de montaje, el dueño abriéndolo a mano,
> o una tarea futura (R-04, recalibrar el ritmo con tiempos reales; R-05, `.srt`
> alineado con la toma buena) pueden confiar en esta forma exacta.
>
> `version` sube solo si el JSON cambia de forma incompatible con este documento;
> nunca decrece (mismo criterio que `version_contrato` de `tarjetas.json`, T-29, y
> `VERSION_ESQUEMA_ESTADO` de `estado.json`, T-07). Versión actual: **1**.

## Por qué existe un archivo suelto además de `estado.json`

El reproductor es un único `.html` sin dependencias, ejecutado desde `file://`,
con cero red en tiempo de ejecución (§0.2): no puede escribir directamente en la
carpeta de salida del guion. El registro de tomas vive primero en `localStorage`
del navegador (persistente entre sesiones, mismo mecanismo que T-26/R-01) y se
vuelca a este `.json` independiente cuando el dueño pulsa "Exportar parte de
rodaje" — el archivo es el puente entre el navegador de grabación y el resto del
pipeline, que sí corre en la máquina del dueño con acceso a disco.

## Forma completa

```jsonc
{
  "version": 1,
  "guion": "guion-08-busqueda-investigacion",
  "generado": "2026-09-03T10:00:00.000Z",
  "escenas": [
    {
      "numero": 0,
      "titulo": "Arranque",
      "tomas": [
        { "numero": 1, "duracion_segundos": 24.1, "nota": "muy rápido, repetir", "buena": false },
        { "numero": 2, "duracion_segundos": 26.3, "nota": "", "buena": true }
      ]
    }
  ]
}
```

Solo se incluyen escenas con al menos una toma registrada (una escena sin grabar
todavía no aparece en el archivo, en vez de aparecer con `"tomas": []`).

## Claves de cabecera

| Clave | Tipo | Significado |
|-------|------|-------------|
| `guion` | `string` | Mismo identificador que `nombre_guion` en `generar_reproductor_html(...)` (`datos.guion` en `guion.js`). `cargar_parte_de_rodaje` rechaza un archivo de otro guion. |
| `generado` | `string` | Marca de tiempo ISO-8601 de la exportación (informativa; no se valida). |
| `escenas` | `array` | Ver abajo. |

## Claves de cada elemento de `escenas`

| Clave | Tipo | Significado |
|-------|------|-------------|
| `numero` | `int` | Número de escena (`## BLOQUE N — …`), NO su índice — sobrevive a un troceo distinto tras regenerar el reproductor, mismo criterio que `velocidad_escena_<numero>` de T-26. |
| `titulo` | `string` | Título de la escena en el momento de exportar. |
| `tomas` | `array` | Ver abajo. Nunca vacía en este archivo (una escena sin tomas simplemente no aparece). |

## Claves de cada elemento de `tomas`

| Clave | Tipo | Significado |
|-------|------|-------------|
| `numero` | `int` (> 0) | Orden de la toma dentro de la escena, empieza en 1. |
| `duracion_segundos` | `number` (≥ 0) | Tiempo de reloj real transcurrido durante la toma (mismo cronómetro que T-23, congelado en pausa), redondeado a una décima. |
| `nota` | `string` | Nota rápida escrita durante la grabación (tecla `N`/`n` por defecto, `Configuracion.mapa_teclas_reproductor`). Cadena vacía si no se escribió ninguna. |
| `buena` | `bool` | `true` si esa toma fue marcada como la buena (tecla `G`/`g` por defecto). Como mucho una toma por escena lo tiene a `true`: marcar una nueva desmarca cualquier otra de la misma escena. |

## Cómo se cierra una toma

Una toma se cierra (y pasa a formar parte de este archivo si luego se exporta)
al salir de la escena hacia el índice, al cambiar a otra escena sin pasar por el
índice (flechas arriba/abajo), o al reiniciar la escena en curso (tecla `R`/`r`)
— reiniciar es la forma natural de decir "esta toma no vale, repito": cierra la
que se abandona con el tiempo que llevaba y arranca el cronómetro de cero para
la siguiente, en vez de sumarle el tiempo de la toma fallida.

## `estado.json["tomas"]`: la misma información, fusionada por escena

`scripts/tomas.registrar_tomas` fusiona un parte de rodaje ya validado en
`EstadoProyecto.tomas` (contenedor genérico reservado en la migración `002`),
con esta forma — claves de escena en texto, mismos campos de toma que arriba:

```jsonc
{
  "0": {
    "titulo": "Arranque",
    "tomas": [
      { "numero": 1, "duracion_segundos": 24.1, "nota": "muy rápido, repetir", "buena": false },
      { "numero": 2, "duracion_segundos": 26.3, "nota": "", "buena": true }
    ]
  }
}
```

La fusión reemplaza, escena a escena, con la versión más reciente exportada —
el reproductor siempre exporta su historial completo en memoria, así que nunca
se duplican tomas — y conserva intactas las escenas que un parte concreto ni
siquiera menciona (una exportación parcial nunca borra tomas de una sesión
anterior).

## Invariantes que `cargar_parte_de_rodaje` comprueba

1. El archivo existe, es JSON válido y su raíz es un objeto.
2. `guion` coincide exactamente con el guion sobre el que se está trabajando.
3. Cada escena tiene `numero` numérico; `tomas`, si aparece, es una lista.
4. Cada toma tiene `numero` entero positivo y `duracion_segundos` numérico no
   negativo; `nota` (si aparece) es texto; `buena` (si aparece) se interpreta
   como booleano.

Sin `jsonschema` ni ninguna biblioteca externa (§0.2): comprobación a mano,
mismo patrón que `pptx.validar_tarjetas` (T-29) y `srt.validar_srt` (T-27).
Cualquier archivo que no cumpla esto se rechaza con `RegistroTomasError` y un
mensaje ya accionable en español — nunca se fusiona a medias.
