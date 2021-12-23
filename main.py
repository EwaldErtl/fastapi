from typing import Optional
from fastapi import FastAPI


app = FastAPI()


@app.get('/blog')
def index(limit:int=10, published:bool=False, sort: Optional[str] = None):
    if published:
        return {'data': f'published blog list {limit}' }
    else:
        return {'data': f'blog list {limit}' }

@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'unpublished'}


@app.get('/blog/{id}')
def about(id: int):
    return {'data': id }

@app.get('/blog/{id}/comments')
def comments(id: int): 
    return {'data': {'comments': {'1' :  'comment'}}}
