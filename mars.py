import json
import requests
import requests_cache
import schedule

from mars_api import NASA_API_KEY as nasa_key
from mars_api import BOT_TOKEN as bot_token
from mars_api import bot_chatID

# from mars_api import TELEGRAM_API_KEY as telegram_key

requests_cache.install_cache('mars_cache')


class MarsDataLoader:

    def __init__(self,nasa_key):
        
        self.nasa_key = nasa_key
        data_from_nasa_api = requests.get(f'https://api.nasa.gov/insight_weather/?api_key={nasa_key}&feedtype=json&ver=1.0')
        content = data_from_nasa_api.json()
        self.content = content 

class DayAtMars(MarsDataLoader):

    def __init__(self, content):
        self.today = content['sol_keys'][0]
        self.temperature_on_mars = content[self.today]['AT']['av']
        self.speed_of_wind_on_mars = content[self.today]['HWS']['av']
        self.pressure_on_mars = content[self.today]['PRE']['av']

    def create_weather_on_mars_information(self,):
        massage =f'''Goood morning! Today is going to be sunny day on Elysium Platinia. There will be no clouds. 
        Temperature outside: {self.temperature_on_mars}, light wind with {self.speed_of_wind_on_mars} m/s. Air pressure is {self.pressure_on_mars} Pa. 
        Unfortunately there is still no chance to survive outside on Mars. So brace yourself 
        and prepare for another beautifull day on Earth. In case you ARE on Mars... so sunny 
        weather but still you are in a deep shit if you are outside without a spacesuit on.'''
        return massage

k = 'harrrrry'

def telegram_send_text_massage(massage, bot_token, bot_chatID):
    
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + massage

    response = requests.get(send_text)

    return response.json()

if __name__ == '__main__':
    data_from_nasa_api = MarsDataLoader(nasa_key)
    day_at_mars = DayAtMars(data_from_nasa_api.content)
    current_condition_on_mars = day_at_mars.create_weather_on_mars_information()
    print(type(current_condition_on_mars))
    print(type(k))
    telegram_send_text_massage(k,bot_token,bot_chatID)
    telegram_send_text_massage(current_condition_on_mars,bot_token,bot_chatID)
   



