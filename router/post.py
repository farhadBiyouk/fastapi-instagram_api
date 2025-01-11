from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from schemas.post import PostCreate, PostDisplay
from sqlalchemy.orm.session import Session
from db.database import get_db
from db.models import User, Post
from datetime import datetime
from typing import List
from string import ascii_letters
import shutil
import random

router = APIRouter(prefix='/post', tags=['post'])

valid_image_url_type = ['url', 'uploaded']


@router.post('/create', response_model=PostDisplay)
def create_post(request: PostCreate, db: Session = Depends(get_db)):
	new_post = Post(
		image_url=request.image_url,
		image_url_type=request.image_url_type,
		caption=request.caption,
		timestamp=datetime.now(),
		user_id=request.user_id
	)
	if new_post.image_url_type not in valid_image_url_type:
		raise HTTPException(detail='image url type invalid, must be select url or uploaded',
		                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
	db.add(new_post)
	db.commit()
	db.refresh(new_post)
	
	return new_post


@router.get('/', response_model=List[PostDisplay])
def all_post(db: Session = Depends(get_db)):
	posts = db.query(Post).all()
	return posts


@router.post('/upload-file')
def upload_file(file: UploadFile = File(...)):
	rand_name = ''.join(random.choice(ascii_letters) for _ in range(6))
	new_name = f'_{rand_name}.'.join(file.filename.rsplit('.', 1))
	path = f'upload_files/{new_name}'
	with open(path, 'w+b') as buffer:
		shutil.copyfileobj(file.file, buffer)
	
	return {'path': path}
