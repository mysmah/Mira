# PREPROCESS MODULE
# version 0.0.2
_WATCH_LIST = None
_ME = None
_DB = None
_CUR = None


import logging
import random
import sqlite3

def init(ids, wlist):
	global _WATCH_LIST, _ME, _DB, _CUR
	logging.info('preproc: Initializating module')
	_WATCH_LIST = wlist
	_ME = ids
	_DB = sqlite3.connect(':memory:')
	_CUR = _DB.cursor()
	_CUR.execute('CREATE TABLE short_mem (question text, answer text)')
	_DB.commit()

	logging.info('preproc: Done')
async def process_m(message):
	message.text = message.text.lower()
	if message.reply_to_message and message.reply_to_message.from_user.id == _ME.id:
		if message.from_user.id in _WATCH_LIST and random.randint(0,1) == 0:
			_CUR.execute('INSERT INTO short_mem VALUES (?,?)', (message.reply_to_message.text.lower(), message.text))
			_DB.commit()
		return 1
	else:
		if message.chat.id > 0:
			return 0
		else:
			if message.text.startswith('мира,') or message.text.startswith('mira,') or message.text.startswith('мира ') or message.text.startswith('mira '):
				return 1
			elif _ME.username in message.text:
				return 1
			elif ', мира,' in message.text or ' mira ' in message.text or message.text[-6:] == ', мира' or message.text[-5:] == ' mira':
				return 1
			else:
				if random.randint(0,250) == 0:
					return 0

def update(wlist):
	global _WATCH_LIST
_WATCH_LIST = wlist

def close():
	#Write new dialogs to dialog.txt

	#Get all new dialogs in format question, answer
	_CUR.execute("SELECT question FROM short_mem")
	q_list = _CUR.fetchall()
	_CUR.execute("SELECT answer FROM short_mem")
	a_list = _CUR.fetchall()

	#CRAETING NEW STRING
	result = []
	for n, v in enumerate(q_list):
		v1 = a_list[n]

		#copy finder cycle
		for n1, v2 in enumerate(q_list):
			if n1 != n and v2[0] == v[0] and v1[0] == a_list[n1][0]:
				q_list.pop(n)
				q_list.pop(n1)

		#VALUE to STRING
		result.append('\n' + v[0].replace('\n','⇄') + '\n' + a_list[n][0].replace('\n', ' '))

	#test for matchs in dialog.txt
	with open('dialog.txt','r') as f:
		file = f.read()
		for i, i1 in enumerate(result):
			if i1 in file:
				result.pop(i)
	#Save to dialog.txt
	with open('dialog.txt', 'a') as f:
		ap_text = ''
		for i in result:
			ap_text += i
		f.write(ap_text)
	_DB.close()
	_CUR = None
	_DB = None

	return 0
