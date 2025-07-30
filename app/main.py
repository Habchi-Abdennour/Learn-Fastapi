import time
from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel, Field
import psycopg2
from psycopg2.extras import RealDictCursor
 
app = FastAPI()

while True:

    try:
        
        # Connect to your postgres DB
        conn =psycopg2.connect(host='localhost',dbname='fastapi' ,user="postgres" ,password="123"
            ,cursor_factory=RealDictCursor)
        # Open a cursor to perform database operations
        cur = conn.cursor()
        print("seccsfull connection")
        break

    except Exception as error:
        print("faild to connect")
        print(error)
        time.sleep(2)



# def findpost(id):
#     for post in posts_stack:
#         if post["id"] == id:
#             return {"post": post}

# def find_indice_post(id):
#         for i, post in enumerate(posts_stack):
#             if post["id"] == id:
#                 return i
#         return None

class  Post(BaseModel):
    title:str
    content:str
    



@app.get("/")
async def run_tasks():
    
    return {"task1":"welcome to my endpoint"}



@app.get('/posts')
def get_post():
    cur.execute("SELECT * FROM posts")
    posts=cur.fetchall()
    return {"data":posts}


@app.post('/posts',status_code=status.HTTP_201_CREATED)
def creat(post:Post):
    cur.execute("""insert into posts (title,content) values (%s,%s) RETURNING * """,
                (post.title,post.content))
    new_post=cur.fetchone()
    # Make the changes to the database persistent
    conn.commit()
    # posts_stack.append(new_post.dict())
    context={
        'data':new_post,
    }
    return context



@app.get("/post/lates")
def lates_post():
    cur.execute("""select * from posts order by create_at  desc limit 1""")
    last_post=cur.fetchone()
    # post=posts_stack[len(posts_stack)-1]
    return last_post


@app.get('/post/{id}')
def get_post_by_id(id:int,response:Response):
    cur.execute("""select * from posts where id=%s""",(str(id)))
    get_it=cur.fetchone()
    # get_it=findpost(id)
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
    cur.execute("""delete  from posts where id =%s RETURNING *""",(str(id)),)
    deleted_post=cur.fetchone()
    print(deleted_post)
    conn.commit()
    
    
    if  deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'the post with this id: {id} was not found')

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/update/{id}")
def update_post(id:int,post:Post):
    cur.execute("""update posts set title=%s ,content=%s  where  id=%s RETURNING *""",
        (post.title,post.content,str(id)))
    index=cur.fetchone()
    conn.commit()
    # index=find_indice_post(id)
    if  index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'the post with this id: {id} was not found')
    
    # post_dict=post.dict()
    # posts_stack[index]=post_dict
    return {"data":post}