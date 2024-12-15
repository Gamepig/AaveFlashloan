import mysql.connector
from mysql.connector import Error

def getUserAccountRowCount():
    db_connection = mysql.connector.connect(
    host='127.0.0.1',
    port='3306',
    database='arbfinder',
    user='gamepig',
    password='<@Gamepig1976@>'
    )
    db_cursor = db_connection.cursor(buffered=True)
    sql = "SELECT * FROM AAVE_UserAccount"
    db_cursor.execute(sql)
    rc = db_cursor.rowcount
    db_connection.commit()
    db_cursor.close()
    db_connection.close()
    return rc
    
print(getUserAccountRowCount())