import asyncio
from http import HTTPStatus
from sys import platform

from fastapi import FastAPI

from biblio_fzs_backend.routers.users import fastapi_users, router
from biblio_fzs_backend.schemas.root_schemas import Message
from biblio_fzs_backend.schemas.users_schemas import UserPublic, UserSchema
from biblio_fzs_backend.security.user_settings import auth_backend

if platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


app = FastAPI(title="Meu Bairro API")
app.include_router(router)

app.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=False),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserPublic, UserSchema),
    prefix="/users",
    tags=["users"],
)
app.include_router(
    fastapi_users.get_users_router(
        UserPublic, UserSchema, requires_verification=False
    ),
    prefix="/users",
    tags=["users"],
)


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Meu Bairro. Conecte-se com a sua comunidade"}
