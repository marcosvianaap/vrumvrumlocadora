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
    print('ADMIN:',admin)
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
        SELECT Usuario.Senha
        FROM Pessoa
        JOIN Usuario ON Pessoa.id = Usuario.pessoa_id
        WHERE Pessoa.CPF = ?
    ''', (formulario['usuario'],))
    senha = cursor.fetchone()
    conn.close()

    #usuario nao existe
    if not senha:
        return False

    if check_password_hash(senha[0], formulario["senha"]):
        return True    

    return False


def buscarUsuarioPorCPF(cpf):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT Pessoa.id, Pessoa.Nome, Pessoa.CPF, Pessoa.Telefone, Pessoa.Email, Pessoa.Data_Nascimento, Pessoa.Endereco, Usuario.Status
            FROM Pessoa
            JOIN Usuario ON Pessoa.id = Usuario.pessoa_id
            WHERE Pessoa.CPF = ?
        ''', (cpf,))
        
        usuario = cursor.fetchone()

    except Exception as e:
        print(f"Erro: {e}")
        
    finally:
        conn.close()
    
    if usuario:
        return {
            'id': usuario[0],
            'nome': usuario[1],
            'cpf': usuario[2],
            'telefone': usuario[3],
            'email': usuario[4],
            'data_nascimento': usuario[5],
            'endereco': usuario[6],
            'status': usuario[7]
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
        print("Usuário adicionado com sucesso!")
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
        print("Cliente adicionado com sucesso!")
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

    if len(cpf_cnpj_original)==11:

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

    if informação.isnumeric() :

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

    if informação.isnumeric() :

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

    print(clientesRaw)
    clientes = []
    colunas = ["id", "CPF", "Endereco", "Data_Nascimento", "Email", "Telefone", "Nome", "Numero_CNH", "Tipo_CNH", "CNPJ"]
    for i in clientesRaw:
        cliente = {}
        for index,j in enumerate(i):
            cliente[colunas[index]] = j
        clientes.append(cliente)
    conn.close()

    print(clientes)
    
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

def buscaCarros(placa,modelo,marca,cor,valorLocacaoDia,ano):
    conn = connect_to_db()
    cursor = conn.cursor()

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
                    """, (2,))

    valor_diaria = float((cursor.fetchone()[0]).replace("R$", "").replace(",", "."))
    #arrumar depois que o valor de veiculo for corrigido
    #valor_diaria = cursor.fetchone()[0]
    conn.close()
    print(valor_diaria)
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
        print("Devolucao adicionada com sucesso!")
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

    print(devolucao)
    if devolucao:
        return True
    else:
        return False