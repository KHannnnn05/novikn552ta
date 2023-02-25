import os
import logging
import sqlite3
from aiogram import types
from dotenv import load_dotenv
from os.path import join, dirname
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import exceptions

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
channel_id = os.environ.get('TEST_CHANNEL_ID')
bot = Bot(os.environ.get('TOKEN'), parse_mode="HTML")
memory_storage = MemoryStorage()
dp = Dispatcher(bot, storage=memory_storage)
logging.basicConfig(level=logging.INFO)
with sqlite3.connect('/home/ubuntu/novikn552ta/novikn552ta.sqlite3') as con:
    cur = con.cursor()
    

class UserState(StatesGroup):
    id: int = State()

@dp.message_handler(commands=['get_link'])
async def getURL(message: types.Message):
    await message.answer(
        "Введите пожалуйста ID заказа/тендера.\n" + "Вводите пожалуйста только цифры, без пробелов и посторонних символов!"
    )
    await UserState.id.set()

@dp.message_handler(state=UserState.id)
async def get_id(message: types.Message, state: FSMContext):
    await state.update_data(id=message.text)

    data = await state.get_data()
    uid = data['id']
    if uid.isdigit():
        if cur.execute(f"SELECT url FROM links WHERE (id == {uid});").fetchone() is not None:
            link =  cur.execute(f"SELECT url FROM links WHERE (id == {uid});").fetchone()[0]
            await message.answer(
                f"Ловите сслыку на заказ с ID -> {uid}\n{link}"
            )
        else:
            await message.answer(
                'К сожалению заказа/тендера с таким ID в базе не нашлось :('
            )
    else:
        await message.reply(
                'Пожалуйста, вводите ТОЛЬКО цифры. В id нет букв)!'
            )
    await state.finish()

@dp.message_handler(commands=['info'])
async def send_info(message: types.Message):
    await message.reply("Приветствую вас!\n" + \
                        "Я парсер-бот для рассылки информации в группах/каналах.\n" + \
                        "Меня разработали в ashm.tech\n" + \
                        "Удачного пользования!\n" + \
                        "Контакты разработчиков:\n" + \
                        "e-mail: ahamil435@gmail.com\n" + \
                        "telegram: @abdulaev_sh_m\n" + \
                        "vk: abdulaev_sh_m\n"
                        )


@dp.message_handler(commands=['start'])
async def send_start(message: types.Message):
    await message.reply(
        "Здравствуйте!\n" + "Выберите что вы хотите сделать:\n" + \
        "Получить ссылку на заказ/товар -> /get_link"
    )


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply(
        "Если я работаю плохо, напишите пожалуйста моим разработчикам, и они 'вправят' мне мозги :)\n" + \
        "Информация о разработчиках -> /info"
    )

async def send_message_to_channel(message):
    await bot.send_message(chat_id=channel_id, text=message)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)