from fastapi import status, HTTPException

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


permission_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User without permission for this Request.",
)
