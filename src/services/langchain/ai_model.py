
from typing import Optional, Dict, List
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

class ChatRequest(BaseModel):
    message: str
    system_prompt: Optional[str] = None
    model: Optional[str] = "gemini-2.5flash"
    temperature: Optional[float] = 0.2
    max_output_tokens: Optional[int] = 1024
    top_p: Optional[float] = 0.95
    top_k: Optional[int] = 40
    response_model: Optional[str] = "text"
    stream: Optional[bool] = True

class AIModel:
    def __init__(self):
        pass

    def create_gemini(self, request: ChatRequest) -> ChatGoogleGenerativeAI:
        googleLLm: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(
            model=request.model,
            temperature=request.temperature,
            max_output_tokens=request.max_output_tokens,
            top_p=request.top_p,
            top_k=request.top_k,
            response_model=request.response_model,
            stream=request.stream,
        )
        return googleLLm

    def create_openai(self):
        pass

    def create_claude(self):
        pass

    