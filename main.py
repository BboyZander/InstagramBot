import telebot
import os
from InstaBot import InstaBot


class TokenException(Exception):
    pass


try:
    TOKEN = os.environ['BOT_TOKEN']
except KeyError:
    try:
        with open('./private/token', 'r') as tok:
            TOKEN = tok.read()
    except FileNotFoundError:
        raise TokenException("Can't find token file for connection")

# init telegram bot
tbot = telebot.TeleBot(TOKEN)
# init instagram bot
ibot = InstaBot()


# Create basic func
@tbot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    tbot.reply_to(message, "Howdy, how are you doing?")


@tbot.message_handler(func=lambda message: True)
def echo_all(message):
    tbot.reply_to(message, message.text)


@tbot.message_handler(commands=['connect'])
def instabot(message):
    tbot.reply_to(message, 'Enter your login')


tbot.polling()
