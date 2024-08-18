from fastapi import Request
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.runnables import RunnableWithMessageHistory, RunnableConfig
from langchain_core.tools import create_retriever_tool
from langchain_openai import ChatOpenAI

from app.service.history.chat_data_service import get_session_history


def pdf_text_agent_process(
        question_message: str,
        session_id: str,
        request: Request
):
    # pdf문서에서 question_message와 관련성 높은 Chunk를 추출
    retriever = request.app.state.retriever

    retriever_tool = create_retriever_tool(
        retriever,
        name="mydata_pdf_search",
        description="마이데이터 관련 정보를 PDF 문서에서 검색"
    )

    # tools 지정
    # 검색기반, 파일 분석 기반 등 다양한 Tool을 추가하면 됨
    tools = [retriever_tool]

    # rag_prompt 세팅
    rag_prompt = request.app.state.rag_prompt

    # llm 모델 지정
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

    # OpenAI 함수 기반 Agent 생성
    agent = create_openai_functions_agent(llm, tools, rag_prompt)

    # agent_executor 구성
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

    # 멀티턴 채팅을 지원하기 위해 RunnableWithMessageHistory로 병합
    agent_with_chat_history = RunnableWithMessageHistory(
        agent_executor,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history"
    )

    answer = agent_with_chat_history.invoke({'input' : question_message}, RunnableConfig(configurable={"session_id":session_id}))

    return answer