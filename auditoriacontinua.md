# AUDITORÍA CONTINUA — teleprompter

> Documento del agente Auditor (supervisor externo). Es el **único** archivo que el auditor
> modifica. Dos partes: un registro de hallazgos rastreable (arriba) y la narrativa por
> auditoría (debajo, la más reciente primero).
>
> Para que ningún hallazgo quede en saco roto: el **PM** convierte los hallazgos `ABIERTO` en
> tareas (R-XX o backlog) con `origen: auditoría #N`; los de **severidad alta** (seguridad,
> bug en producción, rotura de UX) los atiende el **programador** como P-XX urgente. En cada
> pasada, el auditor reevalúa los `ABIERTO` contra el código y los cierra o escala.

## REGISTRO DE HALLAZGOS

> Severidad: alta / media / baja. Estado: ABIERTO / RESUELTO / ASUMIDO (riesgo aceptado por el dueño). Numeración nunca reutilizada.

| #ID | Fecha | Área | Severidad | Estado | Resumen | Tarea / origen |
|-----|-------|------|-----------|--------|---------|----------------|
| #1 | 2026-08-31 | Proceso / git | alta | ABIERTO | El protocolo fija `main` como rama de trabajo, pero el repo real está en `develop`, tiene `master` (no `main`) y un remoto `origin` en GitHub. Un agente que siga el protocolo al pie de la letra empujaría a una rama que no existe. | §0.1 y §0.2 de la hoja de ruta · decisión del dueño |
| #2 | 2026-08-31 | Infraestructura | alta | ABIERTO | `.gitignore` excluye `assets/` y `fixtures/` completos. Quedan fuera del control de versiones los logotipos 480, los tres guiones de calibración y —en cuanto existan— las plantillas del reproductor (T-18) y el `guion-ejemplo.md` del health check (T-32). La CI de T-04 no podría reproducir la verificación. | T-04, T-18, T-32 |
| #3 | 2026-08-31 | Producto / marca | alta | ABIERTO | **Poppins no está instalada en esta máquina** (0 archivos); Figtree sí (16) y Montserrat tampoco. Con la decisión vigente, el PDF caería hasta el último respaldo (Calibri) mientras el PPTX sale en Figtree: peor resultado que cualquiera de las dos opciones puras. | T-28, T-29 · §6.6 |
| #4 | 2026-08-31 | Calidad | media | ABIERTO | La 4ª verificación (`verificar_salidas.py --fixture`) es obligatoria desde T-00, pero su fixture no existe hasta T-32 y el generador HTML no existe hasta T-18: la red de seguridad está incompleta durante casi todo el backlog si no se define un talón que degrade con sentido. | T-00, T-04, T-32 |
| #5 | 2026-08-31 | Producto | media | ABIERTO | T-26 asume que `localStorage` persiste al abrir el reproductor desde `file://`. No está verificado en el navegador de grabación; el `try/catch` evita el error pero no salva la promesa de «retomar entre sesiones». | T-26 |
| #6 | 2026-08-31 | Coherencia | baja | ABIERTO | Nomenclatura arrastrada del nombre anterior: la carpeta de salida es `<nombre-guion>-tarjetas/` con el proyecto ya llamado `teleprompter`. Además `assets/` mezcla dos cosas distintas (logotipos de marca y, en el futuro, plantillas del reproductor). | T-07, T-18, T-28 |
| #7 | 2026-08-31 | Trazabilidad | baja | ABIERTO | El paso de la hoja de ruta v1.0 a v1.1 —documento declarado inmutable— está anotado en su propia cabecera pero no en `DECISIONES_TECNICAS.md` ni en §7 de SEGUIMIENTO. Los tres logs siguen vacíos con el proyecto ya commiteado. | §0.4 · `DECISIONES_TECNICAS.md` |
| #8 | 2026-08-31 | Documentación | baja | ABIERTO | `DEVELOPERS.md` se referencia en §0.4 y en T-32 pero todavía no existe. Esperable a esta altura; se registra para que no se pierda. | T-32 |

---

## NARRATIVA POR AUDITORÍA

> Cada pasada: fecha, hallazgos y conclusiones. Append, la más reciente arriba. Prestar
> atención especial a la coherencia entre lo decidido (`DECISIONES_TECNICAS.md` y §0.2 de la
> hoja de ruta) y lo realmente implementado, y a las desviaciones (§7 de SEGUIMIENTO).

