#Desenvolvido :Lucas Almeida
#Data:8/3/21

#-Bibliotecas 
from iqoptionapi.stable_api import IQ_Option #Responsavel  site #
import logging #Responsavel pelo deBug
import time#Responsavel por controle de time 
import sys  #Reponsavel por controle do sistema operacional 
import numpy as np #Reponsavel por trabalha com matrix 
from talib.abstract import * #Responsavel por operações financeira 
from datetime import datetime #Responsavel por controle da data 
from collections import deque #Reponsavel por log 
from Class.AnaliseDF import Analise

#-Memorias Globais 

email='lucasalmeidalds@hotmail.com'
senha='lucaslds'
par ='EURUSD'#'EURUSD'
repra='PRACTICE'
stop_gain=20
stop_loss =50
lucro=0
valor_entrada=20
Vetores = np.zeros( (6, 5) )
vetor=[0]
UtimoId =0
cicloVetor =-1
timeframe = 1
valor_entrada_b=0
martingale=2
operacao = 2
payout = 0
QuantidadeDados=100
payout_stop = 10/100
InicieAnalise=False
candles=deque()
duplacandles=deque()
finalcandles = ''
iniciocandles = ''
Parabolic=''
Bollinguer=''
Fractal=''
Tendencia=''
Volume=''
API=''#Esta variavel vai receber o objeto do iQ
velas_q = 100 #Quantidade de velas analisadas para o metodos de 'Banda de bolliger'

id2=0
cursor=""

#-Configuração de Debug
nameDate ='IQ_MONEY_{}.log'.format(datetime.today())
logging.basicConfig(filename=nameDate, level=logging.INFO,format='%(asctime)s %(levelname)s %(funcName)s => %(message)s')

#-Funçoes
def loguin():#Responsavel por realizar o loguin o site 
    global API
    global email
    global senha
    global par
    
    API = IQ_Option(email,senha)

    API.connect()

    API.change_balance(repra) # PRACTICE / REAL

    if API.check_connect():
        print('\nConectado com sucesso')
        
        
    else:
        print('\n Erro ao se conectar')
        sys.exit()

def comven(dir):#reponsavel por realizar o lance de compra ou venda 
    i=0
    global valor_entrada
    global par
    global payout
    global lucro
    global valor_entrada_b
    global Parabolic
    global Bollinguer
    global Fractal
    global Tendencia
    global Volume

    x=Analise()
    valor_entrada_b=valor_entrada+valor_entrada_b
    print(valor_entrada_b)

    print('Direção:',dir)
    logging.info('Direção : {}'.format(dir))
    status,id = API.buy_digital_spot(par,  valor_entrada_b, dir, 1)
    i=i+1
    if status:
        while True:


            status,valor = API.check_win_digital_v2(id)
            
            if status:
                print('Resultado operação: ', end='')
                print('WIN /' if valor > 0 else 'LOSS /' , round(valor, 2))
                logging.info('Valor : {},{}'.format('WIN /' if valor > 0 else 'LOSS /' , round(valor, 2)))
                lucro+= round(valor, 2)
                if(valor >0):
                    x.loadDF()
                    x.incertDF('{},{},{},{},{}'.format(Parabolic,Bollinguer,Fractal,Tendencia,Volume),'{}'.format('WIN'))
                    x.saveDF()
                    print("fecho win")
                    valor_entrada_b = 0 
                else:
                    x.loadDF()
                    x.incertDF('{},{},{},{},{}'.format(Parabolic,Bollinguer,Fractal,Tendencia,Volume),'{}'.format('LOSS'))
                    x.saveDF()
                    print("Vamos dinovo ")
                    valor_entrada_b = Martingale(valor_entrada, payout)
                    if(payout_stop >payout ):
                        print("Abatido por valor de payout")
 

                stop(lucro, stop_gain, stop_loss)
                       
                break					
        else:
            print('\nERRO AO REALIZAR OPERAÇÃO\n\n')

