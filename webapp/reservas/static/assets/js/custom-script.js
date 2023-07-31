["theme"].forEach((elemento) => {
  verificarLocalStorage(elemento);
});

function themeSwapper() {
    let element = document.body;
    element.dataset.bsTheme = localStorage.getItem('theme') == "light" ? "dark" : "light";
    localStorage.setItem('theme', element.dataset.bsTheme);

    let iconElement = document.getElementById("theme-swapper-icon");
    if (localStorage.getItem('theme') == "light") {
        iconElement.classList.remove("fa-solid", "fa-sun");
        iconElement.classList.add("fa-solid", "fa-moon");
    }
    else {
        iconElement.classList.remove("fa-solid", "fa-moon");
        iconElement.classList.add("fa-solid", "fa-sun");
    }
}

function verificarLocalStorage(key, value = "") {
  if (typeof localStorage !== "undefined") {
    if (localStorage.getItem(key)) {
      if (value !== "") localStorage.setItem(key, value);
      else {
        switch (key) {
          case "theme":
            document.body.dataset.bsTheme = localStorage.getItem('theme');
            break;
          case "view-mode":
            value = localStorage.getItem(key);
            switch (value) {
              case "table":
                tableViewMode()
                break;
              case "compact_card":
                compactCardViewMode()
                break;
              case "card":
                cardViewMode()
                break;
              default:
                console.log("ERROR Filter");
            }
            break;
          default:
            console.log("No se a especificado valor.");
        }
      }
    }
    else {
      switch (key) {
          case "theme":
            localStorage.setItem(key, 'light');
            document.body.dataset.bsTheme = localStorage.getItem('theme');
            break;
          case "view-mode":
            localStorage.setItem(key, 'table');
            break;
          default:
            console.log("Error al establecer key con valor predeterminado");
        }
    }
  }
  else {
    console.log("localStorage no es compatible en este navegador.");
  }
}