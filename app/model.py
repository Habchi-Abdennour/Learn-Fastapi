from datetime import datetime
from  sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP, text
from .database import Base

class Post(Base):
    __tablename__ ="posts"

    id=Column(Integer,primary_key=True)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,nullable=True,server_default=text("false"))
    created_at=Column(TIMESTAMP,nullable=True,server_default=text("now()"))
    # updated_at=Column(TIMESTAMP,nullable=False,onupdate=datetime.utcnow)