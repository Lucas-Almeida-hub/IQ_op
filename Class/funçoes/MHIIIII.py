
from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
import logging# Responsavel pelo deBug
import time
import sys

#-Configuração de Debug
logging.basicConfig(filename='myResult.log', level=logging.INFO,format='%(asctime)s %(levelname)s %(funcName)s => %(message)s')
#

API = IQ_Option('lucasalmeidalvs@gmail.com','lucaslds')
API.connect()

API.change_balance('PRACTICE') # PRACTICE / REAL

if API.check_connect():
	print(' Conectado com sucesso!')
else:
	print(' Erro ao conectar')
	input('\n\n Aperte enter para sair')
	sys.exit()

par = input(' Indique uma paridade para operar: ')
valor_entrada = float(input(' Indique um valor para entrar: '))
logging.info('Iniciando EXE')
while True:
	minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
	entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
	print('Hora de entrar?',entrar,'/ Minutos:',minutos)
	


	
	if entrar:
		logging.info('Iniciando operação! ')
		print('\n\nIniciando operação!')
		dir = False
		print('Verificando cores..', end='')
		velas = API.get_candles(par, 60, 3, time.time())
		
		velas[0] = 'g' if velas[0]['open'] < velas[0]['close'] else 'r' if velas[0]['open'] > velas[0]['close'] else 'd'
		velas[1] = 'g' if velas[1]['open'] < velas[1]['close'] else 'r' if velas[1]['open'] > velas[1]['close'] else 'd'
		velas[2] = 'g' if velas[2]['open'] < velas[2]['close'] else 'r' if velas[2]['open'] > velas[2]['close'] else 'd'
		
		cores = velas[0] + ' ' + velas[1] + ' ' + velas[2]		
		print(cores)
	
		if cores.count('g') > cores.count('r') and cores.count('d') == 0 : dir = 'put'
		if cores.count('r') > cores.count('g') and cores.count('d') == 0 : dir = 'call'
		
		
		if dir:
			print('Direção:',dir)
			
			status,id = API.buy_digital_spot(par, valor_entrada, dir, 1)
			
			if status:
				while True:
					status,valor = API.check_win_digital_v2(id)
					
					if status:
						print('Resultado operação: ', end='')
						print('WIN /' if valor > 0 else 'LOSS /' , round(valor, 2))
						logging.info('Valor : {}'.format('WIN /' if valor > 0 else 'LOSS /' , round(valor, 2)))
						break					
			else:
				print('\nERRO AO REALIZAR OPERAÇÃO\n\n')
				
	time.sleep(0.5)