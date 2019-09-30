import pygame
import math


def drawGrid(screen, grid_step):
    grid_color = (200, 200, 200)

    for i in range(0, screen.get_width(), grid_step):
        for j in range(0, screen.get_height(), grid_step):
            pygame.draw.line(screen, grid_color, (i, 0),
                             (i, screen.get_height()))
            pygame.draw.line(screen, grid_color, (0, j),
                             (screen.get_width(), j))


def drawSquares(screen, squares, grid_step):
    square_color = (150, 150, 150)
    start_color = (10, 210, 10)
    end_color = (200, 10, 10)
    solution_color = (0,0,200)
    for i in range(0, len(squares.xs)):
        if (squares.xs[i]*grid_step) < screen.get_width():
            if (squares.ys[i]*grid_step) < screen.get_height():
                lhb = (squares.xs[i])*grid_step
                tb = (squares.ys[i])*grid_step
                pygame.draw.rect(screen, square_color, [
                                 lhb, tb, grid_step, grid_step])
    if hasattr(squares, 'solution'):
        for i in range(0,len(squares.solution)-1):
            lhb = squares.solution[i][0]*grid_step
            tb = squares.solution[i][1]*grid_step
            pygame.draw.rect(screen, solution_color, [lhb, tb, grid_step, grid_step])
            
    if hasattr(squares, 'start'):
        lhb = squares.start[0]*grid_step
        tb = squares.start[1]*grid_step
        pygame.draw.rect(screen, start_color, [lhb, tb, grid_step, grid_step])

    if hasattr(squares, 'end'):
        lhb = squares.end[0]*grid_step
        tb = squares.end[1]*grid_step
        pygame.draw.rect(screen, end_color, [lhb, tb, grid_step, grid_step])
    



class Node():
    def __init__(self, x, y):
        # print(squares.xs)
        # print(squares.ys)
        
        self.id = (x, y)
        self.x = x
        self.y = y
        self.neighbours = []
        self.costs = []
        self.is_wall = False
        for i in range(0, len(squares.xs)):
            if squares.xs[i] == x and squares.ys[i] == y:
                self.is_wall = True
                break
        if squares.start == self.id:
            self.is_start = True
        else:
            self.is_start = False
        if squares.end == self.id:
            self.is_end = True
        else:
            self.is_end = False
        self.dte = 0

    def ns(self):
        return len(self.neighbours)

    def get_neighbours(self):
        self.neighbours.append(Node(self.x, self.y+1))
        self.costs.append(1)
        self.neighbours.append(Node(self.x+1, self.y+1))
        self.costs.append(math.sqrt(2))
        self.neighbours.append(Node(self.x+1, self.y))
        self.costs.append(1)
        self.neighbours.append(Node(self.x+1, self.y-1))
        self.costs.append(math.sqrt(2))
        self.neighbours.append(Node(self.x, self.y-1))
        self.costs.append(1)
        self.neighbours.append(Node(self.x-1, self.y-1))
        self.costs.append(math.sqrt(2))
        self.neighbours.append(Node(self.x-1, self.y))
        self.costs.append(1)
        self.neighbours.append(Node(self.x-1, self.y+1))
        self.costs.append(math.sqrt(2))

    def set_start(self):
        self.is_start = True
        return self

    def set_end(self):
        self.is_end = True
        return self
    # Calculate the euclidean distance between this node and given (end,usually)

    def get_dte(self, node):
        self.dte = math.sqrt((node.x-self.x)**2 + (node.y-self.y)**2)


class Queue():
    def __init__(self, start_node, end_node):
        self.queue = [[start_node, start_node, 0,
                       start_node.dte, start_node.dte, start_node.id]]
        self.end_node = end_node
        self.start_node = start_node

    def expand(self):
        self.path = []
        while not(self.queue[0][0].is_end):
            # Get info about the expanding node
            self.node = self.queue[0][0]
            self.node_origin = self.queue[0][1]
            self.path_covered = self.queue[0][2]
            # Delete expanding node from list, to reduce backtracking
            self.queue.pop(0)
            self.queue = self.expand_node()
            # Sorting the Queue to expand the best variant next
            self.queue.sort(key=lambda Querry: Querry[4])
            # Add the first element of the Queue to path to later backtrack the shortest path
            self.path.append(self.queue[0])

    def expand_node(self):
        self.node.get_neighbours()
        for i in range(0, self.node.ns()):
            next_node = self.node.neighbours[i]
            next_node.get_dte(self.end_node)
            self.score = next_node.dte + self.path_covered + self.node.costs[i]
            self.adjusted = False
            if next_node.is_end:
                self.queue.append([next_node, self.node, self.path_covered +
                                   self.node.costs[i], next_node.dte, self.score, next_node.id])
                break
            if not(next_node.id == self.node_origin.id) and not(next_node.is_wall):
                self.check_queue(next_node, i)
                if not(self.adjusted):
                    self.queue.append([next_node, self.node, self.path_covered +
                                       self.node.costs[i], next_node.dte, self.score, next_node.id])
        return self.queue

    def check_queue(self, next_node, i):
        for j in range(0, len(self.queue)):
            if (self.queue[j][0].id == next_node.id) and (self.queue[j][2] >= self.path_covered + self.node.costs[i]):
                self.queue[j][1] = self.node
                self.queue[j][2] = self.path_covered + self.node.costs[i]
                self.queue[j][4] = self.path_covered + \
                    self.node.costs[i] + self.queue[j][0].dte
                self.adjusted = True
    
    def get_solution(self):
        index = self.end_node.id
        self.solution = []
        for i in range(len(self.path)-1,-1,-1):
            if self.path[i][0].id == index:
                self.solution.append(index)
                index = self.path[i][1].id
        self.solution.reverse()
        return self.solution

