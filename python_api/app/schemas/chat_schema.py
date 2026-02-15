from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    userId: str
    status: str

class ChatResponse(BaseModel):
    reply: str