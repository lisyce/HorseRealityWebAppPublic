# TODO fix sticky footer covering up text when screen size shrinks
import os, json
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

# TODO actually use the cache if the data already exists to save time
async def cache_user_horses(client, user_id):
    horses = await get_user_horses_json(client, user_id)
    await cache.set(f'horse_list{str(user_id)}', horses)
    return horses

@app.route('/', methods=['GET', 'POST'])
async def index():
    if request.method == 'GET':
        return await render_template('index.html')
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
    username = await get_username_from_id(hr, id_)
    return await render_template('horse_table.html', user_id=id_, username=username)

@app.get('/api/horse-table/<int:id_>')
async def horse_table_api(id_):
    global hr
    async def send_events():
        data = await cache_user_horses(hr, id_)
        event = ServerSentEvent(json.dumps(data))
        yield event.encode()

    response = await make_response(
        send_events(),
        {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
            'Transfer-Encoding': 'chunked',
        },
    )
    response.timeout = None

    return response

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