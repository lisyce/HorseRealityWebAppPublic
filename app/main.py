import json
import horsereality
from quart import Quart, render_template, request

from scraping.detailed_horse import DetailedHorse
from scraping.main import get_user_horses
from scraping.utils import relogin

app = Quart(__name__)

@app.route('/')
async def index():
    return await render_template('index.html')

@app.route('/coming-soon')
async def coming_soon():
    return await render_template('coming_soon.html')

@app.route('/credits')
async def credits():
    return await render_template('credits.html')

@app.route('/about')
async def about():
    return await render_template('about.html')

@app.route('/horse-table', methods=['POST', 'GET'])
async def user_horses():
    global hr

    if request.method == 'GET':
        return await render_template('index.html')
    elif request.method == 'POST':
        form = await request.form      
        id = int(form['user_id'])

        horses = await get_user_horses(hr, id)
        return await render_template('horse_table.html', horses=horses, id=id)

@app.before_serving
async def startup():
    config = json.load(open('config.json'))
    global hr 
    hr = horsereality.Client(remember_cookie_name=config['authentication']['remember-cookie-name'], 
    remember_cookie_value=config['authentication']['remember-cookie-value'], auto_rollover=True)
    
    email = config['authentication']['email']
    password = config['authentication']['password']

    await hr.verify()

if __name__ == "__main__":
    app.run()