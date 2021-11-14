from datetime import datetime

dateofbirth= "28.02.2015"
day = int(dateofbirth.split(".")[0])
month = int(dateofbirth.split(".")[1])
year = int(dateofbirth.split(".")[2])


def datebirth(day, month, year):
    md = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7:31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        md[2] = 29
    
    if (month > 12 or month < 0):
        return False
    if year < 1900 or year > datetime.today().year:
        return False
    if day > md[month]:
        return False
    return True



def calculate_age(day,month,year):
    today = datetime.today()
    if (today.year - year - ((today.month, today.day) < (month, day)) > 16):
        print( today.year - year - ((today.month, today.day) < (month, day)))
        return True
    return False

def controlcheck(day, month, year):
    md = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7:31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        md[2] = 29
    if (month < 12 and month > 0) and (year > 1900 and year < datetime.today().year) and (day <= md[month]) and (datetime.today().year - year - ((datetime.today().month, datetime.today().day) < (month, day)) > 16):
        return True
    else: 
        return False




print (f"Проверка возраста :{calculate_age(day, month, year)}\nПроверка даты: {datebirth(day, month, year)}")
print (f"Общая проверка: {controlcheck(day,month,year)}")