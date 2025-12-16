from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession

from biblio_fzs_backend.database import get_session
from biblio_fzs_backend.models.models import Funcionario
from biblio_fzs_backend.schemas.tipos_acervos_schemas import TCCSchema, TCCResponse, PeriodicoSchema, PeriodicoResponse, MultimeoSchemas, MultimeoResponse, ApostilaSchemas, ApostilaResponse, LivroResponse, LivroSchemas

from biblio_fzs_backend.security.user_settings import auth_funcionario_backend
from biblio_fzs_backend.services.funcionario_service import (
    get_funcionario_repository,
)
from biblio_fzs_backend.services.tipos_acervos_service import create_tcc_service, get_all_tccs_service, get_tcc_by_id_acervo_service, create_apostila_service, get_all_apostilas_service, get_apostila_by_id_acervo_service, create_multimeo_service, get_all_multimeos_service, get_multimeo_by_id_acervo_service, create_periodico_service, get_all_periodicos_service, get_periodico_by_id_acervo_service, create_livro_service, get_all_livros_service, get_livro_by_id_acervo_service

fastapi_users = FastAPIUsers[Funcionario, int](get_funcionario_repository, [auth_funcionario_backend])

T_CurrentFuncionario = Annotated[Funcionario, Depends(fastapi_users.current_user())]

router = APIRouter(prefix="/tipos_acervos", tags=["acervos"])

#tcc
@router.post("/{id_acervo}/tcc", response_model=TCCResponse)
async def create_tcc(
    id_acervo: int, tcc: TCCSchema, session: AsyncSession = Depends(get_session)
):
    return await create_tcc_service(id_acervo, tcc, session)


@router.get('/tcc', response_model=list[TCCResponse] | None)
async def get_all_tccs(session: AsyncSession = Depends(get_session)):
    return await get_all_tccs_service(session)


@router.get('/tcc/{id_acervo}', response_model=TCCResponse | None)
async def get_tcc_by_id_acervo(id_acervo: int, session: AsyncSession = Depends(get_session)):
    return await get_tcc_by_id_acervo_service(id_acervo, session)

#periodio
@router.post("/{id_acervo}/periodico", response_model=PeriodicoResponse)
async def create_periodico(
    id_acervo: int, periodico: PeriodicoSchema, session: AsyncSession = Depends(get_session)
):
    return await create_periodico_service(id_acervo, periodico, session)


@router.get('/periodico', response_model=list[PeriodicoResponse] | None)
async def get_all_periodicos(session: AsyncSession = Depends(get_session)):
    return await get_all_periodicos_service(session)


@router.get('/periodico/{id_acervo}', response_model=TCCResponse | None)
async def get_periodico_by_id_acervo(id_acervo: int, session: AsyncSession = Depends(get_session)):
    return await get_periodico_by_id_acervo_service(id_acervo, session)

#multimeo
@router.post("/{id_acervo}/multimeo", response_model=MultimeoResponse)
async def create_multimeo(
    id_acervo: int, multimeo: MultimeoSchemas, session: AsyncSession = Depends(get_session)
):
    return await create_multimeo_service(id_acervo, multimeo, session)


@router.get('/multimeo', response_model=list[MultimeoResponse] | None)
async def get_all_multimeos(session: AsyncSession = Depends(get_session)):
    return await get_all_multimeos_service(session)


@router.get('/multimeo/{id_acervo}', response_model=MultimeoResponse | None)
async def get_multimeo_by_id_acervo(id_acervo: int, session: AsyncSession = Depends(get_session)):
    return await get_multimeo_by_id_acervo_service(id_acervo, session)

#apostila
@router.post("/{id_acervo}/apostila", response_model=ApostilaResponse)
async def create_apostila(
    id_acervo: int, apostila: ApostilaSchemas, session: AsyncSession = Depends(get_session)
):
    return await create_apostila_service(id_acervo, apostila, session)


@router.get('/apostila', response_model=list[ApostilaResponse] | None)
async def get_all_apostilas(session: AsyncSession = Depends(get_session)):
    return await get_all_apostilas_service(session)


@router.get('/apostila/{id_acervo}', response_model=ApostilaResponse | None)
async def get_apostila_by_id_acervo(id_acervo: int, session: AsyncSession = Depends(get_session)):
    return await get_apostila_by_id_acervo_service(id_acervo, session)

#livro
@router.post("/{id_acervo}/livro", response_model=LivroResponse)
async def create_livro(
    id_acervo: int, livro: LivroSchemas, session: AsyncSession = Depends(get_session)
):
    return await create_livro_service(id_acervo, livro, session)


@router.get('/livro', response_model=list[LivroResponse] | None)
async def get_all_livros(session: AsyncSession = Depends(get_session)):
    return await get_all_livros_service(session)


@router.get('/livro/{id_acervo}', response_model=LivroResponse | None)
async def get_livro_by_id_acervo(id_acervo: int, session: AsyncSession = Depends(get_session)):
    return await get_livro_by_id_acervo_service(id_acervo, session)