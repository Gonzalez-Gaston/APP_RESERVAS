["view-mode"].forEach((elemento) => {
  verificarLocalStorage(elemento);
});

function edit_empleado(boton) {
  document.getElementById("ModalLabel").textContent = "Modificar Empleado";
  let fila = boton.parentNode.parentNode;
  let valores = [fila.cells[0].innerText, fila.cells[1].innerText, fila.cells[2].innerText];
  let ids = ['id_nombre', 'id_apellido', 'id_numero_legajo'];

  for (let i = 0; i < ids.length; i++) {
    document.getElementById(ids[i]).value = valores[i];
  }
  document.getElementById("form_modificar").setAttribute("action", "/empleados/modificar/" + boton.getAttribute("data-id"));
}

function edit_coordinador(boton) {
  let titulo = document.getElementById("ModalLabel").textContent;
  document.getElementById("ModalLabel").textContent = "Modificar Coordinador";
  let fila = boton.parentNode.parentNode;
  let valores = [fila.cells[0].innerText, fila.cells[1].innerText, fila.cells[2].innerText];
  let ids = ['id_nombre', 'id_apellido', 'id_dni'];

  for (let i = 0; i < ids.length; i++) {
    document.getElementById(ids[i]).value = valores[i];
  }

  document.getElementById("form_modificar").setAttribute("action", "/coordinador/modificar/" + boton.getAttribute("data-id"));
}

function edit_cliente(boton) {
  document.getElementById("ModalLabel").textContent = "Modificar Cliente";
  let fila = boton.parentNode.parentNode;
  let valores = [fila.cells[0].innerText, fila.cells[1].innerText];
  let ids = ['id_nombre', 'id_apellido'];

  for (let i = 0; i < ids.length; i++) {
    document.getElementById(ids[i]).value = valores[i];
  }
  document.getElementById("form_modificar").setAttribute("action", "/clientes/modificar/" + boton.getAttribute("data-id"));
}

function edit_reserva(boton) {
  document.getElementById("ModalLabel").textContent = "Modificar Reserva";
  //document.getElementById('id_precio').disabled = true;
  document.getElementById('id_precio').readOnly = true;
  let fila = boton.parentNode.parentNode;
  let valores = [];
  let ids = ['id_precio'];

  document.getElementById('id_precio').value = fila.cells[5].innerText.replaceAll("$ ","");

  let fechaReservaInput = document.getElementById('id_fecha_reserva');

  let fechaHora = fila.cells[0].innerText;
  let partes = fechaHora.split(", "); // Separa la fecha de la hora
  let fechaPartes = partes[0].split(" "); // Separa los componentes de la fecha
  let mesNombre = fechaPartes[0];
  let dia = parseInt(fechaPartes[1], 10);
  let año = parseInt(partes[1], 10);
  let horaPartes = partes[2].split(":"); // Separa los componentes de la hora
  let hora = parseInt(horaPartes[0], 10);
  let minutos = parseInt(horaPartes[1].split(" ")[0], 10);
  let ampm = horaPartes[1].split(" ")[1];

  // Mapea el nombre del mes a su número correspondiente
  const meses = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
  ];
  let mes = meses.findIndex(mes => mes.toLowerCase() === mesNombre.toLowerCase());

  // Ajusta la hora si es PM (p.m.)
  if (ampm.toLowerCase() === "p.m.") {
    hora += 12;
  }

  let fechaExistente = new Date(año, mes, dia, hora, minutos);

  //let fechaExistente = new Date(fila.cells[0].innerText);
  fechaExistente.setHours(fechaExistente.getHours() - fechaExistente.getTimezoneOffset() / 60);
  let fechaFormateada = fechaExistente.toISOString().slice(0, 16);
  fechaReservaInput.value = fechaFormateada;

  document.getElementById("form_modificar").setAttribute("action", "/reservas/modificar/" + boton.getAttribute("data-id"));
}

function edit_servicio(boton, descripcion) {
  let titulo = document.getElementById("ModalLabel").textContent;
  document.getElementById("ModalLabel").textContent = "Modificar Servicio";
  let fila = boton.parentNode.parentNode;
  let valores = [fila.cells[1].innerText, fila.cells[2].innerText.replaceAll("$ ", ""), descripcion];
  let ids = ['id_nombre', 'id_precio', 'id_descripcion'];

  for (let i = 0; i < ids.length; i++) {
    document.getElementById(ids[i]).value = valores[i];
  }
  document.getElementById("form_modificar").setAttribute("action", "/servicios/modificar/" + boton.getAttribute("data-id"));
}

function refresh(titulo, id) {
  var elementoPrecio = document.getElementById('id_precio');
  if (elementoPrecio) {
    elementoPrecio.disabled = true;
  }
  document.getElementById(id).textContent = titulo;
}

