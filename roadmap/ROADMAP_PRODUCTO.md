# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-08-31

---

## Visión y misión

Convertir un guión de producción en `.md` en las tarjetas con el texto exacto que hay que recitar
ante la cámara, entregadas como un teleprompter web autocontenido con resaltado de karaoke, para
que grabar un vídeo de curso deje de exigir memorizar, improvisar o repetir tomas.

## Cliente objetivo y segmentos

**ICP:** Jano (Cuatroochenta) y, por extensión, cualquier formador o divulgador que graba vídeos de
curso en español a partir de guiones escritos por él mismo, sin equipo de producción ni apuntador.

**Segmentos prioritarios:** creadores en solitario que graban con guiones mixtos (locución mezclada
con indicaciones de pantalla) y que ya tienen una cadena de montaje posterior con ffmpeg, donde
esta skill es el paso previo.

## Principios de producto (innegociables; extienden §0.2 de la hoja de ruta)

1. **Nada se descarta en silencio.** Todo bloque del guión se clasifica con su motivo a la vista; si el agente duda, lo marca para revisar, no lo elimina.
2. **Una sola pasada de revisión.** El `guion-escenas.md` es el contrato con el locutor: se revisa entero en el editor, de una sentada. Nada de ping-pong escena por escena.
3. **El texto del dueño manda.** Las mejoras se proponen, nunca se imponen; el original siempre es recuperable y una edición manual jamás se sobrescribe.
4. **Un solo archivo, offline.** El reproductor abre con doble clic en cualquier máquina, sin red, sin dependencias, sin CDN. Si algo no cabe en el archivo, no entra en el producto.
5. **Legibilidad a distancia de cámara por encima de todo.** En el reproductor, cualquier disyuntiva entre estética, branding o funcionalidad y legibilidad se resuelve siempre a favor de la legibilidad.

---

## OLEADAS Y FASES

> Organización por oleadas. El **backlog inicial completo (T-00 a T-33) es la oleada v1** y su
> spec vive en `HOJA_DE_RUTA.md`; el PM no la duplica aquí. Las R-XX de este documento son lo que
> viene **después** de tener un teleprompter funcionando, más lo que entra por auditoría o por
> feedback de rodaje. El estado de todas ellas está en §1 de `SEGUIMIENTO.md`.

### Oleada v1 — Que exista y se pueda grabar con ello  *(T-00…T-33, spec en la hoja de ruta)*

Del guión al reproductor: análisis, locutabilidad, ciclo de validación, reproductor, salidas y
empaquetado. Criterio de salida de la oleada: **grabar un vídeo de curso entero usando la skill**,
que es también el criterio que conmuta el modo de operación a PRODUCCIÓN.

### Oleada v2 — Rodaje real: cerrar el bucle entre lo estimado y lo grabado

Todo lo de v1 trabaja con **estimaciones**. En cuanto haya tomas reales, el producto tiene una
fuente de verdad que hoy desaprovecha: cuánto se tardó de verdad, dónde se repitió, dónde el
locutor se trabó. Esta oleada convierte esos datos en mejoras del propio guión y del ritmo.
Contiene R-01 a R-04.

### Oleada v3 — Continuidad con el montaje

Hacer que lo que sale de aquí no haya que volver a tocarlo en la fase de ffmpeg. Contiene R-05.

### Fase transversal F-D — Deuda y coherencia

Lo que el auditor levanta y no encaja en una oleada de producto. Contiene R-06.

---

## DETALLE DE TAREAS R-XX

> Formato de cada R-XX (mismo rigor que una T-XX). Numeración secuencial, nunca reutilizada.
> Ninguna R-XX puede empezar antes de que la oleada v1 esté entregada, salvo que se diga lo
> contrario en su ficha.

### R-01 — Persistencia verificada de preferencias, con plan B
**Oleada / Fase:** v2 · **Migración:** No · **Depende de:** T-26
**Origen:** auditoría #5

**Objetivo:** que la promesa de «retomar la grabación entre sesiones» sea real y no dependa de una
suposición sobre el navegador. Hoy T-26 confía en que `localStorage` persiste al abrir el
reproductor desde `file://`, y eso no está comprobado en el navegador con el que se graba.

**Requisitos:**
1. Comprobación real en el navegador de grabación: guardar preferencias, cerrar, reabrir el
   archivo y verificar que siguen ahí. Dejar constancia del resultado por navegador.
2. Si no persisten, plan B sin red y sin dependencias: **exportar e importar las preferencias como
   un archivo** (o como texto que el reproductor pueda leer), de modo que retomar sea un gesto y
   no una reconfiguración.
3. Aviso honesto en el propio reproductor cuando detecte que el almacenamiento no persiste, en vez
   de fallar en silencio y perder los ajustes del dueño.

**Criterio de aceptación:** existe evidencia escrita del comportamiento en el navegador de
grabación; si no persiste, el ciclo exportar → reabrir → importar restaura tamaño, velocidad por
escena y última escena vista.

