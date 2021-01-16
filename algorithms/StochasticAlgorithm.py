# Test algorithm file
from talib import abstract, MA_Type
import pandas

class StochasticAlgorithm():
    def __init__(self, data):
        self.data = data
        self.setup()

    def setup(self):
        self.defineIndicators()

        self.portfolio = {}
        self.kSTOCHs = {}
        self.dSTOCHs = {}
        self.soldToday = []
        self.boughtToday = []

        for symbol in self.data.keys():
            k, d = self.STOCH(self.data[symbol].loc[:,'high'], self.data[symbol].loc[:,'low'], self.data[symbol].loc[:,'close'], 
                                fastk_period=100, slowk_period=50, slowk_matype=MA_Type.EMA, slowd_period=10, slowd_matype=MA_Type.EMA)
            k = pandas.Series(k)
            d = pandas.Series(d)
            k.set_axis(self.data[symbol].index, inplace=True)
            d.set_axis(self.data[symbol].index, inplace=True)            
            self.kSTOCHs.update({symbol : k.dropna()})
            self.dSTOCHs.update({symbol : d.dropna()})

    def defineIndicators(self):
        # pylint: disable=no-member
        self.STOCH = abstract.STOCH

    def evaluate(self, date):
        buyTargets = {}
        sellTargets = []

        for symbol in self.data.keys():
            try:
                if(symbol in self.portfolio.keys()):
                    if((self.kSTOCHs[symbol].get(date) <= self.dSTOCHs[symbol].get(date) or self.dSTOCHs[symbol].get(date) > 80) and symbol not in self.boughtToday):
                        #sellTargets.append(symbol)
                        pass

                elif(30 > self.kSTOCHs[symbol].get(date) >= self.dSTOCHs[symbol].get(date) and symbol not in self.soldToday):
                    buyTargets.update({symbol : self.kSTOCHs[symbol].get(date) - self.dSTOCHs[symbol].get(date)})
                    
            except TypeError:
                pass

        return sellTargets, list(dict(sorted(buyTargets.items(), key=lambda x: x[1], reverse=True)))
