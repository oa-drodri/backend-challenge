from unittest.mock import MagicMock, patch
import pytest

from pytest_mock import MockFixture


@pytest.fixture
def mock_collection():
    with patch(
        "beanie.Document.get_motor_collection"
    ) as mock_get_motor_collection:
        mock_collection = MagicMock()
        mock_get_motor_collection.return_value = mock_collection
        yield mock_collection


@pytest.fixture
def mock_user_collection_auth_admin(mocker: MockFixture):
    mock = mocker.patch('auth.admin.user_collection')
    yield mock


@pytest.fixture
def mock_hash_helper_auth_admin(mocker: MockFixture):
    mock = mocker.patch('auth.admin.hash_helper')
    yield mock


@pytest.fixture
def mock_user_collection_routes_admin(mocker: MockFixture):
    mock = mocker.patch('routes.admin.User')
    yield mock


@pytest.fixture
def mock_hash_helper_routes_admin(mocker: MockFixture):
    mock = mocker.patch('routes.admin.hash_helper')
    yield mock


@pytest.fixture
def mock_decoder_routes_admin(mocker: MockFixture):
    mock = mocker.patch('routes.admin.decode_jwt')
    yield mock


@pytest.fixture
def mock_add_user_routes_admin(mocker: MockFixture):
    mock = mocker.patch('routes.admin.add_user')
    yield mock


@pytest.fixture
def mock_add_execution_routes_ecg(mocker: MockFixture):
    mock = mocker.patch('routes.ecg.add_execution')
    yield mock


@pytest.fixture
def mock_celery(mocker: MockFixture):
    mock = mocker.patch('routes.ecg.celery_app')
    yield mock


@pytest.fixture
def mock_decoder_routes_ecg(mocker: MockFixture):
    mock = mocker.patch('routes.ecg.decode_jwt')
    yield mock


@pytest.fixture
def mock_retrieve_execution_routes_ecg(mocker: MockFixture):
    mock = mocker.patch('routes.ecg.retrieve_execution')
    yield mock
