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

invalid_command = "Please specify the city name after command."
invalid_input = "We don't support this city " \
                "or maybe you should check your spelling!"

user_input = ""
city_id = 0
default_city_id = 0


def get_input(update):
    global user_input
    user_input = update.message.text.lower()
    set_city_id()

    return user_input


def set_city_id():
    global city_id

    if "isfahan" in user_input.lower():
        city_id = 418862
    elif "shiraz" in user_input.lower():
        city_id = 115019
    elif "tehran" in user_input.lower():
        city_id = 112931
    elif "yazd" in user_input.lower():
        city_id = 111822
    elif "sari" in user_input.lower():
        city_id = 116996
    elif "mashhad" in user_input.lower():
        city_id = 124665
    elif "karaj" in user_input.lower():
        city_id = 128747
    elif "tabriz" in user_input.lower():
        city_id = 113646
    elif "rasht" in user_input.lower():
        city_id = 118743
    elif "ahvaz" in user_input.lower():
        city_id = 144448
    elif "amol" in user_input.lower():
        city_id = 143534

    return city_id


def weather_response(parameter):
    global default_city_id, city_id

    response = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?id={city_id or default_city_id}&appid"
        f"=f651bfb18cc09dbaf291fb291ab7bc99&units=metric")
    weather_info = json.loads(response.text)
    return weather_info[parameter]


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr"""Hi {user.mention_markdown_v2()}\!
Use /help to get and learn all commands :\)""",
    )


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("""IMPORTANT: In this version of bot you need to specify city name after commands. We are working hard on imporoving this bot :D
By the way, here are the commands that you can mess around :)
/city [city_name] - weather status of a city
/citytemp [city_name] - temperature of a city
/citywind [city_name] - wind status of a city
/citytime [city_name] - sunrise & sunset time of a city

/supportlist - list of all supported cities""")


def city(update: Update, context: CallbackContext) -> None:
    global city_id, default_city_id
    get_input(update)

    if city_id == 0 and default_city_id == 0:
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
        city_id = 0


def city_temp(update: Update, context: CallbackContext) -> None:
    global city_id
    get_input(update)

    if city_id == 0 and default_city_id == 0:
        update.message.reply_text(invalid_command)
    else:
        temp_dict = weather_response('main')
        update.message.reply_text(f"""Temperature in {weather_response('name')} is {temp_dict['temp']} ℃
    Feels like {temp_dict['feels_like']} ℃
    Maximum temperature {temp_dict['temp_min']} ℃
    Minimum temperature {temp_dict['temp_max']} ℃
    """)
        city_id = 0


def city_wind(update: Update, context: CallbackContext) -> None:
    global city_id
    get_input(update)

    if city_id == 0 and default_city_id == 0:
        update.message.reply_text(invalid_command)
    else:
        wind_dict = weather_response('wind')
        update.message.reply_text(f"""Wind speed in {weather_response('name')} is
    {int(wind_dict['speed'] * 3.6)} km/h
    with {wind_dict['deg']} degrees""")
        city_id = 0


def city_time(update: Update, context: CallbackContext) -> None:
    global city_id
    get_input(update)

    if city_id == 0 and default_city_id == 0:
        update.message.reply_text(invalid_command)
    else:
        sys_dict = weather_response('sys')
        update.message.reply_text(f"""Today in {weather_response('name')},
    Sunrise is at {datetime.datetime.fromtimestamp(sys_dict['sunrise']).strftime('%H:%M:%S')} AM
    Sunset is at {datetime.datetime.fromtimestamp(sys_dict['sunset']).strftime('%H:%M:%S')} PM
    """)
        city_id = 0


def city_set(update: Update, context: CallbackContext) -> None:
    global city_id
    global default_city_id
    get_input(update)

    if city_id == 0:
        update.message.reply_text(invalid_command)
    else:
        default_city_id = city_id
        update.message.reply_text(
            f"Success! Default city: {user_input.replace('/cityset ', '').title()}")


def city_reset(update: Update, context: CallbackContext) -> None:
    global city_id
    global default_city_id
    get_input(update)

    if default_city_id == 0:
        update.message.reply_text("You haven't set a city!")
    else:
        default_city_id = 0
        update.message.reply_text(
            f"Success! Your default city has been removed, you can reset it "
            f"anytime.")


def support_list(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("""
Currently we support 10 cities (in Iran):
* Ahvaz
* Amol
* Isfahan
* Karaj
* Mashhad
* Rasht
* Sari
* Shiraz
* Tabriz
* Tehran
* Yazd

We'll add more cities as soon as possible 🤩
""")


def main() -> None:
    updater = Updater("5026942255:AAG092kWM-BxNPOhqB1S-JX-DvG2_KKeVEQ")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("city", city))
    dispatcher.add_handler(CommandHandler("citytemp", city_temp))
    dispatcher.add_handler(CommandHandler("citywind", city_wind))
    dispatcher.add_handler(CommandHandler("citytime", city_time))
    dispatcher.add_handler(CommandHandler("cityset", city_set))
    dispatcher.add_handler(CommandHandler("cityreset", city_reset))
    dispatcher.add_handler(CommandHandler("supportlist", support_list))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
