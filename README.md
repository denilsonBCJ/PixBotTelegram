### **PixBot – Automação de Pagamentos via Telegram e Mercado Pago**

O **PixBot** é um bot desenvolvido em **Python** que automatiza vendas e libera acessos no **Telegram** após confirmação de pagamento via **PIX (Mercado Pago)**.
Ele gera links de pagamento únicos, verifica automaticamente o status da transação e envia o link de acesso ao cliente assim que o pagamento é aprovado.

### 🧠 **Principais recursos**

* 💬 Interface simples via **bot do Telegram**
* 💰 Integração completa com **API do Mercado Pago**
* 🔐 Pagamentos via **PIX com verificação automática**
* 📦 Suporte para múltiplos produtos configuráveis
* 🔗 Envio automático de links VIP após confirmação do pagamento
* ⚙️ Configuração via **variáveis de ambiente (.env)**

### 🚀 **Tecnologias utilizadas**

* Python 3.10+
* Telegram Bot API (`python-telegram-bot`)
* Mercado Pago API (via `requests`)
* dotenv para configuração de ambiente
* logging para registro de eventos

### 🧩 **Como usar**

1. Crie um bot no Telegram via [@BotFather](https://t.me/BotFather) e obtenha o token.
2. Crie uma conta no [Mercado Pago Developers](https://www.mercadopago.com.br/developers/panel) e gere seu **Access Token**.
3. Crie um arquivo `.env` com as seguintes variáveis:

   ```bash
   TELEGRAM_BOT_TOKEN=seu_token_do_telegram
   MERCADO_PAGO_TOKEN=seu_token_do_mercado_pago
   WEBHOOK_URL=https://webhook.site/seu-link-de-teste
   ```
4. Instale as dependências:

   ```bash
   pip install python-telegram-bot requests python-dotenv
   ```
5. Execute o bot:

   ```bash
   python main.py
   ```

### 📊 **Exemplo de uso**

O usuário inicia o bot → escolhe um infoproduto → paga via PIX → e recebe automaticamente o link do infoproduto no Telegram.
Ideal para **vendas de acesso a grupos, canais premium ou produtos digitais**.

### 📜 **Licença**

Este projeto é distribuído sob a licença MIT — sinta-se livre para modificar e adaptar.

