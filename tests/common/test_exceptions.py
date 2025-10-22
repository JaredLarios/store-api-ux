from fastapi import status, HTTPException
from app.common.exceptions import credentials_exception, permission_exception


def test_credentials_exception_properties():
    """Test that the credentials exception has the correct status, message, and headers."""
    assert isinstance(credentials_exception, HTTPException)
    assert credentials_exception.status_code == status.HTTP_401_UNAUTHORIZED
    assert credentials_exception.detail == "Could not validate credentials"
    assert credentials_exception.headers == {"WWW-Authenticate": "Bearer"}


def test_permission_exception_properties():
    """Test that the permission exception has the correct status and message."""
    assert isinstance(permission_exception, HTTPException)
    assert permission_exception.status_code == status.HTTP_403_FORBIDDEN
    assert permission_exception.detail == "User without permission for this Request."
    # 403 doesn't include auth headers
    assert permission_exception.headers is None