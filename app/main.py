# TODO fix sticky footer covering up text when screen size shrinks
import os, time, asyncio
from dotenv import load_dotenv
import horsereality

from quart import Quart, render_template, request, session, redirect
from aiocache import Cache


from app.scraping.utils import get_user_horses, get_username_from_id

app = Quart(__name__)
app.config['DEBUG'] = True
app.config['CACHE_TYPE'] = 'FileSystemCache'
app.config['CACHE_DIR'] = 'app/cache'
cache = Cache()


async def cached_get_user_horses(client, user_id):
    horses = await get_user_horses(client, user_id)
    session['bzp_finished_scraping'] = 'True'
    await cache.add('horse_list', horses)
    horse_list = await cache.get('horse_list')
    print(horse_list)

async def redirect_after_scraping_complete():
    while True:
        print(session['bzp_finished_scraping'])
        time.sleep(2)
        if session['bzp_finished_scraping'] == 'True':
            # print(cache.get('horse_list'))
            break

@app.route('/', methods=['POST', 'GET'])
async def index():
    global hr

    if request.method == 'GET':
        return await render_template('index.html')
    elif request.method == 'POST':
        form = await request.form      
        session['bzp_finished_scraping'] = 'False'
        id = int(form['user_id'])

        username = await get_username_from_id(hr, id)
        session['bzp_user_id'] = id
        session['bzp_username'] = username

        # set the background task
        # TODO if the username we are trying to get already exists in the cache, clear it from the cache
        app.add_background_task(cached_get_user_horses, client=hr, user_id=id)
        # app.add_background_task(redirect_after_scraping_complete)

        return redirect('/loading')

@app.route('/coming-soon')
async def coming_soon():
    return await render_template('coming_soon.html')

@app.route('/credits')
async def credits():
    return await render_template('credits.html')

@app.route('/about')
async def about():
    return await render_template('about.html')

# TODO if the horse data cookie is not set, redirect to homepage. if not, render /horse_table with that cookie data
# TODO if any of the relevant cookies aren't set, handle that
# TODO handle the user not having any horses
# TODO change the cache key to have the player id in it to avoid issues
@app.route('/horse-table')
async def horse_table():
    return await render_template('horse_table.html', horses=cache.get('horse_list'), id=session['bzp_user_id'], username=session['bzp_username'])

@app.route('/loading')
async def loading():    
    return await render_template('loading_horses.html')

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