from pydantic import BaseModel
from enum import Enum

class Message(BaseModel):
    message: str


class CargoEnum(str, Enum):
    auxiliar = 'auxiliar'
    bibliotecario = 'bibliotecario'
    outro = 'Outro'


class TurnoEnum(str, Enum):
    manha = 'manha'
    tarde = 'tarde'
    noite = 'noite'