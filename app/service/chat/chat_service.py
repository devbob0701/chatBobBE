from fastapi import Request
from app.agent.openai.pdf_text_agent import pdf_text_agent_process
from app.manager.chat_data_manager import get_chat_messages_by_session_id, save_chat_data_on_memory
from app.manager.chat_list_manager import get_chat_list_by_user_id, check_and_add_new_chat


class ChatService:
    def get_chat_list(self, user_id: str):
        return get_chat_list_by_user_id(user_id)

    def get_chat_messages(self, session_id: str):
        return get_chat_messages_by_session_id(session_id)

    def chat_by_text_question(
            self,
            question_message: str,
            user_id: str,
            session_id: str,
            session_name: str,
            request: Request
    ):
        agent_execute_result = pdf_text_agent_process(question_message, session_id, request)

        # 응답을 받은 후 최초 대화인지 여부를 판단하여 새로운 채팅방을 만들지 결정
        # 채팅방 이름은 client로부터 전달받아서 사용
        check_and_add_new_chat(user_id, session_id, session_name)

        input_message = agent_execute_result["input"]
        output_message = agent_execute_result["output"]

        save_chat_data_on_memory(session_id, input_message, output_message)

        return {"input": input_message, "output": output_message}
