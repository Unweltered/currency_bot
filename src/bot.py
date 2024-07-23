# Импортируем необходимые библиотеки и модули
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import BOT_TOKEN
from currency_service import get_currency_rates, convert_currency
from redis_service import set_all_currency_rates, get_all_currency_rates

# Создаем объект бота с использованием токена из конфигурации
bot = Bot(token=BOT_TOKEN)
# Создаем диспетчер для обработки сообщений
dp = Dispatcher(bot)

async def update_currency_rates():
    """
    Асинхронная функция для периодического обновления курсов валют.
    Запускается в бесконечном цикле и обновляет курсы каждые 24 часа.
    """
    while True:
        # Получаем актуальные курсы валют
        rates = await get_currency_rates()
        # Сохраняем полученные курсы в Redis
        set_all_currency_rates(rates)
        # Ждем 24 часа перед следующим обновлением
        await asyncio.sleep(86400)  # 86400 секунд = 24 часа

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    Обработчик команд /start и /help.
    Отправляет приветственное сообщение с инструкциями.
    """
    await message.reply("Привет! Я бот для конвертации валют. Используйте /exchange для конвертации или /rates для получения актуальных курсов.")

@dp.message_handler(commands=['exchange'])
async def exchange_command(message: types.Message):
    """
    Обработчик команды /exchange.
    Конвертирует указанную сумму из одной валюты в другую.
    """
    try:
        # Разбиваем сообщение на части: команда, исходная валюта, целевая валюта, сумма
        _, from_currency, to_currency, amount = message.text.split()
        # Преобразуем сумму в число с плавающей точкой
        amount = float(amount)
        # Получаем актуальные курсы валют из Redis
        rates = get_all_currency_rates()
        # Выполняем конвертацию
        result = await convert_currency(amount, from_currency.upper(), to_currency.upper(), rates)
        # Отправляем результат пользователю
        await message.reply(f"{amount} {from_currency.upper()} = {result:.2f} {to_currency.upper()}")
    except ValueError:
        # Если возникла ошибка при разборе сообщения, отправляем инструкцию по использованию
        await message.reply("Неправильный формат. Используйте: /exchange USD RUB 10")

@dp.message_handler(commands=['rates'])
async def rates_command(message: types.Message):
    """
    Обработчик команды /rates.
    Отправляет пользователю список актуальных курсов валют.
    """
    # Получаем актуальные курсы валют из Redis
    rates = get_all_currency_rates()
    # Формируем ответное сообщение
    response = "Актуальные курсы валют:\n\n"
    for currency, rate in rates.items():
        response += f"{currency}: {rate:.4f} RUB\n"
    # Отправляем сформированное сообщение пользователю
    await message.reply(response)

if __name__ == '__main__':
    # Получаем текущий цикл событий
    loop = asyncio.get_event_loop()
    # Создаем задачу для периодического обновления курсов валют
    loop.create_task(update_currency_rates())
    # Запускаем бота
    executor.start_polling(dp, skip_updates=True)