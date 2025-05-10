import sqlite3

DB_NAME = "pacientes.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT UNIQUE NOT NULL,
            nascimento TEXT,
            genero TEXT,
            foto BLOB
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pagamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            valor REAL NOT NULL,
            forma TEXT NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY(paciente_id) REFERENCES pacientes(id)
        )
    """)

    conn.commit()
    conn.close()
