#
#
#
#


#-Bibliotecas 
from iqoptionapi.stable_api import IQ_Option #Responsavel  site #
import logging #Responsavel pelo deBug
import time#Responsavel por controle de time 
import sys  #Reponsavel por controle do sistema operacional 
import numpy as np #Reponsavel por trabalha com matrix 
from talib.abstract import * #Responsavel por operações financeira 
from datetime import datetime #Responsavel por controle da data 

#-Memorias Globais 

email='lucasalmeidalvs@gmail.com'
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
        
        
    else:
        print('\n Erro ao se conectar')
        sys.exit()

def comven(dir):#reponsavel por realizar o lance de compra ou venda 
    

    
	print('Direção:',dir)
	logging.info('Direção : {}'.format(dir))
	status,id = API.buy_digital_spot(par, valor_entrada, dir, 1)
	
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

def fractal(vetor):
    global Vetores 
    global UtimoId 
    global cicloVetor 
    global timeframe 
    global InicieAnalise
    #print(x['id'])
   # print('id da vela :{}'.format(vetor['id']))
   # print('Valor de abertura : {}'.format(vetor['open']))
   # print('Valor de fechamento : {}'.format(vetor['close']))
   # print('valor da media entre abertura e fechamento {}'.format(((vetor['open'])+(vetor['close']))/2))
    

    if(UtimoId != (vetor['id'])):
        cicloVetor=cicloVetor+1
        if(cicloVetor>3):
            InicieAnalise=True
            print(InicieAnalise)
            cicloVetor=0
        UtimoId=vetor['id'] 


    trava=0
    if(cicloVetor==0)&(trava==0):
          #  print("to aqui-0 ")
            Vetores[0]=[vetor['id'],vetor['open'],vetor['close'],(((vetor['open'])+(vetor['close']))/2),0]
            trava=1
    
    if(cicloVetor==1)&(trava==0): 
         #   print("to aqui -1")
            Vetores[1]=[vetor['id'],vetor['open'],vetor['close'],(((vetor['open'])+(vetor['close']))/2),1]
            trava=1

    if(cicloVetor==2)&(trava==0):
          #  print("to aqui -2 ")
            Vetores[2]=[vetor['id'],vetor['open'],vetor['close'],(((vetor['open'])+(vetor['close']))/2),2]
            trava=1

    if(cicloVetor==3)&(trava==0):
         #   print("to aqui -3 ")
            Vetores[3]=[vetor['id'],vetor['open'],vetor['close'],(((vetor['open'])+(vetor['close']))/2),3]
            trava=1


    print(InicieAnalise)
    if(InicieAnalise==True):
        if((Vetores[0][0])<(Vetores[1][0])<(Vetores[2][0])<(Vetores[3][0])):
            print("Ordem de analis  0-1-2-3 ")
            if((Vetores[0][3])>(Vetores[1][3])>(Vetores[2][3])):
                print("Decrecente")
                if((Vetores[2][3]<Vetores[3][3])):# & (Vetores[1][3]==Vetores[3][3])):
                    print("APOSTA cima !!!!!!!!")
                    logging.info("A vela de fractal :{}".format(Vetores[3][0])) 
                   # logging.info("Ordem de analis  0-1-2-3")
                   # logging.info('Valores de media :{},{},{}'.format(Vetores[0][3],Vetores[1][3],Vetores[2][3]))
                   # logging.info('Valores de decisão :{} e {}'.format(Vetores[2][3],Vetores[3][3]))
                    return 'call'
                else:
                    print("continuando ")
            elif((Vetores[0][3])<(Vetores[1][3])<(Vetores[2][3])):
                print("Crecrecente")
                if((Vetores[2][3]>Vetores[3][3])):# & (Vetores[1][3]==Vetores[3][3])):
                    print("APOSTA baixo !!!!!!!!")
                    logging.info("A vela de fractal :{}".format(Vetores[3][0])) 
                   # logging.info("Ordem de analis  0-1-2-3")
                   # logging.info('Valores de vetores:{},{},{}'.format(Vetores[0][3],Vetores[1][3],Vetores[2][3]))
                   # logging.info('Valores de decisão :{} e {}'.format(Vetores[2][3],Vetores[3][3]))
                    return 'put'
                else:
                    print("continuando ")
            else:
                print("Nao a padrao")
                
        elif((Vetores[1][0])<(Vetores[2][0])<(Vetores[3][0])<(Vetores[0][0])):
            print("Ordem de analis é 1-2-3-0 ")
            if((Vetores[1][3])>(Vetores[2][3])>(Vetores[3][3])):
                print("Decrecente")
                if((Vetores[3][3]<Vetores[0][3])):#& (Vetores[2][3]==Vetores[0][3])):
                    print("APOSTA cima !!!!!!!!")
                    logging.info("A vela de fractal :{}".format(Vetores[0][0])) 
                   # logging.info("Ordem de analis é 1-2-3-0 ")
                   # logging.info('Valores de vetores:{},{},{}'.format(Vetores[1][3],Vetores[2][3],Vetores[3][3]))
                   # logging.info('Valores de decisão :{} e {}'.format(Vetores[3][3],Vetores[0][3]))
                    return 'call'
            elif((Vetores[1][3])<(Vetores[2][3])<(Vetores[3][3])):
                print("Crecrecente")
                if((Vetores[3][3]>Vetores[0][3])):#& (Vetores[2][3]==Vetores[0][3])):
                    print("APOSTA baixo !!!!!!!!")
                    logging.info("A vela de fractal :{}".format(Vetores[0][0])) 
                   # logging.info("Ordem de analis é 1-2-3-0 ")
                   # logging.info('Valores de vetores:{},{},{}'.format(Vetores[1][3],Vetores[2][3],Vetores[3][3]))
                   # logging.info('Valores de decisão :{} e {}'.format(Vetores[3][3],Vetores[2][3]))
                    return 'put'
            else:
                print("Nao a padrao")
                
        elif((Vetores[2][0])<(Vetores[3][0])<(Vetores[0][0])<(Vetores[1][0])):
            print("Ordem de analis é 2-3-0-1")
            if((Vetores[2][3])>(Vetores[3][3])>(Vetores[0][3])):
                print("Decrecente")
                if((Vetores[0][3] < Vetores[1][3])):# & (Vetores[3][3] == Vetores[1][3])):
                    print("APOSTA cima !!!!!!!!")
                    logging.info("A vela de fractal :{}".format(Vetores[1][0])) 
                   # logging.info("Ordem de analis é 2-3-0-1")
                   # logging.info('Valores de vetores:{},{},{}'.format(Vetores[2][3],Vetores[3][3],Vetores[0][3]))
                   # logging.info('Valores de decisão :{} e {}'.format(Vetores[0][3],Vetores[1][3]))
                    return 'call'
            elif(((Vetores[2][3])<(Vetores[3][3]))<(Vetores[0][3])):
                print("Crecrecente")
                if((Vetores[0][3] > Vetores[1][3])):#& (Vetores[3][3] ==Vetores[1][3])):
                    print("APOSTA baixo !!!!!!!!")
                    logging.info("A vela de fractal :{}".format(Vetores[1][0])) 
                   # logging.info("Ordem de analis é 2-3-0-1")
                   # logging.info('Valores de vetores:{},{},{}'.format(Vetores[2][3],Vetores[3][3],Vetores[0][3]))
                   # logging.info('Valores de decisão :{} e {}'.format(Vetores[0][3],Vetores[1][3]))
                    return 'put'
            else:
                print("Nao a padrao")
        elif((Vetores[3][0])<(Vetores[0][0])<(Vetores[1][0])<(Vetores[2][0])):
            print("Ordem de analis é 3-0-1-2")
            if((Vetores[3][3])>(Vetores[0][3])>(Vetores[1][3])):
                print("Decrecente")
                if((Vetores[1][3] < Vetores[2][3])):#& (Vetores[0][3] == Vetores[2][3] )):
                    print("APOSTA cima!!!!!!!!")
                    logging.info("A vela de fractal :{}".format(Vetores[2][0])) 
                    #logging.info("Ordem de analis é 3-0-1-2")
                    #logging.info('Valores de vetores:{},{},{}'.format(Vetores[3][3],Vetores[0][3],Vetores[1][3]))
                    #logging.info('Valores de decisão :{} e {}'.format(Vetores[1][3],Vetores[2][3]))
                    return 'call'
            elif((Vetores[3][3])<(Vetores[0][3])<(Vetores[1][3])):
                print("Crecrecente")
                if((Vetores[1][3] > Vetores[2][3])):#& (Vetores[0][3] == Vetores[2][3])):
                    print("APOSTA baixo !!!!!!!!")
                    logging.info("A vela de fractal :{}".format(Vetores[2][0])) 
                   # logging.info("Ordem de analis é 3-0-1-2")
                   # logging.info('Valores de vetores:{},{},{}'.format(Vetores[3][3],Vetores[0][3],Vetores[1][3]))
                   # logging.info('Valores de decisão :{} e {}'.format(Vetores[1][3],Vetores[2][3]))
                    return 'put'
                
            else:
                print("Nao a padrao")
        else:
            print("ERRO")

   # print(Vetores[0])
    #print(Vetores[1])
   # print(Vetores[2])
   # print(Vetores[3])




