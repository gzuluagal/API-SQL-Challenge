from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = 'postgresql://postgres:password@localhost:5433/company_db'
engine = create_engine(DATABASE_URL)
local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()