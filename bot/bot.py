import settings
import vk_api_utils.vk_api_utils as vk_api
import utils.utils as utils
import re
import logger.logger as logger


class Bot:
    def __init__(self, telegram_bot, logger: logger.Logger):
        self.sent_audios_file = open(settings.audio_list_path, "a", encoding='utf-8')
        self.logger = logger
        self.sent_audios = utils.get_sent_audios()
        self.vk_audio = vk_api.get_vk_audio_api()
        self.channels = utils.load_channels_from_json()

        self.bot = telegram_bot
        self.logger.log('Ready')

    def send_message(self, chat_id, message):
        self.bot.send_message(chat_id, message)
        return True

    def send_audio(self, chat_id,
                   audio,
                   title,
                   performer,
                   duration,
                   thumb,
                   timeout):
        self.bot.send_audio(chat_id,
                            audio=audio,
                            title=title,
                            performer=performer,
                            duration=duration,
                            thumb=thumb,
                            timeout=timeout)
        return True

    def add_playlist(self, chat_id: str, text: str):
        regex = re.search(r'audio_playlist(-?\d+_\d+)', text)
        if regex is None or len(regex.groups()) != 1:
            self.send_message(chat_id, 'Invalid playlist address')
        else:
            playlist = regex.groups()[0]
            if chat_id not in self.channels:
                self.channels[chat_id] = []
            self.channels[chat_id].append(playlist)
            utils.save_channels(self.channels)
            self.send_message(chat_id, "Added")
            self.logger.log('Added playlist', playlist, 'to chat', chat_id)

    def add_sent_audio(self, unique_name: str):
        self.sent_audios_file.write(unique_name + '\n')
        self.sent_audios_file.flush()
        self.sent_audios.append(unique_name)

    def update_chat_playlist(self, chat_id, audios):
        self.logger.log("Updating...")
        processed = 0
        for audio in audios:
            name = f'{audio["artist"]} - {audio["title"]}.mp3'
            unique_name = str(chat_id) + '_' + name
            processed += 1
            self.logger.log(f'[{100. * processed / len(audios):.1f}%] {name}...', end=' ')

            if self.sent_audios.count(unique_name) != 0:
                self.logger.log('Skipping')
                continue

            self.logger.log('Sending...', end=' ')
            cover = None
            if len(audio["track_covers"]) > 0:
                cover = utils.get_content(audio["track_covers"][-1])
            content = utils.get_content(audio['url'])
            if content is None:
                self.logger.log('Error getting content')
            else:
                if self.send_audio(chat_id,
                                   audio=content,
                                   title=audio["title"],
                                   performer=audio["artist"],
                                   duration=audio["duration"],
                                   thumb=cover,
                                   timeout=1000):
                    self.add_sent_audio(unique_name)
                    self.logger.log('Ok')
        self.logger.log("Updating done")

    def update_playlist(self, chat_id: str):
        if chat_id not in self.channels:
            self.send_message(chat_id, 'Add Playlist First')
        else:
            for playlist in self.channels[chat_id]:
                self.logger.log('Updating', playlist, chat_id)
                self.logger.log("Getting playlist...", end=' ')
                vk_audios = self.vk_audio.get(owner_id=playlist.split('_')[0], album_id=playlist.split('_')[1])
                self.logger.log("Ok")
                self.logger.log('Playlist length: ', len(vk_audios))
                self.update_chat_playlist(chat_id, vk_audios)
