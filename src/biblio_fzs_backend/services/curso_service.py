from sqlalchemy.ext.asyncio import AsyncSession

from biblio_fzs_backend.schemas.cursos_schemas import CursoSchema, MatricularAlunoFuncionarioModel, MatriculaBase
from biblio_fzs_backend.models.models import Curso, Aluno, AlunoCurso

async def create_cursos_service(
    cursos: list[CursoSchema],
    session: AsyncSession
):
    for curso in cursos:
        curso_db = Curso(**curso.model_dump())
        session.add(curso_db)
    await session.commit()
    return {'message': 'cursos adicionados'}


async def matricular_aluno_com_aluno_autenticado_service(
    current_aluno: Aluno,
    session: AsyncSession,
    matricula_base_data: MatriculaBase
):
    aluno_curso_db = AlunoCurso(
        current_aluno.id,
        id_curso=matricula_base_data.id_curso,
        ra=matricula_base_data.ra
    )
    session.add(aluno_curso_db)
    await session.commit()
    session.refresh(aluno_curso_db)

    return aluno_curso_db



async def matricular_aluno_funcionario_service(
    current_funcionario: Aluno,
    session: AsyncSession,
    matricula_data: MatricularAlunoFuncionarioModel
):
    aluno_curso_db = AlunoCurso(
        matricula_data.id_aluno,
        id_curso=matricula_data.id_curso,
        ra=matricula_data.ra
    )

    session.add(aluno_curso_db)
    await session.commit()
    session.refresh(aluno_curso_db)

    return aluno_curso_db
