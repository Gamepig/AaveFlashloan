import time
from web3.logs import DISCARD
from web3 import Web3
from web3 import HTTPProvider, Web3
import json
from Functions import getContractAddress, getPrivate_Key
import asyncio
def _eventTest():
    # web3 = Web3(HTTPProvider('http://localhost:8545',request_kwargs={'timeout': 180}))
    web3 = Web3(HTTPProvider('https://polygon-rpc.com/',request_kwargs={'timeout': 180}))
    AaveFlashLoanAddress = web3.toChecksumAddress((getContractAddress('AaveFlashLoan_ContractAddress')))

    with open("../build/contracts/AaveFlashLoan.json") as f:
        AaveFlashLoanABI = json.load(f)
        AaveFlashLoanABI = AaveFlashLoanABI['abi']

    AaveFlashLoan = web3.eth.contract(address=AaveFlashLoanAddress, abi=AaveFlashLoanABI)
    # print('----------------------------------------------------------------')
    # for func in eventTest.all_functions():
    #     print('contract functions:', func)

    # print('----------------------------------------------------------------')
    # exit()

    # tx_hash = ('0x92f288d98584036f68b4dded6dc523261c53ec390ca90440ae538306100c6d73')
    tx_hash = ('0x69bfdd72d3d25aea2c6002b1191660aecc759e384c572ee886ed46389336ec71')
    # txn_receipt = web3.eth.waitForTransactionReceipt(tx_hash)  # type: ignore
    txn_receipt = web3.eth.getTransactionReceipt(tx_hash)  # type: ignore
    # gas_price = web3.eth.getTransaction(tx_hash).gasPrice  # type: ignore
    # gas_used = web3.eth.getTransactionReceipt(tx_hash).gasUsed  # type: ignore
    gas_used = txn_receipt['gasUsed']
    gas_price = txn_receipt['effectiveGasPrice']  # type: ignore
    transaction_cost = gas_price * gas_used
    rich_logs = AaveFlashLoan.events.ReturnAmouint().processReceipt(txn_receipt, errors=DISCARD)
    # print(rich_logs[0]['args']['_ReturnAmouint']/1e6)
    # if(rich_logs[0]['args']['_ReturnAmouint']):
    #     print(web3.fromWei(rich_logs[0]['args']['_ReturnAmouint'],'ether'))
    # txn_receipt['gasUsed']
    if(rich_logs):
        print(rich_logs)
    print(web3.fromWei(transaction_cost,'ether'))
    print(gas_used)
    print(web3.fromWei(gas_price,'gwei'))
    print(txn_receipt['blockNumber'])
    # print(fetch_transaction_revert_reason(web3, tx_hash))  # type: ignore
    for topic in txn_receipt:
        print(topic)


if(__name__ == '__main__'):
    _eventTest()
