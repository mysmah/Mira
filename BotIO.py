import json
import re
import time
import logging
import datetime
import random
import confs
import os

import hashlib
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle

from aflood import AntiFlood as aflood
from OFPNNL import *
from aiogram import *
from project_misc import *
from aiogram.types import ParseMode, ContentType
import requests
import asyncio
from typingE import *
from AdvancedMessageObjects import imo
from autoscript import startAS

import database
import message_handler as prepr


rfeedback = 120

logging.basicConfig(filename='log.log', filemode='a', level=logging.INFO)
logging.info(f'\n\n==CHECKPOINT==\nNew instance on {os.name}\nPath: {os.path.abspath(__file__)}\nStart time: {datetime.datetime.now().strftime("%c")}\n')
starttime = time.time()
loop = asyncio.get_event_loop()
afl = aflood(loop, limit=15)
bot = Bot(token=token, parse_mode = ParseMode.MARKDOWN)
dp = Dispatcher(bot, loop=loop)

borntime = time.time()
	     
	    
db = database.INITIALIZATE()
wlist = db.get_wlist()


model = NeuralNet([1024], loop)
model.fit(100)

async def write_au(chat):
    rand = random.randint(0,4)
    if rand == 0:
        await chat.do('typing')
        await asyncio.sleep(1.3)
        await bot.send_message(chat.id, 'Приветики')
        await asyncio.sleep(0.5)
        await chat.do('typing')
        await asyncio.sleep(2)
        await bot.send_message(chat.id, 'Как у вас дела?')
    elif rand == 1:
        await chat.do('typing')
        await asyncio.sleep(0.4)
        await bot.send_message(chat.id, 'Эй')
        await asyncio.sleep(0.5)
        await chat.do('typing')
        await asyncio.sleep(3,4)
        await bot.send_message(chat.id, 'А про меня не забыли?')
    elif rand == 2:
        await chat.do('typing')
        await asyncio.sleep(1.8)
        await bot.send_message(chat.id, 'Всем дарова')
        await asyncio.sleep(0.2)
        await bot.send_stickers(chat.id, stickers['hi2'])
    elif rand == 3:
        await chat.do('typing')
        await asyncio.sleep(1)
        await bot.send_message(chat.id, 'А вы случаем не забыли про меня?')
        await asyncio.sleep(0.2)
        await bot.send_sticker(chat.id, stickers['?'])
    elif rand == 4:
        await bot.send_sticker(chat.id, stickers['hi1'])

def arg(args):
    logging.info(f'[{datetime.datetime.now().strftime("%c")} /INFO]: mira command {args}')
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
        elif args[0] == "-a" or args[0] == "--add":
            q["args"] += [{"key": "-a", "val": None}]
            args = args[1:]
        elif args[0] == "-d":
            q["args"] +=[{"key": args[0], "val": None}]
            args = args[1:]
        elif args[0] == '--set_feedback':
            q["args"] += [{'key': args[0], 'val': int(args[1])}]
            args = args[2:]
        elif args[0] == '-w':
            q["args"] += [{'key': args[0], 'val': None}]
            args = args[1:]
        elif args[0] == '--unwatch':
            q["args"] += [{'key': args[0], 'val': None}]
            args = args[1:]
        else:
            q["args"] += [{"key": args[0], "val": args[1]}]
            args = args[2:]
    return q
	
async def start(arg):
    #Функция при запуске
    await bot.send_message(-1001184868284, "Сеть инициализирована")
    global NCMusePretxt, wlist
    NCMusePretxt = confs.NCMup
    await imo.initof()
    prepr.init(await bot.get_me(), wlist)
    


async def on_close(arg):
    print("Процесс умирает, нетб))9)")
    r = requests.get("https://api.telegram.org/bot" + token + "/sendMessage?chat_id=-1001184868284&text=%D0%9F%D1%80%D0%BE%D1%86%D0%B5%D1%81%D1%81%20%D0%B1%D0%BE%D1%82%D0%B0%20%D0%B7%D0%B0%D0%B2%D0%B5%D1%80%D1%88%D0%B8%D0%BB%D1%81%D1%8F")
    imo.shtdw()

