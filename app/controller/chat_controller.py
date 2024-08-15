from fastapi import APIRouter, Request
from app.service.chat_service import ChatService

router = APIRouter()

@router.post("/chat")
async def chat_by_question(request: Request):
    data = await request.json()
    question_message = data.get("question_message")

    service = ChatService()
    return service.chat_by_question(question_message)