
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = str(os.environ.get("URI"))
