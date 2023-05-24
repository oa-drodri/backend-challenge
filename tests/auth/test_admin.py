import pytest

from fastapi import HTTPException, status
from fastapi.security import HTTPBasicCredentials
from auth.admin import validate_login


@pytest.mark.asyncio
async def test_validate_login_correct_credentials(
    mock_user_collection_auth_admin, mock_hash_helper_auth_admin
):
    mock_user_collection_auth_admin.find_one.return_value = {
        "email": "test@example.com",
        "password": "hashed_password"
    }

    mock_hash_helper_auth_admin.verify.return_value = True

    result = await validate_login(HTTPBasicCredentials(
        username="test@example.com",
        password="password123"
    ))

    assert result is True


@pytest.mark.asyncio
async def test_validate_login_user_not_found(
    mock_user_collection_auth_admin, mock_hash_helper_auth_admin
):
    # Config mocks response
    mock_user_collection_auth_admin.find_one.return_value = None
    mock_hash_helper_auth_admin.verify.return_value = False

    with pytest.raises(HTTPException) as exc_info:
        await validate_login(HTTPBasicCredentials(
                username="test@example.com",
                password="password123"
            )
        )

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Incorrect email or password"


@pytest.mark.asyncio
async def test_validate_login_user_found_incorrect_password(
    mock_user_collection_auth_admin,
    mock_hash_helper_auth_admin
):
    # Config mocks response
    mock_user_collection_auth_admin.find_one.return_value = {
        "email": "test@example.com",
        "password": "hashed_password"
    }
    mock_hash_helper_auth_admin.verify.return_value = False

    with pytest.raises(HTTPException) as exc_info:
        await validate_login(HTTPBasicCredentials(
                username="test@example.com",
                password="password123"
            )
        )

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Incorrect email or password"
