from typing import Optional, Dict
from models.carteira_model import Carteira
from sql.carteira_sql import *
from util.db import obter_conexao

class CarteiraRepo:
    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_DELETAR_TABELA)
            cursor.execute(SQL_CRIAR_TABELA)

    @classmethod
    def inserir(cls, carteira: Carteira) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(SQL_INSERIR_CARTEIRA,
                (carteira.id,
                 carteira.usuario_id,
                 carteira.saldo_fiat,
                 str(carteira.saldos))) 
            return resultado.rowcount > 0

    @classmethod
    def atualizar_saldo(cls, usuario_id: int, saldo_fiat: float, saldos: Dict[str, float]) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(
                SQL_ATUALIZAR_SALDO, 
                (saldo_fiat, str(saldos), usuario_id))  
            return resultado.rowcount > 0

    @classmethod
    def obter_carteira(cls, usuario_id: int) -> Optional[Carteira]:
        with obter_conexao() as db:
            cursor = db.cursor()
            dados = cursor.execute(
                SQL_OBTER_CARTEIRA, (usuario_id,)).fetchone()
            if dados:
                return Carteira(id=dados[0], usuario_id=dados[1], saldo_fiat=dados[2], saldos=eval(dados[3]))
            return None

    @classmethod
    def excluir_carteira(cls, usuario_id: int) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(
                SQL_EXCLUIR_CARTEIRA, (usuario_id,))
            return resultado.rowcount > 0
