from datetime import datetime
from sqlmodel import SQLModel, Field

class Message(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    chat_id: int = Field(index=True)
    user_id: int = Field(index=True)
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)