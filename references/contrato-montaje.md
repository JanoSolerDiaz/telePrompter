# Encaje con la cadena de montaje de vídeo (T-33)

> Esta skill termina donde empieza la fase de montaje (recorte y edición con
> ffmpeg u otra herramienta): esta página documenta el contrato exacto que le
> deja preparado — qué archivos, con qué nombre, en qué carpeta, y qué puede y
> qué NO puede asumir todavía la skill de montaje sobre ellos.

## Carpeta y nombres de archivo

Todas las salidas de un guion viven en una única carpeta, siempre dentro de la
carpeta del propio guion (`scripts/entrada.carpeta_salida_para`, regla de
aislamiento, §0.2 de `HOJA_DE_RUTA.md`):

```
<carpeta-del-guion>/<nombre-guion>-tarjetas/
├── estado.json              # estado del proyecto (T-07); no lo consume el montaje
├── guion-escenas.md         # documento de revisión (T-16/T-17); no lo consume el montaje
├── reproductor.html         # teleprompter (T-18+); no lo consume el montaje
├── guion.srt                # subtítulos borrador (T-27) — CONTRATO DE MONTAJE
├── guion-impresion.html     # HTML de impresión (T-28)
├── guion.pdf                # si hubo Chrome/Edge disponible (T-28)
├── tarjetas.json            # contrato de tarjetas (T-29) — CONTRATO DE MONTAJE
├── brief-pptx.md            # brief de invocación a 480-branded-pptx (T-29)
├── diccionario-locucion.json  # opcional, del dueño (T-13)
└── teleprompter.log         # diagnóstico técnico (T-02); no lo consume el montaje
```

El sufijo `-tarjetas` y el resto de nombres son los que produce hoy el código
(`config.NOMBRE_ARCHIVO_*`); el hallazgo #6 de `auditoriacontinua.md` (severidad
baja, abierto) ya deja constancia de que ese sufijo es un nombre heredado de
antes de renombrar el proyecto a `teleprompter` — la skill de montaje no debe
fijarse en el sufijo en sí, solo en que es la misma carpeta que contiene
`guion.srt` y `tarjetas.json` de un mismo guion.

De todo lo anterior, **la fase de montaje solo necesita leer dos archivos**:
`guion.srt` y `tarjetas.json`. El resto es documentación y herramientas de
producción para el dueño, no entrada de la cadena de montaje.

## Nombres y orden de escenas (requisito 2 de T-33)

El `numero` de cada escena es el capturado del encabezado del guion de origen
(`## BLOQUE N — <título>`, `references/convencion-guion.md`) y **es la única
clave que permite casar una toma grabada con su escena sin ambigüedad**: no hay
ningún otro identificador de escena en el sistema.

Para que ese emparejamiento sea seguro, la cadena de montaje puede asumir que,
en un guion sin desviaciones señaladas:

1. **`numero` es único** dentro del guion (ninguna escena repite el número de otra).
2. **`numero` es estrictamente creciente** en el mismo orden en que aparecen las
   escenas en el documento — el mismo orden en el que aparecen en `tarjetas.json`
   (`escenas`, T-29) y en el que se generan los bloques del `.srt` (T-27).
3. Ese orden de documento es también el orden de grabación previsto: la escena
   `numero=0` se graba primero, y así sucesivamente.

Estas dos primeras propiedades ya NO se dan siempre por supuestas en silencio:
`convencion.detectar_desviaciones` (T-10, ampliada en T-33) señala
`numero_escena_duplicado` y `numero_escena_no_creciente` como desviaciones —
nunca bloquean el proceso (la escena se sigue generando con el número tal cual
viene del encabezado, igual que el resto de desviaciones de esa función), pero
si aparecen, la cadena de montaje no debe confiar en el número de escena para
casar tomas hasta que el guion de origen se corrija. Los tres guiones reales de
`fixtures/reales/` y el guion de ejemplo de `fixtures/guion-ejemplo.md` (T-32)
numeran sus escenas `0, 1, 2, …` sin huecos ni repeticiones — la convención que
`references/convencion-guion.md` ya documenta como recomendada, ahora también
verificada.

## `guion.srt` — qué puede y qué NO puede asumir el montaje

- Es **un único archivo para el guion completo**, con una línea de tiempo
  continua desde `00:00:00,000` (T-27, requisito 1-2): no hay un `.srt` por
  escena.
- Los tiempos son **estimados** a partir del ritmo deducido del guion (T-12),
  no del tiempo real de una toma grabada. Alinear el `.srt` con la toma buena
  de verdad es trabajo de una fase posterior, todavía no implementada
  (`R-05 — .srt alineado con la toma buena`, `roadmap/ROADMAP_PRODUCTO.md`).
- El propio texto del `.srt` **no lleva ninguna marca de escena** (ni número ni
  separador): un lector de subtítulos solo ve índice, marca de tiempo y texto.
  Para saber a qué escena pertenece un subtítulo concreto, la cadena de montaje
  debe cruzarlo con `tarjetas.json` (ver siguiente sección) — nunca intentar
  adivinarlo por el contenido del texto.
- `srt.validar_srt` ya aplica las mismas reglas que un lector estricto tipo
  ffmpeg (índice secuencial desde 1, marca de tiempo bien formada, sin solapes
  ni tiempos decrecientes, ninguna línea por encima de
  `Configuracion.srt_caracteres_por_linea_max`): un `.srt` que pase esa
  validación es, por construcción, consumible por ffmpeg sin avisos.

## `tarjetas.json` — cómo derivar el tiempo de cada escena

`tarjetas.json` (`references/contrato-tarjetas.md`, T-29) no lleva un
`inicio_segundos`/`fin_segundos` absoluto por escena, solo
`duracion_estimada_segundos` (relativa) en el mismo orden que las escenas
aparecen en el guion. Como esas duraciones son exactamente las que usó T-12
para acumular los tiempos del `.srt` (misma fuente única de tiempos,
`tiempos.calcular_tiempos`), la cadena de montaje puede recuperar el instante
de inicio de la escena `k` sumando las duraciones de las escenas anteriores:

```
inicio_escena[k] = suma(duracion_estimada_segundos de escenas[0..k-1])
fin_escena[k]    = inicio_escena[k] + duracion_estimada_segundos de escenas[k]
```

y la suma de `duracion_estimada_segundos` de todas las escenas es exactamente
`metadatos.duracion_total_segundos`, que a su vez es el instante en que termina
el último subtítulo del `.srt` (verificado por
`tests/test_integracion_montaje.py`, T-33). Con ese rango `[inicio_escena,
fin_escena)` por escena, cualquier subtítulo del `.srt` cuyo intervalo cae
dentro de él pertenece a esa escena, sin ambigüedad, mientras no haya
desviaciones de numeración (sección anterior).

## Qué queda fuera de esta tarea

- **Registro de tomas por escena** (grabar más de una toma, marcar cuál es la
  buena): `R-02` del `ROADMAP_PRODUCTO.md`, todavía `PENDIENTE`.
- **Recalibrar el ritmo con tiempos reales** una vez grabada la toma buena:
  `R-04`, `PENDIENTE` — hoy el `.srt`/`tarjetas.json` solo tienen la duración
  *estimada*, nunca la real.
- **`.srt` alineado con la toma buena**: `R-05`, `PENDIENTE`, depende de R-02 y
  R-04.

T-33 no adelanta ninguna de esas tres: solo dejar documentado y verificado el
contrato de lo que ya existe (`.srt` + `tarjetas.json` + estructura de
carpetas), para que esas tareas futuras — y la skill de montaje que las
consuma — no tengan que averiguarlo leyendo código.
