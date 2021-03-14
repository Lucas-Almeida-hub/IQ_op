from iqoptionapi.stable_api import IQ_Option
import logging, json, sys, time
import time

logging.disable(level=(logging.DEBUG))

API = IQ_Option('lucasalmeidalvs@gmail.com', 'lucaslds')

API = IQ_Option('lucasalmeidalvs@gmail.com', 'lucaslds')
API.connect()

API.change_balance('PRACTICE') # PRACTICE / REAL

if API.check_connect():
	print('\n\nConectado com sucesso')
else:
	print('\n Erro ao se conectar')
	sys.exit()
	


par = 'EURUSD'
timeframe = 5

velas = API.get_candles(par, (int(timeframe) * 60),1,  time.time())


fechamento  = round(velas[0]['close'], 4) 
abertura = round(velas[0]['close'], 4) 
atual =

print(tendencia)