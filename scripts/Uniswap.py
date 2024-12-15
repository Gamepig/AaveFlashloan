import sys
from web3 import HTTPProvider, Web3
import requests
from os import system
import json
import uniswap
import time
from Functions import TokenAddress, getPrivate_Key, getContractAddress, approve_token

# for i in sys.argv:
#     print(str(i))

# print(sys.argv[1])

web3 = Web3(HTTPProvider('http://localhost:8545',request_kwargs={'timeout': 180}))
LocalUniswapContract = getContractAddress('UniswapContractAddress')
swapRouter = web3.toChecksumAddress('0xE592427A0AEce92De3Edee1F18E0157C05861564')

MATIC = web3.toChecksumAddress(TokenAddress('MATIC'))
WMATIC = web3.toChecksumAddress(TokenAddress('WMATIC'))
USDC = web3.toChecksumAddress(TokenAddress('USDC'))
USDT = web3.toChecksumAddress(TokenAddress('USDT'))
WETH = web3.toChecksumAddress(TokenAddress('WETH'))

account = web3.eth.accounts[0]
private_key = getPrivate_Key(0)
# with open("../ABI/UniswapRouterABI.json") as f:
#     # UniswapABI = json.load(f)
#     abi = json.load(f)
#     abi = abi['result']
with open("../build/contracts/UniSwapExamples.json") as f:
    # UniswapABI = json.load(f)
    abi = json.load(f)
    abi = abi['abi']

Uniswap_address = web3.toChecksumAddress(LocalUniswapContract)

Uniswap = web3.eth.contract(address=LocalUniswapContract, abi=abi)

# for func in Uniswap.all_functions():
#     print('contract functions:', func)
# exit()
poolFee = 500
_amountIn = web3.toWei(100,'ether')
Params = (
    WMATIC,  # tokenIn
    USDC,  # tokenOut
    poolFee,  # fee
    account,  # recipient
    round(time.time()) + 60 * 20,  # deadline
    _amountIn,  # amountIn
    0,  # amountOutMinimum
    0  # sqrtPriceLimitX96
)
approve_token(WMATIC, Uniswap_address, account, private_key, _amountIn)
nonce = web3.eth.getTransactionCount(account)
buid_Trans = {
    'from': account,
    'gas': 245000,
    'gasPrice': web3.toWei('50', 'gwei'),
    'nonce': nonce
}
# transaction = Uniswap.functions.exactInputSingle(Params).buildTransaction(buid_Trans)
transaction = Uniswap.functions.swapExactInputSingle(WMATIC, USDC, _amountIn).buildTransaction(buid_Trans)  # type: ignore
signed_tx = web3.eth.account.signTransaction(transaction, private_key)
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
txn_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
if(txn_receipt['status']):
    print('Tokens Swapped on TX:', web3.toHex(tx_hash))
else:
    print('SWAP Fail! TX:', web3.toHex(tx_hash))

approve_token(WMATIC, Uniswap_address, account, private_key, 0)
with open("../build/contracts/IERC20.json") as f:
    info_json = json.load(f)
    abi = info_json["abi"]
Token_contract = web3.eth.contract(address=WMATIC, abi=abi)
USDC_contract = web3.eth.contract(address=USDC, abi=abi)
AccountNumber = 0
for account in web3.eth.accounts:
    blance = web3.eth.getBalance(account)
    balanceOf_WMATIC = Token_contract.functions.balanceOf(account).call()
    balanceOf_USDC = USDC_contract.functions.balanceOf(account).call()
    print(f"{AccountNumber} account : {account} {web3.fromWei(blance, 'ether')} MATIC")
    print(f"{AccountNumber} account : {account} {web3.fromWei(balanceOf_WMATIC, 'ether')} WMATIC")
    print(f"{AccountNumber} account : {account} {balanceOf_USDC/1e6} USDC")

    AccountNumber += 1
    if(AccountNumber >= 0):
        break

# print(txn_receipt)
