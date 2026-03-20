from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    userId: str
    status: str

class ChatResponse(BaseModel):
    reply: str

# For task_manager

class ReminderRequest(BaseModel):
    description: str
    due_date: str
    user_id: str
