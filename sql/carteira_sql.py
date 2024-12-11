SQL_DELETAR_TABELA = """
    DROP TABLE IF EXISTS carteira
"""

SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS carteira (
        id TEXT PRIMARY KEY,
        usuario_id INTEGER NOT NULL,
        saldo_fiat REAL DEFAULT 0,
        saldos TEXT DEFAULT '{}',  
        FOREIGN KEY (usuario_id) REFERENCES usuario(id)
    )
"""

SQL_INSERIR_CARTEIRA = """
    INSERT INTO carteira 
    (id, usuario_id, saldo_fiat, saldos)
    VALUES (?, ?, ?, ?)
"""

SQL_ATUALIZAR_SALDO = """
    UPDATE carteira
    SET saldo_fiat = ?, saldos = ?
    WHERE usuario_id = ?
"""

SQL_OBTER_CARTEIRA = """
    SELECT id, usuario_id, saldo_fiat, saldos
    FROM carteira
    WHERE id = ?
"""

SQL_EXCLUIR_CARTEIRA = """
    DELETE FROM carteira
    WHERE usuario_id = ?
"""
