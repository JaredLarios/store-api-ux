from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Auth:
    """
        Utils for verify identification
    """
    def verify_password(self, plain_password: str, hashed_password) -> bool:
        """
            Verify bcrypt password with hashed password
            args:
                plain_password: str -> plain text with password
                hashed_password: str -> hashed text with password
            return:
                A boolean result if the password hash matches or not
        """
        return pwd_context.verify(plain_password, hashed_password)