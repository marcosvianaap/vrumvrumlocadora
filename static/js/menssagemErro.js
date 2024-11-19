// Script de Validação e Exibição de Mensagens do formulário de criação de func.
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('formCriaFuncionario');
    const responseMessage = document.getElementById('responseMessage');

    form.addEventListener('submit', function (event) {
        

        if (form.checkValidity()) {
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

// Script de Validação e Exibição de Mensagens do formulário de criação de func.
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('formCriaCliente');
    const responseMessage = document.getElementById('responseMessage');

    form.addEventListener('submit', function (event) {
        

        if (form.checkValidity()) {
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


document.addEventListener('DOMContentLoaded', function () {
    const forms = document.querySelectorAll('.editarFuncionario');

    forms.forEach(function (form) {
        const responseMessage = form.querySelector('.responseMessage2'); 

        form.addEventListener('submit', function (event) {
            if (form.checkValidity()) {
                responseMessage.classList.remove('d-none', 'alert-danger');
                responseMessage.classList.add('alert-success');
                responseMessage.textContent = 'Atualização feita com sucesso!';
            } else {
                event.preventDefault(); 
                form.classList.add('was-validated');
                responseMessage.classList.remove('d-none', 'alert-success');
                responseMessage.classList.add('alert-danger');
                responseMessage.textContent = 'Erro ao cadastrar. Verifique os campos.';
            }
        });
    });
});
