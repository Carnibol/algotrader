# Test algorithm file
from talib import abstract, MA_Type
import pandas

class TestAlgorithm():
    def __init__(self, data):
        self.data = data
        self.setup()

    def setup(self):
        self.defineIndicators()

        self.portfolio = {}
        self.SMAs = {}
        self.EMAs = {}
        self.RSIs = {}
        self.soldToday = []

        for symbol in self.data.keys():
            self.SMAs.update({symbol : self.SMA(self.data[symbol], timeperiod=10, price='close').dropna()})
            self.EMAs.update({symbol : self.EMA(self.data[symbol], timeperiod=500, price='close').dropna()})
            self.RSIs.update({symbol : self.RSI(self.data[symbol], timeperiod=50, price='close', matype=MA_Type.EMA).dropna()})

    def defineIndicators(self):
        # pylint: disable=no-member
        self.SMA = abstract.SMA
        self.EMA = abstract.EMA
        self.RSI = abstract.RSI

    def evaluate(self, date):
        buyTargets = {}
        sellTargets = []

        for symbol in self.data.keys():
            try:
                if(symbol in self.portfolio.keys()):
                    if(self.SMAs[symbol].get(date) >= self.EMAs[symbol].get(date) or self.RSIs[symbol].get(date) > 70):
                        #sellTargets.append(symbol)
                        pass

                elif((self.SMAs[symbol].get(date) < self.EMAs[symbol].get(date) and self.RSIs[symbol].get(date) < 50) and symbol not in self.soldToday):
                    buyTargets.update({symbol : (self.EMAs[symbol].get(date) - self.SMAs[symbol].get(date)) / self.data[symbol].at[date, 'close']})
                    
            except TypeError:
                pass

        return sellTargets, list(dict(sorted(buyTargets.items(), key=lambda x: x[1], reverse=True)))
