from fastapi import Depends
from fastapi_users import (
    BaseUserManager,
    IntegerIDMixin,
    InvalidPasswordException,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from biblio_fzs_backend.models.models import Aluno
from biblio_fzs_backend.schemas.alunos_schemas import AlunoUpdate
from biblio_fzs_backend.security.user_settings import get_aluno_db

SECRET_KEY = "SECRET"


class AlunoService(IntegerIDMixin, BaseUserManager[Aluno, int]):
    verification_token_secret = SECRET_KEY
    reset_password_token_secret = SECRET_KEY

    @classmethod
    async def validate_password(
        self,
        password: str,
        user: Aluno,
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


async def get_aluno_repository(aluno_db=Depends(get_aluno_db)):
    yield AlunoService(aluno_db)


async def get_aluno_by_id_service(id: int, session: AsyncSession):
    return session.scalar(select(Aluno).where(Aluno.id == id))


async def update_aluno_service(funcionario: AlunoUpdate,
                                     current_aluno: Aluno,
                                     session: AsyncSession):
    for key, value in funcionario.model_dump(exclude_unset=True).items():
        setattr(current_aluno, key, value)

    session.add(current_aluno)
    await session.commit()
    await session.refresh(current_aluno)
    return current_aluno
