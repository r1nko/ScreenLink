import configparser
import screenshot

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

config = configparser.ConfigParser()
config.read('config.ini')
TOKEN = config.get('Telegram', 'TOKEN')

scr = screenshot.WebScreenshot()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

inline_btn_1 = InlineKeyboardButton('Да', callback_data='off')
inline_btn_2 = InlineKeyboardButton('Нет', callback_data='yes')
inline_kb = InlineKeyboardMarkup(row_width=2)
inline_kb.add(inline_btn_1, inline_btn_2)


@dp.message_handler(commands=['start'])
async def welcome_message(message: types.Message):
    await message.reply('Привет! Отправь мне ссылку и получи в ответ скриншот необходимого сайта')


@dp.callback_query_handler(lambda c: c.data)
async def make_screenshot(callback_query: types.CallbackQuery):
    try:
        scr.get_screenshot(scr.link, callback_query.data, callback_query.from_user.id)
        path = InputFile('screenshots/' + str(callback_query.from_user.id) + '.png')
        await bot.send_photo(callback_query.from_user.id, photo=path)
    except Exception:
        await bot.send_message(callback_query.from_user.id, 'Ссылка не действительна!')
    await bot.answer_callback_query(callback_query.id)


@dp.message_handler()
async def ask_static(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'Убрать со скриншота статические элементы?', reply_markup=inline_kb)
    scr.link = msg.text


if __name__ == '__main__':
    executor.start_polling(dp)
