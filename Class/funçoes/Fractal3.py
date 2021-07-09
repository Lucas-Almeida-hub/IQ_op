from iqoptionapi.stable_api import IQ_Option
import logging, json, sys, time
from datetime import datetime
import time
from candlestick import candlestick 
import pandas as pd 

email='lucasalmeidalds@hotmail.com'
senha='lucaslds'
par ='EURUSD'
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
4
vetor=API.get_candles(par,5,10,  time.time())

cadles_df= pd.DataFrame.from_dict(vetor)
cadles_df.rename(columns={"max" : "high","min":"low"},inplace=True)

res=candlestick.hammer(cadles_df,target='result')

trabalhando =res.to_dict('records')
for data in trabalhando:
    print(datetime.fromtimestamp(int(data['from'])),data['result'])
    if data['result']==True:
        print(datetime.fromtimestamp(int(data['from'])),data['result'])
