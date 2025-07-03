from typing import List, Dict, Any, Optional, Union
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from src.services.langchain.chat import Chat
from src.middlewares.auth import get_current_user
from src.models.user import User
from src.models.chat import ChatSession, ChatMessage

router: APIRouter = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    system_prompt: Optional[str] = None
    model: Optional[str] = "gemini-2.0-flash"
    temperature: Optional[float] = 0.2
    max_output_tokens: Optional[int] = 1024
    top_p: Optional[float] = 0.95
    top_k: Optional[int] = 40

class CreateSessionRequest(BaseModel):
    title: Optional[str] = None

class UpdateSessionRequest(BaseModel):
    title: str

@router.post("/sessions")
async def create_chat_session(
    request: CreateSessionRequest,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Create a new chat session"""
    try:
        chat_service: Chat = Chat()
        session_id: str = await chat_service.create_chat_session(
            user_id=current_user.uid,
            title=request.title
        )
        return {"session_id": session_id, "message": "Chat session created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating session: {str(e)}")

@router.get("/sessions")
async def get_chat_sessions(
    current_user: User = Depends(get_current_user)
) -> List[ChatSession]:
    """Get all chat sessions for current user"""
    try:
        chat_service: Chat = Chat()
        return await chat_service.get_chat_sessions(current_user.uid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting sessions: {str(e)}")

@router.get("/sessions/{session_id}")
async def get_chat_session(
    session_id: str,
    current_user: User = Depends(get_current_user)
) -> Optional[ChatSession]:
    """Get a specific chat session"""
    try:
        chat_service: Chat = Chat()
        session: Optional[ChatSession] = await chat_service.get_chat_session(session_id)
        if session and session.user_id == current_user.uid:
            return session
        raise HTTPException(status_code=404, detail="Session not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting session: {str(e)}")

@router.put("/sessions/{session_id}")
async def update_chat_session(
    session_id: str,
    request: UpdateSessionRequest,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Update chat session title"""
    try:
        chat_service: Chat = Chat()
        session: Optional[ChatSession] = await chat_service.get_chat_session(session_id)
        if not session or session.user_id != current_user.uid:
            raise HTTPException(status_code=404, detail="Session not found")
        
        success: bool = await chat_service.update_chat_session(session_id, request.title)
        if success:
            return {"message": "Session updated successfully"}
        raise HTTPException(status_code=400, detail="Failed to update session")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating session: {str(e)}")

@router.delete("/sessions/{session_id}")
async def delete_chat_session(
    session_id: str,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Delete a chat session"""
    try:
        chat_service: Chat = Chat()
        session: Optional[ChatSession] = await chat_service.get_chat_session(session_id)
        if not session or session.user_id != current_user.uid:
            raise HTTPException(status_code=404, detail="Session not found")
        
        success: bool = await chat_service.delete_chat_session(session_id)
        if success:
            return {"message": "Session deleted successfully"}
        raise HTTPException(status_code=400, detail="Failed to delete session")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting session: {str(e)}")

@router.get("/sessions/{session_id}/messages")
async def get_messages(
    session_id: str,
    current_user: User = Depends(get_current_user)
) -> List[ChatMessage]:
    """Get all messages in a chat session"""
    try:
        chat_service: Chat = Chat()
        session: Optional[ChatSession] = await chat_service.get_chat_session(session_id)
        if not session or session.user_id != current_user.uid:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return await chat_service.get_messages(session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting messages: {str(e)}")

@router.post("/")
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Chat with AI - creates session if not provided and saves messages to database
    """
    try:
        chat_service: Chat = Chat()
        
        # Create new session if not provided
        if not request.session_id:
            session_id: str = await chat_service.create_chat_session(
                user_id=current_user.uid,
                title="New Chat"
            )
        else:
            session_id = request.session_id
            # Verify session belongs to user
            session: Optional[ChatSession] = await chat_service.get_chat_session(session_id)
            if not session or session.user_id != current_user.uid:
                raise HTTPException(status_code=404, detail="Session not found")
        
        # Chat with AI
        result: Optional[Dict[str, str]] = await chat_service.chat_with_ai(
            session_id=session_id,
            user_message=request.message,
            system_prompt=request.system_prompt,
            model=request.model,
            temperature=request.temperature,
            max_output_tokens=request.max_output_tokens,
            top_p=request.top_p,
            top_k=request.top_k
        )
        
        if result:
            return {
                "session_id": session_id,
                "reply": result["response"],
                "user_message_id": result["user_message_id"],
                "ai_message_id": result["ai_message_id"]
            }
        
        raise HTTPException(status_code=400, detail="Failed to process chat")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")
    

