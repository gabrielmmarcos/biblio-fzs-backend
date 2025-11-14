from fastapi_users import schemas
from pydantic import BaseModel, EmailStr

from biblio_fzs_backend.schemas.root_schemas import CargoEnum, TurnoEnum


class AlunoSchemaBase(BaseModel):
    nome: str
    sobrenome: str
    email: EmailStr
    cpf: str
    cep: int
    numero_residencia: str | None
    complemento: str | None


class AlunoSchema(schemas.BaseUserCreate, AlunoSchemaBase): ...


class AlunoPublic(schemas.BaseUser[int], AlunoSchemaBase): ...
    

class AlunoUpdate(BaseModel):
    nome: str | None = None
    sobrenome: str | None = None
    cpf: str | None = None
    cep: int | None = None
    numero_residencia: str | None = None
    complemento: str | None = None
