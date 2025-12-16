from http import HTTPStatus

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from biblio_fzs_backend.schemas.acervos_schemas import AcervoSchema, AutorSchema
from biblio_fzs_backend.models.models import Acervo, Autor


async def create_acervo_service(
    id_autor: int, acervo: AcervoSchema, session: AsyncSession
):
    autor_db = await session.scalar(select(Autor).where(Autor.id == id_autor))
    if not autor_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Autor não encontrado",
        )
    # acervo_already_exists = session.scalars(select(Autor))
    acervo_db = Acervo(**acervo.model_dump(), id_autor=id_autor)
    session.add(acervo_db)
    await session.commit()
    await session.refresh(acervo_db)
    return acervo_db


async def get_all_acervos_service(session: AsyncSession):
    result = await session.scalars(select(Acervo))
    return result.all()

async def create_autor_service(autor: AutorSchema, session: AsyncSession):
    autor_db = Autor(autor.nome)
    session.add(autor_db)
    await session.commit()
    await session.refresh(autor_db)
    return autor_db


async def delete_autor_service(id_autor: int, session: AsyncSession):
    autor_db = await get_autor_by_id_service(id_autor, session)
    await session.delete(autor_db)
    await session.commit()
    return



async def get_all_autores_service(session: AsyncSession):
    result = await session.scalars(select(Autor))
    return result.all()

async def get_autor_by_id_service(id_autor: int, session: AsyncSession):
    autor_db = await session.scalar(select(Autor).where(Autor.id == id_autor))
    if not autor_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Autor não encontrado",
        )
    return autor_db

async def get_acervo_by_id_service(id_acervo: int, session: AsyncSession):
    acervo_db = await session.scalar(select(Acervo).where(Acervo.id == id_acervo))
    if not acervo_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Acervo não encontrado",
        )
    return acervo_db

async def delete_acervo_service(id_acervo: int, session: AsyncSession):
    acervo_db = await get_acervo_by_id_service(id_acervo, session)
    await session.delete(acervo_db)
    await session.commit()
    return