import json
from web3 import HTTPProvider, Web3
import mysql.connector
from mysql.connector import Error
import hashlib
from datetime import datetime
import time
def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

Network = 'Local'
# Network = 'Polygon'
# web3 = Web3(HTTPProvider('http://127.0.0.1:8545',request_kwargs={'timeout': 30}))
# web3 = Web3(HTTPProvider('https://polygon-rpc.com/',request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://poly-mainnet.gateway.pokt.network/v1/lb/fb2da9793f63bcbc71fd8f0c', request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://poly-rpc.gateway.pokt.network', request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://polygon.blockpi.network/v1/rpc/public', request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://polygon-mainnet.blastapi.io/fa940a80-11dc-43e6-b0dc-03d6607ddece', request_kwargs={'timeout': 180}))
web3 = Web3(HTTPProvider('https://polygon-mainnet.g.alchemy.com/v2/JOGYiBYYVqQJUCF1UsNqcPWNhJixWaLO',request_kwargs={'timeout': 180}))
# web3 = Web3(HTTPProvider('https://polygon.blockpi.network/v1/rpc/35d20c87d2999a6cfd1971aec2edbc4824ed530a', request_kwargs={'timeout': 180}))
web3_llamarpc = Web3(HTTPProvider('https://polygon.llamarpc.com/rpc/01GTP6RCY2TT1JHMMCSDQEMHRE', request_kwargs={'timeout': 180}))
# web3_alchemy = Web3(HTTPProvider('https://polygon-mainnet.g.alchemy.com/v2/JOGYiBYYVqQJUCF1UsNqcPWNhJixWaLO',request_kwargs={'timeout': 180}))
web3_polygon_rpc = Web3(HTTPProvider('https://polygon-rpc.com/',request_kwargs={'timeout': 180}))

PoolAddressesProviderV3_address = web3.toChecksumAddress("0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb")
UiPoolDataProviderV3_address = web3.toChecksumAddress("0x8F1AD487C9413d7e81aB5B4E88B024Ae3b5637D0")
AaveOracleV3_address = web3.toChecksumAddress("0xb023e699F5a33916Ea823A16485e259257cA8Bd1")
with open("../scripts/AaveOracleV3ABI.json") as f:
    AaveOracleV3ABI = json.load(f)
    AaveOracleV3ABI = AaveOracleV3ABI['result']
AaveOracleV3_Contract = web3_polygon_rpc.eth.contract(address=AaveOracleV3_address, abi=AaveOracleV3ABI)
contract_address = web3.toChecksumAddress("0x794a61358D6845594F94dc1DB02A252b5b4814aD")
with open("../scripts/AavePoolV3ABI.json") as f:
    ABI = json.load(f)
    ABI = ABI['result']
contract = web3_llamarpc.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=ABI)
# contract = web3_polygon_rpc.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=ABI)


with open("../scripts/UiPoolDataProviderV3.json") as f:
    ABI = json.load(f)
    ABI_AAVEUiPoolDataProviderV3 = ABI['result']
UiPoolDataProviderV3Contract = web3.eth.contract(address=Web3.toChecksumAddress(UiPoolDataProviderV3_address), abi=ABI_AAVEUiPoolDataProviderV3)

def getAssetsPricesAaveOracleV3(Tokens): #(變數使用Token Address)
    TokenList = {}
    Price = AaveOracleV3_Contract.functions.getAssetsPrices(Tokens).call()
    x = 0
    for Token in Tokens:
        TokenName = ReservesList(Token)
        TokenList[TokenName[0]] = Price[x]/10**8
        x += 1
    return TokenList

def getUserAccountData(Account):
    UserInfo = contract.functions.getUserAccountData(Account).call()
    return UserInfo

def getAaveAccountsByNumber(Number):
    db_connection = mysql.connector.connect(
    host='127.0.0.1',
    port='3306',
    database='arbfinder',
    user='gamepig',
    password='<@Gamepig1976@>'
    )
    db_cursor = db_connection.cursor(buffered=True)
    sql=f"SELECT account FROM arbfinder.AAVE_UserAccount ORDER BY ID DESC LIMIT {Number}"
    db_cursor.execute(sql)
    UserAccounts = db_cursor.fetchall()
    rc = db_cursor.rowcount
    db_connection.commit()
    db_cursor.close()
    db_connection.close()
    if(rc <= 0):
        return

    return UserAccounts

