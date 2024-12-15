from Functions import getAccounts, getAccount
import json
from web3 import HTTPProvider, Web3
import mysql.connector
from mysql.connector import Error
import threading
from threading import Lock
from time import sleep

lock = threading.Lock()
Accounts = []

web3 = Web3(HTTPProvider('http://localhost:8545',request_kwargs={'timeout': 180}))
accounts = getAccounts()
print(accounts[0][0]['account'])
for account in accounts[0]:
    print(account['id'])
# try:
#     db_connection = mysql.connector.connect(
#         host='127.0.0.1',
#         port='3306',
#         database='arbfinder',
#         user='gamepig',
#         password='<@Gamepig1976@>'
#     )
# except Error as e:
#     print("資料庫連接失敗：", e)

# while(True):
    
#     sleep(3)
#     accountList = getAccounts()
#     Accounts = accountList[0]
