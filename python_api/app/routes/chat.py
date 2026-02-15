from fastapi import APIRouter
from schemas.chat_schema import ChatRequest, ChatResponse
from services.group_helper import process_user_message, process_admin_message

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    if request.status == 'user':
        reply = process_user_message(request.message)
    elif request.status == 'admin':
        reply = process_admin_message(request.message)
    
    return ChatResponse(reply=reply)
