import os
import pandas

file_path = os.path.join("resources", "storage", "chat_data.csv")


# 채팅 기록 불러오기
def load_chat_data() -> dict:
    chat_data = {}

    # 파일이 존재하지 않으면 빈 딕셔너리 반환
    if not os.path.exists(file_path):
        return chat_data

    # pandas를 사용하여 CSV 파일 읽기
    data = pandas.read_csv(file_path, encoding='utf-8')

    # 각 행을 순회하며 chat_data에 추가
    for index, row in data.iterrows():
        session_id = row['session_id']  # session_id 컬럼
        input_text = row['input']  # input 컬럼
        output_text = row['output']  # output 컬럼

        # message 딕셔너리 생성
        message = {'input': input_text, 'output': output_text}

        # chat_data에 해당 session_id가 있는지 확인
        if session_id in chat_data:
            # 이미 세션 ID가 존재하면 해당 리스트에 대화 추가
            chat_data[session_id].append(message)
        else:
            # 세션 ID가 존재하지 않으면 새로운 리스트를 만들어 추가
            chat_data[session_id] = [message]

    return chat_data


# 채팅 기록 저장하기
def save_chat_data(chat_data: dict):
    if chat_data:
        # 데이터를 저장할 리스트 생성
        rows = []

        # 딕셔너리를 순회하면서 각 세션의 데이터를 리스트에 추가
        for session_id, interactions in chat_data.items():
            for interaction in interactions:
                rows.append({
                    'session_id': session_id,
                    'input': interaction['input'],
                    'output': interaction['output']
                })

        # 리스트를 데이터프레임으로 변환
        df = pandas.DataFrame(rows)

        # 디렉토리가 존재하지 않으면 생성
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # 데이터프레임을 CSV 파일로 저장
        df.to_csv(file_path, index=False, encoding='utf-8')