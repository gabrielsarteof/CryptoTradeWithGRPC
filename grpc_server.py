import grpc
from concurrent import futures
import service_pb2
import service_pb2_grpc
from repositories.usuario_repo import UsuarioRepo
from repositories.carteira_repo import CarteiraRepo
from repositories.transacao_repo import TransacaoRepo
from models.usuario_model import Usuario
from models.carteira_model import Carteira
from models.transacao_model import Transacao
from util.auth import criar_token, obter_hash_senha
import secrets
from datetime import datetime

class CryptoServicer(service_pb2_grpc.CryptoServiceServicer):
    def Login(self, request, context):
        usuario = UsuarioRepo.checar_credenciais(request.email, request.senha)
        if usuario is None:
            return service_pb2.LoginResponse(token="")
        token = criar_token(usuario[0], usuario[1], usuario[2])
        return service_pb2.LoginResponse(token=token)

    def Register(self, request, context):
        senha_hash = obter_hash_senha(request.senha)
        carteira_hash = secrets.token_hex(16)
        usuario = Usuario(None, request.nome, request.email, request.cpf, request.data_nascimento, senha_hash, None)
        UsuarioRepo.inserir(usuario)
        usuario_id = UsuarioRepo.obter_id(request.email)
        carteira = Carteira(carteira_hash, usuario_id, saldo_fiat=0, saldos={})
        CarteiraRepo.inserir(carteira)
        UsuarioRepo.atualizar_carteira(usuario_id, carteira_hash)
        return service_pb2.RegisterResponse(success=True)

    def BuyCrypto(self, request, context):
        transacao = Transacao(
            carteira_id=request.carteira_id,
            moeda=request.criptomoeda_id,
            quantidade=request.quantidade,
            preco_unitario=request.preco_unitario,
            valor_total=request.quantidade * request.preco_unitario,
            data=datetime.now().strftime("%d de %B de %Y às %H:%M"),
            tipo="compra"
        )
        TransacaoRepo.inserir(transacao)
        carteira = CarteiraRepo.obter_carteira(request.carteira_id)
        if carteira:
            saldos = carteira.saldos or {}
            if request.criptomoeda_id in saldos:
                saldos[request.criptomoeda_id] += request.quantidade
            else:
                saldos[request.criptomoeda_id] = request.quantidade
            CarteiraRepo.atualizar_saldo(carteira.usuario_id, carteira.saldo_fiat, saldos)
        return service_pb2.BuyCryptoResponse(success=True)

    def GetUserInfo(self, request, context):
        carteira = CarteiraRepo.obter_carteira(request.carteira_id)
        moedas = []
        if carteira and carteira.saldos:
            for moeda, quantidade in carteira.saldos.items():
                moedas.append(service_pb2.Moeda(
                    nome=moeda,
                    quantidade=quantidade,
                    imagem=f"/static/img/{moeda.lower()}.png"
                ))
        transacoes = TransacaoRepo.obter_transacoes(request.carteira_id)
        transacoes_formatadas = [
            service_pb2.Transacao(
                moeda=transacao.moeda,
                imagem=f"/static/img/{transacao.moeda.lower()}.png",
                quantidade=transacao.quantidade,
                data=transacao.data
            )
            for transacao in transacoes
        ]
        return service_pb2.UserInfoResponse(moedas=moedas, transacoes=transacoes_formatadas)

    def MostrarColaboradores(self, request, context):
        colaboradores_message = "gabrielsarteof, brunarcedro e cortefacil"
        return service_pb2.ColaboradoresResponse(message=colaboradores_message)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_CryptoServiceServicer_to_server(CryptoServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()