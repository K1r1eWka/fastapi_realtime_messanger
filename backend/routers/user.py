from fastapi import APIRouter, Cookie, Depends, Response, HTTPException, status
from sqlmodel import select # noqa
from backend.core.security import (
    hash_password,
    verify_password,
    create_access_token
)
from backend.core.config import security_settings   
import jwt # noqa
from backend.db.database import SessionDep, User

from backend.schemas.user import UserCreate, UserLogin



router = APIRouter()

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
async def register(data: UserCreate, session: SessionDep):

    statement = select(User).where(User.username == data.username)
    result = session.exec(statement)
    user = result.first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    # create a new user using User model (sqlmodel)
    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password)
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return {"message": "User registered successfully"}




@router.post("/login")
async def login(data: UserLogin, response: Response, session: SessionDep) -> dict[str, str]:

    statement = select(User).where(User.username == data.username)
    result = session.exec(statement)
    user = result.first()
    
    if not user: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid username or password"
            )
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid username or password"
            )

    token = create_access_token({"user_id": user.id, "username": user.username})

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax"
    )

    return {"message": "Login successful"}
    

# TODOneed to fix this dependencies function to protect all endpoints with JWT token
def get_current_user(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=401)

    payload = jwt.decode(access_token, security_settings.JWT_SECRET, algorithms=[security_settings.JWT_ALGORITHM])
    return payload["user_id"]


@router.get("/me")
def me(current_user: int = Depends(get_current_user)):
    return {"user_id": current_user}
