from db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime


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
	comments = relationship('Comment', back_populates='post')


class Comment(Base):
	__tablename__ = 'comment'
	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey('user.id'))
	post_id = Column(Integer, ForeignKey('post.id'))
	text = Column(Text)
	timestamp = Column(DateTime, default=datetime.now())
	
	user = relationship('User')
	post = relationship('Post', back_populates='comments')
