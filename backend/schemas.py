from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime, date
from typing import Optional

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("username")
    @classmethod
    def username_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Username is required")
        return v.strip()

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    due_date: Optional[date] = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Title is required")
        return v.strip()

    @field_validator("priority")
    @classmethod
    def priority_valid(cls, v):
        if v not in ["low", "medium", "high"]:
            raise ValueError("Priority must be low, medium, or high")
        return v

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[date] = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip() if v else v

    @field_validator("status")
    @classmethod
    def status_valid(cls, v):
        if v is not None and v not in ["pending", "completed"]:
            raise ValueError("Status must be pending or completed")
        return v

    @field_validator("priority")
    @classmethod
    def priority_valid(cls, v):
        if v is not None and v not in ["low", "medium", "high"]:
            raise ValueError("Priority must be low, medium, or high")
        return v

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[date]
    created_at: datetime
    updated_at: Optional[datetime]
    user_id: int

    class Config:
        from_attributes = True
