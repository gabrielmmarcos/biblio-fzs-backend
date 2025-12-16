from pydantic import BaseModel

class AcervoSchema(BaseModel):
    titulo: str
    sub_titulo: str
    ano: int
    descricao: str
    cidade_publicacao: str
    area_conhecimento: str
    imagem: str
    idioma: str
    cdd: str
    cdu: str
    pha: str
    cutter: str

class AcervoResponse(AcervoSchema):
    id: int
    id_autor: int


class AutorSchema(BaseModel):
    nome: str


class AuthorResponse(AutorSchema):
    id: int