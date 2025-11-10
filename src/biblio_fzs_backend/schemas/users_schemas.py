from fastapi_users import schemas
from pydantic import BaseModel
from biblio_fzs_backend.schemas.root_schemas import CargoEnum, TurnoEnum

class UserSchemaBase(BaseModel):
    nome: str
    sobrenome: str
    cpf: str
    cargo: CargoEnum
    turno: TurnoEnum
    crb: str


class UserSchema(schemas.BaseUserCreate, UserSchemaBase): ...


class UserPublic(schemas.BaseUser[int], UserSchemaBase): ...
