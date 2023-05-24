from beanie import PydanticObjectId

from models.admin import User
from models.ecg import ExecutionData, ExecutionStatus

user_collection = User
ecg_data_collection = ExecutionData
ecg_status_collection = ExecutionStatus


async def add_user(new_user: User) -> User:
    user = await new_user.create()
    return user


async def add_execution(
    new_execution: ExecutionData, user_id: str
) -> ExecutionData:
    execution_data = await new_execution.create()
    user = await user_collection.find_one({"email": user_id})
    execution_status = ExecutionStatus(id=execution_data.id, user=user)
    await execution_status.create()
    return execution_data


async def retrieve_execution(id: PydanticObjectId) -> ExecutionData:
    execution = await ecg_status_collection.get(id)
    if execution:
        return execution
