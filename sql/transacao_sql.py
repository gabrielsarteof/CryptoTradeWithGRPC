SQL_DELETAR_TABELA = """
    DROP TABLE IF EXISTS transacao
"""

SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS transacao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        carteira_id INTEGER NOT NULL,  -- Modificado para carteira_id
        moeda TEXT NOT NULL,
        quantidade REAL NOT NULL,
        preco_unitario REAL NOT NULL,
        valor_total REAL NOT NULL,
        data TEXT NOT NULL,
        tipo TEXT CHECK(tipo IN ('compra', 'venda')) NOT NULL,
        FOREIGN KEY (carteira_id) REFERENCES carteira(id) 
    )
"""

SQL_INSERIR_TRANSACAO = """
    INSERT INTO transacao 
    (carteira_id, moeda, quantidade, preco_unitario, valor_total, data, tipo)
    VALUES (?, ?, ?, ?, ?, ?, ?)
"""

SQL_OBTER_TRANSACOES = """
    SELECT id, carteira_id, moeda, quantidade, preco_unitario, valor_total, data, tipo
    FROM transacao
    WHERE carteira_id = ?  -- Modificado para buscar pela carteira_id
"""

SQL_EXCLUIR_TRANSACAO = """
    DELETE FROM transacao
    WHERE id = ?
"""
