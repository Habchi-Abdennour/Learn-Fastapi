from fastapi import APIRouter, Response
from .. import schemas
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from .. import model,oauth2




router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)



@router.get('',response_model=list[schemas.PostResponse])
def get_all_posts(db:Session=Depends(get_db),user_id:schemas.TokenData=Depends(oauth2.get_current_user)):
    
    posts=db.query(model.Post).all()

    return posts


@router.post('',status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def creat(post:schemas.PostCreate,db:Session=Depends(get_db),user_id:schemas.TokenData=Depends(oauth2.get_current_user)):
    creat_item=model.Post(**post.dict())
    db.add(creat_item)
    db.commit()
    db.refresh(creat_item)
    
    return creat_item



@router.get("/latest",response_model=schemas.PostResponse)
def latest_post(db:Session=Depends(get_db),user_id:schemas.TokenData=Depends(oauth2.get_current_user)):
    last_post=db.query(model.Post).order_by(model.Post.created_at.desc()).first()
    return last_post


@router.get('/{id}',response_model=schemas.PostResponse)
def get_post_by_id(id:int,db:Session=Depends(get_db),user_id:schemas.TokenData=Depends(oauth2.get_current_user)):
    get_post=db.query(model.Post).filter(model.Post.id==id).first()

    if not get_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'the post with this id: {id} was not found')

   
    return get_post

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int,db:Session=Depends(get_db),user_id:schemas.TokenData=Depends(oauth2.get_current_user)):
    deleted_post=db.query(model.Post).filter(model.Post.id==id).first()
    
    if  deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'the post with this id: {id} was not found')
    db.delete(deleted_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}",response_model=schemas.PostResponse)
def update_post(id:int,post:schemas.PostUpdate,db:Session=Depends(get_db),user_id:schemas.TokenData=Depends(oauth2.get_current_user)):
    post_query=db.query(model.Post).filter(model.Post.id==id)
    index=post_query.first()

    if  index == None   :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'the post with this id: {id} was not found')
    
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return  post_query.first()