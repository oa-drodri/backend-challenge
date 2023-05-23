from http.client import HTTPException
from fastapi import APIRouter, Body, Depends

from auth.jwt_bearer import JWTBearer
from auth.jwt_handler import decode_jwt

from database.database import *
from models.ecg import *

router = APIRouter()

token_listener = JWTBearer()


@router.post("/", response_description="Queue a new ECG processing", response_model=Response)
async def queue_execution(execution: ExecutionData = Body(...), token: str = Depends(token_listener)):
    print(decode_jwt(token))
    new_execution = await add_execution(execution, user_id=decode_jwt(token).get("user_id"))
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "ECG execution created successfully",
        "execution_id": new_execution.id
    }
   
   
@router.get("/{id}", response_description="Execution status retrieved", response_model=Response)
async def get_execution_status(id: PydanticObjectId, token: str = Depends(token_listener)):
    execution = await retrieve_execution(id)
    if execution:
        if execution.user.email == decode_jwt(token).get("user_id"):
            return {
                "status_code": 200,
                "response_type": "success",
                "description": "Execution status retrieved successfully",
                "data": execution
            }
        else:
            raise HTTPException(status_code=403, detail="Invalid user authorization")
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Execution doesn't exist"
    }