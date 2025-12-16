from datetime import datetime

from pydantic import BaseModel

class EmprestimoSchema(BaseModel):
    id_aluno: int
    id_exemplar: int
    status: str
    tempo_atraso: datetime
    data_emprestimo: datetime
    data_devolucao: datetime


class ExemplarResponse(EmprestimoSchema):
    id: int
    id_funcionario: int
    
class TotalEmprestimosResponse(BaseModel):
    total_emprestimos: int