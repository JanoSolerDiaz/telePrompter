# Guión de producción — "Artefactos: el lienzo donde Claude construye contigo"

**Duración objetivo:** 4:00 – 4:25
**Formato:** locución + captura de pantalla de la app de Claude
**Promesa del vídeo:** el concepto queda definido antes del minuto 1; el resto es cómo trabajar con él sin perder versiones.

---

## Preparación antes de grabar

- Comprueba que tienes **Ajustes → Capacidades → Ejecución de código y creación de archivos** activado. Sin eso no hay artefactos, y es el fallo número uno de quien sigue el curso.
- Prepara **dos chats ya avanzados** para no grabar esperas: uno con un documento (una guía de bienvenida para nuevas incorporaciones) y otro con una pequeña app (un panel con una tabla filtrable de horas por proyecto).
- Ten a mano **una versión anterior deliberadamente peor** del documento, para que el salto atrás con el selector de versiones se vea de golpe.
- Confirma en tu pantalla la **posición exacta** del selector de versiones y de los controles de chat antes de locutar: la interfaz se mueve entre actualizaciones y no conviene decir "abajo a la derecha" si en tu grabación está en otro sitio.
- Si grabas con la interfaz en español, verifica los rótulos reales de los botones (**"Editar con Claude"**, **"Publicar"**) y ajusta la locución si no coinciden.

---

## BLOQUE 0 — Arranque (0:00 – 0:15)

**LOCUCIÓN**
> Hay un momento en el que dejas de pedirle cosas a Claude y empiezas a construir con él. Ese momento tiene un nombre y una ventana propia: los artefactos.

**EN PANTALLA**
Plano de un chat normal, respuesta de texto corrido. Al decir "una ventana propia", timelapse acelerado de un artefacto abriéndose a la derecha y llenándose de contenido.

---

## BLOQUE 1 — Qué es un artefacto (0:15 – 0:55)

**LOCUCIÓN**
> Un artefacto es contenido que Claude no te escribe *dentro* de la conversación, sino en una ventana aparte, al lado del chat. Y esa separación no es estética: cambia la forma de trabajar. El chat es donde hablas. El artefacto es la cosa que estás construyendo.
>
> Claude lo abre solo cuando el contenido lo merece: cuando es algo con cierto cuerpo, que se sostiene por sí mismo, y que previsiblemente vas a querer editar, reutilizar o recuperar más tarde. Un correo de tres líneas no es un artefacto. Una guía de doce páginas, sí.
>
> Y cabe casi de todo: documentos en Markdown o texto plano, fragmentos de código, páginas web de una sola página, imágenes SVG, diagramas y esquemas, y componentes interactivos en React. Es decir: desde un documento hasta una pequeña aplicación que funciona.

**EN PANTALLA**
Al hablar de "una ventana aparte", congelar el plano y sobreponer dos etiquetas: **CHAT** a la izquierda, **ARTEFACTO** a la derecha. Al enumerar los tipos, un carrusel rápido de cinco ejemplos reales tuyos (documento, código, página, diagrama, panel interactivo), un segundo cada uno.

---

## BLOQUE 2 — El requisito que nadie te cuenta (0:55 – 1:15)

**LOCUCIÓN**
> Antes de seguir, un aviso práctico. Los artefactos dependen de una capacidad que puede estar desactivada en tu cuenta: ejecución de código y creación de archivos. Si a ti no se te abre esa ventana, no es que lo estés pidiendo mal. Es esto.

**EN PANTALLA**
Recorrido literal, sin cortes: iniciales abajo a la izquierda → **Ajustes** → **Capacidades** → interruptor de **Ejecución de código y creación de archivos**. Que se vea el clic.

**NOTA**
Si el espectador está en Team o Enterprise, el interruptor vive en los ajustes de la organización y solo lo activa un propietario. Menciónalo en un rótulo, no en la locución, para no romper el ritmo.

---

## BLOQUE 3 — Crear y pulir un documento (1:15 – 2:00)

**LOCUCIÓN**
> Empecemos por lo más común: un documento. Le pido una guía de bienvenida para nuevas incorporaciones. Se abre el artefacto y ya tengo el borrador entero a la derecha.
>
> Ahora viene la parte buena. Para pulirlo no tengo que describir por chat qué párrafo quiero cambiar. Selecciono el texto directamente en el documento, pulso "Editar con Claude", y escribo qué quiero. Claude hace el cambio exactamente ahí, donde lo he marcado.
>
> Y si tienes varios cambios repartidos por el documento, puedes dejarlos todos marcados antes de enviar: se acumulan en tu siguiente mensaje y Claude los aplica de una pasada.

**EN PANTALLA**
Selección de un párrafo → botón **Editar con Claude** → escribir algo corto y concreto tipo "esto en dos frases y sin el tono corporativo" → el párrafo cambiando en su sitio. Después, marcar dos ediciones más en otras zonas y enviarlas juntas; que se vea el contador de peticiones pendientes.

---

## BLOQUE 4 — Versiones: el motivo por el que esto importa (2:00 – 2:45)

