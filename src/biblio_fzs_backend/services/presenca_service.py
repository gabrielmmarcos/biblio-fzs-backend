from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from fastapi import HTTPException

from biblio_fzs_backend.schemas.presenca_schemas import PresencaResponse
from biblio_fzs_backend.models.models import Aluno, Presenca

async def obter_presenca_por_aluno_service(
    id_aluno: int,
    session: AsyncSession,
):
    result = await session.execute(
        select(Presenca).where(Presenca.id_aluno == id_aluno)
    )
    presenca_db = result.scalars().all()
    if not presenca_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Presença não encontrada para o aluno informado."
        )
    return presenca_db  


async def obter_total_presencas_por_aluno_service(
    id_aluno: int,
    session: AsyncSession,
):
    result = await session.execute(
        select(func.count(Presenca.id)).where(Presenca.id_aluno == id_aluno)
    )

    total = result.scalar()
    return total