def fractal(vetor):#Responsavel por realizar a leitura de em modo fractal
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
            #print(InicieAnalise)
            cicloVetor=0
        UtimoId=vetor['id'] 


    trava=0
    if(cicloVetor==0)&(trava==0):
            #print("to aqui-0 ")
            Vetores[0]=[vetor['id'],vetor['open'],vetor['close'],(((vetor['open'])+(vetor['close']))/2),0]
            trava=1
    
    if(cicloVetor==1)&(trava==0): 
            #print("to aqui -1")
            Vetores[1]=[vetor['id'],vetor['open'],vetor['close'],(((vetor['open'])+(vetor['close']))/2),1]
            trava=1

    if(cicloVetor==2)&(trava==0):
            #print("to aqui -2 ")
            Vetores[2]=[vetor['id'],vetor['open'],vetor['close'],(((vetor['open'])+(vetor['close']))/2),2]
            trava=1

    if(cicloVetor==3)&(trava==0):
            #print("to aqui -3 ")
            Vetores[3]=[vetor['id'],vetor['open'],vetor['close'],(((vetor['open'])+(vetor['close']))/2),3]
            trava=1
            


    print(InicieAnalise)
    if(InicieAnalise==True):
        if((Vetores[0][0])<(Vetores[1][0])<(Vetores[2][0])<(Vetores[3][0])):
            print("Ordem de analis  0-1-2-3 ")
            if((Vetores[0][3])>(Vetores[1][3])>(Vetores[2][3])):
                print("Decrecente")
                if((Vetores[2][3]<Vetores[3][3])& (Vetores[1][3]==Vetores[3][3])):
                    print("APOSTA cima !!!!!!!!")
                    #logging.info("A vela de fractal :{}".format(Vetores[3][0])) 
                   # logging.info("Ordem de analis  0-1-2-3")
                   # logging.info('Valores de media :{},{},{}'.format(Vetores[0][3],Vetores[1][3],Vetores[2][3]))
                   # logging.info('Valores de decisão :{} e {}'.format(Vetores[2][3],Vetores[3][3]))
                    return 'call'
                else:
                    print("continuando ")
            elif((Vetores[0][3])<(Vetores[1][3])<(Vetores[2][3])):
                print("Crecrecente")
                if((Vetores[2][3]>Vetores[3][3]) & (Vetores[1][3]==Vetores[3][3])):
                    print("APOSTA baixo !!!!!!!!")
                    #logging.info("A vela de fractal :{}".format(Vetores[3][0])) 
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
                if((Vetores[3][3]<Vetores[0][3])& (Vetores[2][3]==Vetores[0][3])):
                    print("APOSTA cima !!!!!!!!")
                    #logging.info("A vela de fractal :{}".format(Vetores[0][0])) 
                   # logging.info("Ordem de analis é 1-2-3-0 ")
                   # logging.info('Valores de vetores:{},{},{}'.format(Vetores[1][3],Vetores[2][3],Vetores[3][3]))
                   # logging.info('Valores de decisão :{} e {}'.format(Vetores[3][3],Vetores[0][3]))
                    return 'call'
            elif((Vetores[1][3])<(Vetores[2][3])<(Vetores[3][3])):
                print("Crecrecente")
                if((Vetores[3][3]>Vetores[0][3])& (Vetores[2][3]==Vetores[0][3])):
                    print("APOSTA baixo !!!!!!!!")
                    #logging.info("A vela de fractal :{}".format(Vetores[0][0])) 
                   # logging.info("Ordem de analis é 1-2-3-0 ")
                   # logging.info('Valores de vetores:{},{},{}'.format(Vetores[1][3],Vetores[2][3],Vetores[3][3]))
                   # logging.info('Valores de decisão :{} e {}'.format(Vetores[3][3],Vetores[2][3]))
                    return 'put'
            else:
                print("Nao a padrao")
                return 'False'
                
        elif((Vetores[2][0])<(Vetores[3][0])<(Vetores[0][0])<(Vetores[1][0])):
            print("Ordem de analis é 2-3-0-1")
            if((Vetores[2][3])>(Vetores[3][3])>(Vetores[0][3])):
                print("Decrecente")
                if((Vetores[0][3] < Vetores[1][3]) & (Vetores[3][3] == Vetores[1][3])):
                    print("APOSTA cima !!!!!!!!")
                    #logging.info("A vela de fractal :{}".format(Vetores[1][0])) 
                   # logging.info("Ordem de analis é 2-3-0-1")
                   # logging.info('Valores de vetores:{},{},{}'.format(Vetores[2][3],Vetores[3][3],Vetores[0][3]))
                   # logging.info('Valores de decisão :{} e {}'.format(Vetores[0][3],Vetores[1][3]))
                    return 'call'
            elif(((Vetores[2][3])<(Vetores[3][3]))<(Vetores[0][3])):
                print("Crecrecente")
                if((Vetores[0][3] > Vetores[1][3])& (Vetores[3][3] ==Vetores[1][3])):
                    print("APOSTA baixo !!!!!!!!")
                    #logging.info("A vela de fractal :{}".format(Vetores[1][0])) 
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
                if((Vetores[1][3] < Vetores[2][3])& (Vetores[0][3] == Vetores[2][3] )):
                    print("APOSTA cima!!!!!!!!")
                    #logging.info("A vela de fractal :{}".format(Vetores[2][0])) 
                    #logging.info("Ordem de analis é 3-0-1-2")
                    #logging.info('Valores de vetores:{},{},{}'.format(Vetores[3][3],Vetores[0][3],Vetores[1][3]))
                    #logging.info('Valores de decisão :{} e {}'.format(Vetores[1][3],Vetores[2][3]))
                    return 'call'
                else:
                    return 'False'
            elif((Vetores[3][3])<(Vetores[0][3])<(Vetores[1][3])):
                print("Crecrecente")
                
                if((Vetores[1][3] > Vetores[2][3])& (Vetores[0][3] == Vetores[2][3])):
                    print("APOSTA baixo !!!!!!!!")
                   # logging.info("A vela de fractal :{}".format(Vetores[2][0])) 
                   # logging.info("Ordem de analis é 3-0-1-2")
                   # logging.info('Valores de vetores:{},{},{}'.format(Vetores[3][3],Vetores[0][3],Vetores[1][3]))
                   # logging.info('Valores de decisão :{} e {}'.format(Vetores[1][3],Vetores[2][3]))
                    return 'put'
                else:
                    return 'False'
                
            else:
                print("Nao a padrao")
        else:
            print("ERRO")
    else:
        return 'False'


   # print(Vetores[0])
    #print(Vetores[1])
   # print(Vetores[2])
   # print(Vetores[3])

