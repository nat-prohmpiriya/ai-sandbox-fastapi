from typing import List, Dict, Any, Optional, Union
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from src.config.settings import settings
import os

os.environ["GOOGLE_API_KEY"] = settings.google_api_key

router: APIRouter = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    system_prompt: Optional[str] = None
    model: Optional[str] = "gemini-2.0-flash"
    temperature: Optional[float] = 0.2
    max_output_tokens: Optional[int] = 1024
    top_p: Optional[float] = 0.95
    top_k: Optional[int] = 40
    response_model: Optional[str] = "text"
    stream: Optional[bool] = True

@router.post("/")
async def chat(request: ChatRequest) -> Dict[str, Any]:
    """
    Chat endpoint สำหรับรับข้อความจากผู้ใช้และตอบกลับด้วย AI
    ผู้ใช้สามารถกำหนดค่าพารามิเตอร์ของโมเดลได้เอง
    """
    try:
        googleLLm: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(
            model=request.model,
            temperature=request.temperature,
            max_output_tokens=request.max_output_tokens,
            top_p=request.top_p,
            top_k=request.top_k,
            response_model=request.response_model,
            stream=request.stream,
        )

        system_prompt: str = request.system_prompt or "You are a helpful AI assistant."
        messages: List[Union[SystemMessage, HumanMessage]] = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=request.message)
        ]
        response = await googleLLm.ainvoke(messages)
        return {"reply": response.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")