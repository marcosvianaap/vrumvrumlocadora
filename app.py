#Autores: Gabrielli Danker, José Mateus, Lucas Sena, Marcos Viana, Monique Ellen
#Ultima edição: 14/11/2024

#USUARIO E SENHA
#usuario: 11313993905
#senha: 11313993905

from werkzeug.security import generate_password_hash
from flask import Flask, flash, render_template, session,request,redirect,url_for
from flask import render_template
import instance.banco as bd

app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = 'chaveSecretaParaCriptografia'


#rota para a página principal do administrador
@app.route("/administrador")
def administrador():
    return render_template("administrador.html")

#rota para a página para pesquisar funcionários
@app.route("/administrador/funcionarios", methods=['GET', 'POST'])
def pesquisar_funcionario():
    funcionarios = None
    funcionario = None
    informacao= None #verificar se foi digitado algum cpf ou nome

    if request.method == 'POST':
       
        if "form1" in request.form: #Formulário para busca de funcionarios por CPF ou Nome

            informacao = request.form['informacao']
            
            funcionarios = bd.filtro_funcionarios(informacao)

            if not(funcionarios): #Se retornar vazio, avisa ao usuário que não foi encontrado nenhum funcionário com determinado CPF/Nome
                flash('Funcionário não encontrado', 'warning')
                return render_template('pesquisar_funcionario.html')
            
            return render_template('pesquisar_funcionario.html',funcionario= funcionario, informacao=informacao, funcionarios=funcionarios)

        elif "form2" in request.form: #Formulário para alteração de informações do funcionário

            nome = request.form['nome']
            novo_cpf = request.form['cpf'] #CPF que irá substituir no banco
            id = request.form['id']
            funcionario = None

            cpf_original = bd.obterCPF(id)
            if cpf_original:
                cpf_original = cpf_original[0]
            
            if not(cpf_original==novo_cpf) and bd.verificaCpf(novo_cpf): #Verificação de CPF único
                flash('CPF já existente!', 'warning')
                funcionario = bd.filtro_funcionarios(cpf_original)
                return render_template('pesquisar_funcionario.html', funcionario=funcionario, informacao=informacao,  funcionarios=funcionarios)

            telefone = request.form['telefone']
            email = request.form['email']
            Data_Nascimento = request.form['data_nascimento']
            endereco = request.form['endereco']
            senha = request.form['senha']

            if senha:
                senha = generate_password_hash(senha)

            status = request.form['status']

            try:
                bd.atualizaFuncionario(novo_cpf, endereco, Data_Nascimento, email, telefone, nome, senha, status, cpf_original)
                flash('Funcionário atualizado com sucesso!', 'success')

                funcionarios = bd.filtro_funcionarios(novo_cpf)
                return render_template('pesquisar_funcionario.html', funcionario=funcionario, informacao=informacao,  funcionarios=funcionarios)
            
            except Exception as e:
                return f"Ocorreu um erro ao atualizar os dados: {e}", 500
        
    return render_template('pesquisar_funcionario.html', funcionario=funcionario, informacao=informacao, funcionarios=funcionarios)


#rota para criar um novo funcionário no banco de dados
@app.route("/administrador/funcionarios/criarFuncionario", methods=['GET','POST'])
def criar_funcionario():
    script1_url = url_for('static', filename='js/menssagemErro.js') #Caminho absoluto do script
    script2_url = url_for('static', filename='js/Script.js')

    cpf = None

    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']

        if bd.verificaCpf(cpf): #Verificação de CPF único
            flash('CPF já existente!', 'warning')
            return render_template("criar_funcionario.html", script1_url=script1_url, script2_url=script2_url)

        telefone = request.form['telefone']
        email = request.form['email']
        Data_Nascimento = request.form['dataNascimento']
        endereco = request.form['endereco']
        senha = request.form['senha']
        senha = generate_password_hash(senha)

        bd.adicionarFuncionario(cpf, endereco, Data_Nascimento, email, telefone, nome, senha)

        flash('Funcionário criado com sucesso!', 'success')

    return render_template("criar_funcionario.html", script1_url=script1_url, script2_url=script2_url)

# ROTAS PARA HISTÓRICO DE VEICULOS ----------------------------

@app.route("/funcionario/historico_devolução")
def historico_devolucao():
    return render_template("historico_devolução.html")

@app.route("/funcionario/historico_locação")
def historico_locacao():
    return render_template("historico_locação.html")

@app.route("/funcionario/teste")
def teste():
    return render_template("base_cliente.html")


# ROTAS PARA GERENCIAMENTO DE VEICULOS ----------------------------

