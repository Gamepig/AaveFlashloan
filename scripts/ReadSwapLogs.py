import psutil
# from web3.auto import w3
from web3 import Web3, HTTPProvider
import json
from os import system
import datetime
import time
import colorama
from colorama import Fore, Back, Style
import traceback
import sys
import gc
import threading
from Functions import checkWMATICbalance, checkUSDCbalance
import cursor
system('clear')
cursor.hide()
web3 = Web3(HTTPProvider('https://polygon-rpc.com/',request_kwargs={'timeout': 180}))

def ReadSwapLogs():
    Today = (datetime.datetime.now()+datetime.timedelta(days=0)).strftime("%y/%m/%d")
    DateBefor = (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%y/%m/%d")
    monthly = (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%y/%m")
    TokenPairs = {}
    TokenPairsProfit = {}
    TokenPairCount = []
    monthlyTokenPairs ={}
    monthlyTokenPairsProfit = {}
    monthlyTokenPairCount = []
    profit = 0
    GasFee = 0
    with open("SwapLog.json", "r") as file:
        data = json.load(file)
    ProfitDayBefor = 0
    ProfitMonthly = 0
    TotalCount = 0
    MonthlyCount = 0
    # Count_1inch = 0
    # Count_0xAPI = 0
    # Count_1inch_0x = 0
    # Count_0x_1inch = 0
    # Count_TrianSwap_1inch = 0
    # Count_TrianSwap_1inch = 0
    # Count_TrianSwap_0x = 0
    # profit1 = 0
    # profit2 = 0
    # profit3 = 0
    # profit4 = 0
    # profit5 = 0
    # profit6 = 0
    Count_USDC = 0
    Count_USDT = 0
    Count_DAI = 0
    Count_WETH = 0
    # Count_WMATIC_WETH_DAI = 0
    # USDT_profit = 0
    USDC_profit = 0
    # DAI_profit = 0
    WETH_profit = 0
    # WMATIC_WETH_DAI_profit = 0
    # Date = datetime.datetime.now().strftime('%Y%m%d')
    # Date = '20211025'
    LastQuote = ''
    Profit_USD = 0
    MATIC_Price = 0
    profit_USD = 0
    ProfitMonthly_USD = 0
    ArbSucceed = 0
    ArbFail = 0
    SucceedAmount = 0
    FailAmount = 0
    if(len(data)>0):
        TokenPairID = 0
        monthlyTokenPairID = 0
        for i in range(len(data)) :
            if(float(data[i]['Profit'])>=1):
                eventdate = data[i]['Time'][0:8]
                eventMonth = data[i]['Time'][0:5]
                TokenOut = data[i]['Pair'].split('/')
                # TokenPair = (f'{TokenOut[0]}/{TokenOut[1]}')
                TokenPair = data[i]['Pair']
                Profit = data[i]['Profit']
                
                if "Profit_USD" in data[i]:
                    Profit_USD = data[i]['Profit_USD']
                if "MATIC_Price" in data[i]:
                    MATIC_Price = data[i]['MATIC_Price']
                # if(TokenOut[0] == 'USDC'):
                #     Profit = round(float(Profit) * float(MATIC_Price),2)
                    
                if(eventMonth == monthly):
                    ProfitMonthly += float(Profit)
                    ProfitMonthly_USD += float(Profit_USD)
                    if(TokenPair in monthlyTokenPairs):
                        monthlyTokenPairs[TokenPair] += 1
                        monthlyTokenPairsProfit[TokenPair] += float(Profit)
                    else:
                        monthlyTokenPairs[TokenPair] = 1
                        monthlyTokenPairsProfit[TokenPair] = float(Profit)
                        
                    MonthlyCount += 1
                    
                if(eventdate == Today):
                    if(TokenPair in TokenPairs):
                        TokenPairs[TokenPair] += 1
                        TokenPairsProfit[TokenPair] += float(Profit)
                    else:
                        TokenPairs[TokenPair] = 1
                        TokenPairsProfit[TokenPair] = float(Profit)
                    
                    profit += float(Profit)
                    profit_USD += float(Profit_USD)
                    Expected_Return = float(data[i]['Expected_Return'])
                    GasFee += float(data[i]['GasMatic'])
                    TotalCount += 1
                    if(data[i]['SwapStatus']=='1'):
                        ArbSucceed += 1
                        SucceedAmount += float(Profit)
                        ArbSts = Fore.LIGHTGREEN_EX + 'Succeed' + Style.RESET_ALL
                    else:
                        ArbFail += 1
                        FailAmount += float(Profit)
                        ArbSts = Fore.RED + 'Fail' + Style.RESET_ALL
                    # if(TokenOut[1] == 'USDC'):
                    #     Count_USDC += 1
                    #     USDC_profit += float(data[i]['Profit'])
                    # elif(TokenOut[1] == 'WETH'):
                    #     Count_WETH += 1
                    #     WETH_profit += float(data[i]['Profit'])
                    if(i >= (len(data)-20)):
                        # GasMatic = round(float(data[i]['GasMatic']), 6)
                        GasMatic = float(data[i]['GasMatic'])
                        # LastQuote = (Fore.CYAN + data[i]['Time'][9:20], data[i]['DEX'].ljust(10) + Style.RESET_ALL, TokenPair.ljust(11), str(int(Expected_Return)).ljust(5), data[i]['Cost'].ljust(5), Fore.GREEN + data[i]['Profit'].ljust(6) + Style.RESET_ALL, GasMatic, data[i]['GasWei'])
                        print(Fore.CYAN + data[i]['Time'][9:20], data[i]['DEX'].ljust(10) + Style.RESET_ALL, TokenPair.ljust(11),
                              str(int(Expected_Return)).ljust(6), data[i]['Cost'].ljust(6), Fore.GREEN + str(Profit).ljust(8) + Style.RESET_ALL, str(round(web3.fromWei(GasMatic,'ether'),3)).ljust(5), data[i]['GasWei'], ArbSts)
                if(eventdate == DateBefor):
                    ProfitDayBefor += float(Profit)
                
    
            
            
            
            # eventid = data[i].get('eventid')
            # eventdate = eventid[0:8]
            # eventMonth = eventid[0:6]
            
            # if(eventMonth == monthly):
            #     ProfitMonthly += data[i].get('profit')
            
            # if(eventdate == Date):
            #     TotalCount += 1
            #     dex = data[i].get('DEX')
            #     if(dex == '1inch_0x'):
            #         Count_1inch_0x += 1
            #         profit1 += data[i].get('profit')
            #     elif(dex == '0x_1inch'):
            #         Count_0x_1inch += 1
            #         profit2 += data[i].get('profit')
            #     elif(dex == 'TrianSwap_1inch_Sushi'):
            #         Count_TrianSwap_1inch += 1
            #         profit3 += data[i].get('profit')
            #     elif(dex == 'TrianSwap_0x_Sushi'):
            #         Count_TrianSwap_0x += 1
            #         profit4 += data[i].get('profit')
            #     elif(dex == '1inch'):
            #         Count_1inch += 1
            #         profit5 += data[i].get('profit')
            #     elif(dex == '0x'):
            #         Count_0xAPI += 1
            #         profit6 += data[i].get('profit')
                    
            #     Token = data[i].get('TokenPair')
            #     if(Token[1]=='USDT'):
            #         Count_USDT += 1
            #         USDT_profit += data[i].get('profit')
            #     elif(Token[1]=='USDC'):
            #         Count_USDC += 1
            #         USDC_profit += data[i].get('profit')
            #     elif(Token[1]=='DAI'):
            #         Count_DAI += 1
            #         DAI_profit += data[i].get('profit')
            #     elif(Token[1]=='WETH'):
            #         Count_WETH += 1
            #         WETH_profit += data[i].get('profit')
            #     elif(data[i].get('TokenPair') == 'WMATIC/WETH/DAI'):
            #         Count_WMATIC_WETH_DAI += 1
            #         WMATIC_WETH_DAI_profit += data[i].get('profit')
            # elif(eventdate == DateBefor):
            #     ProfitDayBefor += data[i].get('profit')
        
    # ProfitMonthly = format((ProfitMonthly), ",")
    # ProfitDayBefor = format(ProfitDayBefor, ",")
    # print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  {monthly}  :{ProfitMonthly}  / {DateBefor}  :{ProfitDayBefor}")
    # print('-------------------------------------------------------')
    # print(f'1inch_0xAPI : {Count_1inch_0x}')
    # print(f'profit : {format(profit1, ",")} ')
    # print('-------------------------------------------------------')
    # print(f'0xAPI_1inch : {Count_0x_1inch}')
    # print(f'profit : {format(profit2, ",")} ')
    # print('-------------------------------------------------------')
    # print(f'1inch : {Count_1inch}')
    # print(f'profit : {format(profit5, ",")} ')
    # print('-------------------------------------------------------')
    # print(f'0xAPI : {Count_0xAPI}')
    # print(f'profit : {format(profit6, ",")} ')
    # print('-------------------------------------------------------')
    # print(f'TrianSwap_1inch_Sushi : {Count_TrianSwap_1inch}' )
    # print(f'profit : {format(profit3, ",")} ')
    # print('-------------------------------------------------------')
    # print(f'TrianSwap_0x_Sushi : {Count_TrianSwap_0x}' )
    # print(f'profit : {format(profit4, ",")} ')
    # print('-------------------------------------------------------')
    # print(f'USDT : {Count_USDT} / Profit: {format(USDT_profit, ",")}')
    # print(f'USDC : {Count_USDC} / Profit: {format(USDC_profit, ",")}')
    # print(f'DAI  : {Count_DAI} / Profit: {format(DAI_profit, ",")}')
    # print(f'WETH : {Count_WETH} / Profit: {format(WETH_profit, ",")}')
    # print(f'T_Arb: {Count_WMATIC_WETH_DAI} / Profit: {format(WMATIC_WETH_DAI_profit, ",")}')
    # print(f'Total: {TotalCount}')
    # print(f'profit: {format((profit1 + profit2 + profit3 + profit4 + profit5 + profit6),",")} ')
    AveGasCost = 0
    TimeNow = datetime.datetime.now().strftime('%y/%m/%d %H:%M.%S')
    if(TotalCount != 0):
        AveGasCost = GasFee / TotalCount
        AveGasCost = web3.fromWei(AveGasCost,'ether')
        GasFee = web3.fromWei(GasFee, 'ether')
    print('-------------------------------------------------------')
    print(f'{TimeNow}')
    print(f'TotalCount: {TotalCount} , ArbSucceed: {ArbSucceed}, ArbFail: {ArbFail}')
    print(f'{Fore.GREEN + format(int(profit),",") + Style.RESET_ALL}(MATIC)   Succeed Amount:{Fore.GREEN + format(SucceedAmount,",") + Style.RESET_ALL}(MATIC)')
    print(f'{Fore.GREEN + format(int(profit_USD),",") + Style.RESET_ALL}(USD) ≈ {Fore.YELLOW + format(int(int(profit_USD) * 30.9),",") + Style.RESET_ALL}(TWD)')
        
    print('-------------------------------------------------------')
    print(f'GasFee: {format(round(GasFee,2),",")} / AveGasCost: {format(round(AveGasCost,2),",")}')
    print('-------------------------------------------------------')
    TokenPairsProfit = sorted(TokenPairsProfit.items(), key=lambda kv: kv[1], reverse = True)
    for key in TokenPairsProfit:
        print(str(key[0]).ljust(11), ':', str(TokenPairs[key[0]]).ljust(5), ':', format(int(key[1]),','))
    print('-------------------------------------------------------')
    print(f'{monthly}: {MonthlyCount} - {Fore.MAGENTA + format(int(ProfitMonthly),",") + Style.RESET_ALL}(MATIC) {format(int(ProfitMonthly_USD),",")}(USD)')
    print(f'{DateBefor}: {Fore.YELLOW + format(int(ProfitDayBefor),",") + Style.RESET_ALL}(MATIC)')
    
    monthlyTokenPairsProfit = sorted(monthlyTokenPairsProfit.items(), key=lambda kv: kv[1], reverse = True)
    for key in monthlyTokenPairsProfit:
        print(str(key[0]).ljust(11),':', str(monthlyTokenPairs[key[0]]).ljust(5), ':', format(int(key[1]),','),'(MATIC)')
    
    print('-------------------------------------------------------')
    # account0 = web3.toChecksumAddress('0x85D6EceC4F3cD8AE8DF22dcE8437085B4C2A1E4a')
    # account1 = web3.toChecksumAddress('0x9794B41450701c36E6a9d162F9a3e8D09FD62E6E')
    # MATIC0 =  round(web3.fromWei(web3.eth.getBalance(account0), 'ether'),6)
    # MATIC1 =  round(web3.fromWei(web3.eth.getBalance(account1), 'ether'),6)
    # # USDC0 = round(checkUSDCbalance(account0)/1e6, 6)
    # # USDC1 = round(checkUSDCbalance(account1)/1e6, 6)
    # # WMATIC0 = round(web3.fromWei(checkWMATICbalance(account0),'ether'),6)
    # # WMATIC1 = round(web3.fromWei(checkWMATICbalance(account1),'ether'),6)
    # print(f'Account 0 - MATIC: {MATIC0}')
    # print(f'Account 1 - MATIC: {MATIC1}')
    # # print(f'Account 0 - MATIC: {MATIC0} / WMATIC: {WMATIC0} / USDC: {USDC0}')
    # # print(f'Account 1 - MATIC: {MATIC1} / WMATIC: {WMATIC1} / USDC: {USDC1}')
    # print('-------------------------------------------------------')
    
while(True):
    # gc.collect()
    system('clear')
    # pendingTX = web3.eth.filter('pending')
    # print(pendingTX)
    try:
        ReadSwapLogs()
    except Exception as e:
        print('ERROR')
        error_class = e.__class__.__name__  # 取得錯誤類型
        detail = e.args[0]  # 取得詳細內容
        cl, exc, tb = sys.exc_info()  # 取得Call Stack
        lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
        fileName = lastCallStack[0]  # 取得發生的檔案名稱
        lineNum = lastCallStack[1]  # 取得發生的行號
        funcName = lastCallStack[2]  # 取得發生的函數名稱
        errMsg = f"line {lineNum}, {funcName}: [{error_class}] {detail}"
        print(errMsg)
    time.sleep(12)
#check Script running
    # pythons_psutil = []
    # for p in psutil.process_iter():
    #     try:
    #         if p.name() == 'Python':
    #             pythons_psutil.append(p)
    #     except psutil.Error:
    #         pass
        
    # print(*sorted(pythons_psutil[0].as_dict()), sep='\n')
    # print(pythons_psutil[0].exe())
    # for i in range(len(pythons_psutil)):
    #     Process = pythons_psutil[i]
    #     if(Process.name() == 'Python'):
    #         print(Proces
