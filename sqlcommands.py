import psycopg2
from config import host, user, password, db_name
def newtablenote(column, value): #добавление записи в юзера
    print("добавляю запись")
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
            """INSERT INTO testbase (""" + column + """) VALUES ('""" + value + """');"""
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
            cursor.execute("Select name, birth, sex, description, photo, find from testbase where " + column + " = '" + value + "';")
            answer = ["Успешно", cursor.fetchone()]
            print (cursor.fetchone())
        
    except Exception as _ex:
        answer = ["Неуспешно", _ex]
    
    finally:
        if connection:
            connection.close()
    return(answer)
