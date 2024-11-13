#Autores: Gabrielli Danker, José Mateus, Lucas Sena, Marcos Viana, Monique Ellen
#Ultima edição: 04/11/2024

#from flask_bcrypt import Bcrypt

from flask import Flask, render_template, session,request,redirect,url_for
from flask import Blueprint, render_template
import instance.banco as bd

#configurando o framework
app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = 'chaveSecretaParaCriptografia'
#bcrypt = Bcrypt(app)

#rotas para entrar e sair do sistema
@app.route('/')
def index():
    return render_template("index.html")

@app.route("/administrador")
def administrador():
    return render_template("administrador.html")

@app.route("/administrador/funcionarios")
def pesquisar_funcionario():
    return render_template("pesquisar_funcionario.html")


# Rota de gerenciamento de veiculos
@app.route("/administrador/veiculos")
def gerenciar_veiculos():
    return render_template("geren_veic.html")

#Rota para cadastrar um novo veiculo
@app.route("/administrador/veiculos/cadastro")
def criar_veiculos():
    return render_template("criar_veiculo.html")

@app.route("/administrador/funcionarios/criarFuncionario")
def criar_funcionario():
    script_url = url_for('static', filename='js/menssagemErro.js') #Caminho absoluto do script
    return render_template("criar_funcionario.html", script_url=script_url)


@app.route('/tela_login')
def tela_login():
    if 'statusLogin' in session:
        acesso_negado = session["statusLogin"]['acessoNegado']
        mensagem = session["statusLogin"]["mensagemErro"]
        usuario = session["statusLogin"]["nomeUsuario"]
        return render_template("tela_login.html",acesso_negado=acesso_negado,mensagem=mensagem,usuario=usuario)
    else:
        return render_template("tela_login.html")

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