from pydantic import BaseModel
from datetime import date

class TCCSchema(BaseModel):
    tipo_publicacao: str
    num_pg: int
    grau_obtido: int
    instituicao: str
    curso: str
    data_defesa: date
    data_publicacao: date


class TCCResponse(TCCSchema):
    id: int
    id_acervos: int

class PeriodicoSchema(BaseModel):
    editor: str
    tradutor: str
    editora: str
    periodicidade: str
    issn: str
    numero: int
    volume: int
    suplemento: str

class PeriodicoResponse(PeriodicoSchema):
    id: int
    id_acervos:int

class MultimeoSchemas(BaseModel):
    tipo: str
    documento: str

class MultimeoResponse(MultimeoSchemas):
    id: int
    id_acervos:int

class ApostilaSchemas(BaseModel):
    editor: str
    tradutor: str
    editora: str
    num_pg: int

class ApostilaResponse(ApostilaSchemas):
    id: int
    id_acervos: int
    
class LivroSchemas(BaseModel):
    editor: str
    tradutor: str
    editora: str
    num_pg: int
    isbn: str

class LivroResponse(LivroSchemas):
    id: int
    id_acervos: int