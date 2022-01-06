from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from fastapi.params import Body
from sqlalchemy.util.deprecations import deprecated
from . import schemas, models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from .hashing import Hash


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['Blog'])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    newBlog = models.Blog(title=request.title, body=request.body)
    db.add(newBlog)
    db.commit()
    db.refresh(newBlog)
    return newBlog


@app.get('/blog', response_model=List[schemas.ShowBlog], tags=['Blog'])
def getAll(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['Blog'])
def getById(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            'detail': f"Blog with the id {id} is not available"})
    return blog


@app.delete('/blog/{id}', status_code=status.HTTP_200_OK, tags=['Blog'])
def delete(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="blog entry not found")
    blog.delete(synchronize_session=False)
    # blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    # db.delete(blog)
    db.commit()
    return 'deleted'


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED,tags=['Blog'])
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="not found")
    else:
        blog.update({'title': request.title, 'body': request.body})
        db.commit()
    return 'updated'


@app.get('/')
def getRoot():
    return "use sub-URI"



@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser, tags=['User'])
def createUser(request: schemas.User, db: Session = Depends(get_db)):
    newUser = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser


@app.get('/user/{id}', response_model=schemas.ShowUser, tags=['User'])
def getUserById(id: int, db: Session = Depends(get_db)):
	user = db.query(models.User).filter(models.User.id == id ).first()

	if not user: 
		raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
	return user