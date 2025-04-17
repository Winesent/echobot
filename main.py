from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
import os
import re

load_dotenv('token.env')
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение'
    )


@dp.message(Command(commands=['caps']))
async def caps_command(message: Message):
    await message.answer(f'{message.text.split('/caps')[1].upper()}')


@dp.message(Command(commands=['reverse']))
async def reverse_command(message: Message):
    await message.answer(f'{''.join(reversed(message.text.split('/reverse')[1]))}')


@dp.message(
    lambda msg: any(
        word in re.sub(r'[^\w\s]', '', msg.text.lower())  # Удаляет все знаки препинания
        for word in ['привет', 'здравствуйте', 'ку', 'хай', 'хелло',
                     'доброе утро', 'добрый день', 'добрый вечер', 'здарова']
    )
)
async def hello_command(message: Message):
    await message.answer(f'{message.from_user.first_name}, привет!')


@dp.message(F.photo)
async def send_photo(message: Message):
    if message.caption is not None:
        await message.reply(text=f' Что это за {message.caption}')
    else:
        await message.reply("Данный формат пока не поддерживается")


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)


if __name__ == '__main__':
    dp.run_polling(bot)
