import neat
from razdel import tokenize
import time
import json
import re
import os

class NeuralNet:
    def __init__(self):
        self.new_model()

# Создание новой модели нейросети
    def new_model(self):
        fil = open('dict.json')
        self.dict0 = json.loads(fil.read())
        fil.close()

        #fil = open('dialog.txt')
        #dialog = fil.read().split("\n")
        #if not dialog:
        #    fil1=open('dialog.txt','w')
        #    fil1.write('привет\nпривет')
        #    fil1.close()
        #    dialog = fil.read().split('\n')
        #fil.close()
        #fil = open('text.txt', "w")
        #fil.write(" ".join(dialog))
        #fil.close()
        #a = []
        #b = []
        #for i in range(len(dialog)):
        #    if i % 2:
        #        b += [dialog[i]]
        #    else:
        #        a += [dialog[i]]
        #fil = open('train.a', 'w')
        #fil.write(json.dumps(a, ensure_ascii=False))
        #fil.close()
        #fil = open('train.b', 'w')
        #fil.write(json.dumps(b, ensure_ascii=False))
        #fil.close()

        #fil = open('text.txt')
        #text = fil.read()
        #fil.close()
        #self.dict0 = list(set([_.text for _ in list(tokenize(text.lower()))]))
        #fil = open('dict.json', 'w')
        #fil.write(json.dumps(self.dict0, ensure_ascii=False))
        #fil.close()

        fil = open('train.a')
        a = json.loads(fil.read())
        fil.close()
        fil = open('train.b')
        b = json.loads(fil.read())
        fil.close()
        for i in range(len(a)):
            a[i] = self.text2dict1(a[i])
            b[i] = self.text2dict1(b[i])
        self.x = a
        self.y = b
        
        if glob.glob('neat-checkpoint-*'):
            chkpt = "neat-checkpoint-" + str(sorted([int(i[16:]) for i in glob.glob('neat-checkpoint-*')])[-1])
            self.p = neat.Checkpointer.restore_checkpoint(chkpt)
            
            print(chkpt)
            
            local_dir = os.getcwd()
            config_file = os.path.join(local_dir, 'config-feedforward')

            self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                      neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                      config_file)
        else:
            local_dir = os.getcwd()
            config_file = os.path.join(local_dir, 'config-feedforward')

            self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             config_file)
        
            self.p = neat.Population(self.config)

            self.p.add_reporter(neat.StdOutReporter(True))
            stats = neat.StatisticsReporter()
            self.p.add_reporter(stats)
            self.p.add_reporter(neat.Checkpointer(5))
        winner = self.p.run(self.eval_genomes, 1)
        self.winner_net = neat.nn.FeedForwardNetwork.create(winner, self.config)

    def eval_genomes(self, genomes, config):
        for genome_id, genome in genomes:
            genome.fitness = 1.0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            for xi, xo in zip(self.x, self.y):
                output = net.activate(xi)
                genome.fitness -= sum([(output[i] - xo[i]) ** 2 for i in range(len(output))])
# Обучение
    def fit(self, n):
        winner = self.p.run(self.eval_genomes, n)
        self.winner_net = neat.nn.FeedForwardNetwork.create(winner, self.config)

    def spell(self, q):
        tim = time.time()
        req = []
        for i in q:
            if i not in self.dict0 and i[0] != '{' and len(i) > 2:
                word = Word(i).spellsafe
                if word:
                    req.append(word)
                else:
                    req.append(i)
            else:
                req.append(i)
        for z in req:
            if self == None:
                req.remove(self)
        return ' '.join(req)
        
# Обмен айдишниками слов с сетью
    def pred(self, q):
        #q = [_.text for _ in list(tokenize(q.lower()))]
        prediction = self.winner_net.activate(self.text2dict1(q))
        prediction = [int(round(x)) for x in prediction]
        text = self.dict2text1(prediction)
        return text.capitalize() if text else "..."

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
        i = 0
        l = len(ret)
        while i < l - 1:
            _ = ret[i] + ret[i + 1]
            if re.search(' [^\"\'\\w]', _):
                ret = ret[:i] + ret[i+1:]
                l = len(ret)
            else:
                i += 1
        return ret
