import json
import requests
import requests_cache
import schedule

from mars_api import NASA_API_KEY as nasa_key

# from mars_api import TELEGRAM_API_KEY as telegram_key

requests_cache.install_cache('mars_cache')


class MarsDataLoader:

    def __init__(self,nasa_key):
        
        self.nasa_key = nasa_key
        data_from_nasa_api = requests.get(f'https://api.nasa.gov/insight_weather/?api_key={nasa_key}&feedtype=json&ver=1.0')
        content = data_from_nasa_api.json()
        self.content = content 

class DayAtMars:

    def __init__(self, content):
        self.today = content['sol_keys'][0]
        self.temperature_on_mars = content[self.today]['AT']['av']
        self.speed_of_wind_on_mars = content[self.today]['HWS']['av']
        self.pressure_on_mars = content[self.today]['PRE']['av']

    def create_weather_on_mars_information(self):
        massage =f'''Goood morning! Today is going to be sunny day on Elysium Platinia. There will be no clouds. 
        Temperature outside: {self.temperature_on_mars}, light wind with {self.speed_of_wind_on_mars} m/s. Air pressure is {self.pressure_on_mars} Pa. 
        Unfortunately there is still no chance to survive outside on Mars. So brace yourself 
        and prepare for another beautifull day on Earth. In case you ARE on Mars... so sunny 
        weather but still you are in a deep shit if you are outside without a spacesuit on.'''
        return massage

class CreateMessage(MarsDataLoader,DayAtMars):
    # Consider to delete that class
    
    def __init__(self):
        pass
    
    
    def create_message(self):
        loader = MarsDataLoader(nasa_key)
        day_at_mars = DayAtMars(loader.content)
        message = day_at_mars.create_weather_on_mars_information()

        return message





if __name__ == '__main__':
    a = CreateMessage()
    a = a.create_message()
    print(a)
   

'''
def telegram_send_text_massage(massage):
    bot_token = telegram_key.get(996660680)
    bot_chatID = ''
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + massage

    response = requests.get(send_text)

    return response.json()
'''