from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core import Config

DATABASE_URL = Config.DATABASE_URL
engine = create_engine(DATABASE_URL)
Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


def get_database():
    database = Session()
    try:
        yield database
    finally:
        database.close()
