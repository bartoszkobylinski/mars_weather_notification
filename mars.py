import json
import requests
import schedule
import time

from mars_api import NASA_API_KEY as nasa_key
from mars_api import BOT_TOKEN as bot_token
from mars_api import bot_chatID


class MarsDataLoader:
    def __init__(self, nasa_key):

        self.nasa_key = nasa_key
        data_from_nasa_api = requests.get(
            f"https://api.nasa.gov/insight_weather/?api_key={nasa_key}&feedtype=json&ver=1.0"
        )
        content = data_from_nasa_api.json()
        self.content = content


class DayAtMars(MarsDataLoader):
    def __init__(self, content):
        self.today = content["sol_keys"][0]
        # converting temperature from fahrenheit to Celsius
        self.avarage_temperature_on_mars = round(
            (((content[self.today]["AT"]["av"]) - 32) * (5 / 9)), 1
        )
        self.min_temperature_on_mars = round(
            (((content[self.today]["AT"]["mn"]) - 32) * (5 / 9)), 1
        )
        self.max_temperature_on_mars = round(
            (((content[self.today]["AT"]["mx"]) - 32) * (5 / 9)), 1
        )
        self.speed_of_wind_on_mars = content[self.today]["HWS"]["av"]
        self.pressure_on_mars = content[self.today]["PRE"]["av"]

    def create_dict_with_condition(self):
        condition = {}
        condition["max_temp"] = self.max_temperature_on_mars
        condition["min_temp"] = self.min_temperature_on_mars
        condition["av_temp"] = self.avarage_temperature_on_mars
        condition["wind_speed"] = self.speed_of_wind_on_mars
        condition["press"] = self.pressure_on_mars
        return condition

    def create_weather_on_mars_information(self):
        massage = f"""Goood morning! Today is going to be sunny day on Elysium Planitia. There will be no clouds. Minimal temperature is going to be:
        {self.min_temperature_on_mars}C and maximum is going to be: {self.max_temperature_on_mars}C and avarage is going to be: {self.avarage_temperature_on_mars}C, 
        light wind with {self.speed_of_wind_on_mars} m/s. Air pressure is {self.pressure_on_mars} Pa. 
        Unfortunately there is still no chance to survive outside on Mars. So brace yourself 
        and prepare for another beautifull day on Earth. In case you ARE on Mars... so sunny 
        weather but still you are in big problems if you are outside without a spacesuit on."""
        return massage


def telegram_send_text_massage(massage, bot_token, bot_chatID):

    send_text = (
        "https://api.telegram.org/bot"
        + bot_token
        + "/sendMessage?chat_id="
        + bot_chatID
        + "&parse_mode=Markdown&text="
        + massage
    )

    response = requests.get(send_text)

    return response.json()


def job():

    data_from_nasa_api = MarsDataLoader(nasa_key)
    day_at_mars = DayAtMars(data_from_nasa_api.content)
    current_condition_on_mars = day_at_mars.create_weather_on_mars_information()
    telegram_send_text_massage(current_condition_on_mars, bot_token, bot_chatID)


schedule.every().day.at("20:44").do(job)

if __name__ == "__main__":

    while True:
        schedule.run_pending()
        time.sleep(1)
