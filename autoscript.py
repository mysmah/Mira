#autoscripter
from aiogram.types import Message, Chat
from time import time
from warnings import warn

chats = []

def startAS(m: Message, act: str = 'reset'):
	warn('1')
	print(chats)
	id = 0
	for i in chats:
		if i.chat.id == m.chat.id:
			id += 1
	if id == 0:
		chats.append(AutoScript(m.chat))
	else:
		for i in chats:
			if i.chat.id == m.chat.id:
				i.tick(act)
			
				

class AutoScript:
	def __init__(self, c: Chat):
		warn(str(c))
		self.chat = c
		self.unm = 0
		self.unmt = 0
	def tick(self, act):
		if act == 'reset':
			self.unm = 0
			self.unmt = time()
			warn('reset')
			return None
		elif act == 'tick':
			self.unm += 1
			warn(str(self.unm) + str(self.unmt) + str(time()))
			tk = time()
			if self.unm > 1 and self.unmt + 21.0 < tk:
				return self.chat.id
				
if __name__ == '__main__':
	warn('Ты што долбаеб? Ты што сдес делоиш?')
	
			

			
		
