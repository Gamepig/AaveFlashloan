import json
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from datetime import date
import time
from os import system

def ReadErrorLog(date):
    db_connection = mysql.connector.connect(
            host='127.0.0.1',
            port='3306',
            database='arbfinder',
            user='gamepig',
            password='<@Gamepig1976@>'
        )
    ErrLog = []
    result = []
    db_cursor = db_connection.cursor()
    sqlstr = f"SELECT * FROM arbfinder.ErrorLog WHERE datetime > {date};"
    db_cursor.execute(sqlstr)
    # db_cursor.callproc('get_accounts')
    
    # for result in db_cursor.stored_results():
    #     print(result.fetchall())
    for records in db_cursor:  # type: ignore # get data by list
        id = records[0]
        time = records[1]
        type = records[2]
        ErrMSG = records[3]
        result = {'id': id, 'DATETIME': time, 'type': type, 'ErrMSG': ErrMSG}
        ErrLog.append(result)
    db_connection.commit()
    db_cursor.close()
    db_connection.close()

    return ErrLog


while(True):
    today = date.today()
    ErrorLog = ReadErrorLog(today)

    for v in ErrorLog:
        print('--------------------------------------------------------')
        print(v['DATETIME'], v['type'], v['ErrMSG'])
    
    print('--------------------------------------------------------')
    print(f"last Update: {datetime.now()}")
    time.sleep(30)
    system('clear')