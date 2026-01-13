import stripe
import os
from fastapi import HTTPException

# Configurar chave secreta do Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Seus produtos/preços
PRODUCTS = {
    "teste_unico": {
        "name": "DISC YOU - Avaliação Completa",
        "price": 24900,  # R$ 249,00 em centavos
        "currency": "brl",
        "recurring": None,  # Não recorrente
    },
    "starter": {
        "name": "DISC YOU - Starter",
        "price": 4990,  # R$ 49,90 em centavos
        "currency": "brl",
        "recurring": {"interval": "month", "interval_count": 1},
    },
    "professional": {
        "name": "DISC YOU - Professional",
        "price": 9990,  # R$ 99,90 em centavos
        "currency": "brl",
        "recurring": {"interval": "month", "interval_count": 1},
    },
    "premium": {
        "name": "DISC YOU - Premium",
        "price": 19990,  # R$ 199,90 em centavos
        "currency": "brl",
        "recurring": {"interval": "month", "interval_count": 1},
    },
}


async def create_checkout_session(plan: str, user_id: str, user_email: str):
    """Criar sessão de checkout Stripe"""
    
    if plan not in PRODUCTS:
        raise HTTPException(status_code=400, detail="Plano inválido")
    
    product = PRODUCTS[plan]
    
    try:
        # Criar sessão de checkout
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": product["currency"],
                        "product_data": {
                            "name": product["name"],
                            "description": f"Plano {plan} do DISC YOU",
                        },
                        "unit_amount": product["price"],
                        **({"recurring": product["recurring"]} if product["recurring"] else {}),
                    },
                    "quantity": 1,
                }
            ],
            mode="payment" if not product["recurring"] else "subscription",
            success_url="https://discyou.org/payment-success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://discyou.org/payment-canceled",
            customer_email=user_email,
            metadata={
                "user_id": user_id,
                "plan": plan,
            },
        )
        
        return {"checkout_url": session.url}
    
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


async def handle_webhook(payload: bytes, sig_header: str):
    """Processar webhook do Stripe"""
    
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            webhook_secret
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Processar eventos
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session["metadata"]["user_id"]
        plan = session["metadata"]["plan"]
        
        # Ativar assinatura no banco de dados
        await activate_subscription(user_id, plan, session["id"])
        print(f"✅ Assinatura ativada: user={user_id}, plan={plan}")
    
    elif event["type"] == "customer.subscription.updated":
        subscription = event["data"]["object"]
        print(f"📝 Assinatura atualizada: {subscription['id']}")
        # Atualizar assinatura no banco
        await update_subscription(subscription)
    
    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        print(f"❌ Assinatura cancelada: {subscription['id']}")
        # Cancelar assinatura no banco
        await cancel_subscription(subscription)
    
    elif event["type"] == "invoice.payment_succeeded":
        invoice = event["data"]["object"]
        print(f"💰 Pagamento recebido: {invoice['id']}")
    
    return {"status": "success"}


async def activate_subscription(user_id: str, plan: str, session_id: str):
    """Ativar assinatura no banco de dados"""
    # TODO: Implementar lógica para salvar no banco
    print(f"Ativando assinatura: user={user_id}, plan={plan}, session={session_id}")


async def update_subscription(subscription):
    """Atualizar assinatura"""
    # TODO: Implementar lógica para atualizar no banco
    print(f"Atualizando assinatura: {subscription['id']}")


async def cancel_subscription(subscription):
    """Cancelar assinatura"""
    # TODO: Implementar lógica para cancelar no banco
    print(f"Cancelando assinatura: {subscription['id']}")
