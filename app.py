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


@app.after_request
def no_cache(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Decorator para proteger as rotas de usuario
def user_required(f):
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        
        if 'usuario' not in session:
            flash("Você precisa estar autenticado para acessar esta rota!",'danger')
            return redirect(url_for('processoSair'))  # Redireciona para a página de login
        
        if session['usuario'] == 'admin':
            flash("Você precisa estar autenticado para acessar esta rota!",'danger')
            return redirect(url_for('processoSair'))  # Redireciona para a página de login
        
        return f(*args, **kwargs)

    return decorated_function

# Decorator para proteger as rotas de usuario
def admin_required(f):
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        
        if 'usuario' not in session:
            flash("Você precisa estar autenticado para acessar esta rota!",'danger')
            return redirect(url_for('index'))  # Redireciona para a página de login
        
        if session['usuario'] != 'admin':
            flash("Você precisa estar autenticado para acessar esta rota!",'danger')
            return redirect(url_for('processoSair'))  # Redireciona para a página de login
        
        return f(*args, **kwargs)

    return decorated_function





# Rota criada para edição (Deve ser removida no merge)
@app.route("/clientes/loc")
def loc():
    return render_template("criar_locacao.html")


# Rota para a página principal do administrador
@app.route("/administrador")
@admin_required
def administrador():
    return render_template("administrador.html")

#------------------------------------------------------------------
"""GERENCIAMENTO DE CLIENTE"""

#Rota principal para a página de gerenciamento de clientes
@app.route("/funcionarios")
@user_required
def funcionarios():
    return render_template("funcionarios.html")

#rota principal para a página de gerenciamento de clientes
@app.route("/clientes", methods=['GET', 'POST'])
@user_required
def pesquisar_clientes():

    clientes = None
    informacao= None #verificar se foi digitado algum cpf ou nome ou cnpj

    if request.method == 'POST':
       
        if "form1" in request.form: #Formulário para busca de funcionarios por CPF ou Nome ou CNPJ

            informacao = request.form['informacao']
            
            clientes = bd.filtro_clientes(informacao)

            if not(clientes): #Se retornar vazio, avisa ao usuário que não foi encontrado nenhum funcionário com determinado CPF/Nome
                flash('Cliente não encontrado', 'warning')
                return render_template('pesquisar_clientes.html')
            
            return render_template('pesquisar_clientes.html',clientes= clientes, informacao=informacao)

        elif "form2" in request.form: #Formulário para alteração de informações do funcionário

            nome = request.form['nome']
            cpf = None
            cnpj = None
            cpf_cnpj_novo = request.form['cpf_cnpj'] #CPF que irá substituir no banco

            if len(cpf_cnpj_novo) ==11:
                cpf = cpf_cnpj_novo
            else:
                cnpj = cpf_cnpj_novo

            id = request.form['id']

            cpf_cnpj_original = bd.obterCPF_CNPJ(id)

            if cpf_cnpj_original:
                cpf_cnpj_original = cpf_cnpj_original[0]
            
            if not(cpf_cnpj_novo==cpf_cnpj_original) and bd.verificaCpf_Cnpj(cpf_cnpj_novo): #Verificação de CPF único
                flash('CPF/CNPJ já existente!', 'warning')
                clientes = bd.filtro_clientes(cpf_cnpj_original)
                return render_template('pesquisar_clientes.html', clientes=clientes, informacao=informacao)

            telefone = request.form['telefone']
            email = request.form['email']
            Data_Nascimento = request.form['data_nascimento']
            endereco = request.form['endereco']
            cnh = request.form['cnh']
            tipo_cnh= request.form['tipo_cnh']

            try:
                bd.atualizaCliente(cpf, cnpj, endereco, Data_Nascimento, email, telefone, nome, cnh, tipo_cnh, cpf_cnpj_original)
                flash('Cliente atualizado com sucesso!', 'success')

                clientes = bd.filtro_clientes(cpf_cnpj_novo)
                return render_template('pesquisar_clientes.html', clientes=clientes, informacao=informacao)
            
            except Exception as e:
                return f"Ocorreu um erro ao atualizar os dados: {e}", 500
        
    return render_template('pesquisar_clientes.html', clientes=clientes, informacao=informacao)

@app.route("/clientes/cadastrar", methods=['GET', 'POST'])
@user_required
def criar_cliente():

    cpf = None
    cnpj = None

    if request.method == 'POST':
        nome = request.form['nome']
        cpf_cnpj = request.form['cpf_cnpj']

        if len(cpf_cnpj)==11:
            cpf = cpf_cnpj
            cnpj=''
        else:
            cpf=''
            cnpj=cpf_cnpj

        if bd.verificaCpf_Cnpj(cpf_cnpj): #Verificação de CPF único
            flash('CPF/CNPJ já existente!', 'warning')
            return render_template("criar_cliente.html")

        telefone = request.form['telefone']
        email = request.form['email']
        Data_Nascimento = request.form['dataNascimento']
        endereco = request.form['endereco']
        cnh = request.form['cnh']
        tipo_cnh= request.form['tipo_cnh']


        bd.adicionarCliente(cpf, cnpj, endereco, Data_Nascimento, email, telefone, nome, cnh, tipo_cnh)

        flash('Cliente criado com sucesso!', 'success')

    return render_template("criar_cliente.html")


#rota principal para a página de locações
@app.route("/locacoes", methods=['GET', 'POST'])
def locacoes():


    # Dados de exemplo (Devem ser removidos)
    locacoes = [
        {
            "cliente": "João Silva",
            "veiculo": "Toyota Corolla",
            "data_aluguel": "2024-11-20",
            "hora_aluguel": "10:00",
            "data_devolucao": "2024-11-25",
            "hora_devolucao": "10:00",
            "desconto": 5,
            "multa": 10,
            "condicoes_saida": "Tanque cheio, sem danos",
            "status": "Ativo"
        },
        {
            "cliente": "Maria Oliveira",
            "veiculo": "Honda Civic",
            "data_aluguel": "2024-11-22",
            "hora_aluguel": "14:00",
            "data_devolucao": "2024-11-27",
            "hora_devolucao": "14:00",
            "desconto": 10,
            "multa": 0,
            "condicoes_saida": "Tanque cheio, sem danos",
            "status": "Concluído"
        }
    ]
    return render_template('locacao.html', locacoes=locacoes)

    

#-------------------------------------------------------------------


#rota para a página para pesquisar funcionários
@app.route("/administrador/funcionarios", methods=['GET', 'POST'])
@admin_required
def pesquisar_funcionario():
    funcionarios = None
    funcionario= None
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
@admin_required
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
@app.route("/funcionario/historico_devolução",methods=['POST'])
@user_required
def historico_devolucao():
    
    veiculo = request.form['veiculo']


    conn = bd.connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, Data_Hora_Devolucao, Multa, Local_devolucao, Valor_Total, Condicoes_Veiculo, id_locacao FROM Devolucao d WHERE d.id_locacao IN (SELECT l.id FROM Locacao l WHERE l.id_veiculo = ?);",(veiculo,))
    devolucoesRaw = cursor.fetchall()
    devolucoes = []
    colunas = ['id', 'Data_Hora_Devolucao', 'Multa', 'Local_devolucao', 'Valor_Total', 'Condicoes_Veiculo', 'id_locacao']
    for i in devolucoesRaw:
        devolucao = {}
        for index,j in enumerate(i):
            devolucao[colunas[index]] = j
        devolucoes.append(devolucao)
    conn.close()

    print('devolucoes:',devolucoes)
    
    return render_template("historico_devolução.html",devolucoes=devolucoes)

@app.route("/funcionario/historico_locação",methods=['POST'])
@user_required
def historico_locacao():

    veiculo = request.form['veiculo']

    conn = bd.connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, Local_Devolucao, Multa, Data_Hora_Locacao, Data_Hora_Prevista_Devolucao, Valor, id_cliente, id_veiculo, Condicoes_Veiculo,Desconto,Status FROM Locacao WHERE id_veiculo = ?",(veiculo))
    locacoesRaw = cursor.fetchall()
    locacoes = []
    colunas = ['id', 'Local_Devolucao', 'Multa', 'Data_Hora_Locacao', 'Data_Hora_Prevista_Devolucao', 'Valor', 'id_cliente', 'id_veiculo', 'Condicoes_Veiculo', 'Desconto', 'Status']
    for i in locacoesRaw:
        locacao = {}
        for index,j in enumerate(i):
            locacao[colunas[index]] = j
        locacoes.append(locacao)
    conn.close()

    print('LOCACOES:',locacoes)

    return render_template("historico_locação.html",locacoes=locacoes)

@app.route("/funcionario/teste")
def teste():
    return render_template("base_funcionarios.html")





# ROTAS PARA GERENCIAMENTO DE VEICULOS ----------------------------

#rota para a tela de listagem de veiculos
@app.route("/administrador/veiculos")
@admin_required
def gerenciar_veiculos():

    conn = bd.connect_to_db()
    cursor = conn.cursor()
    
    modeloVeiculo = request.args.get('modelo')
    if modeloVeiculo == None:
        cursor.execute("SELECT id,Ano_Aquisicao,Placa,RENAVAM,Modelo,Marca,Ano_Fabricacao,Cor,Tipo_Combustivel,Valor_Locacao_Dia,Status FROM Veiculo")
    else:
        cursor.execute("SELECT id,Ano_Aquisicao,Placa,RENAVAM,Modelo,Marca,Ano_Fabricacao,Cor,Tipo_Combustivel,Valor_Locacao_Dia,Status FROM Veiculo WHERE Modelo LIKE ?",('%' + modeloVeiculo + '%',))
    veiculosRaw = cursor.fetchall()
    veiculos = []
    colunas = ["id","Ano_Aquisicao","Placa","RENAVAM","Modelo","Marca","Ano_Fabricacao","Cor","Tipo_Combustivel","Valor_Locacao_Dia","Status"]
    for i in veiculosRaw:
        veiculo = {}
        for index,j in enumerate(i):
            veiculo[colunas[index]] = j
        veiculos.append(veiculo)
    conn.close()

    return render_template("geren_veic.html",veiculos=veiculos)

#Rota para a tela de cadastro de veiculos
@app.route("/administrador/veiculos/frontend_criar_veiculo")
@admin_required
def frontend_criar_veiculos():
    return render_template("criar_veiculo.html")

#Rota para cadastrar um novo veiculo
@app.route("/administrador/veiculos/backend_criar_veiculo",methods=['POST'])
@admin_required
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

    if request.method == 'POST':

        flash('Veiculo criado com sucesso!', 'success')

    return redirect(url_for("gerenciar_veiculos")) 

#Rota para a tela de editar um veiculo
@app.route("/administrador/veiculos/frontend_editar_veiculo",methods=['POST','GET'])
@admin_required
def frontend_editar_veiculo():

    veiculo = None
    if request.method == 'POST':
        veiculo = request.form["veiculo"]
    elif request.method == 'GET' and 'ultimaEdicao' in session:
        veiculo = session['ultimaEdicao']
        del session['ultimaEdicao']

    
    if not veiculo:
        return redirect(url_for("gerenciar_veiculos")) 
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
@admin_required
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
    veiculosExistentes = cursor.fetchall()

    if veiculosExistentes != []:
        
        jaExiste = False
        if len(veiculosExistentes) > 1:
            jaExiste = True
        else:
            print(veiculosExistentes)
            if int(veiculosExistentes[0][0]) != int(veiculo):
                jaExiste = True

        if jaExiste:
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


#ROTA PARA PESQUISAR VEICULOS
@app.route('/pesquisar', methods=['GET', 'POST'])
@user_required
def pesquisa_veiculo():
    if request.method == 'POST':
        placa = request.form['placa']
        modelo = request.form['modelo']
        marca = request.form['marca']
        cor = request.form['cor']
        ano = request.form['ano']
        valorLocacaoDia = request.form['valor']
        
        carros = bd.buscaCarros(placa,modelo,marca,cor,valorLocacaoDia,ano)

        # Lógica de pesquisa de veículos aqui
        print(carros)
        return render_template('pesquisa_veiculos.html', carros=carros)

    return render_template('pesquisa_veiculos.html')

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
        
        if session['usuario'] == 'admin':
            return redirect(url_for("administrador"))
        else:
            return redirect(url_for("funcionarios"))

#rota para sair do sistema
@app.route("/sair")
def processoSair():
    if 'usuario' in session:
        del session['usuario']
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
