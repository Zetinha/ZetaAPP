document.addEventListener('DOMContentLoaded', () => {
  // Script já existente
  const btn = document.querySelector('.upload button');
  if (btn) {
    btn.addEventListener('click', () => {
      console.log('Botão clicado, formulário vai enviar normalmente.');
    });
  }

  // Novo dropdown do botão "Login"
  const toggle = document.querySelector(".dropdown-toggle");
  const menu = document.querySelector(".dropdown-menu");

  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      menu.style.display = (menu.style.display === "block") ? "none" : "block";
    });

    document.addEventListener("click", function (e) {
      if (!e.target.closest(".dropdown")) {
        menu.style.display = "none";
      }
    });
  }
});
