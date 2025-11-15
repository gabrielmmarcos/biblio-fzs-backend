from datetime import date
from pydantic import BaseModel
from biblio_fzs_backend.schemas.root_schemas import TurnoEnum


class CursoSchema(BaseModel):
    nome: str
    periodo: TurnoEnum
    inicio: date
    fim: date
    instituicao: str


class CursoResponse(CursoSchema):
    id: int


class MatriculaBase(BaseModel):
    id_curso: int
    ra: str


class MatriculaResponse(MatriculaBase):
    id: int
    id_aluno: int

class MatricularAlunoFuncionarioModel(MatriculaBase):
    id_aluno: int
