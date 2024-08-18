from fastapi import Request
from app.agent.openai.pdf_text_agent import pdf_text_agent_process


class ChatService:
    def chat_by_text_question(
            self,
            question_message: str,
            session_id: str,
            request: Request
    ):
        agent_execute_result = pdf_text_agent_process(question_message, session_id, request)
        print(f'agent_result: {agent_execute_result}')

        return {"input": agent_execute_result["input"], "output": agent_execute_result["output"]}