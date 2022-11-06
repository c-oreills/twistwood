from bs4 import BeautifulSoup
import re
import requests

BASE_URL = 'https://m.webtoons.com/en/challenge/twistwood-tales/list?title_no=344740'
BASE_URL = 'https://www.webtoons.com/en/challenge/twistwood-tales/1-when-is-your-bedtime/viewer?title_no=344740&episode_no=1'

url = BASE_URL

main_strips = []
extra_strips = []

while url is not None:
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, features='html.parser')
    
    title = soup.find('title').get_text()
    title, _ = title.rsplit(' - ', 1)
    
    info_el = soup.find(class_='info_area').find('p')
    info = info_el.get_text() if info_el else None
    
    match = re.match(r'\d+', title)
    if match:
        _, title = title.split('-', 1)
        title = title.strip()
        main_strips.append((match[0], title, url, info))
    else:
        extra_strips.append((title, url, info))
    
    next_ep = soup.find(class_='_nextEpisode')
    if not next_ep:
        break
    url = next_ep['href']
    #print(next_ep)
    #print(url)

with open('webtoons_out.py', 'w') as f:
    f.writelines([
        f'main_strips = {repr(main_strips)}\n',
        f'extra_strips = {repr(extra_strips)}'
    ])
    