### Auditoría 2026-08-31 — estado de partida (antes de la primera sesión del programador)

**Alcance.** No hay código todavía: el proyecto está en fase de arranque, con los documentos de
gobierno, tres guiones reales de calibración y los cuatro logotipos de marca. Por tanto esta
pasada audita **el propio andamiaje**: coherencia entre documentos, viabilidad del protocolo
contra la máquina real y suposiciones que el backlog da por buenas sin haberlas comprobado.

**Conclusión general.** El conjunto documental es sólido y poco frecuente en su nivel de
concreción: los invariantes están enunciados en términos verificables por test (cobertura total
del guión, original recuperable, edición manual autoritativa, salida autocontenida) y el backlog
está calibrado contra guiones reales, no contra suposiciones. Lo que falla no es el diseño, sino
**tres choques entre lo escrito y la máquina donde va a ejecutarse**, los tres detectados
midiendo, no leyendo.

**Lo que se ha verificado en esta pasada (no es opinión):**

- `git rev-parse --show-toplevel` → el repositorio **ya existe** y su raíz es el propio proyecto;
  `git branch -a` → `develop` (actual), `master`, `origin/develop`, `origin/master`. **No hay
  `main`.** El protocolo lo nombra siete veces. → **#1**
- `git check-ignore -v` → `assets/480_Gris.png` y `fixtures/reales/guion-09-proyectos.md` están
  ignorados por las dos únicas reglas del `.gitignore`. El commit inicial contiene 11 archivos,
  todos documentación. → **#2**
- Recuento de archivos de fuente en `C:\Windows\Fonts` y en las fuentes de usuario: **Poppins 0,
  Montserrat 0, Figtree 16, Calibri 6**. La decisión de marca del dueño no es aplicable tal cual
  en esta máquina. → **#3**
- `python -m mypy|ruff|pytest` → los tres ausentes. No es un hallazgo: es exactamente el trabajo
  de T-01 y T-03, y confirma que la red de seguridad aún no existe.
- Chrome y Edge presentes en sus rutas estándar: la vía de T-28 para el PDF es viable.

**Sobre #3, que es el más incómodo.** La decisión «Poppins» se tomó ayer con la información
disponible —la guía de marca dice que es la familia oficial— y es defendible. Pero en esta
máquina produce el peor de los resultados posibles: PDF en Calibri y PPTX en Figtree, dos
documentos con la misma marca y tipografías distintas, que es justo lo que la decisión pretendía
evitar. Las salidas son tres: instalar Poppins (y garantizar que esté allí donde se abra el
documento), aceptar Figtree —que ya está instalada y es lo que la skill de marca usa por
defecto—, o incrustar la fuente, que **choca con la regla de cero red y de no distribuir
binarios de fuentes sin licencia comprobada**. No es una decisión del agente.

**Coherencia entre lo decidido y lo escrito.** Buena. Las tres decisiones permanentes del dueño
(convención contractual con aviso, alcance de reescrituras, ritmo deducido del guión) están
promovidas a §0.2, que es donde el método manda que vivan, y cada tarea afectada las referencia
en lugar de duplicarlas. El único punto flojo es de registro, no de fondo: la hoja de ruta se
modificó dos veces antes de la primera sesión sin dejar rastro en los logs (**#7**). Es
legítimo —el dueño gobierna el documento y la propia cabecera lo explica— pero conviene fijar el
precedente ahora: a partir de la primera sesión del programador, ese documento no se toca.

**Riesgo estructural a vigilar (#4).** La verificación de cuatro redes es el corazón del modo
autonomía total, y la cuarta no puede pasar hasta T-32. Si nadie lo resuelve, el agente hará una
de dos cosas malas: saltársela sistemáticamente —y perder el hábito— o dar por buena una
comprobación vacía. La salida limpia es que T-00 cree el talón y que este vaya creciendo con cada
tarea que añada una salida, de modo que la cuarta red diga siempre algo verdadero.

**Lo que no es un hallazgo pero conviene tener presente.** La salida `.pptx` depende de dos
skills que no están instaladas (`480-branded-pptx` y la `pptx` de la que depende). Ya está
registrado como bloqueo #2 en §3 de SEGUIMIENTO, con la funcionalidad correctamente aislada: el
resto del producto no se ve afectado. Es el tratamiento correcto y no requiere acción del auditor.
