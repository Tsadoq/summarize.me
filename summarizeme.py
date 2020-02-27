import recapper
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from io import BytesIO
import requests
import re


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="I'm summarize.me, you send me url to an article you want to read, I send you a short "
                          "recap, a good deal isn't it? "
                          ""
                          "If you want to know how i'm made, please visit https://github.com/Tsadoq/summarize.me"
                          "To use me, send me a link to the article you want to have a recap and a number between 0 "
                          "and 1 (e.g. 0.3) to have a shorter or longer summary")


def startup(tkn):
    updater = Updater(token=tkn)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    print('starting up the bot')
    return updater, dispatcher


def summarize(bot, update):
    print('Article received')
    chat_id = update.message.chat_id
    text = update.message.text
    [url, perc] = text.split(" ")
    if re.match(r'^-?\d+(?:\.\d+)?$', perc) is None:
        txt = "The message has been sent with the wrong syntax, it should be in the form of " \
              "'www.example.com/somearticle 0.3' "
        bot.send_message(chat_id=update.message.chat_id, text=txt)
    else:
        txt = "Article received, processing, this process could take upt to 30 seconds"
        bot.send_message(chat_id=update.message.chat_id, text=txt)
        r = recapper.Recapper(url)
        r.process()
        recap = r.summarize(perc=perc)
        bot.send_message(chat_id=update.message.chat_id, text=recap)


def main():
    tkn = open('token.txt', 'r').readline()
    updater, dispatcher = startup(tkn)
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(MessageHandler(Filters.text, summarize))
    dispatcher.add_handler(start_handler)
    updater.start_polling()


if __name__ == '__main__':
    main()
