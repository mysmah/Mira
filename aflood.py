import asyncio
import time

from aiogram import *
from aiogram.types import Chat

userDict = {}

class AntiFlood:
	limits = 20
	
	async def everysecond(self):
		while True:
			for i in userDict:
				if userDict[i].banned <= time.time():
					userDict[i].banned = 0
			await asyncio.sleep(1)
	async def everyminute(self):
		while True:
			for i in userDict:
				userDict[i].sex = 0
			await asyncio.sleep(60)
			
	def check(self,message):
		if message.from_user.id not in userDict.keys():
			user = message.from_user
			user.sex = 0
			user.banned = 0
			user.warn = 0
			userDict.update({user.id: user})
			return 0
		if userDict[message.from_user.id].banned > 0:
			return 1
		userDict[message.from_user.id].sex += 1
		if userDict[message.from_user.id].sex > AntiFlood.limits and userDict[message.from_user.id].warn <= 2:
			userDict[message.from_user.id].banned = time.time()+1800.0
			userDict[message.from_user.id].warn += 1
			return 2
		elif userDict[message.from_user.id].sex > AntiFlood.limits and userDict[message.from_user.id].warn > 2:
			userDict[message.from_user.id].banned = time.time()+99999999.9
			userDict[message.from_user.id].warn = 0
			return 3
		else:
			return 0
		
	
	def __init__(self, event_loop):
		self.event_loop = event_loop
		event_loop.create_task(self.everysecond())
		event_loop.create_task(self.everyminute())