**LOCUCIÓN**
> Aquí está el título de este vídeo. Cada vez que Claude modifica el artefacto, la versión anterior no se pierde: se guarda. Y puedes moverte entre ellas con el selector de versiones.
>
> Esto es lo que te permite ser valiente. Pedir un cambio radical de tono, probar una reestructuración entera, romperlo a propósito. Si sale mal, vuelves atrás y no has perdido nada.
>
> Y hay una segunda red de seguridad, más potente y menos conocida: puedes editar un mensaje *anterior* de la conversación. Eso crea una rama distinta del chat, con su propio juego de artefactos. Así exploras dos caminos en paralelo, en lugar de sacrificar uno para probar el otro.

**EN PANTALLA**
Primero: pedir en directo un cambio agresivo ("reescríbelo entero en tono de manual técnico"), verlo destrozado, y volver con el selector de versiones. El "uf" tiene que sentirse.
Después: editar un mensaje anterior del chat y mostrar cómo aparece un artefacto distinto conviviendo con el original.

---

## BLOQUE 5 — De la tabla a la pequeña aplicación (2:45 – 3:25)

**LOCUCIÓN**
> Los artefactos no son solo texto. Le paso mis horas por proyecto y le pido una tabla, y la tengo en el documento. Pero si le pido un panel, el salto es otro: obtengo algo interactivo, con filtros y ordenación, que puedo usar de verdad.
>
> Y funciona igual que el documento: si algo no me cuadra, lo pido y se actualiza en la misma ventana, con su historial de versiones detrás.
>
> Cuando algo se rompe —y con las aplicaciones pasa— fíjate en el botón "Intentar arreglarlo con Claude" junto al error. Copia el detalle del fallo a un mensaje nuevo para que Claude lo diagnostique. No siempre lo resuelve a la primera, pero te ahorra explicar el error a mano.

**EN PANTALLA**
Tabla estática primero. Luego el panel: clic en filtros, ordenar una columna, que se vea que responde. Provoca un error de verdad si puedes (un dato mal formado) y muestra el botón de arreglo.

---

## BLOQUE 6 — Sacarlo de la conversación (3:25 – 4:05)

**LOCUCIÓN**
> Última pieza: cómo te lo llevas fuera. En la esquina del panel del artefacto puedes ver el código que hay debajo, copiar el contenido y descargarlo como archivo.
>
> Y un detalle que evita confusión: si abres varios artefactos en un mismo chat, usa los controles del chat para cambiar entre ellos y para decirle a Claude cuál debe actualizar. Si no, corres el riesgo de que modifique el que no querías.
>
> Ojo con una cosa que sorprende a todo el mundo: los artefactos que creas dentro de una conversación **no** aparecen solos en la sección Artefactos de la barra lateral. Para que vivan ahí, tienes que abrirlos y publicarlos. Si algún día no encuentras aquel panel que hiciste, probablemente sigue dentro de su chat.

**EN PANTALLA**
Recorrido por ver código / copiar / descargar. Después, controles de chat cambiando de artefacto. Cierre del bloque: la barra lateral, la sección **Artefactos**, y el clic en **Publicar** que hace aparecer el panel en la lista.

---

## BLOQUE 7 — Cierre (4:05 – 4:25)

**LOCUCIÓN**
> Resumiendo el cambio de mentalidad: sin artefactos, le pides a Claude una versión, y otra, y otra, y vas coleccionando bloques de texto en el chat. Con artefactos hay un solo objeto que va mejorando, y un historial que te deja equivocarte sin coste.
>
> Y esto es solo el lienzo. Lo que se puede colgar de él —conectar el artefacto a tus herramientas, o que guarde datos entre sesiones— lo vemos más adelante.

**EN PANTALLA**
Split screen final: izquierda, un chat larguísimo lleno de versiones sueltas; derecha, un único artefacto limpio con su selector de versiones. Fundido con el bumper de cierre.

---

## Notas de producción

- **La definición cierra antes del minuto 1** (bloque 1). Cumple la promesa del título y no la retrases: es el pacto con el espectador.
- **El momento fuerte es el bloque 4**, la vuelta atrás. Grábalo con una versión destrozada de verdad, no con un cambio menor; el alivio tiene que verse.
- **No expliques la interfaz con palabras.** En este vídeo la pantalla lleva el peso: locuta el "por qué" mientras el espectador ve el "dónde".
- **Si te pasas de 4:30:** el candidato a salir es el trozo de los controles de chat con varios artefactos del bloque 6 (–15 s) y la tabla estática del bloque 5 (–10 s), entrando directamente al panel interactivo.
- **Cuidado con "tabla".** Una tabla dentro de un documento es un artefacto; un `.xlsx` descargable es un archivo, no un artefacto. Si vas a tocar Excel, mejor un vídeo aparte para no mezclar los dos conceptos justo cuando acabas de definir el primero.
- **Fecha de caducidad.** Los rótulos de botones y la posición del selector de versiones cambian con las actualizaciones. Si repones este vídeo en unos meses, revisa los bloques 2 y 6 antes que ningún otro.
