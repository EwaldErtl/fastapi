from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

app = FastAPI()


class Blog(BaseModel):
    title: str
    body: str
    publishedAt: Optional[bool]


@app.get('/blog')
def index(limit: int = 10, published: bool = False, sort: Optional[str] = None):
    if published:
        return {'data': f'published blog list {limit}'}
    else:
        return {'data': f'blog list {limit}'}


@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'unpublished'}


@app.get('/blog/{id}')
def about(id: int):
    return {'data': id}


@app.get('/blog/{id}/comments')
def comments(id: int):
    return {'data': {'comments': {'1':  'comment'}}}


@app.post('/blog/')
def createBlog(request: Blog):
    return {'data':  f'blog is created with {request.title}'}

#if __name__ == "__main__":
#    uvicorn.run(app, host="127.0.0.1", port=8000)