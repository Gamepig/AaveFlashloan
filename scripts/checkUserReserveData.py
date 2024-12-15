from web3 import HTTPProvider, Web3
import json
from decimal import Decimal
import numpy as np
import sys
from colorama import Fore, Back, Style
np.set_printoptions(suppress=False)
from Functions import ReservesList, checkUserReserveData, getOraclePriceFeed, getUserAccountData, getAssetsPricesAaveOracleV3, getAaveAccountsByNumber
# web3 = Web3(HTTPProvider('https://polygon-rpc.com/', request_kwargs={'timeout': 180}))
web3 = Web3(HTTPProvider('https://damp-long-haze.matic.discover.quiknode.pro/df629767bb3228cd4f0cd10461e019375bb2d302/', request_kwargs={'timeout': 180}))
Accounts = []
argv = sys.argv[1]
# User = web3.toChecksumAddress(sys.argv[1])
# Users = getAaveAccountsByNumber(str(sys.argv[1]))
# Users.append('0x2AA756236f096658C3A37DA01C2443a917A427A1','')
# Users = '0x2AA756236f096658C3A37DA01C2443a917A427A1'
if(len(argv)<6):
    argv = int(argv)
if(type(argv)==str):
    Users = str(sys.argv[1])
    Accounts.append(Users)
elif(type(argv)==int):
    Users = getAaveAccountsByNumber(str(sys.argv[1]))
    for acount in Users:
        Accounts.append(acount[0])
else:
    exit()

Count = 1
for User in reversed(Accounts):
    # User = User[0]
    UserData = checkUserReserveData(User)
    UserInfo = getUserAccountData(User)
    totalCollateralBase = '{:,.4f}'.format(UserInfo[0] / 10 ** 8)
    totalDebtBase = '{:,.4f}'.format(UserInfo[1] / 10 ** 8)
    availableBorrowsBase = '{:,.4f}'.format(UserInfo[2] / 10 ** 8)
    currentLiquidationThreshold = UserInfo[3]/ 10 ** 2
    ltv = UserInfo[4]/ 10 ** 2
    UserHF = web3.fromWei(UserInfo[5],'ether')
    # print('--------------------------------------------------------------------------')
    # print(Count)
    print(Count,Fore.LIGHTGREEN_EX + User + Style.RESET_ALL)
    Count += 1
    # print((f"{totalCollateralBase} / {totalDebtBase} / {availableBorrowsBase} / {currentLiquidationThreshold}% / {ltv}% / {'{:.18f}'.format(UserHF)}"))
    # print('------------------------------------------------------')
    totalCollateral = 0
    totalDebtUSD = 0
    Tokens = []
    TokenList = {}
    for token in UserData:
        if(token[2] == True or token[4]>0):
            Tokens.append(token[0])
    TokensPrice = getAssetsPricesAaveOracleV3(Tokens)

    for token in UserData:
        Collateral = ''
        if(token[2] == True or token[4]>0):
            TokenData = ReservesList(token[0])
            TokenName = TokenData[0]
            TokenPrice = TokensPrice[TokenName]
            decimals = TokenData[1]
            if(token[4]>0):
                amount = (token[4] / (10 ** decimals))
                amountUSD = float(amount) * float(TokenPrice)
                totalDebtUSD += amountUSD
                Collateral = 'Debt'
                if(token[2] == True):
                    CollateralAmount = (token[1] / (10 ** decimals))
                    CollateralAmountUSD = float(CollateralAmount) * float(TokenPrice)
                    # print(TokenName.ljust(8), '{:,.6f}'.format(CollateralAmount).ljust(10),'*', '{:,.2f}'.format(TokenPrice).ljust(10), '=', '{:,.4f}'.format(CollateralAmountUSD).ljust(10),'USD', 'Collateral')
                    totalCollateral += CollateralAmountUSD
            elif(token[2] == True):
                # amount = '{:.18f}'.format(web3.fromWei(Token[1],'ether'))
                amount = (token[1] / (10 ** decimals))
                amountUSD = float(amount) * float(TokenPrice)
                Collateral = 'Collateral'
                totalCollateral += amountUSD
            # decimals = TokenData[1]
            # print(TokenName.ljust(8), '{:,.6f}'.format(amount).ljust(10),'*', '{:,.2f}'.format(TokenPrice).ljust(10), '=', '{:,.4f}'.format(amountUSD).ljust(10),'USD', Collateral.ljust(11), token[1], token[4])
    # print('------------------------------------------------------')
    print(f"totalCollateral: {'{:,.2f}'.format(totalCollateral)} USD , totalDebtUSD: {'{:,.2f}'.format(totalDebtUSD)} USD , UserHF: {'{:,.2f}'.format(UserHF)}")
    print('------------------------------------------------------')