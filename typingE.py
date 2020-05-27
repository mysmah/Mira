import asyncio


async def typing(text, message, answer = False):
    length = len(text)
    #await asyncio.sleep(0.3)
    while length > 26:
        #await message.chat.do('typing')
        length -=26
        #await asyncio.sleep(5)
    #await message.chat.do('typing')
    #await asyncio.sleep(0.18*length)
    if answer:
        return await message.answer(text)
    else:
        return await message.reply(text)
       
async def leave(message):
    await typing('Оу', message, answer=True)
    await asyncio.sleep(2.5)
    await typing('Ну чтож...', message, answer=True)
    await asyncio.sleep(1.5)
    await typing('Прощайте.', message, answer=True)
    await asyncio.sleep(0.3)
    await message.chat.leave()
