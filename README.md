# fintech-blockchain-python-homework

This repository contains custom testnet blockchain, test transaction, library for different
cryptocurrency, accompanied with tools and algorithm as part of the Fintech homework assignment Unit
19—Multi-Blockchain Wallet in Python.

In this homework assignment, we build a portfolio management system that supports not only traditional
assets like gold, silver, stocks, etc, but crypto-assets as well!! As there are so many coins out
there, we use Ethereum and Bitcoin Testnet.  Our task is to understand how HD wallet works and build a
system that can create them.

For creating HD wallet, these are the following tasks:

 - use command line tool, hd-wallet-derive that supports not only BIP32, BIP39, and BIP44.
 - develop and integrate the script wallet.py at backend using Python
 - dependencies list:
     - install PHP
     - clone the [hd-wallet-derive](https://github.com/dan-da/hd-wallet-derive) tool
     - [bit](https://ofek.dev/bit/) Python Bitcoin library.
     - [web3.py](https://github.com/ethereum/web3.py) Python Ethereum library.
     
## Steps to setup a Multi-Blockchain Wallet in Python project

    1. Initial setup:
        - create a project directory called `wallet`
        - clone the `hd-wallet-derive` tool into `wallet` folder
        - create a symlink called `derive` for the hd-wallet-derive/hd-wallet-derive.php script
        - test that you can run the ./derive script 
        
     ![Symlink Derive]("./Screenshots/symlink_derive.png")
         - create a file called `wallet.py`
     
     ![Wallet Tree]("./Screenshots/tree.png")
   
    2. Setup constants:  
        - create a file called `constants.py`
            - BTC = 'btc'
            - ETH = 'eth'
            - BTCTEST = 'btc-test'
        - import all constants `from constants import *` in `wallet.py`

    3. Generate a Mnemonic
        - generate a new 12 word mnemonic using hd-wallet-derive or by using [this tool](https:/
        iancoleman.io/bip39/)
        - set this mnemonic as an environment variable by storing it a an .env file and importing it
        into your wallet.py

    4. Derive the wallet keys
        - create a function called `derive_wallets` that does the following:
            - use the `subprocess` library to create a shell command that calls the `./derive` script
            from Python
            - following flags must be passed into the shell command as variables:
                - mnemonic (--mnemonic) must be set from an environment variable, or default to a test
                mnemonic
                - coin (--coin)
                - numderive (--numderive) to set number of child keys generated
                - format (--format=json) to parse the output into a JSON object using json.loads(output)
    
      ![HD Wallet Derive Execute]("./Screenshots/hd_wallet_derive_execute.png")
      - create a dictionary object called `coins` that uses the `derive_wallets` function to derive
      `ETH` and `BTCTEST` wallets
      
      ![Wallet Object]("./Screenshots/wallet_object.png")
      
    5. Linking the transaction signing libraries
        - Use `bit` and `web3.py` to leverage the keys stored in the `coins` object by creating three
        more functions:
            - priv_key_to_account:
                - function will convert the `privkey` string in a child key to an `account` object that
                `bit` or `web3.py` can use to transact.
                - function needs the following parameters:
                    - coin -- the coin type (defined in constants.py).
                    - priv_key -- the privkey string will be passed through here.
                - check the coin type, then return one of the following functions based on the library:
                    - for ETH, return Account.privateKeyToAccount(priv_key)
                    - For BTCTEST, return PrivateKeyTestnet(priv_key)
            - create_tx:
                - create the raw, unsigned transaction that contains all metadata needed to transact
                - function needs the following parameters:
                    - coin -- the coin type (defined in `constants.py`).
                    - account -- the account object from `priv_key_to_account`.
                    - to -- the recipient address.
                    - amount -- the amount of the coin to send.
                - check the coin type, then return one of the following functions based on the
                    library:
                    - for `ETH`, return an `object` containing `to, from, value, gas, gasPrice,
                        nonce, and chainID`
                    - for `BTCTEST`, return `PrivateKeyTestnet.prepare_transaction(account.address,
                        [(to, amount, BTC)])`
            - send_tx:
                - function will call create_tx, sign the transaction, then send it to the
                    designated network.
                - function needs the following parameters:
                    - coin -- the coin type (defined in `constants.py`)
                    - account -- the account object from `priv_key_to_account`
                    - to -- the recipient address.
                    - amount -- the amount of the coin to send
                - check the `coin`, then create a `raw_tx` object by calling `create_tx`
                - sign the `raw_tx` using `bit` or `web3.py`
                - once signed the transaction, need to send it to the designated blockchain network.
                    - for ETH, return w3.eth.sendRawTransaction(signed.rawTransaction)
                    - for BTCTEST, return NetworkAPI.broadcast_tx_testnet(signed)

        6. Send some transactions
            - Bitcoin Testnet transaction
                - fund a BTCTEST address using this [testnet-faucet](https://testnet-faucet.mempool.co/)
                - use a [block-explorer](https://tbtc.bitaps.com/) to watch transactions on the address.
                - send a transaction to another testnet address (either one of your own, or the 
                   faucet's).
                - screenshot the confirmation of the transaction:
              
       ![BTC TEST]("./Screenshots/btc_test.png")
            - Local PoA Ethereum transaction
                - add ETH addresses `0x7c63fb6a44327EDBC025907B1226e0Fdb04fF6b8` and
              '0x43d7F41ff92104A960bd2365E29fF72Ff26Ba1A2' to the pre-allocated accounts in your
              `terracynet.json`
                - delete the `geth` folder in each node, then re-initialize using 
                    - geth --datadir node1 init terracynet.json
                    - geth --datadir node1 init terracynet.json
                - web3.py to support the PoA algorithm:
                  `from web3.middleware import geth_poa_middleware`
                  `w3.middleware_onion.inject(geth_poa_middleware, layer=0)`
                - due to a bug in `web3.py`, we need to send a transaction or two with `MyCrypto` first, since the `w3.eth.generateGasPrice()` function does not work with an empty chain. We use ETH address privkey, or node keystore files.
                - send a transaction from the MyCrypto wallet account `0x97D71601E848c06c4965b87A77853115BAC5B00b` to ethereum address `0x7c63fb6a44327EDBC025907B1226e0Fdb04fF6b8`
              
       ![ETH Test]("./Screenshots/eth_test.png")