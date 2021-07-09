from iqoptionapi.stable_api import IQ_Option
import logging, json, sys, time
import time

email='lucasalmeidalds@hotmail.com'
senha='lucaslds'
par ='EURUSD-OTC'
repra='PRACTICE'
API=''

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

loguin()
par = 'EURUSD-OTC'
timeframe = 5
while(1):
    velas = API.get_candles(par, (int(timeframe) * 60), 20 ,  time.time())

    ultimo = round(velas[0]['close'], 4)
    primeiro = round(velas[-1]['close'], 4)

    diferenca = abs( round( ( (ultimo - primeiro) / primeiro ) * 100, 3) )
    tendencia = "CALL" if ultimo < primeiro and diferenca > 0.01 else "PUT" if ultimo > primeiro and diferenca > 0.01 else False

    print(tendencia)