import atexit
import os

from app.dto import chat_data_dto

chat_data = {}

file_path = os.path.join("resources", "storage", "chat_data.csv")


# 채팅 기록 불러오기
def load_chat_data():
    global chat_data
    chat_data = chat_data_dto.load_chat_data()

def get_chat_messages_by_session_id(session_id: str):
    return chat_data.get(session_id, [])

def save_chat_data_on_memory(session_id:str ,input: str, output: str):
    global chat_data
    if session_id in chat_data:
        chat_data[session_id].append({"input" : input, "output": output})
    else:
        chat_data[session_id] = [{"input" : input, "output": output}]

# 채팅 기록 저장하기
def save_chat_data():
    chat_data_dto.save_chat_data(chat_data)

# 앱 종료 시 save_chat_history 함수가 호출되도록 설정
atexit.register(save_chat_data)