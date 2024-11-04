#Autores: Gabrielli Danker, José Mateus, Lucas Sena, Marcos Viana, Monique Ellen
#Ultima edição: 04/11/2024

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def tela_login():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)