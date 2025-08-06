from fastapi import HTTPException,Depends,status,APIRouter
from jose import JWTError,jwt
from datetime import datetime,timedelta
from .  import  schemas
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme=OAuth2PasswordBearer(tokenUrl="auth/login")

ALGORITHM="HS256"
SECRET_KEY="3fdf06379f2c95e3f1ee850b19dd8c17458f402a96b3f12956a5d46fe24d1b57"
ACCESS_TOKEN_EXPIRE_MINUTES=60

router=APIRouter(
    tags=["authentication"]
)

@router.post("/login")
def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def verify_access_token(Token:str,credentials_exception):
    try:
        payload=jwt.decode(Token,SECRET_KEY,algorithms=[ALGORITHM])
        id:int = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))  # Convert id to string
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(Token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(Token, credentials_exception)