lista = [1, 2, 3, 4, 5]
indice=[0]*3
for x in range(0,3):
    indice[x] = len(lista) - x
    print(indice)
    print(x)

print(indice)
