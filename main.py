from random import choices, random, randrange
import time
import os
import blessed


def canMove(matriz, i, j, maxi, maxj):    
    if matriz[i][j] == " " or matriz[i][j] == "0": 
        return True
    return False
    
def newCookie(matriz, i, j):
    if matriz[i][j] == " ":
        return True
    return False

def moveAllWorm(matriz, i, j, k, l, queue):
    
    last = []

    if matriz[k][l] != "0":
        last = queue.pop()
        matriz[last[0]][last[1]] = " "
    else:
        flag = True
        while flag:
            choiceposi = randrange(1,len(matriz)-1)
            choiceposj = randrange(1,len(matriz[0])-1)
            if newCookie(matriz, choiceposi, choiceposj):
                matriz[choiceposi][choiceposj] = "0"
                break

    if matriz[k][l] == "#" or matriz[k][l] == "@":
        return False, matriz, -1, -1, queue
    
    if len(queue) > 0:
        matriz[i][j] = "#"
    matriz[k][l] = "@"

    queue.insert(0, [k,l])

    return True, matriz, k, l, queue

def moveUp(matriz, i, j, maxi, maxj, worm):
    if canMove(matriz, i+1, j, maxi, maxj):
        return moveAllWorm(matriz, i, j, i+1, j, worm)
    else:
        return False, matriz, i, j, worm

def moveDown(matriz, i, j, maxi, maxj, worm):
    if canMove(matriz, i-1, j, maxi, maxj):
        return moveAllWorm(matriz, i, j, i-1, j, worm)
    else:
        return False, matriz, i, j, worm

def moveRight(matriz, i, j, maxi, maxj, worm):
    if canMove(matriz, i, j+1, maxi, maxj):
        return moveAllWorm(matriz, i, j, i, j+1, worm)
    else:
        return False, matriz, i, j, worm

def moveLeft(matriz, i, j, maxi, maxj, worm):
    if canMove(matriz, i, j-1, maxi, maxj):
        return moveAllWorm(matriz, i, j, i, j-1, worm)
    else:
        return False, matriz, i, j, worm
    
def printWorm(matriz):
    term = blessed.Terminal()
    for i in matriz:
        for j in i:
            if j == "#":
                print(term.green_reverse(' '), end="")
            elif j == "@":
                print(term.firebrick1_reverse(' '), end="")
            elif j == "|" or j == "-":
                print(term.cornflowerblue_reverse(' '), end="")
            elif j == "0":
                print(term.darkgoldenrod3_on_gray30('0'), end="")
            else:
                print(term.gray30_reverse(' '), end="")
        print()

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def graficPart(matriz, maxi, maxj):
    for i in matriz:
        i[0] = "|"
    for i in matriz:
        i[maxj-1] = "|"
    for i in range(0, maxj):
        matriz[0][i] = "-"
        matriz[maxi-1][i] = "-"
    
    return matriz

def main(): 
    # numero_columnas = 70
    # numero_filas = 20

    numero_columnas = 30
    numero_filas = 10

    matriz = [[' '] * numero_columnas for i in range(numero_filas)] 
    posi = numero_filas//2
    posj = numero_columnas//2
    lasti = numero_filas//2
    lastj = numero_columnas//2

    matriz[posi][posj] = "#"
    matriz[posi][posj+1] = "0"

    apples = 0
    while apples < 15:
        posCookiei = randrange(1, numero_filas-1)
        posCookiej = randrange(1, numero_columnas-1)
        if newCookie(matriz, posCookiei, posCookiej):
            apples += 1
            matriz[posCookiei][posCookiej] = "0" 
        

    movey = [1, 0, -1, 0]
    movex = [0, 1, 0, -1]
    choic = [0,0]
    choicpos = 0
    worm = []
    worm.append([posi,posj])

    res = True
    matriz = graficPart(matriz, numero_filas, numero_columnas)
    printWorm(matriz)
    rep = 0
    while True: 
        
        choicpos = randrange(0,4,1)

        if rep > 1000000:
            print("La culebra no puede ir a otro lugar")
            break

        rep += 1
        if choicpos == 0: 
            res, matriz, posi, posj, worm = moveUp(matriz, posi, posj, numero_filas, numero_columnas, worm)
            if res == True:
                rep = 0
            
        elif choicpos == 1:
            res, matriz, posi, posj, worm = moveRight(matriz, posi, posj, numero_filas, numero_columnas, worm)
            if res == True:
                rep = 0
            
        elif choicpos == 2:
            res, matriz, posi, posj, worm = moveDown(matriz, posi, posj, numero_filas, numero_columnas, worm)
            if res == True:
                rep = 0
            
        elif choicpos == 3:
            res, matriz, posi, posj, worm = moveLeft(matriz, posi, posj, numero_filas, numero_columnas, worm)
            if res == True:
                rep = 0
            

        if res:
            clearConsole()
            printWorm(matriz)
            time.sleep(0.1)
        elif posi == -1 and posj == -1: 
            print("\n la culebra se choco consigo misma")
            break
         
main()