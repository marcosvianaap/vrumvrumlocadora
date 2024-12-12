import re
import sqlite3
import os
from werkzeug.security import check_password_hash,generate_password_hash

#ACESSO ADMIN
#usuario: admin
#senha: senha123


#coisas relacionadas com a estrutura do BD
def connect_to_db():

    conn = sqlite3.connect('instance/banco.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pessoa (
            id                  INTEGER   PRIMARY KEY AUTOINCREMENT,
            CPF                 TEXT NOT NULL,
            Endereco            TEXT NOT NULL,
            Data_Nascimento     DATE NOT NULL,
            Email               TEXT NOT NULL,
            Telefone            TEXT NOT NULL,
            Nome                TEXT NOT NULL
        );
    ''')
    conn.commit()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Usuario (
            pessoa_id           INTEGER NOT NULL,
            Senha               TEXT NOT NULL,
            Cargo               TEXT NOT NULL,
            Status              TEXT NOT NULL,
            FOREIGN KEY (pessoa_id) REFERENCES Pessoa(id)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cliente (
            pessoa_id           INTEGER NOT NULL,
            Numero_CNH          TEXT NOT NULL,
            CNPJ                TEXT NOT NULL,
            Tipo_CNH            TEXT NOT NULL,
            FOREIGN KEY (pessoa_id) REFERENCES Pessoa(id)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Veiculo (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            Ano_Aquisicao       DATE NOT NULL,
            Placa               TEXT NOT NULL,
            RENAVAM             TEXT NOT NULL,
            Modelo              TEXT NOT NULL,
            Marca               TEXT NOT NULL,
            Ano_Fabricacao      DATE NOT NULL,
            Cor                 TEXT NOT NULL,
            Tipo_Combustivel    TEXT NOT NULL,
            Valor_Locacao_Dia   REAL NOT NULL,
            Status              TEXT NOT NULL
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Locacao (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            Local_Devolucao     TEXT NOT NULL,
            Data_Hora_Locacao   DATETIME NOT NULL,
            Data_Hora_Prevista_Devolucao DATETIME NOT NULL,
            Valor               REAL NOT NULL,
            id_cliente          INTEGER NOT NULL,
            id_veiculo          INTEGER NOT NULL,
            Condicoes_Veiculo   TEXT NOT NULL,
            Desconto            REAL NOT NULL,
            Multa               REAL NOT NULL,
            Status              TEXT NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES Pessoa(id),
            FOREIGN KEY (id_veiculo) REFERENCES Veiculo(id)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Devolucao (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            Data_Hora_Devolucao DATETIME NOT NULL,
            Multa               REAL NOT NULL,
            Local_devolucao     TEXT NOT NULL,
            Valor_Total         REAL NOT NULL,
            Condicoes_Veiculo   TEXT NOT NULL,
            id_locacao          INTEGER NOT NULL,
            FOREIGN KEY (id_locacao) REFERENCES Locacao(id)
        );
    ''')
    
    cursor.execute('SELECT pessoa_id FROM Usuario WHERE cargo = ?',('admin',))
    admin = cursor.fetchone()
    if not admin:
        cursor.execute('INSERT INTO Pessoa (CPF,Endereco,Data_Nascimento,Email,Telefone,Nome) VALUES (?,?,?,?,?,?)',('admin','Algum_lugar','22/10/1998','admin@email','40028922','admin'))        
        usuarioIdP = cursor.lastrowid
        cursor.execute('INSERT INTO Usuario (pessoa_id,Senha,Cargo,Status) VALUES (?, ?, ?, ?)', (usuarioIdP, generate_password_hash('senha123'), 'admin', 'ativo'))
        conn.commit()
    conn.commit()
    return conn

