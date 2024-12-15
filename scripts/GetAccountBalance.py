from Functions import UpdateAccountBalance, SendMATIC
from getBalance import getBalance
from web3 import HTTPProvider, Web3
web3 = Web3(HTTPProvider('http://localhost:8545',
                         request_kwargs={'timeout': 30}))
# UpdateBalance = UpdateAccountBalance()
# if(UpdateBalance):
#     print('Balance Update Succeed')
# else:
#     print('Balance Update Fail')
_fromAccount = web3.toChecksumAddress('0x32d55dd4eae334110c26ecb3217af267117922d3')
_toAccount = web3.toChecksumAddress('0xcf222b5f52f53f763fa2f1d55441420d475d770f')
private_key = '0x1c5e00deeb6b03a1176b76c7ddc91f2dbad518b4a6fa3a8266cd3fa663296561'
amount = 100
# SendMATIC(_fromAccount, _toAccount, amount, private_key)
# UpdateAccountBalance()
getBalance()
