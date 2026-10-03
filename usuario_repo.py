import os
import sqlite3

from usuario_model import Usuario
from usuario_sql import *


def get_connection():
    database_path = os.environ.get('TEST_DATABASE_PATH', 'dados.db')
    conexao = sqlite3.connect(database_path)
    conexao.row_factory = sqlite3.Row
    return conexao

def criar_tabela():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(CRIAR_TABELA)
    conn.commit()
    cursor.close()
    return 1

def inserir_usuario(usuario: Usuario):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(INSERIR_USUARIO, (usuario.email,))
    conn.commit()
    cursor.close()
    return cursor.lastrowid

def obter_usuario_por_id(usuario_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(PROUCURAR_USUARIO, (usuario_id,))
    row = cursor.fetchone()
    cursor.close()
    if row:
        return Usuario(id=row['id'], email=row['email'])
    return None

