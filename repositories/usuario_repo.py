from typing import Optional
from models.usuario_model import Usuario
from sql.usuario_sql import *
from util.auth import conferir_senha
from util.db import obter_conexao


class UsuarioRepo:
    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_DELETAR_TABELA)
            cursor.execute(SQL_CRIAR_TABELA)

    @classmethod
    def inserir(cls, usuario: Usuario) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(SQL_INSERIR_USUARIO,
                (usuario.nome,
                 usuario.email,
                 usuario.cpf,
                 usuario.data_nascimento,
                 usuario.senha,
                 usuario.carteira))
            return resultado.rowcount > 0
        
    @classmethod
    def atualizar_dados(cls, nome: str, email: str, telefone: str) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(
                SQL_ATUALIZAR_DADOS, (nome, email, telefone, email))
            return resultado.rowcount > 0
    
    @classmethod
    def atualizar_senha(cls, email: str, senha: str) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(
                SQL_ATUALIZAR_SENHA, (senha, email))
            return resultado.rowcount > 0
        
    @classmethod
    def atualizar_carteira(cls, id: int, carteira: str) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(
                SQL_ATUALIZAR_CARTEIRA, (carteira, id))
            return resultado.rowcount > 0
        
    @classmethod
    def obter_id(cls, email: str) -> Optional[int]:
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_OBTER_ID, (email,))
            resultado = cursor.fetchone()
            
            if resultado:
                return resultado[0]  
            return None  
      
    @classmethod
    def checar_credenciais(cls, email: str, senha: str) -> Optional[tuple]:
        with obter_conexao() as db:
            cursor = db.cursor()
            dados = cursor.execute(
                SQL_CHECAR_CREDENCIAIS, (email,)).fetchone()
            if dados:
                if conferir_senha(senha, dados[3]):
                    return (dados[0], dados[1], dados[2])
            return None
    
    @classmethod
    def excluir_usuario(cls, email: str) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            resultado = cursor.execute(
                SQL_EXCLUIR_USUARIO, (email,))
            return resultado.rowcount > 0    