def getAaveAccounts():
    db_connection = mysql.connector.connect(
    host='127.0.0.1',
    port='3306',
    database='arbfinder',
    user='gamepig',
    password='<@Gamepig1976@>'
    )
    db_cursor = db_connection.cursor(buffered=True)
    sql='SELECT * FROM arbfinder.AAVE_UserAccount'
    db_cursor.execute(sql)
    AllUserAccount = db_cursor.fetchall()
    rc = db_cursor.rowcount
    db_connection.commit()
    db_cursor.close()
    db_connection.close()
    if(rc <= 0):
        return

    return AllUserAccount

def getOraclePriceFeed(Token):
    ContractInfor = getOraclePriceFeedContractAddress(Token)
    ContractAddress = web3.toChecksumAddress(ContractInfor[0])
    decimals = ContractInfor[1]
    with open("../scripts/ChainlinkPriceOraclesABI.json") as f:
        ABI = json.load(f)
        ABI = ABI['result']
        8. 

    Contract = web3.eth.contract(address=ContractAddress, abi=ABI)
    Price = Contract.functions.latestAnswer().call()
    return Price

def getOraclePriceFeedContractAddress(Token):
    decimals = 8
    match Token:
        case 'DAI':
            return '0x4746DeC9e833A82EC7C2C1356372CcF2cfcD2F3D', decimals
        case 'LINK':
            return '0xd9FFdb71EbE7496cC440152d43986Aae0AB76665',decimals
        case 'USDC':
            return '0xfE4A8cc5b5B2366C1B58Bea3858e81843581b2F7',decimals
        case 'WBTC':
            return '0xDE31F8bFBD8c84b5360CFACCa3539B938dd78ae6',decimals
        case 'WETH':
            return '0xF9680D99D6C9589e2a93a78A04A279e509205945',decimals
        case 'USDT':
            return '0x0A6513e40db6EB1b165753AD52E80663aeA50545',decimals
        case 'AAVE':
            return '0x72484B12719E23115761D5DA1646945632979bB6',decimals
        case 'WMATIC':
            return '0xAB594600376Ec9fD91F8e885dADF0CE036862dE0',decimals
        case 'CRV':
            return '0x336584C8E6Dc19637A5b36206B1c79923111b405',decimals
        case 'SUSHI':
            return '0x49B0c695039243BBfEb8EcD054EB70061fd54aa0',decimals
        case 'GHST':
            return '0xDD229Ce42f11D8Ee7fFf29bDB71C7b81352e11be',decimals
        case 'BAL':
            return '0xD106B538F2A868c28Ca1Ec7E298C3325E0251d66',decimals
        case 'agEUR':
            return '0x9b88d07B2354eF5f4579690356818e07371c7BeD',decimals
        case 'miMATIC':
            return '0xd8d483d813547CfB624b8Dc33a00F2fcbCd2D428',decimals
        case 'stMATIC':
            return '0x97371dF4492605486e23Da797fA68e55Fc38a13f',decimals
        case 'MaticX':
            return '0x5d37E4b374E6907de8Fc7fb33EE3b0af403C7403',decimals
        case 'DPI':
            return '0xC70aAF9092De3a4E5000956E672cDf5E996B4610',decimals
        case _:
            return 'error'

def AAVE_RiskParameters(token):
    match token:
        case 'DAI':
            return 0.975, 0.02
        case 'USDC':
            return 0.975, 0.02
        case 'USDT':
            return 0.975, 0.02
        case 'EURS':
            return 0.975, 0.02
        case 'agEUR':
            return 0.975, 0.02
        case 'jEUR':
            return 0.975, 0.02
        case _:
            return 0

def checkUserReserveData(User):
    User = web3.toChecksumAddress(User)
    UserData = UiPoolDataProviderV3Contract.functions.getUserReservesData(PoolAddressesProviderV3_address,User).call()
    UserData = UserData[0]

    return UserData

def checkUserReserveNumbers():
    pass

def calculateFromWei(amount, decimals):
    if(decimals==2,6,8):
        am = amount/(10**decimals)
        return am
    elif(decimals==18):
        am = web3.fromWei(amount, 'ether')
        return am

