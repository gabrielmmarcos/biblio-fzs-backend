from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from biblio_fzs_backend.database import get_session
from biblio_fzs_backend.schemas.reserva_schemas import ReservaResponse
from biblio_fzs_backend.services.reserva_service import create_reservas_by_aluno_service, get_reservas_by_aluno_service, cancel_reserva_by_id_service, get_all_reservas_service, get_total_reservas_service


router = APIRouter(prefix="/reservas", tags=["reservas"])

@router.get('/{id_aluno}/reservas/', response_model=list[ReservaResponse])
async def get_reservas_by_aluno(   
    id_aluno: int,
    session: AsyncSession = Depends(get_session),
):
    return await get_reservas_by_aluno_service(session, id_aluno)   

@router.get('/all_reservas/', response_model=list[ReservaResponse])
async def get_all_reservas(
    session: AsyncSession = Depends(get_session),
):
    return await get_all_reservas_service(session)

@router.get('/{id_aluno}/total_reservas/')
async def get_total_reservas(
    id_aluno: int,
    session: AsyncSession = Depends(get_session),
):
    return await get_total_reservas_service(session, id_aluno)

@router.post('/{id_aluno}/reservas/{id_acervo}/create_reserva/', response_model=ReservaResponse)
async def create_reserva_by_aluno(
    id_aluno: int,
    id_acervo: int,
    session: AsyncSession = Depends(get_session),
):
    return await create_reservas_by_aluno_service(
        session, id_aluno, id_acervo
    )

@router.delete('/reservas/{id_reserva}/cancel_reserva/')
async def cancel_reserva_by_id(
    id_reserva: int,
    session: AsyncSession = Depends(get_session),
):
    return await cancel_reserva_by_id_service(session, id_reserva)
