from db.database import Base
from sqlalchemy import Column, Integer, String


class UserBase(Base):
	__tablename__ = 'user'
	
	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, unique=True, nullable=False)
	email = Column(String, unique=True, nullable=False)
	password = Column(String, nullable=False)