# ЗОНА ХАНДЛЕРОВ
		
@dp.message_handler(commands=['mira'])
async def mira(m: types.Message):
    print(m.from_user.full_name, " (@", m.from_user.username, ", title: ", m.chat.title, " (", await m.chat.get_url(), ")): ", m.text, sep="")
    args = arg(" ".join(m.text.lower().split()[1:]))
    print(args)
    global wlist, rfeedback
    if args["password"] == passGen(m):
        for i in args["args"]:
            if i["key"] == "--reboot":
                await m.reply("reboot")
                exit()
            elif i["key"] == "-f":
                await m.reply("fit started")
                n = int(i["val"])
                t = time.time()
                model.fit(1)
                await m.reply('Время на эпоху: {} \nОставшиеся время: {} минут.'.format(round(time.time() - t, 1), round(((time.time() - t) * n-1.0)/60, 2)))
                await bot.send_message(-1001184868284, "Бот переведён в режим тренировки на " + str(n) + " эпох")
                model.fit(n-1)
                await bot.send_message(-1001184868284, "Бот переведён в активный режим")
                await m.reply("fit success")
            elif i["key"] == "-r":
                l = [int(x) for x in i["val"]]
                await m.reply(l)
                if model.new_model(l) == 1:
                    await m.reply("fail")
                else:
                    await bot.send_message(-1001184868284, "Нейросеть бота была сброшена\nНовая сеть:\n")
                    await bot.send_message(-1001184868284, l)
                    await m.reply("reset success")
            elif i["key"] == "-s":
                await m.reply(await model.pred(i["val"]))
            elif i["key"] == "--ping":
                await m.reply('Alive time: {lt}'.format(lt = (time.time()-borntime)//1))
            elif i["key"] == "-d":
                await m.reply('*disabled for this chat*')
                await leave(m)
            elif i["key"] == "-a":
                print(m.reply_to_message.text)
                if m.reply_to_message and len(m.reply_to_message.text.split("\n")) > 0 and len(m.reply_to_message.text.split("\n")) % 2 == 0:
                    writin = open("dialog.txt", "a")
                    writin.write("\n" + m.reply_to_message.text)
                    writin.close()
                    await bot.send_message(-1001184868284, "Добавлен новый диалог:\n" + m.reply_to_message.text)
                    await m.reply("success")
                else:
                    await message.reply("fail")
            elif i['key'] == '--set_feedback':
                rfeedback = i['val']
                await m.reply(f'rfeedback turns into {rfeedback}')
            elif i['key'] == '-w':
                wlist = db.add_to_wlist(m.reply_to_message.from_user.id)
                prepr.update(wlist)
                await m.delete()
            elif i['key'] == '-unwatch':
                wlist = db.remove_from_wlist(m.reply_to_message.from_user.id)
                prepr.update(wlist)
                await m.delete()		 
    else:
        await m.reply("invalid password")
	


@dp.message_handler(commands=['help','donate', 'support_project'])
async def help(m: types.Message):
    await m.reply('Данная фича пока не поддерживается, или была хакнута котбом')

@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def decor(message: types.Message):
    if message.new_chat_members[0].id == botid:
        await bot.send_message(message.chat.id, pretxt[1], parse_mode = ParseMode.MARKDOWN)
    else:
        if NCMusePretxt == 1:
            await message.reply("Привет, [" + message.new_chat_members[0].first_name + "](tg://user?id=" + str(message.new_chat_members[0].id) + "), добро пожаловать в *" + message.chat.title + "*!", parse_mode = ParseMode.MARKDOWN)
        elif NCMusePretxt == 0:
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


@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    text = inline_query.query or ''
    ans = await model.pred(text)
    text = "- " + text + "\n- " + ans
    input_content = InputTextMessageContent(text)
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    print("inline: ", inline_query.from_user.full_name, " (@", inline_query.from_user.username, "): ", text, sep="")
    item = InlineQueryResultArticle(
        id=result_id,
        title=ans,
        input_message_content=input_content,
   )
    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)

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
    print(message.from_user.full_name, " (@", message.from_user.username, ", title: ", message.chat.title, " (", await message.chat.get_url(), ")): ", message.text, sep="")
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

@dp.message_handler(commands=['get_id'])
async def getid(m: types.Message):
    if len(m.text.split()) == 2:
        if m.text.split()[1] in stickers.keys():
            await m.reply_sticker(stickers[m.text.split()[1]])
        else:
            await m.reply('unknown key')
    else:
        await m.reply('fail')

@dp.message_handler(commands=['adddialog'])
async def adialog(message: types.Message):
    print(message.from_user.full_name, " (@", message.from_user.username, ", title: ", message.chat.title, " (", await message.chat.get_url(), ")): ", message.text, sep="")
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

@dp.message_handler(content_types=ContentType.PINNED_MESSAGE)
async def pinnedansw(m):
    text = await model.pred(m.pinned_message.text.lower())
    await typing(text,m.pinned_message)

#@dp.message_handler(regexp='[\s\S]+')
async def nya(message: types.Message):
    text = message.text.lower()
    print(message.from_user.full_name, " (@", message.from_user.username, ", title: ", message.chat.title, " (", await message.chat.get_url(), ")): ", message.text, sep="")
    check = None
    if message.reply_to_message and message.reply_to_message.from_user.id == botid:
        check = afl.check(message)
    elif text.startswith('мира ') or text.startswith('мира,') or text.startswith('mira ') or text.startswith('mira,') or ', мира,' in text or ', mira,' in text:
        check = afl.check(message)
    elif len(text.split(', ')) > 1 and text.split(', ')[1] == 'мира':
        check = afl.check(message)
    elif message.chat.id > 0:
        check = afl.check(message)
    else:
        check = 0
    rand = random.randint(0,2)
    if check == 3:
        if rand == 0:
            await typing('btest0', message)
        elif rand == 1:
            await typing('btest1', message)
        else:
            await typing('btest2', message)
            
    elif check == 2:
        if rand == 0:
            await typing('Да ты уже достал!', message)
        elif rand == 1:
            await typing('Ну сколько можно?', message)
        else:
            await typing('Я уже устала от тебя!', message)
            
    elif check == 1:
        pass
        
    elif check == 0:
        logging.info(f'[{datetime.datetime.now().strftime("%c")} /INFO]: Message event with {id(message)}')
        if message.reply_to_message and message.reply_to_message.from_user.id == botid:
            text = await model.pred(text)
            await typing(text, message)
        elif text.startswith('мира ') or text.startswith('мира,') or text.startswith('mira ') or text.startswith('mira,') or ', мира,' in text or ', mira,' in text:
            text = await model.pred(text[5:])
            await typing(text, message)
        elif len(text.split(', ')) > 1 and text.split(', ')[1] == 'мира':
            text = await model.pred(text.replace(', мира', ''))
            await typing(text, message)
        elif message.chat.id > 0:
            text = await model.pred(text)
            await typing(text, message, answer = True)
        elif random.randint(0, rfeedback) == 0:
            rm = await typing(await model.pred(text), message, answer = True)
            await message.forward(563868409)
            await rm.forward(563868409)
@dp.message_handler(regexp='[\s\S]+')
async def nnya(m):
    result = await prepr.process_m(m)
    if result == 0:
        await typing(await model.pred(m.text.lower()),m,answer = True)
    elif result == 1:
        await typing(await model.pred(m.text.lower()),m)

# Инициализация
if __name__ == '__main__':
    logging.info(f'[{datetime.datetime.now().strftime("%c")} /INFO]: bot inited in {str(time.time() - starttime)} seconds')
executor.start_polling(dp, loop=loop, skip_updates=True, on_startup=start, on_shutdown=on_close)
