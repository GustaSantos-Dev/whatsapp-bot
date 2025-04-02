import requests
import openai

# 🔥 1. CONFIGURAÇÃO DO BOT (Adicione suas credenciais)
TOKEN = "YOUR_ACCESS_TOKEN"
PHONE_NUMBER_ID = "YOUR_PHONE_NUMBER_ID"
GOOGLE_SHEETS_API = "LINK_DA_SUA_API"
OPENAI_API_KEY = "SUA_CHAVE_OPENAI"


# 🔥 2. FUNÇÃO PARA ENVIAR MENSAGENS NO WHATSAPP
def enviar_mensagem(whatsapp_numero, mensagem):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": whatsapp_numero,
        "type": "text",
        "text": {
            "body": mensagem
        }
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.json())


# 🔥 3. RESPOSTAS AUTOMÁTICAS
def resposta_automatica(mensagem):
    mensagem = mensagem.lower()

    if "oi" in mensagem or "olá" in mensagem:
        return "Olá! Como posso te ajudar hoje? 😊"
    elif "preço" in mensagem:
        return "Nossos serviços variam entre R$100 e R$500. Qual serviço você precisa?"
    elif "horário" in mensagem:
        return "Atendemos de segunda a sexta, das 9h às 18h."
    else:
        return "Não entendi sua mensagem. Digite 'ajuda' para ver opções."


# 🔥 4. SALVAR LEADS NO GOOGLE SHEETS
def salvar_lead(nome, telefone, mensagem):
    data = {"nome": nome, "telefone": telefone, "mensagem": mensagem}
    response = requests.post(GOOGLE_SHEETS_API, json=data)
    print(response.json())


# 🔥 5. MENU INTERATIVO
def enviar_menu(whatsapp_numero):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": whatsapp_numero,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": "Escolha uma opção:"
            },
            "action": {
                "buttons": [{
                    "type": "reply",
                    "reply": {
                        "id": "precos",
                        "title": "📌 Ver Preços"
                    }
                }, {
                    "type": "reply",
                    "reply": {
                        "id": "horario",
                        "title": "🕒 Horário de Atendimento"
                    }
                }]
            }
        }
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.json())


# 🔥 6. ENVIO EM MASSA
contatos = ["+5511987654321", "+5511998765432"]
for numero in contatos:
    enviar_mensagem(
        numero, "Promoção especial! Desconto de 20% para novos clientes. 🚀")


# 🔥 7. INTEGRAÇÃO COM CHATGPT
def resposta_chatgpt(mensagem):
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[{
                                                "role": "user",
                                                "content": mensagem
                                            }])
    return response["choices"][0]["message"]["content"]


# 🔥 8. TESTE FINAL DO BOT
numero_teste = "SEU_NUMERO_CADASTRADO"
mensagem_teste = "Oi"
resposta = resposta_chatgpt(mensagem_teste)
enviar_mensagem(numero_teste, resposta)
