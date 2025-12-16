from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from biblio_fzs_backend.database import get_session
from biblio_fzs_backend.schemas.presenca_schemas import PresencaResponse, PresencaTotalResponse
from biblio_fzs_backend.schemas.root_schemas import Message
from biblio_fzs_backend.models.models import Presenca
from biblio_fzs_backend.routers.alunos import T_CurrentAluno
from biblio_fzs_backend.services.presenca_service import obter_presenca_por_aluno_service, obter_total_presencas_por_aluno_service


router = APIRouter(prefix="/presenca", tags=["presenca"])


@router.post("/", status_code=201, response_model=PresencaResponse)
async def registrar_presenca(
    current_aluno: T_CurrentAluno,
    session: AsyncSession = Depends(get_session),
):
    presenca_db = Presenca(datetime.now(), current_aluno.id)
    session.add(presenca_db)
    await session.commit()
    await session.refresh(presenca_db)
    return presenca_db

@router.get("/aluno/{id_aluno}", response_model=List[PresencaResponse])
async def obter_presencas_do_aluno(
    id_aluno: int,
    session: AsyncSession = Depends(get_session),
):
    presencas = await obter_presenca_por_aluno_service(id_aluno, session)
    return presencas

@router.get("/aluno/{id_aluno}/total", response_model=PresencaTotalResponse)
async def obter_total_presencas_do_aluno(
    id_aluno: int,
    session: AsyncSession = Depends(get_session),
):
    total = await obter_total_presencas_por_aluno_service(id_aluno, session)

    return {
        "id_aluno": id_aluno,
        "total_presencas": total
    }