import settings
from bot.bot import Bot
import telebot
from settings import telegram_token
import logger.logger as logger

bot = telebot.TeleBot(telegram_token)
logger = logger.Logger(bot, 2, settings.admin_user_id)
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


if __name__ == '__main__':
    bot.infinity_polling()
