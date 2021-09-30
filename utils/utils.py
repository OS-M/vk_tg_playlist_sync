import json

import requests

import settings
from m3u8_handler.m3u8_handler import get_m3u8


def save_channels(channels):
    json_text = json.dumps(channels)
    f = open(settings.channels_file_name, "w")
    f.write(json_text)
    f.close()


def load_channels_from_json():
    channels_file = open(settings.channels_file_name, "r", encoding='utf-8')
    channels = json.load(channels_file)
    channels_file.close()
    return channels


def get_sent_audios():
    file = open(settings.audio_list_path, "r", encoding='utf-8')
    audios = []
    for line in file.readlines():
        audios.append(line.strip())
    file.close()
    return audios


def get_content(url: str):
    if url.count('.mp3') >= 1:
        r = requests.get(url)
        if r.status_code != 200:
            print('ERROR: status code', r.status_code, url)
            return None
        return r.content
    else:
        try:
            return get_m3u8(url)
        except:
            return None
