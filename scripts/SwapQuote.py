from time import sleep
from tokenize import Token
from web3 import HTTPProvider, Web3
import requests
from os import system
import json
import datetime
import os
import traceback
import sys
import time
import decimal
import threading
from threading import Lock
import colorama
from colorama import Fore, Back, Style
from uuid import uuid4
import gc
from web3.contract import ConciseContract
from web3.auto import w3
from Functions import getContractAddress, TokenAddress, getPrivate_Key, getAccount, getAccounts, upDateAccountSts, UpdateAccountBalance, checkWMATICbalance, checkUSDCbalance, UnWrappWmatic, QuickSwap, upDateAccountSts1, ErrorLog, getAssetsPricesAaveOracleV3
from AaveFlashloan import AaveFlashloan
import cursor
from eth_abi.packed import encode_single_packed
from web3.middleware import geth_poa_middleware
# system('clear')
s_print_lock = Lock()
lock = threading.Lock()
Accounts = []
SwapSend = 0
block_Nimber = ''
        
# web3 = Web3(HTTPProvider('https://polygon.blockpi.network/v1/rpc/public', request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://poly-rpc.gateway.pokt.network', request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://polygon-mainnet.blastapi.io/fa940a80-11dc-43e6-b0dc-03d6607ddece', request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://poly-mainnet.gateway.pokt.network/v1/lb/fb2da9793f63bcbc71fd8f0c', request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://rpc.ankr.com/polygon/3056719186807a83c61564283e4bdaec7300a35ff09d2a24dc5696c1186597b3', request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://polygon.blockpi.network/v1/rpc/35d20c87d2999a6cfd1971aec2edbc4824ed530a', request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://polygon.llamarpc.com/rpc/01GTP6RCY2TT1JHMMCSDQEMHRE', request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://rpc-mainnet.maticvigil.com/v1/00bd90aa475e05b2176fcde27f1a57075c948422', request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://polygon-bor.publicnode.com', request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://polygon-mainnet.rpcfast.com?api_key=Olw3BXk1TpyW1SI0K86gTfVKB8FpZRVNNoveVkYti5n7S7tgvPjg9FKxs6fsXwzM', request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://polygon-mainnet.g.alchemy.com/v2/JOGYiBYYVqQJUCF1UsNqcPWNhJixWaLO', request_kwargs={'timeout': 240}))
# web3 = Web3(HTTPProvider('https://polygon-rpc.com/', request_kwargs={'timeout': 240}))
web3 = Web3(HTTPProvider('http://127.0.0.1:8545/',request_kwargs={'timeout': 180}))

web3.middleware_onion.inject(geth_poa_middleware, layer=0)

try:
    if(web3.isConnected() == False):
        print(Fore.RED + 'Network Not connected' + Style.RESET_ALL)
        sleep(5)
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
    else:
        print('Network connected')
except Exception as e :
    ErrorLog('web3_Connect',e)
    sleep(5)
    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
    
Uniswap_Quoter = '0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6'
SushiRouter = '0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506'
QuickSwap_Router = '0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff'
ApeSwap_Router = '0xC0788A3aD43d79aa53B09c2EaCc313A787d1d607'

wmatic = web3.toChecksumAddress('0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270')

with open("Uniswap_QuoterABI.json") as f:
    info_json = json.load(f)
Uniswap_QuoterABI = info_json["result"]

with open("Quickswap_QuoterABI.json") as f:
    info_json = json.load(f)
Quickswap_QuoterABI = info_json["result"]

with open("SushiSwapRouterABI.json") as f:
    info_json = json.load(f)
SushiSwap_RouterABI = info_json["result"]

with open("ApeSwap_RouterABI.json") as f:
    info_json = json.load(f)
ApeSwap_RouterABI = info_json["result"]

Uniswap_Quotercontract_address = web3.toChecksumAddress(Uniswap_Quoter)
Uniswap_QuoterContract = web3.eth.contract(address=Uniswap_Quotercontract_address, abi=Uniswap_QuoterABI)

