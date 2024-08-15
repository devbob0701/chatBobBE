import os
from openai import OpenAI

os.environ['OPENAI_API_KEY'] = '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'

class ChatService:
    def chat_by_question(self, question_message: str):
        client = OpenAI()
    
        # ChatCompletion 객체 생성
        completion = client.chat.completions.create(model="gpt-4", messages=[{"role": "user", "content": question_message}], stream=True)

        # 응답을 저장할 변수
        full_response = ""

        # 스트림으로 받은 내용을 하나의 문자열로 결합
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content

        # 최종 결과 반환
        return {"message": full_response}