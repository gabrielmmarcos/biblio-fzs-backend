from http import HTTPStatus

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from biblio_fzs_backend.schemas.avaliacao_schemas import AvaliacaoResponse
from biblio_fzs_backend.models.models import Avaliacao, Aluno, Acervo

async def get_avalicoes_by_acervo_service(
    session: AsyncSession,
    id_acervo: int
):
    acervo_db = await session.scalar(select(Acervo).where(
        Acervo.id == id_acervo
    ))
    if not acervo_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Acervo não encontrado",
        )

    avalicoes_db = await session.scalars(
        select(Avaliacao).where(
            Avaliacao.id_acervo == id_acervo
        )
    )
    avalicoes_list = avalicoes_db.all()

    avalicoes_response = [
        AvaliacaoResponse(
            id=Avaliacao.id,
            id_aluno=Avaliacao.id_aluno,
            id_acervo=Avaliacao.id_acervo,
            nota=Avaliacao.nota,
            comentario=Avaliacao.comentario
        )
        for Avaliacao in avalicoes_list
    ]

    return avalicoes_response

async def create_avaliacao_by_aluno_service(
    session: AsyncSession,
    id_aluno: int,
    id_acervo: int,
    nota: int,
    comentario: str
):
    aluno_db = await session.scalar(select(Aluno).where(
        Aluno.id == id_aluno
    ))
    if not aluno_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Aluno não encontrado",
        )

    acervo_db = await session.scalar(select(Acervo).where(
        Acervo.id == id_acervo
    ))
    if not acervo_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Acervo não encontrado",
        )

    Avaliacao_db = Avaliacao(
        id_aluno=id_aluno,
        id_acervo=id_acervo,
        nota=nota,
        comentario=comentario
    )
    session.add(Avaliacao_db)
    await session.commit()
    await session.refresh(Avaliacao_db)

    return Avaliacao_db


async def delete_avaliacao_by_id_service(
    session: AsyncSession,
    id_avaliacao: int
):
    avaliacao_db = await session.scalar(select(Avaliacao).where(
        Avaliacao.id == id_avaliacao
    ))
    if not avaliacao_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Avaliação não encontrada",
        )

    await session.delete(avaliacao_db)
    await session.commit()

    return {"detail": "Avaliação deletada com sucesso"}
