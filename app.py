from flask import Flask
from flask import Blueprint, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/administrador")
def administrador():
    return render_template("home_administrador.html")

@app.route("/administrador/funcionarios")
def pesquisar_funcionario():
    return render_template("pesquisar_funcionario.html")

if __name__ == "__main__":
    app.run(debug=True)
