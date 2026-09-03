# ROADMAP DE PRODUCTO — teleprompter — Documento vivo

> Roadmap de producto VIVO, gestionado por el agente Product Manager. Aquí se especifican las
> mejoras (tareas R-XX), agrupadas en oleadas y fases. Es la **spec de las R-XX** (las T-XX
> tienen su spec en `HOJA_DE_RUTA.md`).
>
> Reglas: este documento **especifica**, no lleva estado — el estado de cada R-XX vive en §1 de
> `SEGUIMIENTO.md` (no duplicar). Las oleadas 100 % entregadas se mueven a
> `ROADMAP_HISTORICO.md` para mantener vivo solo lo pendiente o en curso.

**Última actualización:** 2026-09-03

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

### Fase transversal F-E — Robustez en el entorno real del dueño

La primera vez que el proyecto corrió de verdad fuera de un contenedor de nube (sesión local de
T-32, en el Windows del dueño) aparecieron fallos que ninguna sesión de nube podía ver, porque
ninguna corre en Windows. Esta fase recoge esos hallazgos de uso real, del mismo modo que F-D
recogía los del auditor. Contiene R-10.

---

## DETALLE DE TAREAS R-XX

> Formato de cada R-XX (mismo rigor que una T-XX). Numeración secuencial, nunca reutilizada.
> Ninguna R-XX puede empezar antes de que la oleada v1 esté entregada, salvo que se diga lo
> contrario en su ficha.

### R-10 — Robustez multiplataforma detectada al correr en Windows por primera vez
**Oleada / Fase:** F-E · **Migración:** No · **Depende de:** T-06
**Origen:** hallazgo de sesión (T-32 local, máquina del dueño, 2026-09-03 — no es hallazgo del
auditor, que audita desde sesiones de nube sin acceso a esa máquina)

**Objetivo:** la primera vez que la suite completa corrió en la máquina real del dueño (Windows,
no un contenedor de nube) aparecieron cuatro tests en rojo, documentados en
`roadmap/HISTORIAL_SESIONES.md` (sesión "T-32 desbloqueada + P-04"). Tres son ruido de plataforma
sin riesgo real para el producto; el cuarto sí lo tiene: cualquier guión que el dueño escriba y
guarde en Windows llevará fin de línea `\r\n`, y `entrada.leer_guion` no lo normaliza — el `\r`
llega intacto a todo el pipeline de parseo, troceo y revalidación, con riesgo de comparaciones de
texto que fallan en silencio exactamente donde el invariante (c) («la edición manual manda»)
depende de que dos textos idénticos se reconozcan como idénticos. Esta tarea cierra el hallazgo
real y adapta o descarta el ruido de plataforma sin gastar más esfuerzo del que vale cada uno.

**Requisitos:**
1. `entrada.leer_guion` normaliza cualquier fin de línea (`\r\n`, `\r` suelto) a `\n` en el mismo
   punto donde ya decodifica UTF-8, antes de que ninguna capa posterior vea el texto. Test con un
   guión de prueba escrito con bytes `\r\n` explícitos (no solo con el `newline` que decide la
   plataforma que ejecuta el test) que confirme un resultado idéntico al mismo guión con `\n`.
2. Diagnosticar la causa exacta de `test_nombre_guion_seguro_nunca_vacio` en Windows antes de
   tocar código — `PureWindowsPath` ya interpreta `.md` como sufijo igual que en POSIX incluso con
   nombres terminados en varios puntos, así que puede que la causa real no sea la que parecía a
   primera vista — y corregir `nombre_guion_seguro` si el diagnóstico confirma un caso real.
3. `test_instalar_hook_copia_y_da_permiso_de_ejecucion` (verifica el bit de ejecución POSIX,
   inexistente en Windows) pasa a `skip` explícito cuando `os.name != "posix"`, en vez de quedar
   en rojo: instalar el hook sigue siendo una operación real en Windows (la copia del archivo),
   solo la comprobación del bit deja de aplicar ahí.
4. Verificar que ninguna salida generada (`.srt`, `.pdf`, `tarjetas.json`, reproductor) reintroduce
   `\r\n` en su propio proceso de escritura — comprobación puntual, no una tarea nueva si ya
   escriben con `\n`.

**Criterio de aceptación:** un guión guardado con `\r\n` produce exactamente el mismo
`guion-escenas.md` (mismo contenido, no solo mismo número de escenas) que el mismo guión guardado
con `\n`; los cuatro tests que la sesión de T-32 marcó en rojo en Windows quedan en verde o
correctamente `skip`, con la causa raíz de cada uno documentada en `DECISIONES_TECNICAS.md`; la
suite sigue en verde en las sesiones de nube (Linux).

---

*(El estado de cada R-XX se sigue en §1 de `SEGUIMIENTO.md`.)*