QuickRoutercontract_address = web3.toChecksumAddress(QuickSwap_Router)
QuickRouterContract = web3.eth.contract(address=QuickRoutercontract_address, abi=Quickswap_QuoterABI)

SushiRouterContract_address = web3.toChecksumAddress(SushiRouter)
SushiRouterContract = web3.eth.contract(address=SushiRouterContract_address, abi=SushiSwap_RouterABI)

ApeSwap_Routercontract_address = web3.toChecksumAddress(ApeSwap_Router)
ApeSwap_RouterContract = web3.eth.contract(address=ApeSwap_Routercontract_address, abi=ApeSwap_RouterABI)
print('----------------------------------------------')

# Amounts = {10000,25000,50000,100000,250000}
# Amounts = {25000,50000,100000,250000,500000}
# Amounts = {1000,2500,5000,10000,25000,50000}
Amounts = {5000,10000,25000,50000,100000}

TokenIn = {'WMATIC', 'USDC'}
# TokensOut = {'WMATIC', 'USDC'}
TokensOut = {'WMATIC', 'WBTC', 'USDC','WETH'}
# TokensOut = {'WMATIC', 'USDC', 'WETH'}
QRecords = []
threads = []
LastQuoteInfor = ''
FlashLoanFee = 1.0009


def StratFlahloan(Token_in, Token_out, amount, DEX, gasPriceCount, eventid):
    try:
        if(len(Accounts)<=0):
            return 'NoAccountForSwap'
        tx_hash = ''
        lock.acquire()
        accountInfor = getAccount(Accounts)
        upDateAccountSts(accountInfor[0], 1, eventid)
        lock.release()
        account = web3.toChecksumAddress(accountInfor[0])
        private_key = accountInfor[1]
        _tokenIn = web3.toChecksumAddress(TokenAddress(Token_in))
        _tokenOut = web3.toChecksumAddress(TokenAddress(Token_out))
        tx_hash = AaveFlashloan(Token_in, _tokenIn, _tokenOut, amount,
                                gasPriceCount[3], DEX, account, private_key, eventid)
        # AaveFlashloanTH = threading.Thread(target=AaveFlashloan, args=[
        #                                    Token_in, _tokenIn, _tokenOut, amount, gasPriceCount[3], DEX, account, private_key])
        # AaveFlashloanTH.start()
        return tx_hash
    except Exception as e:
        upDateAccountSts(accountInfor[0], 0, eventid)
        # playsound_Error()
        Error_Log = str(e)
        ErrorLog('StratFlahloan',Error_Log)
        print(e)

def QuoteAllDEX(amount, tokenin, tokenout):
    try:
        path = encode_single_packed("(address,uint24,address)", [tokenin, 500, tokenout])
        # quote1 = Uniswap_QuoterContract.functions.quoteExactInputSingle(tokenin, tokenout, 500, amount, 0).call()
        quote1 = Uniswap_QuoterContract.functions.quoteExactInput(path, amount).call()
        # Quote2 = SushiRouterContract.functions.getAmountsOut(amount, [tokenin, tokenout]).call()
        # Quote3 = ApeSwap_RouterContract.functions.getAmountsOut(amount, [tokenin, tokenout]).call()
        Quote4 = QuickRouterContract.functions.getAmountsOut(amount, [tokenin, tokenout]).call()

        # allprice = {"Uni": quote1, "Sushi": Quote2[1], "Quick": Quote3[1]}
        # allprice = {"Uni": quote1, "Quick": Quote3[1], "Ape": Quote2[1]}
        # allprice = {"Uni": quote1, "Quick": Quote4[1], "Sushi": Quote2[1], "Ape": Quote3[1]}
        allprice = {"Uni": quote1, "Quick": Quote4[1]}
        return allprice
    except Exception as e:
        ErrorLog('QuoteAllDEX',e)
        print(e)
        os.execv(sys.executable, ['python'] + [sys.argv[0]])

