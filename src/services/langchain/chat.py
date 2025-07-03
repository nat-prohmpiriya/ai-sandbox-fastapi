from typing import List, Dict, Optional, Union
import uuid
from datetime import datetime
from src.models.chat import ChatMessage, ChatSession, MessageRole
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from src.config.settings import settings
import os

os.environ["GOOGLE_API_KEY"] = settings.google_api_key

class Chat:
    def __init__(self) -> None:
        pass

    async def create_chat_session(self, user_id: str, title: Optional[str] = None) -> str:
        """Create a new chat session and save to MongoDB"""
        session: ChatSession = ChatSession(
            user_id=user_id,
            title=title or "New Chat",
            is_active=True,
            messages=[],
            message_count=0,
            created_at=datetime.utcnow()
        )
        await session.insert()
        return str(session.id)

    async def get_chat_sessions(self, user_id: str) -> List[ChatSession]:
        """Get all chat sessions for a user"""
        return await ChatSession.find(ChatSession.user_id == user_id, ChatSession.deleted_at == None).to_list()

    async def get_chat_session(self, session_id: str) -> Optional[ChatSession]:
        """Get a specific chat session by ID"""
        return await ChatSession.get(session_id)

    async def update_chat_session(self, session_id: str, title: Optional[str] = None) -> bool:
        """Update chat session title"""
        session: Optional[ChatSession] = await ChatSession.get(session_id)
        if session:
            if title:
                session.title = title
            session.updated_at = datetime.utcnow()
            await session.save()
            return True
        return False

    async def delete_chat_session(self, session_id: str) -> bool:
        """Soft delete chat session"""
        session: Optional[ChatSession] = await ChatSession.get(session_id)
        if session:
            session.deleted_at = datetime.utcnow()
            session.is_active = False
            await session.save()
            return True
        return False

    async def create_message(self, session_id: str, role: MessageRole, content: str) -> Optional[str]:
        """Create a message in a chat session"""
        session: Optional[ChatSession] = await ChatSession.get(session_id)
        if session:
            message: ChatMessage = ChatMessage(
                id=str(uuid.uuid4()),
                role=role,
                content=content,
                chat_session_id=session_id,
                created_at=datetime.utcnow()
            )
            session.messages.append(message)
            session.message_count += 1
            session.last_message_at = datetime.utcnow()
            session.updated_at = datetime.utcnow()
            await session.save()
            return message.id
        return None

    async def get_messages(self, session_id: str) -> List[ChatMessage]:
        """Get all messages in a chat session"""
        session: Optional[ChatSession] = await ChatSession.get(session_id)
        if session:
            return [msg for msg in session.messages if msg.deleted_at is None]
        return []


    async def update_message(self, session_id: str, message_id: str, new_content: str) -> bool:
        """Update a message content"""
        session: Optional[ChatSession] = await ChatSession.get(session_id)
        if session:
            for message in session.messages:
                if message.id == message_id and message.deleted_at is None:
                    message.content = new_content
                    message.updated_at = datetime.utcnow()
                    await session.save()
                    return True
        return False

    async def delete_message(self, session_id: str, message_id: str) -> bool:
        """Soft delete a message"""
        session: Optional[ChatSession] = await ChatSession.get(session_id)
        if session:
            for message in session.messages:
                if message.id == message_id:
                    message.deleted_at = datetime.utcnow()
                    await session.save()
                    return True
        return False
    
    async def chat_with_ai(
            self, 
            session_id: str, 
            user_message: str, 
            system_prompt: Optional[str] = None,
            model: str = "gemini-2.0-flash",
            temperature: float = 0.2,
            max_output_tokens: int = 1024,
            top_p: float = 0.95,
            top_k: int = 40
        ) -> Optional[Dict[str, str]]:
        """Chat with AI and save messages to database"""
        try:
            # Create user message
            user_msg_id: Optional[str] = await self.create_message(session_id, MessageRole.USER, user_message)
            if not user_msg_id:
                return None

            # Initialize AI model
            googleLLm: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(
                model=model,
                temperature=temperature,
                max_output_tokens=max_output_tokens,
                top_p=top_p,
                top_k=top_k,
                response_model="text",
                stream=False,
            )

            # Get chat history
            messages: List[ChatMessage] = await self.get_messages(session_id)
            
            # Build conversation for AI
            conversation: List[Union[SystemMessage, HumanMessage, AIMessage]] = []
            
            # Add system prompt if provided
            if system_prompt:
                conversation.append(SystemMessage(content=system_prompt))
            
            # Add message history
            for msg in messages:
                if msg.role == MessageRole.USER:
                    conversation.append(HumanMessage(content=msg.content))
                elif msg.role == MessageRole.ASSISTANT:
                    conversation.append(AIMessage(content=msg.content))

            # Get AI response
            response = await googleLLm.ainvoke(conversation)
            ai_response: str = response.content

            # Save AI response
            ai_msg_id: Optional[str] = await self.create_message(session_id, MessageRole.ASSISTANT, ai_response)
            
            return {
                "user_message_id": user_msg_id,
                "ai_message_id": ai_msg_id,
                "response": ai_response
            }
            
        except Exception as e:
            raise Exception(f"AI chat error: {str(e)}")
