import re
import sqlite3
import os

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
            Valor               REAL NOT NULL,
            id_cliente          INTEGER NOT NULL,
            id_veiculo          INTEGER NOT NULL,
            Condicoes_Veiculo   TEXT NOT NULL,
            Desconto            REAL NOT NULL,
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

    #usuario autenticados
    if senha[0] == formulario['senha']:
        return True
    #if bcrypt.check_password_hash(senha[0], formulario["senha"]):
    #    return True    

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

def verificaCpf(cpf):
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM Pessoa WHERE cpf = ?", (cpf,))
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
        funcionarios.append(funcionario)
    conn.close()
    
    return funcionarios

def obterCPF(id):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    cpf_original = cursor.execute("SELECT CPF FROM Pessoa WHERE id = ?", (id,)).fetchone()
    conn.close()
    return cpf_original