def autenticarUsuario(formulario):
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT Usuario.Senha, Usuario.Status
        FROM Pessoa
        JOIN Usuario ON Pessoa.id = Usuario.pessoa_id
        WHERE Pessoa.CPF = ?
    ''', (formulario['usuario'],))
    resultado = cursor.fetchone()
    conn.close()

    # verificação de status de usuario
    if not resultado:
        return False
    
    senha, status = resultado

    if status.lower() != 'ativo':
        return False 

    if check_password_hash(senha, formulario["senha"]):
        return True    

    return False


def buscarClientePorCPFouCNPJ(cpf_ou_cnpj):
    conn = connect_to_db()
    cursor = conn.cursor()
    usuario = None

    try:
        # Primeira tentativa: Buscar pelo CPF
        cursor.execute('''
            SELECT Pessoa.id, Pessoa.Nome, Pessoa.CPF, Pessoa.Telefone, Pessoa.Email, Pessoa.Data_Nascimento, Pessoa.Endereco
            FROM Pessoa
            JOIN Cliente ON Pessoa.id = Cliente.pessoa_id
            WHERE Pessoa.CPF = ?
        ''', (cpf_ou_cnpj,))
        
        usuario = cursor.fetchone()
        # Se não encontrar pelo CPF, buscar pelo CNPJ
        if usuario==None:
            print(cpf_ou_cnpj)
            cursor.execute('''
                SELECT Pessoa.id, Pessoa.Nome, Cliente.CNPJ, Pessoa.Telefone, Pessoa.Email, Pessoa.Data_Nascimento, Pessoa.Endereco
                FROM Pessoa
                JOIN Cliente ON Pessoa.id = Cliente.pessoa_id
                WHERE Cliente.CNPJ = ?
            ''', (cpf_ou_cnpj,))

    except Exception as e:
        print(f"Erro: {e}")
        
    finally:
        conn.close()

    if usuario:
        return {
            'id': usuario[0],
            'nome': usuario[1],
            'cpf_ou_cnpj': usuario[2],
            'telefone': usuario[3],
            'email': usuario[4],
            'data_nascimento': usuario[5],
            'endereco': usuario[6],
        }
    
    return None


def adicionarFuncionario(cpf, endereco, Data_Nascimento, email, telefone, nome, senha):
    conn = connect_to_db()
    cursor = conn.cursor()
    cargo = 'funcionario'
    status = 'ativo'
    usuarioIdP = ''
    try:
        cursor.execute('INSERT INTO Pessoa (cpf, endereco, Data_Nascimento, email, telefone, nome) VALUES (?, ?, ?, ?, ?, ?)', (cpf, endereco, Data_Nascimento, email, telefone, nome))
        usuarioIdP = cursor.lastrowid
        cursor.execute('INSERT INTO Usuario (senha, cargo, status, pessoa_id) VALUES (?, ?, ?, ?)', (senha, cargo, status, usuarioIdP))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Erro: {e}")
    finally:
        conn.close()

def adicionarCliente(cpf, cnpj, endereco, Data_Nascimento, email, telefone, nome, numero_cnh, tipo_cnh):
    conn = connect_to_db()
    cursor = conn.cursor()
    usuarioIdP = ''
    try:
        cursor.execute('INSERT INTO Pessoa (cpf, endereco, Data_Nascimento, email, telefone, nome) VALUES (?, ?, ?, ?, ?, ?)', (cpf, endereco, Data_Nascimento, email, telefone, nome))
        usuarioIdP = cursor.lastrowid
        cursor.execute('INSERT INTO Cliente (CNPJ, Numero_CNH, Tipo_CNH, pessoa_id) VALUES (?, ?, ?, ?)', (cnpj, numero_cnh, tipo_cnh, usuarioIdP))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Erro: {e}")
    finally:
        conn.close()

def atualizaFuncionario(cpf1, endereco, Data_Nascimento, email, telefone, nome, senha, status, cpf2):
    conn = connect_to_db()
    cursor = conn.cursor()
    cargo = 'funcionario'

    cursor.execute("SELECT id FROM Pessoa WHERE cpf = ?", (cpf2,))
    row = cursor.fetchone()
    if row:
        row_id = row[0]

    try:
        cursor.execute('UPDATE Pessoa SET cpf = ?, endereco = ?, data_nascimento = ?, email = ?, telefone = ?, nome = ? WHERE cpf = ?', (cpf1, endereco, Data_Nascimento, email, telefone, nome, cpf2))
        
        if senha:

            cursor.execute('UPDATE Usuario SET senha = ?, cargo = ?, status = ? WHERE pessoa_id = ?', (senha, cargo, status, row_id))

        else:
            cursor.execute('UPDATE Usuario SET cargo = ?, status = ? WHERE pessoa_id = ?', (cargo, status, row_id))

        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"Erro: {e}")
    finally:
        conn.close()

def atualizaCliente(cpf, cnpj, endereco, Data_Nascimento, email, telefone,nome, numero_cnh, tipo_cnh, cpf_cnpj_original):
    conn = connect_to_db()
    cursor = conn.cursor()

    if len(cpf_cnpj_original)==14:

        cursor.execute("SELECT id FROM Pessoa WHERE cpf = ?", (cpf_cnpj_original,))
        row = cursor.fetchone()
        if row:
            row_id = row[0]
        cnpj=''
    else:
        cursor.execute("SELECT pessoa_id FROM Cliente WHERE CNPJ = ?", (cpf_cnpj_original,))
        row = cursor.fetchone()
        if row:
            row_id = row[0]
        cpf=''

    try:
        cursor.execute('UPDATE Pessoa SET cpf = ?, endereco = ?, data_nascimento = ?, email = ?, telefone = ?, nome = ? WHERE id = ?', (cpf, endereco, Data_Nascimento, email, telefone, nome, row_id))
        cursor.execute('UPDATE Cliente SET CNPJ = ?, Tipo_CNH = ?, Numero_CNH = ? WHERE pessoa_id = ?', (cnpj,tipo_cnh, numero_cnh, row_id))
        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"Erro: {e}")
    finally:
        conn.close()

def verificaCpf(cpf):
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM Pessoa WHERE cpf = ?", (cpf,))
    row = cursor.fetchone()
    if row:
        return True

    return False

def verificaCpf_Cnpj(informacao):
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM Pessoa WHERE cpf = ?", (informacao,))
    row = cursor.fetchone()
    if row:
        return True
    
    cursor.execute("SELECT pessoa_id FROM Cliente WHERE CNPJ = ?", (informacao,))
    row = cursor.fetchone()
    if row:
        return True

    return False

def filtro_funcionarios(informação):
    conn = connect_to_db()
    cursor = conn.cursor()

    if informação=='':
        cursor.execute('''SELECT Pessoa.id, Pessoa.CPF, Pessoa.Endereco, Pessoa.Data_Nascimento, Pessoa.Email, Pessoa.Telefone, Pessoa.Nome, Usuario.Status 
                    FROM Pessoa 
                    JOIN Usuario ON Pessoa.id = Usuario.pessoa_id 
                    ''',)

    elif re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', informação):

        cursor.execute('''SELECT Pessoa.id, Pessoa.CPF, Pessoa.Endereco, Pessoa.Data_Nascimento, Pessoa.Email, Pessoa.Telefone, Pessoa.Nome, Usuario.Status 
                    FROM Pessoa 
                    JOIN Usuario ON Pessoa.id = Usuario.pessoa_id 
                    WHERE Pessoa.CPF LIKE ?''', ('%' + informação + '%',))

    else:

        cursor.execute('''SELECT Pessoa.id, Pessoa.CPF, Pessoa.Endereco, Pessoa.Data_Nascimento, Pessoa.Email, Pessoa.Telefone, Pessoa.Nome, Usuario.Status 
                    FROM Pessoa 
                    JOIN Usuario ON Pessoa.id = Usuario.pessoa_id 
                    WHERE Pessoa.Nome LIKE ?''', ('%' + informação + '%',))
    
    funcionariosRaw = cursor.fetchall()
    funcionarios = []
    colunas = ["id", "CPF", "Endereco", "Data_Nascimento", "Email", "Telefone", "Nome", "Status"]
    for i in funcionariosRaw:
        funcionario = {}
        for index,j in enumerate(i):
            funcionario[colunas[index]] = j
        if funcionario['CPF'] != 'admin':
            funcionarios.append(funcionario)
    conn.close()
    
    return funcionarios

def filtro_clientes(informação):
    conn = connect_to_db()
    cursor = conn.cursor()

    if informação=='':
        cursor.execute('''
                    SELECT Pessoa.id, Pessoa.CPF, Pessoa.Endereco, Pessoa.Data_Nascimento, Pessoa.Email, Pessoa.Telefone, Pessoa.Nome, Cliente.Numero_CNH, Cliente.Tipo_CNH, Cliente.CNPJ
                    FROM Pessoa
                    JOIN Cliente ON Pessoa.id = Cliente.pessoa_id
                    ''',)

    elif re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$|^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$', informação):

        cursor.execute('''
                    SELECT Pessoa.id, Pessoa.CPF, Pessoa.Endereco, Pessoa.Data_Nascimento, Pessoa.Email, Pessoa.Telefone, Pessoa.Nome, Cliente.Numero_CNH, Cliente.Tipo_CNH, Cliente.CNPJ
                    FROM Pessoa
                    JOIN Cliente ON Pessoa.id = Cliente.pessoa_id
                    WHERE Pessoa.CPF LIKE ? OR Cliente.CNPJ LIKE ?
                ''', ('%' + informação + '%', '%' + informação + '%'))

    else:

        cursor.execute('''SELECT Pessoa.id, Pessoa.CPF, Pessoa.Endereco, Pessoa.Data_Nascimento, Pessoa.Email, Pessoa.Telefone, Pessoa.Nome, Cliente.Numero_CNH, Cliente.Tipo_CNH, Cliente.CNPJ
                    FROM Pessoa 
                    JOIN Cliente ON Pessoa.id = Cliente.pessoa_id 
                    WHERE Pessoa.Nome LIKE ?''', ('%' + informação + '%',))
    
    
    clientesRaw = cursor.fetchall()

    clientes = []
    colunas = ["id", "CPF", "Endereco", "Data_Nascimento", "Email", "Telefone", "Nome", "Numero_CNH", "Tipo_CNH", "CNPJ"]
    for i in clientesRaw:
        cliente = {}
        for index,j in enumerate(i):
            cliente[colunas[index]] = j
        clientes.append(cliente)
    conn.close()
    
    return clientes

def obterCPF(id):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    cpf_original = cursor.execute("SELECT CPF FROM Pessoa WHERE id = ?", (id,)).fetchone()
    conn.close()
    return cpf_original

def obterCPF_CNPJ(id):

    conn = connect_to_db()
    cursor = conn.cursor()
    
    resultado = cursor.execute("SELECT CPF FROM Pessoa WHERE id = ?", (id,)).fetchone()
    if resultado[0]=='':
        resultado = cursor.execute("SELECT Cliente.CNPJ FROM Cliente WHERE Cliente.pessoa_id = ?", (id,)).fetchone()

    conn.close()
    return resultado

def buscaCarros(*args):
    conn = connect_to_db()
    cursor = conn.cursor()

    if (len(args) == 6):
        placa = args[0]
        modelo = args[1]
        marca = args[2]
        ano = args[3]
        cor = args[4]
        valorLocacaoDia = args[5]

        cursor.execute("""SELECT id,Ano_Aquisicao,Placa,RENAVAM,Modelo,Marca,Ano_Fabricacao,Cor,Tipo_Combustivel,
                    Valor_Locacao_Dia,Status FROM Veiculo WHERE Placa LIKE ? AND Modelo LIKE ? AND
                    Marca LIKE ? AND Ano_Fabricacao LIKE ? AND Cor LIKE ? AND Valor_Locacao_Dia LIKE ?""",
                    ('%' + placa + '%','%' + modelo + '%','%' + marca + '%', '%' + ano + '%', '%' + cor + '%','%' + valorLocacaoDia + '%',))
        veiculosRaw = cursor.fetchall()
        
        veiculos = []
        colunas = ["id","Ano_Aquisicao","Placa","RENAVAM","Modelo","Marca","Ano_Fabricacao","Cor","Tipo_Combustivel","Valor_Locacao_Dia","Status"]
        for i in veiculosRaw:
            veiculo = {}
            for index,j in enumerate(i):
                veiculo[colunas[index]] = j
            veiculos.append(veiculo)
        conn.close()
        return veiculos
    
    else:
        id = args[0]
        cursor.execute("SELECT * FROM Veiculo WHERE id = ?", (id,))
        veiculo = cursor.fetchone()
        return veiculo

def buscaCliente(informação):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT Pessoa.id, Pessoa.CPF, Pessoa.Endereco, Pessoa.Data_Nascimento, Pessoa.Email, Pessoa.Telefone, Pessoa.Nome, Cliente.Numero_CNH, Cliente.Tipo_CNH, Cliente.CNPJ
            FROM Pessoa 
            JOIN Cliente ON Pessoa.id = Cliente.pessoa_id 
            WHERE Pessoa.Nome LIKE ?''', ('%' + informação + '%',))
    resultados = [row[6] for row in cursor.fetchall()]
    conn.close()
    return resultados