def banda_bollinguer(velas):

    
        inicio =time.time()
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

        up, mid, low = BBANDS(dados_f, timeperiod=17, nbdevup=2.627924, nbdevdn=2.627924, matype=0)

        up = round(up[len (up)-3],5)
        low = round (low[len(low)-3],5)
        taxa_atual = round(velas[98]['close'],5)

        if (taxa_atual>= up )or (taxa_atual<=low):
           # print("carreagando informaçoes par  compra ")
            if(taxa_atual>=up):
                logging.info("A vela de banda é a {}" .format(velas[98]['id']))
                return 'put'  
            else:
                logging.info("A vela de banda é a {}" .format(velas[98]['id']))
                return 'call'

def mhi(vetor1,vetor2,vetor3):

    minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
    if ((minutos >= 4.58 and minutos <= 5)or(minutos >= 9.58)):
        entrar = True
    else:
        entrar = False 
    print('Hora de entrar? {} / Minutos: {} '.format(entrar,minutos))

    if entrar:
        print('\n\nIniciando operação!')
        dir = False
        print('Verificando cores..', end='')
        velas=[0]*3
        velas[0] = vetor1#  API.get_candles(par, 60, 3, time.time())
        velas[1] = vetor2
        velas[2] = vetor3

        velas[0] = 'g' if velas[0]['open'] < velas[0]['close'] else 'r' if velas[0]['open'] > velas[0]['close'] else 'd'
        velas[1] = 'g' if velas[1]['open'] < velas[1]['close'] else 'r' if velas[1]['open'] > velas[1]['close'] else 'd'
        velas[2] = 'g' if velas[2]['open'] < velas[2]['close'] else 'r' if velas[2]['open'] > velas[2]['close'] else 'd'

        cores = velas[0] + ' ' + velas[1] + ' ' + velas[2]		
        print(cores)

        if cores.count('g') > cores.count('r') and cores.count('d') == 0 :
            return 'put'
        if cores.count('r') > cores.count('g') and cores.count('d') == 0 : 
            logging.info("Modelo : MHI | direcao : Call")
            return 'call'
    time.sleep(0.5)

