# Импортируем необходимые библиотеки
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем токен бота из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Получаем хост Redis из переменных окружения или используем значение по умолчанию
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')

# Получаем порт Redis из переменных окружения или используем значение по умолчанию
# Преобразуем строковое значение в целое число
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

# URL для получения XML файла с курсами валют от ЦБ РФ
CURRENCY_URL = 'https://www.cbr.ru/scripts/XML_daily.asp'