def adicionarLocacao(LocalDevolucao,DataHoraLocacao,DataHoraPrevDevolucao,Valor,id_cliente,id_veiculo,Condicoes_Veiculo,Desconto,Multa,Status):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO Locacao (Local_Devolucao,Data_Hora_Locacao,Data_Hora_Prevista_Devolucao,Valor,id_cliente,id_veiculo,Condicoes_Veiculo,Desconto,Multa,Status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (LocalDevolucao,DataHoraLocacao,DataHoraPrevDevolucao,Valor,id_cliente,id_veiculo,Condicoes_Veiculo,Desconto,Multa,Status))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Erro: {e}")
    finally:
        conn.close()

def buscaLocacao():
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("""SELECT Locacao.id, Locacao.Local_Devolucao, Locacao.Data_Hora_Locacao, Locacao.Data_Hora_Prevista_Devolucao, Locacao.Valor, Locacao.id_cliente, Locacao.id_veiculo, Locacao.Condicoes_Veiculo, Locacao.Desconto, Locacao.Multa, Locacao.Status, 
                   Pessoa.Nome, Veiculo.Modelo, Veiculo.Valor_Locacao_Dia, Locacao.Local_devolucao
                   FROM Locacao
                   JOIN Pessoa ON Locacao.id_cliente = Pessoa.id 
                   JOIN Cliente ON Locacao.id_cliente = Cliente.pessoa_id
                   JOIN Veiculo ON Locacao.id_veiculo = Veiculo.id
                   WHERE Locacao.Status='Ativo'""")
    locacaoRaw = cursor.fetchall()

    locacoes = []
    colunas = ["id","Local_Devolucao","Data_Hora_Locacao","Data_Hora_Prevista_Devolucao","Valor","id_cliente","id_veiculo","Condicoes_Veiculo","Desconto","Multa","Status","Nome","Modelo", "Diaria", "LocalDevolucao"]

    for i in locacaoRaw:
        locacao = {}
        for index,j in enumerate(i):
            locacao[colunas[index]] = j
        locacao['data_locacao'] = locacao['Data_Hora_Locacao'].split(' ')[0]
        locacao['hora_locacao'] = locacao['Data_Hora_Locacao'].split(' ')[1]
        locacao['data_devolucao'] = locacao['Data_Hora_Prevista_Devolucao'].split(' ')[0]
        locacao['hora_devolucao'] = locacao['Data_Hora_Prevista_Devolucao'].split(' ')[1]
        locacoes.append(locacao)
    print(locacoes)

    conn.close()
    return locacoes

