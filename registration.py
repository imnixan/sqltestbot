from aiogram.types.photo_size import PhotoSize
import pyowm
from cities import cities_list
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
from datetime import datetime
import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from zsign import zsign




async def registration():
    class Regstate(StatesGroup):
        regnewname = State()
        regnewsex = State()
        regnewfind = State()
        regnewage = State()
        regnewcity = State()
        regnewdescription = State()
        regnewphoto = State()
        regnewbirth = State()
    def botcommands(dp: Dispatcher):
        dp.register_message_handler(regcheckname, state=Regstate.regnewname)
        dp.register_message_handler(regchecksex, state=Regstate.regnewsex)
        dp.register_message_handler(regcheckfind, state=Regstate.regnewfind)
        dp.register_message_handler(regcheckage, state=Regstate.regnewage)
        dp.register_message_handler(regcheckcity, state=Regstate.regnewcity)
        dp.register_message_handler(regcheckdescription, state=Regstate.regnewdescription)
        dp.register_message_handler(regcheckbirth, state=Regstate.regnewbirth)
        dp.register_message_handler(regcheckphoto, content_types = ['text', 'photo'], state=Regstate.regnewphoto)
        
                
    await Regstate.regnewname.set()
        
    async def regcheckname(message: types.Message, state: FSMContext):        
        global regname
        regname = message.text
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ['Мужской', "Женский"]
        keyboard.add(*buttons)
        
        await message.answer("Выбери свой пол", reply_markup=keyboard)
        await Regstate.regnewsex.set()
    
    async def regchecksex(message: types.Message, state: FSMContext):

        if message.text == 'Мужской' or message.text == 'Женский':
            global regsex
            regsex = message.text
            await message.answer("Укажи свою дату рождения в формате ДД.ММ.ГГГГ")
            await Regstate.regnewbirth.set()
    
    async def regcheckbirth (message: types.Message,  state: FSMContext):

        if (re.match('\d\d\.\d\d\.\d\d\d\d', message.text)):
            day = int(message.text.split(".")[0])
            month = int(message.text.split(".")[1])
            year = int(message.text.split(".")[2])
            md = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7:31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
            if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
                md[2] = 29

            if (month < 12 and month > 0) and (year > 1900 and year < datetime.today().year) and (day <= md[month]):

                if ( datetime.today().year - year - ((datetime.today().month, datetime.today().day) < (month, day)) > 16):
                    global regsign, regbirth
                    regsign = zsign(message.text)
                    regbirth = message.text
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    buttons = ['Мужчину', "Женщину"]
                    keyboard.add(*buttons)
                      
                    
                    await message.answer(f"""Твой возраст: {datetime.today().year - year - ((datetime.today().month, datetime.today().day) < (month, day))} лет
    Знак зодиака: {regsign}""", reply_markup=keyboard)
                    await message.answer('Кого будешь искать?')
                    await Regstate.regnewfind.set()

                else: 
                    await message.answer("К сожалению, наш сервис доступен только для лиц старше 16 лет")
                    await State.finish()
            else: 
                await message.answer("Указана несуществующая дата, попробуй еще раз")    
        else:
            await message.answer("""Дата рождения указана некорректно. Пожалуйста, укажи ее в формате дд.мм.гггг 
    Например: 31.12.2001""")

    async def regcheckfind(message: types.Message, state: FSMContext):
    
    
        if message.text == 'Мужчину' or message.text == 'Женщину':
            global regfind
            regfind = message.text
            await message.answer("В каком диапазоне по возрасту будем искать? Укажи в формате минимальный возраст-максимальный возраст, например 18-20")
            await Regstate.regnewage.set()

    async def regcheckage(message: types.Message, state: FSMContext):
        
        agemin = int(re.search("\d\d(?=\-)", message.text).group(0))
        agemax = int(re.search("(?<=\-)\d\d", message.text).group(0))
            
        if (agemin > 16 and agemax > 16 and agemin <= agemax):
    
            global regagemax, regagemin
            regagemax = agemax
            regagemin = agemin       
            await message.answer("В каком городе будем искать?")
            await Regstate.regcheckcity.set()
        else:
            await message.answer("Проверь, что минимальный возраст не больше максимального и больше 16")
    


    async def regcheckcity(message: types.Message, state: FSMContext):
        if message.text.lower() not in cities_list:
            await message.answer("К сожалению, такого города не существует или он находится не в России")
            return
        global regcity
        regcity = message.text
        await message.answer("Расскажи о себе. Это будет описанием твоего профиля для других участников")
        await Regstate.regnewdescription.set()

    async def regcheckdescription(message: types.Message, state: FSMContext):
    
        global regdescription
        regdescription = message.text
        await message.answer("Почти готово. Теперь давай прикрепим к твоему профилю фотографию. Пришли свое фото")
        await Regstate.regnewphoto.set()

    async def regcheckphoto(message: types.Message, state:FSMContext):
   
        if ('photo' in message.content_type):
            global regphoto
            regphoto = message.photo[-1].file_id
               
            answer = sqlcommands.register(regname, regbirth, regsex, regdescription, regphoto, str(message.from_user.id), regfind, regsign, regcity, regagemax, regagemin)
            if answer[0] == "Успешно":
                return "Зарегистрирован"
                
        else:
            await message.answer("Пришли фото")


































    async def main():
        bot = Bot(token=config.token)

        dp = Dispatcher(bot, storage=MemoryStorage())

        logging.basicConfig(level=logging.INFO)

        botcommands(dp)
        await dp.start_polling()
   # asyncio.run(main())   
    