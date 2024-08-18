# ChatBob 서비스 개요
 
**ChatBobBE**는 **FastAPI**를 기반으로 한 백엔드 애플리케이션입니다.

AI 기능을 위해 OpenAI와 LangChain, HuggingFace 등의 라이브러리를 사용합니다.

## Agent 설명

사용자가 입력한 질문(`question_message`)을 기반으로, PDF 문서에서 관련성 높은 정보를 추출하여 응답을 생성하는 핵심 로직을 담당합니다.

### PDF 텍스트 에이전트

`app > agent > openai > pdf_text_agent.py`

#### 주요 기능

1. **PDF 문서에서 정보 검색**:
   - PDF에서 관련 정보를 추출하기 위한 `retriever`와 `retriever_tool` 설정.

2. **LLM 모델 및 프롬프트 설정**:
   - `ChatOpenAI`로 `gpt-4o-mini` 모델 설정 및 RAG 프롬프트 구성.

3. **에이전트 및 도구 설정**:
   - OpenAI 함수 기반 에이전트 생성 및 `AgentExecutor`로 에이전트 실행 환경 구성.

4. **채팅 히스토리 관리**:
   - `RunnableWithMessageHistory`를 사용해 멀티턴 대화 기록을 포함한 에이전트 구성.

5. **질문 처리 및 응답 생성**:
   - 질문 메시지를 처리하고, 세션 히스토리를 반영한 응답 생성 및 반환.

## 프로젝트 구성
```
app
├── agent
│   └─── openai
│       └─── pdf_text_agent.py
├── controller
│   └─── chat_controller.py
├── dto
│   ├─── chat_data_dto.py
│   └─── chat_list_dto.py
├── manager
│   ├─── chat_data_manager.py
│   └─── chat_list_manager.py
├── service
│   ├─── chat
│   │    └─── chat_service.py
│   └─── history
│        └─── chat_data_service.py
└── utils
    └─── resource_initializer.py
```

- **agent**: LLM 모델 별 Agent를 분리 구현한 패키지
- **controller**: controller 모음 (현재는 chat_controller만 존재)
- **dto**: 데이터 저장/로드 관련 패키지 
  - resources > storage 내에 생성되는 chat_data.csv, chat_list.csv 관련 처리를 담당하는 파일들로 구성
  - 최초 질문을 던지는 경우 user_id와 session_id로 매핑되는 채팅방 생성
  - chat_data는 메모리에서 관리되다 어플리케이션 종료 시 chat_data.csv 파일에 백업. 이후 어플리케이션 실행 시 chat_data에 딕셔너리 형태로 로드
    
    ![image](https://github.com/user-attachments/assets/e1db5206-5384-4f8a-ab84-765ca3482131)
    
    ![image](https://github.com/user-attachments/assets/f4dc88b0-453d-4e33-aead-e38f429f02c5)
    
    ![image](https://github.com/user-attachments/assets/0066a05e-211a-4b39-ae48-949c0862c75f)


- **manager**: 메모리에 올린 데이터를 관리하는 패키지. Redis 등 외부 리소스 사용을 하지 않기 위해 프로세스 상의 메모리에 해당 데이터들이 올라감
- **service**: service 모음
- **utils**: 최초 어플리케이션 실행 시점에 retriever와 llm 초기화를 하는 패키지

## API 호출

1. **질문 전달하기**
   - **URL**: `http://localhost:8000/chat`
   - **Method**: `POST`
   - **Body**:
     ```json
     {
         "user_id": {user_id},
         "session_id": {session_id},
         "session_name": {session_name},
         "question_message": {question_message}
     }
     ```
   - **Response 예시**:
     ```json
     {
         "answer": {
             "input": "API 스펙 중 aNS는 어떤 것을 뜻하나요?",
             "output": "\"aNS\"는 일반적으로 \"Application Name Server\"의 약어로 사용됩니다..."
         }
     }
     ```

2. **채팅방 목록 가져오기**
   - **URL**: `http://localhost:8000/get-chat-list?user_id={user_id}`
   - **Method**: `GET`
   - **Response 예시**:
     ```json
     [
         {
             "session_id": "session_1_user_1",
             "session_name": "Chat 1"
         },
         {
             "session_id": "session_2_user_1",
             "session_name": "Chat 2"
         }
     ]
     ```

3. **채팅 메시지 목록 가져오기**
   - **URL**: `http://localhost:8000/get-chat-messages?session_id={session_id}`
   - **Method**: `GET`
   - **Response 예시**:
     ```json
     [
         {
             "input": "안녕?",
             "output": "안녕하세요! 어떻게 도와드릴까요?"
         },
         {
             "input": "마이데이터에 대해 설명해줘",
             "output": "마이데이터(MyData)는 개인이 자신의 데이터를 주체적으로 관리하고 활용할 수 있도록..."
         }
     ]
     ```

## 주요 종속성

- **Python**: `^3.12`
- **FastAPI**: `^0.112.0`
- **Uvicorn**: `^0.30.6` (ASGI 서버)
- **OpenAI**: `^1.40.6` (OpenAI API 연동)
- **LangChain**: `^0.2.13` (LangChain 프레임워크)
- **LangChain-Community**: `^0.2.12`
- **pypdf**: `^4.3.1` (PDF 처리)
- **ChromaDB**: `^0.5.5` (벡터 DB)
- **Tiktoken**: `^0.7.0` (토크나이저)
- **Sentence-Transformers**: `^3.0.1` (문장 임베딩)
- **python-dotenv**: `^1.0.1` (환경 변수 관리)
- **LangChain-OpenAI**: `^0.1.21`
- **LangChain-Huggingface**: `^0.0.3`
- **Pandas**: `^2.2.2` (데이터 처리)

## 빌드 시스템

- **Poetry**: 프로젝트 관리 및 의존성 관리 도구
- **Build 백엔드**: `poetry-core`

## 실행 시 주의 사항

.env 파일에 OPEN_API_KEY, LANCHAIN_API_KEY를 세팅하고 python-dotenv를 통해 세팅하여 실행하므로

프로젝트 다운로드 후 .env 파일을 생성하여 위 두개의 키를 추가해야 Agent 생성 가능 (필요 시 첨부파일 참고)
