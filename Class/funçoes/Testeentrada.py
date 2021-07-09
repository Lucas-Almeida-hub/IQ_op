#-Bibliotecas 
from iqoptionapi.stable_api import IQ_Option #Responsavel  site #
import logging #Responsavel pelo deBug
import time#Responsavel por controle de time 
import sys  #Reponsavel por controle do sistema operacional 
import numpy as np #Reponsavel por trabalha com matrix 
from talib.abstract import * #Responsavel por operações financeira 
from datetime import datetime #Responsavel por controle da data 

#-Memorias Globais 

email='lucasalmeidalds@hotmail.com'
senha='lucaslds'
par ='EURUSD'
valor_entrada=20
Vetores = np.zeros( (6, 5) )
vetor=[0]
UtimoId =0
cicloVetor =-1
timeframe = 1
InicieAnalise=False
API=''#Esta variavel vai receber o objeto do iQ
velas_q = 100 #Quantidade de velas analisadas para o metodos de 'Banda de bolliger'


#-Configuração de Debug
nameDate ='IQ_MONEY_{}.log'.format(datetime.today())
logging.basicConfig(filename=nameDate, level=logging.INFO,format='%(asctime)s %(levelname)s %(funcName)s => %(message)s')

#-Funçoes
def loguin():#Responsavel por realizar o loguin o site 
    #email=input("Digite seu email :")
    #senha=input("Digite sua senha ")
    #par =input(' Indique uma paridade para operar: ')
    #valor_entrada =float(input(' Indique um valor para entrar: '))
    global API
    API = IQ_Option(email,senha)

    API.connect()

    API.change_balance('PRACTICE') # PRACTICE / REAL

    if API.check_connect():
        print('\n\nConectado com sucesso')
        
        for x in range (0,5):
            dados_recebidos = API.get_candles(par, 60,20, time.time())
        comven('call')
        
    else:
        print('\n Erro ao se conectar')
        sys.exit()



def comven(dir):#reponsavel por realizar o lance de compra ou venda 
    

    
	print('Direção:',dir)
	logging.info('Direção : {}'.format(dir))
	status,id = API.buy_digital_spot(par, valor_entrada, dir,1)
	
	if status:
		while True:
			status,valor = API.check_win_digital_v2(id)
			
			if status:
				print('Resultado operação: ', end='')
				print('WIN /' if valor > 0 else 'LOSS /' , round(valor, 2))
				logging.info('Valor : {},{}'.format('WIN /' if valor > 0 else 'LOSS /' , round(valor, 2)))
				break					
	else:
		print('\nERRO AO REALIZAR OPERAÇÃO\n\n')


loguin()