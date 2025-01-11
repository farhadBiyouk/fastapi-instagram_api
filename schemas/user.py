from pydantic import BaseModel


class UserBase(BaseModel):
	username: str
	email: str


class UserCreate(UserBase):
	password: str


class UserDisplayPost(BaseModel):
	username: str
	
	class Config:
		orm_mode = True


class UserDisplay(UserBase):
	id: int
	
	class Config:
		orm_mode = True
