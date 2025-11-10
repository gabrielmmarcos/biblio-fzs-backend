from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession

from biblio_fzs_backend.models.models import Funcionario
from biblio_fzs_backend.schemas.users_schemas import UserPublic
from biblio_fzs_backend.security.user_settings import auth_backend
from biblio_fzs_backend.database import get_session
from biblio_fzs_backend.services.user_service import (
    UserService,
    get_user_repository,
    get_user_by_id_service
)

fastapi_users = FastAPIUsers[Funcionario, int](get_user_repository, [auth_backend])

router = APIRouter(prefix="/users", tags=["users"])
T_UserManager = Annotated[UserService, Depends(get_user_repository)]


@router.get("/get_by_id/{id}", response_model=UserPublic)
async def get_users_by_id(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await get_user_by_id_service(id, session)
