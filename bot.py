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
import acmd
from datetime import datetime
import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from zsign import zsign


class BotState(StatesGroup):
    waiting_for_birth = State()
    logged = State()
    edit_profile = State()
    newname = State()
    newsex = State()
    newfind = State()
    newage = State()
    newcity = State()
    newdescription = State()
    newphoto = State()
    newbirth = State()
    registrationcheck = State()
    regname = State()
    regsex = State()
    regfind = State()
    regcity = State()

def botcommands(dp: Dispatcher):
    dp.register_message_handler(cancel, Text(equals="отмена", ignore_case=True), state=BotState.newphoto)
    dp.register_message_handler(cancel, Text(equals="отмена", ignore_case=True), state=BotState.newname)
    dp.register_message_handler(cancel, Text(equals="отмена", ignore_case=True), state=BotState.newsex)
    dp.register_message_handler(cancel, Text(equals="отмена", ignore_case=True), state=BotState.newfind)
    dp.register_message_handler(cancel, Text(equals="отмена", ignore_case=True), state=BotState.newage)
    dp.register_message_handler(cancel, Text(equals="отмена", ignore_case=True), state=BotState.newcity)
    dp.register_message_handler(cancel, Text(equals="отмена", ignore_case=True), state=BotState.newdescription)
    dp.register_message_handler(cancel, Text(equals="отмена", ignore_case=True), state=BotState.newbirth)
    dp.register_message_handler(datebirth, state=BotState.waiting_for_birth)
    dp.register_message_handler(editbirth, Text(equals="дата рождения", ignore_case=True), state=BotState.edit_profile)
    dp.register_message_handler(editname, Text(equals="имя", ignore_case=True), state=BotState.edit_profile)
    dp.register_message_handler(editsex, Text(equals="пол", ignore_case=True), state=BotState.edit_profile)
    dp.register_message_handler(editfind, Text(equals="кого я ищу", ignore_case=True), state=BotState.edit_profile)
    dp.register_message_handler(editage, Text(equals="возраст поиска", ignore_case=True), state=BotState.edit_profile)
    dp.register_message_handler(editcity, Text(equals="город поиска", ignore_case=True), state=BotState.edit_profile)
    dp.register_message_handler(editdescription, Text(equals="подпись", ignore_case=True), state=BotState.edit_profile)
    dp.register_message_handler(editphoto, Text(equals="фото", ignore_case=True), state=BotState.edit_profile)
    dp.register_message_handler(checkname, state=BotState.newname)
    dp.register_message_handler(checksex, state=BotState.newsex)
    dp.register_message_handler(checkfind, state=BotState.newfind)
    dp.register_message_handler(checkage, state=BotState.newage)
    dp.register_message_handler(checkcity, state=BotState.newcity)

    dp.register_message_handler(checkname, state=BotState.regname)
    dp.register_message_handler(checksex, state=BotState.regsex)
    dp.register_message_handler(checkfind, state=BotState.regfind)
    dp.register_message_handler(checkcity, state=BotState.regcity)

    dp.register_message_handler(checkdescription, state=BotState.newdescription)
    dp.register_message_handler(checkbirth, state=BotState.newbirth)
    dp.register_message_handler(checkphoto, content_types = ['text', 'photo'], state=BotState.newphoto)
    dp.register_message_handler(myprofile, Text(equals="показать мой профиль", ignore_case=True), state=BotState.edit_profile)
    dp.register_message_handler(myprofile, Text(equals="моя анкета", ignore_case=True), state=BotState.logged)
    dp.register_message_handler(cmd_start,  state ="*")
 
    



#Блок с функциями



