from web3 import HTTPProvider, Web3
from web3.middleware import geth_poa_middleware  # type: ignore
import decimal
import mysql.connector
from mysql.connector import Error
import time
import json
import threading
from threading import Lock
from colorama import Fore, Back, Style
from os import system
import cursor
from Functions import ReservesList, checkUserReserveData, DeleteAAVEUserAccount, calculateFromWei
s_print_lock = Lock()
lock = threading.Lock()
threads = []
AccountInfor = []
AccountHFCount = 0
# web3 = Web3(HTTPProvider('https://polygon-rpc.com/', request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://polygon.llamarpc.com/rpc/01GTP6RCY2TT1JHMMCSDQEMHRE', request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://polygon.blockpi.network/v1/rpc/public', request_kwargs={'timeout': 180}))
web3 = Web3(HTTPProvider('https://polygon.blockpi.network/v1/rpc/35d20c87d2999a6cfd1971aec2edbc4824ed530a', request_kwargs={'timeout': 180}))
contract_address = web3.toChecksumAddress("0x794a61358D6845594F94dc1DB02A252b5b4814aD")
with open("../scripts/AavePoolV3ABI.json") as f:
    ABI = json.load(f)
    ABI = ABI['result']
contract = web3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=ABI)

def getUserInfo(account):
    try:
        UserInfo = contract.functions.getUserAccountData(account).call()
        totalCollateralBase = web3.fromWei(UserInfo[0],'ether') 
        # if(totalCollateralBase<1):
        #     DeleteAAVEUserAccount(account)
        #     return
        totalDebtBase = UserInfo[1]
        currentLiquidationThreshold = UserInfo[3]
        ltv = UserInfo[4]
        UserHF = web3.fromWei(UserInfo[5],'ether')
        UserInfo = [account,UserHF]
        if(UserHF>=1):
            UserInfo = ''
        elif(UserHF>=2):
            UserInfo = ''
            DeleteAAVEUserAccount(account)
        else:
            UserInfo = [account,UserHF]
            
        if(UserInfo!=''):
            global AccountHFCount
            AccountHFCount += 1 
            
            UserReserveData = checkUserReserveData(account)
            for Token in UserReserveData:
                if(Token[2] == True or Token[4]>0):
                    TokenData = ReservesList(Token[0])
                    decimals = TokenData[1]
                    print(TokenData[0],'/',Token[1],'/',Token[4],'/',Token[5],'/',Token[6])
            with s_print_lock:
                print(UserInfo[0],UserInfo[1], totalCollateralBase, (totalDebtBase), currentLiquidationThreshold, ltv)
                print('---------------------------------------------------------')
        return UserInfo
    except Exception as e:
        print('getUserInfo:',e)


def getAaveAccountInfor():
    db_connection = mysql.connector.connect(
    host='127.0.0.1',
    port='3306',
    database='arbfinder',
    user='gamepig',
    password='<@Gamepig1976@>'
    )
    db_cursor = db_connection.cursor(buffered=True)
    sql='SELECT * FROM arbfinder.AAVE_UserAccount'
    db_cursor.execute(sql)
    RecordCount = 0
    AllUserAccount = db_cursor.fetchall()
    rc = db_cursor.rowcount
    db_connection.commit()
    db_cursor.close()
    db_connection.close()
    if(rc <= 0):
        return
    for records in AllUserAccount:  # type: ignore # get data by list
        UserAccount = web3.toChecksumAddress(records[1])
        RecordCount += 1
        UserInfo = threading.Thread(target=getUserInfo, args=[UserAccount])
        UserInfo.start()
        print('Request Send:',RecordCount, end='\r')
        time.sleep(0.025)
    
    return rc
    
while(True):
    system('clear')
    print(time.ctime())
    # print(time.strftime("%H:%M:%S"))
    rc = getAaveAccountInfor()
    print(f"Total Request Send: {rc}")
    print(f"Account for Liquidation: {AccountHFCount}")
    print(time.ctime())
    # print(time.strftime("%H:%M:%S"))
    print('--------------------------------------------------')
    AccountHFCount = 0
    cursor.hide()
    LINE_CLEAR = '\x1b[2K'
    print(end=LINE_CLEAR)
    for i in reversed(range(15)):
        print('Restart in:',(i+1),'sec', end='\r')
        time.sleep(1)
    print(end=LINE_CLEAR)
    print('Starting...', end='\r')