from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from db.database import get_db
from db.models import User
from utils.hash_password import HashPassword
from auth import oath2

router = APIRouter(tags=['Authentication-JWT'])


@router.post('/token')
def get_token(request: OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
	db_user = db.query(User).filter(User.username==request.username).first()
	if not db_user:
		raise HTTPException(detail='user not found', status_code=status.HTTP_404_NOT_FOUND01_UNAUTHORIZED)
	if not HashPassword.verify(db_user.password, request.password):
		raise HTTPException(detail='invalid auth', status_code=status.HTTP_401_UNAUTHORIZED)
	access_token = oath2.create_access_token(data={'sub': request.username})
	
	return {
		'access_token': access_token,
		'token_type': 'bearer',
		'user_id': db_user.id,
		'username': db_user.username
	}