from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from fastapi import HTTPException

from biblio_fzs_backend.schemas.emprestimos_schemas import EmprestimoSchema, TotalEmprestimosResponse
from biblio_fzs_backend.models.models import Funcionario, Exemplar, Aluno, Emprestimo, Acervo


async def create_emprestimo_service(
    current_funcionario: Funcionario,
    session: AsyncSession,
    emprestimo_data: EmprestimoSchema
):
    exemplar_db = await session.scalar(select(Exemplar).where(
        Exemplar.id == emprestimo_data.id_exemplar
    ))
    if not exemplar_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Exemplar não encontrado",
        )

    if exemplar_db.status != 'disponivel':
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Livro já emprestado!"
        )

    aluno_db = await session.scalar(select(Aluno).where(
        Aluno.id == emprestimo_data.id_aluno
        ))
    if not aluno_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Aluno não encontrado",
        )

    emprestimo_already_exists = await session.scalar(
        select(Emprestimo)
        .join(Exemplar, Exemplar.id == Emprestimo.id_exemplar)
        .join(Acervo, Acervo.id == Exemplar.id_acervo)
        .where(
            and_(
            Emprestimo.id_aluno == emprestimo_data.id_aluno,
            Acervo.id == exemplar_db.id_acervo,
            Emprestimo.status != 'entregue'
            )
        )
    )

    if emprestimo_already_exists:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Acervo já emprestado, ainda não entregue"
        )

    emprestimo_db = Emprestimo(**emprestimo_data.model_dump(), id_funcionario=current_funcionario.id)
    session.add(emprestimo_db)
    await session.commit()
    await session.refresh(emprestimo_db)

    return emprestimo_db

async def finish_emprestimo_service(
    session: AsyncSession,
    id_emprestimo: int
):
    emprestimo_db = await session.scalar(select(Emprestimo).where(
        Emprestimo.id == id_emprestimo
    ))
    if not emprestimo_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Empréstimo não encontrado",
        )

    if emprestimo_db.status == 'entregue':
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Empréstimo já finalizado",
        )

    emprestimo_db.status = 'entregue'
    await session.commit()
    await session.refresh(emprestimo_db)

    return emprestimo_db

async def get_emprestimos_by_aluno_service(
    session: AsyncSession,
    id_aluno: int
):
    emprestimos_db = await session.scalars(
        select(Emprestimo).where(
            Emprestimo.id_aluno == id_aluno
        )
    )
    emprestimos_list = emprestimos_db.all()

    return emprestimos_list

async def get_all_emprestimos_service(
    session: AsyncSession,
):
    emprestimos_db = await session.scalars(
        select(Emprestimo)
    )
    emprestimos_list = emprestimos_db.all()

    return emprestimos_list

async def get_total_emprestimos_service(
    session: AsyncSession,
    id_aluno: int,
):
    total_emprestimos = await session.execute(
        select(func.count(Emprestimo.id)).where(Emprestimo.id_aluno == id_aluno)
    )
    
    total_emprestimos = total_emprestimos.scalar()

    return total_emprestimos

async def delete_emprestimo_service(
    session: AsyncSession,
    id_emprestimo: int
):
    emprestimo_db = await session.scalar(select(Emprestimo).where(
        Emprestimo.id == id_emprestimo
    ))
    if not emprestimo_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Empréstimo não encontrado",
        )

    await session.delete(emprestimo_db)
    await session.commit()

    return None