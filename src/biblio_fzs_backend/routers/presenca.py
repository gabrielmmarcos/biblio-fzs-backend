from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from biblio_fzs_backend.database import get_session
from biblio_fzs_backend.schemas.presenca_schemas import PresencaResponse
from biblio_fzs_backend.schemas.root_schemas import Message
from biblio_fzs_backend.models.models import Presenca
from biblio_fzs_backend.routers.alunos import T_CurrentAluno


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

