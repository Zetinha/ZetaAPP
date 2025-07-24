document.addEventListener('DOMContentLoaded', function () {
  const generoSelect = document.getElementById('id_genero');
  const categoriaSelect = document.getElementById('id_categoria');

  const categoriasPorGenero = {
    'M': ['53', '59', '66', '74', '83', '93', '105', '120', '120+'],
    'F': ['47', '52', '57', '63', '69', '76', '84', '84+']
  };

  function atualizarCategorias() {
    const genero = generoSelect.value;
    categoriaSelect.innerHTML = '';
    if (categoriasPorGenero[genero]) {
      categoriasPorGenero[genero].forEach(cat => {
        const option = document.createElement('option');
        option.value = cat;
        option.textContent = cat;
        categoriaSelect.appendChild(option);
      });
    }
  }

  generoSelect.addEventListener('change', atualizarCategorias);

  // inicializa ao carregar a página
  atualizarCategorias();
});
