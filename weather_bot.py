import datetime
import json
import requests
import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

invalid_command = "Enter the city name after command!"
invalid_input = "Oh, we don't support this city " \
                "or maybe you should check your spelling!"

city_id = 0
city_cmd = "city"
citytemp_cmd = "citytemp"
citywind_cmd = "citywind"
citytime_cmd = "citytime"


def format_input(update):
    global city_id
    user_input = update.message.text.lower()

    if user_input.replace(city_cmd, '').replace(citytemp_cmd, '').replace(citywind_cmd, '').replace(
            citytime_cmd, '') == "/ tehran":
        city_id = 112931
    elif user_input.replace(city_cmd, '').replace(citytemp_cmd, '').replace(citywind_cmd, '').replace(
            citytime_cmd, '') == "/ sydney":
        city_id = 6619279
    elif user_input.replace(city_cmd, '').replace(citytemp_cmd, '').replace(citywind_cmd, '').replace(
            citytime_cmd, '') == "/ yazd":
        city_id = 111822
    elif user_input.replace(city_cmd, '').replace(citytemp_cmd, '').replace(citywind_cmd, '').replace(
            citytime_cmd, '') == "/ shiraz":
        city_id = 115019
    elif user_input.replace(city_cmd, '').replace(citytemp_cmd, '').replace(citywind_cmd, '').replace(
            citytime_cmd, '') == "/ isfahan":
        city_id = 418862

    return user_input


def weather_response(parameter):
    response = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid=f651bfb18cc09dbaf291fb291ab7bc99&units=metric")
    weather_info = json.loads(response.text)
    return weather_info[parameter]


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr"""Hi {user.mention_markdown_v2()}\!
Use /help to get and learn all commands :\)""",
    )


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("""List of commands:
/city [name] - weather status of a city
/citytemp [city_name] - temperature of a city
/citywind [city_name] - wind status of a city
/citytime [city_name] - sunrise & sunset time of a city

/supportlist - list of all supported cities""")


def city(update: Update, context: CallbackContext) -> None:
    if format_input(update) == "/city":
        update.message.reply_text(invalid_command)
    else:
        temp_dict = weather_response('main')
        for weather in weather_response('weather'):
            update.message.reply_text(f"""
    Weather status in {weather_response('name')}
    temperature: {temp_dict['temp']} ℃
    status: {weather['main']}
    details: {weather['description']}
    """)


def city_temp(update: Update, context: CallbackContext) -> None:
    if format_input(update) == "/citytemp":
        update.message.reply_text(invalid_command)
    else:
        temp_dict = weather_response('main')
        update.message.reply_text(f"""Temperature in {weather_response('name')} is {temp_dict['temp']} ℃
    Feels like {temp_dict['feels_like']} ℃
    Maximum temperature {temp_dict['temp_min']} ℃
    Minimum temperature {temp_dict['temp_max']} ℃
    """)


def city_wind(update: Update, context: CallbackContext) -> None:
    if format_input(update) == "/citywind":
        update.message.reply_text(invalid_command)
    else:
        wind_dict = weather_response('wind')
        update.message.reply_text(f"""Wind speed in {weather_response('name')} is
    {int(wind_dict['speed'] * 3.6)} km/h
    with {wind_dict['deg']} degrees""")


def city_time(update: Update, context: CallbackContext) -> None:
    if format_input(update) == "/citytime":
        update.message.reply_text(invalid_command)
    else:
        sys_dict = weather_response('sys')
        update.message.reply_text(f"""Today in Tehran,
    Sunrise is at {datetime.datetime.fromtimestamp(sys_dict['sunrise']).strftime('%H:%M:%S')} AM
    Sunset is at {datetime.datetime.fromtimestamp(sys_dict['sunset']).strftime('%H:%M:%S')} PM
    """)


def support_list(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("""
* Tehran
* Yazd
* Shiraz
* Isfahan
* Sydney

We'll add more cities as soon as possible 🤩
""")


def main() -> None:
    updater = Updater("5026942255:AAG092kWM-BxNPOhqB1S-JX-DvG2_KKeVEQ")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler(city_cmd, city))
    dispatcher.add_handler(CommandHandler(citytemp_cmd, city_temp))
    dispatcher.add_handler(CommandHandler(citywind_cmd, city_wind))
    dispatcher.add_handler(CommandHandler(citytime_cmd, city_time))
    dispatcher.add_handler(CommandHandler("supportlist", support_list))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
