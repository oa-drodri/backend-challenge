from beanie import Document
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr


class User(Document):
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
    class Config:
        schema_extra = {
            "example": {
                "username": "admin@admin.com",
                "password": "1234"
            }
        }


class UserData(BaseModel):
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
