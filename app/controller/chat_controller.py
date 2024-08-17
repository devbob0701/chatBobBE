from fastapi import APIRouter, Request
from app.service.chat_service import ChatService

router = APIRouter()


@router.post("/chat")
async def chat(request: Request):
    data = await request.json()
    session_id = data.get("session_id", "")
    question_message = data.get("question_message", "")

    # ChatService를 사용하여 질문 처리
    service = ChatService()
    answer = service.chat_by_question(question_message, session_id, request)

    return {"answer": answer}