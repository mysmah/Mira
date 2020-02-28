# PREPROCESS MODULE
# version 0.0.1
_WATCH_LIST = None
_ME = None


import logging
import random

def init(ids, wlist):
	global _WATCH_LIST, _ME
	logging.info('preproc: Initializating module')
	_WATCH_LIST = wlist
	_ID = ids
	logging.info('preproc: Done')
async def process_m(message):
	message.text = message.text.lower()
	if message.reply_to_message and message.reply_to_message.from_user.id == _ME.id:
		if message.from_user.id in _WATCH_LIST and random.randint(0,1) == 0:
			with open('dialog.txt', 'a') as f:
				f.write('\n{}\n{}'.format(message.reply_to_message.text.lower().replace('\n', ' '), message.text.replace('\n',' ')))
				logging.info('preproc: added replica: \n{}\n{}'.format(message.reply_to_message.text.lower().replace('\n', ' '), message.text.replace('\n',' ')))
		return 1
	else:
		if message.chat.id > 0:
			return 0
		else:
			if message.text.startswith('мира,') or message.startswith('mira,'):
				return 1
			elif _ME.username in message.text:
				return 1
			elif ', мира,' in message.text or ' mira ' in message.text or message.text[-6:] == ', мира' or message.text[-5:] == ' mira':
				return 1
			else:
				if random.randint(0,250) == 0:
					return 0


