# Импортируем необходимые библиотеки
import aiohttp
import xml.etree.ElementTree as ET
from config import CURRENCY_URL


async def get_currency_rates():
    """
    Асинхронно получает актуальные курсы валют от ЦБ РФ.

    Returns:
        dict: Словарь с кодами валют в качестве ключей и их курсами в качестве значений.
    """
    # Создаем асинхронную сессию для отправки HTTP-запроса
    async with aiohttp.ClientSession() as session:
        # Отправляем GET-запрос к URL ЦБ РФ
        async with session.get(CURRENCY_URL) as response:
            # Получаем XML-данные из ответа
            xml_data = await response.text()

    # Парсим XML-данные
    root = ET.fromstring(xml_data)
    currency_rates = {}

    # Извлекаем информацию о каждой валюте из XML
    for valute in root.findall('Valute'):
        # Получаем код валюты (например, USD, EUR)
        code = valute.find('CharCode').text
        # Получаем значение курса, заменяем запятую на точку и преобразуем в число с плавающей точкой
        value = float(valute.find('Value').text.replace(',', '.'))
        # Добавляем пару код-значение в словарь
        currency_rates[code] = value

    return currency_rates


async def convert_currency(amount, from_currency, to_currency, rates):
    """
    Конвертирует заданную сумму из одной валюты в другую.

    Args:
        amount (float): Сумма для конвертации.
        from_currency (str): Код исходной валюты.
        to_currency (str): Код целевой валюты.
        rates (dict): Словарь с курсами валют.

    Returns:
        float: Сконвертированная сумма.
    """
    if from_currency == 'RUB':
        # Если исходная валюта - рубли, делим сумму на курс целевой валюты
        return amount / rates[to_currency]
    elif to_currency == 'RUB':
        # Если целевая валюта - рубли, умножаем сумму на курс исходной валюты
        return amount * rates[from_currency]
    else:
        # В остальных случаях конвертируем через рубль:
        # сначала конвертируем в рубли, затем из рублей в целевую валюту
        return amount * rates[from_currency] / rates[to_currency]