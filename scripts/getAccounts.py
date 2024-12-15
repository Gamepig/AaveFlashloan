from web3 import HTTPProvider, Web3
from web3.middleware import geth_poa_middleware  # type: ignore
import time
import json
import os
import sys
import datetime
from colorama import Fore, Back, Style
from Functions import Insert_aave_UserAccount, getUserAccountData
try:
    # web3 = Web3(HTTPProvider('https://polygon-rpc.com/', request_kwargs={'timeout': 180}))
    # web3 = Web3(HTTPProvider('https://polygon.llamarpc.com/rpc/01GTP6RCY2TT1JHMMCSDQEMHRE', request_kwargs={'timeout': 180}))
    web3 = Web3(HTTPProvider('https://polygon.blockpi.network/v1/rpc/public', request_kwargs={'timeout': 180}))
    # web3 = Web3(HTTPProvider('https://polygon-mainnet.g.alchemy.com/v2/JOGYiBYYVqQJUCF1UsNqcPWNhJixWaLO',request_kwargs={'timeout': 180}))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # create an empty dictionary we will add transaction data to
    tx_dictionary = []
    contract_address = web3.toChecksumAddress("0x794a61358D6845594F94dc1DB02A252b5b4814aD")
    with open("../scripts/AavePoolV3ABI.json") as f:
                ABI = json.load(f)
                ABI = ABI['result']
    contract = web3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=ABI)
    # lpAddressProviderContract = web3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=ABI)
    # contract = lpAddressProviderContract.caller().getLendingPool()
except Exception as e:
                print('HTTPProvider:', e)
                os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)  # 程式重新啟動
                

def getEvents(CONTRACT_CREATION_BLOCK):
    try:
        events = contract.events.Borrow.getLogs(fromBlock=CONTRACT_CREATION_BLOCK)
        # events = contract.events.Borrow.createFilter(fromBlock=CONTRACT_CREATION_BLOCK, argument_filters= {'Borrow()'})
        return(events)
    except Exception as e:
        print('getEvents:',e)
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)  # 程式重新啟動
def getTransactions(start, end, address):
    '''This function takes three inputs, a starting block number, ending block number
    and an Ethereum address. The function loops over the transactions in each block and
    checks if the address in the to field matches the one we set in the blockchain_address.
    Additionally, it will write the found transactions to a pickle file for quickly serializing and de-serializing
    a Python object.'''
    # print(f"Started filtering through block number {start} to {end} for transactions involving the address - {address}...")
    transaction_Count = 0
    for x in range(start, end):
        if x is not None:
            tx_count = 0
            try:
                block = web3.eth.getBlock(x, True)
                for transaction in block.transactions:  # type: ignore
                    if transaction['to'] == address or transaction['from'] == address:
                        # Event = getEvents(x)
                        # if(Event is not None):
                        account =str(transaction['from'])
                        UserInfo = getUserAccountData(account)
                        totalCollatera = UserInfo[0] / 10 ** 8
                        totalDebtBase = UserInfo[1] / 10 ** 8
                        UserHF = web3.fromWei(UserInfo[5],'ether')
                        if(UserHF>2):
                            continue
                        if(totalDebtBase==0):
                            continue
                        if(totalCollatera >= 100):
                            try:
                                Insert_aave_UserAccount(account)
                                print(f"{Fore.LIGHTGREEN_EX + account + Style.RESET_ALL}")
                            except Exception as e:
                                print('MYSQL INSERT ERROR:', e)

                    Event = ''
                    tx_count+=1
                # time.sleep(1)
                TimeNow = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-1]
                curent_block = web3.eth.blockNumber
                print('BlockNumber:', x, curent_block, TimeNow, 'tx_count:',tx_count)  
            except Exception as e:
                print('Main Loop:', e)
                # os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)  # 程式重新啟動
        # time.sleep(1)             
            
# filter through blocks and look for transactions involving this address
try:
    last_blocknumber = ''
    ending_blocknumber = web3.eth.blockNumber  # request the latest block number
    starting_blocknumber = ending_blocknumber - 1000 # latest block number minus 20 blocks
    getTransactions(starting_blocknumber, ending_blocknumber, contract_address)
    starting_blocknumber = ending_blocknumber
except Exception as e:
    print('First Loop:', e)
    # os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)  # 程式重新啟動
while(True):
    try:
        ending_blocknumber = web3.eth.blockNumber  # request the latest block number
        BD = ending_blocknumber - starting_blocknumber
        if(BD>50):
            print(f'starting_blocknumber: {starting_blocknumber}')
            print(f'ending_blocknumber: {ending_blocknumber}')
            print(f'BD: {BD}')
            starting_blocknumber = ending_blocknumber - 1
            continue
        
        if(starting_blocknumber!=ending_blocknumber):
            getTransactions(starting_blocknumber, ending_blocknumber, contract_address)
        starting_blocknumber = ending_blocknumber
        time.sleep(2)
    except Exception as e:
                print('while Loop:', e)
                time.sleep(6)
                os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)  # 程式重新啟動
