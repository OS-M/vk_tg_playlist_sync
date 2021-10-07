from bot.bot import Bot
import telebot
from settings import telegram_token

bot = telebot.TeleBot(telegram_token)
vk_bot = Bot(bot)


@bot.message_handler(func=lambda m: True)
def telegram_update(message):
    chat_id = message.chat.id
    text = str(message.text).strip()

    if text.startswith('/add_vk_playlist'):
        vk_bot.add_playlist(str(chat_id), text)

    if text.startswith('/update_vk_playlist'):
        vk_bot.update_playlist(str(chat_id))


if __name__ == '__main__':
    bot.infinity_polling()
