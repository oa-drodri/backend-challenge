import pytest
import asyncio


from fastapi import HTTPException
from models.admin import User, UserSignIn
from routes.admin import user_login, user_signup

from auth.jwt_handler import settings


@pytest.mark.asyncio
async def test_user_login_correct_credentials(
    mock_user_collection_routes_admin,
    mock_hash_helper_routes_admin,
    mock_collection
):
    settings.secret_key = "sample_key"

    user_instance = User(
        email="test@example.com",
        password="hashed_password",
        fullname="test@example.com"
    )

    mock_user_collection_routes_admin.find_one.return_value = asyncio.Future()
    mock_user_collection_routes_admin.find_one.return_value.set_result(
        user_instance
    )

    mock_hash_helper_routes_admin.verify.return_value = True

    result = await user_login(UserSignIn(
        username="test@example.com",
        password="password123"
    ))

    assert result


@pytest.mark.asyncio
async def test_user_login_user_not_found(
    mock_user_collection_routes_admin,
    mock_hash_helper_routes_admin,
    mock_collection
):
    settings.secret_key = "sample_key"

    user_instance = None

    mock_user_collection_routes_admin.find_one.return_value = asyncio.Future()
    mock_user_collection_routes_admin.find_one.return_value.set_result(
        user_instance
    )

    mock_hash_helper_routes_admin.verify.return_value = True

    with pytest.raises(HTTPException) as login_info:
        await user_login(UserSignIn(
            username="test@example.com",
            password="password123"
        ))

    assert login_info.value.status_code == 403
    assert login_info.value.detail == "Incorrect email or password"


@pytest.mark.asyncio
async def test_user_login_password_incorrect(
    mock_user_collection_routes_admin,
    mock_hash_helper_routes_admin,
    mock_collection
):
    settings.secret_key = "sample_key"

    user_instance = User(
        email="test@example.com",
        password="hashed_password",
        fullname="test@example.com"
    )

    mock_user_collection_routes_admin.find_one.return_value = asyncio.Future()
    mock_user_collection_routes_admin.find_one.return_value.set_result(
        user_instance
    )

    mock_hash_helper_routes_admin.verify.return_value = False

    with pytest.raises(HTTPException) as login_info:
        await user_login(UserSignIn(
            username="test@example.com",
            password="password123"
        ))

    assert login_info.value.status_code == 403
    assert login_info.value.detail == "Incorrect email or password"


@pytest.mark.asyncio
async def test_signup(
    mock_user_collection_routes_admin,
    mock_hash_helper_routes_admin,
    mock_decoder_routes_admin,
    mock_add_user_routes_admin,
    mock_collection
):
    user_instance = None

    mock_user_collection_routes_admin.find_one.return_value = asyncio.Future()
    mock_user_collection_routes_admin.find_one.return_value.set_result(
        user_instance
    )

    mock_hash_helper_routes_admin.encrypt.return_value = "P422"

    mock_decoder_routes_admin.return_value = {
        "role": "ADMIN"
    }

    expected_result = User(
        fullname="Test",
        email="test@example.com",
        password="P422",
        role="NORMAL"
    )

    mock_add_user_routes_admin.return_value = expected_result

    result: User = await user_signup(
        User(
            fullname="Test",
            email="test@example.com",
            password="PASS"
        ), ""
    )

    assert result == expected_result


@pytest.mark.asyncio
async def test_signup_no_admin_creator(
    mock_user_collection_routes_admin,
    mock_hash_helper_routes_admin,
    mock_decoder_routes_admin,
    mock_add_user_routes_admin,
    mock_collection
):
    user_instance = None

    mock_user_collection_routes_admin.find_one.return_value = asyncio.Future()
    mock_user_collection_routes_admin.find_one.return_value.set_result(
        user_instance
    )

    mock_hash_helper_routes_admin.encrypt.return_value = "P422"

    mock_decoder_routes_admin.return_value = {
        "role": "NORMAL"
    }

    expected_result = User(
        fullname="Test",
        email="test@example.com",
        password="P422",
        role="NORMAL"
    )

    mock_add_user_routes_admin.return_value = expected_result

    with pytest.raises(HTTPException) as login_info:
        await user_signup(
            User(
                fullname="Test",
                email="test@example.com",
                password="PASS"
            ), ""
        )

    assert login_info.value.status_code == 403
    assert login_info.value.detail == "User does not have enough permission"


@pytest.mark.asyncio
async def test_signup_user_exists(
    mock_user_collection_routes_admin,
    mock_hash_helper_routes_admin,
    mock_decoder_routes_admin,
    mock_add_user_routes_admin,
    mock_collection
):
    expected_result = User(
        fullname="Test",
        email="test@example.com",
        password="P422",
        role="NORMAL"
    )

    user_instance = expected_result

    mock_user_collection_routes_admin.find_one.return_value = asyncio.Future()
    mock_user_collection_routes_admin.find_one.return_value.set_result(
        user_instance
    )

    mock_hash_helper_routes_admin.encrypt.return_value = "P422"

    mock_decoder_routes_admin.return_value = {
        "role": "ADMIN"
    }

    mock_add_user_routes_admin.return_value = expected_result

    with pytest.raises(HTTPException) as login_info:
        await user_signup(
            User(
                fullname="Test",
                email="test@example.com",
                password="PASS"
            ), ""
        )

    assert login_info.value.status_code == 409
    assert login_info.value.detail == "User with email supplied already exists"
