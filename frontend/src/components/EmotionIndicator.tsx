import React from 'react'
import { TrendingUp, AlertCircle } from 'lucide-react'
import clsx from 'clsx'

interface EmotionAnalysis {
  state: string
  sentiment: string
  confidence: number
  intensity: number
  keywords: string[]
}

const emotionColors: Record<string, string> = {
  joy: 'from-emotion-joy to-yellow-300',
  sadness: 'from-emotion-sadness to-blue-300',
  anxiety: 'from-emotion-anxiety to-red-300',
  anger: 'from-emotion-anger to-red-500',
  fear: 'from-emotion-fear to-purple-400',
  calm: 'from-emotion-calm to-green-300',
  hope: 'from-emotion-hope to-cyan-300',
  confusion: 'from-emotion-confusion to-amber-300',
  frustration: 'from-emotion-frustration to-orange-400',
  overwhelmed: 'from-emotion-overwhelmed to-gray-400',
}

const sentimentEmojis: Record<string, string> = {
  positive: '😊',
  neutral: '😐',
  negative: '😔'
}

export default function EmotionIndicator({ emotion }: { emotion: EmotionAnalysis }) {
  if (!emotion) return null

  const gradientClass = emotionColors[emotion.state] || 'from-empathic-400 to-empathic-600'

  return (
    <div className="bg-gradient-to-r from-gray-50 to-gray-100 rounded-lg p-4 border border-gray-200">
      <div className="flex items-start gap-4">
        {/* Indicador Visual */}
        <div className={clsx(
          'w-16 h-16 rounded-full bg-gradient-to-br flex items-center justify-center text-2xl shadow-md',
          gradientClass
        )}>
          {sentimentEmojis[emotion.sentiment] || '💭'}
        </div>

        {/* Informações */}
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <h3 className="font-bold text-gray-900 capitalize text-lg">
              {emotion.state}
            </h3>
            <span className="text-xs bg-gray-200 text-gray-700 px-2 py-1 rounded capitalize">
              {emotion.sentiment}
            </span>
          </div>

          {/* Barras de Progresso */}
          <div className="space-y-2">
            {/* Confiança */}
            <div>
              <div className="flex justify-between items-center mb-1">
                <span className="text-xs text-gray-600">Confiança</span>
                <span className="text-xs font-medium text-gray-700">
                  {Math.round(emotion.confidence * 100)}%
                </span>
              </div>
              <div className="w-full bg-gray-300 rounded-full h-2">
                <div
                  className="bg-empathic-600 h-2 rounded-full transition-all"
                  style={{ width: `${emotion.confidence * 100}%` }}
                />
              </div>
            </div>

            {/* Intensidade */}
            <div>
              <div className="flex justify-between items-center mb-1">
                <span className="text-xs text-gray-600">Intensidade</span>
                <span className="text-xs font-medium text-gray-700">
                  {Math.round(emotion.intensity * 100)}%
                </span>
              </div>
              <div className="w-full bg-gray-300 rounded-full h-2">
                <div
                  className={clsx(
                    'h-2 rounded-full transition-all',
                    emotion.intensity > 0.7 ? 'bg-red-500' :
                    emotion.intensity > 0.4 ? 'bg-yellow-500' :
                    'bg-green-500'
                  )}
                  style={{ width: `${emotion.intensity * 100}%` }}
                />
              </div>
            </div>
          </div>

          {/* Palavras-chave */}
          {emotion.keywords && emotion.keywords.length > 0 && (
            <div className="mt-3 pt-3 border-t border-gray-200">
              <p className="text-xs text-gray-600 mb-1">Palavras-chave detectadas:</p>
              <div className="flex flex-wrap gap-1">
                {emotion.keywords.map((keyword, idx) => (
                  <span
                    key={idx}
                    className="text-xs bg-empathic-100 text-empathic-700 px-2 py-1 rounded"
                  >
                    {keyword}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Ícone de Insight */}
        {emotion.intensity > 0.7 && (
          <div className="flex-shrink-0">
            <AlertCircle className="text-red-500" size={20} />
          </div>
        )}
      </div>
    </div>
  )
}
