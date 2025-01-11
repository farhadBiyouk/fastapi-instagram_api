from datetime import datetime
from pydantic import BaseModel
from .user import UserDisplay
from .post import PostDisplay


class CommentCreate(BaseModel):
	user_id: int
	post_id: int
	text: str


class CommentDisplay(BaseModel):
	id: int
	text: str
	timestamp: datetime
	user: UserDisplay
	post: PostDisplay
	
	class Config:
		orm_mode=True
