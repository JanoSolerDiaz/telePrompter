# Mapa de teclas del reproductor y clicker Bluetooth (T-24)

> Vive en `Configuracion.mapa_teclas_reproductor` (`scripts/config.py`): nombre de
> acción → teclas que la disparan. Cambiar el mapa es cambiar esa constante; el
> manejador de teclado (`guion.js`) y la ayuda en pantalla (`?`) lo leen tal cual,
> nunca hay una copia paralela que se pueda desincronizar.

## Por qué un clicker Bluetooth funciona sin código especial

Un clicker de presentaciones se identifica ante el sistema operativo como un
**teclado corriente**: no hay API que lo distinga de una pulsación real de teclado.
Toda la "compatibilidad" es, por tanto, cuestión de qué tecla envía cada botón físico
y de tolerar el rebote de contacto típico de un mando barato — nunca detección de
hardware.

## Mapa por defecto

| Acción | Teclas | Efecto |
|--------|--------|--------|
| `pausa_avanza` | `Espacio` | Pausa/reanuda el automático (o avanza un bloque si `espacio_avanza_bloque=True`) |
| `bloque_siguiente` | `→` / `Av Pág` | Avanza un bloque de respiración |
| `bloque_anterior` | `←` / `Re Pág` | Retrocede un bloque de respiración |
| `escena_anterior` | `↑` | Vuelve a la escena anterior |
| `escena_siguiente` | `↓` | Pasa a la escena siguiente |
| `velocidad_mas` | `+` / `=` | Sube la velocidad del automático (`paso_velocidad`) |
| `velocidad_menos` | `-` | Baja la velocidad del automático |
| `tamano_mas` | `]` | Aumenta el tamaño de texto en vivo |
| `tamano_menos` | `[` | Reduce el tamaño de texto en vivo |
| `reiniciar_escena` | `R` | Vuelve al primer bloque de la escena actual |
| `ocultar_indicadores` | `H` | Muestra/oculta cabecera y barra de progreso |
| `salir_pantalla_completa` | `Esc` | Sale de pantalla completa |
| `ayuda` | `?` | Muestra/oculta el panel con este mismo mapa |
| `espejo` | `M` | Activa/desactiva el modo espejo (T-25) |

Ninguna acción depende de un modificador (`Ctrl`/`Alt`/`Mayús`): un clicker no puede
enviarlos, así que ningún atajo los exige.

## Antirrebote

`Configuracion.antirrebote_clicker_ms` (120 ms por defecto) descarta una repetición de
la **misma acción** si llega antes de ese tiempo desde la anterior — un clicker barato
puede enviar la misma tecla dos veces por un único clic físico (rebote de contacto).
Es por acción, no global: pulsar rápido dos teclas *distintas* nunca se descarta por
error. `0` desactiva el antirrebote por completo.

## Calibrar un clicker físico

1. Abre el reproductor generado y pulsa `?` para ver el mapa vigente.
2. Pulsa cada botón del clicker y anota qué tecla envía (se puede comprobar con
   cualquier verificador de teclado del sistema si el reproductor no la reconoce).
3. Si algún botón no coincide con el mapa de arriba, edita
   `Configuracion.mapa_teclas_reproductor` en `scripts/config.py` (o pásalo como
   override al generar el reproductor) añadiendo esa tecla a la acción que
   corresponda. No hace falta tocar `guion.js`.

**Estado:** el dueño no dispone hoy de un clicker Bluetooth para verificar esto en
hardware real (T-24b, bloqueada — ver §3 de `roadmap/SEGUIMIENTO.md`). El mapa de
arriba cubre las tres teclas que cualquier clicker de presentaciones envía
(`Espacio`, `Av Pág`, `Re Pág`), verificado con teclado real.

## Ver también

- `DEVELOPERS.md`, sección T-24 — implementación del antirrebote y la ayuda en
  pantalla.
- `SKILL.md`, sección «Atajos de teclado y clicker Bluetooth» — resumen y opciones.
