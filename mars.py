import json
import requests
import requests_cache
import schedule

from mars_api import NASA_API_KEY as nasa_key
from mars_api import TELEGRAM_API_KEY as telegram_key

requests_cache.install_cache('mars_cache')


class MarsDataLoader():

    def __init__(self,nasa_key):
        
        self.nasa_key = nasa_key
    
    def load_mars_data(self):
        # methods to download data from Nasa Insight
        data = requests.get(f'https://api.nasa.gov/insight_weather/?api_key={nasa_key}&feedtype=json&ver=1.0')
        content = data.text
        content = json.loads(content)
        return content
    
    def get_today(self, mars_data):
        today = mars_data['sol_keys'][0]
        return today

class DayAtMars():

    def __init__(self, today):
        self.today = today

    def get_temp_on_mars(self, data_from_mars, today):
        mars_temp = data_from_mars[self.today]['AT']['av']
        return mars_temp
    
    def get_speed_of_wind_on_mars(self, data_from_mars, today):
        mars_wind_speed = data_from_mars[self.today]['HWS']['av']
        return mars_wind_speed

    def get_pressure_on_mars(self, data_from_mars, today):
        press_on_mars = data_from_mars[self.today]['PRE']['av']
        return press_on_mars

    def get_weather_info(self):
        pass

def job():

    loader = MarsDataLoader(nasa_key)
    mars_data = loader.load_mars_data()
    today = loader.get_today(mars_data)
    day_at_mars = DayAtMars(today)
    current_temp_mars = day_at_mars.get_temp_on_mars(mars_data,day_at_mars)
    current_mars_wind_speed = day_at_mars.get_speed_of_wind_on_mars(mars_data,day_at_mars)
    current_pressure_on_mars = day_at_mars.get_pressure_on_mars(mars_data,day_at_mars)
    print(current_temp_mars)
    print(current_mars_wind_speed)
    print(current_pressure_on_mars)

def main(job):
    schedule.every().day.at("8:30").do(job)

'''
def telegram_send_text_massage(massage):
    bot_token = telegram_key.get(996660680)
    bot_chatID = ''
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + massage

    response = requests.get(send_text)

    return response.json()
'''