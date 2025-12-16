from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession

from biblio_fzs_backend.database import get_session
from biblio_fzs_backend.models.models import Funcionario
from biblio_fzs_backend.schemas.exemplares_schemas import ExemplarSchema, ExemplarResponse

from biblio_fzs_backend.security.user_settings import auth_funcionario_backend
from biblio_fzs_backend.services.funcionario_service import (
    get_funcionario_repository,
)
from biblio_fzs_backend.services.exemplar_service import create_exemplar_service, get_exemplar_by_id_acervo_service, get_all_exemplar_service

fastapi_users = FastAPIUsers[Funcionario, int](get_funcionario_repository, [auth_funcionario_backend])

T_CurrentFuncionario = Annotated[Funcionario, Depends(fastapi_users.current_user())]

router = APIRouter(prefix="/exemplares", tags=["exemplares"])

@router.post("/{id_acervo}", response_model=ExemplarResponse)
async def create_exemplar(
    id_acervo: int,
    exemplar: ExemplarSchema,
    session: AsyncSession = Depends(get_session)
):
    return await create_exemplar_service(id_acervo, exemplar, session)


@router.get("/{id_acervo}", response_model=list[ExemplarResponse])
async def get_exemplar_by_id_acervo(
    id_acervo: int,
    session: AsyncSession = Depends(get_session)
):
    return await get_exemplar_by_id_acervo_service(id_acervo, session)


@router.get("/all/", response_model=list[ExemplarResponse])
async def get_all_exemplar(
    session: AsyncSession = Depends(get_session)
):
    return await get_all_exemplar_service(session)