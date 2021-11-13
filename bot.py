import re
from sqlcommands import newtablenote, showsqluser, delsqluser
import logging
import config
from config import host, user, password, db_name
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


bot = Bot(token=config.token)

dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


#первый запуск
@dp.message_handler(commands="/start")
async def cmd_test1(message: types.Message):
    answer = newtablenote('telegramid', str(message.from_user.id))
    if (answer[0] == "Успешно"):
        await  message.answer ("Пользователь успешно зарегистрирован")
    else:
        if (re.search('Ключ ".*" уже существует', str(answer[1]))):
            await  message.answer ("Вы уже были зарегистрированы")



#ловим сообщения
@dp.message_handler()
async def messagehandler(message: types.Message):
    
    if (re.search('shw.usr', message.text) and message.from_user.id == 268026070):
        print("функция выполняется")
        answer = showsqluser(re.search('(?<=\.usr ).*(?=\()', str(message.text)).group(0), re.search('(?<=\().*(?=\))', str(message.text)).group(0))
        if (answer[0] == "Успешно"):
            await  message.answer (f"""Пользователь найден:
            Имя - {answer[1][0]}
            Дата рождения - {answer[1][1]}
            Пол - {answer[1][2]}
            Ищет - {answer[1][6]}
            Описание - {answer[1][3]}
            Telegram Id - {answer[1][5]}
            {answer[1][4]}"""
            )
            if (answer[1][4] == None):
                print ('фотки нет')
    
    elif (re.search('del.usr', message.text) and message.from_user.id == 268026070):
        print("функция выполняется")
        answer = delsqluser(re.search('(?<=\.usr ).*(?=\()', str(message.text)).group(0), re.search('(?<=\().*(?=\))', str(message.text)).group(0))
        if (answer == "Успешно"):
            await  message.answer ("Пользователь удален")
            
executor.start_polling(dp, skip_updates=True)