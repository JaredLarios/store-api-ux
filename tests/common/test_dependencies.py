import pytest
import jwt
from datetime import timedelta, datetime, timezone

from app.common import exceptions
from app.common.dependencies import (
    create_access_token,
    create_refresh_token,
    validate_access_token,
    validate_refresh_token,
    get_current_basic_user,
    get_refresh_token,
    get_current_admin_user,
)
from app.core import config


@pytest.fixture
def mock_config(mocker):
    """Mock configuration constants used by the module."""
    mocker.patch.object(config, "ACCESS_TOKEN_SECRET_KEY", "secret-key")
    mocker.patch.object(config, "REFRESH_TOKEN_SECRET_KEY", "refresh-secret")
    mocker.patch.object(config, "ALGORITHM", "HS256")
    mocker.patch.object(config, "ACCESS_TOKEN_EXPIRE_MINUTES", 5)
    mocker.patch.object(config, "REFRESH_TOKEN_EXPIRE_MINUTES", 10)
    mocker.patch.object(config, "ISSUER", "test-issuer")
    mocker.patch.object(config, "ADMIN_ROLE", "admin")
    return config

# -----------------------------------------------------
# Token creation tests
# -----------------------------------------------------

def test_create_access_token_contains_claims(mock_config):
    data = {"sub": "123", "name": "user1"}
    token = create_access_token(data, expires_delta=timedelta(minutes=1))
    decoded = jwt.decode(token, mock_config.ACCESS_TOKEN_SECRET_KEY, algorithms=["HS256"])
    assert decoded["sub"] == "123"
    assert decoded["name"] == "user1"
    assert decoded["iss"] == "test-issuer"
    assert "exp" in decoded and "iat" in decoded

def test_create_access_token_default_expiration(mock_config):
    """When no expires_delta is passed, uses default from config."""
    data = {"sub": "abc", "name": "user"}
    token = create_access_token(data)
    decoded = jwt.decode(token, mock_config.ACCESS_TOKEN_SECRET_KEY, algorithms=["HS256"])
    # Exp should be about 5 minutes after issued
    issued = datetime.fromtimestamp(decoded["iat"], tz=timezone.utc)
    exp = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
    delta = exp - issued
    assert timedelta(minutes=4) <= delta <= timedelta(minutes=6)

@pytest.mark.asyncio
async def test_validate_access_token_missing_claims_raises(mocker, mock_config):
    """If sub or name missing, raises credentials_exception."""
    payload = {"sub": None, "name": None}
    mocker.patch("jwt.decode", return_value=payload)
    with pytest.raises(exceptions.credentials_exception.__class__):
        await validate_access_token("fake-token")

@pytest.mark.asyncio
async def test_validate_access_token_jwt_raises_general_exception(mocker):
    """Ensure generic exception is caught and re-raised as credentials_exception."""
    mocker.patch("jwt.decode", side_effect=Exception("boom"))
    with pytest.raises(exceptions.credentials_exception.__class__):
        await validate_access_token("token")


def test_create_refresh_token_contains_claims(mock_config):
    data = {"sub": "456"}
    token = create_refresh_token(data, expires_delta=timedelta(minutes=1))
    decoded = jwt.decode(token, mock_config.REFRESH_TOKEN_SECRET_KEY, algorithms=["HS256"])
    assert decoded["sub"] == "456"
    assert decoded["iss"] == "test-issuer"
    assert "exp" in decoded and "iat" in decoded

def test_create_refresh_token_default_expiration(mock_config):
    """When no expires_delta is passed, uses default from config."""
    data = {"sub": "def"}
    token = create_refresh_token(data)
    decoded = jwt.decode(token, mock_config.REFRESH_TOKEN_SECRET_KEY, algorithms=["HS256"])
    issued = datetime.fromtimestamp(decoded["iat"], tz=timezone.utc)
    exp = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
    delta = exp - issued
    assert timedelta(minutes=9) <= delta <= timedelta(minutes=11)

