import re
import config
import psycopg2
column = 'telegramid'
value = '268026070'
try:
        
    connection = psycopg2.connect(
    host=config.host,
    user=config.user,
    password=config.password,
    database=config.db_name    
    )
    connection.autocommit = True
             
        
    with connection.cursor() as cursor:
        cursor.execute(
        """SELECT * FROM testbase ;"""# WHERE """ + column + """ = '""" + value + """'"""
        )
        answer = ["Успешно", cursor.fetchone()]
        print ('connect and ask ok')
     
        print(cursor.fetchone())
        
except Exception as _ex:
    answer = ["Что-то пошло не так - ", _ex]
    print (_ex)
          
finally:
    if connection:
        cursor.close()
        print("[INFO] PostgreSQL connection closed")
    