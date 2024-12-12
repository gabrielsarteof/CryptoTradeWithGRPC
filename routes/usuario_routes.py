import grpc
import service_pb2
import service_pb2_grpc
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import httpx

router = APIRouter(prefix="/usuario")

templates = Jinja2Templates(directory="templates")

channel = grpc.insecure_channel('localhost:50051')
stub = service_pb2_grpc.CryptoServiceStub(channel)

@router.get("/")
async def get_usuario(request: Request, colaboradores_message: str = None):
    carteira_id = request.state.usuario.carteira
    response = stub.GetUserInfo(service_pb2.UserInfoRequest(carteira_id=carteira_id))
    
    moedas = [
        {
            "nome": moeda.nome,
            "quantidade": moeda.quantidade,
            "imagem": moeda.imagem
        }
        for moeda in response.moedas
    ]

    transacoes_formatadas = [
        {
            "moeda": transacao.moeda,
            "imagem": transacao.imagem,
            "quantidade": transacao.quantidade,
            "data": transacao.data
        }
        for transacao in response.transacoes
    ]

    return templates.TemplateResponse(
        "pages/usuario/index.html",
        {
            "request": request,
            "moedas": moedas,
            "transacoes": transacoes_formatadas,
            "colaboradores_message": colaboradores_message
        }
    )

@router.get("/comprar_cripto", response_class=HTMLResponse)
async def get_comprar_cripto(request: Request):
    coingecko_url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": "false"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(coingecko_url, params=params)
            response.raise_for_status()
            moedas = response.json()
        lista_moedas = [
            {"id": moeda["id"], "nome": moeda["name"], "preco": moeda["current_price"]}
            for moeda in moedas
        ]
    except Exception as e:
        print(f"Erro ao buscar dados da API: {e}")
        lista_moedas = []

    return templates.TemplateResponse(
        "pages/usuario/comprar_cripto.html",
        {"request": request, "moedas": lista_moedas}
    )

@router.post("/post_comprar_cripto")
async def post_comprar_cripto(request: Request):
    form_data = await request.form()
    criptomoeda_id = form_data.get("criptomoeda")
    quantidade = float(form_data.get("quantidade"))
    preco_unitario = float(form_data.get("preco").replace("R$ ", "").replace(",", ".")) / quantidade
    
    carteira_id = request.state.usuario.carteira

    response = stub.BuyCrypto(service_pb2.BuyCryptoRequest(
        carteira_id=carteira_id,
        criptomoeda_id=criptomoeda_id,
        quantidade=quantidade,
        preco_unitario=preco_unitario
    ))

    if response.success:
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse("/usuario/comprar_cripto", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/mostrar_colaboradores")
async def mostrar_colaboradores(request: Request):
    response = stub.MostrarColaboradores(service_pb2.ColaboradoresRequest())
    colaboradores_message = response.message

    return RedirectResponse(
        url=f"/usuario/?colaboradores_message={colaboradores_message}",
        status_code=status.HTTP_303_SEE_OTHER
    )