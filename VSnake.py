import Snake
import Cell

class VSnake(Snake):
    def VSnake(self, snake):
        self.initHead = Cell.Cell()
        self.body = list(snake.body)
        self.fruitX = snake.fruitX
        self.fruitY = snake.fruitY
        self.BFS_PATH = list(snake.BFS_PATH)
        self.BFS_TAIL_PATH = list(snake.BFS_TAIL_PATH)
    def next(self):
        self.turnOrNot()
        if self.head().nextNode().x is self.fruitX and self.head().nextNode().y is self.fruitY:
            self.expand()
        else:
            self.move()
    def eatFruit(self):
        while self.head().nextNode().x is not self.fruitX or self.head().nextNode().y is not self.fruitY:
            self.next()
        self.expand()
    def sayYES(self):
        self.eatFruit()
        if len(self.bfsPathRecal(self, self.tail().prevNode().x, self.tail().prevNode().y)) == 0:
            return False
        else:
            return True