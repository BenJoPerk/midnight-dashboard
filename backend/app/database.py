import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

def get_database_url():
    return os.getenv("DATABASE_URL")

def get_engine():
    return create_engine(get_database_url())

def get_session_local():
    engine = get_engine()
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
