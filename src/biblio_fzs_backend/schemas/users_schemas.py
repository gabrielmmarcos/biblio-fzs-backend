from fastapi_users import schemas
from pydantic import BaseModel, EmailStr

from biblio_fzs_backend.schemas.root_schemas import CargoEnum, TurnoEnum


class UserSchemaBase(BaseModel):
    nome: str
    sobrenome: str
    cpf: str
    telefone: str
    cargo: CargoEnum
    turno: TurnoEnum
    crb: str


class UserSchema(schemas.BaseUserCreate, UserSchemaBase): ...


class UserPublic(schemas.BaseUser[int], UserSchemaBase): ...


class FuncionarioPublic(schemas.BaseUser[int], UserSchemaBase):
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
