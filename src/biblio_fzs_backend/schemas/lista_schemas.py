from pydantic import BaseModel
from datetime import datetime

class ListaResponse(BaseModel):
    id: int
    id_aluno: int
    id_acervo: int
    data_adicionado: datetime
    status: str