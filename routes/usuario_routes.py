from datetime import datetime
import httpx
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.transacao_model import Transacao
from models.usuario_model import Usuario
from repositories.carteira_repo import CarteiraRepo
from repositories.transacao_repo import TransacaoRepo


router = APIRouter(prefix="/usuario")

templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_usuario(request: Request, colaboradores_message: str = None):
    carteira_id = request.state.usuario.carteira  
    carteira = CarteiraRepo.obter_carteira(carteira_id)

    moedas = []
    if carteira and carteira.saldos:
        for moeda, quantidade in carteira.saldos.items():
            moedas.append({
                "nome": moeda,
                "quantidade": quantidade,
                "imagem": f"/static/img/{moeda.lower()}.png"  
            })

    transacoes = TransacaoRepo.obter_transacoes(carteira_id)
    transacoes_formatadas = [
        {
            "moeda": transacao.moeda,
            "imagem": f"/static/img/{transacao.moeda.lower()}.png",
            "quantidade": transacao.quantidade,
            "data": transacao.data
        }
        for transacao in transacoes
    ]
    print (colaboradores_message)
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
    valor_total = float(form_data.get("preco").replace("R$ ", "").replace(",", "."))  

    carteira_id = request.state.usuario.carteira

    meses = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}
    data_criacao = datetime.now()

    data_formatada = f"{data_criacao.day} de {meses[data_criacao.month]} de {data_criacao.year} às {data_criacao.hour}:{data_criacao.minute:02d}"


    transacao = Transacao(
        carteira_id=carteira_id,
        moeda=criptomoeda_id,  
        quantidade=quantidade,
        preco_unitario=preco_unitario,
        valor_total=valor_total,
        data=data_formatada,
        tipo="compra"
    )

    TransacaoRepo.inserir(transacao)

    carteira = CarteiraRepo.obter_carteira(carteira_id)
    
    if carteira:
        saldos = carteira.saldos or {}
        if criptomoeda_id in saldos:
            saldos[criptomoeda_id] += quantidade  
        else:
            saldos[criptomoeda_id] = quantidade  

        print(carteira, "oi")
        print(saldos)

        CarteiraRepo.atualizar_saldo(carteira.usuario_id, carteira.saldo_fiat, saldos)

    response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    return response

@router.get("/mostrar_colaboradores")
async def mostrar_colaboradores(request: Request):
    colaboradores_message = "gabrielsarteof, brunarcedro e cortefacil"

    response = RedirectResponse(
        url=f"/usuario/?colaboradores_message={colaboradores_message}",
        status_code=status.HTTP_303_SEE_OTHER
    )
    return response



