from datetime import date

from pydantic import BaseModel

class ExemplarSchema(BaseModel):
    # nome: str
    tombo: str
    status: str
    data_aquisicao: date
    modo_aquisicao: str


class ExemplarResponse(ExemplarSchema):
    id: int
    id_acervo: int