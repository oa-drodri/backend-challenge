from auth.jwt_bearer import JWTBearer
from auth.jwt_handler import decode_jwt
from beanie import PydanticObjectId
from celery import Celery
from database.database import add_execution, retrieve_execution
from fastapi import APIRouter, Body, Depends, HTTPException
from models.ecg import ExecutionData, Response

router = APIRouter()

token_listener = JWTBearer()

celery_app = Celery('worker', broker='amqp://guest:guest@rabbitmq:5672//')


@router.post(
    "/",
    response_description="Queue a new ECG processing",
    response_model=Response
)
async def queue_execution(
    execution: ExecutionData = Body(...),
    token: str = Depends(token_listener)
):
    """Allows authenticated and authorized user
    to queue a execution providing the ECG data

    Args:
        execution (ExecutionData, optional): ECG data.
        Defaults to Body(...).
        token (str, optional): User's token. Defaults to
        Depends(token_listener).

    Raises:
        HTTPException: 403 indicates that authenticated user is not authorized

    Returns:
        dict: http response generated when execution is queued, providing the
        execution id
    """
    user = decode_jwt(token)
    if user.get("role") != "ADMIN":
        new_execution = await add_execution(
            execution, user_id=user.get("user_id")
        )
        celery_app.send_task(
            "worker.process_execution",
            args=[str(new_execution.id)]
        )
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "ECG execution created successfully",
            "execution_id": new_execution.id
        }
    else:
        raise HTTPException(
            status_code=403,
            detail="Admin user cannot queue ECG processing"
        )


@router.get(
    "/{id}",
    response_description="Execution status retrieved",
    response_model=Response
)
async def execution_status(
    id: PydanticObjectId,
    token: str = Depends(token_listener)
):
    """Allows authenticated and authorized users to query the state from
    an executed queried.

    Args:
        id (PydanticObjectId): execution id
        token (str, optional): User's token. Defaults to Depends(token_
        listener).

    Raises:
        HTTPException: 403 indicates that authenticated user is not authorized.
        HTTPException: 404 execution id provided does not corresponds to any
        execution.

    Returns:
        dict: Execution status info
    """
    user = decode_jwt(token)
    if user.get("role") != "ADMIN":
        execution = await retrieve_execution(id)
        if execution:
            if execution.user.email == user.get("user_id"):
                return {
                    "status_code": 200,
                    "response_type": "success",
                    "description": "Execution status retrieved successfully",
                    "data": {
                        "result": execution.result,
                        "status": execution.status
                        }
                }
            else:
                raise HTTPException(
                    status_code=403,
                    detail="Invalid user authorization"
                )
    else:
        raise HTTPException(
            status_code=403,
            detail="Admin user cannot queue ECG processing"
        )
    raise HTTPException(
        status_code=404,
        detail="Execution doesn't exist"
    )
