import requests
from requests.exceptions import HTTPError
from urllib.parse import urlsplit
import os
import argparse
from dotenv import load_dotenv

def get_short_link(token, version, url, is_private):
    params_short_link = {
        'access_token':token,
        'v':version,
        'url':url,
        'private':is_private
    }
    method = 'https://api.vk.ru/method/utils.getShortLink'
    response = requests.get(method, params = params_short_link) 
    response_content = response.json()
    if 'error' in response_content:
        raise HTTPError(response_content['error']['error_msg'])
    else:
        return response_content['response']['short_url']
        

def count_clicks(token, version, key, extended, interval):
    params_short_link = {
        'access_token':token,
        'key':key,
        'interval': interval,
        'extended':extended,
        'v':version,
    }
    method = 'https://api.vk.ru/method/utils.getLinkStats'
    response = requests.get(method, params = params_short_link)
    return response.content


def check_link(token, version, key, extended, interval):
    method = 'https://api.vk.ru/method/utils.getLinkStats'
    params = {
        'access_token':token,
        'key':key,
        'interval': interval,
        'extended':extended,
        'v':version,
    }

    response = requests.get(method, params = params)
    is_short_link = 'error' not in response.text
    return is_short_link


if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser(description='Программа кторая сокращает ссылки, либо выводит данные этих ссылок')
    parser.add_argument('short_link', type=str, help='Введите либо короткую ссылку, либо длинную')
    args = parser.parse_args()
    short_link = args.short_link
    vk_token= os.getenv("VC_TOKEN")
    version = 5.199
    is_private = 0
    extended = True
    interval = 'forever'
    key = urlsplit(short_link).path[1:]
    is_short_link = check_link(vk_token, version, key, extended, interval)
    if is_short_link:
        print(count_clicks(vk_token, version, key, extended, interval))
    else:
        print(get_short_link(vk_token, version, short_link, is_private))
   