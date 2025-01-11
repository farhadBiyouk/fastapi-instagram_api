import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from schemas.comment import CommentDisplay, CommentCreate

from sqlalchemy.orm.session import Session
from db.database import get_db
from db.models import User, Comment
from schemas.user import UserDisplay
from auth import oath2

router = APIRouter(prefix='/comment', tags=['comment'])


@router.post('/create', response_model=CommentDisplay)
def create_comment(request: CommentCreate, db: Session = Depends(get_db)):
	new_comment = Comment(
		post_id=request.post_id,
		user_id=request.user_id,
		text=request.text,
		timestamp=datetime.datetime.now()
	)
	
	db.add(new_comment)
	db.commit()
	db.refresh(new_comment)
	return new_comment


@router.get('/{post_id}', response_model=CommentDisplay)
def get_comment_by_post_id(post_id: int, db: Session = Depends(get_db)):
	db_post = db.query(Comment).filter(Comment.post_id == post_id).first()
	if not db_post:
		raise HTTPException(detail='comment not found', status_code=status.HTTP_404_NOT_FOUND)
	
	return db_post


@router.delete('/delete/{comment_id}')
def del_comment(comment_id: int, db: Session = Depends(get_db),
                current_user: UserDisplay = Depends(oath2.get_current_user)):
	db_post = db.query(Comment).filter(Comment.id == comment_id).first()
	if not db_post:
		raise HTTPException(detail='comment not found', status_code=status.HTTP_404_NOT_FOUND)
	
	if db_post.user_id == current_user.id or db_post.post.user_id == current_user.id:
		db.delete(db_post)
		db.commit()
		return 'ok'
	raise HTTPException(detail='operation have error', status_code=status.HTTP_400_BAD_REQUEST)
