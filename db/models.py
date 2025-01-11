from db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship


class User(Base):
	__tablename__ = 'user'
	
	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, unique=True, nullable=False)
	email = Column(String, unique=True, nullable=False)
	password = Column(String, nullable=False)
	posts = relationship('Post', back_populates='user')


class Post(Base):
	__tablename__ = 'post'
	id = Column(Integer, primary_key=True, index=True)
	image_url = Column(String)
	image_url_type = Column(String)
	caption = Column(Text)
	timestamp = Column(DateTime)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship('User', back_populates='posts')
