from pydantic import BaseModel


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