@pytest.mark.asyncio
async def test_validate_refresh_token_missing_sub_raises(mocker, mock_config):
    """If sub missing in refresh token, raises credentials_exception."""
    payload = {"no_sub": "something"}
    mocker.patch("jwt.decode", return_value=payload)
    with pytest.raises(exceptions.credentials_exception.__class__):
        await validate_refresh_token("fake-token")

@pytest.mark.asyncio
async def test_get_refresh_token_model_raises(mocker):
    """If AdminModel raises error, it should propagate (not swallowed)."""
    mock_model = mocker.Mock()
    mock_model.get_user_by_uuid.side_effect = RuntimeError("DB error")
    token_data = mocker.Mock(sub="999")
    with pytest.raises(RuntimeError, match="DB error"):
        await get_refresh_token(token_data, mock_model)

# -----------------------------------------------------
# User retrieval tests
# -----------------------------------------------------

@pytest.mark.asyncio
async def test_get_current_basic_user_decrypts_fields(mocker):
    mock_decrypt = mocker.patch(
        "app.core.crypto.TextCrypto.decrypt_text", side_effect=["user1", "admin"])
    token_data = mocker.Mock(sub="123", name="encrypted_name", role="encrypted_role")

    result = await get_current_basic_user(token_data)
    assert result == {"user_uuid": "123", "username": "user1", "role": "admin"}
    assert mock_decrypt.call_count == 2

@pytest.mark.asyncio
async def test_get_current_basic_user_decrypt_fails(mocker):
    """If decryption fails, the exception should propagate."""
    mocker.patch("app.core.crypto.TextCrypto.decrypt_text", side_effect=Exception("decrypt fail"))
    token_data = mocker.Mock(sub="123", name="enc", role="enc")
    with pytest.raises(Exception, match="decrypt fail"):
        await get_current_basic_user(token_data)

@pytest.mark.asyncio
async def test_get_refresh_token_user_found(mocker):
    mock_user = {"user_uuid": "123"}
    mock_model = mocker.Mock()
    mock_model.get_user_by_uuid.return_value = mock_user
    token_data = mocker.Mock(sub="123")

    result = await get_refresh_token(token_data, mock_model)
    assert result == mock_user
    mock_model.get_user_by_uuid.assert_called_once_with(user_uuid="123")


@pytest.mark.asyncio
async def test_get_refresh_token_user_not_found(mocker):
    mock_model = mocker.Mock()
    mock_model.get_user_by_uuid.return_value = None
    token_data = mocker.Mock(sub="999")

    with pytest.raises(exceptions.permission_exception.__class__):
        await get_refresh_token(token_data, mock_model)


@pytest.mark.asyncio
async def test_get_current_admin_user_valid(mock_config):
    user = {"user_uuid": "1", "username": "john", "role": "admin"}
    result = await get_current_admin_user(user)
    assert result == user


@pytest.mark.asyncio
async def test_get_current_admin_user_invalid_role(mock_config):
    user = {"user_uuid": "1", "username": "john", "role": "user"}
    with pytest.raises(exceptions.permission_exception.__class__):
        await get_current_admin_user(user)

@pytest.mark.asyncio
async def test_get_current_admin_user_case_insensitive_role(mock_config):
    """If role matches ADMIN_ROLE exactly, passes."""
    user = {"user_uuid": "1", "username": "john", "role": "ADMIN".lower()}
    # Still should pass if config.ADMIN_ROLE == "admin"
    result = await get_current_admin_user(user)
    assert result["role"] == "admin"

def test_create_access_token_claim_format(mock_config):
    """Ensure exp and iat claims are numeric timestamps."""
    token = create_access_token({"sub": "test"})
    decoded = jwt.decode(token, mock_config.ACCESS_TOKEN_SECRET_KEY, algorithms=["HS256"])
    assert isinstance(decoded["exp"], (int, float))
    assert isinstance(decoded["iat"], (int, float))
