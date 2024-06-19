import requests
from bs4 import BeautifulSoup
import random

url = 'https://mp3uks.ru/'

def get_random_music():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    musics = soup.find_all('div', class_='track-item')
    music = random.choice(musics)

    music_title = music.find('div', class_='track-title').text
    music_subtitle = music.find('div', class_='track-subtitle').text
    music_url = 'https:' + music.find('a', class_='track-dl').get('href')

    response = requests.get(music_url)
    with open (f'{music_title}.mp3', 'wb' ) as f:
        f.write(response.content)
    
    return music_title