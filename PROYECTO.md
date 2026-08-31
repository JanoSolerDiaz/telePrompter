# PROYECTO — teleprompter  *(documento opcional)*

> Ancla de **contexto estable**: qué ES el producto, no cómo se ejecuta (eso es la hoja de ruta).
> Sirve de referencia común para el PM y el auditor. Cambia poco.

## Qué es teleprompter

Una skill de Claude Code que convierte un guión de producción en `.md` en las tarjetas con el
texto exacto que hay que recitar ante la cámara. La salida principal es un reproductor web tipo
teleprompter, autocontenido y offline, con resaltado de karaoke por bloques de respiración.

## Propuesta de valor

Hoy, grabar un vídeo de curso a partir de un guión mixto obliga a separar mentalmente lo que se
dice de lo que es indicación de pantalla, a traducir cifras y siglas a su forma dicha sobre la
marcha, y a leer de un documento pensado para producción, no para locutar. Esta skill hace ese
trabajo antes de encender la cámara y entrega un apuntador que se maneja con un clicker, marca
el ritmo y no exige memorizar. Frente a un teleprompter genérico, entiende el guión: sabe qué es
locución y qué no, trocea por respiración y estima tiempos.

## Cliente objetivo

**ICP:** Jano (Cuatroochenta) y, por extensión, cualquier formador o divulgador que graba vídeos
de curso en español a partir de guiones escritos por él mismo, sin equipo de producción.

**Segmentos prioritarios:** creadores en solitario con guiones mixtos (locución + indicaciones de
pantalla + timestamps) y una cadena de montaje posterior con ffmpeg.

## Dominio y cumplimiento

Sin normativa aplicable: la herramienta es local, no trata datos personales y no se comunica con
ningún servicio. La restricción dominante es operativa, no legal: **cero red en ejecución** y
**salidas autocontenidas**, porque el reproductor tiene que funcionar en el equipo de grabación,
abriéndose con doble clic, sin depender de nada externo.

## Glosario del dominio

- **Escena** — unidad de guión delimitada por un encabezado del `.md`. Es lo que se graba de una vez.
- **Bloque de respiración** — fragmento de 6–12 palabras que se dice de una sola respiración. Es la unidad de resaltado en todas las salidas.
- **Locución** — el texto que se recita literalmente ante la cámara.
- **No locución** — indicaciones de pantalla, B-roll, notas de producción y timestamps; se conservan y se muestran al pie de la escena, nunca se recitan.
- **Forma dicha** — la versión pronunciable de cifras, fechas, unidades, símbolos y siglas («2026» → «dos mil veintiséis»).
- **Reescritura marcada** — propuesta de mejora de locutabilidad que muestra original y propuesta a la vez, y que el dueño acepta o rechaza una a una.
- **Validación** — momento en que el dueño da por bueno el `guion-escenas.md`; dispara el recálculo y la generación de salidas.
- **Ritmo (ppm)** — palabras por minuto de la locución. Por defecto 120, propio de locución didáctica y pausada.

## Arquitectura de alto nivel

**Stack:** skill de Claude Code — `SKILL.md` + `references/` + `assets/` + `scripts/` en Python 3
(solo biblioteca estándar en tiempo de ejecución; `mypy`, `ruff` y `pytest` solo en desarrollo).
El reproductor es HTML/CSS/JS vanilla generado a partir de plantillas, en un único archivo.

**Despliegue:** instalación local de la skill en `~/.claude/skills/teleprompter/`. No hay
servidor, ni servicio, ni repositorio remoto.

**Aislamiento de datos:** por proyecto de guión. Todo se escribe en
`<carpeta-del-guion>/<nombre-guion>-tarjetas/` y nunca fuera. Sin red, sin telemetría.

**Invariantes de datos:** cobertura total del guión (nada se descarta en silencio) · original de
toda reescritura recuperable · las ediciones manuales del dueño mandan al revalidar · sin borrado
destructivo (copia `.bak` antes de sobrescribir).

## Decisiones de producto estables

- **El reproductor es neutro.** Legibilidad a distancia de cámara por encima del branding: tema oscuro de alto contraste, sin identidad corporativa. La marca 480 vive solo en `.pptx` y `.pdf`, con su guía en `references/marca-480.md` y sus logotipos en `assets/`.
- **Una sola pasada de revisión.** El ciclo de validación se diseña para revisar el guión entero en el editor, no para conversar escena por escena.
- **La skill propone, el dueño dispone.** Ninguna mejora de texto se aplica sin quedar marcada y ser reversible.
- **Un archivo, offline, doble clic.** Cualquier funcionalidad que exija red o dependencias queda fuera del producto.
- **Encaja en la cadena, no la sustituye.** El montaje es de otra skill; aquí se entrega el `.srt` borrador y el contrato `tarjetas.json`.
