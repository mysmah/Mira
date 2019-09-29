import json
import re
import time
import random
import confs
import os
from OFPNNL import *
from aiogram import *
from project_misc import *
from aiogram.types import ParseMode
import requests
import asyncio
from AdvancedMessageObjects import imo
from autoscript import start

borntime = time.time()

model = NeuralNet([1024])
model.fit(100)

def arg(args):
    args = args.split()
    q = {"password": args[-1], "args": []}
    args = args[:-1]
    while len(args):
        if args[0] == "-r":
            q["args"] += [{"key": args[0], "val": args[1].split(";")}]
            args = args[2:]
        elif args[0] == "--reboot":
            q["args"] += [{"key": args[0], "val": None}]
            args = args[1:]
        elif args[0] == "--ping":
            q["args"] += [{"key": args[0], "val": None}]
            args = args[1:]
        elif args[0] == "-s":
            q["args"] += [{"key": args[0], "val": " ".join(args[1].split("-"))}]
            args = args[2:]
        else:
            q["args"] += [{"key": args[0], "val": args[1]}]
            args = args[2:]
    return q
	
async def start(arg):
    #Функция при запуске
    await bot.send_message(-1001184868284, "Сеть инициализирована")
    global NCMusePretxt
    NCMusePretxt = confs.NCMup
    await imo.initof()
    


async def on_close(arg):
    print("Процесс умирает, нетб))9)")
    r = requests.get("https://api.telegram.org/bot" + token + "/sendMessage?chat_id=-1001184868284&text=%D0%9F%D1%80%D0%BE%D1%86%D0%B5%D1%81%D1%81%20%D0%B1%D0%BE%D1%82%D0%B0%20%D0%B7%D0%B0%D0%B2%D0%B5%D1%80%D1%88%D0%B8%D0%BB%D1%81%D1%8F")
    imo.shtdw()


bot = Bot(token=token, parse_mode = ParseMode.MARKDOWN)
dp = Dispatcher(bot)

# ЗОНА ХАНДЛЕРОВ
		
@dp.message_handler(commands=['mira'])
async def mira(m: types.Message):
    args = arg(" ".join(m.text.lower().split()[1:]))
    print(args)
    if args["password"] == passGen(m):
        for i in args["args"]:
            if i["key"] == "--reboot":
                await m.reply("reboot")
                exit()
            elif i["key"] == "-f":
                await m.reply("fit started")
                n = int(i["val"])
                await bot.send_message(-1001184868284, "Бот переведён в режим тренировки на " + str(n) + " эпох")
                model.fit(n)
                await bot.send_message(-1001184868284, "Бот переведён в активный режим")
                await m.reply("fit success")
            elif i["key"] == "-r":
                l = [int(x) for x in i["val"]]
                await m.reply(l)
                if model.new_model(l) == 1:
                    await m.reply("fail")
                else:
                    await bot.send_message(-1001184868284, "Нейросеть бота была сброшена\nНовая сеть:\n"+str(l))
                    await m.reply("reset success")
            elif i["key"] == "-s":
                await m.reply(model.pred(i["val"]))
            elif i["key"] == "--ping":
                await m.reply('Alive time: {lt}'.format(lt = (time.time()-borntime)//1))
    else:
        await m.reply("invalid password")
	


@dp.message_handler(commands=['help'])
async def help(m: types.Message):
    await m.reply('Текст для данной команды ещё не готов')

@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def decor(message: types.Message):
    if message.new_chat_members[0].id == botid:
        await bot.send_message(message.chat.id, pretxt[1], parse_mode = ParseMode.MARKDOWN)
    else:
        if NCMusePretxt == 1:
            await message.reply("Привет, [" + message.new_chat_members[0].first_name + "](tg://user?id=" + str(message.new_chat_members[0].id) + "), добро пожаловать в *" + message.chat.title + "*!", parse_mode = ParseMode.MARKDOWN)
        elif NCMusePretxt == 0:
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

@dp.message_handler(commands=['settings'])
async def knopki(m: types.Message):
    text = m.text.split()[1:]
    if text[0] == passGen(m):
        await imo.summon(model, bot, 'settings', m, locked = True, pdata = ['Меню с настройками(кнопоки)', ['СВИТЧИ','close:toggles:0'], ['FIT','counter:fit:50:0','send:fit:0','close:fit:0'], ['RESET','counter:neurod:1024:0','counter:layers:1:0','send:reset:0','close:reset:0'],['Перезагрузка'], 'close:null:0'])


@dp.callback_query_handler()
async def ebuchie(c: types.CallbackQuery):
    ret = await imo.prc(c, bot, model)
    if ret == 'fit:fited':
        await bot.send_message('@catgirl_channel', 'Бот переведен в активный режим')
    elif isinstance(ret, list) and ret[0] == 'reset:reseted':
        await bot.send_message('@catgirl_channel', 'Нейросеть бота была сброшена\nНовая сеть:\n'+str(ret[1]))
    elif ret == 'reboot':
        exit()

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
        if text.startswith("мира ") or text.startswith("mira ") or text.startswith("мира,") or text.startswith("mira,"):
            text = model.pred(text[5:])
            length = len(text)
            await asyncio.sleep(0.3)
            while length > 27:
                await message.chat.do('typing')
                length -=27
                await asyncio.sleep(5)
            await message.chat.do('typing')
            await asyncio.sleep(0.18*length)
            await message.reply(text)
        elif "@catgirl_chat_bot" in text:
            text = model.pred(text.replace('@catgirl_chat_bot', ''))
            length = len(text)
            await asyncio.sleep(0.3)
            while length > 27:
                await message.chat.do('typing')
                length -=27
                await asyncio.sleep(5)
            await message.chat.do('typing')
            await asyncio.sleep(0.18*length)
            await message.reply(text)
        elif message.reply_to_message and message.reply_to_message.from_user.id == botid:
            text = model.pred(text)
            length = len(text)
            await asyncio.sleep(0.3)
            while length > 27:
                await message.chat.do('typing')
                length -=27
                await asyncio.sleep(5)
            await message.chat.do('typing')
            await asyncio.sleep(0.18*length)
            await message.reply(text)
    else:
        text = model.pred(text)
        length = len(text)
        await asyncio.sleep(0.3)
        while length > 26:
            await message.chat.do('typing')
            length -=26
            await asyncio.sleep(5)
        await message.chat.do('typing')
        await asyncio.sleep(0.18*length)
        await message.reply(text)


# Инициализация
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start, on_shutdown=on_close)
