# 🤖 Empathic AI Coach

Uma IA conversacional empática e inteligente, focada em interação emocional e sensível. Semelhante ao ChatGPT, mas especializada em coaching emocional com análise de sentimento, contexto persistente e segurança emocional integrada.

## 🎯 Características Principais

### 🧠 Inteligência Emocional
- **Detecção de 10 estados emocionais**: Alegria, Tristeza, Ansiedade, Raiva, Medo, Confusão, Frustração, Esperança, Calma, Sobrecarregado
- **Análise de Sentimento**: Positivo, Neutro, Negativo
- **Cálculo de Intensidade**: Força da emoção (0-100%)
- **Confiança de Classificação**: Precisão da análise

### 💬 Conversação Natural
- **Prompt Dinâmico**: Sistema de prompt adaptado por emoção
- **Contexto Persistente**: Memória de até 10 mensagens anteriores
- **Histórico Completo**: Todas as conversas salvas no banco de dados
- **Streaming de Respostas**: Respostas em tempo real

### 🛡️ Segurança Emocional
- **Detecção de Crise**: Identifica risco de suicídio/auto-agressão
- **Detecção de Abuso**: Reconhece situações de violência
- **Redirecionamento**: Encaminha para profissionais quando necessário
- **Recursos de Emergência**: Links para linhas de crise
- **Proteção contra Dependência**: Monitora e desestimula dependência emocional

### 📊 Análise Avançada
- **Análise de Segurança**: Classifica mensagens por nível de risco
- **Logs de Auditoria**: Registra eventos importantes
- **Histórico Emocional**: Rastreia padrões emocionais

## 🏗️ Arquitetura Técnica

### Backend
```
FastAPI (Python 3.11)
├── Emotion Analyzer (análise de sentimento)
├── Dynamic Prompt Builder (prompt adaptativo)
├── Emotional Safety Guard (proteção)
├── LLM Service (integração OpenAI/Claude)
└── Database Layer (PostgreSQL)
```

### Banco de Dados
```
PostgreSQL
├── Users (usuários e preferências)
├── Conversations (conversas)
├── Messages (mensagens com análise)
├── Sessions (contexto em cache)
└── AuditLogs (segurança)
```

### IA
```
OpenAI GPT-4 ou Claude 3.5 Sonnet
├── System Prompt Dinâmico
├── Contexto de Conversa
├── Análise Emocional
└── Streaming
```

## 🚀 Instalação

### Pré-requisitos
- Python 3.11+
- PostgreSQL 12+
- Redis (opcional, para cache)

### Setup

1. **Clonar repositório**
```bash
git clone <repo>
cd empathic-ai
```

2. **Criar ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instalar dependências**
```bash
pip install -r requirements.txt
```

4. **Configurar variáveis de ambiente**
```bash
cp .env.example .env
# Editar .env com suas configurações
```

5. **Iniciar banco de dados**
```bash
# PostgreSQL deve estar rodando
# Criar banco de dados
createdb empathic_ai
```

6. **Iniciar servidor**
```bash
python -m uvicorn backend.main:app --reload
```

Servidor estará disponível em: `http://localhost:8000`

## 📚 API Endpoints

### POST `/api/v1/messages`
Enviar mensagem e obter resposta empática

**Request:**
```json
{
  "content": "Estou me sentindo triste",
  "conversation_id": "optional-id"
}
```

**Response:**
```json
{
  "conversation_id": "conv-123",
  "user_message": {
    "id": "msg-1",
    "role": "user",
    "content": "Estou me sentindo triste",
    "emotional_state": "sadness",
    "emotion_intensity": 0.85,
    "created_at": "2024-01-12T10:30:00"
  },
  "assistant_message": {
    "id": "msg-2",
    "role": "assistant",
    "content": "Percebo que você está se sentindo triste...",
    "created_at": "2024-01-12T10:30:05"
  },
  "emotion_analysis": {
    "state": "sadness",
    "sentiment": "negative",
    "confidence": 0.92,
    "intensity": 0.85,
    "keywords": ["triste", "sentindo"]
  }
}
```

### GET `/api/v1/conversations`
Listar todas as conversas

### GET `/api/v1/conversations/{conversation_id}`
Obter conversa com histórico completo

### DELETE `/api/v1/conversations/{conversation_id}`
Deletar conversa

### GET `/api/v1/audit-logs`
Obter logs de auditoria

## 🧪 Fluxo de Processamento