def get_GasPricePolygonArry():
    GasLimit = 1000000
    ETHTransactionfee = 0
    profitOffset = 0
    GasPrice = '--'
    ETHPrice = '--'
    wmatic = web3.toChecksumAddress('0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270')
    usdc = web3.toChecksumAddress('0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174')
    weth = web3.toChecksumAddress('0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619')
    usdt = web3.toChecksumAddress('0xc2132D05D31c914a87C6611C10748AEb04B58e8F')
    '''
    try:
        # result = requests.get('https://api.polygonscan.com/api?module=gastracker&action=gasoracle&apikey=ZRRWE3PP5WJ4WP2BKTK9UZAVHAJJ7KG6JD').json()
        # GasPrice = (float(result['result']['FastGasPrice']) * 1.1)
        # result = requests.get('https://gasstation-mainnet.matic.network/v2').json()
        # if result.get("fast") is not None:
        #     GasPrice = (result['fast']['maxFee'] * 1.1)
        gasPrice = web3.fromWei(web3.eth.gas_price, 'gwei')
        max_priority_fee = web3.fromWei(web3.eth.max_priority_fee, 'gwei')
        GasPrice = (gasPrice + max_priority_fee)
        # else:
        #     # print('get_GasPricePolygonArry Error')
        #     # ErrorLog('get_GasPricePolygonArry','Get Gas Retrun Error HTML')
        #     time.sleep(2.5)
        #     os.execv(sys.executable, ['python'] + [sys.argv[0]])
    except Exception as e:
        # playsound_Error()
        # error_class = e.__class__.__name__  # 取得錯誤類型
        # detail = e.args[0]  # 取得詳細內容
        cl, exc, tb = sys.exc_info()  # 取得Call Stack
        lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
        # fileName = lastCallStack[0]  # 取得發生的檔案名稱
        lineNum = lastCallStack[1]  # 取得發生的行號
        # funcName = lastCallStack[2]  # 取得發生的函數名稱
        # errMsg = fileName, "line {}, in {}: [{}] {}".format(
        #     lineNum, funcName, error_class, detail)
        print(lineNum)
        print('get_GasPricePolygonArry',e)
        # print(errMsg)
        ErrorLog('get_GasPricePolygonArry 2','Get Gas Retrun Error HTML')
        time.sleep(2.5)
        os.execv(sys.executable, ['python'] + [sys.argv[0]])
    '''    
    gasPrice = web3.fromWei(web3.eth.gas_price, 'gwei')
    max_priority_fee = web3.fromWei(web3.eth.max_priority_fee, 'gwei')
    GasPrice = float(gasPrice + max_priority_fee) * 1.1
    try:
        Tokens = [wmatic,weth]
        TokenPrice = getAssetsPricesAaveOracleV3(Tokens)
        ETHPrice = TokenPrice['WMATIC']
        WETHPrice = TokenPrice['WETH']
        '''
        amount = web3.toWei(1, 'ether')
        quote1 = QuoteAllDEX(amount, wmatic, usdt)
        
        quote1 = sorted(quote1.items(), key=lambda kv: kv[1])
        Q1Len = len(quote1) - 1

        toAmount = (quote1[Q1Len][1] / 1e6)
        ETHPrice = round(float(toAmount), 4)

        quote2 = QuoteAllDEX(amount, weth, usdt)

        quote2 = sorted(quote2.items(), key=lambda kv: kv[1])
        Q2Len = len(quote2) - 1

        toAmount2 = (quote2[Q2Len][1] / 1e6)
        WETHPrice = round(float(toAmount2), 4)
        '''
        # Gas Used * Gas Price / 10^9 (礦工費計算＊美金)
        profitOffset = round(GasLimit*((GasPrice/pow(10, 9)))*ETHPrice, 4)
        ETHTransactionfee = round(GasLimit * GasPrice/pow(10, 9), 5)
        return ETHPrice, profitOffset, ETHTransactionfee, round(GasPrice, 4), WETHPrice

    except Exception as e:
        # playsound_Error()
        # error_class = e.__class__.__name__  # 取得錯誤類型
        # detail = e.args[0]  # 取得詳細內容
        # cl, exc, tb = sys.exc_info()  # 取得Call Stack
        # lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
        # lineNum = lastCallStack[1]  # 取得發生的行號
        # funcName = lastCallStack[2]  # 取得發生的函數名稱
        # errMsg = fileName, "line {}, in {}: [{}] {}".format(
        #     lineNum, funcName, error_class, detail)
        cl, exc, tb = sys.exc_info()  # 取得Call Stack
        lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
        fileName = lastCallStack[0]  # 取得發生的檔案名稱
        lineNum = lastCallStack[1]  # 取得發生的行號
        print(fileName,lineNum)
        print('get_GasPricePolygonArry_ETHPrice: ', e)
        ErrorLog('get_GasPricePolygonArry_ETHPrice',e)
        time.sleep(2)
        os.execv(sys.executable, ['python'] + [sys.argv[0]])