def ReservesList(Token):
    match Token:
        case '0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063':
            return 'DAI',18
        case '0x53E0bca35eC356BD5ddDFebbD1Fc0fD03FaBad39':
            return 'LINK',18
        case '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174':
            return 'USDC',6
        case '0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6':
            return 'WBTC',8
        case '0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619':
            return 'WETH',18
        case '0xc2132D05D31c914a87C6611C10748AEb04B58e8F':
            return 'USDT',6
        case '0xD6DF932A45C0f255f85145f286eA0b292B21C90B':
            return 'AAVE',18
        case '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270':
            return 'WMATIC',18
        case '0x172370d5Cd63279eFa6d502DAB29171933a610AF':
            return 'CRV',18
        case '0x0b3F868E0BE5597D5DB7fEB59E1CADBb0fdDa50a':
            return 'SUSHI',18
        case '0x385Eeac5cB85A38A9a07A70c73e0a3271CfB54A7':
            return 'GHST',18
        case '0x9a71012B13CA4d3D0Cdc72A177DF3ef03b0E76A3':
            return 'BAL',18
        case '0x85955046DF4668e1DD369D2DE9f3AEB98DD2A369':
            return 'DPI',18
        case '0xE111178A87A3BFf0c8d18DECBa5798827539Ae99':
            return 'EURS',2
        case '0x4e3Decbb3645551B8A19f0eA1678079FCB33fB4c':
            return 'jEUR',18
        case '0xE0B52e49357Fd4DAf2c15e02058DCE6BC0057db4':
            return 'agEUR',18
        case '0xa3Fa99A148fA48D14Ed51d610c367C61876997F1':
            return 'miMATIC',18
        case '0x3A58a54C066FdC0f2D55FC9C89F0415C92eBf3C4':
            return 'stMATIC',18
        case '0xfa68FB4628DFF1028CFEc22b4162FCcd0d45efb6':
            return 'MaticX',18
        case '0x03b54A6e9a984069379fae1a4fC4dBAE93B3bCCD':
            return 'wstETH',18

def DeleteAAVEUserAccount(account):
    db_connection = mysql.connector.connect(
    host='127.0.0.1',
    port='3306',
    database='arbfinder',
    user='gamepig',
    password='<@Gamepig1976@>'
    )
    db_cursor = db_connection.cursor()
    sql = "DELETE FROM arbfinder.AAVE_UserAccount WHERE account='"+account+"'"
    db_cursor.execute(sql)
    db_connection.commit()
    db_cursor.close()
    db_connection.close()
    
def Insert_aave_UserAccount(account):
    db_connection = mysql.connector.connect(
    host='127.0.0.1',
    port='3306',
    database='arbfinder',
    user='gamepig',
    password='<@Gamepig1976@>'
    )
    db_cursor = db_connection.cursor()
    sql = "SELECT EXISTS(SELECT * FROM arbfinder.AAVE_UserAccount WHERE account='"+account+"')"
    db_cursor.execute(sql)
    for records in db_cursor:  # type: ignore # get data by list
        if(records[0]==0):
            db_cursor2 = db_connection.cursor()
            sql = "INSERT  INTO arbfinder.AAVE_UserAccount (account) VALUES ('"+account+"')"
            db_cursor2.execute(sql)
            db_connection.commit()
            db_cursor2.close()

    db_cursor.close()
    db_connection.close()
    
def ErrorLog(Type,e):
    # Time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    # ErrMessage = {
    #     "TIME":Time,
    #     "TYPE":str(Type),
    #     "MSG":str(e)
    # }
    # with open("ErrorLog.json", "r", errors='ignore') as file:
    #             data = json.load(file)
    #             data.append(ErrMessage)
    # with open("ErrorLog.json", "w", errors='ignore') as file:
    #     json.dump(data, file, indent=4)
    Error_Log = str(e)
    if(len(Error_Log)>200):
        Error_Log = 'Error massage string too long'
    db_connection = mysql.connector.connect(
        host='127.0.0.1',
        port='3306',
        database='arbfinder',
        user='gamepig',
        password='<@Gamepig1976@>'
    )
    db_cursor = db_connection.cursor()
    sql = "INSERT INTO arbfinder.ErrorLog (type, ErrMSG) VALUES (%s, %s)"
    val = (Type, Error_Log)
    db_cursor.execute(sql, val)
    db_connection.commit()
    db_cursor.close()
    db_connection.close()
    
