from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from backend.db.database import get_session

from backend.services.user import UserService

# Dependencie injection for database session
SessionDep = Annotated[Session, Depends(get_session)]


# Dependencie injection for User service, it needed to oreder to not to write 
# all time UserSerevice and pass Session injection to user service
def get_user_service(session: SessionDep):
    return UserService(session)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]

