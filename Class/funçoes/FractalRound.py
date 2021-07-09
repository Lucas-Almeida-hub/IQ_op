from iqoptionapi.stable_api import IQ_Option
import logging# Responsavel pelo deBug
import time
import sys
import numpy as np # Reposnsavell por trabalha com matrix 
 
#-Configuração de Debug
logging.basicConfig(filename='myFractalResult.log', level=logging.INFO,format='%(asctime)s %(levelname)s %(funcName)s => %(message)s')
#

#logging.disable(level=(logging.DEBUG))
#email=input("Digite seu email :")
#senha=input("Digite sua senha ")
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

par ='EURUSD'# input(' Indique uma paridade para operar: ')
valor_entrada = 20 #float(input(' Indique um valor para entrar: '))



Vetores = np.zeros( (6, 5) )
vetor=[0]


UtimoId =0
cicloVetor =-1
#Vetores=[0]*6
timeframe = 1
InicieAnalise=False


def compra(dir):

	print('Direção:',dir)
	logging.info('Direção : {}'.format(dir))
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


logging.info('Iniciando EXE')
while True:

	vetor=API.get_candles(par, (int(timeframe) * 60),1,  time.time())
	time.sleep(1)
	print('id da vela :{}'.format(vetor[0]['id']))
	print('Valor de abertura : {}'.format(vetor[0]['open']))
	print('Valor de fechamento : {}'.format(vetor[0]['close']))
	print('valor da media entre abertura e fechamento {}'.format(((vetor[0]['open'])+(vetor[0]['close']))/2))
	

	if(UtimoId != (vetor[0]['id'])):
		cicloVetor=cicloVetor+1
		if(cicloVetor>3):
			InicieAnalise=True
			print(InicieAnalise)
			cicloVetor=0
		UtimoId=vetor[0]['id'] 


	trava=0
	if(cicloVetor==0)&(trava==0):
			print("to aqui-0 ")
			Vetores[0]=[vetor[0]['id'],vetor[0]['open'],vetor[0]['close'],(((vetor[0]['open'])+(vetor[0]['close']))/2),0]
			trava=1
				
	if(cicloVetor==1)&(trava==0): 
			print("to aqui -1")
			Vetores[1]=[vetor[0]['id'],vetor[0]['open'],vetor[0]['close'],(((vetor[0]['open'])+(vetor[0]['close']))/2),1]
			trava=1

	if(cicloVetor==2)&(trava==0):
			print("to aqui -2 ")
			Vetores[2]=[vetor[0]['id'],vetor[0]['open'],vetor[0]['close'],(((vetor[0]['open'])+(vetor[0]['close']))/2),2]
			trava=1

	if(cicloVetor==3)&(trava==0):
			print("to aqui -3 ")
			Vetores[3]=[vetor[0]['id'],vetor[0]['open'],vetor[0]['close'],(((vetor[0]['open'])+(vetor[0]['close']))/2),3]
			trava=1


	print(InicieAnalise)
	if(InicieAnalise==True):
		if((Vetores[0][0])<(Vetores[1][0])<(Vetores[2][0])<(Vetores[3][0])):
			print("Ordem de analis  0-1-2-3 ")
			if((Vetores[0][3])>(Vetores[1][3])>(Vetores[2][3])):
				print("Decrecente")
				if((Vetores[2][3]<Vetores[3][3]) & (Vetores[1][3]==Vetores[3][3])):
					print("APOSTA cima !!!!!!!!")
					logging.info("Ordem de analis  0-1-2-3")
					logging.info('Valores de media :{},{},{}'.format(Vetores[0][3],Vetores[1][3],Vetores[2][3]))
					logging.info('Valores de decisão :{} e {}'.format(Vetores[2][3],Vetores[3][3]))
					compra('call')
				else:
					print("continuando ")
			elif((Vetores[0][3])<(Vetores[1][3])<(Vetores[2][3])):
				print("Crecrecente")
				if((Vetores[2][3]>Vetores[3][3]) & (Vetores[1][3]==Vetores[3][3])):
					print("APOSTA baixo !!!!!!!!")
					logging.info("Ordem de analis  0-1-2-3")
					logging.info('Valores de vetores:{},{},{}'.format(Vetores[0][3],Vetores[1][3],Vetores[2][3]))
					logging.info('Valores de decisão :{} e {}'.format(Vetores[2][3],Vetores[3][3]))
					compra('put')
				else:
					print("continuando ")
			else:
				print("Nao a padrao")
				
		elif((Vetores[1][0])<(Vetores[2][0])<(Vetores[3][0])<(Vetores[0][0])):
			print("Ordem de analis é 1-2-3-0 ")
			if((Vetores[1][3])>(Vetores[2][3])>(Vetores[3][3])):
				print("Decrecente")
				if((Vetores[3][3]<Vetores[0][3]) & (Vetores[2][3]==Vetores[0][3])):
					print("APOSTA cima !!!!!!!!")
					logging.info("Ordem de analis é 1-2-3-0 ")
					logging.info('Valores de vetores:{},{},{}'.format(Vetores[1][3],Vetores[2][3],Vetores[3][3]))
					logging.info('Valores de decisão :{} e {}'.format(Vetores[3][3],Vetores[0][3]))
					compra('call')
			elif((Vetores[1][3])<(Vetores[2][3])<(Vetores[3][3])):
				print("Crecrecente")
				if((Vetores[3][3]>Vetores[0][3]) & (Vetores[2][3]==Vetores[0][3])):
					print("APOSTA baixo !!!!!!!!")
					logging.info("Ordem de analis é 1-2-3-0 ")
					logging.info('Valores de vetores:{},{},{}'.format(Vetores[1][3],Vetores[2][3],Vetores[3][3]))
					logging.info('Valores de decisão :{} e {}'.format(Vetores[3][3],Vetores[2][3]))
					compra('put')
			else:
				print("Nao a padrao")
				
		elif((Vetores[2][0])<(Vetores[3][0])<(Vetores[0][0])<(Vetores[1][0])):
			print("Ordem de analis é 2-3-0-1")
			if((Vetores[2][3])>(Vetores[3][3])>(Vetores[0][3])):
				print("Decrecente")
				if((Vetores[0][3] < Vetores[1][3]) & (Vetores[3][3] == Vetores[1][3])):
					print("APOSTA cima !!!!!!!!")
					logging.info("Ordem de analis é 2-3-0-1")
					logging.info('Valores de vetores:{},{},{}'.format(Vetores[2][3],Vetores[3][3],Vetores[0][3]))
					logging.info('Valores de decisão :{} e {}'.format(Vetores[0][3],Vetores[1][3]))
					compra('call')
			elif(((Vetores[2][3])<(Vetores[3][3]))<(Vetores[0][3])):
				print("Crecrecente")
				if((Vetores[0][3] > Vetores[1][3]) & (Vetores[3][3] ==Vetores[1][3])):
					print("APOSTA baixo !!!!!!!!")
					logging.info("Ordem de analis é 2-3-0-1")
					logging.info('Valores de vetores:{},{},{}'.format(Vetores[2][3],Vetores[3][3],Vetores[0][3]))
					logging.info('Valores de decisão :{} e {}'.format(Vetores[0][3],Vetores[1][3]))
					compra('put')
			else:
				print("Nao a padrao")
		elif((Vetores[3][0])<(Vetores[0][0])<(Vetores[1][0])<(Vetores[2][0])):
			print("Ordem de analis é 3-0-1-2")
			if((Vetores[3][3])>(Vetores[0][3])>(Vetores[1][3])):
				print("Decrecente")
				if((Vetores[1][3] < Vetores[2][3]) & (Vetores[0][3] == Vetores[2][3] )):
					print("APOSTA cima!!!!!!!!")
					logging.info("Ordem de analis é 3-0-1-2")
					logging.info('Valores de vetores:{},{},{}'.format(Vetores[3][3],Vetores[0][3],Vetores[1][3]))
					logging.info('Valores de decisão :{} e {}'.format(Vetores[1][3],Vetores[2][3]))
					compra('call')
			elif((Vetores[3][3])<(Vetores[0][3])<(Vetores[1][3])):
				print("Crecrecente")
				if((Vetores[1][3] > Vetores[2][3]) & (Vetores[0][3] == Vetores[2][3])):
					print("APOSTA baixo !!!!!!!!")
					logging.info("Ordem de analis é 3-0-1-2")
					logging.info('Valores de vetores:{},{},{}'.format(Vetores[3][3],Vetores[0][3],Vetores[1][3]))
					logging.info('Valores de decisão :{} e {}'.format(Vetores[1][3],Vetores[2][3]))
					compra('put')
				
			else:
				print("Nao a padrao")
		else:
			print("ERRO")

	print(Vetores[0])
	print(Vetores[1])
	print(Vetores[2])
	print(Vetores[3])



	
          
