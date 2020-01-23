from app import app
from flask import render_template
from mars import DayAtMars, MarsDataLoader
from mars_api import NASA_API_KEY as nasa_key

@app.route('/')
@app.route('/index')
def index():
    mars = MarsDataLoader(nasa_key)
    mars_weather = DayAtMars(mars.content)
    mars_weather_condition = mars_weather.create_dict_with_condition()
    return render_template("index.html", mars=mars_weather_condition)