from app.dto import chat_list_dto

chat_list = {}

def load_chat_list():
    global chat_list
    chat_list = chat_list_dto.load_chat_list()
    print(f'chat_list : {chat_list}')

def save_chat_list(user_id: str, session_id: str, session_name: str):
    if user_id not in chat_list:
        chat_list[user_id] = []
    chat_list[user_id].append({"session_id": session_id, "session_name": session_name})
    print(f'chat_list : {chat_list}')
    # chat_list를 DTO를 통해 저장
    chat_list_dto.save_chat_list(chat_list)


def get_chat_list_by_user_id(user_id: str):
    return chat_list.get(user_id, [])

def check_and_add_new_chat(user_id: str, session_id: str, session_name: str):
    user_chats = chat_list.get(user_id, [])
    matching_chat = None

    for chat in user_chats:
        if chat["session_id"] == session_id:
            matching_chat = chat
            break

    if matching_chat:
        return None

    # 채팅방이 없으면 새로운 채팅방 생성
    save_chat_list(user_id, session_id, session_name)