#rota para a tela de listagem de veiculos
@app.route("/administrador/veiculos")
def gerenciar_veiculos():

    conn = bd.connect_to_db()
    cursor = conn.cursor()
    
    modeloVeiculo = request.args.get('modelo')
    if modeloVeiculo == None:
        cursor.execute("SELECT id,Ano_Aquisicao,Placa,RENAVAM,Modelo,Marca,Ano_Fabricacao,Cor,Tipo_Combustivel,Valor_Locacao_Dia,Status FROM Veiculo")
    else:
        cursor.execute("SELECT id,Ano_Aquisicao,Placa,RENAVAM,Modelo,Marca,Ano_Fabricacao,Cor,Tipo_Combustivel,Valor_Locacao_Dia,Status FROM Veiculo WHERE Modelo = ?",(modeloVeiculo,))

    veiculosRaw = cursor.fetchall()
    veiculos = []
    colunas = ["id","Ano_Aquisicao","Placa","RENAVAM","Modelo","Marca","Ano_Fabricacao","Cor","Tipo_Combustivel","Valor_Locacao_Dia","Status"]
    for i in veiculosRaw:
        veiculo = {}
        for index,j in enumerate(i):
            veiculo[colunas[index]] = j
        veiculos.append(veiculo)
    conn.close()

    flash('Veiculo criado com sucesso!', 'success')

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

    #verificar se existe um renavam ou placa ja no banco de dados
    cursor.execute("SELECT id FROM Veiculo WHERE Placa = ? OR RENAVAM = ?",(placa,renavam))
    veiculo = cursor.fetchone()
    if veiculo:
        flash('Erro ao criar veiculo! Já existe um veiculo com essa placa ou RENAVAM', 'danger')
        return redirect(url_for("frontend_criar_veiculos")) 

    cursor.execute("INSERT INTO Veiculo (Ano_Aquisicao,Placa,RENAVAM,Modelo,Marca,Ano_Fabricacao,Cor,Tipo_Combustivel,Valor_Locacao_Dia,Status) VALUES (?,?,?,?,?,?,?,?,?,?)",(anoAquisicao,placa,renavam,modelo,marca,anoFabricacao,cor,tipoCombustivel,valorAlocacao,status))
    conn.commit()

    return redirect(url_for("gerenciar_veiculos")) 

#Rota para a tela de editar um veiculo
@app.route("/administrador/veiculos/frontend_editar_veiculo",methods=['POST','GET'])
def frontend_editar_veiculo():

    veiculo = None
    if request.method == 'POST':
        veiculo = request.form["veiculo"]
    elif request.method == 'GET' and 'ultimaEdicao' in session:
        veiculo = session['ultimaEdicao']
        del session['ultimaEdicao']

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

    cursor.execute("SELECT id FROM Veiculo WHERE Placa = ? OR RENAVAM = ?",(placa,renavam))
    veiculoExistente = cursor.fetchone()
    print(f'ID: {veiculoExistente[0]}\nVEICULO: {veiculo}')

    if veiculoExistente != None:
        
        if int(veiculo) != int(veiculoExistente[0]):
            session['ultimaEdicao'] = veiculo
            flash('Erro ao editar veiculo! Já existe um veiculo com essa placa ou RENAVAM', 'danger')
            return redirect(url_for("frontend_editar_veiculo")) 

    cursor.execute("""
                   UPDATE Veiculo 
                   SET Ano_Aquisicao = ?, Placa = ?, RENAVAM = ?, Modelo = ?, Marca = ?, Ano_Fabricacao = ?, Cor = ?, Tipo_Combustivel = ?, Valor_Locacao_Dia = ?, Status = ? 
                   WHERE id = ? 
                   """,(anoAquisicao,placa,renavam,modelo,marca,anoFabricacao,cor,tipoCombustivel,valorAlocacao,status,veiculo))
    conn.commit()
    conn.close()

    flash('Veiculo editado com sucesso!', 'success')
    return redirect(url_for("gerenciar_veiculos")) 



@app.route('/')
def index():
    if 'statusLogin' in session:
        del session['statusLogin']
        flash('Credenciais de acesso invalidas', 'danger')
        return render_template("index.html")
    else:
        return render_template("index.html")

      
@app.route("/entrar",methods=['POST'])
def processoEntrar():
    if not bd.autenticarUsuario(request.form):
        if 'usuario' in session:
            del session['usuario']
        session["statusLogin"] = {"acessoNegado":True,"nomeUsuario":request.form["usuario"],"mensagemErro":"Credenciais de acesso inválidas. Tente novamente"}
        return redirect(url_for("index"))
    else:
        session['usuario'] = request.form['usuario']
        return redirect(url_for("administrador"))

#rota para sair do sistema
@app.route("/sair")
def processoSair():
    if 'usuario' in session:
        del session['usuario']
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
