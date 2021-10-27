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
        print(*args, end=end)
        for s in args:
            self.cache += str(s) + ' '
        self.cache += end

    def update(self):
        if time.time() - self.last_updated >= self.update_period:
            if len(self.cache) == 0:
                return
            self.bot.send_message(self.chat_id, self.cache[:4000])
            self.cache = self.cache[4000:]
            self.last_updated = time.time()
