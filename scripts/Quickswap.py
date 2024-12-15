import sys
from web3 import HTTPProvider, Web3
import requests
from os import system
import json
import uniswap
import time
from Functions import TokenAddress, getPrivate_Key, approve_token, getContractAddress
from getBalance import getBalance

# for i in sys.argv:
#     print(str(i))

# print(sys.argv[1])

web3 = Web3(HTTPProvider('http://localhost:8545',request_kwargs={'timeout': 180}))
LocalQuickswapContract = getContractAddress('QuickswapContractAddress')
QuickswapRouter = web3.toChecksumAddress('0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff')
_TokenIn = sys.argv[1]
_TokenOut = sys.argv[2]
TokenIn = web3.toChecksumAddress(TokenAddress(sys.argv[1]))
TokenOut = web3.toChecksumAddress(TokenAddress(sys.argv[2]))
amount = int(sys.argv[3])

MATIC = web3.toChecksumAddress(TokenAddress('MATIC'))
WMATIC = web3.toChecksumAddress(TokenAddress('WMATIC'))
USDC = web3.toChecksumAddress(TokenAddress('USDC'))
USDT = web3.toChecksumAddress(TokenAddress('USDT'))
WETH = web3.toChecksumAddress(TokenAddress('WETH'))

account = web3.eth.accounts[0]
private_key = getPrivate_Key(0)

with open("../build/contracts/Quickswap.json") as f:
    abi = json.load(f)
    QuickswapABI = abi['abi']
    
Quickswap_address = web3.toChecksumAddress(LocalQuickswapContract)

Quickswap = web3.eth.contract(address=LocalQuickswapContract, abi=QuickswapABI)

# for func in Uniswap.all_functions():
#     print('contract functions:', func)
# exit()

poolFee = 100

if(_TokenIn=='WMATIC'):
    _amountIn = web3.toWei(amount, 'ether')
    approve_token(WMATIC, Quickswap_address, account, private_key, _amountIn)
elif(_TokenIn=='USDC'):
    _amountIn = int(amount*1e6)
    approve_token(USDC, Quickswap_address, account, private_key, _amountIn)
nonce = web3.eth.getTransactionCount(account)
# print(nonce)
# exit()
buid_Trans = {
    'from': account,
    'gas': 245000,
    'gasPrice': web3.toWei('50', 'gwei'),
    'nonce': nonce,
    'chainId': 137
}
transaction = Quickswap.functions.swap_quickswap(TokenIn, TokenOut, _amountIn).buildTransaction(buid_Trans)  # type: ignore
signed_tx = web3.eth.account.signTransaction(transaction, private_key)
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
txn_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
if(txn_receipt['status']):
    print('Tokens Swapped on TX:', web3.toHex(tx_hash))
else:
    print('SWAP Fail! TX:', web3.toHex(tx_hash))

approve_token(WMATIC, Quickswap_address, account, private_key, 0)

f = open('../build/contracts/IERC20.json')
info_json = json.load(f)
abi = info_json["abi"]
Token_contract = web3.eth.contract(address=WMATIC, abi=abi)
USDC_contract = web3.eth.contract(address=USDC, abi=abi)
getBalance()
# AccountNumber = 0
# for account in web3.eth.accounts:
#     blance = web3.eth.getBalance(account)
#     balanceOf_WMATIC = Token_contract.functions.balanceOf(account).call()
#     balanceOf_USDC = USDC_contract.functions.balanceOf(account).call()
#     print(f"{AccountNumber} account : {account} {web3.fromWei(blance, 'ether')} MATIC")
#     print(f"{AccountNumber} account : {account} {web3.fromWei(balanceOf_WMATIC, 'ether')} WMATIC")
#     print(f"{AccountNumber} account : {account} {balanceOf_USDC/1e6} USDC")

#     AccountNumber += 1
#     if(AccountNumber >= 1):
#         break

# print(txn_receipt)
