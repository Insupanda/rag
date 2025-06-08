from pathlib import Path
from typing import Any

from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel

from config.settings import settings
from db.sql_utils import TemplateManager
from services.insurance_service import InsuranceService

app = FastAPI(title="보험 상담 챗봇 API")

PROJECT_ROOT = Path(__file__).parent.resolve()
template_manager = TemplateManager(templates_dir=PROJECT_ROOT / "prompts")
openai_client = OpenAI(api_key=settings.openai_api_key)
insurance_service = InsuranceService(openai_client, template_manager)


# 요청/응답 스키마
class ChatRequest(BaseModel):
    user_input: str


class ChatResponse(BaseModel):
    response: Any


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    """
    클라이언트가 보낸 질문(user_input)에 대해
    InsuranceService로 처리하고 응답을 반환합니다.
    """
    response = insurance_service.run(req.user_input)
    return ChatResponse(response=response)