class Squares():
    def __init__(self):
        self.xs = []
        self.ys = []

    def add(self, pos, grid_step):
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
            for i in range(0, len(self.xs)):
                same_x = (self.xs[i]) == (pos[0]//grid_step)
                same_y = (self.ys[i]) == (pos[1]//grid_step)
                if same_x and same_y:
                    such_node = True
                    break
            if not such_node:
                self.xs.append(pos[0]//grid_step)
                self.ys.append(pos[1]//grid_step)

    def remove(self, pos, grid_step):
        if len(self.xs) == 1:
            self.xs.pop(0)
            self.ys.pop(0)
        else:
            for i in range(0, len(self.xs)):
                if (self.xs[i]) is (pos[0]//grid_step):
                    if (self.ys[i]) is (pos[1]//grid_step):
                        self.xs.pop(i)
                        self.ys.pop(i)
                        break

    def add_start(self, pos, grid_step):
        self.start = (pos[0]//grid_step, pos[1]//grid_step)

    def add_end(self, pos, grid_step):
        self.end = (pos[0]//grid_step, pos[1]//grid_step)

    def remove_start(self):
        if hasattr(self, 'start'):
            del self.start

    def remove_end(self):
        if hasattr(self, 'end'):
            del self.end
    
    def add_solution(self,path):
        self.solution = path

class Buttons():
    pass


def main():
    pygame.init()
    menu_color = (200, 200, 250, 128)

    screen = pygame.display.set_mode((500, 500), flags=pygame.RESIZABLE)

    s = pygame.Surface((300, 100), pygame.SRCALPHA)  # the size of your rect
    s.fill(menu_color)           # this fills the entire surface
    screen.blit(s, (0, 0))

    pygame.display.set_caption('A-Star Visual')
    clock = pygame.time.Clock()
    k = False
    screen.fill((255, 255, 255))
    grid_width = 20

    global squares
    squares = Squares()

    start_flag, end_flag, run_flag, not_done = False, False, False, True
    while not k:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                k = True

            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(
                    event.size, flags=pygame.RESIZABLE)

            if event.type == pygame.MOUSEBUTTONDOWN:

                # zoom in
                if event.button == 4:
                    grid_width += 1

                # zoom out
                if event.button == 5:
                    if grid_width <= 1:
                        grid_width = 1
                    else:
                        grid_width -= 1

                # place walls
                if event.button == 1:  # LMB
                    if start_flag:
                        squares.add_start(event.pos, grid_width)
                    elif end_flag:
                        squares.add_end(event.pos, grid_width)
                    else:
                        squares.add(event.pos, grid_width)

                # remove walls
                if event.button == 3:  # RMB
                    if start_flag:
                        squares.remove_start()
                    if end_flag:
                        squares.remove_end()
                    else:
                        squares.remove(event.pos, grid_width)

            if event.type == pygame.MOUSEMOTION:
                if not start_flag and not end_flag:
                    if event.buttons[0] == 1:  # LMB
                        squares.add(event.pos, grid_width)
                    if event.buttons[2] == 1:  # RMB
                        squares.remove(event.pos, grid_width)

            if event.type == pygame.KEYDOWN:
                if event.key == 115:  # s-key down
                    start_flag = True
                if event.key == 101:
                    end_flag = True
                if event.key == 114:  # r-key down
                    run_flag = True

            if event.type == pygame.KEYUP:
                if event.key == 115:  # s-key down
                    start_flag = False
                if event.key == 101:
                    end_flag = False

        screen.fill((255, 255, 255))
        drawGrid(screen, grid_width)
        drawSquares(screen, squares, grid_width)

        if run_flag:
            # if not start_flag or not end_flag:
                # print('No Start or End flag!')
            # else:
            if not_done:
                not_done = False
                print('Start',squares.start)
                print('End',squares.end)
                start_node = Node(squares.start[0], squares.start[1])
                end_node = Node(squares.end[0], squares.end[1])
                start_node.get_dte(end_node)

                Q = Queue(start_node, end_node)
                Q.expand()
                solution = Q.get_solution()
                squares.add_solution(solution)
                print(solution)
            # do smthing
            # Queue = updateQueue(Queue)

        screen.blit(s, (screen.get_width()/2-150, screen.get_height()-100))
        s.fill(menu_color)
        pygame.draw.rect(s, (10, 220, 50), (30, 30, 60, 20))

        pygame.display.update()

        clock.tick(200)

    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
