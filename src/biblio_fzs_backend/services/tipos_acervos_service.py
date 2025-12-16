from http import HTTPStatus

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from biblio_fzs_backend.schemas.tipos_acervos_schemas import TCCSchema, PeriodicoSchema, ApostilaSchemas, MultimeoSchemas, LivroSchemas
from biblio_fzs_backend.models.models import Acervo, TCC, Periodico, Multimeo, Apostila, Livro


async def create_tcc_service(
    id_acervo: int, acervo: TCCSchema, session: AsyncSession
):
    acervo_db = await session.scalar(select(Acervo).where(Acervo.id == id_acervo))
    if not acervo_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Acervo não encontrado",
        )

    tcc_db = TCC(**acervo.model_dump(), id_acervos=id_acervo)
    session.add(tcc_db)
    await session.commit()
    await session.refresh(tcc_db)
    return tcc_db


async def get_all_tccs_service(session: AsyncSession):
    result = await session.scalars(select(TCC))
    return result.all()


async def get_tcc_by_id_acervo_service(id_acervo: int, session: AsyncSession):
    result = await session.scalars(select(TCC).where(TCC.id_acervos == id_acervo))
    return result.first()


async def create_periodico_service(
    id_acervo: int, acervo: PeriodicoSchema, session: AsyncSession
):
    acervo_db = await session.scalar(select(Acervo).where(Acervo.id == id_acervo))
    if not acervo_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Acervo não encontrado",
        )

    periodico_db = Periodico(**acervo.model_dump(), id_acervos=id_acervo)
    session.add(periodico_db)
    await session.commit()
    await session.refresh(periodico_db)
    return periodico_db


async def get_all_periodicos_service(session: AsyncSession):
    result = await session.scalars(select(Periodico))
    return result.all()


async def get_periodico_by_id_acervo_service(id_acervo: int, session: AsyncSession):
    result = await session.scalars(select(Periodico).where(TCC.id_acervos == id_acervo))
    return result.first()


async def create_multimeo_service(
    id_acervo: int, acervo: MultimeoSchemas, session: AsyncSession
):
    acervo_db = await session.scalar(select(Acervo).where(Acervo.id == id_acervo))
    if not acervo_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Acervo não encontrado",
        )

    
    multimeo_db = Multimeo(
        tipo=acervo.tipo,
        documento=acervo.documento,
        id_acervos=id_acervo
    )

    session.add(multimeo_db)
    await session.commit()
    await session.refresh(multimeo_db)
    return multimeo_db


async def get_all_multimeos_service(session: AsyncSession):
    result = await session.scalars(select(Multimeo))
    return result.all()


async def get_multimeo_by_id_acervo_service(id_acervo: int, session: AsyncSession):
    result = await session.scalars(select(Multimeo).where(Multimeo.id_acervos == id_acervo))
    return result.first()


async def create_apostila_service(
    id_acervo: int, acervo: ApostilaSchemas, session: AsyncSession
):
    acervo_db = await session.scalar(select(Acervo).where(Acervo.id == id_acervo))
    if not acervo_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Acervo não encontrado",
        )

    apostila_db = Apostila(**acervo.model_dump(), id_acervos=id_acervo)
    session.add(apostila_db)
    await session.commit()
    await session.refresh(apostila_db)
    return apostila_db


async def get_all_apostilas_service(session: AsyncSession):
    result = await session.scalars(select(Apostila))
    return result.all()


async def get_apostila_by_id_acervo_service(id_acervo: int, session: AsyncSession):
    result = await session.scalars(select(Apostila).where(Apostila.id_acervos == id_acervo))
    return result.first()


async def create_livro_service(
    id_acervo: int, acervo: LivroSchemas, session: AsyncSession
):
    acervo_db = await session.scalar(select(Acervo).where(Acervo.id == id_acervo))
    if not acervo_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Acervo não encontrado",
        )

    livro_db = Livro(**acervo.model_dump(), id_acervos=id_acervo)
    session.add(livro_db)
    await session.commit()
    await session.refresh(livro_db)
    return livro_db


async def get_all_livros_service(session: AsyncSession):
    result = await session.scalars(select(Livro))
    return result.all()


async def get_livro_by_id_acervo_service(id_acervo: int, session: AsyncSession):
    result = await session.scalars(select(Livro).where(Livro.id_acervos == id_acervo))
    return result.first()