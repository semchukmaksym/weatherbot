import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Твої ключі
TELEGRAM_TOKEN = '6324889917:AAEhMJbosa1yaLo6TBXc_2k-SOH0WOuABug'
OPENWEATHERMAP_API_KEY = '08a374c848fced2b5665a4a7fb20544b'

# Налаштування логування
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Функція для отримання погоди
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric&lang=uk"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        weather_desc = data['weather'][0]['description']
        city_name = data['name']
        return f"Погода в {city_name}: {temp}°C, {weather_desc.capitalize()}."
    else:
        return "Не вдалося знайти місто. Спробуйте ще раз."

# Обробник команди /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Привіт! Надішли мені назву міста, щоб дізнатися погоду.")

# Обробник повідомлень з назвою міста
def weather(update: Update, context: CallbackContext) -> None:
    city = ' '.join(context.args)
    if city:
        weather_info = get_weather(city)
        update.message.reply_text(weather_info)
    else:
        update.message.reply_text("Будь ласка, введіть назву міста після команди /weather.")

# Головна функція
def main() -> None:
    # Створюємо апдейтера та передаємо йому токен бота
    updater = Updater(TELEGRAM_TOKEN)

    # Додаємо обробники команд
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("weather", weather))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if name == '__main__':
    main()