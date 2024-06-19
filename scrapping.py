import requests
from bs4 import BeautifulSoup
import random

url_anekdots = 'https://www.anekdot.ru/'
url_quotes = 'https://asana.com/ru/resources/team-motivational-quotes'

def get_random_quote():
    response = requests.get(url_quotes)

    b = BeautifulSoup(response.text, 'html.parser')
    a = b.find_all('h3')
    div = random.choice(a)

    return div.text

def get_random_anekdot():
    response = requests.get(url_anekdots)
    b = BeautifulSoup(response.text, 'html.parser')
    a = b.find_all('div', class_='text')

    div = random.choice(a)

    a_a = div.find_all('a', class_='next')
    if a_a:
        new_url = url_anekdots  + a_a.get('href')
        response = requests.get(new_url)
        b = BeautifulSoup(response.text, 'html.parser')
        a = b.find_all('div', class_='text')
        div = random.choice(a)

    a_br = div.find_all('br')
    for br in a_br:
        br.replace_with('\n')

    return div.text

def get_random_meme():
    response = requests.get(url_anekdots)
    b = BeautifulSoup(response.text, 'html.parser')
    a = b.find_all('img', class_='data')

    img = random.choice(a)
    
    return img.get('src')
