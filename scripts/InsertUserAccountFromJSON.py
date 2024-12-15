import json
import mysql.connector
# from Functions import Insert_aave_UserAccount
with open("AAVE_UserAccount.json", "r") as file:
     data = json.load(file)

db_connection = mysql.connector.connect(
host='127.0.0.1',
port='3306',
database='arbfinder',
user='gamepig',
password='<@Gamepig1976@>'
)

for account in data:
    db_cursor = db_connection.cursor()
    # sql = "call arbfinder.Insert_AAVE_UserAccount('"+str(account['account'])+"')"
    sql = "SELECT EXISTS(SELECT * FROM arbfinder.AAVE_UserAccount WHERE account='"+account['account']+"')"
    db_cursor.execute(sql)
    for records in db_cursor:  # type: ignore # get data by list
        if(records[0]==0):
            db_cursor2 = db_connection.cursor()
            sql = "INSERT  INTO arbfinder.AAVE_UserAccount (account) VALUES ('"+account['account']+"')"
            db_cursor2.execute(sql)
            db_connection.commit()
            print(f"Insert {account['account']}")

db_cursor.close()

# Insert_aave_UserAccount(account['account'])


db_connection.close()


