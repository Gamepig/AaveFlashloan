import sys
from web3 import HTTPProvider, Web3
import requests
from os import system
import json
import uniswap
from Functions import TokenAddress, getPrivate_Key, getContractAddress, approve_token
from getBalance import getBalance
# for i in sys.argv:
#     print(str(i))

# print(sys.argv[1], sys.argv[2])
# exit()


# web3 = Web3(HTTPProvider('https://polygon-rpc.com/', request_kwargs={'timeout': 30}))
web3 = Web3(HTTPProvider('http://localhost:8545',request_kwargs={'timeout': 180}))
Token = sys.argv[1]
# Token = 'USDC'
amount = int(sys.argv[2])
# with open("../build/contracts/WMATICABI.json") as f:
with open("../build/contracts/IERC20.json") as f:
    info_json = json.load(f)
    abi = info_json["abi"]
Token_Address = web3.toChecksumAddress(TokenAddress(Token))
AaveFlashLoanAddress = web3.toChecksumAddress(
    getContractAddress('AaveFlashLoan_ContractAddress'))
Token_Contract = web3.eth.contract(address=Token_Address, abi=abi)
# contract_Balance = Token_Contract.functions.balanceOf(AaveFlashLoanAddress).call()
# print(contract_Balance)
# exit()
# for func in Token_Contract.all_functions():
#     print('contract functions:', func)
# exit()

account = web3.eth.accounts[0]
if(Token == 'USDC'):
    amount = int(amount*1e6)
else:
    amount = web3.toWei(amount, 'ether')
print(f'Sending Amount: {amount}')
approve_status = approve_token(TokenAddress(Token), Token_Address, account, getPrivate_Key(0), (amount))
print(f'approve_status: {approve_status[0]}')
print(f'approve allowance: {approve_status[1]}')
#build a transaction in a dictionary
nonce = web3.eth.getTransactionCount(web3.eth.accounts[0])
buid_Trans = {
    'from': account,
    'nonce': nonce,
    'gas': 2000000,
    'gasPrice': web3.toWei('50', 'gwei')
}
transaction = Token_Contract.functions.transfer(AaveFlashLoanAddress, amount).buildTransaction(buid_Trans)  # type: ignore
#sign the transaction
signed_tx = web3.eth.account.sign_transaction(transaction, getPrivate_Key(0))

#send transaction
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
txn_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
#get transaction hash
print('transaction succeed at :', web3.toHex(tx_hash))

getBalance()
# contract_Balance = Token_Contract.functions.balanceOf(AaveFlashLoanAddress).call()
# if(Token == 'USDC'):
#     print((contract_Balance/1e6))
#     print((Token_Contract.functions.balanceOf(account).call()/1e6))
# else:
#     print(web3.fromWei(contract_Balance, 'ether'))
#     print(web3.fromWei(Token_Contract.functions.balanceOf(account).call(), 'ether'))