def TokenAddress(Token):
    return {
        'MATIC': '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE',
        'DAI': '0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063',
        'USDC': '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174',
        'USDT': '0xc2132D05D31c914a87C6611C10748AEb04B58e8F',
        'WBTC': '0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6',
        'WETH': '0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619',
        'WMATIC': '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270',
        'LINK': '0x53E0bca35eC356BD5ddDFebbD1Fc0fD03FaBad39',
        'UNI': '0xb33EaAd8d922B1083446DC23f610c2567fB5180f',
        'AAVE': '0xD6DF932A45C0f255f85145f286eA0b292B21C90B',
        'SUSHI': '0x0b3F868E0BE5597D5DB7fEB59E1CADBb0fdDa50a',
        'BAL': '0x9a71012B13CA4d3D0Cdc72A177DF3ef03b0E76A3',
        'DPI': '0x85955046DF4668e1DD369D2DE9f3AEB98DD2A369',
        'stMATIC': '0x3A58a54C066FdC0f2D55FC9C89F0415C92eBf3C4',
        'MaticX': '0xfa68FB4628DFF1028CFEc22b4162FCcd0d45efb6',
        'EURS': '0xE111178A87A3BFf0c8d18DECBa5798827539Ae99',
        'jEUR': '0x4e3Decbb3645551B8A19f0eA1678079FCB33fB4c',
        'agEUR': '0xE0B52e49357Fd4DAf2c15e02058DCE6BC0057db4',
        'miMATIC': '0xa3Fa99A148fA48D14Ed51d610c367C61876997F1'
    }.get(Token, 'error')

def getPrivate_Key(key):
    with open("MetaMask_Private_Keys.json", 'r') as PK_file:
    # with open("Private_Keys.json", 'r') as PK_file:
        data = json.load(PK_file)
        for keys in data:
            if(keys['Account'] == key):
                return keys['Private_Key']

def getContractAddress(contractName):
    with open("./AppSettings.json", "r") as file:
        data = json.load(file)
        data = data[Network]
    address = data.get(contractName)
    return address

