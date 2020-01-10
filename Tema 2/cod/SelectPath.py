import sys
import numpy as np


def select_random_path_height(E):
    # pentru linia 0 alegem primul pixel in mod aleator
    col = 0
    line = np.random.randint(low=0, high=E.shape[0], size=1)[0]
    pathway = [(line, col)]
    for i in range(E.shape[1]):
        # alege urmatorul pixel pe baza vecinilor
        col = i
        # coloana depinde de coloana pixelului anterior
        if pathway[-1][0] == 0:  # pixelul este localizat la marginea din stanga
            opt = np.random.randint(low=0, high=2, size=1)[0]
        elif pathway[-1][0] == E.shape[0] - 1:  # pixelul este la marginea din dreapta
            opt = np.random.randint(low=-1, high=1, size=1)[0]
        else:
            opt = np.random.randint(low=-1, high=2, size=1)[0]
        line = pathway[-1][0] + opt
        pathway.append((line, col))
    #print(len(pathway))
    return pathway

def select_random_path_width(E):
    # pentru linia 0 alegem primul pixel in mod aleator
    line = 0
    col = np.random.randint(low=0, high=E.shape[1], size=1)[0]
    pathway = [(line, col)]
    for i in range(E.shape[0]):
        # alege urmatorul pixel pe baza vecinilor
        line = i
        # coloana depinde de coloana pixelului anterior
        if pathway[-1][1] == 0:  # pixelul este localizat la marginea din stanga
            opt = np.random.randint(low=0, high=2, size=1)[0]
        elif pathway[-1][1] == E.shape[1] - 1:  # pixelul este la marginea din dreapta
            opt = np.random.randint(low=-1, high=1, size=1)[0]
        else:
            opt = np.random.randint(low=-1, high=2, size=1)[0]
        col = pathway[-1][1] + opt
        pathway.append((line, col))
    #print(len(pathway))
    return pathway


def select_greedy_path_height(E,first=0):
    if first == 0:
        first=np.where(E[0][:]==min(E[1][:]))[0][0]
    col = 0
    pathway = [(first,col)]
    for i in range(1,E.shape[1]):
        col=i
        if first == 0:
            min1=99999
            min2 = E[first][i]
            min3 = E[first + 1][i]
        else:
            min1=E[first-1][i]
            min2=E[first][i]
            min3=E[first+1][i]
        tempList=[min1,min2,min3]
        aux = np.where(min(min1,min2,min3)==tempList)[0][0]
        if aux ==0:
            first-=1
        if aux == 2:
            first+=1
        pathway.append([first,col])
    #print(pathway)
    return pathway





def select_greedy_path_width(E,first=0):
    if first == 0:
        first=np.where(E[:][0]==min(E[:][0]))[0][0]
    col = 0
    pathway = [(col,first)]
    for i in range(1,E.shape[0]):
        lin=i
        if first == 0:
            min1= 99999
            min2 = E[i,first]
            min3 = E[i,first + 1]
        elif first == E.shape[1]-1:
            min1 = E[i,first - 1]
            min2 = E[i,first]
            min3 = 99999
        else:
            min1=E[i,first-1]
            min2=E[i,first]
            min3=E[i,first+1]
        tempList=[min1,min2,min3]
        aux = np.where(min(min1,min2,min3)==tempList)[0][0]
        if aux ==0:
            first-=1
        if aux == 2:
            first+=1
        pathway.append([lin,first])
    #print(pathway)
    return pathway


def select_dynamic_path_width(E):
    M = np.zeros((E.shape[0], E.shape[1]), np.float32)
    for j in range(E.shape[1] - 1):
        for i in range(E.shape[0]-1):
            M[i][j] = E[i,j] + min(M[i-1,j-1],M[i-1,j],M[i-1,j+1])
    first = np.where(M == M.min())[0][0]
    a = select_greedy_path_width(M,first)
    return a

def select_dynamic_path_height(E):
    M = np.zeros((E.shape[0], E.shape[1]), np.float32)
    for i in range(E.shape[0]-1):
        for j in range(E.shape[1]-1):
            M[i][j] = E[i,j] + min(M[i-1,j-1],M[i,j-1],M[i+1,j-1])
    first = np.where(M == M.min())[0][0]
    a = select_greedy_path_height(M,first)
    return a


def select_path(E, method,option='*'):
    if method == 'aleator' and option == 'width' :
        return select_random_path_width(E)
    if method == 'aleator' and option == 'height':
        return select_random_path_height(E)
    if method == 'greedy' and option == 'height':
        return select_greedy_path_height(E)
    if method == 'greedy' and option == 'width' :
        return select_greedy_path_width(E)
    if method == 'programareDinamica' and option =='width':
        return select_dynamic_path_width(E)
    if method == 'programareDinamica' and option == 'height':
        return select_dynamic_path_height(E)
    else:
        print('The selected method %s is invalid.' % method)
        sys.exit(-1)