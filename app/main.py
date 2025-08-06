from fastapi import FastAPI 
from .database import engine
from . import model
from .routers import posts, users,auth




app = FastAPI(
    title="FastAPI Blog",
    description="A simple blog API built with FastAPI",
    version="1.0.0"
)


model.Base.metadata.create_all(bind=engine)



@app.get("/")
async def run_tasks():
    
    return {"task1":"welcome to my endpoint"}


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
