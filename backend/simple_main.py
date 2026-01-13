from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
from datetime import datetime
from backend.emotion_analyzer import emotion_analyzer
from backend.emotional_safety import safety_guard, SafetyLevel
from backend.dynamic_prompt import prompt_builder
from backend.stripe_service import create_checkout_session, handle_webhook

app = FastAPI(
    title="Empathic AI Coach",
    version="1.0.0",
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

# In-memory storage (para demo)
conversations = {}
messages_store = {}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.post("/api/v1/messages")
async def send_message(request: dict):
    """Enviar mensagem e obter resposta empática"""
    
    try:
        content = request.get("content", "")
        conversation_id = request.get("conversation_id")
        
        # Análise de segurança
        safety_analysis = safety_guard.analyze(content)
        
        if safety_analysis.level == SafetyLevel.CRITICAL:
            return JSONResponse(
                status_code=200,
                content={
                    "safety_alert": True,
                    "message": safety_analysis.redirect_message,
                    "level": safety_analysis.level.value
                }
            )
        
        # Análise emocional
        emotion_analysis = emotion_analyzer.analyze(content)
        
        # Criar ou buscar conversa
        if not conversation_id:
            conversation_id = f"conv-{datetime.utcnow().timestamp()}"
            conversations[conversation_id] = {
                "id": conversation_id,
                "title": f"Conversation - {emotion_analysis.emotional_state.value}",
                "primary_emotion": emotion_analysis.emotional_state.value,
                "message_count": 0,
                "created_at": datetime.utcnow().isoformat()
            }
            messages_store[conversation_id] = []
        
        # Gerar resposta empática (versão simplificada)
        ai_response = generate_empathic_response(emotion_analysis, content)
        
        # Salvar mensagens
        user_msg_id = f"msg-{datetime.utcnow().timestamp()}"
        assistant_msg_id = f"msg-{datetime.utcnow().timestamp() + 0.001}"
        
        messages_store[conversation_id].append({
            "id": user_msg_id,
            "role": "user",
            "content": content,
            "emotional_state": emotion_analysis.emotional_state.value,
            "created_at": datetime.utcnow().isoformat()
        })
        
        messages_store[conversation_id].append({
            "id": assistant_msg_id,
            "role": "assistant",
            "content": ai_response,
            "created_at": datetime.utcnow().isoformat()
        })
        
        conversations[conversation_id]["message_count"] += 2
        
        return {
            "conversation_id": conversation_id,
            "user_message": {
                "id": user_msg_id,
                "role": "user",
                "content": content,
                "emotional_state": emotion_analysis.emotional_state.value,
                "emotion_intensity": emotion_analysis.intensity,
                "created_at": datetime.utcnow().isoformat()
            },
            "assistant_message": {
                "id": assistant_msg_id,
                "role": "assistant",
                "content": ai_response,
                "created_at": datetime.utcnow().isoformat()
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
        print(f"Erro: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def generate_empathic_response(emotion_analysis, user_input: str) -> str:
    """Gera resposta empática baseada na emoção"""
    
    responses = {
        "sadness": [
            "Percebo que você está se sentindo triste. Isso é completamente válido. Quer compartilhar o que está causando isso?",
            "Vejo que há tristeza em suas palavras. Estou aqui para ouvir. O que você gostaria de explorar?",
            "Entendo que você está passando por um momento difícil. Sua dor é importante. Fale-me mais sobre isso."
        ],
        "anxiety": [
            "Sinto que há preocupação em suas palavras. Vamos respirar juntos e explorar o que está gerando essa ansiedade.",
            "Reconheço sua ansiedade. É normal se sentir assim. Qual é a preocupação mais urgente agora?",
            "Percebo que você está nervoso. Vamos quebrar isso em partes menores. Por onde começamos?"
        ],
        "anger": [
            "Entendo sua raiva. Essa emoção é válida e importante. O que a está causando?",
            "Percebo uma frustração forte em suas palavras. Vamos explorar isso juntos. O que aconteceu?",
            "Sua raiva me diz que algo importante foi violado. Quer compartilhar?"
        ],
        "joy": [
            "Que maravilhoso! Estou feliz por você! O que está trazendo essa alegria?",
            "Que energia positiva! Conte-me mais sobre isso. Como você está se sentindo?",
            "Adorei ouvir isso! Vamos celebrar juntos. O que tornou isso possível?"
        ],
        "calm": [
            "Você parece centrado. Isso é ótimo. Sobre o que você gostaria de conversar?",
            "Sinto uma tranquilidade em você. Qual é o tema que você quer explorar?",
            "Você está bem equilibrado. Vamos aprofundar em algo que importa para você?"
        ],
        "hope": [
            "Que esperança bonita! Vejo potencial em suas palavras. Vamos construir sobre isso?",
            "Adorei esse otimismo! Como podemos transformar essa esperança em ação?",
            "Sua confiança é inspiradora. Qual é o próximo passo?"
        ],
        "confusion": [
            "Percebo que você está um pouco confuso. Tudo bem. Vamos esclarecer as coisas juntos.",
            "Entendo a incerteza. Vamos explorar isso passo a passo. Por onde começamos?",
            "Há confusão em suas palavras. Vamos simplificar. Qual é a questão principal?"
        ],
        "frustration": [
            "Sinto sua frustração. É válida. O que está causando isso?",
            "Entendo que algo não está funcionando como esperado. Vamos resolver isso juntos.",
            "Sua frustração me diz que você se importa. Vamos encontrar uma solução."
        ],
        "overwhelmed": [
            "Você parece sobrecarregado. Tudo bem. Vamos respirar e simplificar as coisas.",
            "Sinto que há muito acontecendo. Vamos focar em uma coisa de cada vez.",
            "Você está no limite. Vamos desacelerar. O que é mais urgente agora?"
        ]
    }
    
    emotion_key = emotion_analysis.emotional_state.value
    emotion_responses = responses.get(emotion_key, responses["calm"])
    
    # Escolher resposta aleatória
    import random
    return random.choice(emotion_responses)

@app.get("/api/v1/conversations")
async def list_conversations():
    """Listar conversas"""
    return list(conversations.values())

@app.get("/api/v1/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Obter conversa com histórico"""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    
    conv = conversations[conversation_id]
    conv["messages"] = messages_store.get(conversation_id, [])
    return conv

@app.delete("/api/v1/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Deletar conversa"""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    
    del conversations[conversation_id]
    if conversation_id in messages_store:
        del messages_store[conversation_id]
    
    return {"status": "deleted"}

# ========== ROTAS STRIPE ==========

@app.post("/api/v1/checkout")
async def checkout(plan: str, user_id: str, user_email: str):
    """
    Criar sessão de checkout Stripe
    
    Exemplo de uso:
    POST /api/v1/checkout?plan=starter&user_id=123&user_email=user@example.com
    """
    result = await create_checkout_session(plan, user_id, user_email)
    return result


@app.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    """
    Webhook do Stripe para processar eventos de pagamento
    
    Eventos processados:
    - checkout.session.completed (pagamento realizado)
    - customer.subscription.updated (assinatura atualizada)
    - customer.subscription.deleted (assinatura cancelada)
    - invoice.payment_succeeded (pagamento recebido)
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    result = await handle_webhook(payload, sig_header)
    return result


@app.get("/api/v1/payment-status")
async def payment_status(session_id: str):
    """
    Verificar status do pagamento
    
    Exemplo de uso:
    GET /api/v1/payment-status?session_id=cs_test_123
    """
    import stripe
    
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return {
            "status": session.payment_status,
            "customer": session.customer,
            "subscription": session.subscription,
            "metadata": session.metadata,
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
