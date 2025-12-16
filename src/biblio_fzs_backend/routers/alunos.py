from typing import Annotated
from http import HTTPStatus

from fastapi import APIRouter, Depends,  UploadFile
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from biblio_fzs_backend.database import get_session
from biblio_fzs_backend.models.models import Aluno
from biblio_fzs_backend.schemas.alunos_schemas import (
    AlunoPublic,
    AlunoUpdate,
)
from biblio_fzs_backend.security.user_settings import auth_aluno_backend
from biblio_fzs_backend.services.aluno_service import (
    AlunoService,
    get_aluno_by_id_service,
    get_aluno_repository,
    update_aluno_service,
    delete_aluno_service,
    delete_aluno_by_id_service
)

from biblio_fzs_backend.services.images_services import upload_image_to_s3
from biblio_fzs_backend.services.aws import get_s3_client

fastapi_users = FastAPIUsers[Aluno, int](get_aluno_repository, [auth_aluno_backend])

T_CurrentAluno = Annotated[Aluno, Depends(fastapi_users.current_user())]

router = APIRouter(prefix="/alunos", tags=["alunos"])
T_UserManager = Annotated[AlunoService, Depends(get_aluno_repository)]


@router.get("/get_by_id/{id}/", response_model=AlunoPublic | None)
async def get_aluno_by_id(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    return await get_aluno_by_id_service(id, session)


@router.get("/get_all", response_model=list[AlunoPublic])
async def get_aluno_by_id(
    session: AsyncSession = Depends(get_session)
):
    return await session.scalars(select(Aluno))


@router.patch("/update/me", response_model=AlunoPublic)
async def update_aluno(
    aluno: AlunoUpdate,
    current_user: T_CurrentAluno,
    session: AsyncSession = Depends(get_session),
):
    return await update_aluno_service(aluno, current_user, session)


# @router.delete("/delete/{id}", status_code=200)
# async def delete_aluno(
#     id: int,
   
#     session: AsyncSession = Depends(get_session)
# ):

#     aluno = await session.scalar(
#         select(Aluno).where(Aluno.id == id)
#     )

#     if not aluno:
#         raise HTTPException(status_code=404, detail="Aluno não encontrado.")

#     await session.delete(aluno)
#     await session.commit()

#     return {"message": "Aluno deletado com sucesso."}



@router.put("/alunos/{id_aluno}/image", status_code=HTTPStatus.CREATED)
async def upload_aluno_image(
    id_aluno: int,
    image: UploadFile,
    s3_client=Depends(get_s3_client),
):
    ext = image.filename.split(".")[-1].lower()

    filename_with_ext = f"images/profile_images/alunos/{id_aluno}.{ext}"

    return await upload_image_to_s3(
        image=image,
        s3_client=s3_client,
        filename_with_ext=filename_with_ext,
    )
    
@router.delete("/delete/{id_aluno}/", status_code=200)
async def delete_aluno_by_id(
    id_aluno: int,
    session: AsyncSession = Depends(get_session)
):
    result = await delete_aluno_by_id_service(id_aluno, session)

    if result is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")

    return result    


