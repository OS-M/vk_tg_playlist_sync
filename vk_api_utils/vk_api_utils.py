import vk_api
from vk_api import audio as vk_audio
from settings import vk_login, vk_password


def captcha_handler(captcha):
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)


def two_factor():
    code = input('Two factor code:')
    return code


def get_vk_audio_api():
    print("VK auth...", end=' ')
    vk_session = vk_api.VkApi(login=vk_login,
                              password=vk_password,
                              auth_handler=two_factor,
                              captcha_handler=captcha_handler)
    vk_session.auth()
    vk_audio_ = vk_audio.VkAudio(vk_session)
    print("Ok")
    return vk_audio_
