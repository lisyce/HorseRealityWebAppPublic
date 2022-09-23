from bs4 import BeautifulSoup

from horsereality.utils import get_lifenumber_from_url

from .detailed_horse import DetailedHorse

async def get_user_horses_json(client, user_id):
    horse_page_html = await get_hr_html(client, f'/user/{str(user_id)}/horses', True)
    soup = BeautifulSoup(horse_page_html, 'html.parser')

    horses = {}
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
                horses[lifenumber] = detailed_horse.to_dict('layers', 'lifenumber')
    return horses

async def get_username_from_id(client, user_id):
    profile_link =  f'/user/{str(user_id)}'
    profile_html = await get_hr_html(client, profile_link, True)
    soup = BeautifulSoup(profile_html, 'html.parser')
    
    tag = soup.find(name='a', href=f'https://v2.horsereality.com{profile_link}')
    return tag.get_text()[1:-1]

async def get_hr_html(client, url, isV2):
    data = await client.http.request(method='GET', path=url, v2=isV2, headers={'User-Agent': 'Barley\'HorseRealityTools/1.0 (Language=Python/3.10.7)'})
    return data['data']