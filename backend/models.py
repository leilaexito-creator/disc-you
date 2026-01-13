from sqlalchemy import Column, String, Integer, DateTime, Float, Text, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    """Modelo de usuário"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    
    # Perfil
    full_name = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    
    # Preferências
    preferred_tone = Column(String(50), default="empathic")  # empathic, direct, gentle, etc
    language = Column(String(10), default="pt-BR")
    
    # Histórico emocional
    emotional_baseline = Column(JSON, nullable=True)  # Estado emocional típico
    emotional_triggers = Column(JSON, nullable=True)  # Gatilhos conhecidos
    
    # Metadados
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_active = Column(DateTime, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Relacionamentos
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")

class Conversation(Base):
    """Modelo de conversa"""
    __tablename__ = "conversations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), index=True)
    
    # Contexto
    title = Column(String(255), nullable=True)
    topic = Column(String(255), nullable=True)
    
    # Análise emocional
    primary_emotion = Column(String(50), nullable=True)
    sentiment = Column(String(20), nullable=True)
    average_intensity = Column(Float, default=0.5)
    
    # Histórico
    message_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Status
    is_archived = Column(Boolean, default=False)
    
    # Relacionamentos
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    """Modelo de mensagem"""
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, ForeignKey("conversations.id"), index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    
    # Conteúdo
    content = Column(Text)
    role = Column(String(20))  # "user" ou "assistant"
    
    # Análise emocional (apenas para mensagens do usuário)
    emotional_state = Column(String(50), nullable=True)
    sentiment = Column(String(20), nullable=True)
    emotion_confidence = Column(Float, nullable=True)
    emotion_intensity = Column(Float, nullable=True)
    emotion_keywords = Column(JSON, nullable=True)
    
    # Análise de segurança
    safety_level = Column(String(20), nullable=True)
    safety_reason = Column(Text, nullable=True)
    
    # Metadados
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    tokens_used = Column(Integer, nullable=True)
    
    # Relacionamentos
    conversation = relationship("Conversation", back_populates="messages")
    user = relationship("User", back_populates="messages")

class Session(Base):
    """Modelo de sessão (para cache de contexto)"""
    __tablename__ = "sessions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), index=True)
    
    # Contexto da sessão
    context_data = Column(JSON)  # Últimas mensagens, estado emocional, etc
    conversation_id = Column(String, nullable=True)
    
    # Metadados
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)  # Quando a sessão expira
    
    # Relacionamentos
    user = relationship("User", back_populates="sessions")

class AuditLog(Base):
    """Modelo de log de auditoria para segurança"""
    __tablename__ = "audit_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=True, index=True)
    
    # Evento
    event_type = Column(String(50))  # "login", "message", "safety_alert", etc
    event_data = Column(JSON)
    
    # Segurança
    safety_level = Column(String(20), nullable=True)
    action_taken = Column(String(255), nullable=True)
    
    # Metadados
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(255), nullable=True)
