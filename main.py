from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel, Field


app = FastAPI()

def findpost(id):
    for post in posts_stack:
        if post["id"] == id:
            return {"post": post}

def find_indice_post(id):
        for i, post in enumerate(posts_stack):
            if post["id"] == id:
                return i
        return None

class  Post(BaseModel):
    id: int
    title:str
    content:str
    published:bool =True
    rating:Optional[float]=None


posts_stack=[
    { "id": 1,
        "title": "dz",
        "content": "setif",
        "published": True,
        "rating": 4.5
        },
        {
        "id": 2,
        "title": "dz",
        "content": "djelfa",
        "published": True,
        "rating": 3.75
        },
        {
        "id": 3,
        "title": "dz",
        "content": "algers",
        "published": False,
        "rating": 5
        },
         {
        "id": 4,
        "title": "dz",
        "content": "adrare",
        "published": False,
        "rating": 2.5
        },
        {
        "id": 5,
        "title": "dz",
        "content": "laghout",
        "published": False,
        "rating": 3.5
        }
]

@app.get("/")
async def run_tasks():
    
    return {"task1":"welcome to my endpoint"}



@app.get('/posts')
def get_post():
    return {"data":posts_stack}


@app.post('/posts',status_code=status.HTTP_201_CREATED)
def creat(new_post:Post):
    posts_stack.append(new_post.dict())
    context={
        'data':"successful post"
    }
    return context



@app.get("/post/lates")
def lates_post():
    post=posts_stack[len(posts_stack)-1]
    return post


@app.get('/post/{id}')
def get_post_by_id(id:int,response:Response):
    get_it=findpost(id)
    if not get_it:
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return f'the post with this id: {id} does not exist'
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'the post with this id: {id} was not found')


    context={
        "post detail":get_it
    }
    return context

@app.delete('/delete/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    find_it=find_indice_post(id)
    if  find_it is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'the post with this id: {id} was not found')
    posts_stack.pop(find_it)

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/update/{id}")
def update_post(id:int,post:Post):
    index=find_indice_post(id)
    if  index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'the post with this id: {id} was not found')
    
    post_dict=post.dict()
    posts_stack[index]=post_dict
    return {"detail":post}