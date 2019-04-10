import pygame
pygame.init()

def drawGrid(screen, grid_step):
    grid_color = (200,200,200)
    for i in range(0, screen.get_width(), grid_step):
        for j in range(0, screen.get_height(), grid_step):
            pygame.draw.line(screen, grid_color, (i,0), (i, screen.get_height()))
            pygame.draw.line(screen, grid_color, (0,j), (screen.get_width(), j))

def drawSquares(screen, squares, grid_step):
    square_color = (150,150,150)
    for i in range(0, len(squares.xs)):
        for m in range(0, screen.get_width()):
            if squares.xs[i] < m*grid_step:
                rhb = m*grid_step
                lhb = (m-1)*grid_step
                break
        for m in range(0, screen.get_height()):
            if squares.ys[i] < m*grid_step:
                bb = m*grid_step
                tb = (m-1)*grid_step
                break
        pygame.draw.rect(screen, square_color, [lhb,tb,grid_step,grid_step])


class Squares():
    def __init__(self):
        self.xs = []
        self.ys = []
    
    def add(self,pos):
        self.xs.append(pos[0])
        self.ys.append(pos[1])


screen = pygame.display.set_mode((500,500), flags = pygame.RESIZABLE)

pygame.display.set_caption('A-Star Visual')
clock = pygame.time.Clock()
k = False
screen.fill((255,255,255))
grid_width = 20
squares = Squares()
while not k:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            k = True
        print(event)

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
            if event.button == 1:
                squares.add(event.pos)
        if event.type == pygame.MOUSEMOTION:
            if event.buttons[0] == 1:
                squares.add(event.pos)


    screen.fill((255,255,255))
    drawGrid(screen, grid_width)
    drawSquares(screen, squares, grid_width)
    pygame.display.update()

    clock.tick(60)

pygame.quit()
quit()