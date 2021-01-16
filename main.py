from tester import Tester
from backtester import BackTester

algorithm = 'TestAlgorithm'
symbols = ['AAL','ADT','AEG','AES','AGNC','AIG','AMAT','AMD','APA','ATUS','ATVI','AUY','AVTR','AZN','BAC','BBVA','BCS','BHC','BILI','BK','BKR','BLDP','BMY','BNTX','BP','BSX','BTG','C','CARR','CCJ','CCL','CHL','CHWY','CIEN','CLF','CMCSA','CNHI','CNP','CNQ','COG','COP','COTY','CPRI','CSCO','CSX','CTVA','CVE','CVS','CVX','CX','D','DAL','DB','DBX','DD','DDOG','DELL','DHI','DISH','DKNG','DVN','DXC','EBAY','ELAN','ENB','EPD','EQNR','ERIC','ET','EVRG','F','FANG','FAST','FCX','FE','FEYE','FHN','FITB','FLEX','FSLR','FSLY','FTCH','FUTU','GE','GFI','GGB','GILD','GM','GOLD','GPS','GSK','GSX','HAL','HBAN','HBI','HPE','HPQ','HST','HWM','HZNP','IBN','INFO','INFY','ING','INTC','IQ','ITUB','IVZ','JCI','JD','KDP','KEY','KGC','KHC','KMI','KO','KR','KSS','LAZR','LB','LUMN','LUV','LVS','LYFT','LYG','MAT','MDLZ','MET','MGM','MO','MOS','MPC','MPW','MRK','MRO','MRVL','MS','MT','MU','MUFG','NCLH','NEE','NEM','NET','NI','NIO','NKLA','NLOK','NLSN','NLY','NOK','NOV','NTES','NVS','NVTA','OKE','ON','ORCC','ORCL','OXY','PAA','PBCT','PBR','PBR.A','PCG','PE','PENN','PFE','PINS','PLAN','PLUG','PM','PPL','PSTG','PSX','RCL','RDS.A','RDS.B','RF','RP','RTX','RUN','SAN','SCHW','SFIX','SID','SIRI','SJR','SKLZ','SLB','SNAP','SPCE','SPG','STNE','STOR','STWD','STX','SU','T','TAL','TAP','TCOM','TEVA','TFC','TJX','TME','TPR','TRP','TWTR','UAL','UBER','UL','UMC','USB','VALE','VER','VIAC','VIPS','VLO','VOD','VST','VZ','WB','WBA','WDC','WFC','WMB','WORK','XOM','ZNGA','ZTO']
#symbols = ['AAL']

x = BackTester(algorithm, symbols)

x.backtest()
