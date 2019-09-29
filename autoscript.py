#autoscripter
from aiogram.types import Message, Chat
from time import time
from warnings import warn

chats = []

def start(m: Message, act: str = 'reset'):
	if m.chat not in chats:
		chats.append(AutoScript(m.chat))
	else:
		for i in chats:
			if i.id == m.chat.id:
				return i.tick(act)
				

class AutoScript:
	def __init__(self, c: Chat):
		self.chat = c
		self.unm = 0
	def tick(self, act):
		if act == 'reset':
			self.unm = 0
			self.unmt = time()
			return None
		elif act == 'tick':
			self.unm += 1
			if self.unm > 1 and self.unmt + 21.0 < time:
				return self.chat.id
				
if __name__ == '__main__':
	warn('Ты што долбаеб? Ты што сдес делоиш?')
	
			

			
		