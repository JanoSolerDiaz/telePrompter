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

  var titulo = document.createElement("h1");
  titulo.textContent = datos.guion;
  contenedor.appendChild(titulo);

  var resumen = document.createElement("p");
  resumen.className = "resumen-guion";
  resumen.textContent =
    datos.escenas.length +
    " escenas · " +
    formatearTiempo(datos.duracion_total_segundos) +
    " estimado · " +
    datos.ritmo_ppm +
    " ppm";
  contenedor.appendChild(resumen);

  datos.escenas.forEach(function (escena) {
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

    var lista = document.createElement("ol");
    lista.className = "bloques";
    escena.bloques.forEach(function (bloque) {
      var item = document.createElement("li");
      item.className = "bloque";
      item.textContent = bloque.texto;
      lista.appendChild(item);
    });
    seccion.appendChild(lista);

    contenedor.appendChild(seccion);
  });
})();
