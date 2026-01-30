from sqlmodel import SQLModel, Field

class Chat(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    is_private: bool = Field(default=True)

