
import logging
import random

from aiogram import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import BoundFilter, Text
import os

import config
from config import *

from aiogram.types import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3


bot = Bot(token=token,disable_web_page_preview=True,parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
db = "DataBase.db"

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")
logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A WARNING")
logging.error("An ERROR")
logging.critical("A message of CRITICAL severity")

@dp.message_handler(commands='start')
async def start(message: types.Message):
    try:
        with sqlite3.connect(db) as cursor:
            cursor.execute("INSERT INTO user (user_id) VALUES (?)", (message.from_user.id,)).fetchall()
        markup = InlineKeyboardMarkup(row_width=1)
        reg = InlineKeyboardButton(text="Пройти регестрацию", callback_data="reg")
        instr = InlineKeyboardButton(text="Инструкция", callback_data='instr')
        sign = InlineKeyboardButton(text="Выдать сигнал",callback_data="sign")
        markup.add(reg,instr,sign)
        await bot.send_message(message.from_user.id,"Добро пожаловать в MINES OpenA!\n3 Mines - это гэмблинг игра в букмекерской конторе 1win, которая основывается на классическом “Сапёре”. Ваша цель - открывать безопасные ячейки и не попадаться в ловушки.\n7 Наш бот основан на нейросети от OpenA. Он может предугадать расположение звёзд с вероятностью 85%.",reply_markup=markup)
    except:
        markup = InlineKeyboardMarkup(row_width=1)
        reg = InlineKeyboardButton(text="Пройти регестрацию", callback_data="reg")
        instr = InlineKeyboardButton(text="Инструкция", callback_data='instr')
        sign = InlineKeyboardButton(text="Выдать сигнал", callback_data="sign")
        markup.add(reg, instr, sign)
        await bot.send_message(message.from_user.id, "Добро пожаловать в MINES OpenA!\n3 Mines - это гэмблинг игра в букмекерской конторе 1win, которая основывается на классическом “Сапёре”. Ваша цель - открывать безопасные ячейки и не попадаться в ловушки.\n7 Наш бот основан на нейросети от OpenA. Он может предугадать расположение звёзд с вероятностью 85%.", reply_markup=markup)


@dp.callback_query_handler(text='instr')
async def instr(callback: types.CallbackQuery):
    photo = InputFile('instr.png')
    await bot.send_photo(callback.from_user.id,photo=photo,caption=f'1. Пройти регистрацию на БК https://1wymi.pro/casino/list?open=register&sub1={callback.from_user.id}#jwoe\n2. Пополнить баланс\n3. Перейти в игру "Mines"\n4. Выбрать кол-во ловушек 3\n5. Ставить по сигналам из бота\n6. При проигрыше удвоить ставку')

@dp.callback_query_handler(text='sign')
async def sign(callback: types.CallbackQuery):
    with sqlite3.connect(db) as cursor:
        user = cursor.execute("SELECT * FROM user WHERE user_id = ?", (callback.from_user.id,)).fetchall()
    if user[0][1] != None:
        directory = 'sign'
        files = os.listdir(directory)
        print(len(files))
        text = f"sign/{random.randint(1, len(files))}.png"
        photo = InputFile(text)
        markup = InlineKeyboardMarkup(row_width=1)
        instr = InlineKeyboardButton(text="Инструкция", callback_data='instr')
        sign = InlineKeyboardButton(text="Выдать сигнал", callback_data="sign")

        markup.add(sign, instr)
        await bot.send_photo(callback.from_user.id,photo=photo,reply_markup=markup)
    else:
        markup = InlineKeyboardMarkup(row_width=1)
        url = InlineKeyboardButton(text="Зарегистрироваться", url=f'https://1wymi.pro/casino/list?open=register&sub1={callback.from_user.id}#jwoe')
        markup.add(url)
        await bot.send_message(callback.from_user.id, "Сначало пройдите регестрацию👇", reply_markup=markup)


@dp.callback_query_handler(text='reg')
async def reg(callback: types.CallbackQuery):
    markup = InlineKeyboardMarkup(row_width=1)
    url = InlineKeyboardButton(text="Зарегистрироваться", url=f'https://1wymi.pro/casino/list?open=register&sub1={callback.from_user.id}#jwoe')
    markup.add(url)
    await bot.send_message(callback.from_user.id, "Пройдите регестрацию👇", reply_markup=markup)

@dp.message_handler(commands='admin')
async def admin(message: types.Message):
    if str(message.from_user.id) == config.admin_id:
        markup = InlineKeyboardMarkup(row_width=1)
        add_photo = InlineKeyboardButton(text="Добавить сигнал",callback_data='add_photo')
        markup.add(add_photo)
        await bot.send_message(message.from_user.id,"Админ панель",reply_markup=markup)
    else:
        await bot.send_message(message.from_user.id, "Вы не админ")

class add_photo_st(StatesGroup):
    add_ph = State()

@dp.callback_query_handler(text='add_photo')
async def add_photo(callack: types.CallbackQuery):

    await bot.send_message(callack.from_user.id,f"Отправьте фото которое хотите добавить")
    await add_photo_st.add_ph.set()

@dp.message_handler(state=add_photo_st.add_ph,content_types=['photo'])
async def add_ph(message: types.Message, state: FSMContext):
    directory = 'sign'
    files = os.listdir(directory)
    await message.photo[-1].download(destination_file=f"sign/{len(files) + 1}.png")
    await bot.send_message(message.from_user.id,"Сигнал добавлен")
    await state.finish()


if __name__ == '__main__':
    print("Бот запущен")
    executor.start_polling(dp, skip_updates=True)