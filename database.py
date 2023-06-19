import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import text
from dotenv import dotenv_values

if hasattr(sys, '_called_from_test'):
    SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"
elif 'DATABASE_URL' in os.environ:
    SQLALCHEMY_DATABASE_URL = os.environ['DATABASE_URL']
else:
    config = dotenv_values('.env')
    SQLALCHEMY_DATABASE_URL = config['DATABASE_DSN']


engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

BaseModel = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


try:
    db = next(get_db())
    db.execute(text('SELECT 1'))
except Exception as e:
    raise SystemExit(
        "DB connection has issues. please read the Readme.md file")
