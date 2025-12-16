from pydantic import BaseModel
from datetime import datetime

class ReservaResponse(BaseModel):
    id: int
    id_aluno: int
    id_acervo: int
    data_reserva: datetime
    status: str
    data_validade: datetime
  
class TotalReservasResponse(BaseModel):
    total_reservas: int