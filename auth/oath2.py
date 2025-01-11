from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm.session import Session
from datetime import datetime, timedelta, timezone
from jose import jwt
from db.database import get_db
from db.models import User
from jose.exceptions import JWTError

SECRET_KEY = "8eb6784ba6e58c56b89feace1dc8313469c697538f4eb0773de92c8ffdbe7a9e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.now(timezone.utc) + expires_delta
	else:
		expire = datetime.now(timezone.utc) + timedelta(minutes=15)
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
	try:
		data_fetch = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
		username = data_fetch.get('sub')
		if not username:
			raise HTTPException(detail='invalid auth', status_code=status.HTTP_401_UNAUTHORIZED)
	except JWTError:
		raise HTTPException(detail='invalid auth', status_code=status.HTTP_401_UNAUTHORIZED)
	
	user = db.query(User).filter(User.username == username).first()
	if user is None:
		raise HTTPException(detail='invalid auth', status_code=status.HTTP_401_UNAUTHORIZED)
	return user
