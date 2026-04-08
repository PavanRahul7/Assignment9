# app/database.py

import os
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, TIMESTAMP
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.sql import func

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/fastapi_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True)
    username   = Column(String(50),  nullable=False, unique=True)
    email      = Column(String(100), nullable=False, unique=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    calculations = relationship("Calculation", back_populates="user", cascade="all, delete")


class Calculation(Base):
    __tablename__ = "calculations"

    id        = Column(Integer, primary_key=True, index=True)
    operation = Column(String(20), nullable=False)
    operand_a = Column(Float,      nullable=False)
    operand_b = Column(Float,      nullable=False)
    result    = Column(Float,      nullable=False)
    timestamp = Column(TIMESTAMP,  server_default=func.now())
    user_id   = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="calculations")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