def obterLocacao(id_locacao):

    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("""
                        SELECT 
                            id,
                            DATE(Data_Hora_Locacao) AS Data_Locacao,
                            TIME(Data_Hora_Locacao) AS Hora_Locacao,
                            DATE(Data_Hora_Prevista_Devolucao) AS Data_Prevista_Devolucao,
                            TIME(Data_Hora_Prevista_Devolucao) AS Hora_Prevista_Devolucao,
                            Valor,
                            Desconto,
                            Multa
                        FROM Locacao
                        WHERE id == ?
                    """, (id_locacao,))

    locacao = cursor.fetchone()
    conn.close()

    if locacao:
        return {
            'id': locacao[0],
            'Data_Locacao': locacao[1],
            'Hora_Locacao': locacao[2],
            'Data_Prevista_Devolucao': locacao[3],
            'Hora_Prevista_Devolucao': locacao[4],
            'Valor': locacao[5],
            'Desconto': locacao[6],
            'Multa': locacao[7]
        }
    else:
        return None


def obterDiariaVeiculo(id_locacao):

    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("""
                        SELECT 
                            Valor_Locacao_Dia
                        FROM Locacao join Veiculo
                        ON Locacao.id_veiculo = veiculo.id WHERE Locacao.id = ?
                    """, (id_locacao,))

    valor_diaria = float((cursor.fetchone()[0]).replace("R$", "").replace(",", "."))
    #arrumar depois que o valor de veiculo for corrigido
    #valor_diaria = cursor.fetchone()[0]
    conn.close()
    if valor_diaria:
        return valor_diaria
    else:
        return None

