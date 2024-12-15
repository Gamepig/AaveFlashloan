from web3 import HTTPProvider, Web3
import json
from decimal import Decimal
import time
import threading
from threading import Lock
from os import system
from colorama import Fore, Back, Style
import cursor
from Functions import getUserAccountData, getAaveAccounts, DeleteAAVEUserAccount

s_print_lock = Lock()
lock = threading.Lock()
Thread_list = []
AccountOver = 0
AccountUnder = 0
UserHFCount = 0
UserHFOver2 = 0
AccountRemain = 0
TotalHFCount = 0
NoDebt = 0
# web3 = Web3(HTTPProvider('https://polygon-rpc.com/', request_kwargs={'timeout': 180}))
web3 = Web3(HTTPProvider('https://polygon.blockpi.network/v1/rpc/35d20c87d2999a6cfd1971aec2edbc4824ed530a', request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://polygon.llamarpc.com/rpc/01GTP6RCY2TT1JHMMCSDQEMHRE', request_kwargs={'timeout': 180}))

def playsound():
    system('afplay /Users/vichuang/Music/音效/ding-idea-40142.mp3')

def UserAccountData(UserAccount):
    UserInfo = getUserAccountData(UserAccount)
    if(UserInfo[1]<=0):
        global NoDebt
        NoDebt += 1
        DeleteAAVEUserAccount(UserAccount)
        return
    totalCollateral = UserInfo[0] / 10 ** 8
    totalDebtBase = UserInfo[1]
    UserHF = web3.fromWei(UserInfo[5],'ether')
    if(totalCollateral<1000):
        global AccountUnder
        AccountUnder += 1
        DeleteAAVEUserAccount(UserAccount)
        return
    if(UserHF > 2):
        global UserHFOver2
        UserHFOver2 += 1
        DeleteAAVEUserAccount(UserAccount)
        return
        
    totalCollateralBase = '{:,.2f}'.format(UserInfo[0] / 10 ** 8)
    totalDebtBase = '{:,.2f}'.format(UserInfo[1] / 10 ** 8)
    currentLiquidationThreshold = UserInfo[3]
    ltv = UserInfo[4]
    
    # if(totalCollateral >= 100):
    global AccountOver
    AccountOver += 1
    if(UserHF<1):
        playsound()
        global UserHFCount
        UserHFCount += 1
        global TotalHFCount
        TotalHFCount += 1
        print(f"{Fore.RED + UserAccount + Style.RESET_ALL}")
        print((UserInfo))
        print((f"{totalCollateralBase} / {totalDebtBase} / {currentLiquidationThreshold} / {ltv} / {UserHF}"))
        print('------------------------------------------------------')
        # with s_print_lock:

while(True):
    # system('clear')
    cursor.hide()
    # print(time.ctime())
    print(time.strftime("%H:%M:%S"))
    RecordCount = 0
    Accounts = getAaveAccounts()
    for records in Accounts:  # type: ignore # get data by list
        UserAccount = str(records[1])
        UserInfo = threading.Thread(target=UserAccountData, args=[UserAccount])
        UserInfo.start()
        Thread_list.append(UserInfo)
        RecordCount += 1
        print('Request Send:',RecordCount, end='\r')
        time.sleep(0.025)
    for i in Thread_list:
        i.join()
    print(f"")
    print(f"UserHFCount: {UserHFCount}")
    print(f"UserHFOver2: {UserHFOver2}")
    print(f"NoDebt: {NoDebt}")
    print(f"Collateral Over 1000: {AccountOver} / Under: {AccountUnder}")
    print(f"TotalHFCount: {TotalHFCount}")
    print(time.strftime("%H:%M:%S"))
    print('----------------------------------------------------------------------------')
    AccountOver = 0
    AccountUnder = 0
    UserHFCount = 0
    UserHFOver2 = 0
    NoDebt = 0
    cursor.hide()
    LINE_CLEAR = '\x1b[2K'
    print(end=LINE_CLEAR)
    for i in reversed(range(30)):
        print('Restart in:',(i+1),'sec', end='\r')
        time.sleep(1)
    print(end=LINE_CLEAR)
    print('Starting...', end='\r')
    print(end=LINE_CLEAR)