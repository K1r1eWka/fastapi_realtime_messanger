from pydantic import BaseModel, Field

class User(BaseModel):
    id: int
    email: str
    username: str = Field(ge=3, le=50, example="username")
    password_hash: str

class UserRegister(BaseModel):
    email: str = Field(example="user@example.com")
    username: str = Field(ge=3, le=50, example="username")
    password: str = Field(example="password")

class UserLogin(BaseModel):
    email: str = Field(example="user@example.com")
    password: str = Field(example="password")

class UserOut(BaseModel):
    id: int 
    email: str = Field(example="user@example.com")
    username: str = Field(ge=3, le=50, example="username")
