from pydantic import BaseModel
from datetime import datetime


class PresencaResponse(BaseModel):
    id: int
    id_aluno: int
    datetime_presenca: datetime
    
class PresencaTotalResponse(BaseModel):
    id_aluno: int
    total_presencas: int
