from fastapi import FastAPI
from datetime import datetime
from dotenv import load_dotenv
import os
import requests

from app.config import settings
from app.schemas import *

from app.services.message_processor import process_message
from app.services.task_manager.database import list_tasks, delete_task

load_dotenv()

app = FastAPI(title=f"{settings.BOT_NAME} API")
API_URL = os.getenv("API_URL")

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply = process_message(request.userId, request.message)
    
    return ChatResponse(reply=reply)

# For task_manager

@app.post("/send-reminder")
def send_reminder(data: ReminderRequest):
    message = (
        f"⏰ Lembrete!\n\n"
        f"Descrição: {data.description}.\n"
        f"Data de vencimento: {data.due_date}"
    )

    # TO-DO: Enviar para o bot

    return {"status": "ok"}


@app.get("/check-tasks")
def check_tasks():
    SEND_REMINDER_IN = 3

    tasks = list_tasks()
    today = datetime.now().date()

    for task in tasks:
        if task.get("completed") or task["due_date"] == None:
            continue

        due_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
        days_remaining = (due_date - today).days

        if days_remaining <= 0:
            delete_task(task["id"])
        elif days_remaining <= SEND_REMINDER_IN:
            try:
                requests.post(API_URL, json={
                    "description": task["description"],
                    "due_date": task["due_date"],
                    "user_id": task["user_id"]
                })
            except Exception as e:
                print("Erro ao enviar lembrete: ", e)
