from fastapi import HTTPException, status
from sqlmodel import Session, select

from backend.models.user import User
from backend.schemas.user import UserCreate
from backend.core.security import hash_password

class UserService:
    def __init__(self, session: Session):
        self.session = session

    # service to register new user, we pass only credentials and use it for creating new user and also we hashing the password
    async def register_new_user(self, credentials: UserCreate) -> dict:
        statement = select(User).where(User.username == credentials.username)
        result = self.session.exec(statement)
        user = result.first()

        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )
        new_user = User(
            **credentials.model_dump(exclude=["password"]),
            password_hash=hash_password(credentials.password)
        )
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
    
        return {"message": "User registered successfully"}
    
