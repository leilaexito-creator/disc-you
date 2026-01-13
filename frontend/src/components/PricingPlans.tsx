import React, { useState } from 'react';
import { Check } from 'lucide-react';

interface Plan {
  id: string;
  name: string;
  price: number;
  description: string;
  features: string[];
  recurring: boolean;
}

const PLANS: Plan[] = [
  {
    id: 'teste_unico',
    name: 'DISC YOU - Avaliação Completa',
    price: 249,
    description: 'Teste único com relatório completo',
    features: [
      'Teste DISC completo',
      'Relatório 10 páginas',
      'Análise comportamental',
      'Plano de ação',
      'Acesso único',
    ],
    recurring: false,
  },
  {
    id: 'starter',
    name: 'DISC YOU - Starter',
    price: 49.9,
    description: 'Plano mensal básico',
    features: [
      'Testes ilimitados',
      '1.000 mensagens IA/mês',
      'Histórico 30 dias',
      'Suporte por email',
      'Sem anúncios',
    ],
    recurring: true,
  },
  {
    id: 'professional',
    name: 'DISC YOU - Professional',
    price: 99.9,
    description: 'Plano mensal profissional',
    features: [
      'Testes ilimitados',
      '5.000 mensagens IA/mês',
      'Histórico 90 dias',
      'Suporte email + chat',
      'Sem anúncios',
      'API básico',
    ],
    recurring: true,
  },
  {
    id: 'premium',
    name: 'DISC YOU - Premium',
    price: 199.9,
    description: 'Plano mensal premium',
    features: [
      'Testes ilimitados',
      '20.000 mensagens IA/mês',
      'Histórico 180 dias',
      'Suporte 24/7',
      'Sem anúncios',
      'API profissional',
      'Análise avançada',
    ],
    recurring: true,
  },
];

export const PricingPlans: React.FC = () => {
  const [loading, setLoading] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleCheckout = async (planId: string) => {
    setLoading(planId);
    setError(null);

    try {
      // Obter dados do usuário (você precisa implementar autenticação)
      const userId = localStorage.getItem('user_id') || 'guest-' + Date.now();
      const userEmail = localStorage.getItem('user_email') || 'user@example.com';

      // Chamar backend para criar sessão de checkout
      const response = await fetch('/api/v1/checkout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          plan: planId,
          user_id: userId,
          user_email: userEmail,
        }),
      });

      if (!response.ok) {
        throw new Error('Erro ao criar checkout');
      }

      const data = await response.json();

      if (data.checkout_url) {
        // Redirecionar para Stripe Checkout
        window.location.href = data.checkout_url;
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro desconhecido';
      setError(errorMessage);
      console.error('Erro ao processar checkout:', err);
    } finally {
      setLoading(null);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 py-12 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-slate-900 mb-4">
            Escolha seu Plano
          </h1>
          <p className="text-xl text-slate-600">
            Comece com o teste único ou escolha um plano mensal
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="max-w-2xl mx-auto mb-8 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-800">❌ {error}</p>
          </div>
        )}

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {PLANS.map((plan) => (
            <div
              key={plan.id}
              className="bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden flex flex-col"
            >
              {/* Card Header */}
              <div className="bg-gradient-to-r from-teal-500 to-cyan-500 p-6 text-white">
                <h3 className="text-xl font-bold mb-2">{plan.name}</h3>
                <p className="text-sm opacity-90">{plan.description}</p>
              </div>

              {/* Price */}
              <div className="px-6 py-6 border-b border-slate-200">
                <div className="flex items-baseline gap-2">
                  <span className="text-4xl font-bold text-slate-900">
                    R$ {plan.price.toFixed(2)}
                  </span>
                  {plan.recurring && (
                    <span className="text-slate-600">/mês</span>
                  )}
                </div>
              </div>

              {/* Features */}
              <div className="px-6 py-6 flex-grow">
                <ul className="space-y-3">
                  {plan.features.map((feature, idx) => (
                    <li key={idx} className="flex items-start gap-3">
                      <Check className="w-5 h-5 text-teal-500 flex-shrink-0 mt-0.5" />
                      <span className="text-slate-700 text-sm">{feature}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Button */}
              <div className="px-6 py-6 border-t border-slate-200">
                <button
                  onClick={() => handleCheckout(plan.id)}
                  disabled={loading === plan.id}
                  className={`w-full py-3 px-4 rounded-lg font-semibold transition-all duration-200 ${
                    loading === plan.id
                      ? 'bg-slate-300 text-slate-600 cursor-not-allowed'
                      : 'bg-gradient-to-r from-teal-500 to-cyan-500 text-white hover:shadow-lg hover:scale-105'
                  }`}
                >
                  {loading === plan.id ? (
                    <span className="flex items-center justify-center gap-2">
                      <span className="animate-spin">⏳</span>
                      Processando...
                    </span>
                  ) : (
                    'Assinar Agora'
                  )}
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="text-center mt-12">
          <p className="text-slate-600">
            Todos os planos incluem acesso completo ao DISC YOU
          </p>
          <p className="text-slate-500 text-sm mt-2">
            Pagamentos seguros com Stripe • PIX, Cartão de Débito e Crédito
          </p>
          <p className="text-slate-400 text-xs mt-4">
            Mais um produto do <span className="font-semibold text-slate-500">Grupo Êxito Empresarial</span>
          </p>
        </div>
      </div>
    </div>
  );
};