async def editphoto(message: types.Message,  state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = "Отмена"
    keyboard.add(back)
    if sqlcommands.showsqluservalue('photo', str(message.from_user.id)) == "не заполнено":
        await message.answer("У тебя еще не загружено фото. Можешь прислать его сейчас",reply_markup=keyboard)
        
    else:
        await message.answer(f"""Твое текущее фото:""", reply_markup=keyboard)
        await message.answer_photo(sqlcommands.showsqluservalue('photo', str(message.from_user.id)))
    await BotState.newphoto.set()


async def checkphoto(message: types.Message, state:FSMContext):
   
    if ('photo' in message.content_type):
        print ('пользователь прислал фото')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Имя", "Дата рождения","Пол", "Кого я ищу", "Возраст поиска", "Город поиска", "Подпись", "Фото"]
        keyboard.add(*buttons)
        back = "На главную"
        keyboard.add(back)
        sqlcommands.updatesqluser('photo', message.photo[-1].file_id, str(message.from_user.id))
        await message.answer(f"Твое новое фото:", reply_markup=keyboard)
        await message.answer_photo(sqlcommands.showsqluservalue('photo', str(message.from_user.id)))
        await BotState.edit_profile.set()
    else:
        await message.answer("Пришли фото")

#Изменить описание
async def editdescription(message: types.Message,  state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = "Отмена"
    keyboard.add(back)
    await message.answer(f"""Текущее описание: {sqlcommands.showsqluservalue('description', str(message.from_user.id))}
Укажи новое описание""", reply_markup=keyboard)
    await BotState.newdescription.set()
#проверка и сохранение описания
async def checkdescription(message: types.Message, state: FSMContext):
    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Имя", "Дата рождения","Пол", "Кого я ищу", "Возраст поиска", "Город поиска", "Подпись", "Фото"]
    keyboard.add(*buttons)
    back = "На главную"
    keyboard.add(back)
    sqlcommands.updatesqluser('description', message.text, str(message.from_user.id))
    await message.answer(f"Твое новое описание: {message.text}", reply_markup=keyboard)
    await BotState.edit_profile.set()

#редактирование города
async def editcity(message: types.Message,  state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = "Отмена"
    keyboard.add(back)
    await message.answer(f"""Текущий город поиска: {sqlcommands.showsqluservalue('city', str(message.from_user.id))}
Укажи новый город для поиска""", reply_markup=keyboard)
    await BotState.newcity.set()
#проверка и сохранение города
async def checkcity(message: types.Message, state: FSMContext):
    if message.text.lower() not in cities_list:
        await message.answer("К сожалению, такого города не существует или он находится не в России")
        return
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Имя", "Дата рождения","Пол", "Кого я ищу", "Возраст поиска", "Город поиска", "Подпись", "Фото"]
    keyboard.add(*buttons)
    back = "На главную"
    keyboard.add(back)
    sqlcommands.updatesqluser('city', message.text.lower(), str(message.from_user.id))
    await message.answer(f"Твой новый город для поиска: {message.text.lower()}", reply_markup=keyboard)
    await BotState.edit_profile.set()
#редактирование диапазона возраста
async def editage(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = "Отмена"
    keyboard.add(back)
    await message.answer(f"""Твой диапазон поиска по возрасту: {sqlcommands.showsqluservalue('agemin', str(message.from_user.id))} - {sqlcommands.showsqluservalue('agemax', str(message.from_user.id))}
Укажи новое значение в формате:
минимальный возраст - максимальный возраст""", reply_markup=keyboard)
    await BotState.newage.set()
#проверка и сохранение диапазона возраста
async def checkage(message: types.Message, state: FSMContext):
    
    agemin = int(re.search("\d\d(?=\-)", message.text).group(0))
    agemax = int(re.search("(?<=\-)\d\d", message.text).group(0))
        
    if (agemin > 16 and agemax > 16 and agemin <= agemax):
 
        sqlcommands.updatesqluser('agemin', str(agemin), str(message.from_user.id))

        sqlcommands.updatesqluser('agemax', str(agemax), str(message.from_user.id))
 
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Имя", "Дата рождения","Пол", "Кого я ищу", "Возраст поиска", "Город поиска", "Подпись", "Фото"]
        keyboard.add(*buttons)
        back = "На главную"
        keyboard.add(back)
        await message.answer(f"""Твой диапазон поиска по возрасту: {agemin} - {agemax}""", reply_markup=keyboard)
        await BotState.edit_profile.set()
    else:
        await message.answer("Проверь, что минимальный возраст не больше максимального и больше 16")

#редактирование пола поиска 
async def editfind(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = "Отмена"
    buttons = ['Мужчину', "Женщину"]
    keyboard.add(*buttons)
    keyboard.add(back)
    await message.answer(f"""Ищешь: {sqlcommands.showsqluservalue('find', str(message.from_user.id))}
Укажи новое значение""", reply_markup=keyboard)
    await BotState.newfind.set()
#проверк и сохранение пола поиска
async def checkfind(message: types.Message, state: FSMContext):
    
 
    if message.text == 'Мужчину' or message.text == 'Женщину':
        sqlcommands.updatesqluser('find', message.text.lower(), str(message.from_user.id))
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Имя", "Дата рождения","Пол", "Кого я ищу", "Возраст поиска", "Город поиска", "Подпись", "Фото"]
        keyboard.add(*buttons)
        back = "На главную"
        keyboard.add(back)
        await message.answer(f"Будем искать для тебя {message.text.lower()}", reply_markup=keyboard)
        await BotState.edit_profile.set()

#редактирование пола
async def editsex(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = "Отмена"
    buttons = ['Мужской', "Женский"]
    keyboard.add(*buttons)
    keyboard.add(back)
    await message.answer(f"""Указанный тобой пол: {sqlcommands.showsqluservalue('sex', str(message.from_user.id))}
Укажи новое значение""", reply_markup=keyboard)
    await BotState.newsex.set()
#проверка и сохранение пола
async def checksex(message: types.Message, state: FSMContext):

    if message.text == 'Мужской' or message.text == 'Женский':
        sqlcommands.updatesqluser('sex', message.text.lower(), str(message.from_user.id))
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Имя", "Дата рождения","Пол", "Кого я ищу", "Возраст поиска", "Город поиска", "Подпись", "Фото"]
        keyboard.add(*buttons)
        back = "На главную"
        keyboard.add(back)
        await message.answer(f"Указанный тобой пол: {message.text.lower()}", reply_markup=keyboard)
        await BotState.edit_profile.set()
#редактирование имени
async def editname(message: types.Message,  state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = "Отмена"
    keyboard.add(back)
    await message.answer(f"""Текущее имя: {sqlcommands.showsqluservalue('name', str(message.from_user.id))}
Укажи новое имя""", reply_markup=keyboard)
    await BotState.newname.set()
#првоерка и сохранение имени
async def checkname(message: types.Message, state: FSMContext):
    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Имя", "Дата рождения","Пол", "Кого я ищу", "Возраст поиска", "Город поиска", "Подпись", "Фото"]
    keyboard.add(*buttons)
    back = "На главную"
    keyboard.add(back)
    sqlcommands.updatesqluser('name', message.text, str(message.from_user.id))
    await message.answer(f"Твое новое имя: {message.text}", reply_markup=keyboard)
    await BotState.edit_profile.set()

# async def blockmenu (state, textmessage, userid):
#     pass



#Когда тыкаешь начать
async def cmd_start(message: types.Message,  state: FSMContext):
    current_state = await state.get_state()
    if current_state is None or message.text.lower()=="на главную":
        checkuser = sqlcommands.showsqluser("telegramid", str(message.from_user.id))
        if (checkuser[0] == "Успешно"):
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = "Моя анкета"
            keyboard.add(back)
            await message.answer("Главная страница", reply_markup=keyboard)
            await BotState.logged.set() 
        else:
            await message.answer("Приветствую! Укажи свою дату рождения в формате ДД.ММ.ГГГГ", reply_markup=types.ReplyKeyboardRemove())
            await BotState.waiting_for_birth.set()
    else:
        return
async def cancel(message:types.Message, state:FSMContext):
    await BotState.edit_profile.set()
    await myprofile(message, FSMContext)
    return

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
                sign = zsign(message.text)
                sqlcommands.register(str(message.from_user.id), message.text, sign)
                
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                buttons = ["Пол", "Кого я ищу", "Возраст поиска", "Город поиска", "Подпись", "Фото"]
                keyboard.add(*buttons)
                profile = "Моя анкета"
                back = "На главную"
                keyboard.add(profile)
                keyboard.add(back)
                await message.answer(f"""Отлично.
Твой возраст: {datetime.today().year - year - ((datetime.today().month, datetime.today().day) < (month, day))} лет
Твой знак зодиака: {sign}
Перейдем к заполнению анкеты?""", reply_markup=keyboard)
                
                await BotState.edit_profile.set()

            else: 
                await message.answer("К сожалению, наш сервис доступен только для лиц старше 16 лет")
                await state.finish()
        else: 
            await message.answer("Указана несуществующая дата, попробуй еще раз")    
    else:
        await message.answer("""Дата рождения указана некорректно. Пожалуйста, укажи ее в формате дд.мм.гггг 
Например: 31.12.2001""")   

async def myprofile(message: types.Message,  state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Имя", "Дата рождения","Пол", "Кого я ищу", "Возраст поиска", "Город поиска", "Подпись", "Фото"]
    keyboard.add(*buttons)
    backbuttons = ["На главную", "Показать мой профиль"]
    keyboard.add(*backbuttons)
    if sqlcommands.showsqluservalue('photo', str(message.from_user.id)) == "не заполнено":

        await message.answer(f""" Фото отсутствует
Имя: {sqlcommands.showsqluservalue('name', str(message.from_user.id))}
Дата рождения: {sqlcommands.showsqluservalue('birth', str(message.from_user.id))}
Пол: {sqlcommands.showsqluservalue('sex', str(message.from_user.id))}
Знак зодиака: {sqlcommands.showsqluservalue('sign', str(message.from_user.id))}
Кого я ищу: {sqlcommands.showsqluservalue('find', str(message.from_user.id))}
Возраст поиска: {sqlcommands.showsqluservalue('agemin', str(message.from_user.id))} - {sqlcommands.showsqluservalue('agemax', str(message.from_user.id))}
Город: {sqlcommands.showsqluservalue('city', str(message.from_user.id))}
Подпись: {sqlcommands.showsqluservalue('description', str(message.from_user.id))}""", reply_markup=keyboard)
        await BotState.edit_profile.set()
    else:
        await BotState.edit_profile.set()
        await message.answer("Твоя анкета:", reply_markup=keyboard)
        await message.answer_photo(caption = f"""Имя: {sqlcommands.showsqluservalue('name', str(message.from_user.id))}
Дата рождения: {sqlcommands.showsqluservalue('birth', str(message.from_user.id))}
Пол: {sqlcommands.showsqluservalue('sex', str(message.from_user.id))}
Знак зодиака: {sqlcommands.showsqluservalue('sign', str(message.from_user.id))}
Кого я ищу: {sqlcommands.showsqluservalue('find', str(message.from_user.id))}
Возраст поиска: {sqlcommands.showsqluservalue('agemin', str(message.from_user.id))} - {sqlcommands.showsqluservalue('agemax', str(message.from_user.id))}
Город: {sqlcommands.showsqluservalue('city', str(message.from_user.id))}
Подпись: {sqlcommands.showsqluservalue('description', str(message.from_user.id))}""", photo = sqlcommands.showsqluservalue('photo', str(message.from_user.id)))

#редактирование даты рождения
async def editbirth(message: types.Message,  state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = "Отмена"
    keyboard.add(back)
    await message.answer(f"""Текущая дата рождения: {sqlcommands.showsqluservalue('birth', str(message.from_user.id))}
Укажи новую дату рождения в формате ДД.ММ.ГГГГ""", reply_markup=keyboard)
    await BotState.newbirth.set()
    


#проверка и сохранение даты рождения
async def checkbirth (message: types.Message,  state: FSMContext):

    if (re.match('\d\d\.\d\d\.\d\d\d\d', message.text)):
        day = int(message.text.split(".")[0])
        month = int(message.text.split(".")[1])
        year = int(message.text.split(".")[2])
        md = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7:31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
        if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
            md[2] = 29

        if (month < 12 and month > 0) and (year > 1900 and year < datetime.today().year) and (day <= md[month]):

            if ( datetime.today().year - year - ((datetime.today().month, datetime.today().day) < (month, day)) > 16):
                sign = zsign(message.text)
                sqlcommands.updatesqluser('birth', message.text, str(message.from_user.id))
                sqlcommands.updatesqluser('sign', sign, str(message.from_user.id))
                    
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                buttons = ["Имя", "Дата рождения","Пол", "Кого я ищу", "Возраст поиска", "Город поиска", "Подпись", "Фото"]
                keyboard.add(*buttons)
                back = "На главную"
                keyboard.add(back)
                await message.answer(f"""Твой обновленный возраст: {datetime.today().year - year - ((datetime.today().month, datetime.today().day) < (month, day))} лет
Твой обновленный знак зодиака: {sign}""", reply_markup=keyboard)
                await BotState.edit_profile.set()

            else: 
                await message.answer("К сожалению, наш сервис доступен только для лиц старше 16 лет")
                await State.finish()
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