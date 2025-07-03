import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# ตั้งค่า
os.environ["OPENAI_API_KEY"] = "your-api-key"
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Router
router = APIRouter(prefix="/chat", tags=["chat"])

# Schema
class ChatRequest(BaseModel):
    message: str

# API Route
@router.post("/")
async def chat(request: ChatRequest):
    try:
        # ส่งข้อความไป LLM
        messages = [HumanMessage(content=request.message)]
        response = await llm.ainvoke(messages)
        
        return {"reply": response.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))