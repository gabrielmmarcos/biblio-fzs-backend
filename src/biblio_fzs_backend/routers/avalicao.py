from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from biblio_fzs_backend.database import get_session
from biblio_fzs_backend.schemas.avaliacao_schemas import AvaliacaoResponse
from biblio_fzs_backend.services.avaliacao_service import create_avaliacao_by_aluno_service, get_avalicoes_by_acervo_service, delete_avaliacao_by_id_service

router = APIRouter(prefix="/avalicoes", tags=["avalicoes"])

@router.get('/{id_acervo}/avalicoes/', response_model=list[AvaliacaoResponse])
async def get_avalicoes_by_acervo(   
    id_acervo: int,
    session: AsyncSession = Depends(get_session),
):
    return await get_avalicoes_by_acervo_service(session, id_acervo)

@router.post('/{id_aluno}/avaliacoes/{id_acervo}/create_avaliacao/', response_model=AvaliacaoResponse)
async def create_avaliacao_by_aluno(
    id_aluno: int,
    id_acervo: int,
    nota: int,
    comentario: str,
    session: AsyncSession = Depends(get_session),
):
    return await create_avaliacao_by_aluno_service(
        session, id_aluno, id_acervo, nota, comentario
    )

@router.delete('/avaliacoes/{id_avaliacao}/delete_avaliacao/')
async def delete_avaliacao_by_id(
    id_avaliacao: int,
    session: AsyncSession = Depends(get_session),
):
    return await delete_avaliacao_by_id_service(session, id_avaliacao)