def banda_bollinguer(velas_local):#Responsavel por analisar por meio da Banda de Bollinguer 
        velas_qua=100
        inicio =time.time()
        dados_f ={
            'open': np.empty(velas_qua),
            'high': np.empty(velas_qua),
            'low' : np.empty(velas_qua),
            'close' : np.empty(velas_qua),
            'volume' : np.empty(velas_qua),
        }
        for x in range (0,velas_q):
            dados_f['open'] [x] =  velas_local[x]['open']
            dados_f['high'] [x] =  velas_local[x]['max']
            dados_f['low'][x] =  velas_local[x]['min']
            dados_f['close'][x] =  velas_local[x]['close']
            dados_f['volume'] [x]=  velas_local[x]['volume']

        up, mid, low = BBANDS(dados_f, timeperiod=5, nbdevup=2.0, nbdevdn=2.0, matype=0)
        #up, mid, low = BBANDS(dados_f, timeperiod=17, nbdevup=2.627924, nbdevdn=2.627924, matype=0)

        up = round(up[len (up)-3],5)
        low = round (low[len(low)-3],5)
        taxa_atual = round( velas_local[99]['close'],5)

        if (taxa_atual>= up )or (taxa_atual<=low):
           # print("carreagando informaçoes par  compra ")
            if(taxa_atual>=up):
                #logging.info("A vela de banda é a {}" .format( velas_local[98]['id']))
                return 'put'  
            else:
                #logging.info("A vela de banda é a {}" .format( velas_local[98]['id']))
                return 'call'

def parabolic(vetor1,vetor2,vetor3):#Responsavel por analisar por meio de MHI

    minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
    if ((minutos >= 4.58 and minutos <= 5)or(minutos >= 9.58)):
        entrar = True
    else:
        entrar = False 
  

    if entrar:
        dir = False
        velas=[0]*3
        velas[0] = vetor1
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
            return 'call'
        else:
            return False
    else:
        return False
    time.sleep(0.5)

def tendencia(velas):#Responsavel por analisar por meio da tendencia 
   # print(len(velas))
    ultimo = round(velas[QuantidadeDados-21]['close'], 4)
    primeiro = round(velas[-1]['close'], 4)

    diferenca = abs( round( ( (ultimo - primeiro) / primeiro ) * 100, 3) )
    tendencia = "call" if ultimo < primeiro and diferenca > 0.01 else "put" if ultimo > primeiro and diferenca > 0.01 else False

    return tendencia

def stop(lucro, gain, loss):#Reponsavel por encerrar o sistema 
    print("valor atual de lucro é:{}".format(lucro))
    if lucro <= float('-' + str(abs(loss))):
        print('Stop Loss batido!')
        sys.exit()

    if lucro >= float(abs(gain)):
        print('Stop Gain Batido!')
        sys.exit()

