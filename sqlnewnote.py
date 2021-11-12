import psycopg2
from config import host, user, password, db_name
def newtablenote(column, value):
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
            """INSERT INTO testbase (""" + column + """) VALUES
            (""" + "'" + value +"'" + """);"""
            )
        answer = ["Успешно", "0"]
        
      
   
    except Exception as _ex:
        answer = ["Ошибка", _ex]
          
    finally:
        if connection:
         cursor.close()
         print("[INFO] PostgreSQL connection closed")
    return answer
    #penis