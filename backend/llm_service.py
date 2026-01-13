import openai
import anthropic
from backend.config import settings
from backend.emotion_analyzer import EmotionAnalysis
from backend.dynamic_prompt import prompt_builder
from typing import Optional, AsyncGenerator
import asyncio

class LLMService:
    """Serviço de integração com LLM (OpenAI ou Claude)"""
    
    def __init__(self):
        self.provider = settings.llm_provider
        
        if self.provider == "openai":
            self.client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
            self.model = "gpt-4-turbo-preview"
        else:
            self.client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
            self.model = "claude-3-5-sonnet-20241022"
    
    async def generate_response(
        self,
        user_message: str,
        emotion_analysis: EmotionAnalysis,
        conversation_history: list[dict],
        user_context: Optional[str] = None
    ) -> str:
        """Gera resposta empática baseada em análise emocional"""
        
        # Construir system prompt dinâmico
        context_str = self._format_conversation_context(conversation_history[-5:])  # Últimas 5 mensagens
        system_prompt = prompt_builder.build_system_prompt(emotion_analysis, context_str)
        
        # Preparar mensagens
        messages = self._prepare_messages(
            conversation_history,
            user_message,
            emotion_analysis
        )
        
        try:
            if self.provider == "openai":
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *messages
                    ],
                    temperature=0.7,
                    max_tokens=1000,
                    top_p=0.9,
                )
                return response.choices[0].message.content
            else:
                response = await self.client.messages.create(
                    model=self.model,
                    max_tokens=1000,
                    system=system_prompt,
                    messages=messages,
                    temperature=0.7,
                )
                return response.content[0].text
        
        except Exception as e:
            print(f"Erro ao gerar resposta: {e}")
            return self._get_fallback_response(emotion_analysis)
    
    async def stream_response(
        self,
        user_message: str,
        emotion_analysis: EmotionAnalysis,
        conversation_history: list[dict],
        user_context: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """Gera resposta em streaming"""
        
        context_str = self._format_conversation_context(conversation_history[-5:])
        system_prompt = prompt_builder.build_system_prompt(emotion_analysis, context_str)
        
        messages = self._prepare_messages(
            conversation_history,
            user_message,
            emotion_analysis
        )
        
        try:
            if self.provider == "openai":
                async with await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *messages
                    ],
                    temperature=0.7,
                    max_tokens=1000,
                    stream=True,
                ) as stream:
                    async for chunk in stream:
                        if chunk.choices[0].delta.content:
                            yield chunk.choices[0].delta.content
            else:
                with self.client.messages.stream(
                    model=self.model,
                    max_tokens=1000,
                    system=system_prompt,
                    messages=messages,
                    temperature=0.7,
                ) as stream:
                    for text in stream.text_stream:
                        yield text
        
        except Exception as e:
            print(f"Erro ao fazer streaming: {e}")
            yield self._get_fallback_response(emotion_analysis)
    
    def _prepare_messages(
        self,
        conversation_history: list[dict],
        user_message: str,
        emotion_analysis: EmotionAnalysis
    ) -> list[dict]:
        """Prepara lista de mensagens para o LLM"""
        
        messages = []
        
        # Adicionar histórico (últimas 10 mensagens)
        for msg in conversation_history[-10:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Adicionar mensagem atual com contexto emocional
        user_msg_with_context = prompt_builder.build_user_message(user_message, emotion_analysis)
        messages.append({
            "role": "user",
            "content": user_msg_with_context
        })
        
        return messages
    
    def _format_conversation_context(self, recent_messages: list[dict]) -> str:
        """Formata contexto da conversa"""
        if not recent_messages:
            return "This is the beginning of the conversation."
        
        context = "Recent conversation context:\n"
        for msg in recent_messages:
            role = "User" if msg["role"] == "user" else "Assistant"
            context += f"{role}: {msg['content'][:100]}...\n"
        
        return context
    
    def _get_fallback_response(self, emotion_analysis) -> str:
        """Resposta de fallback se LLM falhar"""
        
        fallback_responses = {
            "sadness": "I hear that you're going through a difficult time. Your feelings are valid. Would you like to talk about what's on your mind?",
            "anxiety": "I sense some worry in what you're sharing. Take a moment to breathe. What's the most pressing thing on your mind right now?",
            "anger": "I understand you're frustrated. That's a valid feeling. What would help you feel better right now?",
            "joy": "That's wonderful! I'm happy for you. Tell me more about what's bringing you joy.",
            "calm": "You seem grounded right now. What brought you here today?",
            "overwhelmed": "It sounds like a lot is happening. Let's take this one step at a time. What's the most urgent thing?",
        }
        
        emotion_key = emotion_analysis.emotional_state.value
        return fallback_responses.get(emotion_key, "I'm here to listen. What's on your mind?")

# Instância global
llm_service = LLMService()
