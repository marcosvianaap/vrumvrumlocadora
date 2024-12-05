const botoesEditar = document.querySelectorAll(".botaoEditarFuncionario");

botoesEditar.forEach(function (botaoEditar) {
    botaoEditar.addEventListener("click", function () {

        const blocoPesquisa = botaoEditar.closest(".blocoPesquisa");
        const blocoFuncionario = blocoPesquisa.querySelector(".blocoFuncionario");
        const blocoEditar = blocoPesquisa.querySelector(".blocoEditarDados");

        blocoFuncionario.style.display = "none";
        blocoEditar.style.display = "block";
    });
});

const botoesCancelar = document.querySelectorAll(".botaoCancelarEdicao");

botoesCancelar.forEach(function (botaoCancelar) {
    botaoCancelar.addEventListener("click", function (event) {
        event.preventDefault();
        const blocoPesquisa = botaoCancelar.closest(".blocoPesquisa");
        const blocoFuncionario = blocoPesquisa.querySelector(".blocoFuncionario");
        const blocoEditar = blocoPesquisa.querySelector(".blocoEditarDados");

        blocoFuncionario.style.display = "block";
        blocoEditar.style.display = "none";
    });
});

function mostrarOcultarSenha() {
    const campoSenha = document.getElementById("senha");
    if (campoSenha.type === "password") {
      campoSenha.type = "text";
    } else {
      campoSenha.type = "password";
    }
    const olho = document.getElementById("olho");
    const olho1 = olho.getAttribute("data-olho1")
    const olho2 = olho.getAttribute("data-olho2")

    olho.src = olho.src.includes("eye.png") ? olho2 : olho1;

  }


document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.botao-ver-senha').forEach(botao => {
    botao.addEventListener('click', (event) => {
      const botaoClicado = event.currentTarget;
      const container = botaoClicado.closest('.senha-container');
      const campoSenha = container.querySelector('.senha'); 
      const olho = container.querySelector('.olho'); 

      if (campoSenha.type === 'password') {
        campoSenha.type = 'text';
      } else {
        campoSenha.type = 'password';
      }

      const olho1 = olho.getAttribute('data-olho1');
      const olho2 = olho.getAttribute('data-olho2');
      olho.src = olho.src.includes('eye-close-up.png') ? olho1 : olho2;
    });
  });
});