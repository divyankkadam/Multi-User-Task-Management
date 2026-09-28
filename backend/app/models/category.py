from __future__ import annotations  # Prevents runtime type evaluation errors
from typing import List 
from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship 
from backend.app.db.session import Base

# DO NOT IMPORT TaskModel here!

class CategoryModel(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100),  nullable=False)

    # Foreign Key
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    # SQLAlchemy maps string names perfectly at runtime
    tasks: Mapped[List["TaskModel"]] = relationship(back_populates="category")
    user:Mapped["UserModel"] = relationship(back_populates="categories")

    # uniqueness *per user* so a single user cannot duplicate "Work"
    __table_args__ = (
        UniqueConstraint("name", "user_id", name="uq_category_name_user_id"),
    )

