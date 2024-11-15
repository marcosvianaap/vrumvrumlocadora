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
