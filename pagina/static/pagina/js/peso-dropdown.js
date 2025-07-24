document.addEventListener('DOMContentLoaded', function() {
  const generoSelect = document.getElementById('id_genero');
  const pesoSelect = document.getElementById('id_peso_select');

  const pesosMasculino = ['53', '59', '66', '74', '83', '93', '105', '120', '120+'];
  const pesosFeminino = ['47', '52', '57', '63', '69', '76', '84', '84+'];

  function preencherPesos() {
    const genero = generoSelect.value;
    pesoSelect.innerHTML = '';  // limpa opções

    let listaPesos = [];
    if (genero === 'M') {
      listaPesos = pesosMasculino;
    } else if (genero === 'F') {
      listaPesos = pesosFeminino;
    }

    listaPesos.forEach(peso => {
      const option = document.createElement('option');
      option.value = peso;
      option.textContent = peso;
      pesoSelect.appendChild(option);
    });
  }

  generoSelect.addEventListener('change', preencherPesos);

  preencherPesos();

  // Pré-seleciona o peso salvo, se houver
  const pesoAtual = pesoSelect.getAttribute('data-peso-atual');
  if (pesoAtual) {
    pesoSelect.value = pesoAtual;
  }
});
