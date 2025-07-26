from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()



@app.get("/")
async def run_tasks():
    
    return {"task1":"welcome to my endpoint"}

@app.post('/creatpost')
def creat(payload:dict=Body(...)):
    context={
        "title ":payload["title"],
        "content ":payload["content"]
    }
    return context
