from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from backend.db.database import get_session

# Dependencie injection for database session
SessionDep = Annotated[Session, Depends(get_session)]