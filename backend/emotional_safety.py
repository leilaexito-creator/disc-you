from enum import Enum
from dataclasses import dataclass
from typing import Optional, Tuple

class SafetyLevel(str, Enum):
    SAFE = "safe"
    WARNING = "warning"
    CRITICAL = "critical"
    REDIRECT_NEEDED = "redirect_needed"

@dataclass
class SafetyAnalysis:
    """Resultado da análise de segurança"""
    level: SafetyLevel
    reason: str
    action: str  # Ação recomendada
    redirect_message: Optional[str] = None

class EmotionalSafetyGuard:
    """Monitora e garante segurança emocional nas interações"""
    
    # Palavras-chave que indicam risco
    CRISIS_KEYWORDS = [
        'suicida', 'suicídio', 'me matar', 'morrer', 'morte', 'fim',
        'não aguento mais', 'não posso mais', 'desistir', 'acabar com isso',
        'pular da janela', 'overdose', 'veneno', 'corda', 'faca',
        'auto-agressão', 'me cortar', 'machucar a mim mesmo'
    ]
    
    # Palavras que indicam abuso/violência
    ABUSE_KEYWORDS = [
        'abuso', 'violência', 'agredido', 'espancado', 'violado',
        'assalto', 'estupro', 'tortura', 'maltratado'
    ]
    
    # Palavras que indicam dependência emocional
    DEPENDENCY_KEYWORDS = [
        'você é meu único', 'não consigo viver sem você',
        'você é minha razão de viver', 'preciso de você para tudo',
        'não posso estar sem você', 'você é minha vida'
    ]
    
    # Palavras que indicam pedido de conselho médico/legal
    MEDICAL_KEYWORDS = [
        'prescrição', 'medicamento', 'diagnóstico', 'tratamento',
        'doença', 'sintoma', 'cura', 'cirurgia', 'remédio'
    ]
    
    LEGAL_KEYWORDS = [
        'advogado', 'processo', 'lei', 'crime', 'culpa', 'prisão',
        'tribunal', 'julgamento', 'direito', 'contrato'
    ]
    
    def analyze(self, text: str, conversation_length: int = 0) -> SafetyAnalysis:
        """Analisa segurança da mensagem"""
        text_lower = text.lower()
        
        # Verificar risco de crise
        if self._contains_keywords(text_lower, self.CRISIS_KEYWORDS):
            return SafetyAnalysis(
                level=SafetyLevel.CRITICAL,
                reason="Possible suicidal ideation or self-harm risk detected",
                action="IMMEDIATE INTERVENTION REQUIRED",
                redirect_message=self._get_crisis_response()
            )
        
        # Verificar abuso
        if self._contains_keywords(text_lower, self.ABUSE_KEYWORDS):
            return SafetyAnalysis(
                level=SafetyLevel.CRITICAL,
                reason="Possible abuse or violence situation detected",
                action="PROVIDE RESOURCES",
                redirect_message=self._get_abuse_response()
            )
        
        # Verificar dependência emocional excessiva
        if self._contains_keywords(text_lower, self.DEPENDENCY_KEYWORDS):
            return SafetyAnalysis(
                level=SafetyLevel.WARNING,
                reason="Signs of emotional dependency on AI detected",
                action="GENTLY REDIRECT TO HUMAN SUPPORT",
                redirect_message=self._get_dependency_response()
            )
        
        # Verificar pedidos de conselho médico
        if self._contains_keywords(text_lower, self.MEDICAL_KEYWORDS):
            return SafetyAnalysis(
                level=SafetyLevel.WARNING,
                reason="Medical advice request detected",
                action="REDIRECT TO MEDICAL PROFESSIONAL",
                redirect_message=self._get_medical_redirect()
            )
        
        # Verificar pedidos de conselho legal
        if self._contains_keywords(text_lower, self.LEGAL_KEYWORDS):
            return SafetyAnalysis(
                level=SafetyLevel.WARNING,
                reason="Legal advice request detected",
                action="REDIRECT TO LEGAL PROFESSIONAL",
                redirect_message=self._get_legal_redirect()
            )
        
        # Verificar comprimento excessivo de conversa (possível dependência)
        if conversation_length > 100:
            return SafetyAnalysis(
                level=SafetyLevel.WARNING,
                reason="Very long conversation - possible dependency forming",
                action="ENCOURAGE PROFESSIONAL SUPPORT",
                redirect_message=self._get_long_conversation_response()
            )
        
        return SafetyAnalysis(
            level=SafetyLevel.SAFE,
            reason="No safety concerns detected",
            action="PROCEED NORMALLY"
        )
    
    def _contains_keywords(self, text: str, keywords: list[str]) -> bool:
        """Verifica se texto contém keywords"""
        return any(keyword in text for keyword in keywords)
    
    def _get_crisis_response(self) -> str:
        """Resposta para situação de crise"""
        return """I'm genuinely concerned about what you're sharing. Your safety is important.

Please reach out to a mental health professional immediately:

🆘 CRISIS RESOURCES:
- National Suicide Prevention Lifeline: 988 (US)
- Crisis Text Line: Text HOME to 741741
- International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/

If you're in immediate danger, please call emergency services (911 in US).

I'm here to listen, but a trained mental health professional can provide the specialized support you need right now.

Would you like help finding resources in your area?"""
    
    def _get_abuse_response(self) -> str:
        """Resposta para situação de abuso"""
        return """I'm sorry you're experiencing this. What you're describing is serious, and you deserve support.

Please reach out to professionals who specialize in this:

🛡️ ABUSE RESOURCES:
- National Domestic Violence Hotline: 1-800-799-7233 (US)
- RAINN (Sexual Assault): 1-800-656-4673 (US)
- International resources: https://www.hotpeachpages.net/

Your safety comes first. These organizations can:
- Provide confidential support
- Help you create a safety plan
- Connect you with local resources
- Offer legal guidance

I'm here to listen, but trained professionals can provide specialized help.

Would you like information about resources in your area?"""
    
    def _get_dependency_response(self) -> str:
        """Resposta para sinais de dependência emocional"""
        return """I appreciate your trust in sharing this with me. I'm glad I can be helpful.

I want to be honest with you: while I can offer support and perspective, I'm an AI. The deep, ongoing support you might be seeking is best provided by real people who can truly know and care about you.

Consider reaching out to:
- A therapist or counselor
- Close friends or family
- Support groups
- Community resources

These human connections are irreplaceable and can provide the genuine support you deserve.

I'm here to help you think through things, but please don't let our conversations replace human relationships and professional support.

What human connections could you strengthen right now?"""
    
    def _get_medical_redirect(self) -> str:
        """Resposta para pedido de conselho médico"""
        return """I appreciate your trust, but I need to be clear: I'm not a medical professional and cannot provide medical advice.

For health concerns, please consult with:
- Your primary care physician
- A specialist in the relevant field
- A nurse hotline
- Urgent care or emergency services if needed

What I can do:
- Help you think through how to approach your doctor
- Explore your feelings about health concerns
- Support you emotionally through health challenges

Please prioritize getting professional medical guidance. Your health is too important to rely on AI.

How can I support you in getting the professional help you need?"""
    
    def _get_legal_redirect(self) -> str:
        """Resposta para pedido de conselho legal"""
        return """I appreciate your trust, but I cannot provide legal advice. Legal matters require professional expertise.

Please consult with:
- A licensed attorney
- Legal aid services (if cost is a concern)
- Bar association referral services
- Court-appointed legal counsel

What I can do:
- Help you think through your situation emotionally
- Support you as you navigate legal challenges
- Explore your feelings and concerns

Your legal situation deserves professional guidance. Please seek qualified legal counsel.

How can I support you emotionally through this process?"""
    
    def _get_long_conversation_response(self) -> str:
        """Resposta para conversas muito longas"""
        return """I notice we've been talking for quite a while now. I'm glad I could help, and I appreciate your openness.

I want to gently remind you: while I can offer perspective and support, ongoing emotional support is best provided by real people and professionals who can truly know you.

Consider:
- Talking to a therapist or counselor
- Sharing with trusted friends or family
- Joining a support group
- Exploring community resources

These human connections provide something I cannot: genuine, ongoing relationship and specialized expertise.

I'm here to help you think through things, but please don't let our conversations replace professional support and human relationships.

What steps could you take to build stronger human support?"""

# Instância global
safety_guard = EmotionalSafetyGuard()
