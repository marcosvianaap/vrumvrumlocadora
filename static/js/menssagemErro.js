// Script de Validação e Exibição de Mensagens

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('formCriaFuncionario');
    const responseMessage = document.getElementById('responseMessage');

    form.addEventListener('submit', function (event) {
        

        if (form.checkValidity()) {
            // Exemplo de sucesso - pode ser substituído com resposta do backend
            responseMessage.classList.remove('d-none', 'alert-danger');
            responseMessage.classList.add('alert-success');
            responseMessage.textContent = 'Cadastro feito com sucesso!';
        } else {
            event.preventDefault();
            event.stopPropagation();
            form.classList.add('was-validated');
            responseMessage.classList.remove('d-none', 'alert-success');
            responseMessage.classList.add('alert-danger');
            responseMessage.textContent = 'Erro ao cadastrar. Verifique os campos.';
        }
    });
});


// Validação dos campos do formulários e exibição de mensagens.
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('editarFuncionario');
    const responseMessage = document.getElementById('responseMessage2');

    form.addEventListener('submit', function (event) {
        

        if (form.checkValidity()) {
            // Exemplo de sucesso - pode ser substituído com resposta do backend
            responseMessage.classList.remove('d-none', 'alert-danger');
            responseMessage.classList.add('alert-success');
            responseMessage.textContent = 'Cadastro feito com sucesso!';
            
        } else {
            event.preventDefault();
            event.stopPropagation();
            form.classList.add('was-validated');
            responseMessage.classList.remove('d-none', 'alert-success');
            responseMessage.classList.add('alert-danger');
            responseMessage.textContent = 'Erro ao cadastrar. Verifique os campos.';
        }
    });
});