### R-02 — Registro de tomas por escena
**Oleada / Fase:** v2 · **Migración:** Sí (`00N_tomas`) · **Depende de:** T-19, T-23, T-26
**Origen:** roadmap

**Objetivo:** que el índice de escenas deje de ser una lista y pase a ser el parte de rodaje. Hoy
T-19 muestra un estado por escena pero nada registra qué pasó en cada toma, y esa información es
justo la que hace falta al día siguiente y en el montaje.

**Requisitos:**
1. Por escena: número de tomas, duración real de cada una (del cronómetro de T-23) y marca de cuál
   es la buena.
2. Nota rápida por toma, escribible sin salir del modo de grabación y con el mínimo de teclas.
3. Volcado a un archivo de la carpeta de salida, legible por la fase de montaje y por el dueño.
4. El índice muestra de un vistazo qué está grabado, qué se repitió y qué falta.

**Criterio de aceptación:** tras un rodaje simulado de tres escenas con repeticiones, el parte
refleja tomas, duraciones y toma buena, y sobrevive al cierre del navegador.

### R-03 — Marcar tropiezos durante la toma
**Oleada / Fase:** v2 · **Migración:** No · **Depende de:** R-02
**Origen:** roadmap

**Objetivo:** capturar en caliente el dato más valioso para mejorar el guión: dónde se traba el
locutor. Hoy ese conocimiento se pierde entre la grabación y la siguiente revisión.

**Requisitos:**
1. Una tecla que marque el bloque actual como problemático, sin interrumpir la toma.
2. Los bloques marcados se vuelcan a `FEEDBACK.md` como entradas `nuevo`, con escena, bloque y
   texto exacto.
3. En la siguiente validación, esos bloques aparecen destacados en `guion-escenas.md` para
   reescribirlos a mano o con propuesta de la skill, dentro del alcance permitido en §0.2.

**Criterio de aceptación:** marcar dos bloques en una toma produce dos entradas de feedback
localizadas, y la siguiente validación las muestra sin que el dueño tenga que buscarlas.

### R-04 — Recalibrar el ritmo con tiempos reales
**Oleada / Fase:** v2 · **Migración:** No · **Depende de:** R-02, T-12
**Origen:** roadmap

**Objetivo:** cerrar el bucle del ritmo. T-12 deduce el ppm de las duraciones **objetivo**, que
son una intención del guionista; R-02 aporta las duraciones **reales**. Con las dos se puede saber
cuánto se desvía la intención de la realidad y afinar las estimaciones futuras.

**Requisitos:**
1. Comparar, por escena y en total, duración estimada, duración objetivo y duración real.
2. Proponer un ppm personal calibrado con la evidencia acumulada de varios guiones, que el dueño
   acepta o rechaza; nunca se aplica solo.
3. Informe corto y legible: en qué tipo de escena se acelera y en cuál se frena.

**Criterio de aceptación:** con dos guiones grabados, la skill propone un ppm calibrado y muestra
la desviación por escena que lo justifica.

### R-05 — `.srt` alineado con la toma buena
**Oleada / Fase:** v3 · **Migración:** No · **Depende de:** R-02, T-27, T-33
**Origen:** roadmap

**Objetivo:** que el `.srt` deje de ser un borrador estimado y pase a estar alineado con lo que se
grabó de verdad, para que el montaje empiece con subtítulos casi finales en vez de con una
aproximación que hay que rehacer entera.

**Requisitos:**
1. Reescalar los tiempos de los bloques a la duración real de la toma buena de cada escena.
2. Mantener el `.srt` estimado como salida independiente: el estimado sirve antes de grabar, el
   alineado después.
3. Validar el resultado con las mismas reglas estrictas de T-27.

**Criterio de aceptación:** con una toma real cronometrada, el `.srt` alineado no tiene solapes y
su duración total coincide con la de la toma dentro de la tolerancia documentada.

### R-06 — Coherencia de nomenclatura y separación de `assets/`
**Oleada / Fase:** F-D · **Migración:** Sí (`00N_renombrado_salida`) · **Depende de:** T-32
**Origen:** auditoría #6

**Objetivo:** quitar la deuda de nombres antes de que se fosilice en carpetas de guiones reales.

**Requisitos:**
1. Decidir y aplicar el nombre definitivo de la carpeta de salida, hoy `<nombre-guion>-tarjetas/`,
   heredado del nombre anterior del proyecto.
2. Migración que renombre las carpetas de proyectos de guión ya existentes sin perder estado ni
   ediciones, con `.bak` previo.
3. Separar `assets/` en dos espacios con propósitos distintos: los logotipos y recursos de marca
   por un lado, las plantillas HTML/CSS/JS del reproductor por otro.

**Criterio de aceptación:** un proyecto de guión creado antes del cambio se abre después sin
pérdidas; ninguna ruta del código mezcla marca y plantillas.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`.)*