def tendencia(velas):
    ultimo = round(velas[89]['close'], 4)
    primeiro = round(velas[-1]['close'], 4)

    diferenca = abs( round( ( (ultimo - primeiro) / primeiro ) * 100, 3) )
    tendencia = "call" if ultimo < primeiro and diferenca > 0.01 else "put" if ultimo > primeiro and diferenca > 0.01 else False

    return tendencia

def stop(lucro, gain, loss):
    if lucro <= float('-' + str(abs(loss))):
        print('Stop Loss batido!')
        sys.exit()

    if lucro >= float(abs(gain)):
        print('Stop Gain Batido!')
        sys.exit()

#Teste 


loguin()
logging.info("INICIANDO EXE")
while True:
    dados_recebidos = API.get_candles(par, 60,100, time.time())
    time.sleep(1)

    ##indice=[0]*3
    # for x in range(0,3):
       # indice[x] =len(dados_recebidos)- x
    #print(mhi(dados_recebidos[indice[0]-1],dados_recebidos[indice[1]-1],dados_recebidos[indice[2]-1]))
    #print(fractal(dados_recebidos[-1]))
    bollinguer=banda_bollinguer(dados_recebidos)
    Fractal = fractal(dados_recebidos[-1])
    Tendencia = tendencia(dados_recebidos)
    valoresDeTedencia=10
    valoresDeBolliguer=10
    ValoresDeFractal=60
    indicesPut=0
    indicesCall=0
    print("Resposta do modole Fractal : {} ".format(Fractal))
    print("Resposta do modole Bollinguer : {} ".format(bollinguer))
    print("Resposta do modole Tedencia : {} ".format(Tendencia))
    if(bollinguer=='call'):
        indicesPut=indicesPut-valoresDeBolliguer
        indicesCall=indicesCall+valoresDeBolliguer
        logging.info("Modelo :Banda Bollinguer | direcao : call")
       # comven('call')

    if(bollinguer=='put'):
        indicesPut=indicesPut+valoresDeBolliguer
        indicesCall=indicesCall-valoresDeBolliguer
        logging.info("Modelo :Banda Bollinguer | direcao : Put")
       # comven('put')

    if(Fractal=='call'):
        indicesPut=indicesPut-ValoresDeFractal
        indicesCall=indicesCall+ValoresDeFractal
        logging.info("Modelo :Fractal | direcao : call")
       # comven('call')

    if(Fractal=='put'):
        indicesPut=indicesPut+ValoresDeFractal
        indicesCall=indicesCall-ValoresDeFractal
        logging.info("Modelo :Fractal | direcao : Put")
        #comven('put')

    if(Tendencia=='call'):
       # indicesPut=indicesPut-valoresDeTedencia
       # indicesCall=indicesCall+valoresDeTedencia
        logging.info("Modelo :Tedencia | direcao : call")
       # comven('call')

    if(Tendencia=='put'):
       # indicesPut=indicesPut+valoresDeTedencia
       # indicesCall=indicesCall-valoresDeTedencia
        logging.info("Modelo :Tedencia | direcao : Put")
        #comven('put')  

    print("valor porcentual de entrada para Put é : {}%".format(indicesPut))
    print("valor porcentual de entrada para call é : {}%".format(indicesCall))



    if(indicesPut>=50):
        logging.info("valor porcentual de entrada para Put é : {}%".format(indicesPut))
        comven('put')
        
    if(indicesCall>=50):
        logging.info("valor porcentual de entrada para call é : {}%".format(indicesCall))
        comven('call')
    
'''
   # if(bollinguer=='call') and (Fractal=='call'):
        logging.info("Modelo :Banda Bollinguer & Fractal | direcao : call")
        comven('call')

    #if(bollinguer=='put') and (Fractal=='put'):
        logging.info("Modelo :Banda Bollinguer & Fractal | direcao : Put")
        comven('put')
'''



