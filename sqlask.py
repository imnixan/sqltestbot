import psycopg2
from config import host, user, password, db_name


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
            """CREATE TABLE testbase(
                id serial PRIMARY KEY,
                name varchar(50) NOT NULL,
                sex varchar(50) NOT NULL);"""
        )
        

except Exception as _ex:
    print ("Nihuya sebe", _ex)
finally:
    if connection:
        connection.close()
        print ("bb")