from enum import Enum
from dataclasses import dataclass
from typing import Dict, Tuple
import re

# Análise de sentimento usando padrões
class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"

class EmotionalState(str, Enum):
    JOY = "joy"
    SADNESS = "sadness"
    ANXIETY = "anxiety"
    ANGER = "anger"
    FEAR = "fear"
    CONFUSION = "confusion"
    HOPE = "hope"
    FRUSTRATION = "frustration"
    CALM = "calm"
    OVERWHELMED = "overwhelmed"

@dataclass
class EmotionAnalysis:
    """Resultado da análise emocional"""
    sentiment: Sentiment
    emotional_state: EmotionalState
    confidence: float  # 0.0 a 1.0
    keywords: list[str]
    intensity: float  # 0.0 a 1.0 (força da emoção)

class EmotionAnalyzer:
    """Analisador de emoções e sentimentos"""
    
    # Dicionários de palavras-chave por emoção
    EMOTION_KEYWORDS = {
        EmotionalState.SADNESS: [
            'triste', 'deprimido', 'mal', 'infeliz', 'choro', 'chorar',
            'desanimado', 'vazio', 'sem esperança', 'sozinho', 'isolado',
            'melancolia', 'pena', 'luto', 'perda', 'fracasso'
        ],
        EmotionalState.ANXIETY: [
            'ansioso', 'nervoso', 'preocupado', 'medo', 'pânico', 'tenso',
            'estressado', 'inquieto', 'assustado', 'apreensivo', 'angustiado',
            'fobia', 'pânico', 'tremendo', 'suando'
        ],
        EmotionalState.ANGER: [
            'raiva', 'furioso', 'irritado', 'bravo', 'revoltado', 'indignado',
            'ódio', 'ressentido', 'frustrado', 'exasperado', 'agravado',
            'encolerizado', 'furibundo', 'irado'
        ],
        EmotionalState.FEAR: [
            'medo', 'assustado', 'apavorado', 'aterrorizado', 'medroso',
            'fobia', 'pânico', 'horror', 'pavor', 'susto', 'tremendo'
        ],
        EmotionalState.JOY: [
            'feliz', 'alegre', 'contente', 'animado', 'entusiasmado',
            'grato', 'grato', 'maravilhoso', 'incrível', 'ótimo', 'excelente',
            'amor', 'adoro', 'amando', 'perfeito'
        ],
        EmotionalState.HOPE: [
            'esperança', 'otimista', 'confiante', 'positivo', 'acredito',
            'possível', 'vou conseguir', 'conseguir', 'melhorar', 'progresso',
            'oportunidade', 'chance', 'futuro brilhante'
        ],
        EmotionalState.CONFUSION: [
            'confuso', 'perdido', 'desorientado', 'não entendo', 'incerto',
            'dúvida', 'indeciso', 'perplexo', 'atordoado', 'embaraçado'
        ],
        EmotionalState.FRUSTRATION: [
            'frustrado', 'decepcionado', 'insatisfeito', 'desapontado',
            'arrependido', 'ressentido', 'descontente', 'amargado'
        ],
        EmotionalState.OVERWHELMED: [
            'sobrecarregado', 'esgotado', 'cansado', 'exausto', 'sem força',
            'drenado', 'destruído', 'acabado', 'no limite', 'queimado'
        ],
        EmotionalState.CALM: [
            'calmo', 'tranquilo', 'sereno', 'pacífico', 'relaxado', 'zen',
            'em paz', 'equilibrado', 'centrado', 'mindful'
        ]
    }
    
    # Intensificadores de emoção
    INTENSIFIERS = ['muito', 'demais', 'extremamente', 'super', 'ultra', 'mega', 'bastante']
    
    # Negadores
    NEGATORS = ['não', 'nunca', 'jamais', 'nada']
    
    def analyze(self, text: str) -> EmotionAnalysis:
        """Analisa emoção e sentimento do texto"""
        text_lower = text.lower()
        
        # Detectar emoção primária
        emotional_state, confidence, keywords = self._detect_emotion(text_lower)
        
        # Detectar sentimento geral
        sentiment = self._detect_sentiment(text_lower, emotional_state)
        
        # Calcular intensidade
        intensity = self._calculate_intensity(text_lower, keywords)
        
        return EmotionAnalysis(
            sentiment=sentiment,
            emotional_state=emotional_state,
            confidence=confidence,
            keywords=keywords,
            intensity=intensity
        )
    
    def _detect_emotion(self, text: str) -> Tuple[EmotionalState, float, list[str]]:
        """Detecta a emoção primária do texto"""
        emotion_scores: Dict[EmotionalState, float] = {}
        found_keywords: Dict[EmotionalState, list[str]] = {state: [] for state in EmotionalState}
        
        for emotion, keywords in self.EMOTION_KEYWORDS.items():
            score = 0.0
            for keyword in keywords:
                if keyword in text:
                    score += 1.0
                    found_keywords[emotion].append(keyword)
            emotion_scores[emotion] = score
        
        # Encontrar emoção com maior score
        if max(emotion_scores.values()) == 0:
            return EmotionalState.CALM, 0.3, []
        
        primary_emotion = max(emotion_scores, key=emotion_scores.get)
        max_score = emotion_scores[primary_emotion]
        total_score = sum(emotion_scores.values())
        
        confidence = max_score / total_score if total_score > 0 else 0.5
        confidence = min(confidence, 1.0)
        
        return primary_emotion, confidence, found_keywords[primary_emotion]
    
    def _detect_sentiment(self, text: str, emotional_state: EmotionalState) -> Sentiment:
        """Detecta sentimento geral (positivo/negativo/neutro)"""
        positive_emotions = {EmotionalState.JOY, EmotionalState.HOPE, EmotionalState.CALM}
        negative_emotions = {EmotionalState.SADNESS, EmotionalState.ANXIETY, EmotionalState.ANGER, 
                            EmotionalState.FEAR, EmotionalState.FRUSTRATION, EmotionalState.OVERWHELMED}
        
        if emotional_state in positive_emotions:
            return Sentiment.POSITIVE
        elif emotional_state in negative_emotions:
            return Sentiment.NEGATIVE
        else:
            return Sentiment.NEUTRAL
    
    def _calculate_intensity(self, text: str, keywords: list[str]) -> float:
        """Calcula a intensidade da emoção (0.0 a 1.0)"""
        intensity = 0.0
        
        # Base: número de palavras-chave encontradas
        intensity += min(len(keywords) * 0.2, 0.5)
        
        # Intensificadores
        intensifier_count = sum(1 for intensifier in self.INTENSIFIERS if intensifier in text)
        intensity += min(intensifier_count * 0.15, 0.3)
        
        # Pontuação (exclamações, reticências)
        exclamation_count = text.count('!')
        intensity += min(exclamation_count * 0.1, 0.2)
        
        # Caps lock (palavras em maiúscula)
        caps_words = len([word for word in text.split() if word.isupper() and len(word) > 1])
        intensity += min(caps_words * 0.1, 0.2)
        
        return min(intensity, 1.0)

# Instância global
emotion_analyzer = EmotionAnalyzer()
