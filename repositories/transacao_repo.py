from typing import Optional
from models.transacao_model import Transacao
from sql.transacao_sql import *
from util.db import obter_conexao

class TransacaoRepo:
    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_CRIAR_TABELA)

    @classmethod
    def inserir(cls, transacao: Transacao) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(SQL_INSERIR_TRANSACAO,
                (transacao.carteira_id,  
                 transacao.moeda,
                 transacao.quantidade,
                 transacao.preco_unitario,
                 transacao.valor_total,
                 transacao.data,
                 transacao.tipo)) 
            return resultado.rowcount > 0

    @classmethod
    def obter_transacoes(cls, carteira_id: int) -> list[Transacao]:
        with obter_conexao() as db:
            cursor = db.cursor()
            dados = cursor.execute(
                SQL_OBTER_TRANSACOES, (carteira_id,)).fetchall()
            return [Transacao(id=dado[0], 
                              carteira_id=dado[1],  # Modificado para carteira_id
                              moeda=dado[2], 
                              quantidade=dado[3], 
                              preco_unitario=dado[4], 
                              valor_total=dado[5], 
                              data=dado[6], 
                              tipo=dado[7]) for dado in dados]

    @classmethod
    def excluir_transacao(cls, transacao_id: int) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(
                SQL_EXCLUIR_TRANSACAO, (transacao_id,))
            return resultado.rowcount > 0
