import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "INFO-BOT: Bot For Whatsapp"
    BOT_NAME: str = "INFO-BOT"
    VERSION: str = "1.0.0"

settings = Settings()