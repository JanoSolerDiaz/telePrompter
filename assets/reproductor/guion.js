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
    if (document.fullscreenElement) {
      // Ya en pantalla completa (p. ej. al pasar de escena a escena desde el
      // propio reproductor, T-20): no hace falta pedirla de nuevo, solo
      // recuperar el foco en el elemento indicado.
      if (elementoAFocarAlTerminar) {
        elementoAFocarAlTerminar.focus();
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
          elementoAFocarAlTerminar.focus();
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

    indicadorVelocidad = document.createElement("span");
    indicadorVelocidad.className = "velocidad-escena";
    indicadorVelocidad.id = "velocidad-escena";
    info.appendChild(indicadorVelocidad);

    indicadorPausa = document.createElement("span");
    indicadorPausa.className = "estado-pausa";
    indicadorPausa.id = "estado-pausa";
    info.appendChild(indicadorPausa);

    cabecera.appendChild(info);

    var botonVolver = document.createElement("button");
    botonVolver.type = "button";
    botonVolver.className = "btn-volver";
    botonVolver.id = "btn-volver-indice";
    botonVolver.textContent = "Volver al índice";
    botonVolver.addEventListener("click", function () {
      volverAlIndice(indice);
    });
    cabecera.appendChild(botonVolver);

    vistaReproductor.appendChild(cabecera);

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
    iniciarMotor(indice);
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
  var indicadorPausa = null;
  var escenaActual = -1;
  var bloqueActual = 0;
  var pausado = false;
  var temporizadorBloque = null;
  var bloqueInicioMarca = 0;
  var bloqueMsRestantes = 0;

  function bloquesEscenaActual() {
    return datos.escenas[escenaActual].bloques;
  }

  function duracionBaseBloqueMs(bloque) {
    return Math.max(bloque.fin_segundos - bloque.inicio_segundos, 0) * 1000;
  }

  function marcarBloqueActivo(indice) {
    elementosBloque.forEach(function (elemento, i) {
      elemento.classList.toggle("bloque--activo", i === indice);
    });
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
    iniciarTemporizadorBloque();
  }

  function irABloque(indice) {
    var bloques = bloquesEscenaActual();
    if (bloques.length === 0) {
      return;
    }
    bloqueActual = Math.max(0, Math.min(indice, bloques.length - 1));
    marcarBloqueActivo(bloqueActual);
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
      if (bloqueMsRestantes > 0) {
        temporizadorBloque = setTimeout(avanzarAutomatico, bloqueMsRestantes);
      }
    } else {
      pausado = true;
      detenerTemporizador();
      bloqueMsRestantes = Math.max(bloqueMsRestantes - (Date.now() - bloqueInicioMarca), 0);
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
    actualizarIndicadorPausa();
    if (bloquesEscenaActual().length > 0) {
      marcarBloqueActivo(0);
      iniciarTemporizadorBloque();
    }
  }

  function detenerMotor() {
    detenerTemporizador();
    escenaActual = -1;
    bloqueActual = 0;
    pausado = false;
  }

  function manejarTeclaReproductor(evento) {
    if (vistaReproductor.hidden) {
      return;
    }
    switch (evento.key) {
      case " ":
      case "Spacebar":
        evento.preventDefault();
        togglePausa();
        break;
      case "+":
      case "=":
        evento.preventDefault();
        ajustarVelocidad(datos.paso_velocidad);
        break;
      case "-":
        evento.preventDefault();
        ajustarVelocidad(-datos.paso_velocidad);
        break;
      case "ArrowRight":
      case "PageDown":
        evento.preventDefault();
        bloqueSiguienteManual();
        break;
      case "ArrowLeft":
      case "PageUp":
        evento.preventDefault();
        bloqueAnteriorManual();
        break;
      case "ArrowUp":
        evento.preventDefault();
        escenaAdyacente(-1);
        break;
      case "ArrowDown":
        evento.preventDefault();
        escenaAdyacente(1);
        break;
      case "r":
      case "R":
        evento.preventDefault();
        reiniciarEscenaActual();
        break;
      default:
        break;
    }
  }

  document.addEventListener("keydown", manejarTeclaReproductor);

  renderizarIndice();
})();
