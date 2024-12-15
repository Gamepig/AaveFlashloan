from web3 import HTTPProvider, Web3

# web3 = Web3(HTTPProvider('https://polygon-rpc.com/',request_kwargs={'timeout': 180}))
web3 = Web3(HTTPProvider('https://polygon-mainnet.g.alchemy.com/v2/JOGYiBYYVqQJUCF1UsNqcPWNhJixWaLO',request_kwargs={'timeout': 180}))
# web3 = Web3(Web3.WebsocketProvider('wss://polygon-mainnet.g.alchemy.com/v2/JOGYiBYYVqQJUCF1UsNqcPWNhJixWaLO'))

account = web3.toChecksumAddress('0x85D6EceC4F3cD8AE8DF22dcE8437085B4C2A1E4a')
# account = web3.toChecksumAddress('0x9794B41450701c36E6a9d162F9a3e8D09FD62E6E')

print(web3.eth.getTransactionCount(account))
# print(web3.eth.getTransactionCount(account,"pending"))