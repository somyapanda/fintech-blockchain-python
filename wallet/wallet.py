# Import dependencies
import subprocess
import json
import os
import pprint

# Import necessary functions from bit and web3
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
from dotenv import load_dotenv
from eth_account import Account
from web3 import Web3
from web3.gas_strategies.time_based import medium_gas_price_strategy

# Import constants from constants.py
from constants import *

# Nodes runing with POW
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Load and set environment variables
load_dotenv()
mnemonic = os.getenv("mnemonic")

# Create a function called derive_wallets
def derive_wallets(coin):
    """Use the subprocess library to create a shell command that calls the ./derive script from Python"""
    command = 'php ./derive -g --mnemonic="'+ mnemonic +'" --coin=' + coin + ' --numderive=3 --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {
    ETH: derive_wallets(ETH),
    BTCTEST: derive_wallets(BTCTEST)
}

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(coins)

# Creating a private keys object
eth_privkey = coins[ETH][0]['privkey']
btc_privkey = coins[BTCTEST][0]['privkey']

print(eth_privkey)
print(btc_privkey)

#Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, priv_key):
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)

eth_acc = priv_key_to_account(ETH,eth_privkey)
btc_acc = priv_key_to_account(BTCTEST,btc_privkey) 

print(eth_acc)
print(btc_acc)

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata
def create_tx(coin, account, to, amount):
    if coin == ETH:
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": to, "value": amount}
        )
        return {
            'to': to,
            'from': account.address,
            'value': amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
        }
    elif coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)])
    
# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction
def send_tx(coin, account, to, amount):
    raw_tx = create_tx(coin, account, to, amount)
    signed_tx = account.sign_transaction(raw_tx)
    if coin == ETH:
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(result.hex())
        return result.hex()
    elif coin == BTCTEST:
        return NetworkAPI.broadcast_tx_testnet(signed_tx)
    
# Create BTC transaction
create_tx(BTCTEST, btc_acc, "msVBoDtk9UrSUjPj2n2RhdkeyxjcKiVUCD", 0.001)

# Send BTC transaction
send_tx(BTCTEST,btc_acc,'msVBoDtk9UrSUjPj2n2RhdkeyxjcKiVUCD',0.001)

# Local PoA Ethereum transaction
from web3.middleware import geth_poa_middleware
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
from web3 import Web3, HTTPProvider

# Connecting to HTTP with address pk
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Checking the Block Number
w3.eth.blockNumber

# Double check if I am connected to blockchain.
w3.isConnected()

# Check the Balance of the account with local mining blockchain
w3.eth.getBalance("0x7c63fb6a44327EDBC025907B1226e0Fdb04fF6b8")

create_tx(ETH, eth_acc,"0x43d7F41ff92104A960bd2365E29fF72Ff26Ba1A2", 2000)
send_tx(ETH,eth_acc,"0x43d7F41ff92104A960bd2365E29fF72Ff26Ba1A2", 2000)

# Confirmation of Transaction
w3.eth.getBalance("0x43d7F41ff92104A960bd2365E29fF72Ff26Ba1A2")