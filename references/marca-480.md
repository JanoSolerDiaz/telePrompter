# Marca 480 / Cuatroochenta — referencia para las salidas `.pdf` y `.pptx`

> **Procedencia:** transcrito por el dueño el 2026-08-31 desde el `SKILL.md` y el
> `references/brand-guide.md` de la skill `480-branded-pptx`, que **no está instalada en esta
> máquina**. Este archivo existe para que T-28 y T-29 puedan construirse sin depender de esa
> transcripción. Si algún día el paquete original llega a `~/.claude/skills/480-branded-pptx/`,
> **ese paquete manda** y este archivo pasa a ser un espejo: contrástalo y actualízalo.
>
> **Alcance:** esta guía se aplica **solo** a las salidas `.pdf` y `.pptx`. El reproductor HTML es
> neutro y oscuro, sin identidad corporativa (§0.2 de la hoja de ruta). No mezclar.

---

## ⚠ Discrepancia conocida: Poppins vs Figtree

Los dos documentos de la misma skill se contradicen:

| Documento | Dice |
|-----------|------|
| `SKILL.md` de `480-branded-pptx` | «Tipografía — Figtree. **Familia obligatoria: Figtree.** Si el sistema destino no la tiene, fallback a Montserrat → Calibri.» |
| `references/brand-guide.md` | «Tipografía — Poppins. **Familia oficial: Poppins.** Fallback: Montserrat → Calibri.» |

**Decisión del dueño (2026-08-31): Poppins.** Manda la guía de marca. El `.pdf` se genera en
Poppins, y el brief de T-29 **pide explícitamente Poppins** a la skill de marca en lugar del
Figtree de su `SKILL.md`, para que los dos documentos coincidan si van al mismo tercero. La clave
`tipografia_marca` permite cambiarlo sin tocar código.

En ambos casos la cadena de respaldo es la misma: **Montserrat → Calibri → sans del sistema**. Las
fuentes se resuelven **por nombre del sistema**: prohibido descargar o incrustar una fuente remota
(§0.2, cero red).

---

## Paleta, por orden de prioridad

| Prioridad | Color | Hex | Rol |
|-----------|-------|-----|-----|
| 1º Primario | Verde 480 | `39FE90` | Acento principal, destacados, KPIs |
| 2º Secundario | Cyan 480 | `1CF9FC` | Líneas decorativas, subtítulos |
| 3º Terciario | Rojo 480 | `FF4950` | Alertas, warnings, datos negativos |
| Neutro | Gris 480 | `4D4D4D` | Texto principal |

### Derivados

| Elemento | Hex |
|----------|-----|
| Fondo oscuro | `141414` |
| Fondo contenido | `FFFFFF` |
| Fondo alternativo | `F7F8FA` |
| Texto principal claro | `333333` |
| Texto secundario | `888888` |
| Bordes sutiles | `E5E7EB` (claro) / `2A2A2A` (oscuro) |
| Header de tablas | `333333` |

**En hex sin `#`** cuando se pase a `pptxgenjs` (lo exige su QA). En el CSS del PDF, con `#`.

---

## Tipografía — escala

| Elemento | Peso | Tamaño | Color |
|----------|------|--------|-------|
| Título portada | Bold | 28–32 pt | Según fondo |
| Título de página/slide | SemiBold | 20–24 pt | `333333` / blanco |
| Subtítulo | Medium | 13–14 pt | `888888` / Cyan |
| Cuerpo | Regular | 10–12 pt | `333333` / blanco |
| KPIs | Bold | 28–40 pt | Verde / Cyan |
| Captions | Regular | 8–9 pt | `888888` |
| Header de tabla | SemiBold | 9–10 pt | Blanco sobre `333333` |
| Celda de tabla | Regular | 8,5–9,5 pt | `333333` |
| Footer | Regular | 7 pt | `888888` / blanco |

**Interlineado del cuerpo: 1,3–1,5. Alineación: izquierda — nunca justificado.**

---

## Logotipo

