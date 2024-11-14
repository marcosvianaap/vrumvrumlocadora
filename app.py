#Autores: Gabrielli Danker, José Mateus, Lucas Sena, Marcos Viana, Monique Ellen
#Ultima edição: 14/11/2024

from werkzeug.security import generate_password_hash
from flask import Flask, flash, render_template, session,request,redirect,url_for
from flask import render_template
import instance.banco as bd

app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = 'chaveSecretaParaCriptografia'

#rota para entrar no sistema
@app.route('/')
def index():
    return render_template("index.html")

#rota para a página principal do administrador
@app.route("/administrador")
def administrador():
    return render_template("administrador.html")

#rota para a página para pesquisar funcionários
@app.route("/administrador/funcionarios", methods=['GET', 'POST'])
def pesquisar_funcionario():
    funcionario = None
    cpf1= None #verificar se foi digitado algum cpf

    if request.method == 'POST':
       
        if "form1" in request.form:

            cpf1 = request.form['cpf']
            session['cpfBusca'] = cpf1 #Guarda o CPF em sessão para ser utilizado na busca
            funcionario = bd.buscarUsuarioPorCPF(cpf1)

        elif "form2" in request.form:

            cpf1 = session['cpfBusca'] #CPF usado na busca
            nome = request.form['nome']
            cpf2 = request.form['cpf'] #CPF que irá substituir no banco
            telefone = request.form['telefone']
            email = request.form['email']
            Data_Nascimento = request.form['data_nascimento']
            endereco = request.form['endereco']
            senha = request.form['senha']

            if senha:
                senha = generate_password_hash(senha)

            status = request.form['status']

            try:
                bd.atualizaFuncionario(cpf2, endereco, Data_Nascimento, email, telefone, nome, senha, status, cpf1)
                flash('Funcionário atualizado com sucesso!', 'success')

                return render_template('pesquisar_funcionario.html', funcionario=funcionario, cpf1=cpf1)
            
            except Exception as e:
                return f"Ocorreu um erro ao atualizar os dados: {e}", 500


#rota para criar um novo funcionário no banco de dados
@app.route("/administrador/funcionarios/criarFuncionario", methods=['GET','POST'])
def criar_funcionario():
    script_url = url_for('static', filename='js/menssagemErro.js') #Caminho absoluto do script

    cpf = None

    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        email = request.form['email']
        Data_Nascimento = request.form['dataNascimento']
        endereco = request.form['endereco']
        senha = request.form['senha']
        senha = generate_password_hash(senha)

        bd.adicionarFuncionario(cpf, endereco, Data_Nascimento, email, telefone, nome, senha)

        flash('Funcionário criado com sucesso!', 'success')

    return render_template("criar_funcionario.html", script_url=script_url)

#rota para acessar a tela de login
@app.route('/tela_login')
def tela_login():
    if 'statusLogin' in session:
        acesso_negado = session["statusLogin"]['acessoNegado']
        mensagem = session["statusLogin"]["mensagemErro"]
        usuario = session["statusLogin"]["nomeUsuario"]
        return render_template("tela_login.html",acesso_negado=acesso_negado,mensagem=mensagem,usuario=usuario)
    else:
        return render_template("tela_login.html")

#rota para autenticar as credenciais do usuário e entrar no sistema
@app.route("/entrar",methods=['POST'])
def processoEntrar():
    if not bd.autenticarUsuario(request.form):
        if 'usuario' in session:
            del session['usuario']
        session["statusLogin"] = {"acessoNegado":True,"nomeUsuario":request.form["usuario"],"mensagemErro":"Credenciais de acesso inválidas. Tente novamente"}
        return redirect(url_for("tela_login"))
    else:
        session['usuario'] = request.form['usuario']
        return redirect(url_for("index"))

@app.route("/processo/sair")
def processoSair():
    if 'usuario' in session:
        del session['usuario']
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)