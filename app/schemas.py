from pydantic import BaseModel
from typing import Optional


class PostBase(BaseModel):
    title:str
    content:str

class PostCreate(PostBase):
    pass 

class PostResponse(PostBase):
    pass 

    class Config:
        orm_mode=True

class PostUpdate(PostBase):
    pass




class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str

class UserCreate(UserBase):
    password: str 

class UserResponse(UserBase):
    pass 

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class  TokenData(BaseModel):
    id: Optional[str] = None