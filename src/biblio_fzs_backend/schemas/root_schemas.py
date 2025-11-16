from enum import Enum

from pydantic import BaseModel


class Message(BaseModel):
    message: str


class CargoEnum(str, Enum):
    auxiliar = 'auxiliar'
    bibliotecario = 'bibliotecario'
    outro = 'Outro'


class TurnoEnum(str, Enum):
    manha = 'manhã'
    tarde = 'tarde'
    noite = 'noite'
