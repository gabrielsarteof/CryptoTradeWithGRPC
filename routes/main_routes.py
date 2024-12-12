import grpc
import service_pb2
import service_pb2_grpc
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from util.auth import NOME_COOKIE_AUTH

router = APIRouter()

templates = Jinja2Templates(directory="templates")

channel = grpc.insecure_channel('localhost:50051')
stub = service_pb2_grpc.CryptoServiceStub(channel)

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
    login_response = stub.Login(service_pb2.LoginRequest(email=email, senha=senha))
    if not login_response.token:
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    response = RedirectResponse("/usuario/", status_code=status.HTTP_303_SEE_OTHER)    
    response.set_cookie(
        key=NOME_COOKIE_AUTH,
        value=login_response.token,
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
    response = stub.Register(service_pb2.RegisterRequest(
        nome=nome,
        email=email,
        cpf=cpf,
        data_nascimento=data_nascimento,
        senha=senha
    ))
    if response.success:
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse("/cadastrar", status_code=status.HTTP_303_SEE_OTHER)

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