from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from biblio_fzs_backend.database import get_session
from biblio_fzs_backend.schemas.emprestimos_schemas import EmprestimoSchema, ExemplarResponse, TotalEmprestimosResponse
from biblio_fzs_backend.services.emprestimo_service import create_emprestimo_service, finish_emprestimo_service, get_emprestimos_by_aluno_service, get_all_emprestimos_service, get_total_emprestimos_service, delete_emprestimo_service
from biblio_fzs_backend.routers.funcionarios import T_CurrentFuncionario

router = APIRouter(prefix="/emprestimos", tags=["emprestimos"])


@router.get('/{id_aluno}/emprestimos/', response_model=list[ExemplarResponse])
async def get_emprestimos_by_aluno(   
    id_aluno: int,
    session: AsyncSession = Depends(get_session),
):
    return await get_emprestimos_by_aluno_service(session, id_aluno)

@router.get('/all_emprestimos/', response_model=list[ExemplarResponse])
async def get_all_emprestimos(
    session: AsyncSession = Depends(get_session),
):
    return await get_all_emprestimos_service(session)

@router.get('/{id_aluno}/total_emprestimos/')
async def get_total_emprestimos(
    id_aluno: int,
    session: AsyncSession = Depends(get_session),
):
    return await get_total_emprestimos_service(session, id_aluno)

@router.post('/create_emprestimo/', response_model=ExemplarResponse)
async def create_emprestimo(
    emprestimo_data: EmprestimoSchema,
    current_funcionario: T_CurrentFuncionario,
    session: AsyncSession = Depends(get_session),
):
    return await create_emprestimo_service(
        current_funcionario, session, emprestimo_data
        )

@router.put('/finish_emprestimo/{id_emprestimo}/', response_model=ExemplarResponse)
async def finish_emprestimo(
    id_emprestimo: int,

    session: AsyncSession = Depends(get_session),
):
    return await finish_emprestimo_service( session, id_emprestimo)
    
    
@router.delete('/delete_emprestimo/{id_emprestimo}/')
async def delete_emprestimo(
    id_emprestimo: int,
    session: AsyncSession = Depends(get_session),
):
    return await delete_emprestimo_service(session, id_emprestimo)