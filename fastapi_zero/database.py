from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# cria banco SQLite
DATABASE_URL = "sqlite:///./todo.db"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
