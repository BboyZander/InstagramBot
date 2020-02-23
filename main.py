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
    chat_id = message.chat.id
    tbot.send_message(chat_id, 'write login pas')

    tbot.reply_to(message, message.text)



@tbot.message_handler(commands=['connect'])
def instabot(message):
    chat_id = message.chat.id
    tbot.send_message(chat_id, 'write login pas')
    data = message.text
    username = data.split(' ')[0]
    password = data.split(' ')[1]
    tbot.send_message(chat_id, f'well your username {username} and pass {password}')


tbot.polling()
