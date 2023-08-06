import requests

TELEGRAM_TOKEN = None
TELEGRAM_CHAT_ID = None

def setToken(TOKEN):
    global TELEGRAM_TOKEN
    TELEGRAM_TOKEN = TOKEN

def setChatID(CHAT_ID):
    global TELEGRAM_CHAT_ID
    TELEGRAM_CHAT_ID = CHAT_ID

def sendMessage(message):
    global TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
    requests.post('https://api.telegram.org/bot' + TELEGRAM_TOKEN + '/sendMessage', data={'chat_id': TELEGRAM_CHAT_ID, 'text': message, 'parse_mode': "Markdown"})