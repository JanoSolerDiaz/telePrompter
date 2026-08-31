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

> El PM organiza las R-XX en oleadas (v1, v2…) y fases temáticas (F-XX), en un orden que
> entregue valor incremental y facilite la adopción. Vacío al arrancar: el PM lo rellena en su
> primer ciclo, alimentándose de los requisitos, del feedback (`FEEDBACK.md`, entradas `nuevo`)
> y de los hallazgos ABIERTO del auditor (`auditoriacontinua.md`).

### Oleada v1 — <título>
*(pendiente de definir por el PM; el backlog inicial completo son T-XX en `HOJA_DE_RUTA.md`)*

---

## DETALLE DE TAREAS R-XX

> Formato de cada R-XX (mismo rigor que una T-XX). Numeración secuencial, nunca reutilizada.

```
### R-NN — <título>
**Oleada / Fase:** v_ / F-_ · **Migración:** Sí (`NNN_<nombre>`) | No · **Depende de:** <R-XX/T-XX o —>
**Origen:** roadmap | feedback #N | auditoría #N

**Objetivo:** <qué problema de producto resuelve y para quién>

**Requisitos:**
1. <paso concreto>

**Bloqueo humano (si lo hay):** <decisión o alta que solo puede hacer el dueño>

**Criterio de aceptación:** <condición objetiva y verificable>
```

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`.)*
