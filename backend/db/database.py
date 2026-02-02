from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine

from backend.models.user import User
from backend.models.message import Message
# from backend.models.chat import Chat
# from backend.models.chat_member import ChatMember

from backend.core.config import db_settings

DATABASE_URL = f"postgresql://{db_settings.POSTGRES_USER}:{db_settings.POSTGRES_PASSWORD}@{db_settings.POSTGRES_SERVER}:{db_settings.POSTGRES_PORT}/{db_settings.POSTGRES_NAME}"
engine = create_engine(DATABASE_URL, echo=True)


SQLModel.metadata.create_all(engine)

# create a session generator 
def get_session():
    with Session(engine) as session:
        yield session



