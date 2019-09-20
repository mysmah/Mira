from aiogram.types import \
InlineKeyboardMarkup, InlineKeyboardButton

one = InlineKeyboardMarkup()
one.add(InlineKeyboardButton('Кноп(очка)', callback_data = 'response'))

choose = InlineKeyboardMarkup()
choose.add(InlineKeyboardButton('Принять', callback_data='accept'), InlineKeyboardButton('Отклонить', callback_data='decline'))