def Martingale(valor, payout):#Reponsavel por reapostar por meio do martingale 
    lucro_esperado = valor * payout
    perca = float(valor)	
		
    while True:
        if round(valor * payout, 2) > round(abs(perca) + lucro_esperado, 2):
            return round(valor, 2)
            break
        valor += 0.01

def Payout(par):#Ler o payout da entrada 
    API.subscribe_strike_list(par, 1)
    while True:
        d = API.get_digital_current_profit(par, 1)
        if d != False:
            d = round(int(d) / 100, 2)
            break
        time.sleep(1)
    API.unsubscribe_strike_list(par, 1)

    return d

def ParametroDeTrabalho():# Resposavel por setar os parametros de trabalho 

    global email
    global senha
    global par 
    global valor_entrada 
    global repra
    global martingale
    global stop_gain
    global stop_loss 
    global payout_stop

    email=input("Digite seu email :")
    senha=input("Digite sua senha ")
    par =input(' Indique uma paridade para operar: ')
    valor_entrada =float(input(' Indique um valor para entrar: '))
    repra=input(' Digite PRACTICE ou REAL:')
    martingale=int(input(' Digite a quantidade de martingale:'))+1
    stop_gain=float(input(' Digite o valor para stop gain:'))
    stop_loss =float(input(' Digite o valor para stop loss:'))
    payout_stop=float(input(' Digite o valor Minimo de Payout '))/100

def fractal2 (vetor):
    global iniciocandles
    global finalcandles 
    global candles 
    global duplacandles
    global UtimoId

    ids = (vetor['id']) #input("digite o id ")
    x= (vetor['close']) #int(input("Digite qualquer numero : " ))
    if(UtimoId != (vetor['id'])):
    #if(UtimoId != ids):
        UtimoId=vetor['id'] 
        duplacandles.append(x)
    if(UtimoId ==(vetor['id'])):
    #if(UtimoId == ids):
        duplacandles[len(duplacandles)-1]=x
  
    print(duplacandles)
    
    if (len(duplacandles)==3):
        if(duplacandles[0]<duplacandles[1])& (duplacandles[1]<duplacandles[2]):
            finalcandles = True   
        elif(duplacandles[0]>duplacandles[1])& (duplacandles[1]>duplacandles[2]):
            finalcandles = False
        else:
            finalcandles = None
       # print("valor da posição 4 :{} 5 :{}".format (duplacandles[1],duplacandles[2]))
        candles.append(duplacandles.popleft())
        #print(candles)
    if(len(candles)==3):
        if(candles[0]<candles[1]) & (candles[1]<candles[2]):
            iniciocandles = True
        elif(candles[0]>candles[1]) & (candles[1]>candles[2]):
            iniciocandles = False
        else:
            finalcandles = None
        
       # print("valor da posição 1:{} 2:{} 3:{}".format (candles [0],candles [1],candles[2]))
        
        candles.popleft()

        # Tru quando a aumento 
        # false quando a decida 
        if(iniciocandles==True)&(finalcandles==True):
            return "Crecente "
        elif(iniciocandles==True)&(finalcandles==False):
            return "call"
        elif(iniciocandles==False)&(finalcandles==False):
            return "Decrecente"
        elif(iniciocandles==False)&(finalcandles==True):
            return "put"
        elif(iniciocandles==None)&(finalcandles==None):
            return "Sem padrão"

def volume(velas_local):
        velas_qua=100
        inicio =time.time()
        dados_f ={
            'open': np.empty(velas_qua),
            'high': np.empty(velas_qua),
            'low' : np.empty(velas_qua),
            'close' : np.empty(velas_qua),
            'volume' : np.empty(velas_qua),
        }
        for x in range (0,velas_q):
            #dados_f['open'] [x] =  velas_local[x]['open']
            #dados_f['high'] [x] =  velas_local[x]['max']
            #dados_f['low'][x] =  velas_local[x]['min']
            dados_f['close'][x] =  velas_local[x]['close']
            dados_f['volume'] [x]=  velas_local[x]['volume']

        #up, mid, low = BBANDS(dados_f, timeperiod=17, nbdevup=2.627924, nbdevdn=2.627924, matype=0)
        real  =  OBV ( dados_f)
        if(real[97]<real[98])& (real[98]<real[99]):
             Vol = 'put'  
        elif(real[97]>real[98])& (real[98]>real[99]):
             Vol = 'call'
        else:
             Vol = None
        return  Vol

