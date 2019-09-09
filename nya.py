import json
import re
import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import models
from tensorflow.keras import layers
import numpy as np
from aiogram import *
from razdel import tokenize
from project_misc import *
from OFPNNL import *

async def start(arg):
    #Функция при запуске
    await bot.send_message(-1001184868284, "Сеть инициализирована")

model = NeuralNet([1024])

bot = Bot(token=token)
dp = Dispatcher(bot)

# ЗОНА ХАНДЛЕРОВ

@dp.message_handler(commands=['say'])
async def nyan(message: types.Message):
    print(message.from_user.full_name, " (@", message.from_user.username, "): ", message.text, sep="")
    await message.reply(model.pred(message.text))

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
    #await message.reply(model.pred(message.text))
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
    executor.start_polling(dp, skip_updates=True, on_startup=start)
