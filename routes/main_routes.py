import secrets
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from models.carteira_model import Carteira
from models.usuario_model import Usuario
from repositories.carteira_repo import CarteiraRepo
from repositories.usuario_repo import UsuarioRepo
from util.auth import NOME_COOKIE_AUTH, criar_token, obter_hash_senha


router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_root(request: Request):
    usuario = request.state.usuario if hasattr(request.state, "usuario") else None
    if not usuario or not usuario.email:
        return RedirectResponse("/conecte-se", status_code=status.HTTP_303_SEE_OTHER)        
    else:
        return RedirectResponse("/usuario", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/conecte-se")
async def get_entrar(request: Request):
    return templates.TemplateResponse("pages/conecte-se.html", {"request": request})

@router.post("/post_login")
async def post_entrar(
    email: str = Form(...), 
    senha: str = Form(...)):
    usuario = UsuarioRepo.checar_credenciais(email, senha)
    if usuario is None:
        response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
        return response
    token = criar_token(usuario[0], usuario[1], usuario[2])
    response = RedirectResponse(f"/usuario/", status_code=status.HTTP_303_SEE_OTHER)    
    response.set_cookie(
        key=NOME_COOKIE_AUTH,
        value=token,
        max_age=3600*24*365*10,
        httponly=True,
        samesite="lax"
    )
    return response

@router.get("/cadastre-se")
async def get_cadastrar(request: Request):
    return templates.TemplateResponse("pages/cadastre-se.html", {"request": request})

@router.post("/post_cadastrar")
async def post_cadastrar(
    nome: str = Form(...),
    email: str = Form(...),
    cpf: str = Form(...),
    data_nascimento: str = Form(...),
    senha: str = Form(...),
    confsenha: str = Form(...)):
    if senha != confsenha:
        return RedirectResponse("/cadastrar", status_code=status.HTTP_303_SEE_OTHER)
    print("oi")
    senha_hash = obter_hash_senha(senha)
    carteira_hash = secrets.token_hex(16)
    usuario = Usuario(None, nome, email, cpf, data_nascimento, senha_hash, None)
    UsuarioRepo.inserir(usuario)
    usuario_id = UsuarioRepo.obter_id(email)
    carteira = Carteira(carteira_hash, usuario_id, saldo_fiat=0, saldos={})
    CarteiraRepo.inserir(carteira)
    UsuarioRepo.atualizar_carteira(usuario_id, carteira_hash)
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/sair")
async def get_sair():
    response = RedirectResponse("/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    response.set_cookie(
        key=NOME_COOKIE_AUTH,
        value="",
        max_age=1,
        httponly=True,
        samesite="lax")
    return response    