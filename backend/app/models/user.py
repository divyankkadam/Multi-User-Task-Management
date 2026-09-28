from __future__ import annotations
from typing import List 
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship 
from backend.app.db.session import Base

# DO NOT IMPORT TaskModel here!

class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    tasks: Mapped[List["TaskModel"]] = relationship(back_populates="user")

    categories: Mapped[List["CategoryModel"]] = relationship(back_populates="user", cascade="all, delete-orphan")