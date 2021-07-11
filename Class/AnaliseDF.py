from os import closerange
import pandas as pd

Dados =''
Padrao=''
Resut =''
DadosPorcent=''


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
    
    def __analiseDFPORCENT__():
        global DadosPorcent
        print(Dados)
        A =(Dados.groupby(['Parabolic,Bollinguer,Fractal,Tendencia,Volume','Resut']).size()/Dados['Resut'].count()*100)
        A = A.groupby(level=0).apply(lambda x:100 * x / float(x.sum()))
        DadosPorcent = A
        print(DadosPorcent)
        
 
    def requestAnalise(self,analise):
        global DadosPorcent
        Analise.__analiseDFPORCENT__()

        
        try:
            Dwin=(DadosPorcent[analise,'WIN'])
        except:
            Dwin=0
        try:
            Dloss=(DadosPorcent[analise,'LOSS'])
        except:
            Dloss=0
    
        print (Dwin)
        
        print(Dwin)
        if(Dwin>Dloss):
            return True
        elif(Dwin<Dloss):
            return False
        elif(Dwin==Dloss):
            return True

'''

    def compute_percentage(x):
        pct = float(x/p['score'].sum()) * 100
        return round(pct, 2)

   # p['percentage'] = p.apply(compute_percentage, axis=1)

'''




