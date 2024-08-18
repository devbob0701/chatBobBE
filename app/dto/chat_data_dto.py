import os
import pandas
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

file_path = os.path.join("resources", "storage", "chat_data.csv")


# 채팅 기록 불러오기
def load_chat_data():
    chat_data = {}
    if not os.path.exists(file_path):
        return chat_data

    # pandas를 사용하여 CSV 파일 읽기
    data = pandas.read_csv(file_path, encoding='utf-8')
    if data.empty:
        return chat_data

    for _, row in data.iterrows():
        session_id = row["session"]
        sender = row["sender"]
        content = row["message"]

        if session_id not in chat_data:
            chat_data[session_id] = InMemoryChatMessageHistory(messages=[])

        if sender == "Human":
            chat_data[session_id].messages.append(HumanMessage(content=content))
        else:
            chat_data[session_id].messages.append(AIMessage(content=content))

    return chat_data


# 채팅 기록 저장하기
def save_chat_data(chat_data: dict):
    # 데이터를 저장할 리스트 초기화
    records = []

    # 각 세션의 메시지 기록을 리스트에 추가
    for session_id, history in chat_data.items():
        for message in history.messages:
            sender = "Human" if isinstance(message, HumanMessage) else "AI"
            records.append({"session": session_id, "sender": sender, "message": message.content})

    if records:
        # 디렉토리가 존재하지 않으면 생성
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # pandas를 사용하여 CSV 파일로 저장
        df = pandas.DataFrame(records)
        df.to_csv(file_path, index=False, encoding='utf-8')