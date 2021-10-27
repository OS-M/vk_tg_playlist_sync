import sched
import threading
import time

import settings
from bot.bot import Bot
import telebot
from settings import telegram_token
import logger.logger as logger

logger_update_scheduler = sched.scheduler(time.time, time.sleep)
bot = telebot.TeleBot(telegram_token)
logger = logger.Logger(bot, 1 / 30, settings.admin_user_id)
vk_bot = Bot(bot, logger)


@bot.message_handler(func=lambda m: True)
def telegram_update(message):
    chat_id = message.chat.id
    text = str(message.text).strip()

    if text.startswith('/add_vk_playlist'):
        vk_bot.add_playlist(str(chat_id), text)

    if text.startswith('/update_vk_playlist'):
        vk_bot.update_playlist(str(chat_id))

    if text.lower() == "ping":
        bot.send_message(chat_id, "pong")

    if text == "flush":
        logger.update()


def update_logger():
    while True:
        try:
            logger.update()
        except Exception as e:
            logger.log(e)
        time.sleep(1 / 5)


if __name__ == '__main__':
    threading.Thread(target=update_logger).start()
    while True:
        try:
            bot.infinity_polling()
        except Exception as e:
            logger.log(e)
