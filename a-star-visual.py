import pygame

def drawGrid(screen, grid_step):
    grid_color = (200,200,200)

    for i in range(0, screen.get_width(), grid_step):
        for j in range(0, screen.get_height(), grid_step):
            pygame.draw.line(screen, grid_color, (i,0), (i, screen.get_height()))
            pygame.draw.line(screen, grid_color, (0,j), (screen.get_width(), j))


def drawSquares(screen, squares, grid_step):
    square_color = (150,150,150)
    start_color = (10,210,10)
    end_color = (200,10,10)
    for i in range(0, len(squares.xs)):
        if (squares.xs[i]*grid_step) < screen.get_width():
            if (squares.ys[i]*grid_step) < screen.get_height():
                lhb = (squares.xs[i])*grid_step
                tb = (squares.ys[i])*grid_step
                pygame.draw.rect(screen, square_color, [lhb,tb,grid_step,grid_step])
    
    if hasattr(squares,'start'):
        lhb = squares.start[0]*grid_step
        tb = squares.start[1]*grid_step
        pygame.draw.rect(screen, start_color, [lhb,tb,grid_step,grid_step])
  
    if hasattr(squares,'end'):
        lhb = squares.end[0]*grid_step
        tb = squares.end[1]*grid_step
        pygame.draw.rect(screen, end_color, [lhb,tb,grid_step,grid_step])


class Squares():
    def __init__(self):
        self.xs = []
        self.ys = []
    
    def add(self,pos,grid_step):
        such_node = False
        if len(self.xs) == 0:
            self.xs.append(pos[0]//grid_step)
            self.ys.append(pos[1]//grid_step)    
        elif len(self.xs) == 1:
            same_x = (self.xs[0]) == (pos[0]//grid_step)
            same_y = (self.ys[0]) == (pos[1]//grid_step)
            if not same_x or not same_y:
                self.xs.append(pos[0]//grid_step)
                self.ys.append(pos[1]//grid_step)       
        else:    
            for i in range(0,len(self.xs)):
                same_x = (self.xs[i]) == (pos[0]//grid_step)
                same_y = (self.ys[i]) == (pos[1]//grid_step)
                if same_x and same_y:
                    such_node = True
                    break
            if not such_node:
                self.xs.append(pos[0]//grid_step)
                self.ys.append(pos[1]//grid_step)  

    
    def remove(self,pos,grid_step):
        if len(self.xs) == 1:
            self.xs.pop(0)
            self.ys.pop(0)
        else:   
            for i in range(0,len(self.xs)):
                if (self.xs[i]) is (pos[0]//grid_step):
                    if (self.ys[i]) is (pos[1]//grid_step):
                        self.xs.pop(i)
                        self.ys.pop(i)
                        break

    def add_start(self,pos,grid_step):
        self.start = (pos[0]//grid_step,pos[1]//grid_step)
    
    def add_end(self,pos,grid_step):
        self.end = (pos[0]//grid_step,pos[1]//grid_step)

    def remove_start(self):
        if hasattr(self,'start'):
            del self.start
    
    def remove_end(self):
        if hasattr(self,'end'):
            del self.end
        

class Buttons():
    pass    
        
def main():
    pygame.init()
    menu_color = (200,200,250,128)


    screen = pygame.display.set_mode((500,500), flags = pygame.RESIZABLE)

    s = pygame.Surface((300,100),pygame.SRCALPHA)  # the size of your rect
    s.fill(menu_color)           # this fills the entire surface
    screen.blit(s, (0,0))

    pygame.display.set_caption('A-Star Visual')
    clock = pygame.time.Clock()
    k = False
    screen.fill((255,255,255))
    grid_width = 20
    squares = Squares()
    start_flag, end_flag = False, False
    while not k:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                k = True


            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, flags = pygame.RESIZABLE)


            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 4:
                    grid_width += 1

                if event.button == 5:
                    if grid_width <= 1:
                        grid_width = 1
                    else:
                        grid_width -= 1

                if event.button == 1: ## LMB
                    if start_flag:
                        squares.add_start(event.pos,grid_width)
                    elif end_flag:
                        squares.add_end(event.pos,grid_width)
                    else: 
                        squares.add(event.pos,grid_width)

                if event.button == 3: ## RMB
                    if start_flag:
                        squares.remove_start()
                    if end_flag:
                        squares.remove_end()
                    else:
                        squares.remove(event.pos,grid_width)   
                        

            if event.type == pygame.MOUSEMOTION:
                if event.buttons[0] == 1:  ## LMB
                    squares.add(event.pos,grid_width)
                if event.buttons[2] == 1:  ### RMB
                    squares.remove(event.pos,grid_width)
            

            if event.type == pygame.KEYDOWN:
                if event.key == 115: ## s-key down
                    start_flag = True
                if event.key == 101:
                    end_flag = True


            if event.type == pygame.KEYUP:
                if event.key == 115: ## s-key down
                    start_flag = False
                if event.key == 101:
                    end_flag = False
        

        screen.fill((255,255,255))
        drawGrid(screen, grid_width)
        drawSquares(screen, squares, grid_width)

        screen.blit(s, (screen.get_width()/2-150, screen.get_height()-100))
        s.fill(menu_color)
        pygame.draw.rect(s,(10,220,50),(30,30,60,20))

        pygame.display.update()

        clock.tick(200)

    pygame.quit()
    quit()

if __name__ =='__main__':main()