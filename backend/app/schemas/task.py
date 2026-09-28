from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field , ConfigDict

from backend.app.schemas.category import CategoryResponse


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=250)
    category_id: int | None = None

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=250)
    is_completed: Optional[bool] = None
    category_id: Optional[int] = None

    model_config = ConfigDict(extra="ignore")
    
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    is_completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    user_id: int

    # Optional: Nested category details if fetched via a joined query
    category: Optional[CategoryResponse] = None 

    class Config:
        from_attributes = True
