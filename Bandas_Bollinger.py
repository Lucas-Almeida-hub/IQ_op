from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
from time import time
import sys
 
import numpy as np 
from talib.abstract import *


valor_entrada = 20

def compra(dir):
    
	print('Direção:',dir)
	#logging.info('Direção : {}'.format(dir))
	status,id = API.buy_digital_spot(par, valor_entrada, dir, 1)
	
	if status:
		while True:
			status,valor = API.check_win_digital_v2(id)
			
			if status:
				print('Resultado operação: ', end='')
				print('WIN /' if valor > 0 else 'LOSS /' , round(valor, 2))
				#logging.info('Valor : {}'.format('WIN /' if valor > 0 else 'LOSS /' , round(valor, 2)))
				break					
	else:
		print('\nERRO AO REALIZAR OPERAÇÃO\n\n')

email='lucasalmeidalvs@gmail.com'
senha='lucaslds'
API = IQ_Option(email,senha)

API.connect()

API.change_balance('PRACTICE') # PRACTICE / REAL

if API.check_connect():
	print('\n\nConectado com sucesso')
	
else:
	print('\n Erro ao se conectar')
	sys.exit()

par ='EURUSD'
velas_q = 100
velas= API.get_candles(par,60,velas_q,time())

while True:

    inicio =time()
    velas= API.get_candles(par,60,velas_q,time())

    print(len(velas))

    dados_f ={
        'open': np.empty(velas_q),
        'high': np.empty(velas_q),
        'low' : np.empty(velas_q),
        'close' : np.empty(velas_q),
        'volume' : np.empty(velas_q),
    }
    for x in range (0,velas_q):
        dados_f['open'] [x] = velas[x]['open']
        dados_f['high'] [x] = velas[x]['max']
        dados_f['low'][x] = velas[x]['min']
        dados_f['close'][x] = velas[x]['close']
        dados_f['volume'] [x]= velas[x]['volume']

    up, mid, low = BBANDS(dados_f, timeperiod=5, nbdevup=2.0, nbdevdn=2.0, matype=0)

    up = round(up[len (up)-2],5)
    low = round (low[len(low)-2],5)
    taxa_atual = round(velas[-1]['close'],5)

    if (taxa_atual>= up )or (taxa_atual<=low):
        print("carreagando informaçoes par  compra ")
        if(taxa_atual>=up):
            compra('put')
        else:
            compra('call')






    
