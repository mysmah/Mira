import json
import re
import random
import os
from OFPNNL import *
from aiogram import *
from project_misc import *
from aiogram.types import ParseMode
import requests
import AdvancedMessageObject as amo

model = NeuralNet([1024])
model.fit(100)

async def start(arg):
    #Функция при запуске
    await bot.send_message(-1001184868284, "Сеть инициализирована")
async def on_close(arg):
    print("Процесс умирает, нетб))9)")
    r = requests.get("https://api.telegram.org/bot" + token + "/sendMessage?chat_id=-1001184868284&text=%D0%9F%D1%80%D0%BE%D1%86%D0%B5%D1%81%D1%81%20%D0%B1%D0%BE%D1%82%D0%B0%20%D0%B7%D0%B0%D0%B2%D0%B5%D1%80%D1%88%D0%B8%D0%BB%D1%81%D1%8F")
bot = Bot(token=token)
dp = Dispatcher(bot)

# GПеременные

global NCMusePretxt
NCMusePretxt = True

# GПеременные/

# ЗОНА ХАНДЛЕРОВ

@dp.message_handler(commands=['say'])
async def nyan(message: types.Message):
    print(message.from_user.full_name, " (@", message.from_user.username, "): ", message.text, sep="")
    await message.reply(model.pred(message.text))


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def decor(message: types.Message):
    if message.new_chat_members[0].id == botid:
        await bot.send_message(message.chat.id, pretxt[1], parse_mode = ParseMode.MARKDOWN)
    else:
        if NCMusePretxt == True:
            await message.reply("Привет, [" + message.new_chat_members[0].first_name + "](tg://user?id=" + str(message.new_chat_members[0].id) + "), добро пожаловать в *" + message.chat.title + "*!", parse_mode = ParseMode.MARKDOWN)
        elif NCMusePretxt == False:
            random.seed()
            if random.randint(0,4) == 0:
                text = model.pred('sys.io.answ0')
            elif random.randint(0,4) == 1:
                text = model.pred('sys.io.answ1')
            elif random.randint(0,4) == 2:
                text = model.pred('sys.io.answ2')
            elif random.randint(0,4) == 3:
                text = model.pred('sys.io.answ3')
            elif random.randint(0,4) == 4:
                text = model.pred('sys.io.answ4')
            text.replace('usrn', ', [' + message.new_chat_message[0].first_name+"](tg://user?id="+str(message.new_chat_members[0].id)+"), ")
            text.replace('chtn', message.chat.title)
            await message.reply(text, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=['start'])
async def court(message: types.Message):
	if message.chat.id > 0:
		await bot.send_message(message.chat.id, pretxt[0], parse_mode = ParseMode.MARKDOWN)


@dp.message_handler(commands=['fit'])
async def fit(message: types.Message):
    print(message.from_user.full_name, " (@", message.from_user.username, "): ", message.text, sep="")
    await message.reply("started")
    try:
        n = int(message.text.split()[1])
    except:
        n = 1
    await bot.send_message(-1001184868284, "Бот переведён в режим тренировки на " + str(n) + " эпох")
    model.fit(n)
    await bot.send_message(-1001184868284, "Бот переведён в активный режим")
    await message.reply("success")


@dp.message_handler(commands=['reset'])
async def reset(message: types.Message):
    print(message.from_user.full_name, " (@", message.from_user.username, "): ", message.text, sep="")
    m = [int(x) for x in message.text.split()[1:]]
    await message.reply(m)
    if model.new_model(m) == 1:
        await message.reply("fail")
    else:
        await bot.send_message(-1001184868284, "Нейросеть бота была сброшена\nНовая сеть:")
        await bot.send_message(-1001184868284, m)
        await message.reply("success")

@dp.message_handler(commands=['settings'])
async def knopki(m: types.Message):
    text = m.text.split()[1:]
    if text[0] == passGen(m):
        await amo.create('settings', m, m.from_user.id)


@dp.callback_query_handler()
async def ebuchie(c: types.CallbackQuery):
    await amo.proccess(c)


@dp.message_handler(commands=['add'])
async def add(message: types.Message):
    print(message.from_user.full_name, " (@", message.from_user.username, "): ", message.text, sep="")
    text = message.text.split()[1:]
    text = " ".join(text[1:]).split("&") if text[0] == passGen(message) else "fail: invalid password"
    if type(text) == list: text = text if len(text) == 2 else "fail: invalid format"
    await message.reply(text)
    if type(text) == list:
        text = "\n".join(text)
        writin = open("dialog.txt", "a")
        writin.write("\n" + text)
        writin.close()
        await bot.send_message(-1001184868284, "Добавлен новый диалог:\n" + text)
        await message.reply("success")
    await message.delete()


@dp.message_handler(commands=['adddialog'])
async def adialog(message: types.Message):
    print(message.from_user.full_name, " (@", message.from_user.username, "): ", message.text, sep="")
    print(message.reply_to_message.text)
    if message.reply_to_message and "".join(message.text.split()[1:]) == passGen(message) and len(message.reply_to_message.text.split("\n")) > 0 and len(message.reply_to_message.text.split("\n")) % 2 == 0:
        writin = open("dialog.txt", "a")
        writin.write("\n" + message.reply_to_message.text)
        writin.close()
        await bot.send_message(-1001184868284, "Добавлен новый диалог:\n" + message.reply_to_message.text)
        await message.reply("success")
    else:
        await message.reply("fail")
    await message.delete()


@dp.message_handler(regexp='[\s\S]+')
async def nya(message: types.Message):
    print(message.from_user.full_name, " (@", message.from_user.username, "): ", message.text, sep="")
    text = message.text.lower()
    if message.chat.id < 0:
        if text.startswith("мира ") or text.startswith("mira") or text.startswith("мира,") or text.startswith("mira,"):
            await message.reply(model.pred(text[5:]))
        elif "@catgirl_chat_bot" in text:
            await message.reply(model.pred(text.replace("@catgirl_chat_bot", "")))
        elif message.reply_to_message and message.reply_to_message.from_user.id == botid:
            await message.reply(model.pred(text))
    else:
        await message.reply(model.pred(text))


# Инициализация
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start, on_shutdown=on_close)
