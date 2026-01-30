from sqlmodel import SQLModel, Field

class ChatMember(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    chat_id: int = Field(foreign_key="chat.id")
    user_id: int = Field(foreign_key="user.id")