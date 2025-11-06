from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime  # Correct import for datetime


# Base schema shared across all user types
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: Optional[str] = "user"


# For creating a new user (signup)
class UserCreate(UserBase):
    password: str  # plain password (will be hashed before storing)


# For reading a user (response model)
class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime  # Use datetime directly, not datetime.datetime


    class Config:
        orm_mode = True  # allows reading ORM objects directly


# For login requests
class UserLogin(BaseModel):
    email: EmailStr
    password: str
