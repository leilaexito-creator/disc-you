import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { CheckCircle, AlertCircle } from 'lucide-react';

export const PaymentSuccess: React.FC = () => {
  const [searchParams] = useSearchParams();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [paymentInfo, setPaymentInfo] = useState<any>(null);

  const sessionId = searchParams.get('session_id');

  useEffect(() => {
    const verifyPayment = async () => {
      if (!sessionId) {
        setStatus('error');
        return;
      }

      try {
        const response = await fetch(`/api/v1/payment-status?session_id=${sessionId}`);
        const data = await response.json();

        if (data.error) {
          setStatus('error');
        } else {
          setPaymentInfo(data);
          setStatus('success');
        }
      } catch (error) {
        console.error('Erro ao verificar pagamento:', error);
        setStatus('error');
      }
    };

    verifyPayment();
  }, [sessionId]);

  if (status === 'loading') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center px-4">
        <div className="text-center">
          <div className="animate-spin mb-4">
            <div className="w-16 h-16 border-4 border-teal-200 border-t-teal-500 rounded-full"></div>
          </div>
          <p className="text-xl text-slate-600">Verificando seu pagamento...</p>
        </div>
      </div>
    );
  }

  if (status === 'error') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center px-4">
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-md w-full text-center">
          <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-slate-900 mb-2">
            Erro no Pagamento
          </h1>
          <p className="text-slate-600 mb-6">
            Desculpe, não conseguimos verificar seu pagamento. Por favor, tente novamente.
          </p>
          <a
            href="/pricing"
            className="inline-block bg-gradient-to-r from-teal-500 to-cyan-500 text-white px-6 py-3 rounded-lg font-semibold hover:shadow-lg transition-all"
          >
            Voltar para Planos
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center px-4">
      <div className="bg-white rounded-lg shadow-lg p-8 max-w-md w-full text-center">
        <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4 animate-bounce" />
        
        <h1 className="text-3xl font-bold text-slate-900 mb-2">
          ✅ Pagamento Confirmado!
        </h1>
        
        <p className="text-slate-600 mb-6">
          Seu pagamento foi processado com sucesso. Seu acesso foi ativado!
        </p>

        {paymentInfo && (
          <div className="bg-slate-50 rounded-lg p-4 mb-6 text-left">
            <div className="space-y-2 text-sm">
              <div>
                <span className="text-slate-600">Status:</span>
                <span className="ml-2 font-semibold text-green-600">
                  {paymentInfo.status === 'paid' ? 'Pago' : paymentInfo.status}
                </span>
              </div>
              {paymentInfo.subscription && (
                <div>
                  <span className="text-slate-600">Assinatura:</span>
                  <span className="ml-2 font-mono text-xs text-slate-700">
                    {paymentInfo.subscription.substring(0, 20)}...
                  </span>
                </div>
              )}
            </div>
          </div>
        )}

        <div className="space-y-3">
          <a
            href="/dashboard"
            className="block w-full bg-gradient-to-r from-teal-500 to-cyan-500 text-white px-6 py-3 rounded-lg font-semibold hover:shadow-lg transition-all"
          >
            Ir para Dashboard
          </a>
          
          <a
            href="/"
            className="block w-full bg-slate-200 text-slate-900 px-6 py-3 rounded-lg font-semibold hover:bg-slate-300 transition-all"
          >
            Voltar para Home
          </a>
        </div>

        <p className="text-slate-500 text-xs mt-6">
          Um email de confirmação foi enviado para você.
        </p>
      </div>
    </div>
  );
};
