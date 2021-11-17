import importlib
import os
import subprocess
import sys
import traceback
from time import localtime, strftime

import pyetherbalance
from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtTest
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from pycoingecko import CoinGeckoAPI
from web3 import Web3, middleware
from web3 import types
from web3.gas_strategies.time_based import fast_gas_price_strategy

from gui import Ui_MainWindow
from swap import Uniswap

sys.path.insert(0, './')
import configfile
import requests

sys.setrecursionlimit(1500)

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)  # enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)  # use highdpi icons


# Written by Aviddot: https://github.com/aviddot/Pancakeswap-v2-trading-bot
def __ne__(self, other):
    return not self.__eq__(other)


@pyqtSlot(str)
def trap_exc_during_debug(*args):
    if configfile.debugmode == '1':
        exception_type, exception_object, exception_traceback = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


sys.excepthook = trap_exc_during_debug


@pyqtSlot()
class Worker(QObject):
    sig_step = pyqtSignal(int, str)  # worker id, step description: emitted every step through work() loop
    sig_done = pyqtSignal(int)  # worker id: emitted at end of work()
    sig_msg = pyqtSignal(str)  # message to be shown to user

    def __init__(self, id: int):
        super().__init__()
        self.__id = id
        self.__abort = False

    def work(self):
        while self.__abort != True:
            thread_name = QThread.currentThread().objectName()
            thread_id = int(QThread.currentThreadId())  # cast to int() is necessary
            self.sig_msg.emit('Running worker #{} from thread "{}" (#{})'.format(self.__id, thread_name, thread_id))

            if 'step' not in locals():
                step = 1
            else:
                step = 1
            self.sig_step.emit(self.__id, 'step ' + str(step))
            QCoreApplication.processEvents()
            if self.__abort == True:
                # note that "step" value will not necessarily be same for every thread
                self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))

            importlib.reload(configfile)
            w33 = Web3()
            cg = CoinGeckoAPI()
            maxgwei = int(configfile.maxgwei)
            if configfile.maxgweinumber == '':
                maxgweinumber = 0
            else:
                maxgweinumber = int(configfile.maxgweinumber)
            diffdeposit = float(configfile.diffdeposit)
            diffdepositaddress = str(configfile.diffdepositaddress)
            speed = str(configfile.speed)
            max_slippage = float(configfile.max_slippage)
            incaseofbuyinghowmuch = int(configfile.incaseofbuyinghowmuch)
            ethtokeep = int(configfile.ethtokeep)
            timesleepaftertrade = int(configfile.secondscheckingprice_2)
            timesleep = int(configfile.secondscheckingprice)
            infura_url = str(configfile.infuraurl)
            infuraurl = infura_url
            tokentokennumerator = float(configfile.tokentokennumerator)
            mcotoseeassell = float(configfile.mcotoseeassell)
            debugmode = int(configfile.debugmode)

            # Written by Aviddot: https://github.com/aviddot/Pancakeswap-v2-trading-bot
            ##for token_number,eth_address,high,low,activate,stoploss_value,stoploss_activate,trade_with_ERC,trade_with_ETH,fast_token in all_token_information:
            all_token_information = [
                (1, str(configfile.token1ethaddress), float(configfile.token1high), float(configfile.token1low),
                 float(configfile.activatetoken1), float(configfile.token1stoploss), float(configfile.stoplosstoken1)
                 , float(configfile.tradewithERCtoken1), float(configfile.tradewithETHtoken1), '0',
                 str(configfile.token1name), int(configfile.token1decimals)),
                (2, str(configfile.token2ethaddress), float(configfile.token2high), float(configfile.token2low),
                 float(configfile.activatetoken2), float(configfile.token2stoploss), float(configfile.stoplosstoken2)
                 , float(configfile.tradewithERCtoken2), float(configfile.tradewithETHtoken2), '0',
                 str(configfile.token2name), int(configfile.token2decimals)),
                (3, str(configfile.token3ethaddress), float(configfile.token3high), float(configfile.token3low),
                 float(configfile.activatetoken3), float(configfile.token3stoploss), float(configfile.stoplosstoken3)
                 , float(configfile.tradewithERCtoken3), float(configfile.tradewithETHtoken3), '0',
                 str(configfile.token3name), int(configfile.token3decimals)),
                (4, str(configfile.token4ethaddress), float(configfile.token4high), float(configfile.token4low),
                 float(configfile.activatetoken4), float(configfile.token4stoploss), float(configfile.stoplosstoken4)
                 , float(configfile.tradewithERCtoken4), float(configfile.tradewithETHtoken4), '0',
                 str(configfile.token4name), int(configfile.token4decimals)),
                (5, str(configfile.token5ethaddress), float(configfile.token5high), float(configfile.token5low),
                 float(configfile.activatetoken5), float(configfile.token5stoploss), float(configfile.stoplosstoken5)
                 , float(configfile.tradewithERCtoken5), float(configfile.tradewithETHtoken5), '0',
                 str(configfile.token5name), int(configfile.token5decimals)),
                (6, str(configfile.token6ethaddress), float(configfile.token6high), float(configfile.token6low),
                 float(configfile.activatetoken6), float(configfile.token6stoploss), float(configfile.stoplosstoken6)
                 , float(configfile.tradewithERCtoken6), float(configfile.tradewithETHtoken6), '0',
                 str(configfile.token6name), int(configfile.token6decimals)),
                (7, str(configfile.token7ethaddress), float(configfile.token7high), float(configfile.token7low),
                 float(configfile.activatetoken7), float(configfile.token7stoploss), float(configfile.stoplosstoken7)
                 , float(configfile.tradewithERCtoken7), float(configfile.tradewithETHtoken7), '0',
                 str(configfile.token7name), int(configfile.token7decimals)),
                (8, str(configfile.token8ethaddress), float(configfile.token8high), float(configfile.token8low),
                 float(configfile.activatetoken8), float(configfile.token8stoploss), float(configfile.stoplosstoken8)
                 , float(configfile.tradewithERCtoken8), float(configfile.tradewithETHtoken8), '0',
                 str(configfile.token8name), int(configfile.token8decimals)),
                (9, str(configfile.token9ethaddress), float(configfile.token9high), float(configfile.token9low),
                 float(configfile.activatetoken9), float(configfile.token9stoploss), float(configfile.stoplosstoken9)
                 , float(configfile.tradewithERCtoken9), float(configfile.tradewithETHtoken9), '0',
                 str(configfile.token9name), int(configfile.token9decimals)),
                (10, str(configfile.token10ethaddress), float(configfile.token10high), float(configfile.token10low),
                 float(configfile.activatetoken10), float(configfile.token10stoploss), float(configfile.stoplosstoken10)
                 , float(configfile.tradewithERCtoken10), float(configfile.tradewithETHtoken10), '0',
                 str(configfile.token10name), int(configfile.token10decimals))]

            for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, trade_with_ETH, fast_token, small_case_name, decimals in all_token_information:
                if (high < low):
                    print(
                        'Stop the script, a tokenlow is higher than its tokenhigh')
                    count = 0
                    QCoreApplication.processEvents()
                    while self.__abort != True:
                        QCoreApplication.processEvents()
                        pass
                if (stoploss_value > high):
                    print(
                        'Stop the script, a stoploss is higher than the tokenhigh')
                    count = 0
                    QCoreApplication.processEvents()
                    while self.__abort != True:
                        QCoreApplication.processEvents()
                        pass
                if (ethtokeep > mcotoseeassell):
                    print(
                        'The buy/sell boundary is lower than the $ to keep in BNB after trade')
                    count = 0

            my_address = str(configfile.my_address)
            my_pk = str(configfile.my_pk)

            pk = my_pk
            if configfile.maincoinoption == 'BNB':
                ethaddress = "0x0000000000000000000000000000000000000000"
                maindecimals = 18
            if configfile.maincoinoption == 'DAI':
                ethaddress = "0x1af3f329e8be154074d8769d1ffa4ee058b1dbc3"
                maindecimals = 18
            if configfile.maincoinoption == 'BUSD':
                ethaddress = "0xe9e7cea3dedca5984780bafc599bd69add087d56"
                maindecimals = 18
            if configfile.maincoinoption == 'USDC':
                ethaddress = "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d"
                maindecimals = 18
            if configfile.maincoinoption == 'wBTC':
                ethaddress = "0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c"
                maindecimals = 18
            if configfile.maincoinoption == 'ETH':
                ethaddress = "0x2170ed0880ac9a755fd29b2688956bd959f933f8"
                maindecimals = 18
            maincoinname = configfile.maincoinoption
            maincoinoption = ethaddress
            append = QtCore.pyqtSignal(str)

            if 'step' not in locals():
                step = 1
            else:
                step = 1
            self.sig_step.emit(self.__id, 'step ' + str(step))
            QCoreApplication.processEvents()
            if self.__abort == True:
                # note that "step" value will not necessarily be same for every thread
                self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
            totaldollars = 1

            def gettotaltokenbalance(all_token_information, infura_url, ethaddress, maindecimals, my_address,
                                     ethtokeep):
                print('(re)Preparing bot...')
                QCoreApplication.processEvents()
                if 'step' not in locals():
                    step = 1
                else:
                    step = 1
                self.sig_step.emit(self.__id, 'step ' + str(step))
                QCoreApplication.processEvents()
                if self.__abort == True:
                    # note that "step" value will not necessarily be same for every thread
                    self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                ethbalance = pyetherbalance.PyEtherBalance(infura_url)
                priceeth = int(
                    float((requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())['price']))
                threeeth = 1
                ethereum_address = my_address
                try:  # balances
                    if ethaddress == "0x0000000000000000000000000000000000000000":
                        balance_eth = ethbalance.get_eth_balance(my_address)['balance']
                        dollarbalancemaintoken = priceeth * balance_eth
                    else:
                        details = {'symbol': 'potter', 'address': ethaddress, 'decimals': maindecimals,
                                   'name': 'potter'}
                        erc20tokens = ethbalance.add_token('potter', details)
                        balance_eth = ethbalance.get_token_balance('potter', ethereum_address)['balance']
                        maintokeneth = uniswap_wrapper.get_eth_token_input_price(w33.toChecksumAddress(ethaddress),
                                                                                 100)

                        if maindecimals != 18:
                            mainusd = (priceeth / (maintokeneth)) * 100
                        else:
                            mainusd = (priceeth / (maintokeneth)) * 100
                        dollarbalancemaintoken = mainusd * balance_eth

                    if len(all_token_information[0]) > 15:
                        all_token_information[0] = all_token_information[0][:15]
                        all_token_information[1] = all_token_information[1][:15]
                        all_token_information[2] = all_token_information[2][:15]
                        all_token_information[3] = all_token_information[3][:15]
                        all_token_information[4] = all_token_information[4][:15]
                        all_token_information[5] = all_token_information[5][:15]
                        all_token_information[6] = all_token_information[6][:15]
                        all_token_information[7] = all_token_information[7][:15]
                        all_token_information[8] = all_token_information[8][:15]
                        all_token_information[9] = all_token_information[9][:15]
                    if len(all_token_information[0]) > 14:
                        for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:
                            if eth_address != '0' or '':
                                erc20tokens = ethbalance.add_token(small_case_name,
                                                                   {'symbol': small_case_name, 'address': eth_address,
                                                                    'decimals': decimals,
                                                                    'name': small_case_name})
                                a = ethbalance.get_token_balance(small_case_name, ethereum_address)['balance']
                                all_token_information[token_number - 1] = all_token_information[token_number - 1][
                                                                          :12] + (a, all_token_information[
                                    token_number - 1][13], all_token_information[token_number - 1][14])
                            else:
                                a = 0
                                all_token_information[token_number - 1] = all_token_information[token_number - 1][
                                                                          :12] + (a, all_token_information[
                                    token_number - 1][13], all_token_information[token_number - 1][14])
                    else:
                        for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, trade_with_ETH, fast_token, small_case_name, decimals in all_token_information:
                            if eth_address != '0' or '':
                                details = {'symbol': small_case_name, 'address': eth_address, 'decimals': decimals,
                                           'name': small_case_name.upper}
                                erc20tokens = ethbalance.add_token(small_case_name.upper, details)
                                a = ethbalance.get_token_balance(small_case_name.upper, ethereum_address)['balance']
                                all_token_information[token_number - 1] = all_token_information[token_number - 1] + (a,)
                            else:
                                a = 0
                                all_token_information[token_number - 1] = all_token_information[token_number - 1] + (a,)
                    # its now: for token_number,eth_address,high,low,activate,stoploss_value,stoploss_activate,trade_with_ERC,trade_with_ETH,fast_token,small_case_name,decimals,balance in all_token_information:
                # Written by Aviddot: https://github.com/aviddot/Pancakeswap-v2-trading-bot
                except Exception as e:
                    exception_type, exception_object, exception_traceback = sys.exc_info()
                    if configfile.debugmode == '1':
                        print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                QCoreApplication.processEvents()
                if 'step' not in locals():
                    step = 1
                else:
                    step = 1
                self.sig_step.emit(self.__id, 'step ' + str(step))
                QCoreApplication.processEvents()
                if self.__abort == True:
                    # note that "step" value will not necessarily be same for every thread
                    self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                try:  # prices
                    if len(all_token_information[0]) > 15:
                        all_token_information[0] = all_token_information[0][:15]
                        all_token_information[1] = all_token_information[1][:15]
                        all_token_information[2] = all_token_information[2][:15]
                        all_token_information[3] = all_token_information[3][:15]
                        all_token_information[4] = all_token_information[4][:15]
                        all_token_information[5] = all_token_information[5][:15]
                        all_token_information[6] = all_token_information[6][:15]
                        all_token_information[7] = all_token_information[7][:15]
                        all_token_information[8] = all_token_information[8][:15]
                        all_token_information[9] = all_token_information[9][:15]
                    priceeth = int(
                        float((requests.get(
                            'https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())[
                                  'price']))

                    if len(all_token_information[0]) > 14:
                        for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:
                            if str(eth_address) != '0' or '':
                                token1eth = uniswap_wrapper.get_eth_token_input_price(
                                    w33.toChecksumAddress(eth_address),
                                    10000000000000)
                                if decimals != 18:
                                    pricetoken1usd = (priceeth / (token1eth)) / (10 ** (18 - (decimals)))
                                else:
                                    pricetoken1usd = (priceeth / (token1eth))
                                a = pricetoken1usd
                                all_token_information[token_number - 1] = all_token_information[token_number - 1][
                                                                          :13] + (a, all_token_information[
                                    token_number - 1][14])
                            else:
                                a = 0
                                all_token_information[token_number - 1] = all_token_information[token_number - 1][
                                                                          :13] + (a, all_token_information[
                                    token_number - 1][14])
                    else:
                        for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, trade_with_ETH, fast_token, small_case_name, decimals, balance in all_token_information:
                            if str(eth_address) != '0' or '':
                                try:
                                    token1eth = uniswap_wrapper.get_eth_token_input_price(
                                        w33.toChecksumAddress(eth_address),
                                        10000000000000)
                                    if decimals != 18:
                                        pricetoken1usd = (priceeth / (token1eth)) / (10 ** (18 - (decimals)))
                                    else:
                                        pricetoken1usd = (priceeth / (token1eth))
                                    a = pricetoken1usd
                                    all_token_information[token_number - 1] = all_token_information[token_number - 1][:13] + (a,)
                                except Exception as e:
                                    exception_type, exception_object, exception_traceback = sys.exc_info()
                                    if configfile.debugmode == '1':
                                        print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                                        e = (str(e))
                                    if 'Could not decode' in str(e):
                                        try:
                                            kanka = uniconnect.factory_contract.functions.getPair(
                                                w33.toChecksumAddress(eth_address),
                                                token22).call()
                                            kanka2 = uniconnect._load_contract(abi_name="erc20",
                                                                               address=w33.toChecksumAddress(
                                                                                   eth_address)).functions.balanceOf(
                                                kanka).call
                                            if kanka2 < 2:
                                                print(
                                                    'Token ' + str(token_number) + ' has no liquidity on Pancakeswap 2')
                                        except:
                                            print(
                                                'Token ' + str(token_number) + ' has no liquidity on Pancakeswap 2')
                                    b = None
                                    letsgoo = 0

                            else:
                                a = 0
                                all_token_information[token_number - 1] = all_token_information[token_number - 1] + (a,)

                    # its now: for token_number,eth_address,high,low,activate,stoploss_value,stoploss_activate,trade_with_ERC,trade_with_ETH,fast_token,small_case_name,decimals,balance,price in all_token_information:
                except Exception as e:
                    exception_type, exception_object, exception_traceback = sys.exc_info()
                    if configfile.debugmode == '1':
                        print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                totalbalancedollarscript = 0
                if len(all_token_information[0]) > 15:
                    all_token_information[0] = all_token_information[0][:15]
                    all_token_information[1] = all_token_information[1][:15]
                    all_token_information[2] = all_token_information[2][:15]
                    all_token_information[3] = all_token_information[3][:15]
                    all_token_information[4] = all_token_information[4][:15]
                    all_token_information[5] = all_token_information[5][:15]
                    all_token_information[6] = all_token_information[6][:15]
                    all_token_information[7] = all_token_information[7][:15]
                    all_token_information[8] = all_token_information[8][:15]
                    all_token_information[9] = all_token_information[9][:15]
                if len(all_token_information[0]) > 14:
                    for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:
                        if balance != 0:
                            a = price * balance * 100
                            all_token_information[token_number - 1] = all_token_information[token_number - 1][:14] + (
                                a,)
                        else:
                            a = 0
                            all_token_information[token_number - 1] = all_token_information[token_number - 1][:14] + (
                                a,)

                        totalbalancedollarscript += a
                        if token_number == 10:
                            totalbalancedollarscript += dollarbalancemaintoken
                else:
                    for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, trade_with_ETH, fast_token, small_case_name, decimals, balance, price in all_token_information:
                        if balance != 0:
                            a = price * balance * 100
                            all_token_information[token_number - 1] = all_token_information[token_number - 1] + (a,)
                        else:
                            a = 0
                            all_token_information[token_number - 1] = all_token_information[token_number - 1] + (a,)

                        totalbalancedollarscript += a
                        if token_number == 10:
                            totalbalancedollarscript += dollarbalancemaintoken

                # its now: for token_number,eth_address,high,low,activate,stoploss_value,stoploss_activate,trade_with_ERC,
                # trade_with_ETH,fast_token,small_case_name,decimals,balance,price, dollar_balance in all_token_information:

                maintokenbalance = balance_eth
                return {'all_token_information': all_token_information,
                        'totalbalancedollarscript': totalbalancedollarscript,
                        'dollarbalancemaintoken': dollarbalancemaintoken, 'maintokenbalance': maintokenbalance}

            # Written by Aviddot: https://github.com/aviddot/Pancakeswap-v2-trading-bot
            QCoreApplication.processEvents()
            if 'step' not in locals():
                step = 1
            else:
                step = 1
            self.sig_step.emit(self.__id, 'step ' + str(step))
            QCoreApplication.processEvents()
            if self.__abort == True:
                # note that "step" value will not necessarily be same for every thread
                self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))

            def checkbalance(all_token_information, infura_url, my_address, maincoinoption, dollarbalancemaintoken,
                             mcotoseeassell):

                ethereum_address = my_address
                cg = CoinGeckoAPI()

                ethbalance = pyetherbalance.PyEtherBalance(infura_url)

                for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:
                    if (dollarbalancemaintoken > mcotoseeassell):
                        gelukt = "sell"
                    else:
                        lol543 = dollar_balance * 100000000000
                        if lol543 > mcotoseeassell:
                            gelukt = "buy " + small_case_name
                    keer = 0
                    if 'gelukt' not in locals():
                        gelukt = 'nothing'
                QCoreApplication.processEvents()
                if 'step' not in locals():
                    step = 1
                else:
                    step = 1
                self.sig_step.emit(self.__id, 'step ' + str(step))
                QCoreApplication.processEvents()
                if self.__abort == True:
                    # note that "step" value will not necessarily be same for every thread
                    self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:
                    if (dollarbalancemaintoken > mcotoseeassell and gelukt != "sell"):
                        gelukt2 = "sell"
                    else:
                        if dollar_balance > mcotoseeassell and gelukt != 'buy ' + small_case_name:
                            gelukt2 = "buy " + small_case_name
                    keer = 0
                    if 'gelukt2' not in locals():
                        gelukt2 = 'nothing'
                try:
                    gelukt3 = gelukt2
                except:
                    gelukt2 = '0'
                return {'keer': keer, 'gelukt': gelukt, 'gelukt2': gelukt2,
                        'all_token_information': all_token_information}

            def getprice(all_token_information, incaseofbuyinghowmuch, uniswap_wrapper, timesleep, gelukt,
                         maintokenbalance, ethaddress, maindecimals, totalbalancedollarscript):
                count = 0
                try:
                    QCoreApplication.processEvents()
                    # Written by Aviddot: https://github.com/aviddot/Pancakeswap-v2-trading-bot
                    while count < timesleep:
                        count = count + 1
                        QtTest.QTest.qWait(1000)
                        QCoreApplication.processEvents()
                    QtTest.QTest.qWait(166)
                    if ethaddress == "0x0000000000000000000000000000000000000000" and maintokenbalance > 0.001:
                        priceeth = int(float(
                            (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())[
                                'price']))
                        threeeth = int(maintokenbalance * 1000000000000000000)
                    if ethaddress == "0x0000000000000000000000000000000000000000" and maintokenbalance < 0.001:
                        threeeth = 1
                        priceeth = int(float(
                            (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())[
                                'price']))
                    if ethaddress != "0x0000000000000000000000000000000000000000":
                        if ethaddress == "0x1af3f329e8be154074d8769d1ffa4ee058b1dbc3":
                            jajaja = (float(
                                (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BUSDDAI').json())[
                                    'price']))
                            priceeth = int(float(
                                (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())[
                                    'price']))
                            ethtest = (jajaja / priceeth) * maintokenbalance
                            if ethtest < 0.01:
                                threeeth = 1
                            else:
                                threeeth = int((ethtest) * 1000000000000000000)

                        if ethaddress == "0xe9e7cea3dedca5984780bafc599bd69add087d56":
                            jajaja = (float(
                                (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BUSDUSDT').json())[
                                    'price']))
                            priceeth = int(float(
                                (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())[
                                    'price']))
                            ethtest = (jajaja / priceeth) * maintokenbalance

                            if ethtest < 0.01:
                                threeeth = 1
                            else:
                                threeeth = int((ethtest) * 1000000000000000000)

                        if ethaddress == "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d":
                            jajaja = (float(
                                (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=USDCBUSD').json())[
                                    'price']))
                            priceeth = int(float(
                                (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())[
                                    'price']))
                            ethtest = (jajaja / priceeth) * maintokenbalance
                            if ethtest < 0.01:
                                threeeth = 1
                            else:
                                threeeth = int((ethtest) * 1000000000000000000)

                        if ethaddress == "0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c":
                            jajaja = (float(
                                (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT').json())[
                                    'price']))
                            priceeth = int(float(
                                (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())[
                                    'price']))
                            ethtest = (jajaja / priceeth) * maintokenbalance
                            if ethtest < 0.01:
                                threeeth = 1
                            else:
                                threeeth = int((ethtest) * 1000000000000000000)
                        if ethaddress == "0x2170ed0880ac9a755fd29b2688956bd959f933f8":
                            jajaja = (float(
                                (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT').json())[
                                    'price']))
                            priceeth = int(float(
                                (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())[
                                    'price']))
                            ethtest = (jajaja / priceeth) * maintokenbalance
                            if ethtest < 0.01:
                                threeeth = 1
                            else:
                                threeeth = int((ethtest) * 1000000000000000000)
                    QCoreApplication.processEvents()
                    if 'step' not in locals():
                        step = 1
                    else:
                        step = 1
                    self.sig_step.emit(self.__id, 'step ' + str(step))
                    QCoreApplication.processEvents()
                    if self.__abort == True:
                        # note that "step" value will not necessarily be same for every thread
                        self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                    if 'buy' in gelukt:
                        priceright = 'buy'
                        threeeth = int((totalbalancedollarscript / int(float(
                            (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())[
                                'price']))) * 1000000000000000000)
                    else:
                        priceright = 'sell'
                    if ethaddress == "0x0000000000000000000000000000000000000000":
                        dollarbalancemaintoken = maintokenbalance * (priceeth)
                    else:
                        token11eth = uniswap_wrapper.get_token_eth_output_price(w33.toChecksumAddress(ethaddress),
                                                                                threeeth)
                        token11eth2 = token11eth / threeeth

                        if maindecimals != 18:
                            dollarbalancemaintoken = float(maintokenbalance) * ((priceeth / (token11eth2)) / (
                                    10 ** (18 - (maindecimals))))
                        else:
                            dollarbalancemaintoken = maintokenbalance * (priceeth / (token11eth2))
                    priceeth = int(float(
                        (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())['price']))
                    QCoreApplication.processEvents()
                    if 'step' not in locals():
                        step = 1
                    else:
                        step = 1
                    self.sig_step.emit(self.__id, 'step ' + str(step))
                    QCoreApplication.processEvents()
                    if self.__abort == True:
                        # note that "step" value will not necessarily be same for every thread
                        self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))

                    for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, \
                        trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:
                        if eth_address != '0':
                            if priceright == 'sell':
                                token1eth = uniswap_wrapper.get_eth_token_input_price(
                                    w33.toChecksumAddress(eth_address),
                                    threeeth)
                                token1eth2 = token1eth / threeeth
                                if decimals != 18:
                                    pricetoken1usd = (priceeth / (token1eth2)) / (10 ** (18 - (decimals)))
                                    dollarbalancetoken1 = pricetoken1usd * balance
                                    all_token_information[token_number - 1] = all_token_information[token_number - 1][
                                                                              :13] + (
                                                                                  pricetoken1usd, dollarbalancetoken1)
                                else:
                                    pricetoken1usd = (priceeth / (token1eth2))
                                    dollarbalancetoken1 = pricetoken1usd * balance
                                    if eth_address == '0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d':
                                        pricetoken1usd = 1.032319
                                    all_token_information[token_number - 1] = all_token_information[token_number - 1][
                                                                              :13] + (
                                                                                  pricetoken1usd, dollarbalancetoken1)
                            else:
                                token1eth = uniswap_wrapper.get_token_eth_output_price(
                                    w33.toChecksumAddress(eth_address),
                                    threeeth)
                                token1eth2 = (token1eth / threeeth)
                                if decimals != 18:
                                    pricetoken1usd = (priceeth / (token1eth2)) / (10 ** (18 - (decimals)))
                                    dollarbalancetoken1 = pricetoken1usd * balance
                                    all_token_information[token_number - 1] = all_token_information[token_number - 1][
                                                                              :13] + (
                                                                                  pricetoken1usd, dollarbalancetoken1)
                                else:
                                    pricetoken1usd = (priceeth / (token1eth2))
                                    dollarbalancetoken1 = pricetoken1usd * balance
                                    if eth_address == '0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d':
                                        pricetoken1usd = 1.032319
                                    all_token_information[token_number - 1] = all_token_information[token_number - 1][
                                                                              :13] + (
                                                                                  pricetoken1usd, dollarbalancetoken1)
                        else:
                            pricetoken1usd = 0
                            dollarbalancetoken1 = 0
                            all_token_information[token_number - 1] = all_token_information[token_number - 1][:13] + (
                                pricetoken1usd, dollarbalancetoken1)
                    # Written by Aviddot: https://github.com/aviddot/Pancakeswap-v2-trading-bot
                    weergave = ''

                    for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, \
                        trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:
                        if eth_address != '0' and activate == 1:
                            weergave += ('   [' + small_case_name + '  ' + str("{:.8f}".format(price)) + ']')
                    QCoreApplication.processEvents()
                    if 'step' not in locals():
                        step = 1
                    else:
                        step = 1
                    self.sig_step.emit(self.__id, 'step ' + str(step))
                    QCoreApplication.processEvents()
                    if self.__abort == True:
                        # note that "step" value will not necessarily be same for every thread
                        self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                    return {'all_token_information': all_token_information, 'priceeth': priceeth, 'weergave': weergave,
                            'dollarbalancemaintoken': dollarbalancemaintoken}
                except Exception as e:
                    o = 0
                    exception_type, exception_object, exception_traceback = sys.exc_info()
                    if configfile.debugmode == '1':
                        print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))

            def letstrade(all_token_information, keer, my_address, pk, max_slippage,
                          infura_url, gelukt,
                          tokentokennumerator,
                          weergave, notyet, priceeth, speed, maxgwei, maxgweinumber, diffdeposit, diffdepositaddress,
                          maindecimals, timesleepaftertrade):
                QCoreApplication.processEvents()
                if 'step' not in locals():
                    step = 1
                else:
                    step = 1
                self.sig_step.emit(self.__id, 'step ' + str(step))
                QCoreApplication.processEvents()
                if self.__abort == True:
                    # note that "step" value will not necessarily be same for every thread
                    self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, \
                    trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:
                    QCoreApplication.processEvents()
                    for token_number2, eth_address2, high2, low2, activate2, stoploss_value2, stoploss_activate2, trade_with_ERC2, \
                        trade_with_ETH2, fast_token2, small_case_name2, decimals2, balance2, price2, dollar_balance2 in all_token_information:
                        if eth_address != eth_address2:
                            if eth_address != 0 and eth_address2 != 0:
                                if price > ((high + low) / 2) and price2 < (
                                        (high2 + low2) / 2):
                                    locals()['token%stotoken%s' % (str(token_number), str(token_number2))] = ((
                                                                                                                      price - low) / (
                                                                                                                      high - low)) / (
                                                                                                                     (
                                                                                                                             price2 - low2) / (
                                                                                                                             high2 - low2))
                                else:
                                    locals()['token%stotoken%s' % (str(token_number), str(token_number2))] = 0.1
                            else:
                                locals()['token%stotoken%s' % (str(token_number), str(token_number2))] = 0.1

                def makeTrade(buytokenaddress, selltokenaddress, my_address, pk, max_slippage, infura_url,
                              buysmallcasesymbol, sellsmallcasesymbol, ethtokeep, speed, maxgwei, maxgweinumber,
                              diffdeposit, diffdepositaddress, ethaddress):
                    selldecimals = 18
                    try:
                        def api(speed):
                            res = requests.get(
                                'https://data-api.defipulse.com/api/v1/egs/api/ethgasAPI.json?api-key=f2ff6e6755c2123799676dbe8ed3af94574000b4c9b56d1f159510ec91b0')
                            data = int(res.json()[speed] / 10)
                            return data

                        # Written by Aviddot: https://github.com/aviddot/Pancakeswap-v2-trading-bot
                        print(
                            'Current gwei chosen for trading:' + configfile.maxgweinumber + '.   Current BNB price:$' + str(
                                int(float(
                                    (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())[
                                        'price']))))
                        gwei = types.Wei(Web3.toWei(int(configfile.maxgweinumber), "gwei"))

                    except Exception as e:
                        o = 0
                        exception_type, exception_object, exception_traceback = sys.exc_info()
                        if configfile.debugmode == '1':
                            print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                        w33.eth.setGasPriceStrategy(fast_gas_price_strategy)
                    if 1 == 1:

                        try:
                            uniconnect = Uniswap(my_address, pk, web3=Web3(
                                w33.HTTPProvider(infura_url)),
                                                 version=2, max_slippage=max_slippage)
                            eth = Web3.toChecksumAddress(selltokenaddress)
                            token = w33.toChecksumAddress(buytokenaddress)
                            selldecimals = 18
                        except Exception as e:
                            exception_type, exception_object, exception_traceback = sys.exc_info()
                            if configfile.debugmode == '1':
                                print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                        try:
                            if selltokenaddress == "0x0000000000000000000000000000000000000000":
                                ethbalance = pyetherbalance.PyEtherBalance(infura_url)
                                balance_eth = ethbalance.get_eth_balance(my_address)
                                priceeth = int(float(
                                    (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())[
                                        'price']))
                                ethamount2 = (float(balance_eth['balance'])) - (
                                        ethtokeep / (float(priceeth)))
                            else:
                                ethbalance = pyetherbalance.PyEtherBalance(infura_url)
                                balance_eth = ethbalance.get_eth_balance(my_address)['balance']
                                token2 = sellsmallcasesymbol.upper
                                details2 = {'symbol': sellsmallcasesymbol.upper, 'address': selltokenaddress,
                                            'decimals': selldecimals,
                                            'name': sellsmallcasesymbol.upper}
                                erc20tokens2 = ethbalance.add_token(token2, details2)
                                ethamount2 = ethbalance.get_token_balance(token2, ethereum_address)['balance']
                            tradeamount = ethamount2 * 10 ** selldecimals
                            ethamount = tradeamount
                            eth = Web3.toChecksumAddress(selltokenaddress)
                            token = w33.toChecksumAddress(buytokenaddress)
                            contractaddress = token
                        except Exception as e:
                            o = 0
                            exception_type, exception_object, exception_traceback = sys.exc_info()
                            if configfile.debugmode == '1':
                                print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                        tradeamount = int((ethamount2 / 1.000000001) * 10 ** selldecimals)
                        if len(str(tradeamount)) > 2:
                            tradeamount = int(str(tradeamount)[:-4] + '0000')
                        if tradeamount < 0:
                            tradeamount = int(1)

                        ethamount = ethamount2
                        contractaddress = token
                        if int(diffdeposit) == 0:
                            uniconnect.make_trade(eth, token, tradeamount, gwei, my_address, pk, my_address)
                        if int(diffdeposit) == 1:
                            uniconnect.make_trade(eth, token, tradeamount, gwei, my_address, pk, diffdepositaddress)

                        if buytokenaddress == ethaddress:
                            gelukt = 'sell'
                        if buytokenaddress != ethaddress:
                            gelukt = 'buy ' + buysmallcasesymbol
                        return {'gelukt': gelukt}
                    else:
                        print(
                            'Current gwei chosen for trading:' + configfile.maxgweinumber + '.   Current BNB price:$' + str(
                                int(float(
                                    (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())[
                                        'price']))))
                        gelukt = 'mislukt'
                        return {'gelukt': gelukt}

                QCoreApplication.processEvents()
                if 'step' not in locals():
                    step = 1
                else:
                    step = 1
                self.sig_step.emit(self.__id, 'step ' + str(step))
                QCoreApplication.processEvents()
                if self.__abort == True:
                    # note that "step" value will not necessarily be same for every thread
                    self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))

                try:
                    for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:  # stop loss
                        if (
                                price < stoploss_value and stoploss_activate == 1 and activate == 1 and trade_with_ETH == 1 and gelukt == "buy " + small_case_name) or (
                                price < stoploss_value and activate == 1 and trade_with_ETH == 1 and gelukt2 == "buy " + small_case_name and stoploss_activate == 1):
                            print("Selling " + str(
                                small_case_name) + ' for Maincoin-option (current price in USD: ' + str(
                                price) + ')')
                            buysmallcasesymbol = 'eth'
                            kaka = makeTrade(buytokenaddress=ethaddress, selltokenaddress=eth_address,
                                             my_address=my_address,
                                             pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                             buysmallcasesymbol=buysmallcasesymbol,
                                             sellsmallcasesymbol=small_case_name, ethtokeep=ethtokeep, speed=speed,
                                             maxgwei=maxgwei, maxgweinumber=maxgweinumber, diffdeposit=diffdeposit,
                                             diffdepositaddress=diffdepositaddress, ethaddress=ethaddress)
                            gelukt = kaka['gelukt']
                            if gelukt != 'mislukt':
                                count = 0
                                while count < timesleepaftertrade:
                                    count += 1
                                    QtTest.QTest.qWait(1000)
                                    QCoreApplication.processEvents()
                                    if self.__abort == True:
                                        count += 100
                            keer = 9999
                            fasttoken1 = 0
                            all_token_information[token_number - 1] = all_token_information[token_number - 1][:9] + (
                                fasttoken1, all_token_information[token_number - 1][10],
                                all_token_information[token_number - 1][11], all_token_information[token_number - 1][12],
                                all_token_information[token_number - 1][13], all_token_information[token_number - 1][14])
                        if (
                                eth_address != 0) and activate == 1 and trade_with_ETH == 1:  # sell alt and buy ETH trades
                            if (price > high and gelukt == "buy " + small_case_name) or (
                                    price > high and gelukt2 == "buy " + small_case_name) or (
                                    activate == 1 and gelukt == 'buy ' + small_case_name and fast_token == 1):
                                print("Selling " + str(
                                    small_case_name) + ' for Maincoin-option (current price in USD: ' + str(
                                    price) + ')')
                                buysmallcasesymbol = 'eth'
                                kaka = makeTrade(buytokenaddress=ethaddress, selltokenaddress=eth_address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=buysmallcasesymbol,
                                                 sellsmallcasesymbol=small_case_name, ethtokeep=ethtokeep, speed=speed,
                                                 maxgwei=maxgwei, maxgweinumber=maxgweinumber, diffdeposit=diffdeposit,
                                                 diffdepositaddress=diffdepositaddress, ethaddress=ethaddress)
                                gelukt = kaka['gelukt']
                                if gelukt != 'mislukt':
                                    count = 0
                                    while count < timesleepaftertrade:
                                        count += 1
                                        QtTest.QTest.qWait(1000)
                                        QCoreApplication.processEvents()
                                        if self.__abort == True:
                                            count += 100
                                        if 'step' not in locals():
                                            step = 1
                                        else:
                                            step = 1
                                        self.sig_step.emit(self.__id, 'step ' + str(step))
                                        QCoreApplication.processEvents()
                                        if self.__abort == True:
                                            # note that "step" value will not necessarily be same for every thread
                                            self.sig_msg.emit(
                                                'Worker #{} aborting work at step {}'.format(self.__id, step))
                                keer = 9999
                                fasttoken1 = 0
                                all_token_information[token_number - 1] = all_token_information[token_number - 1][
                                                                          :9] + (fasttoken1, all_token_information[
                                    token_number - 1][10], all_token_information[token_number - 1][11],
                                                                                 all_token_information[
                                                                                     token_number - 1][12],
                                                                                 all_token_information[
                                                                                     token_number - 1][13],
                                                                                 all_token_information[
                                                                                     token_number - 1][14])
                        if (eth_address != 0) and activate == 1 and trade_with_ETH == 1:  # sell ETH and buy ALT
                            if (price < low and gelukt == "sell") or (
                                    price < low and gelukt2 == "sell"):
                                print(
                                    "Buying " + str(small_case_name) + ' (Current price: ' + str(
                                        float(price)) + ')')

                                sellsmallcasesymbol = 'eth'
                                kaka = makeTrade(buytokenaddress=eth_address, selltokenaddress=ethaddress,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=small_case_name,
                                                 sellsmallcasesymbol=sellsmallcasesymbol, ethtokeep=ethtokeep,
                                                 speed=speed,
                                                 maxgwei=maxgwei, maxgweinumber=maxgweinumber, diffdeposit=diffdeposit,
                                                 diffdepositaddress=diffdepositaddress, ethaddress=ethaddress)
                                gelukt = kaka['gelukt']
                                if gelukt != 'mislukt':
                                    count = 0
                                    while count < timesleepaftertrade:
                                        count += 1
                                        QtTest.QTest.qWait(1000)
                                        QCoreApplication.processEvents()
                                        if self.__abort == True:
                                            count += 100
                                        if 'step' not in locals():
                                            step = 1
                                        else:
                                            step = 1
                                        self.sig_step.emit(self.__id, 'step ' + str(step))
                                        QCoreApplication.processEvents()
                                        if self.__abort == True:
                                            # note that "step" value will not necessarily be same for every thread
                                            self.sig_msg.emit(
                                                'Worker #{} aborting work at step {}'.format(self.__id, step))
                                keer = 9999
                        QCoreApplication.processEvents()
                        for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, \
                            trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:
                            QCoreApplication.processEvents()
                            for token_number2, eth_address2, high2, low2, activate2, stoploss_value2, stoploss_activate2, trade_with_ERC2, \
                                trade_with_ETH2, fast_token2, small_case_name2, decimals2, balance2, price2, dollar_balance2 in all_token_information:
                                if eth_address2 != eth_address:
                                    if (eth_address != 0) and (
                                            eth_address2 != 0) and activate == 1 and trade_with_ETH == 1 \
                                            and activate2 == 1 and trade_with_ETH2 == 1 and trade_with_ERC == 1 and trade_with_ERC2 == 1:
                                        if (
                                                locals()['token%stotoken%s' % (str(token_number), str(
                                                    token_number2))] > tokentokennumerator and gelukt == "buy " + small_case_name) or (
                                                locals()['token%stotoken%s' % (str(token_number), str(
                                                    token_number2))] > tokentokennumerator and gelukt2 == "buy " + small_case_name):
                                            print("Trading " + str(small_case_name) + ' ($' + str(
                                                price) + ') for ' + str(small_case_name2) + " ($" + str(
                                                price2) + ")")
                                            # Written by Aviddot: https://github.com/aviddot/Pancakeswap-v2-trading-bot
                                            kaka = makeTrade(buytokenaddress=eth_address2, selltokenaddress=eth_address,
                                                             my_address=my_address,
                                                             pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                             buysmallcasesymbol=small_case_name2,
                                                             sellsmallcasesymbol=small_case_name, ethtokeep=ethtokeep,
                                                             speed=speed, maxgwei=maxgwei, maxgweinumber=maxgweinumber,
                                                             diffdeposit=diffdeposit,
                                                             diffdepositaddress=diffdepositaddress,
                                                             ethaddress=ethaddress)
                                            gelukt = kaka['gelukt']
                                            if gelukt != 'mislukt':
                                                count = 1
                                                while count < timesleepaftertrade:
                                                    count += 1
                                                    if self.__abort == True:
                                                        count += 100
                                                    QtTest.QTest.qWait(1000)
                                                    QCoreApplication.processEvents()
                                                    if 'step' not in locals():
                                                        step = 1
                                                    else:
                                                        step = 1
                                                    self.sig_step.emit(self.__id, 'step ' + str(step))
                                                    QCoreApplication.processEvents()
                                                    if self.__abort == True:
                                                        # note that "step" value will not necessarily be same for every thread
                                                        self.sig_msg.emit(
                                                            'Worker #{} aborting work at step {}'.format(self.__id,
                                                                                                         step))
                                            keer = 9999
                        QCoreApplication.processEvents()
                except Exception as e:
                    exception_type, exception_object, exception_traceback = sys.exc_info()
                    traceback.print_exc()
                    if configfile.debugmode == '1':
                        print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                    gelukt = 'mislukt'
                return {'gelukt': gelukt, 'keer': keer, 'all_token_information': all_token_information}

            if 'step' not in locals():
                step = 1
            else:
                step = 1
            QCoreApplication.processEvents()
            self.sig_step.emit(self.__id, 'step ' + str(step))
            QCoreApplication.processEvents()
            if self.__abort == True:
                # note that "step" value will not necessarily be same for every thread
                self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
            # def marketordersell():
            # def marketorderbuy():

            # def preapproval():

            # def recharge():

            # paytokenholding
            if 0 == 1:
                details2 = {'symbol': paytokensmallname, 'address': paytokenaddress,
                            'decimals': paytokendecimals,
                            'name': paytokenname}
                erc20tokens2 = ethbalance.add_token(token2, details2)
                ethamount2 = ethbalance.get_token_balance(paytokenname, my_address)['balance']
                QCoreApplication.processEvents()
                if ethamount2 < paytokenamount:
                    print("You are not holding the required token, the application will now stop")
                    exit()
                    subprocess.call(["taskkill", "/F", "/IM", "bot.exe"])
                    QtTest.QTest.qWait(4294960 * 1000)
            if 'step' not in locals():
                step = 1
            else:
                step = 1
            self.sig_step.emit(self.__id, 'step ' + str(step))
            QCoreApplication.processEvents()

            if self.__abort == True:
                # note that "step" value will not necessarily be same for every thread
                self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
            while self.__abort != True:
                w3 = Web3(Web3.HTTPProvider(infura_url))
                w33 = Web3()
                address = my_address
                private_key = my_pk
                QCoreApplication.processEvents()
                uniswap_wrapper = Uniswap(address, private_key, web3=w3, version=2)
                ethereum_address = address
                pieuw = gettotaltokenbalance(all_token_information, infura_url, ethaddress, maindecimals, my_address,
                                             ethtokeep)
                QCoreApplication.processEvents()
                all_token_information = pieuw['all_token_information']
                totalbalancedollarscript = pieuw['totalbalancedollarscript']
                dollarbalancemaintoken = pieuw['dollarbalancemaintoken']
                maintokenbalance = pieuw['maintokenbalance']
                try:
                    w33 = Web3()
                    try:
                        def api(speed):
                            res = requests.get(
                                'https://data-api.defipulse.com/api/v1/egs/api/ethgasAPI.json?api-key=f2ff6e6755c2123799676dbe8ed3af94574000b4c9b56d1f159510ec91b0')
                            data = (res.json()[speed]) / 10
                            return data

                        gwei = int(configfile.maxgweinumber)
                        print(
                            'Current gwei chosen for trading:' + configfile.maxgweinumber + '.   Current BNB price:$' + str(
                                int(float(
                                    (requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json())[
                                        'price']))))

                    except Exception as e:
                        o = 0
                        exception_type, exception_object, exception_traceback = sys.exc_info()
                        if configfile.debugmode == '1':
                            print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                        # w33.eth.setGasPriceStrategy(fast_gas_price_strategy)
                    w33.middleware_onion.add(middleware.time_based_cache_middleware)
                    w33.middleware_onion.add(middleware.latest_block_based_cache_middleware)
                    w33.middleware_onion.add(middleware.simple_cache_middleware)
                    w3 = Web3(Web3.HTTPProvider(infura_url))
                    QCoreApplication.processEvents()
                    keer543 = 0
                    for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, \
                        trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:
                        if (eth_address == '0' or '') or activate == 0:
                            keer543 += 1
                    # Written by Aviddot: https://github.com/aviddot/Pancakeswap-v2-trading-bot
                    if keer543 == 10:
                        print(
                            'Please stop the application and add at least token1, otherwise the application will do nothing. Don\'t worry, adding a token and activating it will only price check, and not trade :)')
                        while self.__abort != True:
                            QCoreApplication.processEvents()
                            pass
                    address = my_address
                    private_key = my_pk
                    QCoreApplication.processEvents()
                    uniswap_wrapper = Uniswap(address, private_key, web3=w3, version=2)
                    ethereum_address = address
                    if 'gelukt' not in locals() or gelukt == "mislukt" or gelukt == "mislukt buy" or gelukt == "mislukt sell":
                        if 'step' not in locals():
                            step = 1
                        else:
                            step = step + 1
                        self.sig_step.emit(self.__id, 'step ' + str(step))
                        QCoreApplication.processEvents()

                        if self.__abort == True:
                            # note that "step" value will not necessarily be same for every thread
                            self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                        rara = checkbalance(all_token_information, infura_url, my_address, maincoinoption,
                                            dollarbalancemaintoken, mcotoseeassell)
                        all_token_information = rara['all_token_information']
                        gelukt = rara['gelukt']
                        gelukt2 = rara['gelukt2']
                        keer = rara['keer']

                        print('Last thing we did is ' + gelukt + '. Second token available for trading is ' + gelukt2)
                    if 'step' not in locals():
                        step = 1
                    else:
                        step = step + 1
                    QCoreApplication.processEvents()
                    while self.__abort != True:
                        # check if we need to abort the loop; need to process events to receive signals;
                        self.sig_step.emit(self.__id, 'step ' + str(step))
                        QCoreApplication.processEvents()
                        if self.__abort == True:
                            # note that "step" value will not necessarily be same for every thread
                            self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                        keer = keer + 1
                        QCoreApplication.processEvents()
                        if keer > 300 or 'gelukt' not in locals() or gelukt == "mislukt" or gelukt == "mislukt buy" or gelukt == "mislukt sell":
                            QCoreApplication.processEvents()
                            pieuw = gettotaltokenbalance(all_token_information, infura_url, ethaddress, maindecimals,
                                                         my_address, ethtokeep)
                            all_token_information = pieuw['all_token_information']
                            totalbalancedollarscript = pieuw['totalbalancedollarscript']
                            dollarbalancemaintoken = pieuw['dollarbalancemaintoken']
                            maintokenbalance = pieuw['maintokenbalance']
                            QCoreApplication.processEvents()
                            rara = checkbalance(all_token_information, infura_url, my_address, maincoinoption,
                                                dollarbalancemaintoken, mcotoseeassell)
                            all_token_information = rara['all_token_information']
                            gelukt = rara['gelukt']
                            gelukt2 = rara['gelukt2']
                            keer = rara['keer']
                            QCoreApplication.processEvents()
                        QCoreApplication.processEvents()
                        try:
                            if "weergave" in locals():
                                weergave1 = weergave
                            if 'step' not in locals():
                                step = 1
                            else:
                                step = step + 1
                            self.sig_step.emit(self.__id, 'step ' + str(step))
                            QCoreApplication.processEvents()

                            if self.__abort == True:
                                # note that "step" value will not necessarily be same for every thread
                                self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                            ku = getprice(all_token_information, incaseofbuyinghowmuch, uniswap_wrapper, timesleep,
                                          gelukt, maintokenbalance, ethaddress, maindecimals, totalbalancedollarscript)

                            QCoreApplication.processEvents()
                            weergave12 = ku['weergave']
                            weergave = weergave12
                            priceeth = ku['priceeth']
                            all_token_information = ku['all_token_information']

                            totaldollars = dollarbalancemaintoken + all_token_information[0][14] + \
                                           all_token_information[1][14] + all_token_information[2][14] + \
                                           all_token_information[3][14] + all_token_information[4][14] + \
                                           all_token_information[5][14] + all_token_information[6][14] + \
                                           all_token_information[7][14] + all_token_information[8][14] + \
                                           all_token_information[9][14]

                            QCoreApplication.processEvents()
                            weergavegeld = str(configfile.maincoinoption) + ':$' + str(
                                "{:.2f}".format(dollarbalancemaintoken))
                            for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, \
                                trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:
                                totaldollars += dollar_balance
                                if dollar_balance > 0:
                                    weergavegeld += '   ' + str(small_case_name) + ':$' + str(
                                        "{:.2f}".format(dollar_balance))
                            if 'nogeenkeer' not in locals():
                                nogeenkeer = 1
                                print('Current balance:  ' + weergavegeld)
                            else:
                                nogeenkeer = nogeenkeer + 1
                                if nogeenkeer > 300:
                                    print('Current balance:  ' + weergavegeld)
                                    nogeenkeer = 1
                            if 'step' not in locals():
                                step = 1
                            else:
                                step = step + 1
                            self.sig_step.emit(self.__id, 'step ' + str(step))
                            QCoreApplication.processEvents()
                            if self.__abort == True:
                                # note that "step" value will not necessarily be same for every thread
                                self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                                break

                            if 'pricetoken1usd2' in locals() and 0 == 1:
                                for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, \
                                    trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:
                                    if price / locals()['pricetoken%susd2' % (
                                            str(token_number))] >= 1.15 and price > low and gelukt == 'buy ' + small_case_name:
                                        all_token_information[token_number - 1] = all_token_information[
                                                                                      token_number - 1][:9] + (1,
                                                                                                               all_token_information[
                                                                                                                   token_number - 1][
                                                                                                                   10],
                                                                                                               all_token_information[
                                                                                                                   token_number - 1][
                                                                                                                   11],
                                                                                                               all_token_information[
                                                                                                                   token_number - 1][
                                                                                                                   12],
                                                                                                               all_token_information[
                                                                                                                   token_number - 1][
                                                                                                                   13],
                                                                                                               all_token_information[
                                                                                                                   token_number - 1][
                                                                                                                   14])
                                        all_token_information[token_number - 1] = all_token_information[
                                                                                      token_number - 1][:2] + (
                                                                                      price / 1.09, all_token_information[
                                                                                          token_number - 1][4],
                                                                                      all_token_information[
                                                                                          token_number - 1][5],
                                                                                      all_token_information[
                                                                                          token_number - 1][6],
                                                                                      all_token_information[
                                                                                          token_number - 1][7],
                                                                                      all_token_information[
                                                                                          token_number - 1][8],
                                                                                      all_token_information[
                                                                                          token_number - 1][9],
                                                                                      all_token_information[
                                                                                          token_number - 1][10],
                                                                                      all_token_information[
                                                                                          token_number - 1][11],
                                                                                      all_token_information[
                                                                                          token_number - 1][12],
                                                                                      all_token_information[
                                                                                          token_number - 1][13],
                                                                                      all_token_information[
                                                                                          token_number - 1][14])
                            if 1 == 1:
                                for token_number, eth_address, high, low, activate, stoploss_value, stoploss_activate, trade_with_ERC, \
                                    trade_with_ETH, fast_token, small_case_name, decimals, balance, price, dollar_balance in all_token_information:
                                    locals()['pricetoken%susd2' % (str(token_number))] = \
                                        all_token_information[token_number - 1][13]

                            notyet = 1
                            if 'step' not in locals():
                                step = 1
                            else:
                                step = step + 1
                            self.sig_step.emit(self.__id, 'step ' + str(step))
                            QCoreApplication.processEvents()

                            if self.__abort == True:
                                # note that "step" value will not necessarily be same for every thread
                                self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                                break
                            if totaldollars < 0:
                                totaldollars2 = 0
                            else:
                                if (totaldollars * 0.9) > (all_token_information[0][14] + all_token_information[1][14] +
                                                           all_token_information[2][14] + all_token_information[3][14] +
                                                           all_token_information[4][14] + all_token_information[5][14] +
                                                           all_token_information[6][14] + all_token_information[7][14] +
                                                           all_token_information[8][14] + all_token_information[9][14]):
                                    if dollarbalancemaintoken < mcotoseeassell:
                                        totaldollars = totaldollars / 2
                                totaldollars2 = totaldollars
                            if "weergave1" not in locals() and "notyet" in locals():
                                print(str(strftime("%H:%M:%S",
                                                   localtime())) + weergave + "  Current total balance($): $" + str(
                                    "{:.2f}".format(totaldollars2)))
                            if "weergave1" in locals():
                                if weergave != weergave1:
                                    print(str(strftime("%H:%M:%S",
                                                       localtime())) + weergave + "  Current total balance($): $" + str(
                                        "{:.2f}".format(totaldollars2)))
                        # Written by Aviddot: https://github.com/aviddot/Pancakeswap-v2-trading-bot
                        except Exception as e:
                            exception_type, exception_object, exception_traceback = sys.exc_info()
                            if configfile.debugmode == '1':
                                print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                            if e is not IndexError:
                                o = 0
                                exception_type, exception_object, exception_traceback = sys.exc_info()
                                if configfile.debugmode == '1':
                                    print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                            if 'step' not in locals():
                                step = 1
                            else:
                                step = step + 1
                            self.sig_step.emit(self.__id, 'step ' + str(step))
                            QCoreApplication.processEvents()

                            if self.__abort == True:
                                # note that "step" value will not necessarily be same for every thread
                                self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                                break
                            QtTest.QTest.qWait(1000)
                            notyet = 0
                        if 'notyet' not in locals():
                            notyet = 0
                        else:
                            notyet = notyet + 1
                        if notyet > 0:
                            if 'step' not in locals():
                                step = 1
                            else:
                                step = step + 1
                            self.sig_step.emit(self.__id, 'step ' + str(step))
                            QCoreApplication.processEvents()

                            if self.__abort == True:
                                # note that "step" value will not necessarily be same for every thread
                                self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                                break
                            oke = letstrade(all_token_information, keer, my_address, pk, max_slippage, infura_url,
                                            gelukt, tokentokennumerator, weergave, notyet, priceeth, speed, maxgwei,
                                            maxgweinumber, diffdeposit, diffdepositaddress, maindecimals,
                                            timesleepaftertrade)
                            all_token_information = oke['all_token_information']
                            gelukt = oke['gelukt']
                            gelukt2 = oke['gelukt']
                            keer = oke['keer']



                except Exception as e:
                    if 'step' not in locals():
                        step = 1
                    else:
                        step = step + 1
                    self.sig_step.emit(self.__id, 'step ' + str(step))
                    QCoreApplication.processEvents()

                    if self.__abort == True:
                        # note that "step" value will not necessarily be same for every thread
                        self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                        break
                    exception_type, exception_object, exception_traceback = sys.exc_info()
                    if configfile.debugmode == '1':
                        print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                    if e is not IndexError:
                        o = 0
                        exception_type, exception_object, exception_traceback = sys.exc_info()
                        if configfile.debugmode == '1':
                            print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                        # o=0
                    import socket

                    def is_connected():
                        try:
                            # connect to the host -- tells us if the host is actually
                            # reachable
                            socket.create_connection(("1.1.1.1", 53))
                            return True
                        except OSError:
                            pass
                        return False

                    internetcheck = is_connected()
                    if internetcheck is False:
                        try:
                            count = 0
                            while self.__abort != True or count < 5:
                                count += 1
                                QtTest.QTest.qWait(1000)
                                QCoreApplication.processEvents()
                        except:
                            count = 0
                            while self.__abort != True or count < 5:
                                count += 1
                                QtTest.QTest.qWait(1000)
                                QCoreApplication.processEvents()
                    if 'step' not in locals():
                        step = 1
                    else:
                        step = step + 1
                    self.sig_step.emit(self.__id, 'step ' + str(step))
                    QCoreApplication.processEvents()
                    if self.__abort == True:
                        # note that "step" value will not necessarily be same for every thread
                        self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
            if 'step' not in locals():
                step = 1
            else:
                step = step + 1
            self.sig_step.emit(self.__id, 'step ' + str(step))
            QCoreApplication.processEvents()

            if self.__abort == True:
                # note that "step" value will not necessarily be same for every thread
                self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
            self.sig_done.emit(self.__id)

    # Written by Aviddot: https://github.com/aviddot/Pancakeswap-v2-trading-bot
    def abort(self):
        self.sig_msg.emit('Worker #{} notified to abort'.format(self.__id))
        self.__abort = True


# def funtie voor toevoeging tokens en automaties make trade met elkaar maken --> done alleen testen
# GUI maken en gebruiken mey pyqt desinger
# functie maken voor auto high low
# winst toevoegen tijdens runtime (hiervoor extra configfiletje maken)
# GUI maken mey pyqt desinger

def abort(self):
    self.__abort = True


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    lollol = ui.setupUi(MainWindow)
    lollol2 = MainWindow.show()
    try:
        sys.exit(app.exec_())
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        if configfile.debugmode == '1':
            print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
    print(lollol2)
