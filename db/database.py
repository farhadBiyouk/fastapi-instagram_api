from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine

SQLALCHEMY_DATABASE_URL = 'sqlite:///./insta.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
Session_local = sessionmaker(engine)
Base = declarative_base()


def get_db():
	db = Session_local()
	try:
		yield db
	finally:
		db.close()
