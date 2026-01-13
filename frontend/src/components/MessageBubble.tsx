import React from 'react'
import { formatDistanceToNow } from 'date-fns'
import { ptBR } from 'date-fns/locale'
import clsx from 'clsx'

interface MessageBubbleProps {
  message: {
    role: 'user' | 'assistant'
    content: string
    emotional_state?: string
    emotion_intensity?: number
    created_at: string
  }
  showEmotion?: boolean
}

const emotionColors: Record<string, string> = {
  joy: 'bg-emotion-joy/20 border-emotion-joy',
  sadness: 'bg-emotion-sadness/20 border-emotion-sadness',
  anxiety: 'bg-emotion-anxiety/20 border-emotion-anxiety',
  anger: 'bg-emotion-anger/20 border-emotion-anger',
  fear: 'bg-emotion-fear/20 border-emotion-fear',
  calm: 'bg-emotion-calm/20 border-emotion-calm',
  hope: 'bg-emotion-hope/20 border-emotion-hope',
  confusion: 'bg-emotion-confusion/20 border-emotion-confusion',
  frustration: 'bg-emotion-frustration/20 border-emotion-frustration',
  overwhelmed: 'bg-emotion-overwhelmed/20 border-emotion-overwhelmed',
}

const emotionEmojis: Record<string, string> = {
  joy: '😊',
  sadness: '😢',
  anxiety: '😰',
  anger: '😠',
  fear: '😨',
  calm: '😌',
  hope: '🌟',
  confusion: '😕',
  frustration: '😤',
  overwhelmed: '😵',
}

export default function MessageBubble({ message, showEmotion }: MessageBubbleProps) {
  const isUser = message.role === 'user'
  const timeAgo = formatDistanceToNow(new Date(message.created_at), {
    addSuffix: true,
    locale: ptBR
  })

  return (
    <div className={clsx('flex', isUser ? 'justify-end' : 'justify-start', 'animate-slide-up')}>
      <div
        className={clsx(
          'max-w-md px-4 py-3 rounded-lg',
          isUser
            ? 'bg-empathic-600 text-white rounded-br-none'
            : 'bg-white text-gray-900 border border-gray-200 rounded-bl-none shadow'
        )}
      >
        {/* Indicador de Emoção */}
        {showEmotion && message.emotional_state && (
          <div className={clsx(
            'mb-2 p-2 rounded border-l-4',
            emotionColors[message.emotional_state] || 'bg-gray-100'
          )}>
            <div className="flex items-center gap-2 text-xs font-medium">
              <span>{emotionEmojis[message.emotional_state] || '💭'}</span>
              <span className="capitalize">{message.emotional_state}</span>
              {message.emotion_intensity && (
                <span className="ml-auto">
                  {Math.round(message.emotion_intensity * 100)}%
                </span>
              )}
            </div>
          </div>
        )}

        {/* Conteúdo */}
        <p className="text-sm leading-relaxed whitespace-pre-wrap break-words">
          {message.content}
        </p>

        {/* Timestamp */}
        <p
          className={clsx(
            'text-xs mt-2',
            isUser ? 'text-empathic-100' : 'text-gray-500'
          )}
        >
          {timeAgo}
        </p>
      </div>
    </div>
  )
}
