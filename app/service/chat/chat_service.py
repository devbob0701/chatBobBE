from fastapi import Request
import json
from app.agent.openai.pdf_text_agent import PdfTextAgent


class ChatService:
    def chat_by_text_question(
            self,
            question_message: str,
            session_id: str,
            request: Request
    ):
        pdf_text_agent = PdfTextAgent()
        agent_execute_result = pdf_text_agent.pdf_text_agent_process(question_message, session_id, request)
        print(f'agent_result: {agent_execute_result}')

        return {"input": agent_execute_result["input"], "output": agent_execute_result["output"]}