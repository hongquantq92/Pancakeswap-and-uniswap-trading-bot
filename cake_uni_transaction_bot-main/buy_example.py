from txns import Txn_bot
import web3
from web3 import Web3
import time


private = '739c45243e8702e2ffce4f62d7af270a0abfa7e3af81b4906e05f31ff1c16231'
bsc = "https://bsc-dataseed.binance.org/"
bsc = "wss://bsc-ws-node.nariox.org:443"
web3x = Web3(Web3.WebsocketProvider(bsc))

# token_address = '0xf9ba5210f91d0474bd1e1dcdaec4c58e359aad85' #Example UNI eth-rinkeby / eth-mainnet
token_address = '0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82' #Example CAKE bsc-mainnet
# token_address = '0xe9e7cea3dedca5984780bafc599bd69add087d56' #BUSD bsc-mainnet
# token_address = "0x73b01a9c8379a9d3009f2351f22583f8b75cc1ba"
# token_address = "0xD40bEDb44C081D2935eebA6eF5a3c8A31A1bBE13"

quantity = web3x.toWei(0.001, 'ether')
net = 'bsc-mainnet'
slippage = 30 #%
gas_price = web3x.toWei('5', 'gwei') #Gwei, bsc-mainnet=5, eth-mainnet=https://www.gasnow.org/, eth-rinkeby=1
bot = Txn_bot(token_address, quantity, net, slippage, gas_price)
tokens = bot.get_amounts_out_buy()
print(tokens)
# bot.buy_token()

