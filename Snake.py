import Cell
import random
import time


class Snake:
    time = 0
    random_num = 0
    initHead = Cell.Cell()
    body = [initHead]
    vBody = Cell.Cell()
    preTail = Cell.Cell()
    vPreTail = Cell.Cell()
    fruitX = 1
    fruitY = 0
    BFS_FRUIT_PATH = [Cell.Cell(0,0,0)]
    DFS_TAIL_PATH = [Cell.Cell(0,0,0)]
    checkingVTail = False
    max_push_num = 15
    
    rock = []
        
    def head(self):
        return self.body[0]
    
    def tail(self):
        return self.body[-1]
    
    def turnToPoint(self, x, y):
        if x-self.head().x == -1:
            self.body[0].d = 2
        if x-self.head().x == 1:
            self.body[0].d = 0
        if y-self.head().y == 1:
            self.body[0].d = 1
        if y-self.head().y == -1:
            self.body[0].d = 3
    
    def vTurnToPoint(self, x, y):
        if x-self.vBody[0].x == -1:
            self.vBody[0].d = 2
        if x-self.vBody[0].x == 1:
            self.vBody[0].d = 0
        if y-self.vBody[0].y == 1:
            self.vBody[0].d = 1
        if y-self.vBody[0].y == -1:
            self.vBody[0].d = 3
    
    def fruitValid(self):
        for cell in self.body:
            if self.fruitX == cell.x and self.fruitY == cell.y:
                return False
        for cell in self.rock:
            if self.fruitX == cell.x and self.fruitY == cell.y:
                return False
        return True
    
    def turnedNext(self):
        if self.head().nextNode().x is self.fruitX and self.head().nextNode().y is self.fruitY:
            self.expand()
        else:
            self.move()
            
    def vTurnedNext(self):
        if self.vBody[0].nextNode().x is self.fruitX and self.vBody[0].nextNode().y is self.fruitY:
            self.vExpand()
        else:
            self.vMove()
    
    def next(self):
        self.time += 1
        self.turnOrNot()
        if self.head().nextNode().x is self.fruitX and self.head().nextNode().y is self.fruitY:
            self.expand()            
            self.fruitX = random.randint(0, Cell.BOARD_X-1)
            self.fruitY = random.randint(0, Cell.BOARD_Y-1)
            while self.fruitValid() is not True:
                if Cell.BOARD_X*Cell.BOARD_Y != len(self.body):
                    self.fruitX = random.randint(0, Cell.BOARD_X-1)
                    self.fruitY = random.randint(0, Cell.BOARD_Y-1)
                else:
                    self.fruitX = self.head().x
                    self.fruitY = self.head().y
                    break
        else:
            self.move()
        #print("x,y: "+str(self.head().x) +" "+ str(self.head().y)+" "+str(self.head().d))
    
    def expand(self):     
        self.checkingVTail = True   
        self.body.insert(0,self.head().nextNode())
        '''print("head d:"+str(self.body[0].d))'''
        
    def vExpand(self):        
        self.vBody.insert(0,self.vBody[0].nextNode())
    
    def move(self):
        self.preTail.x = self.body[-1].x
        self.preTail.y = self.body[-1].y
        i = len(self.body)-1
        while i > 0:
            if i > 0:
                self.body[i] = self.body[i-1]
            i -= 1
        self.body[0] = self.body[0].nextNode()
        '''print("x,y: "+str(self.head().x)+" "+str(self.head().y))
        print("fruit: "+str(self.fruitX)+" "+str(self.fruitY))'''
     
    def vMove(self):
        self.vPreTail.x = self.vBody[-1].x
        self.vPreTail.y = self.vBody[-1].y
        i = len(self.vBody)-1
        while i > 0:
            if i > 0:
                self.vBody[i] = self.vBody[i-1]
            i -= 1
        self.vBody[0] = self.vBody[0].nextNode()    
    
    def notValid(self):
        for i,cell in enumerate(self.body):
            if self.body[0].equalTo(cell) and i != 0:
                '''print("not valid1")
                print(i)
                print(self.body[0].x)
                print(self.body[0].y)
                print(cell.x)
                print(cell.y)'''
                return True
            if cell.valid() is not True:
                '''print("not valid2")
                print(i)'''
                return True
        return False
    def nextNotValid(self):
        for cell in self.body:
            if self.body[0].nextNode().equalTo(cell):
                return True
        return False
    
    def correctDirection(self, targetX, targetY):
        
        if targetX == self.head().x and targetY > self.head().y:
            return 1
        if targetX == self.head().x and targetY < self.head().y:
            return 3
        if targetX > self.head().x and targetY == self.head().y:
            return 0
        if targetX > self.head().x and targetY == self.head().y:
            return 2
        return -1
    
    def optimalDirection(self, targetX, targetY):
        if (#self.fruitX - self.head().x > self.fruitY - self.head().y and 
            targetX - self.head().x > 0):
            return 0
        if (#self.fruitX - self.head().x < self.fruitY - self.head().y and 
            targetY - self.head().y > 0):
            return 1
        if (#self.fruitX - self.head().x < self.fruitY - self.head().y and 
            targetX - self.head().x < 0):
            return 2
        if (#self.fruitX - self.head().x > self.fruitY - self.head().y and 
            targetY - self.head().y < 0):
            return 3
        return 0
    
    def checkDirection(self, targetX, targetY):
        if self.head().d is 0 and targetX > self.head().x:
            return True
        if self.head().d is 1 and targetY > self.head().y:
            return True
        if self.head().d is 2 and targetX < self.head().x:
            return True
        if self.head().d is 3 and targetY < self.head().y:
            return True
        return False
    
    
    def nodeInBody(self, node):
        for cell in self.body:
            if cell.equalTo(node):
                return True
        return False
    

    def vbfsPathRecal(self, targetX, targetY):
        #self.vBody = list(self.body)
        board = [[0]*Cell.BOARD_Y for x in xrange(Cell.BOARD_X)]
        path = [[[[] for k in xrange(0)] for j in xrange(Cell.BOARD_Y)] for i in xrange(Cell.BOARD_X)]
        for i, bodyCell in enumerate(self.vBody):
            if bodyCell.valid() and i != len(self.vBody)-1:
                board[bodyCell.x][bodyCell.y] = 1
        for rockCell in self.rock:
            board[rockCell.x][rockCell.y] = 1
        #board[self.fruitX][self.fruitY] = 1
        #if len(self.vBody)>=5:
            #for i in range(0,4):
                #print ("vSnake "+str(i)+": "+str(self.vBody[i].x)+" "+str(self.vBody[i].y))
        bfsHead = Cell.Cell(self.vBody[0].x,self.vBody[0].y,self.vBody[0].d)
        queue = [bfsHead]
        while len(queue) != 0:
            cells = []
           
            cells.append(Cell.Cell(queue[0].x-1, queue[0].y,   0))              
            cells.append(Cell.Cell(queue[0].x,   queue[0].y-1, 0))            
            cells.append(Cell.Cell(queue[0].x+1, queue[0].y,   0))              
            cells.append(Cell.Cell(queue[0].x,   queue[0].y+1, 0))
            for cell in cells:
                #print(123)
                if cell.valid():
                    #print(1234)
                    if board[cell.x][cell.y] == 0:
                        #print(12345)
                        #print(str(cell.x)+" "+str(cell.y))
                        board[cell.x][cell.y] = 1
                        path[cell.x][cell.y] = list(path[queue[0].x][queue[0].y])
                        path[cell.x][cell.y].append(cell)
                        queue.append(cell)
                        if cell.x == targetX and cell.y == targetY:
                            #print("test1")
                            #print(len(self.body))
                            #for pathCell in path[targetX][targetY]:
                                #print("path: "+str(pathCell.x)+" "+str(pathCell.y))
                            return path[targetX][targetY]      
            queue.pop(0)
        #print("test3")
        return []
    
    def vbfsPathRecalToTail(self, targetX, targetY):
        #self.vBody = list(self.body)
        board = [[0]*Cell.BOARD_Y for x in xrange(Cell.BOARD_X)]
        path = [[[[] for k in xrange(0)] for j in xrange(Cell.BOARD_Y)] for i in xrange(Cell.BOARD_X)]
        for i, bodyCell in enumerate(self.vBody):
            if bodyCell.valid() and i != len(self.vBody)-1:
                board[bodyCell.x][bodyCell.y] = 1
        for rockCell in self.rock:
            board[rockCell.x][rockCell.y] = 1
        if len(self.body) != Cell.BOARD_X*Cell.BOARD_Y:
            board[self.fruitX][self.fruitY] = 1
        #if len(self.vBody)>=5:
            #for i in range(0,4):
                #print ("vSnake "+str(i)+": "+str(self.vBody[i].x)+" "+str(self.vBody[i].y))
        bfsHead = Cell.Cell(self.vBody[0].x,self.vBody[0].y,self.vBody[0].d)
        queue = [bfsHead]
        while len(queue) != 0:
            cells = []
           
            cells.append(Cell.Cell(queue[0].x-1, queue[0].y,   0))              
            cells.append(Cell.Cell(queue[0].x,   queue[0].y-1, 0))            
            cells.append(Cell.Cell(queue[0].x+1, queue[0].y,   0))              
            cells.append(Cell.Cell(queue[0].x,   queue[0].y+1, 0))
            for cell in cells:
                #print(123)
                if cell.valid():
                    #print(1234)
                    if board[cell.x][cell.y] == 0:
                        #print(12345)
                        #print(str(cell.x)+" "+str(cell.y))
                        board[cell.x][cell.y] = 1
                        path[cell.x][cell.y] = list(path[queue[0].x][queue[0].y])
                        path[cell.x][cell.y].append(cell)
                        queue.append(cell)
                        if cell.x == targetX and cell.y == targetY:
                            #print("test1")
                            #print(len(self.body))
                            #for pathCell in path[targetX][targetY]:
                                #print("path: "+str(pathCell.x)+" "+str(pathCell.y))
                            return path[targetX][targetY]      
            queue.pop(0)
        #print("test3")
        return []
                    
    def bfsPath(self, targetX, targetY):
        if len(self.BFS_FRUIT_PATH) <= 1:
            board = [[0]*Cell.BOARD_Y for x in xrange(Cell.BOARD_X)]
            path = [[[[] for k in xrange(0)] for j in xrange(Cell.BOARD_Y)] for i in xrange(Cell.BOARD_X)]
            #print(path)
            for i, bodyCell in enumerate(self.body):
                if bodyCell.valid() and i != len(self.body)-1:
                    board[bodyCell.x][bodyCell.y] = 1
            for rockCell in self.rock:
                board[rockCell.x][rockCell.y] = 1
            bfsHead = Cell.Cell(self.head().x,self.head().y,self.head().d)
            queue = [bfsHead]
            while len(queue) != 0:
                cells = []
                
                cells.append(Cell.Cell(queue[0].x-1, queue[0].y,   0))              
                cells.append(Cell.Cell(queue[0].x,   queue[0].y-1, 0))            
                cells.append(Cell.Cell(queue[0].x+1, queue[0].y,   0))              
                cells.append(Cell.Cell(queue[0].x,   queue[0].y+1, 0))
                for cell in cells:
                    if cell.valid():
                        if board[cell.x][cell.y] == 0:
                            board[cell.x][cell.y] = 1
                            path[cell.x][cell.y] = list(path[queue[0].x][queue[0].y])
                            path[cell.x][cell.y].append(cell)
                            queue.append(cell)
                            if cell.x == targetX and cell.y == targetY:
                                #print("test1")
                                #print(len(self.body))if len(path) != 0:
                                
                                self.BFS_FRUIT_PATH = path[targetX][targetY]
                                '''for cell in self.BFS_FRUIT_PATH:
                                    print("TrueEatFruit path: "+str(cell.x)+" "+str(cell.y))'''
                                return path[targetX][targetY]      
                queue.pop(0)
            #print("test3")
            return []
        else:
            self.BFS_FRUIT_PATH.pop(0)
            return self.BFS_FRUIT_PATH
    
    #dfsboard = [[0]*Cell.BOARD_Y for x in xrange(Cell.BOARD_X)]
    #dfspath = [[[[] for k in xrange(0)] for j in xrange(Cell.BOARD_Y)] for i in xrange(Cell.BOARD_X)]
    
    pushing_check_board = [[0]*Cell.BOARD_Y for x in xrange(Cell.BOARD_X)]
    
    def dfsHeadTail2(self, currentX, currentY, limit):
        if currentX < 0 or currentY < 0 or currentX >= Cell.BOARD_X or currentY >= Cell.BOARD_Y:
            #print("out of box")
            return 0
        if self.pushing_check_board[currentX][currentY] == 1:
            #print("occupied")
            return 0
        self.pushing_check_board[currentX][currentY] = 1
        result = 1
        dir = [[0]*2 for x in xrange(4)]
        dir[0][0] = 1
        dir[0][1] = 0
        dir[1][0] = 0
        dir[1][1] = 1
        dir[2][0] = -1
        dir[2][1] = 0
        dir[3][0] = 0
        dir[3][1] = -1
        for i in range(0,4):
            temp = self.dfsHeadTail2(currentX + dir[i][0], currentY + dir[i][1], limit - result)
            result = result + temp
            if result > limit:
                return result
        return result
    
    def dfsHeadTail(self):
        self.pushing_check_board = [[0]*Cell.BOARD_Y for x in xrange(Cell.BOARD_X)]
        for i, bodyCell in enumerate(self.body):
            if bodyCell.valid() and i != len(self.body)-1:
                self.pushing_check_board[bodyCell.x][bodyCell.y] = 1
        for rockCell in self.rock:
            self.pushing_check_board[rockCell.x][rockCell.y] = 1
        currentX = self.body[0].x
        currentY = self.body[0].y
        #print(str(currentX) + " " + str(currentY))
        result = 0
        dir = [[0]*2 for x in xrange(4)]
        dir[0][0] = 1
        dir[0][1] = 0
        dir[1][0] = 0
        dir[1][1] = 1
        dir[2][0] = -1
        dir[2][1] = 0
        dir[3][0] = 0
        dir[3][1] = -1
        for i in range(0,4):
            temp = self.dfsHeadTail2(currentX + dir[i][0], currentY + dir[i][1], self.max_push_num - result)
            #print(str(i) + " " + str(temp))
            result = result + temp
            if result > self.max_push_num:
                return result
        return result
        
    longPathBoard = [[0]*Cell.BOARD_Y for x in xrange(Cell.BOARD_X)]
    
    def dfsLongPath(self, targetX, targetY, currentX, currentY):
        if currentX < 0 or currentY < 0 or currentX >= Cell.BOARD_X or currentY >= Cell.BOARD_Y:
            return -1000
        if currentX == targetX and currentY == targetY:
            return 0
        if self.longPathBoard[currentX][currentY] == 1:
            return -1000
        memorize = self.longPathBoard[currentX][currentY]
        dir = [[0]*2 for x in xrange(4)]
        dir[0][0] = 1
        dir[0][1] = 0
        dir[1][0] = 0
        dir[1][1] = 1
        dir[2][0] = -1
        dir[2][1] = 0
        dir[3][0] = 0
        dir[3][1] = -1
        self.longPathBoard[currentX][currentY] = 1;
        temp = -1000
        for i in range(0,4):
            newX = currentX + dir[i][0]
            newY = currentY + dir[i][1]
            ans = self.dfsLongPath(targetX, targetY, newX, newY)
            if ans > -1000 and ans+1 > temp:
                temp = ans+1
        self.longPathBoard[currentX][currentY] = memorize;
        if temp == -1000:
            return temp
        if memorize == 2:
            return temp-1
        elif memorize == 3:
            return temp-2
        else: 
            return temp
    
    def longPathRecal(self, targetX, targetY):
        dir = [[0]*2 for x in xrange(4)]
        dir[0][0] = 1
        dir[0][1] = 0
        dir[1][0] = 0
        dir[1][1] = 1
        dir[2][0] = -1
        dir[2][1] = 0
        dir[3][0] = 0
        dir[3][1] = -1
        self.longPathBoard = [[0]*Cell.BOARD_Y for x in xrange(Cell.BOARD_X)]
        for i, bodyCell in enumerate(self.body):
            if bodyCell.valid():
                self.longPathBoard[bodyCell.x][bodyCell.y] = 1
        for rockCell in self.rock:
            self.longPathBoard[rockCell.x][rockCell.y] = 1
        if len(self.body) != Cell.BOARD_X*Cell.BOARD_Y:
            self.longPathBoard[self.fruitX][self.fruitY] = 3
        self.longPathBoard[self.body[-1].x][self.body[-1].y] = 2
        currentX = self.body[0].x
        currentY = self.body[0].y
        resultX = -1
        resultY = -1
        ans = -1000
        for i in range(0,4):
            temp = self.dfsLongPath(self.body[-2].x, self.body[-2].y, currentX + dir[i][0], currentY+dir[i][1])
            #print(str(i) + " " + str(temp))
            if temp > ans and temp >= -1 and self.longPathBoard[currentX + dir[i][0]][currentY + dir[i][1]] != 1:
                ans = temp;
                resultX = currentX + dir[i][0]
                resultY = currentY + dir[i][1]
        result = [Cell.Cell(resultX, resultY, 0)]
        return result
    
    def dfsPathRecal(self, targetX, targetY):
        dfsboard = [[0]*Cell.BOARD_Y for x in xrange(Cell.BOARD_X)]
        dir = [[0]*2 for x in xrange(4)]
        dir[0][0] = 1
        dir[0][1] = 0
        dir[1][0] = 0
        dir[1][1] = 1
        dir[2][0] = -1
        dir[2][1] = 0
        dir[3][0] = 0
        dir[3][1] = -1
        
        dfspath = [[[[] for k in xrange(0)] for j in xrange(Cell.BOARD_Y)] for i in xrange(Cell.BOARD_X)]
        for i, bodyCell in enumerate(self.body):
            if bodyCell.valid() and i != len(self.body)-1:
                dfsboard[bodyCell.x][bodyCell.y] = 1
        for rockCell in self.rock:
                dfsboard[rockCell.x][rockCell.y] = 1
        if len(self.body) != Cell.BOARD_X*Cell.BOARD_Y:
            dfsboard[self.fruitX][self.fruitY] = 1
        dfsHead = Cell.Cell(self.head().x,self.head().y,self.head().d)
        queue = [dfsHead]
        #start_pushing = False
        
        #if(Cell.BOARD_X*Cell.BOARD_Y - len(self.body) < Cell.BOARD_X*Cell.BOARD_Y/10):
            #start_pushing = True
            #self.random_num = self.head().d
        while len(queue) != 0:        
            cells = []
            
            if self.time % (Cell.BOARD_X*Cell.BOARD_Y/4) == 0 or (Cell.BOARD_X*Cell.BOARD_Y-len(self.body)) < Cell.BOARD_X*Cell.BOARD_Y/15:
                #if start_pushing is not True:
                self.random_num = random.randint(0,100)
                    
            
            for i in range(0,4):
                #if queue[0].x+dir[(self.random_num+i)%4][0] == targetX and queue[0].y+dir[(self.random_num+i)%4][1] == targetY:
                cells.append(Cell.Cell(queue[0].x+dir[(self.random_num+i)%4][0], queue[0].y+dir[(self.random_num+i)%4][1], 0))             
            '''print("queueHead:"+str(queue[0].x)+" "+str(queue[0].y))
            for cell in cells:
                print("queueNeighbour:"+str(cell.x)+" "+str(cell.y))'''
            
            flag = True
            for cell in cells:
                if cell.valid():
                    if dfsboard[cell.x][cell.y] == 0:
                        flag = False
                        dfsboard[cell.x][cell.y] = 1
                        dfspath[cell.x][cell.y] = list(dfspath[queue[0].x][queue[0].y])
                        '''print("target cuole1!!!:"+str(cell.x)+" "+str(cell.y))
                        print("target cuole2!!!:"+str(queue[0].x)+" "+str(queue[0].y))'''
                        dfspath[cell.x][cell.y].append(cell)
                        #if len(dfspath[cell.x][cell.y])>2 and abs(dfspath[cell.x][cell.y][-1].x - dfspath[cell.x][cell.y][-2].x) + abs(dfspath[cell.x][cell.y][-1].y - dfspath[cell.x][cell.y][-2].y) >1:
                        '''print("CUOLE!!!")
                        print("new: "+str(dfspath[cell.x][cell.y][-1].x)+" "+str(dfspath[cell.x][cell.y][-1].y) )
                        print("last: "+str(dfspath[cell.x][cell.y][-2].x)+" "+str(dfspath[cell.x][cell.y][-2].y) )'''
                        queue.insert(0, cell)
                        
                        
                        if cell.x == targetX and cell.y == targetY:
                            '''print("here!")
                            print("dfshhead: "+str(self.head().x)+" "+str(self.head().y))
                            for path_cell in dfspath[targetX][targetY]:
                                print("dfspath: "+str(path_cell.x)+" "+str(path_cell.y))
                            print("pretail target: "+str(self.preTail.x)+" "+str(self.preTail.y))'''
                            return dfspath[targetX][targetY]
                        break
                            
            if flag:                
                queue.pop(0)            
        return []
    
    def dfsPath(self, targetX, targetY):
        if len(self.DFS_TAIL_PATH) <= 1 or self.time % Cell.BOARD_X*Cell.BOARD_Y == 0:
            dfsboard = [[0]*Cell.BOARD_Y for x in xrange(Cell.BOARD_X)]
            dir = [[0]*2 for x in xrange(4)]
            dir[0][0] = 1
            dir[0][1] = 0
            dir[1][0] = 0
            dir[1][1] = 1
            dir[2][0] = -1
            dir[2][1] = 0
            dir[3][0] = 0
            dir[3][1] = -1
            
            dfspath = [[[[] for k in xrange(0)] for j in xrange(Cell.BOARD_Y)] for i in xrange(Cell.BOARD_X)]
            for i, bodyCell in enumerate(self.body):
                if bodyCell.valid() and i != len(self.body)-1:
                    dfsboard[bodyCell.x][bodyCell.y] = 1
            for rockCell in self.rock:
                dfsboard[rockCell.x][rockCell.y] = 1
            if len(self.body) != Cell.BOARD_X*Cell.BOARD_Y:
                dfsboard[self.fruitX][self.fruitY] = 1
            dfsHead = Cell.Cell(self.head().x,self.head().y,self.head().d)
            queue = [dfsHead]
            #start_pushing = False
            
            #if(Cell.BOARD_X*Cell.BOARD_Y - len(self.body) < Cell.BOARD_X*Cell.BOARD_Y/10):
                #start_pushing = True
                #self.random_num = self.head().d
            while len(queue) != 0:        
                cells = []
                
                if self.time % (Cell.BOARD_X*Cell.BOARD_Y/4) == 0 or (Cell.BOARD_X*Cell.BOARD_Y-len(self.body)) < Cell.BOARD_X*Cell.BOARD_Y/15:
                    #if start_pushing is not True:
                    self.random_num = random.randint(0,100)
                        
                
                for i in range(0,4):
                    #if queue[0].x+dir[(self.random_num+i)%4][0] == targetX and queue[0].y+dir[(self.random_num+i)%4][1] == targetY:
                    cells.append(Cell.Cell(queue[0].x+dir[(self.random_num+i)%4][0], queue[0].y+dir[(self.random_num+i)%4][1], 0))             
                '''print("queueHead:"+str(queue[0].x)+" "+str(queue[0].y))
                for cell in cells:
                    print("queueNeighbour:"+str(cell.x)+" "+str(cell.y))'''
                
                flag = True
                for cell in cells:
                    if cell.valid():
                        if dfsboard[cell.x][cell.y] == 0:
                            flag = False
                            dfsboard[cell.x][cell.y] = 1
                            dfspath[cell.x][cell.y] = list(dfspath[queue[0].x][queue[0].y])
                            '''print("target cuole1!!!:"+str(cell.x)+" "+str(cell.y))
                            print("target cuole2!!!:"+str(queue[0].x)+" "+str(queue[0].y))'''
                            dfspath[cell.x][cell.y].append(cell)
                            #if len(dfspath[cell.x][cell.y])>2 and abs(dfspath[cell.x][cell.y][-1].x - dfspath[cell.x][cell.y][-2].x) + abs(dfspath[cell.x][cell.y][-1].y - dfspath[cell.x][cell.y][-2].y) >1:
                            '''print("CUOLE!!!")
                            print("new: "+str(dfspath[cell.x][cell.y][-1].x)+" "+str(dfspath[cell.x][cell.y][-1].y) )
                            print("last: "+str(dfspath[cell.x][cell.y][-2].x)+" "+str(dfspath[cell.x][cell.y][-2].y) )'''
                            queue.insert(0, cell)
                            
                            
                            if cell.x == targetX and cell.y == targetY:
                                '''print("here!")
                                print("dfshhead: "+str(self.head().x)+" "+str(self.head().y))
                                for path_cell in dfspath[targetX][targetY]:
                                    print("dfspath: "+str(path_cell.x)+" "+str(path_cell.y))
                                print("pretail target: "+str(self.preTail.x)+" "+str(self.preTail.y))'''
                                self.DFS_TAIL_PATH = dfspath[targetX][targetY]
                                return dfspath[targetX][targetY]
                            break
                                
                if flag:                
                    queue.pop(0)            
            return []
        else:
            #print("saved")
            self.DFS_TAIL_PATH.pop(0)
            self.DFS_TAIL_PATH.append(Cell.Cell(self.body[-1].x,self.body[-1].y,0))
            return self.DFS_TAIL_PATH
                
                        
    def bfsPathRecalLong(self, targetX, targetY):
        board = [[0]*Cell.BOARD_Y for x in xrange(Cell.BOARD_X)]
        path = [[[[] for k in xrange(0)] for j in xrange(Cell.BOARD_Y)] for i in xrange(Cell.BOARD_X)]
        #print(path)
        for bodyCell in self.body:
            if bodyCell.valid():
                board[bodyCell.x][bodyCell.y] = 1
        for rockCell in self.rock:
            board[rockCell.x][rockCell.y] = 1
        bfsHead = Cell.Cell(self.head().x,self.head().y,self.head().d)
        queue = [bfsHead]
        while len(queue) != 0:
            print("test")
            cells = []
            
            cells.append(Cell.Cell(queue[-1].x-1, queue[-1].y,   0))              
            cells.append(Cell.Cell(queue[-1].x,   queue[-1].y-1, 0))            
            cells.append(Cell.Cell(queue[-1].x+1, queue[-1].y,   0))              
            cells.append(Cell.Cell(queue[-1].x,   queue[-1].y+1, 0))
            flag = True
            for cell in cells:
                if cell.valid():
                    if board[cell.x][cell.y] == 0:
                        flag = False
                        board[cell.x][cell.y] = 1
                        path[cell.x][cell.y] = list(path[queue[-1].x][queue[-1].y])
                        path[cell.x][cell.y].append(cell)
                        queue.append(cell)
                        if cell.x == targetX and cell.y == targetY:
                            return path[targetX][targetY]
            if flag:      
                queue.pop()
        #print("test3")
        return []

    def bfsPathRecal(self, targetX, targetY):
        board = [[0]*Cell.BOARD_Y for x in xrange(Cell.BOARD_X)]
        path = [[[[] for k in xrange(0)] for j in xrange(Cell.BOARD_Y)] for i in xrange(Cell.BOARD_X)]
            #print(path)
        for bodyCell in self.body:
            if bodyCell.valid():
                board[bodyCell.x][bodyCell.y] = 1
        for rockCell in self.rock:
            board[rockCell.x][rockCell.y] = 1
        bfsHead = Cell.Cell(self.head().x,self.head().y,self.head().d)
        queue = [bfsHead]
        while len(queue) != 0:
            cells = []
            
            cells.append(Cell.Cell(queue[0].x-1, queue[0].y,   0))              
            cells.append(Cell.Cell(queue[0].x,   queue[0].y-1, 0))            
            cells.append(Cell.Cell(queue[0].x+1, queue[0].y,   0))              
            cells.append(Cell.Cell(queue[0].x,   queue[0].y+1, 0))
            for cell in cells:
                if cell.valid():
                    if board[cell.x][cell.y] == 0:
                        board[cell.x][cell.y] = 1
                        path[cell.x][cell.y] = list(path[queue[0].x][queue[0].y])
                        path[cell.x][cell.y].append(cell)
                        queue.append(cell)
                        if cell.x == targetX and cell.y == targetY:
                            #print("test1")
                            #print(len(self.body))
                            self.BFS_FRUIT_PATH = path[targetX][targetY]
                            return path[targetX][targetY]      
            queue.pop(0)
        #print("test3")
        return []
    
    def vEatFruit(self):
        #print(111)
        
        self.vBody = list(self.body)
        path = self.vbfsPathRecal(self.fruitX, self.fruitY)
        '''if len(path) != 0:
            for cell in path:
                print("vEatFruit path: "+str(cell.x)+" "+str(cell.y))
            print(" ")'''
        if len(path) == 0:
            return False
        else:
            while len(path) > 0: 
                '''and (self.vBody[0].nextNode().x is not self.fruitX or self.vBody[0].nextNode().y is not self.fruitY):'''
                self.vTurnToPoint(path[0].x, path[0].y)
                path.pop(0)
                if(len(path) != 0):
                    self.vTurnedNext()
                else:
                    self.vExpand()
                #print("vmovement: "+str(self.vBody[0].x)+" "+str(self.vBody[0].y))
                #print ("a")
            #for i, cell in enumerate(self.vBody):
                #print("vSnake "+str(i)+": "+str(cell.x)+" "+str(cell.y))
            #print(112)
            return True
    
    def targetNearTail(self):
        if len(self.body) == 1:
            return self.body[-1]
        else:
            cell = Cell.Cell(self.body[-2].x+1, self.body[-2].y, 0)
            if cell.equalTo(self.body[-1]) is not True and self.nodeInBody(cell) is not True and cell.valid():
                print("targetNearTail: "+str(cell.x)+" "+str(cell.y))
                return cell
            cell = Cell.Cell(self.body[-2].x-1, self.body[-2].y, 2)
            if cell.equalTo(self.body[-1]) is not True and self.nodeInBody(cell) is not True and cell.valid():
                print("targetNearTail: "+str(cell.x)+" "+str(cell.y))
                return cell
            cell = Cell.Cell(self.body[-2].x, self.body[-2].y+1, 1)
            if cell.equalTo(self.body[-1]) is not True and self.nodeInBody(cell) is not True and cell.valid():
                print("targetNearTail: "+str(cell.x)+" "+str(cell.y))
                return cell
            cell = Cell.Cell(self.body[-2].x, self.body[-2].y-1, 3)
            if cell.equalTo(self.body[-1]) is not True and self.nodeInBody(cell) is not True and cell.valid():
                print("targetNearTail: "+str(cell.x)+" "+str(cell.y))
                return cell
        return self.body[-1]
            
    
    def vSnakeCheck(self):
        self.vBody = list(self.body)
        '''print("inside vcheck, body length: "+str(len(self.body)))
        print("before eat head: "+str(self.vBody[0].x)+" "+str(self.vBody[0].y))
        print("before eat tail: "+str(self.vBody[-1].x)+" "+str(self.vBody[-1].y))'''
        flag = self.vEatFruit()
        '''print("inside vcheck, vbody length: "+str(len(self.vBody)))
        print("after eat head: "+str(self.vBody[0].x)+" "+str(self.vBody[0].y))
        print("fruit: "+str(self.fruitX)+" "+str(self.fruitY))
        print("after eat tail: "+str(self.vBody[-1].x)+" "+str(self.vBody[-1].y))
        print("VPreTail: "+str(self.vPreTail.x)+" "+str(self.vPreTail.y))'''
        if flag is not True:
            #print("false1")
            return False
        elif len(self.vbfsPathRecalToTail(self.body[-2].x, self.body[-2].y)) != 0:
            #print("True1")
            '''for i, cell in enumerate(self.vBody):
                print("vbody "+str(i)+": "+str(cell.x)+" "+str(cell.y))'''
            return True
        else:
            #print("preTail: "+str(self.tail().prevNode().x) + " " + str(self.tail().prevNode().y))
            #print("false2")
            return False
    
    def winning(self):
        if Cell.BOARD_X*Cell.BOARD_Y-len(self.body)-len(self.rock) == 1:
            if abs(self.head().x - self.fruitX) + abs(self.head().y - self.fruitY) == 1:
                return True
        return False
    
    def turnOrNot(self):
        #print("before turn: "+str(self.head().d))
        #prevD = self.body[0].d
        
        
        if self.checkingVTail and (self.vSnakeCheck() is not True):
            self.checkingVTail = True
            #print("to tail!")
            #tailPath = self.bfsPathRecal(self.preTail.x, self.preTail.y)
            temp = self.dfsHeadTail()
            #sprint(temp)
            if temp > self.max_push_num:
                '''for i in range(0,4):
                    target = Cell.Cell(self.body[-2].x, self.body[-2].y, i)
                    target = target.nextNode()
                    if (target.x == self.body[-1].x and target.y == self.body[-1].y) is not True:
                        tailPath = self.dfsPathRecal(target.x, target.y)
                        if len(tailPath) != 0:
                            #print("turn target: "+str(target.x)+" "+str(target.y))
                            break
                if len(tailPath) == 0:'''
                tailPath = self.dfsPathRecal(self.body[-1].x, self.body[-1].y)
            else:
                self.DFS_TAIL_PATH = []
                #print("long path!")
                tailPath = self.longPathRecal(0, 0)
                #print("long path finish!")
                #print("long path: "+str(tailPath[0].x)+" "+str(tailPath[0].y))
            '''if len(tailPath) == 0:
                print("head: "+str(self.head().x)+" "+str(self.head().y))
                print("preTail: "+str(self.preTail.x)+" "+str(self.preTail.y))'''
            if len(tailPath) != 0:
                self.turnToPoint(tailPath[0].x, tailPath[0].y)
            elif len(self.body) < Cell.BOARD_X*Cell.BOARD_Y-1:
                print("empty tail path!!")
                #time.sleep(10000)
            '''print("tailpath[0]: "+str(tailPath[0].x)+" "+str(tailPath[0].y))
            print("head next: "+str(self.head().nextNode().x)+" "+str(self.head().nextNode().y))        
            print("intTurn: "+str(self.head().d)+" "+str(tailPath[0].x-self.head().nextNode().x)+" "+str(tailPath[0].y-self.head().nextNode().y))'''
        else:  
            #print("to fruit!")
            self.DFS_TAIL_PATH = []
            self.checkingVTail = False
            path = self.bfsPath(self.fruitX, self.fruitY)          
            self.turnToPoint(path[0].x, path[0].y)
                #print("left")
        if self.winning():
            self.turnToPoint(self.fruitX, self.fruitY)
            
        
            
        
        

        