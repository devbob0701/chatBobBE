from fastapi import FastAPI
from app.controller import chat_controller

app = FastAPI()

app.include_router(chat_controller.router)