function cleanData(name) {
  var url = "#"
  var ids = []
  switch (name) {
    case "Cliente":
      name = "Nuevo " + name
      ids = ['id_nombre', 'id_apellido'];
      url = "/clientes/nuevo"
      break;
    case "Servicio":
      name = "Nuevo " + name
      ids = ['id_nombre', 'id_precio', 'id_descripcion'];
      url = "/servicios/nuevo"
      break;
    case "Empleado":
      name = "Nuevo " + name
      ids = ['id_nombre', 'id_apellido', 'id_numero_legajo'];
      url = "/empleados/nuevo"
      break;
    case "Coordinador":
      name = "Nuevo " + name
      ids = ['id_nombre', 'id_apellido', 'id_dni'];
      url = "/coordinadores/nuevo"
      break;
    case "Reserva":
      name = "Nueva " + name
      url = "/reservas/nuevo"
      const select = document.getElementById('id_servicios');
      const selectedOption = select.options[select.selectedIndex];
      document.getElementById('id_precio').value = selectedOption.getAttribute('data-precio');
      document.getElementById('id_precio').readOnly = true;
      break;
    default:
      console.log("ERROR: ID no encontrado");
  }
  document.getElementById("ModalLabel").textContent = name;
  for (let i = 0; i < ids.length; i++) {
    document.getElementById(ids[i]).value = '';
  }
  document.getElementById("form_modificar").setAttribute("action", url);
}

function setViewMode(key, value) {
  key = "view-mode";
  switch (value) {
    case "table":
      tableViewMode();
      break;
    case "compact_cards":
      compactCardViewMode();
      break;
    case "cards":
      cardViewMode();
      break;
    default:
      console.log("ERROR View");
  }
  verificarLocalStorage(key, value);
}

function tableViewMode() {
  let row = document.getElementById("a_table_id");
  ["a_compact_cards_id", "a_cards_id"].forEach((elemento) => {
    row = document.getElementById(elemento);
    if (row.classList.contains('active')) {
      row.classList.remove('active');
    }

    if (row.getAttribute('href') == null) {
      row.setAttribute('href', '#');
    }
  });

  row = document.getElementById("a_table_id");
  if (!row.classList.contains('active')) {
    row.classList.add('active');
  }

  row.removeAttribute('href');

  ["compact_cards_id", "cards_id"].forEach((elemento) => {
    row = document.getElementById(elemento);
    if (row.classList.contains('active')) {
      row.classList.remove('active');
    }
    if (row.classList.contains('show')) {
      row.classList.remove('show');
    }
  });

  row = document.getElementById("table_id");
  if (!row.classList.contains('active')) {
    row.classList.add('active');
  }
  if (!row.classList.contains('show')) {
    row.classList.add('show');
  }
  verificarLocalStorage("view-mode", "table");
}

function compactCardViewMode() {
  let row = document.getElementById("a_compact_cards_id");
  ["a_table_id", "a_cards_id"].forEach((elemento) => {
    row = document.getElementById(elemento);
    if (row.classList.contains('active')) {
      row.classList.remove('active');
    }

    if (row.getAttribute('href') == null) {
      row.setAttribute('href', '#');
    }
  });

  row = document.getElementById("a_compact_cards_id");
  if (!row.classList.contains('active')) {
    row.classList.add('active');
  }

  row.removeAttribute('href');

  ["table_id", "cards_id"].forEach((elemento) => {
    row = document.getElementById(elemento);
    if (row.classList.contains('active')) {
      row.classList.remove('active');
    }
    if (row.classList.contains('show')) {
      row.classList.remove('show');
    }
  });

  row = document.getElementById("compact_cards_id");
  if (!row.classList.contains('active')) {
    row.classList.add('active');
  }
  if (!row.classList.contains('show')) {
    row.classList.add('show');
  }
  verificarLocalStorage("view-mode", "compact_card");
}

function cardViewMode() {
  let row = document.getElementById("a_cards_id");
  
  ["a_table_id", "a_compact_cards_id"].forEach((elemento) => {
    row = document.getElementById(elemento);
    if (row.classList.contains('active')) {
      row.classList.remove('active');
    }

    if (row.getAttribute('href') == null) {
      row.setAttribute('href', '#');
    }
  });

  row = document.getElementById("a_cards_id");
  if (!row.classList.contains('active')) {
    row.classList.add('active');
  }

  row.removeAttribute('href');

  ["compact_cards_id", "table_id"].forEach((elemento) => {
    row = document.getElementById(elemento);
    if (row.classList.contains('active')) {
      row.classList.remove('active');
    }
    if (row.classList.contains('show')) {
      row.classList.remove('show');
    }
  });

  row = document.getElementById("cards_id");
  if (!row.classList.contains('active')) {
    row.classList.add('active');
  }
  if (!row.classList.contains('show')) {
    row.classList.add('show');
  }
  verificarLocalStorage("view-mode", "card");
}