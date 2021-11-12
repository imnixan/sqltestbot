import re
from sqlcommands import newtablenote, delsqluser, showsqluser
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
    if (answer[1] == "Успешно"):
        await  message.answer ("Пользователь успешно зарегистрирован")
    else:
        if (re.search('Ключ ".*" уже существует', str(answer[1]))):
            await  message.answer ("Вы уже были зарегистрированы")




executor.start_polling(dp, skip_updates=True)