from datetime import datetime
import re
import sqlcommands
import logging
import config
from config import host, user, password, db_name
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text, IDFilter
import acmd
from datetime import datetime
import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from zsign import zsign







# ловим сообщения
# @dp.message_handler()
# async def messagehandler(message: types.Message):
    
#     if (re.search('shw.usr', message.text) and message.from_user.id == 268026070):
#        result = acmd.showuser(message.text)
#        await message.answer (f"""Пользователь найден:
#         Имя - {result[0]}
#         Дата рождения - {result[1]}
#         Пол - {result[2]}
#         Ищет - {result[6]}
#         Описание - {result[3]}
#         Telegram Id - {result[5]}
#         {result[4]}""")
        
#     elif (re.search('del.usr', message.text) and message.from_user.id == 268026070):
#        await message.answer(acmd.deluser(message.text))

#первый запуск
# @dp.message_handler(commands="start")
# async def cmd_test1(message: types.Message):
#     answer = newtablenote('telegramid', str(message.from_user.id))
#     if (answer[0] == "Успешно"):
#         await  message.answer ("Приветствую!")
#         keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         buttons = ["Моя Анкета"]
#         keyboard.add(*buttons)
#         await message.answer("Чем займемся?", reply_markup=keyboard)

#     else:
#         await  message.answer ("С возвращением!")
#         keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         buttons = ["Моя Анкета", "Мэтчи"]
#         keyboard.add(*buttons)
#         await message.answer("Чем займемся?", reply_markup=keyboard)

class BotState(StatesGroup):
    waiting_for_birth = State()
    logged = State()

def botcommands(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands = "start", state ="*")
    dp.register_message_handler(cmd_start, Text(equals="начать", ignore_case=True), state ="*")
    dp.register_message_handler(datebirth, state=BotState.waiting_for_birth)

#Блок с функциями
#Когда тыкаешь начать
async def cmd_start(message: types.Message):
    checkuser = sqlcommands.showsqluser("telegramid", str(message.from_user.id))
    if (checkuser[0] == "Успешно"):
        await message.answer("Вновь привет!")
        await BotState.logged.set() 
    else:
        await message.answer("Приветствую! Укажи свою дату рождения в формате ДД.ММ.ГГГГ")
        await BotState.waiting_for_birth.set()
#Проверка введенной даты возраста
async def datebirth(message: types.Message,  state: FSMContext):
    if (re.match('\d\d\.\d\d\.\d\d\d\d', message.text)):
        day = int(message.text.split(".")[0])
        month = int(message.text.split(".")[1])
        year = int(message.text.split(".")[2])
        md = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7:31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
        if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
            md[2] = 29

        if (month < 12 and month > 0) and (year > 1900 and year < datetime.today().year) and (day <= md[month]):

            if ( datetime.today().year - year - ((datetime.today().month, datetime.today().day) < (month, day)) > 16):
                sqlcommands.register(str(message.from_user.id), message.text)
                await message.answer("вы успешно зарегистрированы")
            else: 
                await message.answer("К сожалению, наш сервис доступен только для лиц старше 16 лет")
                await state.finish()
        else: 
            await message.answer("Указана несуществующая дата, попробуй еще раз")    
    else:
        await message.answer("""Дата рождения указана некорректно. Пожалуйста, укажи ее в формате дд.мм.гггг 
Например: 31.12.2001""")   
    
async def main():
    bot = Bot(token=config.token)

    dp = Dispatcher(bot, storage=MemoryStorage())

    logging.basicConfig(level=logging.INFO)

    botcommands(dp)
    await dp.start_polling()
asyncio.run(main())    