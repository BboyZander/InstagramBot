import telebot

with open('./private/token', 'r') as token:
    TOKEN = token.read()

# init bot
tbot = telebot.TeleBot(TOKEN)

# Create basic func
@tbot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    tbot.reply_to(message, "Howdy, how are you doing?")


@tbot.message_handler(func=lambda message: True)
def echo_all(message):
    tbot.reply_to(message, message.text)


tbot.polling()