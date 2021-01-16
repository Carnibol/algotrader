import datetime
import importlib

import pandas
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tda

from algorithms import TestAlgorithm

class BackTester():
    def __init__(self, algorithm, symbols):
        self.setup(algorithm, symbols)

    def setup(self, algorithm, symbols):
        self.symbols = symbols
        self.startingCash = 3000
        self.stopLoss = 0.85
        self.collectProfit = 1.2
        self.startDate = datetime.datetime(2020,4,16,hour=9)
        self.currentDate = self.startDate
        self.endDate = datetime.datetime(2020,12,31,hour=18)
        self.period = 5 # Minutes
        self.portfolio = {}
        self.data = self.loadData(self.symbols)
        self.prices = {}
        self.stopLosses = {}
        self.collectProfits = {}
        self.breakEvenPrices = {}
        self.boughtToday = []
        self.soldToday = []
        self.dayTrades = {}
        self.dayTradeCount = 0
        self.maxDayTrades = 0
        self.winningTrades = 0
        self.losingTrades = 0
        self.cash = self.startingCash
        self.equity = self.startingCash
        self.maxEquity = self.startingCash
        self.maxDrawdown = 0
        self.algorithm = self.getAlgorithm(algorithm)
        self.datetimes = []
        self.equities = []
        self.cashes = []

    def getAlgorithm(self, algorithm):
        return getattr(importlib.import_module(f'algorithms.{algorithm}'), algorithm)(self.data)

    def buy(self, symbol, shares, price):
        self.portfolio.update({symbol : shares})
        self.cash -= (shares * price)
        self.stopLosses.update({symbol : price * self.stopLoss})
        self.collectProfits.update({symbol : price * self.collectProfit})
        self.breakEvenPrices.update({symbol : price})
        self.boughtToday.append(symbol)
        self.updateEquity()
        self.algorithm.portfolio = self.portfolio
        self.algorithm.boughtToday = self.boughtToday

        print(f'Bought {shares} shares of {symbol}')

    def sell(self, symbol, shares, price):
        self.portfolio.update({symbol : self.portfolio[symbol] - shares})
        self.cash += (shares * price)

        if(self.portfolio[symbol] == 0):
            self.portfolio.pop(symbol)
            self.stopLosses.pop(symbol)
            self.collectProfits.pop(symbol)

            if(price >= self.breakEvenPrices[symbol]):
                self.winningTrades += 1
            else:
                self.losingTrades += 1

            self.breakEvenPrices.pop(symbol)
        else:
            self.breakEvenPrices.update({symbol : ((self.breakEvenPrices[symbol] * (shares + self.portfolio[symbol])) - (shares * price)) / self.portfolio[symbol]})

        self.soldToday.append(symbol)
        self.updateEquity()
        self.algorithm.portfolio = self.portfolio
        self.algorithm.soldToday = self.soldToday

    def liquidate(self):
        for symbol in list(self.portfolio):
            self.sell(symbol, self.portfolio[symbol], self.prices[symbol])

    def updateEquity(self):
        equity = self.cash

        for symbol in self.portfolio.keys():
            equity += (self.portfolio[symbol] * self.prices[symbol])

        self.equity = equity

        if(equity > self.maxEquity):
            self.maxEquity = equity
        elif((1 - (equity / self.maxEquity)) * 100 > self.maxDrawdown):
            self.maxDrawdown = (1 - (equity / self.maxEquity)) * 100

    def updatePrices(self, date):
        for symbol in self.symbols:
            try:
                self.prices.update({symbol : self.data[symbol].at[date, 'close']})
            except KeyError:
                pass

    def loadData(self, symbols):
        data = {}
        for symbol in symbols:
            df = pandas.read_csv(f'historical-data/{symbol}.csv')

            df.infer_objects()
            df.loc[:,'datetime'] = pandas.to_datetime(df.loc[:,'datetime'], infer_datetime_format=True)
            df.set_index('datetime', inplace=True)
            #df.drop('Unnamed: 0', axis=1, inplace=True)

            data.update({symbol : df})

        return data

    def getNextPeriod(self):
        self.updateEquity()
        self.datetimes.append(self.currentDate)
        self.equities.append(self.equity)
        self.cashes.append(self.cash)

        if(self.currentDate.time() >= datetime.time(hour=18)):
            self.checkForDayTrades()
            self.updateDayTrades()

            self.boughtToday = []
            self.soldToday = []
            self.algorithm.soldToday = []
            self.algorithm.boughtToday = []

            self.updateGraph()

            if(self.currentDate.isoweekday() == 5):
                if(len(self.portfolio.keys()) > 0):
                    self.rebalancePortfolio()
                return self.currentDate + datetime.timedelta(days=2, hours=15)
            else:
                return self.currentDate + datetime.timedelta(hours=15)
        else:
            return self.currentDate + datetime.timedelta(minutes=5)

    def rebalancePortfolio(self, newSymbols=0):
        print("REBALANCE")
        self.updateEquity()

        if(newSymbols == 0):
            maxValue = min(self.equity * 0.25, self.equity / len(self.portfolio.keys()))
        else:
            maxValue = self.equity / (len(self.portfolio.keys()) + newSymbols)

        for symbol in list(self.portfolio):
            value = self.portfolio[symbol] * self.prices[symbol]
            if(value > maxValue and maxValue > self.prices[symbol] and symbol not in self.boughtToday):
                self.sell(symbol, -1 * ((maxValue - value) // self.prices[symbol]), self.prices[symbol])
        
    def attemptBuys(self, symbols):
        maxValue = min(self.equity / (len(self.portfolio.keys()) + len(symbols)), self.equity * 0.2)

        for symbol in symbols:
            try:
                shares = max(1, int(maxValue // self.prices[symbol]))

                if(self.prices[symbol] * shares <= self.cash):
                    self.buy(symbol, shares, self.prices[symbol])
            except KeyError:
                pass

    def checkHoldings(self):
        for symbol in list(self.portfolio):
            price = self.prices[symbol]
            if(price >= self.collectProfits[symbol]):
                self.sell(symbol, self.portfolio[symbol], price)
                print('Collect Profit')
            elif(price <= self.stopLosses[symbol]):
                self.sell(symbol, self.portfolio[symbol], price)
                print('Stop Loss')
            elif(price * self.stopLoss > self.stopLosses[symbol]):
                self.stopLosses.update({symbol : price * self.stopLoss})

    def checkForDayTrades(self):
        for symbol in self.boughtToday:
            if(symbol in self.soldToday):
                self.dayTradeCount += 1
                self.dayTrades.update({self.dayTradeCount : 5})

        if(len(self.dayTrades.keys()) > self.maxDayTrades):
            self.maxDayTrades = len(self.dayTrades.keys())

    def updateDayTrades(self):
        for x in list(self.dayTrades):
            self.dayTrades.update({x : self.dayTrades[x] - 1})
            if(self.dayTrades[x] == 0):
                self.dayTrades.pop(x)

    def backtest(self):
        print(f"Backtesting {type(self.algorithm)}")
        plt.ion()

        self.graph, ax = plt.subplots(figsize=(16,10))
        self.line, = ax.plot(self.datetimes, self.equities)

        plt.title("Equity Over Time",fontsize=25)
        plt.xlabel("Datetime",fontsize=18)
        plt.ylabel("Equity",fontsize=18)
        plt.tight_layout()

        while self.currentDate <= self.endDate:
            self.updatePrices(self.currentDate)

            self.checkHoldings()

            sells, buys = self.algorithm.evaluate(self.currentDate)

            for symbol in sells:
                self.sell(symbol, self.portfolio[symbol], self.prices[symbol])

            if(len(buys) != 0):
                #self.rebalancePortfolio(len(buys))
                self.attemptBuys(buys)

            self.currentDate = self.getNextPeriod()

        self.liquidate()
        self.results()

    def updateGraph(self):
        if(self.equity >= self.startingCash):
            graphColor = 'green'
        else:
            graphColor = 'red'

        plt.plot(self.datetimes, self.equities, color=graphColor)
        plt.plot(self.datetimes, self.cashes, color='blue')
        self.graph.canvas.draw()
        self.graph.canvas.flush_events()

    def results(self):
        self.updateEquity()

        if(self.winningTrades + self.losingTrades == 0):
            print('No trades made. Algorithm Sucks.')
            return

        print(f'Total Trades:     {self.winningTrades + self.losingTrades}')
        print(f'Total Day Trades: {self.dayTradeCount}')
        print(f'Max Day Trades:   {self.maxDayTrades}')
        print(f'Winning Trade %:  {(self.winningTrades / (self.winningTrades + self.losingTrades)) * 100}%')
        print(f'Max Drawdown %:   {self.maxDrawdown}%')
        print(f'Ending Equity:    ${self.equity}')
        print(f'Profit/Loss %:    {((self.equity / self.startingCash) * 100) - 100}%')
