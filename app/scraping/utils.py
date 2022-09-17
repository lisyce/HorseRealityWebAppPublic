from cgitb import html
from bs4 import BeautifulSoup

from horsereality.utils import get_lifenumber_from_url
from .detailed_horse import DetailedHorse

async def get_user_horses(client, user_id):
    horse_page_html = await get_hr_html(client, f'/user/{str(user_id)}/horses', True)
    soup = BeautifulSoup(horse_page_html, 'html.parser')

    horses = []
    for link in soup.find_all('a'):

        href = link.get('href')
        if('horsereality.com/horses/' in href):
            # the image by the horse is clickable too, but we want to ignore those
            # if it has a child  of a div or img, we don't want it. otherwise, we get duplicates
            children = list(link.children)
            if(len(children) == 1):
                
                lifenumber = get_lifenumber_from_url(href)
                html_text = await client.http.get_horse(lifenumber)
                detailed_horse = await DetailedHorse._from_page(client=client, http=client.http, html_text=html_text)
                horses.append(detailed_horse)
    return horses

async def get_hr_html(client, url, isV2):
    data = await client.http.request(method='GET', path=url, v2=isV2, headers={'User-Agent': 'Barley\'HorseRealityTools/1.0 (Language=Python/3.10.0)'})
    return data['data']