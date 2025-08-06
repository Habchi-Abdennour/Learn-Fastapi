from fastapi import Depends ,APIRouter ,HTTPException,status
from ..database import get_db
from sqlalchemy.orm import Session
from .. import model,schemas,oauth2
from   ..utils import  verify_password




router=APIRouter(
     prefix="/auth",
    tags=["authentication"]
)


@router.post('/login',response_model=schemas.Token)
def login(user_credentials:schemas.UserLogin,db:Session=Depends(get_db)):
    user=db.query(model.User).filter(model.User.email==user_credentials.email).first()
    if not user:
        raise HTTPException( status_code=status.HTTP_403_FORBIDDEN,
            detail="email does not exsist")
    
    if not verify_password(user_credentials.password,user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                detail="wrong pasword  or email")
    
    access_token=oauth2.create_access_token({"user_id":user.id})

    return {"access_token": access_token, "token_type": "bearer"}

