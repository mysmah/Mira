from tensorflow import keras
from tensorflow.keras import models
from tensorflow.keras import layers
from razdel import tokenize
from pyaspeller import Word

import tensorflow as tf
import numpy as np
import json
import re
import os

class NeuralNet:
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
        q = q.lower()
        q = q.replace(',',' {comma} ').replace('.',' {point} ').replace('<',' {parenthesescor0} ').replace('>',' {parenthesescor1} ').replace(':',' {dbpoint} ').replace('(',' {parentheses0} ').replace(')',' {parentheses1} ').replace('?',' {question} ').replace('!',' {exclamation} ').replace('-',' {spliter} ')
        req = []
        for i in q.split():
            if i not in self.dict0 and i[0] != '{':
                word = Word(i)
                req.append(word.spellsafe)
            else:
                req.append(i)
        print(req)
        print(' '.join(req)
        q = ' '.join(req).format(comma = ',', point = '.',parenthesescor0='<', parenthesescor1='>', dbpoint=':', parentheses0='(', parentheses1=')', question='?', exclamation='!', spliter='-')
            
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
        ret = " ".join(text)
        ret = ret.replace(' , ', ', ')
        ret = ret.replace(' ! ', '! ')
        ret = ret.replace(' . ', '. ')
        ret = ret.replace(' ? ', '? ')
        ret = ret.replace(' : ', ':')
        ret = ret.replace(' ,', ', ')
        ret = ret.replace(' !', '! ')
        ret = ret.replace(' ?', '? ')
        ret = ret.replace(' .', '. ')
        ret = ret.replace(' < ', '<')
        ret = ret.replace(' " ', ' "')
        ret = ret.replace(' :', ':')
        ret = ret.replace('< ', '<')
        return ret
