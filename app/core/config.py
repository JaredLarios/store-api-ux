import os
import base64
from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = str(os.environ.get("DATABASE_URI", ""))
PRODUCT_API = str(os.environ.get("API_PRODUCT_URI", ""))

AES_SECRET_KEY = str(os.environ.get("CRYPTO_AES_SECRET_KEY", ""))
VI_SECRET_KEY = str(os.environ.get("CRYPTO_VI_SECRET_KEY", ""))
AES_KEY = base64.b64decode(AES_SECRET_KEY)
AES_IV = base64.b64decode(VI_SECRET_KEY)

ISSUER = str(os.environ.get("JWT_ISSUER", ""))
ALGORITHM = str(os.environ.get("JWT_ALGORITHM", ""))
ACCESS_TOKEN_SECRET_KEY = str(os.environ.get("JWT_ACCESS_TOKEN_SECRET_KEY", ""))
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 0))
REFRESH_TOKEN_SECRET_KEY = str(os.environ.get("JWT_REFRESH_TOKEN_SECRET_KEY", ""))
REFRESH_TOKEN_EXPIRE_MINUTES = int(
    os.environ.get("JWT_REFRESH_TOKEN_EXPIRE_MINUTES", 0)
)
VERIFY_TOKEN_SECRET_KEY = str(os.environ.get("JWT_VERIFY_TOKEN_SECRET_KEY", ""))
VERIFY_TOKEN_EXPIRE_MINUTES = int(os.environ.get("JWT_VERIFY_TOKEN_EXPIRE_MINUTES", 0))
ADMIN_ROLE = str(os.environ.get("JWT_ADMIN_ROLE", ""))
USER_ROLE = str(os.environ.get("JWT_USER_ROLE", ""))
