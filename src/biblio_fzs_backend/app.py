import asyncio
from http import HTTPStatus
from sys import platform

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from biblio_fzs_backend.routers.funcionarios import fastapi_users, router
from biblio_fzs_backend.schemas.root_schemas import Message
from biblio_fzs_backend.schemas.users_schemas import FuncionarioPublic, FuncionarioSchema
from biblio_fzs_backend.security.user_settings import auth_funcionario_backend

if platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


app = FastAPI(title="Meu Bairro API")
app.include_router(router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[''],
    allow_credentials=True,
    allow_methods=[''],
    allow_headers=['*'],
)

app.include_router(
    fastapi_users.get_auth_router(auth_funcionario_backend, requires_verification=False),
    prefix="/funcionarios/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(FuncionarioPublic, FuncionarioSchema),
    prefix="/funcionarios",
    tags=["funcionarios"],
)
app.include_router(
    fastapi_users.get_users_router(
        FuncionarioPublic, FuncionarioSchema, requires_verification=False
    ),
    prefix="/funcionarios",
    tags=["funcionarios"],
)


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Meu Bairro. Conecte-se com a sua comunidade"}
