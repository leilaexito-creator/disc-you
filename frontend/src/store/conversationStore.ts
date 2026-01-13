import { create } from 'zustand'

interface ConversationStore {
  conversationId: string | null
  setConversationId: (id: string) => void
  clearConversation: () => void
}

export const useConversationStore = create<ConversationStore>((set) => ({
  conversationId: null,
  setConversationId: (id: string) => set({ conversationId: id }),
  clearConversation: () => set({ conversationId: null }),
}))
