from fastapi import FastAPI
from routes import chat, health
from config import settings

app = FastAPI(title=f"{settings.BOT_NAME} API")

app.include_router(chat.router)
app.include_router(health.router)
