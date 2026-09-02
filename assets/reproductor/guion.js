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

    var cabecera = document.createElement("header");
    cabecera.className = "reproductor-cabecera";

    var contador = document.createElement("span");
    contador.className = "contador-escena";
    contador.id = "contador-escena";
    contador.textContent = (indice + 1) + "/" + datos.escenas.length;
    cabecera.appendChild(contador);

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
    escena.bloques.forEach(function (bloque) {
      var item = document.createElement("li");
      item.className = "bloque";
      item.textContent = bloque.texto;
      listaBloques.appendChild(item);
    });
    seccion.appendChild(listaBloques);

    vistaReproductor.appendChild(seccion);
    botonVolver.focus();
    return botonVolver;
  }

  function reproducirEscena(indice) {
    var botonVolver = renderizarReproductor(indice);
    vistaIndice.hidden = true;
    vistaReproductor.hidden = false;
    solicitarPantallaCompleta(botonVolver);
  }

  function volverAlIndice(indice) {
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

  renderizarIndice();
})();
