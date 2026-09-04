# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-09-04

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

### Oleadas v2, v3 y fase F-D — entregadas

Las oleadas v2 (rodaje real, R-01 a R-04), v3 (continuidad con el montaje, R-05 y R-07) y la fase
transversal F-D (deuda y coherencia, R-06/R-08/R-09) tienen las nueve R-XX en **COMPLETADA** en §1
de `SEGUIMIENTO.md`, sin ningún hito de negocio propio pendiente. Se movieron a
`ROADMAP_HISTORICO.md` en el ciclo de PM del 2026-09-03; su spec completa y cómo se entregó cada
una vive ahí.

### Fase transversal F-E — entregada

La fase F-E (robustez detectada al correr por primera vez en el Windows real del dueño) tiene su
única R-XX (R-10) en **COMPLETADA** en §1 de `SEGUIMIENTO.md`, sin ningún hito de negocio propio
pendiente. Se movió a `ROADMAP_HISTORICO.md` en el ciclo de PM del 2026-09-04; su spec completa y
cómo se entregó vive ahí.

### Fase transversal F-F — Robustez de los datos derivados del rodaje real

La auditoría de 2026-09-04, la primera pasada tras completarse toda la oleada R (rodaje real,
R-01 a R-07), encontró tres huecos menores en cómo esos datos de rodaje se propagan a las salidas
derivadas — ninguno reproducido como bug hoy sobre material real, los tres cierres preventivos del
mismo tipo que ya motivó F-D. Contiene R-11.

---

## DETALLE DE TAREAS R-XX

> Formato de cada R-XX (mismo rigor que una T-XX). Numeración secuencial, nunca reutilizada.
> Ninguna R-XX puede empezar antes de que la oleada v1 esté entregada, salvo que se diga lo
> contrario en su ficha.

### R-11 — Robustez de datos derivados del rodaje (toma buena ambigua, capítulos sobrantes, cobertura cruzada)
**Oleada / Fase:** F-F · **Migración:** No · **Depende de:** R-02, R-05, R-07
**Origen:** auditoría #16, #17, #18

**Objetivo:** cerrar tres huecos de robustez de menor entidad alrededor de los datos de rodaje real
(R-02) y sus dos consumidores derivados (`.srt` alineado de R-05, capítulos de YouTube de R-07),
detectados por el auditor sin bug reproducido hoy sobre material real — cierre preventivo, no
corrección de una regresión. (1) `tomas.duracion_toma_buena` no valida que como mucho una toma esté
marcada `buena` por escena — esa exclusividad hoy solo la garantiza el lado JS
(`finalizarTomaActual`); un `.json` con dos tomas `buena` para la misma escena (edición manual,
fusión de exportaciones, un futuro bug de `guion.js`) hace que la función Python elija la primera
en silencio, sin ninguna señal de ambigüedad, propagándose sin aviso a R-04/R-05/R-07 (#16). (2)
`capitulos_youtube.calcular_capitulos` empareja títulos de capítulo con escenas posicionalmente
"hasta la más corta"; cuando sobran títulos de capítulo (más títulos que escenas), los sobrantes se
descartan de `capitulos-youtube.txt` sin ningún aviso ni `motivo_sin_generar` — el caso simétrico
(menos títulos que escenas) sí está cubierto (#17). (3) no existe ningún test de integración
cruzada, en el espíritu de `tests/test_integracion_montaje.py` (T-33), entre `guion-alineado.srt`
(R-05) y `capitulos-youtube.txt` (R-07): ambos comparten `tomas.duracion_toma_buena`, así que la
coherencia hoy es "por construcción", no verificada por regresión (#18).

**Requisitos:**
1. `tomas.duracion_toma_buena` (o quien la invoque desde `scripts/tomas.py`) detecta más de una
   toma `buena` en la misma escena y lo señala como una incidencia explícita — nunca elige la
   primera en silencio. Test que reproduce exactamente el escenario del hallazgo #16 (dos tomas
   `buena: true` en la misma escena).
2. `capitulos_youtube.calcular_capitulos` deja constancia explícita (aviso o campo equivalente al
   `motivo_sin_generar` ya existente) cuando hay títulos de capítulo sin escena correspondiente, en
   vez de descartarlos sin rastro. Test que reproduce el escenario del hallazgo #17 (más títulos de
   capítulo que escenas).
3. Un test nuevo (no necesariamente un módulo nuevo) que, a partir del mismo `ResultadoTiempos` +
   `tomas_por_escena`, genere `guion-alineado.srt` y `capitulos-youtube.txt` y confirme que sus
   marcas de tiempo son mutuamente coherentes — cierra el hallazgo #18.

**Criterio de aceptación:** un `.json` de tomas con dos tomas `buena` en la misma escena produce
una incidencia visible en vez de una elección silenciosa; un guion con más títulos de capítulo que
escenas no pierde ningún título sin dejar rastro explícito; existe al menos un test de integración
que verifica la coherencia cruzada entre el `.srt` alineado y los capítulos de YouTube sobre el
mismo dato de partida.

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`.)*
