SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    nome TEXT NOT NULL, 
    email TEXT NOT NULL UNIQUE,
    telefone TEXT NOT NULL UNIQUE, 
    senha TEXT NOT NULL,
    tema TEXT NOT NULL,
    perfil INTEGER NOT NULL)
"""

SQL_INSERIR_USUARIO = """
    INSERT INTO usuario 
    (nome, email, telefone, senha, tema, perfil)
    VALUES (?, ?, ?, ?, "default", ?)
"""


SQL_CHECAR_CREDENCIAIS = """
    SELECT nome, email, perfil, senha
    FROM usuario
    WHERE email = ?
"""

SQL_ATUALIZAR_DADOS = """
    UPDATE usuario
    SET nome = ?, email = ?, telefone = ?
    WHERE email = ?
"""

SQL_ATUALIZAR_SENHA = """
    UPDATE usuario
    SET senha = ?
    WHERE email = ?
"""

SQL_ATUALIZAR_TEMA = """
    UPDATE usuario
    SET tema = ?
    WHERE email = ?
"""

SQL_EXCLUIR_USUARIO = """
    DELETE FROM usuario
    WHERE email = ?
"""