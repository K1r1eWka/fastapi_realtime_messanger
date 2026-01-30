from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(max_length=100)
    email: str = Field(max_length=100)
    password_hash: str = Field(max_length=100)  
