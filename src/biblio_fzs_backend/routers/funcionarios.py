from typing import Annotated
from http import HTTPStatus

from fastapi import APIRouter, Depends, UploadFile
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from biblio_fzs_backend.database import get_session
from biblio_fzs_backend.models.models import Funcionario
from biblio_fzs_backend.schemas.funcionarios_schemas import (
    FuncionarioPublic,
    FuncionarioUpdate,
    FuncionarioPublic,
)
from biblio_fzs_backend.security.user_settings import auth_funcionario_backend
from biblio_fzs_backend.services.funcionario_service import (
    FuncionarioService,
    get_funcionario_by_id_service,
    get_funcionario_repository,
    update_funcionario_service,
)

from biblio_fzs_backend.services.images_services import upload_image_to_s3
from biblio_fzs_backend.services.aws import get_s3_client


fastapi_users = FastAPIUsers[Funcionario, int](get_funcionario_repository, [auth_funcionario_backend])

T_CurrentFuncionario = Annotated[Funcionario, Depends(fastapi_users.current_user())]

router = APIRouter(prefix="/funcionarios", tags=["funcionarios"])
T_UserManager = Annotated[FuncionarioService, Depends(get_funcionario_repository)]


@router.get("/get_by_id/{id}", response_model=FuncionarioPublic)
async def get_users_by_id(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await get_funcionario_by_id_service(id, session)


@router.patch("/update/me", response_model=FuncionarioPublic)
async def update_funcionario(
    funcionario: FuncionarioUpdate,
    current_user: T_CurrentFuncionario,
    session: AsyncSession = Depends(get_session),
):
    return await update_funcionario_service(funcionario, current_user, session)

@router.get("/get_all", response_model=list[FuncionarioPublic])
async def get_users_by_id(
    session: AsyncSession = Depends(get_session)
):
    return await session.scalars(select(Funcionario))

@router.delete("/delete/{id}", status_code=200)
async def delete_funcionario(
    id: int,
    current_user: T_CurrentFuncionario,
    session: AsyncSession = Depends(get_session)
):
    if id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Você não pode deletar sua própria conta."
        )

    funcionario = await session.scalar(
        select(Funcionario).where(Funcionario.id == id)
    )

    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado.")

    await session.delete(funcionario)
    await session.commit()

    return {"message": "Funcionário deletado com sucesso."}



@router.put("/funcionarios/{id_funcionario}/image", status_code=HTTPStatus.CREATED)
async def upload_funcionario_image(
    id_funcionario: int,
    image: UploadFile,
    s3_client=Depends(get_s3_client),
):
    ext = image.filename.split(".")[-1].lower()

    filename_with_ext = f"images/profile_images/funcionarios/{id_funcionario}.{ext}"

    return await upload_image_to_s3(
        image=image,
        s3_client=s3_client,
        filename_with_ext=filename_with_ext,
    )
