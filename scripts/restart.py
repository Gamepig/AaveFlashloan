import os
import signal
import subprocess
import time
import sys
from web3 import HTTPProvider, Web3

web3 = Web3(HTTPProvider('https://polygon-mainnet.g.alchemy.com/v2/JOGYiBYYVqQJUCF1UsNqcPWNhJixWaLO', request_kwargs={'timeout': 180}))
# Query the blockchain (replace example parameters)
estGas = web3.eth.estimate_gas({
     'to': '0xd3CdA913deB6f67', 
     'from':web3.eth.coinbase, 
     'value': 12345
     })

# Print the output to console
print(estGas)

# def main():
#     print("Start to sleep")
#     time.sleep(1)
#     print("Sleep end")    
#     test= 1/0 #強制製造錯誤

# if __name__=='__main__':
#     try:
#         main()
#     except:
#         print('y')
#         os.execv(sys.executable, ['python'] + [sys.argv[0]])