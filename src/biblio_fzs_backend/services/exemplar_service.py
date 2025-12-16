from http import HTTPStatus

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from biblio_fzs_backend.schemas.exemplares_schemas import ExemplarSchema
from biblio_fzs_backend.models.models import Acervo, Exemplar


async def create_exemplar_service(
    id_acervo: int, exemplar: ExemplarSchema, session: AsyncSession
):
    acervo_db = await session.scalar(select(Acervo).where(Acervo.id == id_acervo))
    if not acervo_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Acervo não encontrado",
        )
    
    exemplar_already_exists = await session.scalars(select(Exemplar).where(
        Exemplar.tombo == exemplar.tombo
    ))
    if exemplar_already_exists.first():
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Exemplar com esse tombo já existe",
        )


    exemplar_db = Exemplar(**exemplar.model_dump(), id_acervo=id_acervo)
    session.add(exemplar_db)
    await session.commit()
    await session.refresh(exemplar_db)
    return exemplar_db


async def get_exemplar_by_id_acervo_service(
    id_acervo: int,
    session: AsyncSession
):
    exemplares = await session.scalars(
        select(Exemplar).where(Exemplar.id_acervo == id_acervo)
    )
    return exemplares.all()


async def get_all_exemplar_service(session: AsyncSession):
    exemplares = await session.scalars(select(Exemplar))
    return exemplares.all()