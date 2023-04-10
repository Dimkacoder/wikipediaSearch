import requests.exceptions
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import wikipediaapi
from os import getenv

TOKEN = getenv('TOKEN')  # введите токен своего бота здесь
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)
wiki_wiki = wikipediaapi.Wikipedia('ru')


# обработчик команды "/start"
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id,
                           "Привет!👋\nНапиши мне любой запрос, и я найду для тебя ответ в Википедии!🔍")


# обработчик любого сообщения
@dp.message_handler()
async def echo_message(message: types.Message):
    query = message.text
    try:
        # получаем страницу по запросу
        page_py = wiki_wiki.page(query)
        if page_py.exists():
            await bot.send_message(message.from_user.id,
                                   f'<b>{page_py.title.upper()}</b>\n\n{page_py.summary[0:60]}...\n\n{page_py.fullurl}')
        else:
            await bot.send_message(message.from_user.id, 'Такой страницы не найдено 😔')
    except requests.exceptions.ConnectTimeout:
        await bot.send_message(message.from_user.id, 'Сервер Википедии перегружен⚠️\n Пожалуйста, попробуйте еще раз '
                                                     'позже 🕐')


if __name__ == '__main__':
    executor.start_polling(dp)
