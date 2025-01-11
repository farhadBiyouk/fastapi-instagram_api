from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user import UserCreate, UserDisplay
from utils.hash_password import HashPassword
from sqlalchemy.orm.session import Session
from db.database import get_db
from db.models import User

router = APIRouter(prefix='/user', tags=['user'])


@router.post('/create', response_model=UserDisplay)
def create_user(reqeust: UserCreate, db: Session = Depends(get_db)):
	user = db.query(User).filter(User.email == reqeust.email).first()
	if user:
		raise HTTPException(detail='user already exists', status_code=status.HTTP_400_BAD_REQUEST)
	new_user = User(username=reqeust.username, email=reqeust.email, password=HashPassword.bcrypt(reqeust.password))
	db.add(new_user)
	db.commit()
	db.refresh(new_user)
	
	return new_user
