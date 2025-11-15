from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from biblio_fzs_backend.database import get_session
from biblio_fzs_backend.schemas.cursos_schemas import CursoSchema, MatriculaBase, MatriculaResponse, CursoResponse, MatricularAlunoFuncionarioModel
from biblio_fzs_backend.schemas.root_schemas import Message
from biblio_fzs_backend.services.curso_service import create_cursos_service, matricular_aluno_funcionario_service, matricular_aluno_com_aluno_autenticado_service
from biblio_fzs_backend.models.models import Curso, AlunoCurso
from biblio_fzs_backend.routers.alunos import T_CurrentAluno
from biblio_fzs_backend.routers.funcionarios import T_CurrentFuncionario

router = APIRouter(prefix="/cursos", tags=["cursos"])


@router.post("/create", status_code=201, response_model=Message)
async def create_cursos(
    cursos: list[CursoSchema],
    session: AsyncSession = Depends(get_session),
):
    return await create_cursos_service(cursos, session)


@router.get('/', response_model=list[CursoResponse])
async def get_all(session: AsyncSession = Depends(get_session)):
    cursos = await session.scalars(select(Curso))

    return cursos.all()


@router.post('/auto_matricular_aluno/', response_model=MatriculaResponse)
async def matricular_aluno_com_aluno_autenticado(
    matricula_data: MatriculaBase,
    current_aluno: T_CurrentAluno,
    session: AsyncSession = Depends(get_session),
):
    return await matricular_aluno_com_aluno_autenticado_service(
        current_aluno, session, matricula_data
        )


@router.get('/matriculas', response_model=list[MatriculaResponse])
async def get_all_matriculas(session: AsyncSession = Depends(get_session)):
    cursos = await session.scalars(select(AlunoCurso))

    return cursos.all()


@router.get('/matriculas/me', response_model=list[MatriculaResponse])
async def get_all_matriculas(
    current_aluno: T_CurrentAluno,
    session: AsyncSession = Depends(get_session)):
    cursos = await session.scalars(select(AlunoCurso).where(AlunoCurso.id_aluno == current_aluno.id))

    return cursos.all()


@router.get('/matriculas/{id_aluno}', response_model=list[MatriculaResponse])
async def get_all_matriculas(
    id_aluno: int,
    session: AsyncSession = Depends(get_session),
):
    cursos = await session.scalars(select(AlunoCurso).where(AlunoCurso.id_aluno == id_aluno))

    return cursos.all()


@router.post('/matricular_aluno_funcionario/', response_model=MatriculaResponse)
async def matricular_aluno_funcionario(
    matricula_data: MatricularAlunoFuncionarioModel,
    current_funcionario: T_CurrentFuncionario,
    session: AsyncSession = Depends(get_session),
):
    return await matricular_aluno_funcionario_service(
        current_funcionario, session, matricula_data
        )

