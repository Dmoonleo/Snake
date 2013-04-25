import wx
import Snake
import Cell
import random

TIME_INTERVAL = 1

class PaintWindow(wx.Window): 

    snake = Snake.Snake()
    time = 0
    rock_num = 0
    is_drawing = False
    end = False
    test = True
    
    
    def __init__(self, parent, id):  
        wx.Window.__init__(self, parent, id)  
        self.SetBackgroundColour("Black")  
        self.color = "White"  
        
        self.pen = wx.Pen("Solid")
        self.pen.Colour = "White"
        self.pen.SetWidth(2)
        self.brush = wx.Brush("Solid")
        self.brush.Colour = "White"
        
        self.lines = []
        self.curLine = []  
        self.pos = (0, 0)  
        self.InitBuffer()  
        self.timer = wx.Timer(self)
        
        for i in range(0,self.rock_num):
            rockX = random.randint(0, Cell.BOARD_X-1)
            rockY = random.randint(0, Cell.BOARD_Y-1)
            self.snake.rock.append(Cell.Cell(rockX, rockY, 0))
        
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        #self.Bind(wx.EVT_KEY_DOWN, self.begin)
        
        #self.Bind(wx.EVT_PAINT, self.OnPaint) 
           
    #def begin(self, event):
        #keycode = event.GetKeyCode()  
        #if keycode == wx.WXK_SPACE:  
        self.timer.Start(TIME_INTERVAL)      
    
    def InitBuffer(self):  
        if self.is_drawing is not True:
            #print("start drawing")
            self.is_drawing = True
            size = self.GetClientSize()  
            self.buffer = wx.EmptyBitmap(size.width, size.height)  
            dc = wx.BufferedDC(None, self.buffer)
            dc.SetBackground(wx.Brush(self.GetBackgroundColour()))  
            dc.Clear()
            self.pen.Colour = "White"
            self.pen.SetWidth(2)
            dc.SetPen(self.pen)
            
            #for i in range(0, Cell.BOARD_X+2):
            dc.DrawRectangle(0,0,10*(Cell.BOARD_X+2),9)
            dc.DrawRectangle(0,0,9,10*(Cell.BOARD_Y+2))
            dc.DrawRectangle(0,10*(Cell.BOARD_Y+1)+1,10*(Cell.BOARD_X+2),9)
            dc.DrawRectangle(10*(Cell.BOARD_X+1)+1,0,9,10*(Cell.BOARD_Y+2))
                        
            for i,cell in enumerate(self.snake.body):
                dc.DrawRectangle(10*(self.snake.body[i].x+1)+1,10*(self.snake.body[i].y+1)+1,8,8)
            
            i = 0
            while i < len(self.snake.body)-2:
                if self.snake.body[i].d == 0 and self.snake.body[i].d == self.snake.body[i+1].d:
                    dc.DrawRectangle(10*(self.snake.body[i].x+1),10*(self.snake.body[i].y+1)+2,12,6)
                if self.snake.body[i].d == 1 and self.snake.body[i].d == self.snake.body[i+1].d:
                    dc.DrawRectangle(10*(self.snake.body[i].x+1)+2,10*(self.snake.body[i].y+1),6,12)
                if self.snake.body[i].d == 2 and self.snake.body[i].d == self.snake.body[i+1].d:
                    dc.DrawRectangle(10*(self.snake.body[i].x+1),10*(self.snake.body[i].y+1)+2,12,6)
                if self.snake.body[i].d == 3 and self.snake.body[i].d == self.snake.body[i+1].d:
                    dc.DrawRectangle(10*(self.snake.body[i].x+1)+2,10*(self.snake.body[i].y+1),6,12)
                if(i < len(self.snake.body)-3 and (self.snake.body[i].d%4+4 - (self.snake.body[i+2].d+2)%4))%2 == 0:
                    if self.snake.body[i].d == 0 and self.snake.body[i+1].d == 1:
                        dc.DrawRectangle(10*(self.snake.body[i+1].x+1)+2,10*(self.snake.body[i+1].y+1)+2,6,16)
                    if self.snake.body[i].d == 0 and self.snake.body[i+1].d == 3:
                        dc.DrawRectangle(10*(self.snake.body[i+1].x+1)+2,10*(self.snake.body[i+1].y+1)-8,6,16)
                    if self.snake.body[i].d == 1 and self.snake.body[i+1].d == 2:
                        dc.DrawRectangle(10*(self.snake.body[i+1].x+1)-8,10*(self.snake.body[i+1].y+1)+2,16,6)
                    if self.snake.body[i].d == 1 and self.snake.body[i+1].d == 0:
                        dc.DrawRectangle(10*(self.snake.body[i+1].x+1)+2,10*(self.snake.body[i+1].y+1)+2,16,6)
                    if self.snake.body[i].d == 2 and self.snake.body[i+1].d == 1:
                        dc.DrawRectangle(10*(self.snake.body[i+1].x+1)+2,10*(self.snake.body[i+1].y+1)+2,6,16)
                    if self.snake.body[i].d == 2 and self.snake.body[i+1].d == 3:
                        dc.DrawRectangle(10*(self.snake.body[i+1].x+1)+2,10*(self.snake.body[i+1].y+1)-8,6,16)
                    if self.snake.body[i].d == 3 and self.snake.body[i+1].d == 2:
                        dc.DrawRectangle(10*(self.snake.body[i+1].x+1)-8,10*(self.snake.body[i+1].y+1)+2,16,6)
                    if self.snake.body[i].d == 3 and self.snake.body[i+1].d == 0:
                        dc.DrawRectangle(10*(self.snake.body[i+1].x+1)+2,10*(self.snake.body[i+1].y+1)+2,16,6)
                           
                i += 1
                length = len(self.snake.body)-1
                if self.snake.body[length].d == 0:
                    dc.DrawRectangle(10*(self.snake.body[length].x+1)+2,10*(self.snake.body[length].y+1)+2,16,6)
                if self.snake.body[length].d == 1:
                    dc.DrawRectangle(10*(self.snake.body[length].x+1)+2,10*(self.snake.body[length].y+1)+2,6,16)
                if self.snake.body[length].d == 2:
                    dc.DrawRectangle(10*(self.snake.body[length].x+1)-8,10*(self.snake.body[length].y+1)+2,16,6)
                if self.snake.body[length].d == 3:
                    dc.DrawRectangle(10*(self.snake.body[length].x+1)+2,10*(self.snake.body[length].y+1)-8,6,16)
            
            self.brush.SetColour("Blue")
            dc.SetBrush(self.brush)         
            dc.DrawRectangle(10*(self.snake.body[-1].x+1),10*(self.snake.body[-1].y+1),10,10)
            
            self.brush.SetColour("Red")
            dc.SetBrush(self.brush)         
            dc.DrawRectangle(10*(self.snake.body[0].x+1),10*(self.snake.body[0].y+1),10,10)
            
            self.brush.SetColour("White")
            dc.SetBrush(self.brush)          
            if len(self.snake.body) == Cell.BOARD_X*Cell.BOARD_Y:
               dc.SetBrush(wx.TRANSPARENT_BRUSH)
            self.pen.Colour = "Green"
            self.pen.SetWidth(1)
            dc.SetPen(self.pen)        
            dc.DrawCircle(10*(self.snake.fruitX+1)+4,10*(self.snake.fruitY+1)+4,4)
            
            for cell in self.snake.rock:
                self.brush.SetColour("Grey")
                self.pen.Colour = "Yellow"
                self.pen.SetWidth(1)
                dc.SetPen(self.pen)     
                dc.SetBrush(self.brush)         
                dc.DrawRectangle(10*(cell.x+1),10*(cell.y+1),10,10)
            
            #self.Refresh(True)
            self.OnPaint(None)
            self.is_drawing = False
             
    def OnPaint(self, event):
        #print("start painting")
        dc = wx.BufferedPaintDC(self, self.buffer)  
    
    def update(self, event):

            
        if self.is_drawing is not True:
            self.InitBuffer()
        #elif self.time % ((Cell.BOARD_X*Cell.BOARD_Y/20)/TIME_INTERVAL) == 0:        
        #    self.InitBuffer()
        self.snake.next()
        #print("fff")
        #self.time += 1
        if self.snake.notValid() or len(self.snake.body) == Cell.BOARD_X*Cell.BOARD_Y:
            self.is_drawing = False
            self.InitBuffer()
            #self.Refresh(False)
            #self.OnPaint(None)
            #print(str(self.dc))
            self.timer.Stop() 
    
        self.time += 1
              
class PaintFrame(wx.Frame):  
    def __init__(self, parent):  
        wx.Frame.__init__(self, parent, -1, "Snake", size = (Cell.BOARD_X*10+20, Cell.BOARD_Y*10+20))  
        self.paint = PaintWindow(self, -1)  
          
if __name__ == '__main__':  
    app = wx.PySimpleApp()  
    frame = PaintFrame(None)  
    frame.Show(True)  
    app.MainLoop() 