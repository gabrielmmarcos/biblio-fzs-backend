from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from fastapi import HTTPException
from datetime import datetime, timedelta

from biblio_fzs_backend.schemas.reserva_schemas import ReservaResponse, TotalReservasResponse
from biblio_fzs_backend.models.models import Aluno, Reserva, Acervo

async def get_reservas_by_aluno_service(
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

    reservas_db = await session.scalars(
        select(Reserva).where(
            and_(
                Reserva.id_aluno == id_aluno,
                Reserva.status != 'cancelada'
            )
        )
    )
    reservas_list = reservas_db.all()

    reservas_response = [
        ReservaResponse(
            id=reserva.id,
            id_aluno=reserva.id_aluno,
            id_acervo=reserva.id_acervo,
            data_reserva=reserva.data_reserva,
            status=reserva.status,
            data_validade=reserva.data_validade
        )
        for reserva in reservas_list
    ]

    return reservas_response

async def create_reservas_by_aluno_service(
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

    reserva_db = Reserva(
        id_aluno=id_aluno,
        id_acervo=id_acervo,
        status='ativa',
        data_reserva=datetime.utcnow(),
        data_validade=datetime.utcnow().date() + timedelta(days=7)
    ) 
    session.add(reserva_db)
    await session.commit()
    await session.refresh(reserva_db)

    reserva_response = ReservaResponse(
        id=reserva_db.id,
        id_aluno=reserva_db.id_aluno,
        id_acervo=reserva_db.id_acervo,
        data_reserva=reserva_db.data_reserva,
        status=reserva_db.status,
        data_validade=reserva_db.data_validade
    )

    return reserva_response

async def cancel_reserva_by_id_service(
    session: AsyncSession,
    id_reserva: int
):
    reserva_db = await session.scalar(select(Reserva).where(
        Reserva.id == id_reserva
    ))
    if not reserva_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Reserva não encontrada",
        )

    reserva_db.status = 'cancelada'
    await session.commit()
    await session.refresh(reserva_db)

    reserva_response = ReservaResponse(
        id=reserva_db.id,
        id_aluno=reserva_db.id_aluno,
        id_acervo=reserva_db.id_acervo,
        data_reserva=reserva_db.data_reserva,
        status=reserva_db.status,
        data_validade=reserva_db.data_validade
    )

    return reserva_response

async def get_all_reservas_service(
    session: AsyncSession,
):
    reservas_db = await session.scalars(
        select(Reserva).where(
            Reserva.status != 'cancelada'
        )
    )
    reservas_list = reservas_db.all()

    reservas_response = [
        ReservaResponse(
            id=reserva.id,
            id_aluno=reserva.id_aluno,
            id_acervo=reserva.id_acervo,
            data_reserva=reserva.data_reserva,
            status=reserva.status,
            data_validade=reserva.data_validade
        )
        for reserva in reservas_list
    ]

    return reservas_response

async def get_total_reservas_service(
    session: AsyncSession,
    id_aluno: int
):
    total_reservas = await session.execute(
         select(func.count(Reserva.id)).where(Reserva.id_aluno == id_aluno)
    )

    total_reservas = total_reservas.scalar()
    return total_reservas


