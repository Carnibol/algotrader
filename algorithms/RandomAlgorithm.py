# Algorithm to simulate randomly purchasing and selling stocks
import numpy
import random
import pandas

class RandomAlgorithm():
    def __init__(self, data):
        self.data = data
        self.setup()

    def setup(self):
        self.portfolio = {}
        self.symbols = list(self.data.keys())

    def evaluate(self, date):
        buyTargets = []
        sellTargets = []

        x = numpy.random.randint(0, high=11)

        for i in range(0, x): # pylint: disable=unused-variable
            buyTargets.append(random.choice(self.symbols))

        return sellTargets, buyTargets
