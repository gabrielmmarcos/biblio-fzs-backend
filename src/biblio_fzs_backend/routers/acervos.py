from typing import Annotated
from http import HTTPStatus

from fastapi import APIRouter, Depends,  UploadFile
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession

from biblio_fzs_backend.database import get_session
from biblio_fzs_backend.models.models import Funcionario
from biblio_fzs_backend.schemas.acervos_schemas import AcervoSchema, AcervoResponse, AutorSchema, AuthorResponse

from biblio_fzs_backend.security.user_settings import auth_funcionario_backend
from biblio_fzs_backend.services.funcionario_service import (
    get_funcionario_repository,
)
from biblio_fzs_backend.services.acervo_service import create_acervo_service, get_all_acervos_service, create_autor_service, get_all_autores_service, get_acervo_by_id_service, delete_acervo_service, get_autor_by_id_service,delete_autor_service

from biblio_fzs_backend.services.images_services import upload_image_to_s3
from biblio_fzs_backend.services.aws import get_s3_client


fastapi_users = FastAPIUsers[Funcionario, int](get_funcionario_repository, [auth_funcionario_backend])

T_CurrentFuncionario = Annotated[Funcionario, Depends(fastapi_users.current_user())]

router = APIRouter(prefix="/acervos", tags=["acervos"])

@router.post("/{id_autor}", response_model=AcervoResponse)
async def create_acervo(
    id_autor: int, acervo: AcervoSchema, session: AsyncSession = Depends(get_session)
):
    return await create_acervo_service(id_autor, acervo, session)


@router.get('/', response_model=list[AcervoResponse] | None)
async def get_all_acervos(session: AsyncSession = Depends(get_session)):
    return await get_all_acervos_service(session)


@router.post('/autor/', response_model=AuthorResponse)
async def create_autor(autor: AutorSchema, session: AsyncSession = Depends(get_session)):
    return await create_autor_service(autor, session)


@router.get('/autor/', response_model=list[AuthorResponse])
async def get_all_autores(session: AsyncSession = Depends(get_session)):
    return await get_all_autores_service(session)

@router.get('/autor/{id_autor}', response_model=AuthorResponse)
async def get_autor_by_id(id_autor: int, session: AsyncSession = Depends(get_session)):
    return await get_autor_by_id_service(id_autor, session)

@router.delete('/autor/{id_autor}/delete/')
async def delete_autor(id_autor: int, session: AsyncSession = Depends(get_session)):
    return await delete_autor_service(id_autor, session)

@router.get('/{id_acervo}', response_model=AcervoResponse)
async def get_acervo_by_id(id_acervo: int, session: AsyncSession = Depends(get_session)):
    return await get_acervo_by_id_service(id_acervo, session)

@router.delete('/{id_acervo}/delete/')
async def delete_acervo(id_acervo: int, session: AsyncSession = Depends(get_session)):
    return await delete_acervo_service(id_acervo, session)


@router.put("/acervos/{id_acervo}/image", status_code=HTTPStatus.CREATED)
async def upload_acervo_image(
    id_acervo: int,
    image: UploadFile,
    s3_client=Depends(get_s3_client),
):
    ext = image.filename.split(".")[-1].lower()

    filename_with_ext = f"images/acervos/{id_acervo}.{ext}"

    return await upload_image_to_s3(
        image=image,
        s3_client=s3_client,
        filename_with_ext=filename_with_ext,
    )
