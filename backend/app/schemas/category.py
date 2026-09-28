from pydantic import BaseModel , Field


class CategoryCreate(BaseModel):

    name : str = Field(min_length=1, max_length=100, examples=["Work", "Personal"])


class CategoryResponse(BaseModel):

    id : int
    name : str 
    user_id : int

    class Config:
        from_attributes = True  # Allows Pydantic to read SQLAlchemy objects directly
        