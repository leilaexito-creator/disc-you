import React, { useState, useRef, useEffect } from 'react'
import { Send, Loader, Heart, AlertCircle, TrendingUp } from 'lucide-react'
import { useConversationStore } from '../store/conversationStore'
import { useChatService } from '../hooks/useChatService'
import MessageBubble from './MessageBubble'
import EmotionIndicator from './EmotionIndicator'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  emotional_state?: string
  emotion_intensity?: number
  created_at: string
}

export default function ChatInterface() {
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const [currentEmotion, setCurrentEmotion] = useState<any>(null)
  const [safetyAlert, setSafetyAlert] = useState<any>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const { conversationId, setConversationId } = useConversationStore()
  const { sendMessage } = useChatService()

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      created_at: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await sendMessage(input, conversationId)

      if (response.safety_alert) {
        setSafetyAlert(response)
        setMessages(prev => [...prev, {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: response.message,
          created_at: new Date().toISOString()
        }])
      } else {
        setConversationId(response.conversation_id)
        setCurrentEmotion(response.emotion_analysis)

        setMessages(prev => [...prev, {
          id: response.assistant_message.id,
          role: 'assistant',
          content: response.assistant_message.content,
          created_at: response.assistant_message.created_at
        }])
      }
    } catch (error) {
      console.error('Erro ao enviar mensagem:', error)
      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Desculpe, tive um problema ao processar sua mensagem. Tente novamente.',
        created_at: new Date().toISOString()
      }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-empathic-50 to-empathic-100">
      {/* Header */}
      <div className="bg-gradient-to-r from-empathic-600 to-empathic-700 text-white p-6 shadow-lg">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold flex items-center gap-2 mb-2">
            <Heart className="text-red-300" size={32} />
            Empathic AI Coach
          </h1>
          <p className="text-empathic-100">Conversação empática com IA inteligente</p>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 overflow-y-auto p-6">
        <div className="max-w-4xl mx-auto space-y-4">
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full text-center py-12">
              <Heart size={64} className="text-empathic-300 mb-4" />
              <h2 className="text-2xl font-bold text-gray-800 mb-2">Bem-vindo ao Empathic AI</h2>
              <p className="text-gray-600 max-w-md">
                Sou aqui para ouvir, entender e apoiar você. Compartilhe seus pensamentos e sentimentos livremente.
              </p>
            </div>
          )}

          {messages.map((message) => (
            <MessageBubble
              key={message.id}
              message={message}
              showEmotion={message.role === 'user' && currentEmotion}
            />
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-white rounded-lg shadow p-4 flex items-center gap-2">
                <Loader size={20} className="animate-spin text-empathic-600" />
                <span className="text-gray-600">Coach está pensando...</span>
              </div>
            </div>
          )}

          {safetyAlert && (
            <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
              <div className="flex gap-3">
                <AlertCircle className="text-red-600 flex-shrink-0" size={24} />
                <div>
                  <h3 className="font-bold text-red-800">Alerta de Segurança</h3>
                  <p className="text-red-700 text-sm mt-1">{safetyAlert.message}</p>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Emotion Indicator */}
      {currentEmotion && (
        <div className="bg-white border-t border-gray-200 px-6 py-4">
          <div className="max-w-4xl mx-auto">
            <EmotionIndicator emotion={currentEmotion} />
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 p-6">
        <div className="max-w-4xl mx-auto">
          <form onSubmit={handleSendMessage} className="flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Compartilhe seus pensamentos..."
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-empathic-600 focus:border-transparent"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="bg-empathic-600 text-white px-6 py-3 rounded-lg hover:bg-empathic-700 transition disabled:opacity-50 flex items-center gap-2 font-medium"
            >
              {loading ? (
                <Loader size={20} className="animate-spin" />
              ) : (
                <Send size={20} />
              )}
              Enviar
            </button>
          </form>
          <p className="text-xs text-gray-500 mt-2">
            💡 Dica: Seja honesto sobre seus sentimentos. Estou aqui para ouvir sem julgamentos.
          </p>
        </div>
      </div>
    </div>
  )
}
