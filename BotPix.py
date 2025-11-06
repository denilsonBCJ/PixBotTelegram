import os
import logging
import requests
import hashlib
import secrets
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

from dotenv import load_dotenv
load_dotenv()

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Verifica se o token do Telegram está definido
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("❌ Token do Telegram não encontrado. Defina a variável TELEGRAM_BOT_TOKEN.")

CONFIG = {
    'TOKEN': TELEGRAM_TOKEN,
    'MP_TOKEN': os.getenv("MERCADO_PAGO_TOKEN"),
    'WEBHOOK_URL': os.getenv("WEBHOOK_URL", "https://webhook.site/your-webhook-url")
}

PRODUTOS = {
    "1": {"nome": "NOME DO PRODUTO AQUI", "preco": 20.00, "ativo": True},
    "2": {"nome": "NOME DO PRODUTO AQUI", "preco": 20.00, "ativo": True},
    "3": {"nome": "NOME DO PRODUTO AQUI", "preco": 20.00, "ativo": True},
    "4": {"nome": "NOME DO PRODUTO AQUI", "preco": 20.00, "ativo": True},
    "5": {"nome": "NOME DO PRODUTO AQUI", "preco": 20.00, "ativo": True},

    

    
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Exibe os produtos disponíveis."""
    keyboard = [
        [InlineKeyboardButton(f"{p['nome']} - R${p['preco']:.2f}", callback_data=f"pagar_{k}")]
        for k, p in PRODUTOS.items() if p['ativo']
    ]
    await update.message.reply_text(
    f"🛍️ Olá, {update.message.from_user.first_name}! 👋 Bem-vindo(a) ao melhor canal de sinais VIP🎰🔥!",
    reply_markup=InlineKeyboardMarkup(keyboard),
    parse_mode='Markdown'
)

async def create_payment(user_id: int, product_id: str):
    """Cria um link de pagamento PIX."""
    produto = PRODUTOS.get(product_id)
    if not produto:
        raise ValueError("Produto inválido")

    transaction_id = hashlib.sha256(
        f"{datetime.now().timestamp()}{product_id}{user_id}{secrets.token_urlsafe(8)}".encode()
    ).hexdigest()

    payload = {
        "items": [{
            "title": produto['nome'],
            "quantity": 1,
            "unit_price": float(produto['preco']),
            "currency_id": "BRL"
        }],
        "payment_methods": {"default_payment_method_id": "pix"},
        "external_reference": transaction_id,
        "notification_url": CONFIG['WEBHOOK_URL']
    }

    headers = {
        "Authorization": f"Bearer {CONFIG['MP_TOKEN']}",
        "Content-Type": "application/json",
        "X-Idempotency-Key": transaction_id
    }

    response = requests.post("https://api.mercadopago.com/checkout/preferences", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()['init_point'], transaction_id

async def handle_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa o pagamento ao clicar no botão."""
    query = update.callback_query
    await query.answer()
    product_id = query.data.replace("pagar_", "")
    
    try:
        payment_url, transaction_id = await create_payment(query.from_user.id, product_id)
        
        # Salva a transaction_id no contexto do usuário
        context.user_data['transaction_id'] = transaction_id
        context.user_data['product_id'] = product_id
        
        # Cria teclado com botão de pagamento e verificação
        keyboard = [
            [InlineKeyboardButton("🔗 Pagar com PIX", url=payment_url)],
            [InlineKeyboardButton("✅ JÁ PAGUEI", callback_data="verificar_pagamento")]
        ]
        
        await query.edit_message_text(
            text=f"💳 *{PRODUTOS[product_id]['nome']}*\n"
                 f"💵 Valor: R${PRODUTOS[product_id]['preco']:.2f}\n\n"
                 "1. Clique em 'Pagar com PIX' para realizar o pagamento\n"
                 "2. Após pagar, clique em 'JÁ PAGUEI' para liberar seu acesso\n\n"
                 f"⏳ Link válido por 30 minutos\n"
                 f"🔢 Código da transação: `{transaction_id}`",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard),
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.error(f"Erro ao gerar pagamento: {str(e)}")
        await query.edit_message_text("❌ Falha ao processar pagamento")

async def verificar_pagamento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia o processo de verificação."""
    query = update.callback_query
    await query.answer()
    
    # Verifica se existe uma transação pendente
    if 'transaction_id' not in context.user_data or 'product_id' not in context.user_data:
        await query.edit_message_text("❌ Nenhum pagamento pendente encontrado.")
        return
    
    transaction_id = context.user_data['transaction_id']
    product_id = context.user_data['product_id']
    
    try:
        # Verifica o pagamento na API do Mercado Pago
        headers = {"Authorization": f"Bearer {CONFIG['MP_TOKEN']}"}
        response = requests.get(
            f"https://api.mercadopago.com/v1/payments/search?external_reference={transaction_id}",
            headers=headers
        )
        payment_data = response.json()
        
        if payment_data['results'] and payment_data['results'][0]['status'] == 'approved':
            # Links específicos para cada produto
            group_links = {
                "1": "LINK DO SEU PRODUTO AQUI",  #PESSE O LINKE DO SEU PRODUTO AQUI
                "2": "LINK DO SEU PRODUTO AQUI", 
                "3": "LINK DO SEU PRODUTO AQUI",
                "4": "LINK DO SEU PRODUTO AQUI",
                "5": "LINK DO SEU PRODUTO AQUI", 
            }
            
            group_link = group_links.get(product_id, "https://t.me/link_generico")
            
            await query.edit_message_text(
                text=f"✅ *Pagamento confirmado!*\n\n"
                f"Acesso ao {PRODUTOS[product_id]['nome']} liberado!\n"
                f"🌟 *Aproveite seu VIP!*\n\n"
                f"👉 Acesse o grupo VIP através deste link: [Clique aqui para entrar no grupo]({group_link})\n"
                "🎉 Aproveite o conteúdo exclusivo!",
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
            # Limpa os dados temporários
            context.user_data.pop('transaction_id', None)
            context.user_data.pop('product_id', None)
        else:
            keyboard = [
                [InlineKeyboardButton("🔄 Tentar novamente", callback_data="verificar_pagamento")]
            ]
            await query.edit_message_text(
                text="⚠️ *Pagamento não encontrado ou ainda não aprovado*\n\n"
                     "Por favor, aguarde alguns minutos e tente novamente.\n"
                     "Se já fez o pagamento, o sistema pode demorar alguns minutos para processar.",
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            
    except Exception as e:
        logger.error(f"Erro na verificação: {str(e)}")
        await query.edit_message_text("❌ Erro ao verificar pagamento. Tente novamente mais tarde.")
def main():
    """Inicializa o bot."""
    app = Application.builder().token(CONFIG['TOKEN']).build()
    
    # Handlers de comandos
    app.add_handler(CommandHandler("start", start))
    
    # Handlers de callbacks
    app.add_handler(CallbackQueryHandler(handle_payment, pattern="^pagar_"))
    app.add_handler(CallbackQueryHandler(verificar_pagamento, pattern="^verificar_pagamento$"))
    
    logger.info("🤖 Bot iniciado com sucesso")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()