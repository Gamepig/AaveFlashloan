from Functions import getContractAddress, TokenAddress, getPrivate_Key, upDateAccountSts, ErrorLog
from getBalance import getBalance
from web3 import HTTPProvider, Web3
from web3.logs import DISCARD
import json
from time import sleep
import os
import sys
from colorama import Fore, Back, Style
# web3 = Web3(HTTPProvider('https://polygon-mainnet.blastapi.io/fa940a80-11dc-43e6-b0dc-03d6607ddece', request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://poly-rpc.gateway.pokt.network', request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://polygon.blockpi.network/v1/rpc/public', request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://poly-mainnet.gateway.pokt.network/v1/lb/fb2da9793f63bcbc71fd8f0c', request_kwargs={'timeout': 180}))
web3_alchemy = Web3(HTTPProvider('https://polygon-mainnet.g.alchemy.com/v2/JOGYiBYYVqQJUCF1UsNqcPWNhJixWaLO',request_kwargs={'timeout': 240}))
# web3 = Web3(HTTPProvider('https://polygon-mainnet.g.alchemy.com/v2/JOGYiBYYVqQJUCF1UsNqcPWNhJixWaLO',request_kwargs={'timeout': 240}))
# web3 = Web3(HTTPProvider('https://polygon.blockpi.network/v1/rpc/35d20c87d2999a6cfd1971aec2edbc4824ed530a', request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://polygon.llamarpc.com/rpc/01GTP6RCY2TT1JHMMCSDQEMHRE', request_kwargs={'timeout': 180}))
web3 = Web3(HTTPProvider('https://polygon-rpc.com/',request_kwargs={'timeout': 240}))
# web3 = Web3(HTTPProvider('http://127.0.0.1:8545', request_kwargs={'timeout': 180}))


def AaveFlashloan(Token, tokenIn, tokenOut, amount, gasPrice, DEX, account, private_key, eventid):
    
    ReturnAmount = 0
    blockNumber = ''
    tx_hash = ''
    transaction_cost = ''
    # web3 = Web3(HTTPProvider('https://polygon-rpc.com/',request_kwargs={'timeout': 180}))
    # web3 = Web3(HTTPProvider('http://localhost:8545', request_kwargs={'timeout': 180}))
    AaveFlashLoanAddress = web3.toChecksumAddress(
        (getContractAddress('AaveFlashLoan_ContractAddress')))

    with open("../build/contracts/AaveFlashLoan.json") as f:
        AaveFlashLoanABI = json.load(f)
        AaveFlashLoanABI = AaveFlashLoanABI['abi']

    AaveFlashLoan = web3.eth.contract(
        address=AaveFlashLoanAddress, abi=AaveFlashLoanABI)

    # account = web3.eth.accounts[0]
    # private_key = getPrivate_Key(0)

    DEX1 = DEX[0]
    DEX2 = DEX[1]
    
    if(DEX1=='Uni'): DEX1 = 0
    elif(DEX1=='Quick'): DEX1 = 1
    elif(DEX1=='Sushi'): DEX1 = 2
    elif(DEX1=='Ape'): DEX1 = 3
    
    if(DEX2=='Uni'): DEX2 = 0
    elif(DEX2=='Quick'): DEX2 = 1
    elif(DEX2=='Sushi'): DEX2 = 2
    elif(DEX2=='Ape'): DEX2 = 3
    
    # if(DEX1 == 'Uni'): DEX1 = 0
    # else:DEX1 = 1 
    # if(DEX2 == 'Uni'): DEX2 = 0
    # else:DEX2 = 1 
    
    if(Token=='USDC'):
        _amountIn = (amount*1e6)
    else:
        _amountIn = web3.toWei(amount, 'ether')
    try:    
        # nonce = web3.eth.getTransactionCount(account,"pending")
        # nonce = web3.eth.getTransactionCount(account)
        nonce = web3_alchemy.eth.get_transaction_count(account)
        # if(gasPrice<50):gasPrice=50
        buid_Trans = {
            'from': account,
            'gas': 7000000,
            'gasPrice': web3.toWei(gasPrice, 'gwei'),
            'nonce': nonce
        }
        transaction = AaveFlashLoan.functions.getFlashLoan(
                tokenIn,
                tokenOut,
                int(_amountIn),
                DEX1,
                DEX2
            ).buildTransaction(buid_Trans)  # type: ignore
    
        signed_tx = web3.eth.account.signTransaction(transaction, private_key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        txn_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        rich_logs = AaveFlashLoan.events.ReturnAmouint().processReceipt(txn_receipt, errors=DISCARD)
        # gas_price = web3.eth.getTransaction(tx_hash).gasPrice  # type: ignore
        # gas_used = web3.eth.getTransactionReceipt(tx_hash).gasUsed  # type: ignore
        gas_used = txn_receipt['gasUsed']
        gas_price = txn_receipt['effectiveGasPrice']  # type: ignore
        blockNumber = txn_receipt['blockNumber']
        transaction_cost = gas_price * gas_used
        swapstatus = 0
        if(rich_logs):
            if(txn_receipt['status']==1):
                swapstatus = 1
                if(Token=='USDC'):
                    ReturnAmount = rich_logs[0]['args']['_ReturnAmouint']/1e6
                else:
                    ReturnAmount = web3.fromWei(rich_logs[0]['args']['_ReturnAmouint'], 'ether')
                print('Tokens Swapped on TX:', web3.toHex(tx_hash))
                os.system('afplay /Users/vichuang/Music/音效/cash.mp3')
    except Exception as e:
        print(web3.toHex(tx_hash))
        print(e)
        # print(txn_receipt)
        upDateAccountSts(str(account), 0, eventid)
        swapstatus = 0
        type = 'AaveFlashloan_'+web3.toHex(tx_hash)
        Error_Log = str(e)
        ErrorLog(type,Error_Log)
        
    upDateAccountSts(str(account), 0, eventid)
    return web3.toHex(tx_hash), swapstatus, transaction_cost, ReturnAmount, blockNumber

# if len(sys.argv) > 1:
#     Token = sys.argv[1]
#     tokenIn = sys.argv[2]
#     tokenOut = sys.argv[3]
#     amount = int(sys.argv[4])
#     gasPrice = 50
#     account = web3.eth.accounts[0]
#     private_key = getPrivate_Key(0)
#     DEX = ['Uni', 'Uni']
#     tokenIn = web3.toChecksumAddress(TokenAddress(tokenIn))
#     tokenOut = web3.toChecksumAddress(TokenAddress(tokenOut))
#     result = AaveFlashloan(Token, tokenIn, tokenOut, amount, gasPrice, DEX, account, private_key, 'TEST')
#     print('ReturnAmount:',float(result[3])/1e6)
#     print(result)
    

