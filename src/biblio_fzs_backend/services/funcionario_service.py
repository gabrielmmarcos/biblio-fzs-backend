from fastapi import Depends
from fastapi_users import (
    BaseUserManager,
    IntegerIDMixin,
    InvalidPasswordException,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from biblio_fzs_backend.models.models import Funcionario
from biblio_fzs_backend.schemas.users_schemas import FuncionarioUpdate
from biblio_fzs_backend.security.user_settings import get_funcionario_db

SECRET_KEY = "SECRET"


class FuncionarioService(IntegerIDMixin, BaseUserManager[Funcionario, int]):
    verification_token_secret = SECRET_KEY
    reset_password_token_secret = SECRET_KEY

    @classmethod
    async def validate_password(
        self,
        password: str,
        user: Funcionario,
    ) -> None:
        MIN_LENGTH_PASSWORD = 5
        if len(password) < MIN_LENGTH_PASSWORD:
            raise InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Password should not contain e-mail"
            )

    async def get_by_id(self, id: int):
        user_db: SQLAlchemyUserDatabase = self.user_db
        users = await user_db.session.scalars(
            select(user_db.user_table).where(
                user_db.user_table.id == id
            )
        )
        return users


async def get_funcionario_repository(user_db=Depends(get_funcionario_db)):
    yield FuncionarioService(user_db)


async def get_funcionario_by_id_service(id: int, session: AsyncSession):
    return session.scalar(select(Funcionario).where(Funcionario.id == id))


async def update_funcionario_service(funcionario: FuncionarioUpdate,
                                     current_user: Funcionario,
                                     session: AsyncSession):
    for key, value in funcionario.model_dump(exclude_unset=True).items():
        setattr(current_user, key, value)

    session.add(current_user)
    await session.commit()
    await session.refresh(current_user)
    return current_user
