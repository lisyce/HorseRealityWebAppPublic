# TODO fix sticky footer covering up text when screen size shrinks (mobile)
# TODO theory: go through building DetailedHorses by horse tab to reduce time. if you keep visiting horse pages in browser, it defaults to the most recent tab. this could save requests
# TODO comment the code so it looks nice
# TODO show progress bar when loading

import os, json, asyncio
from dotenv import load_dotenv
import horsereality

from quart import Quart, render_template, request, redirect, make_response, url_for
from aiocache import Cache

from app.scraping.utils import get_user_horses_json, get_username_from_id
from app.server_sent_event import ServerSentEvent

app = Quart(__name__)
app.config['DEBUG'] = True
app.config['CACHE_TYPE'] = 'FileSystemCache'
app.config['CACHE_DIR'] = 'app/cache'
cache = Cache()

# TODO actually use the cache if the data already exists to save time (needs a hard refresh button during session)
async def cache_user_horses(client, id_):
    horses = await get_user_horses_json(client, id_)
    await cache.set(f'horse_list_{str(id_)}', horses)

@app.route('/', methods=['GET', 'POST'])
async def index():
    if request.method == 'GET':
        return await render_template('index.html', error="no error")
    elif request.method == 'POST':
        form = await request.form
        id = form['user_id']
        return redirect(url_for('horse_table_display', id_=id))
    

@app.get('/coming-soon')
async def coming_soon():
    return await render_template('coming_soon.html')

@app.get('/credits')
async def credits():
    return await render_template('credits.html')

@app.get('/about')
async def about():
    return await render_template('about.html')

@app.get('/horse-table/<int:id_>')
async def horse_table_display(id_):
    global hr
    try:
        username = await get_username_from_id(hr, id_)
    except:
        return await render_template('index.html', error="Invalid player ID. Please try again.")
    return await render_template('horse_table.html', user_id=id_, username=username)

# polling link
@app.get('/api/horse-table/<int:id_>')
async def horse_table_api(id_):

    horse_data_exists = await cache.exists(f'horse_list_{str(id_)}')
    if not horse_data_exists:
        # the data doesn't exist in the cache.
        await cache.add(f'horse_list_{str(id_)}', None)

        global hr
        loop = asyncio.get_running_loop();
        loop.create_task(cache_user_horses(hr, id_))
        return "", 202

    # see if the data is None or not
    cache_data = await cache.get(f'horse_list_{str(id_)}')
    if cache_data is None:
        return "", 202
    else:
        # the scraping has finished
        await cache.delete(f'horse_list_{str(id_)}')
        return json.dumps(cache_data)


@app.before_serving
async def startup():
    load_dotenv()
    app.secret_key = os.environ['QUART_SECRET_KEY']

    global hr 
    hr = horsereality.Client(remember_cookie_name=os.environ['HR_REMEMBER_COOKIE_NAME'], 
    remember_cookie_value=os.environ['HR_REMEMBER_COOKIE_VALUE'], auto_rollover=True)

    await hr.verify()

if __name__ == "__main__":
    app.run()