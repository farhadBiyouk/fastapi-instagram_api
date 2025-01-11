from pydantic import BaseModel
from user import UserDisplayPost


class PostCreate(BaseModel):
	image_url: str
	image_url_type: str
	caption: str
	creator_id: int


class PostDisplay(BaseModel):
	id: int
	image_url: str
	image_url_type: str
	caption: str
	creator_id: int
	user: UserDisplayPost
