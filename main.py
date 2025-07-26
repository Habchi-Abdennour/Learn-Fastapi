from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
app = FastAPI()

class  Post(BaseModel):
    title:str
    content:str
    published:bool =True
    rating:Optional[int]=None


@app.get("/")
async def run_tasks():
    
    return {"task1":"welcome to my endpoint"}


@app.post('/creatpost')
def creat(new_post:Post):
    
    context={
        "data":new_post
    }
    return context
