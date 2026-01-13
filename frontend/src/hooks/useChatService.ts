import axios from 'axios'

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export function useChatService() {
  const sendMessage = async (content: string, conversationId: string | null) => {
    try {
      const response = await apiClient.post('/api/v1/messages', {
        content,
        conversation_id: conversationId,
      })
      return response.data
    } catch (error) {
      console.error('Erro ao enviar mensagem:', error)
      throw error
    }
  }

  const getConversations = async () => {
    try {
      const response = await apiClient.get('/api/v1/conversations')
      return response.data
    } catch (error) {
      console.error('Erro ao buscar conversas:', error)
      throw error
    }
  }

  const getConversation = async (conversationId: string) => {
    try {
      const response = await apiClient.get(`/api/v1/conversations/${conversationId}`)
      return response.data
    } catch (error) {
      console.error('Erro ao buscar conversa:', error)
      throw error
    }
  }

  const deleteConversation = async (conversationId: string) => {
    try {
      const response = await apiClient.delete(`/api/v1/conversations/${conversationId}`)
      return response.data
    } catch (error) {
      console.error('Erro ao deletar conversa:', error)
      throw error
    }
  }

  return {
    sendMessage,
    getConversations,
    getConversation,
    deleteConversation,
  }
}
