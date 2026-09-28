from pydantic import BaseModel, Field, EmailStr



class CreateUser(BaseModel):
    username : str = Field(..., min_length=3 , max_length=50)
    email: EmailStr = Field(..., description="Email ID of the user")
    password: str = Field(..., min_length=6 , max_length=255, description="Strong password") 

class UserResponse(BaseModel):
    id: int
    username : str
    email: EmailStr

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Stores the payload payload parsed from a verified JWT token."""
    username: str | None = None