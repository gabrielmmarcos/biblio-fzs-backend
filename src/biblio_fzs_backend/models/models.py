from datetime import datetime

from fastapi_users.db import SQLAlchemyBaseUserTable
from biblio_fzs_backend.schemas.root_schemas import CargoEnum, TurnoEnum

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class Funcionario(SQLAlchemyBaseUserTable[int]):
    __tablename__ = "funcionarios"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    nome: Mapped[str] = mapped_column(nullable=False)
    sobrenome: Mapped[str] = mapped_column(nullable=False)
    cpf: Mapped[str] = mapped_column(nullable=False)
    cargo: Mapped[CargoEnum] = mapped_column(nullable=False)
    turno: Mapped[TurnoEnum] = mapped_column(nullable=False)
    cep: Mapped[int] = mapped_column(nullable=True, init=False)
    numero_residencia: Mapped[str] = mapped_column(nullable=True, init=False)
    complemento: Mapped[str] = mapped_column(nullable=True, init=False)
    is_verified: Mapped[bool] = mapped_column(default=False, init=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, init=False)
    is_active: Mapped[bool] = mapped_column(default=True, init=False)
    crb: Mapped[str] = mapped_column(nullable=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), init=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, onupdate=func.now(), server_default=func.now(), init=False
    )