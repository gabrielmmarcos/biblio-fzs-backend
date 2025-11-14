import asyncio
from http import HTTPStatus
from sys import platform

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from biblio_fzs_backend.routers.funcionarios import fastapi_users as fastapi_funcionario_users, router as funcionarios_router
from biblio_fzs_backend.routers.alunos import fastapi_users as fastapi_aluno_users, router as alunos_router
from biblio_fzs_backend.schemas.root_schemas import Message
from biblio_fzs_backend.schemas.funcionarios_schemas import FuncionarioPublic, FuncionarioSchema
from biblio_fzs_backend.schemas.alunos_schemas import AlunoPublic, AlunoSchema
from biblio_fzs_backend.security.user_settings import auth_funcionario_backend, auth_aluno_backend

if platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


app = FastAPI(title="Meu Bairro API")
app.include_router(funcionarios_router)
app.include_router(alunos_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[''],
    allow_credentials=True,
    allow_methods=[''],
    allow_headers=['*'],
)

app.include_router(
    fastapi_funcionario_users.get_auth_router(auth_funcionario_backend, requires_verification=False),
    prefix="/funcionarios/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_funcionario_users.get_register_router(FuncionarioPublic, FuncionarioSchema),
    prefix="/funcionarios",
    tags=["funcionarios"],
)
app.include_router(
    fastapi_funcionario_users.get_users_router(
        FuncionarioPublic, FuncionarioSchema, requires_verification=False
    ),
    prefix="/funcionarios",
    tags=["funcionarios"],
)


app.include_router(
    fastapi_aluno_users.get_auth_router(auth_aluno_backend, requires_verification=False),
    prefix="/alunos/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_aluno_users.get_register_router(AlunoPublic, AlunoSchema),
    prefix="/alunos",
    tags=["alunos"],
)
app.include_router(
    fastapi_aluno_users.get_users_router(
        AlunoPublic, AlunoSchema, requires_verification=False
    ),
    prefix="/alunos",
    tags=["alunos"],
)



@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Meu Bairro. Conecte-se com a sua comunidade"}
