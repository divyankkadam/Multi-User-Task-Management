from __future__ import annotations
from datetime import datetime
from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship 
from sqlalchemy.sql import func
from backend.app.db.session import Base

# DO NOT IMPORT CategoryModel or UserModel here!

class TaskModel(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(250))
    is_completed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=func.now())

    # Foreign Keys
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("category.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    user: Mapped["UserModel"] = relationship(back_populates="tasks")
    category: Mapped[Optional["CategoryModel"]] = relationship(back_populates="tasks")
