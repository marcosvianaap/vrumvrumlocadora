import sqlite3
import os

#coisas relacionadas com a estrutura do BD
def connect_to_db():

    conn = sqlite3.connect('banco.db')
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

