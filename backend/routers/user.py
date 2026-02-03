from fastapi import APIRouter, Cookie, Depends, Response, HTTPException, status
from sqlmodel import select # noqa
from backend.core.security import (
    hash_password,
    verify_password,
    create_access_token
)
from backend.core.config import security_settings   
import jwt # noqa
from backend.db.database import User
from backend.dependencies import SessionDep, UserServiceDep

from backend.schemas.auth import UserLogin, UserRegister
from backend.schemas.user import UserCreate



router = APIRouter(tags=["User"])

@router.get("/all_users")
async def all_users(session: SessionDep):
    statement = select(User)
    users = session.exec(statement).all()
    return [
        {
            "id": user.id,
            "username": user.username
        }
        for user in users
    ]



@router.post("/register")
async def register(data: UserCreate, service: UserServiceDep):
    return await service.register_new_user(data)


@router.post("/login")
async def login(data: UserLogin, response: Response, service: UserServiceDep) -> dict[str, str]:
    return await service.login_user(data, response)
    
    
    

# TODO need to fix this dependencies function to protect all endpoints with JWT token
def get_current_user(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=401)

    payload = jwt.decode(access_token, security_settings.JWT_SECRET, algorithms=[security_settings.JWT_ALGORITHM])
    return payload["user_id"]


@router.get("/me")
def me(current_user: int = Depends(get_current_user)):
    return {"user_id": current_user}
