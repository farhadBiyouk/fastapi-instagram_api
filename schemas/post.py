from datetime import datetime

from pydantic import BaseModel
from .user import UserDisplayPost,UserDisplay


class PostCreate(BaseModel):
	image_url: str
	image_url_type: str
	caption: str
	user_id: int


class PostDisplay(BaseModel):
	id: int
	image_url: str
	image_url_type: str
	caption: str
	timestamp: datetime
	user_id: UserDisplay
