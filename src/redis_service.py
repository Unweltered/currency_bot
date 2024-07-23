# Импортируем библиотеку для работы с Redis
import redis
# Импортируем конфигурационные параметры
from config import REDIS_HOST, REDIS_PORT

# Создаем клиент Redis с указанными хостом и портом
# decode_responses=True обеспечивает автоматическое декодирование ответов из байтов в строки
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def set_currency_rate(currency_code, rate):
    """
    Устанавливает курс для заданной валюты в Redis.

    Args:
        currency_code (str): Код валюты (например, USD, EUR).
        rate (float): Курс валюты.
    """
    # Сохраняем курс валюты в Redis, используя ключ вида "currency:USD"
    redis_client.set(f"currency:{currency_code}", rate)


def get_currency_rate(currency_code):
    """
    Получает курс заданной валюты из Redis.

    Args:
        currency_code (str): Код валюты (например, USD, EUR).

    Returns:
        str: Курс валюты или None, если курс не найден.
    """
    # Получаем курс валюты из Redis по ключу вида "currency:USD"
    return redis_client.get(f"currency:{currency_code}")


def set_all_currency_rates(rates):
    """
    Устанавливает курсы для всех валют в Redis.

    Args:
        rates (dict): Словарь с кодами валют в качестве ключей и их курсами в качестве значений.
    """
    # Проходим по всем валютам в словаре
    for currency_code, rate in rates.items():
        # Устанавливаем курс для каждой валюты
        set_currency_rate(currency_code, rate)


def get_all_currency_rates():
    """
    Получает курсы всех валют из Redis.

    Returns:
        dict: Словарь с кодами валют в качестве ключей и их курсами в качестве значений.
    """
    # Получаем все ключи, начинающиеся с "currency:"
    keys = redis_client.keys("currency:*")
    rates = {}
    # Проходим по всем найденным ключам
    for key in keys:
        # Извлекаем код валюты из ключа (например, "USD" из "currency:USD")
        currency_code = key.split(':')[1]
        # Получаем курс валюты и преобразуем егgoо в число с плавающей точкой
        rates[currency_code] = float(get_currency_rate(currency_code))
    return rates