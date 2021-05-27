from collections import deque 

candles=deque()
duplacandles=deque()
finalcandles = ''
iniciocandles = ''

def fractal2 ():
    global iniciocandles
    global finalcandles 
    global candles 
    global duplacandles


    
    duplacandles.append(int(input("Digite qualquer numero : " )))
    
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
        print(candles)
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
            return "Tendencia de reversão para baixo "
        elif(iniciocandles==False)&(finalcandles==False):
            return "Decrecente"
        elif(iniciocandles==False)&(finalcandles==True):
            return "Tendencia de reversão  para cima  "
        elif(iniciocandles==None)&(finalcandles==None):
            return "Sem padrão"

        


while(1):
    print(fractal2())