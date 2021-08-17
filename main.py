import random
import re
import vk_api
from vk_api import audio
import requests
from telegram.ext import Updater, MessageHandler, Filters
import json
from settings import *


def SaveChannels():
    json_text = json.dumps(channels)
    f = open(channels_file_name, "w")
    f.write(json_text)
    f.close()


def captcha_handler(captcha):
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)


def two_factor():
    code = input('Two factor code:')
    return code


print("Auth...", end=' ')
vk_session = vk_api.VkApi(login=vk_login,
                          password=vk_password,
                          auth_handler=two_factor,
                          captcha_handler=captcha_handler)
vk_session.auth()
vk = vk_session.get_api()
vk_audio = audio.VkAudio(vk_session)
print("Ok")

print("Files...", end=' ')

channels_file = open(channels_file_name, "r", encoding='utf-8')
channels = json.load(channels_file)
channels_file.close()

file = open(audio_list_path, "r", encoding='utf-8')
audios = []
for line in file.readlines():
    audios.append(line.strip())
file.close()
file = open(audio_list_path, "a", encoding='utf-8')
print("Ok")

access_key = 0


def GenerateNewAccessKey():
    global access_key
    access_key = random.randint(0, 100000000)
    print('New access key is', access_key)


def TelegramUpdate(update, context):
    chat_id = update.message.chat.id
    text = str(update.message.text)
    chat_id_str = str(chat_id)

    if text.startswith('/add_vk_playlist') and len(text.split(' ')) == 3 and text.count(str(access_key)) == 1:
        GenerateNewAccessKey()
        regex = re.search(r'audio_playlist(\d+_\d+)', text)
        if len(regex.groups()) != 1:
            bot.send_message(chat_id, 'Invalid playlist address')
        else:
            playlist = regex.groups()[0]
            if chat_id_str not in channels:
                channels[chat_id_str] = []
            channels[chat_id_str].append(playlist)
            SaveChannels()
            bot.send_message(chat_id, "Ok")
            print('Added playlist', playlist, 'to chat', chat_id_str)

    if text.startswith('/update_vk_playlist'):
        if chat_id_str not in channels:
            bot.send_message(chat_id, 'Add Playlist First')
        else:
            for playlist in channels[chat_id_str]:
                Update(chat_id, playlist.split('_'))


def Update(chat_id, playlist):
    print('Updating', playlist, chat_id)
    print("Getting playlist...", end=' ')
    vk_audios = vk_audio.get(owner_id=playlist[0], album_id=playlist[1])
    print("Ok")
    print('Playlist length: ', len(vk_audios))

    print("Updating...")
    processed = 0
    for audio in vk_audios:
        name = audio["artist"] + ' - ' + audio["title"] + '.mp3'
        unique_name = str(chat_id) + '_' + name
        print('[' + f"{100. * processed / len(vk_audios):.1f}" + '%] ' + name + '...', end=' ')
        if audios.count(unique_name) == 0:
            print('Sending...', end=' ')
            r = requests.get(audio["url"])
            if r.status_code != 200:
                print('ERROR', r.status_code)
                continue
            if len(audio["track_covers"]) > 0:
                cover = requests.get(audio["track_covers"][-1]).content
            else:
                cover = None
            bot.send_audio(chat_id,
                           audio=r.content,
                           filename=name,
                           title=audio["title"],
                           performer=audio["artist"],
                           duration=audio["duration"],
                           thumb=cover,
                           timeout=1000)
            file.write(unique_name + '\n')
            audios.append(unique_name)
            file.flush()
            print('Ok')
        else:
            print('Skipping')
        processed = processed + 1
    print("Updating done")


GenerateNewAccessKey()

updater = Updater(telegram_token, use_context=True)
dp = updater.dispatcher
bot = updater.bot
dp.add_handler(MessageHandler(Filters.text & Filters.update.message, TelegramUpdate))
updater.start_polling()
print('Ready')
