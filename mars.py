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
    
    def load_mars_data_from_api(self):
        # methods to download data from Nasa Insight
        data = requests.get(f'https://api.nasa.gov/insight_weather/?api_key={nasa_key}&feedtype=json&ver=1.0')
        content = data.text
        content = json.loads(content)
        return content

class DayAtMars:

    def __init__(self, data_from_mars):
        self.data_from_mars = data_from_mars

    
    def get_today(self,data_from_mars):
        today = data_from_mars['sol_keys'][0]
        return today
    
   
    def get_temp_on_mars(self,data_from_mars):
        mars_temp = data_from_mars[self.get_today(data_from_mars)]['AT']['av']
        return mars_temp
    

    def get_speed_of_wind_on_mars(self, data_from_mars):
        mars_wind_speed = data_from_mars[self.get_today(data_from_mars)]['HWS']['av']
        return mars_wind_speed
    

    def get_pressure_on_mars(self, data_from_mars):
        press_on_mars = data_from_mars[self.get_today(data_from_mars)]['PRE']['av']
        return press_on_mars

    def set_weather_info(self,mars_temp,mars_wind_speed,press_on_mars):
        massage =f'''Goood morning! Today is going to be sunny day on Elysium Platinia. There will be no clouds. 
        Temperature outside: {mars_temp}, light wind with {mars_wind_speed} m/s. Air pressure is {press_on_mars} Pa. 
        Unfortunately there is still no chance to survive outside on Mars. So brace yourself 
        and prepare for another beautifull day on Earth. In case you ARE on Mars... so sunny 
        weather but still you are in a deep shit if you are outside without a spacesuit on.'''
        return massage

class CreateMessage(MarsDataLoader,DayAtMars):
    
    def __init__(self):
        pass
    
    
    def create_message(self):
        loader = MarsDataLoader(nasa_key)
        mars_data = loader.load_mars_data_from_api()
        day_at_mars = DayAtMars(mars_data)
        #today = day_at_mars.get_today
        temp_at_mars = day_at_mars.get_temp_on_mars(mars_data)
        pressure_at_mars = day_at_mars.get_pressure_on_mars(mars_data)
        wind_speed_at_mars = day_at_mars.get_speed_of_wind_on_mars(mars_data)
        message_with_weathercast_from_mars = day_at_mars.set_weather_info(temp_at_mars,wind_speed_at_mars,pressure_at_mars)
        return message_with_weathercast_from_mars




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