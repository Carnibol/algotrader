# Test algorithm file
from talib import abstract, MA_Type
import pandas

class EMACrossAlgorithm():
    def __init__(self, data):
        self.data = data
        self.setup()

    def setup(self):
        self.defineIndicators()

        self.portfolio = {}
        self.fastEMAs = {}
        self.slowEMAs = {}
        self.RSIs = {}
        self.soldToday = []
        self.boughtToday = []

        for symbol in self.data.keys():
            self.fastEMAs.update({symbol : self.EMA(self.data[symbol], timeperiod=100, price='close').dropna()})
            self.slowEMAs.update({symbol : self.EMA(self.data[symbol], timeperiod=400, price='close').dropna()})
            self.RSIs.update({symbol : self.RSI(self.data[symbol], timeperiod=50, price='close', matype=MA_Type.EMA).dropna()})

    def defineIndicators(self):
        # pylint: disable=no-member
        self.EMA = abstract.EMA
        self.RSI = abstract.RSI

    def evaluate(self, date):
        buyTargets = {}
        sellTargets = []

        for symbol in self.data.keys():
            try:
                if(symbol in self.portfolio.keys()):
                    if(self.slowEMAs[symbol].get(date) > self.fastEMAs[symbol].get(date) and symbol not in self.boughtToday):
                        #sellTargets.append(symbol)
                        pass

                elif(self.fastEMAs[symbol].get(date) > self.slowEMAs[symbol].get(date) and self.RSIs[symbol].get(date) < 50 and symbol not in self.soldToday):
                    buyTargets.update({symbol : (self.fastEMAs[symbol].get(date) - self.slowEMAs[symbol].get(date)) / self.data[symbol].at[date, 'close']})
                    
            except TypeError:
                pass

        return sellTargets, list(dict(sorted(buyTargets.items(), key=lambda x: x[1], reverse=True)))