def AllSwap(Token_in, Token_out, amount, gasPriceCount):
    try:
        TokenPair = (f'{Token_in}/{Token_out}')
        if(Token_in == 'USDC' or Token_in == 'USDT'):
            Amount = int(amount * 1e6)
        else:
            Amount = web3.toWei(amount, 'ether')

        # try:
        token_in = web3.toChecksumAddress(TokenAddress(Token_in))
        token_out = web3.toChecksumAddress(TokenAddress(Token_out))
        try:
            quote1 = QuoteAllDEX(Amount, token_in, token_out)
            quote1 = sorted(quote1.items(), key=lambda kv: kv[1])
            Q1Len = len(quote1) - 1
        except Exception as e:
            ErrorLog('quote1',e)
            print('quote1:',e)
            # os.execl(sys.executable, os.path.abspath(__file__))
            os.execv(sys.executable, ['python'])
            return
        try:
            quote2 = QuoteAllDEX(quote1[Q1Len][1], token_out, token_in)
            # block_Nimber = web3.eth.getBlock('latest')
            # block_Nimber = web3.eth.getBlock('pending')
            # block_Nimber = block_Nimber['number']
            quote2 = sorted(quote2.items(), key=lambda kv: kv[1])
            Q2Len = len(quote2) - 1
        except Exception as e:
            ErrorLog('quote2',e)
            print('quote2:', e)
            return
        
        # cost = web3.fromWei(int(Amount * 1.0009), 'ether') + decimal.Decimal(gasPriceCount[2])
        if(Token_in == 'USDC' or Token_in == 'USDT'):
            Quote2 = decimal.Decimal(quote2[Q2Len][1]/1e6)
            # GasPriceMatic = gasPriceCount[2]
            cost = amount + (decimal.Decimal(gasPriceCount[2] * gasPriceCount[0]))
        else:
            Quote2 = web3.fromWei(quote2[Q2Len][1], 'ether')
            # GasPriceMatic = gasPriceCount[2]
            cost = amount + decimal.Decimal(gasPriceCount[2])
            
        cost = cost * decimal.Decimal(FlashLoanFee)
        profit = Quote2 - cost
        
        if(Token_in == 'USDC' or Token_in == 'USDT'):
            profit_USD = profit
            profit = float(profit) / float(gasPriceCount[0])
        else:
            profit_USD = float(profit) * float(gasPriceCount[0])
            
        TimeNow = datetime.datetime.now().strftime('%y/%m/%d %H:%M:%S.%f')[:-1]
        ShowProfit = str(int(profit)).ljust(7)
        # ShowProfit = str(round(profit, 2)).ljust(9)
        dex = quote1[Q1Len][0] + quote2[Q2Len][0]
        DEX = [quote1[Q1Len][0], quote2[Q2Len][0]]
        swapNoGo = ''
        TimeNow2 = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-5]
        profitTaget = 50
        Tx_hash =''
        # print((profit) >= (-30))
        # if((profit) >= (-30)):
        if(decimal.Decimal(profit) >= decimal.Decimal(profitTaget) and profit > decimal.Decimal(gasPriceCount[2])):
            eventid = datetime.datetime.now().strftime('%Y%m%d-%H%M%S-')+ str(uuid4())
            if(decimal.Decimal(gasPriceCount[2]) < 2):
                global SwapSend
                SwapSend = 1
                Tx_hash = StratFlahloan(Token_in, Token_out, amount, DEX, gasPriceCount, eventid)

            Excuted_BlockNumber = ''
            if(Tx_hash == 'NoAccountForSwap'):
                SwapSend = 0
                GasPriceMatic = 0
                # GasPriceMatic = 0 * gasPriceCount[4]/pow(10, 9)
                _TX_HASH = ''
                _SwapStatus = '0'
                swapNoGo = 'All Account in use'
                _ReturnAmount = 0
            elif(Tx_hash == ''):
                SwapSend = 0
                GasPriceMatic = 0
                # GasPriceMatic = 0 * gasPriceCount[4]/pow(10, 9)
                _TX_HASH = ''
                _SwapStatus = '2'
                swapNoGo = ''
                _ReturnAmount = 0
            elif(Tx_hash != ''):
                GasPriceMatic = Tx_hash[2]
                # GasPriceMatic = Tx_hash[2] * gasPriceCount[4]/pow(10, 9)
                _TX_HASH = Tx_hash[0]
                _SwapStatus = str(Tx_hash[1])
                _ReturnAmount = Tx_hash[3]
                Excuted_BlockNumber = Tx_hash[4]
                
            date = {
                "eventid": eventid,
                "DEX": dex,
                "Time": TimeNow,
                "Pair": TokenPair,
                "MATIC_Price": gasPriceCount[0],
                "Expected_Return": str(round(Quote2, 2)),
                "Cost": str(round(cost, 0)),
                "Profit": str(round(profit, 2)),
                "Profit_USD": str(round(profit_USD, 2)),
                "GasMatic": str(round(GasPriceMatic, 5)),
                "GasWei": str(round(gasPriceCount[3], 1)),
                "Tx_hash": _TX_HASH,
                "SwapStatus": _SwapStatus,
                "ReturnAmount": str(_ReturnAmount),
                "pending_BlockNNumber": str(block_Nimber),
                "Excuted_BlockNumber": str(Excuted_BlockNumber)
            }
            if(Tx_hash != 'NoAccountForSwap'):
                QRecords.append(date)

            ShowProfit = Fore.LIGHTGREEN_EX + ShowProfit + Style.RESET_ALL
            if(_SwapStatus == '1'):
                SwapStatus = Fore.LIGHTGREEN_EX + 'Succeed' + Style.RESET_ALL
            # elif(_SwapStatus == '2'):
            #     SwapStatus = Fore.LIGHTGREEN_EX + 'Under 1000' + Style.RESET_ALL
            else:
                SwapStatus = Fore.RED + 'Fail' + Style.RESET_ALL
            QuoteInfor = f'{TimeNow2} {TokenPair.ljust(12)} {str(round(Quote2,2)).ljust(9)} - {str(round(cost, 2)).ljust(9)}  {ShowProfit}  {dex.ljust(8)} {SwapStatus} {swapNoGo} {block_Nimber}'
            
        else:
            QuoteInfor = f'{Style.DIM + TimeNow2} {TokenPair.ljust(12)} {str(round(Quote2,2)).ljust(9)} - {str(round(cost, 2)).ljust(9)}  {ShowProfit}  {dex + Style.RESET_ALL} {block_Nimber}'
        
        # LastQuoteInfor = QuoteInfor
        # QuoteInfors.append(QuoteInfor)
        with s_print_lock:
            print(QuoteInfor)
    except Exception as e:
        Error_MSG = str(e)
        ErrorLog('AllSwap',Error_MSG)
        print('AllSwap:', e)
        # playsound_Error()
        os.execv(sys.executable, ['python'] + [sys.argv[0]])
    '''
    # except Exception as e:
    #     print('AllSwap:')
    #     error_class = e.__class__.__name__  # 取得錯誤類型
    #     detail = e.args[0]  # 取得詳細內容
    #     cl, exc, tb = sys.exc_info()  # 取得Call Stack
    #     lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
    #     fileName = lastCallStack[0]  # 取得發生的檔案名稱
    #     lineNum = lastCallStack[1]  # 取得發生的行號
    #     funcName = lastCallStack[2]  # 取得發生的函數名稱
    #     errMsg = f"file {fileName}, line {lineNum}, {funcName}: [{error_class}] {detail}"
    #     print(errMsg)
    '''

