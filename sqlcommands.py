import psycopg2
from config import host, user, password, db_name
def register(regname, regbirth, regsex, regdescription, regphoto, telegramid, regfind, regsign, regcity, regagemax, regagemin): #добавление юзера в базу по телеграм айди
    try:
        
        connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name    
    )
        connection.autocommit = True
    
            
        
        with connection.cursor() as cursor:
            cursor.execute(
            """INSERT INTO zodiacusers (name, birth, sex, description, photo, telegramid, find, sign, city, agemax, agemin) VALUES ('""" + regname + """','""" + regbirth + """','""" + regsex + """','""" + regdescription + """','""" + regphoto + """','""" + telegramid + """','""" + regfind + """','""" + regsign + """','""" + regcity + """','""" + regagemax + """','""" + regagemin + """');"""
            )
        answer = ["Успешно", 1]
        print ('connect and ask ok')
   
    except Exception as _ex:
        answer = ["Что-то пошло не так - ", _ex]
        print (_ex)
          
    finally:
        if connection:
         connection.close()
         print("[INFO] PostgreSQL connection closed")
    return answer

def showsqluser (column, value):
    try: 
        connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name    
    )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute("Select * from zodiacusers where " + column + " = '" + value + "';")
            if (cursor.fetchone() != None):
                answer = ["Успешно", cursor.fetchone()]
            else: 
                answer = ["Неуспешно", "Не заполнено"]

        
    except Exception as _ex:
        answer = ["Неуспешно", _ex]
    
    finally:
        if connection:
            connection.close()
    return(answer)

def showsqluservalue (column, userid):
    try: 
        connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name    
    )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute("Select " + column + " from zodiacusers where telegramid = '" + userid + "';")
            answer = str(cursor.fetchone()[0])
            if answer == "None":
                answer = "не заполнено"

        
    except Exception as _ex:
        print(_ex)
        answer = _ex
    
    finally:
        if connection:
            connection.close()     
    return(answer)


def delsqluser (column, value):
    try: 
        connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name    
    )
        connection.autocommit = True
        
        with connection.cursor() as cursor:
            cursor.execute("Delete from zodiacusers where " + column + " = '" + value + "';")
            answer = "Успешно"
            print('удалил')
            
        
    except Exception as _ex:
        answer = "Неуспешно"
        print(_ex)
    
    finally:
        if connection:
            connection.close()
    return(answer)

def updatesqluser (column, value, userid):
    try: 
        connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name    
    )
        connection.autocommit = True
        
        with connection.cursor() as cursor:
            cursor.execute("update zodiacusers set " + column + " = '" + value + "' where telegramid = '"+ userid + "';")
            answer = "Успешно"
            
            
        
    except Exception as _ex:
        answer = "Неуспешно"
        print(_ex)
    
    finally:
        if connection:
            connection.close()
    