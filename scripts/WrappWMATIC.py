from web3 import HTTPProvider, Web3
import json
from Functions import getPrivate_Key
from getBalance import getBalance
import sys

web3 = Web3(HTTPProvider('http://localhost:8545',request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://polygon-rpc.com/',request_kwargs={'timeout': 60}))

WMATIC = web3.toChecksumAddress('0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270')
amount = int(sys.argv[1])
account = web3.toChecksumAddress(sys.argv[2])
# account = web3.eth.accounts[0]
private_key = getPrivate_Key(0)
with open("../build/contracts/WMATICABI.json") as f:
    # UniswapABI = json.load(f)
    abi = json.load(f)
    abi = abi['result']

WMATIC_Contract = web3.eth.contract(address=WMATIC, abi=abi)
balanceOfWMATIC = WMATIC_Contract.functions.balanceOf(account).call()
# for func in WMATIC_Contract.all_functions():
#     print('contract functions:', func)
# exit()
nonce = web3.eth.getTransactionCount(account)
# Wrapp
buid_Trans = {
    'from': account,
    'gas': 245000,
    'gasPrice': web3.toWei('50', 'gwei'),
    'nonce': nonce,
    'value': Web3.toWei(amount, 'ether')
}
#Unwrapp
# buid_Trans_withdraw = {
#     'from': account,
#     'gas': 500000,
#     'gasPrice': web3.toWei('50', 'gwei'),
#     'nonce': nonce,
#     'value': 0
# }
transaction = WMATIC_Contract.functions.deposit().buildTransaction(buid_Trans)  # type: ignore Wrapp
# transaction = WMATIC_Contract.functions.withdraw(balanceOfWMATIC).buildTransaction(buid_Trans_withdraw)# type: ignore Unwrapp
signed_tx = web3.eth.account.signTransaction(transaction, private_key)
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
txn_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
if(txn_receipt['status']):
    print('Tokens Swapped on TX:', web3.toHex(tx_hash))
else:
    print('SWAP Fail! TX:', web3.toHex(tx_hash))

getBalance()