def playsound():
    os.system('afplay /Users/vichuang/Music/音效/ding-idea-40142.mp3')

def playsound_Flashloan():
    os.system('afplay /Users/vichuang/Music/音效/cash.mp3')

def playsound_Error():
    os.system('afplay /Users/vichuang/Music/音效/mixkit-electric-fence-alert-2969.wav')

while(True):    
    # account = web3.toChecksumAddress('0x85D6EceC4F3cD8AE8DF22dcE8437085B4C2A1E4a')
    # nonce = web3.eth.getTransactionCount(account)
    # nonce = web3.eth.get_transaction_count(account)
    Accounts = getAccounts()
    gasPriceCount = get_GasPricePolygonArry()
    system('clear')
    # print((nonce))
    print('----------------------------------------------')
    print(f"MATIC: {round(gasPriceCount[0],4)} - WETH: {round(gasPriceCount[4],4)} - GAS : [{round(gasPriceCount[2], 3)} {round(gasPriceCount[3], 1)}]")
    for Token_in in TokenIn:
        for Token_out in TokensOut:
            if(Token_in != Token_out):
                for amount in Amounts:
                    # AllSwap(Token_in, Token_out, amount, gasPriceCount)
                    Price_Quote_AllSwap = threading.Thread(target=AllSwap, args=[Token_in, Token_out, amount, gasPriceCount])
                    threads.append(Price_Quote_AllSwap)
                    Price_Quote_AllSwap.start()
    for x in threads:
        x.join()

    
    if(bool(QRecords)):
        try:
            # account = web3.toChecksumAddress('0x85D6EceC4F3cD8AE8DF22dcE8437085B4C2A1E4a')
            account = web3.toChecksumAddress('0x32d55dd4eae334110c26ecb3217af267117922d3')
            upDateAccountSts1(str(account),0)
            with open("SwapLog.json", "r") as file:
                data = json.load(file)
            for Record in QRecords:
                data.append(Record)
            with open("SwapLog.json", "w") as file:
                json.dump(data, file, indent=4)
                
            QRecords = []
            # playsoundTH = threading.Thread(target=playsound)
            # playsoundTH.start()

            if(SwapSend == 1):
                # playsoundTH = threading.Thread(target=playsound)
                # playsoundTH.start()
                USDC = checkUSDCbalance(account)
                if(USDC>0): QuickSwap(account, 'USDC', 'WMATIC', USDC)
                # # WMATIC = checkWMATICbalance(account)
                # # if(WMATIC>0): UnWrappWmatic(account)
                UnWrappWmatic(account)
                UpdateAccountBalance()
                SwapSend = 0
                
                # sleep(25)
        except Exception as e:
            ErrorLog('QRecords',e)
            print('QRecords:',e)    
            # exit()
            os.execv(sys.executable, ['python'] + [sys.argv[0]])
            
        
        
        
    print('----------------------------------------------')
    cursor.hide()
    LINE_CLEAR = '\x1b[2K'
    for i in reversed(range(8)):
        print('Restart in:',(i+1), end='\r')
        sleep(1)
    print(end=LINE_CLEAR)
    print('Starting...', end='\r')
    # sleep(10)
