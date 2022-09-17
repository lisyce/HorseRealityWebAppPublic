from bs4 import BeautifulSoup

async def get_hr_html(client, url, isV2):
    data = await client.http.request(method='GET', path=url, v2=isV2, headers={'User-Agent': 'Barley\'HorseRealityTools/1.0 (Language=Python/3.10.0)'})
    return data['data']