from fastapi import Request
from langchain_core.runnables import RunnablePassthrough

class ChatService:
    def chat_by_question(self, question_message: str, request: Request):

        # rag_chain 구성
        rag_chain = (
                {"context": request.app.state.retriever | self.format_docs, "question": RunnablePassthrough()}
                | request.app.state.rag_prompt
                | request.app.state.llm
        )

        # 질문을 이용해 응답 생성
        answer = rag_chain.invoke(question_message)

        return answer

    @staticmethod
    def format_docs(docs):
        return "\n\n".join([doc.page_content for doc in docs])