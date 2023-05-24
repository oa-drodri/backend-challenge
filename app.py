from fastapi import FastAPI

from config.config import initiate_database
from routes.admin import router as AdminRouter
from routes.ecg import router as EcgRouter

app = FastAPI()


@app.on_event("startup")
async def start_database():
    await initiate_database()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app."}


app.include_router(AdminRouter, tags=["Administrator"], prefix="/user")
app.include_router(EcgRouter, tags=["ECG"], prefix="/ecg")
