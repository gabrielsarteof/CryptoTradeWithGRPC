import dotenv
import threading
from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from repositories.carteira_repo import CarteiraRepo
from repositories.transacao_repo import TransacaoRepo
from repositories.usuario_repo import UsuarioRepo
from routes.main_routes import router as main_router
from routes.usuario_routes import router as usuario_router
from util.auth import checar_autenticacao, checar_autorizacao
from util.exceptions import configurar_excecoes
from grpc_server import serve as serve_grpc 

UsuarioRepo.criar_tabela()
CarteiraRepo.criar_tabela()
TransacaoRepo.criar_tabela()

dotenv.load_dotenv()

app = FastAPI(dependencies=[Depends(checar_autorizacao)])
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")

app.middleware("http")(checar_autenticacao)

configurar_excecoes(app)

app.include_router(main_router)
app.include_router(usuario_router)

def run_grpc_server():
    serve_grpc()

grpc_thread = threading.Thread(target=run_grpc_server, daemon=True)
grpc_thread.start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)