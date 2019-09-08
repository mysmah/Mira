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
from q import *


class md:
    def __init__(self, arr):
        self.new_model(arr)

# Создание новой модели нейросети
    def new_model(self, arr: list):
        if arr == []:
            return 1
        fil = open('dict.json')
        self.dict0 = json.loads(fil.read())
        fil.close()

        fil = open('dialog.txt')
        dialog = fil.read().split("\n")
        fil.close()
        fil = open('text.txt', "w")
        fil.write(" ".join(dialog))
        fil.close()
        a = []
        b = []
        for i in range(len(dialog)):
            if i % 2:
                b += [dialog[i]]
            else:
                a += [dialog[i]]
        fil = open('train.a', 'w')
        fil.write(json.dumps(a, ensure_ascii=False))
        fil.close()
        fil = open('train.b', 'w')
        fil.write(json.dumps(b, ensure_ascii=False))
        fil.close()

        fil = open('text.txt')
        text = fil.read()
        fil.close()
        self.dict0 = list(set([_.text for _ in list(tokenize(text.lower()))]))
        fil = open('dict.json', 'w')
        fil.write(json.dumps(self.dict0, ensure_ascii=False))
        fil.close()

        fil = open('train.a')
        a = json.loads(fil.read())
        fil.close()
        fil = open('train.b')
        b = json.loads(fil.read())
        fil.close()
        for i in range(len(a)):
            a[i] = self.text2dict1(a[i])
            b[i] = self.text2dict1(b[i])
        self.x = np.asarray(a)
        self.y = np.asarray(b)

        self.model = models.Sequential()
        self.model.add(layers.Dense(arr[0], input_dim=len(self.dict0), activation='tanh'))
        for i in arr[1:]:
            self.model.add(layers.Dense(i, activation='tanh'))
        self.model.add(layers.Dense(len(self.dict0), activation='tanh'))
        self.model.compile(optimizer=tf.train.AdamOptimizer(0.001), loss='mse', metrics=['mae'])

# Обучение
    def fit(self, n):
        self.model.fit(self.x, self.y, epochs=n, batch_size=1000)

# Обмен айдишниками слов с сетью
    def pred(self, q):
        prediction = self.model.predict([[self.text2dict1(q)]])
        prediction = [int(round(x)) for x in prediction[0]]
        text = self.dict2text1(prediction)
        return text.capitalize() if text else "?"

# Преобразование текста в айдишники слов
    def text2dict1(self, text):
        text = [_.text for _ in list(tokenize(text.lower()))]
        out = []
        for i in range(len(self.dict0)):
            out += [int(self.dict0[i] in text)]
        return out

# Обратное преобразование
    def dict2text1(self, arr):
        text = []
        for i in range(len(self.dict0)):
            if arr[i]:
                text += [self.dict0[i]]
        return " ".join(text)

model = md([1024])

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
    await bot.send_message(-1001184868284, "Бот переведён в режим тренировки на " + str(n) + " эпох)
    model.fit(n)
    await message.reply("success")

@dp.message_handler(commands=['reset'])
async def reset(message: types.Message):
    print(message.from_user.full_name, " (@", message.from_user.username, "): ", message.text, sep="")
    m = [int(x) for x in message.text.split()[1:]]
    await message.reply(m)
    if model.new_model(m) == 1:
        await message.reply("fail")
    else:
        await bot.send_message(-1001184868284, "Нейросеть бота была сброшена\nНовая сеть: ")
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

# ЗОНА ХАНДЛЕРОВ


# Инициализация
if __name__ == '__main__':
    bot.send_message(-1001184868284, "Бот был запущен")
    executor.start_polling(dp, skip_updates=True)