```
Usuário digita mensagem
    ↓
[1] Análise de Segurança
    ├─ Detecta crise/abuso/dependência
    └─ Se crítico → Retorna recursos de emergência
    ↓
[2] Análise de Sentimento
    ├─ Classifica emoção (10 estados)
    ├─ Calcula sentimento (pos/neg/neutro)
    └─ Mede intensidade (0-100%)
    ↓
[3] Busca de Contexto
    └─ Últimas 10 mensagens da conversa
    ↓
[4] Construção de Prompt Dinâmico
    ├─ System prompt adaptado à emoção
    ├─ Instruções específicas de tom
    └─ Contexto da conversa
    ↓
[5] Chamada ao LLM
    ├─ OpenAI GPT-4 ou Claude 3.5
    └─ Streaming de resposta
    ↓
[6] Salvamento no Histórico
    ├─ Mensagem do usuário
    ├─ Resposta do assistente
    └─ Análise emocional
    ↓
[7] Resposta ao Usuário
    └─ Mensagem empática e contextualizada
```

## 🛡️ Segurança Emocional

### Detecção de Crise
```python
# Palavras-chave que acionam alerta
"suicida", "suicídio", "me matar", "morrer", "fim"
"não aguento mais", "desistir", "acabar com isso"
```

### Resposta de Crise
```
I'm genuinely concerned about what you're sharing. Your safety is important.

Please reach out to a mental health professional immediately:

🆘 CRISIS RESOURCES:
- National Suicide Prevention Lifeline: 988 (US)
- Crisis Text Line: Text HOME to 741741
- International resources: [links]
```

### Proteção contra Dependência
- Monitora comprimento de conversa
- Detecta padrões de dependência emocional
- Encoraja busca de apoio humano
- Reforça limites saudáveis

## 📊 Exemplo de Análise Emocional

**Entrada:** "Estou muito ansioso com a entrevista de amanhã. Tenho medo de não conseguir!"

**Análise:**
```json
{
  "emotional_state": "anxiety",
  "sentiment": "negative",
  "confidence": 0.94,
  "intensity": 0.78,
  "keywords": ["ansioso", "medo", "não conseguir"]
}
```

**Prompt Dinâmico Gerado:**
```
Tone: calm, grounding, reassuring
Response Length: medium
Approach: Help ground in present moment, break down worries
Include: breathing techniques, perspective, actionable steps
```

**Resposta Gerada:**
```
Reconheço sua ansiedade. É completamente normal se sentir assim antes de uma entrevista importante.

Vamos transformar esse medo em preparação:

1. Respire profundamente - 4 segundos inspirando, 4 expirando
2. Qual é o pior cenário que você imagina?
3. Se isso acontecesse, como você lidaria?

Frequentemente, quando exploramos o medo, descobrimos que somos mais capazes do que pensávamos.
```

## 🔧 Configuração Avançada

### Variáveis de Ambiente Importantes

```env
# LLM Provider
LLM_PROVIDER=openai  # ou "anthropic"
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=...

# Segurança
MAX_CONVERSATION_LENGTH=50
CONTEXT_WINDOW=10
RATE_LIMIT_REQUESTS=100

# Monitoramento
ENABLE_AUDIT_LOGS=True
LOG_LEVEL=INFO
```

### Customização de Emoções

Editar `backend/emotion_analyzer.py`:
```python
EMOTION_KEYWORDS = {
    EmotionalState.CUSTOM: [
        'palavra1', 'palavra2', 'palavra3'
    ]
}
```

## 📈 Métricas e Monitoramento

### Logs de Auditoria
- Eventos de segurança
- Alertas de crise
- Padrões de uso
- Erros do sistema

### Histórico Emocional
- Emoções mais frequentes
- Intensidade média
- Padrões temporais
- Progressão do usuário

## 🚨 Considerações Legais e Éticas

### Importante
- **NÃO é substituto para terapia profissional**
- **NÃO fornece diagnóstico médico**
- **NÃO fornece conselho jurídico**
- **Deve redirecionar para profissionais quando apropriado**

### Responsabilidades
- Manter logs de segurança
- Respeitar privacidade do usuário
- Implementar rate limiting
- Monitorar abuso do sistema

## 📝 Roadmap

- [ ] Frontend React com interface empática
- [ ] Autenticação e autorização
- [ ] Análise de padrões emocionais
- [ ] Recomendações de recursos
- [ ] Integração com profissionais
- [ ] Mobile app (Flutter/React Native)
- [ ] Multilingual support
- [ ] Voice interface

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:
1. Fork o repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

MIT License - veja LICENSE.md para detalhes

## 📞 Suporte

Para questões, issues ou sugestões:
- Abra uma issue no GitHub
- Entre em contato através do email
- Consulte a documentação

---

**Desenvolvido com ❤️ para criar conexões empáticas através da IA**
