from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
import logging
from datetime import datetime, timedelta
from typing import Optional, List

from backend.config import settings
from backend.models import Base, User, Conversation, Message, AuditLog
from backend.emotion_analyzer import emotion_analyzer
from backend.emotional_safety import safety_guard, SafetyLevel
from backend.llm_service import llm_service
from backend.dynamic_prompt import prompt_builder

# Configurar logging
logging.basicConfig(level=getattr(logging, settings.log_level))
logger = logging.getLogger(__name__)

# Criar aplicação FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Empathic AI Coach - Conversational AI with Emotional Intelligence"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency para obter sessão do banco"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modelos Pydantic
from pydantic import BaseModel

class MessageRequest(BaseModel):
    content: str
    conversation_id: Optional[str] = None

class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    emotional_state: Optional[str] = None
    created_at: datetime

class ConversationResponse(BaseModel):
    id: str
    title: Optional[str] = None
    primary_emotion: Optional[str] = None
    message_count: int
    created_at: datetime

# Rotas

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.post("/api/v1/messages")
async def send_message(
    request: MessageRequest,
    db: Session = Depends(get_db)
):
    """Enviar mensagem e obter resposta empática"""
    
    try:
        # Análise de segurança
        safety_analysis = safety_guard.analyze(request.content)
        
        if safety_analysis.level == SafetyLevel.CRITICAL:
            # Log de auditoria
            if settings.enable_audit_logs:
                audit_log = AuditLog(
                    event_type="safety_alert",
                    event_data={
                        "type": "crisis_detected",
                        "message": request.content[:100]
                    },
                    safety_level="CRITICAL"
                )
                db.add(audit_log)
                db.commit()
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "safety_alert": True,
                    "message": safety_analysis.redirect_message,
                    "level": safety_analysis.level
                }
            )
        
        # Análise emocional
        emotion_analysis = emotion_analyzer.analyze(request.content)
        
        # Buscar ou criar conversa
        conversation = None
        if request.conversation_id:
            conversation = db.query(Conversation).filter(
                Conversation.id == request.conversation_id
            ).first()
        
        if not conversation:
            conversation = Conversation(
                title=f"Conversation - {emotion_analysis.emotional_state.value}",
                primary_emotion=emotion_analysis.emotional_state.value,
                sentiment=emotion_analysis.sentiment.value
            )
            db.add(conversation)
            db.flush()
        
        # Salvar mensagem do usuário
        user_message = Message(
            conversation_id=conversation.id,
            content=request.content,
            role="user",
            emotional_state=emotion_analysis.emotional_state.value,
            sentiment=emotion_analysis.sentiment.value,
            emotion_confidence=emotion_analysis.confidence,
            emotion_intensity=emotion_analysis.intensity,
            emotion_keywords=emotion_analysis.keywords,
            safety_level=safety_analysis.level.value if safety_analysis.level != SafetyLevel.SAFE else None
        )
        db.add(user_message)
        db.flush()
        
        # Buscar histórico de conversa
        conversation_history = db.query(Message).filter(
            Message.conversation_id == conversation.id
        ).order_by(Message.created_at).all()
        
        # Converter para formato esperado pelo LLM
        history = [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in conversation_history[-10:]  # Últimas 10 mensagens
        ]
        
        # Gerar resposta com IA
        ai_response = await llm_service.generate_response(
            user_message=request.content,
            emotion_analysis=emotion_analysis,
            conversation_history=history
        )
        
        # Salvar resposta do assistente
        assistant_message = Message(
            conversation_id=conversation.id,
            content=ai_response,
            role="assistant"
        )
        db.add(assistant_message)
        
        # Atualizar conversa
        conversation.message_count += 2
        conversation.updated_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "conversation_id": conversation.id,
            "user_message": {
                "id": user_message.id,
                "role": "user",
                "content": request.content,
                "emotional_state": emotion_analysis.emotional_state.value,
                "emotion_intensity": emotion_analysis.intensity,
                "created_at": user_message.created_at
            },
            "assistant_message": {
                "id": assistant_message.id,
                "role": "assistant",
                "content": ai_response,
                "created_at": assistant_message.created_at
            },
            "emotion_analysis": {
                "state": emotion_analysis.emotional_state.value,
                "sentiment": emotion_analysis.sentiment.value,
                "confidence": emotion_analysis.confidence,
                "intensity": emotion_analysis.intensity,
                "keywords": emotion_analysis.keywords
            }
        }
    
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar mensagem")

@app.get("/api/v1/conversations")
async def list_conversations(
    db: Session = Depends(get_db)
):
    """Listar conversas"""
    conversations = db.query(Conversation).order_by(
        Conversation.updated_at.desc()
    ).limit(20).all()
    
    return [
        {
            "id": conv.id,
            "title": conv.title,
            "primary_emotion": conv.primary_emotion,
            "message_count": conv.message_count,
            "created_at": conv.created_at,
            "updated_at": conv.updated_at
        }
        for conv in conversations
    ]

@app.get("/api/v1/conversations/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """Obter conversa com histórico"""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at).all()
    
    return {
        "id": conversation.id,
        "title": conversation.title,
        "primary_emotion": conversation.primary_emotion,
        "message_count": conversation.message_count,
        "created_at": conversation.created_at,
        "messages": [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "emotional_state": msg.emotional_state,
                "created_at": msg.created_at
            }
            for msg in messages
        ]
    }

@app.delete("/api/v1/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """Deletar conversa"""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    
    db.delete(conversation)
    db.commit()
    
    return {"status": "deleted"}

@app.get("/api/v1/audit-logs")
async def get_audit_logs(
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obter logs de auditoria (apenas para admin)"""
    if not settings.enable_audit_logs:
        raise HTTPException(status_code=403, detail="Audit logs desabilitados")
    
    logs = db.query(AuditLog).order_by(
        AuditLog.created_at.desc()
    ).limit(limit).all()
    
    return [
        {
            "id": log.id,
            "event_type": log.event_type,
            "safety_level": log.safety_level,
            "created_at": log.created_at
        }
        for log in logs
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
