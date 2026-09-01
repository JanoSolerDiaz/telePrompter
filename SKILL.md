---
name: teleprompter
description: Convierte un guion de produccion en .md en tarjetas de locucion y un teleprompter web autocontenido con resaltado tipo karaoke. Usala cuando el usuario hable de "tarjetas de locucion", "teleprompter", "guion para grabar", "bloques de respiracion", "que tengo que recitar", o cuando pida preparar la locucion de un video a partir de un guion en Markdown, o generar subtitulos .srt borrador desde ese guion.
---

# teleprompter — del guion a la camara

> **BORRADOR (T-00).** Este archivo se completa en T-31, que exige que toda opcion por
> defecto del codigo aparezca aqui documentada, con un test que falla si divergen.
> De momento describe el flujo previsto y lo ya decidido.

Tres pasos: **guion → validacion → salidas**.

1. **Guion.** Le pasas un `.md`. La skill lo trocea en escenas, separa lo que se recita de lo que no, lo parte en bloques de respiracion y estima tiempos.
2. **Validacion.** Genera `guion-escenas.md` con todo anotado. Lo revisas **de una sola pasada en tu editor**, editas lo que quieras y dices «validado».
3. **Salidas.** Te pregunta cada vez cuales generar: el reproductor `.html` (principal), `.pptx` con marca 480, `.pdf` y `.srt` borrador.

## Reglas que esta skill no rompe nunca

- **Nada se descarta en silencio:** todo bloque del guion queda clasificado con su motivo a la vista.
- **El texto del dueno manda:** las reescrituras se proponen marcadas, el original siempre es recuperable y una edicion manual jamas se sobrescribe al revalidar.
- **El reproductor es UN archivo `.html`**, sin dependencias ni CDN, que funciona offline con doble clic.
- **Cero red y cero dependencias en ejecucion:** solo biblioteca estandar de Python 3.
- **Todo se escribe dentro de la carpeta de salida del guion**, nunca fuera, y nada se sobrescribe sin copia `.bak`.

## Convencion de guion (contractual, con aviso)

Los rotulos mandan. Cuando faltan, la skill infiere y **avisa** de la desviacion; nunca falla por ello.

| Elemento | Marca |
|----------|-------|
| Escena | `## BLOQUE N — <titulo> (m:ss – m:ss)` |
| Texto a recitar | `**LOCUCIÓN**` y el cuerpo en cita de bloque (`> `) |
| No recitable | `**EN PANTALLA**`, `**NOTA**` |
| Secciones auxiliares | `Capítulos`, `Preparación antes de grabar`, `Notas de producción` |

## Normalizacion a forma dicha (T-13)

El texto de la tarjeta es exactamente lo que hay que decir: nunca hay que traducir mentalmente una cifra o una sigla al leer en voz alta. Cada familia de regla propone una reescritura marcada (original y propuesta a la vez, nunca se pierde el texto de partida); el diccionario del dueno manda siempre sobre cualquiera de ellas.

| Familia | Ejemplo | Por defecto |
|---------|---------|-------------|
| Cardinales y anios | `2026` → «dos mil veintiséis» | Lectura completa en espanol; apocope («un»/«veintiún») y concordancia de genero solo si hay un sustantivo justo detras, por heuristica de sufijo (`config.py`, sin lista exhaustiva) |
| Ordinales | `1ª` → «primera», `3er` → «tercer» | Del 1º al 10º; fuera de ese rango no se propone nada |
| Porcentajes | `15 %` → «quince por ciento» | — |
| Monedas | `1.500 €` → «mil quinientos euros» | `SIMBOLOS_MONEDA` (`€`, `$`); con decimales, «con N céntimos» |
| Unidades abreviadas | `10 km` → «diez kilómetros» | `UNIDADES_ABREVIADAS` (km, kg, cm, mm, min, seg, h, m) |
| Rangos y fracciones | `10-250` → «diez a doscientos cincuenta»; `3/4` → «tres partido por cuatro» | — |
| Simbolos sueltos | `+` → «más», `>` → «mayor que» | `/` solo se lee dentro de una fraccion (ambiguo suelto, no se toca) |
| Siglas | `SVG` → «ese uve ge» | Deletreo letra a letra si no hay entrada en el diccionario del dueno |
| Conjunciones | `Fernando y Iker` → «Fernando e Iker»; `siete o ocho` → «siete u ocho» | Regla estandar del espanol, con la excepcion del diptongo `hie-`/`hia-` |
| Diccionario del dueno | `diccionario-locucion.json` en la carpeta de salida | Prioridad sobre cualquier regla automatica de esta tabla; ausente por defecto |

## Detector de problemas de lectura en voz alta (T-14)

Avisa de lo que va a costar decir antes de grabar. **Solo avisa, no reescribe** (salvo la excepcion de la primera fila): severidad y recomendacion por bloque de respiracion, nunca un texto sustituido en su lugar.

| Familia | Ejemplo de aviso | Por defecto |
|---------|-------------------|-------------|
| Frase sin punto de respiracion | Bloque largo sin coma ni guion dentro | ≥ 15 palabras sin puntuacion intermedia; unica familia que puede sugerir una particion (no la aplica: T-15 decide) |
| Cacofonias | «de» encadenado, silaba inicial repetida, rima involuntaria | Ventana de 6 palabras; heuristica de prefijo/sufijo de caracteres, no un silabeador real |
| Trabalenguas | Grupo de 4+ consonantes seguidas, o 3+ palabras de 10+ caracteres seguidas | `config.py` |
| Anglicismos | `feedback` → «retroalimentacion» | `ANGLICISMOS_COMUNES` (email, link, online, workshop...) |
| Estructuras dificiles | Incisos acumulados, subordinadas encadenadas, doble negacion, voz pasiva larga | `config.py` |

## Valores por defecto (extracto — la tabla completa la cierra T-31)

Todos viven en `scripts/config.py`, unico lugar del codigo donde puede haber un valor por defecto.

| Opcion | Por defecto | Nota |
|--------|-------------|------|
| Ritmo | **deducido del guion** | Del total de palabras frente a las duraciones objetivo de los encabezados |
| Ritmo de respaldo | 120 ppm | Si el guion no trae duraciones o el valor deducido no es plausible |
| Banda plausible de ritmo | 90–180 ppm | Fuera de ella se descarta el deducido, avisando |
| Bloque de respiracion | 6–12 palabras (objetivo 9) | Unidad de resaltado de todas las salidas |
| Alcance de reescrituras | forma dicha + respiracion | Cacofonias, anglicismos y estilo solo se **avisan** |
| Tipografia de marca | Poppins | Solo `.pdf` y `.pptx`; el reproductor es neutro |
| Notas internas en las salidas | incluidas | `--para-terceros` las omite |

**Precedencia:** valores por defecto → configuracion del usuario → configuracion del proyecto de guion → argumentos de la invocacion.

## Donde encaja

Es el **paso previo al montaje**. Entrega un `.srt` borrador estandar (consumible por ffmpeg) y
`tarjetas.json`, para que la fase de edicion de video no empiece de cero. Ver T-33.

## Verificacion

```
python -m mypy                                 # tipos
python -m ruff check scripts/ tests/           # estilo
python -m pytest                               # tests
python scripts/verificar_salidas.py --fixture  # extremo a extremo + auto-contencion del HTML
```

Las herramientas son **solo de desarrollo** (`requirements-dev.txt`): la skill se ejecuta sin ellas.
