from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Response
from schemas.post import PostCreate, PostDisplay
from schemas.user import UserDisplay
from sqlalchemy.orm.session import Session
from db.database import get_db
from db.models import User, Post
from datetime import datetime
from typing import List
from string import ascii_letters
from auth import oath2
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


@router.delete('/delete/{id}')
def delete_post(id: int, db: Session = Depends(get_db), current_user: UserDisplay = Depends(oath2.get_current_user)):
	post_obj = db.query(Post).filter(Post.id == id).first()
	if not post_obj:
		raise HTTPException(detail='post not found', status_code=status.HTTP_404_NOT_FOUND)
	if post_obj.user_id != current_user.id:
		raise HTTPException(detail='you do not have any permission for delete post, because not owner this post',
		                    status_code=status.HTTP_401_UNAUTHORIZED)
	
	db.delete(post_obj)
	db.commit()
	return Response(content='post deleted successfully', status_code=status.HTTP_204_NO_CONTENT)
