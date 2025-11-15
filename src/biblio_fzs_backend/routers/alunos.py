from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from biblio_fzs_backend.database import get_session
from biblio_fzs_backend.models.models import Aluno
from biblio_fzs_backend.schemas.alunos_schemas import (
    AlunoPublic,
    AlunoUpdate,
)
from biblio_fzs_backend.security.user_settings import auth_aluno_backend
from biblio_fzs_backend.services.aluno_service import (
    AlunoService,
    get_aluno_by_id_service,
    get_aluno_repository,
    update_aluno_service,
)

fastapi_users = FastAPIUsers[Aluno, int](get_aluno_repository, [auth_aluno_backend])

T_CurrentAluno = Annotated[Aluno, Depends(fastapi_users.current_user())]

router = APIRouter(prefix="/alunos", tags=["alunos"])
T_UserManager = Annotated[AlunoService, Depends(get_aluno_repository)]


@router.get("/get_by_id/{id}/", response_model=AlunoPublic | None)
async def get_aluno_by_id(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    return await get_aluno_by_id_service(id, session)


@router.get("/get_all", response_model=list[AlunoPublic])
async def get_aluno_by_id(
    session: AsyncSession = Depends(get_session)
):
    return await session.scalars(select(Aluno))


@router.patch("/update/me", response_model=AlunoPublic)
async def update_aluno(
    aluno: AlunoUpdate,
    current_user: T_CurrentAluno,
    session: AsyncSession = Depends(get_session),
):
    return await update_aluno_service(aluno, current_user, session)
