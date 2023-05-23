from typing import List, Union

from beanie import PydanticObjectId

from models.admin import Admin
from models.ecg import ExecutionData, ExecutionStatus

admin_collection = Admin
ecg_data_collection = ExecutionData
ecg_status_collection = ExecutionStatus


async def add_admin(new_admin: Admin) -> Admin:
    admin = await new_admin.create()
    return admin


async def add_execution(new_execution: ExecutionData, user_id: str) -> ExecutionData:
    execution_data = await new_execution.create()
    user = await admin_collection.find_one({"email": user_id})
    execution_status = ExecutionStatus(id=execution_data.id, user=user)
    await execution_status.create()
    return execution_data


async def retrieve_execution(id: PydanticObjectId) -> ExecutionData:
    execution = await ecg_status_collection.get(id)
    if execution:
        return execution
