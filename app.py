#Autores: Gabrielli Danker, José Mateus, Lucas Sena, Marcos Viana, Monique Ellen
#Ultima edição: 04/11/2024

from flask import Flask, render_template, session,request,redirect,url_for
#from flask_bcrypt import Bcrypt
import instance.banco as bd

#configurando o framework
app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = 'chaveSecretaParaCriptografia'
#bcrypt = Bcrypt(app)




#rotas para a pagina de inicio
@app.route('/')
def index():
    return render_template("index.html")




#rotas para entrar e sair do sistema
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