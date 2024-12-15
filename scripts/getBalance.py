import sys
from web3 import HTTPProvider, Web3
from os import system
import json
from datetime import datetime
from Functions import TokenAddress, getContractAddress

def getBalance():
    
    # web3 = Web3(HTTPProvider('http://localhost:8545', request_kwargs={'timeout': 180}))
    # web3 = Web3(HTTPProvider('https://polygon-rpc.com/', request_kwargs={'timeout': 30}))
    web3 = Web3(HTTPProvider('https://polygon-mainnet.g.alchemy.com/v2/JOGYiBYYVqQJUCF1UsNqcPWNhJixWaLO',request_kwargs={'timeout': 180}))
    # web3 = Web3(Web3.WebsocketProvider('wss://polygon-mainnet.g.alchemy.com/v2/JOGYiBYYVqQJUCF1UsNqcPWNhJixWaLO'))


    WMATIC_Address = web3.toChecksumAddress(TokenAddress('WMATIC'))
    USDC_Address = web3.toChecksumAddress(TokenAddress('USDC'))
    AaveFlashLoanAddress = web3.toChecksumAddress(
        getContractAddress('AaveFlashLoan_ContractAddress'))

    with open("../build/contracts/IERC20.json") as f:
        info_json = json.load(f)
        abi = info_json["abi"]

    WMATIC_Contract = web3.eth.contract(address=WMATIC_Address, abi=abi)
    USDC_Contract = web3.eth.contract(address=USDC_Address, abi=abi)
    # account = web3.eth.accounts[0]
    accountNumber = 0
    account = web3.toChecksumAddress('0x85D6EceC4F3cD8AE8DF22dcE8437085B4C2A1E4a')
    # account = web3.toChecksumAddress('0xb2D997119b15Be609c8Efc75d6Ad66383693dB47')
    print(f"AccountBalance : {'{:,.2f}'.format(web3.fromWei(web3.eth.getBalance(account), 'ether'),',')} MATIC")
    print(f"                 {'{:,.2f}'.format(web3.fromWei(WMATIC_Contract.functions.balanceOf(account).call(), 'ether'))} WMATIC")
    print(f"                 {'{:,.2f}'.format(USDC_Contract.functions.balanceOf(account).call()/1e6)} USDC")
    # for account in web3.eth.accounts:
    #     print('---------------------------------------------')
    #     print(f"Account[{accountNumber}] Balance : {'{:,.2f}'.format(web3.fromWei(web3.eth.getBalance(account), 'ether'),',')} MATIC")
    #     print(f"                  {'{:,.2f}'.format(web3.fromWei(WMATIC_Contract.functions.balanceOf(account).call(), 'ether'))} WMATIC")
    #     print(f"                  {'{:,.2f}'.format(USDC_Contract.functions.balanceOf(account).call()/1e6)} USDC")
    #     accountNumber += 1
    #     if(accountNumber > 2):
    #         break
    # print('---------------------------------------------')
    # print(f"Contract Balance:")
    # print(f"                  {'{:,.2f}'.format(web3.fromWei(WMATIC_Contract.functions.balanceOf(AaveFlashLoanAddress).call(), 'ether'))} WMATIC")
    # print(f"                  {'{:,.2f}'.format(USDC_Contract.functions.balanceOf(AaveFlashLoanAddress).call()/1e6)} USDC")
    # print('---------------------------------------------')

if len(sys.argv) > 1: getBalance()