def approve_token(token, spender_address, wallet_address, private_key, amount):

    contract = web3.toChecksumAddress(token)
    with open("../build/contracts/IERC20.json") as f:
        info_json = json.load(f)
        abi = info_json["abi"]
    contract = web3.eth.contract(address=contract, abi=abi)
    _owner = web3.toChecksumAddress(wallet_address)
    _spender = web3.toChecksumAddress(spender_address)
    spender = _spender
    
    # for Content in txn_receipt:
    #     print(Content)

    # print(f"allowance: { x }")
    
    nonce = web3.eth.getTransactionCount(_owner)
    
    payload = {
        "gasPrice": web3.eth.gasPrice,
        "gas": 245000,
        "chainId": 137,
        "from": _owner,
        "nonce": nonce,
    }
    
    tx = contract.functions.approve(spender, amount).buildTransaction(payload)  # type: ignore

    signed_tx = web3.eth.account.signTransaction(tx, private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    txn_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    allowance = contract.functions.allowance(_owner, _spender).call()
    if txn_receipt['status'] == 1:
        status = ("transaction successful.")
    else:
        status = ("transaction fail")
        
    return status, allowance

def getAccounts():

    db_connection = mysql.connector.connect(
        host='127.0.0.1',
        port='3306',
        database='arbfinder',
        user='gamepig',
        password='<@Gamepig1976@>'
    )
    Account = []
    result = []
    db_cursor = db_connection.cursor()
    sqlstr = "select * from accounts where inuse = 0 and type = 'MetaMask' and account_balance > 1 order by LastUsed"
    # sqlstr = "select * from accounts where inuse = 0 and type = 'Local' and account_balance > 1 order by LastUsed"
    db_cursor.execute(sqlstr)
    # db_cursor.callproc('get_accounts')
    
    # for result in db_cursor.stored_results():
    #     print(result.fetchall())
    for records in db_cursor:  # type: ignore # get data by list
        id = records[0]
        account = records[1]
        key = records[2]
        result = {'id': id, 'account': account, 'key': key}
        Account.append(result)
        # print(id, account, key)
        # del AccountInfo[0][0]
    db_connection.commit()
    db_cursor.close()
    db_connection.close()
    
    return Account
    
def getAccount(accountList):
    account = accountList[0]['account']
    key = accountList[0]['key']
    del accountList[0]
    accountForuse = account, key
    return accountForuse
    
def upDateAccountSts(account, inuse, eventid):
    db_connection = mysql.connector.connect(
        host='127.0.0.1',
        port='3306',
        database='arbfinder',
        user='gamepig',
        password='<@Gamepig1976@>'
    )
    db_cursor = db_connection.cursor()
    sqlstr = f"UPDATE accounts SET LastEventid = '{eventid}', inuse = {inuse}, LastUsed = '{str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))}' where account = '{str(account)}'"
    db_cursor.execute(sqlstr)
    db_connection.commit()
    db_connection.close()
    
def upDateAccountSts1(account, inuse):
    db_connection = mysql.connector.connect(
        host='127.0.0.1',
        port='3306',
        database='arbfinder',
        user='gamepig',
        password='<@Gamepig1976@>'
    )
    db_cursor = db_connection.cursor()
    sqlstr = f"UPDATE accounts SET inuse = {inuse} where account = '{str(account)}'"
    db_cursor.execute(sqlstr)
    db_connection.commit()
    db_connection.close()

def UpdateAccountBalance():
    db_connection = mysql.connector.connect(
        host='127.0.0.1',
        port='3306',
        database='arbfinder',
        user='gamepig',
        password='<@Gamepig1976@>'
    )
    Accounts = []
    result = []
    db_cursor = db_connection.cursor()
    # sqlstr = "select * from accounts where type = 'Local' order by LastUsed"
    sqlstr = "select * from accounts where type = 'MetaMask' order by LastUsed"
    db_cursor.execute(sqlstr)
    for records in db_cursor:  # type: ignore # get data by list
        id = records[0]
        account = records[1]
        key = records[2]
        result = {'id': id, 'account': account, 'private_key': key}
        Accounts.append(result)
        # print(id, account, key)
        # del AccountInfo[0][0]
    
    WMATIC_Address = web3.toChecksumAddress(TokenAddress('WMATIC'))
    USDC_Address = web3.toChecksumAddress(TokenAddress('USDC'))

    with open("../build/contracts/IERC20.json") as f:
        info_json = json.load(f)
        abi = info_json["abi"]

    WMATIC_Contract = web3.eth.contract(address=WMATIC_Address, abi=abi)
    USDC_Contract = web3.eth.contract(address=USDC_Address, abi=abi)
    # account = web3.eth.accounts[0]
    accountNumber = 0
    MainAccount = web3.toChecksumAddress('0x85D6EceC4F3cD8AE8DF22dcE8437085B4C2A1E4a')
    # MainAccount = web3.toChecksumAddress(web3.eth.accounts[0])
    private_key = 'c5f5b4c1575d03c2960567ee70c325151b46db3762cdf0694301509ded6e0db1'
    # private_key = '0x1c5e00deeb6b03a1176b76c7ddc91f2dbad518b4a6fa3a8266cd3fa663296561'
    for account in Accounts:
        account = web3.toChecksumAddress(account['account'])
        MATIC = float(web3.fromWei(web3.eth.getBalance(account),'ether'))
        WMATIC = float(web3.fromWei(WMATIC_Contract.functions.balanceOf(account).call(),'ether'))
        USDC = float(USDC_Contract.functions.balanceOf(account).call()/1e6)
        # --MetaMask帳號手續費分配
        # if(MATIC<5):
        #     NewAmount = 25 - MATIC
        #     # NewAmount = 25
        #     # SendMATIC(MainAccount, account, NewAmount, private_key)
        #     MATIC = web3.fromWei(web3.eth.getBalance(account),'ether')
        #     WMATIC = web3.fromWei(WMATIC_Contract.functions.balanceOf(account).call(),'ether')
        #     USDC = (USDC_Contract.functions.balanceOf(account).call()/1e6)
        sqlstr = f"UPDATE accounts SET account_balance = {MATIC}, account_balance_WMATIC = {WMATIC}, account_balance_USDC = {USDC} where account ='{account}'"
        db_cursor.execute(sqlstr)
        db_connection.commit()
    db_cursor.close()
    db_connection.close()

    return True

def SendMATIC(_fromAccount, _toAccount, amount, private_key):
    #get the nonce.  Prevents one from sending the transaction twice
    nonce = web3.eth.getTransactionCount(_fromAccount)

    #build a transaction in a dictionary
    tx = {
        'nonce': nonce,
        'to': _toAccount,
        'value': web3.toWei(amount, 'ether'),
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei')
    }

    #sign the transaction
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)

    #send transaction
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    txn_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    #get transaction hash
    return(txn_receipt)

