# Mars Weather Information

Program connecting to NASA API for daily information from Insigt Mars Lander about weather on Mars. It gets maximum, minimum and avarage temperature than converted to Celsius scale, wind speed, and pressure in Pa (Pressure on Mars is comparable with pressure on 35km above Earth surface). Insight Mars Lander is located on Elysium Planitia. It's a place on Mars very close to the equator of Mars. Additionally application is sending daily information at 8:00 to chat on Telegram.

## Install Application

1. Clone repository
2. Install requirements.txt pip install -r requirements.txt
3. To be able to start application user has to have own NASA api key, bot token and bot chat ID saved in a file named mars_api.py with a content:

```python
NASA_API_KEY = 'your nasa api key'
BOT_TOKEN = 'your bot token'
bot_chatID = 'your bot chat ID'
```

4. How can be chat in Telegram create? For further information user should go and read documentation to <https://core.telegram.org/bots>
