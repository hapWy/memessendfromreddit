from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.utils import executor
from aiogram import types
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import *
import asyncpraw

#  CREATE BOT

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)



#  REDDIT

reddit = asyncpraw.Reddit(client_id=CLIENT_ID,
                     client_secret=SECRET,
                     user_agent="random_reddit_bot/0.0.1")





#  KEYBOARD

b1 = KeyboardButton('/TopMemes')
b2 = KeyboardButton('/HotMemes')
b3 = KeyboardButton('/RisingMemes')
b4 = KeyboardButton('/NewMemes')
kb = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard= True)

kb.row(b1,b2).row(b3,b4)



#  TECHNICAL PART

async def on_startup(_):
    print('MEMEMEMEMEMEMEMEs')

@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await message.answer('Каничива', reply_markup=kb)


async def mems(message, str):
    loop = asyncio.get_event_loop()
    if 'Memes' in message.text:
        await asyncio.ensure_future(meme_loop(message, str), loop=loop)


@dp.message_handler(commands=['HotMemes','Stop'])
async def send_meme_hot(message:types.Message):
    await mems(message, 'hot')

@dp.message_handler(commands=['NewMemes','Stop'])
async def send_meme_hot(message:types.Message):
    await mems(message, 'new')

@dp.message_handler(commands=['RisingMemes','Stop'])
async def send_meme_hot(message:types.Message):
    await mems(message, 'rising')

@dp.message_handler(commands=['TopMemes','Stop'])
async def send_meme_hot(message:types.Message):
    await mems(message, 'top')



@dp.message_handler()
async def otherMsg(message:types.Message):
    await message.answer('Wow!! You can write')

async def meme_loop(message:types.Message, str):
    meme = ['Let us explain "Rule 8: No Reposts"',
            'Spooktober Meme Contest! Rules and Details in the comments. Ends on October 31st.']
    while True:
        await asyncio.sleep(10)
        memes_sub = await reddit.subreddit('memes')
        if str == 'hot':
            memes_sub = memes_sub.hot(limit=1)
        if str == 'top':
            memes_sub = memes_sub.top(limit=1)
        if str == 'rising':
            memes_sub = memes_sub.rising(limit=1)
        if str == 'new':
            memes_sub = memes_sub.new(limit=1)
        item = await memes_sub.__anext__()
        if item.title not in meme:
            meme.append(item.title)
            await message.answer_photo(item.url, caption=item.title)




executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
