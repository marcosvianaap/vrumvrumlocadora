from flask import Flask, url_for
from flask import Blueprint, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/administrador")
def administrador():
    return render_template("administrador.html")

@app.route("/administrador/funcionarios")
def pesquisar_funcionario():
    return render_template("pesquisar_funcionario.html")

@app.route("/administrador/funcionarios/criarFuncionario")
def criar_funcionario():
    script_url = url_for('static', filename='js/menssagemErro.js') #Caminho absoluto do script
    return render_template("criar_funcionario.html", script_url=script_url)

if __name__ == "__main__":
    app.run(debug=True)
