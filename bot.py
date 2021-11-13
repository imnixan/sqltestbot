import re
from sqlcommands import newtablenote, showsqluser
import logging
import config
from config import host, user, password, db_name
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


bot = Bot(token=config.token)

dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


# запуск бота
@dp.message_handler(commands="start")
async def cmd_test1(message: types.Message):
    answer = newtablenote('telegramid', str(message.from_user.id))
    if (answer[0] == "Успешно"):
        await  message.answer ("Пользователь успешно зарегистрирован")
    else:
        if (re.search('Ключ ".*" уже существует', str(answer[1]))):
            await  message.answer ("Вы уже были зарегистрированы")



#вывод пользователя
@dp.message_handler()
async def showuser(message: types.Message):
    
    if (re.search('shw.usr', message.text) and message.from_user.id == 268026070):
        answer = showsqluser(re.search('(?<=shw\.usr ).*(?=\.)', str(message.text)).group(0),re.search('(?<=\w\.)(\w|\d)+$', str(message.text)).group(0))
        if (answer[0] == "Успешно"):
            print (answer)
            await  message.answer ("Пользователь найден: " + str(answer[1]))
       

executor.start_polling(dp, skip_updates=True)