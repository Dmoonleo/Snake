BOARD_X = 15
BOARD_Y = 15

class Cell:
    def __init__(self,x=0,y=0,d=0):
        self.x = x
        self.y = y
        self.d = d
        
    def valid(self):
        if self.x >=0 and self.y >= 0 and self.x < BOARD_X and self.y < BOARD_Y:
            return True
        else:
            return False
    
    def equalTo(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False
    
    def nextNode(self):
        cell = Cell(self.x,self.y,self.d)
        if cell.d == 0:
            cell.x += 1
        elif cell.d == 1:
            cell.y += 1
        elif cell.d == 2:
            cell.x -= 1
        elif cell.d == 3:
            cell.y -= 1
        return cell
    
