from fastapi_users import schemas
from pydantic import BaseModel, EmailStr

from biblio_fzs_backend.schemas.root_schemas import CargoEnum, TurnoEnum


class FuncionarioSchemaBase(BaseModel):
    nome: str
    sobrenome: str
    cpf: str
    telefone: str
    cargo: CargoEnum
    turno: TurnoEnum
    crb: str
    cep: int


class FuncionarioSchema(schemas.BaseUserCreate, FuncionarioSchemaBase): ...


class FuncionarioPublic(schemas.BaseUser[int], FuncionarioSchemaBase): ...


class FuncionarioPublic(schemas.BaseUser[int], FuncionarioSchemaBase):
    cep: int | None
    numero_residencia: str | None
    email: EmailStr
    complemento: str | None


class FuncionarioUpdate(BaseModel):
    nome: str | None = None
    sobrenome: str | None = None
    cpf: str | None = None
    cargo: CargoEnum | None = None
    turno: TurnoEnum | None = None
    cep: int | None = None
    numero_residencia: str | None = None
    complemento: str | None = None
    crb: str | None = None
    telefone: str | None = None
