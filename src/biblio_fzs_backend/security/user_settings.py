from fastapi import Depends
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from biblio_fzs_backend.database import get_session
from biblio_fzs_backend.models.models import Funcionario

SECRET_KEY = "SECRET"

bearer_funcionario_transport = BearerTransport(tokenUrl="/funcionarios/auth/jwt/login")


def get_jwt_strategy():
    return JWTStrategy(
        secret=SECRET_KEY, lifetime_seconds=3600, algorithm="HS256"
    )


async def get_funcionario_db(session: AsyncSession = Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, Funcionario)


auth_funcionario_backend = AuthenticationBackend(
    name="jwt", transport=bearer_funcionario_transport, get_strategy=get_jwt_strategy
)
