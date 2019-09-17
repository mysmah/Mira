import BotIO
from OFPNNL import *
import logging
import kb
from kb import *
import requests
from aiogram.types import \
InlineKeyboardMarkup, InlineKeyboardButton



amolist = []



# /////public funcs\\\\\\

async def create(type, m, sender):
	logging.debug(':AMO: Called create method')
	await InlineMessage().reg(type, m, s = sender)

async def proccess(c):
	logging.debug(':AMO: Called proccess method')
	for i in amolist:
		await i.proc(c)







class InlineMessage:
	type = None
	m = None
	s = None
	data = []
	kb = None
	
	
	
	async def reg(self, type, m, s):
		
		print(s)
		self.type = type
		self.s = s
		
# Determine type of Inline Message
		
		if type == 'settings':
			self.data = [0, 0]
			
			#KeyBoard
			
			self.kb = InlineKeyboardMarkup(row_width=3)
			self.kb.add(InlineKeyboardButton('NCM_UsePretxt: ' + str(BotIO.NCMusePretxt), callback_data='boolNCM'))
			self.kb.row(InlineKeyboardButton('FIT', callback_data='open_fit'), InlineKeyboardButton('RESET', callback_data='open_reset'))
			self.kb.add(InlineKeyboardButton('Close', callback_data='stop'))
			
			#Sending and registring
			
			self.m = await m.reply('Настроечное меню', reply_markup = self.kb)
			await m.delete()
			amolist.append(self)
	
		#Proccess message	
		
	async def proc(self, c):
		
		if self.type == 'settings' and self.data[0]== 0:
			
			if c.data == 'empty':
				logging.debug('AMO: Return null')
				self.data[1] += 1
				if self.data[1]==5:
					logging.info("Lol")
					await c.answer(text='Лол')
				else:
					await c.answer('a')
			
			elif c.data == 'boolNCM':
				if self.s == c.from_user.id:
					logging.debug('AMO: Inverting bool')
					BotIO.NCMusePretxt = -BotIO.NCMusePretxt
					
			#KeyBoardInit
					
					self.kb = InlineKeyboardMarkup(row_width = 3)
					self.kb.add(InlineKeyboardButton('NCM_UsePretxt: ' + str(BotIO.NCMusePretxt), callback_data='boolNCM'))
					self.kb.row(InlineKeyboardButton('FIT', callback_data='open_fit'), InlineKeyboardButton('RESET', callback_data='open_reset'))
					self.kb.add(InlineKeyboardButton('Close', callback_data='stop'))
					
					await self.m.edit_text(self.m.text, reply_markup = self.kb)
					await c.answer('NCMusePretext changed')
				else:
					await c.answer('Изменять эти параметры может лишь тот, кто открыл их')
				
				
				
					
			elif c.data == 'open_fit':
				if c.from_user.id == self.s:
					logging.debug('AMO: Opening fit')
					self.data = [1, 50]
					await self.m.edit_text(self.m.text, reply_markup=kb.keyboard)
					await c.answer('Opened fit menu')
				else:
					await c.answer('Изменять эти параметры может лишь тот, кто открыл их')
				
				
				
			elif c.data == 'open_reset':
				if c.from_user.id == self.s:
					logging.debug('AMO: Opening reset')
					await c.answer('#400: Пошол нахуй', show_alert=True)
#					self.data = ['section: reset', 1024, 1]
#					await self.m.edit_text(self.m.text, reply_markup = kb.keyboard1)
#					await c.answer('Opened reset menu')
				else:
					await c.answer('Изменять эти параметры может лишь тот, кто открыл их')
					
			elif c.data == 'stop':
				if c.from_user.id == self.s:
					logging.debug('AMO: #02 -> Message closed')
					await c.answer('Closed')
					await self.__delete()
				else:
					await c.answer('Изменять эти параметры может лишь тот, кто открыл их')
		
		
		
		
		if self.type == 'settings' and self.data[0] == 1:
			if c.data == 'minus':
				logging.debug('AMO: Proccessing fit menu')
				if c.from_user.id == self.s:
					if self.data[1] == 10:
						await c.answer('Данное число - минимум данной функции')
					else:
						self.data[1] -= 10
						await c.answer()
						await self.m.edit_text(self.m.text, reply_markup=InlineKeyboardMarkup().add(btn2, InlineKeyboardButton(self.data[1], callback_data='empty'), btn4).add(btn5).add(btn6))
						
						
						
			elif c.data == 'plus':
				if c.from_user.id == self.s:
					self.data[1] += 10
					await c.answer()
					await self.m.edit_text(self.m.text, reply_markup=InlineKeyboardMarkup().add(btn2, InlineKeyboardButton(self.data[1], callback_data='empty'), btn4).add(btn5).add(btn6))
				else:
					await c.answer('Изменять эти параметры может лишь тот, кто открыл их')
					
					
					
			elif c.data == 'start':
				if c.from_user.id == self.s:
					await c.answer('Сеть переведена в режим обучения')
					self.data[0] = 0
					await self.m.edit_text(self.m.text, reply_markup = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton('NCM_UsePretxt: ' + str(BotIO.NCMusePretxt), callback_data='boolNCM')).row(InlineKeyboardButton('FIT', callback_data='open_fit'), InlineKeyboardButton('RESET', callback_data='open_reset')).add(InlineKeyboardButton('Close', callback_data='stop')))
					await BotIO.fit(self.m)
					
				else:
					await c.answer('Изменять эти параметры может лишь тот, кто открыл их')
			
			
			
			elif c.data == 'stop':
				if c.from_user.id == self.s:
					logging.debug('AMO: Leaving fit menu')
					self.data[0] = 0
					await c.answer('«Back')
					await self.m.edit_text(self.m.text, reply_markup = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton('NCM_UsePretxt: ' + str(BotIO.NCMusePretxt), callback_data='boolNCM')).row(InlineKeyboardButton('FIT', callback_data='open_fit'), InlineKeyboardButton('RESET', callback_data='open_reset')).add(InlineKeyboardButton('Close', callback_data='stop')))
				else:
					await c.answer('Изменять эти параметры может лишь тот, кто открыл их')
						


	async def closeSession(self):
		for i in amolist:
			r = requests.get("https://api.telegram.org/bot"+token+"/deleteMessage?chat_id="+str(i.m.chat.id)+"&message_id="+str(i.m.message_id))
			if amolist != []:
				await amo.closeSession()



	async def __delete(self):
		await self.m.delete()
		amolist.remove(self)
