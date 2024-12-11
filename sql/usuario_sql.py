SQL_DELETAR_TABELA = """
    DROP TABLE IF EXISTS usuario
"""

SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    nome TEXT NOT NULL, 
    email TEXT NOT NULL UNIQUE,
    cpf TEXT NOT NULL UNIQUE,
    data_nascimento TEXT NOT NULL UNIQUE, 
    senha TEXT NOT NULL,
    carteira TEXT DEFAULT NULL UNIQUE )
"""

SQL_INSERIR_USUARIO = """
    INSERT INTO usuario 
    (nome, email, cpf, data_nascimento, senha, carteira)
    VALUES (?, ?, ?, ?, ?, ?)
"""


SQL_CHECAR_CREDENCIAIS = """
    SELECT nome, email, carteira, senha
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

SQL_ATUALIZAR_CARTEIRA = """
    UPDATE usuario
    SET carteira = ?
    WHERE id = ?
"""

SQL_OBTER_ID = """
    SELECT id 
    FROM usuario 
    WHERE email = ?
"""

SQL_EXCLUIR_USUARIO = """
    DELETE FROM usuario
    WHERE email = ?
"""