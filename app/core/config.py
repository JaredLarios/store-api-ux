
import os
import base64
from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = str(os.environ.get("URI"))

AES_SECRET_KEY = str(os.environ.get("AES_SECRET_KEY"))
VI_SECRET_KEY = str(os.environ.get("VI_SECRET_KEY"))
AES_KEY = base64.b64decode(AES_SECRET_KEY)
AES_IV = base64.b64decode(VI_SECRET_KEY)
