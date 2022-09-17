import os
from dotenv import load_dotenv
import horsereality
from quart import Quart, render_template, request

import scraping

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

        horses = await scraping.get_user_horses(hr, id)
        return await render_template('horse_table.html', horses=horses, id=id)

@app.before_serving
async def startup():
    load_dotenv()

    global hr 
    hr = horsereality.Client(remember_cookie_name=os.environ['HR_REMEMBER_COOKIE_NAME'], 
    remember_cookie_value=os.environ['HR_REMEMBER_COOKIE_VALUE'], auto_rollover=True)

    await hr.verify()

if __name__ == "__main__":
    app.run()