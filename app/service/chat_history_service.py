from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

store = {}  # 세션 기록을 저장할 딕셔너리


# 세션 ID를 기반으로 세션 기록을 가져오는 함수
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    print(session_id)
    if session_id not in store:  # 세션 ID가 store에 없는 경우
        # 새로운 ChatMessageHistory 객체를 생성하여 store에 저장
        store[session_id] = ChatMessageHistory()
    return store[session_id]  # 해당 세션 ID에 대한 세션 기록 반환