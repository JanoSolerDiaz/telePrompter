# Validador de auto-contención — lista completa de patrones vigilados (R-09)

> «Salida autocontenida» (§0.2) es uno de los invariantes más sensibles del producto: un único
> archivo `.html`, cero red en tiempo de ejecución. Esta referencia documenta, de una vez, todo
> lo que `scripts/verificar_salidas.py` (`PATRONES_RECURSO_EXTERNO`, función
> `buscar_recursos_externos`) rechaza — para que quien amplíe el reproductor (`assets/reproductor/`)
> o el HTML de impresión (`assets/pdf/`) sepa qué evitar sin tener que leer el código del
> validador. Si un cambio necesita legítimamente algo de esta lista, la respuesta casi siempre es
> incrustarlo (base64/`data:`), nunca debilitar el validador — ver la decisión de T-28 en
> `DECISIONES_TECNICAS.md` sobre el logotipo incrustado.

## Patrones bloqueados

| Patrón | Qué detecta | Desde |
| --- | --- | --- |
| `https?://` | Cualquier URL absoluta http(s) | T-18 |
| `//cdn\.` | Referencia a un CDN sin esquema explícito | T-18 |
| `<link rel="stylesheet" ...>` | Hoja de estilos enlazada en vez de incrustada | T-18 |
| `@import` de CSS | Importación de otra hoja de estilos | T-18 |
| `fetch(...)` | Llamada a la API `fetch` | T-18 |
| `XMLHttpRequest` | Petición de red por el API clásico | T-18 |
| `src=` en `<script>`/`<img>`/`<iframe>`/`<video>`/`<audio>`/`<source>` | Recurso externo en un atributo `src`, salvo que empiece por `data:` | T-18 |
| `<object>` | Cualquier uso de la etiqueta, con o sin atributo `data` | R-09 |
| `src=` en `<embed>` | Igual que el resto de atributos `src`, salvo `data:` | R-09 |
| `<base href="...">` | Cambia la resolución de toda referencia relativa del documento | R-09 |
| `WebSocket` | Apertura de una conexión WebSocket | R-09 |
| `EventSource` / `sendBeacon` | Server-sent events o envío de telemetría en segundo plano | R-09 |
| `url(...)` de CSS fuera de `@import` | Cualquier `url()` de CSS (`background`, `@font-face`, etc.), salvo que apunte a `data:` | R-09 |

## Excepción `data:`

Los patrones que vigilan un atributo `src=` o un `url()` de CSS permiten explícitamente que el
valor empiece por `data:` (una imagen o fuente incrustada en base64 sigue siendo autocontenida:
no depende de ningún archivo aparte ni de la red). Esta es la única excepción; no existe ninguna
lista blanca de dominios ni de rutas locales — cualquier ruta de archivo relativa también falla el
validador, a propósito (ver la decisión de T-28: incrustar en base64 es la única forma de pasar
la regla sin debilitarla).

## Huecos conocidos, deliberadamente fuera de alcance

Este validador es una comprobación léxica sobre el texto del `.html`, no un intérprete de
JavaScript ni de CSS: no sigue variables, no evalúa plantillas ni construye un DOM. Un vector de
red construido dinámicamente en tiempo de ejecución (por ejemplo, concatenando un string a partir
de trozos que ninguno contiene por separado los patrones de esta tabla) no se detectaría. No se
conoce ningún caso así en el código real del reproductor o del HTML de impresión; si aparece uno,
la respuesta es ampliar esta tabla y `PATRONES_RECURSO_EXTERNO` a la vez, nunca confiar en que el
validador lo habría atrapado.
