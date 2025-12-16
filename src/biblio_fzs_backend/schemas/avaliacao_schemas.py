from pydantic import BaseModel

class AvaliacaoResponse(BaseModel):
    id: int
    id_aluno: int
    id_acervo: int
    nota: int
    comentario: str