> ### ⚠ La constante de la guía NO coincide con los archivos reales
>
> La guía dice «relación de aspecto fija **1.7766:1** (668 × 376 px), INVIOLABLE». Los cuatro
> archivos entregados el 2026-08-31 y medidos en su cabecera PNG son **1993 × 805 px → ratio
> 2.4758**, los cuatro idénticos en dimensiones y recortados sin margen sobrante.
>
> Aplicar `alto = ancho / 1.7766` a estos archivos los **estira un 39 % en vertical**: para un
> ancho de 2,4" daría 1,351" cuando lo correcto son 0,969". Es exactamente el fallo que la propia
> guía marca como error («un logo que se ve cuadrado es un error»).
>
> **Regla para este proyecto:** la relación de aspecto **se mide del archivo en tiempo de
> generación** (leyendo el `IHDR` del PNG, sin dependencias) y nunca se codifica como constante.
> Así da igual qué versión del asset llegue mañana. La constante `668/376` no se usa en ninguna
> parte de nuestro código.
>
> **Consecuencia para el `.pptx`:** la skill `480-branded-pptx` **sí** lleva `668/376` fijo en su
> `SKILL.md`, así que con estos archivos sacará el logotipo deformado. El brief de invocación de
> T-29 debe indicarle explícitamente la relación medida y las alturas correctas, y su propio QA
> visual («logo estirado = ERROR») debería cazarlo.

Regla general, válida sea cual sea el archivo:

```
ratio = ancho_px / alto_px      # medido del PNG, no fijado a mano
alto  = ancho / ratio
```

Alturas para los anchos estándar **con los archivos actuales** (ratio 2,4758):

| Ubicación | Ancho | Alto correcto | Alto si se usa la constante de la guía |
|-----------|-------|---------------|-----------------------------------------|
| Portada (centrado) | 2,4" | **0,969"** | ~~1,351"~~ (+39 %) |
| Footer de contenido | 0,7" | **0,283"** | ~~0,394"~~ |
| Cierre (centrado) | 2,8" | **1,131"** | ~~1,576"~~ |
| Header en fondo oscuro | 0,9" | **0,364"** | ~~0,507"~~ |

### Variantes disponibles

Los cuatro archivos están en `assets/` del proyecto, PNG RGBA de 8 bits con transparencia real:

| Variante | Archivo | Uso |
|----------|---------|-----|
| Color negativo | `480_Color_negativo.png` | Fondo oscuro. "4" cian+verde, "80" blanco |
| Color positivo | `480_Color_positivo.png` | Fondo oscuro. "4" cian+verde, "80" gris |
| Blanco | `480_Blanco.png` | Fondo oscuro. Todo blanco |
| Gris | `480_Gris.png` | **Fondo claro** — la que usa nuestro PDF. Tinta oscura, monocroma |

### Reglas

- Tamaño mínimo: **50 px** en digital, **20 mm** en impresión.
- Margen de seguridad alrededor: el ancho de la cruz del "4". Los archivos vienen recortados al
  contorno, sin margen incorporado: hay que reservarlo en la maqueta.
- No cortar, estirar ni alterar bajo ninguna circunstancia.

---

## Maquetación

- Espacio negativo generoso: no saturar la página.
- Jerarquía visual clara: título → subtítulo → cuerpo, con contraste de tamaño notable.
- Márgenes laterales consistentes, **mínimo 0,6"**; superior 0,5".
- Fondo **blanco puro** en páginas de contenido (óptimo para impresión).
- Tarjetas con sombra sutil para dar elevación y separar bloques.
- **Línea fina de acento verde bajo los títulos** (~0,8–1,0" de ancho), no en todas partes.
- Fondos planos: **sin gradientes**, sin efectos pesados.
- Verde como protagonista en lo decorativo y de énfasis; cian como apoyo; rojo solo para alertas.

---

## Lo que espera la skill `480-branded-pptx` (para el brief de T-29)

Estructura de deck que genera por su cuenta, y que nuestro brief debe respetar en vez de reinventar:

| Slide | Tipo | Propósito |
|-------|------|-----------|
| 1 | Portada (DARK) | Título, subtítulo, fecha. Logo prominente |
| 2 | Índice (LIGHT) | Solo si hay 4+ secciones |
| 3–N | Contenido (LIGHT) | Una o más por sección |
| — | Separador (DARK) | Entre bloques mayores, solo si hay 3+ |
| N+1 | Cierre (DARK) | Conclusiones, próximos pasos, contacto |

Notas de implementación suyas, útiles para saber qué **no** debemos hacer nosotros: genera el
`.pptx` con **Node + `pptxgenjs`**, apoyándose en la skill `pptx`; define Slide Masters DARK y
LIGHT; copia los assets al directorio de trabajo; y exige **QA visual** convirtiendo cada slide a
imagen. Todo eso lo ejecuta Claude delegando en esa skill: nuestra skill solo aporta
`tarjetas.json` y el brief (T-29).
