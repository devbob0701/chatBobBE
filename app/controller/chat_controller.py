from fastapi import APIRouter, Request
from app.service.chat_service import ChatService

router = APIRouter()


@router.post("/chat")
async def chat(request: Request):
    data = await request.json()
    question_message = data.get("question_message", "")

    # ChatService를 사용하여 질문 처리
    service = ChatService()
    answer = service.chat_by_question(question_message, request)

    return {"answer": answer}