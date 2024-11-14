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



@app.route('/')
def index():
    return render_template("index.html")

@app.route("/administrador")
def administrador():
    return render_template("administrador.html")



#ROTAS PARA GERENCIAMENTO DE FUNCIONARIOS
@app.route("/administrador/funcionarios")
def pesquisar_funcionario():
    return render_template("pesquisar_funcionario.html")

@app.route("/administrador/funcionarios/criarFuncionario")
def criar_funcionario():
    script_url = url_for('static', filename='js/menssagemErro.js') #Caminho absoluto do script
    return render_template("criar_funcionario.html", script_url=script_url)







# ROTAS PARA GERENCIAMENTO DE VEICULOS ----------------------------

#rota para a tela de listagem de veiculos
@app.route("/administrador/veiculos")
def gerenciar_veiculos():

    conn = bd.connect_to_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id,Ano_Aquisicao,Placa,RENAVAM,Modelo,Marca,Ano_Fabricacao,Cor,Tipo_Combustivel,Valor_Locacao_Dia,Status FROM Veiculo")
    veiculosRaw = cursor.fetchall()
    veiculos = []
    colunas = ["id","Ano_Aquisicao","Placa","RENAVAM","Modelo","Marca","Ano_Fabricacao","Cor","Tipo_Combustivel","Valor_Locacao_Dia","Status"]
    for i in veiculosRaw:
        veiculo = {}
        for index,j in enumerate(i):
            veiculo[colunas[index]] = j
        veiculos.append(veiculo)
    print(veiculos)
    conn.close()

    return render_template("geren_veic.html",veiculos=veiculos)

#Rota para a tela de cadastro de veiculos
@app.route("/administrador/veiculos/frontend_criar_veiculo")
def frontend_criar_veiculos():
    return render_template("criar_veiculo.html")

#Rota para cadastrar um novo veiculo
@app.route("/administrador/veiculos/backend_criar_veiculo",methods=['POST'])
def backend_criar_veiculo():

    modelo = request.form["modelo"]
    cor = request.form["cor"]
    marca = request.form["marca"]
    placa = request.form["placa"]
    renavam = request.form["renavam"]
    anoFabricacao = request.form["anoFabricacao"]
    anoAquisicao = request.form["anoAquisicao"]
    valorAlocacao = request.form["valorAlocacao"]
    tipoCombustivel = request.form["tipoCombustivel"]
    status = request.form["status"]

    conn = bd.connect_to_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Veiculo (Ano_Aquisicao,Placa,RENAVAM,Modelo,Marca,Ano_Fabricacao,Cor,Tipo_Combustivel,Valor_Locacao_Dia,Status) VALUES (?,?,?,?,?,?,?,?,?,?)",(anoAquisicao,placa,renavam,modelo,marca,anoFabricacao,cor,tipoCombustivel,valorAlocacao,status))
    conn.commit()

    return redirect(url_for("gerenciar_veiculos")) 

#Rota para a tela de editar um veiculo
@app.route("/administrador/veiculos/frontend_editar_veiculo",methods=['POST'])
def frontend_editar_veiculo():
    veiculo = request.form["veiculo"]

    conn = bd.connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id,Ano_Aquisicao,Placa,RENAVAM,Modelo,Marca,Ano_Fabricacao,Cor,Tipo_Combustivel,Valor_Locacao_Dia,Status FROM Veiculo WHERE id = ?",(veiculo))
    veiculoRaw = cursor.fetchone()
    veiculoDict = {}
    colunas = ["id","Ano_Aquisicao","Placa","RENAVAM","Modelo","Marca","Ano_Fabricacao","Cor","Tipo_Combustivel","Valor_Locacao_Dia","Status"]
    for index,j in enumerate(veiculoRaw):
        veiculoDict[colunas[index]] = j
    conn.close()

    return render_template("editar_veiculo.html",veiculo=veiculoDict)

#Rota para salvar a edicao de um veiculo
@app.route("/administrador/veiculos/backend_editar_veiculo",methods=['POST'])
def backend_editar_veiculo():

    veiculo = request.form["veiculo"]
    modelo = request.form["modelo"]
    cor = request.form["cor"]
    marca = request.form["marca"]
    placa = request.form["placa"]
    renavam = request.form["renavam"]
    anoFabricacao = request.form["anoFabricacao"]
    anoAquisicao = request.form["anoAquisicao"]
    valorAlocacao = request.form["valorAlocacao"]
    tipoCombustivel = request.form["tipoCombustivel"]
    status = request.form["status"]

    conn = bd.connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
                   UPDATE Veiculo 
                   SET Ano_Aquisicao = ?, Placa = ?, RENAVAM = ?, Modelo = ?, Marca = ?, Ano_Fabricacao = ?, Cor = ?, Tipo_Combustivel = ?, Valor_Locacao_Dia = ?, Status = ? 
                   WHERE id = ? 
                   """,(anoAquisicao,placa,renavam,modelo,marca,anoFabricacao,cor,tipoCombustivel,valorAlocacao,status,veiculo))
    conn.commit()

    return redirect(url_for("gerenciar_veiculos")) 







# ROTAS PARA ENTRAR E SAIR DO SISTEMA ----------------------------------

#rota para a tela de login do sistema
@app.route('/tela_login')
def tela_login():
    if 'statusLogin' in session:
        acesso_negado = session["statusLogin"]['acessoNegado']
        mensagem = session["statusLogin"]["mensagemErro"]
        usuario = session["statusLogin"]["nomeUsuario"]
        return render_template("tela_login.html",acesso_negado=acesso_negado,mensagem=mensagem,usuario=usuario)
    else:
        return render_template("tela_login.html")

#rota para entrar no sistema
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

#rota para sair do sistema
@app.route("/sair")
def processoSair():
    if 'usuario' in session:
        del session['usuario']
    return redirect(url_for('index'))





if __name__ == '__main__':
    app.run(debug=True)