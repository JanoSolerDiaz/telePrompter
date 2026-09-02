(function () {
  "use strict";

  var datosElemento = document.getElementById("datos-reproductor");
  var contenedor = document.getElementById("app");
  if (!datosElemento || !contenedor) {
    return;
  }

  var datos;
  try {
    datos = JSON.parse(datosElemento.textContent);
  } catch (error) {
    contenedor.textContent = "No se han podido leer los datos del guion.";
    return;
  }

  function formatearTiempo(segundos) {
    var total = Math.max(Math.round(segundos), 0);
    var minutos = Math.floor(total / 60);
    var resto = total % 60;
    return minutos + ":" + (resto < 10 ? "0" : "") + resto;
  }

  // Persistencia local del ajuste de espejo (T-25, requisito 3 y criterio de
  // aceptacion: "el ajuste persiste tras recargar"). T-26 disena el mecanismo
  // general para el resto de preferencias (tamano de texto, velocidad por
  // escena, ultima escena vista, indicadores); esta clave sigue ya el mismo
  // patron que T-26 va a necesitar (derivada del guion, requisito 2 de T-26)
  // para que esa tarea solo tenga que reutilizarla, no redisenarla. Con
  // `try/catch`: `localStorage` puede fallar (navegacion privada, cuota
  // agotada, o el propio `file://` sin soporte -- hallazgo #5 de
  // `auditoriacontinua.md`, ya conocido) y el reproductor sigue funcionando
  // en memoria, solo sin recordar el ajuste entre sesiones.
  function claveAlmacenamiento(preferencia) {
    return "teleprompter:" + datos.guion + ":" + preferencia;
  }

  function leerPreferencia(preferencia) {
    try {
      return window.localStorage.getItem(claveAlmacenamiento(preferencia));
    } catch (error) {
      return null;
    }
  }

  function guardarPreferencia(preferencia, valor) {
    try {
      window.localStorage.setItem(claveAlmacenamiento(preferencia), valor);
    } catch (error) {
      // Sin persistencia disponible: se ignora, no es un error del reproductor.
    }
  }

  // Estado por escena (T-19, requisito 1). Solo en memoria: no persiste entre
  // sesiones (eso es T-26/R-02, con su propio mecanismo). Aqui una escena pasa
  // de "pendiente" a "grabada" en cuanto se ha abierto y cerrado el reproductor
  // sobre ella al menos una vez; "revisada" queda definida para cuando R-02
  // aporte un dato real de revision, pero ninguna interaccion de T-19 la activa
  // todavia.
  var ETIQUETAS_ESTADO = { pendiente: "Pendiente", grabada: "Grabada", revisada: "Revisada" };
  var estadosEscena = datos.escenas.map(function () {
    return "pendiente";
  });
  // Velocidad recordada por escena (T-20, requisito 5): multiplicador sobre la
  // duracion estimada de cada bloque, 1.0 = sin acelerar ni frenar. Solo en
  // memoria de la pestaña, mismo criterio que `estadosEscena` de arriba --
  // persistirla entre sesiones es T-26, con su propio mecanismo.
  var velocidadesEscena = datos.escenas.map(function () {
    return 1.0;
  });
  var botonesEscena = [];

  var vistaIndice = document.createElement("section");
  vistaIndice.id = "vista-indice";
  var vistaReproductor = document.createElement("section");
  vistaReproductor.id = "vista-reproductor";
  vistaReproductor.hidden = true;
  contenedor.appendChild(vistaIndice);
  contenedor.appendChild(vistaReproductor);

  function crearBadgeEstado(indice) {
    var badge = document.createElement("span");
    badge.className = "escena-estado escena-estado--" + estadosEscena[indice];
    badge.textContent = ETIQUETAS_ESTADO[estadosEscena[indice]];
    return badge;
  }

  function actualizarBadgeEstado(indice) {
    var fila = botonesEscena[indice];
    var badgeAnterior = fila.querySelector(".escena-estado");
    fila.replaceChild(crearBadgeEstado(indice), badgeAnterior);
  }

  function moverFocoEnIndice(evento) {
    var indiceActual = botonesEscena.indexOf(document.activeElement);
    if (indiceActual === -1) {
      return;
    }
    var siguiente = null;
    if (evento.key === "ArrowDown") {
      siguiente = Math.min(indiceActual + 1, botonesEscena.length - 1);
    } else if (evento.key === "ArrowUp") {
      siguiente = Math.max(indiceActual - 1, 0);
    } else if (evento.key === "Home") {
      siguiente = 0;
    } else if (evento.key === "End") {
      siguiente = botonesEscena.length - 1;
    }
    if (siguiente !== null) {
      evento.preventDefault();
      botonesEscena[siguiente].focus();
    }
  }

  function renderizarIndice() {
    var titulo = document.createElement("h1");
    titulo.textContent = datos.guion;
    vistaIndice.appendChild(titulo);

    var resumen = document.createElement("p");
    resumen.className = "resumen-guion";
    resumen.textContent =
      datos.escenas.length +
      " escenas · " +
      formatearTiempo(datos.duracion_total_segundos) +
      " estimado · " +
      datos.ritmo_ppm +
      " ppm";
    vistaIndice.appendChild(resumen);

    var lista = document.createElement("ul");
    lista.className = "lista-escenas";
    lista.addEventListener("keydown", moverFocoEnIndice);

    datos.escenas.forEach(function (escena, indice) {
      var item = document.createElement("li");
      var fila = document.createElement("button");
      fila.type = "button";
      fila.className = "escena-fila";
      fila.id = "escena-fila-" + indice;
      fila.setAttribute(
        "aria-label",
        "Reproducir escena " + (indice + 1) + ": " + escena.titulo
      );

      var numero = document.createElement("span");
      numero.className = "escena-numero";
      numero.textContent = (indice + 1) + ".";
      fila.appendChild(numero);

      var tituloEscena = document.createElement("span");
      tituloEscena.className = "escena-titulo";
      tituloEscena.textContent = escena.titulo;
      fila.appendChild(tituloEscena);

      var duracion = document.createElement("span");
      duracion.className = "escena-duracion";
      duracion.textContent = formatearTiempo(escena.duracion_estimada_segundos);
      fila.appendChild(duracion);

      fila.appendChild(crearBadgeEstado(indice));

      fila.addEventListener("click", function () {
        reproducirEscena(indice);
      });

      botonesEscena[indice] = fila;
      item.appendChild(fila);
      lista.appendChild(item);
    });

    vistaIndice.appendChild(lista);
  }

  function solicitarPantallaCompleta(elementoAFocarAlTerminar) {
    // `{ preventScroll: true }` (T-22): sin esto, un foco en un boton situado
    // arriba de la pagina (la cabecera) dispara el scroll-into-view por
    // defecto del navegador y deshace el centrado que acaba de calcular
    // `centrarBloqueActivo` -- confirmado con Playwright: al conceder pantalla
    // completa, este foco diferido llegaba DESPUES del centrado inicial de
    // `iniciarMotor` y lo pisaba, devolviendo el scroll a 0 en cada entrada a
    // una escena.
    if (document.fullscreenElement) {
      // Ya en pantalla completa (p. ej. al pasar de escena a escena desde el
      // propio reproductor, T-20): no hace falta pedirla de nuevo, solo
      // recuperar el foco en el elemento indicado.
      if (elementoAFocarAlTerminar) {
        elementoAFocarAlTerminar.focus({ preventScroll: true });
      }
      return;
    }
    if (!document.documentElement.requestFullscreen) {
      return;
    }
    document.documentElement
      .requestFullscreen()
      .then(function () {
        // Chromium quita el foco de cualquier elemento al completar la
        // transicion a pantalla completa; sin esto, el recorrido por teclado
        // se quedaria sin foco visible justo despues de arrancar la escena.
        if (elementoAFocarAlTerminar) {
          elementoAFocarAlTerminar.focus({ preventScroll: true });
        }
      })
      .catch(function () {
        // El navegador de grabacion puede denegar pantalla completa (p. ej.
        // sin gesto de usuario reconocido); el reproductor sigue funcionando
        // en modo ventana, sin romper la pagina ni dejar un error en consola.
      });
  }

  function salirPantallaCompleta() {
    if (document.fullscreenElement && document.exitFullscreen) {
      document.exitFullscreen().catch(function () {});
    }
  }

  function renderizarReproductor(indice) {
    // Devuelve el boton "Volver al indice" para que quien reproduce la escena
    // pueda recuperarle el foco tras la transicion a pantalla completa.
    vistaReproductor.textContent = "";
    elementosBloque = [];

    var cabecera = document.createElement("header");
    cabecera.className = "reproductor-cabecera";

    var info = document.createElement("div");
    info.className = "reproductor-info";

    var contador = document.createElement("span");
    contador.className = "contador-escena";
    contador.id = "contador-escena";
    contador.textContent = (indice + 1) + "/" + datos.escenas.length;
    info.appendChild(contador);

    elementoCronometro = document.createElement("span");
    elementoCronometro.className = "cronometro-toma";
    elementoCronometro.id = "cronometro-toma";
    info.appendChild(elementoCronometro);

    indicadorTamano = document.createElement("span");
    indicadorTamano.className = "tamano-texto";
    indicadorTamano.id = "tamano-texto";
    info.appendChild(indicadorTamano);

    indicadorVelocidad = document.createElement("span");
    indicadorVelocidad.className = "velocidad-escena";
    indicadorVelocidad.id = "velocidad-escena";
    info.appendChild(indicadorVelocidad);

    indicadorPausa = document.createElement("span");
    indicadorPausa.className = "estado-pausa";
    indicadorPausa.id = "estado-pausa";
    info.appendChild(indicadorPausa);

    cabecera.appendChild(info);

    var controles = document.createElement("div");
    controles.className = "reproductor-controles";

    botonEspejo = document.createElement("button");
    botonEspejo.type = "button";
    botonEspejo.className = "btn-volver btn-espejo";
    botonEspejo.id = "btn-espejo";
    botonEspejo.addEventListener("click", alternarEspejo);
    actualizarBotonEspejo();
    controles.appendChild(botonEspejo);

    var botonVolver = document.createElement("button");
    botonVolver.type = "button";
    botonVolver.className = "btn-volver";
    botonVolver.id = "btn-volver-indice";
    botonVolver.textContent = "Volver al índice";
    botonVolver.addEventListener("click", function () {
      volverAlIndice(indice);
    });
    controles.appendChild(botonVolver);

    cabecera.appendChild(controles);

    vistaReproductor.appendChild(cabecera);
    aplicarClaseEspejo();

    // Barra de progreso de la escena por bloques (T-23, requisito 3): el
    // relleno crece con `(bloqueActual + 1) / total`, asi que llega al 100 %
    // justo con el ultimo bloque, no con el tiempo estimado.
    var barraProgresoContenedor = document.createElement("div");
    barraProgresoContenedor.className = "barra-progreso-contenedor";
    elementoBarraProgreso = document.createElement("div");
    elementoBarraProgreso.className = "barra-progreso-relleno";
    barraProgresoContenedor.appendChild(elementoBarraProgreso);
    vistaReproductor.appendChild(barraProgresoContenedor);

    // Cuenta atras 3-2-1 antes de arrancar (T-23, requisito 1): oculta por
    // defecto, `iniciarCuentaAtras` la muestra si esta activada en la
    // configuracion.
    elementoCuentaAtras = document.createElement("div");
    elementoCuentaAtras.className = "cuenta-atras";
    elementoCuentaAtras.hidden = true;
    vistaReproductor.appendChild(elementoCuentaAtras);

    // Ayuda de teclado (T-24, requisito 3): oculta por defecto, `alternarAyuda`
    // la muestra/oculta con la tecla `?`. Se reconstruye en cada escena, igual
    // que el resto de la cabecera -- es barata (una docena de elementos) y asi
    // no hay que preocuparse de que sobreviva a `vistaReproductor.textContent = ""`.
    elementoAyuda = document.createElement("div");
    elementoAyuda.className = "ayuda-teclado";
    elementoAyuda.id = "ayuda-teclado";
    elementoAyuda.hidden = true;
    var panelAyuda = document.createElement("div");
    panelAyuda.className = "ayuda-teclado-panel";
    var tituloAyuda = document.createElement("h2");
    tituloAyuda.textContent = "Atajos de teclado";
    panelAyuda.appendChild(tituloAyuda);
    panelAyuda.appendChild(construirListaAyudaTeclado());
    var cierreAyuda = document.createElement("p");
    cierreAyuda.className = "ayuda-teclado-cierre";
    cierreAyuda.textContent = "Pulsa ? para cerrar esta ayuda.";
    panelAyuda.appendChild(cierreAyuda);
    elementoAyuda.appendChild(panelAyuda);
    vistaReproductor.appendChild(elementoAyuda);

    var escena = datos.escenas[indice];
    var seccion = document.createElement("section");
    seccion.className = "escena";

    var encabezado = document.createElement("h2");
    encabezado.textContent =
      escena.numero +
      ". " +
      escena.titulo +
      " — " +
      formatearTiempo(escena.duracion_estimada_segundos);
    seccion.appendChild(encabezado);

    var listaBloques = document.createElement("ol");
    listaBloques.className = "bloques";
    escena.bloques.forEach(function (bloque, indiceBloque) {
      var item = document.createElement("li");
      item.className = "bloque";
      item.id = "bloque-" + indiceBloque;
      item.textContent = bloque.texto;
      elementosBloque[indiceBloque] = item;
      listaBloques.appendChild(item);
    });
    seccion.appendChild(listaBloques);

    vistaReproductor.appendChild(seccion);
    botonVolver.focus();
    return botonVolver;
  }

  function reproducirEscena(indice) {
    detenerMotor();
    var botonVolver = renderizarReproductor(indice);
    vistaIndice.hidden = true;
    vistaReproductor.hidden = false;
    solicitarPantallaCompleta(botonVolver);
    iniciarCuentaAtras(function () {
      iniciarMotor(indice);
    });
  }

  function volverAlIndice(indice) {
    detenerMotor();
    salirPantallaCompleta();
    if (estadosEscena[indice] === "pendiente") {
      estadosEscena[indice] = "grabada";
      actualizarBadgeEstado(indice);
    }
    vistaReproductor.hidden = true;
    vistaIndice.hidden = false;
    var boton = botonesEscena[indice];
    if (boton) {
      boton.focus();
    }
  }

  // --- Motor de avance hibrido (T-20) --------------------------------------
  //
  // El automatico resalta cada bloque durante su duracion estimada (T-12:
  // `fin_segundos - inicio_segundos`, que ya incluye la pausa tras el
  // bloque), escalada por la velocidad vigente de la escena. Avanzar a mano
  // (bloque/escena) o pausar nunca "sale" de este modo ni lo reinicia por
  // completo: solo reinician el reloj del bloque actual (requisito 3).
  var elementosBloque = [];
  var indicadorVelocidad = null;
  var indicadorTamano = null;
  var indicadorPausa = null;
  var escenaActual = -1;
  var bloqueActual = 0;
  var pausado = false;
  var temporizadorBloque = null;
  var bloqueInicioMarca = 0;
  var bloqueMsRestantes = 0;

  // --- Ayudas de grabacion (T-23) -------------------------------------------
  var elementoCuentaAtras = null;
  var temporizadorCuentaAtras = null;
  var elementoCronometro = null;
  var cronometroInicioMarca = 0;
  var cronometroMsAcumulados = 0;
  var intervaloCronometro = null;
  var elementoBarraProgreso = null;

  // --- Atajos de teclado y clicker Bluetooth (T-24) --------------------------
  var elementoAyuda = null;

  // --- Modo espejo (T-25) -----------------------------------------------------
  var botonEspejo = null;
  var espejoActivado = leerPreferencia("espejo") === "1";

  // Texto de cada accion en la ayuda (requisito 3): fijo en espanol, no viaja
  // en el JSON -- a diferencia de las TECLAS (que si son configurables por el
  // dueno via `datos.mapa_teclas`), estas etiquetas son literales de interfaz
  // que no tiene sentido reconfigurar.
  var ETIQUETAS_ACCION_TECLADO = {
    pausa_avanza: "Pausar / reanudar (o avanzar, segun configuracion)",
    bloque_siguiente: "Bloque siguiente",
    bloque_anterior: "Bloque anterior",
    escena_anterior: "Escena anterior",
    escena_siguiente: "Escena siguiente",
    velocidad_mas: "Aumentar velocidad",
    velocidad_menos: "Reducir velocidad",
    tamano_mas: "Aumentar tamano de texto",
    tamano_menos: "Reducir tamano de texto",
    reiniciar_escena: "Reiniciar escena",
    ocultar_indicadores: "Mostrar / ocultar indicadores",
    salir_pantalla_completa: "Salir de pantalla completa",
    ayuda: "Mostrar / ocultar esta ayuda",
    espejo: "Activar / desactivar modo espejo"
  };

  // Nombre legible de una tecla tal como la reporta `KeyboardEvent.key`
  // (requisito 3, "mapa... visible en una ayuda"): sin esto la ayuda mostraria
  // literales crudos como " " o "ArrowRight", ilegibles para quien graba.
  var ETIQUETAS_TECLA = {
    " ": "Espacio",
    Spacebar: "Espacio",
    ArrowRight: "→",
    ArrowLeft: "←",
    ArrowUp: "↑",
    ArrowDown: "↓",
    PageDown: "Av Pág",
    PageUp: "Re Pág",
    Escape: "Esc"
  };

  function etiquetaTecla(tecla) {
    return ETIQUETAS_TECLA[tecla] || tecla;
  }

  // Construye la lista de la ayuda leyendo `datos.mapa_teclas` (requisito 3:
  // "visible... el mapa VIGENTE" -- nunca una copia escrita a mano que pudiera
  // desincronizarse del mapa real que usa `manejarTeclaReproductor`).
  function construirListaAyudaTeclado() {
    var lista = document.createElement("ul");
    lista.className = "ayuda-teclado-lista";
    Object.keys(datos.mapa_teclas).forEach(function (accion) {
      var etiquetasTeclas = [];
      datos.mapa_teclas[accion].forEach(function (tecla) {
        var etiqueta = etiquetaTecla(tecla);
        if (etiquetasTeclas.indexOf(etiqueta) === -1) {
          etiquetasTeclas.push(etiqueta);
        }
      });
      var item = document.createElement("li");
      var teclasSpan = document.createElement("span");
      teclasSpan.className = "ayuda-teclado-teclas";
      teclasSpan.textContent = etiquetasTeclas.join(" / ");
      var accionSpan = document.createElement("span");
      accionSpan.className = "ayuda-teclado-accion";
      accionSpan.textContent = ETIQUETAS_ACCION_TECLADO[accion] || accion;
      item.appendChild(teclasSpan);
      item.appendChild(accionSpan);
      lista.appendChild(item);
    });
    return lista;
  }

  function alternarAyuda() {
    if (elementoAyuda) {
      elementoAyuda.hidden = !elementoAyuda.hidden;
    }
  }

  // Mapa de teclas -> accion, construido una vez a partir de `datos.mapa_teclas`
  // (requisito 3, "configurable en la generacion"): `manejarTeclaReproductor`
  // nunca compara literales de teclas escritos a mano.
  var teclaAAccion = {};
  Object.keys(datos.mapa_teclas).forEach(function (accion) {
    datos.mapa_teclas[accion].forEach(function (tecla) {
      teclaAAccion[tecla] = accion;
    });
  });

  // Antirrebote del clicker (requisito 2): un clicker Bluetooth barato puede
  // enviar la misma tecla dos veces por un unico clic fisico (rebote de
  // contacto). Se descarta una pulsacion de la MISMA accion si llega antes de
  // que pasen `antirrebote_clicker_ms` desde la ultima aceptada; distintas
  // acciones no se bloquean entre si.
  var ultimaPulsacionPorAccion = {};

  function pulsacionPermitida(accion) {
    var ahora = Date.now();
    var ultima = ultimaPulsacionPorAccion[accion] || 0;
    if (ahora - ultima < datos.antirrebote_clicker_ms) {
      return false;
    }
    ultimaPulsacionPorAccion[accion] = ahora;
    return true;
  }

  // Cuenta atras 3-2-1 antes de arrancar el automatico (requisito 1). Si esta
  // desactivada en la configuracion (o su duracion es 0), arranca al instante
  // -- "desactivable" es este booleano, nunca poner la duracion a cero.
  function iniciarCuentaAtras(alTerminar) {
    if (!datos.cuenta_atras_activada || datos.cuenta_atras_segundos <= 0) {
      alTerminar();
      return;
    }
    var restante = datos.cuenta_atras_segundos;
    elementoCuentaAtras.hidden = false;
    elementoCuentaAtras.textContent = String(restante);
    function tick() {
      restante -= 1;
      if (restante <= 0) {
        elementoCuentaAtras.hidden = true;
        temporizadorCuentaAtras = null;
        alTerminar();
        return;
      }
      elementoCuentaAtras.textContent = String(restante);
      temporizadorCuentaAtras = setTimeout(tick, 1000);
    }
    temporizadorCuentaAtras = setTimeout(tick, 1000);
  }

  function detenerCuentaAtras() {
    if (temporizadorCuentaAtras !== null) {
      clearTimeout(temporizadorCuentaAtras);
      temporizadorCuentaAtras = null;
    }
    if (elementoCuentaAtras) {
      elementoCuentaAtras.hidden = true;
    }
  }

  // Cronometro de la toma (requisito 2): tiempo real transcurrido frente a la
  // duracion estimada de la escena. Cuenta tiempo de reloj, no tiempo de
  // guion -- por eso se congela en pausa (`cronometroMsAcumulados` guarda lo
  // ya transcurrido, `cronometroInicioMarca` se reinicia al reanudar), igual
  // que ya hace el reloj del bloque (`bloqueMsRestantes`/`bloqueInicioMarca`).
  function actualizarCronometro() {
    if (!elementoCronometro || escenaActual === -1) {
      return;
    }
    var transcurridoMs = cronometroMsAcumulados;
    if (!pausado) {
      transcurridoMs += Date.now() - cronometroInicioMarca;
    }
    var estimado = datos.escenas[escenaActual].duracion_estimada_segundos;
    elementoCronometro.textContent =
      formatearTiempo(transcurridoMs / 1000) + " / " + formatearTiempo(estimado);
  }

  function iniciarCronometro() {
    cronometroMsAcumulados = 0;
    cronometroInicioMarca = Date.now();
    actualizarCronometro();
    intervaloCronometro = setInterval(actualizarCronometro, 250);
  }

  function detenerCronometro() {
    if (intervaloCronometro !== null) {
      clearInterval(intervaloCronometro);
      intervaloCronometro = null;
    }
  }

  // Barra de progreso de la escena por bloques (requisito 3): progreso por
  // recuento de bloques, no por tiempo -- asi llega al 100 % exactamente con
  // el ultimo bloque, sin depender de que la duracion real coincida con la
  // estimada.
  function actualizarBarraProgreso() {
    if (!elementoBarraProgreso) {
      return;
    }
    var total = escenaActual === -1 ? 0 : bloquesEscenaActual().length;
    var progreso = total > 0 ? (bloqueActual + 1) / total : 0;
    elementoBarraProgreso.style.width = (progreso * 100) + "%";
  }

  // Indicadores discretos, ocultables con una tecla (requisito 4): un unico
  // interruptor sobre la vista del reproductor, persistente mientras se
  // navega de escena en escena (no se resetea en `renderizarReproductor`,
  // porque el toggle no toca `vistaReproductor.classList`, solo su contenido).
  function alternarIndicadores() {
    vistaReproductor.classList.toggle("indicadores-ocultos");
  }

  // Modo espejo (T-25, requisito 1): volteo horizontal via CSS `transform`, no
  // clases fijas por bloque -- por eso es compatible gratis con el resaltado
  // (T-21, opacidad por bloque) y el autoscroll (T-22, requisito 2): un
  // `transform: scaleX(-1)` no cambia la posicion/altura vertical que usa
  // `getBoundingClientRect` para centrar, solo el eje horizontal. Por defecto
  // (`espejo_incluye_indicadores=false`) el volteo se aplica solo a `.escena`
  // (titulo + bloques, el "texto" del requisito 1); con la configuracion
  // activada, cubre tambien la cabecera y el resto de indicadores.
  function aplicarClaseEspejo() {
    var completo = !!datos.espejo_incluye_indicadores;
    vistaReproductor.classList.toggle("espejo-texto", espejoActivado && !completo);
    vistaReproductor.classList.toggle("espejo-completo", espejoActivado && completo);
  }

  function actualizarBotonEspejo() {
    if (!botonEspejo) {
      return;
    }
    botonEspejo.setAttribute("aria-pressed", String(espejoActivado));
    botonEspejo.textContent = espejoActivado ? "Espejo: activado" : "Espejo: desactivado";
  }

  function alternarEspejo() {
    espejoActivado = !espejoActivado;
    aplicarClaseEspejo();
    guardarPreferencia("espejo", espejoActivado ? "1" : "0");
    actualizarBotonEspejo();
  }

  function bloquesEscenaActual() {
    return datos.escenas[escenaActual].bloques;
  }

  function duracionBaseBloqueMs(bloque) {
    return Math.max(bloque.fin_segundos - bloque.inicio_segundos, 0) * 1000;
  }

  // Resaltado del bloque activo y atenuacion del contexto (T-21, requisito 1):
  // el bloque activo queda a opacidad plena, y cada bloque de contexto recibe
  // la opacidad que le toque segun su distancia, leida del gradiente
  // configurable (`atenuacion_niveles`); mas alla del ultimo nivel se aplica
  // el suelo `atenuacion_minima`, para que el contexto nunca desaparezca del
  // todo.
  function opacidadPorDistancia(distancia) {
    var niveles = datos.atenuacion_niveles;
    var indiceNivel = distancia - 1;
    if (indiceNivel < niveles.length) {
      return niveles[indiceNivel];
    }
    return datos.atenuacion_minima;
  }

  function marcarBloqueActivo(indice) {
    elementosBloque.forEach(function (elemento, i) {
      var esActivo = i === indice;
      elemento.classList.toggle("bloque--activo", esActivo);
      elemento.style.opacity = esActivo ? "" : String(opacidadPorDistancia(Math.abs(i - indice)));
    });
    actualizarBarraProgreso();
  }

  // --- Autoscroll con bloque centrado (T-22) -------------------------------
  //
  // El documento entero desplaza (no hay un contenedor propio con overflow:
  // `#app` crece con la altura natural de la pagina), asi que centrar el
  // bloque activo es mover `window.scrollY`. La animacion es una interpolacion
  // manual con `requestAnimationFrame` -- no `scrollIntoView({behavior:
  // 'smooth'})` -- para poder cancelar limpiamente una animacion en curso y
  // arrancar la siguiente desde la posicion real en ese instante (requisito 2,
  // "sin rebotes al avanzar rapido a mano"): con el nativo, dos llamadas
  // seguidas encolan o interrumpen sin control sobre el punto de partida.
  var animacionScroll = null;

  function detenerAnimacionScroll() {
    if (animacionScroll !== null) {
      cancelAnimationFrame(animacionScroll);
      animacionScroll = null;
    }
  }

  function alturaViewport() {
    return document.documentElement.clientHeight;
  }

  function scrollMaximo() {
    return Math.max(document.documentElement.scrollHeight - alturaViewport(), 0);
  }

  // Suavizado ease-in-out (aceleracion y frenado simetricos, sin rebote).
  function suavizarProgreso(progreso) {
    return progreso < 0.5
      ? 2 * progreso * progreso
      : 1 - Math.pow(-2 * progreso + 2, 2) / 2;
  }

  function centrarBloqueActivo(animado) {
    if (escenaActual === -1) {
      return;
    }
    var elemento = elementosBloque[bloqueActual];
    if (!elemento) {
      return;
    }
    var rect = elemento.getBoundingClientRect();
    var origen = window.scrollY;
    var centroElemento = rect.top + origen + rect.height / 2;
    var objetivo = Math.max(
      0,
      Math.min(centroElemento - alturaViewport() / 2, scrollMaximo())
    );
    detenerAnimacionScroll();
    // Requisito 3 (si el texto cabe entero, no se desplaza nada) sale gratis
    // de esta clausula: con `scrollMaximo() === 0` el objetivo siempre coincide
    // con el origen, y no hay animacion ni salto que hacer.
    if (!animado || Math.abs(objetivo - origen) < 1) {
      window.scrollTo(0, objetivo);
      return;
    }
    var distancia = objetivo - origen;
    var duracion = datos.duracion_autoscroll_ms;
    var marcaInicio = null;
    function paso(marcaActual) {
      if (marcaInicio === null) {
        marcaInicio = marcaActual;
      }
      var progreso = Math.min((marcaActual - marcaInicio) / duracion, 1);
      window.scrollTo(0, origen + distancia * suavizarProgreso(progreso));
      if (progreso < 1) {
        animacionScroll = requestAnimationFrame(paso);
      } else {
        animacionScroll = null;
      }
    }
    animacionScroll = requestAnimationFrame(paso);
  }

  function actualizarIndicadorVelocidad() {
    if (!indicadorVelocidad || escenaActual === -1) {
      return;
    }
    indicadorVelocidad.textContent =
      "Velocidad ×" + velocidadesEscena[escenaActual].toFixed(1);
  }

  function actualizarIndicadorPausa() {
    if (!indicadorPausa) {
      return;
    }
    indicadorPausa.textContent = pausado ? "En pausa" : "";
  }

  // Control en vivo del tamano de texto (T-21, requisito 2). Preferencia de
  // lectura de quien graba, no del ritmo de una escena concreta: a proposito
  // NO es un array paralelo a `datos.escenas` como `velocidadesEscena` -- un
  // unico valor global que persiste mientras se navega de escena en escena,
  // igual que ya hace la velocidad dentro de una misma escena.
  var tamanoTextoActualPx = datos.tamano_texto_base_px;

  function actualizarIndicadorTamano() {
    if (!indicadorTamano) {
      return;
    }
    indicadorTamano.textContent = tamanoTextoActualPx + " px";
  }

  function ajustarTamanoTexto(delta) {
    var nuevo = Math.max(
      datos.tamano_texto_minimo_px,
      Math.min(tamanoTextoActualPx + delta, datos.tamano_texto_maximo_px)
    );
    tamanoTextoActualPx = nuevo;
    document.documentElement.style.setProperty("--tamano-base", nuevo + "px");
    actualizarIndicadorTamano();
    // Requisito 4 (correcto tras cambiar el tamano de texto): el cambio de
    // fuente reflow-ea el bloque activo a otra altura de pagina; recentrarlo
    // con animacion para que el salto no se note como un tirón.
    centrarBloqueActivo(true);
  }

  function detenerTemporizador() {
    if (temporizadorBloque !== null) {
      clearTimeout(temporizadorBloque);
      temporizadorBloque = null;
    }
  }

  // Arranca (o reinicia) el reloj del bloque actual con la duracion completa
  // que le toca a la velocidad vigente. Si esta en pausa, dej a el reloj
  // preparado (`bloqueMsRestantes`) pero no programa el avance automatico
  // hasta que se reanude.
  function iniciarTemporizadorBloque() {
    detenerTemporizador();
    var bloques = bloquesEscenaActual();
    if (bloqueActual >= bloques.length) {
      return;
    }
    var duracionMs = duracionBaseBloqueMs(bloques[bloqueActual]) / velocidadesEscena[escenaActual];
    bloqueInicioMarca = Date.now();
    bloqueMsRestantes = duracionMs;
    if (!pausado) {
      temporizadorBloque = setTimeout(avanzarAutomatico, duracionMs);
    }
  }

  function avanzarAutomatico() {
    var bloques = bloquesEscenaActual();
    temporizadorBloque = null;
    if (bloqueActual + 1 >= bloques.length) {
      return; // ultimo bloque de la escena: nada mas que avanzar solo.
    }
    bloqueActual += 1;
    marcarBloqueActivo(bloqueActual);
    centrarBloqueActivo(true);
    iniciarTemporizadorBloque();
  }

  function irABloque(indice) {
    var bloques = bloquesEscenaActual();
    if (bloques.length === 0) {
      return;
    }
    bloqueActual = Math.max(0, Math.min(indice, bloques.length - 1));
    marcarBloqueActivo(bloqueActual);
    centrarBloqueActivo(true);
    iniciarTemporizadorBloque();
  }

  function bloqueSiguienteManual() {
    if (escenaActual === -1) {
      return;
    }
    irABloque(bloqueActual + 1);
  }

  function bloqueAnteriorManual() {
    if (escenaActual === -1) {
      return;
    }
    irABloque(bloqueActual - 1);
  }

  function reiniciarEscenaActual() {
    if (escenaActual === -1) {
      return;
    }
    irABloque(0);
  }

  function togglePausa() {
    if (escenaActual === -1) {
      return;
    }
    if (pausado) {
      pausado = false;
      bloqueInicioMarca = Date.now();
      cronometroInicioMarca = Date.now();
      if (bloqueMsRestantes > 0) {
        temporizadorBloque = setTimeout(avanzarAutomatico, bloqueMsRestantes);
      }
    } else {
      pausado = true;
      detenerTemporizador();
      bloqueMsRestantes = Math.max(bloqueMsRestantes - (Date.now() - bloqueInicioMarca), 0);
      cronometroMsAcumulados += Date.now() - cronometroInicioMarca;
    }
    actualizarIndicadorPausa();
  }

  function redondearVelocidad(valor) {
    // Evita la deriva de coma flotante al acumular el paso muchas veces
    // seguidas (p. ej. 0.1 + 0.1 + 0.1 en JS no es exactamente 0.3).
    var paso = datos.paso_velocidad;
    return Number((Math.round(valor / paso) * paso).toFixed(2));
  }

  function ajustarVelocidad(delta) {
    if (escenaActual === -1) {
      return;
    }
    // Requisito 2: el cambio de velocidad no toca el bloque en curso, solo
    // se aplica desde el bloque siguiente (el proximo `iniciarTemporizadorBloque`
    // la lee de `velocidadesEscena` de nuevo).
    var nueva = redondearVelocidad(velocidadesEscena[escenaActual] + delta);
    nueva = Math.max(datos.velocidad_minima, Math.min(nueva, datos.velocidad_maxima));
    velocidadesEscena[escenaActual] = nueva;
    actualizarIndicadorVelocidad();
  }

  function escenaAdyacente(delta) {
    if (escenaActual === -1) {
      return;
    }
    var destino = escenaActual + delta;
    if (destino < 0 || destino >= datos.escenas.length) {
      return;
    }
    reproducirEscena(destino);
  }

  function iniciarMotor(indice) {
    escenaActual = indice;
    bloqueActual = 0;
    pausado = false;
    actualizarIndicadorVelocidad();
    actualizarIndicadorTamano();
    actualizarIndicadorPausa();
    actualizarBarraProgreso();
    iniciarCronometro();
    if (bloquesEscenaActual().length > 0) {
      marcarBloqueActivo(0);
      centrarBloqueActivo(false);
      iniciarTemporizadorBloque();
    }
  }

  function detenerMotor() {
    detenerTemporizador();
    detenerCronometro();
    detenerCuentaAtras();
    escenaActual = -1;
    bloqueActual = 0;
    pausado = false;
  }

  // Mapa completo (T-24, requisito 1): cada tecla reconocida se resuelve a una
  // ACCION via `teclaAAccion` (construido a partir de `datos.mapa_teclas`, no
  // de literales aqui), asi que anadir o remapear una tecla es cosa de
  // `Configuracion.mapa_teclas_reproductor`, nunca de tocar este switch.
  function manejarTeclaReproductor(evento) {
    if (vistaReproductor.hidden) {
      return;
    }
    var accion = teclaAAccion[evento.key];
    if (!accion) {
      return;
    }
    // Requisito 2 ("evitar el desplazamiento nativo de la pagina"): toda tecla
    // reconocida cancela su accion por defecto del navegador ANTES de aplicar
    // el antirrebote, para que una pulsacion descartada por rebote tampoco
    // desplace la pagina.
    evento.preventDefault();
    if (!pulsacionPermitida(accion)) {
      return;
    }
    switch (accion) {
      case "pausa_avanza":
        if (datos.espacio_avanza_bloque) {
          bloqueSiguienteManual();
        } else {
          togglePausa();
        }
        break;
      case "bloque_siguiente":
        bloqueSiguienteManual();
        break;
      case "bloque_anterior":
        bloqueAnteriorManual();
        break;
      case "escena_anterior":
        escenaAdyacente(-1);
        break;
      case "escena_siguiente":
        escenaAdyacente(1);
        break;
      case "velocidad_mas":
        ajustarVelocidad(datos.paso_velocidad);
        break;
      case "velocidad_menos":
        ajustarVelocidad(-datos.paso_velocidad);
        break;
      case "tamano_mas":
        ajustarTamanoTexto(datos.paso_tamano_texto_px);
        break;
      case "tamano_menos":
        ajustarTamanoTexto(-datos.paso_tamano_texto_px);
        break;
      case "reiniciar_escena":
        reiniciarEscenaActual();
        break;
      case "ocultar_indicadores":
        alternarIndicadores();
        break;
      case "salir_pantalla_completa":
        salirPantallaCompleta();
        break;
      case "ayuda":
        alternarAyuda();
        break;
      case "espejo":
        alternarEspejo();
        break;
      default:
        break;
    }
  }

  document.addEventListener("keydown", manejarTeclaReproductor);

  // Cursor oculto en pantalla completa tras inactividad (T-21, requisito 4):
  // "cero elementos que distraigan" incluye el propio puntero del raton
  // quieto sobre la imagen. Solo se oculta con pantalla completa activa; al
  // salir de ella (o al mover el raton) vuelve a mostrarse de inmediato.
  var temporizadorCursor = null;

  function ocultarCursor() {
    temporizadorCursor = null;
    if (document.fullscreenElement) {
      contenedor.classList.add("cursor-oculto");
    }
  }

  function reprogramarOcultarCursor() {
    contenedor.classList.remove("cursor-oculto");
    if (temporizadorCursor !== null) {
      clearTimeout(temporizadorCursor);
    }
    temporizadorCursor = setTimeout(ocultarCursor, datos.tiempo_inactividad_cursor_ms);
  }

  // Requisito 4 (correcto tras redimensionar la ventana): recentra sin
  // animacion -- un redimensionado no es un gesto de lectura, es un cambio
  // estructural del lienzo, y animarlo solo añadiria un desfase visible
  // mientras el usuario todavia esta arrastrando el borde de la ventana.
  window.addEventListener("resize", function () {
    centrarBloqueActivo(false);
  });

  document.addEventListener("mousemove", reprogramarOcultarCursor);
  document.addEventListener("fullscreenchange", function () {
    if (document.fullscreenElement) {
      reprogramarOcultarCursor();
    } else {
      contenedor.classList.remove("cursor-oculto");
      if (temporizadorCursor !== null) {
        clearTimeout(temporizadorCursor);
        temporizadorCursor = null;
      }
    }
  });

  renderizarIndice();
})();
