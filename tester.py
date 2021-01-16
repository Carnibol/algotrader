import tda
from tda.client import Client
from tda.streaming import StreamClient

import asyncio
import json
import csv
import datetime
import pandas

import secrets

#Class to test various functionalities without changing anything important
class Tester():
    def __init__(self):
        self.authenticate()

        symbols = ['AAL','ADT','AEG','AES','AGNC','AIG','AMAT','AMD','APA','ATUS','ATVI','AUY','AVTR','AZN','BAC','BBVA','BCS','BHC','BILI','BK','BKR','BLDP','BMY','BNTX','BP','BSX','BTG','C','CARR','CCJ','CCL','CHL','CHWY','CIEN','CLF','CMCSA','CNHI','CNP','CNQ','COG','COP','COTY','CPRI','CSCO','CSX','CTVA','CVE','CVS','CVX','CX','D','DAL','DB','DBX','DD','DDOG','DELL','DHI','DISH','DKNG','DVN','DXC','EBAY','ELAN','ENB','EPD','EQNR','ERIC','ET','EVRG','F','FANG','FAST','FCX','FE','FEYE','FHN','FITB','FLEX','FSLR','FSLY','FTCH','FUTU','GE','GFI','GGB','GILD','GM','GOLD','GPS','GSK','GSX','HAL','HBAN','HBI','HPE','HPQ','HST','HWM','HZNP','IBN','INFO','INFY','ING','INTC','IQ','ITUB','IVZ','JCI','JD','KDP','KEY','KGC','KHC','KMI','KO','KR','KSS','LAZR','LB','LUMN','LUV','LVS','LYFT','LYG','MAT','MDLZ','MET','MGM','MO','MOS','MPC','MPW','MRK','MRO','MRVL','MS','MT','MU','MUFG','NCLH','NEE','NEM','NET','NI','NIO','NKLA','NLOK','NLSN','NLY','NOK','NOV','NTES','NVS','NVTA','OKE','ON','ORCC','ORCL','OXY','PAA','PBCT','PBR','PBR.A','PCG','PE','PENN','PFE','PINS','PLAN','PLUG','PM','PPL','PSTG','PSX','RCL','RDS.A','RDS.B','RF','RP','RTX','RUN','SAN','SCHW','SFIX','SID','SIRI','SJR','SKLZ','SLB','SNAP','SPCE','SPG','STNE','STOR','STWD','STX','SU','T','TAL','TAP','TCOM','TEVA','TFC','TJX','TME','TPR','TRP','TWTR','UAL','UBER','UL','UMC','USB','VALE','VER','VIAC','VIPS','VLO','VOD','VST','VZ','WB','WBA','WDC','WFC','WMB','WORK','XOM','ZNGA','ZTO']
        #symbols = ['AAL']

        self.stream_client = StreamClient(self.client, account_id=secrets.account_id)
        #asyncio.get_event_loop().run_until_complete(self.read_stream())

        self.getHistoricalData(symbols)
        #self.test(symbols)

    def authenticate(self):
        self.client = tda.auth.easy_client(secrets.api_key, 'localhost', secrets.token_path)

    def test(self, symbols):
        for symbol in symbols:
            data = pandas.read_csv(f'historical-data/{symbol}.csv')
            
            data.dropna()

            index = []

            for element in data.loc[:, 'datetime']:
                index.append(pandas.to_datetime(element, unit='ms'))

            data.loc[:, 'datetime'] = index

            data.set_index('datetime', inplace=True)
            #data.drop('Unnamed: 0', axis=1, inplace=True)

            data.to_csv(f'historical-data/{symbol}.csv')
              


    def getHistoricalData(self, symbols):
        for symbol in symbols:
            data = self.client.get_price_history(symbol,
                                                        frequency=Client.PriceHistory.Frequency.EVERY_FIVE_MINUTES,
                                                        frequency_type=Client.PriceHistory.FrequencyType.MINUTE,
                                                        #period=Client.PriceHistory.Period.ONE_YEAR,
                                                        period_type=Client.PriceHistory.PeriodType.DAY,
                                                        start_datetime=datetime.datetime.fromtimestamp(1577836800), #1/1/2020 12am
                                                        end_datetime=datetime.datetime.fromtimestamp(1609459200), #1/1/2021 12am
                                                        need_extended_hours_data=True).json()
            
            csv_file = open(f'historical-data/{symbol}.csv', 'w')
            writer = csv.writer(csv_file)

            if(data['empty'] == True):
                print(f'{symbol} is EMPTY!')
                return

            writer.writerow(data['candles'][0].keys())
            
            for minute in data['candles']:
                writer.writerow(minute.values())

            csv_file.close()

            self.test([symbol])

    async def read_stream(self):
        
        await self.stream_client.login()
        await self.stream_client.level_one_equity_subs(['AMZN', 'AAPL'])
        self.stream_client.add_level_one_equity_handler(lambda msg: self.handler(msg))

        while True:
            await self.stream_client.handle_message()

    def handler(self, data):
        for symbol in data['content']:
            try:
                print(f"{symbol['key']}: {symbol['LAST_PRICE']}")
            except KeyError:
                continue