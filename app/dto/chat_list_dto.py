import os
import pandas

file_path = os.path.join("resources", "storage", "chat_list.csv")


def load_chat_list():
    if os.path.exists(file_path):
        data = pandas.read_csv(file_path)
        chat_list = {}
        for _, row in data.iterrows():
            user_id = row["user_id"]
            if user_id not in chat_list:
                chat_list[user_id] = []
            chat_list[user_id].append({"session_id": row["session_id"], "session_name": row["session_name"]})
        return chat_list
    else:
        return {}


def save_chat_list(chat_list):
    # 파일이 존재하지 않으면 디렉토리, 파일 생성
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    # 데이터프레임을 생성하기 위한 리스트
    records = []
    for user_id, chats in chat_list.items():
        for chat in chats:
            records.append({
                "user_id": user_id,
                "session_id": chat["session_id"],
                "session_name": chat["session_name"]
            })

    # 데이터프레임을 파일에 저장
    data_frame = pandas.DataFrame(records)
    data_frame.to_csv(file_path, index=False)