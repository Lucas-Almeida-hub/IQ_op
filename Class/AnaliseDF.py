from os import closerange
import pandas as pd

Dados =''
Padrao=''
Resut =''


class Analise:

    def __init__(self):
        
        pass
    
    def __CreatCSV__():
        global Dados
        data = {'Parabolic,Bollinguer,Fractal,Tendencia,Volume':['null,null,null,null,null'], 'Resut':['null']}
        Dados = pd.DataFrame(data)
        Dados.to_csv("Analise.csv")
        

    def loadDF(self):
        global Dados
        try:
            Dados= pd.read_csv("Analise.csv")
            Dados=Dados.drop(columns=['Unnamed: 0'])
        except:
            Analise.__CreatCSV__()
    

    def incertDF(self,info,resut):
        global Dados
        line=[info,resut]
        Dados.loc[len(Dados)]=line
        print(Dados)

    def imprimirDadosDF(self):
        global Dados
        print(Dados)

    def saveDF(self):
        global Dados
        Dados.to_csv("Analise.csv")

    def analiseDf(self):
        global Dados
        A=(Dados.groupby(['Parabolic,Bollinguer,Fractal,Tendencia,Volume','Resut']).size())
        #print(percents_df)
        A.to_csv("AnaliseResult.csv")
        return A
        #Dados.Student.pct_change()
        # size()
    
    def analiseDFPORCENT(self):
        #data = {'a':[2,2,0],'b':[1,0,1],'c':[1,0,0]}
        print(Dados)
        A =(Dados.groupby(['Parabolic,Bollinguer,Fractal,Tendencia,Volume','Resut']).size()/100)
        print(A)
       # A['perc'] = A['Resut']
      #  print(A)









