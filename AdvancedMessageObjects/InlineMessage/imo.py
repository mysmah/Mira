import logging
from . import kb
import requests
from .pG import pageGen, listGen
from aiogram.types import \
InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from warnings import warn
from project_misc import token
import pickle

objects=[]


async def summon(model, bot, type, msg, locked = False, pdata = None, calledby = None):
	logging.debug('New imo object')
	await Module(model, bot).init(type, locked, pdata, calledby, msg)

async def prc(c, bot, pdata = None):
	logging.debug('Processing imo object')
	for i in objects:
		if i.msg.message_id == c.message.message_id:
			return await i.process(c, pdata)




class Module:
	types = ('list', 'funct', 'choose', 'one', 'settings')
	
	def __init__(self, model, bot):
		self.model = model
		self.bot = bot
		self.pdata = None
		self.senderid = None
		self.calledby = None
		self.locked = False
		objects.append(self)
	
	async def init(self, type, locked, pdata, calledby, msg):
		if type in Module.types:
			self.type = type
		else:
			raise TypeError('Такого типа нет')
			
		if locked and msg == None:
			raise ValueError('Если сообщение заблокировано, то обьект types.Message из хандлера обязателен')
		else:
			self.locked = locked
			self.senderid = msg.from_user.id
		
		self.calledby = calledby
		self.pdata = pdata
		self.msg = await self.__register(msg,pdata)
	
	
	
	async def __register(self, m, pdata):
		
		if self.type == 'one':
			if isinstance(pdata, list):
				return await m.reply(pdata[0], reply_markup=kb.one)
			else:
				return await m.reply('Type of One', reply_markup=kb.one)
				
		elif self.type == 'settings':
			self.section = 0
			await m.delete()
			if isinstance(pdata, list) and len(pdata) >= 2:
				return await self.bot.send_message(m.chat.id, str(pdata[0]), reply_markup = pageGen(pdata))
			else:
				raise ValueError('Тип "funct" требует 2 или больше аргументов ')
				
		elif self.type == 'list':
			if isinstance(pdata, list) and len(pdata) > 2:
				return await m.reply(str(pdata[0]), reply_markup=listGen(pdata))
			else:
				raise ValueError('Тип "list" требует 2 или более аргументов')
		
		elif self.type == 'choose':
			if isinstance(pdata, list):
				return await self.bot.send_message(pdata[1], pdata[0], reply_markup=kb.choose)
				
	async def process(self, c, bot, pdata):
		self.bot = bot
		if self.locked == True:
			if self.senderid == c.from_user.id:
				return await self.__proc(c, pdata)
			else:
				await c.answer('#400: Ошибка доступа')
		else:
			return await self.__proc(c, pdata)
				

	async def __proc(self, c, pdata):
		if self.type == 'one' and c.data == 'respone':
			await c.answer('Нажато')
			await self.msg.edit_text(self.msg.text)
			self.__unload()
			return 'onepress'
			
		elif self.type == 'list' and c.data == 'list':
			await c.answer()
			return 'list stimulation'
			
		elif self.type == 'choose':
			if c.data == 'accept':
				await c.answer('>> Принято')
				await self.msg.edit_text(self.msg.text)
				self.__unload()
				return 'accepted'
			elif c.data == 'decline':
				await c.answer('>> Отклонено')
				await self.msg.edit_text(self.msg.text)
				self.__unload()
				return 'declined'
				
		elif self.type == 'funct':
			self.offset = []
			if c.data.startswith('bool:'):
				await c.answer('>> Изменено')
				if self.offset != []:
					pass
					
		elif self.type == 'settings':
			if c.data.startswith('open:') and self.section == 0:
				if c.data == 'open:2':
					self.counter = 50
					self.section = 2
					await self.__updatePage(self.pdata[2])
					await c.answer('>> Открыт раздел FIT')
				elif c.data == 'open:1':
					self.section = 1
					await self.__updatePage(self.pdata[1])
					await c.answer('>> Открыт раздел с свитчами')
				elif c.data == 'open:3':
					self.neurod = 1024
					self.layers = 1
					self.section = 3
					await self.__updatePage(self.pdata[3])
					await c.answer('>> Открыт раздел RESET')
				else:
					await c.answer('>> Неизвестный коллбэк')
				return 'settings:open'
			elif c.data.startswith('open:') and self.section != 0:
				await c.answer('#228: Неизвестная ошебка(номер хуй)', show_alert=True)
				return 'err:null:open'
				
			elif self.section != 0 and c.data.startswith('close:'):
				await c.answer('>> Назад')
				self.section = 0
				await self.__updatePage(self.pdata)
				return 'sections:back'
			
			elif self.section == 0 and c.data == 'close:null:0':
				await c.answer('>> Настройки закрыты')
				await self.msg.delete()
				self.__unload()
				return 'settings:closed'
			
			elif self.section == 1 and c.data.startswith('bool:'):
				for i, e in enumerate(self.pdata[self.section]):
					if e.startswith(c.data):
						par = e.split(':')
						if int(par[2]) == 0:
							par[2] = 1
						elif int(par[2]) == 1:
							par[2] = 0
						self.pdata[self.section][i]=':'.join(map(str,par))
						boolc = ':'.join(map(str,par))
				await c.answer('>> Значение изменено')
				await self.__updatePage(self.pdata[self.section])
				return ['bool:changed', self.pdata, boolc]
			
			elif self.section == 2 and c.data.startswith('minus:'):
				if self.counter <= 100:
					if self.counter == 10:
						await c.answer('>> Счетчик FIT не может принять нулевое значение')
						return 'err:counter'
					else:
						self.counter -= 10
						await c.answer('>> Операция вычитания')
						self.pdata[self.section][1] = 'counter:fit:'+str(self.counter)+':0'
						await self.__updatePage(self.pdata[self.section])
						return 'fit:minus'
				else:
					self.counter -=50
					await c.answer('>> Операция вычитания')
					self.pdata[self.section][1] = 'counter:fit:'+str(self.counter)+':0'
					await self.__updatePage(self.pdata[self.section])
					return 'fit:minus'
			elif self.section == 2 and c.data.startswith('add:'):
				if self.counter >= 100:
					self.counter +=50
					await c.answer('>> Операция сложения')
					self.pdata[self.section][1] = 'counter:fit:'+str(self.counter)+':0'
					await self.__updatePage(self.pdata[self.section])
					return 'fit:plus'
				else:
					self.counter +=10
					await c.answer('>> Операция сложения')
					self.pdata[self.section][1] = 'counter:fit:'+str(self.counter)+':0'
					await self.__updatePage(self.pdata[self.section])
					return 'fit:plus'
			elif self.section == 2 and c.data.startswith('send:'):
				self.section = 0
				await c.answer('#200: Сеть переведена в режим обучения', show_alert=True)
				await self.bot.send_message('@catgirl_channel', "Бот переведен в режим обучения")
				await self.__updatePage(self.pdata)
				self.model.fit(self.counter)
				return 'fit:fited'
			elif self.section == 2 and c.data == 'null':
				await c.answer()
				return None
				
			elif self.section == 3 and c.data.startswith('minus:neurod:'):
				if self.neurod == 512:
					await c.answer('>> Счетчик Neurod не может принять нулевое значение')
					return 'err:counter'
				else:
					self.neurod -= 512
					await c.answer('>> Операция вычитания')
					self.pdata[self.section][1] = 'counter:neurod:'+str(self.neurod)+':0'
					await self.__updatePage(self.pdata[self.section])
					return 'reset:neurod:minus'
					
			elif self.section == 3 and c.data.startswith('minus:layers:'):
				if self.layers == 1:
					await c.answer('>> Счетчик Layers не может принять нулевое значение')
					return 'err:counter'
				else:
					self.layers -= 1
					await c.answer('>> Операция вычитания')
					self.pdata[self.section][2] = 'counter:layers:'+str(self.layers)+':0'
					await self.__updatePage(self.pdata[self.section])
					return 'reset:layers:minus'
			
			elif self.section == 3 and c.data.startswith('add:neurod:'):
				self.neurod += 512
				await c.answer('>> Операция сложения')
				self.pdata[self.section][1] = 'counter:neurod:'+str(self.neurod)+':0'
				await self.__updatePage(self.pdata[self.section])
				return 'reset:neurod:add'
			elif self.section == 3 and c.data.startswith('add:layers:'):
				self.layers += 1
				await c.answer('>> Операция сложения')
				self.pdata[self.section][2] = 'counter:layers:'+str(self.layers)+':0'
				await self.__updatePage(self.pdata[self.section])
				return 'reset:layers:add'
			
			elif self.section == 3 and c.data.startswith('send:'):
				self.section = 0
				await c.answer('#200: Нейросеть была сброшена', show_alert=True)
				reseted = []
				inter = 0
				while inter <= self.layers:
					reseted.append(self.neurod)
					inter += 1
				self.model.new_model(reseted)
				await self.__updatePage(self.pdata)
				return ['reset:reseted', reseted]
				
						
	def __unload(self):
		objects.remove(self)
		del self
					
					
		
		
	async def __updatePage(self, pdata):
		if isinstance(pdata, list) and len(pdata)>=2:
			try:
				if self.msg.text:
					self.msg = await self.msg.edit_text(self.msg.text, reply_markup=pageGen(pdata))
				elif self.msg.caption:
					await self.msg.edit_caption(self.msg.caption, reply_markup=pageGen(pdata))
				return True
			except Exception:
				return False
				
	def sleep(self):
		if self.type == 'settings':
			r.requests.get('https://api.telegram.org/bot'+token+'/messageDelete?chat_id='+self.msg.chat.id+'&message_id='+self.msg.message_id)
			return None
		r = requests.get('https://api.telegram.org/bot'+token+'/editMessageText?chat_id='+str(self.msg.chat.id)+'&message_id='+str(self.msg.message_id)+'&text=%D0%92%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%B9%20%D0%BC%D0%BE%D0%BC%D0%B5%D0%BD%D1%82%20%D0%B1%D0%BE%D1%82%20%D0%BE%D1%82%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD%2C%20%D0%BA%D0%BD%D0%BE%D0%BF%D0%BA%D0%B8%20%D0%BD%D0%B5%20%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%D1%8E%D1%82')
		with open('runtime.bytes', 'wb') as save:
			self.bot =None
			pickle.dump(self, save, -1)
	async def run(self):
		await self.msg.edit_text(self.msg.text, reply_markup=self.msg.reply_markup)
		
		
		
async def shtdw():
	with open('runtime.bytes', 'wb') as save:
		for i in objects:
			print(type(i))
			i.sleep()

async def initof():
	with open('runtime.bytes', 'rb') as save:
		while True:
			try:
				loaded = pickle.load(save)
				await loaded.run()
				print(loaded)
				objects.append(loaded)
				
			except Exception:
				return None


