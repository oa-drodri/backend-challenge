from beanie import Document
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr


class User(Document):
    """Database user representation."""
    fullname: str
    email: EmailStr
    password: str
    role: str = "NORMAL"

    class Collection:
        name = "user"

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Admin",
                "email": "admin@admin.com",
                "password": "1234",
                "role": "ADMIN"
            }
        }


class UserSignIn(HTTPBasicCredentials):
    """Request user info representation"""
    class Config:
        schema_extra = {
            "example": {
                "username": "admin@admin.com",
                "password": "1234"
            }
        }


class UserData(BaseModel):
    """User info representation as admin endpoints response"""
    fullname: str
    email: EmailStr
    role: str

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Admin",
                "email": "admin@admin.com",
            }
        }
