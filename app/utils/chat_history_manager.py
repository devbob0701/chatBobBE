import atexit
import csv
import os

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

chat_data = {}

file_path = os.path.join("resources","storage", "chat_history.csv")

# 채팅 기록 불러오기 함수
def load_chat_history():
    if not os.path.exists(file_path):
        return

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            session_id = row["session"]
            sender = row["sender"]
            content = row["message"]

            if session_id not in chat_data:
                chat_data[session_id] = InMemoryChatMessageHistory(messages=[])

            if sender == "Human":
                chat_data[session_id].messages.append(HumanMessage(content=content))
            else:
                chat_data[session_id].messages.append(AIMessage(content=content))

# 앱이 종료될 때 호출될 함수
def save_chat_history():

    # 디렉토리가 존재하지 않으면 생성
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # CSV 파일에 저장
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # CSV 헤더 작성
        writer.writerow(["session", "sender", "message"])

        # 각 세션의 메시지 기록을 CSV 파일에 저장
        for session_id, history in chat_data.items():
            for message in history.messages:
                sender = "Human" if isinstance(message, HumanMessage) else "AI"
                writer.writerow([session_id, sender, message.content])

# 앱 종료 시 save_chat_history 함수가 호출되도록 설정
atexit.register(save_chat_history)