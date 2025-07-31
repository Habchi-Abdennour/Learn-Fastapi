import time
from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel, Field
from .database import engine,SessionLocal,get_db
from . import model
from sqlalchemy.orm import Session

app = FastAPI()


model.Base.metadata.create_all(bind=engine)


class  Post(BaseModel):
    title:str
    content:str
    








@app.get("/")
async def run_tasks():
    
    return {"task1":"welcome to my endpoint"}



@app.get('/posts')
def get_post(db:Session=Depends(get_db)):
    
    posts=db.query(model.Post).all()

    return posts


@app.post('/posts',status_code=status.HTTP_201_CREATED)
def creat(post:Post,db:Session=Depends(get_db)):
    creat_item=model.Post(**post.dict())
    db.add(creat_item)
    db.commit()
    db.refresh(creat_item)
    
    return creat_item



@app.get("/post/lates")
def lates_post(db:Session=Depends(get_db)):
    last_post=db.query(model.Post).order_by(model.Post.created_at.desc()).limit(1).all()
    print(last_post)
    # post=posts_stack[len(posts_stack)-1]
    return last_post


@app.get('/post/{id}')
def get_post_by_id(id:int,response:Response,db:Session=Depends(get_db)):
    get_post=db.query(model.Post).filter(model.Post.id==id).first()

    if not get_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'the post with this id: {id} was not found')

   
    return get_post

@app.delete('/delete/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int,db:Session=Depends(get_db)):
    deleted_post=db.query(model.Post).filter(model.Post.id==id).first()
    
    if  deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'the post with this id: {id} was not found')
    db.delete(deleted_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/update/{id}")
def update_post(id:int,post:Post,db:Session=Depends(get_db)):
    post_query=db.query(model.Post).filter(model.Post.id==id)
    index=post_query.first()

    if  index == None   :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'the post with this id: {id} was not found')
    
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return {"message": "Post updated successfully", "post": post_query.first()}