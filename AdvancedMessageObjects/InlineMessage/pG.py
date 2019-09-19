from aiogram.types import \
InlineKeyboardMarkup, InlineKeyboardButton
from warnings import warn

		
def pageGen(arr):
	kb = InlineKeyboardMarkup(row_width=2)
	for i, data in enumerate(arr[1:]):
		if isinstance(data, str) and len(data.split(':')) >= 3:
			trt = data.split(':')
			if trt[0] == 'bool':
				kb.insert(InlineKeyboardButton(trt[1]+": "+str(trt[2]), callback_data="bool:"+trt[1]))
				
			elif trt[0]=='counter':
				kb.row(InlineKeyboardButton('-', callback_data='minus:'+trt[1]+':'+str(trt[3])),InlineKeyboardButton(str(trt[2]), callback_data="null"),InlineKeyboardButton('+', callback_data='add:'+trt[1]+':'+str(trt[3])))
				
			elif trt[0]=='send':
				kb.add(InlineKeyboardButton('Отправить', callback_data='send:'+trt[1]+':'+str(trt[2])))
				
			elif trt[0]=='close':
				kb.add(InlineKeyboardButton('Назад', callback_data='close:'+trt[1]+':'+str(trt[2])))
				
			else:
				warn('Неизвестный тип кнопки: данный компонент был пропущен')
		elif isinstance(data, list):
			kb.add(InlineKeyboardButton(data[0], callback_data='open:'+str(i+1)))
	
	return kb
	
def listGen(arr):
	kb = InlineKeyboardMarkup()
	for i in arr[1:]:
		if i.startswith('https://') or i.startswith('http://') or i.startswith('t.me/'):
			kb.add(InlineKeyboardButton(str(i), url=str(i)))
		else:
			kb.add(InlineKeyboardButton(str(i), callback_data='list'))
			