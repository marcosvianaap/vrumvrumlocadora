const botaoEditar = document.getElementById("botaoEditarFuncionario");
const blocoDadosFuncionario = document.getElementById("blocoFuncionario");
const blocoEditarDados = document.getElementById("blocoEditarDados");

botaoEditar.addEventListener("click", function () {

    blocoDadosFuncionario.style.display = "none";
    blocoEditarDados.style.display = "block";
});

const botaoConfirmarEdicao = document.getElementById("botaoConfirmarEdicao");

botaoConfirmarEdicao.addEventListener("click", function (event) {

    event.preventDefault();

    blocoDadosFuncionario.style.display = "block";
    blocoEditarDados.style.display = "none";
});
