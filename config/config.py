from typing import Optional

from beanie import init_beanie
from database.database import add_user
from models.admin import User
from models.ecg import ExecutionData, ExecutionStatus, Lead
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from pydantic import BaseSettings


class Settings(BaseSettings):
    # database configurations
    DATABASE_URL: Optional[str] = None

    # JWT
    secret_key: str
    algorithm: str = "HS256"

    class Config:
        env_file = ".env"
        orm_mode = True


async def initiate_database():
    client = AsyncIOMotorClient(Settings().DATABASE_URL)
    await init_beanie(
        database=client.get_default_database(),
        document_models=[User, ExecutionData, ExecutionStatus, Lead]
    )
    hash_helper = CryptContext(schemes=["bcrypt"])
    admin_user = User(
        fullname="Admin",
        email="admin@admin.com",
        password=hash_helper.encrypt("1234"),
        role="ADMIN"
    )
    admin_user = await add_user(admin_user)
