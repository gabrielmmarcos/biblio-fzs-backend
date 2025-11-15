from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession

from biblio_fzs_backend.database import get_session
from biblio_fzs_backend.models.models import Funcionario
from biblio_fzs_backend.schemas.funcionarios_schemas import (
    FuncionarioPublic,
    FuncionarioUpdate,
    FuncionarioPublic,
)
from biblio_fzs_backend.security.user_settings import auth_funcionario_backend
from biblio_fzs_backend.services.funcionario_service import (
    FuncionarioService,
    get_funcionario_by_id_service,
    get_funcionario_repository,
    update_funcionario_service,
)

fastapi_users = FastAPIUsers[Funcionario, int](get_funcionario_repository, [auth_funcionario_backend])

T_CurrentFuncionario = Annotated[Funcionario, Depends(fastapi_users.current_user())]

router = APIRouter(prefix="/funcionarios", tags=["funcionarios"])
T_UserManager = Annotated[FuncionarioService, Depends(get_funcionario_repository)]


@router.get("/get_by_id/{id}", response_model=FuncionarioPublic)
async def get_users_by_id(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await get_funcionario_by_id_service(id, session)


@router.patch("/update/me", response_model=FuncionarioPublic)
async def update_funcionario(
    funcionario: FuncionarioUpdate,
    current_user: T_CurrentFuncionario,
    session: AsyncSession = Depends(get_session),
):
    return await update_funcionario_service(funcionario, current_user, session)
