from fastapi import FastAPI,Response,status,HTTPException,Depends
from .database import engine,get_db
from . import model
from sqlalchemy.orm import Session
from . import schemas

app = FastAPI()


model.Base.metadata.create_all(bind=engine)


@app.get("/")
async def run_tasks():
    
    return {"task1":"welcome to my endpoint"}



@app.get('/posts',response_model=list[schemas.PostResponse])
def get_all_posts(db:Session=Depends(get_db)):
    
    posts=db.query(model.Post).all()

    return posts


@app.post('/posts',status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def creat(post:schemas.PostCreate,db:Session=Depends(get_db)):
    creat_item=model.Post(**post.dict())
    db.add(creat_item)
    db.commit()
    db.refresh(creat_item)
    
    return creat_item



@app.get("/post/latest",response_model=schemas.PostResponse)
def latest_post(db:Session=Depends(get_db)):
    last_post=db.query(model.Post).order_by(model.Post.created_at.desc()).first()
    print(last_post)
    return last_post


@app.get('/post/{id}',response_model=schemas.PostResponse)
def get_post_by_id(id:int,db:Session=Depends(get_db)):
    get_post=db.query(model.Post).filter(model.Post.id==id).first()

    if not get_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'the post with this id: {id} was not found')

   
    return get_post

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int,db:Session=Depends(get_db)):
    deleted_post=db.query(model.Post).filter(model.Post.id==id).first()
    
    if  deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'the post with this id: {id} was not found')
    db.delete(deleted_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}",response_model=schemas.PostResponse)
def update_post(id:int,post:schemas.PostUpdate,db:Session=Depends(get_db)):
    post_query=db.query(model.Post).filter(model.Post.id==id)
    index=post_query.first()

    if  index == None   :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'the post with this id: {id} was not found')
    
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return  post_query.first()

@app.get('/users',response_model=list[schemas.UserResponse])
def get_all_users(db:Session=Depends(get_db)):
    users=db.query(model.User).all()
    return users

@app.post('/users',status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse) 
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    new_user=model.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user