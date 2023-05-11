from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime
from uuid import uuid4 as uuid

class Post(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    published: Optional[bool] = False
    published_at: Optional[datetime]
    created_at: Optional[datetime] = datetime.now()

app = FastAPI()

posts = [{
  "id": "dd637e41-6f49-458e-adfc-dc9f68bfb1a5",
  "title": "My firts post",
  "author": "Bamio Dev",
  "content": "Some content UPDATEEED...",
  "published": True,
  "published_at": "2023-05-09T15:10:10.028070",
  "created_at": "2023-05-10T19:47:18.406508"
}]

@app.get("/")
async def root():
    return { "welcome": "Welcome to my Rest API" }

@app.get("/posts")
async def get_posts():
    return posts

@app.get("/posts/{id}")
async def get_post(id: str):

    for post in posts:
        if post["id"] == id:
            return post

    raise HTTPException(status_code=404, detail="Post not found")

@app.post("/posts")
async def save_post(post: Post):
    post.id = str(uuid())
    posts.append(post.dict())

    return posts[-1]

@app.put("/posts/{id}")
async def put_post(id: str, updated_post: Post):
    for index, post in enumerate(posts):
        if post["id"] == id:
            posts[index]["title"] = updated_post.dict()["title"]
            posts[index]["author"] = updated_post.dict()["author"]
            posts[index]["content"] = updated_post.dict()["content"]
            return {"message": "Post has been updated succesfully"}

    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/posts/{id}")
async def delete_post(id: str):
    for index, post in enumerate(posts):
        if post["id"] == id:
            posts.pop(index)
            return {"message": "Post has been deleted succesfully"}
        
    raise HTTPException(status_code=404, detail="Item not found")
