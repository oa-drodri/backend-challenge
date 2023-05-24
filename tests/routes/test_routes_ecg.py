import pytest

from fastapi import HTTPException, Response

from routes.ecg import execution_status, queue_execution
from models.ecg import ExecutionData, ExecutionStatus
from models.admin import User


@pytest.mark.asyncio
async def test_queue_execution(
    mock_add_execution_routes_ecg,
    mock_celery,
    mock_decoder_routes_ecg,
    mock_collection
):
    execution_instance = ExecutionData(
        date="2000/01/01",
        leads=[]
    )
    mock_add_execution_routes_ecg.return_value = execution_instance

    id_execution = execution_instance.id

    mock_celery.send_task.return_value = None

    mock_decoder_routes_ecg.return_value = {
        "role": "NORMAL",
        "user_id": "test@test.com"
    }

    result: Response = await queue_execution(
        {
            "date": "2000/01/01",
            "leads": []
        }, ""
    )

    assert result == {
        "description": "ECG execution created successfully",
        "response_type": "success",
        "status_code": 200,
        "execution_id": id_execution,
    }


@pytest.mark.asyncio
async def test_queue_execution_admin_role(
    mock_add_execution_routes_ecg,
    mock_celery,
    mock_decoder_routes_ecg,
    mock_collection
):
    execution_instance = ExecutionData(
        date="2000/01/01",
        leads=[]
    )
    mock_add_execution_routes_ecg.return_value = execution_instance

    mock_celery.send_task.return_value = None

    mock_decoder_routes_ecg.return_value = {
        "role": "ADMIN",
        "user_id": "test@test.com"
    }

    with pytest.raises(HTTPException) as execution_info:
        await queue_execution(
            {
                "date": "2000/01/01",
                "leads": []
            }, ""
        )

    assert execution_info.value.status_code == 403
    assert (
        execution_info.value.detail
        == "Admin user cannot queue ECG processing"
    )


@pytest.mark.asyncio
async def test_execution_status(
    mock_retrieve_execution_routes_ecg,
    mock_decoder_routes_ecg,
    mock_collection
):
    user = User(
        fullname="Test",
        email="test@test.com",
        role="NORMAL",
        password="1234"
    )
    execution_status_instance = ExecutionStatus(
        status="IN PROGRESS",
        result={},
        user=user
    )
    execution_id = execution_status_instance.id

    mock_retrieve_execution_routes_ecg.return_value = execution_status_instance

    mock_decoder_routes_ecg.return_value = {
        "role": "NORMAL",
        "user_id": "test@test.com"
    }

    result: Response = await execution_status(
        execution_id, ""
    )

    assert result == {
        "description": "Execution status retrieved successfully",
        "response_type": "success",
        "status_code": 200,
        "data": {
            "result": {},
            "status": "IN PROGRESS"
        }
    }


@pytest.mark.asyncio
async def test_execution_status_admin_role(
    mock_retrieve_execution_routes_ecg,
    mock_decoder_routes_ecg
):
    mock_retrieve_execution_routes_ecg.return_value = {
        "status": "IN PROGRESS",
        "result": {},
        "user": {
            "email": "test@test.com"
        }
    }

    mock_decoder_routes_ecg.return_value = {
        "role": "ADMIN",
        "user_id": "test@test.com"
    }

    with pytest.raises(HTTPException) as execution_info:
        await execution_status(345, "")

    assert execution_info.value.status_code == 403
    assert (
        execution_info.value.detail
        == "Admin user cannot queue ECG processing"
    )


@pytest.mark.asyncio
async def test_execution_status_not_owned(
    mock_retrieve_execution_routes_ecg,
    mock_decoder_routes_ecg,
    mock_collection
):
    user = User(
        fullname="Test",
        email="test@test.com",
        role="NORMAL",
        password="1234"
    )
    execution_status_instance = ExecutionStatus(
        status="IN PROGRESS",
        result={},
        user=user
    )
    execution_id = execution_status_instance.id

    mock_retrieve_execution_routes_ecg.return_value = execution_status_instance

    mock_decoder_routes_ecg.return_value = {
        "role": "NORMAL",
        "user_id": "test2@test.com"
    }

    with pytest.raises(HTTPException) as execution_info:
        await execution_status(execution_id, "")

    assert execution_info.value.status_code == 403
    assert (
        execution_info.value.detail
        == "Invalid user authorization"
    )


@pytest.mark.asyncio
async def test_execution_status_not_exists(
    mock_retrieve_execution_routes_ecg,
    mock_decoder_routes_ecg
):
    mock_retrieve_execution_routes_ecg.return_value = None

    mock_decoder_routes_ecg.return_value = {
        "role": "NORMAL",
        "user_id": "test2@test.com"
    }

    with pytest.raises(HTTPException) as execution_info:
        await execution_status(345, "")

    assert execution_info.value.status_code == 404
    assert (
        execution_info.value.detail
        == "Execution doesn't exist"
    )
