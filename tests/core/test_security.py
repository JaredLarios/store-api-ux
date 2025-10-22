import pytest
from fastapi import HTTPException, status
from app.core.security import AuthUtils
from app.core.crypto import TextCrypto


@pytest.fixture
def mock_auth_model(mocker):
    """Mock AdminModel used in authentication tests."""
    return mocker.Mock()


@pytest.fixture
def auth_utils():
    """Return instance of AuthUtils."""
    return AuthUtils()


# ---------- verify_password ----------
def test_verify_password_success(auth_utils):
    hashed = auth_utils.get_password_hash("mypassword")
    assert auth_utils.verify_password("mypassword", hashed) is True


def test_verify_password_failure(auth_utils):
    hashed = auth_utils.get_password_hash("mypassword")
    assert auth_utils.verify_password("wrongpassword", hashed) is False


# ---------- authenticate_user ----------
def test_authenticate_user_success(mocker, auth_utils, mock_auth_model):
    """Should return user object if username and password match."""
    user = mocker.Mock()
    user.sys_user_password = auth_utils.get_password_hash("secret")
    mock_auth_model.get_user_by_username.return_value = user

    result = auth_utils.authenticate_user("admin", "secret", mock_auth_model)

    assert result == user
    mock_auth_model.get_user_by_username.assert_called_once_with("admin")


def test_authenticate_user_invalid_username(mocker, auth_utils, mock_auth_model):
    """Should return None when user not found."""
    mock_auth_model.get_user_by_username.return_value = None

    result = auth_utils.authenticate_user("invalid", "secret", mock_auth_model)

    assert result is None


def test_authenticate_user_invalid_password(mocker, auth_utils, mock_auth_model):
    """Should return None when password does not match."""
    user = mocker.Mock()
    user.sys_user_password = auth_utils.get_password_hash("realpassword")
    mock_auth_model.get_user_by_username.return_value = user

    result = auth_utils.authenticate_user("admin", "wrong", mock_auth_model)

    assert result is None


# ---------- verify_code ----------
def test_verify_code_success(mocker, auth_utils):
    """Should return decoded JSON data when code is valid."""
    # Mock decrypted payload with valid expiration
    data = {"exp": 9999999999.0, "user": "admin"}
    mock_decrypt = mocker.patch.object(
        TextCrypto, "decrypt_text", return_value='{"exp": 9999999999.0, "user": "admin"}'
    )
    mocker.patch("app.core.crypto.TextCrypto", return_value=TextCrypto(encrypted_text="abc"))

    result = auth_utils.verify_code("abc")

    mock_decrypt.assert_called_once()
    assert result["user"] == "admin"
    assert "exp" in result


def test_verify_code_expired(mocker, auth_utils):
    """Should raise HTTPException if code is expired."""
    expired_data = '{"exp": 1.0, "user": "admin"}'
    mocker.patch.object(TextCrypto, "decrypt_text", return_value=expired_data)
    mocker.patch("app.core.crypto.TextCrypto", return_value=TextCrypto(encrypted_text="abc"))

    with pytest.raises(HTTPException) as exc_info:
        auth_utils.verify_code("abc")

    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
    assert "expired" in exc_info.value.detail.lower()


def test_verify_code_invalid_json(mocker, auth_utils):
    """Should raise HTTPException if decryption or JSON fails."""
    mocker.patch.object(TextCrypto, "decrypt_text", side_effect=Exception("bad decrypt"))
    mocker.patch("app.core.crypto.TextCrypto", return_value=TextCrypto(encrypted_text="abc"))

    with pytest.raises(HTTPException) as exc_info:
        auth_utils.verify_code("abc")

    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
    assert "not valid" in exc_info.value.detail.lower()


# ---------- get_password_hash ----------
def test_get_password_hash(auth_utils):
    """Should generate different hash for same password (salted)."""
    hash1 = auth_utils.get_password_hash("password")
    hash2 = auth_utils.get_password_hash("password")
    assert hash1 != hash2
    assert hash1.startswith("$2b$")