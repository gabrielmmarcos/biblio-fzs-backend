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


@table_registry.mapped_as_dataclass
class Autor:
    __tablename__ = "autores"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    nome: Mapped[str] = mapped_column(nullable=False)


@table_registry.mapped_as_dataclass
class Acervo:
    __tablename__ = "acervos"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    id_autor: Mapped[int] = mapped_column(
        ForeignKey('autores.id', ondelete='CASCADE'), nullable=False
    )
    titulo: Mapped[str] = mapped_column(nullable=False)
    sub_titulo: Mapped[str] = mapped_column(nullable=False)
    ano: Mapped[int] = mapped_column(nullable=False)
    descricao: Mapped[str] = mapped_column(nullable=False)
    cidade_publicacao: Mapped[str] = mapped_column(nullable=False)
    area_conhecimento: Mapped[str] = mapped_column(nullable=False)
    imagem: Mapped[str] = mapped_column(nullable=False)
    idioma: Mapped[str] = mapped_column(nullable=False)
    cdd: Mapped[str] = mapped_column(nullable=False)
    cdu: Mapped[str] = mapped_column(nullable=False)
    pha: Mapped[str] = mapped_column(nullable=False)
    cutter: Mapped[str] = mapped_column(nullable=False)


@table_registry.mapped_as_dataclass
class TCC:
    __tablename__ = "tccs"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    id_acervos: Mapped[int] = mapped_column(
        ForeignKey('acervos.id', ondelete='CASCADE'), nullable=False
    )
    tipo_publicacao: Mapped[str] = mapped_column(nullable=False)
    num_pg: Mapped[int] = mapped_column(nullable=False)
    grau_obtido: Mapped[int] = mapped_column(nullable=False)
    instituicao: Mapped[str] = mapped_column(nullable=False)
    curso: Mapped[str] = mapped_column(nullable=False)
    data_defesa: Mapped[date] = mapped_column(nullable=False)
    data_publicacao: Mapped[date] = mapped_column(nullable=False)


@table_registry.mapped_as_dataclass
class Periodico:
    __tablename__ = "periodicos"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    id_acervos: Mapped[int] = mapped_column(
        ForeignKey('acervos.id', ondelete='CASCADE'), nullable=False
    )
    editor: Mapped[str] = mapped_column(nullable=False)
    tradutor: Mapped[str] = mapped_column(nullable=False)
    editora: Mapped[str] = mapped_column(nullable=False)
    periodicidade: Mapped[str] = mapped_column(nullable=False)
    issn: Mapped[str] = mapped_column(nullable=False)
    numero: Mapped[int] = mapped_column(nullable=False)
    volume: Mapped[int] = mapped_column(nullable=False)
    suplemento: Mapped[str] = mapped_column(nullable=False)

@table_registry.mapped_as_dataclass
class Multimeo:
    __tablename__ = "multimeios"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    id_acervos: Mapped[int] = mapped_column(
        ForeignKey('acervos.id', ondelete='CASCADE'), nullable=False
    )
    tipo: Mapped[str] = mapped_column(nullable=False)
    documento: Mapped[str] = mapped_column(nullable=False)

@table_registry.mapped_as_dataclass
class Apostila:
    __tablename__ = "apostilas"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    id_acervos: Mapped[int] = mapped_column(
        ForeignKey('acervos.id', ondelete='CASCADE'), nullable=False
    )       
    editor: Mapped[str] = mapped_column(nullable=False)
    tradutor: Mapped[str] = mapped_column(nullable=False)
    editora: Mapped[str] = mapped_column(nullable=False)
    num_pg: Mapped[int] = mapped_column(nullable=False)

@table_registry.mapped_as_dataclass
class Livro:
    __tablename__ = "livros"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    id_acervos: Mapped[int] = mapped_column(
        ForeignKey('acervos.id', ondelete='CASCADE'), nullable=False
    )       
    editor: Mapped[str] = mapped_column(nullable=False)
    tradutor: Mapped[str] = mapped_column(nullable=False)
    editora: Mapped[str] = mapped_column(nullable=False)
    num_pg: Mapped[int] = mapped_column(nullable=False)
    isbn: Mapped[str] = mapped_column(nullable=False)


@table_registry.mapped_as_dataclass
class Exemplar:
    __tablename__ = "exemplares"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    id_acervo: Mapped[int] = mapped_column(
        ForeignKey('acervos.id', ondelete='CASCADE'), nullable=False
    )
    # nome: Mapped[str] = mapped_column(nullable=False)
    tombo: Mapped[str] = mapped_column(nullable=False, unique=True)
    status: Mapped[str] = mapped_column(nullable=False)
    data_aquisicao: Mapped[date] = mapped_column(nullable=False)
    modo_aquisicao: Mapped[str] = mapped_column(nullable=False)


@table_registry.mapped_as_dataclass
class Emprestimo:
    __tablename__ = "emprestimos"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    id_aluno: Mapped[int] = mapped_column(
        ForeignKey('alunos.id', ondelete='CASCADE'), nullable=False
    )
    id_exemplar: Mapped[int] = mapped_column(
        ForeignKey('exemplares.id', ondelete='CASCADE'), nullable=False
    )
    id_funcionario: Mapped[int] = mapped_column(
        ForeignKey('funcionarios.id', ondelete='CASCADE'), nullable=False
    )
    status: Mapped[str] = mapped_column(nullable=False)
    tempo_atraso: Mapped[datetime] = mapped_column(nullable=False)
    data_emprestimo: Mapped[datetime] = mapped_column(nullable=False)
    data_devolucao: Mapped[datetime] = mapped_column(nullable=False)
    
@table_registry.mapped_as_dataclass
class Reserva:
    __tablename__ = "reservas"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    id_aluno: Mapped[int] = mapped_column(
        ForeignKey('alunos.id', ondelete='CASCADE'), nullable=False
    )
    id_acervo: Mapped[int] = mapped_column(
        ForeignKey('acervos.id', ondelete='CASCADE'), nullable=False
    )
    status: Mapped[str] = mapped_column(nullable=False)
    data_reserva: Mapped[datetime] = mapped_column(nullable=False)
    data_validade: Mapped[datetime] = mapped_column(nullable=False)
    
@table_registry.mapped_as_dataclass
class Avaliacao:
    __tablename__ = "avaliacoes"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    id_aluno: Mapped[int] = mapped_column(
        ForeignKey('alunos.id', ondelete='CASCADE'), nullable=False
    )
    id_acervo: Mapped[int] = mapped_column(
        ForeignKey('acervos.id', ondelete='CASCADE'), nullable=False
    )
    nota: Mapped[int] = mapped_column(nullable=False)
    comentario: Mapped[str] = mapped_column(nullable=True)

@table_registry.mapped_as_dataclass
class ListaDesejos:
    __tablename__ = "listas_desejos"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    id_aluno: Mapped[int] = mapped_column(
        ForeignKey('alunos.id', ondelete='CASCADE'), nullable=False
    )
    id_acervo: Mapped[int] = mapped_column(
        ForeignKey('acervos.id', ondelete='CASCADE'), nullable=False
    )
    data_adicionado: Mapped[datetime] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)