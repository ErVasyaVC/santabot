import logging
import json
import datetime
from datetime import datetime
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

bot = Bot(token='6987030665:AAE0xuZ6PsFtXaSdWHNqSxxPbawhY9oIt-8', parse_mode='HTML')
dp = Dispatcher()

logger = logging.getLogger(__name__)

with open('text.json', 'r', encoding='utf-8') as f:
    text_message = json.load(f)


class WaitingForMessage(StatesGroup):
    hello_text = State()
    text2 = State()
    text3 = State()
    text4 = State()
    text5 = State()
    text6 = State()
    text7 = State()
    text8 = State()
    text9 = State()

@dp.message(Command("admin"))
async def text4(message: Message):
    mss = "Список участников которые написали первое сообщение:"
    for i in text_message["message1"].keys():
        if text_message["message1"][i][1] == 0 and i != "simple":
            mss += "\n@" + i + " - " + "еще нет"
        elif i != "simple":
            mss += "\n@" + i + " - " + "да"
    mss += "\nСписок участников которые написали второе сообщение:"
    for i in text_message["message2"].keys():
        if text_message["message2"][i][1] == 0 and i != "simple":
            mss += "\n@" + i + " - " + "еще нет"
        elif i != "simple":
            mss += "\n@" + i + " - " + "да"
    mss += "\nОтзывы:"
    for i in text_message["feedback"].keys():
        if i != "simple":
            mss += "\n@" + i + " - " + text_message["feedback"][i]
    if message.from_user.id in text_message['admins'].values():
        await message.answer(mss)


@dp.message(Command("start"))
async def hello(message: Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text=text_message['texts']['answer1'])]],
        resize_keyboard=True,
    )
    await message.answer(
        text=text_message['texts']['hello_text'],
        reply_markup=keyboard
    )
    await state.set_state(WaitingForMessage.hello_text)


@dp.message(WaitingForMessage.hello_text, F.text == text_message['texts']['answer1'])
async def text2(message: Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text=text_message['texts']['answer2'])]],
        resize_keyboard=True,
    )
    await message.reply(
        text=text_message['texts']['text2'],
        reply_markup=keyboard
    )
    # await message.reply(text_message['texts']['text2'], reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(WaitingForMessage.text2)