def connectBD():
    global cursor 
    con = mysql.connector.connect(host="127.0.0.1", user="root", password="l5c1s32lds", db="IQoption")
    con.select_db('banco de dados')
    cursor = con.cursor()
    return cursor

def Professor (vela,Fractal,bolliguer,tendencia,volume,parabolic):
    
    logging.info("{}-Id vela".format(vela['id']))
    logging.info("{}-Valor da vela".format(vela['close']))
    logging.info("{}-Fractal".format(Fractal))
    logging.info("{}-boliguer".format(bolliguer))
    logging.info("{}-tendencia".format(tendencia))
    logging.info("{}-volume".format(volume))
    logging.info("{}-parabolic".format(parabolic))

def main():# Main

    global payout
    global Parabolic
    global Bollinguer
    global Fractal
    global Tendencia
    global Volume

    tempo =1
    #ParametroDeTrabalho()
    loguin()
    payout=Payout(par)
    Dev =2
    while(Dev==1):#Laços de teste 
        comven('call')
    while(Dev==2):#laços de funcionamento 
        indicesPut=0 
        indicesCall=0
        dados_recebidos = API.get_candles(par, 60*tempo,QuantidadeDados, time.time())
        time.sleep(1)
        Parabolic=parabolic(dados_recebidos[97],dados_recebidos[98], dados_recebidos[99])
        Fractal = fractal(dados_recebidos[-1])
        Bollinguer=banda_bollinguer(dados_recebidos)
        Tendencia = tendencia(dados_recebidos)
        Volume = volume(dados_recebidos)
        valoresDeParabolic=10#50
        valoresDeVolume=10#1
        valoresDeTedencia=10#0
        valoresDeBolliguer=10#1
        ValoresDeFractal=10#50
        if(InicieAnalise==False):
            print("Carregando buffer de analise ")
        if(InicieAnalise==True):
            print("")
            print("Resposta do modole Fractal    : {} ".format(Fractal))
            print("Resposta do modole Bollinguer : {} ".format(Bollinguer))
            print("Resposta do modole Tedencia   : {} ".format(Tendencia))
            print("Resposta do modole Volume     : {} ".format(Volume))
            print("Resposta do modole Parabolic  : {} ".format(Parabolic))
            print("")

            
            if(Parabolic=='call'):
                indicesPut=indicesPut-valoresDeParabolic
                indicesCall=indicesCall+valoresDeParabolic

            elif(Parabolic=='put'):
                indicesPut=indicesPut+valoresDeParabolic
                indicesCall=indicesCall-valoresDeParabolic

            if(Bollinguer=='call'):
                indicesPut=indicesPut-valoresDeBolliguer
                indicesCall=indicesCall+valoresDeBolliguer

            elif(Bollinguer=='put'):
                indicesPut=indicesPut+valoresDeBolliguer
                indicesCall=indicesCall-valoresDeBolliguer

            if(Fractal=='call'):
                indicesPut=indicesPut-ValoresDeFractal
                indicesCall=indicesCall+ValoresDeFractal

            elif(Fractal=='put'):
                indicesPut=indicesPut+ValoresDeFractal
                indicesCall=indicesCall-ValoresDeFractal

            if(Tendencia=='call'):
                indicesPut=indicesPut-valoresDeTedencia
                indicesCall=indicesCall+valoresDeTedencia

            elif(Tendencia=='put'):
                indicesPut=indicesPut+valoresDeTedencia
                indicesCall=indicesCall-valoresDeTedencia

            if(Volume=='call'):
                indicesPut=indicesPut-valoresDeVolume
                indicesCall=indicesCall+valoresDeVolume

            elif(Volume=='put'):
                indicesPut=indicesPut+valoresDeVolume
                indicesCall=indicesCall-valoresDeVolume

            print("Valor porcentual de entrada para Put  é : {}%".format(indicesPut))
            print("Valor porcentual de entrada para call é : {}%".format(indicesCall))
            print("")

            

            if(indicesPut==30):
                Professor(dados_recebidos[-1],Fractal,Bollinguer,Tendencia,Volume,Parabolic)
                comven('put')
                
                
            if(indicesCall==30):
                Professor(dados_recebidos[-1],Fractal,Bollinguer,Tendencia,Volume,Parabolic)
                comven('call')
                

print("Iniciando sistema ")

main()



