import re
import os
import shutil
import sys
import tempfile
import subprocess
import requests
import threading

regex = "https.*key.pub"
regex_2 = '"https.*pub?.*"'
regex_3 = 'ts?.*'


def parse_m3u8(url):
    urldir = os.path.dirname(url)
    playlist = requests.get(url).text
    keyurl = re.findall(regex, playlist)[0]
    key = requests.get(keyurl).text

    for match in re.finditer(regex_2, playlist, re.MULTILINE):
        playlist = playlist.replace(match.group(), 'key.pub')

    for match in re.finditer(regex_3, playlist):
        playlist = playlist.replace(match.group(), 'ts')

    return playlist, key, urldir


def download_file(urldir, file_name):
    with open(file_name, 'wb') as audio:
        audio.write(requests.get(os.path.join(urldir, file_name)).content)


def clear_folder(folder_name):
    for filename in os.listdir(folder_name):
        file_path = os.path.join(folder_name, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def download_m3u8(playlist, key, urldir):
    ts_list = [x for x in playlist.split('\n') if not x.startswith('#')]

    dir_ = 'temp/'
    if os.path.exists(dir_):
        clear_folder(dir_)
    else:
        os.makedirs(dir_)
    os.chdir(dir_)
    threads = []
    for file in ts_list[:-1]:
        threads.append(threading.Thread(target=download_file, args=(urldir, file)))
        threads[-1].start()
    for thread in threads:
        thread.join()
    with open('key.pub', 'w') as keyfile:
        keyfile.write(key)
    with open('index.m3u8', 'w') as playlist_file:
        playlist_file.write(playlist)

    p = subprocess.call(['ffmpeg', '-allowed_extensions', "ALL", '-protocol_whitelist',
                     "crypto,file", '-i', 'index.m3u8', '-c', 'copy', 'temp.mp3'],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return open('temp.mp3', 'rb').read()


def get_m3u8(url):
    result = parse_m3u8(url)
    return download_m3u8(*result)
