from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.controller import chat_controller
from app.manager.chat_data_manager import load_chat_data
from app.manager.chat_list_manager import load_chat_list
from app.utils.resource_initializer import initialize_resources

load_dotenv()

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    app.state.retriever, app.state.rag_prompt = initialize_resources()
    load_chat_list()
    load_chat_data()

app.include_router(chat_controller.router)