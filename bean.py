from urllib.parse import urlparse
import requests
from dotenv import load_dotenv
from requests.exceptions import HTTPError
import os


def shorten_link(token, get_url):
    params = {
        'access_token': token,
        'v': 5.199,
        "private": 0,
        "url": get_url,
    }
    url = 'https://api.vk.ru/method/utils.getShortLink'
    response = requests.get(url, params=params)
    print(response.json())
    response.raise_for_status()
    return response.json()['response']['short_url']


def count_clicks(token, parsed_key):
    url_ = "https://api.vk.ru/method/utils.getLinkStats"
    params = {
        'access_token': token,
        'v': 5.199,
        "key": parsed_key,
        "interval": "forever",
        "extended": 0
    }
    response_2 = requests.get(url_, params)
    if 'error'  in response_2.text:
        raise HTTPError
    else:
        clicks_count = response_2.json()['response']["stats"]
        return clicks_count


def is_shorten_link(token, parsed_key):
    is_short = False
    url = "https://api.vk.ru/method/utils.getLinkStats"
    params = {
        'access_token': token,
        'v': 5.199,
        "key": parsed_key,
        "interval": "forever",
        "extended": 0
    }
    response_2 = requests.get(url, params)
    if 'error' not in response_2.text:
        is_short = True
    return is_short


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("token")
    get_url = input('введите ссылку')
    parsed_url = urlparse(get_url)
    parsed_key = parsed_url.path[1:]
    is_short = is_shorten_link(token, parsed_key)
    if is_short:
        clicks_link = count_clicks(token, parsed_key)
        print(clicks_link)
    else:
        short_url = shorten_link(token, get_url)
        print(short_url)