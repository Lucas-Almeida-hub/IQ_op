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

velas = API.get_candles(par, (int(timeframe) * 60), 20,  time.time())

ultimo = round(velas[0]['close'], 4)
primeiro = round(velas[-1]['close'], 4)

diferenca = abs( round( ( (ultimo - primeiro) / primeiro ) * 100, 3) )
tendencia = "CALL" if ultimo < primeiro and diferenca > 0.01 else "PUT" if ultimo > primeiro and diferenca > 0.01 else False
 
print(tendencia)