from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas
from ..database import get_db
from sqlalchemy.orm import Session
from .. import model
from ..utils import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)






@router.get('/',response_model=list[schemas.UserResponse])
def get_all_users(db:Session=Depends(get_db)):
    users=db.query(model.User).all()
    return users

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse) 
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    if db.query(model.User).filter(model.User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already registered")
    
    user.password=hash_password(user.password)
    new_user=model.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user