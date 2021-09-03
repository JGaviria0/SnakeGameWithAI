from random import choices, random, randrange
import time
import os
import blessed


class Enviroment:
    def __init__(self, maxi, maxj):
        self.matriz = [[' '] * maxj for i in range(maxi)] 
        self.maxi = maxi
        self.maxj = maxj

    def canMove(self, i, j):    
        if self.matriz[i][j] == " " or self.matriz[i][j] == "0": 
            return True
        return False  
    
    def newCookie(self, i, j):
        self.matriz[i][j] = "0"

    def moveAllWorm(self, i, j, k, l, queue):
        last = []

        if self.matriz[k][l] != "0":
            last = queue.pop()
            self.matriz[last[0]][last[1]] = " "
        else:
            flag = True
            while flag:
                posCookiei = randrange(1, self.maxi-1)
                posCookiej = randrange(1, self.maxj-1)
                newPos = [posCookiei, posCookiej]
                if not newPos in queue:
                    self.matriz[posCookiei][posCookiej] = "0"
                    break
        
        if len(queue) > 0:
            self.matriz[i][j] = "#"
        self.matriz[k][l] = "@"

        queue.insert(0, [k,l])

        return k, l, queue  
    

    def border(self):
        for i in self.matriz:
            i[0] = "|"
        for i in self.matriz:
            i[self.maxj-1] = "|"
        for i in range(0, self.maxj):
            self.matriz[0][i] = "-"
            self.matriz[self.maxi-1][i] = "-"
        
    def printWorm(self, term):
        for i in self.matriz:
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



class Worm: 
    def __init__(self, i, j):
        self.posi = i
        self.posj = j
        self.tam = 1
        self.movements = [ [1,0], [-1,0], [0, 1], [0,-1] ]
        self.queue = [ [i, j], [i, -j]]
    
    def changeTam(self):
        self.tam += 1
    
    def choiseMove(self):
        self.choicpos = choices(self.movements)
        return self.choicpos[0]



class Cookie:

    def __init__(self, i, j):
        self.posi = i
        self.posj = j
    
    def newCookiePos(self, queue, maxi, maxj):
        if len(queue) < maxi*maxj: 
            while True:
                self.posCookiei = randrange(1, maxi-1)
                self.posCookiej = randrange(1, maxj-1)
                self.newPos = [self.posCookiei, self.posCookiej]
                if not self.newPos in queue:
                    return True, self.newPos
        else:
            return False, [-1,-1]
    

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


def main(): 

    term = blessed.Terminal()

    numero_columnas = term.width
    numero_filas = term.height -1

    posi = numero_filas//2
    posj = numero_columnas//2

    garden = Enviroment(numero_filas, numero_columnas)
    garden.border()
    worm = Worm(posi, posj)
    cookie = Cookie(posi , posj + 5)
    cookiesNew = []

    apples = 1
    while apples > 0:
        apples -=1
        puede, newPos = cookie.newCookiePos(worm.queue, numero_filas, numero_columnas)
        garden.newCookie(newPos[0], newPos[1])

    rep = 0

    with term.hidden_cursor(), term.cbreak(), term.location():
        while True: 
            rep += 1
            if rep > 1000000:
                print("La culebra no puede ir a otro lugar")
                break
            
            move = worm.choiseMove()
            if garden.canMove(worm.posi + move[0], worm.posj + move[1]):
                worm.posi, worm.posj, worm.queue = garden.moveAllWorm(worm.posi, worm.posj, worm.posi+move[0], worm.posj+move[1], worm.queue)
                clearConsole()
                garden.printWorm(term)
                time.sleep(0.1)
         
main()