def checkWMATICbalance(account):
    account = web3.toChecksumAddress(account)
    WMATIC_Address = web3.toChecksumAddress(TokenAddress('WMATIC'))
    with open("../build/contracts/IERC20.json") as f:
        info_json = json.load(f)
        abi = info_json["abi"]
    WMATIC_Contract = web3.eth.contract(address=WMATIC_Address, abi=abi)
    WMATIC = WMATIC_Contract.functions.balanceOf(account).call()
    # WMATIC = float(web3.fromWei(WMATIC_Contract.functions.balanceOf(account).call(), 'ether'))
    return WMATIC

def checkUSDCbalance(account):
    account = web3.toChecksumAddress(account)
    USDC_Address = web3.toChecksumAddress(TokenAddress('USDC'))
    with open("../build/contracts/IERC20.json") as f:
        info_json = json.load(f)
        abi = info_json["abi"]
    USDC_Contract = web3.eth.contract(address=USDC_Address, abi=abi)
    USDC = USDC_Contract.functions.balanceOf(account).call()
    # USDC = float(web3.fromWei(USDC_Contract.functions.balanceOf(account).call(), 'ether'))
    return USDC

def UnWrappWmatic(account):
    account = web3.toChecksumAddress(account)
    private_key = getPrivate_Key(0)
    # WMATIC = web3.toChecksumAddress('0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270')
    # with open("../build/contracts/WMATICABI.json") as f:
    #     # UniswapABI = json.load(f)
    #     abi = json.load(f)
    #     abi = abi['result']

    # WMATIC_Contract = web3.eth.contract(address=WMATIC, abi=abi)
    balanceOfWMATIC = checkWMATICbalance(account)
    if(int(balanceOfWMATIC) > 1):
        nonce = web3.eth.getTransactionCount(account)
        buid_Trans_withdraw = {
            'from': account,
            'gas': 500000,
            'gasPrice': web3.toWei('50', 'gwei'),
            'nonce': nonce,
            'value': 0
        }
        transaction = WMATIC_Contract.functions.withdraw(balanceOfWMATIC).buildTransaction(buid_Trans_withdraw)# type: ignore
        signed_tx = web3.eth.account.signTransaction(transaction, private_key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        txn_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

def QuickSwap(account, TokenIn, TokenOut, amount):
    QuickswapRouter = web3.toChecksumAddress('0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff')

    TokenIn = web3.toChecksumAddress(TokenAddress(TokenIn))
    TokenOut = web3.toChecksumAddress(TokenAddress(TokenOut))
    TokenPath = [TokenIn, TokenOut]
    _amountIn = amount
    # _amountIn = web3.toWei(amount, 'ether')
    account = web3.toChecksumAddress(account)
    private_key = getPrivate_Key(0)
    with open("../build/contracts/QuickswapRouter.json") as f:
        abi = json.load(f)
        QuickswapABI = abi['result']
    Quickswap = web3.eth.contract(address=QuickswapRouter, abi=QuickswapABI)
    approve_token(TokenIn, QuickswapRouter, account, private_key, _amountIn)
    nonce = web3.eth.getTransactionCount(account)
    buid_Trans = {
        'from': account,
        'gas': 245000,
        'gasPrice': web3.toWei('50', 'gwei'),
        'nonce': nonce,
        'chainId': 137
    }
    time_stamp = time.time()
    transaction = Quickswap.functions.swap_quickswap(_amountIn, 1, TokenPath, account, time_stamp).buildTransaction(buid_Trans)  # type: ignore
    signed_tx = web3.eth.account.signTransaction(transaction, private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    txn_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
