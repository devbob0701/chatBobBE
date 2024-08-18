from fastapi import APIRouter, Request

from app.service.chat.chat_service import ChatService

router = APIRouter()

@router.get("/get-chat-list")
async def get_chat_list(request: Request):
    user_id = request.query_params.get("user_id", "")

    chat_service = ChatService()
    return chat_service.get_chat_list(user_id)

@router.get("/get-chat-messages")
async def get_chat_messages(request: Request):
    session_id = request.query_params.get("session_id", "")

    chat_service = ChatService()
    return chat_service.get_chat_messages(session_id)

@router.post("/chat")
async def chat(request: Request):
    request_data = await request.json()
    user_id = request_data.get("user_id", "")
    session_id = request_data.get("session_id", "")
    session_name = request_data.get("session_name", "")
    question_message = request_data.get("question_message", "")

    # ChatService를 사용하여 질문 처리
    chat_service = ChatService()

    answer = chat_service.chat_by_text_question(question_message, user_id, session_id, session_name, request)

    return {"answer": answer}