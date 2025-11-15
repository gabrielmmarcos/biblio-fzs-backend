from datetime import datetime, date

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, registry

from biblio_fzs_backend.schemas.root_schemas import CargoEnum, TurnoEnum

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
    cep: Mapped[int] = mapped_column(nullable=True, init=True)
    numero_residencia: Mapped[str] = mapped_column(nullable=True, init=False)
    complemento: Mapped[str] = mapped_column(nullable=True, init=False)
    is_verified: Mapped[bool] = mapped_column(default=False, init=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, init=False)
    is_active: Mapped[bool] = mapped_column(default=True, init=False)
    crb: Mapped[str] = mapped_column(nullable=True, unique=True)
    telefone: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), init=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, onupdate=func.now(), server_default=func.now(), init=False
    )


@table_registry.mapped_as_dataclass
class Aluno(SQLAlchemyBaseUserTable[int]):
    __tablename__ = "alunos"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    nome: Mapped[str] = mapped_column(nullable=False)
    sobrenome: Mapped[str] = mapped_column(nullable=False)
    cpf: Mapped[str] = mapped_column(nullable=False)
    cep: Mapped[int] = mapped_column(nullable=True, init=True)
    numero_residencia: Mapped[str] = mapped_column(nullable=True, init=True)
    complemento: Mapped[str] = mapped_column(nullable=True, init=True)
    is_verified: Mapped[bool] = mapped_column(default=False, init=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, init=False)
    is_active: Mapped[bool] = mapped_column(default=True, init=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), init=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, onupdate=func.now(), server_default=func.now(), init=False
    )


@table_registry.mapped_as_dataclass
class Curso:
    __tablename__ = "cursos"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    nome: Mapped[str] = mapped_column(nullable=False)
    periodo: Mapped[TurnoEnum] = mapped_column(nullable=False)
    inicio: Mapped[date] = mapped_column(nullable=False)
    fim: Mapped[date] = mapped_column(nullable=False)
    instituicao: Mapped[str] = mapped_column(nullable=False)


@table_registry.mapped_as_dataclass
class AlunoCurso:
    __tablename__ = "alunos_cursos"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    id_aluno: Mapped[int] = mapped_column(
        ForeignKey('alunos.id', ondelete='CASCADE'), nullable=False
    )
    id_curso: Mapped[int] = mapped_column(
        ForeignKey('cursos.id', ondelete='CASCADE'), nullable=False
    )
    ra: Mapped[str] = mapped_column(nullable=False, unique=True)


@table_registry.mapped_as_dataclass
class Presenca:
    __tablename__ = "presencas"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    datetime_presenca: Mapped[datetime]
    id_aluno: Mapped[int] = mapped_column(
        ForeignKey('alunos.id', ondelete='CASCADE'), nullable=False
    )