@dp.message(WaitingForMessage.text2, F.text == text_message['texts']['answer2'])
async def text3(message: Message, state: FSMContext):
    text_message["message1"][message.from_user.username] = [message.from_user.id, 0, ""]
    text_message["message2"][message.from_user.username] = [message.from_user.id, 0, ""]
    with open('text.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(text_message, sort_keys=True, indent=2))
    await message.reply(text_message['texts']['text3'], reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(WaitingForMessage.text3)


@dp.message(WaitingForMessage.text3, Command("mail1"))
async def text4(message: Message, state: FSMContext):
    await message.answer(text_message['texts']['text4'])
    await state.set_state(WaitingForMessage.text4)


@dp.message(WaitingForMessage.text4, F.text)
async def text5(message: Message, state: FSMContext):
    await message.answer(text_message['texts']['text5'])
    print(message.from_user.username)
    text_message["message1"][message.from_user.username] = [message.from_user.id, 1, message.text]
    # text_message["participant"][message.from_user.username] = [message.from_user.id, 1]
    with open('text.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(text_message, sort_keys=True, indent=4))
    await state.set_state(WaitingForMessage.text5)
    print(message.text)
    # await message.answer(text_message["message1"][message.from_user.username])


@dp.message(WaitingForMessage.text5, Command("mail2"))
async def text6(message: Message, state: FSMContext):
    text_message["message2"][message.from_user.username] = [message.from_user.id, 0, ""]
    with open('text.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(text_message, sort_keys=True, indent=2))
    await message.answer(text_message['texts']['text6'])
    await state.set_state(WaitingForMessage.text6)


@dp.message(WaitingForMessage.text6, F.text)
async def text7(message: Message, state: FSMContext):
    await message.answer(text_message['texts']['text7'])
    print(message.from_user.username)
    text_message["message2"][message.from_user.username] = [message.from_user.id, 1, message.text]
    # text_message["participant"][message.from_user.username] = [message.from_user.id, 1]
    with open('text.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(text_message, sort_keys=True, indent=4))
    await state.set_state(WaitingForMessage.text7)
    print(message.text)


@dp.message(WaitingForMessage.text7, Command("feedback"))
async def text8(message: Message, state: FSMContext):
    text_message["feedback"][message.from_user.username] = ""
    with open('text.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(text_message, sort_keys=True, indent=2))
    await message.answer(text_message['texts']['text8'])
    await state.set_state(WaitingForMessage.text8)


@dp.message(WaitingForMessage.text8, F.text)
async def text9(message: Message, state: FSMContext):
    await message.answer(text_message['texts']['text9'])
    text_message["feedback"][message.from_user.username] = [message.from_user.username, message.text]
    # text_message["participant"][message.from_user.username] = [message.from_user.id, 1]
    with open('text.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(text_message, sort_keys=True, indent=4))
    await state.set_state(WaitingForMessage.text9)


async def remind1():
    arr = text_message["message1"]
    for i in arr.values():
        if i[1] == 0:
            await bot.send_message(i[0], text_message['texts']['remind1'])
            # await state.set_state(WaitingForMessage.text8)


async def remind2():
    arr = text_message["message1"]
    for i in arr.values():
        if i[1] == 0:
            await bot.send_message(i[0], text_message['texts']['remind2'])


async def remind3():
    arr = text_message["message1"]
    for i in arr.values():
        if i[1] == 0:
            await bot.send_message(i[0], text_message['texts']['remind3'])


async def remind4():
    arr = text_message["message1"]
    for i in arr.values():
        if i[1] == 0:
            await bot.send_message(i[0], text_message['texts']['remind4'])


async def send_pre_message():
    arr = text_message["participant"]
    for i in arr.keys():
        await bot.send_message(text_message["message1"][i][0], text_message['texts']['pre_message1'])
        await bot.send_message(text_message["message1"][i][0], text_message["message1"][arr[i]][2])
        await bot.send_message(text_message["message1"][i][0], text_message['texts']['pre_message'])


async def send_message():
    arr = text_message["participant"]
    for i in arr.keys():
        await bot.send_message(text_message["message2"][arr[i]][0], text_message['texts']['message'])
        await bot.send_message(text_message["message2"][arr[i]][0], text_message["message2"][i][2])
        await bot.send_message(text_message["message2"][arr[i]][0], text_message['texts']['message1'])


async def remind5():
    arr = text_message["message2"]
    for i in arr.values():
        if i[1] == 0:
            await bot.send_message(i[0], text_message['texts']['remind5'])
            # await state.set_state(WaitingForMessage.text8)


async def remind6():
    arr = text_message["message2"]
    for i in arr.values():
        if i[1] == 0:
            await bot.send_message(i[0], text_message['texts']['remind6'])


async def remind7():
    arr = text_message["message2"]
    for i in arr.values():
        if i[1] == 0:
            await bot.send_message(i[0], text_message['texts']['remind7'])


async def remind8():
    arr = text_message["message2"]
    for i in arr.values():
        if i[1] == 0:
            await bot.send_message(i[0], text_message['texts']['remind8'])


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(remind1, "date", run_date=datetime(2023, 12, 18, 14, 55))
    scheduler.add_job(remind2, "date", run_date=datetime(2023, 12, 18, 14, 56))
    scheduler.add_job(remind3, "date", run_date=datetime(2023, 12, 18, 14, 57))
    scheduler.add_job(remind4, "date", run_date=datetime(2023, 12, 18, 14, 58))
    scheduler.add_job(send_pre_message, "date", run_date=datetime(2023, 12, 18, 15, 00))
    scheduler.add_job(remind5, "date", run_date=datetime(2023, 12, 18, 15, 2))
    scheduler.add_job(remind6, "date", run_date=datetime(2023, 12, 18, 15, 3))
    scheduler.add_job(remind7, "date", run_date=datetime(2023, 12, 18, 15, 5))
    scheduler.add_job(remind8, "date", run_date=datetime(2023, 12, 18, 15, 6))
    scheduler.add_job(send_message, "date", run_date=datetime(2023, 12, 18, 15, 10))
    scheduler.start()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
