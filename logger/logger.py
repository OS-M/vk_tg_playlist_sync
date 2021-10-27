import telebot
import time


class Logger:
    def __init__(self, bot: telebot.TeleBot, update_period, chat_id):
        self.bot = bot
        self.chat_id = chat_id
        self.update_period = update_period
        self.cache = ""
        self.last_updated = time.time()

    def log(self, *args, end='\n'):
        for s in args:
            self.cache += str(s) + ' '
        self.cache += end
        self.update()

    def update(self):
        if time.time() - self.last_updated >= self.update_period:
            if len(self.cache.strip()) == 0:
                self.cache = "**Empty**"
            self.bot.send_message(self.chat_id, self.cache)
            self.cache = ""
            self.last_updated = time.time()
