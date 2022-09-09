from bs4 import BeautifulSoup
from horsereality.utils import get_lifenumber_from_url
from horsereality.models import Horse

async def get_hr_html(client, url, isV2):
    data = await client.http.request(method='GET', path=url, v2=isV2, headers={'User-Agent': 'Barley\'HorseRealityTools/1.0 (Language=Python/3.10.0)'})
    return data['data']

# using this idea from the RealTools api (https://github.com/hr-tools/api/blob/main/api/v1/auth.py)
async def relogin(hr_client):
    try:
        return hr_client.http.cookies['horsereality']
    except KeyError:
        await hr_client.login()
        return hr_client.http.cookies['horsereality']