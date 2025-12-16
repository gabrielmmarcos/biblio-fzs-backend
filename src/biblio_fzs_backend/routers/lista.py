from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from biblio_fzs_backend.database import get_session
from biblio_fzs_backend.schemas.lista_schemas import ListaResponse
from biblio_fzs_backend.services.lista_service import create_lista_by_aluno_service, get_listas_by_aluno_service, remove_acervo_from_lista_service

router = APIRouter(prefix="/listas", tags=["listas"])

@router.get('/{id_aluno}/listas/', response_model=list[ListaResponse])
async def get_listas_by_aluno(   
    id_aluno: int,
    session: AsyncSession = Depends(get_session),
):
    return await get_listas_by_aluno_service(session, id_aluno)

@router.post('/{id_aluno}/listas/{id_acervo}/create_lista/', response_model=ListaResponse)
async def create_lista_by_aluno(
    id_aluno: int,
    id_acervo: int,
    session: AsyncSession = Depends(get_session),
):
    return await create_lista_by_aluno_service(
        session, id_aluno, id_acervo
    )



@router.delete('/{id_aluno}/listas/{id_acervo}/remove_acervo/', response_model=dict)
async def remove_acervo_from_lista(
    id_aluno: int,
    id_acervo: int,
    session: AsyncSession = Depends(get_session),
):
    return await remove_acervo_from_lista_service(
        session, id_aluno, id_acervo
    )
    