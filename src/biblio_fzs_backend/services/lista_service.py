from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from fastapi import HTTPException
from datetime import datetime, timedelta

from biblio_fzs_backend.schemas.lista_schemas import ListaResponse
from biblio_fzs_backend.models.models import Aluno, ListaDesejos, Acervo

async def get_listas_by_aluno_service(
    session: AsyncSession,
    id_aluno: int
):
    aluno_db = await session.scalar(select(Aluno).where(
        Aluno.id == id_aluno
    ))
    if not aluno_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Aluno não encontrado",
        )

    listas_db = await session.scalars(
        select(ListaDesejos).where(
            and_(
                ListaDesejos.id_aluno == id_aluno,
                ListaDesejos.status != 'removida'
            )
        )
    )
    listas_list = listas_db.all()

    listas_response = [
        ListaResponse(
            id=lista.id,
            id_aluno=lista.id_aluno,
            id_acervo=lista.id_acervo,
            data_adicionado=lista.data_adicionado,
            status=lista.status
        )
        for lista in listas_list
    ]

    return listas_response

async def create_lista_by_aluno_service(
    session: AsyncSession,
    id_aluno: int,
    id_acervo: int
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

    lista_db = ListaDesejos(
        id_aluno=id_aluno,
        id_acervo=id_acervo,
        data_adicionado=datetime.utcnow(),
        status='ativo'
    )
    session.add(lista_db)
    await session.commit()
    await session.refresh(lista_db)

    return ListaResponse(
        id=lista_db.id,
        id_aluno=lista_db.id_aluno,
        id_acervo=lista_db.id_acervo,
        data_adicionado=lista_db.data_adicionado,
        status=lista_db.status
    )
    
    
async def remove_acervo_from_lista_service(
    session: AsyncSession,
    id_aluno: int,
    id_acervo: int
):
    lista_db = await session.scalar(
        select(ListaDesejos).where(
            and_(
                ListaDesejos.id_aluno == id_aluno,
                ListaDesejos.id_acervo == id_acervo,
                ListaDesejos.status == 'ativo'
            )
        )
    )
    if not lista_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Acervo não encontrado na lista de desejos do aluno",
        )

    lista_db.status = 'removida'
    await session.commit()
    await session.refresh(lista_db)

    return ListaResponse(
        id=lista_db.id,
        id_aluno=lista_db.id_aluno,
        id_acervo=lista_db.id_acervo,
        data_adicionado=lista_db.data_adicionado,
        status=lista_db.status
    )   
    