def criaDevolucao(dataHoraDevolucao, multa, valorTotal, localDevolucao, condicoes, id_locacao):
    
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO Devolucao (Data_Hora_Devolucao, Multa, Local_devolucao, Valor_Total, Condicoes_Veiculo, id_locacao) VALUES (?, ?, ?, ?, ?, ?)', (dataHoraDevolucao, multa,localDevolucao, valorTotal, condicoes, id_locacao))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Erro: {e}")
    finally:
        conn.close()

def verificarDevolucao(id_locacao):
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("""
                        SELECT 
                            id
                        FROM Devolucao
                        WHERE id_locacao = ?
                    """, (id_locacao,))

    devolucao = cursor.fetchall()

    conn.close()

    if devolucao:
        return True
    else:
        return False

def obterDevolucao(id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Devolucao WHERE id = ?",(id))
    devolucaoRaw = cursor.fetchall()
    devolucoes = []
    colunas = ['id','Data_Hora_Devolucao','Multa','Local_devolucao','Valor_Total','Condicoes_Veiculo','id_locacao']
    for i in devolucaoRaw:
        devolucao = {}
        for index,j in enumerate(i):
            devolucao[colunas[index]] = j
        devolucao['data_devolucao'] = devolucao['Data_Hora_Devolucao'].split(' ')[0]
        devolucao['hora_devolucao'] = devolucao['Data_Hora_Devolucao'].split(' ')[1]
        devolucoes.append(devolucao)
    return devolucoes
def atualizaDevolucao(id_devolucao,dataHoraDevolucao,multa,localDevolucao,valorTotal,condicoes):
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE Devolucao SET Data_Hora_Devolucao = ?, Multa = ?, Local_devolucao = ?, Valor_Total = ?, Condicoes_Veiculo = ? WHERE id = ?', (dataHoraDevolucao,multa,localDevolucao,valorTotal,condicoes,id_devolucao))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Erro: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Cria o banco de dados e as tabelas
    connect_to_db()
    print("Banco de dados criado com sucesso!")
