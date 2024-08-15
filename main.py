import os

from dotenv import load_dotenv
from fastapi import FastAPI

from app.controller import chat_controller
from app.utils.resource_initializer import initialize_resources

load_dotenv()

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    app.state.retriever, app.state.rag_prompt, app.state.llm = initialize_resources()

app.include_router(chat_controller.router)