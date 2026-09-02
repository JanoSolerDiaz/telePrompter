# Formato de `guion-escenas.md` — documento de revisión de una sola pasada (T-16, T-17)

> Lo genera `scripts/documento_revision.py`; lo relee como autoritativo
> `scripts/revalidacion.py` (T-17). Es el único archivo que el dueño edita a mano
> entre la generación inicial y las salidas finales.

## Estructura, de arriba a abajo

1. **Cabecera global**: instrucciones breves de edición y el resumen agregado del
   guion completo (escenas, palabras, duración, ritmo, avisos, reescrituras
   pendientes).
2. **Una sección por escena**, en el mismo orden del guion de origen, con el mismo
   encabezado `## BLOQUE N — <título>` (ver `references/convencion-guion.md`) más
   duración estimada/objetivo, palabras y número de bloques.
3. Dentro de cada escena, sus **bloques de respiración** (T-11) numerados, cada uno
   delimitado por un ancla:
   ```
   <!-- bloque escena=N indice=K -->
   Texto del bloque tal como se recita.
   ```
   La edición de este texto respeta la posición lógica (`escena`/`indice`), no la
   columna ni la indentación: puedes reformatear el párrafo a tu gusto sin romper
   nada.
4. Junto a cada bloque, sus **reescrituras propuestas** (T-13/T-15) marcadas:
   ```
   <!-- reescritura id=... -->
   > **Original:** 2026
   > **Propuesta:** dos mil veintiséis
   > **Motivo:** cifra: se lee en letras
   > **Decisión:** PENDIENTE
   <!-- /reescritura -->
   ```
   y sus **avisos de locutabilidad** (T-14) que no dieron ya lugar a una reescritura
   de partición, para no repetir el mismo aviso dos veces.
5. Al pie de cada escena, las **indicaciones no recitables** (`**EN PANTALLA**`,
   `**NOTA**`, y texto sin rótulo marcado `revisar`) con su motivo.
6. Al final del documento, la **marca de estado de la revisión completa**:
   ```
   **Estado de la revisión:** PENDIENTE
   ```

Lo que NO cabe dentro de una escena (preámbulo, secciones auxiliares del guion
original) no se repite aquí: ese texto no es locución de ninguna escena y ya vive
íntegro en el `.md` de entrada.

## Qué puedes editar a mano

| Acción | Cómo |
|--------|------|
| Corregir el texto de un bloque de locución | Edita el texto entre su ancla `<!-- bloque -->` y la siguiente; la revalidación (T-17) respeta tu edición como autoritativa (invariante (c), §0.2) — nunca se sobrescribe al recalcular. |
| Aceptar o rechazar una reescritura | Sobrescribe `PENDIENTE` por `ACEPTAR` o `RECHAZAR` en su línea `**Decisión:**`. La lectura ignora mayúsculas y espacios de más. Una vez decidida, no se vuelve a proponer; solo aparecen las nuevas en la siguiente revalidación. Un rechazo nunca borra el original (queda en `estado.json`, append-only). |
| Forzar la clasificación de un bloque `REVISAR` | Añade el rótulo que corresponda (`**LOCUCIÓN**`/`**EN PANTALLA**`/`**NOTA**`) en el guion de **origen**, no en `guion-escenas.md`: este documento es una vista derivada, no la fuente de la clasificación. |
| Marcar el documento como revisado | Cambia `PENDIENTE` por `VALIDADO` en la línea final `**Estado de la revisión:**`. Sin esa marca, se asume `PENDIENTE`: nunca se da una revisión por completa por omisión. |

## Copia de seguridad

Si ya existía una versión previa de `guion-escenas.md`, se copia primero a
`<nombre>.bak-<marca_de_tiempo>` antes de sobrescribirla — nunca se pierde sin dejar
rastro de lo que había (invariante (d), §0.2).

## Ver también

- `references/convencion-guion.md` — la convención de marcado del guion de origen.
- `DEVELOPERS.md`, secciones T-15 a T-17 — implementación del emparejamiento
  ancla→identidad y los límites conocidos documentados en `DECISIONES_TECNICAS.md`.
